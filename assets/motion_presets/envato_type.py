from envato_common import *

def lines_for(s,n=3):
    if '\n' in s:return s.split('\n')[:5]
    words=s.split();chunk=max(1,math.ceil(len(words)/n))
    return [' '.join(words[i:i+chunk]) for i in range(0,len(words),chunk)][:5] or ['IDEA']

def typography(t,cfg):
    p=palette(cfg);im=base(cfg);mode=cfg['mode'];s=cfg.get('text','SMALL STEPS BIG IDEAS');words=s.split();u=q(t,.2,1.1)
    if mode in ('type_glow','type_delete','type_finish','type_code'):
        if mode=='type_code':
            lines=cfg.get('code_lines',['input = receive()','result = process(input)','publish(result)'])[:4]
            for i,sline in enumerate(lines):
                a=prog(t,.25+i*.62,1.25+i*.62);visible=sline[:round(len(sline)*a)];text(im,visible,260,280+i*77,fit_size(sline,800,35,'mono'),p['text'],'mono',anchor='left')
                if a<1 and a>0:rr(im,(260+measure(visible,35,'mono'),261+i*77,266+measure(visible,35,'mono'),302+i*77),p['accent'],1)
        else:
            shown=s[:round(len(s)*prog(t,.3,2.5))]
            if mode=='type_delete':
                draft=cfg.get('draft','START HERE')
                shown=draft[:round(len(draft)*q(t,.1,.8))] if t<1.1 else draft[:round(len(draft)*(1-prog(t,1.1,1.75)))] if t<1.75 else s[:round(len(s)*prog(t,1.85,3.5))]
            fs=fit_size(s,990,59,'sans');ww=measure(s,fs,'sans');x=640-ww/2
            if mode=='type_finish':
                visible_len=len(shown);offset=0
                for word in words:
                    w=measure(word+' ',fs,'sans')
                    if visible_len>=offset+len(word):rr(im,(x+measure(s[:offset],fs,'sans')-3,335,x+measure(s[:offset],fs,'sans')+w-4,393),rgba(p['accent'],180),3)
                    offset+=len(word)+1
            if mode=='type_finish':
                cursor=x;offset=0
                for word in s.split(' '):
                    visible=shown[offset:offset+len(word)]
                    text(im,visible,cursor,364,fs,'#17202C' if len(shown)>=offset+len(word) else p['text'],'sans',anchor='left')
                    cursor+=measure(word+' ',fs,'sans');offset+=len(word)+1
            else:text(im,shown,x,364,fs,p['text'],'sans',anchor='left')
            if mode!='type_finish' and (int(t*4)%2==0 or t<2.5):
                xx=x+measure(shown,fs,'sans')+8;caret=layer();rr(caret,(xx,336,xx+7,391),p['accent'],2)
                im.alpha_composite(caret.filter(ImageFilter.GaussianBlur(11)));im.alpha_composite(caret)
    elif mode in ('type_marker','type_serif','type_erase','type_side','type_accent','type_label'):
        ls=lines_for(s);fs=min(64,min(fit_size(z,930,64) for z in ls));spacing=fs+21
        for i,row in enumerate(ls):
            tokens=row.split();width=sum(measure(w+' ',fs,'serif' if (j+i)%2 and mode in ('type_serif','type_marker') else 'bold') for j,w in enumerate(tokens));x=220 if mode=='type_side' else 640-width/2;y=355+(i-(len(ls)-1)/2)*spacing
            for j,w in enumerate(tokens):
                face='serif' if (j+i)%2 and mode in ('type_serif','type_marker') else 'bold';ww=measure(w,fs,face);v=q(t,.15+(i*3+j)*.11,.65);active=(j+i)%2==1
                if mode=='type_erase':v*=1-prog(t,3.5+(len(tokens)-j)*.1,4.35+(len(tokens)-j)*.1)
                if active and mode in ('type_marker','type_serif','type_label'):
                    wipe=q(t,.7+(i*3+j)*.12,.65);rr(im,(x-3,y-fs*.49,x+ww*wipe+4,y+fs*.5),p['accent'],2)
                color=p['accent'] if active and mode=='type_accent' else '#17202C' if active and mode in ('type_marker','type_label','type_serif') else p['text']
                text(im,w,x,y+(1-v)*(46 if mode=='type_serif' else 22),fs,color,face,opacity=v,anchor='left',angle=(1-v)*-12 if mode=='type_serif' else 0);x+=ww+measure(' ',fs,face)
    elif mode in ('hook_orbit','hook_number'):
        if mode=='hook_orbit':
            for i in range(7):
                a=i*math.tau/7+.12*math.sin(t);r=190+30*(1-u);x=640+r*math.cos(a);y=378+r*math.sin(a)
                circle(im,x,y,28*u,p['panel'],p['accent'],2);icon(im,['screen','clock','chat','pin'][i%4],x,y,30*u,p['accent'])
            text(im,s,640,378,fit_size(s,285,44),p['text'],opacity=u)
        else:
            text(im,formatted(cfg,q(t,.2,2)),640,322,fit_size(formatted(cfg,1),930,131),p['accent']);text(im,s,640,472,fit_size(s,920,49),p['text'],opacity=q(t,1.2,.7))
    elif mode in ('type_box','type_window','type_tracking'):
        fs=fit_size(s,880 if mode=='type_window' else 1010,81);ww=measure(s,fs);left=640-ww/2
        if mode=='type_box':
            rr(im,(640-(ww/2+22)*u,301,640+(ww/2+22)*u,431),None,0,p['text'],4)
            src=text_img(s,fs,p['text']);paste(im,crop_reveal(src,u,'left'),640,366)
        elif mode=='type_window':
            rr(im,(175,313,1105,415),p['text'],0)
            src=text_img(s,fs,p['bg']);mask=layer(930,102);paste(mask,src,465,51+100*(1-u))
            paste(im,mask,640,364)
        else:
            glyphs=list(s);size=fit_size(s,850,58);full=measure(s,size);x=640-full/2
            for i,ch in enumerate(glyphs):
                target=x+measure(ch,size)/2;dx=(i-(len(glyphs)-1)/2)*8*(1-u)
                text(im,ch,target+dx,365,size,p['text'],opacity=u);x+=measure(ch,size)
            rr(im,(210,426,210+860*q(t,.7,1),433),p['accent'],2)
    else:
        ls=lines_for(s,5 if mode=='type_tower' else 3);sizes=[fit_size(z,970,70 if mode!='type_tower' else 54) for z in ls];spacing=76 if mode!='type_tower' else 66
        for i,(row,fs) in enumerate(zip(ls,sizes)):
            y=372+(i-(len(ls)-1)/2)*spacing;v=q(t,.2+i*.17,.9);angle=0;scale=1;dx=0;dy=0;face='bold';color=p['text'];src=None
            if mode=='type_weight':face='sans' if i%2 else 'bold';dy=(1-v)*55
            elif mode=='type_compress':scale=max(.01,v);src=text_img(row,fs,color);src=src.resize((max(1,round(src.width*(.35+.65*v))),max(1,round(src.height*(1.7-.7*v)))),Image.Resampling.BICUBIC)
            elif mode=='type_glitch':
                dx=(1-v)*math.sin(t*75+i)*18
                if v<.99:
                    text(im,row,640+dx+10*(1-v),y,fs,'#F15C72',opacity=v);text(im,row,640+dx-10*(1-v),y,fs,'#4ACFE4',opacity=v)
            elif mode=='type_tower':dy=(1-v)*70;scale=.8+.2*v
            elif mode in ('type_redstack','type_slant','type_tags','type_stencil'):
                ww=measure(row,fs);strip=layer(ww+24,fs+22)
                fill=p['accent'] if i%2 else p['text'];ink=p['bg'];rr(strip,(0,0,ww+24,fs+22),fill,0);text(strip,row,(ww+24)/2,(fs+22)/2,fs,ink)
                src=crop_reveal(strip,v,'left');angle=(-7 if i%2 else 5)*(v if mode=='type_slant' else (1-v));dx=(-1 if i%2 else 1)*110*(1-v)
                if mode=='type_tags':dx+=(-1 if i%2 else 1)*45;angle=(-4 if i%2 else 4)
                if mode=='type_stencil':
                    # Reveal narrow stencil bands, then settle into the solid strip.
                    if v<.95:
                        d=ImageDraw.Draw(src)
                        for k in range(0,src.width,29):d.rectangle((k,0,k+round((1-v)*12),src.height),fill=(0,0,0,0))
            elif mode=='type_inset':
                scale=(1.8-0.8*v) if i==0 else v;fs=round(fs*(1.25 if i==0 else .85))
                if i==0:rr(im,(200,240,1080,418),p['accent'],0)
                color=p['bg'] if i==0 else p['text'];dy=30 if i==0 else 80
            elif mode=='type_flip':
                src=text_img(row,fs,color);src=src.resize((src.width,max(1,round(src.height*abs(math.cos((1-v)*math.pi))))));dy=(1-v)*40
            elif mode=='type_gradient':
                ww=measure(row,fs)+30;strip=layer(ww,fs+26);d=ImageDraw.Draw(strip)
                for xx in range(strip.width):d.line((xx,0,xx,strip.height),fill=tuple(round(mix(a,b,xx/strip.width)) for a,b in zip(rgb(p['accent']),rgb(p['secondary']))))
                text(strip,row,ww/2,(fs+26)/2,fs,p['bg']);src=crop_reveal(strip,v)
            elif mode=='type_outline':
                src=text_img(row,fs,(0,0,0,0),stroke=2,stroke_color=p['text'])
                text(im,row,640+28*(1-v),y+14*(1-v),fs,p['accent'],opacity=(1-v)*.8)
            elif mode=='type_scribble':
                pts=[(180+j*18,y+30+math.sin(j*1.7)*14) for j in range(52)];trace(im,pts,q(t,.6+i*.17,.8),p['accent'],3);dy=(1-v)*35
            if src is None:src=text_img(row,fs,color,face)
            paste(im,src,640+dx,y+dy,opacity=v,scale=max(.001,scale),angle=angle)
    if cfg.get('show_titles',cfg.get('_labels',False)):
        c=dict(cfg);c['text']=cfg['name'];heading(im,c,p)
    return im
