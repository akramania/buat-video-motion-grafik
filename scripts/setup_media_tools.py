#!/usr/bin/env python3
"""Check cached media tools by default; explicitly install pinned tools with --install."""
import argparse, os, subprocess, sys, tempfile
from pathlib import Path


def main():
    p=argparse.ArgumentParser(description=__doc__)
    default_cache=Path(os.environ.get('MOTION_MEDIA_CACHE',str(Path(os.environ.get('XDG_CACHE_HOME',str(Path.home()/'.cache')))/'video-motion-media')))
    p.add_argument('--cache-root',type=Path,default=default_cache)
    req=Path(__file__).resolve().parent.parent/'assets'/'media_tools'/'requirements.txt'
    if not req.is_file():req=Path(__file__).with_name('requirements-media-tools.txt')
    p.add_argument('--requirements',type=Path,default=req)
    p.add_argument('--install',action='store_true')
    p.add_argument('--wheelhouse',type=Path,help='Offline Python wheel directory matching OS/architecture/Python; use with --install')
    p.add_argument('--skip-model-download',action='store_true')
    p.add_argument('--whisper-model',default='tiny')
    p.add_argument('--rembg-model',choices=['u2netp','u2net','u2net_human_seg'],default='u2netp')
    p.add_argument('--revision',default='d90ca5fe260221311c53c58e660288d3deb8d356',help='HF commit for tiny smoke model; choose matching revision for other model IDs')
    a=p.parse_args()
    helper=Path(__file__).with_name('media_tools.py')
    cache=a.cache_root.expanduser().resolve()
    deps=cache/'python-deps'
    if a.install:
        if sys.version_info<(3,12):p.error('The tested locked environment requires Python >=3.12. Select Python3.12+ or resolve/test compatible alternatives explicitly.')
        cache.mkdir(parents=True,exist_ok=True)
        stage=Path(tempfile.mkdtemp(prefix='python-deps-install-',dir=cache))
        cmd=[sys.executable,'-m','pip','install','--target',str(stage),'-r',str(a.requirements)]
        if a.wheelhouse:cmd += ['--no-index','--find-links',str(a.wheelhouse.resolve())]
        subprocess.run(cmd,check=True)
        if not a.skip_model_download and not a.wheelhouse:
            subprocess.run([sys.executable,str(helper),'--python-deps',str(stage),'download-models','--model-root',str(cache/'models'),'--whisper-model',a.whisper_model,'--rembg-model',a.rembg_model,'--revision',a.revision],check=True)
        subprocess.run([sys.executable,str(helper),'--python-deps',str(stage),'preflight','--strict','--model-root',str(cache/'models'),'--whisper-model',a.whisper_model,'--rembg-model',a.rembg_model],check=True)
        if deps.exists():
            backup=Path(tempfile.mkdtemp(prefix='python-deps-backup-',dir=cache));backup.rmdir();deps.rename(backup)
        stage.rename(deps)
    return subprocess.run([sys.executable,str(helper),'--python-deps',str(deps),'preflight','--strict','--model-root',str(cache/'models'),'--whisper-model',a.whisper_model,'--rembg-model',a.rembg_model]).returncode

if __name__=='__main__':raise SystemExit(main())
