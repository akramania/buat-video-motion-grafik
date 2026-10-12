"""T, X and H families: original, frame-deterministic typography recipes.

The display coordinates are 1280 x 720. The CLI owns output scaling and timing.
All positions are measured with the same font used for painting. User text can
replace the defaults; one-line treatments shrink to fit and phrases wrap into
stable slots before animation starts. Caption cues here are demonstration cues,
not automatically aligned to a voice track.
"""
from core import *
import unicodedata

PRESETS = {
 'T01': dict(name='Perkataan melalui mask', description='Setiap perkataan naik di dalam mask tetap, kemudian keluar mengikut turutan.', genre='education', genres=['education','corporate','saas'], text='IDEA BESAR BERMULA DI SINI', subtitle='Beri setiap perkataan ruang untuk bernafas.'),
 'T02': dict(name='Huruf menetap ke baseline', description='Glyph berputar dari anchor sendiri sebelum berhenti pada baseline yang sama.', genre='creator', genres=['creator','promo','education'], text='BERANI CIPTA', subtitle='Satu huruf. Satu gerakan. Satu mesej.'),
 'T03': dict(name='Taip, padam, ganti', description='State typing, pause, deleting dan replacement dengan caret berasingan.', genre='saas', genres=['saas','education','creator'], text='IDEA MENJADI NYATA', subtitle='Tulis semula kemungkinan anda.'),
 'T04': dict(name='Frasa mengikut beat', description='Baris dibina pada cue berasingan dalam slot akhir yang stabil.', genre='corporate', genres=['corporate','education','documentary'], text='FIKIR. CIPTA. GERAK.', subtitle='Susun cerita dengan rentak yang jelas.'),
 'X01': dict(name='Kata besar dan echo', description='Lattice bergerak perlahan dengan satu perkataan tajam sebagai fokus.', genre='promo', genres=['promo','creator'], text='CIPTA', subtitle='Besar pada idea. Jelas pada mesej.'),
 'X02': dict(name='Bar wipe dan underline', description='Bar mendedahkan tajuk, berubah menjadi underline, lalu ditarik keluar.', genre='education', genres=['education','promo','corporate'], text='MULA SEKARANG', subtitle='Aksen yang mengarah pandangan.'),
 'X03': dict(name='Gelombang outline dan fill', description='Outline kekal dalam slot tetap sementara isi warna bergerak merentasi glyph.', genre='creator', genres=['creator','promo','saas'], text='BERGERAK', subtitle='Ritma warna tanpa mengubah kedudukan.'),
 'X04': dict(name='Blur, warna dan glow', description='Pinggir warna dan blur mengecil kepada teks tajam sebelum exit berlapis.', genre='promo', genres=['promo','creator','saas'], text='LEBIH JELAS', subtitle='Tenaga pada transisi. Fokus ketika membaca.'),
 'H01': dict(name='Caption dengan kata aktif', description='Cue demo memberi satu perkataan warna dan skala aktif pada satu masa.', genre='creator', genres=['creator','education','documentary'], text='BUAT VIDEO YANG DIINGATI', subtitle='Cue demo • selaraskan dengan voice-over sebenar'),
 'H02': dict(name='Penanda kata kunci', description='Pill yang diukur bergerak antara kata dan menetap dengan padding konsisten.', genre='creator', genres=['creator','education','promo'], text='IDEA HEBAT BERMULA DI SINI', subtitle='Arahkan mata kepada kata yang penting.'),
 'H03': dict(name='Hook bersama ikon', description='Ikon menyokong frasa dengan orbit kecil dan kemunculan berturutan.', genre='saas', genres=['saas','creator','education'], text='SATU IDEA BANYAK CARA', subtitle='Ikon mengikuti cerita, bukan mengganggunya.'),
 'H04': dict(name='Angka besar dan punch', description='Counter terkunci pada nilai sasaran, dengan punch skala dan frasa sokongan.', genre='promo', genres=['promo','corporate','education'], text='SATU CERITA.', subtitle='Nilai demonstrasi • gantikan dengan data sebenar'),
}


@lru_cache(maxsize=256)
def graphemes(s):
    """Join combining marks, variation selectors and ZWJ chains (Latin demos)."""
    units=[]
    for ch in s:
        if units and (unicodedata.combining(ch) or ch in '\ufe0e\ufe0f\u200d' or units[-1].endswith('\u200d')):
            units[-1]+=ch
        else: units.append(ch)
    return tuple(units)


def words_layout(s, max_width=1060, size=76, max_lines=2, gap_ratio=.29):
    """Return fixed left x, line y and measured width per word before painting."""
    words=str(s).split() or [' ']
    for fs in range(size,19,-1):
        gap=fs*gap_ratio; pairs=[(word,measure(word,fs)) for word in words]
        total=sum(w for _,w in pairs)+gap*(len(pairs)-1)
        if total>max_width and max_lines==2 and len(pairs)>1:
            # Balance a two-line phrase instead of leaving an orphan final word.
            candidates=[]
            for split in range(1,len(pairs)):
                wa=sum(w for _,w in pairs[:split])+gap*(split-1)
                wb=sum(w for _,w in pairs[split:])+gap*(len(pairs)-split-1)
                candidates.append((max(wa,wb)>max_width,abs(wa-wb),split,wa,wb))
            _,_,split,wa,wb=min(candidates)
            lines=[pairs[:split],pairs[split:]];widths=[wa,wb]
        else:
            lines=[[]]; widths=[0.]
            for word,ww in pairs:
                if lines[-1] and widths[-1]+gap+ww>max_width:
                    lines.append([]);widths.append(0.)
                if lines[-1]:widths[-1]+=gap
                lines[-1].append((word,ww));widths[-1]+=ww
        if len(lines)<=max_lines and max(widths)<=max_width:break
    layout=[];line_height=fs*1.35
    for j,(row,ww) in enumerate(zip(lines,widths)):
        x=640-ww/2
        for word,w in row:
            layout.append((word,x,j*line_height,w,j));x+=w+gap
    return fs,layout,(len(lines)-1)*line_height


def support(dst,cfg,p,y=550,opacity=1):
    s=str(cfg.get('subtitle',''))
    if s:text(dst,s,640,y,fit_size(s,1050,23,'sans'),p['muted'],'sans',opacity=opacity)


def footer_rule(dst,p,t,y=505,width=80):
    k=enter(t,.55,1.3)*(1-leave(t,4.1,4.65))
    if k>0:line(dst,[(640-width*k/2,y),(640+width*k/2,y)],rgba(p['accent'],round(255*k)),3)


def group(dst,content,t,mode='up'):
    q=leave(t)
    x=640-65*q if mode=='left' else 640
    y=360-35*q if mode=='up' else 360+45*q if mode=='down' else 360
    paste(dst,content,x,y,1-q)


def masked_words(t,cfg,p):
    out=layer();fs,slots,span=words_layout(cfg['text'],size=76,max_lines=2)
    center=345;offset=center-span/2
    n=len(slots)
    for i,(word,x,dy,w,row) in enumerate(slots):
        start=.17+i*min(.085,.5/max(1,n-1))
        exit_step=min(.025,.15/max(1,n-1))
        a=enter(t,start,start+.54);q=leave(t,4.15+i*exit_step,4.68+i*exit_step)
        # The local mask never moves. Its child does.
        im=text_img(word,fs,p['accent'] if i==max(0,n-2) else p['text'])
        cell=layer(w+12,fs*1.6)
        paste(cell,im,3+im.width/2,cell.height/2+(1-a)*fs-q*fs,a*(1-q))
        cell=crop_reveal(cell,a)
        paste(out,cell,x-3,offset+dy,anchor='left')
    footer_rule(out,p,t);support(out,cfg,p,opacity=life(t,.65,1.25))
    return out


def rotate_glyphs(t,cfg,p):
    out=layer();s=str(cfg['text']);fs=fit_size(s,1080,103)
    f=font(fs);units=graphemes(s);x=640-measure(s,fs)/2
    step=min(.025,.35/max(1,len(units)-1));exit_step=min(.014,.18/max(1,len(units)-1))
    for i,g in enumerate(units):
        adv=f.getlength(g);a=pop(prog(t,.15+i*step,.72+i*step));alpha=clamp(a)
        q=leave(t,4.15+i*exit_step,4.62+i*exit_step)
        if not g.isspace():
            # The font's baseline anchor preserves ascenders and descenders.
            slot=glyph_slot(g,fs,p['accent'] if i%4==0 else p['text'])
            ang=(1-a)*(-32 if i%2 else 32)+q*(18 if i%2 else -18)
            paste(out,slot,x+adv/2,370+(1-a)*70-q*52,alpha*(1-q),angle=ang)
        x+=adv
    footer_rule(out,p,t,480);support(out,cfg,p,530,life(t,.75,1.25))
    return out


def typewriter(t,cfg,p):
    out=layer();target=str(cfg['text']);draft=str(cfg.get('draft','MULA'))
    units=graphemes(target);initial=graphemes(draft)
    if t<1.15:shown=''.join(initial[:int(len(initial)*prog(t,.32,1.))])
    elif t<1.45:shown=draft
    elif t<1.78:shown=''.join(initial[:len(initial)-int(len(initial)*prog(t,1.45,1.76))])
    else:shown=''.join(units[:int(len(units)*prog(t,1.8,3.08))])
    fs=fit_size(max([target,draft],key=len),1020,73,'mono')
    left=640-max(measure(target,fs,'mono'),measure(draft,fs,'mono'))/2
    a=enter(t,.15,.65);q=leave(t)
    rr(out,(86,242,1194,465),p['panel'],24,rgba(p['muted'],55))
    tag(out,'TEXTO / LIVE',112,272,p)
    line(out,[(112,307),(1168,307)],rgba(p['muted'],40),1)
    text(out,shown,left,365,fs,p['text'],'mono',anchor='left')
    caret_x=left+measure(shown,fs,'mono')+7
    cursor_on=t<3.08 or math.sin(t*math.pi*3)>-.2
    if cursor_on and t<4.18:
        style=cfg.get('caret','vertical')
        if style=='underscore':line(out,[(caret_x,399),(caret_x+fs*.55,399)],p['accent'],4)
        elif style=='bracket':line(out,[(caret_x+12,330),(caret_x,330),(caret_x,399),(caret_x+12,399)],p['accent'],3)
        else:rr(out,(caret_x,329,caret_x+4,399),p['accent'],2)
    support(out,cfg,p,535)
    framed=layer();paste(framed,out,640,360+(1-a)*22,a*(1-q),scale=mix(.975,1,a)*(1-q*.03))
    return framed


def beat_lines(t,cfg,p):
    out=layer();words=str(cfg['text']).split()
    if len(words)<=3:rows=words
    else:
        m=max(1,math.ceil(len(words)/3));rows=[' '.join(words[i:i+m]) for i in range(0,len(words),m)]
    rows=rows[:3] or [''];fs=min(90,*(fit_size(s,990,90) for s in rows));spacing=112
    y=340-(len(rows)-1)*spacing/2
    for i,s in enumerate(rows):
        a=enter(t,.18+i*.39,.72+i*.39);q=leave(t,4.1+i*.07,4.61+i*.07)
        yy=y+i*spacing
        text(out,s,640+(1-a)*80-q*100,yy,fs,p['accent'] if i==1 else p['text'],opacity=a*(1-q),scale=1+(1-a)*.09)
        # The index is a quiet beat cue; it shares the row's timing.
        text(out,f'0{i+1}',110,yy,18,p['muted'],'mono',opacity=a*(1-q))
        line(out,[(153,yy+36),(153+50*a,yy+36)],rgba(p['accent'],round(180*a*(1-q))),2)
    support(out,cfg,p,570,life(t,1.05,1.5))
    return out


def lattice(t,cfg,p):
    out=layer();a=enter(t,.15,.95);q=leave(t);s=str(cfg['text'])
    fs=fit_size(s,950,152);echo_size=max(30,int(fs*.83));ww=measure(s,echo_size)+70
    field=layer(1280,460)
    for row,yy in enumerate([38,138,246,360,452]):
        drift=(t*27+(1-a)*145)*(1 if row%2 else -1)
        for col in range(-2,4):
            xx=640+col*ww+drift%ww-ww/2
            text(field,s,xx,yy,echo_size,p['muted'],opacity=.12*a,stroke=1,stroke_color=p['muted'])
    paste(out,field,640,380)
    slab=layer(1120,150);rr(slab,(0,0,1120,150),p['bg'],4)
    paste(out,slab,640,353,opacity=.9*a)
    text(out,s,640,351,fs,p['accent'],opacity=a,scale=mix(1.22,1,pop(prog(t,.18,1.1))))
    # Framing brackets separate the primary word from decorative echoes.
    for x,sgn in [(92,1),(1188,-1)]:
        line(out,[(x+sgn*28,290),(x,290),(x,414),(x+sgn*28,414)],rgba(p['accent'],round(a*180)),3)
    support(out,cfg,p,565,a)
    result=layer();paste(result,out,640-q*90,360,1-q,scale=1+q*.1)
    return result


def bar_underline(t,cfg,p):
    out=layer();s=str(cfg['text']);fs=fit_size(s,1050,88);im=text_img(s,fs,p['text']);w=im.width
    a=enter(t,.16,.94);q=leave(t);left=640-w/2
    revealed=crop_reveal(im,a,'left');paste(out,revealed,640,350)
    # A moving, measured bar leads the wipe, then compresses to a rule.
    if t<1.12:
        bar_x=left+w*a;bh=mix(im.height+24,5,prog(t,.78,1.12));bw=mix(15,w,prog(t,.94,1.12))
        bx=mix(bar_x,640,prog(t,.94,1.12));by=mix(350,409,prog(t,.78,1.12))
        rr(out,(bx-bw/2,by-bh/2,bx+bw/2,by+bh/2),rgba(p['accent'],round(255*enter(t,.15,.32))),2)
    else:
        reveal=1-leave(t,4.07,4.57);pts=[]
        for i in range(101):
            u=i/100
            if u>reveal:break
            amp=4*math.sin(math.pi*prog(t,1.12,4.1))
            pts.append((left+w*u,409+amp*math.sin(u*math.pi*4-t*2.3)))
        if len(pts)>1:line(out,pts,p['accent'],5)
    support(out,cfg,p,530,life(t,.6,1.2))
    result=layer();paste(result,out,640,360-q*32,1-q)
    return result


@lru_cache(maxsize=2048)
def glyph_slot(s,size,color,outline=False):
    f=font(size);im=layer(measure(s,size)+16,size*1.6)
    ImageDraw.Draw(im).text((8,size),s,font=f,anchor='ls',fill=(0,0,0,0) if outline else color,
                           stroke_width=2 if outline else 0,stroke_fill=color)
    return im


def outline_wave(t,cfg,p):
    out=layer();s=str(cfg['text']);fs=fit_size(s,1080,140);units=graphemes(s);full=measure(s,fs)
    x=640-full/2;a=enter(t,.2,.9);q=leave(t);n=len(units)
    for i,g in enumerate(units):
        adv=measure(g,fs)
        if not g.isspace():
            start=.15+i*min(.022,.35/max(1,n-1));entry=enter(t,start,start+.57)
            outline=glyph_slot(g,fs,p['accent'],True)
            fill=glyph_slot(g,fs,p['text'] if i%2 else p['accent'])
            active=clamp(1-abs((t-1.05)*max(2,n/1.35)-i)/2.1)
            final=enter(t,2.9,3.5)
            opacity=max(active,final)
            yy=355+(1-entry)*36
            paste(out,outline,x+adv/2,yy,entry*(1-q)*.8)
            paste(out,fill,x+adv/2,yy,opacity*entry*(1-q))
        x+=adv
    # One swept light marks the direction of the weight/fill wave.
    xx=640-full/2+full*prog(t,1.,3.25)
    if 1<t<3.25:circle(out,xx,458,3,p['accent'])
    support(out,cfg,p,530,life(t,.7,1.2))
    return out


@lru_cache(maxsize=256)
def blurred_text(s,fs,color,radius):
    im=text_img(s,fs,color);pad=36;out=layer(im.width+pad*2,im.height+pad*2);paste(out,im,out.width/2,out.height/2)
    return out.filter(ImageFilter.GaussianBlur(radius)) if radius else out


def chromatic(t,cfg,p):
    out=layer();s=str(cfg['text']);fs=fit_size(s,1080,105)
    a=enter(t,.15,1.13);q=leave(t);energy=max(1-a,q);alpha=a*(1-q)
    shift=24*energy;blur=round(8*energy)
    # Coarse radius steps are restricted to transient underlayers; hero stays sharp.
    glow=blurred_text(s,fs,p['accent'],12)
    paste(out,glow,640,350,alpha*(.10+.28*energy))
    paste(out,blurred_text(s,fs,p['accent'],blur),640-shift,350+4*energy,alpha*.6*energy)
    paste(out,blurred_text(s,fs,p['secondary'],blur),640+shift,350-4*energy,alpha*.6*energy)
    paste(out,blurred_text(s,fs,p['text'],max(0,blur-2)),640,350+(1-a)*25-q*20,alpha,scale=1+energy*.035)
    rr(out,(600,460,680,463),rgba(p['accent'],round(alpha*220)),2)
    support(out,cfg,p,530,life(t,.8,1.25))
    return out


def active_caption(t,cfg,p):
    out=layer();fs,slots,span=words_layout(cfg['text'],1010,81,2);top=340-span/2
    a=enter(t,.17,.72);q=leave(t);n=len(slots)
    index=min(n-1,max(0,int((t-.8)/max(.35,2.8/n))))
    cue_start=.8+index*max(.35,2.8/n)
    pulse=math.sin(math.pi*prog(t,cue_start,cue_start+.24))*.05 if t<cue_start+.24 else 0
    # Safe-area guides frame the caption block, not an imagined speaker's face.
    for xx,sgn in [(100,1),(1180,-1)]:
        line(out,[(xx+sgn*22,220),(xx,220),(xx,470),(xx+sgn*22,470)],rgba(p['muted'],round(65*a*(1-q))),2)
    for i,(word,x,dy,w,row) in enumerate(slots):
        active=i==index;entry=enter(t,.16+i*.03,.66+i*.03)
        text(out,word,x+w/2,top+dy+(1-entry)*25,fs,p['accent'] if active else p['text'],opacity=entry*(1-q),scale=1+pulse if active else 1)
        if active:rr(out,(x,top+dy+fs*.62,x+w,top+dy+fs*.62+4),rgba(p['accent'],round(a*(1-q)*230)),2)
    # A small cue track makes this demo's cue-based nature clear.
    for i in range(n):circle(out,640+(i-(n-1)/2)*18,502,3,rgba(p['accent'] if i==index else p['muted'],round(255*a*(1-q))))
    support(out,cfg,p,560,a*(1-q))
    return out


def keyword_pill(t,cfg,p):
    out=layer();fs,slots,span=words_layout(cfg['text'],1000,77,2);top=344-span/2
    a=enter(t,.17,.9);q=leave(t);n=len(slots)
    candidates=list(dict.fromkeys([min(1,n-1),max(0,n-2),n-1]))
    which=min(len(candidates)-1,max(0,int((t-.9)/1.05)));cur=candidates[which];prev=candidates[max(0,which-1)]
    trans=smooth(prog(t,.9+which*1.05,.9+which*1.05+.28))
    old=slots[prev];new=slots[cur]
    xx=mix(old[1],new[1],trans);yy=top+mix(old[2],new[2],trans);ww=mix(old[3],new[3],trans)
    pad=17;expand=pop(prog(t,.32,1.04));width=(ww+pad*2)*expand
    center=xx+ww/2
    rr(out,(center-width/2,yy-fs*.67,center+width/2,yy+fs*.66),rgba(p['accent'],round(a*(1-q)*255)),18)
    for i,(word,x,dy,w,row) in enumerate(slots):
        # Main text is cut through the exact highlight shape so moving markers
        # retain contrast even between two word slots.
        entry=enter(t,.18+i*.045,.75+i*.045)
        text(out,word,x+w/2,top+dy,fs,p['text'],opacity=entry*(1-q))
    dark=layer()
    for i,(word,x,dy,w,row) in enumerate(slots):text(dark,word,x+w/2,top+dy,fs,p['bg'])
    mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rounded_rectangle((round(center-width/2),round(yy-fs*.67),round(center+width/2),round(yy+fs*.66)),radius=18,fill=round(a*(1-q)*255))
    dark.putalpha(Image.fromarray(np.minimum(np.asarray(dark.getchannel('A')),np.asarray(mask)).astype('uint8')))
    out.alpha_composite(dark)
    support(out,cfg,p,555,life(t,.7,1.2))
    return out


@lru_cache(maxsize=64)
def hook_icon(kind,panel_color,accent,text_color):
    im=layer(126,126);rr(im,(9,9,117,117),panel_color,28,rgba(accent,90),2)
    if kind==0:
        pts=[]
        for i in range(10):
            rad=29 if i%2==0 else 13;ang=-math.pi/2+i*math.pi/5;pts.append((63+math.cos(ang)*rad,63+math.sin(ang)*rad))
        ImageDraw.Draw(im).polygon(pts,fill=accent)
    elif kind==1:
        circle(im,63,63,29,None,accent,4);line(im,[(63,43),(63,63),(78,72)],accent,4)
    elif kind==2:ImageDraw.Draw(im).polygon([(49,37),(49,89),(87,63)],fill=accent)
    else:ImageDraw.Draw(im).polygon([(70,30),(42,67),(62,67),(55,96),(85,55),(66,55)],fill=accent)
    return im


def icon_hook(t,cfg,p):
    out=layer();s=str(cfg['text']);fs,slots,span=words_layout(s,690,66,2);top=347-span/2
    for i,(word,x,dy,w,row) in enumerate(slots):
        a=enter(t,.24+i*.045,.86+i*.045)
        text(out,word,x+w/2,top+dy+(1-a)*35,fs,p['accent'] if i==1 else p['text'],opacity=a)
    for i,(xx,yy) in enumerate([(168,280),(1112,280),(190,454),(1090,454)]):
        a=pop(prog(t,.25+i*.09,.94+i*.09))
        # During motion is subtle after the reveal; all orbits share stable centres.
        drift=3*math.sin(t*1.7+i);x=mix(640,xx,a)+drift;y=mix(347,yy,a)+3*math.cos(t*1.7+i)
        icon=hook_icon(i,p['panel'],p['accent'],p['text'])
        paste(out,icon,x,y,clamp(a),scale=mix(.6,1,a),angle=(1-a)*(16 if i%2 else -16)+math.sin(t+i)*1.8)
        if .9<t<1.6:
            r=54+prog(t,.9,1.6)*24;circle(out,x,y,r,None,rgba(p['accent'],round(80*(1-prog(t,.9,1.6)))),2)
    support(out,cfg,p,566,life(t,.85,1.35))
    return out


def punch_number(t,cfg,p):
    out=layer();target=float(cfg.get('value',24));decimals=max(0,min(3,int(cfg.get('decimals',0))))
    value=target*smooth(prog(t,.3,1.65))
    number=f'{value:,.{decimals}f}';number=str(cfg.get('prefix',''))+number+str(cfg.get('suffix',''))
    a=pop(prog(t,.17,.92));q=leave(t)
    fs=fit_size(str(cfg.get('prefix',''))+f'{target:,.{decimals}f}'+str(cfg.get('suffix','')),680,173)
    text(out,number,640,310+(1-a)*70,fs,p['accent'],opacity=clamp(a),scale=a)
    s=str(cfg['text']);text(out,s,640,455,fit_size(s,1040,56),p['text'],opacity=enter(t,.65,1.2),scale=1+(1-enter(t,.65,1.2))*.06)
    support(out,cfg,p,557,life(t,.8,1.3))
    result=layer();paste(result,out,640,360+q*60,1-q,scale=1-q*.08)
    return result


RENDERERS={'T01':masked_words,'T02':rotate_glyphs,'T03':typewriter,'T04':beat_lines,
           'X01':lattice,'X02':bar_underline,'X03':outline_wave,'X04':chromatic,
           'H01':active_caption,'H02':keyword_pill,'H03':icon_hook,'H04':punch_number}


def render(pid,t,cfg):
    defaults=PRESETS[pid];params={**defaults,**cfg};p=palette(params);dst=base(params)
    content=RENDERERS[pid](float(t),params,p)
    if pid=='H03':group(dst,content,t,'down')
    else:dst.alpha_composite(content)
    return dst
