#!/usr/bin/env python3
"""Find, copy or apply an original VL asset to local video footage.

Requires FFmpeg/ffprobe; procedural compositing also uses NumPy, Pillow and
CairoSVG for SVG. Renders SDR MP4, preserves source audio for single-clip
effects. A/B transitions render a silent transition segment. No camera Log
conversion, HDR processing, timeline editing or platform project export.
"""
import argparse, importlib, io, json, math, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent/'assets'/'vlog_montage'
TYPES=('lut','transition','overlay','vlog-graphic','montage-graphic','sfx')

def index():
    rows=[]
    for p in sorted(ROOT.glob('index_*.json')):
        data=json.loads(p.read_text(encoding='utf-8'))
        rows.extend(data.get('items',[]) if isinstance(data,dict) else data)
    ids=[r['id'] for r in rows]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate VL IDs')
    return sorted(rows,key=lambda r:r['id'])

def asset_path(name):
    p=(ROOT/name).resolve()
    if not p.is_relative_to(ROOT.resolve()):
        raise ValueError('Missing or invalid asset path: '+str(name))
    if not p.is_file() and (ROOT/'bundle_manifest.json').is_file():
        from prepare_vlog_assets import prepare
        prepare(ROOT)
    if not p.is_file():
        raise ValueError('Missing or invalid asset path: '+str(name))
    return p

def run(cmd):
    subprocess.run(cmd,check=True)

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))

def ffbase():return ['ffmpeg','-hide_banner','-loglevel','error','-y','-threads','1','-filter_threads','1','-filter_complex_threads','1']

def encoder_args():return ['-c:v','libx264','-threads','1','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart']

def video_info(p):
    info=probe(p)
    stream=next((s for s in info['streams'] if s['codec_type']=='video'),None)
    if stream is None:raise ValueError('Input must contain video')
    return info,stream,float(info.get('format',{}).get('duration',stream.get('duration',0)))

def decoder(p,w,h,fps,duration):
    fit=f'scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps}'
    return subprocess.Popen(ffbase()+['-i',str(p),'-t',str(duration),'-vf',fit,'-an','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)

def read_frame(proc,w,h):
    import numpy as np
    need=w*h*3;data=bytearray()
    while len(data)<need:
        chunk=proc.stdout.read(need-len(data))
        if not chunk:break
        data.extend(chunk)
    if len(data)!=need:raise ValueError('Footage ended before requested duration')
    return np.frombuffer(data,dtype=np.uint8).reshape(h,w,3).copy()

def procedural(row,args,info,w,h,duration):
    import numpy as np
    from PIL import Image
    sys.path.insert(0,str(ROOT))
    recipe=None; graphic=None
    if row['type']=='transition':
        engine=importlib.import_module('transition_engine')
        recipe=json.loads(asset_path(row['file']).read_text())
    elif row['type']=='overlay':
        engine=importlib.import_module('overlay_engine')
        recipe_file=next(f for f in row['files'] if f.endswith('.json'))
        recipe=json.loads(asset_path(recipe_file).read_text())
    else:
        import cairosvg
        png=cairosvg.svg2png(url=str(asset_path(row['file'])),output_width=w,output_height=round(w*360/640))
        layer=Image.open(io.BytesIO(png)).convert('RGBA')
        # Preserve the 16:9 artwork; fit inside another aspect ratio without crop.
        layer.thumbnail((w,h),Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',(w,h));canvas.alpha_composite(layer,((w-layer.width)//2,(h-layer.height)//2))
        graphic=np.asarray(canvas).astype(np.float32)/255
    frame_count=max(2,round(duration*args.fps))
    with tempfile.TemporaryDirectory(prefix='vl-render-') as temp:
        silent=Path(temp)/'video.mp4'
        a=decoder(args.input,w,h,args.fps,duration)
        b=decoder(args.input_b,w,h,args.fps,duration) if row['type']=='transition' else None
        out=subprocess.Popen(ffbase()+['-f','rawvideo','-pixel_format','rgb24','-video_size',f'{w}x{h}','-framerate',str(args.fps),'-i','pipe:0','-an']+encoder_args()+[str(silent)],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
        completed=False
        try:
            for i in range(frame_count):
                src=read_frame(a,w,h).astype(np.float32)/255
                if row['type']=='transition':
                    dst=read_frame(b,w,h).astype(np.float32)/255
                    matte=engine.mask_frame(recipe,i/(frame_count-1),w,h)[...,None]
                    result=src*(1-matte)+dst*matte
                elif row['type']=='overlay':
                    t=i/args.fps;clip_duration=float(row.get('duration',2))
                    if row.get('technical',{}).get('loopable'):t%=clip_duration
                    effect=engine.frame(recipe,t,w,h).astype(np.float32)/255 if t<clip_duration else np.zeros_like(src)
                    result=1-(1-src)*(1-effect*args.strength)
                else:
                    t=i/(frame_count-1)
                    fade=min(1,t*8,(1-t)*8) if args.animate else 1
                    alpha=graphic[...,3:]*args.strength*max(0,fade)
                    result=src*(1-alpha)+graphic[...,:3]*alpha
                out.stdin.write(np.clip(result*255+.5,0,255).astype(np.uint8).tobytes())
            out.stdin.close()
            if out.wait()!=0:raise RuntimeError('FFmpeg encoding failed')
            completed=True
        finally:
            for proc in (a,b,out):
                if proc is not None and proc.poll() is None:proc.terminate()
            for proc in (a,b,out):
                if proc is not None:proc.wait()
        if completed:
            has_audio=any(s['codec_type']=='audio' for s in info['streams'])
            if has_audio and row['type']!='transition':
                run(ffbase()+['-i',str(silent),'-i',str(args.input),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(frame_count/args.fps),'-movflags','+faststart',str(args.render)])
            else:shutil.copyfile(silent,args.render)

def render(row,args):
    info,stream,source_duration=video_info(args.input)
    duration=args.duration if args.duration is not None else (float(row.get('duration',1)) if row['type']=='transition' else source_duration)
    if not math.isfinite(duration) or not .05<=duration<=1800:raise ValueError('duration must be 0.05..1800 seconds')
    if duration>source_duration+1/args.fps:raise ValueError('Requested duration exceeds source clip')
    w=args.width or int(stream['width']);h=round(w*int(stream['height'])/int(stream['width']))
    w+=w%2;h+=h%2
    if not (32<=w<=8192 and 32<=h<=8192):raise ValueError('Output dimensions must be 32..8192')
    args.render=args.render.resolve();args.render.parent.mkdir(parents=True,exist_ok=True)
    if args.render.suffix.lower()!='.mp4':raise ValueError('render output must end in .mp4')
    if args.render==args.input.resolve() or (args.input_b and args.render==args.input_b.resolve()):raise ValueError('Use a separate output file')
    if row['type']=='lut':
        lut=asset_path(row['file'])
        # Generated asset paths have no filter delimiters; never interpolate user paths here.
        if any(c in str(lut) for c in "':,;[]\\"):raise ValueError('LUT asset path contains filter delimiters')
        vf=f"[0:v]scale={w}:{h},setsar=1,fps={args.fps},split[base][grade];[grade]lut3d=file='{lut}':interp=tetrahedral[graded];[base][graded]blend=all_expr='A*{1-args.strength}+B*{args.strength}'[v]"
        run(ffbase()+['-i',str(args.input),'-filter_complex',vf,'-map','[v]','-map','0:a?','-t',str(duration)]+encoder_args()+['-c:a','aac','-b:a','192k',str(args.render)])
    elif row['type']=='sfx':
        audio=any(s['codec_type']=='audio' for s in info['streams'])
        af=f'[1:a]volume={args.strength},apad[sfx];'+('[0:a][sfx]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.891:level=false:latency=1[a]' if audio else '[sfx]alimiter=limit=0.891:level=false:latency=1[a]')
        frame_count=max(1,round(duration*args.fps))
        vf=f'scale={w}:{h},setsar=1,fps={args.fps},trim=end_frame={frame_count},setpts=PTS-STARTPTS'
        run(ffbase()+['-i',str(args.input),'-i',str(asset_path(row['file'])),'-filter_complex',af,'-map','0:v:0','-map','[a]','-vf',vf]+encoder_args()+['-c:a','aac','-b:a','192k','-t',str(frame_count/args.fps),str(args.render)])
    else:
        if row['type']=='transition':
            if args.input_b is None:raise ValueError('Transition requires --input-b')
            _,_,bd=video_info(args.input_b)
            if duration>bd+1/args.fps:raise ValueError('Requested duration exceeds B clip')
        procedural(row,args,info,w,h,duration)
    print(str(args.render))

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--search',default='');ap.add_argument('--type',choices=['all',*TYPES],default='all')
    ap.add_argument('--id');ap.add_argument('--limit',type=int,default=20)
    ap.add_argument('--copy-to',type=Path);ap.add_argument('--render',type=Path)
    ap.add_argument('--input',type=Path);ap.add_argument('--input-b',type=Path)
    ap.add_argument('--duration',type=float);ap.add_argument('--width',type=int)
    ap.add_argument('--fps',type=int,default=30);ap.add_argument('--strength',type=float,default=1)
    ap.add_argument('--animate',action='store_true',help='Fade SVG graphics in and out')
    ap.add_argument('--prepare',action='store_true',help='Prepare the verified original asset collection before use')
    args=ap.parse_args()
    if args.limit<0:ap.error('limit must be nonnegative')
    if not 1<=args.fps<=120 or not math.isfinite(args.strength) or not 0<=args.strength<=1:ap.error('fps 1..120; strength 0..1')
    try:
        if args.prepare:
            from prepare_vlog_assets import prepare
            print(json.dumps(prepare(ROOT),ensure_ascii=False,indent=2))
            if not args.id and not args.search and args.type=='all':return
        rows=index()
        if args.id is None:
            if args.render or args.copy_to:ap.error('--id is required')
            q=args.search.casefold()
            rows=[r for r in rows if (args.type=='all' or r['type']==args.type) and q in ' '.join([r['id'],r['title'],r['category'],*r.get('tags',[]),*r.get('use_cases',[])]).casefold()]
            print(json.dumps(rows[:args.limit] if args.limit else rows,ensure_ascii=False,indent=2));return
        row=next((r for r in rows if r['id']==args.id),None)
        if row is None:ap.error('Unknown VL ID')
        if args.copy_to:
            args.copy_to.mkdir(parents=True,exist_ok=True)
            for name in row.get('files',[row['file']]):
                src=asset_path(name);dest=args.copy_to/src.name
                if src!=dest.resolve():shutil.copyfile(src,dest)
            print(str(args.copy_to.resolve()))
        if args.render:
            if args.input is None:ap.error('--input is required for render')
            render(row,args)
        if not args.render and not args.copy_to:print(json.dumps(row,ensure_ascii=False,indent=2))
    except (ValueError,RuntimeError,subprocess.CalledProcessError,ImportError) as e:ap.error(str(e))

if __name__=='__main__':main()
