#!/usr/bin/env python3
"""Composite multiple actual Atlas animations with scene-local clocks into MP4."""
import argparse
import json
from pathlib import Path
import subprocess
from atlas_preset import AtlasLibrary, AtlasPreset

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    spec=json.loads(a.config.read_text())
    width,height=spec.get('size',[1920,1080]);fps=spec.get('fps',30);duration=spec['duration']
    if any(not isinstance(v,int) or v<=0 or v%2 for v in (width,height)) or fps not in (24,25,30,50,60) or not 0<duration<=1800:
        raise ValueError('Use positive even dimensions, supported fps and duration <=1800s')
    from PIL import Image,ImageOps
    library=AtlasLibrary()
    if spec.get('font'):raise ValueError('Global font override unsupported')
    palette=spec.get('palette','cream');theme=spec.get('theme','soft')
    bg=spec.get('bg','#F8F3E8')
    layers=[]
    for item in spec['layers']:
        start,end=item['start'],item['end']
        if not 0<=start<end<=duration:raise ValueError('Layer must lie within timeline')
        job=(a.config.resolve().parent/item['job']).resolve()
        raw=json.loads(job.read_text());raw['output']['duration']=end-start
        if raw.get('mode')!='native':raise ValueError('Render footage layers with atlas_preset first')
        if 'transparent' in item:raw['output']['transparent']=bool(item['transparent'])
        cfg=AtlasPreset(raw,library,job.parent)
        rect=item.get('rect',[0,0,width,height]);x,y,w,h=rect
        if any(not isinstance(v,int) for v in rect) or w<=0 or h<=0 or x<0 or y<0 or x+w>width or y+h>height:
            raise ValueError('Invalid pixel rect')
        layers.append((item,cfg))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x{height}','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(a.output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(round(duration*fps)):
            t=i/fps;canvas=Image.new('RGBA',(width,height),bg)
            for item,cfg in layers:
                if not item['start']<=t<item['end']:continue
                frame=cfg.frame(t-item['start']).convert('RGBA')
                x,y,w,h=item.get('rect',[0,0,width,height])
                # Preserve native 16:9 artwork; never stretch limbs or clip text.
                frame=ImageOps.contain(frame,(w,h),Image.Resampling.LANCZOS)
                canvas.alpha_composite(frame,(x+(w-frame.width)//2,y+(h-frame.height)//2))
            proc.stdin.write(canvas.convert('RGB').tobytes())
        proc.stdin.close()
        if proc.wait():raise RuntimeError('FFmpeg composition failed')
    except BaseException:
        proc.kill();proc.wait();raise
    print(a.output)

if __name__=='__main__':main()
