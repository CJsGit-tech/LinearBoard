#!/usr/bin/env python3
"""Prepare or apply local Codex setup. No LinearBoard, model or network calls."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import tomllib

BEGIN = '<!-- linearboard:init:begin -->'
END = '<!-- linearboard:init:end -->'
ROLE_BEGIN = '<!-- linearboard:init:role:begin -->'
ROLE_END = '<!-- linearboard:init:role:end -->'
SKILL = Path(__file__).resolve().parents[1]


class SetupError(ValueError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def merge_block(old: str, new: str, begin: str, end: str, append: bool = True) -> str:
    if begin not in old and end not in old:
        if not append:
            return old
        return old + ('' if not old or old.endswith('\n\n') else '\n' if old.endswith('\n') else '\n\n') + new
    if old.count(begin) != 1 or old.count(end) != 1 or old.index(begin) > old.index(end):
        raise SetupError('Ambiguous or incomplete managed markers; reconcile them before init.')
    start, stop = old.index(begin), old.index(end) + len(end)
    # Replace only marker-owned text, preserving every byte outside the block.
    return old[:start] + new.rstrip('\n') + old[stop:]


def safe_path(repo: Path, relative: str) -> Path:
    path = repo / relative
    for node in (path, *path.parents):
        if node == repo:
            break
        if node.is_symlink():
            raise SetupError(f'Refusing symlinked configuration path: {node}')
    if path.exists() and not path.is_file():
        raise SetupError(f'Expected a file: {path}')
    return path


def parse_toml(text: str, label: str) -> dict:
    try:
        return tomllib.loads(text)
    except tomllib.TOMLDecodeError as cause:
        raise SetupError(f'Invalid TOML in {label}: {cause}') from cause


def roster_text(roster: list[dict]) -> str:
    return '\n\n'.join(
        item['name'] + '\n- role: ' + item['role'] + '\n- commands: ' + ', '.join(item['commands'])
        for item in roster
    )


def role_block(role: dict) -> str:
    return (
        ROLE_BEGIN + '\n'
        'Read applicable AGENTS.md and current parent-supplied LinearBoard sources.\n'
        'Supported command responsibilities: ' + ', '.join(role['commands']) + '.\n'
        'Commands do not grant authority beyond the delegated stage and scope.\n'
        + role['instructions'] + '\n'
        'Report concise source-backed results to the main agent. Never mark Done,\n'
        'deploy, send external messages, spawn agents or save PM report archives.\n'
        + ROLE_END
    )


def role_file(role: dict) -> str:
    instructions = role_block(role)
    if "'''" in instructions:
        raise SetupError('Unsupported literal delimiter in role template.')
    return (
        'name = ' + json.dumps(role['name']) + '\n'
        'description = ' + json.dumps(role['role'], ensure_ascii=False) + '\n'
        '# Model, reasoning, permissions and provider inherit from the parent.\n'
        "developer_instructions = '''\n" + instructions + "\n'''\n"
    )


def plan_setup(project: str, repository: str | Path, skill: Path = SKILL) -> dict:
    project = project.strip()
    if not project or len(project) > 200 or any(ord(c) < 32 or c in '`<>' for c in project):
        raise SetupError('Supply an unambiguous project name without control characters or markup delimiters.')
    repo = Path(repository).expanduser().resolve(strict=True)
    if not repo.is_dir():
        raise SetupError('Repository must be an existing, explicitly selected directory.')
    skill = skill.resolve(strict=True)
    registry = json.loads((skill / 'assets/init/agents.json').read_text())
    roles = registry['agents']
    names = [item['name'] for item in roles]
    if len(names) != len(set(names)) or not all(re.fullmatch(r'[a-z][a-z0-9_]*', n) for n in names):
        raise SetupError('Duplicate or unsafe agent names in initializer assets.')
    roster = [registry['orchestrator'], *roles]
    snapshots: dict[str, str | None] = {}
    actions = []
    warnings = []

    def read(relative: str) -> str | None:
        path = safe_path(repo, relative)
        raw = path.read_bytes() if path.exists() else None
        snapshots[relative] = digest(raw) if raw is not None else None
        return raw.decode('utf-8') if raw is not None else None

    def propose(relative: str, old: str | None, new: str) -> None:
        actions.append({'path': relative, 'action': 'unchanged' if old == new else 'create' if old is None else 'update', 'content': new})

    old = read('AGENTS.md')
    if old and BEGIN in old:
        # A repeat run must not silently rebind this repository to another project.
        region = old[old.index(BEGIN):old.find(END, old.index(BEGIN))]
        binding = re.search(r'^\*\*Configured project:\*\* `([^`]+)`$', region, re.M)
        if not binding or binding[1] != project:
            raise SetupError('Existing initializer project binding differs or is malformed; resolve the target before init.')
    template = (skill / 'assets/init/AGENTS.template.md').read_text()
    new = template.replace('{{PROJECT}}', project).replace('{{SKILL_PATH}}', (skill / 'SKILL.md').as_posix())
    new = new.replace('{{CHANGE_REVIEW_PATH}}', (skill / 'references/change-review.md').as_posix())
    new = new.replace('{{ROSTER}}', roster_text(roster))
    propose('AGENTS.md', old, merge_block(old or '', new, BEGIN, END))

    agent_dir = repo / '.codex/agents'
    # Check parents even if the directory itself does not yet exist.
    safe_path(repo, '.codex/agents/.init-path-check')
    existing = {}
    inventory = []
    for path in sorted(agent_dir.glob('*.toml')) if agent_dir.exists() else []:
        relative = path.relative_to(repo).as_posix()
        text = read(relative)
        data = parse_toml(text or '', relative)
        name = data.get('name')
        if not isinstance(name, str) or not name or name in existing:
            raise SetupError(f'Missing or duplicate existing agent name in {relative}.')
        if not all(isinstance(data.get(key), str) and data[key].strip() for key in ('description', 'developer_instructions')):
            raise SetupError(f'Incomplete existing agent definition in {relative}.')
        existing[name] = (relative, text, data)
        inventory.append(relative)

    for role in roles:
        name = role['name']
        if name in existing:
            relative, text, data = existing[name]
            if ROLE_BEGIN in text or ROLE_END in text:
                instructions = data['developer_instructions']
                if ROLE_BEGIN not in instructions or ROLE_END not in instructions:
                    raise SetupError(f'Managed role markers outside developer_instructions in {relative}.')
                new_text = merge_block(text, role_block(role), ROLE_BEGIN, ROLE_END, append=False)
                parsed = parse_toml(new_text, relative)
                if {k: v for k, v in parsed.items() if k != 'developer_instructions'} != {k: v for k, v in data.items() if k != 'developer_instructions'}:
                    raise SetupError(f'Role update would change custom settings in {relative}.')
                propose(relative, text, new_text)
            else:
                propose(relative, text, text)
                warnings.append(f'Reused custom agent {name} unchanged; review its instructions for compatibility.')
        else:
            relative = f'.codex/agents/{name}.toml'
            text = read(relative)
            if text is not None:
                raise SetupError(f'Agent filename is owned by a different role: {relative}.')
            new_text = role_file(role)
            parse_toml(new_text, relative)
            propose(relative, None, new_text)

    config = read('.codex/config.toml')
    settings = parse_toml(config or '', '.codex/config.toml')
    if 'agents' not in settings:
        # Do not override an inherited user choice to disable subagents.
        suffix = '[agents]\nmax_concurrent_threads_per_session = 3\n'
        new_config = (config or '') + ('' if not config or config.endswith('\n\n') else '\n' if config.endswith('\n') else '\n\n') + suffix
        parse_toml(new_config, '.codex/config.toml')
        propose('.codex/config.toml', config, new_config)
    else:
        if not isinstance(settings['agents'], dict):
            raise SetupError('Existing agents configuration is not a table.')
        propose('.codex/config.toml', config, config)
        if settings['agents'].get('enabled') is False:
            warnings.append('Subagents are explicitly disabled; setting retained. Resolve activation with the user before claiming agents are ready.')
        warnings.append('Existing agents configuration retained, including model defaults and thread limits.')

    extras = [
        {'name': name, 'role': ' '.join(data['description'].split()), 'commands': ['Not declared; preserve existing project instructions.']}
        for name, (_, _, data) in existing.items() if name not in names
    ]
    plan = {'project': project, 'repository': str(repo), 'skill': str(skill), 'actions': actions,
            'snapshots': snapshots, 'agent_inventory': inventory, 'agent_roster': roster,
            'extra_agents': extras, 'warnings': warnings}
    plan['plan_sha256'] = digest(json.dumps(plan, sort_keys=True, ensure_ascii=False).encode())
    return plan


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
    fd, staged = tempfile.mkstemp(prefix='.linearboard-init-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(staged, mode)
        os.replace(staged, path)
    finally:
        Path(staged).unlink(missing_ok=True)


def apply_setup(plan: dict, expected: str) -> list[str]:
    if not expected or expected != plan['plan_sha256']:
        raise SetupError('Plan changed or expected hash missing; inspect a fresh plan before applying.')
    repo = Path(plan['repository'])
    for relative, expected_hash in plan['snapshots'].items():
        path = safe_path(repo, relative)
        current = digest(path.read_bytes()) if path.exists() else None
        if current != expected_hash:
            raise SetupError(f'Concurrent change to {relative}; inspect a fresh plan.')
    inventory = sorted(p.relative_to(repo).as_posix() for p in (repo / '.codex/agents').glob('*.toml'))
    if inventory != sorted(plan['agent_inventory']):
        raise SetupError('Agent inventory changed; inspect a fresh plan.')
    written = []
    try:
        for action in plan['actions']:
            if action['action'] == 'unchanged':
                continue
            path = safe_path(repo, action['path'])
            # Recheck the target immediately before replacing it.
            current = digest(path.read_bytes()) if path.exists() else None
            if current != plan['snapshots'][action['path']]:
                raise SetupError(f'Concurrent change to {action["path"]}; inspect a fresh plan.')
            atomic_write(path, action['content'])
            if path.read_bytes() != action['content'].encode('utf-8'):
                raise SetupError(f'Readback mismatch: {action["path"]}')
            written.append(action['path'])
    except (OSError, SetupError) as cause:
        raise SetupError(f'{cause}; verified completed files: {json.dumps(written)}. Keep them and re-plan remaining work.') from cause
    return written


def public_report(plan: dict, applied: bool = False, written: list[str] | None = None) -> dict:
    return {key: value for key, value in plan.items() if key not in ('snapshots', 'agent_inventory', 'actions')} | {
        'applied': applied, 'written': written or [],
        'files': [{k: v for k, v in action.items() if k != 'content'} for action in plan['actions']],
        'checks': 'Local configuration only; no model call, agent dispatch, hook installation or live document audit.',
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True)
    parser.add_argument('--repo', required=True, help='Resolved existing repository directory; no cwd guessing')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--expect-plan', help='Hash from a reviewed dry run')
    parser.add_argument('--json', action='store_true', help='Machine-readable engineering result, not a saved PM record')
    args = parser.parse_args(argv)
    try:
        plan = plan_setup(args.project, args.repo)
        written = apply_setup(plan, args.expect_plan) if args.apply else []
        report = public_report(plan, args.apply, written)
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(('Initialized' if args.apply else 'Proposed initialization for') + f' {plan["project"]}: {plan["repository"]}')
            print('\n' + roster_text(plan['agent_roster'] + plan['extra_agents']))
            print('\nCommands identify scoped responsibilities; the main agent routes the workflow.')
            for item in report['files']:
                print(item['action'] + ': ' + item['path'])
            for warning in plan['warnings']:
                print('Review: ' + warning)
            print('Plan SHA256: ' + plan['plan_sha256'])
            print(report['checks'])
        return 0
    except (OSError, ValueError, KeyError) as cause:
        print('Initialization blocked: ' + str(cause), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
