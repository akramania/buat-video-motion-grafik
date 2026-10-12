#!/usr/bin/env python3
"""Reproducible original explainer assemblies SV1101--SV1200.

Static layered SVG, transparent 256-square canvas. Suggested motion metadata is
guidance only, not animation embedded in the file. No external artwork is used.
Every recipe has its own component arrangement and semantic connections.
"""
from pathlib import Path
from collections import Counter
import argparse, hashlib, html, io, json, math, re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
INK='#416070';BLUE='#B7DDF2';MINT='#B7E6D4';LILAC='#D5CCF0';CREAM='#FFF1D6';WHITE='#F8FBFF'
PALETTE=[BLUE,MINT,LILAC,CREAM]

def n(v):return f'{v:g}' if isinstance(v,(int,float)) else str(v)
def att(fill='none',stroke=INK,width=4):
 return f'fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"'
def rect(x,y,w,h,fill=BLUE,rx=7,stroke=INK,width=4):
 return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{n(rx)}" {att(fill,stroke,width)}/>'
def circle(x,y,r,fill=CREAM,stroke=INK,width=4):return f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(r)}" {att(fill,stroke,width)}/>'
def ellipse(x,y,rx,ry,fill=MINT):return f'<ellipse cx="{n(x)}" cy="{n(y)}" rx="{n(rx)}" ry="{n(ry)}" {att(fill)}/>'
def path(d,fill='none',stroke=INK,width=4):return f'<path d="{d}" {att(fill,stroke,width)}/>'
def line(x,y,xx,yy,stroke=INK,width=4):return path(f'M{n(x)} {n(y)} L{n(xx)} {n(yy)}',stroke=stroke,width=width)
def poly(pts,fill=BLUE):return f'<polygon points="{" ".join(f"{n(x)},{n(y)}" for x,y in pts)}" {att(fill)}/>'
def arrow(x,y,xx,yy,color=INK,width=4):
 a=math.atan2(yy-y,xx-x);le=8
 return line(x,y,xx,yy,color,width)+path(f'M{n(xx-le*math.cos(a-.65))} {n(yy-le*math.sin(a-.65))} L{n(xx)} {n(yy)} L{n(xx-le*math.cos(a+.65))} {n(yy-le*math.sin(a+.65))}',stroke=color,width=width)
def curve(d,tip=None):return path(d)+(arrow(*tip) if tip else '')
def tick(x,y,s=8):return path(f'M{n(x-s)} {n(y)} l{n(s*.65)} {n(s*.65)} l{n(s*1.45)} {n(-s*1.6)}',width=3)
def plus(x,y,s=7):return line(x-s,y,x+s,y,width=3)+line(x,y-s,x,y+s,width=3)
def rows(x,y,w,count=3,step=10):return ''.join(line(x,y+i*step,x+w-(i%2)*w*.2,y+i*step,width=3) for i in range(count))
def badge(x,y,r=14,kind='check'):
 return circle(x,y,r,MINT)+(tick(x,y,r*.45) if kind=='check' else plus(x,y,r*.43) if kind=='plus' else line(x-r*.4,y,x+r*.4,y,width=3))
def doc(x,y,w=44,h=58,fill=CREAM):
 return path(f'M{x} {y} H{x+w-12} L{x+w} {y+12} V{y+h} H{x} Z',fill)+path(f'M{x+w-12} {y} V{y+12} H{x+w}')+rows(x+8,y+23,w-16,3,max(7,(h-28)/3))
def card(x,y,w=64,h=42,fill=BLUE):return rect(x,y,w,h,fill,7)+rows(x+10,y+12,w-20,2,11)
def screen(x,y,w=78,h=57,fill=BLUE):
 return rect(x,y,w,h,fill,7)+line(x+3,y+13,x+w-3,y+13,width=3)+circle(x+10,y+7,1.5,INK,INK,3)+line(x+w*.4,y+h,x+w*.4,y+h+12)+line(x+w*.6,y+h,x+w*.6,y+h+12)+line(x+w*.25,y+h+12,x+w*.75,y+h+12)
def laptop(x,y,w=76,h=53):return rect(x+5,y,w-10,h,BLUE,6)+path(f'M{x} {y+h} H{x+w} L{x+w-6} {y+h+12} H{x+6} Z',LILAC)+rows(x+14,y+17,w-28,2,11)
def phone(x,y,w=35,h=61):return rect(x,y,w,h,LILAC,8)+rect(x+5,y+10,w-10,h-20,WHITE,3,width=3)+line(x+w*.35,y+h-5,x+w*.65,y+h-5,width=3)
def rack(x,y,w=48,h=73):
 s=rect(x,y,w,h,BLUE,5)
 for j in range(3):s+=rect(x+6,y+7+j*(h-12)/3,w-12,(h-20)/3,LILAC if j==1 else WHITE,3,width=3)+circle(x+12,y+15+j*(h-12)/3,2,MINT,INK,3)
 return s
def database(x,y,w=46,h=52,fill=BLUE):
 return path(f'M{x} {y+8} V{y+h-8} C{x} {y+h+2} {x+w} {y+h+2} {x+w} {y+h-8} V{y+8}',fill)+ellipse(x+w/2,y+8,w/2,8,fill)+path(f'M{x} {y+h/2} C{x} {y+h/2+10} {x+w} {y+h/2+10} {x+w} {y+h/2}',width=3)
def cloud(x,y,w=80,h=42):return path(f'M{x+14} {y+h} C{x-8} {y+h} {x-2} {y+14} {x+17} {y+15} C{x+20} {y-7} {x+w*.6} {y-6} {x+w*.66} {y+15} C{x+w+8} {y+4} {x+w+17} {y+h} {x+w-7} {y+h} Z',BLUE)
def lock(x,y,w=28,h=30):return rect(x,y+12,w,h-12,LILAC,5)+path(f'M{x+5} {y+12} V{y+5} Q{x+w/2} {y-6} {x+w-5} {y+5} V{y+12}')+circle(x+w/2,y+21,2.5,INK,INK,3)
def shield(x,y,w=49,h=57,fill=MINT):return path(f'M{x+w/2} {y} L{x+w} {y+11} V{y+h*.53} Q{x+w} {y+h*.8} {x+w/2} {y+h} Q{x} {y+h*.8} {x} {y+h*.53} V{y+11} Z',fill)
def key(x,y,le=32):return circle(x,y,8,CREAM)+line(x+8,y,x+le,y)+line(x+le-7,y,x+le-7,y+7,width=3)+line(x+le,y,x+le,y+6,width=3)
def folder(x,y,w=65,h=45,fill=CREAM):return path(f'M{x} {y+10} V{y} H{x+w*.4} L{x+w*.52} {y+10} H{x+w} V{y+h} H{x} Z',fill)
def node(x,y,r=13,fill=MINT):return circle(x,y,r,fill)+circle(x,y,3,WHITE,INK,3)
def person(x,y,scale=1,fill=MINT):
 r=8*scale;return circle(x,y,r,CREAM)+path(f'M{x-14*scale} {y+27*scale} V{y+18*scale} Q{x} {y+6*scale} {x+14*scale} {y+18*scale} V{y+27*scale} Z',fill)
def bubble(x,y,w=58,h=35,fill=BLUE):return path(f'M{x+8} {y} H{x+w-8} Q{x+w} {y} {x+w} {y+8} V{y+h-8} Q{x+w} {y+h} {x+w-8} {y+h} H{x+22} L{x+10} {y+h+10} V{y+h} H{x+8} Q{x} {y+h} {x} {y+h-8} V{y+8} Q{x} {y} {x+8} {y} Z',fill)
def clock(x,y,r=20):return circle(x,y,r,CREAM)+line(x,y,x,y-r*.55,width=3)+line(x,y,x+r*.45,y+r*.2,width=3)
def leaf(x,y,w=29,h=45):return path(f'M{x} {y+h} Q{x-8} {y+7} {x+w} {y} Q{x+w+7} {y+h-5} {x} {y+h} Z',MINT)+path(f'M{x} {y+h} Q{x+w*.3} {y+h*.5} {x+w*.7} {y+h*.2}',width=3)
def gear(x,y,r=18):
 points=[]
 for i in range(16):
  a=i*math.tau/16;rr=r if i%4 in (0,3) else r*.78;points.append((x+rr*math.cos(a),y+rr*math.sin(a)))
 return poly(points,LILAC)+circle(x,y,r*.32,WHITE,width=3)
def chart(x,y,w=55,h=41):return line(x,y+h,x+w,y+h,width=3)+line(x,y+h,x,y,width=3)+''.join(rect(x+8+j*15,y+h-(12+j*9),9,12+j*9,[BLUE,MINT,LILAC][j],2,width=3) for j in range(3))
def meter(x,y,w=50,h=15,q=.6):return rect(x,y,w,h,WHITE,6,width=3)+rect(x+4,y+4,max(5,(w-8)*q),h-8,MINT,3,width=3)
def table(x,y,w=61,h=55,cols=3,rowsn=3):
 s=rect(x,y,w,h,WHITE,4)
 for j in range(1,cols):s+=line(x+w*j/cols,y+2,x+w*j/cols,y+h-2,width=3)
 for j in range(1,rowsn):s+=line(x+2,y+h*j/rowsn,x+w-2,y+h*j/rowsn,width=3)
 return s
def cursor(x,y,fill=LILAC):return poly([(x,y),(x+4,y+20),(x+10,y+14),(x+20,y+10)],fill)
def bolt(x,y,w=24,h=37):return poly([(x+w*.55,y),(x,y+h*.55),(x+w*.46,y+h*.55),(x+w*.27,y+h),(x+w,y+h*.4),(x+w*.55,y+h*.4)],CREAM)
def tree(x,y,s=1):return line(x,y+10*s,x,y+48*s)+circle(x,y,19*s,MINT)+circle(x-14*s,y+11*s,14*s,MINT)+circle(x+14*s,y+11*s,14*s,MINT)
def house(x,y,w=48,h=45,fill=BLUE):return rect(x,y+15,w,h-15,fill,3)+poly([(x-3,y+16),(x+w/2,y),(x+w+3,y+16)],LILAC)+rect(x+w*.4,y+h-18,w*.2,18,CREAM,2,width=3)
def building(x,y,w=36,h=80):return rect(x,y,w,h,BLUE,3)+''.join(rect(x+6+j*14,y+9+k*18,8,10,CREAM,1,width=3) for k in range(max(1,int((h-16)/18))) for j in range(2))
def wheel(x,y,r=10):return circle(x,y,r,WHITE,width=3)+circle(x,y,2,INK,INK,3)
def car(x,y,w=67,h=34):return path(f'M{x} {y+14} H{x+13} L{x+23} {y} H{x+w-18} L{x+w-8} {y+14} H{x+w} V{y+h-7} H{x} Z',BLUE)+wheel(x+14,y+h-7,8)+wheel(x+w-14,y+h-7,8)+path(f'M{x+24} {y+5} H{x+w-23} L{x+w-15} {y+14} H{x+18} Z',WHITE,width=3)
def bicycle(x,y,s=1):
 return wheel(x,y,13*s)+wheel(x+45*s,y,13*s)+path(f'M{x} {y} L{x+18*s} {y-22*s} L{x+31*s} {y} H{x} L{x+12*s} {y-17*s} H{x+40*s} L{x+45*s} {y}',width=3)+line(x+15*s,y-23*s,x+26*s,y-23*s,width=3)+line(x+39*s,y-24*s,x+49*s,y-24*s,width=3)
def solar(x,y,w=63,h=26):return poly([(x+9,y),(x+w,y),(x+w-9,y+h),(x,y+h)],BLUE)+line(x+6,y+h/2,x+w-5,y+h/2,width=3)+line(x+w/3+6,y,x+w/3-3,y+h,width=3)+line(x+2*w/3+6,y,x+2*w/3-3,y+h,width=3)
def tank(x,y,w=38,h=46):return rect(x,y,w,h,BLUE,8)+line(x+3,y+h*.46,x+w-3,y+h*.46,width=3)+path(f'M{x+9} {y+5} Q{x+w/2} {y+13} {x+w-9} {y+5}',width=3)
def crate(x,y,w=38,h=32):return rect(x,y,w,h,CREAM,3)+line(x+2,y+10,x+w-2,y+10,width=3)+line(x+w*.4,y+2,x+w*.4,y+h-2,width=3)
def flag(x,y,h=37):return line(x,y,x,y+h)+path(f'M{x} {y} H{x+28} L{x+22} {y+10} L{x+28} {y+20} H{x} Z',MINT)
def dashed_box(x,y,w,h):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" {att("none",INK,3)} stroke-dasharray="7 6"/>'
def pipes(points):return path('M'+' L'.join(f'{n(x)} {n(y)}' for x,y in points),stroke=INK,width=4)
def ring_arrow(x,y,r=35):return path(f'M{x-r} {y} A{r} {r} 0 1 1 {x+2} {y+r}')+arrow(x+2,y+r,x-9,y+r-5)

class Art:
 def __init__(self):self.groups={'main':[],'accent':[],'details':[]}
 def add(self,group,*shapes):self.groups[group].extend(shapes)
 def main(self,*s):self.add('main',*s)
 def accent(self,*s):self.add('accent',*s)
 def details(self,*s):self.add('details',*s)
 def svg(self,title):
  groups=''.join(f'<g id="{k}">{"".join(v)}</g>' for k,v in self.groups.items())
  return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img"><title>{html.escape(title)}</title>{groups}</svg>\n'

def digital(i,a):
 if i==0: # intake, scan and validated delivery
  a.main(doc(23,69,46,69),rack(105,59,48,93),folder(183,77,49,61))
  a.accent(arrow(73,105,99,105),arrow(157,105,178,105),badge(208,165,17),rect(22,180,211,36,WHITE,6))
  a.details(rows(34,192,69,2,11),meter(135,189,84,16,.78),line(128,157,128,174))
 elif i==1:
  a.main(rect(21,39,52,175,CREAM),rect(101,40,72,173,WHITE),rect(195,82,39,90,BLUE))
  a.accent(*(rect(30,52+j*43,34,29,PALETTE[j%4],4) for j in range(3)),*(gear(136,66+j*56,17) for j in range(3)),badge(214,128,13))
  a.details(*(arrow(76,65+j*56,108,65+j*56) for j in range(3)),pipes([(173,66),(185,66),(185,186),(172,186)]),arrow(185,128,194,128))
 elif i==2:
  a.main(screen(22,47,81,65),doc(177,55,51,65),rect(72,164,121,53,CREAM))
  a.accent(person(132,111,.88),shield(111,33,43,50),tick(132,57),badge(205,177,15))
  a.details(arrow(106,90,117,106),arrow(149,104,171,93),rows(85,182,93,2,14),line(132,139,132,158))
 elif i==3:
  a.main(doc(23,107,44,66),screen(98,51,75,68),circle(207,137,25,BLUE))
  a.accent(card(94,169,83,46,MINT),flag(203,38,42),ellipse(207,137,10,25,WHITE))
  a.details(arrow(73,132,95,107),arrow(175,107,188,118),line(182,137,232,137,width=3),arrow(128,132,128,160),rows(108,184,52,2,12))
 elif i==4:
  a.main(rack(35,64,54,111),card(140,63,80,49),card(140,158,80,49,MINT))
  a.accent(gear(114,137,15),ring_arrow(113,137,45),badge(207,133,13,'minus'))
  a.details(arrow(93,87,131,87),arrow(153,139,171,139),arrow(190,146,190,153),meter(46,190,75,16,.42))
 elif i==5:
  a.main(doc(25,33,43,52),doc(25,102,43,52,MINT),doc(25,171,43,52,LILAC),folder(169,89,63,87))
  a.accent(node(119,129,22),poly([(191,109),(214,109),(214,135),(203,148),(191,135)],MINT))
  a.details(pipes([(72,58),(87,58),(87,198),(72,198)]),arrow(86,129,94,129),arrow(144,129,162,129),rows(178,159,44,2,9))
 elif i==6:
  a.main(laptop(22,142,90,62),cloud(79,35,89,49),rack(185,132,48,83))
  a.accent(node(124,122,15),badge(148,197,14))
  a.details(arrow(64,128,88,87),arrow(163,84,205,124),arrow(117,176,174,176),arrow(177,187,120,187),rows(94,50,39,2,10))
 elif i==7:
  a.main(rect(22,92,57,76,WHITE),rect(100,60,56,105,BLUE),rect(180,103,54,73,MINT))
  a.accent(gear(50,117,13),crate(113,95,30,30),flag(195,121,35),badge(128,210,15))
  a.details(arrow(81,130,95,118),arrow(160,118,176,138),meter(28,151,45,10,.75),meter(107,147,42,10,.65),line(128,172,128,191))
 elif i==8:
  a.main(rect(98,80,59,94,BLUE),doc(23,39,40,47),doc(193,37,40,47,MINT),table(20,170,46,46),database(192,163,43,54))
  a.accent(gear(127,128,21),badge(129,207,12))
  a.details(arrow(68,72,93,95),arrow(190,72,160,97),arrow(93,159,72,184),arrow(160,159,186,184),rows(109,90,33,2,9))
 elif i==9:
  a.main(path('M113 31 Q128 21 143 31 V61 L154 76 H102 L113 61 Z',CREAM),card(23,133,53,70),phone(111,133,34,74),folder(181,142,52,61))
  a.accent(circle(128,82,7,LILAC),node(128,110,9))
  a.details(pipes([(49,126),(49,110),(209,110),(209,136)]),line(128,89,128,124),rows(30,175,33,2,11),tick(128,169),rows(190,170,34,2,10))
 elif i==10:
  a.main(table(21,65,59,105),poly([(100,73),(161,73),(143,109),(143,156),(118,171),(118,109)],LILAC),doc(184,101,49,72,MINT))
  a.accent(badge(136,205,16),circle(101,184,5,CREAM),circle(168,170,5,BLUE))
  a.details(arrow(82,118,98,118),arrow(150,136,178,136),line(102,86,159,86,width=3),line(107,99,153,99,width=3))
 elif i==11:
  a.main(rack(23,90,48,96),database(103,51,49,54,MINT),rack(185,91,48,96))
  a.accent(rect(94,167,71,48,CREAM),bolt(116,177,26,31))
  a.details(pipes([(71,112),(89,112),(89,78),(98,78)]),pipes([(157,78),(174,78),(174,112),(183,112)]),arrow(72,168,88,168),arrow(168,168,181,168),line(128,111,128,151))
 elif i==12:
  a.main(rect(23,39,118,170,WHITE),card(174,114,59,59,MINT))
  a.accent(*(rect(37,65+j*39,86,25,PALETTE[j],4) for j in range(3)),badge(183,56,16))
  a.details(*(tick(107,78+j*39,6) for j in range(3)),arrow(145,134,168,134),rows(36,188,77,1),rows(184,130,32,3,12))
 elif i==13:
  a.main(doc(21,37,39,49),doc(21,104,39,49,MINT),doc(21,171,39,49,LILAC),rect(109,42,124,168,BLUE))
  a.accent(circle(159,117,25,WHITE),line(177,137,197,158,width=5),rect(127,179,76,17,MINT,3))
  a.details(pipes([(67,60),(86,60),(86,196),(67,196)]),arrow(86,128,104,128),rows(129,63,87,2,12),rows(146,110,27,2,11))
 elif i==14:
  a.main(clock(76,76,36),card(139,39,89,43),card(139,106,89,44,MINT),card(61,180,155,43,LILAC))
  a.accent(node(111,143,11),badge(36,192,11))
  a.details(pipes([(111,80),(123,80),(123,128),(137,128)]),arrow(78,118,101,138),arrow(117,157,131,176),rows(70,191,113,2,13))
 elif i==15:
  a.main(doc(25,51,86,145),rect(151,85,81,80,MINT),rect(126,187,107,35,CREAM))
  a.accent(rect(41,87,53,63,BLUE,3),line(27,133,108,133,MINT,5),badge(198,45,16))
  a.details(arrow(118,126,145,126),rows(164,103,52,4,13),rows(139,201,80,1),poly([(161,38),(181,43),(165,53)],CREAM))
 elif i==16:
  a.main(rect(23,42,67,90,CREAM),rect(137,93,94,122,BLUE),person(57,72,.9))
  a.accent(key(108,51,34),*(rect(148+j*38,121+k*36,27,25,[MINT,LILAC][(j+k)%2],3) for j in range(2) for k in range(2)),badge(78,178,16))
  a.details(arrow(94,104,129,115),rows(150,192,66,1),path('M53 139 V178 H57'))
 elif i==17:
  a.main(rect(24,102,208,36,CREAM),card(30,30,56,47),database(172,29,52,56),phone(44,173,33,59),rack(176,160,51,72))
  a.accent(node(128,120,12),node(60,120,7),node(198,120,7))
  a.details(arrow(60,81,60,100),arrow(197,92,197,98),arrow(60,140,60,166),arrow(197,141,197,155),line(77,120,111,120,width=3),line(145,120,180,120,width=3))
 elif i==18:
  a.main(card(23,48,83,54),doc(151,37,77,92),rect(45,170,163,53,MINT))
  a.accent(circle(118,127,18,CREAM),badge(191,189,17))
  a.details(arrow(85,115,100,124),arrow(139,123,151,113),arrow(117,149,117,164),rows(57,187,102,2,14),line(41,63,83,63,width=3))
 elif i==19:
  a.main(rect(23,63,87,72,LILAC),rect(23,160,87,48,CREAM),doc(180,72,52,89,BLUE))
  a.accent(poly([(54,82),(54,115),(84,99)],MINT),gear(142,139,23),badge(204,201,14))
  a.details(*(line(31,172+j*13,100,172+j*13,width=3) for j in range(2)),arrow(114,103,126,121),arrow(113,181,133,158),arrow(166,136,174,128),line(24,74,108,74,width=3),line(24,124,108,124,width=3))
 elif i==20:
  a.main(rect(38,32,180,79,BLUE),card(20,162,94,60,CREAM),card(143,162,92,60,MINT))
  a.accent(chart(59,54,63,42),circle(164,70,22,LILAC),node(128,137,9))
  a.details(pipes([(68,155),(68,137),(187,137),(187,155)]),line(128,113,128,129),rows(30,191,62,2,12),rows(153,191,62,2,12))
 elif i==21:
  a.main(rack(27,79,45,101),cloud(94,30,72,45),database(187,81,44,49,MINT),database(186,163,45,50,LILAC))
  a.accent(clock(128,145,23))
  a.details(arrow(76,95,95,71),arrow(169,70,188,88),arrow(209,138,209,158),path('M175 192 H140 V183'),arrow(99,147,79,147),rows(109,48,40,1))
 elif i==22:
  a.main(doc(29,43,85,139),card(160,43,66,49),card(160,120,66,49,MINT),rect(65,205,151,22,CREAM,4))
  a.accent(path('M82 129 L125 82 L137 94 L94 140 Z',LILAC),poly([(78,145),(81,130),(94,141)],CREAM),badge(131,179,14))
  a.details(arrow(119,78,153,67),arrow(155,143,125,143),rows(74,216,121,1),line(113,188,98,203))
 elif i==23:
  a.main(rect(24,66,58,67,CREAM),rect(105,48,52,73,BLUE),rect(181,83,52,70,MINT),rect(111,178,73,44,LILAC))
  a.accent(clock(53,99,17),gear(131,86,16),bolt(196,99,21,30))
  a.details(arrow(86,98,100,87),arrow(161,90,176,108),pipes([(207,158),(207,199),(189,199)]),pipes([(105,199),(50,199),(50,140)]),arrow(50,145,50,139))
 else:
  a.main(phone(23,86,42,77),rack(186,61,46,105),rect(87,181,114,39,CREAM))
  a.accent(rect(91,75,55,65,MINT),gear(118,109,16),badge(218,203,14))
  a.details(arrow(70,104,85,104),arrow(151,104,180,104),arrow(180,143,71,143),rows(98,194,85,2,11),line(119,145,119,175))

def privacy(i,a):
 if i==0:
  a.main(table(23,44,111,95,4,4),doc(178,135,53,86,MINT),card(25,177,109,39,CREAM))
  a.accent(rect(33,76,92,16,LILAC,3,width=3),shield(159,40,58,67),tick(188,69,13),badge(150,199,12))
  a.details(arrow(140,80,153,80),pipes([(135,115),(155,115),(155,171),(172,171)]),line(60,149,60,168),line(75,149,75,168),rows(188,194,32,1))
 elif i==1:
  a.main(laptop(22,74,74,57),rack(190,68,43,94),rect(76,176,119,41,MINT))
  a.accent(lock(115,80,32,44),*(rect(108+j*15,147,10,15,LILAC,2,width=3) for j in range(4)))
  a.details(arrow(99,111,111,111),arrow(151,111,183,111),rows(88,189,90,2,13),line(133,131,133,142))
 elif i==2:
  a.main(person(52,56,1.4),doc(135,35,93,157,CREAM),rect(27,168,80,46,BLUE))
  a.accent(rect(150,82,53,17,MINT,8),circle(194,90,6,WHITE,width=3),rect(150,118,53,17,LILAC,8),circle(159,126,6,WHITE,width=3),badge(211,216,13))
  a.details(arrow(100,117,129,117),rows(44,185,47,2,11),rows(151,159,58,2,11),line(43,142,43,158))
 elif i==3:
  a.main(rect(24,46,102,98,BLUE),database(169,41,62,72),folder(164,171,68,51,LILAC))
  a.accent(line(26,73,124,73),circle(48,95,4,MINT),circle(72,95,4,LILAC),circle(96,95,4,CREAM),lock(47,169,33,42))
  a.details(line(42,36,42,56),line(107,36,107,56),arrow(131,99,161,77),arrow(199,117,199,164),line(172,187,224,215),line(224,187,172,215),rows(35,125,77,1))
 elif i==4:
  a.main(rect(24,41,90,155,CREAM),table(166,78,65,92,3,4))
  a.accent(*(circle(49,67+j*48,10,[BLUE,MINT,LILAC][j]) for j in range(3)),*(rect(69,60+j*48,28,14,WHITE,3,width=3) for j in range(3)),shield(107,100,44,51),tick(129,124))
  a.details(arrow(117,123,121,123),arrow(154,123,163,123),*(circle(178+j*18,91+k*22,3,MINT,INK,3) for j in range(3) for k in range(3)),rows(111,199,110,2,13))
 elif i==5:
  a.main(doc(26,35,88,154),doc(154,64,78,143,BLUE))
  a.accent(rect(39,74,55,13,LILAC,2,width=3),rect(39,111,62,13,MINT,2,width=3),rect(168,103,45,12,INK,2,width=3),rect(168,134,49,12,INK,2,width=3),badge(123,213,15))
  a.details(arrow(120,128,148,128),rows(169,163,40,3,11),rows(41,161,53,1))
 elif i==6:
  a.main(person(48,63,1.15),rect(108,46,125,162,WHITE),rect(24,163,58,47,CREAM))
  a.accent(key(67,118,31),rect(126,63,90,32,MINT,4),rect(126,113,90,32,BLUE,4),rect(126,163,90,27,LILAC,4),lock(187,153,25,33))
  a.details(tick(201,79,6),badge(199,129,8,'minus'),arrow(86,185,101,185),rows(34,179,34,2,11))
 elif i==7:
  a.main(table(22,54,64,113,3,4),circle(137,122,31,LILAC),chart(185,104,49,52))
  a.accent(shield(111,23,51,59),tick(137,49),*(circle(x,y,3,CREAM,INK,3) for x,y in [(125,109),(148,119),(129,136),(149,139),(140,104)]),rect(57,203,145,24,MINT,4))
  a.details(arrow(92,122,102,122),arrow(171,122,182,122),rows(70,215,119,1),line(137,158,137,195))
 elif i==8:
  a.main(laptop(22,47,78,53),phone(30,157,35,64),rect(129,52,48,153,MINT),rack(198,93,34,95))
  a.accent(lock(141,112,25,38),badge(91,170,12),shield(132,43,41,48))
  a.details(arrow(104,83,121,83),pipes([(72,188),(98,188),(98,162),(122,162)]),arrow(182,130,193,130),tick(152,66),line(187,44,187,212,width=3))
 elif i==9:
  a.main(folder(23,44,99,173,BLUE),folder(145,55,87,162,LILAC))
  a.accent(doc(41,91,62,93,CREAM),lock(175,98,34,47),badge(75,202,11))
  a.details(rows(157,170,62,2,14),line(132,42,132,218,width=3),circle(55,52,3,MINT,INK,3),circle(164,63,3,CREAM,INK,3))
 elif i==10:
  a.main(doc(86,31,106,192,CREAM),person(38,68,.8),person(218,136,.8,LILAC))
  a.accent(*(circle(110,91+j*45,8,[BLUE,MINT,LILAC][j]) for j in range(3)),badge(169,199,15))
  a.details(*(rows(129,85+j*45,46,2,12) for j in range(3)),arrow(52,108,79,108),arrow(197,158,211,158),line(110,101,110,127,width=3),line(110,146,110,171,width=3))
 elif i==11:
  a.main(database(21,31,49,55),doc(27,161,42,62,MINT),doc(183,37,47,63,LILAC),doc(183,154,47,69,CREAM))
  a.accent(node(125,124,21),badge(204,123,11))
  a.details(pipes([(74,61),(93,61),(93,104),(108,112)]),arrow(70,188,107,144),arrow(145,105,178,78),arrow(145,142,178,172),rows(94,190,59,2,13))
 elif i==12:
  a.main(circle(128,127,69,WHITE),key(64,82,29),key(160,82,32),key(113,179,37))
  a.accent(lock(111,97,34,48),node(128,35,9),node(220,127,9),node(36,127,9))
  a.details(path('M166 54 Q204 70 207 101'),arrow(205,96,208,108),path('M201 174 Q175 201 147 204'),arrow(155,203,144,204),path('M87 193 Q47 176 44 151'),arrow(46,156,43,146))
 elif i==13:
  a.main(dashed_box(21,68,145,151),screen(46,115,97,73),cloud(167,29,65,47))
  a.accent(lock(125,77,31,40),badge(97,161,13))
  a.details(arrow(191,86,169,115),line(177,102,196,116,width=5),rows(57,139,66,2,14),rows(37,202,110,1))
 elif i==14:
  a.main(dashed_box(22,42,94,173),dashed_box(150,43,83,174),node(48,85,12),node(88,166,13),node(180,85,12),node(204,160,13))
  a.accent(shield(109,101,36,57,LILAC),badge(125,51,11,'minus'))
  a.details(line(54,98,82,151),line(185,98,198,147),arrow(67,117,101,117),line(155,132,165,132,width=3),line(130,64,130,87,width=3),rows(164,195,52,1))
 elif i==15:
  a.main(rect(26,43,112,177,BLUE),database(43,65,42,37,MINT),database(78,117,43,39,LILAC),rect(157,66,75,144,CREAM))
  a.accent(circle(195,139,28,WHITE),lock(181,120,28,38),rect(170,81,45,14,MINT,3))
  a.details(arrow(141,149,152,149),line(30,173,134,173),rows(42,192,82,2,12),line(218,119,218,159,width=3))
 elif i==16:
  a.main(rect(22,43,123,118,BLUE),person(191,64,1.25),doc(166,134,64,89,CREAM))
  a.accent(poly([(34,144),(67,101),(92,126),(116,80),(134,145)],MINT),circle(48,68,9,CREAM),circle(81,190,24,LILAC),tick(81,190,11))
  a.details(arrow(145,116,158,149),line(42,168,60,177,width=3),rows(179,179,36,2,13),line(78,184,85,196,width=3))
 elif i==17:
  a.main(cloud(32,33,96,49),doc(145,80,87,122,CREAM),shield(24,143,71,79))
  a.accent(tick(60,179,17),badge(210,219,13),rect(164,118,50,16,MINT,3))
  a.details(arrow(90,89,90,125),arrow(94,141,130,141),rows(161,157,54,3,13),line(59,116,90,116,width=3))
 elif i==18:
  a.main(person(48,60,1.2),rect(111,42,118,163,BLUE),folder(29,165,59,48,LILAC))
  a.accent(key(70,114,26),rect(132,80,75,48,CREAM,4),badge(169,154,18,'minus'))
  a.details(arrow(94,114,105,114),line(102,104,102,125,width=5),line(40,180,77,203),line(76,181,40,204),rows(125,184,82,1))
 elif i==19:
  a.main(doc(23,32,104,179,CREAM),rect(162,61,70,124,MINT))
  a.accent(circle(96,190,20,LILAC),tick(96,189,10),lock(181,80,31,45),badge(175,215,14))
  a.details(arrow(133,112,157,112),rows(175,145,43,2,13),path('M37 153 Q53 126 60 154 Q73 138 81 157'),rows(36,90,69,3,18))
 elif i==20:
  a.main(rect(21,40,80,169,CREAM),person(48,64,.8),person(69,129,.8,LILAC),rect(166,47,65,159,BLUE))
  a.accent(lock(116,91,29,44),*(rect(177,73+j*49,42,23,MINT if j==1 else LILAC,4) for j in range(3)))
  a.details(arrow(105,117,111,117),arrow(149,117,161,117),rows(37,185,47,1),*(circle(188,84+j*49,2,INK,INK,3) for j in range(3)))
 elif i==21:
  a.main(database(22,45,50,66,LILAC),database(184,45,50,66,BLUE),rect(87,115,83,102,CREAM))
  a.accent(shield(102,137,54,66),chart(105,149,46,32))
  a.details(arrow(64,116,87,140),arrow(193,116,171,140),rows(98,193,60,1),lock(31,144,30,44),lock(194,144,30,44))
 elif i==22:
  a.main(rect(22,34,126,175,BLUE),doc(37,62,89,126,CREAM),rect(178,146,54,70,MINT))
  a.accent(circle(181,82,28,WHITE),line(201,103,218,122,width=5),badge(204,171,10))
  a.details(rows(51,94,59,4,16),rows(165,76,28,2,12),rows(188,192,33,1),arrow(152,154,171,154))
 elif i==23:
  a.main(rack(24,52,70,154),rect(138,61,94,139,CREAM))
  a.accent(rect(133,105,104,27,MINT,5),shield(166,150,38,48),tick(186,173,8))
  a.details(arrow(101,120,126,120),*(line(153,77+j*24,217,77+j*24,width=3) for j in range(4)),path('M141 81 L153 94 M218 137 L228 149',width=3))
 else:
  a.main(rect(68,63,164,143,BLUE),phone(22,89,34,63),person(102,98,.82),person(153,98,.82,LILAC),person(204,98,.82,CREAM))
  a.accent(rect(91,155,33,15,MINT,7),circle(116,162,5,WHITE,width=3),rect(142,155,33,15,LILAC,7),circle(149,162,5,WHITE,width=3),lock(193,143,25,31))
  a.details(arrow(58,119,63,119),rows(82,187,130,1),line(77,77,223,77,width=3),badge(42,203,14))

def collaboration(i,a):
 if i==0:
  a.main(rect(39,65,177,146,WHITE),rect(57,92,63,42,BLUE),rect(138,95,61,78,MINT))
  a.accent(cursor(48,41),cursor(173,49,MINT),cursor(98,170,CREAM),bubble(124,189,102,34,LILAC))
  a.details(rows(65,102,42,2,12),rows(148,110,40,3,17),rows(139,203,69,1),line(55,82,200,82,width=3))
 elif i==1:
  a.main(ellipse(129,145,78,43,BLUE),person(126,37,1.1),person(33,127,.9,LILAC),person(222,130,.9,CREAM))
  a.accent(doc(94,121,45,55,CREAM),badge(159,159,15),bubble(75,72,107,30,MINT))
  a.details(rows(90,84,69,1),line(82,170,82,205),line(177,170,177,205),arrow(65,142,86,142),arrow(192,142,169,142))
 elif i==2:
  a.main(person(46,58,.95),person(202,58,.95,LILAC),person(45,170,.95,CREAM),person(203,170,.95,BLUE),poly([(128,74),(167,97),(167,148),(128,173),(89,148),(89,97)],MINT))
  a.accent(gear(129,124,25),badge(128,211,12))
  a.details(arrow(68,84,84,104),arrow(178,84,174,103),arrow(70,189,90,161),arrow(177,190,168,161),line(128,177,128,194))
 elif i==3:
  a.main(person(42,80,1.2),person(214,150,1.2,LILAC),doc(102,76,54,71,CREAM),rect(43,194,94,31,BLUE))
  a.accent(badge(182,193,15),bubble(173,40,61,39,MINT))
  a.details(path('M62 106 Q87 48 117 64'),arrow(111,67,119,64),path('M145 160 Q176 199 191 176'),arrow(186,180,192,174),rows(52,208,73,1),tick(202,60,7))
 elif i==4:
  a.main(doc(27,52,96,150,CREAM),bubble(144,46,88,50,BLUE),bubble(144,126,88,57,MINT))
  a.accent(person(139,98,.67),person(219,204,.67,LILAC),badge(103,215,13))
  a.details(rows(156,61,59,2,13),rows(155,141,60,3,13),arrow(127,86,137,77),arrow(138,154,125,154),rows(43,112,61,4,17))
 elif i==5:
  a.main(rect(49,50,181,158,CREAM),bubble(75,78,132,34,BLUE),bubble(75,134,132,36,MINT),person(28,65,.75),person(28,146,.75,LILAC))
  a.accent(clock(201,212,17))
  a.details(rows(88,92,101,1),rows(88,148,101,1),line(62,69,62,188,width=3),arrow(39,85,46,85),arrow(39,166,46,166),line(78,188,174,188,width=3))
 elif i==6:
  a.main(doc(65,36,127,185,CREAM),path('M20 106 L49 77 L60 88 L31 117 Z',BLUE),path('M204 154 L231 127 L241 139 L215 164 Z',MINT))
  a.accent(rect(82,82,93,38,BLUE,3),rect(82,141,93,41,MINT,3),cursor(57,118),cursor(184,179,LILAC))
  a.details(rows(88,93,80,2,13),rows(88,152,80,2,13),line(82,64,169,64,width=3),poly([(18,120),(20,108),(31,118)],CREAM))
 elif i==7:
  a.main(doc(23,38,45,56,BLUE),doc(188,38,45,56,MINT),doc(103,173,47,59,LILAC),circle(128,115,31,CREAM))
  a.accent(path('M111 110 Q128 88 145 110 V125 L137 137 H119 L111 125 Z',MINT),line(118,143,139,143,width=3),line(121,152,137,152,width=3))
  a.details(arrow(74,85,99,103),arrow(183,85,158,103),arrow(128,153,128,167),rows(88,213,8,1))
 elif i==8:
  a.main(rect(80,42,153,172,WHITE),person(39,72,.9),person(39,145,.9,LILAC))
  a.accent(*(rect(94+j*43,67+k*42,34,27,PALETTE[(j+k)%4],4) for j in range(3) for k in range(3)),badge(41,214,12))
  a.details(arrow(56,102,75,102),arrow(56,168,75,168),line(92,193,220,193,width=3))
 elif i==9:
  a.main(person(53,58,1.3),person(154,62,1.02,LILAC),rect(25,152,112,64,BLUE),rect(163,142,70,77,CREAM))
  a.accent(bubble(87,34,84,37,MINT),badge(201,169,11),badge(201,198,11))
  a.details(arrow(84,109,128,109),rows(39,171,85,3,13),rows(101,47,55,1),line(170,176,182,176,width=3),line(170,202,182,202,width=3))
 elif i==10:
  a.main(bubble(22,37,85,63,BLUE),bubble(149,37,85,63,LILAC),rect(77,142,105,77,MINT))
  a.accent(person(48,116,.83),person(211,116,.83,CREAM),badge(130,180,18))
  a.details(rows(35,51,53,3,13),rows(163,51,52,3,13),path('M75 128 Q103 100 128 132 Q153 100 181 128'),arrow(95,121,121,139),arrow(167,121,138,138),line(94,202,163,202,width=3))
 elif i==11:
  a.main(person(38,46,.8),person(129,36,.8,LILAC),person(218,46,.8,CREAM),rect(27,125,203,96,WHITE))
  a.accent(rect(41,143,67,18,BLUE,4),rect(89,169,90,18,MINT,4),rect(151,193,64,14,LILAC,4))
  a.details(arrow(39,82,62,117),arrow(128,69,128,117),arrow(214,84,195,117),line(37,134,37,211,width=3),line(41,211,218,211,width=3))
 elif i==12:
  a.main(screen(20,35,66,63),screen(104,29,61,69),screen(183,35,51,63),rect(54,161,148,60,CREAM))
  a.accent(person(52,64,.67),person(135,61,.67,LILAC),person(208,64,.67,MINT),clock(128,131,19))
  a.details(arrow(65,114,91,150),arrow(194,114,166,150),rows(68,178,118,3,13),line(129,151,129,157))
 elif i==13:
  a.main(person(40,148,1.03),person(128,165,1.03,LILAC),person(214,148,1.03,CREAM),rect(54,61,149,62,BLUE))
  a.accent(flag(118,44,56),badge(183,135,14),plus(47,79,7),plus(215,59,7),poly([(70,30),(75,38),(66,44),(60,35)],MINT))
  a.details(arrow(58,135,77,127),arrow(195,138,176,128),rows(70,105,111,1),line(59,217,199,217,width=3))
 elif i==14:
  a.main(person(49,49,1.35),person(155,126,.95,LILAC),doc(91,176,48,56,BLUE),doc(183,177,48,55,CREAM))
  a.accent(bubble(106,31,126,44,MINT),flag(183,92,36))
  a.details(rows(120,47,95,2,12),path('M65 115 Q104 90 141 108'),arrow(136,105,145,109),line(163,157,185,174),line(137,157,121,170))
 elif i==15:
  a.main(bubble(22,39,69,43,BLUE),bubble(166,39,67,43,MINT),doc(97,113,63,94,CREAM))
  a.accent(node(127,51,13),rect(109,144,37,19,LILAC,3),badge(198,205,13))
  a.details(rows(35,55,38,1),rows(178,55,40,1),arrow(96,59,107,59),arrow(147,59,160,59),arrow(126,70,126,105),rows(108,185,37,1),path('M21 142 H75 V188'))
 elif i==16:
  a.main(rect(25,51,48,71,BLUE),rect(104,51,48,71,CREAM),rect(184,51,48,71,MINT),rect(46,177,164,45,LILAC))
  a.accent(path('M35 101 L57 79 L65 86 L43 108 Z',LILAC),ellipse(127,83,17,10,WHITE),circle(127,83,5,BLUE),flag(194,72,35),badge(213,155,12))
  a.details(arrow(77,86,98,86),arrow(157,86,178,86),pipes([(128,130),(128,160),(128,172)]),rows(61,193,132,2,13))
 elif i==17:
  a.main(person(34,47,.8),person(219,47,.8,LILAC),person(34,168,.8,CREAM),person(219,168,.8,BLUE),rack(98,64,60,137))
  a.accent(node(80,98,8),node(178,98,8),node(80,175,8),node(177,175,8))
  a.details(arrow(52,75,74,93),arrow(202,75,183,93),arrow(52,183,74,177),arrow(202,183,183,177),line(89,98,95,98),line(161,98,168,98),line(89,175,95,175),line(161,175,168,175))
 elif i==18:
  a.main(bubble(22,32,66,41,BLUE),bubble(99,27,59,46,MINT),bubble(176,32,59,41,LILAC),rect(68,137,132,87,CREAM))
  a.accent(chart(90,157,65,47),badge(181,194,14))
  a.details(rows(32,45,44,2,11),rows(111,43,36,2,11),rows(187,45,37,2,11),arrow(55,91,86,131),arrow(128,88,128,130),arrow(207,91,180,131))
 elif i==19:
  a.main(rect(32,57,192,156,BLUE),doc(45,80,39,68,CREAM),doc(99,80,40,68,MINT),doc(154,80,43,68,LILAC))
  a.accent(rect(44,165,156,30,WHITE,3),badge(213,189,13))
  a.details(line(37,67,217,67,width=3),rows(55,177,130,1),line(52,48,52,64),line(209,48,209,64),tick(64,138,6),tick(121,138,6),tick(176,138,6))
 elif i==20:
  a.main(person(37,159,.93),person(126,87,.95,LILAC),person(217,33,.93,CREAM),card(22,33,68,53),card(157,147,76,69,MINT))
  a.accent(doc(95,167,43,59,CREAM),badge(214,110,14))
  a.details(arrow(58,154,106,116),arrow(144,86,202,66),path('M79 92 H99 V100'),rows(167,187,52,2,12),line(135,120,116,160))
 elif i==21:
  a.main(rect(24,44,106,111,CREAM),phone(183,54,40,80),rect(66,192,159,32,MINT))
  a.accent(path('M94 82 A22 22 0 1 0 107 116 A17 17 0 0 1 94 82 Z',LILAC),tree(37,181,.65),badge(158,150,14))
  a.details(line(29,68,125,68,width=3),line(39,35,39,53),line(111,35,111,53),line(154,59,154,103,width=4),line(145,82,163,82,width=4),rows(80,207,131,1))
 elif i==22:
  a.main(person(43,51,.94),person(211,51,.94,LILAC),person(126,170,.94,CREAM),crate(94,80,66,54),crate(28,171,48,43),crate(185,171,48,43))
  a.accent(badge(127,53,12),leaf(135,103,17,26))
  a.details(arrow(67,89,88,97),arrow(183,91,166,98),arrow(124,141,124,157),line(65,168,91,150),line(187,165,163,150))
 elif i==23:
  a.main(rect(98,85,61,65,CREAM),person(41,48,.85),person(214,48,.85,LILAC),person(44,176,.85,MINT),person(214,176,.85,BLUE))
  a.accent(path('M116 92 Q129 71 142 92 V112 H116 Z',LILAC),circle(129,116,5,WHITE),plus(129,136,7))
  a.details(arrow(59,88,94,102),arrow(192,88,164,101),arrow(64,190,96,155),arrow(193,190,162,155),line(84,40,98,60),line(173,40,157,60),line(122,46,122,61))
 else:
  a.main(rect(22,35,85,67,BLUE),rect(152,35,80,67,MINT),rect(80,167,99,64,LILAC))
  a.accent(person(48,57,.65),person(80,57,.65,LILAC),person(176,57,.65),person(207,57,.65,CREAM),person(105,190,.65),person(154,190,.65,BLUE),node(128,127,17,CREAM))
  a.details(arrow(92,108,113,118),arrow(167,107,144,118),arrow(128,147,128,161),line(26,93,103,93,width=3),line(157,93,228,93,width=3),line(84,221,175,221,width=3))

def city(i,a):
 if i==0:
  a.main(house(24,80,59,63),house(163,109,67,70),rect(101,157,37,65,MINT),solar(83,30,89,40))
  a.accent(bolt(109,171,21,34),circle(209,43,17,CREAM),leaf(35,171,29,42))
  a.details(line(125,72,125,106),pipes([(87,113),(124,113),(124,151)]),pipes([(141,189),(196,189),(196,184)]),arrow(140,119,159,132),line(39,104,68,104,width=3),line(179,142,213,142,width=3))
 elif i==1:
  a.main(house(25,49,99,105),tank(166,73,51,97),tree(74,182,.75))
  a.accent(path('M130 70 H146 V151 H163'),path('M220 163 V189 H171'),poly([(168,186),(193,186),(183,199),(179,199)],BLUE),rect(153,201,80,25,CREAM,4))
  a.details(line(194,42,188,52,width=3),line(214,31,208,41,width=3),line(163,39,157,49,width=3),line(64,69,64,96,width=3),arrow(161,205,100,205),rows(37,115,65,2,14))
 elif i==2:
  a.main(rect(20,42,108,66,BLUE),rect(32,146,89,63,CREAM),rect(168,66,66,101,MINT))
  a.accent(bicycle(154,216,.84),wheel(44,105,8),wheel(106,105,8),rect(184,87,35,44,WHITE,3),person(202,151,.75,LILAC))
  a.details(rect(29,55,88,30,WHITE,3,width=3),line(36,173,117,173,width=3),pipes([(130,78),(150,78),(150,118),(150,134)]),arrow(150,135,150,152),line(31,228,226,228,width=3))
 elif i==3:
  a.main(rect(25,46,48,67,BLUE),rect(104,38,48,75,MINT),rect(184,46,48,67,LILAC),rect(38,176,93,44,CREAM),crate(177,171,55,49))
  a.accent(gear(87,184,20),leaf(192,178,20,33),ring_arrow(129,135,30))
  a.details(line(20,47,78,47,width=3),line(99,40,157,40,width=3),line(179,47,237,47,width=3),arrow(72,129,86,161),arrow(166,162,181,176),line(113,226,168,226,width=3))
 elif i==4:
  a.main(building(22,39,40,104),building(88,59,36,84),tank(180,50,49,66),rect(82,176,92,47,CREAM))
  a.accent(gear(128,199,18),path('M31 172 Q45 187 60 172 Q75 157 89 172',fill=BLUE),path('M189 156 Q209 170 230 156',fill=BLUE))
  a.details(pipes([(42,148),(42,166),(83,166),(83,174)]),pipes([(173,199),(205,199),(205,120)]),arrow(207,128,207,151),arrow(107,166,107,150),line(172,177,192,177,width=3))
 elif i==5:
  a.main(building(22,98,54,105),building(99,119,51,84),building(178,83,55,120))
  a.accent(rect(20,82,58,18,MINT,5),rect(97,103,55,18,MINT,5),rect(176,65,59,20,MINT,5),leaf(35,48,20,33),leaf(112,70,19,30),leaf(194,31,20,33))
  a.details(pipes([(50,210),(50,225),(202,225),(202,210)]),arrow(84,91,94,112),arrow(155,112,173,81),circle(128,225,4,CREAM,INK,3))
 elif i==6:
  a.main(house(21,83,63,94),rect(156,119,76,57,CREAM),rect(94,189,63,37,LILAC))
  a.accent(rect(22,79,61,17,MINT,3),leaf(37,43,18,32),leaf(59,48,17,29),crate(164,135,27,30),crate(195,135,26,30),gear(126,207,14))
  a.details(path('M154 119 L173 94 H215 L234 119 Z',BLUE),arrow(89,133,148,133),arrow(193,181,163,203),arrow(87,205,54,183),line(182,177,182,193,width=3))
 elif i==7:
  a.main(building(23,35,43,102),building(187,36,44,100),rect(21,168,214,57,CREAM),person(124,112,.95,MINT))
  a.accent(tree(98,54,.66),tree(161,57,.68),*(rect(36+j*37,183,23,30,WHITE,2,width=3) for j in range(5)))
  a.details(line(21,150,84,150,width=3),line(165,150,234,150,width=3),arrow(123,150,123,163),line(81,223,81,230,width=3),line(179,223,179,230,width=3))
 elif i==8:
  a.main(poly([(25,76),(130,34),(232,74),(226,87),(32,88)],BLUE),line(40,90,40,199),line(216,90,216,199),rect(101,125,44,74,MINT))
  a.accent(bicycle(51,192,.74),bicycle(168,193,.68),bolt(111,136,24,39))
  a.details(line(84,103,171,103,width=3),line(28,221,232,221,width=3),path('M142 162 H158 V183 H159'),badge(195,117,11),line(100,202,148,202,width=3))
 elif i==9:
  a.main(building(22,41,41,91),house(92,75,49,53),path('M19 186 Q43 152 73 161 Q105 154 127 175 Q147 153 176 166 Q214 146 237 180 V216 H19 Z',BLUE))
  a.accent(tree(195,102,.75),path('M53 189 Q76 180 99 191 Q121 201 145 191 Q171 181 195 192',stroke=INK,width=3),path('M71 208 Q91 201 116 209',stroke=INK,width=3),leaf(28,167,18,34))
  a.details(arrow(68,141,90,157),line(32,140,32,156,width=3),line(199,170,204,155,width=3),line(218,169,223,153,width=3))
 elif i==10:
  a.main(building(24,81,44,92),house(177,111,53,65),rect(26,199,204,26,CREAM,4),tree(124,85,1.14))
  a.accent(circle(192,43,19,CREAM),path('M91 174 Q127 153 162 174 V191 H91 Z',MINT))
  a.details(*(line(192+math.cos(k*math.tau/6)*25,43+math.sin(k*math.tau/6)*25,192+math.cos(k*math.tau/6)*31,43+math.sin(k*math.tau/6)*31,width=3) for k in range(6)),arrow(141,156,141,184),arrow(107,157,107,184),line(78,218,164,218,width=3))
 elif i==11:
  a.main(rect(24,85,42,69,BLUE),rect(89,65,43,70,MINT),rect(155,88,44,65,LILAC),car(133,189,95,38))
  a.accent(node(44,56,10),node(111,37,10),node(177,61,10),rect(32,100,25,18,WHITE,3),rect(98,82,25,18,WHITE,3),rect(165,103,25,18,WHITE,3))
  a.details(pipes([(43,159),(43,180),(104,180),(104,209),(126,209)]),line(110,140,110,178),line(177,156,177,180,width=3),line(24,156,65,156,width=3),rows(39,123,17,2,10))
 elif i==12:
  a.main(rect(93,56,73,134,BLUE),tree(36,143,.64),building(187,91,45,93))
  a.accent(circle(129,89,23,WHITE),chart(105,128,49,41),cloud(21,39,61,33),leaf(47,208,18,25))
  a.details(path('M111 88 Q120 75 129 87 Q137 101 147 88',width=3),rows(191,205,42,2,11),line(128,194,128,219),line(115,221,142,221),arrow(75,119,88,119))
 elif i==13:
  a.main(tank(22,90,47,88),rect(99,80,57,110,CREAM),house(187,65,43,49),house(187,164,44,53))
  a.accent(rect(112,100,30,18,BLUE,3),rect(112,130,30,18,MINT,3),rect(112,160,30,18,LILAC,3),poly([(38,41),(26,64),(49,64)],BLUE))
  a.details(arrow(73,133,94,133),pipes([(160,133),(174,133),(174,90),(181,90)]),pipes([(174,133),(174,190),(182,190)]),line(35,196,68,196,width=3),line(30,211,78,211,width=3))
 elif i==14:
  a.main(house(22,56,105,124),rect(149,113,84,103,CREAM),screen(149,43,79,47,LILAC))
  a.accent(path('M57 109 L76 90 Q65 79 81 69 L99 73 L91 89 L101 95 L96 111 L78 116 L68 132 Z',MINT),gear(193,147,21),car(45,196,68,33))
  a.details(rows(164,187,49,2,12),arrow(130,153,143,153),rows(154,57,61,2,10),line(30,176,120,176,width=3))
 elif i==15:
  a.main(rect(70,47,113,168,BLUE),person(31,120,.88),person(219,139,.88,LILAC))
  a.accent(*(doc(83+j*31,74,25,48,[CREAM,MINT,LILAC][j]) for j in range(3)),key(102,167,39),crate(136,172,33,31))
  a.details(line(76,134,176,134,width=3),line(76,207,176,207,width=3),arrow(51,153,65,153),arrow(187,178,205,178),rows(85,56,81,1))
 elif i==16:
  a.main(solar(34,36,187,54),line(48,92,48,189),line(209,92,209,189),car(73,172,104,46),rect(23,119,31,67,MINT))
  a.accent(bolt(29,129,20,34),circle(128,122,17,CREAM))
  a.details(path('M55 143 H70 V171'),line(30,231,225,231,width=3),arrow(128,143,128,165),line(147,173,147,188,width=3),line(71,100,188,100,width=3))
 elif i==17:
  a.main(path('M22 143 Q49 116 76 134 L78 203 H24 Z',MINT),path('M177 130 Q202 103 234 129 V203 H177 Z',MINT),path('M74 160 Q129 119 182 159 L182 181 Q127 145 74 182 Z',CREAM))
  a.accent(tree(44,80,.67),tree(213,69,.7),circle(118,160,6,LILAC),circle(132,167,6,LILAC),ellipse(125,179,9,7,LILAC))
  a.details(leaf(31,150,19,30),leaf(206,152,17,29),line(99,210,169,210,width=3),circle(147,160,3,CREAM,INK,3),circle(98,180,3,CREAM,INK,3))
 elif i==18:
  a.main(house(25,55,58,62),line(33,119,33,173),line(72,119,72,173),tree(116,111,.76),tree(184,83,.8))
  a.accent(path('M22 195 Q50 178 77 194 Q105 208 133 193 Q161 178 188 194 Q212 207 235 192',stroke=INK,width=4),path('M24 218 Q54 203 81 217 Q109 230 137 216 Q166 202 193 217 Q215 228 233 216',stroke=INK,width=3),poly([(147,151),(160,134),(171,153),(163,174),(148,174)],MINT))
  a.details(path('M116 147 L103 181 M116 147 L132 181 M184 125 L168 178 M184 125 L199 177'),line(21,174,86,174,width=3))
 elif i==19:
  a.main(rect(21,80,214,42,CREAM,3),path('M35 150 H104 L132 197 H220 V224 H24 V197 Z',BLUE),path('M23 123 H235 V149 H129 L101 124 Z',MINT))
  a.accent(leaf(153,132,21,38),leaf(187,134,21,39),leaf(214,153,18,34))
  a.details(*(line(38+j*48,91,61+j*48,91,width=3) for j in range(4)),arrow(56,127,56,143),arrow(83,159,111,182),line(29,202,93,202,width=3),path('M32 33 L27 45 M81 44 L76 56 M128 30 L123 42 M179 42 L174 54 M221 28 L216 40',width=3))
 elif i==20:
  a.main(building(26,61,46,113),rect(96,145,64,80,MINT),rack(189,75,43,98),solar(95,34,65,29))
  a.accent(bolt(117,164,23,38),gear(127,111,19),badge(202,211,12))
  a.details(pipes([(73,118),(97,118),(97,111),(104,111)]),arrow(151,111,182,111),line(127,135,127,142),arrow(128,69,128,87),path('M178 200 H161',width=3))
 elif i==21:
  a.main(rect(24,51,150,104,BLUE),rect(34,66,63,52,WHITE,4),rect(112,68,46,71,MINT,3),path('M37 196 H185 L226 222 H38 Z',CREAM))
  a.accent(wheel(49,155,9),wheel(148,155,9),person(204,87,.92,LILAC),rect(106,137,59,17,WHITE,2))
  a.details(line(114,70,114,137,width=3),path('M160 156 L210 191 H185 L148 165 Z',MINT),*(circle(51+j*24,208,2,INK,INK,3) for j in range(6)),line(228,132,228,184,width=3))
 elif i==22:
  a.main(house(91,35,77,86,CREAM),person(38,133,.95),person(127,179,.95,LILAC),person(218,133,.95,BLUE))
  a.accent(bubble(20,72,55,37,MINT),bubble(181,70,52,37,BLUE),bubble(98,132,59,35,LILAC))
  a.details(arrow(77,90,89,90),arrow(174,90,179,90),line(127,124,127,128,width=3),rows(34,86,24,1),rows(192,84,25,1),rows(112,146,32,1),line(74,229,179,229,width=3))
 elif i==23:
  a.main(building(89,106,68,110),line(31,41,31,211),line(31,42,216,42),path('M31 43 L79 21 L119 42',CREAM),crate(176,172,53,45))
  a.accent(leaf(192,97,25,41),rect(108,89,35,19,MINT,2),gear(56,161,17))
  a.details(line(194,46,194,79),path('M187 78 Q194 92 202 80'),line(90,126,156,126,width=3),line(111,109,111,214,width=3),line(135,109,135,214,width=3),line(30,214,78,214,width=3),arrow(170,175,162,175))
 else:
  a.main(building(21,49,45,111),tank(97,116,51,87),house(182,51,48,54),tree(203,166,.72))
  a.accent(rect(90,94,65,18,MINT,4),leaf(114,50,22,40),poly([(76,172),(82,160),(89,172),(83,181)],BLUE))
  a.details(pipes([(67,139),(85,139),(85,148),(95,148)]),pipes([(152,147),(164,147),(164,82),(176,82)]),arrow(153,184,171,184),arrow(181,217,87,217),line(42,166,42,215,width=3),line(42,215,74,215,width=3))

CATEGORIES=[
 ('Digital process assemblies',[
  'Validated document intake pipeline','Queued worker processing pool','Human review release gate','Multichannel content publishing rail','Controlled workflow retry loop',
  'Batch source merge workspace','Mirrored local cloud synchronisation','Software release staging chain','Structured API routing hub','Notification channel orchestration',
  'Data quality filtering sieve','Cache assisted processing fast lane','Form validation and submission desk','Reference document indexing station','Timed task scheduling engine',
  'Document scan to structured records','Workspace access provisioning','Event bus service connectors','Payment confirmation state assembly','Media packaging export workstation',
  'Analytics detail report branches','Rotating cloud backup assembly','Editorial approval and revision desk','Sensor feedback control circuit','Remote command acknowledgement system']),
 ('Information and privacy concepts',[
  'Purpose limited data minimisation','Encrypted device server transmission','Granular consent choice workspace','Retention schedule and disposal archive','Anonymised record conversion assembly',
  'Selective document redaction station','Least privilege workspace access','Protected aggregate statistics','Independent device trust gateway','Public private information partition',
  'Accountable access audit history','Document lineage provenance tree','Scheduled secret key rotation','Isolated secure workspace boundary','Network incident containment zones',
  'Protected backup recovery vault','Attributable image ownership seal','Verified download trust assembly','Revoked credential access barrier','Signed release verification desk',
  'Separated pseudonym mapping vault','Private clean room aggregate comparison','Readable policy inspection workspace','Verified storage wipe station','Shared family device privacy settings']),
 ('Team collaboration systems',[
  'Multi cursor shared design canvas','Meeting decisions working table','Complementary skills coordination mesh','Confirmed collaborator file handoff','Peer review comments and resolution',
  'Asynchronous team briefing timeline','Coauthored document working regions','Cross source knowledge exchange','Balanced team capacity planner','Buddy supported onboarding desk',
  'Constructive disagreement resolution','Multidisciplinary project roadmap','Remote standup screen assembly','Shared milestone celebration','Mentor guided learning pathway',
  'Multilingual briefing relay','Cross functional product release','Shared resource team allocator','Consolidated team feedback station','Archived decisions evidence shelf',
  'Expert escalation support pathway','Healthy work availability boundaries','Volunteer supply coordination','Coordinated response team beacon','Federated local team workspaces']),
 ('Sustainable city systems',[
  'Solar neighbourhood battery microgrid','Rainwater harvest and garden reuse','Connected public transit interchange','Circular recycling material system','District cooling return circuit',
  'Connected planted rooftop neighbourhood','Local food market compost loop','Pedestrian priority shaded crossing','Covered cycle parking energy hub','Urban flood retention landscape',
  'Tree shaded heat mitigation street','Sensor guided waste collection route','Neighbourhood air quality station','Filtered water distribution network','Community product repair workshop',
  'Shared tools and books resource library','Solar powered electric vehicle carport','Connected urban habitat corridor','Raised homes shoreline protection','Roadside stormwater bioswale',
  'Resilient distributed power hub','Accessible tram boarding interchange','Citizen participation town network','Circular construction material site','Greywater garden reuse district']),
]

MOTION=[
 ('Stagger the intake, processing and output groups','Pulse active connectors; retain the whole composition','Retract connector paths, then fade component groups'),
 ('Reveal the information object before its privacy control','Trace checks or scan bars gently; keep protected records still','Close the privacy control and dissolve the assembly'),
 ('Introduce participants, then their shared work surface','Float cursor/comment accents or highlight the active handoff','Resolve the shared task, then separate participant groups'),
 ('Build infrastructure first, then introduce the resource path','Move small resource markers along connectors; sway plant accents','Settle resource markers, then fade the system as a whole'),
]

def entries():
 result=[]
 for group,(category,titles) in enumerate(CATEGORIES):
  assert len(titles)==25
  for j,title in enumerate(titles):
   ident=f'SV{1101+group*25+j:04d}';entrance,ambient,exit_motion=MOTION[group]
   result.append({'id':ident,'title':title,'category':category,
    'tags':[category.lower(),'explainer','original','pastel','layered']+title.lower().split()[:5],
    'svg':f'svg/files/{ident}.svg','viewBox':'0 0 256 256','license':'Original generated SVG; reusable',
    'layers':['main','accent','details'],'collection':'explainer',
    'use_cases':['Educational video explainer','Animated process explanation','Presentation infographic','Original layered motion asset'],
    'suggested_motion':{'entrance':entrance,'ambient':ambient,'exit':exit_motion}})
 return result

def geometry_hash(xml):
 root=ET.fromstring(xml);parts=[]
 # Ignore colours, layer order and styling when checking exact shape recipes.
 keys={'d','x','y','width','height','rx','ry','cx','cy','r','points','transform','x1','y1','x2','y2'}
 for elem in root.iter():
  name=elem.tag.split('}')[-1]
  if name in {'path','rect','circle','ellipse','polygon','polyline','line'}:
   attrs=tuple(sorted((key,re.sub(r'\s+',' ',value.strip())) for key,value in elem.attrib.items() if key in keys))
   parts.append((name,attrs))
 return hashlib.sha256(repr(sorted(parts)).encode()).hexdigest()

def build(output=ROOT,qa_dir=None):
 output=Path(output);dest=output/'files';dest.mkdir(parents=True,exist_ok=True)
 rows_index=entries();handlers=[digital,privacy,collaboration,city]
 for k,row in enumerate(rows_index):
  art=Art();handlers[k//25](k%25,art)
  assert all(art.groups.values()),row['id']+' has an empty motion layer'
  (dest/(row['id']+'.svg')).write_text(art.svg(row['title']))
 (output/'svg_explainer_systems_index.json').write_text(json.dumps(rows_index,indent=2)+'\n')
 if qa_dir is not None:qa(output,Path(qa_dir),rows_index)
 return rows_index

def qa(output,qa_dir,rows_index):
 import cairosvg
 from PIL import Image,ImageDraw,ImageFont
 qa_dir.mkdir(parents=True,exist_ok=True)
 failures=[];records=[];seen={};previous={}
 for fp in (output/'files').glob('SV*.svg'):
  try:
   number=int(fp.stem[2:])
   if 1<=number<=1000:previous[geometry_hash(fp.read_text())]=fp.stem
  except (ValueError,ET.ParseError):pass
 for row in rows_index:
  fp=output/'files'/(row['id']+'.svg');xml=fp.read_text();root=ET.fromstring(xml)
  forbidden=[elem.tag.split('}')[-1] for elem in root.iter() if elem.tag.split('}')[-1] in {'script','image','foreignObject','use'}]
  hrefs=[value for elem in root.iter() for key,value in elem.attrib.items() if key.endswith('href')]
  layers=[elem.get('id') for elem in root if elem.tag.endswith('g')]
  valid=root.get('viewBox')=='0 0 256 256' and layers==['main','accent','details'] and not forbidden and not hrefs
  widths=[float(elem.attrib['stroke-width']) for elem in root.iter() if 'stroke-width' in elem.attrib]
  if any(w<3 or w>5 for w in widths):valid=False
  png=cairosvg.svg2png(bytestring=xml.encode(),output_width=256,output_height=256)
  image=Image.open(io.BytesIO(png)).convert('RGBA');alpha=image.getchannel('A');bbox=alpha.getbbox()
  margin_ok=bbox is not None and bbox[0]>=12 and bbox[1]>=12 and bbox[2]<=244 and bbox[3]<=244
  if not margin_ok:valid=False
  geom=geometry_hash(xml);duplicate=seen.get(geom) or previous.get(geom)
  if duplicate:valid=False
  seen[geom]=row['id'];image.save(qa_dir/(row['id']+'.png'))
  record={'id':row['id'],'xml_valid':valid,'bbox':bbox,'margin_12px':margin_ok,'transparent_corners':all(image.getpixel(pos)[3]==0 for pos in [(0,0),(255,0),(0,255),(255,255)]),'geometry_sha256':geom,'duplicate_geometry':duplicate,'shape_count':sum(1 for el in root.iter() if el.tag.split('}')[-1] in {'path','rect','circle','ellipse','polygon','line'})}
  records.append(record)
  if not valid:failures.append(row['id'])
 try:fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
 except OSError:fnt=ImageFont.load_default()
 for g,(category,titles) in enumerate(CATEGORIES):
  sheet=Image.new('RGB',(1200,1390),'#F5F8FA');draw=ImageDraw.Draw(sheet);draw.text((20,12),category,font=fnt,fill=INK)
  for j,row in enumerate(rows_index[g*25:(g+1)*25]):
   x=20+(j%5)*238;y=40+(j//5)*268
   art=Image.open(qa_dir/(row['id']+'.png')).resize((218,218));sheet.paste(art,(x,y),art)
   draw.text((x+4,y+221),row['id'],font=fnt,fill=INK)
   name=row['title'];words=name.split();line1='';lines=[]
   for word in words:
    if len(line1)+len(word)+1>31:lines.append(line1);line1=word
    else:line1=(line1+' '+word).strip()
   lines.append(line1)
   for k,s in enumerate(lines[:2]):draw.text((x+4,y+236+k*14),s,font=fnt,fill=INK)
  sheet.save(qa_dir/f'systems_contact_{g+1}.jpg',quality=92)
 report={'collection':'explainer','ids':'SV1101--SV1200','asset_count':len(rows_index),'categories':dict(Counter(x['category'] for x in rows_index)),
  'xml_and_cairosvg_checked':len(records),'previous_geometry_hashes_checked':len(previous),'unique_geometry_hashes':len(seen),'failures':failures,
  'static_svg':True,'suggested_motion_is_guidance_only':True,'no_external_artwork':True,'outline_range':'3--5','palette':[BLUE,MINT,LILAC,CREAM],
  'visual_contact_sheets':[str(qa_dir/f'systems_contact_{g+1}.jpg') for g in range(4)],'records':records}
 (output/'svg_explainer_systems_qa.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'assets':100,'passed':100-len(failures),'failures':failures,'geometry_unique':len(seen),'compared_previous':len(previous)}))
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT);parser.add_argument('--qa-dir',type=Path)
 args=parser.parse_args();items=build(args.output,args.qa_dir)
 print(f'Wrote {len(items)} original static explainer SVG assemblies.')


