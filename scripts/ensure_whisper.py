#!/usr/bin/env python3
"""Ensure reusable local Whisper dependencies and weights before audio work."""
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import fcntl

CACHE = Path(os.environ.get('MOTION_MEDIA_CACHE', str(Path.home()/'.cache/video-motion-media')))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model', default='medium', help='Multilingual production model; tiny is for smoke tests only')
    p.add_argument('--model-path', type=Path, help='Reuse a complete local model instead of downloading')
    p.add_argument('--cache-root', type=Path, default=CACHE)
    p.add_argument('--offline', action='store_true', help='Verify only; never install or download')
    p.add_argument('--report', type=Path)
    a = p.parse_args()
    root = a.cache_root.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    report = {'ready': False, 'model': a.model, 'cache_root': str(root)}
    try:
        # Serialize setup, so multiple episodes never install/download concurrently.
        with (root/'whisper-setup.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            deps = root/'whisper-python-deps'
            if deps.is_dir():
                sys.path.insert(0, str(deps))
            try:
                importlib.metadata.version('faster-whisper')
                if importlib.metadata.version('av') != '16.1.0':
                    raise RuntimeError('Whisper requires the tested av==16.1.0')
                import faster_whisper
            except Exception:
                if a.offline:
                    raise RuntimeError('Whisper dependencies missing or incompatible; rerun without --offline during online preparation')
                stage = Path(tempfile.mkdtemp(prefix='whisper-deps-', dir=root))
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--disable-pip-version-check', '--retries', '1', '--timeout', '20', '--target', str(stage), 'faster-whisper==1.2.1', 'av==16.1.0'], check=True)
                # Restart to avoid retaining previously imported incompatible modules.
                env = dict(os.environ)
                env['PYTHONPATH'] = str(stage) + os.pathsep + env.get('PYTHONPATH', '')
                subprocess.run([sys.executable, '-c', 'import faster_whisper, av; assert av.__version__ == "16.1.0"'], env=env, check=True)
                if deps.exists():
                    backup = Path(tempfile.mkdtemp(prefix='whisper-deps-backup-', dir=root))
                    backup.rmdir()
                    deps.rename(backup)
                stage.rename(deps)
                fcntl.flock(lock, fcntl.LOCK_UN)
                os.execv(sys.executable, [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]])
            from faster_whisper import WhisperModel
            from faster_whisper.utils import download_model
            if a.model_path:
                model_path = a.model_path.expanduser().resolve()
            else:
                # Reuse HF snapshots if already present; otherwise download once.
                try:
                    model_path = Path(download_model(a.model, local_files_only=True))
                except Exception:
                    model_path = root/'models'/('whisper-'+a.model)
                    required = ['model.bin', 'config.json', 'tokenizer.json', 'vocabulary.txt']
                    if not all((model_path/f).is_file() and (model_path/f).stat().st_size for f in required):
                        if a.offline:
                            raise RuntimeError('Complete Whisper weights unavailable offline')
                        model_path = Path(download_model(a.model, output_dir=str(model_path)))
            required = ['model.bin', 'config.json', 'tokenizer.json', 'vocabulary.txt']
            if not all((model_path/f).is_file() and (model_path/f).stat().st_size for f in required):
                raise RuntimeError('Whisper model incomplete: required files missing or empty')
            model = WhisperModel(str(model_path), device='cpu', compute_type='int8', cpu_threads=2, local_files_only=True)
            # Decode a short silent sample to catch runtime/PyAV/API failures.
            import numpy as np
            segments, _ = model.transcribe(np.zeros(16000, dtype=np.float32), language='ar', word_timestamps=True, condition_on_previous_text=False)
            list(segments)
            report.update(ready=True, python_deps=str(deps) if deps.is_dir() else None, model_path=str(model_path), faster_whisper=importlib.metadata.version('faster-whisper'), av=importlib.metadata.version('av'), load_and_decode=True)
    except Exception as e:
        report['error'] = f'{type(e).__name__}: {e}'
    if a.report:
        a.report.parent.mkdir(parents=True, exist_ok=True)
        a.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    return 0 if report['ready'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
