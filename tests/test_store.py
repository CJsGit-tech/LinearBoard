import base64
import json
import tempfile
import unittest
from pathlib import Path
from linearboard.store import Store, Invalid, Conflict
from linearboard.contracts import capabilities

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'test.sqlite3'
        self.s = Store(self.path)
        self.team = self.s.snapshot()['teams'][0]
        self.p = self.create('projects', name='Disposable QA', team_id=self.team['id'])
        self.m = self.create('milestones', name='M1', project_id=self.p['id'])

    def tearDown(self):
        self.tmp.cleanup()

    def create(self, kind, **data):
        return self.s.mutate(kind, data)

    def issue(self, category='FrontEnd', **data):
        return self.create('issues', title='Test outcome', category=category, project_id=self.p['id'], milestone_id=self.m['id'], **data)

    def update(self, kind, r, **data):
        return self.s.mutate(kind, {'expected_version': r['version'], **data}, r['id'])

    def test_vision_milestones_frd_are_native_documents(self):
        for t in ['Vision', 'Milestones', 'FRD']:
            d=self.create('documents',title=t,body='# Rule\n- One',doc_type=t,project_id=self.p['id'])
            self.assertEqual(self.s.get('documents', d['id'])['project_id'], self.p['id'])
        self.assertEqual(self.s.get('milestones',self.m['id'])['project_id'],self.p['id'])

    def test_story_prd_design_and_fe_be_traceability(self):
        story=self.issue('UserStory',body='## Story\nOutcome\n## Acceptance\nObservable')
        prd=self.issue('ProductRequirement'); design=self.issue('Design')
        self.assertEqual(design['status'],'Todo')
        for issue in [prd,design,self.issue('FrontEnd'),self.issue('BackEnd')]:
            rel=self.create('relations',source_id=issue['id'],target_id=story['id'],relation='related')
            self.assertEqual(rel['project_id'],self.p['id'])
            self.assertTrue(issue['identifier'].startswith('LB-'))
            self.assertEqual(issue['milestone_id'],self.m['id'])
        labels=self.s.snapshot()['labels']
        group=next(l for l in labels if l['name']=='Category')
        self.assertTrue(group['single_select'])
        children=[l for l in labels if l.get('parent_id')==group['id']]
        self.assertEqual(len(children),5)
        with self.assertRaises(Invalid):
            self.update('issues',story,label_ids=[children[0]['id'],children[1]['id']])

    def test_multistory_labels_and_category_change(self):
        labels=[self.create('labels',name=n,team_id=self.team['id']) for n in ['M1','US1','US2','Coder']]
        r=self.issue(label_ids=[l['id'] for l in labels])
        updated=self.update('issues',r,category='BackEnd')
        self.assertTrue(all(l['id'] in updated['label_ids'] for l in labels))
        self.assertEqual(len(updated['label_ids']),5)

    def test_prd_demystify_keeps_original_qa_and_revisions(self):
        prd=self.issue('ProductRequirement',body='Original rule')
        qa=self.create('documents',title='M1-工能釐清QA紀錄',body='Original answer: defer',project_id=self.p['id'])
        self.update('issues',prd,body='Confirmed rule')
        self.update('documents',qa,body=qa['body']+'\nFinal decision: confirmed')
        self.assertEqual(self.s.history(prd['id'])[0]['before_data']['body'],'Original rule')
        self.assertIn('Original answer',self.s.get('documents',qa['id'])['body'])

    def test_design_documents_visual_versions_and_user_approval(self):
        for title in ['設計總覽','畫面與互動規格']:
            self.create('documents',title=title,project_id=self.p['id'])
        design=self.issue('Design')
        a=self.create('attachments',target_kind='issues',target_id=design['id'],name='screen-v1.png',content_base64=base64.b64encode(b'\x89PNG\r\n\x1a\nQA').decode(),mime='image/png',screen='issues',visual_version='v1')
        self.assertEqual(a['approval'],'draft')
        with self.assertRaises(Invalid):
            self.update('attachments',a,approval='approved')
        a=self.s.mutate('attachments',{'expected_version':a['version'],'approval':'approved'},a['id'],actor='user')
        self.assertEqual(self.s.blob(a['id'])[1],b'\x89PNG\r\n\x1a\nQA')
        self.assertEqual(a['approval'],'approved')

    def test_saved_views_exact_category_project_all_milestones_statuses(self):
        expected=[self.issue('FrontEnd')]
        m2=self.create('milestones',name='M2',project_id=self.p['id'])
        second=self.create('issues',title='M2 task',category='FrontEnd',status='In Review',project_id=self.p['id'],milestone_id=m2['id']);expected.append(second)
        self.issue('BackEnd')
        other=self.create('projects',name='Other',team_id=self.team['id'])
        self.create('issues',title='Other project',project_id=other['id'])
        view=self.create('views',name='QA-FE',project_id=self.p['id'],category='FrontEnd',placement='tabs')
        self.assertEqual({i['id'] for i in self.s.view_members(view['id'])},{i['id'] for i in expected})
        self.assertEqual(view['group_by'],'status')
        self.assertEqual(view['placement'],'tabs')

    def test_views_do_not_truncate_at_list_page_boundary(self):
        for i in range(205): self.issue()
        view=self.create('views',name='All FE',project_id=self.p['id'],category='FrontEnd')
        self.assertEqual(len(self.s.view_members(view['id'])),205)
        page=self.s.list('issues',limit=100)
        self.assertEqual(page['next_cursor'],100)
        self.assertEqual(len(self.s.list('issues',cursor=200,limit=100)['items']),5)

    def test_batch_organize_snapshot_and_no_invalid_categories(self):
        fe,be=self.issue(),self.issue('BackEnd')
        b=self.create('batches',name='Batch 1',project_id=self.p['id'],milestone_id=self.m['id'],issue_ids=[fe['id'],be['id']],checkpoint='Observable end-to-end result')
        self.assertEqual(b['issue_ids'],[fe['id'],be['id']])
        story=self.issue('UserStory')
        with self.assertRaises(Invalid):
            self.update('batches',b,issue_ids=[story['id']])

    def test_dispatch_no_duplicate_max_three_review_plan_report(self):
        issues=[self.issue() for _ in range(4)]
        ds=[self.create('dispatches',project_id=self.p['id'],issue_ids=[i['id']],worker='QA') for i in issues[:3]]
        with self.assertRaises(Conflict):
            self.create('dispatches',project_id=self.p['id'],issue_ids=[issues[0]['id']])
        with self.assertRaises(Invalid):
            self.create('dispatches',project_id=self.p['id'],issue_ids=[issues[3]['id']])
        with self.assertRaises(Invalid):
            self.update('dispatches',ds[0],state='executing')
        d=self.update('dispatches',ds[0],state='executing',plan='Reviewed scoped plan')
        with self.assertRaises(Invalid):
            self.update('dispatches',d,state='completed')
        d=self.update('dispatches',d,state='completed',report='Delivered; external checks required')
        self.assertEqual(d['state'],'completed')

    def test_dispatch_excludes_in_review_done_and_canceled(self):
        for status in ['In Review','Canceled']:
            i=self.issue(status=status)
            with self.assertRaises(Invalid): self.create('dispatches',project_id=self.p['id'],issue_ids=[i['id']])

    def test_debug_log_fix_document_result_comment_and_evidence(self):
        bugs=self.create('documents',title='QA-M1-Bugs',project_id=self.p['id'],body='Datetime: supplied time\nUser Report:\n- Original report')
        fix=self.issue(body='Source report: '+bugs['id'])
        evidence=self.create('evidence',project_id=self.p['id'],issue_id=fix['id'],criterion='Reproduction',result='Not tested',environment='Local QA')
        c=self.create('comments',target_kind='documents',target_id=bugs['id'],body='Result: '+fix['id'])
        self.assertEqual(c['target_id'],bugs['id'])
        self.assertEqual(self.s.get('documents',bugs['id'])['body'],bugs['body'])
        self.assertEqual(evidence['result'],'Not tested')

    def test_sync_idempotency_conflicts_and_preserved_done(self):
        data={'title':'Same operation','project_id':self.p['id']}
        first=self.s.mutate('issues',data,key='same-operation')
        second=self.s.mutate('issues',data,key='same-operation')
        self.assertEqual(first,second)
        with self.assertRaises(Conflict): self.s.mutate('issues',{**data,'title':'Different'},key='same-operation')
        updated=self.update('issues',first,body='Changed')
        with self.assertRaises(Conflict): self.update('issues',first,body='Stale')
        with self.assertRaises(Invalid): self.update('issues',updated,status='Done')
        done=self.s.mutate('issues',{'expected_version':updated['version'],'status':'Done'},updated['id'],actor='user')
        changed=self.update('issues',done,body='Reconciled metadata')
        self.assertEqual(changed['status'],'Done')

    def test_dependency_cycles_and_cross_project_relations_rejected(self):
        a,b,c=self.issue(),self.issue(),self.issue()
        self.create('relations',source_id=a['id'],target_id=b['id'],relation='blocks')
        self.create('relations',source_id=b['id'],target_id=c['id'],relation='blocks')
        with self.assertRaises(Invalid): self.create('relations',source_id=c['id'],target_id=a['id'],relation='blocks')
        other=self.create('projects',name='Other',team_id=self.team['id'])
        issue=self.create('issues',title='Other',project_id=other['id'])
        with self.assertRaises(Invalid): self.create('relations',source_id=a['id'],target_id=issue['id'],relation='related')

    def test_restart_trash_restore_and_blob_persistence(self):
        i=self.issue(body='Persistent content')
        a=self.create('attachments',target_kind='issues',target_id=i['id'],name='proof.txt',content_base64=base64.b64encode(b'proof').decode())
        impact=self.s.trash_impact('issues',i['id'])
        deleted=self.s.trash_move('issues',i['id'],impact['fingerprint'])
        self.s=Store(self.path)
        self.assertEqual(self.s.list('issues')['total'],0)
        self.s.trash_restore(deleted['batch_id'])
        self.assertEqual(self.s.get('issues',i['id'])['body'],'Persistent content')
        self.assertEqual(self.s.blob(a['id'])[1],b'proof')
        restored=self.s.get('issues',i['id'])
        self.assertEqual(restored['identifier'],i['identifier'])
        self.assertEqual(len(self.s.history(i['id'])),3)

    def test_all_main_command_contracts_and_aliases(self):
        c=capabilities()
        self.assertEqual(len(c['commands']),16)
        self.assertFalse(c['unchanged_linear_tpm_compatible'])
        self.assertEqual(c['aliases']['prd'],'create-PRDs')

if __name__ == '__main__': unittest.main()
