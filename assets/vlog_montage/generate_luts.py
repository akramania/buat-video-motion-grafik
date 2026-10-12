#!/usr/bin/env python3
"""Generate 100 original creative SDR Rec.709 3D .cube LUTs and real previews.

Each LUT is a 33-cube: red varies fastest, green next, blue slowest. Input
and output are normalized gamma-encoded Rec.709 RGB, not camera Log or HDR.
The original procedural preview is an analytical illustration/test chart,
not a photograph and not a camera calibration target. It has no stock assets.

Dependencies: Python, numpy, Pillow, FFmpeg for optional compatibility QA.
Run: python generate_luts.py [--ffmpeg-qa]
All code, LUT tables and procedural artwork in this file are original and
may be reused/modified in personal or commercial video projects.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SIZE = 33
WEIGHTS = np.array([0.2126, 0.7152, 0.0722], dtype=np.float64)

# 20 independently art-directed base recipes; variants tune their tonal use.
FAMILIES = [
    dict(name="Amber Diary", category="Everyday warm", sat=1.02, contrast=1.07, temp=.020, tint=.000, lift=.005, shadow=[.004,-.002,-.006], highlight=[.015,.006,-.012], selective=[.000,-.004,.005], use="daily diaries, home routines, warm travel memories"),
    dict(name="Coastal Air", category="Coastal travel", sat=1.07, contrast=.97, temp=-.014, tint=-.006, lift=.010, shadow=[-.012,.005,.016], highlight=[.010,.012,.015], selective=[-.013,.018,.017], use="beach trips, water sports, island montages"),
    dict(name="Alpine Pine", category="Nature travel", sat=.89, contrast=1.11, temp=-.012, tint=.005, lift=.005, shadow=[-.006,.009,.011], highlight=[.006,.005,-.004], selective=[.005,-.014,-.004], use="forest hikes, mountains, outdoor journals"),
    dict(name="Tropical Pop", category="Nature vivid", sat=1.16, contrast=1.04, temp=.010, tint=-.003, lift=.000, shadow=[-.003,.006,.009], highlight=[.010,.012,-.003], selective=[-.012,.023,-.007], use="tropical holidays, parks, vivid destination reels"),
    dict(name="Desert Rose", category="Warm pastel", sat=.87, contrast=.94, temp=.020, tint=.004, lift=.025, shadow=[.012,.002,.005], highlight=[.017,.006,-.009], selective=[.014,-.005,-.004], use="sand landscapes, road trips, soft warm montages"),
    dict(name="Urban Steel", category="Urban cool", sat=.84, contrast=1.19, temp=-.020, tint=-.002, lift=.002, shadow=[-.013,.001,.012], highlight=[-.004,.005,.010], selective=[-.005,.002,.012], use="city walks, architecture, high contrast urban b-roll"),
    dict(name="Neon Nights", category="Night colour", sat=1.03, contrast=1.08, temp=-.011, tint=.013, lift=.006, shadow=[.006,-.010,.019], highlight=[.012,-.004,.007], selective=[.010,-.014,.016], use="night streets, concert diaries, neon city montages"),
    dict(name="Cafe Mocha", category="Food warm", sat=.86, contrast=1.06, temp=.025, tint=.002, lift=.014, shadow=[.010,.002,-.005], highlight=[.013,.003,-.010], selective=[.013,-.004,-.006], use="cafe visits, coffee preparation, cozy food vlogs"),
    dict(name="Food Fresh", category="Food vivid", sat=1.12, contrast=1.06, temp=.008, tint=-.002, lift=.001, shadow=[-.001,.003,.002], highlight=[.010,.006,-.006], selective=[.021,.012,-.004], use="cooking closeups, fruit, fresh food promotional montages"),
    dict(name="Golden Wedding", category="Wedding warm", sat=.93, contrast=.91, temp=.022, tint=.005, lift=.016, shadow=[.008,.002,.001], highlight=[.023,.009,-.011], selective=[.009,-.007,-.002], use="weddings, romantic celebrations, golden hour portraits"),
    dict(name="Pearl Portrait", category="Portrait soft", sat=.89, contrast=.93, temp=.005, tint=.004, lift=.012, shadow=[.004,.002,.004], highlight=[.010,.008,.011], selective=[.006,-.006,.002], use="talking heads, beauty routines, gentle portrait montages"),
    dict(name="Retro Print", category="Retro colour", sat=.82, contrast=.95, temp=.010, tint=-.006, lift=.027, shadow=[-.003,.010,.014], highlight=[.021,.013,-.012], selective=[.012,-.010,-.003], use="memory reels, nostalgic travel, diary chapters"),
    dict(name="Vintage Sepia", category="Monochrome warm", sat=.14, contrast=1.03, temp=.015, tint=.001, lift=.018, shadow=[.011,.004,-.002], highlight=[.020,.007,-.011], selective=[.000,.000,.000], monochrome="sepia", use="heritage walks, archival style memory montages"),
    dict(name="Silver B&W", category="Monochrome neutral", sat=0., contrast=1.14, temp=0., tint=0., lift=.004, shadow=[0.,0.,0.], highlight=[0.,0.,0.], selective=[0.,0.,0.], monochrome="neutral", use="documentary vlogs, expressive portrait and rhythm montages"),
    dict(name="Matte Street", category="Matte urban", sat=.78, contrast=1.04, temp=-.004, tint=.005, lift=.040, shadow=[.006,.006,.013], highlight=[.008,.004,-.001], selective=[.003,-.011,.008], use="streetwear, skate diaries, low contrast lifestyle reels"),
    dict(name="Teal Cinema", category="Cinematic split", sat=.91, contrast=1.17, temp=.003, tint=-.004, lift=.004, shadow=[-.014,.010,.019], highlight=[.023,.007,-.014], selective=[.006,.011,.015], use="dramatic travel edits, action and cinematic montages"),
    dict(name="Sunset Stories", category="Sunset warm", sat=1.03, contrast=.97, temp=.027, tint=.009, lift=.012, shadow=[.013,-.002,.011], highlight=[.030,.011,-.017], selective=[.016,-.008,-.010], use="sunset walks, golden skies, emotive travel diaries"),
    dict(name="Winter Blue", category="Cool pastel", sat=.82, contrast=.92, temp=-.021, tint=.002, lift=.020, shadow=[-.005,.006,.018], highlight=[.003,.008,.014], selective=[-.004,-.006,.016], use="snow trips, winter cities, calm cool montages"),
    dict(name="Adventure Crisp", category="Action crisp", sat=1.11, contrast=1.20, temp=.002, tint=-.002, lift=.000, shadow=[-.002,.000,.004], highlight=[.008,.006,.002], selective=[.002,.013,.005], use="hiking, cycling, energetic outdoor montages"),
    dict(name="Clean Montage", category="Clean neutral", sat=1.02, contrast=1.06, temp=.000, tint=.000, lift=.001, shadow=[.001,.001,.001], highlight=[.004,.004,.004], selective=[.000,.000,.000], use="mixed footage, everyday montages, clean product b-roll"),
]

# Distinct tonal targets, rather than five identical LUTs with renamed files.
VARIANTS = [
    dict(name="Balanced", use="balanced exposure and daylight footage", exposure=0., contrast=0., sat=0., lift=0., knee=0., temp=0., tint=0., shadow=0.),
    dict(name="Backlight", use="gentle shadow lift and highlight compression for backlit scenes", exposure=.015, contrast=-.045, sat=-.018, lift=.009, knee=.024, temp=.003, tint=0., shadow=.006),
    dict(name="Indoor", use="subtly cooler white balance for warm indoor footage", exposure=.010, contrast=-.020, sat=.015, lift=.003, knee=.008, temp=-.014, tint=.002, shadow=.002),
    dict(name="Lowlight", use="open shadows with restrained saturation for darker footage", exposure=.045, contrast=-.055, sat=-.040, lift=.013, knee=.012, temp=-.003, tint=.001, shadow=.010),
    dict(name="Bold", use="stronger midtone separation for energetic rhythmic edits", exposure=-.010, contrast=.065, sat=.035, lift=-.002, knee=-.004, temp=.002, tint=-.001, shadow=-.003),
]


def rec709_decode(x):
    return np.where(x < .081, x / 4.5, ((x + .099) / 1.099) ** (1 / .45))


def rec709_encode(x):
    x = np.clip(x, 0., 1.)
    return np.where(x < .018, 4.5 * x, 1.099 * x ** .45 - .099)


def grade(rgb, family, variant):
    """Art-directed exposure, luma curve, split tone and selective chroma."""
    temp = family["temp"] + variant["temp"]
    tint = family["tint"] + variant["tint"]
    linear = rec709_decode(np.asarray(rgb, dtype=np.float64))
    gains = np.array([1 + temp, 1 + tint, 1 - temp])
    x = rec709_encode(linear * (2 ** variant["exposure"]) * gains)
    weights = WEIGHTS.copy()
    if family.get("monochrome"):
        # The neutral B&W variants also have different channel-response targets.
        mix = VARIANTS.index(variant)
        weights += np.array([[0.,0.,0.],[.018,-.012,-.006],[-.012,.018,-.006],[.010,-.020,.010],[.025,-.015,-.010]])[mix]
    y = x @ weights
    curve = (3 * y * y - 2 * y * y * y) - y
    contrast = family["contrast"] + variant["contrast"]
    x += (curve * ((contrast - 1.) * 1.85))[..., None]
    lift = max(0., family["lift"] + variant["lift"])
    shadows = np.array(family["shadow"]) + variant["shadow"]
    highlights = np.array(family["highlight"])
    x += shadows * ((1 - y) ** 2)[..., None]
    x += highlights * (y ** 2)[..., None]
    x += lift * ((1 - y) ** 3)[..., None]
    # A broad shoulder keeps white highlights below the upper boundary.
    x -= variant["knee"] * (y ** 4)[..., None]
    y = x @ weights
    saturation = max(0., family["sat"] + variant["sat"])
    if family.get("monochrome") == "neutral":
        saturation = 0.
    x = y[..., None] + saturation * (x - y[..., None])
    # Smooth bounded hue-sector masks; no discontinuous keying of LUT cells.
    sector = np.maximum(x - (x.sum(axis=-1, keepdims=True) - x) / 2, 0.)
    selective = np.array(family["selective"])
    x += sector * selective * 1.4
    if family.get("monochrome") == "sepia":
        luma = x @ WEIGHTS
        x = luma[..., None] * np.array([1.045,1.006,.920]) + np.array([.006,.001,-.004])
    return np.clip(x, 0., 1.)


def lut_grid(size=SIZE):
    # Flatten C order gives blue outer, green middle, red innermost.
    axis = np.linspace(0., 1., size)
    b, g, r = np.meshgrid(axis, axis, axis, indexing="ij")
    return np.stack([r, g, b], axis=-1)


def write_cube(path, title, table):
    header = (
        '# Original creative LUT, not a camera calibration / Log transform.\n'
        '# Input/output: normalized gamma-encoded SDR Rec.709 RGB.\n'
        '# Red fastest, green next, blue slowest.\n'
        f'TITLE "{title}"\nLUT_3D_SIZE {table.shape[0]}\n'
        'DOMAIN_MIN 0.0 0.0 0.0\nDOMAIN_MAX 1.0 1.0 1.0\n'
    )
    with path.open("w", encoding="ascii", newline="\n") as f:
        f.write(header)
        np.savetxt(f, table.reshape(-1, 3), fmt="%.7f")


def read_cube(path):
    lines = path.read_text().splitlines()
    size = int(next(line.split()[1] for line in lines if line.startswith("LUT_3D_SIZE")))
    data = np.array([[float(c) for c in line.split()] for line in lines if line and line[0] in "0123456789.-"], dtype=np.float64)
    if data.shape != (size ** 3, 3):
        raise ValueError(f"Wrong table length in {path}")
    return data.reshape(size, size, size, 3)


def apply_lut(rgb, table):
    """Trilinear interpolation from the actual serialized cube values."""
    pos = np.clip(np.asarray(rgb, dtype=np.float64), 0., 1.) * (table.shape[0] - 1)
    lo = np.floor(pos).astype(np.int32)
    hi = np.minimum(lo + 1, table.shape[0] - 1)
    fraction = pos - lo
    result = np.zeros_like(pos)
    for db in (0, 1):
        for dg in (0, 1):
            for dr in (0, 1):
                rr = hi[..., 0] if dr else lo[..., 0]
                gg = hi[..., 1] if dg else lo[..., 1]
                bb = hi[..., 2] if db else lo[..., 2]
                weight = (fraction[..., 0] if dr else 1 - fraction[..., 0]).copy()
                weight *= (fraction[..., 1] if dg else 1 - fraction[..., 1])
                weight *= (fraction[..., 2] if db else 1 - fraction[..., 2])
                result += table[bb, gg, rr] * weight[..., None]
    return result


def font(size, bold=False):
    suffix = "-Bold" if bold else ""
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{suffix}.ttf", size)


def source_scene():
    """Original shaded landscape, warm/cool props and analytic swatch strips."""
    w, h = 640, 600
    yy, xx = np.mgrid[0:h, 0:w]
    top = np.array([.36,.66,.87])
    bottom = np.array([.80,.84,.75])
    amount = np.clip(yy / 450, 0., 1.)[..., None]
    arr = np.broadcast_to(top * (1 - amount) + bottom * amount, (h,w,3)).copy()
    # A soft luminous sun, deterministic and smoothly varying.
    radius = np.sqrt(((xx-490)/110)**2+((yy-92)/110)**2)
    arr += np.maximum(1 - radius, 0.)[...,None] * np.array([.10,.06,-.02])
    im = Image.fromarray(np.uint8(np.clip(arr,0,1)*255), "RGB")
    d = ImageDraw.Draw(im)
    d.polygon([(0,245),(90,133),(180,259),(318,124),(422,251),(567,179),(640,281),(640,410),(0,410)], fill=(99,133,139))
    d.polygon([(0,296),(158,231),(260,339),(432,211),(640,343),(640,440),(0,440)], fill=(45,111,98))
    d.polygon([(0,349),(134,302),(274,356),(423,282),(640,347),(640,453),(0,453)], fill=(61,139,93))
    d.rectangle((0,385,640,505), fill=(33,92,92))
    for i in range(15):
        y=392+i*7
        d.line((20+(i*29)%100,y,590-(i*17)%110,y), fill=(69,131,128), width=2)
    # Cabin and tree give distinctive hue sectors and darker detail.
    d.rectangle((70,303,173,389), fill=(204,154,100))
    d.polygon([(49,307),(121,254),(193,307)], fill=(126,63,49))
    d.rectangle((109,329,143,389), fill=(83,48,37))
    d.rectangle((82,322,102,345), fill=(173,221,222))
    d.rectangle((285,334,296,421), fill=(93,69,45))
    for cx,cy,rx,ry,c in [(290,286,44,66,(24,88,68)),(269,320,40,60,(37,113,66)),(315,324,38,62,(41,123,80))]:
        d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=c)
    # Foreground wooden surface and smooth shaded objects.
    d.polygon([(0,438),(640,432),(640,520),(0,520)],fill=(171,119,78))
    for i in range(8): d.line((0,443+i*10,640,437+i*10),fill=(151,101,64),width=2)
    d.ellipse((378,432,513,461), fill=(116,72,47))
    d.rounded_rectangle((408,365,483,437), radius=17, fill=(233,226,208))
    d.ellipse((408,352,483,379), fill=(238,231,215))
    d.ellipse((416,358,474,374), fill=(66,38,24))
    d.ellipse((471,374,504,409), outline=(223,212,192), width=9)
    for cx,cy,r,col in [(558,416,34,(218,105,47)),(356,435,23,(200,79,57)),(530,378,23,(222,167,132))]:
        # Per-pixel Lambert-style sphere, including a skin-colour reference.
        bx0,bx1=max(0,cx-r),min(w,cx+r+1)
        by0,by1=max(0,cy-r),min(h,cy+r+1)
        a=np.asarray(im).copy()
        # Update canvas first: draw state is recreated after each raster sphere.
        region=a[by0:by1,bx0:bx1].copy()
        sy,sx=np.mgrid[by0:by1,bx0:bx1]
        nx=(sx-cx)/r; ny=(sy-cy)/r
        inside=nx*nx+ny*ny<=1
        nz=np.sqrt(np.maximum(0,1-nx*nx-ny*ny))
        light=np.clip(.44+(-nx*.24-ny*.32+nz*.35),.25,1.05)
        sphere=np.clip(np.array(col)*light[...,None],0,255).astype(np.uint8)
        region[inside]=sphere[inside]
        a[by0:by1,bx0:bx1]=region
        im=Image.fromarray(a,"RGB");d=ImageDraw.Draw(im)
    # Ten grayscale steps and 16 warm/cool/skin colours at the bottom.
    for i in range(10):
        v=round(i*255/9)
        d.rectangle((i*64,526,(i+1)*64-1,555),fill=(v,v,v))
    colors=[(204,51,44),(237,121,53),(240,197,74),(80,150,71),(34,143,121),(60,158,199),(64,87,176),(160,80,172),(220,102,150),(233,194,157),(207,155,119),(159,106,79),(118,73,52),(76,52,41),(101,118,125),(184,180,166)]
    for i,c in enumerate(colors): d.rectangle((i*40,560,(i+1)*40-1,592),fill=c)
    return im


def make_preview(source, table, record, path):
    arr=np.asarray(source,dtype=np.float64)/255
    graded=Image.fromarray(np.uint8(np.rint(apply_lut(arr,table)*255)),"RGB")
    before=source.resize((314,294),Image.Resampling.LANCZOS)
    after=graded.resize((314,294),Image.Resampling.LANCZOS)
    out=Image.new("RGB",(640,360),(18,24,32));d=ImageDraw.Draw(out)
    d.text((10,9),"SDR INPUT",font=font(13,True),fill=(188,201,211))
    d.text((330,9),record["id"]+"  "+record["title"],font=font(12,True),fill=(233,235,226))
    out.paste(before,(4,32));out.paste(after,(322,32))
    d.line((319,32,319,326),fill=(244,201,111),width=2)
    d.text((10,337),"Original procedural scene + chart",font=font(11),fill=(174,190,197))
    d.text((330,337),"33\u00b3 .cube \u00b7 Rec.709 creative grade",font=font(11),fill=(174,190,197))
    out.save(path,quality=86,method=6)


def ffmpeg_apply(source_path, cube_path, output_path):
    # Paths are controlled local files. subprocess receives argument arrays.
    subprocess.run(["ffmpeg","-v","error","-y","-threads","1","-i",str(source_path),"-vf",f"lut3d=file='{cube_path}':interp=trilinear","-frames:v","1","-update","1",str(output_path)],check=True,capture_output=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg-qa",action="store_true",help="Parse and apply every LUT with FFmpeg; verify ordering against identity.")
    args=parser.parse_args()
    (ROOT/"luts").mkdir(parents=True,exist_ok=True)
    (ROOT/"previews/luts").mkdir(parents=True,exist_ok=True)
    grid=lut_grid()
    source=source_scene()
    records=[]; checks=[]; hashes=set(); values=[]
    rng=np.random.default_rng(10841)
    points=rng.random((512,3))
    identity_error=float(np.max(np.abs(apply_lut(points,grid)-points)))
    assert identity_error<1e-12
    # Ordering assertion on consecutive serial entries and all lattice corners.
    flat=grid.reshape(-1,3)
    assert np.array_equal(flat[1],np.array([1/32,0.,0.]))
    assert np.array_equal(flat[SIZE],np.array([0.,1/32,0.]))
    assert np.array_equal(flat[SIZE*SIZE],np.array([0.,0.,1/32]))
    for fi,family in enumerate(FAMILIES):
        for vi,variant in enumerate(VARIANTS):
            asset_id=f"VL{fi*5+vi+1:04d}"
            title=family["name"]+" · "+variant["name"]
            cube=ROOT/f"luts/{asset_id}.cube"
            # ASCII .cube titles keep broad editor compatibility.
            write_cube(cube,family["name"]+" - "+variant["name"],grade(grid,family,variant))
            table=read_cube(cube)
            assert table.shape==(SIZE,SIZE,SIZE,3)
            assert np.isfinite(table).all() and table.min()>=0 and table.max()<=1
            digest=hashlib.sha256(table.tobytes()).hexdigest()
            assert digest not in hashes,asset_id
            hashes.add(digest); values.append(table.astype(np.float32))
            sample=apply_lut(points,table)
            effect=float(np.mean(np.abs(sample-points)))
            assert effect>.0025,(asset_id,effect)
            # All grayscale response curves remain monotonic, including B&W.
            gray=np.repeat(np.linspace(0,1,257)[:,None],3,axis=1)
            gray_y=apply_lut(gray,table) @ WEIGHTS
            monotonic=float(np.min(np.diff(gray_y)))
            assert monotonic>-.00001,(asset_id,monotonic)
            record=dict(id=asset_id,type="lut",title=title,category=family["category"],tags=["vlog","montage","colour grading",family["name"].lower(),variant["name"].lower(),"rec709"],use_cases=[family["use"],variant["use"]],format="cube",file=f"luts/{asset_id}.cube",preview=f"previews/luts/{asset_id}.webp",technical=dict(input_color_space="SDR Rec.709",output_color_space="SDR Rec.709",encoding="gamma-encoded RGB",domain=[0.,1.],lut_3d_size=SIZE,entry_count=SIZE**3,ordering="red fastest; green next; blue slowest",interpolation_recommendation="trilinear or tetrahedral",purpose="creative look; not camera Log/HDR conversion",preview_source="original procedural illustration and analytic colour/grayscale chart",variant_target=variant["use"],adjustment_hint="Normalize exposure and white balance first; adjust LUT strength to footage."))
            make_preview(source,table,record,ROOT/record["preview"])
            with Image.open(ROOT/record["preview"]) as p:
                assert p.size==(640,360) and p.format=="WEBP"
            records.append(record)
            checks.append(dict(id=asset_id,table_sha256=digest,entries=table.shape[0]**3,min=float(table.min()),max=float(table.max()),mean_absolute_rgb_effect=round(effect,6),minimum_grayscale_luma_step=round(monotonic,7),preview_pixels=[640,360]))
    # Stronger uniqueness check than names/hash: quantify closest pair tables.
    flattened=np.stack([v[::4,::4,::4].reshape(-1) for v in values])
    nearest_distance=1.;nearest_pair=None
    for i in range(len(flattened)):
        if i+1<len(flattened):
            distances=np.mean(np.abs(flattened[i+1:]-flattened[i]),axis=1)
            j=int(np.argmin(distances));distance=float(distances[j])
            if distance<nearest_distance: nearest_distance=distance;nearest_pair=[records[i]["id"],records[i+1+j]["id"]]
    assert nearest_distance>.0005,(nearest_distance,nearest_pair)
    ffmpeg_results=[];ffmpeg_identity_error=None
    if args.ffmpeg_qa:
        with tempfile.TemporaryDirectory(prefix="vlog_lut_qa_") as tmp:
            tmp=Path(tmp)
            # Exact lattice and arbitrary colours test axis ordering independently.
            pixels=(rng.integers(0,256,size=(64,96,3))).astype(np.uint8)
            pixels[0,:8]=np.array([[0,0,0],[255,0,0],[0,255,0],[0,0,255],[255,255,0],[0,255,255],[255,0,255],[255,255,255]],dtype=np.uint8)
            test=tmp/"input.png";Image.fromarray(pixels,"RGB").save(test)
            identity=tmp/"identity.cube";write_cube(identity,"Temporary identity QA",grid)
            out=tmp/"identity.png";ffmpeg_apply(test,identity,out)
            ffmpeg_identity_error=int(np.max(np.abs(np.asarray(Image.open(out)).astype(int)-pixels.astype(int))))
            assert ffmpeg_identity_error==0,ffmpeg_identity_error
            for record,table in zip(records,values):
                out=tmp/(record["id"]+".png")
                ffmpeg_apply(test,ROOT/record["file"],out)
                actual=np.asarray(Image.open(out),dtype=float)/255.
                expected=apply_lut(pixels.astype(float)/255.,table)
                error=float(np.max(np.abs(actual-expected))*255)
                assert error<1.05,(record["id"],error)
                ffmpeg_results.append(dict(id=record["id"],max_interpolation_error_in_8bit_steps=round(error,5)))
    report=dict(count=len(records),families=len(FAMILIES),variants_per_family=len(VARIANTS),format="Iridas .cube 3D",cube_size=SIZE,entry_count_each=SIZE**3,total_unique_tables=len(hashes),identity_max_error=identity_error,serialized_ordering_check="red fastest, green next, blue slowest; consecutive index and primary corner checks",nearest_pair=nearest_pair,nearest_table_mean_absolute_difference=nearest_distance,all_values_finite_bounded=True,all_grayscale_luma_curves_monotonic=True,ffmpeg_parsed_applied_count=len(ffmpeg_results),ffmpeg_identity_max_error_8bit_steps=ffmpeg_identity_error,ffmpeg_interpolation="trilinear",technical_reference="https://ffmpeg.org/ffmpeg-filters.html#lut3d",limitations=["Creative SDR Rec.709 looks, not exposure/white balance restoration or camera Log/HDR transforms.","No temporal effects, grain, blur or vignettes are encoded in a 3D colour LUT.","Previews use original procedural illustration and charts; no real footage, skin appearance or camera calibration is claimed."],checks=checks,ffmpeg_checks=ffmpeg_results)
    (ROOT/"index_luts.json").write_text(json.dumps(records,ensure_ascii=False,indent=2)+"\n")
    (ROOT/"luts_qa.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:report[k] for k in ["count","cube_size","total_unique_tables","nearest_pair","nearest_table_mean_absolute_difference","ffmpeg_parsed_applied_count","ffmpeg_identity_max_error_8bit_steps"]}))


if __name__=="__main__":
    main()
