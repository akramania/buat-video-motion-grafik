#!/usr/bin/env python3
"""Reproduce SV1401–SV1500: 100 original transparent promotional assemblies.

Static SVG only. Motion suggestions live in metadata and do not animate SVGs.
No trademarks, prices, fabricated ratings, scarcity or testimonial claims.
Run: python generate_promo_commerce.py [--output DIR] [--index FILE]
"""
from pathlib import Path
from xml.sax.saxutils import escape
import argparse,json,math

BLUE='#C9E9F7';MINT='#D4F0E4';LILAC='#E5DCF7';CREAM='#FFF2D8';INK='#55718A';WHITE='#FFFFFF'

def num(n):return str(round(n,2)).rstrip('0').rstrip('.') if isinstance(n,float) else str(n)
class Scene:
    def __init__(self):self.layers={k:[] for k in ['main','accent','details']}
    def add(self,tag,layer='main',**attrs):
        attrs.setdefault('stroke',INK);attrs.setdefault('stroke-width',3.6);attrs.setdefault('stroke-linejoin','round');attrs.setdefault('stroke-linecap','round')
        self.layers[layer].append('<'+tag+' '+ ' '.join(f'{k}="{escape(str(num(v)) if isinstance(v,(int,float)) else str(v))}"' for k,v in attrs.items())+'/>' )
    def rect(self,x,y,w,h,c=BLUE,r=9,l='main'):self.add('rect',l,x=x,y=y,width=w,height=h,rx=r,fill=c)
    def circle(self,x,y,r,c=MINT,l='main'):self.add('circle',l,cx=x,cy=y,r=r,fill=c)
    def line(self,x1,y1,x2,y2,l='details',color=INK,width=3.6):self.add('line',l,x1=x1,y1=y1,x2=x2,y2=y2,fill='none',stroke=color,**{'stroke-width':width})
    def path(self,d,c='none',l='main'):self.add('path',l,d=d,fill=c)
    def poly(self,points,c=BLUE,l='main'):self.add('polygon',l,points=' '.join(f'{num(x)},{num(y)}' for x,y in points),fill=c)
    def ellipse(self,x,y,rx,ry,c=CREAM,l='main'):self.add('ellipse',l,cx=x,cy=y,rx=rx,ry=ry,fill=c)
    def star(self,x,y,r=12,c=CREAM,l='accent',n=5):
        self.poly([(x+math.sin(j*math.pi/n)*r*(1 if j%2==0 else .45),y-math.cos(j*math.pi/n)*r*(1 if j%2==0 else .45)) for j in range(n*2)],c,l)
    def arrow(self,x1,y1,x2,y2,l='accent'):
        self.line(x1,y1,x2,y2,l);a=math.atan2(y2-y1,x2-x1)
        self.line(x2,y2,x2-10*math.cos(a-.6),y2-10*math.sin(a-.6),l);self.line(x2,y2,x2-10*math.cos(a+.6),y2-10*math.sin(a+.6),l)
    def card(self,x,y,w,h,c=WHITE,bars=2):
        self.rect(x,y,w,h,c,7)
        for j in range(bars):self.line(x+9,y+11+j*10,x+w-10-j%2*7,y+11+j*10)
    def package(self,x,y,w=50,h=45,c=CREAM):
        self.rect(x,y,w,h,c,4);self.line(x+w*.5,y,x+w*.5,y+h);self.rect(x+w*.5-7,y,14,13,LILAC,1,'accent')
    def bottle(self,x,y,w=30,h=60,c=MINT):
        self.rect(x,y+12,w,h-12,c,8);self.rect(x+w*.22,y,w*.56,14,LILAC,3,'accent');self.rect(x+5,y+h*.47,w-10,h*.24,WHITE,3,'details')
    def bubble(self,x,y,w=67,h=43,c=BLUE,bars=1):
        self.rect(x,y,w,h,c,12);self.path(f'M {x+15} {y+h} L {x+12} {y+h+10} L {x+30} {y+h}',c,'main')
        for j in range(bars):self.line(x+12,y+15+j*10,x+w-12-j*8,y+15+j*10)
    def person(self,x,y,r=12,c=LILAC):
        self.circle(x,y,r,c);self.path(f'M {x-r*1.5} {y+36} Q {x-r*1.4} {y+15} {x} {y+15} Q {x+r*1.4} {y+15} {x+r*1.5} {y+36} Z',c)
    def heart(self,x,y,size=16,c=LILAC,l='accent'):
        self.path(f'M {x} {y+size*.78} C {x-size*1.4} {y-size*.2} {x-size*.7} {y-size*1.1} {x} {y-size*.25} C {x+size*.7} {y-size*1.1} {x+size*1.4} {y-size*.2} {x} {y+size*.78} Z',c,l)
    def cursor(self,x,y,size=28,l='accent'):self.poly([(x,y),(x+size*.2,y+size),(x+size*.45,y+size*.69),(x+size*.71,y+size*.86),(x+size*.86,y+size*.66),(x+size*.6,y+size*.5),(x+size,y+size*.36)],CREAM,l)
    def mic(self,x,y,w=28,h=48):
        self.rect(x,y,w,h,LILAC,w/2);self.path(f'M {x-8} {y+h*.55} V {y+h-3} Q {x-8} {y+h+14} {x+w/2} {y+h+14} Q {x+w+8} {y+h+14} {x+w+8} {y+h-3} V {y+h*.55}','none','details');self.line(x+w/2,y+h+14,x+w/2,y+h+30);self.line(x+w/2-15,y+h+30,x+w/2+15,y+h+30)
    def camera(self,x,y,w=65,h=45):
        self.rect(x,y,w,h,BLUE,7);self.circle(x+w*.55,y+h*.52,min(h*.29,w*.2),LILAC,'accent');self.rect(x+8,y-7,20,10,MINT,3,'accent');self.line(x+10,y+10,x+20,y+10)
    def phone(self,x,y,w=50,h=89,c=BLUE):
        self.rect(x,y,w,h,c,11);self.rect(x+6,y+14,w-12,h-27,WHITE,3,'accent');self.line(x+w*.38,y+7,x+w*.62,y+7);self.circle(x+w/2,y+h-7,2.3,INK,'details')
    def spark(self,x,y,r=8):
        self.line(x-r,y,x+r,y,'accent');self.line(x,y-r,x,y+r,'accent')
    def svg(self,title):
        parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img">','<title>'+escape(title)+'</title>']
        for k,v in self.layers.items():parts += [f'<g id="{k}">',*v,'</g>']
        return '\n'.join(parts+['</svg>'])+'\n'

OFFER_TITLES=['Comparison shelf with blank value cards','Bundle tray with linked components','Three tier plan board','Itemised value ledger with product','Coupon envelope and resource stack','Feature balance and product pair','Cost structure mosaic','Gift and resource bundle','Upgrade route with modular steps','Sliding option plan rack','Benefit orbit around package','Modular starter kit layout','Package cross section with contents','Stacked value pages with tab dividers','Value ledger and neutral chart','Conditional choice branch assembly','Refill package and reusable bottle','Access key with resource portfolio','Comparison flipbook with sample planes','Discovery telescope and feature cards','Choice board with three alternatives','Layered value pyramid kit','Add on connector system','Bundle download desk','Transparent inclusion folder']
AUDIENCE_TITLES=['Question and answer gallery','Audience poll board without counts','Topic discussion wall','Question queue and listening host','Applause hands and celebratory response accents','Pointer led reaction chain','Bookmark conversation timeline','Emotion selection wheel','Collaborative learning circle','Question bridge between participants','Popup discussion across screens','Reciprocal message exchange','Audience topic cluster','Message inbox sorting tray','Drag and choose interaction board','Insight magnifier and comments','Pinned announcement discussion board','Comment forest with branching ideas','Story reply thread panels','Idea sharing environment','Listening antenna and conversation','Collaborative puzzle conversation','Balanced speaking and listening','Question cards for audience participation','Follow up note and message trail']
PRODUCTION_TITLES=['Desktop commerce presentation set','Phone overhead demonstration mount','Stream switching control deck','Adjustable two light production kit','Microphone audio routing chain','Camera teleprompter station','Product turntable with shot marker','Shot director preview grid','Overhead product flatlay station','Live monitoring desk','Blank background presentation frame','Multi camera routing arrangement','Clapperboard and product display','Tactile detail demonstration station','Production cue card carousel','Cable and accessory organisation tray','Acoustic panel and microphone','Compact tabletop presentation kit','Unboxing camera arrangement','Generic reaction overlay composition','Rotating product presentation rig','Lens and colour reference board','Product demonstration step board','Product photography lightbox','Subtitle cue and playback gate']
LAUNCH_TITLES=['Product unveiling plinth','Confetti preparation kit','Ceremony arch and display platform','Opening curtain showcase','Calendar invitation and gift','Folded ribbon presentation package','Presentation podium with cue cards','Paper rocket and launch platform','Collective hands around launch kit','Blooming component showcase','Product cart procession','Milestone roadmap to presentation','Spotlight unveiling scene','Banner drone and showcase package','Fireworks around blank launch card','Origami star assembly','Miniature stage with balloons','Pennant line and product parcel','Journey finish gate','Event map with blank destination pins','Ribbon runner presentation','Pop up launch storybook','Team collection presentation tray','Showcase frame and radiating pieces','Lantern procession display']

def offer(i):
    s=Scene()
    if i==0:
        s.rect(27,170,202,20,MINT,4);s.line(48,190,48,226);s.line(208,190,208,226);s.bottle(47,80,33,78);s.package(103,102,49,56);s.rect(180,82,34,76,LILAC,6);s.card(30,27,82,34,CREAM,1);s.card(142,27,82,34,BLUE,1);s.line(129,31,129,150,'accent')
    elif i==1:
        s.path('M 26 154 L 55 111 L 202 111 L 231 154 L 219 219 L 38 219 Z',BLUE);s.bottle(55,59,36,98);s.card(104,51,53,89,LILAC,3);s.package(171,78,43,71);s.line(60,172,196,172);s.line(92,153,92,189,'accent');s.line(163,153,163,189,'accent');s.spark(127,201)
    elif i==2:
        for x,y,w,h,c in [(24,79,57,132,CREAM),(96,48,63,163,MINT),(175,91,57,120,LILAC)]:s.card(x,y,w,h,c,3);s.rect(x+8,y+h-34,w-16,21,WHITE,4,'accent')
        s.path('M 45 53 Q 127 18 207 56','none','accent');s.spark(127,26)
    elif i==3:
        s.card(22,34,116,190,CREAM,0);s.line(36,57,114,57)
        for j in range(4):s.rect(35,78+j*28,18,17,BLUE,4,'details');s.line(66,87+j*28,119,87+j*28)
        s.line(35,199,122,199);s.package(163,101,65,72);s.arrow(146,190,203,190);s.star(194,55,17)
    elif i==4:
        s.path('M 27 95 L 128 42 L 228 95 L 228 214 L 27 214 Z',BLUE);s.card(77,21,104,119,CREAM,3);s.path('M 27 95 L 128 161 L 228 95','none','accent');s.path('M 27 214 L 92 150 M 228 214 L 164 150','none','details');s.rect(91,177,74,18,MINT,5,'accent');s.spark(219,35)
    elif i==5:
        s.line(128,42,128,188);s.line(63,214,193,214);s.poly([(103,213),(128,171),(153,213)],MINT);s.line(56,84,200,84);s.line(61,83,35,149);s.line(61,83,88,149);s.path('M 31 149 Q 61 181 91 149 Z',BLUE);s.line(195,83,167,149);s.line(195,83,223,149);s.path('M 163 149 Q 193 181 225 149 Z',LILAC);s.card(37,115,48,32,WHITE,1);s.bottle(181,106,25,42);s.circle(128,69,16,CREAM,'accent')
    elif i==6:
        s.rect(27,27,202,202,WHITE,13)
        for x,y,w,h,c in [(41,42,81,66,BLUE),(132,42,83,66,MINT),(41,119,49,90,LILAC),(100,119,115,42,CREAM),(100,172,115,37,BLUE)]:s.rect(x,y,w,h,c,6,'accent')
        s.line(56,62,105,62);s.line(147,64,199,64);s.line(117,141,195,141);s.line(117,191,182,191);s.spark(65,164)
    elif i==7:
        s.package(34,140,99,73);s.rect(26,119,115,28,LILAC,5,'accent');s.line(83,122,83,211);s.path('M 82 119 C 31 69 48 53 84 83 C 124 51 140 75 82 119',MINT,'accent');s.card(151,47,75,118,CREAM,3);s.card(144,173,86,43,BLUE,1);s.spark(51,40)
    elif i==8:
        for j,(x,y,c) in enumerate([(23,170,BLUE),(91,111,MINT),(165,48,LILAC)]):s.rect(x,y,67,57,c,8);s.card(x+11,y+11,44,28,WHITE,1)
        s.arrow(77,147,96,126);s.arrow(149,86,169,65);s.path('M 29 213 H 224','none','details');s.spark(199,144)
    elif i==9:
        s.rect(29,28,198,196,CREAM,11);s.line(46,84,210,84);s.line(46,141,210,141);s.line(46,199,210,199)
        for j,(x,c) in enumerate([(53,BLUE),(104,MINT),(149,LILAC)]):s.rect(x,47+j*57,64,25,c,7,'accent');s.circle(x+52,59+j*57,5,WHITE,'details')
        s.cursor(200,163,24)
    elif i==10:
        s.package(92,96,71,65);s.ellipse(128,128,101,88,'none','accent')
        for x,y,c in [(43,81,BLUE),(128,29,CREAM),(210,91,LILAC),(192,195,MINT),(67,205,CREAM)]:s.card(x-21,y-14,43,29,c,1)
        s.line(89,84,104,98);s.line(167,92,154,107);s.line(176,179,159,161)
    elif i==11:
        s.rect(26,32,204,192,BLUE,12);s.rect(39,45,83,83,CREAM,6,'accent');s.rect(133,45,83,45,MINT,6,'accent');s.rect(133,102,83,97,LILAC,6,'accent');s.rect(39,141,83,58,WHITE,6,'accent');s.package(56,62,49,47);s.bottle(160,122,30,60);s.line(148,66,200,66);s.line(53,161,106,161);s.spark(80,179)
    elif i==12:
        s.path('M 26 92 L 127 40 L 230 92 L 230 189 L 128 231 L 26 189 Z',CREAM);s.path('M 26 92 L 128 136 L 230 92 M 128 136 V 231','none','accent');s.path('M 140 145 L 216 115 L 216 176 L 140 207 Z',BLUE,'accent');s.bottle(46,104,29,64);s.card(84,114,30,64,LILAC,2);s.line(155,151,198,135);s.line(155,177,198,161);s.arrow(129,24,129,56)
    elif i==13:
        for j,c in enumerate([BLUE,MINT,LILAC]):s.card(42+j*15,39+j*28,155,135,c,3)
        s.rect(25,72,32,23,CREAM,5,'accent');s.rect(40,125,32,23,CREAM,5,'accent');s.rect(55,178,32,23,CREAM,5,'accent');s.cursor(204,192,26)
    elif i==14:
        s.card(27,39,104,178,CREAM,4);s.line(43,149,111,149);s.line(43,169,90,169);s.line(155,201,225,201);s.line(155,201,155,84);s.rect(166,156,12,44,BLUE,3,'accent');s.rect(186,128,12,72,MINT,3,'accent');s.rect(206,105,12,95,LILAC,3,'accent');s.circle(189,52,22,WHITE,'accent');s.spark(189,52,10)
    elif i==15:
        s.card(80,25,96,62,BLUE,2);s.line(128,87,128,117);s.line(61,117,196,117);s.line(61,117,61,143);s.line(196,117,196,143);s.card(23,145,75,69,MINT,2);s.card(157,145,75,69,LILAC,2);s.circle(128,119,11,CREAM,'accent');s.arrow(61,219,102,219);s.arrow(196,219,157,219)
    elif i==16:
        s.package(24,136,96,80);s.bottle(155,75,52,138);s.path('M 75 67 C 111 35 161 31 198 57','none','accent');s.arrow(190,47,198,57);s.path('M 214 108 Q 240 134 223 167','none','accent');s.line(47,159,96,159);s.line(47,181,83,181);s.circle(69,43,18,MINT,'accent')
    elif i==17:
        s.circle(71,98,42,CREAM);s.circle(71,98,18,WHITE,'details');s.path('M 109 96 H 204 V 117 H 184 V 133 H 161 V 117 H 108 Z',MINT,'accent');s.card(129,149,96,71,BLUE,2);s.card(40,170,67,49,LILAC,1);s.line(67,143,67,158)
    elif i==18:
        s.path('M 27 61 L 117 43 L 117 210 L 27 224 Z',CREAM);s.path('M 117 43 L 228 65 L 228 224 L 117 210 Z',BLUE);s.path('M 128 60 L 219 76 L 219 207 L 128 195 Z',LILAC,'accent');s.line(48,87,98,77);s.line(48,109,98,100);s.line(149,104,198,111);s.line(149,127,198,134);s.line(149,150,187,156);s.spark(62,171)
    elif i==19:
        s.path('M 26 118 L 47 72 L 166 123 L 148 166 Z',BLUE);s.ellipse(158,145,24,33,LILAC,'accent');s.ellipse(35,96,17,27,CREAM,'accent');s.line(151,178,128,223);s.line(151,178,176,223);s.card(170,25,60,59,MINT,2);s.card(190,94,40,45,CREAM,1);s.spark(93,44)
    elif i==20:
        s.rect(24,34,207,188,CREAM,11)
        for j,c in enumerate([BLUE,MINT,LILAC]):s.card(39+j*63,55,52,100,c,3);s.circle(65+j*63,183,13,WHITE,'accent')
        s.cursor(132,168,27);s.line(37,207,218,207)
    elif i==21:
        s.poly([(24,221),(231,221),(207,168),(48,168)],BLUE);s.poly([(50,167),(205,167),(179,113),(76,113)],MINT,'accent');s.poly([(78,112),(177,112),(150,59),(104,59)],LILAC,'accent');s.package(111,22,33,38);s.line(71,193,185,193);s.line(97,140,159,140);s.line(115,87,140,87)
    elif i==22:
        s.package(90,91,77,74);s.card(25,27,60,51,BLUE,2);s.card(171,25,59,52,LILAC,2);s.card(24,175,61,50,MINT,2);s.card(175,175,57,51,CREAM,2);s.line(82,75,99,97);s.line(172,77,160,99);s.line(83,182,96,162);s.line(171,184,159,163);s.circle(128,128,14,WHITE,'details');s.spark(128,128,7)
    elif i==23:
        s.rect(54,34,144,101,BLUE,9);s.card(68,47,49,62,WHITE,2);s.card(128,47,54,62,LILAC,2);s.line(125,136,125,154);s.line(88,154,162,154);s.package(66,180,54,46);s.package(139,180,54,46);s.arrow(127,164,127,215);s.line(28,228,228,228)
    else:
        s.path('M 26 64 H 83 L 98 45 H 230 V 222 H 26 Z',BLUE);s.rect(40,83,175,124,WHITE,8,'accent');s.bottle(55,104,33,77);s.package(105,120,46,61);s.card(163,104,36,77,LILAC,3);s.line(48,69,68,69);s.path('M 34 194 L 210 96','none','details')
    return s

def audience(i):
    s=Scene()
    if i==0:
        s.bubble(25,26,89,63,BLUE,2);s.bubble(140,66,88,63,MINT,2);s.bubble(28,145,98,62,LILAC,2);s.person(190,178,17,CREAM);s.line(118,99,144,115,'accent');s.line(133,162,161,183,'accent')
    elif i==1:
        s.rect(39,27,178,194,CREAM,12)
        for j,c in enumerate([BLUE,MINT,LILAC]):s.circle(62,67+j*53,10,WHITE,'accent');s.rect(83,53+j*53,113,28,c,6,'accent');s.line(96,67+j*53,165,67+j*53)
        s.cursor(177,188,31)
    elif i==2:
        s.rect(26,32,205,190,BLUE,9)
        for j,(x,y,c) in enumerate([(39,49,CREAM),(124,49,LILAC),(45,137,MINT),(144,137,WHITE)]):s.card(x,y,66,61,c,2)
        s.line(31,119,220,119,'accent');s.circle(111,116,7,LILAC,'accent');s.spark(217,50)
    elif i==3:
        for j,c in enumerate([BLUE,LILAC,MINT]):s.bubble(22+j*18,29+j*42,85,40,c,1)
        s.person(185,136,21,CREAM);s.path('M 147 119 Q 135 154 153 178','none','accent');s.path('M 133 116 Q 117 154 138 183','none','accent');s.rect(151,196,75,28,BLUE,7,'accent')
    elif i==4:
        s.path('M 39 210 L 27 171 L 26 124 Q 32 112 39 125 L 46 147 V 88 Q 55 76 61 89 V 140 L 65 72 Q 73 61 81 75 L 80 142 L 90 93 Q 101 85 106 98 L 97 165 L 116 148 Q 129 149 126 162 L 104 189 L 102 220 Z',BLUE)
        s.path('M 150 217 L 131 184 Q 125 168 138 168 L 153 177 L 145 113 Q 151 100 159 112 L 170 149 V 96 Q 178 83 185 97 L 186 149 L 194 113 Q 204 106 209 119 L 208 163 L 221 144 Q 233 142 232 155 L 219 192 L 211 220 Z',MINT,'accent');s.star(133,43,16);s.spark(206,61)
    elif i==5:
        s.cursor(35,180,35);s.line(74,172,109,139,'accent');s.bubble(29,35,72,59,BLUE,2);s.heart(132,102,20,LILAC);s.circle(202,63,25,CREAM,'accent');s.path('M 191 62 Q 202 78 213 62','none','details');s.circle(194,54,1.9,INK,'details');s.circle(210,54,1.9,INK,'details');s.arrow(114,68,150,68);s.arrow(173,113,190,138);s.card(164,157,66,60,MINT,2)
    elif i==6:
        s.line(56,29,56,225);s.bubble(88,35,133,48,BLUE,2);s.bubble(88,108,109,44,MINT,2);s.bubble(88,179,133,39,LILAC,1)
        for y in [58,128,197]:s.circle(56,y,10,CREAM,'accent');s.line(66,y,83,y)
        s.poly([(25,30),(40,30),(40,78),(32,68),(25,78)],LILAC,'accent')
    elif i==7:
        s.circle(128,128,92,CREAM);s.circle(128,128,29,WHITE,'accent')
        for j,c in enumerate([BLUE,MINT,LILAC,BLUE,MINT,LILAC]):
            a=j*math.tau/6;x=128+65*math.sin(a);y=128-65*math.cos(a);s.circle(x,y,18,c,'accent');s.line(x-6,y-3,x-3,y-3);s.line(x+3,y-3,x+6,y-3);s.path(f'M {x-7} {y+5} Q {x} {y+11 if j%2==0 else y+1} {x+7} {y+5}','none','details')
        s.cursor(119,115,28)
    elif i==8:
        s.circle(128,128,80,'none','accent');s.card(92,102,72,49,CREAM,2)
        for x,y,c in [(128,37,BLUE),(209,105,MINT),(181,193,LILAC),(68,193,BLUE),(45,105,MINT)]:s.person(x,y,11,c)
        s.line(89,112,102,114);s.line(160,112,176,112)
    elif i==9:
        s.person(46,133,15,BLUE);s.person(210,133,15,LILAC);s.path('M 74 186 Q 129 128 183 186','none','accent');s.path('M 74 201 Q 129 149 183 201','none','accent');s.bubble(79,29,98,67,MINT,2);s.line(128,110,128,149);s.spark(127,171)
    elif i==10:
        s.phone(27,102,61,114);s.rect(119,107,111,75,BLUE,7);s.line(172,182,172,205);s.line(147,206,198,206);s.bubble(47,26,91,55,MINT,2);s.bubble(137,45,78,49,LILAC,2);s.line(111,81,95,109,'accent');s.line(176,98,176,111,'accent')
    elif i==11:
        s.person(53,142,15,BLUE);s.person(204,142,15,MINT);s.bubble(27,32,85,48,CREAM,2);s.bubble(142,91,87,49,LILAC,2);s.arrow(118,54,157,54);s.arrow(136,172,96,172);s.line(63,111,63,94,'accent');s.line(198,81,198,66,'accent')
    elif i==12:
        s.person(129,111,17,CREAM);s.bubble(25,35,66,41,BLUE,1);s.bubble(170,31,62,45,LILAC,1);s.bubble(28,174,64,42,MINT,1);s.bubble(171,174,61,42,BLUE,1);s.line(91,71,112,101,'accent');s.line(170,72,146,102,'accent');s.line(96,177,114,158,'accent');s.line(170,177,145,158,'accent')
    elif i==13:
        s.path('M 25 158 L 51 109 H 205 L 231 158 V 222 H 25 Z',BLUE);s.path('M 25 158 H 96 Q 103 180 128 180 Q 152 180 159 158 H 231','none','details');s.bubble(35,32,70,49,CREAM,2);s.bubble(125,56,90,53,LILAC,2);s.arrow(82,95,93,130);s.arrow(163,122,161,140)
    elif i==14:
        s.rect(24,31,209,194,CREAM,11);s.rect(38,46,68,59,BLUE,7,'accent');s.rect(137,46,77,59,LILAC,7,'accent');s.rect(38,137,76,62,MINT,7,'accent');s.rect(145,139,68,58,WHITE,7,'accent');s.arrow(119,76,125,144);s.cursor(116,104,36);s.line(50,65,90,65);s.line(153,66,197,66);s.line(54,157,95,157)
    elif i==15:
        s.bubble(23,44,99,73,BLUE,3);s.bubble(43,140,97,70,MINT,3);s.circle(179,124,43,LILAC,'accent');s.circle(179,124,29,WHITE,'details');s.line(209,156,231,194,'accent',width=5);s.path('M 164 123 L 175 133 L 197 110','none','details');s.spark(192,43)
    elif i==16:
        s.rect(28,35,201,186,BLUE,11);s.card(45,53,119,103,CREAM,3);s.circle(101,52,9,LILAC,'accent');s.path('M 101 61 V 78','none','details');s.bubble(63,174,151,35,MINT,1);s.person(199,94,12,LILAC);s.line(179,143,179,164,'accent')
    elif i==17:
        s.line(128,76,128,225);s.bubble(80,24,94,48,CREAM,2);s.bubble(25,102,72,49,BLUE,2);s.bubble(159,101,73,49,MINT,2);s.bubble(68,176,119,39,LILAC,1);s.line(128,91,91,112,'accent');s.line(128,91,164,112,'accent');s.line(128,161,143,177,'accent');s.path('M 105 225 Q 128 213 151 225','none','details')
    elif i==18:
        s.rect(27,25,90,181,BLUE,9);s.card(39,45,66,61,WHITE,2);s.bubble(130,53,96,42,LILAC,2);s.bubble(140,122,86,42,MINT,2);s.bubble(130,187,96,36,CREAM,1);s.line(118,77,126,77,'accent');s.line(123,78,123,205);s.line(123,144,136,144);s.line(123,205,126,205)
    elif i==19:
        s.path('M 47 223 Q 43 166 107 153 Q 111 184 77 201',MINT);s.path('M 107 153 Q 132 112 163 94','none','details');s.bubble(121,31,94,59,CREAM,2);s.bubble(26,48,73,47,BLUE,2);s.bubble(157,151,72,50,LILAC,2);s.star(95,121,15);s.line(82,220,198,220)
    elif i==20:
        s.path('M 114 107 Q 88 95 92 67 Q 96 40 126 35 Q 158 37 164 65 Q 173 97 140 111',BLUE);s.circle(128,80,17,WHITE,'accent');s.line(127,110,127,179);s.line(88,222,128,177);s.line(168,222,128,177);s.bubble(20,128,76,43,MINT,2);s.bubble(165,127,68,43,LILAC,2);s.path('M 49 31 Q 19 60 49 95 M 207 31 Q 237 60 207 95','none','accent')
    elif i==21:
        s.path('M 27 42 H 109 V 91 Q 129 65 146 88 Q 153 108 131 117 H 213 V 213 H 129 V 168 Q 104 198 90 174 Q 80 155 109 147 H 27 Z',BLUE);s.path('M 128 27 H 229 V 123 H 179 Q 204 147 179 160 Q 158 162 150 139 H 129 V 88 Q 111 111 97 93 Q 90 69 128 76 Z',MINT,'accent');s.bubble(43,65,52,43,WHITE,1);s.bubble(166,176,59,40,LILAC,1)
    elif i==22:
        s.line(128,38,128,202);s.line(34,88,222,88);s.circle(128,88,15,CREAM,'accent');s.line(60,88,34,164);s.line(60,88,86,164);s.path('M 31 164 Q 60 195 90 164 Z',BLUE);s.line(195,88,169,164);s.line(195,88,221,164);s.path('M 165 164 Q 195 195 225 164 Z',MINT);s.bubble(35,114,52,34,WHITE,1);s.mic(184,114,22,38);s.line(85,221,171,221);s.poly([(101,220),(128,190),(155,220)],LILAC,'accent')
    elif i==23:
        for j,c in enumerate([BLUE,MINT,LILAC]):s.card(26+j*28,36+j*43,141,70,c,3)
        s.person(201,159,14,CREAM);s.circle(205,48,22,WHITE,'accent');s.path('M 198 43 Q 202 34 212 42 Q 218 50 206 55 V 59','none','details');s.circle(206,66,1.9,INK,'details')
    else:
        s.card(30,35,118,166,CREAM,4);s.path('M 30 178 L 56 201 H 30 Z',LILAC,'accent');s.bubble(153,50,75,43,BLUE,2);s.bubble(157,119,71,40,MINT,2);s.bubble(155,185,73,38,LILAC,1);s.line(172,104,172,112);s.line(175,170,175,180);s.star(114,180,13)
    return s

def production(i):
    s=Scene()
    if i==0:
        s.line(24,204,231,204);s.line(43,205,43,230);s.line(214,205,214,230);s.rect(34,67,105,81,BLUE,8);s.line(86,149,86,177);s.line(59,178,115,178);s.card(45,81,82,44,WHITE,2);s.mic(166,102,24,45);s.package(153,160,62,43);s.spark(203,56)
    elif i==1:
        s.line(39,43,39,223);s.line(39,44,193,44);s.line(193,44,193,76);s.phone(169,76,48,82);s.line(20,225,62,225);s.rect(75,175,154,46,CREAM,6);s.bottle(101,152,31,59);s.card(148,179,62,32,LILAC,1);s.arrow(192,162,192,173)
    elif i==2:
        s.path('M 25 124 L 51 63 H 208 L 231 124 V 219 H 25 Z',BLUE);s.rect(62,78,65,36,WHITE,4,'accent');s.rect(143,78,49,36,LILAC,4,'accent')
        for j,c in enumerate([MINT,LILAC,CREAM]):s.circle(61+j*40,149,12,c,'accent');s.rect(42+j*43,181,31,18,c,4,'details')
        s.rect(181,139,23,60,WHITE,4,'accent');s.line(192,148,192,190);s.circle(192,171,5,MINT,'details')
    elif i==3:
        for x,c in [(49,BLUE),(207,LILAC)]:s.rect(x-28,41,56,66,c,7);s.line(x,108,x,205);s.line(x,205,x-23,228);s.line(x,205,x+23,228);s.line(x-14,69,x+14,69)
        s.path('M 77 59 L 125 117 L 100 147 Z',CREAM,'accent');s.path('M 179 59 L 134 117 L 155 147 Z',CREAM,'accent');s.bottle(108,126,41,87);s.line(94,218,162,218)
    elif i==4:
        s.mic(28,45,32,57);s.rect(109,71,113,99,BLUE,9);s.rect(122,85,86,38,WHITE,5,'accent');s.path('M 129 106 L 139 99 L 148 110 L 159 97 L 168 111 L 180 99 L 197 105','none','details');s.circle(136,146,8,MINT,'accent');s.circle(169,146,8,LILAC,'accent');s.circle(202,146,8,CREAM,'accent');s.path('M 44 135 V 194 Q 44 216 86 216 H 188 Q 208 216 208 184','none','accent')
    elif i==5:
        s.camera(47,155,79,51);s.poly([(45,146),(56,65),(192,65),(210,146)],BLUE);s.rect(66,77,117,49,WHITE,5,'accent');s.line(80,91,170,91);s.line(80,106,151,106);s.line(139,147,139,206);s.line(111,229,167,229);s.line(139,206,139,227);s.arrow(216,56,216,111)
    elif i==6:
        s.ellipse(128,188,98,31,BLUE);s.rect(30,187,196,32,BLUE,2);s.ellipse(128,186,98,31,CREAM,'accent');s.bottle(107,71,43,110);s.path('M 70 74 Q 126 28 187 69','none','accent');s.arrow(179,60,187,69);s.circle(128,199,5,LILAC,'details');s.line(72,217,72,228);s.line(188,217,188,228)
    elif i==7:
        s.rect(27,28,201,196,BLUE,12)
        for j,c in enumerate([CREAM,MINT,LILAC,WHITE]):
            x=41+j%2*89;y=47+j//2*78;s.rect(x,y,74,61,c,5,'accent');s.circle(x+37,y+23,12,WHITE,'details');s.line(x+11,y+47,x+61,y+47)
        s.line(43,210,191,210);s.cursor(190,181,24)
    elif i==8:
        s.rect(27,121,202,105,CREAM,8);s.bottle(49,140,34,68);s.card(103,148,55,57,BLUE,2);s.package(177,147,34,53);s.camera(81,29,94,53);s.line(128,82,128,103);s.arrow(128,102,128,117);s.path('M 38 128 L 47 137 M 217 128 L 208 137 M 38 219 L 47 210 M 217 219 L 208 210','none','accent')
    elif i==9:
        s.rect(28,40,129,91,BLUE,8);s.card(40,54,57,57,WHITE,2);s.bottle(109,63,24,43);s.line(91,132,91,158);s.line(61,159,122,159);s.rect(173,84,53,42,LILAC,6);s.line(200,126,200,155);s.line(183,155,218,155);s.rect(47,180,165,39,MINT,6);s.line(62,194,196,194);s.line(78,206,187,206)
    elif i==10:
        s.rect(31,32,194,148,MINT,5);s.rect(44,45,168,117,CREAM,4,'accent');s.line(48,180,39,227);s.line(207,180,219,227);s.package(101,110,57,52);s.camera(103,191,53,34);s.line(128,225,128,236);s.path('M 59 66 H 77 M 59 66 V 84 M 197 66 H 179 M 197 66 V 84','none','details')
    elif i==11:
        s.camera(23,39,64,43);s.camera(168,40,64,43);s.camera(28,162,61,43);s.rect(105,106,82,61,MINT,9);s.rect(119,122,54,28,WHITE,4,'accent');s.line(58,87,116,111);s.line(198,88,174,112);s.line(92,177,107,156);s.arrow(188,145,228,145);s.line(132,167,132,217);s.rect(106,217,54,16,LILAC,4,'accent')
    elif i==12:
        s.rect(28,46,114,97,BLUE,8);s.poly([(28,46),(136,27),(142,49),(33,69)],LILAC,'accent');s.line(53,43,69,61);s.line(88,37,105,55);s.line(39,92,125,92);s.line(39,113,104,113);s.package(139,123,88,88);s.bottle(166,81,36,65);s.line(151,211,151,229);s.line(215,211,215,229)
    elif i==13:
        s.rect(30,123,194,100,CREAM,8);s.bottle(91,93,48,111);s.circle(188,80,40,BLUE,'accent');s.circle(188,80,28,WHITE,'details');s.bottle(178,61,18,39);s.line(155,107,139,126,'accent');s.path('M 47 193 L 47 162 Q 55 149 63 163 L 67 178 L 78 166 Q 88 166 87 178 L 78 203 Z',MINT,'accent');s.spark(49,53)
    elif i==14:
        s.circle(128,132,89,'none','main');s.card(38,27,66,69,BLUE,2);s.card(153,37,68,70,MINT,2);s.card(75,157,108,68,LILAC,3);s.circle(128,132,19,CREAM,'accent');s.line(108,103,119,117);s.line(151,100,138,116);s.line(128,151,128,156);s.line(128,108,128,113)
    elif i==15:
        s.rect(27,39,202,184,BLUE,12);s.rect(42,54,91,151,CREAM,6,'accent');s.rect(147,54,65,68,MINT,6,'accent');s.rect(147,139,65,66,LILAC,6,'accent');s.path('M 62 74 Q 113 71 109 97 Q 111 119 65 121 Q 50 122 59 143 Q 70 167 114 162','none','details');s.rect(72,176,22,18,WHITE,4,'details');s.circle(180,87,16,WHITE,'details');s.line(167,167,191,167);s.line(167,178,192,178)
    elif i==16:
        s.rect(25,29,115,187,BLUE,8)
        for j in range(6):s.line(42+j*16,44,42+j*16,202)
        s.mic(175,70,33,69);s.path('M 154 57 Q 141 96 155 132 M 227 57 Q 239 96 227 132','none','accent');s.line(158,230,223,230)
    elif i==17:
        s.rect(24,192,208,28,CREAM,7);s.phone(29,49,60,113);s.line(57,163,57,192);s.line(40,190,78,190);s.mic(175,69,27,49);s.bottle(108,113,42,78);s.card(104,28,100,36,LILAC,1);s.line(92,221,92,235);s.line(175,221,175,235)
    elif i==18:
        s.path('M 29 130 L 129 91 L 228 130 V 220 H 29 Z',CREAM);s.path('M 129 133 V 220 M 29 130 L 129 164 L 228 130','none','details');s.poly([(29,130),(17,103),(116,65),(129,92)],BLUE,'accent');s.poly([(129,91),(145,64),(237,105),(228,130)],MINT,'accent');s.camera(87,28,84,52);s.arrow(129,85,129,119);s.bottle(104,143,39,57)
    elif i==19:
        s.phone(87,28,85,190);s.bottle(114,80,34,73);s.bubble(20,51,62,42,LILAC,1);s.bubble(174,89,59,46,MINT,1);s.heart(44,166,18,CREAM);s.star(205,169,16);s.rect(103,187,52,17,BLUE,4,'details');s.path('M 43 115 Q 59 115 70 103 M 198 143 V 146','none','accent')
    elif i==20:
        s.ellipse(129,195,102,26,BLUE);s.path('M 35 195 V 62 Q 130 23 221 62 V 195','none','accent');s.line(35,62,80,80);s.line(221,62,177,80);s.rect(79,66,99,25,LILAC,5);s.line(128,91,128,109);s.bottle(108,110,42,77);s.arrow(59,216,89,216);s.arrow(199,216,170,216)
    elif i==21:
        s.circle(81,116,52,BLUE);s.circle(81,116,34,LILAC,'accent');s.circle(81,116,19,WHITE,'details');s.rect(144,46,84,169,CREAM,8)
        for j,c in enumerate([BLUE,MINT,LILAC,WHITE]):s.rect(159,62+j*35,54,24,c,3,'accent')
        s.line(37,176,119,176);s.line(50,192,106,192)
    elif i==22:
        s.rect(27,34,200,186,BLUE,11)
        for j,c in enumerate([CREAM,MINT,LILAC]):s.circle(52,71+j*57,12,c,'accent');s.rect(77,51+j*57,128,37,WHITE,5,'accent');s.line(90,70+j*57,189,70+j*57)
        s.line(53,84,53,114);s.line(53,141,53,170);s.cursor(195,181,25)
    elif i==23:
        s.path('M 28 61 L 74 30 H 182 L 228 61 V 224 H 28 Z',BLUE);s.path('M 28 61 H 228 M 74 30 L 73 195 M 182 30 L 183 195 M 28 224 L 73 195 H 183 L 228 224','none','details');s.poly([(37,76),(64,90),(64,177),(37,201)],CREAM,'accent');s.poly([(219,76),(192,90),(192,177),(219,201)],CREAM,'accent');s.bottle(110,90,37,106);s.line(106,207,152,207)
    else:
        s.rect(26,32,204,137,BLUE,10);s.poly([(113,69),(113,123),(160,96)],MINT,'accent');s.rect(44,140,169,17,WHITE,4,'accent');s.line(59,148,198,148);s.card(50,192,152,34,CREAM,1);s.arrow(128,175,128,188);s.line(40,183,68,183);s.line(187,183,215,183)
    return s

def launch(i):
    s=Scene()
    if i==0:
        s.ellipse(128,206,94,21,BLUE);s.package(85,125,89,76);s.path('M 52 48 Q 125 28 201 53 L 179 139 Q 154 106 129 142 Q 110 108 77 142 Z',LILAC,'accent');s.line(50,53,35,103);s.line(203,53,219,103);s.star(45,158,13);s.spark(212,167)
    elif i==1:
        s.path('M 89 224 L 68 116 L 126 93 L 165 201 Z',BLUE);s.ellipse(97,113,33,13,LILAC,'accent');s.path('M 119 224 L 140 115 L 193 137 L 167 230 Z',MINT);s.ellipse(167,124,29,12,CREAM,'accent')
        for x,y,a in [(39,42,0),(101,39,1),(177,39,0),(216,75,1),(49,92,1),(207,186,0)]:s.rect(x,y,12,17,[CREAM,LILAC][a],3,'accent')
        s.star(135,66,15);s.path('M 52 180 Q 29 170 31 149 M 208 111 Q 224 99 220 87','none','details')
    elif i==2:
        s.path('M 30 222 V 112 Q 30 29 128 29 Q 227 29 227 112 V 222 H 204 V 112 Q 204 53 128 53 Q 53 53 53 112 V 222 Z',BLUE);s.ellipse(129,217,79,16,CREAM,'accent');s.package(94,137,70,67);s.line(34,90,56,83);s.line(200,83,224,90);s.star(128,79,13)
    elif i==3:
        s.line(24,33,233,33);s.path('M 31 37 H 113 Q 99 88 69 118 Q 61 176 42 222 H 27 Z',LILAC);s.path('M 142 37 H 226 L 230 222 H 211 Q 190 176 188 118 Q 158 92 142 37 Z',BLUE);s.ellipse(128,215,74,17,CREAM,'accent');s.bottle(108,111,43,93);s.line(43,144,64,144);s.line(193,144,214,144)
    elif i==4:
        s.rect(29,33,134,166,BLUE,9);s.rect(29,33,134,36,LILAC,9,'accent');s.line(57,25,57,47);s.line(135,25,135,47)
        for r in range(3):
            for c in range(3):s.rect(47+c*34,88+r*28,19,17,CREAM,3,'details')
        s.package(144,142,85,74);s.rect(137,127,95,20,MINT,4,'accent');s.line(186,130,186,216);s.star(203,78,17)
    elif i==5:
        s.package(36,102,185,120,CREAM);s.rect(28,81,200,29,BLUE,5,'accent');s.rect(111,105,35,115,LILAC,3,'accent');s.path('M 123 82 Q 44 29 63 22 Q 100 21 127 76 Q 151 26 189 24 Q 212 32 138 81',MINT,'accent');s.line(51,144,89,144);s.line(166,171,206,171)
    elif i==6:
        s.path('M 53 115 H 203 L 183 220 H 72 Z',BLUE);s.rect(43,96,170,26,LILAC,5,'accent');s.mic(98,31,24,41);s.card(151,39,67,42,CREAM,2);s.line(96,222,160,222);s.circle(128,157,24,MINT,'accent');s.star(128,157,11,WHITE,'details')
    elif i==7:
        s.path('M 99 141 L 99 73 Q 128 22 159 73 V 141 Z',BLUE);s.path('M 100 124 L 71 144 V 175 L 104 159 M 158 124 L 185 144 V 175 L 154 159',LILAC,'accent');s.circle(129,83,17,WHITE,'details');s.poly([(109,166),(128,219),(149,166)],CREAM,'accent');s.line(37,228,220,228);s.line(50,201,50,216);s.line(207,191,207,216);s.star(49,76,13)
    elif i==8:
        s.package(95,92,68,65);s.path('M 27 101 L 47 101 L 65 121 L 83 121 Q 100 124 94 135 L 73 139 L 57 132 L 36 144 Z',BLUE);s.path('M 230 101 L 209 101 L 191 121 L 173 121 Q 156 124 162 135 L 183 139 L 201 132 L 220 145 Z',MINT,'accent');s.path('M 96 229 V 207 L 113 191 V 173 Q 115 157 128 165 L 132 185 L 125 205 L 136 221 Z',LILAC,'accent');s.path('M 105 28 H 127 L 148 46 V 74 Q 142 86 130 72 L 127 58 L 110 54 Z',CREAM,'accent')
    elif i==9:
        s.circle(128,126,33,CREAM);s.package(108,110,41,32)
        for j,c in enumerate([BLUE,MINT,LILAC,BLUE,MINT,LILAC]):
            a=j*math.tau/6;x=128+65*math.sin(a);y=126-65*math.cos(a);s.ellipse(x,y,25,31,c,'accent');s.line(128+35*math.sin(a),126-35*math.cos(a),x,y)
        s.line(127,197,127,229);s.path('M 127 218 Q 88 186 83 221 Z',MINT,'details')
    elif i==10:
        s.path('M 23 105 H 51 L 68 192 H 202 L 221 124 H 57',BLUE);s.circle(86,217,14,CREAM,'accent');s.circle(181,217,14,CREAM,'accent');s.package(77,63,59,74);s.bottle(157,51,35,85);s.poly([(39,39),(104,39),(84,57),(104,75),(39,75)],LILAC,'accent');s.line(39,39,39,106);s.spark(216,55)
    elif i==11:
        s.path('M 28 218 C 105 196 48 133 128 130 C 205 126 149 63 224 40','none','accent')
        for x,y,c in [(46,205,BLUE),(92,149,MINT),(166,101,LILAC),(211,53,CREAM)]:s.circle(x,y,17,c,'accent');s.circle(x,y,5,WHITE,'details')
        s.package(171,161,54,53);s.card(30,32,79,51,BLUE,2)
    elif i==12:
        s.poly([(53,29),(199,29),(165,178),(95,178)],CREAM);s.rect(26,193,205,32,BLUE,6);s.bottle(109,112,39,80);s.circle(54,49,21,LILAC,'accent');s.circle(201,49,21,MINT,'accent');s.path('M 67 61 L 92 99 M 187 61 L 164 101','none','details');s.spark(202,154)
    elif i==13:
        s.rect(82,69,92,29,BLUE,9);s.circle(48,59,26,LILAC,'accent');s.circle(207,59,26,MINT,'accent');s.line(61,69,83,78);s.line(174,78,196,69);s.line(115,98,115,127);s.line(144,98,144,127);s.rect(75,130,110,39,CREAM,6,'accent');s.line(90,149,169,149);s.package(100,188,57,41);s.arrow(42,128,42,173);s.arrow(213,128,213,173)
    elif i==14:
        s.card(61,86,133,116,BLUE,2)
        for cx,cy,c in [(54,56,CREAM),(204,61,LILAC),(49,171,MINT),(213,170,CREAM)]:
            s.circle(cx,cy,5,c,'accent')
            for j in range(7):
                a=j*math.tau/7;s.line(cx+12*math.sin(a),cy+12*math.cos(a),cx+23*math.sin(a),cy+23*math.cos(a),'accent')
        s.line(88,215,170,215)
    elif i==15:
        s.star(129,119,76,BLUE);s.path('M 129 43 L 129 119 L 172 180 M 58 97 L 129 119 L 198 97 M 85 180 L 129 119','none','details');s.poly([(24,202),(50,177),(74,227)],LILAC,'accent');s.poly([(197,210),(229,184),(224,230)],MINT,'accent');s.spark(36,47);s.spark(217,47)
    elif i==16:
        s.rect(43,181,171,42,BLUE,8);s.rect(59,166,139,20,LILAC,5,'accent');s.package(99,105,60,61);s.ellipse(44,63,22,30,MINT,'accent');s.ellipse(210,65,22,30,CREAM,'accent');s.path('M 44 94 Q 72 129 55 159 M 210 96 Q 186 127 202 159','none','details');s.line(65,224,65,234);s.line(192,224,192,234);s.star(128,43,16)
    elif i==17:
        s.path('M 24 55 Q 127 85 232 54','none','details')
        for x,y,c in [(37,59,BLUE),(81,69,LILAC),(126,76,MINT),(169,69,CREAM),(213,59,BLUE)]:s.poly([(x-13,y),(x+13,y),(x,y+32)],c,'accent')
        s.package(65,145,130,80);s.rect(59,125,141,26,LILAC,4,'accent');s.line(128,127,128,225);s.spark(38,156);s.spark(221,177)
    elif i==18:
        s.rect(34,71,22,151,BLUE,4);s.rect(200,71,22,151,BLUE,4);s.rect(24,38,208,41,CREAM,7,'accent');s.path('M 56 121 Q 128 158 199 121','none','accent');s.package(99,156,58,54);s.line(73,229,182,229);s.arrow(128,89,128,111);s.poly([(38,39),(63,39),(63,77),(38,77)],LILAC,'details');s.poly([(188,39),(214,39),(214,77),(188,77)],MINT,'details')
    elif i==19:
        s.path('M 28 49 L 92 30 L 163 49 L 229 31 V 209 L 163 227 L 92 208 L 28 226 Z',CREAM);s.line(92,30,92,208);s.line(163,49,163,227);s.path('M 49 173 Q 98 192 115 126 Q 157 98 208 71','none','accent')
        for x,y,c in [(55,147,BLUE),(114,103,MINT),(171,132,LILAC),(208,58,BLUE)]:s.path(f'M {x} {y+34} Q {x-23} {y+9} {x-15} {y-8} Q {x} {y-28} {x+15} {y-8} Q {x+23} {y+9} {x} {y+34} Z',c,'accent');s.circle(x,y,5,WHITE,'details')
    elif i==20:
        s.path('M 27 163 C 96 117 135 204 228 160 L 227 191 C 135 232 97 144 29 193 Z',BLUE);s.path('M 27 69 C 93 29 150 113 230 66 L 228 96 C 145 139 92 60 29 99 Z',LILAC,'accent');s.package(92,102,75,61);s.line(128,112,128,161);s.star(47,128,14);s.spark(212,126)
    elif i==21:
        s.path('M 27 183 L 128 150 L 229 183 V 226 L 128 205 L 27 226 Z',CREAM);s.line(128,150,128,205);s.card(50,87,65,81,BLUE,2);s.card(146,77,61,90,LILAC,2);s.package(101,41,54,63);s.line(76,173,90,157);s.line(189,173,175,153);s.spark(43,46);s.spark(220,42)
    elif i==22:
        s.path('M 26 156 H 231 L 216 222 H 42 Z',BLUE);s.person(55,42,12,MINT);s.person(126,31,13,LILAC);s.person(203,43,12,CREAM);s.package(41,99,52,66);s.bottle(111,86,34,77);s.card(171,99,42,67,LILAC,2);s.line(39,184,218,184);s.line(82,186,82,213);s.line(163,186,163,213)
    elif i==23:
        s.rect(60,61,135,134,BLUE,10);s.rect(72,73,111,111,WHITE,6,'accent');s.bottle(108,95,37,75)
        for x1,y1,x2,y2,c in [(36,38,49,53,BLUE),(128,23,128,46,MINT),(219,36,202,54,LILAC),(226,131,207,131,BLUE),(217,219,203,200,MINT),(128,231,128,207,LILAC),(30,217,47,201,BLUE),(23,129,46,129,CREAM)]:s.line(x1,y1,x2,y2,'accent',color=INK,width=4);s.circle(x1,y1,4,c,'accent')
    else:
        s.path('M 25 41 Q 128 83 230 41','none','details')
        for j,(x,y,c) in enumerate([(44,70,BLUE),(99,84,LILAC),(155,85,MINT),(211,69,CREAM)]):
            s.line(x,y-17,x,y-5);s.rect(x-17,y,34,54,c,10,'accent');s.line(x-17,y+14,x+17,y+14);s.line(x-17,y+39,x+17,y+39);s.line(x,y+55,x,y+71)
        s.package(86,171,86,55);s.ellipse(129,228,70,7,BLUE,'accent');s.star(31,176,12);s.spark(221,180)
    return s

CATEGORIES=[('Offer and value assemblies',OFFER_TITLES,offer,'value'),('Audience engagement props',AUDIENCE_TITLES,audience,'engagement'),('Live-commerce production elements',PRODUCTION_TITLES,production,'production'),('Launch and celebration kits',LAUNCH_TITLES,launch,'launch')]
MOTIONS=[('stagger components into place','gentle floating depth offsets','separate components into a neat stack'),('reveal dialogue and participant layers in sequence','soft response pulses without changing counts','fold conversation into one departing panel'),('assemble equipment with short linked connector draws','subtle recording pulse or slow product tilt','withdraw equipment and retract connectors'),('unfold showcase first then reveal accents','slow decorative drift and restrained celebratory sparkle','close showcase and let decorations settle')]

def generate(output,index):
    output.mkdir(parents=True,exist_ok=True);rows=[]
    for g,(category,titles,draw,tag) in enumerate(CATEGORIES):
        assert len(titles)==25
        for i,title in enumerate(titles):
            pid=f'SV{1401+g*25+i}';svg=draw(i).svg(title);(output/(pid+'.svg')).write_text(svg)
            en,am,ex=MOTIONS[g]
            rows.append({'id':pid,'title':title,'category':category,'tags':['promotion',tag,'original assembly','pastel','transparent'],'svg':f'svg/files/{pid}.svg','viewBox':'0 0 256 256','license':'Original artwork. User may use and modify commercially. No third-party assets.','layers':['main','accent','details'],'collection':'promotion','use_cases':['motion graphic promotions','product explainers','educational presentations'] if g!=1 else ['audience participation','educational explainers','discussion overlays'],'suggested_motion':{'entrance':en,'ambient':am,'exit':ex}})
    assert len(rows)==100;index.write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n');return rows

if __name__=='__main__':
    root=Path(__file__).resolve().parent;ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,default=root/'files');ap.add_argument('--index',type=Path,default=root/'svg_promo_commerce_index.json');args=ap.parse_args();r=generate(args.output,args.index);print(f'Generated {len(r)} original SVG assemblies SV1401–SV1500')
