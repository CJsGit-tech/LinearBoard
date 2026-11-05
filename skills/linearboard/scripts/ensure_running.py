#!/usr/bin/env python3
"""Check the existing LinearBoard deployment and start its Compose services if needed."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.error import URLError, HTTPError
from urllib.parse import urlsplit
from urllib.request import urlopen

DEFAULT_PROJECT = Path('/Users/chuang/Desktop/projects/LinearBoard')


def run(command, timeout=100):
    result = subprocess.run(command, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        # Do not print Compose config or environment values containing credentials.
        raise RuntimeError('Command failed: '+ ' '.join(command[:3]) + '; check Docker access, service logs and existing configuration')
    return result.stdout


def healthy(url):
    try:
        with urlopen(url.rstrip('/')+'/api/health', timeout=4) as response:
            state=json.load(response)
    except (URLError, HTTPError, TimeoutError):
        return False
    except (ValueError, OSError) as error:
        raise RuntimeError('The selected endpoint is not a valid LinearBoard health service') from error
    if not isinstance(state, dict) or state.get('status') != 'ok' or state.get('database') != 'postgresql':
        raise RuntimeError('Endpoint is running but is not the expected healthy PostgreSQL LinearBoard; no service was replaced')
    with urlopen(url.rstrip('/')+'/api/capabilities', timeout=4) as response:
        identity = json.load(response)
        if not isinstance(identity, dict) or identity.get('application') != 'LinearBoard':
            raise RuntimeError('Unexpected application at selected URL')
    return True


def ensure(url='http://127.0.0.1:8765', project=None):
    parsed=urlsplit(url)
    if parsed.scheme != 'http' or parsed.hostname not in ('localhost','127.0.0.1') or parsed.port != 8765 or parsed.path not in ('','/') or parsed.query or parsed.fragment or parsed.username or parsed.password:
        raise RuntimeError('Automatic startup supports only the configured local port 8765; use --no-autostart for a different explicit service')
    if healthy(url):
        return 'already-running'
    root=Path(project or os.environ.get('LINEARBOARD_PROJECT_DIR',DEFAULT_PROJECT)).resolve()
    compose=root/'compose.yaml'
    if not compose.is_file():
        raise RuntimeError('LinearBoard compose.yaml was not found at '+str(root))
    command=['docker','compose','--project-directory',str(root),'-f',str(compose)]
    config=json.loads(run(command+['config','--format','json']))
    if config.get('name') != 'linearboard' or not {'app','db'} <= config.get('services',{}).keys():
        raise RuntimeError('Unexpected Compose project; refusing to select another application')
    if config['services']['app'].get('environment',{}).get('DATABASE_URL') != 'postgresql://linearboard@db:5432/linearboard':
        raise RuntimeError('Unexpected database destination; resolve it before automatic startup')
    volume=config.get('volumes',{}).get('postgres_data',{}).get('name')
    if volume != 'linearboard_postgres_data':
        raise RuntimeError('Unexpected data volume; no new volume was created')
    if not (root/'data/docker/database-password').is_file():
        raise RuntimeError('Existing database secret is missing; do not regenerate credentials')
    engine=subprocess.run(['docker','info','--format','{{.ServerVersion}}'],capture_output=True,text=True,timeout=15)
    if engine.returncode:
        print('Starting Docker Desktop…',file=sys.stderr)
        run(['docker','desktop','start','--timeout','90'],timeout=100)
    run(['docker','volume','inspect',volume])
    print('Starting existing LinearBoard Compose services…',file=sys.stderr)
    run(command+['up','-d','--no-build','--pull','never','--wait','--wait-timeout','90','db','app'],timeout=110)
    if not healthy(url):
        raise RuntimeError('Compose started but LinearBoard is not healthy; stop the workflow and inspect service logs')
    return 'started'


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default=os.environ.get('LINEARBOARD_URL','http://127.0.0.1:8765'))
    parser.add_argument('--project-dir',type=Path)
    args=parser.parse_args()
    try:
        print(json.dumps({'application':'LinearBoard','status':ensure(args.url,args.project_dir)}))
    except (OSError,ValueError,RuntimeError,subprocess.SubprocessError) as error:
        print(str(error),file=sys.stderr)
        sys.exit(1)
