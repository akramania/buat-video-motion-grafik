"""Seven original source-observed presets. Public references are analysis only.

All animation uses deterministic timeline evaluation; no state carries between frames.
Number styles use semantic clamped values. Digit motion is decorative and settles
exactly. User assets may be supplied as cfg['asset']; no stock preview is bundled.
"""
from core import *
from PIL import ImageChops, ImageOps
from functools import lru_cache
import random

PRESETS={
 'B01':dict(name='Paper Fold Reveal',description='Kertas bertekstur membuka dari lipatan pusat, tahan, kemudian berlipat semula.',genre='documentary',genres=['documentary','creator','education'],text='CERITA YANG BERMAKNA',subtitle='Satu cerita. Banyak perspektif.',source_url='https://elements.envato.com/ripped-paper-text-presets-62SS98C',observed_timestamp='12.5–14.2 s'),
 'B02':dict(name='Diagonal Glass Opener',description='Panel media serong bergerak berlapis dengan tajuk utama dan echo besar.',genre='corporate',genres=['corporate','promo','documentary'],text='PERSPEKTIF BAHARU',subtitle='LUASKAN PANDANGAN ANDA',source_url='https://elements.envato.com/opener-V3BHS5Y',observed_timestamp='4.7–6.3 s'),
 'B03':dict(name='Decode Typography',description='Glyph bertukar secara deterministik sebelum mengunci kepada teks sebenar.',genre='saas',genres=['saas','creator','promo'],text='IDEA MENJADI NYATA',subtitle='DARIPADA KEMUNGKINAN KEPADA TINDAKAN',source_url='https://elements.envato.com/text-animation-5FDKCMH',observed_timestamp='11.2–12.8 s'),
 'B04':dict(name='Inline Metric Marker',description='Nilai meningkat tepat dalam ayat dengan penanda warna yang menyapu di belakangnya.',genre='education',genres=['education','corporate','saas'],text='Kami telah membantu',subtitle='pasukan bergerak lebih pantas',from_value=0,to_value=37000,prefix='',suffix='',decimals=0,source_url='https://elements.envato.com/number-text-animation-pp-FL3YXDY',observed_timestamp='9.6–12.0 s'),
 'B05':dict(name='Neon Cue Captions',description='Ayat kekal stabil; warna dan neon berpindah mengikut cue setiap perkataan.',genre='creator',genres=['creator','education','promo'],text='Jadikan setiap perkataan jelas dan bermakna',subtitle='Tutorial / podcast / kandungan sosial',source_url='https://elements.envato.com/modern-creator-subtitle-KHLUZHK',observed_timestamp='10.8–12.3 s'),
 'B06':dict(name='Finished Word Typewriter',description='Teks ditaip dengan jeda; penanda hanya muncul selepas sesuatu perkataan lengkap.',genre='documentary',genres=['documentary','education','corporate'],text='Idea kecil.\nPerubahan besar.',subtitle='CATATAN HARI INI',source_url='https://elements.envato.com/typewriter-pro-GURUKWQ',observed_timestamp='46.5–49.05 s'),
 'B07':dict(name='Gradient Metric Reels',description='Digit bergulung dalam klip, gradien dan bar kemajuan berakhir pada nilai yang tepat.',genre='corporate',genres=['corporate','saas','promo'],text='Kemajuan yang boleh diukur',subtitle='DATA DEMO / BUKAN PRESTASI SEBENAR',from_value=0,to_value=120,prefix='',suffix='%',decimals=0,source_url='https://elements.envato.com/number-counter-7LZ6EUM',observed_timestamp='9.5–10.5 s'),
}


def _words_layout(s,size,maxw=1000,face='bold'):
    """Retain character ranges and explicit line breaks for typing and cue layouts."""
    f=font(size,face); rows=[];row=[];x=0;idx=0
    for para in s.split('\n'):
        for word in para.split(' '):
            if not word:idx+=1;continue
            ww=f.getlength(word)
            if x and x+ww>maxw:
                rows.append((row,x-f.getlength(' ')));row=[];x=0
            row.append((word,x,idx,idx+len(word)));x+=ww+f.getlength(' ');idx+=len(word)+1
        rows.append((row,max(0,x-f.getlength(' '))));row=[];x=0
    return rows


def _number(cfg,p):
    a=float(cfg.get('from_value',0));b=float(cfg.get('to_value',100))
    if not math.isfinite(a) or not math.isfinite(b):raise ValueError('Counter values must be finite')
    dp=int(cfg.get('decimals',0))
    if not 0<=dp<=6:raise ValueError('decimals must be 0..6')
    value=b if p>=1 else a if p<=0 else mix(a,b,p)
    grouping=bool(cfg.get('grouping',True)); spec=',' if grouping else ''
    result=format(value,f'{spec}.{dp}f')
    return str(cfg.get('prefix',''))+result+str(cfg.get('suffix',''))


@lru_cache(maxsize=128)
def _paper(s,ink,accent):
    ww,hh=1000,235;rng=random.Random(8204)
    im=layer(ww,hh);d=ImageDraw.Draw(im)
    xs=list(range(6,ww-5,16));pts=[(x,9+rng.randint(-4,4)) for x in xs]
    pts += [(ww-8,hh-10)]+[(x,hh-10+rng.randint(-4,4)) for x in reversed(xs)]
    d.polygon(pts,fill='#F3EDD8')
    texture=layer(ww,hh);td=ImageDraw.Draw(texture)
    for i in range(1600):
        x=rng.randrange(12,ww-12);y=rng.randrange(16,hh-16);v=rng.randrange(165,220)
        td.point((x,y),fill=(v,v-4,v-14,80))
    im.alpha_composite(texture)
    fs=fit_size(s,920,73,'bold');text(im,s,500,118,fs,ink)
    # Original thin fold shading and distressed edge fibres, stable over time.
    folds=layer(ww,hh);fd=ImageDraw.Draw(folds)
    for x in range(125,1000,125):
        fd.line((x,12,x,hh-10),fill=(80,55,30,22),width=3)
        fd.line((x+3,12,x+3,hh-10),fill=(255,255,255,65),width=2)
    im.alpha_composite(folds)
    return im


def _b01(t,cfg):
    im=base(cfg);p=palette(cfg);s=cfg.get('text',PRESETS['B01']['text']);sub=cfg.get('subtitle','')
    incoming=pop(prog(t,.15,1.15));out=leave(t);opening=clamp(incoming)*(1-out)
    paper=_paper(s,cfg.get('text_color','#342D2B'),p['accent']);parts=8;ww=paper.width/parts
    scale_y=mix(.18,1,ease(prog(t,.15,.65)))*(1-.65*out)
    if opening>.001:
        shadow=layer(1060,300);rr(shadow,(50,55,1010,265),(0,0,0,60),15)
        shadow=shadow.filter(ImageFilter.GaussianBlur(18))
        paste(im,shadow,640,380,opening*.8,scale=max(.03,opening))
        total=paper.width*max(.04,opening);left=640-total/2
        for i in range(parts):
            src=paper.crop((round(i*ww),0,round((i+1)*ww),paper.height))
            sw=max(2,round(ww*max(.04,opening)));sh=max(2,round(paper.height*scale_y))
            src=src.resize((sw,sh),Image.Resampling.BICUBIC)
            if opening<.98:
                shade=layer(sw,sh);ImageDraw.Draw(shade).rectangle((0,0,sw,sh),fill=(35,20,5,round((1-opening)*(100 if i%2 else 35))))
                src=Image.alpha_composite(src,shade)
            dy=math.sin(i*math.pi/2)*(1-opening)*32+math.sin(t*.8+i*.3)*1.6*opening
            paste(im,src,left+i*sw+sw/2,355+dy,opacity=clamp(prog(t,.1,.3))*(1-out),angle=(1-opening)*(-1 if i%2 else 1)*5)
    v=life(t,.7,1.3,4.05,4.65)
    text(im,sub,640,535+18*(1-v),fit_size(sub,950,25,'serif'),p['muted'],'serif',opacity=v)
    text(im,'01 / NOTES IN MOTION',640,197,17,p['accent'],'mono',opacity=life(t,.2,.7,4.1,4.6))
    return im


@lru_cache(maxsize=48)
def _landscape(genre,accent,asset=''):
    w,h=1140,430
    if asset:
        with Image.open(asset) as a:
            return ImageOps.fit(a.convert('RGB'),(w,h),Image.Resampling.LANCZOS).convert('RGBA')
    # Original designed landscape illustration, not a retrieved stock photograph.
    yy,xx=np.mgrid[:h,:w];top=np.array((36,67,100));bottom=np.array((220,161,121))
    grad=top[None,None,:]*(1-yy[:,:,None]/h)+bottom[None,None,:]*(yy[:,:,None]/h)
    arr=np.repeat(grad,w,axis=1) if grad.shape[1]==1 else grad
    im=Image.fromarray(np.uint8(arr)).convert('RGBA');d=ImageDraw.Draw(im)
    d.ellipse((760,70,885,195),fill='#FFD7A1')
    d.polygon([(0,300),(150,190),(240,250),(380,125),(580,270),(725,200),(1000,260),(1140,220),(1140,430),(0,430)],fill='#6D7F8E')
    d.polygon([(0,340),(220,270),(320,305),(510,210),(680,305),(900,220),(1140,350),(1140,430),(0,430)],fill='#3A5366')
    d.polygon([(0,390),(180,340),(450,378),(720,300),(890,340),(1140,305),(1140,430),(0,430)],fill='#213F50')
    d.polygon([(530,430),(645,340),(670,340),(605,430)],fill='#CBB497')
    for k in range(7):
        y=385+k*6;d.line((0,y,360-30*k,y),fill=(221,189,156,70),width=1)
    return im


def _b02(t,cfg):
    im=base(cfg);p=palette(cfg);s=cfg.get('text','');sub=cfg.get('subtitle','')
    foreground=cfg.get('text_color','#FFFFFF')
    src=_landscape(cfg.get('genre','corporate'),p['accent'],str(cfg.get('asset','')))
    media=layer();v=life(t,.1,.55,4.45,4.95)
    if v:
        baseimg=ImageOps.fit(src,(1100,422),Image.Resampling.BICUBIC)
        paste(media,baseimg,640,374,opacity=v)
        shade=layer();ImageDraw.Draw(shade).rectangle((90,162,1190,586),fill=(0,0,0,45));media.alpha_composite(shade)
        for i in range(4):
            ent=enter(t,.15+i*.09,.85+i*.09);out=leave(t,4.1+i*.08,4.72+i*.06)
            shift=340*(1-ent)-600*out;cx=80+i*295+shift
            mask=Image.new('L',(W,H));d=ImageDraw.Draw(mask)
            pts=[(cx+125,162),(cx+440,162),(cx+265,586),(cx-50,586)];d.polygon(pts,fill=105 if i%2 else 175)
            shifted=layer();offset=8*math.sin(t*.6+i)+10*(i-1.5)
            paste(shifted,src,640+offset,374,scale=1+.015*i)
            shifted.putalpha(ImageChops.multiply(shifted.getchannel('A'),mask));media.alpha_composite(shifted)
            line(media,[pts[0],pts[3]],rgba('#FFFFFF',90*v),2)
        rr(media,(88,159,1192,588),(0,0,0,0),0,rgba('#FFFFFF',150*v),2)
        im.alpha_composite(media)
    hold=life(t,.55,1.3,4.05,4.7)
    echo=text_img(s,fit_size(s,1340,148),foreground);paste(im,echo,640-25*math.sin(t*.3),383,opacity=.16*hold)
    text(im,s,640,364+22*(1-hold),fit_size(s,980,65),foreground,opacity=hold)
    text(im,sub,640,291,fit_size(sub,850,20,'sans'),foreground,'sans',opacity=hold)
    for x,y in [(129,202),(1147,544)]:
        line(im,[(x-5,y),(x+5,y)],rgba(foreground,160*hold),2);line(im,[(x,y-5),(x,y+5)],rgba(foreground,160*hold),2)
    return im


def _b03(t,cfg):
    im=base(cfg);p=palette(cfg);s=cfg.get('text','').replace('\n',' ');sub=cfg.get('subtitle','')
    fs=fit_size(s,1090,78,'mono');adv=[measure(c,fs,'mono') for c in s];x=640-sum(adv)/2
    out=leave(t);alpha=life(t,.15,.5,4.2,4.8);n=max(1,len(s));alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    for i,(c,a) in enumerate(zip(s,adv)):
        lock=.8+1.15*i/n;pr=prog(t,lock-.35,lock)
        char=c;col=p['text'];offset=0
        if c!=' ' and pr<1:
            rnd=random.Random(912+i*311+int(max(0,t)*21));char=alphabet[rnd.randrange(len(alphabet))]
            col=p['accent'];offset=14*(1-pr)*math.sin(t*9+i)
        if out>0 and c!=' ':
            if out>i/n:
                rnd=random.Random(i+int(t*30));char=alphabet[rnd.randrange(len(alphabet))];col=p['accent']
        text(im,char,x+a/2,341+offset-45*out,fs,col,'mono',opacity=alpha)
        if c!=' ':
            line(im,[(x+3,396),(x+a-3,396)],rgba(p['accent'],int(90*(1-pr)*alpha)),2)
        x+=a
    pr=prog(t,.6,2.05);left=640-180
    line(im,[(left,466),(left+360,466)],rgba(p['muted'],50*alpha),2)
    line(im,[(left,466),(left+360*pr,466)],rgba(p['accent'],220*alpha),2)
    text(im,'DECODE / '+str(round(pr*100)).zfill(3)+'%',640,503,16,p['accent'],'mono',opacity=alpha)
    text(im,sub,640,217,fit_size(sub,1020,18,'mono'),p['muted'],'mono',opacity=alpha)
    return im


def _b04(t,cfg):
    im=base(cfg);p=palette(cfg);alpha=life(t,.15,.8,4.15,4.85);out=leave(t)
    v=ease(prog(t,.75,3.35));value=_number(cfg,v)
    final=_number(cfg,1);initial=_number(cfg,0);fs=fit_size(max([final,initial],key=len),790,112)
    width=max(measure(final,fs),measure(initial,fs))+50;left=640-width/2
    marker=ease(prog(t,1.1,2.7))*(1-out)
    y=357-25*out
    if marker:
        rr(im,(left,y-70,left+width*marker,y+70),rgba(p['accent'],240*alpha),12)
    text(im,value,640,y,fs,p['bg'] if marker>.98 else p['text'],opacity=alpha)
    text(im,cfg.get('text',''),640,240+20*(1-alpha),fit_size(cfg.get('text',''),1040,36,'sans'),p['text'],'sans',opacity=alpha)
    text(im,cfg.get('subtitle',''),640,485,fit_size(cfg.get('subtitle',''),1000,29,'sans'),p['muted'],'sans',opacity=alpha)
    text(im,'NILAI DEMO',640,559,14,p['accent'],'mono',opacity=alpha)
    for i in range(9):
        r=3+3*smooth(prog(v,i/10,(i+1)/10));circle(im,560+i*20,197,r,rgba(p['accent'],100*alpha))
    return im


@lru_cache(maxsize=1024)
def _glowing_word(word,size,color):
    txt=text_img(word,size,color);pad=24;out=layer(txt.width+pad*2,txt.height+pad*2)
    paste(out,txt,pad,pad,anchor='topleft');glow=out.filter(ImageFilter.GaussianBlur(9))
    glow=Image.blend(layer(out.width,out.height),glow,.72);glow.alpha_composite(out)
    return glow


def _b05(t,cfg):
    im=base(cfg);p=palette(cfg);s=cfg.get('text','');fs=58
    rows=_words_layout(s,fs,950)
    if len(rows)>3:fs=44;rows=_words_layout(s,fs,1030)
    allwords=[w for row,_ in rows for w in row];n=max(1,len(allwords));v=life(t,.18,.7,4.2,4.8)
    cue=cfg.get('cues');y0=350-(len(rows)-1)*44;index=0;active_indices=set()
    for ri,(row,rw) in enumerate(rows):
        for word,x,a,b in row:
            start=.85+index*(2.85/n);end=.85+(index+1)*(2.85/n)
            if isinstance(cue,list) and index<len(cue):
                start=float(cue[index].get('start',start));end=float(cue[index].get('end',end))
            active=start<=t<end;cx=640-rw/2+x+measure(word,fs)/2;cy=y0+ri*88
            if active:
                active_indices.add(index)
                glow=_glowing_word(word,fs,p['accent']);pulse=1+.035*math.sin(math.pi*prog(t,start,end))
                paste(im,glow,cx,cy,opacity=v,scale=pulse)
            else:text(im,word,cx,cy,fs,p['text'],opacity=v)
            index+=1
    text(im,cfg.get('subtitle',''),640,551,fit_size(cfg.get('subtitle',''),1020,21,'sans'),p['muted'],'sans',opacity=v)
    for i in range(n):
        active=i in active_indices
        circle(im,640-(n-1)*12+i*24,216,5 if active else 3,rgba(p['accent'] if active else p['muted'],int(220*v)))
    return im


def _b06(t,cfg):
    im=base(cfg);p=palette(cfg);s=cfg.get('text','');fs=56;rows=_words_layout(s,fs,960,'mono')
    if len(rows)>3:fs=40;rows=_words_layout(s,fs,1020,'mono')
    v=life(t,.15,.7,4.2,4.8);out=leave(t)
    # Timeline-derived event schedule: explicit pauses reserve time after the named
    # character, with no backwards count or jump when a pause starts/ends.
    weights=[1.7 if c in ' .,!?:\n' else 1 for c in s];total=max(1,sum(weights))
    pauses={}
    for item in cfg.get('pauses',[]):
        if not isinstance(item,dict):raise ValueError('pauses must contain objects')
        after=int(item.get('after_character',0));duration=float(item.get('duration',0))
        if not 0<=after<=len(s) or not math.isfinite(duration) or duration<0:
            raise ValueError('Invalid typewriter pause')
        pauses[after]=pauses.get(after,0)+duration
    reserve=sum(pauses.values())
    if reserve>=2.95:raise ValueError('Total typewriter pauses must be below 2.95 scene seconds')
    step=(2.95-reserve)/total;elapsed=t-.7;count=0;clock=pauses.get(0,0)
    for i,w in enumerate(weights,1):
        clock+=w*step
        if elapsed<clock:break
        count=i;clock+=pauses.get(i,0)
    if t>=3.65:count=len(s)
    top=337-(len(rows)-1)*46;cursor=None
    for ri,(row,rw) in enumerate(rows):
        x0=170;y=top+ri*92
        for word,x,a,b in row:
            shown=max(0,min(len(word),count-a));xx=x0+x
            if shown==len(word) and shown:
                w=measure(word,fs,'mono');rr(im,(xx-5,y-40,xx+w+5,y+42),rgba(p['accent'],36*v),4)
                text(im,word,xx,y,fs,p['accent'],'mono',opacity=v,anchor='left')
            elif shown:
                text(im,word[:shown],xx,y,fs,p['text'],'mono',opacity=v,anchor='left')
            if a<=count<=b:cursor=(xx+measure(word[:shown],fs,'mono')+6,y)
    if cursor is None and rows and rows[-1][0]:
        row,rw=rows[-1];cursor=(170+rw+6,top+(len(rows)-1)*92)
    if cursor and (count<len(s) or int(t*2.5)%2==0):
        xx,y=cursor;line(im,[(xx,y-31),(xx,y+31)],rgba(p['accent'],255*v),3)
    text(im,cfg.get('subtitle',''),170,204,fit_size(cfg.get('subtitle',''),950,18,'mono'),p['muted'],'mono',anchor='left',opacity=v)
    line(im,[(170,540),(1110,540)],rgba(p['muted'],60*v),1)
    text(im,'SELESAI DITAIP → DISERLAHKAN',170,568,15,p['muted'],'mono',anchor='left',opacity=v)
    return im


@lru_cache(maxsize=256)
def _gradient_glyph(c,size,left,right):
    glyph=text_img(c,size,'#FFFFFF','bold');yy,xx=np.mgrid[:glyph.height,:glyph.width]
    a=np.array(rgb(left));b=np.array(rgb(right));r=xx/max(1,glyph.width-1)
    ar=a[None,None,:]*(1-r[:,:,None])+b[None,None,:]*r[:,:,None]
    im=Image.fromarray(np.uint8(ar)).convert('RGBA');im.putalpha(glyph.getchannel('A'));return im


def _b07(t,cfg):
    im=base(cfg);p=palette(cfg);v=life(t,.15,.7,4.15,4.85);out=leave(t)
    valprogress=smooth(prog(t,.6,3.1));value=_number(cfg,valprogress);final=_number(cfg,1);start=_number(cfg,0)
    fs=fit_size(max([final,start],key=len),990,142);rowheight=fs*1.25
    # Digits have a constant cell width; center the currently formatted number as a row.
    digitwidth=measure('0',fs,'bold')+3;chars=list(value)
    widths=[digitwidth if c.isdigit() else measure(c,fs,'bold')+2 for c in chars]
    total=sum(widths);x=640-total/2;cy=355-35*out
    stage=layer(W,H);cliptop=cy-rowheight/2;clipbottom=cy+rowheight/2
    for i,(c,cw) in enumerate(zip(chars,widths)):
        cx=x+cw/2
        if c.isdigit():
            # The current semantic digit is centered as value settles. Incoming previous
            # digit only appears within its own clipped column, never as a separate value.
            velocity=(1-valprogress)**1.2
            fraction=(t*7+i*.21)%1 if .6<t<2.75 else 0
            shift=fraction*rowheight*velocity
            current=_gradient_glyph(c,fs,p['accent'],p['secondary'])
            paste(stage,current,cx,cy-shift,opacity=v)
            if velocity>.02 and shift>0:
                nxt=str((int(c)+1)%10);paste(stage,_gradient_glyph(nxt,fs,p['accent'],p['secondary']),cx,cy-shift+rowheight,opacity=v)
        else:
            # Align punctuation to the same font baseline as the rolling digits.
            glyph_box=font(fs,'bold').getbbox(c)
            digit_box=font(fs,'bold').getbbox('0')
            glyph_y=cy+(glyph_box[1]+glyph_box[3]-digit_box[1]-digit_box[3])/2
            text(stage,c,cx,glyph_y,fs,p['text'],opacity=v)
        x+=cw
    clip=Image.new('L',(W,H));ImageDraw.Draw(clip).rectangle((100,cliptop,1180,clipbottom),fill=255)
    stage.putalpha(ImageChops.multiply(stage.getchannel('A'),clip));im.alpha_composite(stage)
    barw=660;left=640-barw/2
    rr(im,(left,470,left+barw,480),rgba(p['muted'],35*v),5)
    if valprogress>0:rr(im,(left,470,left+barw*valprogress*(1-out),480),rgba(p['accent'],230*v),5)
    label=cfg.get('text','');text(im,label,640,235,fit_size(label,1060,30,'sans'),p['text'],'sans',opacity=v)
    text(im,cfg.get('subtitle',''),640,545,fit_size(cfg.get('subtitle',''),1000,16,'mono'),p['muted'],'mono',opacity=v)
    return im


def render(pid,t,cfg):
    funcs={'B01':_b01,'B02':_b02,'B03':_b03,'B04':_b04,'B05':_b05,'B06':_b06,'B07':_b07}
    if pid not in funcs:raise ValueError('Unknown preset '+pid)
    return funcs[pid](float(t),cfg)
