"""PX301–PX400: original Pillow motion recipes inspired by public listing concepts.

All artwork is procedural, not extracted from Envato. Time is normalized 0..5.
Depth effects are 2.5D image planes, not reconstructed 3D photography. User
photos are contained without cropping; no automatic subject cutout is claimed.
Transition endpoints are clean media with show_titles=False.
"""
from core import *
from PIL import ImageOps
import json

ROOT=Path(__file__).resolve().parent
PRESETS=json.loads((ROOT/'premium_promo_fx_index.json').read_text())

@lru_cache(maxsize=64)
def _demo(i=0,w=640,h=360):
    """Original graphic stills: paper landscape / product / architecture / art."""
    colors=[('#F5EBDA','#BBD8D1','#528B91','#223F4D','#E9AC81'),
            ('#EEE6FA','#D4BAF0','#7960A5','#332A58','#F3B6A1'),
            ('#E7ECF4','#B6CDDD','#617D95','#273F58','#E1AD74'),
            ('#FAE1D6','#DAB4AC','#A9676D','#583E57','#F7D185')][i%4]
    im=Image.new('RGBA',(640,360),colors[0]); d=ImageDraw.Draw(im)
    if i%4==0:
        circle(im,488,86,47,colors[4]); d.polygon([(0,270),(156,91),(317,273)],fill=colors[1]);d.polygon([(139,302),(368,130),(611,302)],fill=colors[2]);d.polygon([(0,360),(0,280),(216,227),(406,288),(640,231),(640,360)],fill=colors[3]);
        for j in range(6):line(im,[(40+j*24,316),(73+j*24,299),(110+j*24,314)],rgba(colors[1],150),2)
    elif i%4==1:
        for j in range(4): rr(im,(52+j*130,35,134+j*130,325),rgba(colors[1],110),40)
        circle(im,320,175,115,colors[1]);d.ellipse((198,280,446,321),fill=rgba(colors[3],35));
        rr(im,(264,93,378,288),colors[2],26);rr(im,(280,66,362,109),colors[3],10);rr(im,(282,160,360,219),colors[0],6);text(im,'M',321,189,40,colors[3]);line(im,[(283,113),(283,145)],rgba('#FFFFFF',110),5)
    elif i%4==2:
        d.polygon([(0,360),(0,282),(640,255),(640,360)],fill=colors[1]);
        for j in range(5):
            x=38+j*122;y=134-j%3*26;rr(im,(x,y,x+96,323),colors[2] if j%2 else colors[3],3)
            for r in range(5):
                for c in range(3):rr(im,(x+13+c*25,y+17+r*31,x+25+c*25,y+33+r*31),colors[0],1)
        circle(im,551,61,30,colors[4]);line(im,[(0,334),(640,297)],colors[0],3)
    else:
        circle(im,241,181,133,colors[1]);circle(im,412,174,110,colors[2]);
        d.polygon([(171,306),(317,52),(463,306)],fill=colors[4]);circle(im,332,230,68,colors[3]);
        for j in range(8): line(im,[(59+j*68,30),(40+j*68,75)],rgba(colors[3],100),3)
    return im.resize((w,h),Image.Resampling.LANCZOS)

@lru_cache(maxsize=32)
def _load(path):
    try:
        with Image.open(path) as src:
            if src.width*src.height>80_000_000: raise ValueError('Image too large')
            return ImageOps.exif_transpose(src).convert('RGBA').copy()
    except (OSError,ValueError,TypeError): return None

def _paths(cfg):
    paths=cfg.get('image_paths',[])
    if isinstance(paths,str): paths=[paths]
    if not isinstance(paths,(list,tuple)): paths=[]
    if cfg.get('image_path'): paths=[cfg['image_path']]+list(paths)
    return [str(p) for p in paths if isinstance(p,(str,Path))]

def _image(cfg,i,w,h,fill='#EEE5D8'):
    paths=_paths(cfg); src=_load(paths[i%len(paths)]) if paths else None
    if src is None:return _demo(i,w,h).copy()
    out=Image.new('RGBA',(int(w),int(h)),fill); fitted=ImageOps.contain(src,(int(w),int(h)),Image.Resampling.LANCZOS)
    out.alpha_composite(fitted,((out.width-fitted.width)//2,(out.height-fitted.height)//2)); return out

def _card(cfg,i,w=280,h=180,paper=False):
    pad=12 if paper else 5;bottom=32 if paper else pad
    im=Image.new('RGBA',(w+pad*2,h+pad+bottom),'#FFF8EC' if paper else '#213443')
    im.alpha_composite(_image(cfg,i,w,h),(pad,pad))
    if paper:text(im,f'{i+1:02d} / COLLECTION',pad+4,h+pad+bottom/2,11,'#66564D','mono',anchor='left')
    return im

def _shadow(dst,src,x,y,scale=1,angle=0,alpha=1):
    # Localized fast shadow, contained inside the composited panel dimensions.
    mask=src.getchannel('A');sh=Image.new('RGBA',src.size,(0,0,0,0)); sh.putalpha(mask.point(lambda v:int(v*.2)))
    paste(dst,sh,x+5,y+8,alpha,scale,angle);paste(dst,src,x,y,alpha,scale,angle)

def _paper(w,h,color,seed=0):
    im=Image.new('RGBA',(int(w),int(h)),color);d=ImageDraw.Draw(im)
    for y in range(8,h,11):d.line((5,y,w-5,y),fill=(80,55,45,12),width=1)
    # Deterministic drawn fibre speckles; no external raster textures.
    for n in range(90):
        x=(n*83+seed*31)%max(1,w);y=(n*47+seed*19)%max(1,h);d.point((x,y),fill=(70,45,35,25))
    return im

def _poly(dst,pts,fill):ImageDraw.Draw(dst).polygon([(int(x),int(y)) for x,y in pts],fill=fill)
def _mask_comp(a,b,mask):return Image.composite(b,a,mask)
def _curve(a,b,c,p):return ((1-p)**2*a[0]+2*(1-p)*p*b[0]+p*p*c[0],(1-p)**2*a[1]+2*(1-p)*p*b[1]+p*p*c[1])
def _cap(dst,s,x,y,p):text(dst,s,x,y,13,p['muted'],'mono')

def _titles(im,cfg,p,t):
    if not cfg.get('show_titles',True):return
    title=cfg.get('text','A NEW PERSPECTIVE');size=fit_size(title,1120,34)
    text(im,title,76,170,size,p['text'],anchor='left',opacity=life(t,.1,.75,4.45,5))
    text(im,cfg.get('subtitle',''),76,616,fit_size(cfg.get('subtitle',''),1120,17),p['muted'],'sans',anchor='left',opacity=life(t,.45,1.05,4.3,4.9))

def _match(st,t,v,cfg,p):
    q=enter(t,.1,1);switch=smooth(prog(t,2,3));out=1-leave(t,4.6,5)
    if v==0:
        for k in range(2):
            page=_paper(420,314,'#F5EDDF',k);d=ImageDraw.Draw(page)
            for row in range(12):line(page,[(29,31+row*22),(380-row%3*33,31+row*22)],'#B9AB95',5)
            yy=109 if k==0 else 153;rr(page,(53,yy,350,yy+28),p['accent'],2);text(page,'COMMON THREAD',69,yy+14,21,'#242C3D',anchor='left')
            x=mix(330 if k==0 else 840,580,switch);y=200+(-22 if k==0 else 22)*switch
            _shadow(st,page,x,y,scale=(1 if k==0 else .95)*q,alpha=out*(1-switch if k==0 else switch))
        rr(st,(453,175,707,216),None,8,rgba(p['accent'],210*out),3)
    elif v==1:
        for k in range(2):
            sc=q*(1+.3*switch);x=580+(k*2-1)*290*(1-switch);_shadow(st,_card(cfg,k,340,236),x,211,sc,alpha=out*(1 if switch<.5 else (1 if k==1 else 0)))
        for r in [30,78]:circle(st,580,210,r,None,rgba(p['accent'],180*out),2)
        line(st,[(480,210),(680,210)],p['accent'],2);line(st,[(580,112),(580,308)],p['accent'],2)
    elif v==2:
        for k in range(8):
            x=100+k*137;circle(st,x,200,34,p['secondary'] if k%2 else p['accent']);line(st,[(x,239),(x,274)],rgba(p['muted'],100),2)
        _shadow(st,_card(cfg,2,355,195),580,204,q*switch)
        circle(st,580,204,91+160*(1-switch),None,rgba(p['accent'],180*out),3)
    else:
        mp=Image.new('RGBA',(690,300),p['panel']);d=ImageDraw.Draw(mp)
        for k in range(9):line(mp,[(0,k*45),(690,k*45-90)],rgba(p['muted'],80),3)
        line(mp,[(40,240),(190,205),(365,82),(575,107),(650,31)],p['accent'],8)
        circle(mp,365,82,15,p['secondary']);_shadow(st,mp,420-180*switch,210,q*(1+.3*switch),alpha=out)
        _shadow(st,_card(cfg,2,320,214),857,210,q*switch,alpha=out)
        arrow(st,675,210,p['accent'],2)

def _cutouts(st,t,v,cfg,p):
    q=enter(t);off=leave(t);pulse=math.sin(t*2)*4
    if v==0:
        for j in range(5):
            paper=_paper(210,280,['#E7CBB2','#EDD9B6','#C8D9CD','#D5BEDC','#F4EADC'][j]);e=enter(t,.15+j*.13,1+j*.13)
            _shadow(st,paper,210+j*175,225+math.sin(j)*22,e*(1-off),(-9+j*4)*(1-.3*q))
        _shadow(st,_card(cfg,0,450,251,True),580,210+35*(1-q),q*(1-off),-4+pulse*.15)
        for j in range(3):line(st,[(346+j*30,78),(359+j*30,95)],p['accent'],4)
    elif v==1:
        src=_card(cfg,1,340,247,True)
        for j in range(4):_shadow(st,src,460+j*64,210+j*15,q*(1-off),-10+j*6,1 if j==3 else .18+j*.12)
        text(st,'CUT / KEEP / CREATE',265,368,25,p['accent'],'mono',anchor='left',opacity=q*(1-off))
    elif v==2:
        poses=[(330,206,-12),(570,234,7),(801,184,-5)]
        for j,(x,y,a) in enumerate(poses):
            e=enter(t,j*.25,j*.25+.8);_shadow(st,_card(cfg,j,295,204,True),x,y+80*(1-e),e*(1-off),a)
            rr(st,(x-41,y-120,x+40,y-95),rgba(p['accent'],150*e*(1-off)),1)
        circle(st,925,310,35,None,p['secondary'],3)
    else:
        src=_image(cfg,3,580,298);mask=Image.new('L',src.size,0);d=ImageDraw.Draw(mask);pts=[]
        for j in range(30):pts.append((j*20,10+(j*17)%13))
        pts +=[(580,294),(0,286)];d.polygon(pts,fill=255);src.putalpha(mask)
        for j in [2,1,0]:paste(st,src,580+j*25,220+j*18,q*(1-off)*(1 if j==0 else .3),1,-j*3)
        for j in range(6):line(st,[(835+j*14,65),(823+j*14,95)],p['accent'],3)

def _news(st,t,v,cfg,p):
    q=enter(t);out=1-leave(t);paper='#F0E5CF'
    if v==0:
        for j in range(7):
            strip=_paper(870,37,paper,j);line(strip,[(10,16),(800,16)],'#A99B88',3);e=enter(t,j*.1,.8+j*.1)
            _shadow(st,strip,580+(-1)**j*400*(1-e),75+j*43,alpha=out)
        _shadow(st,_card(cfg,2,382,238),580,222,q*out,-4)
    elif v==1:
        for j in range(4):
            sheet=_paper(670-j*72,289-j*22,[paper,'#CFC2AE','#D8CDBE','#E8DCCC'][j],j);d=ImageDraw.Draw(sheet)
            for row in range(10):line(sheet,[(25,25+row*23),(sheet.width-24,25+row*23)],'#AEA18F',3)
            e=enter(t,.1+j*.17,.9+j*.17);_shadow(st,sheet,580+12*j,214,e*out,-7+j*4)
        rr(st,(383,167,777,228),p['accent'],3);text(st,'FRESH PERSPECTIVE',580,198,29,'#223F4D',opacity=q*out)
    elif v==2:
        for j in range(12):
            x=210+j%4*245;y=83+j//4*124;e=enter(t,j%4*.11+j//4*.16,.9+j%4*.11+j//4*.16)
            src=_image(cfg,j,220,106);src.alpha_composite(_paper(220,106,'#DCD1BA',j).crop((0,0,5,106)),(0,0));_shadow(st,src,x,y,e*out,(-1)**j*5*(1-e))
    else:
        for j in range(3):
            book=_paper(320,320,paper,j);paste(book,_image(cfg,j,286,188),160,128);text(book,'EDITORIAL',160,259,28,'#413E3A','serif');text(book,f'VOL. {j+1:02d}',160,294,15,'#756B5A','mono')
            e=enter(t,j*.2,.8+j*.2);_shadow(st,book,320+j*250,217,e*out,-11+j*11)

def _film(st,t,v,cfg,p):
    q=enter(t);out=1-leave(t)
    if v==0:
        for j in range(5):
            src=_card(cfg,j,234,170);x=70+j*264-((t*.23)%1)*264
            _shadow(st,src,x,214,q*out)
        for x in range(34,1140,26):
            for y in (100,327):rr(st,(x,y,x+16,y+14),rgba(p['muted'],100),2)
        line(st,[(0,93),(1160,93)],p['secondary'],3);line(st,[(0,354),(1160,354)],p['secondary'],3)
    elif v==1:
        for j in range(5):
            a=(-65+j*32+math.sin(t*.6)*12)*math.pi/180;x=580+390*math.sin(a);y=400-215*math.cos(a)
            _shadow(st,_card(cfg,j,188,142),x,y,q*out,-a*180/math.pi*.24)
        circle(st,580,382,57,None,p['accent'],3);circle(st,580,382,18,p['secondary'])
    elif v==2:
        rr(st,(156,100,1004,335),'#171B20',8);src=_image(cfg,int(t//1.25)%4,673,212);paste(st,src,580,214,q*out)
        for y in range(116,328,38):
            for x in (175,969):rr(st,(x,y,x+16,y+23),p['muted'],3)
        for x in range(190,986,25):line(st,[(x,346),(x+12,346)],p['accent'],4)
        text(st,'24   /   MOTION STUDIES',580,384,18,p['muted'],'mono',opacity=q*out)
    else:
        for j in range(7,-1,-1):
            z=(j+(t*.55)%1);sc=.86**z;x=580+(-1)**j*175*(1-sc);src=_card(cfg,j,690,305)
            _shadow(st,src,x,212,sc*q*out,(-1)**j*3,1 if j==0 else .32)

def _editorial(st,t,v,cfg,p):
    q=enter(t);o=1-leave(t)
    if v==0:
        book=_paper(900,322,'#F2E9D8');paste(book,_image(cfg,0,426,266),233,158);text(book,'FORM',660,102,73,'#233644','serif');text(book,'AND FUNCTION',657,167,23,'#657C80','mono');
        for j in range(6):line(book,[(495,210+j*11),(805-j%3*25,210+j*11)],'#B6AB99',2)
        line(book,[(453,0),(453,322)],'#C8BAA1',2);_shadow(st,book,580,215,q*o)
    elif v==1:
        for j in range(9):
            e=enter(t,j*.07,.7+j*.07);_shadow(st,_card(cfg,j,224,114,True),294+j%3*285,84+j//3*130,e*o)
        rr(st,(190,22,956,413),None,5,rgba(p['accent'],80*o),2)
    elif v==2:
        a=smooth(prog(t,.3,1.5));src=_paper(368,328,'#EEE3D0');paste(src,_image(cfg,2,320,201),184,163);text(src,'URBAN / 03',184,35,25,'#253C4C','serif');
        _shadow(st,src,580,215,q*o);flap=_paper(max(1,int(185*(1-a))),328,'#D5C5AE');paste(st,flap,580+flap.width/2,215,o)
        if a>.1:text(st,'NEW ISSUE',866,205,27,p['accent'],opacity=a*o)
    else:
        for j,(x,y,w,h) in enumerate([(345,209,396,283),(742,139,252,144),(795,307,338,150)]):
            e=enter(t,.15+j*.18,1+j*.18);_shadow(st,_card(cfg,j,w,h),x,y+50*(1-e),e*o,-3+j*2)
        text(st,'01',991,348,48,p['accent'],'serif',opacity=q*o)

def _parallax(st,t,v,cfg,p):
    q=enter(t);o=1-leave(t);pan=math.sin(t*.55)*24
    if v==0:
        # Honest 2.5D: independently moving planes with depth-dependent displacement.
        for j in range(3):
            src=_image(cfg,j,790-j*120,322-j*52);_shadow(st,src,580+pan*(j*.8-1),216+j*14,q*o,0,.24 if j<2 else 1)
        for j in range(3):_poly(st,[(20+j*36,395),(158+j*36,163),(221+j*36,395)],rgba(p['accent'],50+j*25))
    elif v==1:
        paste(st,_image(cfg,0,920,350),580+pan*.35,210,q*o)
        for j in range(2):
            src=_paper(210,390,p['panel'],j);_shadow(st,src,85+j*985-pan*2,215,q*o,(-1)**j*6)
        line(st,[(188,37),(960,392)],rgba(p['secondary'],90),2)
    elif v==2:
        for j in [0,2,1]:
            z=[.58,1,.75][j];x=[306,612,916][j]+pan*z*2;y=[195,233,168][j];_shadow(st,_card(cfg,j,310,200),x,y,q*z*o,[-5,2,7][j])
            line(st,[(x,320),(x,366)],p['accent'],2);_cap(st,['BACKGROUND','HERO PLANE','DETAIL'][j],x,385,p)
    else:
        for j in range(5):
            pts=[(0,428),(0,250+j*27),(190+pan*(j+1),103+j*47),(433+pan*j,283),(732+pan*(j+1),95+j*43),(1160,255+j*27),(1160,428)]
            _poly(st,pts,rgba([p['panel'],p['secondary'],p['accent'],p['panel'],p['bg']][j],255 if j in (0,4) else 155))
        circle(st,832+pan*.3,97,35,p['accent']);
        if _paths(cfg):_shadow(st,_card(cfg,0,420,222),580,231,q*o)

def _depth(st,t,v,cfg,p):
    q=enter(t);o=1-leave(t);phase=smooth(prog(t,1.2,3.8))
    if v==0:
        for j in range(6,-1,-1):
            sc=.78**(j+(1-phase));im=_card(cfg,j,838,332);paste(st,im,580,214,o*(.3+j*.05 if j else 1),sc*q)
            line(st,[(580-424*sc,214-168*sc),(580+424*sc,214-168*sc)],rgba(p['accent'],100),1)
    elif v==1:
        for j in sorted(range(5),key=lambda j:math.cos(j*math.tau/5+t*.55)):
            a=j*math.tau/5+t*.55;x=580+400*math.sin(a);z=.68+.25*math.cos(a);_shadow(st,_card(cfg,j,295,220),x,218-25*math.cos(a),q*z*o,math.sin(a)*7)
        ImageDraw.Draw(st).arc((171,121,989,409),0,180,fill=p['accent'],width=2)
    elif v==2:
        for j in range(5,-1,-1):
            sc=.9/(1+j*.37);x=580+(-1)**j*(400-150*phase)*sc;y=213-j*4;_shadow(st,_card(cfg,j,376,252),x,y,q*sc*o,(-1)**j*7)
        line(st,[(505,385),(566,154)],rgba(p['muted'],120),2);line(st,[(655,385),(594,154)],rgba(p['muted'],120),2)
    else:
        for j in range(5,-1,-1):
            e=enter(t,.1+j*.1,.85+j*.1);x=580+(j-2)*57*phase;y=220+j*10-40*phase*j/5;_shadow(st,_card(cfg,j,485,269),x,y,e*o,(-3+j*2)*phase)

def _blocks(st,t,v,cfg,p):
    q=enter(t);o=1-leave(t)
    if v==0:
        for j in range(4):
            e=enter(t,j*.18,.8+j*.18);x=275+j*207;y=265-j*44;rr(st,(x-90,y-90*e,x+90,y+89),p['accent'] if j%2 else p['secondary'],2)
            _shadow(st,_card(cfg,j,164,119),x,y-12,e*o)
        line(st,[(150,373),(1010,373)],p['muted'],2)
    elif v==1:
        src=_image(cfg,0,810,318)
        for j in range(24):
            c=j%6;r=j//6;e=enter(t,(c+r)*.1,.75+(c+r)*.1);piece=src.crop((c*135,r*79,(c+1)*135,(r+1)*79));paste(st,piece,242+c*135,95+r*79,o,e,180*(1-e))
    elif v==2:
        for j in range(4):
            e=enter(t,.1+j*.15,.9+j*.15);src=_image(cfg,j,610,230);x=580+(-1)**j*160*(1-e);y=170+j*21
            paste(st,src,x,y,q*o*(.3 if j<3 else 1));rr(st,(x-335,y-119,x-315,y+119),p['accent'] if j%2 else p['secondary'],0)
    else:
        paste(st,_image(cfg,1,860,330),580,215,q*o)
        for j in range(4):
            e=enter(t,.1+j*.16,1.4+j*.16);w=425*(1-e);h=166*(1-e);cx=580+(-1 if j%2==0 else 1)*213;cy=215+(-1 if j<2 else 1)*83
            rr(st,(cx-w/2,cy-h/2,cx+w/2,cy+h/2),p['panel'],0)

def _origami(st,t,v,cfg,p):
    q=enter(t);o=1-leave(t);d=ImageDraw.Draw(st)
    if v==0:
        for j in range(9):
            a=(-80+j*20)*math.pi/180*ease(prog(t,.15,1.8));x=580+260*math.sin(a);y=315-245*math.cos(a)
            page=_paper(190,241,[p['secondary'],p['accent'],'#D8E2DC'][j%3],j);_shadow(st,page,x,y,q*o,-a*180/math.pi)
        _shadow(st,_card(cfg,0,235,152),580,269,q*o)
    elif v==1:
        e=smooth(prog(t,.3,1.7));paste(st,_image(cfg,1,720,300),580,215,q*o)
        for j in range(2):
            width=360*(1-e);x=220 if j==0 else 940-width;_poly(st,[(x,65),(x+width,65+35*e),(x+width,365-35*e),(x,365)],p['accent'] if j==0 else p['secondary'])
    elif v==2:
        for j in range(8):
            e=enter(t,j*.09,.9+j*.09);x=190+j*111;src=_image(cfg,j,94,268);_shadow(st,src,x,213,e*o)
            _poly(st,[(x+47,79),(x+65,95),(x+65,346),(x+47,347)],rgba(p['muted'],80))
        for j in range(7):line(st,[(245+j*111,82),(245+j*111,347)],p['accent'],2)
    else:
        for j in range(8):
            a=j*math.tau/8;e=enter(t,j*.1,.75+j*.1);r=135*e;src=_paper(105,169,p['secondary'] if j%2 else p['accent'],j);_shadow(st,src,580+r*math.sin(a),220-r*math.cos(a),q*o,a*180/math.pi)
        circle(st,580,220,58,p['panel']);text(st,'CREATE',580,220,18,p['text'],opacity=q*o)

def _accordion(st,t,v,cfg,p):
    q=enter(t);o=1-leave(t);fold=ease(prog(t,.2,1.9))
    if v==0:
        for j in range(5):
            w=int(90+70*fold);src=_image(cfg,j,w,269);x=580+(j-2)*(w+9);_shadow(st,src,x,217,q*o);_poly(st,[(x+w/2,82),(x+w/2+10,95),(x+w/2+10,338),(x+w/2,351)],rgba(p['muted'],80))
    elif v==1:
        for j in range(6):
            x=200+j*145;top=118+(j%2)*37*(1-fold);src=_paper(145,240,'#E4DDC5',j);line(src,[(5,130),(70,87),(144,109)],'#667B70',7);_shadow(st,src,x,top+105,q*o,(-1)**j*8*(1-fold))
        circle(st,707,209,14,p['accent']);_cap(st,'JOURNEY / UNFOLD',580,391,p)
    elif v==2:
        page=_paper(810,160,'#E8D9BD');_shadow(st,page,580,299,q*o)
        for j in range(3):
            src=_card(cfg,j,213,183,True);_shadow(st,src,340+j*240,277-83*fold,q*o,(-1)**j*8*(1-fold))
        line(st,[(580,225),(580,373)],'#B09E82',2)
    else:
        for j in range(4):
            x=580+(-1 if j%2==0 else 1)*(100+120*fold)*(1 if j<2 else 1.65);src=_paper(198,267,p['secondary'] if j<2 else p['accent'],j);_shadow(st,src,x,215,q*o,(-1)**j*24*fold)
        _shadow(st,_card(cfg,0,307,191),580,213,q*o)

def _product(st,t,v,cfg,p):
    q=enter(t);o=1-leave(t);floaty=math.sin(t*1.7)*6
    if v==0:
        d=ImageDraw.Draw(st);d.ellipse((280,291,881,389),fill=p['panel'],outline=p['secondary'],width=2);rr(st,(280,319,881,383),p['panel'],2)
        _shadow(st,_image(cfg,1,367,274),580,211+floaty,q*o,-3*math.sin(t*.5));line(st,[(316,397),(846,397)],p['accent'],3)
    elif v==1:
        for j in range(3):
            x=260+j*320;e=enter(t,j*.2,.9+j*.2);_poly(st,[(x-126,298),(x+126,298),(x+150,333),(x-150,333)],p['secondary']);_poly(st,[(x-150,333),(x+150,333),(x+150,351),(x-150,351)],p['panel']);_shadow(st,_image(cfg,j,240,213),x,187+floaty*(j+1)/2,e*o)
    elif v==2:
        _poly(st,[(415,20),(745,20),(956,367),(204,367)],rgba(p['secondary'],40));rr(st,(308,30,852,374),None,120,rgba(p['accent'],80),2)
        _shadow(st,_image(cfg,1,430,286),580,210+floaty,q*o);circle(st,580,363,65,None,rgba(p['accent'],160),2)
    else:
        for j in range(4):
            e=enter(t,j*.13,.9+j*.13);src=_image(cfg,1,268,179);_shadow(st,src,440+j*88,283-j*45,e*o,-5+j*3)
            line(st,[(785+j*12,129+j*62),(994,129+j*62)],p['accent'],2);_cap(st,['FORM','DETAIL','FINISH','PURPOSE'][j],1045,129+j*62,p)

def _trail(st,t,v,cfg,p):
    q=enter(t);o=1-leave(t)
    if v==0:
        for j in range(7,-1,-1):
            a=t*.6-j*.17;x=580+190*math.sin(a);y=215+64*math.cos(a);_shadow(st,_card(cfg,j%4,354,220),x,y,q*o,math.sin(a)*8,1-j*.09)
    elif v==1:
        for j in range(5):
            e=enter(t,j*.25,.7+j*.25);_shadow(st,_card(cfg,j,245,162,True),227+j*185,150+(j%2)*102,e*o,-10+j*5)
            if e>.95:_cap(st,f'{j+1:02d}',227+j*185,366,p)
    elif v==2:
        for j in range(6,0,-1):paste(st,_image(cfg,3,590,295),580-j*32*math.sin(t),215,q*o*.09,1)
        _shadow(st,_card(cfg,3,590,295),580,215,q*o);line(st,[(207,82),(313,82)],p['accent'],4);line(st,[(866,347),(970,347)],p['accent'],4)
    else:
        for j in range(4):
            a=prog(t,.2+j*.5,1+j*.5);pos=_curve((80,340),(410+j*88,-10),(300+j*190,205+(-1)**j*80),ease(a));_shadow(st,_card(cfg,j,230,161),pos[0],pos[1],q*o,(-8+j*5)*(1-a))
        line(st,[(116,375),(408,94),(963,306)],rgba(p['muted'],70),2)

def _stickers(st,t,v,cfg,p):
    q=enter(t);o=1-leave(t);poses=[(255,141),(465,276),(710,144),(932,289)]
    if v==0:
        for j,(x,y) in enumerate(poses):
            e=pop(prog(t,j*.15,.9+j*.15));_shadow(st,_card(cfg,j,233,143,True),x,y-60*(1-e),max(0,e)*o,(-1)**j*9);circle(st,x,y-89,8,p['accent'])
    elif v==1:
        for j in range(6):
            a=j*math.tau/6+t*.4;r=mix(355,175,smooth(prog(t,1,3)));_shadow(st,_card(cfg,j,168,121,True),580+r*math.sin(a),215+r*.58*math.cos(a),q*o,math.sin(a)*10)
        circle(st,580,215,58,p['accent']);text(st,'CURATE',580,215,18,p['bg'],opacity=q*o)
    elif v==2:
        sheet=_paper(812,320,'#E8E2D0');_shadow(st,sheet,580,215,q*o)
        for j in range(6):
            x=318+j%3*261;y=144+j//3*144;e=enter(t,j*.17,.85+j*.17);_shadow(st,_card(cfg,j,220,117),x,y-(22 if j==4 else 0)*math.sin(t),q*o,-7*e if j==4 else 0)
        line(st,[(239,371),(922,371)],rgba(p['muted'],80),2)
    else:
        for j,(x,y) in enumerate(poses):
            e=enter(t,j*.15,.9+j*.15);bounce=math.exp(-max(0,t-.7-j*.15)*2)*math.sin((t-j*.15)*9)*25;_shadow(st,_card(cfg,j,227,152,True),x,y+bounce,q*o,math.sin(t*1.7+j)*5)
            for k in range(7):line(st,[(x,y-94+k*4),(x+(-1)**k*7,y-90+k*4)],rgba(p['accent'],150*e),2)

def _split(st,t,v,cfg,p):
    q=enter(t);o=1-leave(t)
    if v==0:
        for j in range(2):
            e=enter(t,j*.3,1+j*.3);im=_image(cfg,j,405,305);ww=max(1,int(im.width*e));im=im.resize((ww,305),Image.Resampling.BICUBIC);_shadow(st,im,368+j*425,216,q*o)
        line(st,[(580,56),(580,375)],p['accent'],4)
    elif v==1:
        for j in range(3):
            e=enter(t,j*.18,1+j*.18);_shadow(st,_card(cfg,j,258,316),305+j*280,216+(-1)**j*250*(1-e),q*o)
    elif v==2:
        src=_image(cfg,2,846,306)
        for j in range(6):
            e=enter(t,j*.1,1+j*.1);piece=src.crop((j*141,0,(j+1)*141,306));_shadow(st,piece,228+j*141,216+(-1)**j*140*(1-e),q*o)
        line(st,[(157,58),(1003,58)],p['accent'],2)
    else:
        src=_image(cfg,0,812,306)
        for j in range(8):
            e=enter(t,(j%4+j//4)*.17,1+(j%4+j//4)*.17);piece=src.crop((j%4*203,j//4*153,j%4*203+203,j//4*153+153));_shadow(st,piece,276+j%4*203+(-1)**j*160*(1-e),139+j//4*153,q*o,(-1)**j*12*(1-e))

def _shape(st,t,v,cfg,p):
    q=enter(t);o=1-leave(t);a=smooth(prog(t,1.1,2.8))
    if v==0:
        src=_image(cfg,0,650,325);mask=Image.new('L',src.size);d=ImageDraw.Draw(mask);r=36+440*a;d.ellipse((325-r,163-r,325+r,163+r),fill=255);src.putalpha(mask);_shadow(st,src,580,215,q*o);circle(st,580,215,36+135*(1-a),None,rgba(p['accent'],200*(1-a)),5)
    elif v==1:
        src=_image(cfg,3,683,326);mask=Image.new('L',src.size);d=ImageDraw.Draw(mask);wide=40+683*a;d.polygon([(341,160-wide*.75),(341-wide*.9,160+wide*.55),(341+wide*.9,160+wide*.55)],fill=255);src.putalpha(mask);_shadow(st,src,580,215,q*o)
        if a<1:line(st,[(580,85),(466,292),(694,292),(580,85)],rgba(p['accent'],190*(1-a)),4)
    elif v==2:
        src=_image(cfg,2,760,max(1,int(6+306*a)));_shadow(st,src,580,215,q*o);line(st,[(200,215-153*a),(960,215-153*a)],p['accent'],4);line(st,[(200,215+153*a),(960,215+153*a)],p['accent'],4)
    else:
        for j in range(6):
            x=284+j%3*296;y=133+j//3*176;sc=.04+.96*enter(t,.2+j*.12,1.6+j*.12);_shadow(st,_card(cfg,j,254,141),x,y,sc*q*o,18*(1-sc))
        circle(st,580,215,21*(1-a),p['accent'])

def _grid(st,t,v,cfg,p):
    o=1-leave(t)
    if v==0:
        order=[0,1,2,3,7,6,5,4,8,9,10,11]
        for j in range(12):
            k=order.index(j);e=enter(t,k*.07,.6+k*.07);_shadow(st,_card(cfg,j,215,101),228+j%4*235,91+j//4*122,e*o)
    elif v==1:
        for j in range(9):
            e=enter(t,j*.09,.65+j*.09);y=97+j//3*128+math.exp(-max(0,t-.55-j*.09)*3)*math.sin((t-j*.09)*12)*16;_shadow(st,_card(cfg,j,241,104),313+j%3*268,y-(1-e)*260,e*o)
    elif v==2:
        for j in range(12):
            c=j%4;r=j//4;e=enter(t,(c+r)*.14,.7+(c+r)*.14);_shadow(st,_card(cfg,j,221,105),222+c*239,91+r*126,e*o,-15*(1-e))
    else:
        q=enter(t)
        for j in range(7):
            a=j*math.tau/7+math.sin(t*.7)*.3;r=300 if j else 0;x=580+r*math.sin(a);y=215+r*.5*math.cos(a);_shadow(st,_card(cfg,j,203 if j else 313,132 if j else 211),x,y,q*o,math.sin(a)*5)

def _callouts(st,t,v,cfg,p):
    q=enter(t);o=1-leave(t)
    _shadow(st,_image(cfg,1,399,294),580,217,q*o)
    if v==0:
        for j in range(6):
            a=j*math.tau/6;e=enter(t,.35+j*.1,1.25+j*.1);x=580+360*math.sin(a);y=218+155*math.cos(a);line(st,[(580+math.sin(a)*183,217+math.cos(a)*115),(x,y)],rgba(p['accent'],180*e*o),2);circle(st,x,y,30,p['panel'],p['accent'],2);text(st,str(j+1),x,y,22,p['accent'],opacity=e*o)
    elif v==1:
        for j in range(4):
            e=enter(t,.3+j*.2,1.3+j*.2);side=-1 if j<2 else 1;x=580+side*320;y=119+j%2*190;line(st,[(580+side*125,y+24),(x-side*54,y),(x,y)],rgba(p['accent'],190*e*o),3);circle(st,580+side*125,y+24,6,p['accent']);text(st,['SURFACE','STRUCTURE','DETAIL','FINISH'][j],x+side*28,y,18,p['text'],anchor='right' if side<0 else 'left',opacity=e*o)
    elif v==2:
        for j in range(4):
            e=enter(t,.3+j*.2,1.2+j*.2);x=260 if j%2==0 else 900;y=113 if j<2 else 315;rr(st,(x-93,y-35,x+93,y+35),p['panel'],10,p['secondary']);text(st,['MATERIAL','FORM','FEEL','PURPOSE'][j],x,y,19,p['text'],opacity=e*o);line(st,[(x+(93 if j%2==0 else -93),y),(580+(-160 if j%2==0 else 160),217)],rgba(p['accent'],170*e*o),2)
    else:
        x=740+math.sin(t*.7)*70;y=210+math.cos(t*.7)*30;src=_image(cfg,1,339,251);mask=Image.new('L',src.size);ImageDraw.Draw(mask).ellipse((64,18,277,231),fill=255);src.putalpha(mask);paste(st,src,x,y,q*o);circle(st,x,y,109,None,p['accent'],5);line(st,[(x+80,y+80),(x+153,y+153)],p['accent'],12);text(st,'THE FINER DETAILS',261,336,24,p['text'],opacity=q*o)

def _transition(st,t,g,v,cfg,p):
    """Pixel-wise original transition masks: exact A at 0, exact B at 5."""
    # In atlas use safe body viewport; clean use whole frame.
    full=(not cfg.get('_labels',True) and not cfg.get('show_titles',True))
    ww,hh=(W,H) if full else (1000,380)
    a=_image(cfg,0,ww,hh,cfg.get('bg',p['bg']));b=_image(cfg,1,ww,hh,cfg.get('bg',p['bg']))
    s=smooth(prog(t,.2,4.8));mask=Image.new('L',(ww,hh),0);d=ImageDraw.Draw(mask)
    if s>=1:mask.paste(255,(0,0,ww,hh))
    elif s>0:
        if g==8: # Liquid contours: wave, droplet swarm, organic lattice, ink cloud.
            if v==0:
                pts=[(0,hh),(ww,hh)]+[(x,int(hh*(1-s)+math.sin(x/ww*math.tau*2+s*6)*hh*.075*math.sin(s*math.pi))) for x in range(ww,-1,-20)];d.polygon(pts,fill=255)
            elif v==1:
                for j in range(13):
                    x=(j*137+73)%ww;y=(j*89+51)%hh;r=max(0,(s-j*.008))**2*ww*.38;d.ellipse((x-r,y-r,x+r,y+r),fill=255)
            elif v==2:
                for j in range(8):
                    x=j*ww/7;y=hh*.5+math.sin(j*1.4+s*4)*hh*.23;r=s*s*hh*1.3;d.ellipse((x-r,y-r,x+r,y+r),fill=255)
            else:
                for j in range(21):
                    a0=j*2.4;x=ww*.5+math.sin(a0)*ww*.24;y=hh*.5+math.cos(a0)*hh*.27;r=s*s*ww*.3;d.ellipse((x-r,y-r*.55,x+r,y+r*.55),fill=255)
        elif g==9: # Light-wipe masks with different reveal geometry.
            if v==0:d.rectangle((0,0,ww*s,hh),fill=255)
            elif v==1:
                d.rectangle((ww/2-ww*s/2,0,ww/2+ww*s/2,hh),fill=255);d.rectangle((0,hh/2-hh*s/2,ww,hh/2+hh*s/2),fill=255)
            elif v==2:d.polygon([(-hh,0),(s*(ww+hh)-hh,0),(s*(ww+hh),hh),(-hh,hh)],fill=255)
            else:
                thick=(min(ww,hh)/2+5)*s;d.rectangle((0,0,ww,thick),fill=255);d.rectangle((0,hh-thick,ww,hh),fill=255);d.rectangle((0,0,thick,hh),fill=255);d.rectangle((ww-thick,0,ww,hh),fill=255)
        elif g==12: # Peel mechanisms; source planes remain uncropped at endpoints.
            if v==0:d.polygon([(0,0),(s*(ww+hh),0),(0,s*(ww+hh))],fill=255)
            elif v==1:
                for j in range(8):
                    e=clamp((s-j*.028)/.8);d.rectangle((j*ww/8,hh*(1-e),(j+1)*ww/8,hh),fill=255)
            elif v==2:
                edge=ww*(1-s);d.rectangle((edge,0,ww,hh),fill=255)
            else:
                e=s*1.4;d.rounded_rectangle((ww/2-ww*e/2,hh/2-hh*e/2,ww/2+ww*e/2,hh/2+hh*e/2),radius=min(ww,hh)*.1*(1-s),fill=255)
        elif g==13: # Stencil construction.
            if v==0:
                for j in range(24):
                    x=(j%8+.5)*ww/8;y=(j//8+.5)*hh/3;r=s*ww/9;d.ellipse((x-r,y-r,x+r,y+r),fill=255)
            elif v==1:
                f=font(int(hh*.53));bbox=d.textbbox((0,0),'MOVE',font=f);d.text(((ww-(bbox[2]-bbox[0]))/2,hh*.17),'MOVE',font=f,fill=255,stroke_width=int(s*s*ww*.09));
                if s>.8:d.rectangle((0,0,ww,hh),fill=round(255*(s-.8)/.2))
            elif v==2:
                for j in range(12):
                    r=j//4;c=j%4;e=clamp((s-(r+c)*.04)/.7);cw=ww/4*e;ch=hh/3*e;cx=(c+.5)*ww/4;cy=(r+.5)*hh/3;d.rectangle((cx-cw/2,cy-ch/2,cx+cw/2,cy+ch/2),fill=255)
            else:
                for j in range(18):
                    x=(j+.5)*ww/18;e=clamp((s-j*.022)/.65);d.rectangle((x-ww/36*e,0,x+ww/36*e,hh),fill=255)
        elif g==15: # Halftone mechanisms.
            if v==0:
                for y in range(0,hh+1,29):
                    for x in range(0,ww+1,29):
                        delay=((x*13+y*7)%97)/97*.2;r=max(0,(s-delay)/.8)*25;d.ellipse((x-r,y-r,x+r,y+r),fill=255)
            elif v==1:
                for j in range(11):
                    r=s*ww*.75-j*ww*.045
                    if r>0:d.ellipse((ww/2-r,hh/2-r,ww/2+r,hh/2+r),fill=255)
            elif v==2:
                for j in range(40):
                    delay=j%7*.028;e=clamp((s-delay)/.79);d.rectangle((0,j*hh/40,ww*e,(j+1)*hh/40),fill=255)
            else:
                for j in range(72):
                    x=(j%12+.5)*ww/12;y=(j//12+.5)*hh/6;dist=math.hypot((x-ww/2)/ww,(y-hh/2)/hh);r=clamp((s-dist*.24)/.7)*ww/10;d.ellipse((x-r,y-r,x+r,y+r),fill=255)
        elif g==17: # Optical masks.
            if v==0:
                r=s*math.hypot(ww,hh)/2*1.15;pts=[(ww/2+r*math.sin(j*math.tau/8+s),hh/2+r*math.cos(j*math.tau/8+s)) for j in range(8)];d.polygon(pts,fill=255)
            elif v==1:
                r=s*ww*.56;d.ellipse((ww*.5-r,hh*.5-r,ww*.5+r,hh*.5+r),fill=255);mask=mask.filter(ImageFilter.GaussianBlur(6+math.sin(s*math.pi)*12))
            elif v==2:
                for cx in [ww*.25,ww*.75]:
                    r=s*ww*.4;d.ellipse((cx-r,hh*.5-r,cx+r,hh*.5+r),fill=255)
            else:
                for j in range(10):
                    a0=j*math.tau/10;cx=ww*.5+math.sin(a0)*ww*.25*(1-s);cy=hh*.5+math.cos(a0)*hh*.25*(1-s);r=s*ww*.33;d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=255)
        elif g==20: # Shutter plates.
            if v==0:
                for j in range(12):
                    e=clamp((s-j*.015)/.82);cx=(j+.5)*ww/12;d.rectangle((cx-ww/24*e,0,cx+ww/24*e,hh),fill=255)
            elif v==1:
                for j in range(10):
                    cy=(j+.5)*hh/10;e=clamp((s-j*.018)/.8);d.rectangle((0,cy-hh/20*e,ww,cy+hh/20*e),fill=255)
            elif v==2:
                for j in range(9):
                    x=j*ww/9;d.polygon([(x-s*ww/18,0),(x+s*ww/18,0),(x+s*ww/18+hh*.12,hh),(x-s*ww/18+hh*.12,hh)],fill=255)
            else:
                d.rectangle((0,0,ww*s/2,hh),fill=255);d.rectangle((ww-ww*s/2,0,ww,hh),fill=255)
        else: # Ribbon and curtain weaves.
            if v==0:
                for j in range(14):
                    e=clamp((s-j%3*.06)/.8);yy=j*hh/14;d.rectangle((0 if j%2==0 else ww*(1-e),yy,ww*e if j%2==0 else ww,yy+hh/14+1),fill=255)
            elif v==1:
                for j in range(12):
                    yy=j*hh/12;x=ww*s+math.sin(j*.8+s*6)*ww*.07*math.sin(s*math.pi);d.rectangle((0,yy,x,yy+hh/12+1),fill=255)
            elif v==2:
                for j in range(8):
                    yy=j*hh/8;e=clamp((s-j*.025)/.79);left=ww*.5*(1-e);d.rectangle((left,yy,ww-left,yy+hh/8+1),fill=255)
            else:
                center=ww/2;extent=s*ww/2;d.rectangle((center-extent,0,center+extent,hh),fill=255)
    comp=_mask_comp(a,b,mask)
    if full:st.alpha_composite(comp,(0,0));return
    _shadow(st,comp,580,215)
    if .03<s<.97 and g in (9,12):
        edge=(s*1000 if g==9 and v==0 else 500);line(st,[(80+edge,29),(80+edge,401)],rgba(p['accent'],160*math.sin(s*math.pi)),3)

DRAW={0:_match,1:_cutouts,2:_news,3:_film,4:_editorial,5:_parallax,6:_depth,7:_blocks,10:_origami,11:_accordion,14:_stickers,16:_split,18:_product,19:_trail,21:_shape,22:_grid,23:_callouts}
TRANSITIONS={8,9,12,13,15,17,20,24}

def render(pid,t,cfg):
    k=int(pid[2:])-301;g,v=divmod(k,4);p=palette(cfg)
    if g in TRANSITIONS and not cfg.get('_labels',True) and not cfg.get('show_titles',True):
        full=layer();_transition(full,t,g,v,cfg,p);return full
    im=base(cfg);st=layer(1160,430)
    if g in TRANSITIONS:_transition(st,t,g,v,cfg,p)
    else:DRAW[g](st,t,v,cfg,p)
    # All scene graphics stay between y=201 and y=593; title/subtitle have
    # separate bands. Viewport clipping prevents rotated collage overlap.
    paste(im,st,640,397,scale=.90);_titles(im,cfg,p,t)
    return im
