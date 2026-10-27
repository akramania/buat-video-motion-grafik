"""Offline SVG rasterization using installed CairoSVG, or local Node sharp."""
from pathlib import Path
import subprocess

def svg2png(*,url=None,bytestring=None,output_width=None,output_height=None,write_to=None,**kwargs):
    try:
        import cairosvg
    except ModuleNotFoundError:
        code="""const sharp=require('sharp');let xs=[];process.stdin.on('data',x=>xs.push(x));process.stdin.on('end',async()=>{try{let p=sharp(Buffer.concat(xs));const w=Number(process.argv[1])||null,h=Number(process.argv[2])||null;if(w||h)p=p.resize(w,h,{fit:'fill'});process.stdout.write(await p.png().toBuffer());}catch(e){process.stderr.write(String(e));process.exitCode=1;}});"""
        data=bytestring if bytestring is not None else Path(url).read_bytes()
        result=subprocess.run(['node','-e',code,str(output_width or 0),str(output_height or 0)],input=data,capture_output=True,check=True).stdout
        if write_to is not None:Path(write_to).write_bytes(result)
        return result
    return cairosvg.svg2png(url=url,bytestring=bytestring,output_width=output_width,output_height=output_height,write_to=write_to,**kwargs)
