#!/usr/bin/env python3
"""Reproduce 100 original layered concept SVGs SV1201–SV1300.
No downloaded artwork, scripts, image embeds, external references or animations.
Motion metadata proposes animation recipes; assets themselves are static SVG.
"""
from pathlib import Path
import json, math, html
ROOT=Path(__file__).resolve().parent
BLUE='#BFE3F3';MINT='#C9EADF';LILAC='#DDD0F4';CREAM='#FFF0D0';WHITE='#FFFDF7';INK='#526D84';PINK='#DDD0F4'
PALETTE=[BLUE,MINT,LILAC,CREAM,PINK]

class Drawing:
 def __init__(self):self.groups={'main':[],'accent':[],'details':[]}
 def add(self,s,g='main'):self.groups[g].append(s)
 def rect(self,x,y,w,h,c=WHITE,r=8,g='main',stroke=INK):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}" stroke="{stroke}" stroke-width="4"/>',g)
 def circle(self,x,y,r,c=WHITE,g='main',stroke=INK):self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{stroke}" stroke-width="4"/>',g)
 def ellipse(self,x,y,rx,ry,c=WHITE,g='main'):self.add(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" stroke="{INK}" stroke-width="4"/>',g)
 def line(self,points,c=INK,g='details',w=4):self.add('<polyline points="'+ ' '.join(f'{x},{y}' for x,y in points)+f'" fill="none" stroke="{c}" stroke-width="{max(3,min(5,w))}" stroke-linecap="round" stroke-linejoin="round"/>',g)
 def poly(self,points,c=BLUE,g='main'):self.add('<polygon points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="{c}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>',g)
 def path(self,path,c='none',g='details',stroke=INK):self.add(f'<path d="{path}" fill="{c}" stroke="{stroke}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',g)
 def arrow(self,a,b,c=INK,g='accent'):
  self.line([a,b],c,g);dx=b[0]-a[0];dy=b[1]-a[1];ang=math.atan2(dy,dx);l=9
  self.line([(b[0]-l*math.cos(ang-.55),b[1]-l*math.sin(ang-.55)),b,(b[0]-l*math.cos(ang+.55),b[1]-l*math.sin(ang+.55))],c,g)
 def check(self,x,y,r=17):self.circle(x,y,r,MINT,'accent');self.line([(x-r*.5,y),(x-r*.12,y+r*.35),(x+r*.5,y-r*.35)])
 def cross(self,x,y,r=15):self.circle(x,y,r,PINK,'accent');self.line([(x-5,y-5),(x+5,y+5)]);self.line([(x+5,y-5),(x-5,y+5)])
 def spark(self,x,y,s=10):self.line([(x-s,y),(x+s,y)],INK,'accent');self.line([(x,y-s),(x,y+s)],INK,'accent')
 def badge(self,x,y,r=15,c=LILAC):self.circle(x,y,r,c,'accent');self.circle(x,y,r*.33,WHITE,'details')
 def screen(self,x,y,w=110,h=76,c=BLUE):
  self.rect(x,y,w,h,c,10);self.rect(x+7,y+8,w-14,h-22,WHITE,5);self.line([(x+w*.4,y+h),(x+w*.4,y+h+15),(x+w*.6,y+h+15),(x+w*.6,y+h)]);self.line([(x+w*.25,y+h+15),(x+w*.75,y+h+15)])
 def laptop(self,x,y,w=125,h=82):self.rect(x,y,w,h,BLUE,8);self.rect(x+8,y+8,w-16,h-17,WHITE,4);self.poly([(x-10,y+h),(x+w+10,y+h),(x+w+3,y+h+13),(x-3,y+h+13)],LILAC);self.line([(x+w*.4,y+h+4),(x+w*.6,y+h+4)])
 def doc(self,x,y,w=58,h=76,c=CREAM):
  fold=min(15,w*.25,h*.24);self.path(f'M{x},{y} H{x+w-fold} L{x+w},{y+fold} V{y+h} H{x} Z',c,'main');self.path(f'M{x+w-fold},{y} V{y+fold} H{x+w}',WHITE,'details');self.line([(x+10,y+h*.4),(x+w-10,y+h*.4)]);self.line([(x+10,y+h*.6),(x+w-10,y+h*.6)]);self.line([(x+10,y+h*.8),(x+w-21,y+h*.8)])
 def book(self,x,y,w=65,h=85,c=LILAC):self.rect(x,y,w,h,c,4);self.line([(x+11,y+3),(x+11,y+h-3)]);self.line([(x+23,y+24),(x+w-11,y+24)]);self.line([(x+23,y+37),(x+w-17,y+37)])
 def person(self,x,y,s=1,c=MINT):self.circle(x,y-18*s,11*s,CREAM);self.path(f'M{x-20*s},{y+22*s} Q{x-20*s},{y-2*s} {x},{y-2*s} Q{x+20*s},{y-2*s} {x+20*s},{y+22*s} Z',c,'main')
 def bulb(self,x,y,r=22):self.circle(x,y,r,CREAM,'accent');self.rect(x-10,y+r-4,20,18,LILAC,4);self.line([(x-6,y-4),(x,y+7),(x+6,y-4)]);self.line([(x,y+7),(x,y+r-4)])
 def clock(self,x,y,r=28):self.circle(x,y,r,WHITE);self.circle(x,y,3,LILAC,'accent');self.line([(x,y-r*.6),(x,y),(x+r*.4,y+r*.2)]);self.line([(x-5,y-r),(x+5,y-r)])
 def calendar(self,x,y,w=92,h=86):
  self.rect(x,y,w,h,WHITE);self.rect(x,y,w,23,BLUE,7,'accent');self.line([(x+19,y-6),(x+19,y+11)]);self.line([(x+w-19,y-6),(x+w-19,y+11)])
  for i in range(6):self.rect(x+12+(i%3)*23,y+36+(i//3)*23,12,12,CREAM,3,'details')
 def play(self,x,y,r=18):self.circle(x,y,r,LILAC,'accent');self.poly([(x-5,y-9),(x+9,y),(x-5,y+9)],WHITE,'details')
 def coins(self,x,y,n=3):
  for i in range(n):self.ellipse(x,y-i*8,22,8,CREAM,'main')
  self.line([(x,y-n*8+7),(x,y-5)])
 def gift(self,x,y,w=62,h=55):self.rect(x,y,w,h,CREAM);self.rect(x-4,y-8,w+8,16,MINT,4,'accent');self.line([(x+w/2,y-8),(x+w/2,y+h)],INK,'details',5);self.path(f'M{x+w/2},{y-8} C{x+w/2-36},{y-30} {x+w/2-21},{y-43} {x+w/2},{y-8} C{x+w/2+32},{y-39} {x+w/2+40},{y-20} {x+w/2},{y-8}',LILAC,'accent')
 def cloud(self,x,y,s=1):self.path(f'M{x-36*s},{y+15*s} C{x-59*s},{y+15*s} {x-52*s},{y-15*s} {x-32*s},{y-12*s} C{x-31*s},{y-42*s} {x+12*s},{y-45*s} {x+19*s},{y-16*s} C{x+54*s},{y-25*s} {x+58*s},{y+16*s} {x+31*s},{y+16*s} Z',BLUE,'main')
 def lock(self,x,y,s=1):self.path(f'M{x-15*s},{y-2*s} V{y-16*s} C{x-15*s},{y-37*s} {x+15*s},{y-37*s} {x+15*s},{y-16*s} V{y-2*s}');self.rect(x-22*s,y-2*s,44*s,37*s,LILAC,6,'accent');self.circle(x,y+13*s,4*s,WHITE,'details');self.line([(x,y+17*s),(x,y+25*s)])
 def tag(self,x,y,w=68,h=40):self.poly([(x,y),(x+w-14,y),(x+w,y+h/2),(x+w-14,y+h),(x,y+h)],CREAM);self.circle(x+12,y+h/2,4,WHITE,'details')
 def flag(self,x,y,h=65):
  side=-1 if x>185 else 1;self.line([(x,y),(x,y+h)]);self.path(f'M{x},{y} Q{x+side*22},{y-12} {x+side*43},{y+1} V{y+30} Q{x+side*20},{y+18} {x},{y+30} Z',MINT,'accent')
 def gear(self,x,y,r=29):
  pts=[]
  for i in range(24):a=i*math.pi/12;rr=r if i%3 else r+7;pts.append((x+rr*math.cos(a),y+rr*math.sin(a)))
  self.poly(pts,BLUE);self.circle(x,y,r*.4,WHITE,'details')
 def star(self,x,y,r=18):
  pts=[]
  for i in range(10):a=-math.pi/2+i*math.pi/5;rr=r if i%2==0 else r*.43;pts.append((x+rr*math.cos(a),y+rr*math.sin(a)))
  self.poly(pts,CREAM,'accent')
 def ticket(self,x,y,w=93,h=54):self.rect(x,y,w,h,LILAC,10);self.line([(x+w*.7,y+5),(x+w*.7,y+h-5)],INK,'details',3);self.circle(x+27,y+h/2,12,CREAM,'accent');self.line([(x+w*.78,y+18),(x+w*.9,y+18)]);self.line([(x+w*.78,y+31),(x+w*.9,y+31)])
 def leaf(self,x,y,s=1,flip=False):self.path(f'M{x},{y} Q{x-25*s},{y-35*s} {x+18*s},{y-45*s} Q{x+26*s},{y-6*s} {x},{y} Z',MINT,'accent');self.line([(x,y),(x+12*s,y-31*s)])
 def route(self,pts):self.line(pts,INK,'main',5);[self.circle(x,y,6,MINT,'accent') for x,y in [pts[0],pts[-1]]]
 def waves(self,x,y,w=140):
  for j in range(3):self.path(f'M{x},{y+j*12} Q{x+w*.25},{y-8+j*12} {x+w*.5},{y+j*12} T{x+w},{y+j*12}',g='details')
 def render(self,pid,title):
  groups=''.join(f'<g id="{g}">'+''.join(self.groups[g])+'</g>' for g in ['main','accent','details'])
  return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title"><title id="title">{html.escape(title)}</title>{groups}</svg>\n'

TITLES=[
 'Balanced paths and two outcomes','Forked road with checkpoint choice','Cost benefit slider comparison','Bridge across a decision gap','Compass surrounded by alternatives','Strategic move on a choice board','Two option voting assembly','Matching key and different locks','Selected card from a decision stack','Three input tradeoff controls','Staircase versus direct elevator','Two funnels and one decision gate','Knowledge versus insight balance','Resource budget allocation buckets','Time and money seesaw','Detour around a blocked path','Three doors branching choice','Pros and cons under a focus lens','Overlapping decision criteria','Risk protection and opportunity','Feasibility pivot and constraint','Resource share comparison wheel','Reversible decision checkpoint','Preference spectrum control panel','Contingency tree with fallback',
 'Triggering domino consequence chain','Gear impulse to output arrow','Chain pull raising an outcome flag','Ripple source and listening receiver','Seed investment growing into result','Thermostat feedback control loop','Small trigger large butterfly effect','Switch circuit lighting a bulb','Two causes mixing into one result','Pressure gauge and stress release','Root causes beneath a focus lens','Visible outcome and hidden iceberg','Pulley effort lifting a load','Queued pipeline bottleneck','Friction slowing an inflating balloon','Wind drive turning energy wheel','Lever and fulcrum producing lift','Magnet drawing separate inputs','Filter funnel separating causes','Resonant waves and linked receivers','Delayed feedback with timer','Preventive stop in domino cascade','Reservoir overflow effect','Signal pulse reaching three outputs','Cascading cards revealing results',
 'Course launch learning screen kit','Digital book bundle and access tag','Tutorial play card and three steps','Certification course completion kit','Membership lessons behind access gate','Prompt kit linked idea cards','Presentation template fan and sample','Webinar learning screen and notes','Digital download package delivery','Syllabus learning path kit','Revision flashcard pack and progress','Quiz lesson correct answer journey','Coaching session and shared workbook','Creator studio course workflow','Productivity course dashboard kit','Coding course laptop and logic blocks','Audio lesson deck and headphones','Language lesson chat pair','Design asset pack and palette layers','Study notes highlighter kit','Product demo preview and detail cards','Skill progression before after kit','Bonus gift with digital course','Lifetime access learning library','Checkout license and access journey',
 'Clinic appointment service kit','Practical workshop table and seats','Community event stage and ticket','Product launch podium celebration','Consulting service roadmap kit','Booking calendar time confirmation','Travel event itinerary and suitcase','Online consultation screen pair','Home service van and tools','Wedding invitation foliage and rings','Conference schedule and podium','Training registration and seats','Exhibition booth and visitor badge','Webinar questions and audience','Festival stage musical event kit','Service offer megaphone coupon','Catering buffet service kit','Help desk support service kit','Charity campaign donation box','Fitness challenge checkpoint bib','Professional networking circle','Delivery service truck and parcels','Open house doorway and location','Photography service camera frame','Awareness campaign boards and people'
]
CATS=['Decision and tradeoff metaphors','Cause and effect assemblies','Course and digital-product promo kits','Service and event promo kits']

# Explicitly authored arrangements; repeated primitives build different semantic relationships.
def draw_recipe(n):
 d=Drawing()
 if n==0:
  d.line([(128,57),(128,205),(92,218),(165,218)]);d.line([(51,88),(205,88)]);d.circle(128,88,8,LILAC,'accent');d.path('M51 88 L28 145 H75 Z',BLUE,'main');d.path('M205 88 L181 145 H229 Z',MINT,'main');d.doc(38,153,37,48);d.bulb(202,176,19)
 elif n==1:
  d.path('M112 224 V143 Q111 122 70 106 L40 51',BLUE,'main');d.path('M144 224 V145 Q143 124 184 106 L213 51',MINT,'main');d.line([(128,223),(128,153)]);d.arrow((88,118),(53,65));d.arrow((168,118),(204,65));d.check(54,39,18);d.cross(207,39,18);d.clock(48,185,24)
 elif n==2:
  d.rect(27,42,202,169,WHITE);d.coins(69,107,3);d.bulb(183,84,20);d.line([(54,154),(202,154)]);d.circle(105,154,14,LILAC,'accent');d.line([(49,184),(98,184)]);d.line([(157,184),(207,184)]);d.arrow((120,95),(145,95))
 elif n==3:
  d.poly([(21,177),(96,177),(96,223),(21,223)],BLUE);d.poly([(161,177),(235,177),(235,223),(161,223)],MINT);d.path('M96 177 Q128 126 161 177',CREAM,'accent');d.person(55,150,.9);d.flag(202,111,66);d.arrow((103,144),(150,144));d.line([(124,186),(124,214)]);d.line([(134,186),(134,214)])
 elif n==4:
  d.circle(128,127,66,WHITE);d.poly([(128,74),(141,126),(128,177),(115,126)],BLUE,'accent');d.circle(128,127,8,LILAC,'details');d.tag(20,29,54,30);d.doc(183,29,45,53);d.clock(52,203,22);d.check(201,202,23);d.line([(88,87),(68,66)]);d.line([(168,171),(185,186)])
 elif n==5:
  d.rect(28,36,158,158,WHITE,6)
  for x in [28,67,106,145]:
   for y in [36,75,114,153]:
    if ((x-28)//39+(y-36)//39)%2==0:d.rect(x,y,39,39,BLUE,0,'accent')
  d.path('M64 151 L82 113 L69 87 L82 66 L110 81 L107 100 L95 127 L105 152 Z',LILAC,'main');d.arrow((126,174),(206,215));d.flag(210,146,65)
 elif n==6:
  d.rect(25,49,89,139,BLUE);d.rect(142,49,89,139,LILAC);d.doc(42,66,49,64);d.doc(160,66,49,64);d.check(70,164,20);d.cross(185,164,20);d.person(128,217,.55);d.arrow((116,206),(82,190))
 elif n==7:
  d.lock(64,104,1);d.lock(195,101,1);d.circle(107,197,17,CREAM,'main');d.line([(124,197),(194,197)]);d.line([(175,197),(175,211)]);d.line([(187,197),(187,207)]);d.arrow((109,170),(72,143));d.cross(195,151,12);d.check(64,150,12)
 elif n==8:
  d.rect(50,33,155,142,BLUE);d.rect(38,48,155,142,LILAC);d.rect(26,65,155,142,WHITE);d.line([(49,91),(133,91)]);d.line([(49,109),(154,109)]);d.line([(49,127),(118,127)]);d.check(154,171,25);d.person(215,211,.7);d.arrow((208,173),(182,173))
 elif n==9:
  d.rect(30,36,194,186,WHITE)
  for i in range(3):x=65+i*64;d.line([(x,66),(x,165)]);d.circle(x,89+i*28,14,PALETTE[i],'accent');d.circle(x,192,8,CREAM,'details')
  d.line([(51,53),(204,53)]);d.line([(51,210),(204,210)])
 elif n==10:
  for i in range(4):d.rect(23+i*29,197-i*30,30,30,BLUE,3)
  d.rect(174,52,53,172,WHITE);d.rect(182,126,37,57,MINT,5,'accent');d.arrow((200,114),(200,71));d.person(78,71,.65);d.flag(117,42,57);d.line([(158,50),(158,223)])
 elif n==11:
  d.poly([(26,38),(113,38),(80,104),(59,104)],BLUE);d.poly([(143,38),(230,38),(197,104),(176,104)],LILAC);d.arrow((69,112),(102,151));d.arrow((187,112),(153,151));d.circle(128,171,29,MINT,'main');d.check(128,171,17);d.doc(104,209,48,25)
 elif n==12:
  d.line([(128,90),(128,212),(77,220),(179,220)]);d.line([(53,110),(203,110)]);d.path('M53 110 L26 165 H82 Z',MINT,'main');d.path('M203 110 L178 165 H230 Z',BLUE,'main');d.book(36,62,36,57);d.bulb(202,75,20);d.circle(128,110,9,LILAC,'accent')
 elif n==13:
  d.coins(53,65,3);d.arrow((87,59),(143,59));d.rect(167,34,49,61,LILAC);d.path('M27 136 H88 L80 221 H36 Z',BLUE,'main');d.path('M100 136 H160 L152 221 H108 Z',MINT,'main');d.path('M172 136 H231 L223 221 H181 Z',CREAM,'main');d.arrow((128,101),(128,128));d.line([(53,171),(66,171)]);d.line([(122,182),(139,182)]);d.line([(192,159),(211,159)])
 elif n==14:
  d.poly([(104,207),(127,173),(149,207)],LILAC);d.line([(31,140),(225,176)],INK,'main',7);d.clock(60,112,26);d.coins(196,145,3);d.arrow((57,169),(57,195));d.arrow((195,114),(195,86));d.circle(127,158,6,MINT,'accent')
 elif n==15:
  d.route([(28,212),(77,158),(126,158),(170,107),(222,107)]);d.rect(89,145,62,32,PINK,5);d.route([(76,158),(76,90),(126,65),(171,107)]);d.arrow((87,98),(112,78));d.flag(217,57,50);d.cross(120,161,11)
 elif n==16:
  d.route([(128,224),(128,159),(51,117),(51,68)]);d.route([(128,159),(202,117),(202,68)]);d.rect(28,26,47,51,BLUE);d.rect(177,26,47,51,MINT);d.rect(101,34,49,59,LILAC);d.arrow((128,151),(128,102));d.circle(60,55,3,CREAM,'details');d.circle(215,55,3,CREAM,'details');d.circle(136,67,3,CREAM,'details')
 elif n==17:
  d.doc(27,45,70,107);d.doc(159,45,70,107,LILAC);d.check(61,108,16);d.cross(191,107,16);d.circle(127,175,40,BLUE,'accent');d.line([(153,204),(182,233)],INK,'details',8);d.line([(108,172),(147,172)]);d.arrow((107,150),(144,150))
 elif n==18:
  d.circle(90,112,57,BLUE);d.circle(162,112,57,LILAC);d.path('M126 68 Q154 111 126 155 Q99 111 126 68 Z',MINT,'accent');d.check(126,112,17);d.doc(100,178,53,55,CREAM);d.arrow((126,161),(126,173))
 elif n==19:
  d.path('M22 99 Q80 22 137 99 Z',BLUE,'main');d.line([(80,99),(80,168)]);d.path('M80 168 Q80 189 100 178');d.star(200,81,22);d.person(163,191,.9);d.arrow((139,136),(194,113));d.circle(204,181,19,LILAC,'accent');d.line([(196,181),(212,181)])
 elif n==20:
  d.rect(29,38,103,145,WHITE);d.rect(146,65,80,117,LILAC);d.check(81,102,22);d.line([(47,147),(110,147)]);d.line([(158,110),(215,110)]);d.line([(158,132),(195,132)]);d.arrow((96,218),(171,218));d.line([(89,197),(89,231)]);d.line([(179,197),(179,231)])
 elif n==21:
  d.circle(89,117,57,BLUE);d.path('M89 117 L89 60 A57 57 0 0 1 146 117 Z',LILAC,'accent');d.line([(89,117),(139,145)]);d.rect(174,56,50,29,MINT);d.rect(174,108,50,29,CREAM);d.rect(174,160,50,29,LILAC);d.line([(32,206),(113,206)]);d.line([(32,225),(83,225)])
 elif n==22:
  d.rect(36,77,182,80,WHITE,40);d.circle(80,117,30,BLUE,'accent');d.arrow((95,53),(158,53));d.arrow((159,186),(96,186));d.check(190,211,18);d.flag(37,187,44);d.line([(139,104),(185,104)]);d.line([(139,127),(166,127)])
 elif n==23:
  d.rect(24,40,207,176,WHITE)
  for i in range(4):x=51+i*48;d.rect(x,64,19,81,PALETTE[i],6,'accent');d.circle(x+9,161+i%2*22,9,WHITE,'details')
  d.line([(47,196),(206,196)]);d.circle(149,196,10,LILAC,'accent')
 elif n==24:
  d.circle(128,45,24,CREAM);d.route([(128,69),(128,99),(61,99),(61,126)]);d.route([(128,99),(197,99),(197,126)]);d.rect(33,127,56,41,BLUE);d.rect(170,127,56,41,MINT);d.line([(61,168),(61,193),(113,193)]);d.line([(197,168),(197,193),(148,193)]);d.rect(102,180,49,51,LILAC);d.arrow((161,199),(151,199))
 elif n==25:
  d.rect(25,143,27,69,BLUE,4);d.poly([(76,122),(99,134),(64,204),(42,192)],MINT);d.poly([(119,93),(140,110),(86,176),(64,158)],LILAC);d.poly([(163,68),(184,86),(129,151),(108,132)],CREAM);d.flag(213,129,77);d.arrow((29,95),(58,119));d.spark(204,49,11)
 elif n==26:
  d.gear(70,138,35);d.gear(140,86,27);d.arrow((95,191),(188,191));d.rect(184,141,40,78,MINT);d.line([(195,162),(215,162)]);d.line([(195,181),(211,181)]);d.spark(40,62,11)
 elif n==27:
  d.circle(52,182,24,CREAM);d.line([(70,165),(122,107)],INK,'main',7)
  for i in range(3):d.ellipse(84+i*15,150-i*17,10,15,LILAC,'accent')
  d.line([(125,28),(125,222)]);d.flag(179,46,143);d.path('M125 109 Q171 109 179 81');d.arrow((178,177),(178,132));d.line([(111,222),(139,222)])
 elif n==28:
  d.circle(66,129,14,LILAC,'accent');d.circle(66,129,41,'none');d.path('M112 63 A74 74 0 0 1 112 195');d.path('M131 43 A98 98 0 0 1 131 215');d.screen(174,100,58,49,MINT);d.line([(190,122),(213,122)]);d.arrow((144,129),(164,129))
 elif n==29:
  d.coins(46,197,4);d.path('M109 211 Q127 160 128 116');d.leaf(126,149,.9);d.leaf(127,180,-.7);d.circle(142,80,24,CREAM,'accent');d.line([(113,223),(154,223)]);d.arrow((63,119),(111,119));d.rect(184,119,38,87,BLUE);d.rect(172,148,13,58,LILAC);d.star(200,80,16)
 elif n==30:
  d.rect(27,86,73,95,WHITE);d.circle(64,123,22,BLUE,'accent');d.line([(64,123),(78,111)]);d.line([(41,159),(85,159)]);d.bulb(193,122,24);d.arrow((108,125),(157,125));d.path('M195 174 V214 H61 V188');d.arrow((61,204),(61,188));d.clock(125,211,15)
 elif n==31:
  d.circle(38,159,10,CREAM,'accent');d.arrow((55,153),(101,121));d.path('M127 87 C67 33 48 103 108 126 C71 146 91 190 127 151 C168 193 193 144 145 126 C202 96 178 39 127 87 Z',LILAC,'main');d.line([(127,89),(127,161)]);d.arrow((160,174),(217,218));d.star(219,64,15);d.spark(48,46,9)
 elif n==32:
  d.rect(29,52,67,34,BLUE);d.circle(44,69,8,CREAM,'accent');d.line([(96,69),(160,69),(160,108)]);d.bulb(188,137,27);d.line([(188,182),(188,216),(45,216),(45,92)]);d.circle(109,216,7,MINT,'accent');d.arrow((114,68),(144,68));d.spark(221,105,8)
 elif n==33:
  d.doc(27,37,57,69,BLUE);d.doc(173,37,57,69,LILAC);d.arrow((65,117),(106,160));d.arrow((193,117),(151,160));d.path('M78 150 H177 L163 203 H92 Z',MINT,'main');d.circle(128,203,20,CREAM,'accent');d.line([(119,204),(137,204)]);d.line([(128,195),(128,213)])
 elif n==34:
  d.poly([(74,220),(127,113),(182,220)],LILAC);d.path('M96 115 Q126 87 152 115',CREAM,'accent');d.path('M89 54 Q103 83 104 99');d.path('M145 43 Q135 75 143 87');d.circle(58,115,31,WHITE);d.line([(58,115),(75,98)]);d.arrow((198,160),(221,124));d.spark(192,88,10)
 elif n==35:
  d.circle(128,61,32,BLUE,'accent');d.line([(150,84),(173,107)],INK,'details',7);d.path('M126 91 V128 M126 125 L70 176 M126 139 L163 188 M73 174 L36 202 M73 174 L75 225 M160 187 L190 220 M159 187 L216 187',g='main');d.circle(39,203,12,MINT,'accent');d.circle(75,225,9,LILAC,'accent');d.circle(192,219,12,CREAM,'accent');d.circle(216,187,9,BLUE,'accent')
 elif n==36:
  d.waves(20,101,213);d.poly([(90,102),(134,35),(167,104)],CREAM);d.poly([(90,115),(69,179),(103,224),(148,217),(190,174),(167,113)],BLUE);d.rect(73,144,32,28,LILAC);d.circle(144,180,20,MINT,'accent');d.line([(110,113),(116,213)]);d.flag(183,51,50)
 elif n==37:
  d.line([(52,35),(204,35)]);d.circle(129,68,24,BLUE);d.path('M76 186 V67 Q76 40 103 40 H129 Q153 40 153 69 V143');d.rect(54,181,45,45,LILAC);d.rect(132,142,46,45,MINT);d.arrow((195,86),(195,163));d.arrow((30,185),(30,116));d.line([(117,68),(141,68)])
 elif n==38:
  for i in range(3):d.rect(25,52+i*54,32,34,PALETTE[i],5)
  d.path('M62 70 H117 L136 121 L117 180 H62',BLUE,'main');d.path('M139 109 H180 V141 H139',CREAM,'main');d.arrow((185,125),(224,125));d.circle(213,195,22,MINT,'accent');d.check(213,195,13);d.line([(142,166),(142,215)]);d.line([(156,173),(166,190)])
 elif n==39:
  d.ellipse(101,79,45,54,LILAC);d.poly([(93,133),(108,133),(101,144)],LILAC,'accent');d.path('M101 144 Q146 177 90 220');d.rect(173,61,48,111,BLUE);d.line([(162,75),(140,83)]);d.line([(161,104),(142,103)]);d.line([(162,137),(145,125)]);d.arrow((44,176),(44,128))
 elif n==40:
  d.line([(126,137),(126,217)]);d.circle(126,111,12,CREAM,'accent');d.path('M126 111 Q65 55 76 39 Q140 45 126 111 Z',BLUE,'main');d.path('M126 111 Q183 53 208 75 Q187 142 126 111 Z',LILAC,'main');d.path('M126 111 Q177 176 159 193 Q92 178 126 111 Z',MINT,'main');d.path('M126 111 Q57 164 40 143 Q55 75 126 111 Z',CREAM,'main');d.arrow((181,213),(224,213));d.bulb(212,180,15)
 elif n==41:
  d.poly([(101,198),(124,161),(145,198)],LILAC);d.line([(40,160),(217,111)],INK,'main',7);d.rect(25,128,39,33,BLUE);d.rect(193,80,39,34,MINT);d.arrow((45,186),(45,218));d.arrow((212,72),(212,42));d.circle(124,137,7,CREAM,'accent')
 elif n==42:
  d.path('M72 70 V155 C72 208 176 208 176 155 V70 H148 V155 C148 174 100 174 100 155 V70 Z',BLUE,'main');d.rect(72,65,28,36,LILAC);d.rect(148,65,28,36,PINK);d.rect(34,27,19,21,MINT);d.rect(203,26,20,21,CREAM);d.arrow((46,57),(68,83));d.arrow((210,57),(181,83));d.spark(125,116,11)
 elif n==43:
  d.poly([(33,41),(220,41),(147,145),(147,202),(107,222),(107,145)],BLUE);d.circle(73,65,11,MINT,'accent');d.rect(107,67,21,20,LILAC,4,'accent');d.circle(171,64,10,CREAM,'accent');d.line([(83,111),(169,111)]);d.check(127,169,15);d.cross(203,203,18);d.arrow((161,147),(193,183))
 elif n==44:
  d.waves(24,45,206);d.circle(49,141,22,BLUE);d.circle(128,141,22,MINT);d.circle(207,141,22,LILAC);d.line([(72,141),(104,141)]);d.line([(151,141),(183,141)]);d.arrow((49,180),(49,218));d.arrow((128,180),(128,218));d.arrow((207,180),(207,218));d.circle(49,226,5,CREAM,'accent');d.circle(128,226,5,CREAM,'accent');d.circle(207,226,5,CREAM,'accent')
 elif n==45:
  d.screen(24,74,81,60);d.clock(181,89,32);d.arrow((109,97),(141,97));d.path('M184 126 V208 H67 V156');d.arrow((67,180),(67,156));d.coins(67,193,2);d.line([(42,96),(60,96),(67,108),(84,87)])
 elif n==46:
  d.rect(26,151,27,74,BLUE);d.poly([(64,157),(87,144),(122,207),(98,220)],LILAC);d.rect(135,121,18,107,MINT);d.rect(173,88,27,139,CREAM);d.arrow((45,90),(65,123));d.cross(144,86,23);d.line([(114,57),(166,57)]);d.spark(207,49,11)
 elif n==47:
  d.path('M25 62 H148 V182 Q86 226 25 182 Z',BLUE,'main');d.waves(31,115,111);d.line([(151,63),(151,218)],INK,'main',8);d.path('M153 139 Q200 134 229 200',g='accent');d.arrow((205,166),(229,201));d.rect(185,204,44,25,MINT);d.circle(217,188,7,CREAM,'accent')
 elif n==48:
  d.rect(24,104,55,53,BLUE);d.line([(79,129),(129,129),(129,56),(173,56)]);d.line([(129,129),(176,129)]);d.line([(129,129),(129,206),(173,206)]);d.circle(129,129,8,LILAC,'accent');d.bulb(207,56,18);d.check(207,129,18);d.flag(199,184,46);d.line([(37,136),(46,122),(55,136),(64,122)])
 elif n==49:
  d.doc(25,30,67,94,BLUE);d.doc(92,81,67,94,MINT);d.doc(162,129,67,94,LILAC);d.arrow((74,136),(93,164));d.arrow((149,186),(164,210));d.circle(66,73,13,CREAM,'accent');d.check(197,193,16);d.spark(183,50,9)
 elif n==50:
  d.screen(24,81,130,90);d.play(88,118,20);d.doc(162,74,62,78,CREAM);d.path('M176 208 L192 174 L202 169 L211 178 L211 197 L190 216 Z',LILAC,'accent');d.line([(172,217),(186,229)]);d.spark(184,36,12)
 elif n==51:
  d.book(28,60,65,102,BLUE);d.book(82,42,65,102,LILAC);d.book(135,66,65,102,MINT);d.tag(159,178,71,38);d.lock(62,206,.55);d.line([(107,212),(144,212)]);d.arrow((203,153),(203,172))
 elif n==52:
  d.rect(25,29,201,114,WHITE);d.play(127,87,27)
  for i in range(3):d.circle(50+i*76,193,23,PALETTE[i],'accent');d.line([(72+i*76,193),(101+i*76,193)]) if i<2 else None
  d.line([(43,193),(55,193)]);d.line([(121,187),(133,199)]);d.check(202,193,13)
 elif n==53:
  d.doc(36,60,151,147,CREAM);d.star(113,112,27);d.line([(64,166),(154,166)]);d.line([(81,184),(136,184)]);d.path('M45 34 L97 15 L150 34 L97 53 Z',BLUE,'accent');d.line([(146,34),(146,72)]);d.circle(147,74,5,MINT,'details');d.badge(200,201,24,LILAC)
 elif n==54:
  d.screen(24,51,144,98);d.rect(181,45,43,64,LILAC);d.rect(181,125,43,64,MINT);d.lock(98,169,.88);d.line([(163,187),(224,187)]);d.arrow((175,211),(219,211));d.play(67,89,15)
 elif n==55:
  d.bulb(128,59,25);d.rect(25,121,61,88,BLUE);d.rect(98,142,61,67,LILAC);d.rect(170,121,61,88,MINT);d.arrow((116,92),(67,114));d.arrow((140,92),(197,115));d.line([(112,122),(145,122)]);d.line([(37,148),(75,148)]);d.line([(110,169),(146,169)]);d.line([(182,148),(219,148)]);d.spark(47,47,9)
 elif n==56:
  d.rect(66,33,147,112,LILAC);d.rect(47,51,147,112,MINT);d.rect(28,70,147,112,WHITE);d.circle(56,96,8,BLUE,'accent');d.rect(47,118,49,38,CREAM,5,'accent');d.line([(110,123),(157,123)]);d.line([(110,141),(145,141)]);d.play(196,204,22);d.line([(42,211),(143,211)])
 elif n==57:
  d.screen(26,40,158,114);d.person(105,101,.9);d.play(152,129,15);d.doc(155,164,68,69,CREAM);d.line([(29,194),(121,194)]);d.circle(42,211,8,LILAC,'accent');d.circle(75,211,8,MINT,'accent');d.circle(108,211,8,BLUE,'accent')
 elif n==58:
  d.cloud(128,65,1);d.arrow((128,97),(128,149));d.rect(61,162,132,68,CREAM);d.line([(61,181),(193,181)]);d.line([(128,162),(128,230)]);d.tag(181,129,48,28);d.spark(30,121,10)
 elif n==59:
  d.book(27,45,70,104,BLUE);d.route([(126,40),(206,40),(206,105),(132,105),(132,180),(211,180)]);d.circle(127,40,15,LILAC,'accent');d.circle(207,105,15,MINT,'accent');d.check(211,180,20);d.line([(28,196),(87,196)]);d.line([(28,217),(112,217)])
 elif n==60:
  d.rect(71,33,138,144,LILAC);d.rect(51,51,138,144,MINT);d.rect(31,69,138,144,WHITE);d.bulb(100,129,25);d.check(190,210,21);d.circle(40,32,8,CREAM,'accent');d.line([(76,186),(126,186)]);d.arrow((159,204),(163,209))
 elif n==61:
  d.screen(24,36,129,103);d.rect(39,53,93,28,MINT);d.check(120,66,10);d.rect(39,91,66,24,CREAM);d.line([(54,64),(87,64)]);d.line([(51,103),(80,103)]);d.route([(37,211),(102,211),(141,179),(208,179)]);d.flag(201,121,59)
 elif n==62:
  d.person(64,65,.9);d.person(191,67,.9,LILAC);d.book(67,140,96,86,CREAM);d.rect(28,96,65,37,BLUE);d.rect(165,99,65,37,MINT);d.arrow((100,113),(153,113));d.line([(103,141),(103,224)]);d.line([(118,167),(148,167)])
 elif n==63:
  d.laptop(25,40,130,89);d.rect(171,31,55,66,LILAC);d.circle(197,55,10,CREAM,'accent');d.line([(181,78),(215,78)]);d.arrow((104,155),(104,181));d.doc(72,180,66,52,MINT);d.gear(194,180,25);d.arrow((151,205),(172,205))
 elif n==64:
  d.screen(22,29,208,137);d.rect(36,46,69,102,BLUE);d.check(70,81,16);d.rect(116,45,98,37,MINT);d.line([(125,66),(146,60),(165,67),(195,53)]);d.rect(116,94,98,53,LILAC);d.line([(127,134),(127,116),(149,116),(149,134),(172,134),(172,108),(195,108),(195,134)]);d.clock(65,213,18);d.book(154,190,51,43,CREAM)
 elif n==65:
  d.laptop(28,49,150,106);d.line([(69,82),(49,99),(69,116)]);d.line([(139,82),(159,99),(139,116)]);d.line([(116,78),(95,123)]);d.rect(28,205,43,28,MINT);d.rect(97,205,43,28,LILAC);d.rect(167,205,43,28,CREAM);d.arrow((78,219),(90,219));d.arrow((148,219),(160,219));d.spark(215,88,10)
 elif n==66:
  d.rect(53,83,153,106,WHITE);d.line([(72,148),(72,125),(92,125),(92,158),(112,158),(112,115),(132,115),(132,148),(152,148),(152,129),(181,129)]);d.path('M41 141 V114 C41 25 218 25 218 114 V141');d.rect(27,113,26,66,BLUE);d.rect(205,113,26,66,LILAC);d.play(129,217,18)
 elif n==67:
  d.path('M27 53 H142 V119 H84 L58 143 V119 H27 Z',BLUE,'main');d.path('M112 121 H229 V188 H194 L173 212 V188 H112 Z',MINT,'main');d.line([(44,78),(124,78)]);d.line([(44,98),(98,98)]);d.line([(130,148),(209,148)]);d.line([(130,168),(188,168)]);d.book(35,183,48,52,LILAC);d.spark(190,64,11)
 elif n==68:
  d.rect(29,49,115,122,WHITE);d.poly([(41,137),(78,92),(104,128),(130,75),(130,157),(41,157)],BLUE,'accent');d.circle(56,77,10,CREAM,'accent');d.rect(161,37,60,53,LILAC);d.rect(161,107,60,53,MINT);d.rect(84,193,137,39,CREAM);d.circle(104,212,10,BLUE,'details');d.circle(139,212,10,MINT,'details');d.circle(174,212,10,LILAC,'details');d.circle(207,212,7,PINK,'details')
 elif n==69:
  d.doc(32,28,121,176,CREAM);d.rect(50,68,84,20,MINT,4,'accent');d.rect(50,111,84,20,LILAC,4,'accent');d.line([(52,165),(132,165)]);d.poly([(175,161),(198,169),(168,230),(153,221)],BLUE);d.poly([(153,221),(168,230),(152,236)],CREAM,'accent');d.circle(203,74,25,MINT,'accent');d.check(203,74,14)
 elif n==70:
  d.screen(28,53,143,107);d.play(100,99,26);d.rect(183,69,45,45,MINT);d.rect(183,132,45,45,LILAC);d.line([(48,218),(136,218)]);d.tag(156,203,76,29);d.line([(192,86),(216,86)]);d.line([(192,149),(218,149)])
 elif n==71:
  d.screen(24,45,90,83,BLUE);d.screen(143,45,90,83,MINT);d.line([(38,104),(48,89),(60,100),(91,66)]);d.line([(157,104),(169,73),(184,84),(214,58)]);d.arrow((111,173),(147,173));d.doc(30,169,49,65,LILAC);d.check(195,197,25)
 elif n==72:
  d.screen(22,28,131,95);d.play(88,69,19);d.gift(148,174,77,57);d.book(28,169,63,62,LILAC);d.arrow((90,139),(127,171));d.spark(201,70,13);d.spark(39,137,8)
 elif n==73:
  d.book(28,124,62,97,BLUE);d.book(92,103,62,118,LILAC);d.book(157,128,62,93,MINT);d.path('M75 64 C36 19 36 100 75 63 C111 25 124 99 153 64 C186 20 202 94 153 64',CREAM,'accent');d.lock(206,43,.55);d.line([(44,173),(75,173)]);d.line([(108,151),(139,151)])
 elif n==74:
  d.tag(25,35,67,39);d.arrow((101,57),(143,57));d.doc(159,26,65,91,MINT);d.check(208,98,14);d.arrow((188,133),(188,166));d.screen(75,171,117,54);d.play(131,195,13);d.lock(43,199,.58)
 elif n==75:
  d.calendar(25,52,105,101);d.check(93,133,18);d.rect(159,39,61,59,BLUE);d.line([(189,50),(189,86)]);d.line([(171,69),(207,69)]);d.person(185,183,.9);d.clock(78,203,23);d.arrow((138,117),(173,130))
 elif n==76:
  d.rect(47,112,161,43,CREAM);d.line([(60,155),(60,203)]);d.line([(194,155),(194,203)]);d.person(77,83,.8);d.person(178,83,.8,LILAC);d.doc(111,94,32,52,BLUE);d.rect(24,176,40,30,MINT);d.rect(193,176,40,30,LILAC);d.spark(128,47,10)
 elif n==77:
  d.rect(38,75,179,100,BLUE);d.path('M38 75 L69 125 L38 175 Z',LILAC,'accent');d.path('M217 75 L186 125 L217 175 Z',LILAC,'accent');d.person(127,123,.9);d.ticket(97,190,120,44);d.star(67,37,14);d.spark(200,39,10)
 elif n==78:
  d.rect(65,166,128,59,BLUE);d.rect(45,154,167,19,LILAC);d.gift(99,105,62,48);d.star(50,57,18);d.star(207,55,19);d.line([(33,101),(45,94)]);d.line([(213,102),(225,110)]);d.spark(129,34,11)
 elif n==79:
  d.person(58,84,1);d.doc(131,39,86,109,CREAM);d.route([(28,203),(97,203),(137,176),(216,176)]);d.circle(94,203,12,LILAC,'accent');d.check(216,176,16);d.line([(151,91),(168,74),(198,97)]);d.line([(150,123),(197,123)])
 elif n==80:
  d.calendar(25,39,122,119);d.clock(194,96,35);d.check(174,197,26);d.doc(38,185,71,45,LILAC);d.arrow((113,206),(140,206));d.line([(173,144),(173,168)])
 elif n==81:
  d.rect(24,116,94,99,BLUE);d.path('M49 116 V102 Q69 87 91 102 V116');d.line([(44,142),(44,187)]);d.line([(98,142),(98,187)]);d.doc(152,27,72,111,CREAM);d.route([(144,162),(200,162),(200,213)]);d.flag(198,184,47);d.star(65,56,20)
 elif n==82:
  d.screen(24,56,90,79,BLUE);d.person(69,100,.7);d.screen(143,56,90,79,MINT);d.person(188,100,.7,LILAC);d.arrow((105,184),(152,184));d.doc(44,180,38,53,CREAM);d.doc(178,180,38,53,LILAC);d.path('M101 30 Q128 14 155 30');d.circle(128,27,5,CREAM,'accent')
 elif n==83:
  d.path('M27 138 H167 V109 H197 L231 143 V201 H27 Z',BLUE,'main');d.rect(179,119,22,33,WHITE);d.circle(72,202,22,LILAC);d.circle(194,202,22,LILAC);d.line([(104,79),(122,43),(138,64),(123,94)]);d.rect(75,43,18,66,MINT);d.line([(46,170),(142,170)]);d.spark(185,53,10)
 elif n==84:
  d.doc(66,34,126,169,CREAM);d.leaf(58,132,.9);d.leaf(199,129,-.9);d.circle(105,126,24,'none','accent');d.circle(137,126,24,'none','accent');d.star(129,80,12);d.line([(87,173),(163,173)]);d.path('M85 220 Q128 236 172 220')
 elif n==85:
  d.doc(27,30,73,103,CREAM);d.line([(41,69),(84,69)]);d.line([(41,91),(78,91)]);d.rect(128,152,93,72,BLUE);d.rect(119,141,111,20,LILAC);d.person(173,100,.9);d.line([(48,171),(98,171)]);d.clock(63,207,23);d.arrow((104,95),(125,95))
 elif n==86:
  d.doc(35,26,99,147,CREAM);d.rect(58,23,50,17,BLUE);d.check(69,77,12);d.line([(91,76),(118,76)]);d.check(69,119,12);d.line([(91,118),(118,118)]);d.person(182,172,.65);d.person(223,172,.55,LILAC);d.person(160,221,.6,BLUE);d.rect(27,205,89,27,MINT)
 elif n==87:
  d.rect(25,52,151,107,BLUE);d.rect(18,38,165,24,LILAC);d.rect(48,107,104,52,CREAM);d.circle(78,78,11,MINT,'accent');d.line([(99,77),(148,77)]);d.line([(37,164),(37,221)]);d.line([(164,164),(164,221)]);d.rect(192,126,39,83,WHITE);d.circle(211,146,10,CREAM,'accent');d.line([(202,177),(220,177)]);d.line([(211,111),(211,125)])
 elif n==88:
  d.screen(23,33,133,96,BLUE);d.person(88,82,.7);d.path('M173 49 H230 V94 H204 L187 110 V94 H173 Z',LILAC,'accent');d.line([(185,70),(218,70)])
  for x in [45,108,172]:d.person(x,203,.73,MINT)
  d.arrow((186,136),(148,168))
 elif n==89:
  d.path('M34 175 V107 C34 25 220 25 220 107 V175 Z',BLUE,'main');d.path('M55 171 V109 C55 49 199 49 199 109 V171 Z',WHITE,'main');d.rect(26,181,203,41,LILAC);d.circle(117,149,17,CREAM,'accent');d.line([(134,149),(134,85),(164,78),(164,132)]);d.circle(148,134,16,MINT,'accent');d.star(75,99,13);d.spark(205,27,9)
 elif n==90:
  d.path('M27 95 H67 L135 61 V159 L67 132 H27 Z',BLUE,'main');d.rect(43,132,24,63,LILAC);d.line([(149,80),(179,66)]);d.line([(151,109),(184,109)]);d.line([(149,140),(179,154)]);d.ticket(109,179,122,50);d.star(211,64,17)
 elif n==91:
  d.rect(31,135,194,27,LILAC);d.line([(46,162),(46,220)]);d.line([(211,162),(211,220)]);d.path('M47 125 Q55 70 105 75 Q150 76 158 125 Z',BLUE,'main');d.line([(37,125),(169,125)]);d.circle(105,66,7,CREAM,'accent');d.circle(193,104,19,MINT,'accent');d.line([(184,93),(184,48)]);d.line([(197,92),(197,48)]);d.line([(211,53),(211,122)]);d.doc(89,185,65,44,CREAM)
 elif n==92:
  d.screen(25,41,125,90,BLUE);d.person(87,84,.67);d.path('M171 88 V65 C171 32 226 32 226 65 V88');d.rect(164,70,14,43,LILAC);d.rect(218,70,14,43,LILAC);d.path('M223 110 V131 H197');d.circle(195,130,5,MINT,'accent');d.rect(44,189,168,42,CREAM);d.check(128,170,18)
 elif n==93:
  d.rect(49,124,157,106,BLUE);d.line([(49,150),(206,150)]);d.line([(101,132),(153,132)],INK,'details',6);d.path('M101 87 C81 55 41 79 65 108 L101 137 L138 107 C163 78 124 57 101 87 Z',PINK,'accent');d.coins(205,66,3);d.arrow((205,89),(185,118));d.person(40,47,.6,MINT)
 elif n==94:
  d.rect(55,68,132,99,BLUE);d.circle(83,86,5,CREAM,'details');d.circle(159,86,5,CREAM,'details');d.line([(100,111),(143,111)]);d.line([(100,133),(143,133)]);d.route([(25,218),(87,218),(129,192),(219,192)]);d.flag(205,27,79);d.star(29,95,11)
 elif n==95:
  d.circle(128,128,59,'none');d.person(128,39,.65,BLUE);d.person(210,127,.65,LILAC);d.person(128,216,.65,MINT);d.person(47,127,.65,CREAM);d.line([(77,83),(90,94)]);d.line([(176,84),(166,94)]);d.line([(78,176),(92,165)]);d.line([(176,176),(164,164)]);d.circle(128,128,22,CREAM,'accent');d.line([(113,128),(143,128)]);d.line([(128,115),(128,141)])
 elif n==96:
  d.rect(26,69,119,135,BLUE);d.path('M145 106 H196 L229 141 V204 H145 Z',MINT,'main');d.rect(155,118,45,41,WHITE);d.circle(63,204,22,LILAC);d.circle(189,204,22,LILAC);d.rect(42,103,44,43,CREAM);d.line([(63,103),(63,146)]);d.rect(99,155,33,28,LILAC);d.arrow((52,45),(121,45))
 elif n==97:
  d.path('M41 111 L123 38 L204 111 Z',CREAM,'main');d.rect(57,106,131,120,BLUE);d.rect(96,145,57,81,MINT);d.circle(141,188,4,CREAM,'details');d.path('M217 47 C183 47 187 90 217 108 C247 90 251 47 217 47 Z',LILAC,'accent');d.circle(217,67,9,WHITE,'details');d.arrow((28,201),(75,201));d.leaf(207,218,.58)
 elif n==98:
  d.rect(45,69,162,112,BLUE);d.path('M78 69 L89 50 H143 L154 69 Z',LILAC,'accent');d.circle(126,124,38,WHITE);d.circle(126,124,24,MINT,'accent');d.circle(126,124,10,CREAM,'details');d.rect(176,88,16,14,CREAM);d.line([(23,28),(23,60),(53,60)]);d.line([(204,27),(233,27),(233,57)]);d.line([(23,196),(23,229),(55,229)]);d.line([(205,229),(234,229),(234,197)])
 elif n==99:
  d.person(55,200,.9,MINT);d.person(190,201,.9,LILAC);d.rect(26,56,76,70,BLUE);d.rect(155,39,76,70,CREAM);d.line([(64,126),(64,176)]);d.line([(193,109),(193,176)]);d.bulb(64,87,15);d.check(193,74,15);d.arrow((111,73),(143,73));d.spark(126,164,11)
 # Each group has actual geometry and can be animated independently.
 if not d.groups['accent']:d.circle(128,128,4,LILAC,'accent')
 if not d.groups['details']:d.line([(116,128),(140,128)])
 return d

def metadata(i,title):
 cid=1201+i;category=CATS[i//25];collection='explainer' if i<50 else 'promotion';use=['decision explainer','tradeoff teaching'] if i<25 else ['cause and effect explainer','educational systems'] if i<50 else ['digital product promotion','course launch'] if i<75 else ['service promotion','event invitation']
 entrance=['Draw relationship paths, then reveal objects in their causal order.','Pop the central object first, then stagger the supporting choices.','Reveal the main assembly with a soft scale and trace detail strokes.','Slide separate objects into their final semantic composition.'][i%4]
 ambient=['Pulse the active accent and move a small highlight along existing connectors.','Use slight parallax between main, accent and details without changing the meaning.','Hold the main object while gently emphasizing one accent at a time.','Cycle a soft focus highlight through the supporting objects.'][i%4]
 exit=['Retract connector strokes before fading the supporting shapes.','Scale the complete composition down together and fade.','Move the accent toward the conclusion, then dissolve the assembly.','Reverse the entrance order with a short soft fade.'][i%4]
 return {'id':f'SV{cid:04d}','title':title,'category':category,'tags':[collection,'concept assembly','pastel','layered','original',*title.lower().split()],'svg':f'svg/files/SV{cid:04d}.svg','viewBox':'0 0 256 256','license':'Original generated SVG; reusable','layers':['main','accent','details'],'collection':collection,'use_cases':use,'suggested_motion':{'entrance':entrance,'ambient':ambient,'exit':exit},'motion_status':'suggestion-only; static SVG'}

def main():
 (ROOT/'files').mkdir(exist_ok=True);rows=[]
 for i,title in enumerate(TITLES):
  row=metadata(i,title);svg=draw_recipe(i).render(row['id'],title);(ROOT/'files'/(row['id']+'.svg')).write_text(svg);rows.append(row)
 assert len(rows)==100
 (ROOT/'svg_explainer_promo_concepts_index.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 print('Generated',len(rows),'original SVG concept compositions')
if __name__=='__main__':main()
