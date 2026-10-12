from envato_common import *

def charts(t,cfg):
    p=palette(cfg);im=base(cfg);mode=cfg['mode'];vals=[float(x) for x in cfg.get('values',[38,68,49,84,61,93])[:6]]
    if not vals or any(not math.isfinite(x) or x<0 for x in vals):raise ValueError('Chart values must be finite and nonnegative')
    n=len(vals);maxv=max(100,max(vals),1);colors=[p['accent'],p['secondary'],'#F58EA6','#E7C86D','#7CCA9D','#A890E4']
    if mode=='chart_mini':
        other=dict(cfg);other.update(mode='chart_area',text='',subtitle='')
        small=charts(t,other).resize((700,394));paste(im,small,510,390)
        card(im,820,260,330,245,p)
        text(im,'REVENUE',985,310,22,p['muted'])
        text(im,formatted(cfg,q(t,.4,1.8)),985,388,fit_size(formatted(cfg,1),295,53),p['accent'])
        text(im,'+18.2%',985,453,28,p['text']);heading(im,cfg,p);return im
    if mode in ('radar','radar_profile'):
        center=(640,382);radius=167;d=ImageDraw.Draw(im)
        for r in (40,80,120,160):
            pts=[(640+r*math.cos(i*math.tau/n-math.pi/2),382+r*math.sin(i*math.tau/n-math.pi/2)) for i in range(n)]
            line(im,pts+[pts[0]],rgba(p['muted'],55),2)
        pts=[]
        for i,val in enumerate(vals):
            a=i*math.tau/n-math.pi/2;u=q(t,.35+i*.07,1.4);r=radius*val/maxv*u
            pts.append((640+r*math.cos(a),382+r*math.sin(a)))
            x=640+202*math.cos(a);y=382+202*math.sin(a)
            text(im,cfg.get('labels',['JAN','FEB','MAR','APR','MAY','JUN'])[i],x,y,18,p['text'])
        l=layer();ImageDraw.Draw(l).polygon(pts,fill=rgba(p['accent'],50));im.alpha_composite(l);line(im,pts+[pts[0]],p['accent'],4)
        for x,y in pts:circle(im,x,y,5,p['text'])
        if mode=='radar_profile':
            shifted=base(cfg);paste(shifted,im,780,385,scale=.82)
            card(shifted,155,230,250,325,p);icon(shifted,'person',280,340,120,p['accent'])
            text(shifted,'TEAM PROFILE',280,453,22,p['text']);text(shifted,'SKILL DEMO',280,496,16,p['muted'],'mono');im=shifted
        heading(im,cfg,p);return im
    if mode in ('nested_rings','profile_rings','donut','pie_legend'):
        if mode in ('nested_rings','profile_rings'):
            for i,val in enumerate(vals[:3]):ring(im,500,380,150-i*31,val/maxv*q(t,.4+i*.2,1.7),colors[i],rgba(p['muted'],35),18)
            if mode=='profile_rings':
                icon(im,'person',500,380,100,p['text'])
                for i,val in enumerate(vals[:3]):
                    y=315+i*80;line(im,[(750,y),(1050,y)],rgba(p['muted'],80),5);line(im,[(750,y),(750+300*val/maxv*q(t,.5+i*.2,1.5),y)],colors[i],5);circle(im,750+300*val/maxv*q(t,.5+i*.2,1.5),y,8,p['text'])
            else:text(im,'PROGRESS',500,380,25,p['text'])
        else:
            d=ImageDraw.Draw(im);total=sum(vals) or 1;angle=-90
            for i,val in enumerate(vals):
                sweep=val/total*360*q(t,.25+i*.2,1.4)
                if sweep>0:d.pieslice((340,218,660,538),angle,angle+sweep,fill=colors[i])
                angle+=val/total*360
            if mode=='donut':circle(im,500,378,104,p['bg']);text(im,'TRAFFIC',500,378,25,p['text'])
            for i,val in enumerate(vals):
                y=237+i*55;u=q(t,.7+i*.15,.5);rr(im,(775,y-10,794,y+10),colors[i],4)
                text(im,f'{cfg.get("labels",["JAN","FEB","MAR","APR","MAY","JUN"])[i]}  {val:g}',820,y,23,p['text'],anchor='left',opacity=u)
        heading(im,cfg,p);return im
    if mode=='funnel':
        d=ImageDraw.Draw(im)
        for i,val in enumerate(sorted(vals,reverse=True)[:5]):
            u=q(t,.2+i*.25,1.2);y=230+i*62;w=(460-i*68)*u
            d.polygon([(640-w/2,y),(640+w/2,y),(640+(w-35*u)/2,y+49),(640-(w-35*u)/2,y+49)],fill=colors[i])
            text(im,f'STAGE {i+1}',985,y+25,21,p['text'],opacity=u)
            text(im,f'{round(val*u)}%',640,y+25,24,p['bg'],opacity=u)
        heading(im,cfg,p);return im
    if mode in ('rank_bars','rank_steps','social_rank','butterfly','mirror_bars'):
        for i,val in enumerate(vals):
            y=228+i*58;u=q(t,.35+i*.13,1.6)
            if mode=='butterfly':
                width=380*val/maxv*u;width2=380*vals[-i-1]/maxv*u
                rr(im,(630-width,y,630,y+28),p['accent'],4);rr(im,(650,y,650+width2,y+28),p['secondary'],4)
                text(im,str(i+1),640,y+14,14,p['text'])
            elif mode=='mirror_bars':
                x=200+i*165;h=135*val/maxv*u;rr(im,(x-20,390-h,x+20,390),colors[i],3);rr(im,(x-20,412,x+20,412+h*.8),rgba(colors[i],150),3);text(im,cfg.get('labels',['JAN','FEB','MAR','APR','MAY','JUN'])[i],x,582,18,p['text'])
            else:
                x=310+(i*10 if mode=='rank_steps' else 0);ww=680*val/maxv*u
                text(im,cfg.get('labels',['JAN','FEB','MAR','APR','MAY','JUN'])[i],240,y+14,21,p['muted'],'mono')
                rr(im,(x,y,1060,y+28),rgba(p['muted'],25),7);rr(im,(x,y,x+ww,y+28),colors[i] if mode=='social_rank' else p['accent'],7)
                text(im,f'{val*u:.0f}',1105,y+14,23,p['text'])
        heading(im,cfg,p);return im
    left,right,top,bottom=200,1080,220,555
    for i in range(5):
        y=mix(bottom,top,i/4);line(im,[(left,y),(right,y)],rgba(p['muted'],40),1);text(im,str(round(i*maxv/4)),left-45,y,17,p['muted'],'mono')
    labels=cfg.get('labels',['JAN','FEB','MAR','APR','MAY','JUN'])
    for i in range(n):text(im,labels[i],mix(left+50,right-50,i/max(1,n-1)),bottom+27,18,p['muted'],'mono')
    area=mode in ('chart_area','chart_mini','chart_dual');lines=area or mode in ('chart_elegant','doc_line','chart_mixed')
    if lines:
        for series in range(2 if mode in ('chart_dual','chart_elegant') else 1):
            values=vals if series==0 else [maxv*.25+z*.35 for z in reversed(vals)]
            pts=[]
            for i in range(n-1):
                for s in np.linspace(0,1,18):
                    value=mix(values[i],values[i+1],smooth(s));x=mix(left+50,right-50,(i+s)/(n-1));y=bottom-(bottom-top)*value/maxv
                    pts.append((x,y))
            if n==1:pts=[(left+50,bottom),(right-50,bottom-(bottom-top)*vals[0]/maxv)]
            u=q(t,.4+series*.25,1.8);pts=pts[:max(2,round(len(pts)*u))]
            if area:
                fill=layer();ImageDraw.Draw(fill).polygon(pts+[(pts[-1][0],bottom),(pts[0][0],bottom)],fill=rgba(colors[series],55));im.alpha_composite(fill)
            if mode=='chart_elegant':
                for z in range(len(pts)-1):
                    rgbc=tuple(round(mix(a,b,z/max(1,len(pts)-1))) for a,b in zip(rgb(colors[series]),rgb(colors[(series+1)%2])))
                    line(im,pts[z:z+2],rgbc,4)
            else:line(im,pts,colors[series],4)
            if mode=='doc_line':
                for i,val in enumerate(values):
                    if u>i/max(1,n-1):circle(im,mix(left+50,right-50,i/max(1,n-1)),bottom-(bottom-top)*val/maxv,6,p['secondary'])
            if u>.85 and mode in ('chart_area','chart_mini','chart_dual'):
                idx=min(len(pts)-1,int(len(pts)*(.45+.15*math.sin(t*.8))));x,y=pts[idx]
                line(im,[(x,top),(x,bottom)],rgba(p['text'],65),2);circle(im,x,y,6,p['text'])
                rr(im,(x-59,y-56,x+59,y-20),p['panel'],8);text(im,f'{(bottom-y)/(bottom-top)*maxv:.1f}',x,y-38,21,p['text'])
    else:
        for i,val in enumerate(vals):
            u=q(t,.35+i*.14,1.8);x=mix(left+50,right-50,i/max(1,n-1));height=(bottom-top)*val/maxv*u
            if mode=='chart_candle':
                lo=height*.5;hi=height;line(im,[(x,bottom-hi-22),(x,bottom-lo+25)],colors[i%2],3);rr(im,(x-19,bottom-hi,x+19,bottom-lo),colors[i%2],1)
            elif mode=='chart_lollipop':line(im,[(x,bottom),(x,bottom-height)],p['accent'],3);circle(im,x,bottom-height,9,p['secondary'])
            elif mode=='doc_bars':
                rr(im,(x-34,bottom-height,x-3,bottom),p['accent'],1);rr(im,(x+4,bottom-height*.72,x+35,bottom),p['secondary'],1)
            elif mode in ('chart_stacked','chart_spending'):
                rr(im,(x-25,bottom-height*.45,x+25,bottom),p['accent'],1);rr(im,(x-25,bottom-height,x+25,bottom-height*.45),p['secondary'],1)
                if mode=='chart_stacked':rr(im,(x-25,bottom-height*.7,x+25,bottom-height*.45),colors[2],1)
            else:rr(im,(x-25,bottom-height,x+25,bottom),colors[i] if mode=='social_columns' else p['accent'],6)
            if u>.05:text(im,str(round(val*u)),x,bottom-height-20,21,p['text'])
    if mode=='chart_mixed':
        for i,val in enumerate(vals):
            x=mix(left+50,right-50,i/max(1,n-1));h=(bottom-top)*val/maxv*.65*q(t,.8+i*.12,1.5)
            rr(im,(x-22,bottom-h,x+22,bottom),rgba(p['secondary'],95),2)
    heading(im,cfg,p);return im
