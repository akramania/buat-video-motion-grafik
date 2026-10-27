#!/usr/bin/env python3
"""Shared, local-only human video matting runtime; setup owns network access."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'assets/media_tools'
CACHE = Path(os.environ.get('MOTION_MEDIA_CACHE', str(Path(os.environ.get('XDG_CACHE_HOME', str(Path.home()/'.cache')))/'video-motion-media')))
MODEL = json.loads((ASSETS/'background-models.json').read_text())['rvm_mobilenetv3_fp32']


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name+'.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    temporary.replace(path)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()


def add_deps(cache=CACHE, explicit=None):
    p = Path(explicit) if explicit else Path(cache)/'background-python-deps'
    if p.is_dir():
        sys.path.insert(0, str(p.resolve()))
        return str(p.resolve())
    return None


def model_path(cache=CACHE, explicit=None):
    return Path(explicit).expanduser().resolve() if explicit else Path(cache).expanduser().resolve()/'models/rvm'/MODEL['file']


def check_model(path):
    p = Path(path)
    if not p.is_file() or p.stat().st_size != MODEL['bytes'] or digest(p) != MODEL['sha256']:
        raise RuntimeError('RVM weights missing, incomplete or checksum mismatch; run ensure_background.py')


def session(path, threads=2):
    import onnxruntime as ort
    check_model(path)
    options = ort.SessionOptions()
    options.intra_op_num_threads = threads
    options.inter_op_num_threads = 1
    return ort.InferenceSession(str(path), sess_options=options, providers=['CPUExecutionProvider'])


def smoke(path, threads=2):
    import numpy as np
    m = session(path, threads)
    rec = [np.zeros((1, 1, 1, 1), np.float32) for _ in range(4)]
    for level in [.25, .50]:
        data = dict(src=np.full((1, 3, 64, 96), level, np.float32), downsample_ratio=np.array([.5], np.float32))
        data.update({f'r{i+1}i': r for i, r in enumerate(rec)})
        fgr, pha, *rec = m.run(None, data)
        if pha.shape != (1, 1, 64, 96) or not np.isfinite(pha).all() or not all(np.isfinite(r).all() for r in rec):
            raise RuntimeError('RVM recurrent inference smoke test failed')
    return dict(frames=2, recurrent_state_reused=True, alpha_shape=list(pha.shape), finite=True, provider=m.get_providers())


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))


def signature(path):
    p = Path(path).resolve()
    s = p.stat()
    return dict(path=str(p), bytes=s.st_size, mtime_ns=s.st_mtime_ns)


def run_checked(command, log):
    with Path(log).open('w') as f:
        subprocess.run(command, stdout=f, stderr=f, check=True)


def read_exact(pipe, n):
    chunks = []
    while n:
        b = pipe.read(n)
        if not b:
            if chunks:
                raise RuntimeError('Incomplete decoded video frame')
            return None
        chunks.append(b)
        n -= len(b)
    return b''.join(chunks)
