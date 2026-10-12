"""Original long-scene presets: fixed anchors, independent fast local events.

All timestamps are actual seconds. ``tempo`` affects movement duration through
long_scene_tools.progress, never the overall scene clock or reading holds.
No supplied footage, character, stock animation or stock template is copied.
"""
from core import *
from PIL import ImageChops
from long_scene_tools import cue, progress


PRESETS = {
    'L04': dict(
        name='Workflow Window Cluster',
        description='Tiga tetingkap kekal di tempatnya; typing, laluan data, cip kemajuan dan handoff bergerak mengikut cue setempat.',
        genre='saas', genres=['saas','corporate','education'],
        text='Idea masuk. Hasil tersusun.', subtitle='SATU RUANG KERJA / PELBAGAI GERAKAN SETEMPAT',
        items=['INPUT','PROSES','HASIL'], words=['Brief projek','Aset visual','Nada jenama'],
        code_lines=['susun(brief, aset)','padankan(warna)','bina(timeline)','semak(output)'],
        output_items=['Struktur siap','Visual disusun','Fail sedia'],ready_label='3 ASET SEDIA',
        processing_label='MEMPROSES',complete_label='SEDIA',summary_text='3 TETINGKAP  /  1 ALIRAN KERJA',
        time_mode='seconds',duration=16,min_duration=16,end_behavior='hold',
        cue_defaults=dict(input=.5,route_a=3.3,process=4.,route_b=7.8,output=8.6,handoff=11.8,summary=13.2)),
    'L05': dict(
        name='Kinetic Editorial Stage',
        description='Pentas editorial kekal dengan tajuk besar, keyword berganti dalam mask, underline dan jubin sisi bergerak berasingan.',
        genre='creator', genres=['creator','promo','corporate'],
        text='SATU SCENE.', subtitle='Ruang kekal. Cerita terus berkembang.',
        words=['BANYAK GERAK.','TEKS BERSUARA.','RITMA TERJAGA.','MESEJ JELAS.'],
        items=['TEKS','LAPISAN','RITMA'],
        eyebrow='STUDIO / IDEAS IN MOTION',summary_text='01 SCENE    04 BEATS    RUANG UNTUK MEMBACA',
        time_mode='seconds',duration=16,min_duration=16,end_behavior='hold',
        cue_defaults=dict(headline=.45,keyword=1.7,replace_a=5.,replace_b=8.4,replace_c=11.6,summary=13.4)),
    'L06': dict(
        name='Before After Rebuild',
        description='Dua kad perbandingan kekal; tiga bar diperbaik satu per satu, nilai asal kekal sebagai bayang dan progress dikongsi.',
        genre='corporate', genres=['corporate','saas','education'],
        text='Lihat perubahan, satu demi satu.', subtitle='DATA DEMO / NILAI ILUSTRASI, BUKAN PRESTASI SEBENAR',
        items=['Kejelasan','Susunan','Konsistensi'], before_values=[42,56,36],after_values=[84,90,78],
        before_label='SEBELUM',after_label='SELEPAS',progress_label='3 LANGKAH PENAMBAHBAIKAN',
        summary_text='NILAI ASAL KEKAL SEBAGAI RUJUKAN',
        suffix='%',time_mode='seconds',duration=16,min_duration=16,end_behavior='hold',
        cue_defaults=dict(bars=.7,improve_a=3.3,improve_b=6.4,improve_c=9.5,summary=12.9)),
}


def _list(cfg,key,default,n):
    value=cfg.get(key,default)
    if not isinstance(value,(tuple,list)) or len(value)!=n:
        raise ValueError(f'{key} must contain exactly {n} entries')
    return [str(x) for x in value[:n]]


def _local(t,cfg,key,default,length=.6):
    return ease(progress(t,cue(cfg,key,default),length,cfg))


def _rgba_lerp(a,b,q):
    return tuple(round(mix(x,y,q)) for x,y in zip(rgb(a),rgb(b)))+(255,)


def _fitted(im,s,x,y,width,size,color,face='bold',opacity=1,anchor='left'):
    text(im,s,x,y,fit_size(s,width,size,face),color,face,opacity=opacity,anchor=anchor)


def _track(im,s,x,y,size,color,tracking=3,opacity=1):
    for char in s:
        text(im,char,x,y,size,color,'mono',anchor='left',opacity=opacity)
        x+=measure(char,size,'mono')+tracking


@lru_cache(maxsize=96)
def _window(w,h,panel_color,muted,accent):
    out=panel(w,h,panel_color,20,muted,True).copy()
    # panel adds 30 px around content for a real soft blurred shadow.
    ox=30;oy=30
    line(out,[(ox+1,oy+43),(ox+w-1,oy+43)],rgba(muted,70),1)
    for i in range(3):circle(out,ox+17+i*13,oy+22,3.5,rgba(accent,80+30*i))
    rr(out,(ox+w-66,oy+14,ox+w-15,oy+29),rgba(muted,30),7)
    return out


def _draw_window(im,x,y,w,h,title,p,active=0):
    paste(im,_window(w,h,p['panel'],p['muted'],p['accent']),x-30,y-30,anchor='topleft')
    if active>.001:
        rr(im,(x,y,x+w,y+h),(0,0,0,0),20,rgba(p['accent'],int(75*active)),2)
    _fitted(im,title,x+66,y+22,w-145,16,p['text'],'mono')


def _check(im,x,y,p,q=1,size=10):
    circle(im,x,y,size,rgba(p['accent'],35*q))
    pts=[(x-size*.48,y),(x-size*.12,y+size*.34),(x+size*.52,y-size*.35)]
    line(im,pts,rgba(p['accent'],255*q),2)


def _path_point(points,q):
    lengths=[math.hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(points,points[1:])]
    target=clamp(q)*sum(lengths)
    for i,length in enumerate(lengths):
        if target<=length or i==len(lengths)-1:
            f=target/max(.001,length);a,b=points[i:i+2]
            return (mix(a[0],b[0],f),mix(a[1],b[1],f))
        target-=length
    return points[-1]


def _partial_path(points,q):
    lengths=[math.hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(points,points[1:])]
    target=clamp(q)*sum(lengths);out=[points[0]]
    for i,length in enumerate(lengths):
        if target<length:
            f=target/max(.001,length);a,b=points[i:i+2]
            out.append((mix(a[0],b[0],f),mix(a[1],b[1],f)));break
        out.append(points[i+1]);target-=length
    return out


def _route(im,points,t,start,p,cfg):
    line(im,points,rgba(p['muted'],75),2)
    q=progress(t,start,.7,cfg)
    if q>0:line(im,_partial_path(points,ease(q)),rgba(p['accent'],185),3)
    if start<=t<start+1.5/max(.15,float(cfg.get('tempo',1))):
        dotq=progress(t,start,1.05,cfg);x,y=_path_point(points,smooth(dotq))
        circle(im,x,y,9,rgba(p['accent'],30));circle(im,x,y,4,p['accent'])


def _l04(t,cfg):
    im=base(cfg);p=palette(cfg)
    names=_list(cfg,'items',PRESETS['L04']['items'],3)
    rows=_list(cfg,'words',PRESETS['L04']['words'],3)
    intro=_local(t,cfg,'input',.5,.55)
    _fitted(im,cfg.get('text',''),84,157,1120,36,p['text'])
    _fitted(im,cfg.get('subtitle',''),84,199,1120,17,p['muted'],'mono')
    # Routes are behind the windows, with locally timed packet travel.
    path_a=[(426,434),(449,434),(449,367),(474,367)]
    path_b=[(804,405),(828,405),(828,439),(852,439)]
    _route(im,path_a,t,cue(cfg,'route_a',3.3),p,cfg)
    _route(im,path_b,t,cue(cfg,'route_b',7.8),p,cfg)
    _draw_window(im,82,258,344,270,names[0],p,intro)
    process=_local(t,cfg,'process',4.,.6)
    _draw_window(im,474,235,330,326,names[1],p,process)
    output=_local(t,cfg,'output',8.6,.55)
    _draw_window(im,852,279,344,252,names[2],p,output)
    # Input row rhythm: row, typing, verification each use an independent clock.
    for i,s in enumerate(rows):
        start=cue(cfg,'input',.5)+i*.68
        q=ease(progress(t,start,.32,cfg));y=328+i*57
        rr(im,(103,y-20,404,y+22),rgba(p['muted'],int(21*q)),9)
        circle(im,121,y,5,rgba(p['secondary'],int(180*q)))
        count=round(len(s)*progress(t,start+.15,.52,cfg))
        shown=s[:count]
        fs=fit_size(s,205,20,'sans')
        text(im,shown,139,y,fs,p['text'],'sans',opacity=q,anchor='left')
        if 0<count<len(s):
            xpos=139+measure(shown,fs,'sans')+4
            line(im,[(xpos,y-9),(xpos,y+9)],p['accent'],2)
        done=progress(t,start+.75,.23,cfg)
        if done>0:_check(im,382,y,p,done,9)
    inputdone=ease(progress(t,cue(cfg,'route_a',3.3),.3,cfg))
    _fitted(im,cfg.get('ready_label','3 ASET SEDIA'),107,499,289,13,p['accent'],'mono',inputdone)
    # Processing code is intentionally semantic, not executable imitation.
    code=_list(cfg,'code_lines',PRESETS['L04']['code_lines'],4)
    for i,s in enumerate(code):
        start=cue(cfg,'process',4.)+i*.64;pp=progress(t,start,.5,cfg)
        yy=305+i*35
        text(im,str(i+1).zfill(2),494,yy,12,p['muted'],'mono',anchor='left')
        text(im,s[:round(len(s)*pp)],528,yy,fit_size(s,250,16,'mono'),p['accent'] if i==3 else p['text'],'mono',anchor='left')
        if start<=t<start+.7:
            rr(im,(490,yy-14,788,yy+15),rgba(p['accent'],15),4)
    process_fill=smooth(progress(t,cue(cfg,'process',4.)+.15,2.9,cfg))
    rr(im,(496,456,782,465),rgba(p['muted'],38),4)
    if process_fill>0:rr(im,(496,456,496+286*process_fill,465),p['accent'],4)
    text(im,f'{round(process_fill*100):03d}%',496,491,24,p['text'],'mono',anchor='left')
    state=cfg.get('complete_label','SEDIA') if process_fill==1 else cfg.get('processing_label','MEMPROSES')
    _fitted(im,state,780,491,156,12,p['accent'],'mono',anchor='right')
    for i in range(5):
        q=ease(progress(t,cue(cfg,'process',4.)+.45+i*.49,.3,cfg))
        rr(im,(496+i*58,528,540+i*58,540),rgba(p['accent'] if q>=1 else p['muted'],60+int(120*q)),4)
    # Output cards become concrete while the other windows remain readable.
    for i,s in enumerate(_list(cfg,'output_items',PRESETS['L04']['output_items'],3)):
        start=cue(cfg,'output',8.6)+i*.54;pp=ease(progress(t,start,.4,cfg))
        yy=356+i*53
        rr(im,(873,yy-19,1175,yy+20),rgba(p['accent'],int(14*pp)),8)
        _check(im,893,yy,p,pp,10)
        _fitted(im,s,916,yy,238,20,p['text'],'sans',pp)
    # Second handoff sweeps along a completely local lower route.
    handoff=cue(cfg,'handoff',11.8)
    lower=[(254,537),(254,576),(1024,576),(1024,538)]
    hq=progress(t,handoff,.9,cfg)
    if hq>0:
        line(im,_partial_path(lower,ease(hq)),rgba(p['secondary'],85),2)
        if hq<1:
            dx,dy=_path_point(lower,smooth(hq));circle(im,dx,dy,4,p['secondary'])
    # Persistent summary at end, with space for reading rather than a global exit.
    end=_local(t,cfg,'summary',13.2,.5)
    rr(im,(366,592,915,629),rgba(p['accent'],int(22*end)),18)
    _fitted(im,cfg.get('summary_text',PRESETS['L04']['summary_text']),640,610,512,17,p['accent'],'mono',end,'center')
    return im


@lru_cache(maxsize=64)
def _outline_word(s,size,color):
    raw=text_img(s,size,(0,0,0,0),'bold',1,color)
    return raw


def _mask_word(im,s,x,y,maxw,size,color,amount,shift=30,opacity=1):
    fs=fit_size(s,maxw,size)
    src=text_img(s,fs,color)
    overshoot=1+.025*math.sin(math.pi*amount)*(1-amount)
    if overshoot>1.002:
        src=src.resize((round(src.width*overshoot),round(src.height*overshoot)),Image.Resampling.BICUBIC)
    clip=layer(round(maxw+8),max(1,round(size*1.48)))
    top=round((clip.height-src.height)/2)
    paste(clip,src,0,top+shift*(1-amount),opacity=opacity,anchor='topleft')
    # Fixed clipping slot. Local movement never alters any neighbour's anchor.
    keep=Image.new('L',clip.size,0)
    ImageDraw.Draw(keep).rectangle((0,top,clip.width,top+src.height+4),fill=255)
    clip.putalpha(ImageChops.multiply(clip.getchannel('A'),keep))
    paste(im,clip,x,y,anchor='left')


def _l05(t,cfg):
    # This design intentionally uses a dark editorial canvas by default. Custom
    # palette remains accepted, with tonal layer strength independent of genre.
    im=base(cfg);p=palette(cfg)
    words=_list(cfg,'words',PRESETS['L05']['words'],4)
    tiles=_list(cfg,'items',PRESETS['L05']['items'],3)
    headline=cfg.get('text',PRESETS['L05']['text'])
    eyebrow=str(cfg.get('eyebrow',PRESETS['L05']['eyebrow']))
    _track(im,eyebrow,82,166,fit_size(eyebrow,770,13,'mono'),p['muted'],2.8)
    line(im,[(82,196),(1200,196)],rgba(p['muted'],45),1)
    # Background outline is subordinate and moves only a handful of pixels.
    echo=_outline_word('MOTION',158,p['muted'])
    paste(im,echo,79+5*math.sin(t*.25),490,opacity=.10,anchor='topleft')
    hstart=cue(cfg,'headline',.45)
    fs=fit_size(headline,795,91)
    x=80
    for i,word in enumerate(headline.split(' ')):
        q=progress(t,hstart+i*.10,.48,cfg)
        size=max(1,measure(word,fs)+5)
        _mask_word(im,word,x,276,size,fs,p['text'],ease(q),42,clamp(q*4))
        x+=measure(word+' ',fs)
    # Independent accent slash with a restrained overshoot, not a scene zoom.
    slash=ease(progress(t,hstart+.36,.42,cfg))
    line(im,[(81,337),(81+95*slash,337)],p['accent'],5)
    cuekeys=['keyword','replace_a','replace_b','replace_c']
    starts=[cue(cfg,k,d) for k,d in zip(cuekeys,[1.7,5.,8.4,11.6])]
    active=-1
    for i,start in enumerate(starts):
        if t>=start:active=i
    if active>=0:
        k=active;pr=progress(t,starts[k],.46,cfg)
        q=ease(pr)
        # Outgoing and incoming share a clipped keyword slot during replacement.
        slot=layer(806,143)
        if k>0 and pr<1:
            old=words[k-1];ofs=fit_size(old,796,70)
            text(slot,old,0,72-96*q,ofs,p['accent'],opacity=1-pr,anchor='left')
        fs2=fit_size(words[k],796,70)
        text(slot,words[k],0,72+96*(1-q),fs2,p['accent'],opacity=min(1,pr*4),anchor='left')
        mask=Image.new('L',slot.size,0)
        ImageDraw.Draw(mask).rectangle((0,28,805,117),fill=255)
        slot.putalpha(ImageChops.multiply(slot.getchannel('A'),mask))
        paste(im,slot,80,343,anchor='topleft')
        wordwidth=min(794,measure(words[k],fs2))
        under=ease(progress(t,starts[k]+.38,.38,cfg))
        line(im,[(81,471),(81+wordwidth*under,471)],rgba(p['accent'],180),2)
    # Side cards create activity in a controlled secondary area.
    for i,label in enumerate(tiles):
        yy=244+i*104
        q=ease(progress(t,hstart+.4+i*.19,.48,cfg))
        paste(im,panel(260,86,p['panel'],16,'',True),909-30,yy-30,opacity=q,anchor='topleft')
        circle(im,944,yy+42,18,rgba(p['accent'],18*q))
        # A rotating segmented dial is decorative, not a progress assertion.
        arc=ImageDraw.Draw(im)
        theta=(t*34+i*82)%360
        arc.arc((931,yy+29,957,yy+55),theta,theta+225,fill=rgba(p['accent'],210*q),width=2)
        _fitted(im,label,978,yy+30,169,18,p['text'],'mono',q)
        for j in range(5):
            phase=.5+.5*math.sin(t*1.8+j*.8+i)
            height=4+phase*10
            rr(im,(979+j*15,yy+59-height,985+j*15,yy+59),rgba(p['secondary'],int((70+80*phase)*q)),2)
        text(im,str(i+1).zfill(2),1148,yy+58,11,p['muted'],'mono',opacity=q,anchor='right')
    # Beat markers keep the same location during all four edits.
    for i,start in enumerate(starts):
        visited=t>=start
        rr(im,(82+i*44,520,111+i*44,525),p['accent'] if visited else rgba(p['muted'],40),2)
    sub=cfg.get('subtitle','')
    sq=ease(progress(t,starts[0]+.55,.48,cfg))
    _fitted(im,sub,82,571,1100,25,p['text'],'sans',sq)
    summary=_local(t,cfg,'summary',13.4,.5)
    _fitted(im,cfg.get('summary_text',PRESETS['L05']['summary_text']),82,615,1100,12,p['muted'],'mono',summary)
    return im


def _values(cfg,key,default):
    vals=cfg.get(key,default)
    if not isinstance(vals,(list,tuple)) or len(vals)!=3:
        raise ValueError(key+' must contain exactly three finite numbers')
    out=[float(x) for x in vals]
    if not all(math.isfinite(x) and x>=0 for x in out):
        raise ValueError(key+' values must be finite and nonnegative')
    return out


def _num(value,suffix):
    return f'{value:.0f}{suffix}'


def _l06(t,cfg):
    im=base(cfg);p=palette(cfg)
    names=_list(cfg,'items',PRESETS['L06']['items'],3)
    before=_values(cfg,'before_values',PRESETS['L06']['before_values'])
    after=_values(cfg,'after_values',cfg.get('values',PRESETS['L06']['after_values']))
    # An explicit domain is respected only when it contains every value.
    maxval=float(cfg.get('max_value',max(100,max(before+after))))
    if not math.isfinite(maxval) or maxval<=0 or maxval<max(before+after):
        raise ValueError('max_value must be positive and include all metric values')
    suffix=str(cfg.get('suffix','%'))
    _fitted(im,cfg.get('text',''),83,161,1120,37,p['text'])
    _fitted(im,cfg.get('subtitle',''),83,204,1120,14,p['muted'],'mono')
    box_y=244;box_h=288
    for x,label,color in [(82,cfg.get('before_label','SEBELUM'),p['muted']),(715,cfg.get('after_label','SELEPAS'),p['accent'])]:
        paste(im,panel(481,box_h,p['panel'],22,'',True),x-30,box_y-30,anchor='topleft')
        _fitted(im,label,x+25,box_y+27,431,16,color,'mono')
        line(im,[(x+25,box_y+51),(x+456,box_y+51)],rgba(p['muted'],35),1)
    # A fixed small comparison hub; it does not cover the chart labels.
    circle(im,640,386,26,rgba(p['accent'],15))
    arrow(im,639,386,p['accent'],.8)
    _track(im,'DEMO',614,430,10,p['muted'],1.5)
    starts=[cue(cfg,k,d) for k,d in zip(['improve_a','improve_b','improve_c'],[3.3,6.4,9.5])]
    changes=[]
    for i,(s,a,b,start) in enumerate(zip(names,before,after,starts)):
        y=320+i*76
        initial=ease(progress(t,cue(cfg,'bars',.7)+i*.17,.55,cfg))
        improve=smooth(progress(t,start,.65,cfg));changes.append(improve)
        current=mix(a,b,improve)
        for x,value,col in [(107,a,p['muted']),(740,current,p['accent'])]:
            _fitted(im,s,x,y,306,20,p['text'],'sans')
            _fitted(im,_num(value,suffix),x+430,y,110,23,col,'mono',anchor='right')
            rr(im,(x,y+25,x+430,y+34),rgba(p['muted'],32),4)
        bw=430*(a/maxval)*initial
        if bw>0:rr(im,(107,y+25,107+bw,y+34),rgba(p['muted'],115),4)
        # Original state remains visible as a muted longer/shorter reference line.
        oldw=430*a/maxval*initial
        if oldw>0:
            rr(im,(740,y+22,740+oldw,y+37),rgba(p['secondary'],35),5)
            line(im,[(740+oldw,y+19),(740+oldw,y+40)],rgba(p['secondary'],95),1)
        neww=430*(current/maxval)*initial
        if neww>0:rr(im,(740,y+25,740+neww,y+34),rgba(p['accent'],225),4)
        # Short local highlight settles while all other rows remain calm.
        if start<=t<start+.9/max(.15,float(cfg.get('tempo',1))):
            strength=math.sin(math.pi*progress(t,start,.9,cfg))
            rr(im,(727,y-21,1183,y+46),(0,0,0,0),12,rgba(p['accent'],110*strength),1)
        if improve==1:_check(im,698,y+26,p,.8,8)
    # One shared slider shows completion of three editorial steps, not performance.
    total=sum(changes)/3
    line(im,[(155,566),(1124,566)],rgba(p['muted'],65),3)
    if total>0:line(im,[(155,566),(155+969*total,566)],p['accent'],3)
    for i in range(4):
        xx=155+323*i
        circle(im,xx,566,5,p['accent'] if total>=i/3 else p['panel'],rgba(p['muted'],65),1)
    circle(im,155+969*total,566,9,p['panel'],p['accent'],2)
    _fitted(im,cfg.get('progress_label',PRESETS['L06']['progress_label']),640,590,900,12,p['muted'],'mono',anchor='center')
    end=_local(t,cfg,'summary',12.9,.46)
    rr(im,(339,607,942,637),rgba(p['accent'],int(17*end)),15)
    _fitted(im,cfg.get('summary_text',PRESETS['L06']['summary_text']),640,622,569,14,p['accent'],'mono',end,'center')
    # Four quiet accent nodes use small local travel around their own anchors.
    for i,(xx,yy) in enumerate([(66,269),(1212,279),(70,511),(1209,510)]):
        dy=2.5*math.sin(t*1.4+i)
        line(im,[(xx-3,yy+dy),(xx+3,yy+dy)],rgba(p['secondary'],80),1)
        line(im,[(xx,yy+dy-3),(xx,yy+dy+3)],rgba(p['secondary'],80),1)
    return im


def render(pid,t,cfg):
    funcs={'L04':_l04,'L05':_l05,'L06':_l06}
    if pid not in funcs:raise ValueError('Unknown preset '+pid)
    return funcs[pid](float(t),cfg)
