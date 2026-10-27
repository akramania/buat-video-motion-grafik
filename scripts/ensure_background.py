#!/usr/bin/env python3
"""Ensure reusable CPU RVM dependencies/model and test actual recurrent inference."""
from __future__ import annotations
import argparse
import fcntl
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from background_runtime import CACHE, ASSETS, MODEL, add_deps, check_model, model_path, smoke, write_json


def dependencies():
    import numpy
    import PIL
    import onnxruntime
    return {name: dict(version=importlib.metadata.version(dist), path=mod.__file__) for name, dist, mod in [('numpy', 'numpy', numpy), ('pillow', 'Pillow', PIL), ('onnxruntime', 'onnxruntime', onnxruntime)]}


def download(url, target):
    temporary = target.with_name(target.name+'.download')
    error = None
    for _ in range(2):
        try:
            with urllib.request.urlopen(url, timeout=30) as src, temporary.open('wb') as dst:
                shutil.copyfileobj(src, dst)
            check_model(temporary)
            temporary.replace(target)
            return
        except Exception as e:
            error = e
    raise RuntimeError(f'Official RVM download failed: {error}')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache-root', type=Path, default=CACHE)
    p.add_argument('--model-path', type=Path, help='Use the exact verified official FP32 model at this path')
    p.add_argument('--offline', action='store_true', help='Never install or access the network')
    p.add_argument('--report', type=Path)
    a = p.parse_args()
    root = a.cache_root.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    report = dict(ready=False, backend='RVM MobileNetV3 FP32', cache_root=str(root), scope='human video matting', offline=a.offline)
    try:
        with (root/'background-setup.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            deps = add_deps(root)
            try:
                versions = dependencies()
            except Exception:
                if a.offline:
                    raise RuntimeError('Background dependencies unavailable offline; rerun online')
                if sys.version_info < (3, 12):
                    raise RuntimeError('Automatic pinned installation requires Python 3.12+')
                stage = Path(tempfile.mkdtemp(prefix='background-deps-', dir=root))
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--disable-pip-version-check', '--only-binary=:all:', '--retries', '1', '--timeout', '20', '--target', str(stage), '-r', str(ASSETS/'requirements-background.txt')], check=True)
                env = dict(os.environ, PYTHONPATH=str(stage))
                subprocess.run([sys.executable, '-c', 'import numpy, PIL, onnxruntime'], env=env, check=True)
                target = root/'background-python-deps'
                if target.exists():
                    backup = Path(tempfile.mkdtemp(prefix='background-deps-backup-', dir=root))
                    backup.rmdir()
                    target.rename(backup)
                stage.rename(target)
                fcntl.flock(lock, fcntl.LOCK_UN)
                os.execv(sys.executable, [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]])
            report['packages'] = versions
            report['python_deps'] = deps
            report['tools'] = {t: shutil.which(t) for t in ['ffmpeg', 'ffprobe']}
            if not all(report['tools'].values()):
                raise RuntimeError('FFmpeg and ffprobe required; install a compatible full FFmpeg build first')
            m = model_path(root, a.model_path)
            try:
                check_model(m)
            except Exception:
                if a.model_path or a.offline:
                    raise
                m.parent.mkdir(parents=True, exist_ok=True)
                download(MODEL['url'], m)
            license_path = root/'models/rvm'/MODEL['license_file']
            license_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ASSETS/MODEL['license_file'], license_path)
            result = smoke(m)
            report.update(ready=True, model_path=str(m), model_sha256=MODEL['sha256'], model_bytes=m.stat().st_size, license=MODEL['license'], license_path=str(license_path), inference=result)
            write_json(root/'background-ready.json', report)
    except Exception as e:
        report['error'] = f'{type(e).__name__}: {e}'
    if a.report:
        write_json(a.report, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['ready'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
