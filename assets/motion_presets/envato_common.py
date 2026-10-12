"""Shared original drawing components for the October preview adaptations."""
from core import *
from PIL import ImageChops,ImageOps
import json,random

def heading(im,cfg,p):
    y=160 if cfg.get('_labels') else 92
    text(im,cfg['text'],640,y,fit_size(cfg['text'],1080,37),p['text'])
    text(im,cfg.get('subtitle',''),640,642,fit_size(cfg.get('subtitle',''),1050,18,'mono'),p['muted'],'mono')

def q(t,start=.3,span=1.8):return ease(prog(t,start,start+span))
def curve(a,b,height=80,n=90):
    return [(mix(a[0],b[0],u),mix(a[1],b[1],u)-height*4*u*(1-u)) for u in np.linspace(0,1,n)]
def trace(im,pts,p,color,width=4):
    if p<=0:return
    line(im,pts[:max(2,round(len(pts)*clamp(p)))],color,width)
def ring(im,x,y,r,value,color,track,width=12):
    d=ImageDraw.Draw(im);box=(x-r,y-r,x+r,y+r)
    d.arc(box,0,360,fill=track,width=width)
    if value>0:d.arc(box,-90,-90+359.9*clamp(value),fill=color,width=width)
def check(im,x,y,c,scale=1):line(im,[(x-8*scale,y),(x-2*scale,y+6*scale),(x+10*scale,y-8*scale)],c,max(2,int(3*scale)))
def arrowline(im,a,b,color,p=1,width=3):
    line(im,[a,(mix(a[0],b[0],p),mix(a[1],b[1],p))],color,width)
    if p>.98:
        v=np.array(b)-a;v=v/max(1,np.linalg.norm(v));u=np.array([-v[1],v[0]])
        c=np.array(b)-v*12;line(im,[c+u*6,b,c-u*6],color,width)
def card(im,x,y,w,h,p,opacity=1):paste(im,panel(w,h,p['panel'],22,rgba(p['muted'],60)),x+w/2,y+h/2,opacity)

def formatted(cfg,progress,compact=False):
    a=float(cfg.get('from_value',0));b=float(cfg.get('to_value',12500));dp=int(cfg.get('decimals',0))
    if not all(map(math.isfinite,[a,b])) or not 0<=dp<=6:raise ValueError('Finite counter values and decimals 0..6 required')
    v=b if progress>=1 else mix(a,b,clamp(progress))
    if compact:
        divisor,suf=(1e6,'M') if abs(v)>=1e6 else (1000,'K') if abs(v)>=1000 else (1,'')
        value=f'{v/divisor:.1f}'.rstrip('0').rstrip('.') if divisor!=1 else f'{v:.0f}'
        return str(cfg.get('prefix',''))+value+suf+str(cfg.get('suffix',''))
    return str(cfg.get('prefix',''))+format(v,(',' if cfg.get('grouping',True) else '')+f'.{dp}f')+str(cfg.get('suffix',''))

@lru_cache(maxsize=12)
def demo_media(index=0):
    """Original geometric landscapes, not extracted source photographs."""
    im=layer();d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,H),fill=['#274D67','#462F62','#284E48'][index%3])
    d.ellipse((830,90,1030,290),fill=['#F8CB8D','#EDADCD','#9BD1C5'][index%3])
    for z,col in enumerate(['#3F7581','#375E71','#203D57']):
        pts=[(x,360+z*92+math.sin(x*.008+index+z)*65) for x in range(0,1281,15)]
        d.polygon(pts+[(W,H),(0,H)],fill=col)
    for i in range(8):
        x=110+i*142;y=520+math.sin(i*.8+index)*70
        d.polygon([(x,y-55),(x-23,y+8),(x+23,y+8)],fill='#172E42');d.line((x,y,x,y+55),fill='#172E42',width=7)
    text(im,['NORTH / 01','SOUTH / 02','EAST / 03'][index%3],80,80,24,'#FFFFFF','mono',anchor='left')
    return im

@lru_cache(maxsize=12)
def glass_background(genre,bg,accent):
    im=background(genre,bg,accent).copy();overlay=layer();d=ImageDraw.Draw(overlay)
    for i in range(9):
        x=150+i*145;y=370+math.sin(i*.6)*115
        d.ellipse((x-85,y-100,x+85,y+100),fill=rgba(accent,25+i*4))
    im.alpha_composite(overlay.filter(ImageFilter.GaussianBlur(30)))
    return im
def glass(im,box,p):
    x,y,x1,y1=box
    # True alpha compositing over an original background, rim + soft highlight.
    rr(im,box,rgba('#FFFFFF',30),25,rgba('#FFFFFF',135),2)
    rr(im,(x+4,y+4,x1-4,y+40),rgba('#FFFFFF',14),19)
    line(im,[(x+28,y+4),(x1-28,y+4)],rgba('#FFFFFF',160),2)

@lru_cache(maxsize=16)
def geo_map(genre,accent):
    p=PALETTES[genre];im=layer(1040,390);d=ImageDraw.Draw(im)
    geo=json.loads((Path(__file__).parent/'world.geojson').read_text())
    for f in geo['features']:
        if f['properties']['ADMIN']=='Antarctica':continue
        polys=f['geometry']['coordinates']
        if f['geometry']['type']=='Polygon':polys=[polys]
        for poly in polys:
            pts=[((lon+180)/360*1040,(85-lat)/145*390) for lon,lat in poly[0]]
            d.polygon(pts,fill=rgba(p['muted'],80),outline=rgba(p['bg'],180))
    return im
def location(lon,lat):return (120+(lon+180)/360*1040,190+(85-lat)/145*390)

def icon(im,kind,x,y,size,color):
    s=size;d=ImageDraw.Draw(im)
    if kind in ('clock','watch'):
        circle(im,x,y,s*.42,None,color,4);line(im,[(x,y-s*.26),(x,y),(x+s*.20,y+s*.08)],color,4)
        line(im,[(x-s*.1,y-s*.54),(x+s*.1,y-s*.54)],color,4)
    elif kind=='megaphone':
        d.polygon([(x-s*.4,y-s*.16),(x+s*.3,y-s*.35),(x+s*.3,y+s*.35),(x-s*.4,y+s*.16)],fill=color)
        line(im,[(x-s*.18,y+s*.16),(x-s*.05,y+s*.46)],color,8)
    elif kind=='person':
        circle(im,x,y-s*.26,s*.14,color);rr(im,(x-s*.18,y-s*.04,x+s*.18,y+s*.28),color,s*.1)
        line(im,[(x-s*.1,y+s*.22),(x-s*.1,y+s*.45)],color,max(2,int(s*.1)));line(im,[(x+s*.1,y+s*.22),(x+s*.1,y+s*.45)],color,max(2,int(s*.1)))
    elif kind=='screen':
        rr(im,(x-s*.48,y-s*.34,x+s*.48,y+s*.28),None,s*.05,color,4)
        line(im,[(x,y+s*.28),(x,y+s*.48),(x-s*.22,y+s*.48),(x+s*.22,y+s*.48)],color,4)
    elif kind=='pin':
        circle(im,x,y-s*.13,s*.30,color);d.polygon([(x-s*.23,y),(x,y+s*.47),(x+s*.23,y)],fill=color);circle(im,x,y-s*.13,s*.10,'#FFFFFF')
    elif kind=='heart':
        d.ellipse((x-s*.4,y-s*.34,x,y+s*.08),fill=color);d.ellipse((x,y-s*.34,x+s*.4,y+s*.08),fill=color);d.polygon([(x-s*.4,y-s*.07),(x,y+s*.38),(x+s*.4,y-s*.07)],fill=color)
    elif kind=='chat':rr(im,(x-s*.45,y-s*.32,x+s*.45,y+s*.22),None,s*.10,color,4);line(im,[(x-s*.1,y+s*.22),(x-s*.22,y+s*.4),(x+s*.12,y+s*.22)],color,4)
    elif kind=='pie':
        d.pieslice((x-s*.4,y-s*.4,x+s*.4,y+s*.4),20,350,fill=color);d.pieslice((x-s*.36,y-s*.48,x+s*.44,y+s*.32),-10,20,fill=rgba(color,150))
    else:
        rr(im,(x-s*.4,y-s*.3,x+s*.4,y+s*.3),None,s*.12,color,4);text(im,'+',x,y,int(s*.6),color)
