"""Original typography choreography derived from inspected public previews.

Public reference footage and paid template assets are never bundled. Frames are
pure functions of time, so seeking and repeated renders produce identical pixels.
"""
from core import *
from PIL import ImageChops, ImageOps
from functools import lru_cache

R7='https://elements.envato.com/text-animation-R7E9UER'
QB='https://elements.envato.com/text-scene-QBTKNGF'
YZ='https://elements.envato.com/text-animation-YZHKP5W'

def _meta(name,description,text_value,subtitle,source,stamp,mechanism,**kw):
    d=dict(name=name,description=description,genre='creator',genres=['creator','promo','saas','education','corporate'],text=text_value,subtitle=subtitle,family='kinetic',source_url=source,observed_timestamp=stamp,mechanism=mechanism,variant_basis='observed')
    d.update(kw);return d

PRESETS={
 'K16':_meta('Mirror Floor Tracking Zoom','Teks mengembang dengan jarak huruf berubah dan pantulan lantai yang mengikut gerakan.','IDEA BESAR','BINA SESUATU YANG BERMAKNA',R7,'12.3–19.9 s','tracking expansion with mirrored floor and depth zoom',reflection=.30,tracking=28,zoom=.72),
 'K17':_meta('Mixed Weight Glyph Slingshot','Huruf berlainan ketebalan bergoyang secara individu sebelum tajuk meluncur sebagai satu kumpulan.','GERAK PANTAS','TENAGA DALAM SETIAP HURUF',R7,'7.75–11.9 s','mixed-weight glyph wobble with whole-group slingshot',wobble=14,stagger=.055,slingshot=150),
 'K18':_meta('Opposing Word Hinge','Dua baris huruf masuk berturutan, kemudian berengsel keluar dalam arah bertentangan.','KATA MENJADI\nCERITA','SUSUNAN YANG MENGHIDUPKAN MESEJ',R7,'25.0–30.4 s','two-row letter cascade with opposing word hinge exits',hinge_angle=62,stagger=.040,line_gap=34),
 'K19':_meta('Vertical Glyph Totem','Huruf dibina sebagai tiang menegak; setiap huruf jatuh keluar mengikut ritma tersendiri.','IDEA','SATU HURUF. SATU LANGKAH.',R7,'35.0–39.8 s','vertical glyph totem build and staggered fall',stagger=.09,fall_distance=180,column_gap=150),
 'K20':_meta('Punctuation Bounce Baseline','Ayat mendarat pada garis dasar; tanda baca melantun secara berasingan untuk memberi tekanan.','IDEA. AKSI!','TANDA KECIL, IMPAK BESAR',R7,'40.0–44.5 s','independent punctuation bounce above stable word baseline',bounce_height=55,punctuation_scale=1.25,stagger=.06),
 'K21':_meta('Chevron Light Gate','Chevron bercahaya membuka teks dengan topeng berterusan, kemudian memadamkannya ketika kembali.','BUKA KEMUNGKINAN','PERKATAAN TERBUKA, IDEA BERMULA',QB,'2.0–5.5 s','continuous chevron-led letter-slice reveal and delete',variant_basis='adapted',gate_width=28,glow=10,reveal_duration=.95),
 'K22':_meta('Perimeter Light Runner','Cahaya bergerak mengelilingi bingkai teks sementara ayat di tengah kekal jelas.','IDEA DI DALAM BINGKAI','CAHAYA YANG MEMBIMBING PERHATIAN',QB,'12.0–20.0 s','traveling luminous textbox perimeter',runner_speed=1.1,trail=.23,glow=9),
 'K23':_meta('Living Bullet Panel','Panel bertambah tinggi sebelum setiap baris masuk, dengan gerakan kecil pada kata pilihan.','Cipta idea baharu\nSusun mesej anda\nGerakkan cerita bersama','MESEJ TERSUSUN, CERITA HIDUP',QB,'21.8–27.2 s','staggered bulletbox growth with independent keyword wiggle',variant_basis='adapted',row_stagger=.28,keyword_index=1,wiggle=6,glow=8),
 'K24':_meta('Plus Anchor Assembly','Tanda tambah membesar; dua frasa berpusing dan berlabuh di sisinya.','IDEA + TINDAKAN','GABUNGKAN UNTUK MELANGKAH',QB,'29.0–33.0 s','oversized plus anchor with phrase rotation and docking',variant_basis='adapted',orbit=105,plus_size=62,glow=8),
 'K25':_meta('Luminous Media Caption','Bukaan media berkembang dan tajuk bercahaya berlabuh pada bahagian bawah bingkai.','CERITA DALAM GERAK','VISUAL YANG MEMBERI KONTEKS',QB,'36.0–45.0 s','media aperture with luminous lower-third and frame edge',asset='',aperture_duration=.90,glow=9,media_scale=1.0),
 'K26':_meta('Angled Border Circuit','Garis mengelilingi bingkai serong sebelum tajuk masuk pada satah yang sama.','GERAKKAN IDEA','BERMULA DENGAN SATU LANGKAH',YZ,'5.5–9.8 s','angled boundary-line circuit revealing a slanted title',slant=-.20,circuit_duration=1.0,line_width=5),
 'K27':_meta('Diagonal Divider Reveal','Garis serong membuka ruang antara dua perkataan yang muncul dari pusat.','FIKIR\nCIPTA','DUA TINDAKAN, SATU ARAH',YZ,'10.0–14.8 s','diagonal slash separating two masked word reveals',divider_slant=55,word_gap=100,divider_width=7),
 'K28':_meta('Slanted Row Unfold','Baris teks serong membuka satu persatu seperti engsel, kemudian melipat semula.','TERUS\nMELANGKAH\nKE HADAPAN','LANGKAH KECIL MENGUBAH CERITA',YZ,'15.0–19.8 s','slanted multirow hinged unfold and reverse collapse',slant=-.18,row_stagger=.17,fold_depth=.10),
 'K29':_meta('Staircase Word Assembly','Perkataan bergerak daripada lajur menegak kepada tangga lalu terkunci pada satu baris.','SATU IDEA BANYAK CARA','SUSUN UNTUK MENJADI JELAS',YZ,'30.0–34.8 s','word chunks moving vertical to staircase to one baseline',step_height=54,step_width=100,assembly_start=1.25),
 'K30':_meta('Inserted Keyword Lockup','Kata tengah disisipkan untuk menolak dua baris luar, kemudian susunan mengecil semula.','CIPTA\nLEBIH\nBERMAKNA','BERI RUANG KEPADA KATA UTAMA',YZ,'40.0–44.8 s','middle keyword insertion displacing outer rows',keyword_scale=1.10,row_spread=84,insertion_time=1.35),
}

def _number(cfg,key,default,lo,hi):
    try:v=float(cfg.get(key,default))
    except (ValueError,TypeError):v=default
    return clamp(v,lo,hi) if math.isfinite(v) else default

def _rows(s,n=2):
    """Balance complete words without losing any part of the supplied copy."""
    s=str(s); explicit=s.splitlines()
    if len(explicit)>1:return explicit
    words=s.split()
    if not words:return []
    if n<=1 or len(words)==1:return [' '.join(words)]
    n=min(n,len(words));result=[];pos=0
    for i in range(n):
        remaining=n-i
        if remaining==1:result.append(' '.join(words[pos:]));break
        target=sum(len(w)+1 for w in words[pos:])/remaining
        end=pos+1
        while end<len(words)-(remaining-1) and len(' '.join(words[pos:end+1]))<=target+2:end+=1
        result.append(' '.join(words[pos:end]));pos=end
    return result

def _row_size(rows,maxw=1040,size=92,maxh=270,gap=24):
    if not rows:return size
    return max(12,min(size,int((maxh-max(0,len(rows)-1)*gap)/max(1,len(rows))/.85),*(fit_size(s,maxw,size) for s in rows)))

def _track_sprite(s,size,color,tracking=0,face='bold'):
    if not s:return layer(1,1)
    f=font(size,face);adv=[f.getlength(c) for c in s];total=max(1,sum(adv)+tracking*max(0,len(s)-1));out=layer(total+12,size*1.5)
    x=6
    for c,w in zip(s,adv):text(out,c,x+w/2,out.height/2,size,color,face);x+=w+tracking
    return out

def _copy(cfg,p,y=572,t=2):
    s=cfg.get('subtitle','');v=life(t,.65,1.35,4.0,4.65)
    text(p[0],s,640,y,fit_size(s,1030,22),p[1]['muted'],opacity=v)

def _pulse(t,a,b):return math.sin(math.pi*prog(t,a,b)) if a<t<b else 0.

def _copy_block(value,color,width=440,size=65,maxh=160):
    rows=_rows(value,2 if len(value)>28 else 1);fs=_row_size(rows,width,size,maxh,10)
    sprites=[text_img(r,fs,color) for r in rows]
    if not sprites:return layer(1,1)
    ww=max(z.width for z in sprites);hh=sum(z.height for z in sprites)+10*(len(sprites)-1);block=layer(ww,hh);y=0
    for sprite in sprites:paste(block,sprite,ww/2,y+sprite.height/2);y+=sprite.height+10
    ratio=min(1,width/max(1,block.width),maxh/max(1,block.height))
    return block.resize((max(1,round(block.width*ratio)),max(1,round(block.height*ratio))),Image.Resampling.LANCZOS) if ratio<1 else block

def _k16(t,cfg,p,out):
    s=cfg.get('text','');rows=_rows(s,2 if len(s)>20 else 1);fs=_row_size(rows,1000,104,205,16)
    progress=ease(prog(t,.15,1.25));exitp=smooth(prog(t,4.12,4.9));v=prog(t,.12,.45)*(1-exitp)
    track=_number(cfg,'tracking',28,0,60)*(1-progress)+_number(cfg,'tracking',28,0,60)*exitp
    zoom=mix(_number(cfg,'zoom',.72,.3,1.4),1,progress)*(1-.26*exitp)
    reflect=_number(cfg,'reflection',.30,0,.7);height=len(rows)*(fs*.85+16)
    group=layer(1100,max(1,height+20))
    for i,row in enumerate(rows):
        sprite=_track_sprite(row,fs,p['text'],track)
        ratio=min(1,1080/max(1,sprite.width));sprite=sprite.resize((max(1,round(sprite.width*ratio)),max(1,round(sprite.height*ratio))),Image.Resampling.BICUBIC)
        paste(group,sprite,550,group.height/2+(i-(len(rows)-1)/2)*(fs*.85+16))
    main_y=320-group.height*.10;paste(out,group,640,main_y,v,zoom)
    flipped=ImageOps.flip(group);a=np.array(flipped.getchannel('A'),dtype=np.float32);a*=np.linspace(.9,0,flipped.height)[:,None]*reflect;flipped.putalpha(Image.fromarray(a.astype('uint8')))
    # Reflect the completed paragraph, not individual rows into their neighbours.
    reflect_h=max(1,round(group.height*.55));flipped=flipped.resize((flipped.width,reflect_h),Image.Resampling.BICUBIC)
    paste(out,flipped,640,main_y+group.height*zoom/2+reflect_h*zoom/2+8,v,zoom)
    floor_y=main_y+group.height*zoom/2+4
    line(out,[(220,floor_y),(1060,floor_y)],rgba(p['accent'],round(95*v)),2)
    _copy(cfg,(out,p),572,t)

def _k17(t,cfg,p,out):
    s=cfg.get('text','');rows=_rows(s,2 if len(s)>18 else 1);fs=_row_size(rows,990,105,260,35)
    stagger=_number(cfg,'stagger',.055,.008,.12);count=sum(len(r) for r in rows);stagger=min(stagger,.55/max(1,count));k=0
    depart=smooth(prog(t,4.05,4.88));kick=_number(cfg,'slingshot',150,0,240)
    groupx=640+kick*(_pulse(t,3.80,4.22)*-.3+depart)
    wobble=_number(cfg,'wobble',14,0,30)
    for r,row in enumerate(rows):
        widths=[measure(c,fs,'bold' if i%3 else 'sans') for i,c in enumerate(row)];x=groupx-sum(widths)/2;y=365+(r-(len(rows)-1)/2)*(fs*.95+35)
        for i,(c,w) in enumerate(zip(row,widths)):
            q=prog(t,.13+k*stagger,.83+k*stagger);settle=pop(q);k+=1
            dy=math.sin((t-.13)*16+i*.73)*wobble*(1-q)**2
            rot=math.sin(t*12+i)*9*(1-q)
            face='bold' if i%3 else 'sans'
            text(out,c,x+w/2,y+(1-settle)*90+dy-depart*30,fs,p['accent'] if i%3==0 else p['text'],face,opacity=clamp(q*3)*(1-depart),angle=rot)
            x+=w
    _copy(cfg,(out,p),572,t)

def _k18(t,cfg,p,out):
    rows=_rows(cfg.get('text',''),2);gap=_number(cfg,'line_gap',34,10,60);fs=_row_size(rows,1010,94,260,gap)
    stagger=min(_number(cfg,'stagger',.04,.005,.12),.48/max(1,sum(map(len,rows))));k=0
    for i,row in enumerate(rows):
        rowlay=layer(1100,max(110,fs*1.6));widths=[measure(c,fs) for c in row];x=(1100-sum(widths))/2
        for c,w in zip(row,widths):
            q=prog(t,.16+k*stagger,.83+k*stagger);k+=1
            text(rowlay,c,x+w/2,rowlay.height/2+(1-pop(q))*55,fs,p['accent'] if i%2 else p['text'],opacity=clamp(q*3));x+=w
        leaveq=smooth(prog(t,4.02+i*.10,4.74+i*.10));sign=-1 if i%2==0 else 1
        # Shrink first, then hinge outside the inter-row gap to avoid collisions.
        y=350+(i-(len(rows)-1)/2)*(fs*.95+gap)+sign*leaveq*40
        paste(out,rowlay,640+sign*leaveq*105,y,1-leaveq,scale=1-.68*math.sqrt(leaveq),angle=sign*_number(cfg,'hinge_angle',62,15,90)*leaveq**2)
    _copy(cfg,(out,p),574,t)

def _k19(t,cfg,p,out):
    words=cfg.get('text','').split();chars=[list(w) for w in words] or []
    # Long copy uses additional columns with bounded height, preserving all glyphs.
    columns=[]
    for ch in chars:
        columns.extend(ch[i:i+7] for i in range(0,len(ch),7))
    if not columns:_copy(cfg,(out,p),584,t);return
    gap=min(_number(cfg,'column_gap',150,50,240),1020/max(1,len(columns)));fs=min(62,320/max(map(len,columns))*.82,gap*.78);fs=max(12,int(fs));k=0
    delay=min(_number(cfg,'stagger',.09,.005,.16),.6/max(1,sum(map(len,columns))))
    for j,col in enumerate(columns):
        h=len(col)*fs*1.12;top=355-h/2
        for i,c in enumerate(col):
            q=prog(t,.15+k*delay,.78+k*delay);ex=prog(t,4.03+k*delay*.65,4.50+k*delay*.65);k+=1
            y=top+(i+.5)*fs*1.12+(1-pop(q))*-65+ease(ex)*_number(cfg,'fall_distance',180,60,240)
            x=640+(j-(len(columns)-1)/2)*gap
            text(out,c,x,y,fs,p['accent'] if i%3==0 else p['text'],opacity=clamp(q*4)*(1-ex),angle=ex*(i%2*2-1)*35)
    _copy(cfg,(out,p),584,t)

def _k20(t,cfg,p,out):
    rows=_rows(cfg.get('text',''),2 if len(cfg.get('text',''))>23 else 1);fs=_row_size(rows,1000,96,245,35);k=0
    delay=min(_number(cfg,'stagger',.06,.005,.12),.55/max(1,sum(map(len,rows))));end=smooth(prog(t,4.12,4.9))
    for r,row in enumerate(rows):
        sizes=[int(fs*_number(cfg,'punctuation_scale',1.25,.8,1.8)) if c in '.,!?;:' else fs for c in row];widths=[measure(c,z) for c,z in zip(row,sizes)];ratio=min(1,1030/max(1,sum(widths)));widths=[w*ratio for w in widths];x=640-sum(widths)/2
        for c,z,w in zip(row,sizes,widths):
            q=prog(t,.14+k*delay,.72+k*delay);k+=1;punct=c in '.,!?;:'
            bounce=abs(math.sin((t-1.35)*9))*math.exp(-(t-1.35)*2.1) if punct and 1.35<t<3.2 else 0
            dy=-bounce*_number(cfg,'bounce_height',55,0,100)
            y=345+(r-(len(rows)-1)/2)*(fs*.95+35)+(1-pop(q))*65+dy+end*70
            text(out,c,x+w/2,y,int(z*ratio),p['accent'] if punct else p['text'],opacity=clamp(q*3)*(1-end));x+=w
    _copy(cfg,(out,p),574,t)

@lru_cache(maxsize=128)
def _glow_text(s,size,color,radius=8,face='bold'):
    crisp=text_img(s,size,color,face);pad=max(12,int(radius*3));canvas=layer(crisp.width+pad*2,crisp.height+pad*2)
    paste(canvas,crisp,canvas.width/2,canvas.height/2)
    soft=canvas.filter(ImageFilter.GaussianBlur(radius));soft.alpha_composite(canvas);return soft

def _glow_layer(out,strokes,radius):
    if radius>0:out.alpha_composite(strokes.filter(ImageFilter.GaussianBlur(radius)))
    out.alpha_composite(strokes)

def _path_piece(dst,pts,start,end,color,width=3):
    segments=[];length=0
    for a,b in zip(pts,pts[1:]):
        ll=math.hypot(b[0]-a[0],b[1]-a[1]);segments.append((a,b,length,ll));length+=ll
    lo=clamp(start)*length;hi=clamp(end)*length
    for a,b,offset,ll in segments:
        if ll<=0:continue
        q0=clamp((lo-offset)/ll);q1=clamp((hi-offset)/ll)
        if q1>q0:line(dst,[(mix(a[0],b[0],q0),mix(a[1],b[1],q0)),(mix(a[0],b[0],q1),mix(a[1],b[1],q1))],color,width)

def _k21(t,cfg,p,out):
    s=cfg.get('text','');rows=_rows(s,2 if len(s)>23 else 1);fs=_row_size(rows,955,91,230,25)
    content=layer();top=360-(len(rows)-1)*(fs*.95+25)/2
    rad=_number(cfg,'glow',10,0,18)
    for i,row in enumerate(rows):paste(content,_glow_text(row,fs,p['text'],round(rad)),640,top+i*(fs*.95+25))
    q=ease(prog(t,.2,.2+_number(cfg,'reveal_duration',.95,.35,1.8)));ex=smooth(prog(t,4.12,4.84));extent=q*(1-ex)
    left=120;right=1160;gate=mix(left,right,extent);visible=content.crop((left,170,max(left+1,round(gate)),520));out.alpha_composite(visible,(left,170))
    v=life(t,.05,.30,4.7,4.98);gw=_number(cfg,'gate_width',28,10,65);strokes=layer()
    line(strokes,[(gate-gw,270),(gate+gw*.20,350),(gate-gw,430)],rgba(p['accent'],round(v*255)),6)
    _glow_layer(out,strokes,rad);_copy(cfg,(out,p),574,t)

def _k22(t,cfg,p,out):
    rows=_rows(cfg.get('text',''),2);fs=_row_size(rows,910,78,210,22);v=life(t,.15,.95,4.1,4.9)
    bounds=[(155,224),(1125,224),(1125,482),(155,482),(155,224)];strokes=layer()
    _path_piece(strokes,bounds,0,ease(prog(t,.12,1.12))*(1-leave(t)),rgba(p['accent'],round(95*v)),3)
    head=((t*.31*_number(cfg,'runner_speed',1.1,.2,3))%1);tail=_number(cfg,'trail',.23,.04,.48)
    for i in range(12):
        seghead=(head-tail*i/12)%1;segstart=seghead-tail/12
        a=round(v*(1-i/12)**1.4*255)
        if segstart<0:_path_piece(strokes,bounds,segstart+1,1,rgba(p['accent'],a),6);segstart=0
        _path_piece(strokes,bounds,segstart,seghead,rgba(p['accent'],a),6)
    _glow_layer(out,strokes,_number(cfg,'glow',9,0,18))
    for i,row in enumerate(rows):text(out,row,640,352+(i-(len(rows)-1)/2)*(fs*.9+22),fs,p['text'],opacity=v,scale=mix(.95,1,ease(prog(t,.3,1.0))))
    _copy(cfg,(out,p),574,t)

def _k23(t,cfg,p,out):
    rows=_rows(cfg.get('text',''),3);n=max(1,len(rows));fs=_row_size(rows,860,49,265,20);gap=min(91,300/n);stagger=_number(cfg,'row_stagger',.28,.08,.48);stagger=min(stagger,.8/n)
    top=216;bottom=top+min(320,n*gap+30);e=smooth(prog(t,4.48,4.94));boxq=ease(prog(t,.08,.64))*(1-e)
    # Every row receives its full card height before its own lettering begins.
    h=0
    for i in range(n):h+=gap*ease(prog(t,.05+i*stagger,.36+i*stagger))
    h=min(bottom-top,max(0,h+30*boxq))*(1-e);strokes=layer()
    if h>1:rr(strokes,(165,top,1115,top+h),rgba(p['panel'],round(245*boxq)),18,rgba(p['accent'],round(190*boxq)),2)
    _glow_layer(out,strokes,_number(cfg,'glow',8,0,16))
    for i,row in enumerate(rows):
        q=ease(prog(t,.40+i*stagger,.95+i*stagger));texit=smooth(prog(t,3.97+(n-1-i)*.07,4.31+(n-1-i)*.07));v=q*(1-texit);y=top+35+gap*(i+.35)
        circle(out,213,y,5*max(.02,pop(prog(t,.33+i*stagger,.70+i*stagger))),rgba(p['accent'],round(255*v)))
        words=row.split();x=249;idx=int(_number(cfg,'keyword_index',1,0,50))
        for j,w in enumerate(words):
            ww=measure(w,fs);motion=_pulse(t,1.7+i*.20,2.6+i*.20)*math.sin(t*17+i)*_number(cfg,'wiggle',6,0,15) if j==idx else 0
            text(out,w,x+ww/2,y+20*(1-q)+motion,fs,p['accent'] if j==idx else p['text'],opacity=v,angle=motion*.30);x+=ww+measure(' ',fs)
    _copy(cfg,(out,p),594,t)

def _k24(t,cfg,p,out):
    s=cfg.get('text','');parts=[v.strip() for v in s.split('+',1)] if '+' in s else _rows(s,2)
    if len(parts)==1:parts.append('')
    parts=parts[:2] if parts else ['',''];fs=_row_size(parts,420,71,200);q=pop(prog(t,.12,.9));ex=smooth(prog(t,4.08,4.9));v=prog(t,.1,.4)*(1-ex)
    plus=layer(200,200);d=ImageDraw.Draw(plus);length=_number(cfg,'plus_size',62,28,96);d.rounded_rectangle((100-length,92,100+length,108),radius=5,fill=p['accent']);d.rounded_rectangle((92,100-length,108,100+length),radius=5,fill=p['accent'])
    rad=_number(cfg,'glow',8,0,18);soft=plus.filter(ImageFilter.GaussianBlur(rad));soft.alpha_composite(plus);paste(out,soft,640,350,v,max(.001,q*(1-.5*ex)),angle=-90*(1-q)+ex*90)
    orb=_number(cfg,'orbit',105,0,170)
    for i,part in enumerate(parts):
        z=ease(prog(t,.3+i*.1,1.26+i*.1));sign=-1 if i==0 else 1;theta=math.radians(sign*orb*(1-z+ex));r=300
        x=640+sign*r*math.cos(theta);y=350+sign*r*.42*math.sin(theta)
        if len(part)>28:paste(out,_copy_block(part,p['text'],420,71,160),x,y,clamp(z*2)*(1-ex),angle=sign*55*(1-z+ex))
        else:text(out,part,x,y,fs,p['text'],opacity=clamp(z*2)*(1-ex),angle=sign*55*(1-z+ex))
    _copy(cfg,(out,p),574,t)

@lru_cache(maxsize=24)
def _media(asset,accent,secondary,panel_color):
    if asset:
        with Image.open(asset) as src:return ImageOps.fit(src.convert('RGBA'),(900,330),Image.Resampling.LANCZOS)
    # Geometric original artwork is a fallback only; supplied media replaces it.
    im=layer(900,330);d=ImageDraw.Draw(im);d.rectangle((0,0,900,330),fill=panel_color)
    for i in range(6):
        d.polygon([(i*190-150,330),(i*190+50,0),(i*190+132,0),(i*190-68,330)],fill=rgba(accent,34+i*15))
    d.ellipse((570,-60,900,270),fill=secondary);d.ellipse((645,5,825,185),fill=panel_color)
    d.polygon([(0,330),(260,160),(520,330)],fill=accent);d.polygon([(170,330),(360,215),(540,330)],fill=secondary)
    return im

def _k25(t,cfg,p,out):
    q=ease(prog(t,.12,.12+_number(cfg,'aperture_duration',.9,.4,1.5)));ex=smooth(prog(t,4.10,4.92));v=prog(t,.1,.40)*(1-ex);media=_media(str(cfg.get('asset','')),p['accent'],p['secondary'],p['panel']);zoom=_number(cfg,'media_scale',1,.8,1.3)
    if zoom!=1:media=ImageOps.fit(media.resize((round(media.width*zoom),round(media.height*zoom)),Image.Resampling.BICUBIC),(900,330),Image.Resampling.BICUBIC)
    half=round(450*q*(1-ex));crop=media.crop((450-half,0,450+half,330)) if half else layer(1,1);paste(out,crop,640,349,v)
    strokes=layer();left=640-half;right=640+half
    if half:rr(strokes,(left,184,right,514),None,4,rgba(p['accent'],round(210*v)),3)
    _glow_layer(out,strokes,_number(cfg,'glow',9,0,18))
    title=cfg.get('text','');fs=fit_size(title,820,53);cq=life(t,.55,1.2,4.02,4.75)
    rr(out,(197,433,1083,507),rgba(p['bg'],round(226*cq)),4)
    if len(title)>55:
        paste(out,_copy_block(title,p['text'],820,36,62),640,470+20*(1-cq),cq)
    else:paste(out,_glow_text(title,fs,p['text'],round(_number(cfg,'glow',9,0,18)*.5)),640,470+20*(1-cq),cq)
    _copy(cfg,(out,p),574,t)

def _slanted(sprite,shear):
    pad=round(abs(shear)*sprite.height)+3;offset=pad if shear<0 else 0
    return sprite.transform((sprite.width+pad,sprite.height),Image.Transform.AFFINE,(1,-shear,-offset,0,1,0),Image.Resampling.BICUBIC)

def _k26(t,cfg,p,out):
    v=life(t,.12,.7,4.18,4.94);q=ease(prog(t,.12,.12+_number(cfg,'circuit_duration',1,.4,1.6)));ex=leave(t);shear=_number(cfg,'slant',-.20,-.4,.4)
    shift=shear*240;pts=[(175-shift/2,230),(1105-shift/2,230),(1105+shift/2,470),(175+shift/2,470),(175-shift/2,230)]
    strokes=layer();_path_piece(strokes,pts,0,q*(1-ex),rgba(p['accent'],round(240*v)),round(_number(cfg,'line_width',5,2,12)));out.alpha_composite(strokes)
    rows=_rows(cfg.get('text',''),2 if len(cfg.get('text',''))>23 else 1);fs=_row_size(rows,810,90,195,17)
    for i,row in enumerate(rows):
        z=ease(prog(t,.45+i*.12,1.16+i*.12));sprite=_slanted(text_img(row,fs,p['text']),shear)
        y=350+(i-(len(rows)-1)/2)*(fs*.92+17)
        paste(out,sprite,640-75*(1-z)+ex*90,y,clamp(z*2)*(1-ex))
    _copy(cfg,(out,p),574,t)

def _k27(t,cfg,p,out):
    parts=_rows(cfg.get('text','').replace('/','\n'),2);parts=(parts+['',''])[:2];gap=_number(cfg,'word_gap',100,50,170);fs=_row_size(parts,470-gap*.30,90,230);q=ease(prog(t,.2,1.18));ex=smooth(prog(t,4.12,4.9));v=prog(t,.12,.45)*(1-ex)
    slant=_number(cfg,'divider_slant',55,15,105);h=115*q*(1-ex)
    line(out,[(640+slant*q,355-h),(640-slant*q,355+h)],rgba(p['accent'],round(255*v)),round(_number(cfg,'divider_width',7,2,16)))
    for i,part in enumerate(parts):
        sign=-1 if i==0 else 1;sp=_copy_block(part,p['text'],470-gap*.30,90,220) if len(part)>28 else text_img(part,fs,p['text']);x=640+sign*(gap/2+sp.width/2)
        tmp=layer();paste(tmp,sp,x-sign*(1-q)*130+sign*ex*120,355,clamp(q*3)*(1-ex))
        box=(110,190,round(640-gap/2),520) if i==0 else (round(640+gap/2),190,1170,520)
        out.alpha_composite(tmp.crop(box),box[:2])
    _copy(cfg,(out,p),574,t)

def _k28(t,cfg,p,out):
    rows=_rows(cfg.get('text',''),3);fs=_row_size(rows,1020,86,310,22);st=min(_number(cfg,'row_stagger',.17,.04,.3),.60/max(1,len(rows)));shear=_number(cfg,'slant',-.18,-.4,.4);depth=_number(cfg,'fold_depth',.10,.015,.35)
    for i,row in enumerate(rows):
        q=ease(prog(t,.15+i*st,.86+i*st));ex=smooth(prog(t,4.08+(len(rows)-1-i)*st*.7,4.61+(len(rows)-1-i)*st*.7));opening=q*(1-ex);sp=_slanted(text_img(row,fs,p['text'] if i%2==0 else p['accent']),shear)
        scale_y=max(.01,mix(depth,1,opening));sp=sp.resize((sp.width,max(1,round(sp.height*scale_y))),Image.Resampling.BICUBIC)
        y=345+(i-(len(rows)-1)/2)*(fs*.94+22);paste(out,sp,640+shear*(y-345),y+(1-opening)*20,clamp(opening*3),angle=(1-opening)*(-6 if i%2 else 6))
    _copy(cfg,(out,p),584,t)

def _k29(t,cfg,p,out):
    words=cfg.get('text','').split();n=len(words)
    if not n:_copy(cfg,(out,p),578,t);return
    # Many-word copy groups into at most six complete chunks, preserving the text.
    if n>6:words=_rows(' '.join(words),6);n=len(words)
    fs=min(67,round(940/max(1,measure(' '.join(words),67))*67));wrap=fs<17;mid=(n+1)//2
    groups=[list(range(mid)),list(range(mid,n))] if wrap else [list(range(n))]
    if wrap:fs=min(40,int(940/max(1,max(measure(' '.join(words[i] for i in g),40) for g in groups))*40))
    fs=max(10,fs);widths=[measure(w,fs) for w in words];spaces=measure(' ',fs);targets=[None]*n;targetys=[345]*n
    for gi,g in enumerate(groups):
        total=sum(widths[i] for i in g)+spaces*(len(g)-1);cursor=640-total/2
        for i in g:targets[i]=cursor+widths[i]/2;targetys[i]=345+(gi-(len(groups)-1)/2)*(fs*1.25+12);cursor+=widths[i]+spaces
    q=ease(prog(t,.15,.75));a=_number(cfg,'assembly_start',1.25,.8,2.3);stairs=ease(prog(t,.62,a));lock=ease(prog(t,a,a+.75));rev=smooth(prog(t,4.04,4.84));v=prog(t,.12,.4)*(1-rev)
    sh=min(_number(cfg,'step_height',54,20,80),285/max(1,n-1));sw=min(_number(cfg,'step_width',100,40,180),600/max(1,n-1))
    for i,(word,w) in enumerate(zip(words,widths)):
        j=i-(n-1)/2;coly=345+j*sh;stairx=640+j*sw;verticalx=640
        x=mix(mix(verticalx,stairx,stairs),targets[i],lock);y=mix(coly,targetys[i],lock)
        x=mix(x,stairx,rev);y=mix(y,coly,rev)+45*(1-q)
        text(out,word,x,y,fs,p['accent'] if i%2 else p['text'],opacity=v,angle=(1-q)*(-8 if i%2 else 8))
    _copy(cfg,(out,p),578,t)

def _k30(t,cfg,p,out):
    rows=_rows(cfg.get('text',''),3)
    if not rows:_copy(cfg,(out,p),582,t);return
    if len(rows)==1:rows=['',rows[0],'']
    elif len(rows)==2:rows=[rows[0],'',rows[1]]
    elif len(rows)>3:rows=[rows[0],' '.join(rows[1:-1]),rows[-1]]
    fs=_row_size(rows,1010,90,290,22);start=_number(cfg,'insertion_time',1.35,.9,2.2);insert=pop(prog(t,start,start+.63));ex=smooth(prog(t,4.02,4.84));v=life(t,.14,.85,4.10,4.9);spread=_number(cfg,'row_spread',84,55,115)
    pos=insert*(1-ex);basegap=fs*.45
    for i in (0,2):
        sign=-1 if i==0 else 1;y=350+sign*(basegap+spread*pos)
        text(out,rows[i],640,y,fs,p['text'],opacity=v,scale=mix(.9,1,ease(prog(t,.15,.85))))
    if rows[1]:
        scale=_number(cfg,'keyword_scale',1.1,.8,1.4);ks=fit_size(rows[1],1020,round(fs*scale));q=clamp(insert)* (1-ex)
        text(out,rows[1],640,350,ks,p['accent'],opacity=clamp(q*3),scale=max(.01,.65+.35*pos))
    _copy(cfg,(out,p),582,t)

_DRAW={f'K{i}':globals()[f'_k{i}'] for i in range(16,31)}

def render(pid,t,cfg):
    im=base(cfg)
    if t<=0 or t>=5:return im
    p=palette(cfg);out=layer();_DRAW[pid](float(t),cfg,p,out)
    # Keep object motion clear of catalogue headings and the progress legend.
    im.alpha_composite(out.crop((0,150,W,621)),(0,150))
    return im
