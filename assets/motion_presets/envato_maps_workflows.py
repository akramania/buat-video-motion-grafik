from envato_common import *

def maps(t,cfg):
    p=palette(cfg);im=base(cfg);mode=cfg['mode'];v=q(t,.1,.9)
    geo=geo_map(cfg['genre'],p['accent']);paste(im,geo,640,385,opacity=v)
    places=[('MALAYSIA',101.7,3.1),('LONDON',-.12,51.5),('NEW YORK',-74,40.7),('SYDNEY',151.2,-33.9),('TOKYO',139.7,35.7)]
    coords=[location(lon,lat) for _,lon,lat in places]
    if mode in ('map_focus','map_itinerary'):
        phase=prog(t,.8,4.6)*4;idx=min(3,int(phase));fraction=smooth(phase-idx)
        target=coords[0] if mode=='map_focus' else (mix(coords[idx][0],coords[idx+1][0],fraction),mix(coords[idx][1],coords[idx+1][1],fraction))
        z=1+q(t,.8,1.2)*.8;dx=(640-target[0])*z;dy=(385-target[1])*z
        im=base(cfg);paste(im,geo,640+dx,385+dy,scale=z,opacity=v)
        circle(im,640,385,9,p['accent']);ring(im,640,385,26,(t*.65)%1,p['accent'],rgba(p['muted'],30),3)
        tag(im,'COUNTRY FOCUS' if mode=='map_focus' else 'DESTINATION '+str(min(5,int(prog(t,.8,4.6)*4)+1)),500,560,p)
    else:
        for i,((name,lon,lat),(x,y)) in enumerate(zip(places,coords)):
            u=q(t,.5+i*.18,.5)
            if mode in ('map_region','map_metric') and i>0:continue
            circle(im,x,y,6*u,p['accent']);ring(im,x,y,14+5*math.sin(t*2),u,p['accent'],rgba(p['muted'],40),2)
            if mode in ('map_pins','map_region','map_metric','map_callout'):text(im,name,x,y+23,15,p['text'],'mono',opacity=u)
        if mode in ('map_network','map_hub','map_travel','map_itinerary'):
            for j,point in enumerate(coords[1:]):
                pts=curve(coords[0],point,80+j*9);u=q(t,.8+j*.45,1.3)
                if mode=='map_travel':
                    for k in range(0,round(len(pts)*u)-3,8):line(im,pts[k:k+4],p['text'],3)
                else:trace(im,pts,u,rgba(p['accent'],190),3)
                if u>0:
                    dot=pts[min(len(pts)-1,int(u*(len(pts)-1)))];circle(im,*dot,5,p['text'])
                    if mode=='map_hub':
                        dot=pts[int(((t*.3+j*.25)%1)*(len(pts)-1))];circle(im,*dot,4,p['secondary'])
                    if mode=='map_travel':
                        x,y=dot;line(im,[(x-11,y+4),(x+9,y-2),(x-3,y-12)],p['text'],4)
        if mode=='map_callout':
            x,y=coords[0];u=q(t,1.2,.8);line(im,[(x,y),(925,290),(980,290)],p['accent'],2)
            pic=demo_media(0).resize((230,130));paste(im,pic,980,300,opacity=u,scale=.85+.15*u)
            text(im,'DESTINATION',980,389,18,p['text'],opacity=u)
        if mode in ('map_region','map_metric'):
            u=q(t,1.2,.8);card(im,175,420,330,135,p,u)
            text(im,'REGION SNAPSHOT',340,449,18,p['muted'],opacity=u)
            text(im,formatted(cfg,q(t,1.4,1.7)),340,500,44,p['accent'],opacity=u)
            if mode=='map_metric':
                x,y=coords[0];line(im,[(505,486),(x-18,486),(x-18,y),(x,y)],p['accent'],2)
                icon(im,'pin',x,y-14,43*u,p['accent'])
            else:
                x,y=coords[0];ring(im,x,y,45,q(t,.8,1.5),p['accent'],rgba(p['muted'],15),9)
    heading(im,cfg,p);return im

def workflow(t,cfg):
    p=palette(cfg);im=base(cfg);mode=cfg['mode'];items=cfg.get('items',['INPUT','RESEARCH','PROCESS','OUTPUT'])[:4]
    if mode=='workflow_pipeline':pos=[(250,360),(640,360),(1030,360)];names=[items[0],items[2],items[3]]
    elif mode=='workflow_chain':pos=[(210,400),(500,280),(780,400),(1070,280)];names=items
    elif mode=='workflow_branch':pos=[(210,360),(520,260),(520,460),(850,360),(1090,360)];names=[items[0],'KNOWLEDGE','MEMORY',items[2],items[3]]
    elif mode=='stream_merge':pos=[(220,240+i*75) for i in range(5)]+[(970,390)];names=['ANALYTICS','PAYMENTS','CLOUD','AI','SECURITY','SYNC']
    else:pos=[(640,370),(240,260),(240,480),(1040,260),(1040,480)];names=['AI AGENT','RESEARCH','MEMORY','TOOLS','RESULT']
    if mode=='workflow_branch':edges=[(0,1),(0,2),(1,3),(2,3),(3,4)]
    elif mode=='stream_merge':edges=[(i,5) for i in range(5)]
    elif mode=='workflow_hub':edges=[(0,i) for i in range(1,5)]
    else:edges=[(i,i+1) for i in range(len(pos)-1)]
    for j,(a,b) in enumerate(edges):
        u=q(t,.5+j*.25,1.1);pts=curve(pos[a],pos[b],0 if mode!='stream_merge' else (j-2)*25)
        trace(im,pts,u,rgba(p['accent'],155),3)
        if u>.05:
            k=int(((t*.6+j*.16)%1)*u*(len(pts)-1));circle(im,*pts[k],5,p['secondary'])
    for i,((x,y),name) in enumerate(zip(pos,names)):
        u=q(t,.15+i*.17,.6);w=188 if mode!='stream_merge' else 180
        card(im,x-w/2,y-42,w,84,p,u)
        circle(im,x-w/2+22,y,6*u,p['accent'])
        text(im,name,x+9,y,fit_size(name,w-49,20),p['text'],opacity=u)
    text(im,'READY  →  PROCESSING  →  COMPLETE',640,577,22,p['muted'],'mono',opacity=q(t,2.3,.7))
    heading(im,cfg,p);return im

def planner(t,cfg):
    p=palette(cfg);im=base(cfg);mode=cfg['mode'];items=cfg.get('items',['PLAN','WRITE','REVIEW','PUBLISH'])[:4]
    if mode=='planner_calendar':
        card(im,245,198,790,398,p);text(im,'MONTH / DEMO',640,222,23,p['accent'])
        for i in range(35):
            x=282+(i%7)*106;y=270+(i//7)*60
            rr(im,(x-35,y-22,x+57,y+27),rgba(p['muted'],25),8)
            text(im,str(i+1) if i<31 else '',x-22,y-8,14,p['muted'])
            if i in (2,8,11,16,23):
                u=q(t,.5+i*.045,.55);rr(im,(x-24,y+4,x+45*u,y+20),rgba(p['accent'],180),7)
                if u>.9:text(im,items[i%4][:7],x+8,y+12,10,p['bg'])
    elif mode=='planner_ribbon':
        line(im,[(150,330),(1130,330)],rgba(p['muted'],100),3)
        for i,name in enumerate(items):
            u=q(t,.2+i*.4,.65);x=150+i*245
            rr(im,(x,340,x+225*u,440),p['accent'] if i%2==0 else p['secondary'],14)
            text(im,f'{9+i*2:02d}:00',x+113,312,21,p['text'],opacity=u)
            text(im,name,x+113,390,fit_size(name,200,23),p['bg'],opacity=u)
            text(im,f'{2+i%2}h',x+113,480,20,p['muted'],opacity=u)
        circle(im,150+980*prog(t,.8,4.5),330,7,p['text'])
    else:
        for i,name in enumerate(items):
            u=q(t,.15+i*.35,.65);y=235+i*89
            if mode in ('agenda','planner_agenda'):
                line(im,[(330,220),(330,562)],rgba(p['muted'],80),2);circle(im,330,y+28,7*u,p['accent'])
                text(im,f'{9+i*2:02d}:00',258,y+28,24,p['muted'],'mono',opacity=u)
                card(im,385,y,600,62,p,u);text(im,name,685,y+31,28,p['text'],opacity=u)
                if mode=='planner_agenda':
                    bar=q(t,.8+i*.35,1.4);rr(im,(390,y+55,390+575*bar,y+61),p['accent'],3)
                    text(im,f'{round(100*bar)}%',1030,y+31,24,p['accent'],opacity=u)
            else:
                card(im,255,y,770,66,p,u);circle(im,310,y+33,14,None,p['muted'],2)
                done=q(t,1.2+i*.55,.3)
                if done>.5:check(im,310,y+33,p['accent'])
                text(im,name,370,y+33,28,p['text'],opacity=u,anchor='left')
                if done>0:line(im,[(370,y+33),(370+measure(name,28)*done,y+33)],rgba(p['accent'],180),2)
    heading(im,cfg,p);return im
