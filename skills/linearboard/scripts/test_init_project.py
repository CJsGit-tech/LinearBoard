import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest

SCRIPT = Path(__file__).with_name('init_project.py')
SPEC = importlib.util.spec_from_file_location('linearboard_init', SCRIPT)
init = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(init)


class InitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def plan(self, project='Fixture Gym'):
        return init.plan_setup(project, self.repo)

    def apply(self, plan=None):
        plan = plan or self.plan()
        return init.apply_setup(plan, plan['plan_sha256'])

    def put(self, path, content):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        return target

    def files(self):
        return {p.relative_to(self.repo).as_posix(): p.read_bytes() for p in self.repo.rglob('*') if p.is_file()}

    def test_dry_run_has_no_side_effects(self):
        plan = self.plan()
        self.assertEqual(self.files(), {})
        self.assertEqual(len(plan['agent_roster']), 8)
        self.assertFalse(init.public_report(plan)['applied'])

    def test_fresh_apply_generates_parseable_seven_agents(self):
        written = self.apply()
        self.assertEqual(len(written), 9)
        self.assertEqual(set(self.files()), set(written))
        roles = [tomllib.loads(p.read_text()) for p in (self.repo / '.codex/agents').glob('*.toml')]
        self.assertEqual(len({r['name'] for r in roles}), 7)
        self.assertTrue(all(r['developer_instructions'] and r['description'] for r in roles))
        self.assertTrue(all('model' not in r and 'sandbox_mode' not in r for r in roles))

    def test_generated_reviewer_owns_evidence_based_status_updates(self):
        self.apply()
        role = self.repo / '.codex/agents/delivery_reviewer.toml'
        instructions = tomllib.loads(role.read_text())['developer_instructions']
        self.assertIn('move verified work to Done through the native UI', instructions)
        self.assertIn('blocked by a test restriction to Todo', instructions)
        self.assertIn('read back status', instructions)
        self.assertNotIn('Never mark Done', instructions)
        self.assertNotIn('Do not edit source or board records', instructions)

    def test_repeat_leaves_all_bytes_and_mtimes_unchanged(self):
        self.apply()
        before = self.files()
        times = {p: (self.repo / p).stat().st_mtime_ns for p in before}
        self.assertEqual(self.apply(), [])
        self.assertEqual(self.files(), before)
        self.assertEqual({p: (self.repo / p).stat().st_mtime_ns for p in before}, times)

    def test_crlf_manual_instructions_are_preserved_and_repeat_is_safe(self):
        old = b'# Existing rules\r\nKeep this exact text.\r\n'
        (self.repo / 'AGENTS.md').write_bytes(old)
        self.apply()
        current = (self.repo / 'AGENTS.md').read_bytes()
        self.assertTrue(current.startswith(old))
        self.assertEqual(self.apply(), [])
        self.assertEqual((self.repo / 'AGENTS.md').read_bytes(), current)

    def test_manual_agents_text_and_existing_config_preserved(self):
        self.put('AGENTS.md', '# Existing app\nOnly owner may publish.\n')
        config = '# manual\nmodel = "custom-model"\n[agents]\nenabled = true\nmax_concurrent_threads_per_session = 1\n'
        self.put('.codex/config.toml', config)
        self.apply()
        self.assertTrue((self.repo / 'AGENTS.md').read_text().startswith('# Existing app\nOnly owner may publish.\n'))
        self.assertEqual((self.repo / '.codex/config.toml').read_text(), config)

    def test_missing_agents_table_added_without_losing_other_config(self):
        old = '# Keep this\nmodel = "chosen"\n[features]\nshell_tool = true\n'
        self.put('.codex/config.toml', old)
        self.apply()
        value = (self.repo / '.codex/config.toml').read_text()
        self.assertTrue(value.startswith(old))
        self.assertEqual(tomllib.loads(value)['agents']['max_concurrent_threads_per_session'], 3)
        self.assertNotIn('enabled', tomllib.loads(value)['agents'])

    def test_custom_role_reused_by_name_not_filename(self):
        original = 'name = "repo_explorer"\ndescription = "My explorer"\nmodel = "my-model"\ndeveloper_instructions = "Preserve this instruction."\n'
        self.put('.codex/agents/my-custom-explorer.toml', original)
        plan = self.plan()
        self.apply(plan)
        self.assertEqual((self.repo / '.codex/agents/my-custom-explorer.toml').read_text(), original)
        self.assertFalse((self.repo / '.codex/agents/repo_explorer.toml').exists())
        self.assertTrue(any('repo_explorer unchanged' in w for w in plan['warnings']))

    def test_generated_role_updates_preserve_model_and_manual_suffix(self):
        self.apply()
        p = self.repo / '.codex/agents/repo_explorer.toml'
        text = p.read_text().replace('Read applicable AGENTS.md', 'Old generated guidance')
        text += '\n# local choice\nmodel = "my-model"\n'
        p.write_text(text)
        self.apply()
        current = p.read_text()
        self.assertIn('Read applicable AGENTS.md', current)
        self.assertTrue(current.endswith('\n# local choice\nmodel = "my-model"\n'))

    def test_disabled_agents_are_not_force_enabled(self):
        original = '[agents]\nenabled = false\n'
        self.put('.codex/config.toml', original)
        plan = self.plan()
        self.apply(plan)
        self.assertEqual((self.repo / '.codex/config.toml').read_text(), original)
        self.assertTrue(any('explicitly disabled' in w for w in plan['warnings']))

    def test_extra_agent_is_preserved_and_reported_without_invented_commands(self):
        self.put('.codex/agents/custom.toml', 'name="custom"\ndescription="Custom role"\ndeveloper_instructions="Keep"\n')
        plan = self.plan()
        self.apply(plan)
        self.assertEqual(plan['extra_agents'][0]['name'], 'custom')
        self.assertIn('Not declared', plan['extra_agents'][0]['commands'][0])

    def test_duplicate_names_and_filename_collision_block_before_writes(self):
        role = 'name="other"\ndescription="Other"\ndeveloper_instructions="Keep"\n'
        self.put('.codex/agents/frontend_delivery.toml', role)
        before = self.files()
        with self.assertRaises(init.SetupError):
            self.plan()
        self.assertEqual(self.files(), before)
        self.put('.codex/agents/second.toml', role)
        with self.assertRaises(init.SetupError):
            self.plan()

    def test_invalid_toml_blocks_before_any_write(self):
        self.put('.codex/config.toml', '[agents\nenabled=')
        before = self.files()
        with self.assertRaises(init.SetupError):
            self.plan()
        self.assertEqual(self.files(), before)

    def test_ambiguous_markers_and_project_rebinding_block(self):
        self.put('AGENTS.md', init.BEGIN + '\nunfinished')
        with self.assertRaises(init.SetupError):
            self.plan()
        (self.repo / 'AGENTS.md').unlink()
        self.apply()
        before = self.files()
        with self.assertRaises(init.SetupError):
            self.plan('Other project')
        self.assertEqual(self.files(), before)

    def test_stale_plan_preserves_concurrent_manual_edit(self):
        plan = self.plan()
        self.put('AGENTS.md', 'Concurrent instruction\n')
        with self.assertRaises(init.SetupError):
            self.apply(plan)
        self.assertEqual(self.files(), {'AGENTS.md': b'Concurrent instruction\n'})

    def test_cli_expected_plan_rejects_changed_snapshot(self):
        old_hash = self.plan()['plan_sha256']
        self.put('AGENTS.md', 'New instruction')
        result = subprocess.run([sys.executable, str(SCRIPT), '--project', 'Fixture Gym', '--repo', str(self.repo), '--apply', '--expect-plan', old_hash], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.repo / '.codex').exists())

    def test_symlinked_config_never_writes_outside_target(self):
        with tempfile.TemporaryDirectory() as external:
            (self.repo / '.codex').symlink_to(external, target_is_directory=True)
            with self.assertRaises(init.SetupError):
                self.plan()
            self.assertEqual(list(Path(external).iterdir()), [])

    def test_cli_apply_and_display_roster_format(self):
        args = [sys.executable, str(SCRIPT), '--project', 'Fixture Gym', '--repo', str(self.repo)]
        dry = subprocess.run(args + ['--json'], capture_output=True, text=True, check=True)
        plan = json.loads(dry.stdout)
        self.assertEqual(self.files(), {})
        applied = subprocess.run(args + ['--apply', '--expect-plan', plan['plan_sha256']], capture_output=True, text=True, check=True)
        self.assertIn('requirements_analyst\n- role:', applied.stdout)
        self.assertIn('\n- commands: planning, create-vision-document', applied.stdout)
        self.assertIn('main\n- role:', applied.stdout)
        self.assertTrue((self.repo / 'AGENTS.md').exists())


if __name__ == '__main__':
    unittest.main()
