from envato_common import *

def counters(t,cfg):
    p=palette(cfg);im=base(cfg);mode=cfg['mode'];u=q(t,.3,2.4)
    c=dict(cfg)
    if mode in ('counter_currency','counter_decimal','counter_neon','counter_block'):c['prefix']=cfg.get('prefix') or 'RM '
    if mode in ('counter_discount','counter_capsule'):c.update(to_value=cfg.get('to_value',70) if cfg.get('to_value',12500)!=12500 else 70,suffix=cfg.get('suffix') or '%')
    if mode=='counter_decimal':c['decimals']=cfg.get('decimals') or 2
    value=formatted(c,u,mode=='counter_compact');fs=fit_size(value,960,112)
    if mode=='counter_ring':
        ring(im,365,365,112,.87*u,p['accent'],rgba(p['muted'],45),18)
        text(im,f'{round(87*u)}%',365,365,61,p['text']);text(im,value,805,365,fit_size(value,520,87),p['text'])
    elif mode=='counter_social':
        for i,k in enumerate(('heart','chat','person')):
            x=340+i*300;v=q(t,.3+i*.35,1.9);rr(im,(x-128,310,x+128,430),p['panel'],24)
            icon(im,k,x-80,370,55,p['accent']);text(im,formatted(c,v),x+31,370,fit_size(value,145,38),p['text'])
    else:
        if mode in ('counter_capsule','counter_block'):
            ww=measure(value,fs)+95;rr(im,(640-ww/2,300,640+ww/2,439),p['accent'] if mode=='counter_block' else None,32,p['accent'],3)
        if mode=='counter_neon':
            glow=text_img(value,fs,p['accent']);paste(im,glow.filter(ImageFilter.GaussianBlur(13)),640,366,opacity=.8)
        if mode=='counter_decimal':
            final=formatted(c,1);size=fit_size(final,960,112);xx=640-measure(final,size)/2
            window=layer(1000,155);start=500-measure(value,size)/2
            f=font(size);ref=f.getbbox('0');top=77-(ref[1]+ref[3])/2
            draw=ImageDraw.Draw(window)
            for j,ch in enumerate(value):
                ww=measure(ch,size);dy=(1-u)*math.sin(t*20+j)*75 if ch.isdigit() else 0
                # Use a shared baseline so decimal points and commas stay below digits.
                draw.text((start,top+dy),ch,font=f,fill=p['text']);start+=ww
            paste(im,window,640,366)
        else:text(im,value,640,366,fs,p['bg'] if mode=='counter_block' else p['accent'] if mode in ('counter_neon','counter_discount') else p['text'])
        if mode=='counter_strike':
            ww=measure(value,fs);rr(im,(640-ww/2,354,640-ww/2+ww*q(t,.7,1.3),378),p['bg'],0)
            text(im,'MEASURED PROGRESS',640,366,18,p['accent'],'mono',opacity=q(t,1,.4))
        if mode=='counter_badge':
            circle(im,935,266,54,p['panel']);text(im,'+24%',935,266,28,p['accent'],opacity=q(t,.8,.6))
        if mode=='counter_trend':
            pts=[(910,437),(950,413),(979,427),(1020,380)];trace(im,pts,q(t,1,.9),p['accent'],6)
        if mode in ('counter_currency','counter_decimal','counter_compact'):
            rr(im,(325,470,325+630*u,478),p['accent'],4)
    status=cfg.get('status_label','FINAL VALUE LOCKED' if cfg.get('_labels') else '')
    text(im,status,640,555,17,p['muted'],'mono',opacity=q(t,2.7,.5));heading(im,cfg,p);return im

def widgets(t,cfg):
    p=palette(cfg);mode=cfg['mode'];isglass=mode.startswith('glass')
    im=glass_background(cfg['genre'],p['bg'],p['accent']).copy() if isglass else base(cfg)
    u=q(t,.2,.8);body=layer();box=(260,200,1020,570)
    if isglass:glass(body,box,p)
    else:card(body,260,200,760,370,p)
    values=cfg.get('values',[38,68,49,84,61,93])[:6];v=q(t,.75,1.8)
    if mode in ('glass_bars','glass_balance'):
        if mode=='glass_bars':
            for i,val in enumerate(values):
                x=360+i*111;h=175*clamp(float(val)/100)*q(t,.7+i*.12,1.4)
                rr(body,(x-19,510-h,x+19,510),p['accent'] if i%2==0 else p['secondary'],12)
                text(body,cfg.get('labels',['JAN','FEB','MAR','APR','MAY','JUN'])[i],x,539,15,p['muted'])
        else:
            pts=[(315+i*10,492-70*math.sin(i*.055)-i*1.2) for i in range(65)]
            trace(body,pts,v,p['accent'],5);text(body,formatted(cfg,v),370,295,51,p['text'],anchor='left')
            text(body,'BALANCE',320,243,18,p['muted'],anchor='left')
    elif mode in ('glass_ring','glass_status'):
        ring(body,475,387,105,.87*v,p['accent'],rgba(p['muted'],65),17);text(body,f'{round(87*v)}%',475,387,67,p['text'])
        if mode=='glass_status':
            for i,s in enumerate(('INPUT RECEIVED','PROCESSING','COMPLETE')):
                r=q(t,1+i*.7,.3);circle(body,690,317+i*67,12,p['panel'],p['muted'],1)
                if r>.5:check(body,690,317+i*67,p['accent'])
                text(body,s,721,317+i*67,21,p['text'],anchor='left',opacity=.35+.65*r)
        else:text(body,'TARGET PROGRESS',777,387,26,p['text'])
    elif mode=='glass_media':
        text(body,'PLAYING / TRACK 01',640,285,29,p['text']);icon(body,'screen',640,385,65,p['accent'])
        for x,word in [(460,'PREV'),(640,'PAUSE'),(820,'NEXT')]:text(body,word,x,439,21,p['text'])
        rr(body,(340,510,940,519),rgba(p['muted'],80),5);rr(body,(340,510,340+600*prog(t,.8,4.6),519),p['accent'],5)
    elif mode=='glass_metric':
        text(body,formatted(cfg,v),640,385,fit_size(formatted(cfg,v),650,104),p['text'])
        text(body,'CURRENT TOTAL',640,480,22,p['accent'])
    elif mode=='widget_goal':
        text(body,formatted(cfg,v),390,325,64,p['text'],anchor='left');text(body,'MONTHLY GOAL',340,245,24,p['muted'],anchor='left')
        rr(body,(340,425,940,449),rgba(p['muted'],60),12);rr(body,(340,425,340+600*.84*v,449),p['accent'],12)
        text(body,f'{round(84*v)}% COMPLETE',340,502,23,p['accent'],anchor='left')
    elif mode=='widget_revenue':
        icon(body,'screen',371,310,60,p['accent']);text(body,formatted(cfg,v),705,347,fit_size(formatted(cfg,v),475,88),p['accent'])
        text(body,'+18.2%  THIS MONTH',640,490,27,p['text'],opacity=q(t,1.6,.5))
    elif mode=='kpi_stack':
        body=layer()
        for i,label in enumerate(('HOURS SAVED','WORKFLOWS','COUNTRIES')):
            z=q(t,.15+i*.45,.65);card(body,360,213+i*113,560,87,p,z)
            text(body,str(round((12+i*16)*q(t,.6+i*.4,1.2))),442,256+i*113,39,p['accent'],opacity=z)
            text(body,label,700,256+i*113,24,p['text'],opacity=z)
    elif mode=='automation_bars':
        for i,val in enumerate((93,61)):
            y=327+i*135;v=q(t,.6+i*.5,1.4);text(body,['AUTOMATED','MANUAL'][i],350,y-48,24,p['text'],anchor='left')
            rr(body,(340,y,940,y+23),rgba(p['muted'],60),12);rr(body,(340,y,340+600*val/100*v,y+23),p['accent'] if i==0 else p['secondary'],12)
            text(body,f'{round(val*v)}%',965,y+12,28,p['text'])
    paste(im,body,640,360+20*(1-u),opacity=u,scale=.95+.05*u)
    heading(im,cfg,p);return im
