#!/usr/bin/env python3
"""Local Whisper timestamps and foreground PNGs. Network only in download-models."""
from __future__ import annotations
import argparse, hashlib, importlib.metadata, importlib.util, json, os
from pathlib import Path
import shutil, sys

CACHE_ROOT=Path(os.environ.get('MOTION_MEDIA_CACHE', str(Path(os.environ.get('XDG_CACHE_HOME',str(Path.home()/'.cache')))/'video-motion-media'))).expanduser().resolve()


def dump(data, path=None):
    s=json.dumps(data,ensure_ascii=False,indent=2)
    if path:
        p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s+'\n',encoding='utf-8')
    print(s)


def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def verify_manifest(root):
    root=Path(root).resolve(); p=root/'model-manifest.json'
    if not p.is_file():return {'ok':False,'error':'model-manifest.json missing; create during download-models'}
    try:
        manifest=json.loads(p.read_text(encoding='utf-8')); errors=[]
        for rel,meta in manifest['files'].items():
            f=(root/rel).resolve()
            if root not in f.parents:raise ValueError('Manifest path outside model root')
            if not f.is_file() or f.stat().st_size!=meta['bytes'] or sha256_file(f)!=meta['sha256']:errors.append(rel)
        return {'ok':bool(manifest['files']) and not errors,'mismatches':errors,'files_verified':len(manifest['files']),'whisper_revision':manifest.get('whisper_revision')}
    except Exception as e:return {'ok':False,'error':str(e)}


def model_files(root, name='u2netp'):
    r=Path(root).expanduser().resolve()
    return [r/'rembg'/'models'/name/(name+'.onnx'),r/'rembg'/(name+'.onnx')]


def preflight(a):
    packages={}
    for dist,mod in [('faster-whisper','faster_whisper'),('ctranslate2','ctranslate2'),('rembg','rembg'),('onnxruntime','onnxruntime')]:
        try:
            v=importlib.metadata.version(dist)
            __import__(mod)
            packages[dist]={'version':v,'import':True}
        except Exception as e: packages[dist]={'import':False,'error':str(e)}
    root=Path(a.model_root).expanduser().resolve()
    whisper=root/('whisper-'+a.whisper_model)
    required=['model.bin','config.json','tokenizer.json','vocabulary.txt']
    wf={x:(whisper/x).is_file() for x in required}
    rm=next((x for x in model_files(root,a.rembg_model) if x.is_file()),None)
    data={'python':sys.version.split()[0],'packages':packages,'tools':{x:shutil.which(x) for x in ['ffmpeg','ffprobe']},'model_root':str(root),'whisper':{'path':str(whisper),'files':wf,'ready':all(wf.values())},'remove_background':{'model':a.rembg_model,'path':str(rm) if rm else None,'ready':bool(rm)}}
    data['model_manifest']=verify_manifest(root)
    data['ready']=data['model_manifest']['ok'] and all(x['import'] for x in packages.values()) and all(data['tools'].values()) and data['whisper']['ready'] and bool(rm)
    dump(data,a.report)
    return 0 if data['ready'] or not a.strict else 2


def download_models(a):
    from faster_whisper.utils import download_model
    root=Path(a.model_root).expanduser().resolve(); root.mkdir(parents=True,exist_ok=True)
    wp=download_model(a.whisper_model,output_dir=str(root/('whisper-'+a.whisper_model)),revision=a.revision)
    os.environ['U2NET_HOME']=str(root/'rembg')
    os.environ.setdefault('OMP_NUM_THREADS',str(a.threads))
    from rembg import new_session
    new_session(a.rembg_model,providers=['CPUExecutionProvider'])
    files={}
    for p in root.rglob('*'):
        if p.is_file() and '.cache' not in p.relative_to(root).parts and p.name!='model-manifest.json':
            files[str(p.relative_to(root))]={'bytes':p.stat().st_size,'sha256':sha256_file(p)}
    metadata=Path(wp)/'.cache'/'huggingface'/'download'/'model.bin.metadata'
    resolved_revision=metadata.read_text().splitlines()[0] if metadata.is_file() else a.revision
    dump({'whisper':str(wp),'rembg_model':a.rembg_model,'whisper_revision':resolved_revision,'requested_revision':a.revision,'files':files},root/'model-manifest.json')
    return 0


def transcribe(a):
    from faster_whisper import WhisperModel
    wp=Path(a.model_path).expanduser().resolve()
    if not wp.is_dir() or not (wp/'model.bin').is_file(): raise ValueError('Local Whisper model not ready; run download-models during online setup.')
    model=WhisperModel(str(wp),device='cpu',compute_type='int8',cpu_threads=a.threads,local_files_only=True)
    segs,info=model.transcribe(a.input,language=a.language,task='transcribe',word_timestamps=True,beam_size=a.beam_size,vad_filter=a.vad,condition_on_previous_text=False)
    segments=[]
    for s in segs:
        words=[{'start':round(w.start+a.offset,3),'end':round(w.end+a.offset,3),'text':w.word,'probability':round(w.probability,5)} for w in (s.words or [])]
        segments.append({'start':round(s.start+a.offset,3),'end':round(s.end+a.offset,3),'text':s.text,'words':words,'avg_logprob':s.avg_logprob,'no_speech_prob':s.no_speech_prob})
    data={'language':info.language,'language_probability':info.language_probability,'source':str(Path(a.input).resolve()),'source_offset_seconds':a.offset,'task':'transcribe','timestamp_method':'Whisper cross-attention/DTW estimate; manually review against source audio','segments':segments,'text':' '.join(s['text'].strip() for s in segments)}
    dump(data,a.output)
    if a.srt:
        def stamp(t):
            n=round(max(0,t)*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'
        p=Path(a.srt);p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text('\n'.join(f'{i+1}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"].strip()}\n' for i,s in enumerate(segments)),encoding='utf-8')
    return 0


def cutout(a):
    root=Path(a.model_root).expanduser().resolve()
    mp=next((x for x in model_files(root,a.rembg_model) if x.is_file()),None)
    if mp is None:raise ValueError('Local rembg model missing; download models before offline rendering.')
    os.environ['U2NET_HOME']=str(root/'rembg')
    os.environ.setdefault('OMP_NUM_THREADS',str(a.threads))
    from rembg import new_session, remove
    from PIL import Image
    import numpy as np
    sess=new_session(a.rembg_model,providers=['CPUExecutionProvider'])
    src=Path(a.input); dest=Path(a.output)
    batch=src.is_dir()
    paths=sorted(p for p in src.iterdir() if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp'}) if batch else [src]
    if not paths: raise ValueError('No input images')
    stats=[]
    for p in paths:
        out=dest/(p.stem+'.png') if batch else dest
        if out.suffix.lower()!='.png': raise ValueError('Cutout output must use .png for alpha')
        out.parent.mkdir(parents=True,exist_ok=True)
        img=Image.open(p).convert('RGBA')
        result=remove(img,session=sess,alpha_matting=a.alpha_matting)
        result.save(out)
        alpha=np.asarray(result.getchannel('A'))
        stats.append({'input':str(p),'output':str(out),'size':result.size,'alpha_min':int(alpha.min()),'alpha_max':int(alpha.max()),'foreground_fraction':float((alpha>127).mean())})
    dump({'model':a.rembg_model,'model_file':str(mp),'frames':stats,'temporal_stabilization':False,'note':'Independent image masks: inspect motion/edges and stabilize or track before final video composite.'},a.report)
    return 0


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--python-deps',default=os.environ.get('MEDIA_TOOLS_PYTHON_PATH',str(CACHE_ROOT/'python-deps') if (CACHE_ROOT/'python-deps').is_dir() else None),help='Optional isolated pip --target directory')
    sub=p.add_subparsers(dest='command',required=True)
    def models(q):
        q.add_argument('--model-root',default=os.environ.get('MOTION_MODEL_ROOT',str(CACHE_ROOT/'models')))
        q.add_argument('--whisper-model',default='tiny',help='tiny for smoke test; use small/medium/large-v3 per hardware and accuracy needs')
        q.add_argument('--rembg-model',choices=['u2netp','u2net','u2net_human_seg'],default='u2netp')
        q.add_argument('--threads',type=int,default=4)
    q=sub.add_parser('preflight');models(q);q.add_argument('--strict',action='store_true');q.add_argument('--report');q.set_defaults(fn=preflight)
    q=sub.add_parser('download-models');models(q);q.add_argument('--revision',default='main',help='Pin HF commit for reproducible deployment');q.set_defaults(fn=download_models)
    q=sub.add_parser('transcribe');q.add_argument('--input',required=True);q.add_argument('--output',required=True);q.add_argument('--srt');q.add_argument('--model-path',required=True);q.add_argument('--language',default=None);q.add_argument('--offset',type=float,default=0);q.add_argument('--threads',type=int,default=4);q.add_argument('--beam-size',type=int,default=5);q.add_argument('--vad',action='store_true');q.set_defaults(fn=transcribe)
    q=sub.add_parser('cutout');models(q);q.add_argument('--input',required=True);q.add_argument('--output',required=True);q.add_argument('--alpha-matting',action='store_true');q.add_argument('--report');q.set_defaults(fn=cutout)
    a=p.parse_args()
    if a.python_deps:sys.path.insert(0,str(Path(a.python_deps).expanduser().resolve()))
    if getattr(a,'threads',1)<1:p.error('--threads must be >= 1')
    try:return a.fn(a)
    except Exception as e:print(f'{type(e).__name__}: {e}',file=sys.stderr);return 1

if __name__=='__main__':raise SystemExit(main())
