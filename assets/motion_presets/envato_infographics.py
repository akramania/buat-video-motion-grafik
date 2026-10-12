from envato_common import *

def infographics(t,cfg):
    p=palette(cfg);im=base(cfg);mode=cfg['mode'];items=cfg.get('items',['PLAN','CREATE','REVIEW','PUBLISH'])[:4]
    if mode=='people_compare':
        for row,value in enumerate((15,35,65)):
            y=260+row*115;u=q(t,.3+row*.4,1.5)
            for i in range(20):icon(im,'person',300+i*31,y,27,p['accent'] if i<round(20*value/100*u) else rgba(p['muted'],85))
            text(im,f'{round(value*u)}%',1040,y,54,p['text'])
            text(im,['GROUP A','GROUP B','GROUP C'][row],248,y+40,16,p['muted'],'mono',anchor='left')
    elif mode=='people_grid':
        for i in range(40):
            x=340+i%10*66;y=263+i//10*85;u=q(t,.12+i*.04,.45)
            color=p['accent'] if i<round(40*.65*q(t,.8,1.6)) else rgba(p['muted'],100)
            icon(im,'person',x,y,50*u,color)
        text(im,f'{round(65*q(t,.8,1.6))}%',1030,380,78,p['text']);text(im,'OF 40 UNITS',1030,451,18,p['muted'],'mono')
    elif mode=='icon_matrix':
        for i in range(16):
            x=390+i%4*165;y=225+i//4*103;u=q(t,.12+i*.08,.6)
            circle(im,x,y,36*u,rgba(p['accent'],28));icon(im,['clock','screen','pin','chat'][i%4],x,y,44*u,p['accent'])
    elif mode.startswith('icon_'):
        k=mode.split('_')[1];u=pop(prog(t,.2,1.1));icon(im,k,640,369,210*max(.01,u),p['accent'])
        if k=='megaphone':
            for i in range(3):
                r=q(t,.8+i*.15,.5);x=795+i*45;line(im,[(x,315-20*i),(x+30*r,292-25*i)],p['secondary'],5);line(im,[(x,395+20*i),(x+30*r,420+25*i)],p['secondary'],5)
        elif k=='clock':
            a=t*math.tau*.35;line(im,[(640,369),(640+69*math.sin(a),369-69*math.cos(a))],p['text'],6)
        elif k=='screen':
            for i in range(4):
                x=580+i*39;h=(35+i*12)*q(t,.7+i*.14,1.1);rr(im,(x-11,403-h,x+11,403),p['secondary'],2)
        elif k=='pie':ring(im,640,369,135,q(t,.4,2),p['secondary'],rgba(p['muted'],30),10)
    elif mode.startswith('compare'):
        if mode=='compare_pills':
            for i in range(4):
                u=q(t,.2+i*.32,.6);y=251+i*81
                for side,x,col in [(0,430,p['accent']),(1,850,p['secondary'])]:
                    rr(im,(x-162,y,x+162,y+55),rgba(col,35),27,col,2)
                    text(im,(items[i] if side==0 else ['COST','TIME','COMPLEXITY','RISK'][i]),x,y+27,23,col,opacity=u)
            text(im,'PROS',430,204,25,p['accent']);text(im,'CONS',850,204,25,p['secondary'])
        elif mode=='compare_ladder':
            for i in range(4):
                y=246+i*83;u=q(t,.2+i*.36,.6)
                for j,x in enumerate((400,880)):
                    rr(im,(x-150,y,x+150,y+60),p['accent'] if j==0 else p['panel'],13,p['secondary'] if j else None,2)
                    text(im,(items[i] if j==0 else ['COST','TIME','SUPPORT','RISK'][i]),x,y+30,25,p['bg'] if j==0 else p['text'],opacity=u)
                    text(im,str(i+1).zfill(2),x+124,y+14,11,p['bg'] if j==0 else p['muted'])
        else:
            for side,x in enumerate((270,685)):
                u=q(t,.25+side*.25,.75);card(im,x,223,325,340,p,u)
                text(im,['BENEFITS','LIMITATIONS'][side],x+162,259,24,p['accent'] if not side else p['secondary'],opacity=u)
                if mode=='compare_media':
                    pic=demo_media(side).resize((275,166));paste(im,pic,x+162,380,opacity=u)
                    text(im,items[side],x+162,513,26,p['text'],opacity=q(t,1.2+side*.3,.6))
                else:
                    for i,s in enumerate(items):
                        v=q(t,.65+i*.3+side*.15,.5);check(im,x+34,319+i*59,p['accent'] if not side else p['secondary']);text(im,s,x+68,319+i*59,fit_size(s,230,23),p['text'],anchor='left',opacity=v)
    elif mode=='timeline_history':
        line(im,[(500,215),(500,565)],rgba(p['muted'],100),3)
        for i,s in enumerate(items):
            y=241+i*96;u=q(t,.2+i*.4,.7);circle(im,500,y,10*u,p['accent']);text(im,str(2023+i),420,y,29,p['accent'],opacity=u)
            card(im,565,y-30,430,62,p,u);text(im,s,780,y,fit_size(s,380,27),p['text'],opacity=u)
    elif mode in ('doc_history','process_steps'):
        y=365;line(im,[(185,y),(1095,y)],rgba(p['muted'],90),3)
        for i,s in enumerate(items):
            x=205+i*290;u=q(t,.2+i*.4,.75);circle(im,x,y,12*u,p['accent']);above=i%2==0
            yy=265 if above else 473;line(im,[(x,y),(x,yy)],rgba(p['muted'],100),2)
            if mode=='doc_history':
                icon(im,'screen',x,yy,65*u,p['text']);text(im,str(1990+i*10),x,yy+55 if above else yy-60,26,p['accent'],opacity=u)
            else:
                card(im,x-110,yy-37,220,74,p,u);text(im,s,x,yy,fit_size(s,180,24),p['text'],opacity=u)
    else:raise ValueError('Unknown infographic '+mode)
    heading(im,cfg,p);return im

def matches(t,cfg):
    p=palette(cfg);im=base(cfg);mode=cfg['mode'];paper=layer(1040,390);d=ImageDraw.Draw(paper);d.rectangle((0,0,1040,390),fill='#F0ECDF')
    shot=min(3,int(prog(t,.35,4.5)*4));ink='#292C30';accent='#E3EA56'
    if mode=='match_feature':
        d.ellipse((330,20,710,500),fill=['#B6C5D1','#D3B1B3','#B3C5AB','#CCC0A5'][shot])
        # The eye positions stay locked while a different original face silhouette appears.
        for x in (445,595):d.ellipse((x-32,136,x+32,163),fill=ink)
        d.line((478,270,562,270),fill=ink,width=6)
        rr(paper,(325,107,715,191),None,0,accent,4)
    elif mode=='match_map':
        rng=random.Random(shot+124)
        for i in range(10):
            pts=[(rng.randrange(1040),rng.randrange(390)) for _ in range(4)];line(paper,pts,'#C2BCA9',2)
        circle(paper,520,195,7,ink);rr(paper,(540,165,820,209),accent,1);text(paper,'TARGET LOCATION',680,188,23,ink,'serif')
    elif mode=='match_headline':
        text(paper,['NEWS / A','REPORT / B','REVIEW / C','NOTES / D'][shot],520,61,18,ink,'serif')
        rr(paper,(255,128,785,185),accent,0);text(paper,'ONE SHARED IDEA',520,157,43,ink,'serif')
        text(paper,['Shapes our next step','Connects different stories','Changes how we think','Remains the common thread'][shot],520,221,28,ink,'serif')
    else:
        for i in range(11):
            x=25+(shot%2)*-45;y=24+i*34
            s=['Research gives context to every decision.','Evidence helps us understand a shared idea.','Small observations create a clearer story.'][(i+shot)%3]
            text(paper,s,x,y,23,ink,'serif',anchor='left')
        rr(paper,(320,157,720,209),accent,0);text(paper,'SHARED IDEA',520,183,38,ink,'serif')
    paste(im,paper,640,386,scale=1+.015*math.sin(t*4));heading(im,cfg,p);return im
