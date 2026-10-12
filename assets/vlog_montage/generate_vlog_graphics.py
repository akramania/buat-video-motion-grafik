#!/usr/bin/env python3
"""Generate 100 original, editable vlogging vector compositions and their previews."""
from pathlib import Path
import hashlib, io, json, re, math, html
import xml.etree.ElementTree as ET
import cairosvg
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
SCRATCH = Path('/workspace/scratch/52cf302c2e1c/vlog_graphics_qa')
PALETTES = [('#202A43','#FFB66E','#F5EEE7','#66C3B4'),('#25374A','#C4EC91','#F0F6E6','#8CBEDF'),('#34304C','#C9B4FF','#F5F0FC','#FAA48F'),('#203844','#83D9E9','#F0FAFC','#FFCA68'),('#41302B','#FFACAC','#FFF5EA','#A4D6BD')]

def n(v): return str(round(v,2))
def attrs(**kw): return ' '.join(f'{k.replace("_","-")}="{html.escape(str(v),quote=True)}"' for k,v in kw.items() if v is not None)
def el(tag, **kw): return '<'+tag+' '+attrs(**kw)+'/>'
def rect(x,y,w,h,fill,rx=0,stroke=None,sw=2,**kw): return el('rect',x=x,y=y,width=w,height=h,rx=rx,fill=fill,stroke=stroke,stroke_width=sw if stroke else None,**kw)
def circle(x,y,r,fill,stroke=None,sw=2): return el('circle',cx=x,cy=y,r=r,fill=fill,stroke=stroke,stroke_width=sw if stroke else None)
def line(x1,y1,x2,y2,stroke,sw=2,**kw): return el('line',x1=x1,y1=y1,x2=x2,y2=y2,stroke=stroke,stroke_width=sw,stroke_linecap='round',**kw)
def path(d,fill='none',stroke=None,sw=2,**kw): return el('path',d=d,fill=fill,stroke=stroke,stroke_width=sw if stroke else None,stroke_linecap='round',stroke_linejoin='round',**kw)
def text(x,y,s,fill,size=18,weight=600,anchor='start',**kw): return '<text '+attrs(x=x,y=y,fill=fill,font_size=size,font_family='DejaVu Sans, sans-serif',font_weight=weight,text_anchor=anchor,**kw)+'>'+html.escape(s)+'</text>'
def group(s,**kw): return '<g '+attrs(**kw)+'>'+s+'</g>'
def star(x,y,r,fill,points=5,inner=.45,rotation=-90):
    xy=[]
    for k in range(points*2):
        a=math.radians(rotation+180*k/points); rr=r if k%2==0 else r*inner
        xy.append((x+rr*math.cos(a),y+rr*math.sin(a)))
    return path('M'+' L'.join(n(x)+','+n(y) for x,y in xy)+' Z',fill)
def pin(x,y,r,col,ink):
    return path(f'M{x},{y+r*1.7} C{x-r*1.3},{y+r*.25} {x-r},{y-r} {x},{y-r} C{x+r},{y-r} {x+r*1.3},{y+r*.25} {x},{y+r*1.7} Z',col)+circle(x,y,r*.36,ink)
def check(x,y,s,col): return path(f'M{x},{y+s*.52} l{s*.3},{s*.3} l{s*.7},-{s*.8}','none',col,3)
def arrow(x,y,s,col): return line(x,y,x+s,y,col,3)+path(f'M{x+s-8},{y-8} l8,8 l-8,8','none',col,3)
def camera(x,y,s,ink,accent,cream):
    return rect(x,y,s*1.5,s,ink,8)+path(f'M{x+s*.3},{y} l8,-12 h{s*.5} l8,12 Z',ink)+circle(x+s*.77,y+s*.5,s*.32,cream)+circle(x+s*.77,y+s*.5,s*.21,accent)+circle(x+s*1.25,y+s*.22,3,accent)
def wave(x,y,w,h,col,count=14):
    return ''.join(line(x+i*w/(count-1),y-h*(.2+.8*abs(math.sin(i*1.51)))/2,x+i*w/(count-1),y+h*(.2+.8*abs(math.sin(i*1.51)))/2,col,4) for i in range(count))
def hatch(x,y,w,h,col,step=14):
    return ''.join(line(x+i,y,x+i+10,y+10,col,2) for i in range(0,int(w)-10,step))
def leaf(x,y,s,fill,ink): return path(f'M{x},{y} Q{x+s},{y-s} {x+s},{y} Q{x+s},{y+s} {x},{y} Z',fill)+line(x,y,x+s*.8,y,ink,1.5)
def badge(x,y,r,col,ink,num): return circle(x,y,r,col)+text(x,y+7,num,ink,23,700,'middle')

FAMILIES = [
 ('recording-hud','Recording HUD','HUD rakaman','Rakaman POV dan pembukaan vlog'),
 ('travel-stamp','Travel stamp','Travel & journey','Cap destinasi dan montaj perjalanan'),
 ('map-route','Map route','Travel & journey','Menunjukkan perjalanan antara lokasi'),
 ('location-pin','Location card','Travel & journey','Memperkenalkan lokasi semasa'),
 ('day-chapter','Day chapter','Chapters & titles','Pembahagian hari atau bab vlog'),
 ('episode-badge','Episode badge','Chapters & titles','Pembukaan siri dan penanda episod'),
 ('caption-callout','Caption callout','Captions & callouts','Komen ringkas dan highlight moment'),
 ('engagement','Engagement prompt','Engagement','Ajakan mengikuti, komen atau simpan'),
 ('lower-third','Creator lower third','Captions & callouts','Nama hos dan maklumat ringkas'),
 ('time-card','Time card','Chapters & titles','Peralihan masa dan rutin harian'),
 ('food-review','Food review','Reviews & lifestyle','Vlog makanan, menu dan tasting'),
 ('rating','Review rating','Reviews & lifestyle','Penilaian pengalaman dan produk'),
 ('gear-frame','Camera and gear frame','Frames & photography','Sorotan kamera dan peralatan kreator'),
 ('journey-ticket','Journey ticket','Travel & journey','Kad perjalanan dan ringkasan trip'),
 ('weather-cue','Weather cue','Travel & journey','Menunjukkan suasana dan cuaca'),
 ('photo-moment','Photo moment','Frames & photography','Foto, kenangan dan highlight montaj'),
 ('checklist','Vlog checklist','Planning & progress','Rutin, persediaan dan senarai aktiviti'),
 ('question-sticker','Question sticker','Engagement','Soalan penonton dan Q&A'),
 ('story-progress','Story progress','Planning & progress','Kemajuan cabaran dan perjalanan cerita'),
 ('audio-indicator','Audio and music indicator','Audio & rhythm','Sorotan muzik, dialog dan suasana')
]

def compose(f,v):
    ink,a,c,b=PALETTES[v]
    m=[]; ac=[]; de=[]; tx=[]
    # Each family has five structurally different compositions, not recolours.
    if f==0:
        layouts=[(76,64,488,232),(120,76,400,208),(64,94,512,192),(88,50,464,260),(148,68,344,224)]
        x,y,w,h=layouts[v]
        for cx,cy,dx,dy in [(x,y,1,1),(x+w,y,-1,1),(x,y+h,1,-1),(x+w,y+h,-1,-1)]:
            m.append(path(f'M{cx},{cy+dy*26} V{cy} H{cx+dx*32}','none',ink,4))
        ac += [circle(x+14,y+15,6,a),rect(x+w-50,y+8,32,15,ink,3),rect(x+w-46,y+11,20+v*2,9,b,1)]
        if v==0: de.append(circle(320,180,32,'none',ink,2)+line(280,180,300,180,ink)+line(340,180,360,180,ink)+line(320,140,320,160,ink)+line(320,200,320,220,ink))
        elif v==1: de.append(rect(248,124,144,112,'none',12,ink,2)+line(320,146,320,214,ink)+line(285,180,355,180,ink))
        elif v==2:
            de.extend(line(x+w*k/3,y+28,x+w*k/3,y+h-28,ink,1,opacity=.25) for k in (1,2)); de.extend(line(x+28,y+h*k/3,x+w-28,y+h*k/3,ink,1,opacity=.25) for k in (1,2))
        elif v==3: de.append(circle(320,176,56,'none',ink,2)+circle(320,176,44,'none',ink,1)+line(308,176,332,176,ink)+line(320,164,320,188,ink))
        else: de.append(path('M220,116 h28 v28 M420,116 h-28 v28 M220,244 h28 v-28 M420,244 h-28 v-28','none',a,3))
        tx += [text(x+28,y+21,['REC','4K REC','POV','MANUAL','AF LOCK'][v],ink,13),text(x+14,y+h-12,['00:12:48','24 FPS','ISO 200','1 / 120','F 2.8'][v],ink,12),text(x+w-14,y+h-12,['4K · 30','01:24','12:08 PM','RAW','4K'][v],ink,12,600,'end')]
    elif f==1:
        if v in (0,3):
            x,y,w,h=(178,88,284,184) if v==0 else (148,96,344,166)
            m += [rect(x,y,w,h,c,10,ink,3),rect(x+9,y+9,w-18,h-18,'none',5,ink,1),line(x+18,y+48,x+w-18,y+48,ink,2),line(x+18,y+h-39,x+w-18,y+h-39,ink,2)]
            ac.append(pin(x+w/2,y+87,17,a,ink) if v==0 else camera(x+37,y+69,42,ink,a,c))
            tx += [text(320,y+33,'TRAVEL JOURNAL',ink,15,700,'middle'),text(320 if v==0 else x+194,y+133 if v==0 else y+98,'KUALA LUMPUR' if v==0 else 'CITY EXPLORER',ink,15,700,'middle'),text(320,y+h-15,'PASSPORT TO NEW STORIES',ink,10,500,'middle')]
        elif v==1:
            m += [circle(320,180,107,c,ink,3),circle(320,180,93,'none',ink,1),circle(320,180,71,'none',ink,2)]
            ac += [pin(320,163,24,a,ink),star(229,180,7,b),star(411,180,7,b)]
            tx += [text(320,118,'EXPLORE MORE',ink,17,700,'middle'),text(320,240,'WEEKEND AWAY',ink,15,700,'middle')]
        elif v==2:
            m.append(path('M200,86 H440 L468,180 L440,274 H200 L172,180 Z',c,ink,3)); de.append(path('M213,98 H427 L452,180 L427,262 H213 L188,180 Z','none',ink,1)); ac += [star(320,135,23,a,8,.65),line(225,206,415,206,ink,2)]
            tx += [text(320,193,'ADVENTURE CLUB',ink,19,700,'middle'),text(320,241,'EST. TODAY',ink,12,500,'middle')]
        else:
            m.append(path('M173,110 Q320,54 467,110 V250 Q320,306 173,250 Z',c,ink,3)); de.append(path('M185,117 Q320,70 455,117 V242 Q320,288 185,242 Z','none',ink,1)); ac += [path('M269,188 l32,-50 32,50 Z',b),path('M303,188 l39,-65 39,65 Z',a),circle(377,138,12,b)]
            tx += [text(320,112,'OFF THE MAP',ink,16,700,'middle'),text(320,238,'COLLECT MOMENTS',ink,15,700,'middle')]
    elif f==2:
        m.append(rect(91,68,458,224,c,20))
        routes=['M132,230 C180,225 164,116 253,140 S338,261 404,195 S457,123 504,110','M128,118 C205,62 239,224 313,217 S394,93 507,237','M133,200 L213,130 L295,218 L386,132 L503,172','M144,242 C244,270 203,108 303,108 S384,211 494,141','M145,112 L238,112 L238,192 L340,192 L340,249 L493,249']
        for k in range(4+v):
            de.append(path(f'M{110+k*58},76 l-18,200','none',ink,1,opacity=.12))
        m.append(path(routes[v],'none',ink,5)); ac.append(path(routes[v],'none',a,3,stroke_dasharray=f'{9+v*2} 8'))
        endpts=[(132,230,504,110),(128,118,507,237),(133,200,503,172),(144,242,494,141),(145,112,493,249)][v]
        ac += [circle(endpts[0],endpts[1],10,ink),circle(endpts[0],endpts[1],4,c),pin(endpts[2],endpts[3]-5,14,a,ink)]
        if v in (2,4): ac.append(circle(295 if v==2 else 340,218 if v==2 else 192,8,b,ink,2))
        tx += [text(113,98,['THE WEEKEND ROUTE','CITY TO COAST','FIVE LITTLE STOPS','TAKE THE SCENIC WAY','OUR WALKING ROUTE'][v],ink,14),text(523,275,['24 KM','3 HOURS','5 STOPS','DAY 02','ON FOOT'][v],ink,12,600,'end')]
    elif f==3:
        if v==0:
            m.append(rect(113,116,414,132,c,24)); ac.append(pin(179,162,28,a,ink)); tx += [text(235,168,'GEORGETOWN',ink,25),text(235,197,'PENANG · MALAYSIA',ink,12),text(235,220,'5.4141° N / 100.3288° E',ink,11,500)]
        elif v==1:
            m.append(rect(179,67,282,236,c,18)); ac += [pin(320,118,26,a,ink),line(205,187,435,187,b,3)]; tx += [text(320,170,'HERE & NOW',ink,22,700,'middle'),text(320,225,'THE OLD TOWN',ink,20,700,'middle'),text(320,254,'STOP NO. 03',ink,12,500,'middle')]
        elif v==2:
            m.append(path('M109,137 H479 L530,180 L479,223 H109 Z',ink)); ac += [circle(165,180,28,a),pin(165,172,15,a,ink),rect(211,204,84,4,b,2)]; tx += [text(220,176,'NEXT STOP',c,12),text(220,199,'RIVERSIDE',c,23)]
        elif v==3:
            m += [rect(110,97,420,165,c,12),rect(110,97,107,165,ink,12),rect(200,97,17,165,ink)]; ac += [pin(161,164,25,a,c),rect(239,212,115,27,a,13)]; tx += [text(241,147,'FOUND A LITTLE',ink,14),text(241,181,'HIDDEN GEM',ink,28),text(296,230,'LOCATION SAVED',ink,9,700,'middle')]
        else:
            m += [rect(159,120,322,121,c,24),circle(320,112,47,ink)]; ac += [pin(320,99,21,a,c),line(206,200,267,200,b,2),line(373,200,434,200,b,2)]; tx += [text(320,181,'FRESH AIR CLUB',ink,22,700,'middle'),text(320,218,'TRAILHEAD / 08:30',ink,12,500,'middle')]
    elif f==4:
        if v==0:
            m.append(rect(124,88,392,182,c,14)); ac += [rect(124,88,16,182,a,6),text(167,212,'01',ink,91,700)]; tx += [text(302,148,'DAY ONE',ink,22),text(302,179,'THE ARRIVAL',ink,14),text(302,239,'CHAPTER / 01',ink,11,500)]
        elif v==1:
            m += [circle(235,180,83,ink),rect(297,128,191,104,c,16)]; ac.append(circle(235,180,72,'none',a,3)); tx += [text(235,201,'02',c,60,700,'middle'),text(330,173,'DAY TWO',ink,20),text(330,204,'SLOW MORNING',ink,12)]
        elif v==2:
            m.append(path('M148,124 H492 V252 H148 Z',c,ink,2)); ac += [rect(169,103,102,37,a,4),hatch(165,230,304,10,ink,20)]; tx += [text(220,129,'CHAPTER 03',ink,11,700,'middle'),text(320,188,'THE ROAD AHEAD',ink,30,700,'middle'),text(320,214,'ONE DAY / MANY STORIES',ink,11,500,'middle')]
        elif v==3:
            m += [rect(129,77,382,204,ink,27),rect(148,94,344,168,'none',18,c,1)]; ac.append(star(463,122,16,a,8,.55)); tx += [text(166,133,'04 / NEXT CHAPTER',a,13),text(166,185,'CITY AFTER DARK',c,30),text(166,225,'A NEW PERSPECTIVE',c,12,500)]
        else:
            m += [rect(128,95,142,177,ink,16),rect(281,95,231,177,c,16)]; ac += [rect(300,230,192,6,b,3),circle(236,124,8,a)]; tx += [text(199,219,'05',a,73,700,'middle'),text(305,147,'LAST DAY',ink,23),text(305,184,'MAKE IT COUNT',ink,16),text(305,211,'BEFORE WE GO',ink,12,500)]
    elif f==5:
        shapes=[path('M215,80 H425 L455,180 L425,280 H215 L185,180 Z',ink),circle(320,180,111,ink),rect(179,90,282,180,ink,28),path('M320,69 L449,132 V245 L320,295 L191,245 V132 Z',ink),path('M205,86 H435 V236 L320,288 L205,236 Z',ink)]
        m.append(shapes[v]); ac += [circle(320,169,49,a),star(235+v*3,180,7,b),star(405-v*3,180,7,b)]; de.append(line(247,226,393,226,c,1)); tx += [text(320,120,'THE VLOG SERIES',c,14,700,'middle'),text(320,185,f'{v+1:02d}',ink,43,700,'middle'),text(320,250,['FIRST LIGHT','WEEKEND NOTES','DAILY MOMENTS','TRAVEL DIARY','BEHIND THE SCENES'][v],c,12,700,'middle')]
        if v in (1,3): ac.append(path('M276,74 l-12,-14 M364,74 l12,-14','none',a,3))
        elif v==2: de.append(rect(192,103,256,154,'none',19,c,1))
        elif v==4: de.append(path('M218,100 H422 V229 L320,273 L218,229 Z','none',c,1))
    elif f==6:
        if v==0:
            m.append(path('M128,101 H511 Q526,101 526,119 V220 Q526,238 507,238 H332 L299,267 V238 H128 Q113,238 113,220 V119 Q113,101 128,101 Z',c,ink,2)); ac.append(circle(153,143,16,a)); tx += [text(184,151,'A LITTLE REMINDER',ink,17),text(145,191,'THE BEST PART IS THE JOURNEY.',ink,18,500),text(145,215,'Take a moment. Look around.',ink,12,500)]
        elif v==1:
            m += [rect(160,107,320,144,ink,25),path('M186,245 l-12,27 l46,-27 Z',ink)]; ac.append(star(451,122,23,a,4,.36)); tx += [text(195,162,'PLOT TWIST:',a,19),text(195,199,'WE TOOK A DETOUR',c,23)]
        elif v==2:
            m += [rect(117,118,406,123,c,10),rect(133,132,374,94,'none',5,ink,1)]; ac += [circle(118,119,15,a),circle(523,242,11,b)]; tx += [text(320,166,'NOTE TO SELF',ink,13,700,'middle'),text(320,199,'TRY SOMETHING NEW',ink,26,700,'middle')]
        elif v==3:
            m.append(path('M145,90 H495 V245 H352 L320,277 L288,245 H145 Z',a,ink,2)); ac += [rect(163,111,313,3,ink,1),circle(178,134,5,ink)]; tx += [text(193,140,'TODAY’S LITTLE WIN',ink,12),text(320,190,'MADE IT HAPPEN',ink,30,700,'middle'),text(320,220,'PROGRESS > PERFECTION',ink,12,500,'middle')]
        else:
            m += [rect(107,113,426,132,ink,17),circle(145,123,31,a)]; ac += [path('M133,123 h8 v14 h-12 v-8 h4 Z',ink),path('M148,123 h8 v14 h-12 v-8 h4 Z',ink)]; tx += [text(186,157,'THE MOMENT THAT',c,18),text(186,192,'MADE MY DAY',a,29),text(186,223,'save this memory',c,12,500)]
    elif f==7:
        if v==0:
            m += [rect(138,126,363,109,ink,40),circle(191,180,33,a)]; ac.append(path('M185,165 l24,15 l-24,15 Z',ink)); tx += [text(249,174,'FOLLOW THE JOURNEY',c,19),text(249,201,'NEW STORIES EVERY WEEK',c,11,500)]
        elif v==1:
            m.append(rect(144,97,352,167,c,21)); ac += [path('M187,128 H222 V166 H209 L198,178 V166 H187 Z',a,ink,2),rect(180,212,280,31,ink,15)]; tx += [text(247,147,'YOUR TURN',ink,18),text(180,192,'WHAT SHOULD WE TRY NEXT?',ink,18),text(320,233,'LEAVE A COMMENT',c,12,700,'middle')]
        elif v==2:
            m += [rect(182,70,276,229,ink,23),path('M241,112 H275 V175 L258,161 L241,175 Z',a)]; ac += [circle(402,122,24,b),check(391,111,21,ink)]; tx += [text(215,214,'SAVE THIS SPOT',c,24),text(215,247,'COME BACK LATER',c,13,500)]
        elif v==3:
            m += [rect(137,120,366,120,c,24),circle(195,180,37,ink)]; ac.append(path('M181,179 l14,-14 l14,14 M195,166 v32 M178,194 v13 h34 v-13','none',a,3)); tx += [text(253,172,'PASS IT ON',ink,26),text(253,204,'SHARE A GOOD MOMENT',ink,11)]
        else:
            m.append(rect(140,81,360,198,c,20)); ac += [circle(195,131,28,a),path('M186,131 c-9,-14 14,-21 10,-7 c11,-12 24,2 12,12 l-12,12 Z',ink),rect(170,213,300,42,ink,21)]; tx += [text(242,134,'PART OF THE CREW',ink,20),text(173,182,'THANKS FOR BEING HERE',ink,20),text(320,240,'LET’S KEEP CREATING',c,13,700,'middle')]
    elif f==8:
        if v==0:
            m += [rect(106,132,428,98,ink,14),rect(106,132,13,98,a,5)]; ac.append(circle(153,181,21,a)); tx += [text(192,173,'AKRAM / CREATOR',c,24),text(193,204,'TRAVEL · LIFESTYLE · STORIES',c,11,500)]
        elif v==1:
            m += [rect(177,154,354,86,c,17),circle(148,180,54,ink)]; ac.append(circle(148,180,42,a)); tx += [text(148,192,'A',ink,36,700,'middle'),text(211,188,'YOUR HOST',ink,24),text(211,214,'A NEW POINT OF VIEW',ink,11,500)]
        elif v==2:
            m += [path('M114,119 H482 L526,162 L482,205 H114 Z',ink),rect(133,213,237,28,a,3)]; tx += [text(144,156,'MEET THE CREATOR',c,13),text(144,189,'STORIES WITH AKRAM',c,26),text(150,232,'EPISODE 03 / ON LOCATION',ink,10)]
        elif v==3:
            m += [rect(124,98,391,63,c,10),rect(124,174,300,88,ink,11)]; ac += [rect(434,174,81,88,a,11),star(475,218,23,ink,4,.4)]; tx += [text(146,139,'IN GOOD COMPANY',ink,21),text(146,211,'TODAY’S HOST',c,24),text(146,240,'VLOGGER / STORYTELLER',c,11,500)]
        else:
            m += [rect(120,127,400,115,c,23),rect(137,146,106,77,ink,15)]; ac += [camera(157,165,34,ink,a,c),rect(267,215,177,4,b,2)]; tx += [text(267,174,'BEHIND THE LENS',ink,21),text(267,200,'THE MAKER’S JOURNAL',ink,12,500)]
    elif f==9:
        if v==0:
            m += [rect(142,90,356,180,ink,26),circle(457,126,15,a)]; tx += [text(175,136,'EARLY START',a,13),text(175,208,'06:30',c,76),text(175,244,'MONDAY / FIRST COFFEE',c,12,500)]
        elif v==1:
            m += [circle(225,180,87,c,ink,3),rect(325,135,178,90,ink,16)]; ac += [line(225,180,225,126,ink,4),line(225,180,264,200,ink,4),circle(225,180,6,a)]; de.extend(line(225+72*math.sin(k*math.pi/6),180-72*math.cos(k*math.pi/6),225+78*math.sin(k*math.pi/6),180-78*math.cos(k*math.pi/6),ink,2) for k in range(12)); tx += [text(345,172,'AFTERNOON',a,13),text(345,204,'02:15 PM',c,23)]
        elif v==2:
            m += [rect(174,86,292,190,c,15),rect(174,86,292,45,a,15),rect(174,115,292,16,a)]; ac += [rect(196,69,12,32,ink,6),rect(433,69,12,32,ink,6)]; tx += [text(320,116,'WEDNESDAY',ink,14,700,'middle'),text(320,214,'18',ink,85,700,'middle'),text(320,251,'A DAY TO REMEMBER',ink,12,500,'middle')]
        elif v==3:
            m += [rect(109,121,422,124,ink,18),rect(126,138,150,90,c,9),rect(291,138,223,90,c,9)]; ac += [circle(239,157,5,a),circle(474,157,5,a)]; tx += [text(203,200,'07',ink,56,700,'middle'),text(402,176,'GOLDEN HOUR',ink,16,700,'middle'),text(402,206,'PM / STILL EXPLORING',ink,10,500,'middle')]
        else:
            m.append(path('M148,103 H492 V250 H148 Z',c,ink,2)); ac += [rect(132,120,33,20,a,3),rect(475,213,33,20,a,3),line(174,208,466,208,ink,2)]; tx += [text(320,143,'A FEW HOURS LATER',ink,19,700,'middle'),text(320,193,'21:45',ink,46,700,'middle'),text(320,234,'NIGHT NOTES',ink,12,500,'middle')]
    elif f==10:
        if v==0:
            m += [rect(143,82,354,199,c,23),circle(212,166,45,a),circle(212,166,32,'none',ink,2)]; ac += [path('M202,166 c5,-22 25,-22 25,0 c0,18 -20,23 -25,0 Z',b,ink,2),line(164,116,164,207,ink,2),line(259,116,259,207,ink,2)]; tx += [text(284,148,'FIRST BITE',ink,25),text(284,180,'TODAY’S FIND',ink,12),text(176,246,'GOOD FOOD / GOOD COMPANY',ink,13)]
        elif v==1:
            m += [rect(177,77,286,222,ink,22),rect(205,104,230,47,a,8)]; ac += [path('M248,169 H350 V213 Q350,235 325,235 H273 Q248,235 248,213 Z',c),path('M350,177 H365 Q387,201 350,211','none',c,6),path('M279,168 c-13,-12 12,-20 0,-32 M312,168 c-13,-12 12,-20 0,-32','none',b,3)]; tx += [text(320,135,'COFFEE BREAK',ink,21,700,'middle'),text(320,269,'SIP / PAUSE / REPEAT',c,12,500,'middle')]
        elif v==2:
            m += [path('M152,96 H488 V264 H152 Z',c,ink,2),rect(168,114,303,5,a,2)]; ac += [circle(206,158,18,ink),path('M196,158 l7,7 l13,-16','none',a,3),line(176,224,464,224,ink,1)]; tx += [text(241,159,'LOCAL FAVOURITE',ink,19),text(176,200,'THE STREET FOOD DIARY',ink,20),text(176,248,'TRY THIS / SAVE THE SPOT',ink,12,500)]
        elif v==3:
            m += [rect(126,105,388,151,c,20),circle(204,180,47,ink)]; ac += [path('M174,197 l60,0 l-30,-49 Z',a),circle(202,180,5,b),circle(214,192,4,b),circle(192,192,4,b)]; tx += [text(274,162,'WORTH THE WAIT',ink,22),text(274,194,'CRISPY / FRESH / LOCAL',ink,11),text(274,228,'TODAY’S FOOD STOP',ink,12)]
        else:
            m += [rect(163,71,314,230,ink,25),rect(187,188,266,82,c,15)]; ac += [path('M250,126 Q320,104 390,126 L374,171 H266 Z',a),path('M266,121 Q280,86 301,117 Q320,74 339,117 Q360,86 374,121 Z',b),line(243,95,256,151,c,3)]; tx += [text(320,224,'SWEET LITTLE FIND',ink,22,700,'middle'),text(320,249,'DESSERT DIARY / 01',ink,12,500,'middle')]
    elif f==11:
        if v==0:
            m.append(rect(123,112,394,135,ink,18)); ac.extend(star(189+k*63,158,20,a if k<4 else c) for k in range(5)); tx += [text(320,216,'4 / 5 — WOULD GO AGAIN',c,18,700,'middle')]
        elif v==1:
            m += [circle(233,180,86,ink),rect(326,130,165,100,c,15)]; ac += [path('M233,100 A80,80 0 1 1 154,180','none',a,8),star(235,142,16,a)]; tx += [text(233,202,'9.2',c,45,700,'middle'),text(348,174,'GREAT FIND',ink,18),text(348,204,'VALUE / VIBE',ink,11)]
        elif v==2:
            m.append(rect(162,74,316,232,c,22)); ac.extend(rect(192,137+k*41,223,10,b,5)+rect(192,137+k*41,[205,175,217][k],10,ink,5) for k in range(3)); tx += [text(192,117,'THE QUICK REVIEW',ink,20),text(430,147,'9',ink,12),text(430,188,'8',ink,12),text(430,229,'10',ink,12),text(192,280,'TASTE / VALUE / ATMOSPHERE',ink,11)]
        elif v==3:
            m += [path('M320,71 L438,117 V237 L320,288 L202,237 V117 Z',ink),circle(320,152,43,a)]; ac += [check(299,133,43,ink),star(241,183,11,b),star(399,183,11,b)]; tx += [text(320,225,'CREATOR APPROVED',c,16,700,'middle'),text(320,254,'A SOLID 10 / 10',c,13,500,'middle')]
        else:
            m += [rect(138,105,364,151,ink,20),rect(160,127,103,107,c,16)]; ac += [star(211,157,22,a),line(288,215,476,215,a,3)]; tx += [text(211,216,'8.5',ink,28,700,'middle'),text(287,155,'THE VERDICT',a,13),text(287,187,'WORTH A TRY',c,22)]
    elif f==12:
        if v==0:
            m.append(rect(142,75,356,215,c,21)); ac += [camera(234,132,78,ink,a,c),rect(169,242,302,27,a,13)]; tx += [text(320,111,'BEHIND THE CAMERA',ink,19,700,'middle'),text(320,261,'SMALL KIT / BIG STORIES',ink,12,700,'middle')]
        elif v==1:
            m += [rect(110,110,420,140,ink,20),rect(126,126,178,108,c,12)]; ac += [circle(215,180,43,ink),circle(215,180,32,a),circle(215,180,23,ink),circle(215,180,9,b)]; tx += [text(331,157,'THE EVERYDAY LENS',a,15),text(331,192,'35 MM',c,33),text(331,222,'MY GO-TO SETUP',c,11,500)]
        elif v==2:
            m.append(path('M149,79 H491 V283 H149 Z',c,ink,2)); ac += [rect(207,108,69,70,ink,9),rect(198,168,86,12,ink,4),path('M242,181 v48 M242,205 l-35,48 M242,205 l35,48','none',ink,4),rect(330,130,112,49,a,9)]; tx += [text(345,161,'THE SETUP',ink,14),text(331,207,'STABLE SHOTS',ink,15),text(331,239,'TAKE / 02',ink,11)]
        elif v==3:
            m += [rect(148,83,344,194,ink,24),rect(168,102,303,155,'none',14,c,1)]; ac += [rect(194,143,49,75,a,19),path('M180,181 v10 Q180,226 219,226 Q258,226 258,191 V181 M219,226 v17 M200,243 h38','none',a,4),wave(299,163,124,54,b,13)]; tx += [text(297,222,'GOOD AUDIO',c,19),text(297,244,'MATTERS',c,13)]
        else:
            m += [rect(132,105,376,155,c,20),rect(154,124,103,117,ink,14)]; ac += [rect(166,136,79,87,a,7),circle(205,229,4,c),camera(172,158,32,ink,b,c)]; tx += [text(284,159,'SHOOT WITH WHAT',ink,16),text(284,188,'YOU HAVE',ink,28),text(284,229,'MOBILE STORYTELLING',ink,11,500)]
    elif f==13:
        if v==0:
            m += [rect(108,109,424,141,c,14),line(429,121,429,238,ink,1,stroke_dasharray='4 5')]; ac += [circle(148,179,23,ink),arrow(136,179,24,a)]; tx += [text(190,152,'THE WEEKEND PASS',ink,22),text(190,184,'CITY → COAST',ink,17),text(190,224,'BOARDING / ANY TIME',ink,10),text(475,174,'01',ink,29,700,'middle'),text(475,203,'ADMIT ONE',ink,9,600,'middle')]
        elif v==1:
            m += [rect(175,62,290,238,c,15),rect(175,62,290,55,ink,15),rect(175,101,290,16,ink),line(190,253,450,253,ink,1,stroke_dasharray='3 5')]; ac += [pin(320,166,21,a,ink)]; tx += [text(320,96,'TICKET TO THE OUTSIDE',c,14,700,'middle'),text(320,226,'DAY TRIP / 02',ink,25,700,'middle'),text(320,280,'BRING YOUR CURIOSITY',ink,11,500,'middle')]
        elif v==2:
            m.append(path('M128,99 H488 V135 Q465,145 488,155 V217 Q465,227 488,237 V263 H128 V237 Q151,227 128,217 V155 Q151,145 128,135 Z',ink)); ac += [rect(154,125,95,114,a,11),circle(202,154,17,ink),line(275,221,462,221,c,1)]; tx += [text(202,213,'GO',ink,32,700,'middle'),text(273,157,'SCENIC ROUTE',c,22),text(273,184,'NO RUSH / NO RULES',c,12),text(273,244,'TRAVEL JOURNAL',c,10)]
        elif v==3:
            m += [rect(111,92,418,178,c,18),rect(111,92,101,178,ink,18),rect(196,92,16,178,ink)]; ac += [path('M142,132 l18,-10 l18,10 v49 l-18,10 l-18,-10 Z',a),line(231,229,510,229,ink,1)]; tx += [text(160,230,'TRIP 04',c,11,700,'middle'),text(233,138,'HERE FOR THE',ink,17),text(233,177,'GOOD VIEWS',ink,32),text(233,251,'DEPARTURE / RIGHT NOW',ink,11)]
        else:
            m += [rect(132,122,376,116,ink,16),rect(145,133,102,94,c,9)]; ac += [path('M162,163 h66 v39 h-66 Z',a),line(176,162,176,151,ink,3),line(214,162,214,151,ink,3),line(176,150,214,150,ink,3)]; tx += [text(267,167,'PACKED & READY',c,22),text(267,201,'LET’S MAKE MEMORIES',c,12,500)]
    elif f==14:
        if v==0:
            m.append(rect(136,100,368,160,c,25)); ac += [circle(221,169,33,a),''.join(line(221+46*math.cos(k*math.pi/4),169+46*math.sin(k*math.pi/4),221+58*math.cos(k*math.pi/4),169+58*math.sin(k*math.pi/4),a,4) for k in range(8))]; tx += [text(293,159,'SUNNY STORIES',ink,21),text(293,196,'28° C',ink,33),text(166,238,'PERFECT WEATHER TO WANDER',ink,11)]
        elif v==1:
            m += [rect(173,75,294,222,ink,23),circle(258,130,31,a),path('M214,155 Q214,132 239,136 Q252,104 284,128 Q316,123 322,147 Q343,156 326,177 H231 Q207,177 214,155 Z',c)]; ac.extend(line(239+k*28,196,234+k*28,211,b,3) for k in range(4)); tx += [text(320,252,'RAINY DAY DIARY',c,20,700,'middle'),text(320,276,'SLOW DOWN / STAY COZY',c,10,500,'middle')]
        elif v==2:
            m.append(rect(117,115,406,133,c,18)); ac += [path('M149,157 h99 q27,0 27,-19 q0,-21 -23,-21 q-20,0 -20,18 M149,179 h119 q26,0 26,21 q0,19 -23,19 q-21,0 -21,-17 M149,200 h51','none',ink,4),leaf(222,206,23,a,ink)]; tx += [text(324,163,'A LITTLE BREEZE',ink,20),text(324,199,'FRESH AIR / 22°',ink,18),text(324,226,'OUTSIDE IS CALLING',ink,10)]
        elif v==3:
            m += [rect(145,87,350,190,ink,22),path('M179,210 Q223,172 265,210 Q304,167 347,210 Q388,182 461,210 V255 H179 Z',b),circle(320,159,45,a),rect(179,210,282,45,ink,0)]; de += [line(188,217,453,217,a,1),line(212,228,432,228,a,1),line(247,239,392,239,a,1)]; tx += [text(320,124,'GOLDEN HOUR CLUB',c,18,700,'middle'),text(320,261,'CHASE THE LIGHT',c,12,500,'middle')]
        else:
            m += [rect(146,101,348,158,c,24),circle(217,171,39,ink),circle(232,153,33,c)]; ac.extend(star(x,y,r,a,4,.35) for x,y,r in [(256,128,8),(173,118,5),(259,205,6)]); tx += [text(296,155,'AFTER HOURS',ink,24),text(296,188,'NIGHT WALK / 19°',ink,13),text(296,225,'CITY LIGHTS ON',ink,12)]
    elif f==15:
        if v==0:
            m += [rect(191,58,258,252,c,6,ink,2),rect(207,75,226,177,ink,2)]; ac += [path('M212,227 L271,144 L315,196 L355,130 L428,227 Z',a),circle(253,108,19,b),rect(183,87,44,19,b,0),rect(414,277,40,18,b,0)]; tx += [text(320,286,'ONE FOR THE MEMORY BOOK',ink,11,600,'middle')]
        elif v==1:
            m += [rect(126,91,387,178,ink,15),rect(143,108,353,126,c,5)]; ac += [path('M149,217 Q204,122 254,181 Q305,119 350,185 Q423,112 490,217 Z',b),circle(429,142,17,a)]; tx += [text(151,256,'STILL / 0021',c,11),text(487,256,'HOLD THIS MOMENT',c,11,500,'end')]
        elif v==2:
            m += [rect(120,74,188,214,c,6,ink,2),rect(328,96,188,191,c,6,ink,2),rect(134,90,160,144,ink,2),rect(342,110,160,127,ink,2)]; ac += [circle(214,148,32,a),path('M348,221 l37,-64 l30,30 l37,-77 l44,111 Z',b),rect(184,64,62,22,b,0),rect(400,86,50,22,a,0)]; tx += [text(214,267,'BEFORE',ink,13,600,'middle'),text(422,267,'AFTER',ink,13,600,'middle')]
        elif v==3:
            m += [rect(166,77,308,206,c,22),rect(183,93,274,144,ink,13)]; ac += [camera(263,130,59,ink,a,c),circle(206,259,5,a),circle(224,259,5,b),circle(242,259,5,ink)]; tx += [text(450,264,'MEMORY / 04',ink,12,500,'end')]
        else:
            m += [path('M129,105 H511 V253 H129 Z',ink),rect(159,125,322,108,c,1)]; de.extend(rect(139+k*25,112,13,7,c,1)+rect(139+k*25,239,13,7,c,1) for k in range(15)); ac += [path('M171,220 L225,145 L269,191 L323,140 L383,198 L422,161 L473,220 Z',b),circle(401,151,15,a)]; tx += [text(320,281,'FRAME BY FRAME / OUR STORY',ink,12,500,'middle')]
    elif f==16:
        if v==0:
            m += [rect(171,66,298,239,c,18),rect(229,53,182,31,ink,10)]; ac.extend(rect(194,119+k*45,22,22,a,5)+check(199,122+k*45,14,ink) for k in range(3)); tx += [text(236,134,'CHARGE THE CAMERA',ink,13),text(236,179,'PACK THE ESSENTIALS',ink,13),text(236,224,'FOLLOW THE STORY',ink,13),text(320,280,'READY FOR THE DAY',ink,15,700,'middle')]
        elif v==1:
            m += [rect(126,106,388,150,ink,24),circle(179,182,31,a)]; ac += [check(162,164,35,ink),rect(236,141,240,8,b,4),rect(236,169,187,8,c,4),rect(236,197,215,8,c,4)]; tx += [text(236,231,'SMALL STEPS / BIG DAY',c,12)]
        elif v==2:
            m.append(rect(158,78,324,207,c,19)); ac += [circle(204,126,18,ink),circle(204,178,18,a),circle(204,230,18,b),check(195,117,18,c),check(195,169,18,ink),rect(245,138,204,2,ink,1),rect(245,190,204,2,ink,1)]; tx += [text(247,127,'WAKE / CREATE',ink,18),text(247,179,'WALK / EXPLORE',ink,18),text(247,231,'EDIT / REPEAT',ink,18)]
        elif v==3:
            m += [rect(137,109,366,142,c,20),rect(157,128,101,104,ink,16)]; ac += [circle(207,164,22,a),check(194,151,26,ink),line(181,200,233,200,a,3)]; tx += [text(283,155,'TODAY’S PLAN',ink,21),text(283,184,'MAKE SOMETHING',ink,16),text(283,212,'WORTH REMEMBERING',ink,14)]
        else:
            m += [rect(161,74,318,226,ink,20),rect(181,96,278,52,a,10)]; ac += [circle(198,182,8,b),circle(198,223,8,b),circle(198,264,8,b)]; tx += [text(320,129,'WEEKEND RESET',ink,20,700,'middle'),text(222,186,'MOVE SLOWER',c,15),text(222,227,'SEE SOMETHING NEW',c,15),text(222,268,'COLLECT A STORY',c,15)]
    elif f==17:
        if v==0:
            m.append(rect(146,91,348,184,c,24)); ac += [rect(163,109,314,45,ink,15),circle(179,254,5,a)]; tx += [text(320,139,'ASK ME ANYTHING',c,18,700,'middle'),text(320,199,'WHAT’S YOUR NEXT',ink,20,700,'middle'),text(320,229,'DREAM DESTINATION?',ink,22,700,'middle')]
        elif v==1:
            m += [circle(219,180,81,ink),rect(314,120,191,120,c,20)]; ac += [circle(219,180,68,'none',a,2)]; tx += [text(219,207,'?',a,84,700,'middle'),text(335,159,'YOUR IDEA',ink,21),text(335,193,'COULD BE OUR',ink,12),text(335,215,'NEXT EPISODE',ink,15)]
        elif v==2:
            m += [rect(144,81,352,204,ink,22),rect(165,210,310,52,c,17)]; ac += [circle(198,124,18,a),text(198,132,'Q',ink,23,700,'middle')]; tx += [text(234,130,'CREATOR Q&A',c,20),text(175,180,'WHAT WOULD YOU TRY?',c,21),text(320,242,'TELL US YOUR STORY',ink,16,700,'middle')]
        elif v==3:
            m.append(path('M117,104 H523 V234 H357 L323,265 L289,234 H117 Z',c,ink,2)); ac += [circle(487,118,24,a),star(487,118,12,ink,4,.35),line(141,194,500,194,ink,1)]; tx += [text(320,151,'THIS OR THAT?',ink,29,700,'middle'),text(236,178,'CITY WALK',ink,14,600,'middle'),text(410,178,'NATURE TRAIL',ink,14,600,'middle'),text(320,221,'THE CHOICE IS YOURS',ink,12,500,'middle')]
        else:
            m += [rect(162,68,316,233,c,25),rect(162,68,316,72,ink,25),rect(162,111,316,29,ink)]; ac += [circle(201,104,15,a),text(201,110,'?',ink,19,700,'middle'),rect(190,249,259,28,a,14)]; tx += [text(234,111,'LET’S TALK',c,22),text(320,193,'YOUR BEST LITTLE',ink,22,700,'middle'),text(320,222,'TRAVEL TIP?',ink,28,700,'middle'),text(320,268,'REPLY WITH AN IDEA',ink,11,700,'middle')]
    elif f==18:
        if v==0:
            m.append(rect(127,113,386,134,ink,22)); ac += [rect(150,188,340,12,c,6),rect(150,188,238,12,a,6)]; tx += [text(152,154,'THE STORY SO FAR',c,21),text(490,225,'70% / KEEP GOING',a,12,600,'end')]
        elif v==1:
            m += [rect(121,103,398,154,c,20),line(171,183,469,183,ink,4)]; ac.extend(circle(171+k*99,183,17,a if k<3 else c,ink,2) for k in range(4)); tx += [text(148,141,'FROM IDEA TO MEMORY',ink,24),text(171,227,'PLAN',ink,10,600,'middle'),text(270,227,'SHOOT',ink,10,600,'middle'),text(369,227,'EDIT',ink,10,600,'middle'),text(468,227,'SHARE',ink,10,600,'middle')]
        elif v==2:
            m += [circle(236,180,88,ink),rect(339,129,164,101,c,16)]; ac += [path('M236,105 A75,75 0 1 1 161,180','none',a,10),circle(236,105,6,b)]; tx += [text(236,195,'75%',c,43,700,'middle'),text(360,168,'CHALLENGE',ink,16),text(360,197,'DAY 21 / 28',ink,15),text(360,219,'STILL SHOWING UP',ink,9,500)]
        elif v==3:
            m.append(rect(155,79,330,202,c,23)); ac.extend(rect(179+k*58,238-(k+1)*25,38,(k+1)*25,a if k<4 else ink,5) for k in range(5)); tx += [text(181,124,'A LITTLE BETTER',ink,23),text(181,148,'EVERY SINGLE DAY',ink,14),text(320,263,'PROGRESS IS A STORY',ink,12,500,'middle')]
        else:
            m += [rect(132,113,376,133,ink,20),rect(155,161,310,37,'none',11,c,2)]; ac.extend(rect(163+k*50,169,42,21,a if k<4 else c,5) for k in range(6)); tx += [text(155,144,'WEEKEND ADVENTURE',c,19),text(471,225,'4 / 6 MOMENTS COLLECTED',c,12,600,'end')]
    else:
        if v==0:
            m += [rect(126,109,388,143,ink,23),circle(185,179,33,a)]; ac += [path('M177,168 l23,12 l-23,12 Z',ink),wave(244,172,229,48,b,22)]; tx += [text(245,224,'SOUNDTRACK TO THE DAY',c,12)]
        elif v==1:
            m += [rect(172,76,296,222,c,22),circle(320,151,55,ink),circle(320,151,41,'none',a,2),circle(320,151,12,a)]; de += [path('M290,112 A47,47 0 0 1 341,106 M356,180 A47,47 0 0 1 302,194','none',a,1)]; tx += [text(320,245,'NOW PLAYING',ink,23,700,'middle'),text(320,274,'GOOD VIBES / 02:48',ink,12,500,'middle')]
        elif v==2:
            m += [rect(128,110,384,138,c,23),rect(148,131,81,95,ink,17)]; ac += [rect(174,146,29,42,a,14),path('M163,173 v10 q0,23 26,23 q25,0 25,-23 v-10 M189,206 v9','none',a,3),wave(265,171,200,43,ink,19)]; tx += [text(268,218,'VOICE NOTES / ON THE GO',ink,11)]
        elif v==3:
            m += [rect(152,93,336,174,ink,22),rect(175,117,54,34,a,8),rect(175,180,54,34,b,8)]; ac += [wave(251,134,211,27,a,15),wave(251,197,211,45,b,20)]; tx += [text(202,140,'L',ink,17,700,'middle'),text(202,202,'R',ink,17,700,'middle'),text(320,247,'LISTEN TO THE MOMENT',c,13,600,'middle')]
        else:
            m += [rect(141,104,358,153,c,20),circle(214,181,46,ink)]; ac += [path('M195,170 h10 l17,-14 v50 l-17,-14 h-10 Z',a),path('M231,169 q17,12 0,24 M237,158 q31,23 0,46','none',a,3),wave(293,173,164,55,ink,16)]; tx += [text(293,226,'AMBIENT / OUTSIDE',ink,12)]
    main=''.join(m); accent=''.join(ac); details=''.join(de); titles=''.join(tx)
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" width="640" height="360"><title>'+html.escape(FAMILIES[f][1]+f' composition {v+1}')+'</title><desc>Original editable vector artwork for vlogging. Palette, shape and text layers can be edited independently.</desc>'+group(main,id='main')+group(accent,id='accent')+group(details,id='details')+group(titles,id='text')+'</svg>'

def canonical_geometry(svg):
    root=ET.fromstring(svg)
    for e in root.iter():
        for k in list(e.attrib):
            if k in ('fill','stroke','opacity','fill-opacity','stroke-opacity','id'): del e.attrib[k]
        if e.tag.rsplit('}',1)[-1] in ('text','title','desc'): e.text=''
    return hashlib.sha256(ET.tostring(root)).hexdigest()

def main():
    (ROOT/'graphics_vlog').mkdir(parents=True,exist_ok=True)
    (ROOT/'previews/graphics_vlog').mkdir(parents=True,exist_ok=True)
    SCRATCH.mkdir(parents=True,exist_ok=True)
    records=[]; hashes=set(); checks=[]; thumbs=[]
    motions=['Stroke-reveal HUD corners, blink recording dot, fade text in; exit with 6-frame fade.', 'Scale badge from 94% with gentle ease-out; stagger the title and decorative mark.', 'Draw the route or frame path before revealing its label; drift artwork 3 px during hold.', 'Slide composition upward 18 px with cubic ease-out; accent layer follows after 0.08 s.', 'Reveal card with a short clip wipe; pulse its focus detail once; exit with downward fade.']
    for f,fam in enumerate(FAMILIES):
        for v in range(5):
            ident=f'VL{301+f*5+v:04d}'
            svg=compose(f,v); p=ROOT/'graphics_vlog'/f'{ident}.svg'; p.write_text(svg,encoding='utf-8')
            xml=ET.fromstring(svg)
            assert xml.attrib['viewBox']=='0 0 640 360'
            assert {e.attrib.get('id') for e in xml.iter()} >= {'main','accent','details','text'}
            assert not re.search(r'<script|<foreignObject|(?:xlink:)?href\s*=|@import|url\(',svg,re.I)
            geo=canonical_geometry(svg); assert geo not in hashes, ident; hashes.add(geo)
            img=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=640,output_height=360))).convert('RGBA')
            bbox=img.getchannel('A').getbbox(); assert bbox and bbox[0]>=20 and bbox[1]>=20 and bbox[2]<=620 and bbox[3]<=340,(ident,bbox)
            assert img.getpixel((0,0))[3]==0 and img.getchannel('A').getextrema()==(0,255)
            prev=ROOT/'previews/graphics_vlog'/f'{ident}.webp'; img.resize((480,270),Image.Resampling.LANCZOS).save(prev,'WEBP',quality=92,method=6)
            records.append({'id':ident,'type':'vlog-graphic','title':fam[1]+f' / Composition {v+1:02d}','category':fam[2],'tags':['vlog','vector','editable','transparent',fam[0],f'composition-{v+1}'],'use_cases':[fam[3],'Vlogging, creator videos and personal montage'],'format':'svg','file':f'graphics_vlog/{ident}.svg','preview':f'previews/graphics_vlog/{ident}.webp','technical':{'background':'transparent','viewbox':'0 0 640 360','width':640,'height':360,'layers':['main','accent','details','text'],'color_space':'sRGB','editable':True,'text':'Editable SVG text using DejaVu Sans / generic sans-serif; outline with the target editor if needed.'},'suggested_motion':motions[v]})
            checks.append({'id':ident,'geometry_sha256':geo,'bounds':list(bbox),'svg_sha256':hashlib.sha256(svg.encode()).hexdigest(),'rasterized':True,'alpha_edge':True,'named_layers':True,'external_references':False})
            thumbs.append((ident,img))
    (ROOT/'index_vlog_graphics.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'vlog_graphics_qa.json').write_text(json.dumps({'total':100,'unique_color_independent_geometry':len(hashes),'rasterized':100,'transparent_edges':100,'security_checks':100,'failures':[],'assets':checks},indent=2)+'\n')
    # Contact sheets remain in scratch; previews keep alpha in the skill.
    for sheet in range(5):
        canvas=Image.new('RGB',(1600,1170),'#ECEDE9'); d=ImageDraw.Draw(canvas)
        for k,(ident,img) in enumerate(thumbs[sheet*20:(sheet+1)*20]):
            x=(k%4)*400; y=(k//4)*234
            card=Image.new('RGBA',(390,219),'#DCE2DE'); reduced=img.resize((384,216),Image.Resampling.LANCZOS); card.alpha_composite(reduced,(3,1)); canvas.paste(card.convert('RGB'),(x+5,y+5))
            d.text((x+14,y+218),ident,fill='#202A43')
        canvas.save(SCRATCH/f'contact_{sheet+1:02d}.jpg',quality=94)
    print(json.dumps({'count':len(records),'unique_geometry':len(hashes),'contact_sheets':str(SCRATCH),'range':'VL0301–VL0400'}))

if __name__=='__main__': main()
