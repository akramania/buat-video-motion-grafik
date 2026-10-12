"""Fifteen original kinetic typography studies from public preview observations.

All glyph positioning uses one Latin baseline (including descenders). Time is
normalised to 0..5 seconds; source timestamps describe observations, not copies.
"""
from core import *
from PIL import ImageChops


def _meta(name,description,source,stamp,mechanism,basis='observed',**kw):
    return dict(name=name,description=description,genre='creator',
                genres=['creator','promo','saas','education','corporate'],
                family='kinetic',source_url='https://elements.envato.com/'+source,
                source_product=source.rsplit('-',1)[-1],observed_timestamp=stamp,
                mechanism=mechanism,variant_basis=basis,**kw)


PRESETS={
 'K31':_meta('Tracking Frame Assembly','Jarak huruf mengembang, dua jalur menyapu dan bingkai membesar mengikut tajuk.',
   'text-animation-N8UXUU6','0.30–1.35 s','tracking expansion + paired ribbons + growing frame',
   text='IDEA JADI NYATA',subtitle='SEMUANYA BERMULA DI SINI',tracking_max=24,frame_padding=36,
   ribbon_text='CIPTA',ribbon_secondary='GERAK'),
 'K32':_meta('Skew Baseline Extrusion','Tajuk naik dari satah condong dengan lapisan kedalaman dan garis sokongan berlawanan arah.',
   'text-animation-N8UXUU6','4.85–5.90 s','slanted baseline + graded extrusion + counter-moving underline',
   text='GERAK KE HADAPAN',subtitle='BINA SESUATU YANG BERMAKNA',depth=18,tilt=0.18,support_text='PERSPEKTIF'),
 'K33':_meta('Elastic Leading Accordion','Tiga baris merapat dan membuka ruang menegak dengan huruf kekal pada saiz yang sama.',
   'text-animation-N8UXUU6','8.00–9.05 s','three-line leading compression and elastic separation','adapted',
   text='SATU IDEA\nBANYAK CARA\nHASIL BERMAKNA',subtitle='RUANG MEMBENTUK RITMA',leading_amplitude=35,line_gap=24),
 'K34':_meta('Leading Block Reflow','Blok warna membuka tajuk pertama, kemudian dua baris lain berpindah ke susunan akhir.',
   'text-animation-N8UXUU6','14.60–16.00 s','leading block travels and opens, following rows relocate',
   text='LANGKAH PERTAMA\nBUKA PELUANG\nCIPTA PERUBAHAN',subtitle='MULA DENGAN SATU TINDAKAN',block_width=46,row_stagger=.16),
 'K35':_meta('Split Caption Aperture','Bingkai bermula sebagai celah nipis sebelum dua pengatup terbuka dan mendedahkan tajuk.',
   'text-animation-N8UXUU6','20.50–21.55 s','central frame expansion + opposed solid shutter reveal',
   text='BUKA PERSPEKTIF',subtitle='LIHAT DENGAN CARA BAHARU',aperture_height=152,shutter_delay=.22,band_text='IDEA DALAM GERAK'),
 'K36':_meta('Live Typeset Pill','Kotak kapsul mengukur setiap huruf yang ditaip dan membesar bersama teks.',
   'text-animation-7NXC4GG','8.20–9.40 s','measured pill width grows with typed glyphs',
   text='Jadikan idea lebih jelas',subtitle='KOTAK MENGIKUT PANJANG TEKS',padding=30),
 'K37':_meta('Travelling Glyph Glow','Cahaya pendek mengikuti hadapan taip, kemudian semua huruf kekal tajam untuk dibaca.',
   'text-animation-7NXC4GG','5.90–6.90 s','glow trails the typing front, not a scanner over a complete phrase',
   text='Gerakkan setiap idea',subtitle='CAHAYA MENGIKUT HURUF BAHARU',glow_trail=3),
 'K38':_meta('Icon Cursor Handoff','Kursor mengikuti huruf yang sedang ditaip dan bertukar bentuk pada hentian perkataan.',
   'text-animation-7NXC4GG','11.40–12.80 s; 16.00–17.40 s','typing cursor follows the measured text and hands off between icons',
   text='Dari idea kepada aksi',subtitle='SATU GERAKAN PADA SATU MASA',cursor_sequence=['circle','square','plus']),
 'K39':_meta('Live Wrap Story','Teks ditaip mengikut ukuran sebenar, membalut baris dan menatal dalam tetingkap bacaan.',
   'text-animation-7NXC4GG','8.20–9.40 s; 17.85–18.30 s','measured multiline wrapping and scrolling during typing','adapted',
   text='Idea yang baik bermula dengan satu langkah. Beri ruang untuk mencuba, belajar dan membina sesuatu yang bermakna bersama.',
   subtitle='CERITA BERGERAK DALAM TETINGKAP',font_size=40,wrap_width=760,visible_lines=3),
 'K40':_meta('Contour to Ink','Empat suku kontur setiap huruf berkumpul terlebih dahulu sebelum isi huruf mengunci.',
   'text-animation-7NXC4GG','0.35–1.55 s','separate contour quadrants per glyph assemble, then resolve to ink','adapted',
   text='Bentuk jadi makna',subtitle='EMPAT BAHAGIAN, SATU BENTUK',segment_distance=28),
 'K41':_meta('Counter-Sliding Strips','Dua jalur teks negatif meluncur bertentangan sebelum berlabuh dalam susunan akhir.',
   'text-animation-TQ2SPTQ','0.20–1.60 s','two negative-text bands counter-slide and dock',
   text='GERAKKAN IDEA\nCIPTA IMPAK',subtitle='JELAS DALAM SETIAP GERAK',band_gap=22),
 'K42':_meta('Offset Quote Reveal','Dua kumpulan baris menyapu dari arah berlawanan bersama garisan dan atribusi.',
   'text-animation-TQ2SPTQ','6.00–7.40 s','opposed line group sweep + line tracers + attribution',
   text='Idea kecil hari ini\nPerubahan besar esok',subtitle='CATATAN KREATIF',quote_offset=72),
 'K43':_meta('Badge Docking','Lencana bergerak ke kiri untuk memberi ruang kepada label dua baris di sebelah kanan.',
   'text-animation-TQ2SPTQ','9.60–12.20 s','badge moves left, freeing room for two-row right label',
   text='BELAJAR\nDAN BERKEMBANG',subtitle='SENTIASA ADA LANGKAH SETERUSNYA',support_text='IDEA',badge_size=126),
 'K44':_meta('Bracket Window Sweep','Kurungan membuka tetingkap sementara tajuk dan subjudul menyapu di dalam kawasan klip.',
   'text-animation-TQ2SPTQ','17.00–18.75 s','brackets open while title and subtitle sweep within a clipped window',
   text='RUANG UNTUK IDEA',subtitle='PANDANGAN BAHARU BERMULA DI SINI',window_subtitle='BERFIKIR. MENCUBA. MENCIPTA.',bracket_width=32),
 'K45':_meta('Polarity Token','Token bulat dilukis mengikut kontur, diisi sapuan terbalik dan diikuti frasa sokongan.',
   'text-animation-TQ2SPTQ','21.60–23.00 s','traced rounded token + inverse fill wipe + trailing phrase',
   text='MULA',subtitle='SATU LANGKAH PUN BERMAKNA',support_text='DENGAN IDEA ANDA',token_padding=28),
}


def _num(cfg,key,default,lo,hi):
    try: v=float(cfg.get(key,default))
    except (ValueError,TypeError):v=default
    return max(lo,min(hi,v)) if math.isfinite(v) else default


def _copy(cfg):return str(cfg.get('text','')).strip()


def _rows(s,n=3):
    explicit=[r.strip() for r in s.splitlines() if r.strip()]
    if len(explicit)>1:return explicit[:n]
    words=s.split()
    if not words:return ['']
    n=min(n,len(words));rows=[]
    for i in range(n):rows.append(' '.join(words[round(i*len(words)/n):round((i+1)*len(words)/n)]))
    return rows


def _fs(rows,maxw=1040,size=75):
    return max(12,min(size,min((fit_size(r,maxw,size) for r in rows),default=size)))


@lru_cache(maxsize=4096)
def _glyph(c,fs,color,face='bold'):
    f=font(fs,face);box=f.getbbox(c,anchor='ls')
    im=layer(max(1,box[2]-box[0]+4),max(1,box[3]-box[1]+4))
    ImageDraw.Draw(im).text((2-box[0],2-box[1]),c,font=f,anchor='ls',fill=color)
    return im,box


def _letter(dst,c,x,baseline,fs,color,opacity=1,dx=0,dy=0,angle=0,scale=1):
    if c.isspace() or opacity<=0:return
    src,box=_glyph(c,int(fs),color)
    # Alignment is based on the font baseline, never each glyph's ink centre.
    cx=x+(box[0]+box[2])/2+dx;cy=baseline+(box[1]+box[3])/2+dy
    paste(dst,src,cx,cy,opacity,scale,angle)


def _row(dst,s,cx,baseline,fs,color,opacity=1,tracking=0,animate=None):
    f=font(fs);width=f.getlength(s)+max(0,len(s)-1)*tracking
    left=cx-width/2
    for i,c in enumerate(s):
        # Prefix widths preserve the font's kerning and a common baseline.
        x=left+f.getlength(s[:i])+i*tracking
        opts=animate(i,c,x) if animate else {}
        opts=dict(opts or {});alpha=opts.pop('opacity',1)
        _letter(dst,c,x,baseline,fs,opts.pop('color',color),opacity*alpha,**opts)
    return width


def _subtitle(dst,cfg,p,t,y=560):
    sub=str(cfg.get('subtitle',''))
    text(dst,sub,640,y,fit_size(sub,1030,23,'sans'),p['muted'],'sans',opacity=life(t,.8,1.45,4.08,4.64))


def _start(cfg,t):
    im=base(cfg);p=palette(cfg)
    return im,p,life(t,.12,.5,4.35,4.9)


def _k31(t,cfg):
    im,p,a=_start(cfg,t);s=_copy(cfg).replace('\n',' ');fs=_fs([s],950,76)
    en=pop(prog(t,.20,1.22));out=smooth(prog(t,4.08,4.85));v=clamp(en)*(1-out)
    tr=_num(cfg,'tracking_max',24,0,60)*(1-clamp(en))
    natural=measure(s,fs);pad=_num(cfg,'frame_padding',36,15,70)
    width=min(1110,natural+2*pad);framew=max(2,width*v)
    top,bottom=286,431
    if a:
        rr(im,(640-framew/2,top,640+framew/2,bottom),(0,0,0,0),0,rgba(p['accent'],220*a),2)
        for i,y in enumerate([top-18,bottom+18]):
            r=ease(prog(t,.14+i*.12,.66+i*.12))*(1-out)
            length=width*.65*r;x=640+(-1 if i else 1)*width*(1-r)*.26
            rr(im,(x-length/2,y-4,x+length/2,y+4),rgba(p['secondary' if i else 'accent'],230*a),0)
        for i,key in enumerate(['ribbon_text','ribbon_secondary']):
            label=str(cfg.get(key,''));ly=240 if i==0 else 489
            text(im,label,640,ly,18,p['secondary' if i else 'accent'],'mono',opacity=a*v)
    scale=min(1,1060/max(1,natural+max(0,len(s)-1)*tr))
    stage=layer();_row(stage,s,640,388,fs,p['text'],a,tracking=tr,
          animate=lambda i,c,x:dict(dy=28*(1-clamp(en))-34*out))
    if scale<.998:paste(im,stage,640,360,scale=scale)
    else:im.alpha_composite(stage)
    _subtitle(im,cfg,p,t);return im


def _k32(t,cfg):
    im,p,a=_start(cfg,t);s=_copy(cfg).replace('\n',' ');fs=_fs([s],1000,82)
    en=ease(prog(t,.14,1.28));out=smooth(prog(t,4.08,4.85))
    depth=_num(cfg,'depth',18,2,38);slant=_num(cfg,'tilt',.18,-.35,.35)
    stage=layer()
    for d in range(round(depth),0,-3):
        color=tuple(round(mix(v,40,d/max(1,depth)*.55)) for v in rgb(p['secondary']))
        _row(stage,s,640+d*.65,390+d*.65,fs,color,a*.6,
             animate=lambda i,c,x:dict(dy=(1-enter(t,.15+i*.025,.70+i*.025))*56-70*out))
    _row(stage,s,640,390,fs,p['text'],a,
         animate=lambda i,c,x:dict(dy=(1-enter(t,.15+i*.025,.70+i*.025))*56-70*out))
    skew=slant*(1-.65*en)+out*slant
    # One affine plane keeps letters registered while the camera-like skew settles.
    stage=stage.transform((W,H),Image.Transform.AFFINE,(1,-skew,skew*360,0,1,0),Image.Resampling.BICUBIC)
    im.alpha_composite(stage)
    w=min(1020,measure(s,fs)+40);u=ease(prog(t,.32,1.12))*(1-out)
    line(im,[(640+w/2-w*u,445),(640+w/2,445)],rgba(p['accent'],240*a),5)
    support=str(cfg.get('support_text',''))
    text(im,support,640-90*(1-u),251,fit_size(support,970,20,'mono'),p['secondary'],'mono',opacity=a*u)
    _subtitle(im,cfg,p,t);return im


def _k33(t,cfg):
    im,p,a=_start(cfg,t);rows=_rows(_copy(cfg));fs=_fs(rows,1050,66)
    en=prog(t,.2,1.55);out=smooth(prog(t,4.06,4.85))
    amp=_num(cfg,'leading_amplitude',35,8,65);gap=fs+_num(cfg,'line_gap',24,8,42)
    bounce=math.sin(en*math.pi*3)*(1-en)**2*amp if en<1 else 0
    gap=(gap*(.3+.7*ease(en))+bounce)*(1-.65*out)
    centre=(len(rows)-1)/2
    for i,s in enumerate(rows):
        y=381+(i-centre)*gap
        _row(im,s,640,y,fs,p['accent'] if i==1 else p['text'],a,
             animate=lambda j,c,x:dict(dx=(1-ease(en))*25*(-1 if i%2 else 1)))
    _subtitle(im,cfg,p,t,585);return im


def _k34(t,cfg):
    im,p,a=_start(cfg,t);rows=_rows(_copy(cfg));fs=_fs(rows,990,63)
    stag=_num(cfg,'row_stagger',.16,.05,.35);bw=_num(cfg,'block_width',46,20,95)
    out=smooth(prog(t,4.1,4.88));ys=[304+i*92 for i in range(len(rows))]
    en=ease(prog(t,.14,.90));barx=mix(126,1090,en)
    for i,s in enumerate(rows):
        e=enter(t,.22+i*stag,1.1+i*stag)
        x=640+(-1 if i%2 else 1)*120*(1-e)+out*120
        y=ys[i]-48*(1-e)
        _row(im,s,x,y,fs,p['text'] if i else p['accent'],a*e)
    if .1<t<1.45:
        fade=1-smooth(prog(t,.92,1.45))
        rr(im,(barx-bw/2,224,barx+bw/2,324),rgba(p['accent'],255*a*fade),3)
    led=ease(prog(t,.34,1.05))*(1-out)
    line(im,[(130,528),(130+1020*led,528)],rgba(p['secondary'],160*a),3)
    _subtitle(im,cfg,p,t,578);return im


def _k35(t,cfg):
    im,p,a=_start(cfg,t);s=_copy(cfg).replace('\n',' ');fs=_fs([s],955,75)
    height=_num(cfg,'aperture_height',152,110,225);delay=_num(cfg,'shutter_delay',.22,0,.55)
    out=smooth(prog(t,4.05,4.85));frame=ease(prog(t,.12,.70))*(1-out)
    reveal=ease(prog(t,.3+delay,1.35+delay))*(1-out)
    width=min(1110,max(540,measure(s,fs)+90));left=640-width/2;right=640+width/2
    top=365-height*frame/2;bottom=365+height*frame/2
    panel=layer();_row(panel,s,640,392,fs,p['text'],a)
    mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rectangle((left,top,right,bottom),fill=255)
    panel.putalpha(ImageChops.multiply(panel.getchannel('A'),mask));im.alpha_composite(panel)
    if a:
        shutter=width*.5*(1-reveal)
        if shutter>0:
            rr(im,(left,top,left+shutter,bottom),rgba(p['accent'],255*a),0)
            rr(im,(right-shutter,top,right,bottom),rgba(p['secondary'],255*a),0)
        rr(im,(left,top,right,bottom),(0,0,0,0),0,rgba(p['accent'],240*a),3)
    text(im,str(cfg.get('band_text','')),640,249,20,p['accent'],'mono',opacity=a*reveal)
    _subtitle(im,cfg,p,t);return im


def _typed(s,t,start=.35,end=2.65):
    return s[:min(len(s),int(len(s)*prog(t,start,end)+1e-7))]


def _k36(t,cfg):
    im,p,a=_start(cfg,t);s=_copy(cfg).replace('\n',' ');fs=_fs([s],960,65)
    shown=_typed(s,t);pad=_num(cfg,'padding',30,12,65)
    full=measure(s,fs);width=max(38,measure(shown,fs))+2*pad
    left=640-(full+2*pad)/2;baseline=392;out=leave(t)
    v=life(t,.14,.55,4.18,4.87)
    if v:
        rr(im,(left,baseline-fs-14,left+width,baseline+24),rgba(p['accent'],255*v),32)
        _row(im,shown,left+pad+measure(shown,fs)/2,baseline,fs,p['bg'],v)
        if t<2.7:
            x=left+pad+measure(shown,fs)+5
            line(im,[(x,baseline-fs*.75),(x,baseline+3)],rgba(p['bg'],220*v),3)
    _subtitle(im,cfg,p,t);return im


@lru_cache(maxsize=512)
def _glow_glyph(c,fs,color):
    src,box=_glyph(c,fs,color);pad=22;im=layer(src.width+2*pad,src.height+2*pad)
    im.alpha_composite(src,(pad,pad));blur=im.filter(ImageFilter.GaussianBlur(8))
    blur.alpha_composite(im);return blur,box


def _k37(t,cfg):
    im,p,a=_start(cfg,t);s=_copy(cfg).replace('\n',' ');fs=_fs([s],1030,69)
    shown=_typed(s,t,.32,2.55);trail=int(_num(cfg,'glow_trail',3,1,9));f=font(fs)
    left=640-f.getlength(s)/2;baseline=389;out=leave(t)
    for i,c in enumerate(shown):
        x=left+f.getlength(s[:i]);age=len(shown)-i-1
        if age<trail and t<2.65 and not c.isspace():
            src,box=_glow_glyph(c,fs,p['accent'])
            paste(im,src,x+(box[0]+box[2])/2,baseline+(box[1]+box[3])/2,
                  opacity=a*(1-age/(trail+1)))
        _letter(im,c,x,baseline-35*out,fs,p['text'],a)
    line(im,[(135,453),(1145,453)],rgba(p['muted'],70*a),1)
    _subtitle(im,cfg,p,t);return im


def _icon(dst,kind,x,y,size,col,alpha):
    r=size/2
    if kind=='square':rr(dst,(x-r,y-r,x+r,y+r),rgba(col,255*alpha),3)
    elif kind=='plus':
        line(dst,[(x-r,y),(x+r,y)],rgba(col,255*alpha),4)
        line(dst,[(x,y-r),(x,y+r)],rgba(col,255*alpha),4)
    else:circle(dst,x,y,r,rgba(col,255*alpha))


def _k38(t,cfg):
    im,p,a=_start(cfg,t);s=_copy(cfg).replace('\n',' ');fs=_fs([s],940,68)
    shown=_typed(s,t,.40,2.75);f=font(fs);left=640-(f.getlength(s)+62)/2
    baseline=391;_row(im,shown,left+f.getlength(shown)/2,baseline,fs,p['text'],a)
    seq=cfg.get('cursor_sequence',['circle','square','plus'])
    if not isinstance(seq,list) or not seq:seq=['circle','square','plus']
    seq=[str(v) for v in seq];word_index=shown.count(' ')
    kind=seq[word_index%len(seq)]
    pulse=1+.15*math.sin(t*11)*(1-prog(t,2.65,2.95))
    x=left+f.getlength(shown)+31
    _icon(im,kind,x,baseline-fs*.34,24*pulse,p['accent'],a)
    _subtitle(im,cfg,p,t);return im


def _wrap(s,fs,width):
    rows=[]
    for para in s.split('\n'):
        row=''
        for c in para:
            if row and measure(row+c,fs)>width:
                split=row.rfind(' ')
                if split>0:
                    rows.append(row[:split]);row=row[split+1:]+c
                else:rows.append(row);row=c
            else:row+=c
        rows.append(row)
    return rows or ['']


def _k39(t,cfg):
    im,p,a=_start(cfg,t);s=_copy(cfg)
    fs=int(_num(cfg,'font_size',40,24,64));ww=_num(cfg,'wrap_width',760,420,1030)
    visible=int(_num(cfg,'visible_lines',3,2,5));leading=fs*1.42
    # Maintain a bounded reading window inside the atlas title/footer margins.
    if visible*leading>310:fs=int(310/visible/1.42);leading=fs*1.42
    shown=_typed(s,t,.32,3.24);rows=_wrap(shown,fs,ww);count=len(rows)
    top=232;bottom=top+visible*leading+24;left=640-ww/2
    rr(im,(left-26,top-30,left+ww+26,bottom+16),rgba(p['panel'],245*a),18,
       rgba(p['accent'],130*a),1)
    stage=layer();scroll=max(0,count-visible)
    for i,srow in enumerate(rows):
        baseline=top+fs+(i-scroll)*leading
        _row(stage,srow,left+measure(srow,fs)/2,baseline,fs,p['text'],a)
    mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rectangle((left-3,top-2,left+ww+3,bottom),fill=255)
    stage.putalpha(ImageChops.multiply(stage.getchannel('A'),mask));im.alpha_composite(stage)
    total=max(1,len(_wrap(s,fs,ww)));progress=count/total
    line(im,[(left,bottom+37),(left+ww*clamp(progress),bottom+37)],rgba(p['accent'],190*a),3)
    _subtitle(im,cfg,p,t,596);return im


@lru_cache(maxsize=512)
def _contour(c,fs,color):
    src,box=_glyph(c,fs,color);mask=src.getchannel('A')
    ring=ImageChops.subtract(mask.filter(ImageFilter.MaxFilter(5)),mask.filter(ImageFilter.MinFilter(3)))
    out=Image.new('RGBA',src.size,color);out.putalpha(ring);return out,box


def _k40(t,cfg):
    im,p,a=_start(cfg,t);s=_copy(cfg).replace('\n',' ');fs=_fs([s],1010,80)
    f=font(fs);left=640-f.getlength(s)/2;baseline=394
    dist=_num(cfg,'segment_distance',28,8,70);out=leave(t)
    for i,c in enumerate(s):
        if c.isspace():continue
        x=left+f.getlength(s[:i]);src,box=_contour(c,fs,p['accent'])
        en=ease(prog(t,.15+i*.018,1.18+i*.018));fill=ease(prog(t,1.20+i*.018,1.75+i*.018))
        w,h=src.size;mx=w//2;my=h//2
        for q,(region,sx,sy) in enumerate([((0,0,mx,my),-1,-1),((mx,0,w,my),1,-1),((0,my,mx,h),-1,1),((mx,my,w,h),1,1)]):
            piece=src.crop(region);cx=x+box[0]-2+(region[0]+region[2])/2
            cy=baseline+box[1]-2+(region[1]+region[3])/2
            paste(im,piece,cx+sx*dist*(1-en+out),cy+sy*dist*(1-en+out),a*(1-.85*fill))
        _letter(im,c,x,baseline,fs,p['text'],a*fill)
    _subtitle(im,cfg,p,t);return im


def _k41(t,cfg):
    im,p,a=_start(cfg,t);rows=_rows(_copy(cfg),2);fs=_fs(rows,915,68)
    gap=_num(cfg,'band_gap',22,8,45);height=fs+40;total=len(rows)*height+(len(rows)-1)*gap
    for i,s in enumerate(rows):
        en=pop(prog(t,.18+i*.17,1.18+i*.17));out=leave(t,4.05+i*.12,4.80+i*.08)
        direction=-1 if i%2==0 else 1;x=640+direction*450*(1-en+out)
        y=365-total/2+height/2+i*(height+gap);w=measure(s,fs)+72
        stage=layer();rr(stage,(x-w/2,y-height/2,x+w/2,y+height/2),rgba(p['accent'] if i==0 else p['secondary'],255*a),3)
        _row(stage,s,x,y+fs*.35,fs,p['bg'],a)
        im.alpha_composite(stage)
    _subtitle(im,cfg,p,t,570);return im


def _k42(t,cfg):
    im,p,a=_start(cfg,t);rows=_rows(_copy(cfg),2);fs=_fs(rows,960,62)
    offset=_num(cfg,'quote_offset',72,20,110);stage=layer();out=leave(t)
    for i,s in enumerate(rows):
        en=enter(t,.18+i*.19,1.17+i*.19);direction=-1 if i%2==0 else 1
        baseline=340+i*105
        _row(stage,s,640+direction*(offset*(1-en)+120*out),baseline,fs,
             p['text'] if i==0 else p['accent'],a*en)
        w=measure(s,fs);tr=ease(prog(t,.2+i*.12,1.12+i*.12))*(1-out)
        left=640-w/2;right=640+w/2
        pts=[(left,baseline+24),(left+w*tr,baseline+24)] if i==0 else [(right-w*tr,baseline+24),(right,baseline+24)]
        line(stage,pts,rgba(p['secondary'],170*a),2)
    mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rectangle((110,230,1170,494),fill=255)
    stage.putalpha(ImageChops.multiply(stage.getchannel('A'),mask));im.alpha_composite(stage)
    text(im,'“',121,269,65,p['accent'],'serif',opacity=a)
    _subtitle(im,cfg,p,t,558);return im


def _k43(t,cfg):
    im,p,a=_start(cfg,t);rows=_rows(_copy(cfg),2);fs=_fs(rows,680,56)
    badge=_num(cfg,'badge_size',126,96,164);dock=ease(prog(t,.58,1.60));out=leave(t)
    bx=mix(640,234,dock)+out*80;by=360
    circle(im,bx,by,badge/2,rgba(p['accent'],255*a))
    support=str(cfg.get('support_text',''))
    text(im,support,bx,by,fit_size(support,badge-26,28),p['bg'],opacity=a)
    stage=layer()
    for i,s in enumerate(rows):
        en=enter(t,.95+i*.15,1.75+i*.15);baseline=344+i*86
        _row(stage,s,775+50*(1-en),baseline,fs,p['text'] if i==0 else p['secondary'],a*en)
    mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rectangle((338,240,1165,491),fill=255)
    stage.putalpha(ImageChops.multiply(stage.getchannel('A'),mask));im.alpha_composite(stage)
    _subtitle(im,cfg,p,t);return im


def _k44(t,cfg):
    im,p,a=_start(cfg,t);s=_copy(cfg).replace('\n',' ');fs=_fs([s],925,66)
    en=ease(prog(t,.13,.93));out=leave(t);width=1060*en*(1-out)
    left=640-width/2;right=640+width/2;top,bottom=261,476;cap=_num(cfg,'bracket_width',32,14,70)
    if width>2:
        cap=min(cap,width/2)
        line(im,[(left+cap,top),(left,top),(left,bottom),(left+cap,bottom)],rgba(p['accent'],240*a),4)
        line(im,[(right-cap,top),(right,top),(right,bottom),(right-cap,bottom)],rgba(p['accent'],240*a),4)
    stage=layer();e=enter(t,.40,1.42)
    _row(stage,s,640-180*(1-e)+100*out,362,fs,p['text'],a*e)
    sub=str(cfg.get('window_subtitle',''))
    text(stage,sub,640+130*(1-e)-80*out,428,fit_size(sub,900,23,'sans'),p['secondary'],'sans',opacity=a*e)
    mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rectangle((left+5,top+5,right-5 if right-left>10 else left+5,bottom-5),fill=255)
    stage.putalpha(ImageChops.multiply(stage.getchannel('A'),mask));im.alpha_composite(stage)
    _subtitle(im,cfg,p,t,565);return im


def _rounded_path(x0,y0,x1,y1,r):
    points=[]
    for cx,cy,start in [(x1-r,y0+r,-90),(x1-r,y1-r,0),(x0+r,y1-r,90),(x0+r,y0+r,180)]:
        for j in range(13):
            theta=math.radians(start+j*90/12);points.append((cx+r*math.cos(theta),cy+r*math.sin(theta)))
    points.append(points[0]);return points


def _k45(t,cfg):
    im,p,a=_start(cfg,t);s=_copy(cfg).replace('\n',' ');support=str(cfg.get('support_text',''))
    fs=_fs([s],380,60);sfs=fit_size(support,575,40);pad=_num(cfg,'token_padding',28,12,50)
    tokenw=measure(s,fs)+2*pad;sw=measure(support,sfs);gap=35
    total=tokenw+gap+sw;left=640-total/2;top,bottom=303,416;right=left+tokenw
    traced=ease(prog(t,.12,.94));out=leave(t);wipe=ease(prog(t,.82,1.75))*(1-out)
    path=_rounded_path(left,top,right,bottom,32);num=max(2,round(len(path)*traced))
    if a:line(im,path[:num],rgba(p['accent'],255*a),3)
    fill=layer();rr(fill,(left,top,right,bottom),rgba(p['accent'],255*a),32)
    mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rectangle((left,top,left+tokenw*wipe,bottom),fill=255)
    fill.putalpha(ImageChops.multiply(fill.getchannel('A'),mask));im.alpha_composite(fill)
    _row(im,s,left+tokenw/2,382,fs,p['accent'],a)
    ink=layer();_row(ink,s,left+tokenw/2,382,fs,p['bg'],a)
    ink.putalpha(ImageChops.multiply(ink.getchannel('A'),mask));im.alpha_composite(ink)
    en=enter(t,1.0,1.85)
    _row(im,support,right+gap+sw/2+44*(1-en),377,sfs,p['text'],a*en)
    _subtitle(im,cfg,p,t);return im


def render(pid,t,cfg):
    if t<=0 or t>=5:return base(cfg)
    return globals()['_k'+pid[1:]](float(t),cfg)
