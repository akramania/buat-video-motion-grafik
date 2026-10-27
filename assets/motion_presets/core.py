"""Original deterministic motion drawing primitives. Coordinates: 1280 x 720."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from functools import lru_cache
import math, os, numpy as np
from pathlib import Path
W,H=1280,720
FONT_ROOT=Path(__file__).resolve().parent/'fonts'
FONTS={key:str(FONT_ROOT/name) for key,name in {'sans':'DejaVuSans.ttf','bold':'DejaVuSans-Bold.ttf','mono':'DejaVuSansMono.ttf','serif':'DejaVuSerif.ttf'}.items()}
PALETTES={
 'saas':{'bg':'#0B1220','panel':'#152238','text':'#F0F5FF','muted':'#8497B0','accent':'#71E8C4','secondary':'#8DABFF'},
 'education':{'bg':'#F4F0E8','panel':'#E4DED1','text':'#222D3B','muted':'#697380','accent':'#2163DA','secondary':'#E6944F'},
 'creator':{'bg':'#161222','panel':'#292039','text':'#FFF9EF','muted':'#AB9BBA','accent':'#DEFF70','secondary':'#CBA1FF'},
 'documentary':{'bg':'#E8E1D4','panel':'#D9CEBC','text':'#342D2B','muted':'#88776A','accent':'#BD4C35','secondary':'#667866'},
 'corporate':{'bg':'#101C33','panel':'#1C2D4A','text':'#F2F5FB','muted':'#91A5C2','accent':'#7AB5FF','secondary':'#D3E0F5'},
 'promo':{'bg':'#23112C','panel':'#38203C','text':'#FFF4E8','muted':'#B399B9','accent':'#FF966B','secondary':'#ECAFED'},
}
def clamp(v,a=0.,b=1.): return max(a,min(b,v))
def mix(a,b,p): return a+(b-a)*p
def prog(t,a,b): return clamp((t-a)/(b-a)) if b>a else float(t>=b)
def ease(p): p=clamp(p); return 1-(1-p)**3
def smooth(p): p=clamp(p); return p*p*(3-2*p)
def pop(p): p=clamp(p); return 1-(1-p)**3*math.cos(p*math.pi*2.8)
def enter(t,a=.2,b=1.): return ease(prog(t,a,b))
def leave(t,a=4.15,b=4.85): return smooth(prog(t,a,b))
def life(t,a=.2,b=.9,c=4.2,d=4.85): return enter(t,a,b)*(1-leave(t,c,d))
def palette(cfg):
 p=dict(PALETTES.get(cfg.get('genre','saas'),PALETTES['saas']))
 for k in p:
  field='text_color' if k=='text' else k
  if cfg.get(field): p[k]=cfg[field]
 return p
def rgb(c):
 if isinstance(c,tuple): return c[:3]
 c=c.lstrip('#'); return tuple(int(c[i:i+2],16) for i in (0,2,4))
def rgba(c,a=255): return rgb(c)+(int(clamp(a,0,255)),)
@lru_cache(maxsize=128)
def font(size=48,face='bold',custom=''):
 path=custom or FONTS.get(face,face)
 return ImageFont.truetype(path,max(1,int(size)))
@lru_cache(maxsize=4096)
def _cached_text_img(text,size=48,color='#FFFFFF',face='bold',stroke=0,stroke_color='#FFFFFF',custom=''):
 f=font(size,face,custom); box=f.getbbox(str(text),stroke_width=stroke)
 if not text: return Image.new('RGBA',(1,1))
 im=Image.new('RGBA',(max(1,box[2]-box[0]+4),max(1,box[3]-box[1]+4)))
 ImageDraw.Draw(im).text((2-box[0],2-box[1]),str(text),font=f,fill=color,stroke_width=stroke,stroke_fill=stroke_color)
 return im
def text_img(text,size=48,color='#FFFFFF',face='bold',stroke=0,stroke_color='#FFFFFF',custom=''):
 # Callers may apply alpha/masks; never expose the shared cached bitmap.
 return _cached_text_img(text,size,color,face,stroke,stroke_color,custom).copy()
text_img.cache_clear=_cached_text_img.cache_clear
text_img.cache_info=_cached_text_img.cache_info
def measure(text,size=48,face='bold',custom=''): return font(size,face,custom).getlength(str(text))
def layer(w=W,h=H): return Image.new('RGBA',(max(1,int(w)),max(1,int(h))))
def paste(dst,src,x,y,opacity=1,scale=1,angle=0,anchor='center'):
 if opacity<=0 or scale<=0:return
 im=src
 if abs(scale-1)>.002:
  im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.BICUBIC)
 if angle:im=im.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
 if opacity<.999:
  im=im.copy(); im.putalpha(im.getchannel('A').point(lambda v:round(v*clamp(opacity))))
 if anchor=='center': x-=im.width/2;y-=im.height/2
 elif anchor=='left': y-=im.height/2
 elif anchor=='right':x-=im.width;y-=im.height/2
 dst.alpha_composite(im,(round(x),round(y)))
def text(dst,s,x,y,size=48,color='#FFFFFF',face='bold',opacity=1,scale=1,angle=0,anchor='center',stroke=0,stroke_color='#FFFFFF',custom=''):
 paste(dst,text_img(str(s),int(size),color,face,stroke,stroke_color,custom),x,y,opacity,scale,angle,anchor)
def fit_size(s,max_width,size=84,face='bold'):
 return max(12,min(size,int(size*max_width/max(1,measure(s,size,face)))))
def translucent(c): return isinstance(c,tuple) and len(c)==4 and c[3]<255
def rr(dst,box,fill,r=22,outline=None,width=1):
 target=layer(*dst.size) if translucent(fill) or translucent(outline) else dst
 ImageDraw.Draw(target).rounded_rectangle(tuple(round(z) for z in box),radius=max(0,round(r)),fill=fill,outline=outline,width=max(1,round(width)))
 if target is not dst:dst.alpha_composite(target)
def line(dst,pts,fill,width=2):
 target=layer(*dst.size) if translucent(fill) else dst
 ImageDraw.Draw(target).line([(round(x),round(y)) for x,y in pts],fill=fill,width=max(1,round(width)),joint='curve')
 if target is not dst:dst.alpha_composite(target)
def circle(dst,x,y,r,fill,outline=None,width=1):
 target=layer(*dst.size) if translucent(fill) or translucent(outline) else dst
 ImageDraw.Draw(target).ellipse((round(x-r),round(y-r),round(x+r),round(y+r)),fill=fill,outline=outline,width=max(1,round(width)))
 if target is not dst:dst.alpha_composite(target)
@lru_cache(maxsize=128)
def _cached_panel(w,h,fill='#152238',radius=28,border='#33445D',shadow=True):
 pad=30 if shadow else 0; im=layer(w+2*pad,h+2*pad)
 if shadow:
  s=layer(im.width,im.height);rr(s,(pad,pad+10,pad+w,pad+h+10),(0,0,0,110),radius);s=s.filter(ImageFilter.GaussianBlur(13));im.alpha_composite(s)
 rr(im,(pad,pad,pad+w,pad+h),fill,radius,border if border else None)
 return im
def panel(w,h,fill='#152238',radius=28,border='#33445D',shadow=True):
 # Drawing labels into a panel must not alter subsequent frames or presets.
 return _cached_panel(w,h,fill,radius,border,shadow).copy()
panel.cache_clear=_cached_panel.cache_clear
panel.cache_info=_cached_panel.cache_info
@lru_cache(maxsize=20)
def background(genre='saas',bg='',accent=''):
 p=dict(PALETTES.get(genre,PALETTES['saas']));p['bg']=bg or p['bg'];p['accent']=accent or p['accent']
 yy,xx=np.mgrid[0:H,0:W];glow=np.exp(-(((xx-1010)/740)**2+((yy-140)/470)**2))*0.09
 base=np.array(rgb(p['bg'])); ac=np.array(rgb(p['accent']));a=base[None,None,:]*(1-glow[:,:,None])+ac[None,None,:]*glow[:,:,None]
 im=Image.fromarray(np.uint8(np.clip(a,0,255))).convert('RGBA'); grid=layer();d=ImageDraw.Draw(grid)
 # Deliberately quiet drafting grid.
 for x in range(80,W,80):d.line((x,115,x,620),fill=rgba(p['muted'],12),width=1)
 for y in range(140,621,80):d.line((50,y,1230,y),fill=rgba(p['muted'],12),width=1)
 im.alpha_composite(grid)
 return im

def base(cfg):
 if cfg.get('_transparent'):return layer()
 return background(cfg.get('genre','saas'),cfg.get('bg',''),cfg.get('accent','')).copy()
def label(dst,s,x,y,p,size=16):text(dst,s,x,y,size,p['muted'],'mono',anchor='left')
def tag(dst,s,x,y,p):
 ww=measure(s,15,'mono')+28;rr(dst,(x,y-16,x+ww,y+16),rgba(p['accent'],25),16,rgba(p['accent'],80));text(dst,s,x+14,y,15,p['accent'],'mono',anchor='left')
def arrow(dst,x,y,color,scale=1):line(dst,[(x-12*scale,y),(x+12*scale,y),(x+4*scale,y-8*scale)],color,3);line(dst,[(x+12*scale,y),(x+4*scale,y+8*scale)],color,3)
def crop_reveal(src,p,direction='up'):
 p=clamp(p); out=layer(src.width,src.height)
 if p==0:return out
 if direction=='left':box=(0,0,round(src.width*p),src.height)
 else:box=(0,round(src.height*(1-p)),src.width,src.height)
 out.paste(src.crop(box),box[:2]);return out

def warp_quad(src,quad,size=(W,H)):
 """Perspective map source corners into quad TL,TR,BR,BL."""
 points=[(0,0),(src.width,0),(src.width,src.height),(0,src.height)]
 matrix=[];rhs=[]
 for (x,y),(u,v) in zip(quad,points):
  matrix.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);rhs.extend([u,v])
 coeff=np.linalg.solve(np.array(matrix),np.array(rhs))
 return src.transform(size,Image.Transform.PERSPECTIVE,coeff,Image.Resampling.BICUBIC)
