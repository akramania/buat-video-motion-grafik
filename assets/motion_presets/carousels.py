"""Four original, editable carousel motion presets; no third-party artwork."""
from core import *
from PIL import ImageOps

PRESETS = {
    'C01': {'name': 'Focus carousel', 'description': 'Continuous focus index drives depth, scale and tilt.', 'genre': 'promo', 'genres': ['promo','creator','saas','corporate'], 'text': 'FIND YOUR FOCUS', 'subtitle': 'Satu fokus. Banyak perspektif.'},
    'C02': {'name': 'Curved card fan', 'description': 'A stacked deck opens into a gently moving curved fan.', 'genre': 'creator', 'genres': ['creator','promo','documentary'], 'text': 'IDEAS IN MOTION', 'subtitle': 'Buka ruang untuk idea baharu.'},
    'C03': {'name': 'Expanding hero', 'description': 'One card expands with a continuous cover crop and radius morph.', 'genre': 'corporate', 'genres': ['corporate','saas','promo','education'], 'text': 'MAKE SPACE', 'subtitle': 'Daripada galeri kepada cerita utama.'},
    'C04': {'name': 'Infinite double track', 'description': 'Two opposing tracks with stable asset IDs and offscreen recycling.', 'genre': 'documentary', 'genres': ['documentary','creator','promo','education'], 'text': 'EVERY FRAME', 'subtitle': 'Dua arah. Koleksi tanpa henti.'},
}

# Rich, original editorial poster palettes. Every shape is generated here.
ART = [
    ('#EC693E','#F4DCA0','#252C58','#F7F0DC'),
    ('#A6B1ED','#E7E3CA','#393356','#F7ECD3'),
    ('#345B51','#D1EBBC','#FF9C68','#E9F4E2'),
    ('#EADFD2','#283C66','#EA8E81','#3B4054'),
    ('#E9B940','#3B487C','#F4E6BA','#302D44'),
    ('#724760','#F0A981','#CFC9E4','#FAEDD9'),
    ('#8BB5BA','#F3DD99','#264759','#F4F1D7'),
    ('#BB493A','#E8CBC0','#3E5074','#FFF1D3'),
    ('#CEC8BA','#496865','#E69B62','#263632'),
]
NAMES = ['FORM','BALANCE','FLOW','STUDIO','FOCUS','SHAPE','GROW','MOTION','CURVE']

def _asset_path(cfg, idx):
    paths = cfg.get('image_paths') or []
    if isinstance(paths, str): paths = [paths]
    return str(paths[idx % len(paths)]) if paths else ''

@lru_cache(maxsize=64)
def _artwork(idx, path=''):
    """A large texture; portrait and landscape cards always use cover crop."""
    if path:
        with Image.open(path) as source:
            return ImageOps.exif_transpose(source).convert('RGB').resize((900,900),Image.Resampling.LANCZOS) if source.width == source.height else ImageOps.exif_transpose(source).convert('RGB').copy()
    bg,a,b,ink = ART[idx % len(ART)]
    im = Image.new('RGBA',(640,720),bg); d=ImageDraw.Draw(im)
    k=idx%6
    if k==0:
        # Oversized nested arches and a small circular counterweight.
        for n in range(7):
            col=a if n%2==0 else bg
            d.rounded_rectangle((40+n*31,70+n*31,600-n*31,725+n*18),radius=280-n*23,fill=col)
        d.rectangle((40,520,600,760),fill=b)
        d.ellipse((325,415,565,655),fill=a)
        for yy in range(580,650,16): d.line((72,yy,245,yy),fill=bg,width=4)
    elif k==1:
        # Asymmetric discs with carefully registered offset halves.
        d.ellipse((-140,30,475,645),fill=b)
        d.ellipse((50,175,525,650),fill=a)
        d.pieslice((40,125,600,685),270,90,fill=bg)
        d.ellipse((355,45,515,205),fill=ink)
        for xx in range(72,510,30): d.line((xx,620,xx,700),fill=b,width=3)
    elif k==2:
        # Flowing vertical wave built from offset capsules.
        for n in range(10):
            xx=-80+n*92; yy=100+85*math.sin(n*.62)
            d.rounded_rectangle((xx,yy,xx+120,yy+570),radius=59,fill=a if n%2==0 else b)
        d.ellipse((420,55,560,195),fill=ink)
    elif k==3:
        # Architectural steps against a central sun.
        d.ellipse((140,50,625,535),fill=a)
        for n in range(7):
            xx=-50+n*107; yy=620-n*59
            d.rectangle((xx,yy,xx+108,760),fill=b if n%2==0 else ink)
        d.line((62,77,190,77),fill=b,width=8)
        d.line((62,98,155,98),fill=b,width=8)
    elif k==4:
        # Radial petals; no raster or brand references.
        for n in range(12):
            ang=n*math.pi/6; cx=325+143*math.cos(ang);cy=355+143*math.sin(ang)
            d.ellipse((cx-95,cy-95,cx+95,cy+95),fill=a if n%2==0 else b)
        d.ellipse((235,265,415,445),fill=bg)
        d.rectangle((47,627,595,640),fill=ink)
    else:
        # Diagonal ribbon grid with a bright contrasting focal circle.
        for n in range(-4,9):
            xx=n*126; d.polygon([(xx,0),(xx+63,0),(xx+563,720),(xx+500,720)],fill=a)
        d.ellipse((90,160,550,620),fill=b)
        d.ellipse((200,270,440,510),fill=bg)
        d.rectangle((460,46,588,174),fill=ink)
    # Printed-like edge rules and edition numerals make assets self-contained.
    d.rectangle((22,22,618,698),outline=rgba(ink,100),width=2)
    text(im,f'{idx+1:02d}',51,51,22,ink,'mono',anchor='left')
    text(im,'FORM / STUDY',586,665,20,ink,'mono',anchor='right')
    return im

def _cover(source,w,h):
    # Scale uniformly; ImageOps.fit crops centrally instead of distorting photos.
    return ImageOps.fit(source.convert('RGBA'),(max(1,int(w)),max(1,int(h))),method=Image.Resampling.LANCZOS,centering=(.5,.48))

@lru_cache(maxsize=256)
def _card(idx,w,h,title='',genre='promo',path='',radius=25):
    w,h=int(w),int(h); pad=28
    im=layer(w+pad*2,h+pad*2)
    s=layer(im.width,im.height)
    rr(s,(pad,pad+12,pad+w,pad+h+12),(0,0,0,92),radius)
    im.alpha_composite(s.filter(ImageFilter.GaussianBlur(11)))
    surface=_cover(_artwork(idx,path),w,h)
    mask=Image.new('L',(w,h));ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1),radius=radius,fill=255)
    surface.putalpha(mask)
    # Legible, deliberately quiet editorial labels are children of the card.
    band=layer(w,h); d=ImageDraw.Draw(band)
    for y in range(max(0,h-88),h):
        alpha=round(210*prog(y,h-89,h-1))
        d.line((0,y,w,y),fill=(12,17,27,alpha))
    band.putalpha(Image.composite(band.getchannel('A'),Image.new('L',(w,h)),mask))
    surface.alpha_composite(band)
    title=title or NAMES[idx%len(NAMES)]
    ts=fit_size(title,w-34,24)
    text(surface,title,17,h-32,ts,'#FFF9EB',anchor='left')
    text(surface,f'{idx+1:02d}',w-18,22,12,'#FFF9EB','mono',anchor='right')
    im.alpha_composite(surface,(pad,pad))
    ImageDraw.Draw(im).rounded_rectangle((pad,pad,pad+w-1,pad+h-1),radius=radius,outline=(255,255,255,90),width=1)
    return im

def _frame_title(im,cfg,p,t,default):
    sub=str(cfg.get('subtitle',default))
    text(im,sub,640,178,fit_size(sub,1060,20),p['muted'],'sans',opacity=life(t,.25,.85,4.05,4.65))

def _clip_content(im,content):
    mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rectangle((45,197,1235,609),fill=255)
    content.putalpha(Image.composite(content.getchannel('A'),Image.new('L',(W,H)),mask))
    im.alpha_composite(content)

def _focus(im,t,cfg,p):
    incoming=enter(t,.12,1.03); outgoing=leave(t,4.15,4.85)
    focus=3+smooth(prog(t,1.35,2.35))+smooth(prog(t,2.75,3.8))
    content=layer(); poses=[]
    for i in range(9):
        rel=i-focus; dist=abs(rel)
        if dist>3.2:continue
        sc=1/(1+.19*dist)
        x=640+rel*252
        y=388+dist*10+(1-incoming)*135-outgoing*85
        angle=-max(-11,min(11,rel*5))
        opacity=clamp((3.2-dist)/.55)*incoming*(1-outgoing)
        poses.append((sc,i,x,y,angle,opacity))
    for sc,i,x,y,angle,opacity in sorted(poses):
        title=str(cfg.get('text','FIND YOUR FOCUS')) if i==4 else ''
        card=_card(i,248,300,title,cfg.get('genre','promo'),_asset_path(cfg,i))
        # A little horizontal foreshortening suggests yaw while keeping labels attached.
        rel=i-focus; comp=1-.055*min(3,abs(rel))
        if comp<.995:card=card.resize((round(card.width*comp),card.height),Image.Resampling.BICUBIC)
        if abs(rel)>1.5:card=card.filter(ImageFilter.GaussianBlur(min(1.2,(abs(rel)-1.5)*.65)))
        paste(content,card,x,y,opacity,sc*mix(.83,1,incoming)*(1-outgoing*.06),angle)
    _clip_content(im,content)
    # Focus pagination has stable slots and follows the continuous index.
    alpha=incoming*(1-outgoing)
    for i in range(3):
        ac=clamp(1-abs(focus-3-i)); r=mix(3,5,ac)
        circle(im,620+i*20,578,r,rgba(p['accent'] if ac>.45 else p['muted'],180*alpha))

def _fan(im,t,cfg,p):
    incoming=enter(t,.17,1.15);outgoing=leave(t,4.15,4.85)
    spread=incoming*(1-outgoing*.28)
    drift=math.sin(prog(t,1.15,4.15)*math.pi*2)*.27
    content=layer();poses=[]
    for i in range(7):
        rel=i-3-drift; dist=abs(rel)
        x=640+rel*155*spread
        y=370+rel*rel*8.5*spread+(1-incoming)*55+outgoing*90
        sc=(1-.047*dist)*mix(.83,1,incoming)
        angle=-rel*8*spread
        poses.append((sc,i,x,y,angle))
    for sc,i,x,y,angle in sorted(poses):
        title=str(cfg.get('text','IDEAS IN MOTION')) if i==3 else ''
        card=_card(i,238,302,title,cfg.get('genre','creator'),_asset_path(cfg,i))
        paste(content,card,x,y,incoming*(1-outgoing),sc,angle)
    _clip_content(im,content)

def _hero(im,t,cfg,p):
    incoming=enter(t,.15,.95);outgoing=leave(t,4.15,4.85)
    expand=smooth(prog(t,1.25,2.2))*(1-smooth(prog(t,3.2,4.06)))
    content=layer()
    for i,side in [(0,-1),(2,1)]:
        x=640+side*(310+170*expand)
        y=382+(1-incoming)*110+outgoing*110
        card=_card(i,240,296,'',cfg.get('genre','corporate'),_asset_path(cfg,i))
        paste(content,card,x,y,incoming*(1-outgoing)*(1-.88*expand),mix(.91,.64,expand),side*mix(-3,9,expand))
    ww=round(mix(256,965,expand));hh=round(mix(312,360,expand));radius=round(mix(28,43,expand))
    # Do not cache every frame of a morph: texture stays cached, crop is calculated.
    shadow=layer(ww+60,hh+60);rr(shadow,(30,40,30+ww,40+hh),(0,0,0,110),radius)
    shadow=shadow.filter(ImageFilter.GaussianBlur(14))
    hero=_cover(_artwork(1,_asset_path(cfg,1)),ww,hh)
    mask=Image.new('L',(ww,hh));ImageDraw.Draw(mask).rounded_rectangle((0,0,ww-1,hh-1),radius=radius,fill=255)
    shade=layer(ww,hh);d=ImageDraw.Draw(shade)
    for y in range(hh):d.line((0,y,ww,y),fill=(8,12,30,round(220*(y/hh)**3)))
    hero.alpha_composite(shade)
    title=str(cfg.get('text','MAKE SPACE'))
    text(hero,title,28,hh-59,fit_size(title,ww-56,mix(25,48,expand)),'#FFF9EF',anchor='left')
    text(hero,'SELECTED / 02',30,hh-28,12,'#FFF9EF','mono',anchor='left')
    hero.putalpha(mask);shadow.alpha_composite(hero,(30,30))
    ImageDraw.Draw(shadow).rounded_rectangle((30,30,30+ww-1,30+hh-1),radius=radius,outline=(255,255,255,150),width=1)
    paste(content,shadow,640,382+(1-incoming)*110-outgoing*55,incoming*(1-outgoing),mix(.85,1,incoming))
    _clip_content(im,content)

def _tracks(im,t,cfg,p):
    content=layer();circ=9*222
    for row in range(2):
        incoming=enter(t,.15+row*.12,1.0+row*.12);outgoing=leave(t,4.15+row*.03,4.85)
        offset=130+(-145 if row==0 else 172)*t+(row*84)
        for i in range(9):
            # Wrapping happens from x > 1700 to x = -260, safely outside frame.
            x=((i*222+offset+260)%circ)-260
            if x < -130 or x > W+130:continue
            y=(306 if row==0 else 496)+(1-incoming)*48+outgoing*(-48 if row==0 else 48)
            idx=i+row*9
            title=str(cfg.get('text','EVERY FRAME')) if i==0 else NAMES[idx%9]
            card=_card(idx,194,164,title,cfg.get('genre','documentary'),_asset_path(cfg,idx),20)
            paste(content,card,x,y,incoming*(1-outgoing),1,0)
    _clip_content(im,content)

def render(pid,t,cfg):
    cfg={**PRESETS[pid],**cfg}
    im=base(cfg);p=palette(cfg)
    _frame_title(im,cfg,p,t,PRESETS[pid]['subtitle'])
    {'C01':_focus,'C02':_fan,'C03':_hero,'C04':_tracks}[pid](im,t,cfg,p)
    return im
