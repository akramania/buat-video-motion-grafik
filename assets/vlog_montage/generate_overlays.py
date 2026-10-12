"""Generate 100 original overlay MP4s, JSON recipes, screen-blend posters and QA.

Run from anywhere. Requires numpy, Pillow, ffmpeg and ffprobe; no downloaded assets.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from overlay_engine import frame

ROOT=Path(__file__).resolve().parent
W,H,FPS,DURATION=640,360,24,2
FAMILIES=[
 ("warm_leak","Light leak hangat","light-leak","amber",["Side spill","Top arc","Corner bloom","Opposing pair","Low haze"]),
 ("cool_leak","Light leak dingin","light-leak","teal",["Ocean edge","Sky spill","Mint corner","Cyan twin","Blue horizon"]),
 ("prism_sweep","Prism sweep","prism","violet",["Diagonal narrow","Rising beam","Vertical split","Falling spectrum","Wide horizontal"]),
 ("anamorphic_flare","Anamorphic flare","lens-flare","teal",["High horizon","Center runway","Low glow","Upper ghosts","Lower ghosts"]),
 ("lens_ring","Lens ghost rings","lens-flare","rose",["Triple drift","Quad halo","Double orbit","Prism rings","Wide lens"]),
 ("bokeh_drift","Bokeh terapung","bokeh","amber",["Cafe glow","Street lights","Celebration lights","Golden hour","Night market"]),
 ("dust_gate","Film dust & scratch","film-texture","silver",["Fine dust","Gate scratch","Dense specks","Twin scratch","Archive dust"]),
 ("film_grain","Film grain simulasi","film-texture","silver",["Fine 16mm","Soft 35mm","Directional grain","Bright speck grain","Pulsing grain"]),
 ("projector_flicker","Projector flicker","film-texture","amber",["Warm gate","Rapid shimmer","Archive reel","Dusty beam","Cinema pulse"]),
 ("scanline_roll","Rolling scanlines","analog","teal",["Fine raster","Medium raster","Wide raster","Retro bands","Broad scan"]),
 ("chromatic_glitch","Chromatic glitch","glitch","violet",["Signal burst","Channel drift","Packet bars","Band breakup","Digital storm"]),
 ("rain_window","Rain on window","weather","silver",["Fine drizzle","Soft rain","Night rain","Travel rain","Heavy beads"]),
 ("snowfall","Snow particles","weather","silver",["Light snowfall","Winter drift","Soft flakes","Dense snow","Snow globe"]),
 ("sparkle_trail","Sparkle trail","particles","rose",["Soft sparkle","Beauty sparkle","Gold dust stars","Celebration glints","Magical trail"]),
 ("ember_rise","Ember particles","particles","amber",["Campfire","Golden embers","Stage sparks","Copper rise","Warm festival"]),
 ("neon_ribbons","Neon light ribbons","abstract-light","violet",["Triple wave","Four wave","Soft sinusoid","Triple electric","Four ribbons"]),
 ("edge_glow","Frame edge glow","frame-glow","rose",["Thin halo","Soft border","Bloom edge","Dream glow","Ambient frame"]),
 ("crt_grid","CRT luminous grid","analog","teal",["Fine dot grid","Green monitor","Soft pixels","Wide phosphor","Retro panel"]),
 ("film_burn","Film burn sweep","film-texture","amber",["Left edge burn","Right flare burn","Sprocket glow","Right roll burn","Center rip"]),
 ("speed_streaks","Speed light streaks","speed","violet",["Horizontal rush","Rising rush","Falling rush","Diagonal lift","Diagonal drop"]),
]

def sample_background():
    x,y=np.meshgrid(np.linspace(0,1,W),np.linspace(0,1,H))
    arr=np.stack([18+34*(1-y),33+35*(1-y),55+35*(1-y)],axis=2).astype(np.uint8)
    im=Image.fromarray(arr);d=ImageDraw.Draw(im)
    d.ellipse((448,42,525,119),fill=(193,142,88))
    d.polygon([(0,235),(120,126),(263,236)],fill=(23,47,58))
    d.polygon([(147,260),(358,123),(520,251)],fill=(22,41,50))
    d.rectangle((0,246,W,H),fill=(20,44,51))
    for k in range(10):
        yy=251+k*10;d.line((30+17*k,yy,610-9*k,yy),fill=(37,67,67),width=2)
    d.rounded_rectangle((28,30,280,83),radius=12,fill=(17,29,42))
    font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:font=ImageFont.truetype(font_path,22)
    except OSError:font=ImageFont.load_default()
    d.text((43,44),"TRAVEL JOURNAL",fill=(231,234,225),font=font)
    return np.array(im)

def ffprobe(path):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-count_frames","-select_streams","v:0","-show_entries","stream=width,height,nb_read_frames,r_frame_rate:format=duration","-of","json",str(path)]))

def make_one(record):
    ident=record["id"];recipe=record.pop("recipe")
    out=ROOT/record["file"]
    (ROOT/record["files"][1]).write_text(json.dumps(recipe,indent=2)+"\n")
    command=["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","pipe:0","-an","-c:v","libx264","-preset","fast","-crf","20","-threads","1","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
    if not ("--verify-existing" in sys.argv and out.exists() and recipe['family']!='film_grain'):
        proc=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        for n in range(FPS*DURATION):proc.stdin.write(frame(recipe,n/FPS,W,H).tobytes())
        proc.stdin.close();error=proc.stderr.read().decode();code=proc.wait()
        if code:raise RuntimeError(error)
    candidates=[frame(recipe,t,W,H) for t in (0,.25,.5,.75,1,1.25,1.5,1.75)]
    poster=max(candidates,key=lambda a:float(np.mean(a)))
    base=sample_background().astype(np.float32)/255
    blended=(1-(1-base)*(1-poster.astype(np.float32)/255*.75))*255
    im=Image.fromarray(blended.clip(0,255).astype(np.uint8))
    d=ImageDraw.Draw(im);d.rectangle((0,322,W,H),fill=(11,19,28))
    try:f=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",12)
    except OSError:f=ImageFont.load_default()
    d.text((14,328),f"{ident}  {record['title']}",font=f,fill=(227,230,235))
    d.text((14,344),"SCREEN BLEND / PROCEDURAL SAMPLE BACKGROUND",font=f,fill=(129,168,185))
    im.save(ROOT/record["preview"],"WEBP",quality=88,method=4)
    # Decode every video frame, not only containers or key frames.
    decoded=subprocess.check_output(["ffmpeg","-v","error","-threads","1","-i",str(out),"-f","rawvideo","-pix_fmt","rgb24","pipe:1"])
    frames=np.frombuffer(decoded,dtype=np.uint8).reshape(-1,H,W,3)
    if len(frames)!=FPS*DURATION:raise AssertionError(f"Wrong frame count {ident}")
    a,b,c=frames[0],frames[FPS],frames[-1]
    change=float(np.mean(np.abs(a.astype(float)-b.astype(float))))
    last_change=float(np.mean(np.abs(a.astype(float)-c.astype(float))))
    active=float(np.mean(frames.max(axis=3)>12))
    endpoint=float(np.mean(np.abs(frame(recipe,0,W,H).astype(float)-frame(recipe,DURATION,W,H).astype(float))))
    info=ffprobe(out)
    if change < .003 or last_change < .001 or active < .0001 or endpoint > .001:
        raise AssertionError((ident,change,last_change,active,endpoint))
    return record,{"id":ident,"decoded_frames":len(frames),"active_fraction":round(active,6),"first_mid_mae":round(change,5),"first_last_mae":round(last_change,5),"procedural_loop_endpoint_mae":endpoint,"mp4_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),"bytes":out.stat().st_size,"ffprobe":info}

def main():
    (ROOT/"overlays").mkdir(exist_ok=True);(ROOT/"previews"/"overlays").mkdir(parents=True,exist_ok=True)
    records=[]
    for fi,(family,title,category,palette,names) in enumerate(FAMILIES):
        for vi,name in enumerate(names,1):
            idx=201+fi*5+vi-1;ident=f"VL{idx:04d}"
            recipe={"id":ident,"type":"overlay","engine":"overlay_engine.frame","family":family,"variant":vi,"seed":17021+idx*31,"palette":palette,"duration":DURATION,"width":W,"height":H,"fps":FPS,"blend":"screen","loopable":True,"original":True}
            records.append({"id":ident,"type":"overlay","title":f"{title} — {name}","category":category,"tags":[family,category,"vlog","montage","screen","original"],"use_cases":["vlogging","travel montage","cinematic B-roll"],"format":"mp4+json","file":f"overlays/{ident}.mp4","files":[f"overlays/{ident}.mp4",f"overlays/{ident}.json"],"preview":f"previews/overlays/{ident}.webp","preview_video":f"overlays/{ident}.mp4","duration":DURATION,"technical":{"blend":"screen","loopable":True,"resolution":[W,H],"fps":FPS,"audio":False,"opacity_recommendation":[.15,.65],"preview_background":"Original procedural travel scene; source MP4 is black-neutral","source":"original procedural RGB overlay; no stock footage"},"recipe":recipe})
    completed=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for i,(record,qa) in enumerate(pool.map(make_one,records),1):
            completed.append((record,qa))
            if i%10==0:print(f"Rendered and fully decoded {i}/100 overlays",flush=True)
    records=[x[0] for x in completed];qa=[x[1] for x in completed]
    hashes={x['mp4_sha256'] for x in qa}
    assert len(records)==100 and len(hashes)==100
    (ROOT/"index_overlays.json").write_text(json.dumps(records,ensure_ascii=False,indent=2)+"\n")
    report={"total":100,"mp4_count":100,"json_count":100,"poster_count":100,"unique_mp4_sha256":len(hashes),"full_decoded_frames":sum(x['decoded_frames'] for x in qa),"resolution":[W,H],"fps":FPS,"duration":DURATION,"loop_test":"frame(recipe,0)==frame(recipe,2) pixel-exact; decoded cycle ends at t=47/24, one frame before periodic endpoint","limitations":["MP4 previews/source overlays are 640×360. Render recipes at target resolution to avoid upscaling.","Screen blend brightens footage; apply opacity by taste.","These are original simulated textures, not scanned film or licensed stock."],"assets":qa}
    (ROOT/"overlays_qa.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"total":100,"decoded_frames":report['full_decoded_frames'],"unique_mp4":len(hashes),"bytes":sum(x['bytes'] for x in qa)}),flush=True)
if __name__=="__main__":main()
