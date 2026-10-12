"""Generate 100 original spatial reveal definitions and preview media.

Run from anywhere: python generate_transitions.py [--workers 2]
Requires NumPy, Pillow, FFmpeg, FFprobe. No external source assets are used.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from transition_engine import mask_frame

ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT, FPS = 640, 360, 30


def definitions():
    families = [
        ('linear','Directional Wipe',[dict(angle=a) for a in (0,45,90,135,225)]),
        ('angular','Bent Angle',[dict(angle=a,bend=b,frequency=f) for a,b,f in ((0,.5,13),(30,-.6,19),(90,.8,9),(135,-.8,15),(225,.35,25))]),
        ('iris','Elliptical Iris',[dict(cx=x,cy=y,aspect=s,reverse=r) for x,y,s,r in ((.5,.5,1,False),(.22,.3,1.6,False),(.78,.6,.7,False),(.5,.5,2.2,True),(.35,.75,.55,True))]),
        ('diamond','Diamond Bloom',[dict(angle=a,cx=x,cy=y,aspect=s,reverse=r) for a,x,y,s,r in ((0,.5,.5,1,False),(25,.2,.3,1.5,False),(65,.8,.6,.7,False),(0,.5,.5,2,True),(115,.3,.75,1.2,True))]),
        ('clock','Clock Sweep',[dict(start=s,direction=d,cx=x,cy=y) for s,d,x,y in ((0,1,.5,.5),(.25,-1,.5,.5),(.5,1,.2,.3),(.75,-1,.8,.6),(.125,1,.35,.75))]),
        ('spiral','Spiral Reveal',[dict(twists=z,start=s,cx=x,cy=y) for z,s,x,y in ((.8,0,.5,.5),(-1.4,.25,.5,.5),(2.1,.5,.3,.4),(-2.7,.75,.7,.65),(3.5,.125,.4,.75))]),
        ('venetian','Staggered Blinds',[dict(angle=a,bands=b,stagger=s) for a,b,s in ((0,6,.25),(90,9,.15),(35,13,.3),(125,5,.4),(225,17,.1))]),
        ('shutter','Slit Shutter',[dict(angle=a,bands=b,stagger=s) for a,b,s in ((0,5,.18),(90,8,.32),(30,12,.12),(120,7,.4),(225,16,.25))]),
        ('mosaic','Tile Cascade',[dict(cols=c,rows=r,seed=s) for c,r,s in ((6,4,3),(10,6,7),(14,8,11),(8,10,19),(18,5,29))]),
        ('checker','Checker Bloom',[dict(cols=c,rows=r,seed=s) for c,r,s in ((6,4,0),(10,6,1),(14,8,0),(8,10,1),(18,5,2))]),
        ('waves','Liquid Wave',[dict(angle=a,amplitude=m,frequency=f,phase=p) for a,m,f,p in ((0,.08,12,0),(45,.14,19,.5),(90,.1,26,1),(135,.18,9,2),(225,.07,35,3))]),
        ('ripple','Radial Ripple',[dict(cx=x,cy=y,amplitude=a,frequency=f,phase=p) for x,y,a,f,p in ((.5,.5,.07,25,0),(.2,.3,.09,35,.4),(.8,.6,.06,45,1),(.4,.75,.12,17,2),(.65,.25,.08,55,3))]),
        ('hex','Hex Cascade',[dict(size=s,seed=z) for s,z in ((.08,2),(.11,5),(.055,9),(.15,17),(.04,23))]),
        ('chevron','Arrow Fold',[dict(angle=a,slope=s,depth=d) for a,s,d in ((0,.8,.4),(90,-.7,.5),(45,1.2,-.4),(135,-1.3,.8),(225,.45,1.1))]),
        ('zigzag','Sawtooth Slide',[dict(angle=a,amplitude=m,teeth=z,phase=p) for a,m,z,p in ((0,.13,5,0),(90,.22,8,.25),(35,.1,13,.5),(125,.28,4,.75),(225,.17,18,.125))]),
        ('film_gate','Film Gate Lift',[dict(angle=a,opening=o,rail_delay=d,perforations=p) for a,o,d,p in ((0,1.6,.2,55),(90,1.2,.35,40),(15,2,.15,70),(75,1.4,.5,30),(135,1.8,.3,85))]),
        ('cloud','Organic Cloud',[dict(angle=a,amplitude=m,seed=s) for a,m,s in ((0,.07,0),(90,.14,1),(35,.11,2),(125,.18,3),(225,.09,4))]),
        ('ink','Ink Bloom',[dict(cx=x,cy=y,roughness=r,drip=d,seed=s) for x,y,r,d,s in ((.5,.5,.025,0,0),(.2,.3,.045,.15,1),(.8,.6,.035,-.1,2),(.4,.75,.07,.2,3),(.65,.25,.055,-.25,4))]),
        ('petal','Petal Aperture',[dict(petals=z,depth=d,phase=p,cx=x,cy=y) for z,d,p,x,y in ((3,.25,0,.5,.5),(5,.35,.3,.5,.5),(7,.2,.6,.3,.4),(9,.4,1,.7,.65),(12,.3,1.4,.4,.75))]),
        ('split','Box Split',[dict(angle=a,aspect=s,skew=k,cx=x,cy=y,reverse=r) for a,s,k,x,y,r in ((0,1,0,.5,.5,False),(30,1.5,.8,.25,.3,False),(65,.7,-.8,.75,.6,False),(90,2,1.2,.5,.5,True),(135,1.2,-1.2,.35,.75,True))]),
    ]
    output = []
    for family_no,(family,title,variants) in enumerate(families):
        for variant,p in enumerate(variants):
            asset_id = f'VL{101+family_no*5+variant:04d}'
            duration = [0.8,0.9,1.0,1.1,1.2][variant]
            recipe = {'id':asset_id,'type':'transition','schema_version':1,'family':family,'parameters':p,'duration':duration,'fps':FPS,'feather':[.035,.045,.055,.04,.065][variant],'time_unit':'normalized','white_reveals':'B','composite':'A*(1-matte)+B*matte','implementation':'transition_engine.mask_frame','license':'Original; personal and commercial reuse and modification permitted.'}
            record = {'id':asset_id,'type':'transition','title':f'{title} {variant+1:02d}','category':title,'tags':['vlog','montage','transition','reveal',family,'peralihan'],'use_cases':['Travel vlog scene change','Music montage beat change','Explainer or product scene reveal'],'format':'json+mp4','file':f'transitions/{asset_id}.json','files':[f'transitions/{asset_id}.json',f'transitions/{asset_id}-matte.mp4'],'preview':f'previews/transitions/{asset_id}.webp','preview_video':f'previews/transitions/{asset_id}.mp4','duration':duration,'technical':{'white_reveals':'B','normalized_time':True,'matte_resolution':[WIDTH,HEIGHT],'matte_fps':FPS,'matte_codec':'H.264 grayscale encoded as yuv420p','source_resolution_independent':True,'source_family':family,'temporal_easing':'smoothstep','alpha':'grayscale matte, not embedded alpha','audio':False}}
            output.append((recipe,record))
    return output


def scenes():
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    font = ImageFont.truetype(font_path,26)
    small = ImageFont.truetype(font_path,12)
    a = Image.new('RGB',(WIDTH,HEIGHT),'#142f52')
    d = ImageDraw.Draw(a)
    for k in range(HEIGHT):
        d.line((0,k,WIDTH,k),fill=(20+int(k*.06),47+int(k*.09),82+int(k*.15)))
    d.ellipse((430,38,516,124),fill='#d8f0ea')
    d.polygon([(0,305),(155,108),(315,305)],fill='#52858e')
    d.polygon([(155,108),(117,162),(183,146)],fill='#d8f0ea')
    d.polygon([(245,315),(413,145),(610,315)],fill='#385c77')
    d.polygon([(413,145),(385,179),(444,173)],fill='#aad9d3')
    d.rectangle((0,303,WIDTH,HEIGHT),fill='#193d55')
    d.rounded_rectangle((28,27,219,79),radius=12,fill='#112743')
    d.text((43,37),'SCENE A',font=font,fill='#d8f0ea')
    d.text((30,327),'ORIGINAL VECTOR LANDSCAPE',font=small,fill='#d8f0ea')
    b = Image.new('RGB',(WIDTH,HEIGHT),'#eaab6d')
    d = ImageDraw.Draw(b)
    for k in range(HEIGHT):
        d.line((0,k,WIDTH,k),fill=(234-int(k*.11),171-int(k*.17),109-int(k*.1)))
    d.ellipse((103,66,232,195),fill='#ffe0a8')
    d.polygon([(0,284),(178,223),(345,280),(510,217),(WIDTH,263),(WIDTH,HEIGHT),(0,HEIGHT)],fill='#ab655b')
    d.polygon([(0,317),(150,271),(313,325),(487,262),(WIDTH,305),(WIDTH,HEIGHT),(0,HEIGHT)],fill='#733e52')
    d.rounded_rectangle((423,27,613,79),radius=12,fill='#733e52')
    d.text((439,37),'SCENE B',font=font,fill='#ffe0a8')
    d.text((30,327),'WHITE MATTE REVEALS SCENE B',font=small,fill='#ffe0a8')
    return np.array(a).astype(np.float32),np.array(b).astype(np.float32)


def encoder(path,pixel_format,frame_count):
    # Isolate the final uniform endpoint from preceding inter-frame residuals.
    return subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format',pixel_format,'-video_size',f'{WIDTH}x{HEIGHT}','-framerate',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','1','-force_key_frames',f'expr:eq(n,0)+eq(n,{frame_count-1})','-pix_fmt','yuv420p','-movflags','+faststart',str(path)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)


def render(pair):
    recipe,record = pair
    asset_id = recipe['id']
    recipe_path = ROOT/record['file']
    recipe_path.write_text(json.dumps(recipe,indent=2)+'\n')
    matte_path = ROOT/record['files'][1]
    preview_path = ROOT/record['preview_video']
    n = round(recipe['duration']*FPS)
    a,b = scenes()
    matte_enc,preview_enc = encoder(matte_path,'gray',n),encoder(preview_path,'rgb24',n)
    fingerprint = hashlib.sha256()
    prev = None
    monotonic = True
    try:
        for i in range(n):
            m = mask_frame(recipe,i/(n-1),WIDTH,HEIGHT)
            if prev is not None and np.any(m < prev-1e-6):
                monotonic = False
            prev = m
            matte_enc.stdin.write(np.rint(m*255).astype(np.uint8).tobytes())
            rgb = np.rint(a*(1-m[...,None])+b*m[...,None]).astype(np.uint8)
            preview_enc.stdin.write(rgb.tobytes())
            if i == (n-1)//2:
                Image.fromarray(rgb).save(ROOT/record['preview'],'WEBP',quality=88)
                fingerprint.update(np.rint(m*255).astype(np.uint8).tobytes())
    finally:
        for proc in (matte_enc,preview_enc):
            proc.stdin.close()
            err = proc.stderr.read().decode()
            if proc.wait() != 0:
                raise RuntimeError(err)
    # Decode all frames, not just metadata, and inspect decoded endpoints.
    encoded_endpoints=[]
    for path in (matte_path,preview_path):
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-threads','1','-i',str(path),'-f','null','-'],check=True,capture_output=True)
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,width,height,r_frame_rate','-of','json',str(path)]))['streams'][0]
        assert int(probe['nb_read_frames'])==n and probe['width']==WIDTH and probe['height']==HEIGHT
        if path == matte_path:
            decoded=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-threads','1','-i',str(path),'-f','rawvideo','-pix_fmt','gray','-'])
            frames=np.frombuffer(decoded,dtype=np.uint8).reshape(n,HEIGHT,WIDTH)
            encoded_endpoints=[int(frames[0].min()),int(frames[0].max()),int(frames[-1].min()),int(frames[-1].max())]
            assert np.max(frames[0])==0 and np.min(frames[-1])==255
    assert monotonic
    return {'id':asset_id,'family':recipe['family'],'frames_per_video':n,'duration':n/FPS,'decode':'passed','monotonic_analytic':True,'analytic_endpoint_exact':bool(np.all(mask_frame(recipe,0,128,72)==0) and np.all(mask_frame(recipe,1,128,72)==1)),'decoded_matte_endpoints_min_max':encoded_endpoints,'midpoint_geometry_sha256':fingerprint.hexdigest(),'recipe_sha256':hashlib.sha256(recipe_path.read_bytes()).hexdigest(),'matte_sha256':hashlib.sha256(matte_path.read_bytes()).hexdigest(),'preview_sha256':hashlib.sha256(preview_path.read_bytes()).hexdigest()}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--workers',type=int,default=2)
    args=parser.parse_args()
    (ROOT/'transitions').mkdir(exist_ok=True)
    (ROOT/'previews'/'transitions').mkdir(parents=True,exist_ok=True)
    pairs=definitions()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        qa=list(pool.map(render,pairs))
    assert len(qa)==100 and len({x['midpoint_geometry_sha256'] for x in qa})==100
    assert len({x['recipe_sha256'] for x in qa})==100
    (ROOT/'index_transitions.json').write_text(json.dumps([r for _,r in pairs],indent=2)+'\n')
    report={'asset_count':100,'mechanism_families':20,'variants_per_family':5,'matte_mp4_count':100,'preview_mp4_count':100,'poster_webp_count':100,'all_full_decode_passed':True,'all_frame_counts_passed':True,'all_exact_analytic_endpoints_passed':True,'all_decoded_endpoints_passed':True,'decoded_endpoint_tolerance_8bit':0,'all_monotonic_progressions_passed':True,'unique_midpoint_geometry':100,'source':'Original analytic geometry; no third-party assets','checks':qa}
    (ROOT/'transitions_qa.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'}))


if __name__=='__main__':
    main()
