"""Eight original product and notification presets; deterministic five-second loops.

No third-party screenshots, templates or preview media are embedded. All UI is
drawn here. Numerical labels are demonstration data, not product performance.
"""
from core import *

PRESETS = {
 'U01':dict(name='Logo → dashboard',description='Satu logo bergerak berterusan ke header sebelum widget muncul.',genre='saas',genres=['saas','corporate','promo'],text='Orbit',subtitle='Semua kerja. Satu ruang.'),
 'U02':dict(name='Dashboard data build',description='Shell, metrik dan carta dibina berperingkat; nilai mengikut progress carta.',genre='saas',genres=['saas','corporate','education'],text='Lihat kemajuan.',subtitle='Angka demo untuk cerita anda.'),
 'U03':dict(name='App icon extraction',description='Ikon aplikasi keluar dari slot skrin dan menjadi objek hero tunggal.',genre='promo',genres=['saas','promo','creator'],text='Idea, bergerak.',subtitle='Dari skrin ke kemungkinan.'),
 'U04':dict(name='Perspective panel stack',description='Panel berperspektif dan kedalaman berlapis dengan kemasukan bersela.',genre='corporate',genres=['saas','corporate','promo'],text='Satu pandangan.',subtitle='Hubungkan setiap bahagian.'),
 'N01':dict(name='Notification reflow',description='Kad berlainan tinggi masuk sambil kad lama beralih dengan gap tetap.',genre='saas',genres=['saas','corporate','creator'],text='Sentiasa seiring.',subtitle='Kemas kini tanpa terlepas.'),
 'N02':dict(name='Grouped notification stack',description='Kad aktif dengan tiga lapisan belakang yang menyebar dan merapat.',genre='creator',genres=['creator','saas','promo'],text='Semua di sini.',subtitle='Satu kumpulan. Banyak cerita.'),
 'N03':dict(name='Message typing reveal',description='Bekas, ikon, nama dan teks muncul mengikut urutan dengan layout terkunci.',genre='corporate',genres=['corporate','saas','education'],text='Mesej yang jelas.',subtitle='Projek anda sudah sedia untuk disemak.'),
 'N04':dict(name='Phone screen notifications',description='Notifikasi dan banner panggilan diklip pada skrin telefon berperspektif.',genre='saas',genres=['saas','promo','corporate'],text='Dekat, sentiasa.',subtitle='Maklumat tepat pada waktunya.'),
}

def _cfg(pid,cfg):
    out=dict(PRESETS[pid]);out.update(cfg);return out

def _wrap(s,size,maxw,face='bold',maxlines=4):
    lines=[];cur=''
    for w in str(s).split():
        trial=(cur+' '+w).strip()
        if measure(trial,size,face)>maxw and cur:lines.append(cur);cur=w
        else:cur=trial
    if cur:lines.append(cur)
    if len(lines)>maxlines:lines=lines[:maxlines-1]+[' '.join(lines[maxlines-1:])]
    return lines

def _copy(dst,cfg,p,t,x=78,y=290,width=330,size=46):
    a=life(t,.23,.95,4.12,4.73);q=enter(t,.23,.95)
    while size>20 and len(_wrap(cfg['text'],size,width,maxlines=99))>3:size-=1
    words=_wrap(cfg['text'],size,width,maxlines=3)
    yy=y+23*(1-q)-12*leave(t)
    for i,s in enumerate(words):
        text(dst,s,x,yy+i*size*1.2,fit_size(s,width,size),p['text'],opacity=a,anchor='left')
    yy+=len(words)*size*1.2+22
    subsize=18
    while subsize>10 and len(_wrap(cfg['subtitle'],subsize,width,'sans',99))>3:subsize-=1
    sublines=_wrap(cfg['subtitle'],subsize,width,'sans',3)
    for i,s in enumerate(sublines):
        fs=min(subsize,max(8,int(subsize*width/max(1,measure(s,subsize,'sans')))))
        text(dst,s,x,yy+i*(subsize+8),fs,p['muted'],'sans',opacity=a,anchor='left')
    if a>.1:
        ll=layer(150,4);rr(ll,(0,0,85*q,3),p['accent'],2)
        paste(dst,ll,x,yy+len(sublines)*(subsize+8)+15,a,anchor='left')

@lru_cache(maxsize=64)
def _orbit(size,accent,bg='#111A2A'):
    im=layer(size,size);d=ImageDraw.Draw(im)
    rr(im,(0,0,size-1,size-1),accent,size*.24)
    c=rgb(bg);d.ellipse((size*.30,size*.30,size*.70,size*.70),fill=c)
    d.arc((size*.15,size*.15,size*.85,size*.85),24,286,fill=c,width=max(2,int(size*.065)))
    circle(im,size*.82,size*.38,size*.065,c)
    return im

@lru_cache(maxsize=64)
def _shell(w,h,bg,panelc,txt,muted,accent,kind='overview'):
    im=layer(w,h);rr(im,(0,0,w-1,h-1),panelc,22,rgba(muted,65))
    rr(im,(1,1,w-2,55),bg,21);rr(im,(1,28,w-2,55),bg,0)
    for i in range(3):circle(im,19+i*13,18,3,rgba(muted,110))
    text(im,'orbit / workspace',58,20,11,muted,'mono',anchor='left')
    rr(im,(w-145,12,w-18,31),rgba(accent,25),8)
    text(im,'●  LIVE DEMO',w-82,22,10,accent,'mono')
    line(im,[(0,55),(w,55)],rgba(muted,60),1)
    # Sidebar is deliberately restrained so the data remains the focus.
    side=126 if w>=600 else 90
    line(im,[(side,55),(side,h-1)],rgba(muted,40),1)
    tabs=['Overview','Projects','Insights','Team']
    for i,s in enumerate(tabs):
        yy=87+i*38
        if i==0:rr(im,(12,yy-14,side-10,yy+14),rgba(accent,22),8)
        circle(im,24,yy,3,accent if i==0 else muted)
        text(im,s,36,yy,11 if w>=600 else 9,txt if i==0 else muted,'sans',anchor='left')
    text(im,'DEMO DATA',17,h-20,9,muted,'mono',anchor='left')
    return im

def _chart(im,box,p,q=1.,variant=0):
    x,y,w,h=box
    for i in range(4):line(im,[(x,y+i*h/3),(x+w,y+i*h/3)],rgba(p['muted'],32),1)
    vals=([.76,.68,.72,.43,.50,.30,.37,.12,.18,.04] if variant==0 else [.8,.73,.54,.65,.44,.39,.50,.25,.20,.10])
    pts=[(x+i*w/(len(vals)-1),y+h*v) for i,v in enumerate(vals)]
    # Reveal by horizontal distance. Endpoint interpolates within the active segment.
    if q<=0:return
    cut=q*(len(pts)-1);idx=min(len(pts)-2,int(cut));frac=cut-idx
    shown=pts[:idx+1]+[(mix(pts[idx][0],pts[idx+1][0],frac),mix(pts[idx][1],pts[idx+1][1],frac))]
    if q>=1:shown=pts
    poly=shown+[(shown[-1][0],y+h),(x,y+h)]
    fill_layer=layer(im.width,im.height)
    ImageDraw.Draw(fill_layer).polygon(poly,fill=rgba(p['accent'],24))
    im.alpha_composite(fill_layer)
    line(im,shown,p['accent'],3)
    ex,ey=shown[-1];circle(im,ex,ey,5,p['accent']);circle(im,ex,ey,2,p['panel'])

def _metric(im,box,p,title,value,unit='',q=1.):
    x,y,w,h=box;rr(im,(x,y,x+w,y+h),rgba(p['bg'],190),13,rgba(p['muted'],50))
    text(im,title,x+14,y+19,10,p['muted'],'sans',anchor='left')
    text(im,str(value)+unit,x+14,y+47,25,p['text'],anchor='left')
    line(im,[(x+14,y+h-13),(x+14+(w-28)*q,y+h-13)],p['accent'],3)

def _dashboard(p,w=740,h=355,q=1.,build=1.,brand='Workspace'):
    im=_shell(w,h,p['bg'],p['panel'],p['text'],p['muted'],p['accent']).copy()
    side=126 if w>=600 else 90
    text(im,brand,side+23,82,fit_size(brand,w-side-46,17),p['text'],anchor='left')
    text(im,'Weekly activity',side+23,109,11,p['muted'],'sans',anchor='left')
    inner=w-side-46;kw=(inner-24)/3
    metrics=[('ACTIVE TASKS',int(round(128*q)),''),('COMPLETED',int(round(84*q)),'%'),('TEAM MEMBERS',int(round(24*q)),'')]
    for i,(title,val,unit) in enumerate(metrics):
        a=clamp(build*3-i*.32)
        if a>0:
            piece=layer(w,h);_metric(piece,(side+23+i*(kw+12),132,kw,78),p,title,val,unit,q)
            paste(im,piece,w/2,h/2+12*(1-a),a)
    a=clamp(build*2-.6)
    if a>0:
        graph=layer(w,h);text(graph,'Performance',side+23,231,12,p['text'],anchor='left')
        text(graph,'7 DAYS',w-66,231,9,p['muted'],'mono')
        _chart(graph,(side+23,252,inner,max(25,h-278)),p,q)
        paste(im,graph,w/2,h/2,a)
    return im

def _body_clip(src):
    out=layer();out.alpha_composite(src.crop((0,146,W,613)),(0,146));return out

def _exitgroup(dst,src,t,y=0):paste(dst,_body_clip(src),W/2,H/2+y-35*leave(t),1-leave(t))

@lru_cache(maxsize=64)
def _phone_shell(w,h,accent,panelc,bg,txt,muted):
    im=layer(w,h);rr(im,(3,0,w-4,h-1),'#030509',39,'#8493A4',2)
    rr(im,(6,3,w-7,h-4),'#131A24',36,'#263342',2)
    rr(im,(13,9,w-14,h-10),bg,29)
    # Rim highlights and buttons give the silhouette controlled depth.
    line(im,[(8,46),(8,h-51)],'#5A6876',1)
    line(im,[(w-7,70),(w-7,h-91)],'#283440',2)
    rr(im,(w*.33,17,w*.67,32),'#010307',8)
    circle(im,w*.61,24,3,'#172638')
    text(im,'9:41',30,27,9,txt,'sans',anchor='left')
    rr(im,(w-42,22,w-28,28),None,2,txt,1)
    rr(im,(w-41,23,w-32,27),txt,1)
    rr(im,(w*.35,h-22,w*.65,h-18),rgba(txt,170),3)
    return im

def _phone_home(p,w=226,h=409,empty_index=4):
    im=_phone_shell(w,h,p['accent'],p['panel'],p['bg'],p['text'],p['muted']).copy()
    text(im,'Tuesday, 24 September',w/2,65,9,p['muted'],'sans')
    text(im,'09:41',w/2,98,37,p['text'])
    rr(im,(27,130,w-27,191),p['panel'],13)
    text(im,'YOUR WORKSPACE',40,147,8,p['muted'],'mono',anchor='left')
    text(im,'Ideas start here.',40,173,15,p['text'],anchor='left')
    for i in range(6):
        col=i%3;row=i//3;x=49+col*64;y=230+row*72
        if i!=empty_index:
            rr(im,(x-20,y-20,x+20,y+20),p['panel'],10)
            if i%3==0:
                for k in range(3):line(im,[(x-10,y-8+k*7),(x+10,y-8+k*7)],p['secondary'],2)
            elif i%3==1:
                circle(im,x,y,10,p['secondary']);circle(im,x,y,5,p['panel'])
            else:
                line(im,[(x-10,y+9),(x-4,y-3),(x+2,y+3),(x+10,y-11)],p['secondary'],3)
        text(im,['Notes','Flow','Insights','Inbox','Orbit','Team'][i],x,y+30,8,p['muted'],'sans')
    return im

def _local_warp(src,quad):
    xs=[x for x,y in quad];ys=[y for x,y in quad]
    x0=math.floor(min(xs));y0=math.floor(min(ys));ww=math.ceil(max(xs))-x0+1;hh=math.ceil(max(ys))-y0+1
    return warp_quad(src,[(x-x0,y-y0) for x,y in quad],(ww,hh)),x0,y0

@lru_cache(maxsize=48)
def _perspective_panel(accent,genre,depth):
    p=palette({'accent':accent,'genre':genre});src=_dashboard(p,620,322,1,1,['Overview','Studio','Analytics'][depth])
    # Static perspective textures can be cached; all scene transforms remain continuous.
    skew=30+depth*6
    quad=[(0,skew),(620,0),(615,295),(4,322)]
    warped,x,y=_local_warp(src,quad)
    shadow=layer(warped.width+34,warped.height+40)
    mask=warped.getchannel('A');shade=Image.new('RGBA',warped.size,(0,0,0,90));shade.putalpha(mask.point(lambda a:a*90//255))
    shadow.alpha_composite(shade,(18,25));shadow=shadow.filter(ImageFilter.GaussianBlur(9));shadow.alpha_composite(warped,(12,8))
    return shadow

def _avatar(dst,cx,cy,r,p,initial='O',color=None):
    circle(dst,cx,cy,r,color or p['accent']);text(dst,initial,cx,cy,max(10,int(r)),p['bg'])

def _notify(p,w,h,title,body,time='now',kind=0,bodyprogress=1.,headeralpha=1.,iconalpha=1.):
    im=layer(w,h);rr(im,(0,0,w-1,h-1),p['panel'],18,rgba(p['muted'],80))
    # A slim accent rule connects cards without cluttering the body copy.
    rr(im,(0,20,3,h-20),p['accent'],1)
    compact=w<300
    iconsize=26 if compact else 36
    icon=_orbit(iconsize,p['accent'],p['bg']) if kind==0 else layer(iconsize,iconsize)
    if kind:
        _avatar(icon,iconsize/2,iconsize/2,iconsize/2,p,['O','A','M','K'][kind%4],p['secondary'] if kind%2 else p['accent'])
    cx,cy,left,ty,by,fs,lh=(24,23,44,19,39,10,14) if compact else (37,31,66,25,49,14,20)
    paste(im,icon,cx,cy,iconalpha)
    text(im,title,left,ty,10 if compact else 13,p['text'],opacity=headeralpha,anchor='left')
    text(im,time,w-14 if compact else w-22,ty,7 if compact else 9,p['muted'],'sans',opacity=headeralpha,anchor='right')
    bodylines=_wrap(body,fs,w-left-18,'sans',2 if compact else 3)
    total=len(str(body));remaining=max(0,int(total*clamp(bodyprogress)))
    # Reveal into premeasured fixed lines; no layout change while typing.
    for i,s in enumerate(bodylines):
        shown=s[:remaining];remaining=max(0,remaining-len(s)-1)
        shownsize=min(fs,max(7,int(fs*(w-left-18)/max(1,measure(s,fs,'sans')))))
        text(im,shown,left,by+i*lh,shownsize,p['text'],'sans',anchor='left')
    return im

def _u01(t,cfg,p,out):
    scene=layer();a=enter(t,.2,.9);move=smooth(prog(t,.85,1.85));b=enter(t,.7,1.6)
    # Logo is intentionally absent from the dashboard texture: one object throughout.
    dash=_dashboard(p,800,382,ease(prog(t,1.2,2.6)),enter(t,1.0,2.15),cfg['text'])
    paste(scene,dash,660,379+45*(1-b),b,scale=.94+.06*b)
    logo=_orbit(114,p['accent'],p['bg']);paste(scene,logo,mix(640,310,move),mix(344,228,move),a,scale=mix(1.,.30,move),angle=0)
    # The terminal brand sits outside the texture beside its continuous icon.
    # Fade the initial label before movement prevents a duplicate word treatment.
    text(scene,cfg['text'],640,443,fit_size(cfg['text'],540,38),p['text'],opacity=a*(1-smooth(prog(t,.7,1.1))))
    text(scene,cfg['subtitle'],660,592,fit_size(cfg['subtitle'],800,18,'sans'),p['muted'],'sans',opacity=enter(t,1.75,2.3))
    _exitgroup(out,scene,t)

def _u02(t,cfg,p,out):
    _copy(out,cfg,p,t,size=44,width=315,y=273)
    scene=layer();e=enter(t,.28,.95)
    q=ease(prog(t,1.0,2.75));dashboard=_dashboard(p,746,375,q,enter(t,.8,1.9),'Performance')
    paste(scene,dashboard,825,379+35*(1-e),e,scale=.96+.04*e)
    # Progress ring and caption use exactly the same value as the primary chart.
    rr(scene,(915,580,1179,606),rgba(p['accent'],24*e),13)
    text(scene,f'{round(84*q)}% COMPLETE · DEMO',1047,594,11,p['accent'],'mono',opacity=e)
    _exitgroup(out,scene,t)

def _u03(t,cfg,p,out):
    _copy(out,cfg,p,t,x=77,y=280,width=295,size=45)
    scene=layer();e=enter(t,.2,.95);detach=smooth(prog(t,1.05,2.35));phoneexit=smooth(prog(t,2.05,3.05))
    phone=_phone_home(p);px=mix(593,488,phoneexit);py=381+40*(1-e)
    paste(scene,phone,px,py,e*(1-phoneexit),angle=3*phoneexit)
    # empty_index=4 leaves the matching slot blank; only this icon is rendered.
    ix0=593;iy0=381-409/2+302
    ix=mix(ix0,889,detach);iy=mix(iy0,344,detach)-40*math.sin(math.pi*detach)
    icon=_orbit(124,p['accent'],p['bg']);paste(scene,icon,ix,iy+40*(1-e),e,scale=mix(40/124,1.08,detach),angle=-9*math.sin(math.pi*detach))
    ring=layer(240,240);ImageDraw.Draw(ring).arc((10,10,230,230),-80,-80+int(270*detach),fill=rgba(p['accent'],110),width=2)
    paste(scene,ring,889,344,detach*.6,angle=12*math.sin(t))
    text(scene,'ORBIT',889,451,22,p['text'],opacity=enter(t,2.15,2.8))
    taglayer=layer();tag(taglayer,'OPEN POSSIBILITIES',799,497,p);paste(scene,taglayer,W/2,H/2,enter(t,2.3,2.9))
    _exitgroup(out,scene,t)

def _u04(t,cfg,p,out):
    _copy(out,cfg,p,t,x=73,y=304,width=286,size=44)
    scene=layer()
    for depth in (2,1,0):
        e=enter(t,.2+(2-depth)*.14,.92+(2-depth)*.14)
        tex=_perspective_panel(p['accent'],cfg.get('genre','corporate'),depth)
        scl=1-depth*.075;x=856-depth*75;y=413-depth*57
        drift=math.sin((t-1.0)*.9)*2*(1-depth*.18)
        paste(scene,tex,x+75*(1-e),y+25*(1-e)+drift,e*(1-depth*.08),scl,angle=(1-e)*-5)
    _exitgroup(out,scene,t)

def _n01(t,cfg,p,out):
    _copy(out,cfg,p,t,x=75,y=283,width=350,size=43)
    scene=layer();p1=enter(t,.18,.78);p2=smooth(prog(t,1.03,1.78));p3=smooth(prog(t,2.15,2.9))
    # Stable IDs A/B/C. Each common shift equals the measured newcomer height+gap.
    bodies=['Fail baharu telah dimuat naik.','Semua maklum balas sudah dikumpulkan. Mari semak bersama.',cfg['subtitle']]
    gap=14;heights=[max(minh,49+(len(_wrap(msg,14,555-89,'sans',3))-1)*20+20) for minh,msg in zip([88,104,92],bodies)]
    yA=580-heights[0]-(heights[1]+gap)*p2-(heights[2]+gap)*p3
    yB=yA+heights[0]+gap;yC=yB+heights[1]+gap
    cards=[('Orbit',bodies[0],heights[0],yA,p1,0),('Aina · Design',bodies[1],heights[1],yB,p2,1),('Team update',bodies[2],heights[2],yC,p3,2)]
    for title,body,h,y,a,kind in cards:
        img=_notify(p,555,h,title,body,'now' if kind else '2m',kind)
        paste(scene,img,881+38*(1-a),y+h/2,a)
    _exitgroup(out,scene,t)

def _n02(t,cfg,p,out):
    _copy(out,cfg,p,t,x=76,y=282,width=338,size=44)
    scene=layer();breathe=.5+.5*math.sin((t-1.3)*1.6);spread=enter(t,.8,1.7)*(18+9*breathe)
    for i in (3,2,1):
        e=enter(t,.16+(3-i)*.13,.78+(3-i)*.13)
        card=_notify(p,544,146,'Orbit workspace','New activity in your workspace.',kind=i)
        paste(scene,card,875,343+i*spread+40*(1-e),e*(.68-.11*i),scale=1-.045*i)
    e=enter(t,.47,1.08);front=_notify(p,544,146,'Orbit workspace',cfg['subtitle'],'3 updates',0)
    text(front,'View updates',67,112,12,p['accent'],'sans',anchor='left');arrow(front,190,112,p['accent'],.6)
    paste(scene,front,875,343+35*(1-e),e,scale=.94+.06*e)
    badge=layer(120,40);rr(badge,(0,0,119,39),p['accent'],20);text(badge,'3 NEW',60,20,12,p['bg'],'mono')
    paste(scene,badge,1085,268,enter(t,1.2,1.65),scale=.6+.4*pop(prog(t,1.2,1.65)))
    _exitgroup(out,scene,t)

def _n03(t,cfg,p,out):
    _copy(out,cfg,p,t,x=75,y=283,width=301,size=42)
    scene=layer();e=enter(t,.2,.9);header=enter(t,.72,1.14);typed=prog(t,1.2,2.95)
    card=_notify(p,740,194,'Aina · Creative team',cfg['subtitle'],'just now',1,typed,header,enter(t,.4,.9))
    # Fixed-size text field and accessory row never react to the revealed substring.
    rr(card,(66,138,267,172),rgba(p['accent'],20),11)
    text(card,'Review workspace',82,155,12,p['accent'],'sans',opacity=enter(t,3.0,3.4),anchor='left')
    arrow(card,246,155,p['accent'],.55)
    if 1.2<t<3.25 and int(t*3)%2==0:
        lines=_wrap(cfg['subtitle'],14,740-89,'sans',3);count=int(len(cfg['subtitle'])*typed)
        for i,s in enumerate(lines):
            if count<=len(s):
                x=66+measure(s[:count],14,'sans')+3;line(card,[(x,42+i*20),(x,57+i*20)],p['accent'],2);break
            count-=len(s)+1
    paste(scene,card,806,367+35*(1-e),e,scale=.97+.03*e)
    if cfg.get('_labels',True):text(scene,'01  CONTAINER     02  IDENTITY     03  MESSAGE',441,498,11,p['muted'],'mono',opacity=enter(t,.75,1.2),anchor='left')
    _exitgroup(out,scene,t)

def _n04(t,cfg,p,out):
    _copy(out,cfg,p,t,x=97,y=285,width=365,size=46)
    scene=layer();w,h=274,456;e=enter(t,.2,.95)
    phone=_phone_shell(w,h,p['accent'],p['panel'],p['bg'],p['text'],p['muted']).copy()
    screen=layer(w,h)
    text(screen,'09:41',w/2,87,40,p['text']);text(screen,'TUESDAY, 24 SEPTEMBER',w/2,121,9,p['muted'],'mono')
    for i,(title,msg) in enumerate([('Orbit','Your ideas are in sync.'),('Aina','The review is ready.'),('Workspace',cfg['subtitle'])]):
        q=enter(t,.8+i*.48,1.32+i*.48)
        small=_notify(p,238,68,title,msg,'now',i,1,1,1)
        paste(screen,small,w/2+30*(1-q),180+i*77,q)
    # Compact call banner is an independent timed child of the same screen mask.
    q=enter(t,2.7,3.15);banner=layer(236,52);rr(banner,(0,0,235,51),p['accent'],15)
    _avatar(banner,25,26,15,{'accent':p['bg'],'bg':p['accent']},'A')
    text(banner,'Aina is calling',47,18,11,p['bg'],anchor='left');text(banner,'Audio call · demo',47,35,9,p['bg'],'sans',anchor='left')
    circle(banner,207,26,14,p['bg']);line(banner,[(200,23),(202,29),(207,32),(213,28)],p['accent'],3)
    paste(screen,banner,w/2,389+50*(1-q),q)
    mask=Image.new('L',(w,h));ImageDraw.Draw(mask).rounded_rectangle((13,38,w-14,h-31),radius=22,fill=255)
    screen.putalpha(Image.fromarray(np.minimum(np.asarray(screen.getchannel('A')),np.asarray(mask)).astype('uint8')))
    phone.alpha_composite(screen)
    # All contents, rim, and screen mask undergo one common perspective transform.
    tex,x,y=_local_warp(phone,[(0,11),(274,0),(280,434),(10,456)])
    paste(scene,tex,845,379+35*(1-e),e,scale=.92+.035*math.sin(prog(t,1.,4.)*math.pi),angle=-1.5)
    _exitgroup(out,scene,t)

_DRAW={'U01':_u01,'U02':_u02,'U03':_u03,'U04':_u04,'N01':_n01,'N02':_n02,'N03':_n03,'N04':_n04}

def render(pid,t,cfg):
    cfg=_cfg(pid,cfg);p=palette(cfg);out=base(cfg);_DRAW[pid](float(t),cfg,p,out);return out
