#!/usr/bin/env python3
"""Original 160s Malay 2D cartoon about the eight Quranic themes of rizq.

Frames are drawn as vector-like layered animation, then encoded with ffmpeg.
The recurring character and bird are original designs, with no sampled frames.
"""

import argparse
import io
import math
import subprocess
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output'
OUT.mkdir(exist_ok=True)
W, H, FPS, LENGTH = 1080, 1920, 24, 160
INTRO, BEAT, OUTRO = 12, 16, 140
NAVY = (35, 62, 68)
CREAM = (255, 249, 230)
INK = (38, 66, 69)
GOLD = (239, 177, 91)
CORAL = (214, 116, 88)
JADE = (96, 152, 128)
WHITE = (255, 254, 247)
SKIN = (222, 160, 116)
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_R = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_S = '/usr/share/fonts/opentype/urw-base35/NimbusRoman-Bold.otf'


@lru_cache(None)
def font(size, kind='b'):
    return ImageFont.truetype({'b':FONT_B,'r':FONT_R,'s':FONT_S}[kind], size)


def clip(v): return max(0., min(1., v))
def ease(v):
    v = clip(v)
    return 1-(1-v)**3
def smooth(v):
    v=clip(v)
    return v*v*(3-2*v)


def txt(d, s, x, y, sz, fill=INK, kind='b', anchor='mm', maxw=None):
    f=font(sz,kind)
    if maxw:
        while d.textbbox((0,0),s,font=f)[2]>maxw and sz>24:
            sz-=2;f=font(sz,kind)
    d.text((int(x),int(y)),s,font=f,fill=fill,anchor=anchor,stroke_width=0)


def rounded(d,box,fill,rad=20,stroke=None,sw=3):
    d.rounded_rectangle(tuple(int(z) for z in box),radius=rad,fill=fill,outline=stroke,width=sw)


def disk(d,x,y,r,col,stroke=None,sw=3):
    d.ellipse((int(x-r),int(y-r),int(x+r),int(y+r)),fill=col,outline=stroke,width=sw)


def line(d,coords,col=INK,w=7):
    d.line(tuple(int(v) for v in coords),fill=col,width=w,joint='curve')


def star(d,x,y,r=13,col=GOLD):
    d.polygon([(x,y-r),(x+r*.27,y-r*.27),(x+r,y),(x+r*.27,y+r*.27),
               (x,y+r),(x-r*.27,y+r*.27),(x-r,y),(x-r*.27,y-r*.27)],fill=col)


def make_bg(top,bottom):
    y=np.linspace(0,1,H,dtype=np.float32)[:,None,None]
    a=np.array(top,dtype=np.float32)[None,None,:]
    b=np.array(bottom,dtype=np.float32)[None,None,:]
    arr=np.broadcast_to(np.clip(a*(1-y)+b*y,0,255).astype('uint8'),(H,W,3)).copy()
    return Image.fromarray(arr,'RGB')


BGS=[
    make_bg((43,82,95),(72,119,110)),        # intro, dusk
    make_bg((166,215,207),(240,226,171)),   # bird
    make_bg((244,211,166),(238,231,195)),   # work
    make_bg((250,220,182),(238,205,176)),   # gratitude
    make_bg((70,104,124),(157,180,172)),    # taqwa
    make_bg((110,155,171),(197,204,179)),   # istighfar
    make_bg((241,214,184),(240,229,188)),   # marriage
    make_bg((213,223,196),(246,225,191)),   # child
    make_bg((248,207,168),(232,215,181)),   # charity
    make_bg((62,112,117),(227,202,150)),    # outro
]


SCENES=[
    {'title':'DIJAMIN ALLAH','ref':'Hūd 11:6', 'accent':(95,155,124),
     'beats':[("Seekor burung keluar", "mencari makan."),
              ("Allah mengurus rezeki", "setiap makhluk."),
              ("Hati jadi tenang.", "Ikhtiar tetap berjalan.")]},
    {'title':'BERUSAHA','ref':'An-Najm 53:39  •  Tirmizi 2344','accent':(212,123,91),
     'beats':[("Kalau burung pun terbang,", "kita juga perlu bergerak."),
              ("Langkah kecil hari ini", "tetap sebuah usaha."),
              ("Tawakal dan ikhtiar", "berjalan bersama.")]},
    {'title':'BERSYUKUR','ref':'Ibrāhīm 14:7','accent':(194,130,81),
     'beats':[("Ada roti yang sederhana.", "Ada hati yang bersyukur."),
              ("Yang ada kita hargai.", "Yang lebih kita mohon."),
              ("Allah menjanjikan", "tambahan nikmat.")]},
    {'title':'TAKWA & TAWAKAL','ref':'At-Talāq 65:2–3','accent':(118,174,172),
     'beats':[("Kadang jalan di depan", "nampak buntu."),
              ("Jaga langkah.", "Serahkan hasil kepada-Nya."),
              ("Jalan keluar boleh datang", "dari arah tak disangka.")]},
    {'title':'ISTIGHFAR','ref':'Nūḥ 71:10–12','accent':(96,160,160),
     'beats':[("Astaghfirullah.", "Aku mahu kembali."),
              ("Mohon ampun,", "perbaiki diri."),
              ("Hujan rahmat mengingatkan", "kita kepada harapan.")]},
    {'title':'MENIKAH','ref':'An-Nūr 24:32','accent':(199,135,113),
     'beats':[("Dua insan membina", "hidup bersama."),
              ("Ada tanggungjawab,", "ada saling menguatkan."),
              ("Kurnia Allah luas", "menurut hikmah-Nya.")]},
    {'title':'ANAK','ref':'Al-Isrā’ 17:31','accent':(169,127,102),
     'beats':[("Anak itu amanah.", "Kita jaga sebaiknya."),
              ("Berusaha, merancang,", "dan membesarkan mereka."),
              ("Allah memberi rezeki", "kepada mereka dan kita.")]},
    {'title':'SEDEKAH','ref':'Saba’ 34:39','accent':(169,123,91),
     'beats':[("Hulurkan yang mampu", "dengan hati yang ikhlas."),
              ("Kebaikan kecil", "bergerak dari tangan ke tangan."),
              ("Apa yang diberi,", "Allah menggantikannya.")]},
]


# The supplied Malay passages, checked against Abdullah Muhammad Basmeih on
# Quran.com. Excerpts are expressly labelled; source ranges match the text.
TRANSLATIONS=[
    ('Surah Hud (11), ayat 6',
     'Dan tiadalah sesuatupun dari makhluk-makhluk yang bergerak di bumi melainkan Allah jualah yang menanggung rezekinya dan mengetahui tempat kediamannya dan tempat ia disimpan. Semuanya itu tersurat di dalam Kitab (Lauh mahfuz) yang nyata (kepada malaikat-malaikat yang berkenaan).', False),
    ('Surah An-Najm (53), ayat 39',
     'Dan bahawa sesungguhnya tidak ada (balasan) bagi seseorang melainkan (balasan) apa yang diusahakannya;', False),
    ('Surah Ibrahim (14), ayat 7',
     'Dan (ingatlah) ketika Tuhan kamu memberitahu: "Demi sesungguhnya! Jika kamu bersyukur nescaya Aku akan tambahi nikmatKu kepada kamu, dan demi sesungguhnya, jika kamu kufur ingkar sesungguhnya azabKu amatlah keras".', False),
    ('Surah At-Talaq (65), petikan ayat 3',
     'Serta memberinya rezeki dari jalan yang tidak terlintas di hatinya. Dan (Ingatlah), sesiapa berserah diri bulat-bulat kepada Allah, maka Allah cukuplah baginya (untuk menolong dan menyelamatkannya). …', True),
    ('Surah Nuh (71), ayat 10–11',
     '(10) Sehingga aku berkata (kepada mereka): Pohonkanlah ampun kepada Tuhan kamu, sesungguhnya adalah Ia Maha Pengampun. (11) (Sekiranya kamu berbuat demikian), Ia akan menghantarkan hujan lebat mencurah-curah, kepada kamu;', False),
    ('Surah An-Nur (24), ayat 32',
     'Dan kahwinkanlah orang-orang bujang (lelaki dan perempuan) dari kalangan kamu, dan orang-orang yang soleh dari hamba-hamba kamu, lelaki dan perempuan. Jika mereka miskin, Allah akan memberikan kekayaan kepada mereka dari limpah kurniaNya kerana Allah Maha Luas (rahmatNya dan limpah kurniaNya), lagi Maha Mengetahui.', False),
    ('Surah Al-Isra’ (17), petikan ayat 31',
     'Dan janganlah kamu membunuh anak-anak kamu kerana takutkan kepapaan; Kamilah yang memberi rezeki kepada mereka dan kepada kamu. …', True),
    ('Surah Saba’ (34), ayat 39',
     'Katakanlah (wahai Muhammad): "Sesungguhnya Tuhanku memewahkan rezeki bagi sesiapa yang dikehendakiNya di antara hamba-hambaNya, dan Ia juga yang menyempitkan baginya; dan apa sahaja yang kamu dermakan maka Allah akan menggantikannya; dan Dia lah jua sebaik-baik Pemberi rezeki".', False),
]


def wrap_translation(d, words, size, width=928):
    rows=[]
    row=''
    for word in words.split():
        candidate=(row+' '+word).strip()
        if row and d.textlength(candidate,font=font(size,'r'))>width:
            rows.append(row);row=word
        else:row=candidate
    if row:rows.append(row)
    return rows


@lru_cache(None)
def translation_panel(n):
    panel=Image.new('RGBA',(W,370),(0,0,0,0))
    d=ImageDraw.Draw(panel)
    heading,body,excerpt=TRANSLATIONS[n]
    rounded(d,(47,3,1033,360),(27,66,67),25,(245,222,174),3)
    txt(d,heading,540,32,29,(249,220,167),maxw=930)
    line(d,(80,58,1000,58),(102,145,129),2)
    for size in range(32,23,-1):
        rows=wrap_translation(d,body,size)
        leading=round(size*1.25)
        if len(rows)*leading<=244:break
    assert len(rows)*leading<=244, heading
    assert ' '.join(rows)==body, heading
    y=73+(244-len(rows)*leading)//2
    for row in rows:
        d.text((80,y),row,font=font(size,'r'),fill=CREAM,anchor='lt')
        y+=leading
    credit=('Petikan terjemahan' if excerpt else 'Terjemahan')+': Abdullah Muhammad Basmeih'
    txt(d,credit,540,335,23,(215,226,206),kind='r',maxw=935)
    if n==1:
        txt(d,'Hadis sokongan: Riwayat At-Tirmizi, no. 2344',540,294,23,(249,220,167),kind='r')
    return panel


def bird(d,x,y,s=1,phase=0,blink=False):
    """A recurring original terracotta sparrow, drawn after scenery."""
    x,y=float(x),float(y)
    disk(d,x-46*s,y+68*s,24*s,(49,73,69))
    d.polygon([(x-28*s,y+13*s),(x-85*s,y+13*s),(x-66*s,y+86*s)],fill=(156,92,69))
    disk(d,x,y,70*s,CORAL,INK,max(1,int(3*s)))
    disk(d,x+36*s,y-42*s,52*s,CORAL,INK,max(1,int(3*s)))
    # Two-frame wing bend plus follow-through.
    wing=math.sin(phase)*43*s
    d.polygon([(x-50*s,y-10*s),(x+20*s,y-4*s),(x-48*s,y-57*s-wing)],
              fill=(241,170,111),outline=INK)
    d.polygon([(x+77*s,y-40*s),(x+113*s,y-22*s),(x+77*s,y-12*s)],fill=GOLD)
    disk(d,x+46*s,y-52*s,6*s,INK)
    if blink:line(d,(x+35*s,y-52*s,x+58*s,y-52*s),INK,max(2,int(3*s)))
    disk(d,x+49*s,y-55*s,2.5*s,WHITE)
    line(d,(x-7*s,y+64*s,x-12*s,y+91*s),INK,max(2,int(4*s)))
    line(d,(x+27*s,y+63*s,x+24*s,y+88*s),INK,max(2,int(4*s)))


def hero(d,x,feet,s=1,mood='hope',phase=0,action='normal',shirt=(89,146,143)):
    """Cartoon protagonist Amir, same face and satchel throughout."""
    x,y=float(x),float(feet)
    bounce=math.sin(phase)*7*s
    y-=bounce
    d.ellipse((x-110*s,y-12*s,x+118*s,y+26*s),fill=(51,76,73))
    strid=math.sin(phase)*26*s if action=='walk' else 0
    line(d,(x-44*s,y-160*s,x-44*s-strid,y-5*s),NAVY,max(5,int(33*s)))
    line(d,(x+48*s,y-155*s,x+46*s+strid,y-5*s),NAVY,max(5,int(33*s)))
    rounded(d,(x-97*s-strid,y-22*s,x-4*s-strid,y+9*s),NAVY,int(12*s))
    rounded(d,(x+4*s+strid,y-22*s,x+99*s+strid,y+9*s),NAVY,int(12*s))
    rounded(d,(x-105*s,y-335*s,x+102*s,y-140*s),shirt,int(52*s),INK,max(2,int(4*s)))
    # satchel strap and persistent shape make him recognizable.
    line(d,(x-71*s,y-320*s,x+77*s,y-170*s),(238,204,142),max(3,int(15*s)))
    rounded(d,(x+21*s,y-250*s,x+128*s,y-133*s),(188,132,94),int(14*s),INK,max(2,int(4*s)))
    shoulder=(x-91*s,y-285*s);other=(x+88*s,y-286*s)
    if action=='point':left=(x-156*s,y-200*s);right=(x+198*s,y-418*s)
    elif action=='reach':left=(x-154*s,y-188*s);right=(x+236*s,y-232*s)
    elif action=='pray':left=(x-40*s,y-230*s);right=(x+45*s,y-230*s)
    elif action=='work':left=(x-166*s,y-177*s);right=(x+188*s,y-199*s)
    elif action=='hold':left=(x-134*s,y-241*s);right=(x+133*s,y-243*s)
    else:
        swing=math.sin(phase)*23*s if action=='walk' else 0
        left=(x-133*s-swing,y-186*s);right=(x+132*s+swing,y-188*s)
    line(d,(*shoulder,*left),shirt,max(4,int(38*s)))
    line(d,(*other,*right),shirt,max(4,int(38*s)))
    disk(d,*left,21*s,SKIN,INK,max(1,int(3*s)))
    disk(d,*right,21*s,SKIN,INK,max(1,int(3*s)))
    disk(d,x,y-420*s,88*s,SKIN,INK,max(2,int(4*s)))
    d.pieslice((x-94*s,y-519*s,x+95*s,y-352*s),178,359,fill=(47,55,53))
    d.polygon([(x-70*s,y-477*s),(x-53*s,y-533*s),(x+80*s,y-489*s),(x+54*s,y-454*s)],fill=(47,55,53))
    eyebrow=-7*s if mood=='worried' else 0
    line(d,(x-53*s,y-437*s+eyebrow,x-18*s,y-431*s-eyebrow),INK,max(2,int(5*s)))
    line(d,(x+19*s,y-431*s-eyebrow,x+53*s,y-437*s+eyebrow),INK,max(2,int(5*s)))
    blink=(int(phase*1.3)%33==0)
    if blink:
        line(d,(x-45*s,y-413*s,x-17*s,y-413*s),INK,max(2,int(4*s)))
        line(d,(x+18*s,y-413*s,x+46*s,y-413*s),INK,max(2,int(4*s)))
    else:
        disk(d,x-32*s,y-412*s,6*s,INK)
        disk(d,x+33*s,y-412*s,6*s,INK)
    if mood=='worried':d.arc((x-22*s,y-391*s,x+26*s,y-365*s),185,350,fill=INK,width=max(2,int(5*s)))
    elif mood=='surprise':disk(d,x+2*s,y-373*s,10*s,INK)
    else:d.arc((x-28*s,y-397*s,x+28*s,y-365*s),0,180,fill=INK,width=max(2,int(5*s)))


def partner(d,x,feet,s=1,phase=0):
    x,y=float(x),float(feet)-math.sin(phase)*5*s
    d.ellipse((x-90*s,y-8*s,x+90*s,y+18*s),fill=(107,113,88))
    d.polygon([(x-68*s,y-285*s),(x+64*s,y-285*s),(x+115*s,y),(x-113*s,y)],fill=(207,126,118))
    d.line((x-110*s,y,x+110*s,y),fill=INK,width=max(2,int(4*s)))
    disk(d,x,y-355*s,76*s,(122,154,123),INK,max(2,int(4*s)))
    d.polygon([(x-78*s,y-355*s),(x-76*s,y-199*s),(x+85*s,y-199*s),(x+75*s,y-355*s)],fill=(122,154,123))
    disk(d,x,y-345*s,56*s,(230,174,133))
    disk(d,x-20*s,y-355*s,5*s,INK);disk(d,x+20*s,y-355*s,5*s,INK)
    d.arc((x-18*s,y-341*s,x+19*s,y-316*s),0,180,fill=INK,width=max(2,int(3*s)))
    line(d,(x-71*s,y-227*s,x-97*s,y-139*s),(207,126,118),max(4,int(30*s)))
    line(d,(x+74*s,y-227*s,x+115*s,y-142*s),(207,126,118),max(4,int(30*s)))
    disk(d,x-97*s,y-139*s,17*s,(230,174,133))
    disk(d,x+115*s,y-142*s,17*s,(230,174,133))


def sprout(d,x,y,grow=1,flowers=False):
    h=max(2,155*clip(grow))
    line(d,(x,y,x-6,y-h),(89,137,92),8)
    for frac,sgn in ((.35,-1),(.62,1),(.84,-1)):
        yy=y-h*frac
        d.ellipse((x-6 if sgn>0 else x-70,yy-21,x+66 if sgn>0 else x+5,yy+17),fill=(87,161,101))
    if flowers:
        for k in range(6):
            a=k*math.pi/3
            disk(d,x+math.cos(a)*20,y-h+math.sin(a)*20,13,(240,204,151))
        disk(d,x,y-h,13,GOLD)


def window(d,x,y,light=True):
    col=(255,221,153) if light else (122,171,166)
    rounded(d,(x,y,x+155,y+170),col,16,INK,5)
    line(d,(x+78,y,x+78,y+170),INK,5);line(d,(x,y+86,x+155,y+86),INK,5)


def cloud(d,x,y,s=1,col=(255,249,227)):
    d.ellipse((x-115*s,y,x+104*s,y+72*s),fill=col)
    disk(d,x-40*s,y,57*s,col);disk(d,x+40*s,y-17*s,75*s,col)


def hills(d,y,c1=(105,164,130),c2=(76,134,118),offset=0):
    d.polygon([(0,H),(W,H),(W,y+57),(870,y+35),(700,y+87),(520,y+21),
               (345,y+95),(172,y+28),(0,y+55)],fill=c1)
    d.polygon([(0,H),(W,H),(W,y+238),(830,y+178),(654,y+265),(470,y+181),
               (280,y+254),(80,y+171),(0,y+191)],fill=c2)


def door(d,x,y,w,h,angle=0,glow=False):
    """Physical arch door and hinged panel."""
    co=GOLD if glow else INK
    d.arc((x-w/2,y-h,x+w/2,y-h+w),180,360,fill=co,width=13)
    line(d,(x-w/2,y-h+w/2,x-w/2,y),co,13)
    line(d,(x+w/2,y-h+w/2,x+w/2,y),co,13)
    d.rectangle((x-w/2+14,y-h+w/2,x+w/2-14,y),fill=(245,224,169) if glow else (91,145,132))
    a=ease(angle)
    left=x-w/2+21
    width=(w-42)*(1-a)
    d.polygon([(left,y-h+w/2),(left+width,y-h+w/2+13*a),
               (left+width,y),(left,y)],fill=(174,111,81),outline=INK)
    disk(d,left+min(width-20,80),y-200,9,GOLD)


def world_intro(d,t):
    p=ease(t/5)
    disk(d,853,857,187,(240,187,112))
    hills(d,1380,(84,139,119),(55,112,104))
    rounded(d,(25,1090,430,1515),(214,167,122),20,INK,6)
    d.polygon([(15,1080),(455,1080),(390,968),(83,968)],fill=(180,106,86),outline=INK)
    txt(d,'KEDAI',225,1035,50,CREAM)
    window(d,65,1153,True)
    line(d,(0,850,1080,850),INK,9)
    for xx in [150,510,825]:bird(d,xx,817,0.48,t*9)
    hero(d,430+65*p,1502,1.14,'worried',t*2,action='hold')
    # Exaggerated phone/wallet balance gag, then a bird escapes the wire.
    if t<5.5:
        rounded(d,(610,1000,925,1216),WHITE,30,INK,8)
        txt(d,'BAKI',768,1058,36,INK)
        txt(d,'RM 12.40',768,1144,51,CORAL)
        for i in range(3):
            xx=648+i*103;yy=946-30*math.sin(t*3+i)
            rounded(d,(xx-37,yy-31,xx+37,yy+31),CREAM,8,CORAL,4)
            txt(d,'BIL',xx,yy,22,INK)
    else:
        bx=780+math.sin(t*1.6)*125;by=753-170*ease((t-5.3)/5)+math.sin(t*4)*25
        bird(d,bx,by,.8,t*14)
        for j in range(8):
            q=ease((t-6-j*.23)/1.2)
            x=110+(j%4)*250;y=1090+(j//4)*225
            d.arc((x-53,y-90-130*(1-q),x+53,y+68-130*(1-q)),180,358,fill=GOLD,width=8)
            txt(d,str(j+1),x,y-20-130*(1-q),40,CREAM)


def world_bird(d,t):
    hills(d,1378,(117,169,129),(91,147,123))
    disk(d,793,870,138,(249,205,127))
    cloud(d,206+18*math.sin(t),755,.84)
    line(d,(455,1380,480,898),(93,111,74),79)
    for xx,yy,rr in [(391,866,166),(561,833,171),(455,746,146)]:disk(d,xx,yy,rr,(84,153,109))
    # Tiny nest at start becomes food discovered on the ground.
    d.ellipse((389,914,559,953),fill=(169,117,80))
    for i in range(8):
        disk(d,615+i*42,1378+(i%2)*11,7,GOLD)
    q=ease((t-1)/6)
    bird(d,255+520*q,1100-235*math.sin(q*math.pi)+19*math.sin(t*10),1.05,t*12)
    hero(d,255,1480,1.06,'hope',t*2,'point')
    for i in range(4):star(d,665+i*69,1150-(i%2)*48,9,(249,217,151))


def world_work(d,t):
    # Literal split of waiting and doing collapses into a busy workspace.
    d.rectangle((0,1370,1080,1920),fill=(192,167,126))
    cloud(d,265+t*4,829,.7)
    window(d,755,861)
    rounded(d,(60,1304,471,1486),(127,163,143),46,INK,6)
    line(d,(140,1455,117,1516),INK,14);line(d,(397,1455,414,1516),INK,14)
    rounded(d,(491,1269,1055,1321),(150,109,79),13,INK,5)
    line(d,(548,1310,548,1530),INK,22);line(d,(999,1310,999,1530),INK,22)
    rounded(d,(719,1097,921,1274),NAVY,13,INK,4)
    rounded(d,(736,1113,904,1241),(146,190,171),6)
    for k in range(3):line(d,(758,1140+k*31,856+23*ease((t-4-k*.9)/1.2),1140+k*31),CREAM,7)
    q=ease((t-3)/3)
    hero(d,210+450*q,1460,1.02,'hope' if q>.4 else 'worried',t*6,'walk' if t<6 else 'work')
    bird(d,400+260*q,1020-95*math.sin(t),.73,t*13)
    if t<5:
        # A blank waiting sign wiggles until the bird nudges Amir.
        rounded(d,(74,875,477,990),WHITE,20,INK,5)
        txt(d,'TUNGGU...',275,935,45,INK)
        for k in range(3):star(d,416+k*22,1044+math.sin(t*8+k)*16,7,CORAL)
    else:
        for k in range(4):
            pop=ease((t-5-k*1.5)/.55)
            rounded(d,(855,775+k*72-45*(1-pop),973,829+k*72-45*(1-pop)),WHITE,12,JADE,3)
            txt(d,'✓',914,800+k*72-45*(1-pop),38,JADE)


def world_gratitude(d,t):
    d.rectangle((0,1395,1080,1920),fill=(197,158,127))
    rounded(d,(52,777,478,1375),(248,225,181),35,INK,6)
    window(d,744,827)
    rounded(d,(232,1320,971,1371),(136,89,70),12,INK,5)
    line(d,(319,1355,319,1517),INK,22);line(d,(877,1355,877,1517),INK,22)
    d.ellipse((537,1268,756,1323),fill=WHITE,outline=INK,width=5)
    d.polygon([(587,1277),(632,1194),(707,1277)],fill=(218,160,91),outline=INK)
    rounded(d,(860,1196,938,1302),WHITE,10,INK,4)
    d.arc((922,1201,970,1263),270,90,fill=INK,width=6)
    hero(d,300,1467,1.03,'hope',t*2,'reach')
    bird(d,791,1130+math.sin(t*4)*21,.7,t*12)
    for j in range(10):
        q=ease((t-5-j*.28)/1.0)
        a=j*2.4+t*.24
        star(d,665+int(math.cos(a)*(80+q*260)),1199+int(math.sin(a)*(55+q*200)),9+6*q,GOLD)
    for j in range(6):sprout(d,120+j*168,1530,ease((t-6-j*.33)/3),j%3==0)


def world_taqwa(d,t):
    d.rectangle((0,1410,1080,1920),fill=(82,123,118))
    d.polygon([(0,540),(460,665),(390,1410),(0,1410)],fill=(69,98,112))
    d.polygon([(1080,520),(695,645),(706,1410),(1080,1410)],fill=(57,88,101))
    # Wall is a comic visual obstacle, not a theological claim.
    wall=1-ease((t-6.1)/2)
    if wall>0:
        d.rectangle((428,889,430+335*wall,1420),fill=(135,132,119),outline=INK,width=7)
        for i in range(5):line(d,(444,935+i*91,420+333*wall,935+i*91),INK,4)
    door(d,806,1417,338,650,ease((t-7)/2),glow=True)
    for k in range(8):
        q=ease((t-7-k*.18)/.9)
        xx=693+(k%4)*69;yy=781+(k//4)*240
        star(d,xx,yy,7+7*q,(253,229,153))
    x=203+350*ease(t/10)
    hero(d,x,1450,1.0,'surprise' if t>8 else 'worried',t*8,'walk')
    bird(d,747+25*math.sin(t*2),772+math.sin(t*3)*39,.7,t*12)
    rounded(d,(80,787,398,888),WHITE,16,INK,5)
    txt(d,'JUJUR  →',240,838,40,INK)


def world_istighfar(d,t):
    d.rectangle((0,1410,1080,1920),fill=(117,159,150))
    cloud(d,164+12*t,785,1,(216,231,222))
    cloud(d,746+8*t,853,.75,(226,233,217))
    for j in range(28):
        x=(j*159+66)%1080;y=780+(j*113)%620
        fall=(t*230+j*67)%650
        line(d,(x,y+fall-320,x-15,y+fall-274),(216,236,232),5)
    # Letter returned to a neighbour is an act of repair; no invented sin is named.
    rounded(d,(738,1140,908,1256),WHITE,10,INK,5)
    txt(d,'AMANAH',823,1200,26,INK)
    hero(d,375,1445,1.02,'hope',t*2,'pray' if t<7 else 'reach')
    if t>=7:
        partner(d,837,1445,.84,t*1.4)
        bird(d,671,970+math.sin(t*3)*32,.63,t*9)
    else:bird(d,832,1082,.63,t*9)
    for i in range(10):sprout(d,88+i*111,1515,ease((t-4-i*.32)/3.6),i%3==1)


def world_marriage(d,t):
    hills(d,1370,(168,177,138),(124,159,126))
    disk(d,775,823,147,(253,211,139))
    d.arc((117,785,963,1444),181,359,fill=(229,176,132),width=33)
    line(d,(117,1110,117,1468),(229,176,132),30)
    line(d,(963,1110,963,1468),(229,176,132),30)
    for i in range(5):sprout(d,105+i*205,1493,.7+(i%2)*.25,True)
    q=ease((t-3)/3)
    hero(d,235+194*q,1467,1.0,'hope',t*2,'hold')
    partner(d,835-184*q,1467,1.0,t*2)
    bird(d,570,1014+18*math.sin(t*5),.66,t*12)
    if t<6:
        # A budget page becomes a shared plan, not a promise of quick riches.
        rounded(d,(418,1014,675,1133),WHITE,10,INK,4)
        txt(d,'BAJET',546,1060,34,INK)
        line(d,(452,1096,640,1096),JADE,5)
    else:
        d.polygon([(473,1098),(558,1000),(645,1098)],fill=(196,115,89),outline=INK)
        rounded(d,(493,1099,625,1207),(245,218,177),7,INK,4)
        window(d,523,1128,True)
        for i in range(7):
            ang=i*math.tau/7+t*.15
            star(d,550+math.cos(ang)*193,900+math.sin(ang)*100,8,GOLD)


def world_child(d,t):
    d.rectangle((0,1400,1080,1920),fill=(191,177,147))
    rounded(d,(58,842,1013,1401),(246,225,190),30,INK,5)
    d.polygon([(49,840),(535,662),(1022,840)],fill=(172,111,89),outline=INK)
    window(d,761,885)
    rounded(d,(144,1250,472,1402),(153,181,155),35,INK,6)
    hero(d,302,1484,.95,'hope',t*3,'point')
    partner(d,762,1484,.96,t*1.5)
    disk(d,541,1175-45*math.sin(t*2),70,(235,180,135),INK,3)
    disk(d,518,1168-45*math.sin(t*2),5,INK);disk(d,561,1168-45*math.sin(t*2),5,INK)
    rounded(d,(477,1223-45*math.sin(t*2),609,1373-45*math.sin(t*2)),(237,197,127),40,INK,3)
    line(d,(416,1324,488,1254-45*math.sin(t*2)),SKIN,25)
    line(d,(669,1324,600,1254-45*math.sin(t*2)),SKIN,25)
    bird(d,856,1011+math.sin(t*4)*12,.51,t*12)
    if t>5:
        for i in range(9):
            a=t*.45+i*math.tau/9
            star(d,541+math.cos(a)*150,1151+math.sin(a)*135,8,(245,188,117))


def world_charity(d,t):
    hills(d,1380,(191,170,123),(134,155,124))
    disk(d,791,782,138,(249,206,135))
    rounded(d,(698,938,1047,1407),(220,170,126),28,INK,5)
    d.polygon([(683,942),(1059,942),(994,842),(744,842)],fill=(186,112,87),outline=INK)
    rounded(d,(750,1073,1003,1239),WHITE,12,INK,4)
    txt(d,'JIRAN',877,1154,42,INK)
    q=ease((t-3)/4)
    hero(d,239+190*q,1474,1.03,'hope',t*3,'reach')
    partner(d,826,1477,.89,t*2)
    bx=496+178*q
    rounded(d,(bx-82,1194,bx+81,1318),(241,197,139),12,INK,5)
    d.polygon([(bx-83,1196),(bx,1145),(bx+81,1196),(bx,1247)],fill=(250,216,166),outline=INK)
    line(d,(bx,1148,bx,1306),CORAL,9)
    bird(d,760-60*q,900+24*math.sin(t*4),.68,t*10)
    if t>7:
        for i in range(8):
            x=88+i*128
            sprout(d,x,1540,ease((t-7-i*.28)/3),i%2==1)
            if i%2:star(d,x+18,1264-25*math.sin(t+i),10,GOLD)


WORLDS=[world_bird,world_work,world_gratitude,world_taqwa,
        world_istighfar,world_marriage,world_child,world_charity]


def world_outro(d,t):
    disk(d,540,883,223,(250,206,141))
    hills(d,1422,(122,166,131),(81,136,120))
    for i in range(8):
        q=ease((t-.45-i*.25)/.65)
        x=156+(i%4)*253;y=1087+(i//4)*263-85*(1-q)
        d.arc((x-61,y-65,x+61,y+71),181,359,fill=GOLD,width=7)
        line(d,(x-61,y+1,x-61,y+90),GOLD,7)
        line(d,(x+61,y+1,x+61,y+90),GOLD,7)
        rounded(d,(x-40,y+8,x+40,y+92),(64,115,106),9,GOLD,3)
        txt(d,str(i+1),x,y+45,35,CREAM,'s')
    if t>7:
        hero(d,300,1510,.9,'hope',t*.5,'normal')
        bird(d,729+95*math.sin(t/4),675-60*math.sin(t/3),.74,t*10)


def stage(n,t):
    idx=0 if n==-1 else 9 if n==8 else n+1
    im=BGS[idx].copy()
    d=ImageDraw.Draw(im)
    # Ambient particles and wisps continue moving behind every character.
    for k in range(11):
        xx=(k*201+120+19*math.sin(t*.43+k))%W
        yy=667+(k*211)%830+9*math.sin(t*.9+k)
        disk(d,xx,yy,3 if k%3 else 5,CREAM)
    if n==-1:world_intro(d,t)
    elif n==8:world_outro(d,t)
    else:WORLDS[n](d,t)
    # Wide setup, close reaction, then open resolution: three camera beats.
    if n>=0 and n<8:
        close=smooth((t-4.6)/.52)*(1-smooth((t-9.2)/.7))
        z=1.02+.13*close+.018*math.sin(t*.28)
        nw,nh=round(W/z),round(H/z)
        focal_x=[480,680,407,555,560,540,550,580][n]
        dx=round((focal_x-nw/2)*close+(W-nw)/2*(1-close)+12*math.sin(t*.19))
        dy=round((1110-nh/2)*close+(H-nh)/2*(1-close)+10*math.cos(t*.31))
        dx=max(0,min(W-nw,dx));dy=max(0,min(H-nh,dy))
        im=im.crop((dx,dy,dx+nw,dy+nh)).resize((W,H),Image.Resampling.BILINEAR)
    return im


def title_card(d,tag,a,b,accent,local,pop=0):
    q=ease((local-pop)/.58)
    dy=int((1-q)*95)
    # Drop shadow and slight squash are the physical reveal of each beat.
    rounded(d,(57,225+dy,1029,625+dy),(65,82,77),39)
    rounded(d,(48,213+dy,1020,608+dy),WHITE,39,INK,5)
    rounded(d,(84,241+dy,497,315+dy),accent,22)
    txt(d,tag,290,278+dy,35,WHITE,maxw=390)
    txt(d,a,539,407+dy,58,INK,maxw=881)
    txt(d,b,539,491+dy,57,INK,maxw=881)
    disk(d,970,264+dy,17,accent)
    star(d,970,264+dy,10,WHITE)


def comic_caption(d,tag,a,b,accent,local):
    """Alternating, staggered speech strips instead of another full card."""
    q=ease(local/.48)
    # The upper and lower strips enter from opposing edges with overshoot.
    dx1=int((1-q)*-420+7*math.sin(min(local,1)*math.pi))
    dx2=int((1-q)*520-7*math.sin(min(local,1)*math.pi))
    rounded(d,(82,232,355,306),accent,20,INK,3)
    txt(d,tag,217,270,34,WHITE,maxw=240)
    rounded(d,(105+dx1,327,977+dx1,457),(45,75,75),26)
    rounded(d,(93+dx1,315,965+dx1,446),WHITE,26,INK,5)
    txt(d,a,528+dx1,380,56,INK,maxw=810)
    rounded(d,(132+dx2,477,996+dx2,606),(45,75,75),26)
    rounded(d,(120+dx2,465,984+dx2,594),accent,26,INK,5)
    txt(d,b,552+dx2,529,55,INK,maxw=808)
    d.polygon([(882+dx2,593),(934+dx2,593),(900+dx2,629)],fill=accent,outline=INK)
    if local>1.1:
        for k in range(3):star(d,87+k*29,529+(k%2)*31,8,GOLD)


def overlay_scene(im,n,t):
    scene=SCENES[n]
    d=ImageDraw.Draw(im)
    accent=scene['accent']
    hdr=CREAM if n==3 else INK
    # Editorial header + unobstructed verse citation.
    txt(d,'SENI MEMAHAMI BAHASA REZEKI',74,79,31,hdr,anchor='lm')
    txt(d,f'{n+1:02} / 08',1003,79,37,hdr,anchor='rm')
    line(d,(72,137,1007,137),hdr,3)
    txt(d,scene['title'],541,177,57,hdr,maxw=930)
    beat=0 if t<4.7 else 1 if t<9.5 else 2
    start=0 if beat==0 else 4.7 if beat==1 else 9.5
    a,b=scene['beats'][beat]
    if n%2:
        comic_caption(d,f'PINTU {n+1:02}',a,b,accent,t-start)
    else:
        title_card(d,f'PINTU {n+1:02}',a,b,accent,t-start)
    # A stationary lower panel carries the actual Malay translation throughout
    # the chapter, with name, surah number, verse number and translator credit.
    panel=translation_panel(n)
    im.paste(panel,(0,1545),panel)
    return im


def intro(im,t):
    d=ImageDraw.Draw(im)
    txt(d,'HUJUNG BULAN.',540,169,76,CREAM,maxw=900)
    if t<5.5:
        title_card(d,'CERITA KITA','Baki makin nipis.','Fikiran makin sibuk.',(200,118,86),t)
    elif t<9:
        title_card(d,'SATU PERSOALAN','Burung di wayar itu...','tenang saja?',(94,156,131),t-5.5)
    else:
        title_card(d,'RENUNGAN','Rezeki bukan cuma gaji.','Ada lapan pintu.',(111,168,139),t-9)
    if 5.55<t<7.95:
        q=ease((t-5.55)/.24)*(1-ease((t-7.55)/.4))
        cx,cy=849,780
        pts=[]
        for i in range(20):
            a=i*math.pi/10-math.pi/2
            r=(95 if i%2==0 else 64)*q
            pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
        d.polygon(pts,fill=GOLD,outline=INK)
        if q>.3:txt(d,'HAH?!',cx,cy,43,INK)
    txt(d,'Berdasarkan renungan ayat-ayat Al-Quran',540,1747,36,CREAM,maxw=935)
    return im


def outro(im,t):
    d=ImageDraw.Draw(im)
    if t<9:
        title_card(d,'LAPAN PINTU','Rezeki lebih luas','daripada wang.',(96,153,130),t)
    else:
        title_card(d,'DOA','Ya Allah, berkati rezeki','yang Engkau beri.',(191,139,92),t-9)
    rounded(d,(76,1570,1004,1790),(32,76,74),30,GOLD,3)
    if t<9:
        txt(d,'Syukur  •  Ikhtiar  •  Tawakal',540,1680,49,CREAM,maxw=900)
    else:
        txt(d,'Cukupkan kami dengan yang halal.',540,1659,45,CREAM,maxw=850)
        txt(d,'Aamiin.',540,1722,49,GOLD,'s')
    txt(d,'Renungan ringkas  •  Rujukan ayat pada setiap pintu',540,1859,26,CREAM,maxw=930)
    return im


def transition(im,local):
    # Comic-style iris between locations, applied only to scene art/text panels.
    dur=.56
    if local<dur:
        p=1-ease(local/dur)
    elif local>BEAT-dur:
        p=ease((local-(BEAT-dur))/dur)
    else:return im
    ov=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(ov)
    w=int(p*W*.55)
    d.polygon([(0,0),(w,0),(max(0,w-190),H),(0,H)],fill=(34,86,84,255))
    d.polygon([(W,0),(W-w,0),(min(W,W-w+190),H),(W,H)],fill=(42,98,91,255))
    for sign in (-1,1):
        x=W/2+sign*(W/2-w)
        line(d,(x,0,x-sign*190,H),GOLD,11)
    return Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')


def frame(t):
    if t<INTRO:
        im=intro(stage(-1,t),t)
    elif t<OUTRO:
        n=min(7,int((t-INTRO)//BEAT));local=t-(INTRO+n*BEAT)
        im=overlay_scene(stage(n,local),n,local)
        im=transition(im,local)
    else:
        im=outro(stage(8,t-OUTRO),t-OUTRO)
    fade=min(1,t/.45,(LENGTH-t)/1.0)
    if fade<1:im=Image.blend(Image.new('RGB',(W,H),NAVY),im,clip(fade))
    return im


def preview():
    times=[2,6.3,10.5]+[INTRO+i*BEAT+v for i in range(8) for v in (2.5,7.4,12.1)]+[143,150,156]
    sheet=Image.new('RGB',(270*6,480*5),NAVY)
    for i,t in enumerate(times):
        im=frame(t)
        if i in (0,4,8,12,16,20,24,27): im.save(OUT/f'Rezeki_Cartoon_Preview_{i:02}.jpg',quality=90)
        sheet.paste(im.resize((270,480),Image.Resampling.LANCZOS),((i%6)*270,(i//6)*480))
    sheet.save(OUT/'8_Pintu_Rezeki_Cartoon_160s_Storyboard.jpg',quality=88)
    print(OUT/'8_Pintu_Rezeki_Cartoon_160s_Storyboard.jpg',flush=True)


def render():
    audio=OUT/'8_Pintu_Rezeki_music_sfx_160s.wav'
    if not audio.exists():
        import audio_rezeki
        audio_rezeki.main()
    dest=OUT/'8_Pintu_Rezeki_Animasi_Cerita_160s_9x16.mp4'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24',
         '-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0',
         '-i',str(audio),'-c:v','libx264','-preset','veryfast','-crf','19',
         '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(LENGTH),
         '-movflags','+faststart',str(dest)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(FPS*LENGTH):
            proc.stdin.write(frame(i/FPS).tobytes())
            if i%(FPS*8)==0: print('Rendered',i/FPS,'/',LENGTH,'s',flush=True)
    finally:
        proc.stdin.close()
        rc=proc.wait()
        if rc:raise RuntimeError(f'ffmpeg exited {rc}')
    print(dest,flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
    preview() if args.preview else render()
