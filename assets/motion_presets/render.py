#!/usr/bin/env python3
"""Render original motion presets. Python 3.10+, Pillow, NumPy and FFmpeg.

Public frame() times and CLI --frame are actual output seconds. Legacy preset
modules retain their normalized 0..5 clock. Modules with time_mode='seconds'
receive actual seconds, cfg['_seconds'] and cfg['_duration']. Their tempo
controls action speed independently of scene duration and cue spacing.
"""
import argparse, importlib, json, math, os, subprocess, sys
from pathlib import Path
from PIL import Image
from core import *

MODULES=['ui','typography','carousels','new_a','new_b','long_a','long_b','kinetic_a','kinetic_b','kinetic_c','motionprompt','guide_a','guide_b','guide_c','guide_d','envato2026','premium_type','premium_maps_data','premium_ui_product','premium_promo_fx','creator_fx','creator_fx_plus']


def registry():
    presets={}; dispatch={}
    for name in MODULES:
        try: mod=importlib.import_module(name)
        except ModuleNotFoundError as e:
            if e.name==name: continue
            raise
        for pid,metadata in mod.PRESETS.items():
            if pid in presets: raise ValueError('Duplicate preset '+pid)
            if not isinstance(metadata,dict): raise ValueError(pid+' metadata must be a dictionary')
            for key in ('name','description','genre','text','subtitle'):
                if not isinstance(metadata.get(key),str): raise ValueError(pid+' requires text metadata: '+key)
            if metadata.get('family')=='kinetic':
                for key in ('source_url','observed_timestamp','mechanism'):
                    if not isinstance(metadata.get(key),str) or not metadata[key].strip():
                        raise ValueError(pid+' requires provenance: '+key)
                if not metadata['source_url'].startswith('https://'):
                    raise ValueError(pid+' source_url must be an HTTPS URL')
                if metadata.get('variant_basis') not in ('observed','adapted'):
                    raise ValueError(pid+' variant_basis must be observed or adapted')
            presets[pid]=metadata; dispatch[pid]=mod.render
    return presets,dispatch


def _number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int,float)) or not math.isfinite(value):
        raise ValueError(name+' must be a finite number')
    return float(value)


def _duration(cfg, value=None):
    duration=_number(cfg.get('duration',5) if value is None else value,'duration')
    minimum=max(.5,float(cfg.get('min_duration',.5)))
    if not minimum <= duration <= 120:
        raise ValueError(f'duration must be between {minimum:g} and 120 seconds for this preset')
    return duration


def configuration(pid,raw=None):
    presets,_=registry()
    if pid not in presets: raise ValueError('Unknown preset: '+pid)
    if raw is not None and not isinstance(raw,dict): raise ValueError('configuration must be a JSON object')
    cfg=dict(presets[pid]); cfg.update(raw or {}); cfg['preset']=pid
    # Timing mode and minimum dwell are renderer contracts, not user overrides.
    cfg['time_mode']=presets[pid].get('time_mode','normalized')
    cfg['min_duration']=presets[pid].get('min_duration',.5)
    cfg['duration']=_duration(cfg)
    cfg['tempo']=_number(cfg.get('tempo',1),'tempo')
    if not .5 <= cfg['tempo'] <= 2: raise ValueError('tempo must be between 0.5 and 2')
    cues=cfg.get('cues',{})
    if pid=='B05' and isinstance(cues,list):
        # B05 predates the named long-scene cue contract. Its word intervals
        # live on the normalized 0..5 clock, even when duration is changed.
        for i,cue in enumerate(cues):
            if not isinstance(cue,dict): raise ValueError('B05 cues must contain start/end objects')
            start=_number(cue.get('start'),'cue start'); end=_number(cue.get('end'),'cue end')
            if not 0 <= start < end <= 5: raise ValueError('B05 cue intervals must satisfy 0 <= start < end <= 5')
        cfg['cues']=[dict(cue) for cue in cues]
    else:
        if not isinstance(cues,dict): raise ValueError('cues must be a JSON object of cue names and seconds')
        defaults=cfg.get('cue_defaults',{})
        for key,value in cues.items():
            if not isinstance(key,str) or not key: raise ValueError('cue names must be nonempty strings')
            if defaults and key not in defaults: raise ValueError('Unknown cue for '+pid+': '+key)
            if not 0 <= _number(value,'cue '+key) <= cfg['duration']:
                raise ValueError('cue '+key+' must fall within the scene duration')
        cfg['cues']=dict(cues)
    if 'end_behavior' in presets[pid]:
        supported=presets[pid].get('supported_end_behaviors',[presets[pid]['end_behavior']])
        if cfg.get('end_behavior') not in supported:
            raise ValueError('end_behavior for '+pid+' must be one of '+', '.join(supported))
    if cfg.get('genre') not in PALETTES: raise ValueError('Unknown genre: '+str(cfg.get('genre')))
    for key in ['text','subtitle']:
        if not isinstance(cfg.get(key,''),str): raise ValueError(key+' must be text')
        if len(cfg.get(key,''))>160: raise ValueError(key+' exceeds 160 characters; shorten copy or split into scenes')
    for key in ['bg','panel','text_color','muted','accent','secondary']:
        if key in cfg:
            value=cfg[key]
            if not (isinstance(value,str) and len(value)==7 and value[0]=='#'):
                raise ValueError(key+' must be #RRGGBB')
            try: int(value[1:],16)
            except ValueError: raise ValueError(key+' must be #RRGGBB')
    if pid.startswith('CFX') and int(pid[3:])>=21:
        import creator_fx_plus
        creator_fx_plus.validate_config(cfg)
    return cfg


def frame(pid,t,cfg,labels=True):
    """Render a frame at actual output time t, respecting cfg.duration."""
    presets,dispatch=registry()
    if pid not in dispatch: raise ValueError('Unknown preset: '+pid)
    cfg=dict(cfg)
    duration=_duration(cfg,cfg.get('_duration',cfg.get('duration',presets[pid].get('duration',5))))
    seconds=_number(t,'frame time')
    if not 0 <= seconds <= duration: raise ValueError('frame time must fall within the scene duration')
    cfg['_labels']=bool(labels); cfg['_seconds']=seconds; cfg['_duration']=duration
    long=presets[pid].get('time_mode')=='seconds'
    clock=seconds if long else seconds/duration*5
    im=dispatch[pid](pid,clock,cfg).convert('RGBA')
    if im.size!=(W,H): raise ValueError(pid+' must return 1280x720')
    if labels:
        p=palette(cfg)
        text(im,'MOTION / PRESET ATLAS',54,38,15,p['muted'],'mono',anchor='left')
        text(im,pid+'  '+presets[pid]['name'],54,83,28,p['text'],anchor='left')
        tag(im,cfg['genre'].upper(),1050,53,p)
        line(im,[(54,118),(1226,118)],rgba(p['muted'],60),1)
        if long:
            text(im,'SCENE KEKAL',54,668,13,p['accent'],'mono',anchor='left')
            text(im,f'{seconds:04.1f} / {duration:g}s',240,668,13,p['muted'],'mono',anchor='left')
        else:
            phases=[('MASUK',.15,1.15),('GERAK',1.15,4.15),('KELUAR',4.15,5.)]
            for i,(label,a,b) in enumerate(phases):
                text(im,label,54+i*118,668,13,p['accent'] if a<=clock<b else p['muted'],'mono',anchor='left')
        line(im,[(477,669),(1120,669)],rgba(p['muted'],65),2)
        line(im,[(477,669),(477+643*clamp(seconds/duration),669)],p['accent'],3)
        text(im,str(cfg.get('_fps',60))+' FPS',1224,667,14,p['muted'],'mono',anchor='right')
    return im if cfg.get('_transparent') else im.convert('RGB')


def render_video(pid,cfg,output,duration=None,fps=60,width=1280,labels=True,crf=20):
    duration=_duration(cfg,duration)
    if fps not in (24,25,30,50,60): raise ValueError('fps must be 24,25,30,50 or 60')
    if width<320 or width>3840 or width%32: raise ValueError('width must be 320..3840 and divisible by 32 (16:9 canvas)')
    height=width*9//16; out=Path(output).resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    cfg=dict(cfg); cfg['_fps']=fps; cfg['_duration']=duration; n=round(duration*fps)
    alpha=bool(cfg.get('_transparent'))
    if alpha and out.suffix.lower()!='.mov': raise ValueError('transparent export requires a .mov output')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgba' if alpha else 'rgb24','-s',f'{width}x{height}','-r',str(fps),'-i','-','-an']
    if alpha: cmd+=['-c:v','prores_ks','-profile:v','4','-pix_fmt','yuva444p10le','-threads','2']
    else: cmd+=['-c:v','libx264','-preset','fast','-crf',str(crf),'-pix_fmt','yuv420p','-threads','2']
    cmd+=['-movflags','+faststart',str(out)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(n):
            im=frame(pid,i/fps,cfg,labels)
            if width!=W: im=im.resize((width,height),Image.Resampling.LANCZOS)
            proc.stdin.write(im.tobytes())
        proc.stdin.close(); code=proc.wait()
    except BaseException:
        proc.kill(); proc.wait(); raise
    if code: raise RuntimeError('FFmpeg failed '+str(code))
    return out


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--list',action='store_true'); ap.add_argument('--preset'); ap.add_argument('--config',type=Path)
    ap.add_argument('--output',default='motion-preset.mp4'); ap.add_argument('--duration',type=float)
    ap.add_argument('--fps',type=int); ap.add_argument('--width',type=int); ap.add_argument('--clean',action='store_true')
    ap.add_argument('--transparent',action='store_true',help='Export ProRes 4444 MOV with alpha, without catalogue labels')
    ap.add_argument('--frame',type=float,help='Export one PNG at this actual output time in seconds instead of MP4')
    a=ap.parse_args(); presets,_=registry()
    if a.list:
        print(json.dumps(presets,indent=2,ensure_ascii=False)); return
    raw=json.loads(a.config.read_text()) if a.config else {}
    if not isinstance(raw,dict): ap.error('configuration must be a JSON object')
    if a.config and raw.get('image_paths'):
        paths=raw['image_paths']; paths=[paths] if isinstance(paths,str) else paths
        raw['image_paths']=[str((a.config.resolve().parent/Path(p)).resolve()) for p in paths]
    for key in ('image_path','asset'):
        if a.config and raw.get(key): raw[key]=str((a.config.resolve().parent/Path(raw[key])).resolve())
    pid=a.preset or raw.get('preset')
    if not pid: ap.error('--preset or config.preset is required')
    if a.duration is not None: raw['duration']=a.duration
    cfg=configuration(pid,raw)
    if a.transparent: cfg['_transparent']=True
    duration=cfg['duration']; fps=a.fps or raw.get('fps',60); width=a.width or raw.get('width',1280)
    if a.frame is not None:
        cfg['_fps']=fps; cfg['_duration']=duration
        out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
        frame(pid,a.frame,cfg,not (a.clean or a.transparent)).save(out)
    else: out=render_video(pid,cfg,a.output,duration,fps,width,not (a.clean or a.transparent))
    print(str(out))
if __name__=='__main__': main()
