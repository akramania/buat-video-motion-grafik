"""48 original renderable 2D/2.5D motion-graphic interpretations of MotionPrompt styles.

The public examples motivate the art direction; all shapes are locally drawn.
Illustrative faux-depth is not a claim that a Three.js scene or source footage
is bundled. Each MPxx has its own scene function and independently moving parts.
"""
from core import *
from PIL import ImageOps
from functools import lru_cache
import random

# ID, source slug, display name, palette, heading, supporting line, motion mechanism.
ROWS = [
 ('MP01','kaiju-attack','Kaiju attack','promo','IDEA BESAR','Mesej anda menguasai kota.','model city shake, monster rise, beam-written title'),
 ('MP02','infographic','Infographic','education','LANGKAH MUDAH','Daripada langkah kepada hasil.','poster pan, staggered steps, pictogram counter'),
 ('MP03','radial-infographic','Radial infographic','corporate','KITARAN IDEA','Setiap langkah saling berkait.','shutter wheel assembly and rotating point focus'),
 ('MP04','slide-deck','Slide deck','education','SLIDE HIDUP','Bentangkan idea dengan jelas.','perspective slide table with flying focus'),
 ('MP05','flat-illustration','Flat illustration','education','JELASKAN IDEA','Watak, papan dan carta bergerak.','rigged vector presenter and drawn charts'),
 ('MP06','isometric-diorama','Isometric diorama','saas','DUNIA KECIL','Produk tumbuh di atas pentas.','isometric stage with independently popping props'),
 ('MP07','kinetic-type','Kinetic typography','promo','CIPTA GERAK','Kata bergerak mengikut beat.','phrase punches, individual glyph offsets'),
 ('MP08','malaysian-heritage','Malaysian heritage','documentary','WARISAN KITA','Motif tempatan dengan rasa baharu.','flying wau, drawn batik, unrolling songket'),
 ('MP09','app-showcase','App showcase','saas','APLIKASI ANDA','Aliran yang boleh dilihat.','tilting phone, scrolling screen, feature popouts'),
 ('MP10','kawaii-pastel','Kawaii pastel','creator','IDEA COMEL','Watak dan pelekat hidup.','chibi arm wave, sticker orbit, bubble typography'),
 ('MP11','tech-noir','Tech noir','saas','SISTEM BERHUBUNG','Data mengalir antara peranti.','dotted globe, circuit pulses and particle type'),
 ('MP12','food-menu','Food menu','promo','MENU PILIHAN','Hidangan hero mendapat tumpuan.','ingredient drop, rotating plate, menu price card'),
 ('MP13','neon-sign','Neon sign','creator','CAHAYA IDEA','Huruf neon menyala satu persatu.','tube segments flicker and wall reflections'),
 ('MP14','map-journey','Map journey','education','JEJAK PERJALANAN','Setiap destinasi ada ceritanya.','map route tracing, pins and travel card'),
 ('MP15','liquid-gradient','Liquid gradient','creator','ALIRAN WARNA','Latar organik untuk mesej utama.','independent soft blob motion and mask reveal'),
 ('MP16','festive-raya','Festive Raya','documentary','SALAM AIDILFITRI','Cahaya pelita dan ketupat berayun.','ketupat sway, sequential lamps and star ornaments'),
 ('MP17','data-story','Data story','corporate','CERITA DATA','Angka menunjukkan perubahan.','bars, line, donut and synchronized metric'),
 ('MP18','claymation','Claymation','creator','BENTUK BAHARU','Objek tanah liat berubah bentuk.','stepped squash-stretch clay buddy and props'),
 ('MP19','retro-synthwave','Retro synthwave','promo','MENUJU MASA DEPAN','Grid neon dan matahari retro.','moving horizon grid and chrome highlight'),
 ('MP20','elegant-wedding','Elegant wedding','documentary','HARI ISTIMEWA','Bunga mekar mengelilingi nama.','watercolour bloom and gold arch drawing'),
 ('MP21','logo-spin-3d','3D logo spin','corporate','IDENTITI ANDA','Logo hadir di pentas studio.','faux-depth rotating brand plate and light sweep'),
 ('MP22','kopitiam','Kopitiam','documentary','PAGI DI KOPITIAM','Teh tarik dan menu kapur.','tea stream, rising steam, chalk-written menu'),
 ('MP23','comic-pop-art','Comic pop art','promo','POW! IDEA','Panel komik penuh tenaga.','slam comic panels, halftone and speech bubble'),
 ('MP24','photo-slideshow','Photo slideshow','documentary','CERITA GAMBAR','Foto bergerak dengan susunan editorial.','full-image contain, Ken Burns, focus handoff'),
 ('MP25','batik-fashion','Batik fashion','promo','CORAK PILIHAN','Butiran kain menjadi cerita.','fashion card orbit with expanding batik motifs'),
 ('MP26','merdeka','Merdeka','documentary','MALAYSIA KITA','Semangat merdeka dan cahaya kota.','layered skyline, flag-inspired ribbon, fireworks'),
 ('MP27','product-turntable','Product turntable','promo','PRODUK UTAMA','Setiap ciri diberi ruang.','pedestal turntable, sweeping light, anchored callouts'),
 ('MP28','glitch','Glitch','creator','ISYARAT BAHARU','Gangguan singkat, mesej tetap jelas.','brief RGB slices and stable terminal type'),
 ('MP29','kampung-sunset','Kampung sunset','documentary','SENJA DI KAMPUNG','Cahaya beralih hingga kelip-kelip hadir.','sun descent, parallax trees, firefly onset'),
 ('MP30','chat-story','Chat story','saas','CERITA CHAT','Mesej timbul mengikut masa.','typing dots, rising bubbles, waveform'),
 ('MP31','sale-countdown','Sale countdown','promo','TAWARAN KINI','Harga dan tindakan jelas.','3-2-1 impact, swinging tag and staged CTA'),
 ('MP32','watercolour-ink','Watercolour ink','documentary','LUKIS CERITA','Dakwat dan warna meresap pada kertas.','watercolour diffusion and traced branch'),
 ('MP33','pasar-malam','Pasar malam','promo','MALAM MERIAH','Gerai, asap dan kad hidangan.','lantern sequence, market parallax, steam and prices'),
 ('MP34','whiteboard-sketch','Whiteboard sketch','education','FAHAMKAN PROSES','Rajah dilukis langkah demi langkah.','stroked doodles, connecting arrow, marker annotations'),
 ('MP35','y2k-chrome','Y2K chrome','creator','ENERGI Y2K','Pantulan metal dan pelekat holografik.','morphing chrome blob, orbiting stickers, shine'),
 ('MP36','chinese-new-year','Chinese heritage','promo','SELAMAT TAHUN BAHARU','Potongan kertas, tanglung dan cop.','symmetric paper-cuts, lantern sway, seal stamp'),
 ('MP37','property-tour','Property tour','corporate','RUANG ANDA','Pelan bilik dibina secara berurutan.','extruded 2.5D floorplan with room focus'),
 ('MP38','particle-field','Particle field','saas','KUMPUL TENAGA','Titik bergerak membentuk mesej.','vector-field particles converge into title'),
 ('MP39','nostalgia-90s','Nostalgia 90s','documentary','IMBAS KENANGAN','Televisyen CRT memaparkan cerita.','CRT switch-on, scanline and VHS title'),
 ('MP40','podcast-audiogram','Podcast audiogram','creator','SUARA UTAMA','Kata penting muncul mengikut beat.','animated bars and highlighted quote'),
 ('MP41','borneo-rainforest','Borneo rainforest','documentary','HUTAN BORNEO','Kabus membuka ruang pada cerita.','forest parallax, drifting mist, hornbill silhouette'),
 ('MP42','paper-cutout','Paper cut-out','education','CERITA KERTAS','Kepingan berlapis disusun tangan.','wobbling paper pieces, taped label and shadows'),
 ('MP43','pixel-art','Pixel art','promo','LEVEL UP!','Ciri produk dijumpai seperti item game.','pixel avatar jumps, item blocks and inventory'),
 ('MP44','deepavali','Deepavali','documentary','SELAMAT DEEPAVALI','Kolam dilukis, pelita menyala.','kolam rings, sequential diyas, floral garland'),
 ('MP45','vintage-archive','Vintage archive','documentary','ARKIB CERITA','Foto dan tahun mengikut urutan.','stacked photos, ink timeline and date stamps'),
 ('MP46','swiss-geometric','Swiss geometric','corporate','REKA DENGAN JELAS','Grid, bentuk dan senarai perkhidmatan.','strict grid slides, quarter turns, row emphasis'),
 ('MP47','floating-3d-icons','Floating 3D icons','saas','CIRI TERHUBUNG','Ikon keluar dari skrin.','faux-depth monitor and orbiting feature icons'),
 ('MP48','neon-tech','Neon tech','saas','TEKNOLOGI HIDUP','Litar bercahaya menghubungkan fungsi.','HUD spin, laptop open, hologram data panels'),
]
assert len(ROWS)==48
PRESETS={pid:dict(name=name,description=f'Animasi asli: {mechanism}.',family='motionprompt',genre=genre,genres=[genre],text=heading,subtitle=sub,source_url=f'https://epool86.github.io/motionprompt/#{slug}',variant_basis='adapted',mechanism=mechanism,duration=6) for pid,slug,name,genre,heading,sub,mechanism in ROWS}
for _pid in ('MP06','MP21','MP27','MP35','MP37','MP47'):
    PRESETS[_pid]['render_mode']='2.5D illustrated depth; no 3D model included'

# Common deterministic drawing helpers. Scene functions remain distinct.
def _canvas(cfg,p,default):
    return layer() if cfg.get('_transparent') else Image.new('RGBA',(W,H),cfg.get('bg',default))
def _fade(t,a=.15,b=.85,c=4.3,d=4.95):return life(t,a,b,c,d)
def _title(im,cfg,p,x=640,y=126,size=67,maxw=1100,align='center',a=.4):
    s=cfg.get('text',''); text(im,s,x,y,max(26,fit_size(s,maxw,size)),p['text'],'bold',opacity=_fade(cfg['_clock'],a,a+.5),anchor=align)
def _sub(im,cfg,p,y=608):
    s=cfg.get('subtitle','');text(im,s,640,y,max(20,fit_size(s,1040,27,'sans')),p['text'],'sans',opacity=_fade(cfg['_clock'],1,1.4,4.1,4.85))
def _items(cfg,defaults):
    v=cfg.get('items',defaults)
    if not isinstance(v,(list,tuple)) or not v:return defaults
    return [str(x)[:45] for x in v[:8]]
def _card(im,x,y,w,h,p,label='',fill=None,accent=None,scale=1,opacity=1,angle=0):
    spr=panel(w,h,fill or p['panel'],22,accent or p['muted'])
    if label:text(spr,label,spr.width/2,spr.height/2,max(19,fit_size(label,w-38,29)),p['text'],'bold')
    paste(im,spr,x,y,opacity,scale,angle)
def _poly(im,pts,color):ImageDraw.Draw(im).polygon([(round(x),round(y)) for x,y in pts],fill=color)
def _rect(im,box,color):ImageDraw.Draw(im).rectangle(tuple(round(v) for v in box),fill=color)
def _ring(im,x,y,r,color,width=4,start=0,end=360):
    ImageDraw.Draw(im).arc((x-r,y-r,x+r,y+r),start,end,fill=color,width=width)
def _star(im,x,y,r,color):
    pts=[]
    for k in range(10):
        a=-math.pi/2+k*math.pi/5;rrr=r if k%2==0 else r*.43;pts.append((x+rrr*math.cos(a),y+rrr*math.sin(a)))
    _poly(im,pts,color)
@lru_cache(maxsize=32)
def _asset(path,w,h):
    try:
        with Image.open(path) as original:
            src=ImageOps.exif_transpose(original).convert('RGBA')
            src.thumbnail((max(1,w),max(1,h)),Image.Resampling.LANCZOS)
            canvas=layer(w,h); canvas.alpha_composite(src,((w-src.width)//2,(h-src.height)//2));return canvas
    except (OSError,ValueError):return None
def _source(cfg,i,w,h):
    paths=cfg.get('image_paths',[])
    if isinstance(paths,str):paths=[paths]
    if not isinstance(paths,list):paths=[]
    path=(paths[i%len(paths)] if paths else cfg.get('image_path') or cfg.get('asset'))
    return _asset(str(path),w,h) if path else None
def _screen(im,cfg,i,x,y,w,h,p,progress=1):
    rr(im,(x-10,y-10,x+w+10,y+h+10),p['panel'],20,p['accent'],2)
    src=_source(cfg,i,w,h)
    if src:paste(im,src,x+w/2,y+h/2,progress)
    else:
        rr(im,(x,y,x+w,y+h),rgba(p['secondary'],35),13)
        for j in range(4):rr(im,(x+24,y+25+j*44,x+w-26,y+38+j*44),rgba(p['muted'],80),6)
        circle(im,x+w*.79,y+h*.72,24,p['accent'])
def _dots(im,n,cx,cy,rad,color,t,seed=11):
    rng=random.Random(seed)
    for j in range(n):
        a=rng.random()*math.tau;rrr=rad*math.sqrt(rng.random());px=cx+rrr*math.cos(a)+14*math.sin(t*2+j);py=cy+rrr*math.sin(a)+8*math.cos(t*2+j)
        circle(im,px,py,1.5+j%3,rgba(color,60+j%3*40))

def render(pid,t,cfg):
    p=palette(cfg);cfg=dict(cfg);cfg['_clock']=t
    im=SCENES[pid](t,cfg,p)
    if im.size!=(W,H):raise ValueError(pid+' produced wrong canvas size')
    return im

# MP01–MP12: cinematic, explainer, characters and product scenes.
def mp01(t,c,p):
    im=_canvas(c,p,'#0D1C22');_dots(im,34,600,275,650,p['secondary'],t,7)
    moon=120;circle(im,1025,170,moon,rgba(p['text'],145))
    for depth in (0,1):
        for i in range(13):
            h=100+(i*71+depth*49)%230;x=i*105-depth*52
            shake=7*math.sin(t*31+i) if 1<t<2.1 else 0
            _rect(im,(x+shake,570-h+depth*65,x+96+shake,720),'#172A33' if depth else '#213944')
            for xx in range(x+15,x+85,23):
                for yy in range(600-h+depth*65,665,31):rr(im,(xx+shake,yy,xx+7+shake,yy+11),rgba(p['accent'],105),1)
    rise=ease(prog(t,.8,2));mx=665;my=575-280*rise
    circle(im,mx,my,118,'#172C30');_poly(im,[(mx-90,my-64),(mx-61,my-195),(mx-10,my-100),(mx+65,my-185),(mx+78,my-52)],'#172C30')
    for k in range(4):_poly(im,[(mx-105+k*55,my-57),(mx-79+k*55,my-131),(mx-54+k*55,my-66)],p['secondary'])
    circle(im,mx-35,my-10,12,p['accent']);circle(im,mx+36,my-10,12,p['accent'])
    if t>2:
        beam=ease(prog(t,2.15,3.1));line(im,[(mx,my+20),(900+160*beam,180)],rgba(p['accent'],180),round(13*beam)+1)
    if t>2.6:
        tx=text_img(c['text'],max(38,fit_size(c['text'],1050,93)),p['accent']);paste(im,crop_reveal(tx,prog(t,2.6,3.8),'left'),640,155)
    rr(im,(65,40,270,82),p['panel'],7);text(im,'BULLETIN',168,61,24,p['text'],'mono');_sub(im,c,p,650);return im

def mp02(t,c,p):
    im=_canvas(c,p,'#EEF2F7');items=_items(c,['Pilih idea','Susun bahan','Bina visual','Semak hasil'])
    view=ease(prog(t,.1,3.5));shift=-210*view
    rr(im,(85+shift,90,1780+shift,635),'#FFFFFF',24,rgba(p['muted'],70),2)
    text(im,c['text'],175+shift,161,fit_size(c['text'],820,67),p['text'],'bold',anchor='left')
    for j,s in enumerate(items[:4]):
        x=182+j*345+shift;y=335+18*math.sin(t*1.1+j)
        q=_fade(t,.4+j*.48,.9+j*.48)
        circle(im,x,y,61,rgba(p['accent'],55*q));circle(im,x,y,32,p['accent'])
        text(im,str(j+1),x,y,29,'#FFFFFF',opacity=q)
        text(im,s,x,y+105,max(20,fit_size(s,290,30)),p['text'],opacity=q)
        if j<3:
            for k in range(8):
                if t>.65+j*.48+k*.035:circle(im,x+95+k*17,y,2,p['muted'])
    if t>3.3:
        _card(im,1020,536,350,116,p,'SEBELUM  →  SELEPAS',opacity=ease(prog(t,3.4,4)))
    return im

def mp03(t,c,p):
    im=_canvas(c,p,'#0B1020');items=_items(c,['IDEA','REKA','BINA','UJI','SIAP','KONGSI']);n=max(4,min(8,len(items)));cx,cy=625,365
    active=min(n-1,int(max(0,t-1.15)*n/3.2))
    for j in range(n):
        a0=-math.pi/2+(j/n)*math.tau;a1=a0+math.tau/n-.06;q=ease(prog(t,.3+j*.18,.85+j*.18));rad=208+(23 if active==j and t>1.3 else 0)
        pts=[(cx,cy),(cx+rad*math.cos(a0),cy+rad*math.sin(a0)),(cx+rad*math.cos(mix(a0,a1,q)),cy+rad*math.sin(mix(a0,a1,q)))]
        for k in range(1,11):
            aa=mix(a0,mix(a0,a1,q),k/10);pts.append((cx+rad*math.cos(aa),cy+rad*math.sin(aa)))
        hue=[p['accent'],p['secondary'],'#F29E4C','#DE6E84','#61B784','#9189DF','#DDBB5A','#5EB7C6'][j]
        _poly(im,pts,rgba(hue,225 if active==j else 155));ang=(a0+a1)/2
        if q>.5:text(im,str(j+1),cx+130*math.cos(ang),cy+130*math.sin(ang),28,'#FFFFFF')
    circle(im,cx,cy,87,p['panel'],p['accent'],4);text(im,c['text'],cx,cy,max(24,fit_size(c['text'],150,37)),p['text'])
    for j,s in enumerate(items[:n]):
        if t<1.25+j*3.1/n:continue
        y=167+(j%4)*98;x=95 if j<4 else 1060
        text(im,s,x,y,max(19,fit_size(s,170,25)),p['text'],anchor='left')
        line(im,[(x+15,y+25),(cx+225*math.cos(j*math.tau/n),cy+225*math.sin(j*math.tau/n))],rgba(p['secondary'],90),2)
    return im

def mp04(t,c,p):
    im=_canvas(c,p,'#E6E7EA');_title(im,c,p,y=83,size=55)
    for j in range(8):
        x=165+(j%4)*315;y=257+(j//4)*235
        q=ease(prog(t,.2+j*.19,.72+j*.19));focus=min(7,int(max(0,t-1.7)*8/2.7));active=j==focus and t>1.7
        spr=layer(270,165);rr(spr,(2,2,266,161),'#FFFFFF',10,rgba(p['muted'],70),2)
        rr(spr,(15,17,80,31),p['accent'],3);text(spr,f'{j+1:02d}  {c["text"][:18]}',18,59,17,p['text'],anchor='left')
        for k in range(3):rr(spr,(18,81+k*20,194,87+k*20),rgba(p['muted'],90),2)
        src=_source(c,j,94,88)
        if src:paste(spr,src,215,104)
        else:circle(spr,215,113,27,p['secondary'])
        paste(im,spr,x,y+60*(1-q),q,1.22 if active else .94,-5+j%4*3)
        if active:_ring(im,x,y,143,p['accent'],4,210,330)
    _sub(im,c,p,665);return im

def mp05(t,c,p):
    im=_canvas(c,p,'#1565D8');p=dict(p,text='#FFFFFF',accent='#FF6098',panel='#A6C9F2')
    _title(im,c,p,y=95,size=70);_sub(im,c,p,644)
    q=ease(prog(t,.4,1.2));rr(im,(570,245,1020,548),p['panel'],18)
    # Character and arm are separate planes; the marker points to a progressing chart.
    circle(im,330,305,54,'#F8C39D');rr(im,(249,357,415,575),'#0D2152',55)
    eye=4+2*math.sin(t*5);circle(im,313,302,eye,'#17243E');circle(im,353,302,eye,'#17243E')
    handx=525+22*math.sin(t*3);line(im,[(398,395),(handx,326)],'#F8C39D',24);circle(im,handx,326,12,'#F8C39D')
    for j in range(4):
        h=45+(j*33)%110;x=615+j*88
        rr(im,(x,487-h*q,x+52,487),rgba(p['accent'],230),6)
    pts=[(622+i*36,424-50*math.sin(i/9*math.pi)-i*9) for i in range(10)]
    n=max(2,round(len(pts)*q));line(im,pts[:n],'#FFFFFF',5)
    for j in range(3):
        x=923+j*62;y=210-12*j;_star(im,x,y,14+2*math.sin(t*4+j),'#FFFFFF')
    return im

def mp06(t,c,p):
    p=dict(p,text=c.get('text_color','#263238'));im=_canvas(c,p,'#F9FAFB');_title(im,c,p,y=91,size=58);_sub(im,c,p,644)
    wobble=15*math.sin(t*.9);ImageDraw.Draw(im).ellipse((245,400,1050,599),fill='#D7E4E5',outline=p['accent'],width=4)
    ImageDraw.Draw(im).ellipse((260,385,1035,554),fill='#ECF2F0')
    parts=[('SCREEN',423,354,145,142),('IDEA',650,330,96,90),('DATA',815,410,112,94),('+1',551,453,84,74)]
    for j,(s,x,y,w,h) in enumerate(parts):
        q=ease(prog(t,.35+j*.38,.9+j*.38));yy=y+130*(1-q)+wobble*(j%2*2-1)
        _poly(im,[(x-w/2,yy-h/2+15),(x,yy-h/2-17),(x+w/2,yy-h/2+15),(x,yy-h/2+45)],rgba(p['secondary'],220))
        rr(im,(x-w/2,yy-h/2+25,x+w/2,yy+h/2),p['accent'] if j==1 else p['panel'],16)
        text(im,s,x,yy+13,max(19,fit_size(s,w-8,24)),p['text'])
        if j==0:_screen(im,c,0,x-50,yy-38,100,70,p)
    return im

def mp07(t,c,p):
    im=_canvas(c,p,'#10131F');words=(c['text'].split() or ['GERAK'])[:5]
    if t>2.1:rr(im,(0,0,W,H),rgba(p['secondary'],25*math.sin(t*2)**2),0)
    unit=865/max(1,len(words));start=640-(len(words)-1)*unit/2
    for j,s in enumerate(words):
        q=_fade(t,.18+j*.47,.59+j*.47,4.1,4.8);x=start+j*unit
        text(im,s,x,320+90*(1-q),max(32,fit_size(s,unit-12,94)),p['text'] if j%2 else p['accent'],opacity=q,scale=1.35-.35*q,angle=(1-q)*(14 if j%2 else -12))
        if q>.9 and j%2==0:line(im,[(x-unit*.25,397),(x+unit*.25,397)],p['secondary'],5)
    text(im,c['subtitle'],640,534,fit_size(c['subtitle'],1000,28),p['text'],'sans',opacity=_fade(t,2.4,2.9))
    return im

def mp08(t,c,p):
    p=dict(p,text=c.get('text_color','#FFF6DF'));im=_canvas(c,p,'#F5D69C');_rect(im,(0,537,W,H),'#619B5F')
    for j in range(5):
        x=130+j*270;line(im,[(x,546),(x+30,390)],'#654F39',12);circle(im,x+30,390,58,'#368464')
    for j in range(2):
        x=270+j*690+48*math.sin(t*.8+j);y=231+j*55-70*ease(prog(t,.25+j*.5,1.5+j*.5))
        _poly(im,[(x-105,y),(x,y-70),(x+105,y),(x,y+63)],p['secondary'])
        _poly(im,[(x-72,y),(x,y-45),(x+70,y),(x,y+42)],p['accent']);line(im,[(x,y+60),(x-24,y+350)],rgba(p['text'],190),2)
        for k in range(4):circle(im,x+28*math.cos(k*1.6),y+25*math.sin(k*1.6),6,'#FDE8A9')
    q=ease(prog(t,1.4,2.5));rr(im,(240,385,1040,385+155*q),'#68132B',14,p['accent'],4)
    if q>.3:text(im,c['text'],640,450,fit_size(c['text'],740,72),p['accent'],opacity=q)
    for j in range(10):_star(im,340+j*67,540+12*math.sin(j),5,p['accent'])
    _sub(im,c,p,660);return im

def mp09(t,c,p):
    im=_canvas(c,p,'#111B32');_title(im,c,p,x=898,y=173,maxw=630,size=65);_sub(im,c,p,629)
    phone=layer(380,550);rr(phone,(26,8,357,545),'#182843',49,p['secondary'],5)
    _screen(phone,c,0,52,72,277,395,p)
    rr(phone,(128,24,252,44),'#0B1120',13)
    paste(im,phone,389+18*math.sin(t*.8),365,1,1,-4*math.sin(t*.7))
    labels=_items(c,['Cari','Pilih','Simpan'])
    for j,s in enumerate(labels[:3]):
        q=_fade(t,.65+j*.52,1.2+j*.52);x=770+(j%2)*206;y=300+j*84
        _card(im,x+80*(1-q),y,160,66,p,s,opacity=q,scale=.7+.3*q)
        line(im,[(554,y),(x-86,y)],rgba(p['accent'],180*q),2)
    return im

def mp10(t,c,p):
    p=dict(p,text=c.get('text_color','#32223B'));im=_canvas(c,p,'#FBE6EF');_title(im,c,p,y=103,size=65);_sub(im,c,p,632)
    q=ease(prog(t,.2,.85));x=450;y=395+23*math.sin(t*2)
    rr(im,(x-95,y-17,x+95,y+191),'#C697DD',90);circle(im,x,y-108,92,'#F8CDB5')
    for xx in (x-35,x+35):circle(im,xx,y-115,6,'#372447')
    _ring(im,x,y-82,26,'#A54675',3,10,170)
    line(im,[(x+88,y+30),(x+150,y-25+18*math.sin(t*5))],'#F8CDB5',25);circle(im,x+155,y-25+18*math.sin(t*5),17,'#F8CDB5')
    for j in range(10):
        xx=140+j*104;yy=235+(j%3)*114+20*math.sin(t*2+j)
        if j%2:_star(im,xx,yy,12,p['accent'])
        else:circle(im,xx,yy,13,'#E9A2D4')
    rr(im,(721,289,1104,496),'#FFFFFF',45,rgba(p['accent'],140),4)
    text(im,c['text'],913,370,fit_size(c['text'],350,42),p['text'],opacity=q)
    return im

def mp11(t,c,p):
    im=_canvas(c,p,'#071321');_dots(im,75,643,335,500,p['secondary'],t)
    cx,cy=650,390
    for j in range(10):_ring(im,cx,cy,120+j*15,rgba(p['secondary'],30+j%2*20),1,0,360)
    for j in range(45):
        a=(j/45*math.tau+t*.15);yy=cy+160*math.sin(a);xx=cx+300*math.cos(a)
        circle(im,xx,yy,2+(j%3),rgba(p['accent'],150))
    for j in range(5):
        a=-.7+j*.4;xx=650+345*math.cos(a);yy=390+180*math.sin(a)
        q=ease(prog(t,.6+j*.29,1.2+j*.29))
        line(im,[(cx,cy),(cx+(xx-cx)*q,cy+(yy-cy)*q)],rgba(p['accent'],150),3)
        circle(im,xx,yy,15,p['secondary'])
    _title(im,c,p,y=105,size=70);_sub(im,c,p,640);return im

def mp12(t,c,p):
    p=dict(p,text=c.get('text_color','#302B30'));im=_canvas(c,p,'#C9B69F');
    for j in range(8):line(im,[(0,j*92),(W,j*92)],rgba('#705843',55),3)
    ImageDraw.Draw(im).ellipse((275,162,800,680),fill='#EEE8DD',outline='#FFFFFF',width=17)
    ImageDraw.Draw(im).ellipse((341,223,743,622),fill='#354F3A')
    for j in range(10):
        q=ease(prog(t,.3+j*.20,.75+j*.20));a=j*2.4+t*.2
        x=540+135*math.cos(a);y=422+127*math.sin(a)
        circle(im,x,y-140*(1-q),25 if j%2 else 33,p['accent'] if j%2 else p['secondary'])
        _ring(im,x,y,14,'#F8D4A0',4)
    q=ease(prog(t,2.25,2.9));rr(im,(804+150*(1-q),159,1187+150*(1-q),548),'#F8F4EB',26)
    text(im,c['text'],995+150*(1-q),252,fit_size(c['text'],345,52),p['text'],opacity=q)
    text(im,c['subtitle'],995+150*(1-q),336,fit_size(c['subtitle'],336,26),p['text'],'sans',opacity=q)
    line(im,[(844,417),(1145,417)],p['accent'],4);text(im,str(c.get('price','MENU')),995,467,38,p['accent'],opacity=q)
    return im

# MP13–MP24: atmospheres, celebrations, data and editorial media.
def mp13(t,c,p):
    im=_canvas(c,p,'#1A1228')
    for x in range(0,W,153):
        for y in range(0,H,75):rr(im,(x+2,y+2,x+150,y+72),'#291C2A',3,rgba('#564253',80),1)
    s=c['text'];sz=fit_size(s,1040,106);q=ease(prog(t,.2,2.45));gl=layer()
    text(gl,s,640,355,sz,p['accent'],stroke=4,stroke_color=p['secondary'],opacity=q)
    im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(18)))
    # Short electrical start-up, stable glow after the word has formed.
    flicker=.3+ .7*q if t<2.6 else 1-.035*math.sin(t*9)
    text(im,s,640,355,sz,'#FFF8EA',opacity=flicker,stroke=4,stroke_color=p['accent'])
    _sub(im,c,p,575);return im

def mp14(t,c,p):
    im=_canvas(c,p,'#E8EFE7');_title(im,c,p,y=88,size=60)
    # Abstract map: no invented geography or geographic claim.
    rng=random.Random(14)
    for j in range(20):
        x=rng.randrange(60,1200);y=rng.randrange(155,660);r=rng.randrange(15,74)
        rr(im,(x-r,y-r,x+r,y+r),rgba('#85BDA0',75),20)
    pts=[(160,540),(353,434),(531,485),(705,308),(891,357),(1107,207)]; q=ease(prog(t,.5,3.6))
    n=(len(pts)-1)*q;i=int(n);path=pts[:i+1]
    if i<len(pts)-1:path.append((mix(pts[i][0],pts[i+1][0],n-i),mix(pts[i][1],pts[i+1][1],n-i)))
    if len(path)>1:line(im,path,p['accent'],7)
    stops=_items(c,['MULA','DESTINASI 1','DESTINASI 2','AKHIR'])
    for j,idx in enumerate([0,2,4,5]):
        x,y=pts[idx];qq=ease(prog(t,.4+idx*.53,.8+idx*.53))
        circle(im,x,y,14*qq,p['secondary']);circle(im,x,y,5*qq,'#FFFFFF')
        if qq>.5:_card(im,x,y-52,190,57,p,stops[j%len(stops)],opacity=qq,scale=.7+.3*qq)
    _sub(im,c,p,672);return im

def mp15(t,c,p):
    im=_canvas(c,p,'#24192D');gl=layer()
    colors=[p['accent'],p['secondary'],'#5684CE','#F2AA86']
    for j,color in enumerate(colors):
        x=250+j*257+90*math.sin(t*.8+j*1.8);y=330+85*math.cos(t*.64+j*1.5);r=165+35*math.sin(t*.9+j)
        circle(gl,x,y,r,rgba(color,180))
    im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(100)))
    _dots(im,42,640,360,610,p['text'],t,8)
    q=_fade(t,.55,1.65);tex=text_img(c['text'],fit_size(c['text'],1060,91),p['text'])
    paste(im,crop_reveal(tex,q,'up'),640,334);_sub(im,c,p,482);return im

def mp16(t,c,p):
    p=dict(p,text=c.get('text_color','#FFF4E2'));im=_canvas(c,p,'#1D2440');_dots(im,24,640,200,600,p['secondary'],t,15)
    for j in range(7):
        x=170+j*157;y=192+20*math.sin(t*.8+j);q=ease(prog(t,.2+j*.17,.95+j*.17))
        if j%2:
            _poly(im,[(x,y-45*q),(x+40*q,y),(x,y+45*q),(x-40*q,y)],p['accent'])
            line(im,[(x-36*q,y),(x+36*q,y)],rgba(p['text'],145),2)
            line(im,[(x,y-40*q),(x,y+40*q)],rgba(p['text'],145),2)
        else:_star(im,x,y,16*q,p['secondary'])
    for j in range(6):
        x=200+j*173;yy=531;rr(im,(x-19,yy,x+19,yy+68),'#C09C5D',7)
        if t>.5+j*.24:circle(im,x,yy-8+4*math.sin(t*6+j),10,p['accent'])
    rr(im,(163,322,1117,491),'#3B3047',21,p['accent'],3)
    _title(im,c,p,y=388,size=75);_sub(im,c,p,630);return im

def mp17(t,c,p):
    im=_canvas(c,p,'#142039');_title(im,c,p,y=86,size=64)
    q=ease(prog(t,.55,3.2));vals=c.get('values',[.45,.67,.88,.72])
    if not isinstance(vals,(list,tuple)) or len(vals)<4: vals=[.45,.67,.88,.72]
    vals=[clamp(float(v)) for v in vals[:4]]
    for j,val in enumerate(vals):
        x=215+j*208;height=245*val*q
        rr(im,(x,535-height,x+95,535),p['accent'] if j==3 else p['secondary'],10)
        text(im,f'{round(val*100*q)}',x+48,535-height-38,32,p['text'],'bold')
        text(im,f'{j+1:02}',x+48,575,20,p['muted'],'mono')
    pts=[(260+j*208,397-(vals[j]-.5)*90*q) for j in range(4)]
    line(im,pts[:max(2,round(1+q*3))],p['accent'],5)
    # Donut shares the same first value, preventing chart/counter disagreement.
    _ring(im,1061,420,93,p['panel'],25);_ring(im,1061,420,93,p['accent'],25,-90,-90+round(360*vals[0]*q))
    text(im,f'{round(vals[0]*100*q)}%',1061,420,38,p['text'])
    if 'values' not in c:text(im,'DATA DEMO',1061,553,17,p['secondary'],'mono')
    _sub(im,c,p,662);return im

def mp18(t,c,p):
    p=dict(p,text=c.get('text_color','#2B2834'));im=_canvas(c,p,'#EFE2CC');_title(im,c,p,y=96,size=61)
    # Twelve distinct poses per second reproduce an intentional stop-motion cadence.
    step=int(t*12);x=650+125*math.sin(step*.14);y=386+38*math.cos(step*.23)
    squish=1+.12*math.sin(step*.47);bl=layer(280,280)
    circle(bl,140,140,104,p['accent']);circle(bl,106,120,11,p['text']);circle(bl,171,120,11,p['text'])
    _ring(bl,140,164,33,p['text'],4,20,160)
    for j in range(8):circle(bl,55+j*25,224+6*math.sin(step*.29+j),5,rgba(p['secondary'],200))
    paste(im,bl,x,y,1,squish,(step%4-2)*2)
    _card(im,291,479,250,122,p,'BENTUK',opacity=ease(prog(t,.8,1.5)),angle=-7)
    _card(im,1030,415,250,122,p,'GERAK',opacity=ease(prog(t,1.8,2.55)),angle=8)
    _sub(im,c,p,644);return im

def mp19(t,c,p):
    im=_canvas(c,p,'#161328');_rect(im,(0,404,W,H),'#1D1642')
    ImageDraw.Draw(im).ellipse((360,90,930,540),fill='#FA845E')
    for j in range(7):_rect(im,(372,264+j*33,918,269+j*33),'#261639')
    for i in range(14):
        q=i/14;xx=640+(i-7)*110*(1+q);line(im,[(640,403),(xx,H)],rgba(p['secondary'],80),2)
    for j in range(7):
        y=408+((j/7+t*.15)%1)**1.8*350;line(im,[(0,y),(W,y)],rgba(p['accent'],130),2)
    q=ease(prog(t,.7,1.55));text(im,c['text'],640,292,fit_size(c['text'],1140,91),p['text'],opacity=q,stroke=2,stroke_color=p['accent'])
    _sub(im,c,p,631);return im

def mp20(t,c,p):
    im=_canvas(c,p,'#F6EEE9');cx=640
    q=ease(prog(t,.4,2.35));_ring(im,cx,403,245,p['accent'],8,180,180+round(360*q))
    for j in range(12):
        ang=j/12*math.tau-t*.08;x=cx+245*math.cos(ang);y=403+245*math.sin(ang)
        if j%3==0:
            for k in range(5):circle(im,x+16*math.cos(k*math.tau/5),y+16*math.sin(k*math.tau/5),12*q,p['secondary'])
            circle(im,x,y,9*q,p['accent'])
        else:_poly(im,[(x,y-20*q),(x+16*q,y),(x,y+20*q),(x-16*q,y)],rgba(p['secondary'],190))
    text(im,c['text'],cx,367,fit_size(c['text'],650,70),p['text'],'serif',opacity=ease(prog(t,1.5,2.7)))
    _sub(im,c,p,465);return im

def mp21(t,c,p):
    im=_canvas(c,p,'#111824');_ring(im,640,590,225,rgba(p['secondary'],85),4,0,360)
    angle=t*2.1;wid=430*max(.08,abs(math.cos(angle)))
    rr(im,(640-wid/2+15,201,640+wid/2+15,516),rgba(p['secondary'],125),32)
    rr(im,(640-wid/2,187,640+wid/2,502),p['accent'],30,p['text'],3)
    if wid>130:
        src=_source(c,0,int(wid*.76),220)
        if src:paste(im,src,640,346)
        else:text(im,c['text'],640,344,fit_size(c['text'],max(100,wid-30),59),p['text'],opacity=_fade(t,.1,.8))
    x=360+(t%3)/3*570;line(im,[(x,200),(x+34,502)],rgba('#FFFFFF',90),12)
    _sub(im,c,p,627);return im

def mp22(t,c,p):
    im=_canvas(c,p,'#C9AA77');_rect(im,(0,480,W,H),'#765342')
    for j in range(5):line(im,[(j*250,0),(j*250,480)],rgba('#65432B',90),5)
    rr(im,(164,175,514,443),'#223129',18,rgba('#E8D0A1',80),5)
    for j,s in enumerate(_items(c,['KOPI','ROTI','TEH'])[:3]):
        q=ease(prog(t,.5+j*.52,1+j*.52));text(im,s[:round(len(s)*q)],196,231+j*70,34,'#F4E5C4','mono',anchor='left')
    ImageDraw.Draw(im).ellipse((629,480,1100,589),fill='#F3E8D4')
    rr(im,(740,378,978,539),'#F8EAD1',35,p['text'],3)
    q=ease(prog(t,.3,2));line(im,[(843,130),(857,378-165*(1-q))],p['accent'],max(3,int(15*q)))
    for j in range(6):
        x=810+j*19;y=350-18*j-17*t;_ring(im,x,y,15,rgba(p['text'],100),2,210,325)
    _title(im,c,p,x=854,y=100,size=56,maxw=680);_sub(im,c,p,657);return im

def mp23(t,c,p):
    p=dict(p,text=c.get('text_color','#2B2033'));im=_canvas(c,p,'#FCE0BC');
    for j in range(130):
        x=(j*109)%W;y=(j*67)%H;circle(im,x,y,2,rgba(p['text'],60))
    boxes=[(67,130,557,550),(572,130,1195,342),(572,360,1195,550)]
    for j,box in enumerate(boxes):
        q=ease(prog(t,.1+j*.49,.65+j*.49));x0,y0,x1,y1=box
        rr(im,(x0,y0+100*(1-q),x1,y1+100*(1-q)),p['accent'] if j==0 else p['secondary'],8,p['text'],6)
        if q>.55:
            _star(im,(x0+x1)/2,(y0+y1)/2,80 if j==0 else 55,p['text'])
            text(im,['POW!',c['text'],'WOW!'][j],(x0+x1)/2,(y0+y1)/2,fit_size(['POW!',c['text'],'WOW!'][j],x1-x0-60,65),p['text'] if j!=0 else '#FFFFFF')
    rr(im,(312,540,930,645),'#FFFFFF',50,p['text'],4)
    text(im,c['subtitle'],620,592,fit_size(c['subtitle'],550,32),p['text']);return im

def mp24(t,c,p):
    im=_canvas(c,p,'#E8E1D4');_title(im,c,p,y=86,size=56)
    for j in range(3):
        q=_fade(t,.25+j*.75,.8+j*.75,4.6,5)
        x=335+j*310+28*math.sin(t*.5+j);y=367+(j%2)*24
        spr=layer(295,375);rr(spr,(2,2,293,373),'#FFFFFF',8)
        src=_source(c,j,265,302)
        if src:paste(spr,src,147,168)
        else:
            rr(spr,(17,19,278,321),rgba(p['secondary'],175),4)
            circle(spr,144,156,64,p['accent']);line(spr,[(23,278),(143,190),(260,280)],p['text'],5)
        text(spr,str(j+1).zfill(2),147,347,21,p['muted'],'mono')
        paste(im,spr,x,y+90*(1-q),q,.94+.05*math.sin(t*.25+j),(-8,0,7)[j])
    _sub(im,c,p,662);return im

# MP25–MP36: culture, offers, interfaces and illustrative processes.
def mp25(t,c,p):
    p=dict(p,text=c.get('text_color','#2C2431'));im=_canvas(c,p,'#F5E4D4');_title(im,c,p,y=92,size=58)
    for j in range(4):
        x=175+j*305;y=408+15*math.sin(t*.8+j)
        q=ease(prog(t,.25+j*.35,.9+j*.35))
        rr(im,(x-101,y-206+70*(1-q),x+101,y+205+70*(1-q)),'#FFFFFF',12)
        _poly(im,[(x-28,y-120),(x+28,y-120),(x+90,y+138),(x-90,y+138)],p['accent'] if j%2 else p['secondary'])
        circle(im,x,y-145,32,'#C38F70')
        for k in range(3):
            a=t*.25+j+k*math.tau/3;xx=x+50*math.cos(a);yy=y+20+k*36
            _ring(im,xx,yy,15,p['text'],2,20,290)
        src=_source(c,j,180,325)
        if src:paste(im,src,x,y+35,opacity=q)
        text(im,f'LOOK {j+1:02d}',x,y+178,20,p['text'],'mono',opacity=q)
    _sub(im,c,p,663);return im

def mp26(t,c,p):
    p=dict(p,text=c.get('text_color','#FFFFFF'));im=_canvas(c,p,'#101D40')
    for j in range(15):
        x=j*91;h=90+(j*79)%230;_rect(im,(x,H-h,x+78,H),'#182852')
        for k in range(3):rr(im,(x+15+k*20,H-h+23,x+20+k*20,H-h+34),rgba(p['accent'],130),1)
    for j in range(11):
        a=j*.7+t*.25;x=150+j*94;y=320+32*math.sin(a)
        line(im,[(x-25,y-21),(x+70,y-21),(x+52,y+23),(x-44,y+23)],'#E64451' if j%2 else '#F9F4E9',8)
    for j in range(7):
        x=180+(j*197)%910;y=160+(j*39)%145
        r=5+65*ease(prog(t,.7+j*.31,1.5+j*.31))
        for k in range(10):
            a=k*math.tau/10+t*.13;line(im,[(x+15*math.cos(a),y+15*math.sin(a)),(x+r*math.cos(a),y+r*math.sin(a))],rgba(p['accent'],160),3)
    _title(im,c,p,y=398,size=88);_sub(im,c,p,502);return im

def mp27(t,c,p):
    im=_canvas(c,p,'#1D1E26');_title(im,c,p,x=915,y=138,maxw=625,size=62)
    ImageDraw.Draw(im).ellipse((115,572,855,657),fill='#111216',outline=p['secondary'],width=4)
    rr(im,(190,485,784,607),'#333743',23,p['accent'],4)
    swing=math.cos(t*1.6);w=170+66*abs(swing)
    rr(im,(490-w/2,188,490+w/2,506),p['accent'],50,p['text'],3)
    rr(im,(490-w/2+15,260,490+w/2-15,438),p['panel'],11)
    src=_source(c,0,int(w)-25,286)
    if src:paste(im,src,490,345)
    else:text(im,str(c.get('product','PRODUK')),490,349,fit_size(c.get('product','PRODUK'),w-30,31),p['text'])
    x=370+210*((t-1.1)%3.1)/3.1;line(im,[(x,193),(x+42,504)],rgba('#FFFFFF',95),13)
    for j,s in enumerate(_items(c,['CIRI 01','CIRI 02','CIRI 03'])[:3]):
        yy=310+j*99;q=_fade(t,.75+j*.56,1.2+j*.56)
        line(im,[(584,yy),(720,yy)],rgba(p['secondary'],190*q),3)
        _card(im,911,yy,311,70,p,s,opacity=q)
    _sub(im,c,p,665);return im

def mp28(t,c,p):
    im=_canvas(c,p,'#091222');_dots(im,29,630,370,680,p['accent'],t,25)
    s=c['text'];sz=fit_size(s,1070,95);q=ease(prog(t,.2,.9));shift=(8 if int(t*22)%8<2 and t<2 else 0)
    if shift:
        text(im,s,644+shift,334,sz,'#FF4488',opacity=q)
        text(im,s,636-shift,337,sz,'#49E3FF',opacity=q)
        for j in range(5):
            y=215+j*49+((int(t*31)*17+j*5)%20);rr(im,(160,y,1110,y+4),rgba(p['secondary'],80),0)
    text(im,s,640,335,sz,p['text'],opacity=q)
    rr(im,(211,496,1070,565),p['panel'],9)
    ss=c['subtitle'];text(im,'> '+ss[:round(len(ss)*ease(prog(t,1.3,3.2)))],236,528,max(21,fit_size(ss,760,27,'mono')),p['accent'],'mono',anchor='left')
    return im

def mp29(t,c,p):
    im=_canvas(c,p,'#E6B579');sun_y=180+195*ease(prog(t,.3,4.1));circle(im,924,sun_y,101,'#FAE0A1')
    _poly(im,[(0,498),(250,352),(445,520),(670,370),(875,525),(1100,410),(1280,496),(1280,720),(0,720)],'#A27762')
    _rect(im,(0,530,W,H),'#355C50')
    for j in range(6):
        x=92+j*246+25*math.sin(t*.35+j)
        line(im,[(x,580),(x,340)],'#47362F',12);circle(im,x-26,332,55,'#42654E');circle(im,x+38,314,63,'#416D55')
    _poly(im,[(460,476),(584,372),(706,476)],'#643A32');rr(im,(477,474,694,619),'#CE9F6E',4)
    if t>2.5:
        for j in range(22):
            x=(j*103)%W;y=425+(j*47)%210;circle(im,x+7*math.sin(t*2+j),y+7*math.cos(t*2+j),3,rgba(p['accent'],150))
    _title(im,c,p,y=130,size=67);_sub(im,c,p,661);return im

def mp30(t,c,p):
    im=_canvas(c,p,'#E8E7EE');rr(im,(345,50,935,673),'#1B1C31',56)
    rr(im,(363,78,917,650),'#FCFCFF',40);rr(im,(518,93,762,113),'#1B1C31',10)
    items=_items(c,['Dah bersedia?','Jom mula sekarang.','Saya dah cuba!','Bagus, teruskan.'])
    for j,s in enumerate(items[:4]):
        q=ease(prog(t,.35+j*.85,.75+j*.85));right=j%2
        x=640+(110 if right else -110);y=206+j*95+90*(1-q)
        color=p['accent'] if right else '#EAE7F4'
        rr(im,(x-(8 if right else 245),y-31,x+(245 if right else 8),y+32),color,18)
        text(im,s,x+(120 if right else -119),y,fit_size(s,220,24),p['text'] if right else '#29233D','sans',opacity=q)
    if t>3.45:
        for j in range(3):circle(im,553+j*25,588,4+math.sin(t*7+j)*2,p['secondary'])
    return im

def mp31(t,c,p):
    im=_canvas(c,p,'#271333')
    num=max(1,3-min(2,int(t/1.12)));q=ease(prog(t%1.12,.04,.5))
    if t<3.38:
        text(im,str(num),640,335,230,p['accent'],opacity=1-.22*(1-q),scale=1.4-.4*q)
        _ring(im,640,343,185,p['secondary'],11,-90,-90+round(360*q))
    else:
        _title(im,c,p,y=198,size=78)
        price=str(c.get('price','TAWARAN'))
        _card(im,640,355,560,158,p,price,fill=p['accent'],accent=p['text'],angle=5*math.sin(t*4),opacity=ease(prog(t,3.45,4)))
        _card(im,640,556,390,76,p,str(c.get('cta','LIHAT SEKARANG')),opacity=ease(prog(t,4.05,4.48)))
        for j in range(21):
            x=(j*73)%W;y=110+(j*47)%540;_rect(im,(x,y,x+9,y+18),p['secondary'] if j%2 else p['accent'])
    return im

def mp32(t,c,p):
    im=_canvas(c,p,'#F4EFE3');rng=random.Random(32)
    for j in range(38):
        x=rng.randrange(70,1210);y=rng.randrange(70,650);r=(15+rng.randrange(90))*ease(prog(t,.2+j*.025,1.4+j*.025))
        circle(im,x,y,r,rgba(p['secondary'] if j%2 else p['accent'],28))
    pts=[(209,570),(335,446),(485,399),(563,320),(702,293),(843,203),(984,178)]
    q=ease(prog(t,.8,3.15));n=max(2,round(2+q*(len(pts)-2)))
    line(im,pts[:n],p['text'],5)
    for j,(x,y) in enumerate(pts[:n]):
        for k in (-1,1):
            _poly(im,[(x,y),(x+k*45,y-32),(x+k*35,y+17)],rgba(p['secondary'],140))
    _title(im,c,p,y=122,size=66);_sub(im,c,p,643);return im

def mp33(t,c,p):
    im=_canvas(c,p,'#152239');
    for j in range(6):
        x=35+j*240+22*math.sin(t*.45+j);color=p['accent'] if j%2 else p['secondary']
        _poly(im,[(x,346),(x+118,225),(x+239,346)],color)
        rr(im,(x+16,345,x+223,620),'#314154',6)
        if t>.3+j*.2:circle(im,x+119,317,20,'#F9DD9A')
        for k in range(4):
            y=525-k*35;_ring(im,x+101+k*16,y,14,rgba(p['text'],65),2,200,335)
    rr(im,(395,367,895,605),p['panel'],28,p['accent'],4)
    src=_source(c,0,420,200)
    if src:paste(im,src,645,482)
    else:circle(im,645,484,94,p['accent']);_ring(im,645,484,60,p['text'],5)
    _title(im,c,p,y=118,size=75);_sub(im,c,p,670);return im

def mp34(t,c,p):
    im=_canvas(c,p,'#F5F2E9');_title(im,c,p,y=86,size=58)
    items=_items(c,['IDEA','PROSES','HASIL']);centers=[(320,362),(640,362),(960,362)]
    for j,(x,y) in enumerate(centers):
        q=ease(prog(t,.25+j*.72,1+j*.72));_ring(im,x,y,88,p['accent'],5,-90,-90+round(360*q))
        if q>.1:
            s=items[j%len(items)];text(im,s[:round(len(s)*q)],x,y,fit_size(s,160,32),p['text'],'mono')
        if j<2:
            ax=x+90;bx=centers[j+1][0]-90;qq=ease(prog(t,1+j*.72,1.7+j*.72))
            line(im,[(ax,y),(mix(ax,bx,qq),y)],p['secondary'],5)
            if qq>.8:arrow(im,bx,y,p['secondary'])
    for j in range(10):
        x=150+j*100;y=574+13*math.sin(j*1.4)
        if t>1.8+j*.18:line(im,[(x,y),(x+32,y-15)],rgba(p['muted'],95),3)
    _sub(im,c,p,639);return im

def mp35(t,c,p):
    im=_canvas(c,p,'#25123E')
    # Metallic illusion from nested moving bands, intentionally a 2.5D composite.
    x=627+60*math.sin(t*.8);y=368+35*math.cos(t*.7)
    for j,color in enumerate(['#2A2A3F','#646779','#BFC6D6','#F4F8FC','#8F95AA']):
        r=185-j*22;circle(im,x+12*j,y-7*j,r,color)
    for j in range(9):
        a=j*math.tau/9+t*.6;xx=x+306*math.cos(a);yy=y+225*math.sin(a)
        rr(im,(xx-23,yy-14,xx+23,yy+14),p['accent'] if j%2 else p['secondary'],7)
    text(im,c['text'],640,390,fit_size(c['text'],1100,95),p['text'],stroke=4,stroke_color=p['accent'],opacity=_fade(t,.5,1.2))
    _sub(im,c,p,644);return im

def mp36(t,c,p):
    im=_canvas(c,p,'#9C1E31')
    for j in range(4):
        x=190+j*295+24*math.sin(t*.8+j);line(im,[(x,0),(x,179)],p['accent'],3)
        rr(im,(x-42,175,x+42,263),p['accent'],13)
        _ring(im,x,218,23,'#B02231',4)
        line(im,[(x,263),(x,297)],p['accent'],3)
    for j in range(9):
        x=105+j*137;y=453+34*math.sin(t*.4+j)
        r=29*ease(prog(t,.2+j*.13,.7+j*.13));_poly(im,[(x,y-r),(x+r,y),(x,y+r),(x-r,y)],rgba('#F5C857',195))
    rr(im,(265,309,1015,538),'#861A2E',18,p['accent'],5)
    _title(im,c,p,y=402,size=67);_sub(im,c,p,618);return im

# MP37–MP48: spatial, documentary, handcrafted and technology scenes.
def mp37(t,c,p):
    p=dict(p,text=c.get('text_color','#273044'));im=_canvas(c,p,'#F3F0EA');_title(im,c,p,y=82,size=58)
    default_rooms=[(150,230,430,450),(430,230,690,450),(690,230,1000,450),(150,450,575,595),(575,450,1000,595)]
    rooms=c.get('rooms',default_rooms)
    if not isinstance(rooms,list) or len(rooms)!=5 or any(not isinstance(box,(list,tuple)) or len(box)!=4 for box in rooms):rooms=default_rooms
    items=_items(c,['RUANG 01','RUANG 02','RUANG 03','RUANG 04','RUANG 05'])
    for j,(x0,y0,x1,y1) in enumerate(rooms):
        q=ease(prog(t,.25+j*.37,.9+j*.37));raised=32*q
        _poly(im,[(x0,y0),(x0+raised,y0-raised),(x1+raised,y0-raised),(x1,y0)],rgba(p['secondary'],170))
        rr(im,(x0,y0,x1,y1),p['accent'] if j==min(4,int(t)) and t>1 else '#FFFFFF',3,p['text'],3)
        line(im,[(x0,y0),(x0+raised,y0-raised),(x1+raised,y0-raised),(x1,y0)],p['text'],2)
        if q>.65:text(im,items[j%len(items)],(x0+x1)/2,(y0+y1)/2,fit_size(items[j%len(items)],x1-x0-18,27),p['text'])
    _card(im,1100,501,238,90,p,str(c.get('price','PELAN')),opacity=ease(prog(t,3.3,3.8)))
    if rooms is default_rooms:text(im,'PELAN DEMO',1086,615,17,p['muted'],'mono')
    return im

def mp38(t,c,p):
    im=_canvas(c,p,'#0B1425');rng=random.Random(38)
    q=ease(prog(t,1.15,3.2));s=c['text'];mask=text_img(s,fit_size(s,980,92),'#FFFFFF').getchannel('A')
    # Deterministic particles target points from the text mask; sampling is cached.
    tx,ty=640-mask.width/2,355-mask.height/2
    coords=[]
    for y in range(0,mask.height,5):
        for x in range(0,mask.width,5):
            if mask.getpixel((x,y))>128:coords.append((x+tx,y+ty))
    for j in range(320):
        a=rng.random()*math.tau;r=90+650*rng.random();sx=640+r*math.cos(a);sy=360+r*.6*math.sin(a)
        dest=coords[j*len(coords)//320] if coords else (640,360)
        xx=mix(sx,dest[0],q)+8*math.sin(t*1.3+j);yy=mix(sy,dest[1],q)+6*math.cos(t*1.1+j)
        circle(im,xx,yy,2+(j%3),rgba(p['accent'] if j%3 else p['secondary'],90+j%4*35))
    if t>3.1:text(im,s,640,355,fit_size(s,980,92),p['text'],opacity=.75*prog(t,3.1,3.8))
    _sub(im,c,p,592);return im

def mp39(t,c,p):
    p=dict(p,text=c.get('text_color','#FFFFFF'));im=_canvas(c,p,'#5A4A3A');rr(im,(244,113,1024,630),'#3C352F',45,p['accent'],5)
    rr(im,(292,159,903,585),'#131F25',42,rgba(p['text'],100),4)
    switch=ease(prog(t,.45,1.1));height=max(2,round(410*switch));_rect(im,(306,370-height/2,889,370+height/2),'#77909B')
    src=_source(c,0,570,390)
    if src and switch>.65:paste(im,src,597,370,opacity=switch)
    else:
        for j in range(7):_rect(im,(307,190+j*53,887,217+j*53),['#D97664','#F4C96E','#7BBEA9','#7386C7'][j%4])
    for j in range(20):
        yy=180+j*20+(t*12)%20;line(im,[(307,yy),(888,yy)],rgba('#1D2732',60),2)
    text(im,c['text'],590,340,fit_size(c['text'],545,55),p['text'],opacity=switch)
    circle(im,962,267,27,p['accent']);circle(im,962,351,21,p['secondary']);_sub(im,c,p,672);return im

def mp40(t,c,p):
    im=_canvas(c,p,'#271C38');rr(im,(124,169,1156,581),p['panel'],31,p['secondary'],3)
    circle(im,312,367,132,p['accent']);src=_source(c,0,224,224)
    if src:paste(im,src,312,367)
    else:text(im,'MIC',312,367,66,p['text'])
    samples=c.get('amplitudes')
    valid=isinstance(samples,list) and len(samples)>0 and all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in samples)
    for j in range(40):
        xx=505+j*14
        amp=clamp(samples[min(len(samples)-1,int(t/5*len(samples)+j*len(samples)/40)%len(samples))]) if valid else abs(math.sin(t*4+j*.55)*math.cos(t*1.6+j*.14))
        h=25+99*amp
        rr(im,(xx,444-h,xx+8,444+h),p['accent'] if j%4 else p['secondary'],4)
    words=c['text'].split();pos=750
    if words:
        active=int(t*len(words)/4)%len(words)
        for j,w in enumerate(words[:5]):
            text(im,w,pos,276+j*45,fit_size(w,340,37),p['accent'] if j==active else p['text'])
    if not valid:text(im,'WAVEFORM DEMO',640,568,16,p['muted'],'mono')
    _sub(im,c,p,635);return im

def mp41(t,c,p):
    p=dict(p,text=c.get('text_color','#F5F1E6'));im=_canvas(c,p,'#10291F')
    for depth,color in [(0,'#1D4B36'),(1,'#276D44'),(2,'#0E382B')]:
        for j in range(7):
            x=j*214-75+depth*53+22*math.sin(t*.3+depth+j)
            line(im,[(x,0),(x+43,720)],color,22+depth*6)
            for k in range(3):
                xx=x+35+k*48;yy=220+k*125
                _poly(im,[(xx,yy-110),(xx+54,yy),(xx,yy+82),(xx-38,yy)],color)
    mist=layer();
    for j in range(9):circle(mist,100+j*150+25*math.sin(t*.28+j),470+j%2*47,125,rgba('#E8F2DC',23))
    im.alpha_composite(mist.filter(ImageFilter.GaussianBlur(48)))
    birdx=100+1100*ease(prog(t,.75,4.3));birdy=244+14*math.sin(t*4)
    _poly(im,[(birdx-75,birdy-20),(birdx,birdy),(birdx+70,birdy-24),(birdx+20,birdy+26)],'#171C1B')
    circle(im,birdx+41,birdy+3,12,p['accent'])
    _title(im,c,p,y=390,size=70);_sub(im,c,p,493);return im

def mp42(t,c,p):
    im=_canvas(c,p,'#F7E4C6')
    for j,color in enumerate(['#D6E1A6','#A0CE8D','#5EAB80']):
        q=ease(prog(t,.2+j*.42,.85+j*.42));y=490+j*67
        _poly(im,[(0,H),(0,y+60*(1-q)),(280,y-90*q),(580,y+30),(860,y-110*q),(1280,y),(1280,H)],color)
    sun_q=ease(prog(t,.5,1.3));circle(im,1010,222+130*(1-sun_q),78,'#F2AD4A')
    for j in range(6):
        x=120+j*203;yy=215+24*math.sin(t*.9+j)
        _poly(im,[(x-82,yy),(x,yy-32),(x+82,yy),(x,yy+32)],'#FFFFFF')
        line(im,[(x-82,yy+12),(x+82,yy+12)],rgba(p['muted'],65),3)
    rr(im,(303,267,979,418),'#FFFAEC',18,rgba(p['muted'],150),3)
    text(im,c['text'],640,339,fit_size(c['text'],640,71),p['text'],opacity=ease(prog(t,1.1,1.8)))
    rr(im,(386,251,463,270),rgba(p['accent'],140),2);rr(im,(860,410,932,431),rgba(p['secondary'],130),2)
    _sub(im,c,p,625);return im

def mp43(t,c,p):
    # Draw at an exact low-resolution grid and scale up with NEAREST.
    lo=Image.new('RGBA',(320,180),'#4CA4D9');d=ImageDraw.Draw(lo)
    for j in range(7):d.rectangle((j*48,122,320,180),fill='#39784A' if j%2 else '#417A3E')
    for j in range(5):
        x=67+j*53;q=ease(prog(t,.4+j*.38,.9+j*.38))
        d.rectangle((x,94-30*q,x+27,122),fill='#EBC663',outline='#1D2036',width=2)
        d.text((x+8,95-25*q),'?',fill='#1D2036')
    player_x=35+233*ease(prog(t,.4,3.9));jump=24*max(0,math.sin(t*4.6))
    d.rectangle((player_x,100-jump,player_x+22,123-jump),fill='#E15E62',outline='#1D2036',width=2)
    d.rectangle((player_x+5,102-jump,player_x+9,106-jump),fill='#FFFFFF')
    im=lo.resize((W,H),Image.Resampling.NEAREST)
    text(im,c['text'],640,182,fit_size(c['text'],950,80),p['text'],stroke=3,stroke_color=p['panel'])
    text(im,c['subtitle'],640,629,fit_size(c['subtitle'],1000,27),p['text'],'mono')
    return im

def mp44(t,c,p):
    p=dict(p,text=c.get('text_color','#FFFFFF'));im=_canvas(c,p,'#2A0A35');cx,cy=640,378
    for j in range(5):
        r=42+j*58;q=ease(prog(t,.15+j*.35,.8+j*.35));_ring(im,cx,cy,r,p['accent'] if j%2 else p['secondary'],7,-90,-90+round(360*q))
        for k in range(8):
            a=k*math.tau/8;xx=cx+r*math.cos(a);yy=cy+r*math.sin(a)
            _poly(im,[(xx,yy-21*q),(xx+18*q,yy),(xx,yy+21*q),(xx-18*q,yy)],p['secondary'] if j%2 else p['accent'])
    for j in range(7):
        x=196+j*148;yy=602;rr(im,(x-24,yy,x+24,yy+47),'#C87843',9)
        if t>.7+j*.26:circle(im,x,yy-9+4*math.sin(t*6+j),11,'#F9C05A')
    _title(im,c,p,y=77,size=66);_sub(im,c,p,655);return im

def mp45(t,c,p):
    im=_canvas(c,p,'#ECDDCA');rng=random.Random(45)
    for j in range(65):circle(im,rng.randrange(W),rng.randrange(H),rng.randrange(1,4),rgba(p['muted'],50))
    _title(im,c,p,y=80,size=60)
    for j in range(3):
        q=ease(prog(t,.3+j*.82,.85+j*.82));x=287+j*330;y=328+22*math.sin(t*.3+j)
        rr(im,(x-119,y-120,x+119,y+133),'#FFF8E9',8,p['muted'],2)
        src=_source(c,j,204,182)
        if src:paste(im,src,x,y-12,opacity=q)
        else:rr(im,(x-103,y-104,x+103,y+71),rgba(p['secondary'],140),3)
        text(im,str(c.get('start_year',1980)+j*10),x,y+104,26,p['text'],'mono',opacity=q)
    q=ease(prog(t,.65,4));line(im,[(135,566),(135+1000*q,566)],p['accent'],6)
    for j in range(3):
        xx=287+j*330
        if t>1+j*.85:circle(im,xx,566,16,p['accent'])
    _sub(im,c,p,647);return im

def mp46(t,c,p):
    p=dict(p,text=c.get('text_color','#141414'));im=_canvas(c,p,'#EFE9DC');
    for x in range(0,W,160):line(im,[(x,0),(x,H)],rgba(p['muted'],65),1)
    for y in range(0,H,120):line(im,[(0,y),(W,y)],rgba(p['muted'],65),1)
    items=_items(c,['01  STRATEGI','02  REKA','03  HASIL'])
    _title(im,c,p,x=135,y=116,maxw=975,size=80,align='left')
    for j,s in enumerate(items[:4]):
        y=260+j*102;q=ease(prog(t,.45+j*.64,1+j*.64))
        line(im,[(140,y-35),(1100,y-35)],p['text'],2)
        text(im,s,158,y,fit_size(s,660,52),p['accent'] if j==int(t)%len(items) else p['text'],opacity=q,anchor='left')
        x=1015;angle=(j+int(t))%4
        if angle%2:rr(im,(x-35,y-38,x+35,y+31),p['accent'],0)
        else:circle(im,x,y-4,34,p['secondary'])
    _sub(im,c,p,674);return im

def mp47(t,c,p):
    p=dict(p,text=c.get('text_color','#2B1055'));im=_canvas(c,p,'#E8D3F5');rr(im,(416,168,871,504),'#5C499C',27,p['text'],4)
    _screen(im,c,0,439,199,409,258,p)
    rr(im,(534,497,759,521),'#7361AC',7);rr(im,(480,521,811,545),'#584789',10)
    labels=_items(c,['VIDEO','DATA','KONGSI','IDEA','CHAT'])
    for j,s in enumerate(labels[:5]):
        a=j*math.tau/5+t*.45;r=229+30*math.sin(t*.9+j);x=640+r*math.cos(a);y=355+r*.55*math.sin(a)
        q=ease(prog(t,.25+j*.3,.9+j*.3));_card(im,x,y-105*(1-q),155,98,p,s,fill=p['accent'] if j%2 else p['secondary'],opacity=q,scale=.7+.3*q)
    _title(im,c,p,y=89,size=63);_sub(im,c,p,657);return im

def mp48(t,c,p):
    im=_canvas(c,p,'#1C0A45');cx,cy=649,367
    for j in range(5):
        r=160+j*36;_ring(im,cx,cy,r,rgba(p['secondary'],90),2,-90+round(t*25+j*7),-90+round(t*25+j*7+210))
    for j in range(8):
        x=80+j*159;y=105+(j%4)*127;line(im,[(x,0),(x,y),(x+85,y)],rgba(p['accent'],150),3)
        circle(im,x+85,y,6,p['secondary'])
    # An isometric device and holograms, with visible layer depth.
    _poly(im,[(417,453),(791,453),(934,566),(300,566)],'#32216E')
    rr(im,(466,270,798,453),'#2D2B73',15,p['secondary'],3)
    _screen(im,c,0,486,291,292,143,p)
    for j,s in enumerate(_items(c,['CLOUD','ANALITIK','AUTOMASI'])[:3]):
        q=ease(prog(t,.65+j*.41,1.3+j*.41));x=380+j*267;y=226-50*q
        _card(im,x,y,206,79,p,s,fill='#204B71',accent=p['accent'],opacity=q)
        line(im,[(x,y+44),(630,288)],rgba(p['accent'],130*q),2)
    text(im,c['text'],640,617,fit_size(c['text'],1080,71),p['text'],opacity=_fade(t,1.2,1.7),stroke=2,stroke_color=p['accent'])
    return im

SCENES={f'MP{i:02d}':globals()[f'mp{i:02d}'] for i in range(1,49)}
