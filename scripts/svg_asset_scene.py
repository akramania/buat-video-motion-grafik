#!/usr/bin/env python3
"""Compose real bundled SVG elements into transparent PNGs or silent opaque MP4s.

Usage:
  python scripts/svg_asset_scene.py --scene scene.json --output frame.png --frame 2
  python scripts/svg_asset_scene.py --scene scene.json --output scene.mp4
Example JSON:
  {"width":1280,"height":720,"duration":6,"fps":30,"background":"#101722",
   "assets":[{"id":"SV0001","x":100,"y":100,"width":240,"start":0,"end":6,
              "entrance":0.5,"exit":0.4,"ambient":"float"}]}
IDs SV1..SV1500 resolve to existing SV0001.svg..SV1500.svg files; an absent ID
is an error. SVG aspect ratio and alpha are preserved. x/y are nominal top-left
coordinates; entry rises 24 px to that placement, float moves at most 4 px,
and pulse scales at most 2% around the asset center. Layer times are clamped
to the scene; overlapping entrance/exit durations shrink proportionally.
background="transparent" is supported for PNG only; MP4 requires #RRGGBB.
PNG requires --frame in seconds, inclusive 0..duration. MP4 rejects --frame.
Dependencies: Pillow, CairoSVG; MP4 additionally needs FFmpeg with libx264.
"""
import argparse, io, json, math, re, shutil, subprocess
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image

FILES = Path(__file__).resolve().parent.parent/'assets'/'svg_elements'/'files'

def number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{name} must be a finite number')
    return float(value)

def dimension(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 8192:
        raise ValueError(f'{name} must be an integer from 1 to 8192')
    return value

def clamp(value, low, high): return max(low, min(high, value))
def ease(value): return 1-(1-clamp(value, 0., 1.))**3
def smooth(value):
    value=clamp(value, 0., 1.); return value*value*(3-2*value)

def asset_id(value, name):
    match=re.fullmatch(r'SV(\d{1,4})', value) if isinstance(value, str) else None
    if not match or not 1 <= int(match[1]) <= 1500:
        raise ValueError(f'{name} must be an SVG ID from SV0001 to SV1500')
    pid=f'SV{int(match[1]):04d}'; source=FILES/(pid+'.svg')
    if not source.is_file(): raise ValueError(f'{name}: unknown asset {pid}; bundled file {source} is missing')
    return pid, source

class Scene:
    """Compiled local scene; each source SVG is rasterized once at its target size."""
    def __init__(self, data):
        if not isinstance(data, dict): raise ValueError('scene must be a JSON object')
        self.width=dimension(data.get('width',1280),'width')
        self.height=dimension(data.get('height',720),'height')
        self.duration=number(data.get('duration',6),'duration')
        if not .1 <= self.duration <= 1800: raise ValueError('duration must be from 0.1 to 1800 seconds')
        self.fps=data.get('fps',30)
        if isinstance(self.fps,bool) or not isinstance(self.fps,int) or not 1 <= self.fps <= 120:
            raise ValueError('fps must be an integer from 1 to 120')
        self.background=data.get('background','#101722')
        if self.background!='transparent' and not (isinstance(self.background,str) and re.fullmatch(r'#[0-9a-fA-F]{6}',self.background)):
            raise ValueError('background must be #RRGGBB or "transparent"')
        rows=data.get('assets',[])
        if not isinstance(rows,list) or len(rows)>1500: raise ValueError('assets must be an array of at most 1500 layer objects')
        self.assets=[]; cache={}
        for i, row in enumerate(rows):
            label=f'assets[{i}]'
            if not isinstance(row,dict): raise ValueError(f'{label} must be an object')
            pid,source=asset_id(row.get('id'),label+'.id')
            width=dimension(row.get('width',240),label+'.width')
            x=number(row.get('x',0),label+'.x'); y=number(row.get('y',0),label+'.y')
            start=clamp(number(row.get('start',0),label+'.start'),0,self.duration)
            end=clamp(number(row.get('end',self.duration),label+'.end'),start,self.duration)
            span=end-start
            entrance=clamp(number(row.get('entrance',.5),label+'.entrance'),0,span)
            exit_time=clamp(number(row.get('exit',.4),label+'.exit'),0,span)
            if entrance+exit_time>span and span>0:
                factor=span/(entrance+exit_time); entrance*=factor; exit_time*=factor
            ambient=row.get('ambient','none')
            if ambient not in ('float','pulse','none'): raise ValueError(f'{label}.ambient must be float, pulse, or none')
            key=(pid,width)
            if key not in cache:
                svg=source.read_bytes()
                try:
                    box=ET.fromstring(svg).get('viewBox','').replace(',',' ').split()
                    values=[float(z) for z in box]
                    if len(values)!=4 or not all(math.isfinite(z) for z in values) or min(values[2:])<=0: raise ValueError()
                    height=round(width*values[3]/values[2])
                except (ET.ParseError,ValueError): raise ValueError(f'{pid}: bundled SVG has an invalid viewBox') from None
                if not 1<=height<=8192: raise ValueError(f'{label}.width produces an SVG height outside 1..8192 pixels')
                try: import cairosvg
                except ImportError: raise RuntimeError('SVG rendering requires CairoSVG; run in a Python environment with CairoSVG and Pillow') from None
                try: blob=cairosvg.svg2png(bytestring=svg,output_width=width,output_height=height)
                except Exception as error: raise RuntimeError(f'{pid}: SVG rasterization failed: {error}') from error
                cache[key]=Image.open(io.BytesIO(blob)).convert('RGBA')
            self.assets.append(dict(id=pid,image=cache[key],x=x,y=y,start=start,end=end,entrance=entrance,exit=exit_time,ambient=ambient))

    def frame(self, seconds):
        seconds=number(seconds,'frame')
        if not 0<=seconds<=self.duration: raise ValueError(f'frame must be from 0 to {self.duration:g} seconds')
        color=(0,0,0,0) if self.background=='transparent' else self.background
        canvas=Image.new('RGBA',(self.width,self.height),color)
        for row in self.assets:
            if seconds<row['start'] or seconds>=row['end']: continue
            elapsed=seconds-row['start']; remaining=row['end']-seconds
            entry=ease(elapsed/row['entrance']) if row['entrance']>0 else 1.
            out=1-smooth(1-remaining/row['exit']) if row['exit']>0 else 1.
            alpha=entry*out
            if alpha<=0: continue
            image=row['image']; x=row['x']; y=row['y']+24*(1-entry)
            if row['ambient']=='float': y+=4*math.sin(elapsed*math.tau/3)*entry
            elif row['ambient']=='pulse':
                scale=1+.02*math.sin(elapsed*math.tau/3)*entry
                size=(max(1,round(image.width*scale)),max(1,round(image.height*scale)))
                x-=(size[0]-image.width)/2; y-=(size[1]-image.height)/2
                image=image.resize(size,Image.Resampling.LANCZOS)
            if alpha<1:
                image=image.copy(); image.putalpha(image.getchannel('A').point(lambda v:round(v*alpha)))
            canvas.alpha_composite(image,(round(x),round(y)))
        return canvas

def export(scene, output, frame=None):
    output=Path(output).resolve(); suffix=output.suffix.lower()
    if suffix not in ('.png','.mp4'): raise ValueError('output must end in .png or .mp4')
    if suffix=='.png':
        if frame is None: raise ValueError('PNG output requires --frame SECONDS')
        image=scene.frame(frame); output.parent.mkdir(parents=True,exist_ok=True); image.save(output); return output
    if frame is not None: raise ValueError('--frame is only valid for PNG output')
    if scene.background=='transparent': raise ValueError('MP4 cannot preserve alpha; set background to an opaque #RRGGBB, or export PNG')
    if scene.width%2 or scene.height%2: raise ValueError('MP4 width and height must both be even for yuv420p')
    ffmpeg=shutil.which('ffmpeg')
    if not ffmpeg: raise RuntimeError('MP4 output requires FFmpeg with libx264 on PATH')
    output.parent.mkdir(parents=True,exist_ok=True)
    command=[ffmpeg,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{scene.width}x{scene.height}',
             '-r',str(scene.fps),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',str(output)]
    process=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(max(1,round(scene.duration*scene.fps))): process.stdin.write(scene.frame(i/scene.fps).convert('RGB').tobytes())
        process.stdin.close(); errors=process.stderr.read().decode('utf-8','replace'); code=process.wait()
    except BaseException:
        if process.poll() is None: process.kill()
        process.wait(); raise
    finally: process.stderr.close()
    if code: raise RuntimeError(f'FFmpeg failed ({code}): {errors.strip()}')
    return output

def main():
    parser=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--scene',type=Path,required=True,help='local scene JSON file')
    parser.add_argument('--output',type=Path,required=True,help='PNG or silent MP4 output')
    parser.add_argument('--frame',type=float,help='PNG frame time in seconds')
    args=parser.parse_args()
    try:
        data=json.loads(args.scene.read_text(encoding='utf-8')); output=export(Scene(data),args.output,args.frame)
    except (ValueError,OSError,RuntimeError) as error: parser.error(str(error))
    print(output)

if __name__=='__main__': main()
