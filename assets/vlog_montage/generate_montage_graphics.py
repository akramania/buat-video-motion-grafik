#!/usr/bin/env python3
"""Build 100 original, editable, transparent montage SVG compositions.

No downloaded art, logos, external fonts, linked images, or JavaScript. Windows
use real transparent holes. Each variant changes composition and geometry.
Run this file to regenerate the assets, WebP previews, index, and QA report.
"""
from pathlib import Path
import hashlib
import io
import json
import math
import re
import xml.etree.ElementTree as ET

import cairosvg
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'graphics_montage'
PREV = ROOT / 'previews' / 'graphics_montage'
OUT.mkdir(parents=True, exist_ok=True)
PREV.mkdir(parents=True, exist_ok=True)
W, H = 640, 360
INK = '#151e2c'
PAPER = '#fff7eb'
MINT = '#b3f2cc'
CORAL = '#ff846e'
GOLD = '#ffd27e'
BLUE = '#a9c7ff'

def rect(x,y,w,h,fill=PAPER,rx=0,stroke='none',sw=1,op=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>'

def line(x1,y1,x2,y2,c=PAPER,sw=2,**extra):
    args=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in extra.items())
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" {args}/>'

def path(d,fill='none',stroke=PAPER,sw=2,**extra):
    args=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in extra.items())
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {args}/>'

def circle(x,y,r,fill=PAPER,stroke='none',sw=1):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def text(x,y,s,size=15,c=PAPER,weight=600,anchor='start',spacing=1):
    return f'<text x="{x}" y="{y}" fill="{c}" font-family="sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{spacing}">{s}</text>'

def poly(points,fill=CORAL,stroke='none',sw=1):
    return f'<polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'

def group(s,transform=''):
    return f'<g transform="{transform}">{s}</g>'

def frame(x,y,w,h,b=8,bottom=None,fill=PAPER):
    """Rectangular ring, with a truly transparent inner opening."""
    bottom=b if bottom is None else bottom
    d=f'M{x} {y}h{w}v{h}h{-w}z M{x+b} {y+b}v{h-b-bottom}h{w-2*b}v{-h+b+bottom}z'
    return path(d,fill,'none',0,fill_rule='evenodd')

def star(x,y,r=12,n=4,fill=CORAL):
    pts=[]
    for i in range(n*2):
        a=-math.pi/2+i*math.pi/n
        rr=r if i%2==0 else r*.35
        pts.append(f'{x+math.cos(a)*rr:.2f},{y+math.sin(a)*rr:.2f}')
    return poly(' '.join(pts),fill)

def tag(x,y,label,w=112,c=MINT):
    return rect(x,y,w,30,c,15)+circle(x+15,y+15,3,INK)+text(x+27,y+20,label,10,INK,700,spacing=1.2)

def pin(x,y,c=CORAL):
    return path(f'M{x} {y+19} C{x-22} {y-3},{x-13} {y-22},{x} {y-22} C{x+13} {y-22},{x+22} {y-3},{x} {y+19}Z',c,'none',0)+circle(x,y-8,5,INK)

def cinematic(v):
    x=34+v*5;y=52+v*3;w=572-v*10;h=250-v*7
    m=frame(x,y,w,h,4+v,fill=PAPER)
    a=line(x+17,y-13,x+103+v*10,y-13,CORAL,3)+line(x+w-100,y+h+13,x+w-13,y+h+13,MINT,3)
    d=text(x+14,y+h-12,['WIDE / 01','CINEMA / 02','OPEN FRAME','STORY / 04','THE MOMENT'][v],11,INK if False else PAPER)
    if v==1:m+=frame(195,82,250,195,2,fill=MINT)
    if v==2:a+=line(x-7,100,x-7,246,MINT,2)+line(x+w+7,118,x+w+7,260,CORAL,2)
    if v==3:m+=frame(72,86,126,116,3,fill=MINT)+frame(446,149,120,110,3,fill=CORAL)
    if v==4:a+=star(78,38,13,4,MINT)+star(562,320,13,4,CORAL)
    return m,a,d

def film(v):
    m='';a='';d=''
    if v in (0,2,4):
        y=52+v*4;h=258-v*8;x=40;w=560
        m=frame(x,y,w,h,17,bottom=17,fill=PAPER)
        for i in range(14-v):
            xx=54+i*(534/(13-v))
            a+=rect(round(xx,2),y+3,12,8,INK,2)+rect(round(xx,2),y+h-11,12,8,INK,2)
        if v==2:m+=line(320,76,320,280,PAPER,6)
        if v==4:m+=line(225,90,225,270,PAPER,4)+line(415,90,415,270,PAPER,4)
        d=text(52,y+h+17,'35MM  •  MEMORY ROLL',9,PAPER,500)
    else:
        for k,(x,y,w,h) in enumerate([(55,40,228,262),(344,65,228,240)] if v==1 else [(76,54,196,230),(355,76,209,222)]):
            m+=frame(x,y,w,h,18,bottom=14,fill=PAPER)
            for i in range(8):
                a+=rect(x+4,y+12+i*(h-35)/7,8,10,INK,2)+rect(x+w-12,y+12+i*(h-35)/7,8,10,INK,2)
            d+=text(x+21,y+h-3,f'ROLL {k+1:02}',8,INK)
    return m,a,d

def polaroid(v):
    layouts=[[(80,57,218,233,-7),(332,72,222,230,8)],[(56,68,174,208,-10),(231,46,175,210,0),(407,79,174,208,9)],[(126,42,269,255,-8),(303,99,215,215,9)],[(60,47,245,259,-3),(337,92,245,230,4)],[(62,77,163,205,-8),(235,52,170,225,3),(421,86,157,211,11)]]
    m='';a='';d=''
    for i,(x,y,w,h,rot) in enumerate(layouts[v]):
        m+=group(frame(x,y,w,h,9,bottom=38,fill=PAPER),f'rotate({rot} {x+w/2} {y+h/2})')
        a+=group(rect(x+w*.28,y-6,w*.44,18,[MINT,CORAL,GOLD][i%3],3,op=.9),f'rotate({rot-4} {x+w/2} {y+h/2})')
        d+=group(text(x+16,y+h-15,['SAVED MOMENTS','THIS DAY','MEMORY CLUB'][i%3],9,INK,500),f'rotate({rot} {x+w/2} {y+h/2})')
    return m,a,d

def contact(v):
    m='';a='';d='';n=3+v
    if v<3:
        width=(556-(n-1)*10)/n
        y=96-v*6;h=161+v*14
        for i in range(n):
            x=42+i*(width+10);m+=frame(round(x,2),y,round(width,2),h,6,bottom=26,fill=PAPER)
            d+=text(x+8,y+h-9,f'{i+1:02} / FRAME',8,INK)
        a=line(42,75,170+v*32,75,CORAL,3)+tag(467,51,'CONTACT',130,MINT)
    else:
        cols=3 if v==3 else 4;rows=2;ww=(548-(cols-1)*10)/cols;hh=112
        for i in range(cols*rows):
            x=46+(i%cols)*(ww+10);y=61+(i//cols)*128
            m+=frame(round(x,2),y,round(ww,2),hh,4,bottom=18,fill=PAPER)
            d+=text(x+7,y+hh-5,f'{i+1:02}',8,INK)
        a+=text(46,337,'A SEQUENCE OF SMALL MOMENTS',10,PAPER)
    return m,a,d

def splits(v):
    layouts=[[(38,50,277,260),(325,50,277,260)],[(38,68,178,225),(231,68,178,225),(424,68,178,225)],[(40,42,560,132),(40,188,560,132)],[(40,48,345,264),(397,48,203,125),(397,187,203,125)],[(42,48,205,264),(259,48,339,124),(259,186,339,126)]]
    m='';a='';d=''
    for i,(x,y,w,h) in enumerate(layouts[v]):
        m+=frame(x,y,w,h,3+v%2,fill=PAPER)
        a+=rect(x+11,y+12,26,22,[MINT,CORAL,GOLD][i%3],4)+text(x+24,y+27,str(i+1),10,INK,700,'middle')
    d=text(45,338,['DUAL PERSPECTIVE','THREE ANGLES','ABOVE / BELOW','MAIN &amp; DETAIL','DETAIL &amp; MAIN'][v],10,PAPER)
    return m,a,d

def editorial(v):
    layouts=[(43,61,312,228),(269,53,328,240),(47,199,548,117),(54,41,535,107),(114,77,410,207)]
    x,y,w,h=layouts[v];m=rect(x,y,w,h,PAPER,4)
    a=rect(x+13,y+13,42+v*6,6,CORAL,3)+rect(x+w-21,y+15,5,h-30,MINT,2)
    d=text(x+20,y+44,'THE MONTAGE',10,INK,700,spacing=2)
    size=34 if h>150 else 26
    words=[['SMALL','MOMENTS'],['MAKE IT','COUNT'],['ON THE MOVE'],['A NEW CHAPTER'],['STORY IN','MOTION']][v]
    for i,s in enumerate(words):
        d+=text(x+20,y+(97 if h>150 else 81)+i*41,s,size if v!=2 else 27,INK,700,spacing=-.8)
    if h>150:d+=text(x+22,y+h-29,'Scenes worth remembering.',11,INK,400,spacing=.2)
    else:a+=circle(x+w-37,y+h-31,10,MINT)+path(f'M{x+w-41} {y+h-35}l8 4 -8 4',INK,'none',0)
    return m,a,d

def tape(v):
    layouts=[[(67,73,208,33,-12),(359,251,218,34,8)],[(99,42,178,37,6),(396,67,151,35,-9),(68,270,162,35,10)],[(63,158,514,50,-2)],[(96,60,450,42,0),(137,260,380,36,0)],[(67,55,153,48,-14),(418,253,160,40,13),(326,40,106,29,5)]]
    m='';a='';d=''
    for i,(x,y,w,h,r) in enumerate(layouts[v]):
        pts=f'{x+4},{y} {x+w-9},{y+3} {x+w},{y+h-2} {x+2},{y+h} {x+8},{y+h*.63} {x},{y+h*.25}'
        m+=group(poly(pts,[PAPER,MINT,CORAL][i%3]),f'rotate({r} {x+w/2} {y+h/2})')
        a+=group(line(x+21,y+h/2,x+w-24,y+h/2,INK,1.5,stroke_dasharray='2 7'),f'rotate({r} {x+w/2} {y+h/2})')
    if v==2:d+=text(100,190,'A LITTLE BIT OF EVERYDAY',19,INK,700,spacing=2)
    else:d+=text(320,185,['COLLECT THE MOMENTS','UNSCRIPTED','EVERYDAY','MEMORIES, TOGETHER','KEEP THIS FEELING'][v],17,PAPER,700,'middle',1.5)
    return m,a,d

def capsules(v):
    shapes=[(55,260,242),(355,52,231),(196,277,248),(51,47,208),(370,250,214)]
    x,y,w=shapes[v];m=rect(x,y,w,49,PAPER,24)
    a=pin(x+27,y+30,CORAL)+line(x+55,y+11,x+55,y+38,INK,1)
    d=text(x+70,y+21,['CITY DIARY','ON LOCATION','OUR ADVENTURE','DAY BY DAY','TAKE ME BACK'][v],11,INK,700)+text(x+70,y+37,['MON  /  10:24','SAT  /  16:30','DAY 03  /  08:15','DAY 07  /  12:00','SUN  /  18:45'][v],9,INK,400)
    for i in range(2+v):a+=circle(61+i*15,63+v*4,3,MINT if i%2 else CORAL)
    if v in (1,3):m+=rect(54,276,123+v*17,30,MINT,15);d+=text(68,296,'NEW MEMORIES',10,INK)
    return m,a,d

def beat(v):
    m='';a='';d='';n=6+v*2
    x=49;y=294-v*6;span=542
    for i in range(n):
        xx=x+span*i/(n-1);height=13+(i%3)*6+v
        m+=line(round(xx,2),y,round(xx,2),y-height,PAPER,2)
        if i%3==0:a+=circle(round(xx,2),y-height-9,4,CORAL)
    a+=line(49,y+11,591,y+11,MINT,1.5)+circle(49+v*64,y+11,6,MINT)
    d=text(48,y+34,['CUT ON BEAT','SYNC THE MOMENT','RHYTHM MAP','KEEP THE PACE','BUILD THE ENERGY'][v],10,PAPER)
    if v>1:
        for i in range(v+1):a+=star(73+i*46,66+(i%2)*9,8,4,GOLD)
    if v%2:m+=line(46,47,46,171,PAPER,1)+text(59,62,'01:24',12,PAPER)
    return m,a,d

def sport(v):
    x=40+v*7;y=221-v*8;w=333+v*18
    m=poly(f'{x+14},{y} {x+w},{y} {x+w-15},{y+73} {x},{y+73}',PAPER)
    a=poly(f'{x+w-50},{y} {x+w},{y} {x+w-15},{y+73} {x+w-65},{y+73}',CORAL)
    d=text(x+23,y+31,['KEEP MOVING','ALL IN','THE NEXT LEVEL','GO THE DISTANCE','BUILT FOR THIS'][v],21,INK,800,spacing=.3)+text(x+23,y+55,'MOTION • MOMENT • MOMENTUM',8,INK,600)
    for i in range(3+v):
        sx=437+i*21;sy=53+(i%2)*14
        a+=line(sx,sy,sx+17,sy+35,MINT,3)
    if v==2:m+=path('M45 62h87l-25 35h84',stroke=PAPER,sw=3)
    if v==4:a+=star(530,169,22,8,GOLD)
    return m,a,d

def travel(v):
    layouts=[[(86,254),(301,109),(552,233)],[(95,97),(268,241),(540,76)],[(76,234),(229,125),(384,226),(550,116)],[(82,87),(195,236),(382,97),(555,248)],[(81,197),(220,75),(430,279),(558,157)]]
    pts=layouts[v];d='';m='';a=''
    for i in range(len(pts)-1):
        x,y=pts[i];xx,yy=pts[i+1];mx=(x+xx)/2;my=min(y,yy)-49-v*3
        m+=path(f'M{x} {y} Q{mx} {my} {xx} {yy}',stroke=PAPER,sw=2,stroke_dasharray='5 7')
    for i,(x,y) in enumerate(pts):
        a+=pin(x,y,[CORAL,MINT,GOLD,BLUE][i]);d+=text(x,y+37,f'STOP {i+1:02}',9,PAPER,600,'middle')
    d+=text(50,329,['THE ROAD AHEAD','PLACES &amp; MOMENTS','ONE TRIP, MANY STORIES','FOLLOW THE ROUTE','ADVENTURE NOTES'][v],12,PAPER,700)
    return m,a,d

def chapter(v):
    x=52+v*8;y=71+v*4;w=536-v*16;h=221-v*7
    m=frame(x,y,w,h,2,fill=PAPER)
    a=rect(x+18,y+18,47+v*7,5,MINT,2)+circle(x+w-32,y+32,7,CORAL)
    d=text(320,y+67,f'CHAPTER {v+1:02}',12,PAPER,600,'middle',4)+text(320,y+123,['THE BEGINNING','A DAY TO KEEP','IN BETWEEN','MOVING FORWARD','THE NEXT STORY'][v],27,PAPER,700,'middle',.4)
    a+=line(x+70,y+h-42,x+w-70,y+h-42,GOLD,1.5)
    if v%2==0:a+=star(x-11,y+h/2,12,4,CORAL)+star(x+w+11,y+h/2,12,4,MINT)
    return m,a,d

def doodles(v):
    m='';a='';d=''
    x=83+v*12;y=86+v*7
    m+=path(f'M{x-42} {y+26} C{x-70} {y-47},{x+60} {y-57},{x+61} {y+6} C{x+47} {y+65},{x-40} {y+62},{x-52} {y+1}',stroke=PAPER,sw=3)
    a+=star(538-v*11,78+v*5,23-v,5,CORAL)+star(494-v*5,115+v*6,11,4,MINT)
    sx=410-v*17;sy=269-v*8
    m+=path(f'M{sx-64} {sy+29} Q{sx+18} {sy+31} {sx+42} {sy-41} M{sx+23} {sy-30}l19 -11 3 24',stroke=MINT,sw=3)
    a+=path(f'M{54+v*8} {290-v*6}q15 -21 31 0t31 0t31 0t31 0',stroke=GOLD,sw=3)
    if v>1:
        for i in range(v):a+=line(272+i*18,48,267+i*18,65,CORAL,2)
    if v==4:m+=path('M303 183l8 -17 8 17 19 3 -14 13 3 19 -17 -10 -17 10 3 -19 -14 -13Z',stroke=PAPER,sw=2)
    return m,a,d

def quotes(v):
    layouts=[(47,74,333,221),(255,72,336,228),(93,85,450,194),(49,191,542,123),(80,43,483,239)]
    x,y,w,h=layouts[v];m=rect(x,y,w,h,PAPER,7)
    a=text(x+15,y+54,'“',67,CORAL,700)+rect(x+21,y+h-31,58+v*8,3,MINT,1.5)
    words=[['Every frame','has a feeling.'],['Keep what','moves you.'],['Make time','for moments.'],['Some days stay with us.'],['A story told','one moment at a time.']][v]
    start=y+(92 if h>150 else 64)
    d=''
    for i,s in enumerate(words):d+=text(x+24,start+i*34,s,25 if v!=3 else 26,INK,600,spacing=-.5)
    d+=text(x+w-19,y+h-18,'YOUR STORY',8,INK,500,'end',1.6)
    return m,a,d

def credits(v):
    layouts=[(405,46,194,267),(44,46,218,267),(47,255,547,65),(58,42,520,79),(201,47,238,267)]
    x,y,w,h=layouts[v];m=rect(x,y,w,h,INK,7,stroke=PAPER,sw=1.5)
    a=rect(x+14,y+14,w-28,4,MINT,2)
    d=''
    if h>120:
        d+=text(x+18,y+43,'THE PEOPLE',11,PAPER,700,spacing=2)
        for i,s in enumerate(['FILMED BY','EDITED BY','SOUND &amp; MUSIC']):
            yy=y+74+i*56;d+=text(x+18,yy,s,8,MINT,500)+text(x+18,yy+20,'YOUR NAME',13,PAPER,600)
        a+=circle(x+w-25,y+h-25,5,CORAL)
    else:
        for i,s in enumerate(['FILM','EDIT','MUSIC']):
            xx=x+18+i*(w-36)/3;d+=text(xx,y+34,s,8,MINT,500)+text(xx,y+52,'YOUR NAME',12,PAPER,600)
    return m,a,d

def endcards(v):
    m='';a='';d=''
    if v in (0,2,4):
        ww=211+v*2;hh=130+v*5
        m+=frame(45,87,ww,hh,4,fill=PAPER)+frame(640-45-ww,87,ww,hh,4,fill=PAPER)
        a+=circle(320,147,24+v*3,MINT)+path('M313 137l17 10 -17 10Z',INK,'none',0)
        d+=text(320,52,['NEXT UP','MORE MOMENTS','CONTINUE THE STORY'][v//2],17,PAPER,700,'middle',2)
        d+=text(320,284+v*5,'THANKS FOR WATCHING',14,PAPER,600,'middle')
        a+=line(262,308+v*4,378,308+v*4,CORAL,3)
    else:
        x=49;y=62;ww=319;hh=221
        m+=frame(x,y,ww,hh,4,fill=PAPER)+rect(400,84,190,176,PAPER,8)
        d+=text(421,120,'STAY',23,INK,700)+text(421,151,'CURIOUS',23,INK,700)
        a+=rect(420,176,150,37,CORAL,18)+text(495,200,'FOLLOW ALONG',11,INK,700,'middle')
        d+=text(52,317,'THE NEXT ADVENTURE STARTS HERE',11,PAPER)
        if v==3:a+=star(556,238,12,4,MINT)+circle(384,66,8,GOLD)
    return m,a,d

def hud(v):
    m='';a='';d='';x=45+v*6;y=46+v*5;w=550-v*12;h=268-v*10;b=34+v*3
    for xx,yy,dx,dy in [(x,y,1,1),(x+w,y,-1,1),(x,y+h,1,-1),(x+w,y+h,-1,-1)]:
        m+=path(f'M{xx+dx*b} {yy}H{xx}V{yy+dy*b}',stroke=PAPER,sw=2)
    a=circle(x+21,y+20,5,CORAL)+text(x+35,y+24,'REC',10,PAPER,700)
    d=text(x+w-13,y+h-13,['24 FPS  •  1/50','30 FPS  •  1/60','60 FPS  •  1/120','4K  •  24 FPS','HD  •  60 FPS'][v],9,PAPER,500,'end')
    if v==0:m+=line(301,180,339,180,PAPER,1)+line(320,161,320,199,PAPER,1)
    if v==1:m+=circle(320,180,42,'none',PAPER,1)+circle(320,180,7,'none',PAPER,1)
    if v==2:
        for i in range(3):m+=frame(252+i*13,130+i*10,136-i*26,100-i*20,1,fill=PAPER)
    if v==3:m+=line(229,180,290,180,PAPER,1)+line(350,180,411,180,PAPER,1)+line(320,94,320,146,PAPER,1)+line(320,214,320,266,PAPER,1)
    if v==4:
        for xx,yy in [(213,130),(427,130),(213,230),(427,230)]:m+=path(f'M{xx-13} {yy}h26 M{xx} {yy-13}v26',stroke=PAPER,sw=1)
    return m,a,d

def audio(v):
    m='';a='';d='';n=35+v*4;y=264-v*11
    for i in range(n):
        xx=47+546*i/(n-1);amp=9+46*abs(math.sin(i*.51+v*.7))*abs(math.cos(i*.17+v*.4))
        m+=line(round(xx,2),round(y-amp,2),round(xx,2),round(y+amp,2),PAPER,3 if v%2 else 2)
    a+=line(47,y,593,y,MINT,1)+circle(78+v*99,y,5,CORAL)
    d+=text(49,y-70,['SOUNDTRACK','THE AMBIENCE','AUDIO NOTES','WAVES &amp; MOMENTS','LISTEN CLOSE'][v],11,PAPER,600,spacing=2)
    if v>1:a+=tag(446,51,'SOUND ON',145,CORAL)
    return m,a,d

def subtitles(v):
    layout=[(68,260,505,52),(112,245,418,61),(52,269,536,46),(67,223,510,89),(102,248,437,60)]
    x,y,w,h=layout[v];m=rect(x,y,w,h,INK if v%2==0 else PAPER,6+v*2)
    c=PAPER if v%2==0 else INK
    d=text(x+w/2,y+32,['Here is where the story begins.','One moment, one memory.','Everyday adventures, together.','The little things become the big things.','A day worth remembering.'][v],15,c,600,'middle',.1)
    a=rect(x+16,y+h-11,64+v*19,3,CORAL,1.5)
    if v==3:d+=text(x+w/2,y+60,'Keep the feeling. Share the story.',13,c,400,'middle',.1)
    if v==4:a+=circle(x+w-23,y+17,4,MINT)
    return m,a,d

def corners(v):
    layouts=[(61,53,517,252),(103,47,434,266),(52,91,535,177),(77,64,490,229),(135,40,373,280)]
    x,y,w,h=layouts[v];m='';a='';d='';b=35+v*5
    for xx,yy,dx,dy in [(x,y,1,1),(x+w,y,-1,1),(x,y+h,1,-1),(x+w,y+h,-1,-1)]:
        m+=poly(f'{xx},{yy} {xx+dx*b},{yy} {xx},{yy+dy*b}',PAPER)
        a+=line(xx+dx*7,yy+dy*7,xx+dx*(b-10),yy+dy*7,INK,1)
    d=text(x+8,y+h+23,['SAVED / 001','A DAY IN FRAMES','THE MEMORY EDIT','COLLECTED MOMENTS','LIFE, IN MOTION'][v],10,PAPER,600)
    if v%2==0:a+=rect(x+21,y-13,94+v*14,26,CORAL,3,op=.92)
    else:a+=rect(x+w-127,y-13,99+v*7,27,MINT,3,op=.9)
    if v==4:m+=frame(225,95,191,147,2,fill=MINT)
    return m,a,d

FAMILIES = [
 ('cinematic-frame',cinematic,['Wide Screen','Inset Portrait','Parallel Rails','Picture in Picture','Starlit Cinema'],'Frame a cinematic montage without covering the footage.'),
 ('film-border',film,['35mm Wide','Twin Reels','Two Takes','Offset Twin','Triple Exposure'],'Add an editable film-roll border to footage or photographs.'),
 ('polaroid-cluster',polaroid,['Two Memories','Three Friends','Layered Keepsake','Weekend Pair','Three Diary Pages'],'Place photos below transparent polaroid openings.'),
 ('contact-strip',contact,['Three Frames','Four Frames','Five Frames','Six Contact Prints','Eight Contact Prints'],'Build a photo contact-sheet sequence with visible frame numbering.'),
 ('split-screen',splits,['Dual Perspective','Three Angles','Above and Below','Hero and Details','Details and Hero'],'Align clips under transparent multi-screen frames.'),
 ('editorial-title',editorial,['Left Story Panel','Right Story Panel','Lower Editorial','Upper Editorial','Central Manifesto'],'Introduce a montage chapter with a bold editable title panel.'),
 ('tape-paper',tape,['Tape Corners','Three Tape Notes','Story Tape','Memory Bands','Scrapbook Marks'],'Add tactile scrapbook accents around a montage.'),
 ('date-location',capsules,['City Diary','On Location','Adventure Log','Day by Day','Take Me Back'],'Label a location, date, or time in an editable capsule.'),
 ('beat-markers',beat,['Cut on Beat','Sync the Moment','Rhythm Map','Keep the Pace','Build the Energy'],'Overlay rhythmic marks and a visual timeline for a music montage.'),
 ('sports-energy',sport,['Keep Moving','All In','Next Level','Go the Distance','Built for This'],'Add angular energy graphics to sports, gym, or activity footage.'),
 ('travel-route',travel,['Road Ahead','Places and Moments','Many Stories','Follow the Route','Adventure Notes'],'Show an abstract journey using pins and editable route arcs.'),
 ('chapter-divider',chapter,['The Beginning','A Day to Keep','In Between','Moving Forward','The Next Story'],'Introduce a chapter with a spacious title and framing accents.'),
 ('hand-doodles',doodles,['Circle and Arrow','Little Sparks','Happy Marks','Wonder Notes','Star Story'],'Highlight subjects with hand-drawn arrows, loops, and sparks.'),
 ('quote-card',quotes,['Every Frame','Keep What Moves You','Make Time','Days That Stay','One Moment at a Time'],'Place an editable quote beside or over montage footage.'),
 ('credits-panel',credits,['Right Credits','Left Credits','Lower Credits','Upper Credits','Central Credits'],'Credit creators with an editable typography panel.'),
 ('end-card',endcards,['Next Up','Stay Curious','More Moments','Follow the Adventure','Continue the Story'],'Arrange end-screen clips and a call to action.'),
 ('camera-hud',hud,['Crosshair Record','Focus Circle','Focus Boxes','Split Reticle','Four Focus Points'],'Add a clean camera overlay with editable recording metadata.'),
 ('audio-waveform',audio,['Soundtrack','The Ambience','Audio Notes','Waves and Moments','Listen Close'],'Use an original waveform-shaped graphic as a music or ambience accent.'),
 ('subtitle-card',subtitles,['Story Begins','One Memory','Everyday Adventures','Little Things','Day Worth Remembering'],'Add a readable editable caption block to a montage.'),
 ('photo-corners',corners,['Saved Frame','Day in Frames','Memory Edit','Collected Moments','Life in Motion'],'Frame photographs with transparent corner mounts and tape.'),
]

def geometry_hash(svg):
    root=ET.fromstring(svg)
    for node in root.iter():
        for key in ['fill','stroke','opacity','color']:
            node.attrib.pop(key,None)
        if node.tag.endswith('text'):node.text=''
    return hashlib.sha256(ET.tostring(root)).hexdigest()

def generate():
    records=[]; checks=[]; hashes=set()
    for fi,(cat,fn,names,use) in enumerate(FAMILIES):
        for v,name in enumerate(names):
            aid=f'VL{401+fi*5+v:04}'
            main,accent,details=fn(v)
            svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360" role="img" aria-label="{name}"><title>{name} — original montage graphic</title><g id="main">{main}</g><g id="accent">{accent}</g><g id="details">{details}</g></svg>'
            ET.fromstring(svg)
            assert not re.search(r'<(?:script|image|foreignObject)|(?:href|url\()|on\w+=',svg,re.I),aid
            geom=geometry_hash(svg)
            assert geom not in hashes,aid
            hashes.add(geom)
            (OUT/f'{aid}.svg').write_text(svg,encoding='utf-8')
            png=cairosvg.svg2png(bytestring=svg.encode(),output_width=640,output_height=360)
            im=Image.open(io.BytesIO(png)).convert('RGBA')
            alpha=im.getchannel('A');bbox=alpha.getbbox()
            assert bbox is not None,aid
            assert min(bbox[0],bbox[1],W-bbox[2],H-bbox[3])>=12,(aid,bbox)
            assert alpha.getextrema()[0]==0,aid
            im.save(PREV/f'{aid}.webp',format='WEBP',lossless=True,method=6)
            records.append({'id':aid,'type':'montage-graphic','title':name,'category':cat,'tags':['montage','editable','transparent',cat,'original'],'use_cases':[use],'format':'svg','file':f'graphics_montage/{aid}.svg','preview':f'previews/graphics_montage/{aid}.webp','technical':{'background':'transparent','viewbox':'0 0 640 360'},'suggested_motion':'Reveal main group over 0.4 seconds with opacity and a 12 px rise; stagger accent and details by 0.1 seconds; hold over footage, then fade over 0.3 seconds.'})
            pixel_check={}
            if cat in ['cinematic-frame','film-border','contact-strip','split-screen','end-card','photo-corners']:
                # These layouts must expose an actual empty window, rather
                # than merely paint a light rectangle that hides the footage.
                empty=0
                for yy in range(90,251,20):
                    for xx in range(90,551,20):
                        if alpha.getpixel((xx,yy))==0:empty+=1
                assert empty>=80,(aid,'photo opening missing',empty)
                pixel_check={'transparent_window_sample_count':empty}
            checks.append({'id':aid,'geometry_sha256':geom,'alpha_bbox':list(bbox),'transparent':True,'xml_safe':True,**pixel_check})
    assert len(records)==100
    (ROOT/'index_montage_graphics.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'montage_graphics_qa.json').write_text(json.dumps({'count':100,'id_range':['VL0401','VL0500'],'geometry_unique':len(hashes),'rendered_previews':100,'minimum_margin_px':12,'security':'No images, scripts, references, URLs, or event handlers','checks':checks},indent=2)+'\n')
    return records

def contacts(records):
    qa=Path('/workspace/scratch/52cf302c2e1c/montage_graphics_qa')
    qa.mkdir(parents=True,exist_ok=True)
    for sheet in range(4):
        canvas=Image.new('RGB',(1280,875),'#202b3c');draw=ImageDraw.Draw(canvas)
        subset=records[sheet*25:(sheet+1)*25]
        for i,r in enumerate(subset):
            x=(i%5)*256;y=(i//5)*175
            im=Image.open(ROOT/r['preview']).convert('RGBA');im.thumbnail((240,135))
            canvas.paste(im,(x+8,y+7),im)
            draw.text((x+10,y+145),r['id']+' '+r['title'],fill='#ffffff')
        canvas.save(qa/f'contact_{sheet+1}.jpg',quality=94)
    return qa

if __name__=='__main__':
    assets=generate()
    print(json.dumps({'assets':len(assets),'qa_dir':str(contacts(assets))}))
