#!/usr/bin/env python3
"""Check or restore the pinned Linux video toolkit; reuse valid caches."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request
import zipfile

SKILL = Path(__file__).resolve().parents[1]
LOCK = json.loads((SKILL / 'assets/runtime-lock.json').read_text())


def command(argv, env=None):
    try:
        result = subprocess.run([str(x) for x in argv], capture_output=True,
                                text=True, env=env, timeout=180)
        return result.returncode, (result.stdout + result.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as error:
        return 1, str(error)


def digest(file):
    with file.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def restore(root, component, offline):
    archive = root / 'downloads' / component['url'].rsplit('/', 1)[-1]
    archive.parent.mkdir(parents=True, exist_ok=True)
    if not archive.is_file() or digest(archive) != component['sha256']:
        if offline:
            raise RuntimeError('Verified archive unavailable offline: ' + archive.name)
        part = archive.with_name(archive.name + '.part')
        with urllib.request.urlopen(component['url'], timeout=60) as response, part.open('wb') as output:
            shutil.copyfileobj(response, output)
        if digest(part) != component['sha256']:
            part.unlink()
            raise RuntimeError('Archive SHA-256 mismatch; previous installation preserved')
        part.replace(archive)
    stage = Path(tempfile.mkdtemp(prefix='extract-', dir=root))
    try:
        if zipfile.is_zipfile(archive):
            with zipfile.ZipFile(archive) as bundle:
                for entry in bundle.infolist():
                    target = (stage / entry.filename).resolve()
                    if not target.is_relative_to(stage.resolve()):
                        raise RuntimeError('Unsafe ZIP path')
                    bundle.extract(entry, stage)
                    mode = (entry.external_attr >> 16) & 0o777
                    if mode:
                        target.chmod(mode)
        else:
            with tarfile.open(archive) as bundle:
                bundle.extractall(stage, filter='data')
        source = stage / component['directory']
        code, version = command([source / component['executable'], component['version_argument']])
        if code or component['version'] not in version:
            raise RuntimeError('Staged executable failed: ' + version[:500])
        target = root / component['directory']
        backup = root / (component['directory'] + '.previous')
        if backup.exists():
            raise RuntimeError('Previous recovery directory exists; inspect before replacement')
        if target.exists():
            target.rename(backup)
        try:
            source.rename(target)
        except Exception:
            if backup.exists():
                backup.rename(target)
            raise
        if backup.exists():
            shutil.rmtree(backup)
    finally:
        shutil.rmtree(stage)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache-root', type=Path, default=Path.home() / '.cache/km-video-components' / LOCK['cache_release'])
    parser.add_argument('--runtime', type=Path, default=Path.home() / '.cache/km-video-hyperframes' / LOCK['npm_packages']['hyperframes']['version'])
    parser.add_argument('--install', action='store_true', help='Restore missing binaries and complete locked node_modules')
    parser.add_argument('--offline', action='store_true', help='Never access the network; installation uses verified archives/npm cache')
    parser.add_argument('--whisper', action='store_true', help='Also ensure/load/decode the production Whisper model')
    parser.add_argument('--model', default='medium')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    root, runtime = args.cache_root.expanduser().resolve(), args.runtime.expanduser().resolve()
    report = {'ready': False, 'platform': platform.platform(), 'lock_date': LOCK['checked_on'], 'components': {}, 'runtime': str(runtime)}
    setup_lock = None
    try:
        if platform.system() != 'Linux' or platform.machine() not in ('x86_64', 'amd64'):
            raise RuntimeError('This binary lock targets Linux x64 glibc; resolve and test a separate lock for this platform')
        if args.install:
            root.mkdir(parents=True, exist_ok=True)
            setup_lock = (root / 'setup.lock').open('a')
            fcntl.flock(setup_lock, fcntl.LOCK_EX)
        binaries = {}
        for name, component in LOCK['binaries'].items():
            executable = root / component['directory'] / component['executable']
            code, version = command([executable, component['version_argument']]) if executable.is_file() else (1, '')
            companion_missing = component.get('companion') and not (root / component['directory'] / component['companion']).is_file()
            if (code or component['version'] not in version or companion_missing) and args.install:
                restore(root, component, args.offline)
                code, version = command([executable, component['version_argument']])
            report['components'][name] = {'ready': code == 0 and component['version'] in version,
                'version': version.splitlines()[0] if version else None, 'path': str(executable)}
            binaries[name] = executable
        ffprobe = binaries['ffmpeg'].parent / 'ffprobe'
        code, version = command([ffprobe, '-version']) if ffprobe.is_file() else (1, '')
        report['components']['ffprobe'] = {'ready': code == 0 and LOCK['binaries']['ffmpeg']['version'] in version, 'path': str(ffprobe)}
        report['binaries_ready'] = all(item['ready'] for item in report['components'].values())
        env = dict(os.environ)
        bin_dirs = [str(binaries['node'].parent), str(binaries['ffmpeg'].parent)]
        env['PATH'] = os.pathsep.join([*bin_dirs, env.get('PATH', '')])
        env['KM_HYPERFRAMES_RUNTIME'] = str(runtime)
        env['HYPERFRAMES_BROWSER_PATH'] = str(binaries['chromium'])
        code, npm_version = command([binaries['node'].parent / 'npm', '--version'], env)
        report['components']['npm'] = {'ready': code == 0 and npm_version.splitlines()[-1] == LOCK['npm'], 'version': npm_version.splitlines()[-1]}
        code, dependencies = command(['ldd', binaries['chromium']], env)
        report['linux_libraries'] = {'ready': code == 0 and 'not found' not in dependencies, 'ldd': dependencies}
        argv = [binaries['node'], SKILL / 'scripts/setup_hyperframes.mjs', '--runtime', runtime, '--browser', binaries['chromium']]
        if args.install:
            argv.append('--install-offline' if args.offline else '--online')
        if report['components']['node']['ready']:
            completed = subprocess.run([str(x) for x in argv], env=env, capture_output=True, text=True)
            report['renderer_ready'] = completed.returncode == 0
            try:
                report['renderer_preflight'] = json.loads(completed.stdout[completed.stdout.rfind('\n{')+1:])
            except (ValueError, TypeError):
                report['renderer_preflight'] = {'ready': False, 'output': (completed.stdout + completed.stderr)[-12000:]}
        else:
            report['renderer_ready'] = False
            report['renderer_preflight'] = {'ready': False, 'error': 'Locked Node executable unavailable; restore it before browser preflight'}
        for name, expected in LOCK['npm_packages'].items():
            package = runtime / 'node_modules' / name / 'package.json'
            version = json.loads(package.read_text())['version'] if package.is_file() else None
            report['components'][name] = {'ready': version == expected['version'], 'version': version}
        code, module_result = command([binaries['node'], SKILL / 'scripts/check_video_modules.mjs', runtime], env)
        report['module_checks'] = {'ready': code == 0, 'output': module_result}
        if args.install:
            (runtime / 'runtime-env.json').write_text(json.dumps({'nodeExecutable': str(binaries['node']), 'binDirs': bin_dirs}, indent=2) + '\n')
        report['whisper'] = {'required': args.whisper, 'checked': False, 'ready': False, 'version_pin': LOCK['whisper']['version']}
        if args.whisper:
            whisper_report = root / 'whisper-ready.json'
            argv = [os.sys.executable, SKILL / 'scripts/ensure_whisper.py', '--model', args.model, '--report', whisper_report]
            if args.offline or not args.install:
                argv.append('--offline')
            completed = subprocess.run([str(x) for x in argv], env=env)
            report['whisper'] = {**json.loads(whisper_report.read_text()), 'checked': True, 'required': True}
            report['whisper']['ready'] = completed.returncode == 0 and report['whisper'].get('ready', False)
        report['ready'] = report['renderer_ready'] and report['module_checks']['ready'] and all(item['ready'] for item in report['components'].values()) and (not args.whisper or report['whisper']['ready'])
        report['all_components_ready'] = report['ready'] and report['whisper']['checked'] and report['whisper']['ready']
    except Exception as error:
        report['error'] = f'{type(error).__name__}: {error}'
    finally:
        if setup_lock:
            setup_lock.close()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if report['ready'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
