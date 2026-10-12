#!/usr/bin/env python3
"""Draw 100 original promotion assemblies SV1301–SV1400.

Standalone deterministic Python generator. Artwork is original code-drawn SVG;
no stock content, scripts, external references, or embedded bitmap resources.
All silhouettes are neutral product placeholders, grouped for recolouring.
"""
from pathlib import Path
import argparse, math, json, hashlib, re, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'files'
INK='#344861'; BLUE='#BFDFF7'; MINT='#C7E8DB'; LILAC='#D9CFF1'; CREAM='#FFF7E8'; PEACH='#F1D3BE'; PINK='#EECFDF'; WHITE='#FFFFFF'
NS='http://www.w3.org/2000/svg'
def at(**kw): return ' '.join(f'{k.replace("_","-")}="{v}"' for k,v in kw.items() if v is not None)
def r(x,y,w,h,fill=BLUE,rx=8,sw=3,**kw): return f'<rect {at(x=x,y=y,width=w,height=h,rx=rx,fill=fill,stroke=INK,stroke_width=sw,**kw)}/>'
def e(x,y,rx,ry,fill=BLUE,sw=3,**kw): return f'<ellipse {at(cx=x,cy=y,rx=rx,ry=ry,fill=fill,stroke=INK,stroke_width=sw,**kw)}/>'
def c(x,y,rad,fill=BLUE,sw=3,**kw): return f'<circle {at(cx=x,cy=y,r=rad,fill=fill,stroke=INK,stroke_width=sw,**kw)}/>'
def p(d,fill='none',sw=3,stroke=INK,**kw): return f'<path {at(d=d,fill=fill,stroke=stroke,stroke_width=sw,stroke_linejoin="round",stroke_linecap="round",**kw)}/>'
def l(x1,y1,x2,y2,stroke=INK,sw=3,**kw): return f'<line {at(x1=x1,y1=y1,x2=x2,y2=y2,stroke=stroke,stroke_width=sw,stroke_linecap="round",**kw)}/>'
def poly(pts,fill=BLUE,sw=3): return f'<polygon {at(points=" ".join(f"{x:.2f},{y:.2f}" for x,y in pts),fill=fill,stroke=INK,stroke_width=sw,stroke_linejoin="round")}/>'
def g(body,tr=None): return f'<g{(" transform="+chr(34)+tr+chr(34)) if tr else ""}>{"".join(body) if isinstance(body,list) else body}</g>'
def linecopy(x,y,w,n=2): return ''.join(l(x,y+k*9,x+w-(k%2)*9,y+k*9,INK,2) for k in range(n))
def sparkle(x,y,s=8,col=CREAM): return p(f'M{x} {y-s} Q{x+2} {y-2} {x+s} {y} Q{x+2} {y+2} {x} {y+s} Q{x-2} {y+2} {x-s} {y} Q{x-2} {y-2} {x} {y-s} Z',col,2)
def leaf(x,y,s=1,rot=0,col=MINT): return g([p('M0 0 Q-24 -35 0 -54 Q24 -35 0 0 Z',col),p('M0 -4 V-46',sw=2)],f'translate({x} {y}) rotate({rot}) scale({s})')
def cylinder(x,y,w=120,h=35,col=BLUE):
    return p(f'M{x-w/2} {y} V{y+h} A{w/2} 12 0 0 0 {x+w/2} {y+h} V{y} Z',col)+e(x,y,w/2,12,CREAM)
def isobox(x,y,w=90,h=52,dep=22,col=BLUE):
    return poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],col)+poly([(x,y),(x+dep,y-dep),(x+w+dep,y-dep),(x+w,y)],CREAM)+poly([(x+w,y),(x+w+dep,y-dep),(x+w+dep,y+h-dep),(x+w,y+h)],LILAC)
def bottle(cx,by,h=82,w=34,col=BLUE,pump=False):
    top=by-h; cap=14; m=[r(cx-w/2,top+cap,w,h-cap,col,w*.2),r(cx-w*.29,top,w*.58,cap,CREAM,3)]
    if pump: m += [r(cx-4,top-12,8,12,LILAC,1),p(f'M{cx-14} {top-12} H{cx+22} V{top-5}',sw=4)]
    m += [r(cx-w*.32,top+h*.44,w*.64,h*.28,CREAM,3,2),linecopy(cx-w*.2,top+h*.56,w*.4,1)]
    return ''.join(m)
def tube(cx,by,h=77,w=38,col=MINT):
    top=by-h; return p(f'M{cx-w/2} {top} H{cx+w/2} L{cx+w*.34} {by-12} H{cx-w*.34} Z',col)+r(cx-w*.34,by-12,w*.68,12,CREAM,2)+l(cx-w*.36,top+8,cx+w*.36,top+8,INK,2)+r(cx-w*.26,top+30,w*.52,22,CREAM,3,2)
def jar(cx,by,w=52,h=45,col=LILAC):
    return r(cx-w/2,by-h,w,h,col,8)+r(cx-w/2-2,by-h-10,w+4,13,CREAM,5)+r(cx-w*.3,by-h+12,w*.6,h*.38,CREAM,3,2)
def carton(cx,by,w=39,h=77,col=CREAM):
    top=by-h; return r(cx-w/2,top,w,h,col,2)+p(f'M{cx-w/2} {top} l7 -10 h{w-14} l7 10',LILAC)+r(cx-w*.3,top+25,w*.6,h*.3,BLUE,2,2)
def pouch(cx,by,w=58,h=74,col=MINT):
    top=by-h; return p(f'M{cx-w/2} {top} H{cx+w/2} Q{cx+w*.32} {top+20} {cx+w/2} {by} H{cx-w/2} Q{cx-w*.32} {top+20} {cx-w/2} {top} Z',col)+l(cx-w/2+5,top+8,cx+w/2-5,top+8,INK,2)+r(cx-w*.29,top+28,w*.58,25,CREAM,4,2)
def can(cx,by,w=34,h=67,col=BLUE):
    return r(cx-w/2,by-h,w,h,col,7)+e(cx,by-h,w/2,5,CREAM)+e(cx,by,w/2,4,CREAM)+r(cx-w*.3,by-h+19,w*.6,25,CREAM,4,2)
def ribbon(cx,y,w=68): return p(f'M{cx} {y} C{cx-w*.65} {y-40} {cx-w*.7} {y+24} {cx} {y} C{cx+w*.7} {y+24} {cx+w*.65} {y-40} {cx} {y} Z',PEACH)+p(f'M{cx-5} {y} L{cx-20} {y+34} L{cx-7} {y+28} L{cx} {y+37} L{cx+7} {y+28} L{cx+20} {y+34} L{cx+5} {y}',PEACH)
def handle(x,y,w=40): return p(f'M{x-w/2} {y} V{y-16} Q{x} {y-42} {x+w/2} {y-16} V{y}',sw=4)
def fin(m,a=None,d=None): return m,a or [],d or []

def stages(i):
    m=[]; a=[]; d=[]
    if i==0: m=[c(128,107,76,BLUE),c(128,107,60,CREAM),cylinder(128,183,149,31,LILAC)]; a=[bottle(128,177,96,41,MINT)]; d=[sparkle(57,66),sparkle(199,122)]
    elif i==1: m=[isobox(28,167,71,44,16,BLUE),isobox(118,123,83,88,18,LILAC)]; a=[jar(63,161,45,33,MINT),bottle(157,116,81,34,BLUE)]; d=[leaf(211,221,.62,34)]
    elif i==2: m=[p('M44 205 V104 C44 3 212 3 212 104 V205 Z',LILAC),p('M60 195 V107 C60 26 196 26 196 107 V195 Z',CREAM),cylinder(128,178,109,31,BLUE)]; a=[bottle(128,171,82,36,MINT)]; d=[l(68,214,189,214)]
    elif i==3: m=[p('M36 41 H220 V206 H36 Z',CREAM),isobox(37,177,156,19,24,BLUE)]; a=[bottle(98,164,83,33,LILAC),jar(165,164,47,34,MINT)]; d=[l(65,75,180,75,WHITE,6),sparkle(196,119)]
    elif i==4: m=[poly([(29,193),(153,130),(227,169),(106,229)],BLUE),poly([(106,229),(227,169),(227,194),(106,241)],LILAC)]; a=[bottle(153,150,91,36,MINT),jar(90,191,44,31,LILAC)]; d=[p('M42 179 L155 121',stroke=CREAM,sw=5)]
    elif i==5: m=[p('M31 39 H225 V210 H31 Z',CREAM),poly([(31,39),(128,132),(31,210)],BLUE),poly([(128,132),(225,39),(225,210)],LILAC),poly([(31,210),(128,132),(225,210)],MINT)]; a=[bottle(128,190,94,37,CREAM)]; d=[sparkle(181,82)]
    elif i==6: m=[e(128,101,70,77,BLUE),e(128,101,56,62,CREAM),cylinder(128,181,164,26,MINT)]; a=[bottle(103,177,81,32,LILAC),tube(157,176,65,32,BLUE)]; d=[p('M86 72 Q112 48 150 50',stroke=WHITE,sw=5)]
    elif i==7: m=[poly([(128,25),(229,169),(27,169)],LILAC),poly([(128,49),(205,159),(51,159)],CREAM),isobox(58,187,126,24,18,BLUE)]; a=[jar(128,175,66,48,MINT)]; d=[sparkle(77,90)]
    elif i==8: m=[isobox(21,188,63,33,10,BLUE),isobox(91,145,71,76,10,LILAC),isobox(169,172,56,49,10,MINT)]; a=[can(52,182,24,56,LILAC),bottle(126,137,75,28,MINT),tube(195,164,60,28,BLUE)]; d=[l(24,236,229,236)]
    elif i==9: m=[c(128,100,74,'none',5),c(128,100,60,'none',3),l(65,46,65,20),l(191,46,191,20),cylinder(128,184,137,26,MINT)]; a=[carton(128,175,43,94,BLUE)]; d=[sparkle(51,113),sparkle(204,78)]
    elif i==10: m=[isobox(48,89,46,137,15,LILAC),isobox(152,136,47,90,15,BLUE),poly([(48,114),(214,114),(199,136),(48,136)],CREAM)]; a=[jar(128,107,55,37,MINT),bottle(177,129,71,27,LILAC)]; d=[l(56,221,207,221)]
    elif i==11: m=[p('M31 205 V69 Q84 28 132 72 Q181 115 225 54 V205 Z',BLUE),p('M31 205 V114 Q84 73 132 117 Q181 160 225 99 V205 Z',MINT),cylinder(128,192,117,24,LILAC)]; a=[tube(128,185,91,42,CREAM)]; d=[sparkle(71,74)]
    elif i==12: m=[poly([(47,87),(93,41),(209,41),(209,173),(164,221),(47,221)],CREAM),p('M47 87 H164 V221 M164 87 L209 41',sw=4),poly([(47,221),(93,173),(209,173),(164,221)],BLUE)]; a=[bottle(117,205,92,35,LILAC)]; d=[leaf(67,203,.55,-30)]
    elif i==13: m=[p('M26 171 H230 V213 H179 Q128 163 77 213 H26 Z',BLUE),poly([(26,171),(47,153),(230,153),(230,171)],CREAM)]; a=[bottle(91,146,89,34,MINT),jar(166,146,51,34,LILAC)]; d=[sparkle(204,105)]
    elif i==14: m=[p('M31 59 H225 V95 Q210 117 195 95 Q180 117 165 95 Q150 117 135 95 Q120 117 105 95 Q90 117 75 95 Q60 117 45 95 Q31 114 31 95 Z',LILAC),l(39,98,39,219,INK,4),l(217,98,217,219,INK,4),cylinder(128,186,131,27,BLUE)]; a=[jar(128,178,61,46,MINT)]; d=[p('M40 220 H217')]
    elif i==15: m=[poly([(36,173),(94,143),(178,146),(226,174),(212,221),(55,223)],BLUE),poly([(36,173),(94,143),(178,146),(226,174),(151,190)],CREAM),poly([(151,190),(226,174),(212,221),(140,236)],LILAC)]; a=[bottle(127,161,90,35,MINT)]; d=[sparkle(192,85)]
    elif i==16: m=[isobox(43,186,149,23,14,BLUE),isobox(59,157,130,22,13,LILAC),isobox(74,128,105,20,12,MINT)]; a=[jar(127,119,59,43,CREAM)]; d=[p('M57 196 H172 M72 167 H171 M86 137 H164',stroke=WHITE,sw=2)]
    elif i==17: m=[p('M40 219 V73 H216 V219',sw=4),r(40,182,176,35,BLUE,6),p('M40 158 H216 V182 H40 Z',CREAM,3)]; a=[bottle(96,151,78,33,LILAC),bottle(166,151,98,37,MINT)]; d=[p('M49 145 H206',stroke=BLUE,sw=5),sparkle(200,40)]
    elif i==18: m=[cylinder(128,166,182,24,BLUE),cylinder(128,208,110,20,LILAC),p('M111 190 H145 V208 H111 Z',MINT)]; a=[jar(81,157,47,33,MINT),bottle(150,157,97,37,LILAC)]; d=[p('M49 203 Q61 222 84 228 M207 203 Q195 222 172 228',stroke=INK,sw=3)]
    elif i==19: m=[p('M31 220 V160 H75 V116 H119 V72 H163 V28 H224 V220 Z',BLUE),p('M65 220 V177 H108 V135 H150 V94 H196 V54 H224 V220 Z',LILAC)]; a=[tube(89,151,69,32,MINT),jar(176,87,43,30,CREAM)]; d=[l(37,231,228,231)]
    elif i==20: m=[p('M26 211 V93 C26 15 119 15 119 93 V211 Z',BLUE),p('M137 211 V109 C137 28 230 28 230 109 V211 Z',LILAC),r(36,179,73,19,CREAM,3),r(147,179,73,19,CREAM,3)]; a=[bottle(73,173,78,30,MINT),jar(184,173,51,39,BLUE)]; d=[sparkle(128,36)]
    elif i==21: m=[poly([(128,196),(29,71),(78,40),(128,29),(178,40),(227,71)],LILAC)]; a=[poly([(128,196),(29,71),(78,40)],BLUE),poly([(128,196),(78,40),(128,29)],MINT),poly([(128,196),(178,40),(227,71)],BLUE),cylinder(128,207,145,23,CREAM),jar(128,199,55,39,MINT)]; d=[l(128,196,128,29),l(128,196,178,40)]
    elif i==22: m=[p('M28 173 Q93 105 128 169 Q161 231 229 167 V209 Q162 241 128 198 Q93 142 28 210 Z',BLUE),cylinder(128,166,112,26,LILAC)]; a=[bottle(128,158,97,39,MINT)]; d=[sparkle(58,110),sparkle(204,69)]
    elif i==23: m=[r(28,30,200,181,CREAM,8),r(39,183,178,29,BLUE,3)]; a=[r(89,141,78,42,LILAC,4),bottle(129,134,85,35,MINT)]; d=[c(x,y,2,INK,1) for x in range(46,213,28) for y in range(48,175,25)]+[leaf(70,180,.56,-32)]
    else: m=[p('M25 171 C43 99 102 99 128 171 C154 243 213 243 231 171 L210 171 C190 211 158 211 139 171 C107 76 41 80 25 171 Z',BLUE),p('M25 171 H231 V208 H25 Z',LILAC)]; a=[bottle(74,160,90,37,MINT),jar(187,160,54,42,CREAM)]; d=[sparkle(154,81)]
    return fin(m,a,d)

def packaging(i):
    m=[]; a=[]; d=[]
    if i==0: m=[isobox(39,151,145,69,25,BLUE),poly([(39,151),(39,81),(184,55),(209,126),(184,151)],LILAC)]; a=[r(60,143,102,32,CREAM,4),jar(112,153,59,42,MINT)]; d=[ribbon(121,77,45)]
    elif i==1: m=[isobox(64,87,137,100,20,LILAC),isobox(23,151,135,70,20,BLUE)]; a=[r(42,162,96,27,CREAM,3),jar(89,164,54,42,MINT)]; d=[p('M63 202 H99',sw=4),sparkle(214,64)]
    elif i==2: m=[poly([(30,79),(131,51),(131,208),(30,227)],BLUE),poly([(131,51),(226,76),(226,229),(131,208)],LILAC),poly([(147,99),(211,114),(211,205),(147,189)],CREAM)]; a=[g(bottle(0,0,70,26,MINT),'translate(180 185) skewY(12)')]; d=[p('M43 114 L112 95 M43 134 L104 118')]
    elif i==3: m=[isobox(30,147,165,74,24,BLUE),poly([(30,147),(21,104),(71,73),(77,123)],CREAM),poly([(195,147),(219,123),(231,82),(176,104)],CREAM)]; a=[poly([(43,146),(64,130),(182,130),(181,183),(43,200)],MINT),bottle(113,166,77,32,LILAC)]; d=[p('M42 207 H181',sw=2)]
    elif i==4: m=[r(30,53,105,164,BLUE,4),r(48,66,69,130,CREAM,3),r(154,91,71,126,LILAC,4)]; a=[bottle(82,192,98,35,MINT),bottle(188,210,93,33,BLUE)]; d=[linecopy(171,104,38,2),sparkle(201,56)]
    elif i==5: m=[pouch(76,216,85,153,BLUE),pouch(177,208,81,124,MINT)]; a=[r(45,50,63,17,CREAM,3),r(148,72,61,17,LILAC,3)]; d=[p('M60 45 H93 M164 66 H195',sw=3),sparkle(211,43)]
    elif i==6: m=[p('M32 102 H225 V205 H32 Z',BLUE),p('M32 102 L77 39 H180 L225 102 Z',LILAC),p('M77 39 V71 H180 V39',CREAM)]; a=[r(82,116,91,54,CREAM,5)]; d=[handle(128,71,47),linecopy(102,138,51,2)]
    elif i==7: m=[p('M51 78 H199 L218 226 H32 Z',BLUE)]; a=[r(68,116,114,73,CREAM,8),r(31,209,188,17,LILAC,2)]; d=[handle(89,78,33),handle(166,78,33),linecopy(85,143,81,3)]
    elif i==8: m=[r(43,49,172,165,LILAC,5),p('M43 49 L76 23 H195 L215 49 Z',CREAM)]; a=[r(76,83,106,99,BLUE,16),bottle(128,171,80,33,MINT)]; d=[r(100,193,56,8,CREAM,4),sparkle(29,108)]
    elif i==9: m=[isobox(27,133,118,80,22,BLUE),isobox(156,78,54,135,20,LILAC)]; a=[pouch(84,144,71,70,MINT),ribbon(187,62,40)]; d=[linecopy(46,174,79,2)]
    elif i==10: m=[p('M37 103 H219 V201 H37 Z',BLUE),e(128,103,91,24,CREAM),e(128,201,91,24,LILAC)]; a=[e(128,54,84,23,LILAC),p('M44 54 V79 Q128 109 212 79 V54',LILAC),e(128,54,84,23,CREAM)]; d=[linecopy(93,146,72,3)]
    elif i==11: m=[p('M58 105 H198 L224 224 H32 Z',BLUE),p('M58 105 L82 58 H176 L198 105 Z',CREAM),r(107,40,42,18,LILAC,3)]; a=[r(79,140,98,48,CREAM,6)]; d=[p('M116 50 H140',sw=3),linecopy(94,160,68,2)]
    elif i==12: m=[isobox(28,133,145,84,24,LILAC),poly([(52,109),(79,71),(221,71),(197,109)],CREAM),poly([(28,133),(31,101),(62,89),(52,109)],BLUE)]; a=[jar(84,147,44,32,MINT),jar(142,147,44,32,BLUE)]; d=[p('M45 195 H154',sw=2),sparkle(179,40)]
    elif i==13: m=[p('M29 92 H228 V153 Q128 189 29 153 Z',BLUE),p('M39 158 H218 V224 H39 Z',LILAC)]; a=[r(50,173,150,25,CREAM,3),ribbon(128,86,62)]; d=[p('M116 161 V222 M140 161 V222',stroke=CREAM,sw=4)]
    elif i==14: m=[poly([(45,89),(91,28),(190,28),(219,89),(219,218),(45,218)],BLUE),poly([(45,89),(91,28),(91,89)],MINT),poly([(91,89),(190,28),(219,89)],CREAM)]; a=[r(69,117,126,60,CREAM,7)]; d=[handle(150,65,38),linecopy(91,140,85,3)]
    elif i==15: m=[r(33,49,106,170,CREAM,3),r(151,77,72,142,BLUE,3)]; a=[r(42,62,88,134,LILAC,2),tube(86,184,107,47,MINT),tube(187,207,99,42,CREAM)]; d=[p('M48 207 H121'),sparkle(199,44)]
    elif i==16: m=[poly([(30,141),(95,103),(224,141),(159,180)],CREAM),poly([(30,141),(159,180),(159,225),(30,185)],BLUE),poly([(159,180),(224,141),(224,186),(159,225)],LILAC)]; a=[poly([(97,135),(147,149),(180,133),(133,119)],MINT),poly([(54,154),(90,165),(116,151),(79,141)],PEACH)]; d=[p('M47 167 L141 196',sw=2),sparkle(199,75)]
    elif i==17: m=[r(35,89,92,130,BLUE,8),r(147,55,77,164,LILAC,8)]; a=[p('M35 109 Q80 140 127 109',CREAM),p('M147 75 Q187 106 224 75',CREAM),r(49,146,64,45,CREAM,5),r(159,121,53,61,MINT,5)]; d=[handle(81,89,37),handle(185,55,31)]
    elif i==18: m=[isobox(38,101,155,110,24,MINT),poly([(38,101),(62,77),(217,77),(193,101)],CREAM)]; a=[p('M78 91 H153 V201 H78 Z',LILAC),r(89,128,52,46,CREAM,6)]; d=[ribbon(116,85,57),linecopy(98,146,33,2)]
    elif i==19: m=[p('M39 74 H218 V214 H39 Z',LILAC),p('M39 74 L66 43 H193 L218 74 Z',CREAM)]; a=[r(65,103,126,82,BLUE,14),p('M67 166 L104 127 L134 156 L163 127 L190 167 V185 H67 Z',MINT)]; d=[r(79,197,99,7,CREAM,3),sparkle(30,36)]
    elif i==20: m=[r(26,93,203,125,BLUE,10),r(38,105,76,101,CREAM,7),r(130,105,87,101,LILAC,7)]; a=[can(75,191,41,72,MINT),jar(173,188,61,48,CREAM)]; d=[p('M26 93 L42 58 H214 L229 93 Z',CREAM),linecopy(73,75,107,1)]
    elif i==21: m=[p('M34 65 H222 V226 H34 Z',BLUE),p('M34 65 L64 28 H197 L222 65 Z',CREAM),r(77,52,102,20,LILAC,5)]; a=[r(76,111,103,65,CREAM,6)]; d=[linecopy(94,130,68,3),p('M47 203 H209',sw=2)]
    elif i==22: m=[p('M35 99 H222 L199 215 H57 Z',LILAC),p('M48 88 H210 L222 99 H35 Z',CREAM)]; a=[r(77,124,105,57,BLUE,6)]; d=[handle(128,88,83),linecopy(92,145,76,2)]
    elif i==23: m=[isobox(30,127,166,91,24,BLUE),poly([(30,127),(81,83),(227,83),(196,127)],CREAM)]; a=[r(97,144,60,48,CREAM,3),p('M73 105 H154 L163 92 H86 Z',PEACH)]; d=[linecopy(108,156,40,3),p('M196 127 L208 87'),sparkle(42,48)]
    else: m=[poly([(128,82),(218,133),(218,197),(128,230),(38,197),(38,133)],BLUE),poly([(128,82),(218,133),(128,181),(38,133)],CREAM)]; a=[poly([(128,29),(211,74),(211,101),(128,145),(45,101),(45,74)],LILAC),poly([(128,29),(211,74),(128,119),(45,74)],CREAM)]; d=[ribbon(128,72,47),p('M128 181 V230',sw=3)]
    return fin(m,a,d)

def props(i):
    m=[]; a=[]; d=[]
    if i==0: m=[cylinder(128,196,174,20,LILAC),bottle(90,185,99,37,BLUE),bottle(159,184,116,42,MINT)]; a=[r(149,54,20,15,CREAM,3),p('M159 53 V35',sw=4),leaf(206,183,.72,28)]; d=[sparkle(55,52),sparkle(204,80)]
    elif i==1: m=[r(28,176,202,48,CREAM,9),bottle(89,174,94,41,MINT,True),jar(170,173,69,45,LILAC)]; a=[p('M40 194 H92 V212 H40 Z',BLUE),p('M119 197 H214',stroke=LILAC,sw=5)]; d=[sparkle(182,58)]
    elif i==2: m=[e(88,182,61,33,LILAC),e(88,166,61,33,CREAM),p('M27 166 V155 Q87 129 149 155 V166',BLUE),e(86,95,50,57,BLUE),e(86,95,40,46,CREAM)]; a=[r(166,122,29,90,LILAC,4),p('M169 122 V79 L192 65 V122 Z',PINK),r(210,98,9,107,PEACH,3),p('M199 98 V68 Q214 46 230 68 V98 Z',MINT)]; d=[p('M50 89 Q72 62 102 66',stroke=WHITE,sw=4)]
    elif i==3: m=[p('M70 116 L100 86 H155 L185 116 V210 H70 Z',BLUE),p('M70 116 H185 M100 86 V116 M155 86 V116',sw=3),r(105,51,46,35,LILAC,5),r(91,39,73,13,CREAM,5)]; a=[r(95,139,65,47,CREAM,5),leaf(55,218,.95,-32),leaf(208,220,.8,33)]; d=[p('M164 44 H197 Q222 45 213 70',sw=3),e(213,80,13,16,PEACH),sparkle(57,65)]
    elif i==4: m=[cylinder(128,196,166,22,BLUE),tube(126,188,120,53,MINT)]; a=[c(63,155,27,PEACH),c(63,155,18,CREAM),c(198,175,22,PEACH),leaf(187,94,.85,45)]; d=[p('M63 138 V172 M46 155 H80 M51 143 L75 167 M51 167 L75 143',sw=2),sparkle(194,52)]
    elif i==5: m=[cylinder(127,202,186,19,MINT),jar(94,188,51,60,CREAM),jar(165,188,47,43,LILAC)]; a=[p('M91 119 Q78 107 94 86 Q109 107 97 119 Z',PEACH),p('M163 136 Q151 123 165 106 Q177 123 168 136 Z',PEACH),e(44,193,18,12,BLUE),e(207,196,22,11,BLUE)]; d=[l(94,128,94,119),l(165,146,165,136),leaf(205,154,.62,30)]
    elif i==6: m=[e(128,197,96,25,MINT),jar(117,183,93,65,BLUE)]; a=[p('M31 161 Q54 134 74 150 M196 144 Q217 123 229 139',stroke=BLUE,sw=5),p('M185 129 L211 84 Q217 72 225 80 Q231 87 218 93 L193 140 Z',CREAM),e(108,92,49,15,LILAC)]; d=[p('M82 98 L160 90',stroke=WHITE,sw=4),sparkle(43,90)]
    elif i==7: m=[cylinder(128,203,182,23,LILAC),r(45,143,35,53,BLUE,4),r(109,128,36,68,MINT,4),r(176,153,35,43,BLUE,4)]; a=[p('M49 143 V107 L75 91 V143 Z',PINK),p('M114 128 V69 L141 52 V128 Z',PEACH),r(176,104,35,47,CREAM,4)]; d=[r(47,152,31,6,CREAM,1),r(111,137,32,6,CREAM,1),sparkle(196,45)]
    elif i==8: m=[p('M75 148 Q75 111 107 111 H149 Q181 111 181 148 V208 H75 Z',BLUE),r(104,98,48,16,CREAM,3)]; a=[r(94,151,67,37,CREAM,5),p('M117 98 L88 34 M128 98 V24 M139 98 L171 32',stroke=PEACH,sw=5),p('M39 221 Q26 155 52 141 Q71 167 66 220 Z',LILAC),p('M196 221 Q185 176 207 156 Q230 179 222 221 Z',MINT)]; d=[leaf(65,114,.72,-31),sparkle(198,71)]
    elif i==9: m=[p('M26 169 H229 V221 H26 Z',LILAC),p('M38 151 H217 V169 H38 Z',CREAM),r(53,83,13,84,PEACH,5),r(101,59,13,108,PEACH,5),r(151,98,13,69,PEACH,5),r(198,83,13,84,PEACH,5)]; a=[p('M43 83 V56 Q60 33 77 56 V83 Z',BLUE),p('M91 59 V34 Q108 13 125 34 V59 Z',MINT),p('M141 98 V79 Q158 59 175 79 V98 Z',PINK),p('M188 83 V65 Q205 45 222 65 V83 Z',BLUE)]; d=[p('M61 190 H195',sw=4)]
    elif i==10: m=[r(27,91,202,129,BLUE,13),r(40,106,79,100,CREAM,8),r(136,106,79,45,LILAC,7),r(136,166,79,40,MINT,7)]; a=[c(63,134,12,PEACH),c(94,162,16,MINT),c(64,187,11,PINK),e(169,129,22,11,PEACH),c(158,186,11,CREAM),c(191,186,11,CREAM)]; d=[p('M37 78 H220',stroke=PEACH,sw=5),p('M37 65 H220',stroke=PEACH,sw=5)]
    elif i==11: m=[p('M61 90 H178 L164 218 H77 Z',BLUE),r(53,73,133,21,CREAM,5),p('M67 61 H172 L185 73 H54 Z',LILAC)]; a=[p('M66 130 H173 L170 179 H70 Z',CREAM),r(184,158,42,50,MINT,6)]; d=[e(38,209,14,9,PEACH),p('M29 210 Q38 201 47 209',sw=2),e(210,224,14,9,PEACH),p('M201 225 Q210 216 219 224',sw=2),p('M99 52 Q90 38 104 25 M131 52 Q122 38 136 25',stroke=BLUE,sw=3)]
    elif i==12: m=[p('M127 62 H211 L229 212 H109 Z',BLUE),p('M127 62 H211 L211 89 H127 Z',CREAM),e(94,200,71,22,CREAM)]; a=[p('M37 184 Q44 113 101 113 Q144 122 153 181 L125 175 Q117 143 102 146 Q76 132 63 177 Z',PEACH)]; d=[p('M57 164 L74 139 M78 172 L89 137 M105 142 L116 174 M124 135 L134 158',sw=2),r(150,113,56,47,CREAM,4)]
    elif i==13: m=[p('M36 144 H220 Q207 216 128 221 Q49 216 36 144 Z',BLUE),e(128,144,92,20,CREAM)]; a=[c(77,127,27,PEACH),c(128,112,34,PINK),c(181,130,28,MINT),c(117,151,22,PEACH)]; d=[p('M122 77 Q113 58 133 49',sw=3),leaf(156,84,.53,55),p('M62 118 Q69 104 82 107',sw=2),sparkle(209,62)]
    elif i==14: m=[cylinder(128,185,164,20,LILAC),r(116,205,25,16,MINT,4),e(128,225,62,8,CREAM)]; a=[p('M69 167 V108 H164 L191 132 V167 Z',PEACH),poly([(69,108),(115,73),(191,132),(164,108)],CREAM),p('M69 130 H189 M69 150 H190',stroke=PINK,sw=8)]; d=[c(124,90,10,PINK),p('M124 80 Q126 67 138 67',sw=2)]
    elif i==15: m=[jar(109,207,98,112,PEACH),r(75,78,68,18,CREAM,5),r(60,109,98,11,LILAC,2)]; a=[r(72,146,74,40,CREAM,6),p('M165 170 L210 72',stroke=PEACH,sw=9),e(208,68,19,13,CREAM,3,transform='rotate(-32 208 68)'),p('M182 207 Q172 192 187 177 Q201 195 194 207 Z',PEACH)]; d=[p('M192 70 L218 58 M196 77 L223 65',sw=2),leaf(44,218,.72,-28)]
    elif i==16: m=[r(30,111,78,107,LILAC,5),e(69,111,39,10,CREAM),p('M126 150 H201 Q201 209 165 210 Q130 209 126 150 Z',BLUE),p('M201 159 Q233 147 230 181 Q227 199 203 193',sw=4),e(165,150,39,10,CREAM)]; a=[r(43,143,52,38,CREAM,4),leaf(189,116,.58,37),leaf(214,224,.49,58)]; d=[p('M149 128 Q139 112 150 98 M173 128 Q163 112 176 96',stroke=MINT,sw=3),linecopy(53,157,32,2)]
    elif i==17: m=[p('M31 137 H224 L207 221 H48 Z',BLUE),p('M29 126 H226 V140 H29 Z',CREAM)]; a=[leaf(62,134,1.33,-22),leaf(95,135,1.7,-5),leaf(140,133,1.76,9),leaf(191,133,1.39,27),c(67,160,18,PEACH),c(187,163,17,PINK)]; d=[p('M55 157 L196 205 M49 180 L198 157 M49 204 L216 174 M83 142 V219 M128 142 V219 M173 142 V219',stroke=CREAM,sw=3)]
    elif i==18: m=[pouch(74,221,93,155,LILAC),r(145,103,74,112,BLUE,8),p('M218 117 Q239 115 237 152 Q235 176 219 169',sw=4),r(141,85,83,16,CREAM,5)]; a=[r(78,52,9,14,CREAM,2),r(173,47,10,39,PEACH,2),e(178,43,22,7,CREAM),p('M152 150 H211 V195 H152 Z',PEACH)]; d=[e(123,223,13,8,PEACH),p('M113 224 Q124 217 133 222',sw=2),linecopy(47,122,57,3)]
    elif i==19: m=[p('M51 134 H206 L180 184 H77 Z',BLUE),r(119,184,20,34,LILAC,4),e(129,222,61,8,CREAM)]; a=[c(94,111,31,PEACH),c(160,106,32,PINK),c(128,70,30,CREAM),p('M182 105 L207 57 L221 64 L196 119 Z',MINT)]; d=[c(128,32,9,PINK),p('M127 23 Q125 16 140 17',sw=2),p('M80 104 H91 M145 96 H156 M119 67 H130',sw=2)]
    elif i==20: m=[p('M25 155 H157 Q145 218 92 222 Q38 218 25 155 Z',BLUE),e(91,155,66,15,CREAM),carton(192,219,62,130,MINT)]; a=[e(57,145,9,6,PEACH),e(82,154,11,7,PEACH),e(104,140,10,6,PEACH),e(124,156,9,5,PEACH),p('M161 128 L140 137 L134 176',stroke=CREAM,sw=7)]; d=[c(92,151,3,PINK),c(115,151,3,PINK),c(69,138,3,PINK)]
    elif i==21: m=[e(128,169,105,54,CREAM),e(128,169,82,39,BLUE)]; a=[p('M68 174 Q89 141 132 157 Q175 171 189 149 M72 187 Q101 160 145 181 Q169 191 187 179 M91 147 Q133 132 174 148',stroke=PEACH,sw=8),p('M35 37 V105 Q35 117 44 117 Q53 117 53 105 V37 M44 37 V103 M44 117 V210',sw=4),p('M214 38 Q197 71 211 111 H222 V210 M222 38 V111',sw=4)]; d=[leaf(145,156,.43,50),c(110,180,5,PINK),c(167,163,5,PINK)]
    elif i==22: m=[can(119,216,75,151,BLUE),poly([(40,172),(62,158),(80,183),(70,212),(42,204)],CREAM),poly([(181,178),(209,163),(227,191),(214,218),(187,217)],CREAM)]; a=[c(194,120,29,PEACH),c(194,120,20,CREAM),leaf(194,78,.71,54)]; d=[p('M194 101 V139 M175 120 H213 M180 106 L208 134 M180 134 L208 106',sw=2),c(41,108,6,BLUE),c(61,139,4,MINT),sparkle(211,39)]
    elif i==23: m=[e(128,203,105,19,CREAM),p('M38 187 V143 A90 90 0 0 1 218 143 V187 Z',BLUE),r(31,184,193,16,LILAC,6),r(116,44,24,14,CREAM,6)]; a=[p('M65 159 Q70 132 103 133 Q114 95 140 126 Q178 121 192 158 Z',MINT)]; d=[p('M65 89 Q97 56 132 70',stroke=WHITE,sw=5),sparkle(219,71)]
    else: m=[r(24,175,207,50,CREAM,7),p('M56 170 H196 V181 H56 Z',LILAC),p('M57 105 Q58 52 128 52 Q196 52 197 105 Z',PEACH),r(57,128,140,21,PEACH,6)]; a=[p('M54 108 H201 L180 129 L150 112 L116 129 L82 113 L58 125 Z',MINT),p('M57 153 H198 L190 170 H65 Z',MINT),p('M72 124 H183 L173 137 H82 Z',PINK)]; d=[p('M91 81 L96 77 M125 70 L130 66 M159 81 L164 77',stroke=CREAM,sw=3),r(203,127,18,47,BLUE,5)]
    return fin(m,a,d)

def retail(i):
    m=[]; a=[]; d=[]
    if i==0: m=[r(31,139,195,80,BLUE,8),r(45,76,166,62,CREAM,0),p('M31 76 L50 40 H207 L226 76 V93 H31 Z',LILAC)]; a=[p('M70 40 L61 93 M108 40 L106 93 M146 40 L150 93 M185 40 L196 93',stroke=CREAM,sw=13),jar(89,135,40,31,MINT),bottle(162,135,62,28,BLUE)]; d=[r(59,161,139,34,CREAM,5),linecopy(80,174,96,2)]
    elif i==1: m=[r(26,48,204,171,CREAM,5),r(38,72,53,128,BLUE,1),r(102,72,53,128,LILAC,1),r(166,72,53,128,MINT,1)]; a=[r(43,178,44,16,CREAM,1),r(107,160,44,34,CREAM,1),r(171,143,44,51,CREAM,1),jar(65,173,31,24,MINT),bottle(129,155,55,25,BLUE),tube(193,137,50,25,LILAC)]; d=[r(66,33,124,18,BLUE,4)]
    elif i==2: m=[r(43,162,172,64,BLUE,5),r(79,51,111,89,LILAC,9),r(89,61,91,68,CREAM,5),r(125,140,19,22,MINT,2)]; a=[r(60,125,44,36,MINT,5),r(168,144,32,19,CREAM,4)]; d=[r(68,185,55,20,CREAM,3),p('M83 86 H164 M83 109 H150',sw=3),sparkle(220,88)]
    elif i==3: m=[r(29,30,198,192,CREAM,8),r(41,84,174,10,BLUE,1),r(41,148,174,10,BLUE,1),r(41,211,174,10,BLUE,1)]; a=[bottle(70,81,43,21,MINT),tube(121,81,42,22,LILAC),jar(173,81,35,24,BLUE),jar(72,145,41,32,LILAC),bottle(129,145,44,22,BLUE),tube(180,145,43,23,MINT),pouch(76,208,42,41,MINT),jar(143,207,40,25,BLUE),jar(188,207,33,25,LILAC)]; d=[r(94,21,68,17,LILAC,3)]
    elif i==4: m=[r(43,26,170,202,BLUE,10),r(58,57,140,151,CREAM,3)]; a=[r(65,74,56,54,MINT,3),r(136,74,55,54,LILAC,3),r(65,141,56,56,LILAC,3),r(136,141,55,56,MINT,3)]; d=[can(85,120,18,36,BLUE),can(151,121,18,36,BLUE),can(90,190,18,36,BLUE),can(162,190,18,36,BLUE),l(129,57,129,208),r(93,37,70,9,CREAM,4)]
    elif i==5: m=[p('M31 227 V60 Q31 36 55 36 H202 Q226 36 226 60 V227',sw=5),p('M22 227 H48 M209 227 H236',sw=5)]; a=[p('M66 79 L91 62 L115 80 H139 M66 79 H139',sw=3),p('M152 79 L174 62 L198 80 H219 M152 79 H219',sw=3),p('M65 80 L52 109 L68 123 V190 H119 V123 L134 108 L120 80 Z',BLUE),p('M156 80 L147 108 L163 124 V197 H201 V124 L216 108 L202 80 Z',LILAC)]; d=[r(77,144,30,17,CREAM,4),sparkle(45,99)]
    elif i==6: m=[cylinder(128,194,180,29,BLUE),p('M70 140 H188 L199 186 H59 Z',LILAC)]; a=[handle(128,139,59),r(81,159,96,17,CREAM,5),p('M52 42 H204 V103 H52 Z',CREAM),p('M52 42 L128 80 L204 42',BLUE)]; d=[sparkle(47,121),sparkle(212,133)]
    elif i==7: m=[r(25,143,207,82,LILAC,7),p('M25 143 V93 L61 65 H231 V143 Z',BLUE),p('M61 65 V113 H231 M25 143 L61 113',sw=3)]; a=[e(81,134,29,9,CREAM),e(157,134,30,9,CREAM),p('M59 122 Q77 83 99 122 Z',PEACH),p('M137 123 Q151 94 176 123 Z',PINK)]; d=[r(43,165,75,31,CREAM,5),r(136,165,76,31,CREAM,5)]
    elif i==8: m=[r(31,192,194,35,BLUE,6),r(55,148,146,14,CREAM,2),r(80,103,97,14,CREAM,2)]; a=[can(66,188,27,57,LILAC),can(127,188,27,57,MINT),can(190,188,27,57,LILAC),can(97,144,26,54,BLUE),can(158,144,26,54,BLUE),can(127,100,25,53,MINT)]; d=[r(76,208,103,9,CREAM,4)]
    elif i==9: m=[p('M27 85 L77 32 H180 L229 85 Z',BLUE),p('M41 85 V228 M215 85 V228',sw=5),r(52,160,151,68,LILAC,5)]; a=[p('M81 85 V128 H178 V85',CREAM),bottle(102,156,58,25,MINT),jar(162,156,38,25,BLUE)]; d=[r(93,58,72,14,CREAM,4),linecopy(81,187,93,3)]
    elif i==10: m=[e(128,163,102,28,CREAM),p('M26 163 V212 Q128 256 230 212 V163 Z',BLUE),e(128,77,68,18,LILAC),p('M61 77 V150 M195 77 V150',sw=4)]; a=[jar(77,160,43,32,MINT),bottle(135,151,76,31,LILAC),tube(181,156,55,26,BLUE)]; d=[p('M105 194 H150',stroke=CREAM,sw=5)]
    elif i==11: m=[r(51,24,154,208,BLUE,10),r(67,44,90,128,CREAM,3),r(168,45,22,87,LILAC,3),r(76,190,106,22,INK,4)]; a=[can(88,101,22,45,MINT),can(134,101,22,45,LILAC),pouch(92,156,26,41,BLUE),pouch(136,156,27,41,MINT)]; d=[r(174,59,10,13,CREAM,2),r(174,83,10,13,CREAM,2),r(174,106,10,13,CREAM,2),p('M67 107 H157',sw=2)]
    elif i==12: m=[r(25,152,205,62,BLUE,6),r(28,139,199,16,LILAC,3),r(39,205,20,25,MINT,4),r(196,205,20,25,MINT,4)]; a=[p('M60 77 H142 L151 136 H51 Z',CREAM),handle(101,77,36),r(169,84,49,44,BLUE,6),r(191,127,8,13,LILAC,1)]; d=[p('M29 165 H228',sw=2),r(89,173,92,19,CREAM,3),linecopy(179,102,28,2)]
    elif i==13: m=[r(29,103,187,101,BLUE,6),r(22,91,209,17,CREAM,4),p('M33 90 V45 H211 V90',sw=4)]; a=[r(71,55,101,21,LILAC,4),bottle(78,90,43,20,MINT),jar(159,90,35,24,BLUE)]; d=[c(62,219,15,LILAC),c(191,219,15,LILAC),c(62,219,5,CREAM),c(191,219,5,CREAM),r(57,128,132,47,CREAM,5)]
    elif i==14: m=[p('M51 35 H205 V225 H51 Z',BLUE),p('M29 225 L51 181 H205 L227 225 Z',LILAC),r(40,105,171,14,CREAM,2),r(40,171,171,14,CREAM,2)]; a=[r(66,57,33,46,MINT,2),r(113,52,34,51,LILAC,2),r(160,58,32,45,CREAM,2),r(68,130,42,39,CREAM,2),r(128,126,58,43,MINT,2)]; d=[p('M77 68 H89 M124 64 H137 M170 70 H182 M78 140 H99 M140 139 H174',sw=2)]
    elif i==15: m=[p('M83 49 H173 V207 H83 Z',BLUE),p('M173 49 L201 68 V224 L173 207',LILAC),cylinder(128,210,172,19,CREAM),p('M83 49 L111 29 H201 V68 L173 49 Z',CREAM)]; a=[jar(108,99,37,23,MINT),jar(145,153,37,23,LILAC),tube(185,140,42,17,MINT)]; d=[p('M91 107 H163 M91 166 H163',sw=3),r(108,187,40,8,CREAM,3)]
    elif i==16: m=[p('M25 163 H114 L98 223 H42 Z',BLUE),p('M134 139 H225 L209 223 H150 Z',LILAC)]; a=[leaf(61,165,1.16,-25),leaf(83,161,1.55,13),leaf(173,141,1.6,-13),leaf(200,144,1.38,24)]; d=[c(49,98,13,PINK),c(82,80,14,CREAM),c(172,55,13,PINK),c(214,83,14,CREAM),r(56,189,31,17,CREAM,4),r(161,176,35,22,CREAM,4)]
    elif i==17: m=[r(25,33,206,195,CREAM,4),r(40,99,177,12,BLUE,2),r(40,163,177,12,BLUE,2),r(40,217,177,10,BLUE,2)]; a=[jar(76,95,44,30,LILAC),p('M140 51 H173 V94 H140 Z',MINT),p('M173 59 Q198 54 197 76 Q194 91 173 86',sw=3),r(60,123,54,37,BLUE,5),e(153,146,28,12,CREAM),r(174,194,33,22,MINT,4),jar(90,213,48,27,LILAC)]; d=[p('M128 33 V227',sw=2)]
    elif i==18: m=[isobox(28,180,92,42,14,BLUE),isobox(125,180,88,42,14,LILAC),isobox(76,126,92,41,14,MINT)]; a=[c(61,173,14,PEACH),c(90,176,12,PINK),leaf(161,164,.79,31),c(97,119,12,PEACH),c(125,121,14,PEACH),c(151,120,11,PINK)]; d=[p('M38 192 H107 M136 192 H199 M88 138 H155',stroke=CREAM,sw=5)]
    elif i==19: m=[p('M29 226 V93 C29 11 227 11 227 93 V226 Z',BLUE),p('M48 226 V99 C48 35 208 35 208 99 V226 Z',CREAM),r(63,165,130,61,LILAC,7)]; a=[bottle(105,161,64,28,MINT),jar(158,161,39,29,BLUE)]; d=[r(94,67,69,17,LILAC,4),r(91,185,74,21,CREAM,4)]
    elif i==20: m=[poly([(28,76),(127,39),(227,76),(227,222),(28,222)],CREAM),p('M127 39 V222',sw=3),r(40,162,173,60,BLUE,4)]; a=[poly([(40,134),(120,107),(120,158),(40,184)],LILAC),poly([(137,107),(213,134),(213,184),(137,158)],MINT),bottle(83,143,63,28,MINT),jar(175,143,43,31,LILAC)]; d=[p('M42 70 L110 48 M145 48 L213 70',sw=4),r(78,192,99,14,CREAM,4)]
    elif i==21: m=[r(37,28,182,184,CREAM,5),r(37,212,182,14,BLUE,3)]; a=[r(62,87,42,46,BLUE,5),r(151,122,43,47,LILAC,5),handle(83,87,22),handle(172,122,23),r(57,181,52,25,MINT,4)]; d=[p('M64 41 V201 M95 41 V201 M126 41 V201 M157 41 V201 M188 41 V201 M47 61 H208 M47 93 H208 M47 125 H208 M47 157 H208 M47 189 H208',stroke=BLUE,sw=2)]
    elif i==22: m=[r(26,49,204,176,CREAM,6),r(39,94,179,11,BLUE,1),r(40,208,177,16,BLUE,2)]; a=[p('M61 110 H110 L117 176 H54 Z',LILAC),handle(86,110,25),p('M145 111 H195 L203 177 H137 Z',MINT),handle(170,111,25)]; d=[r(86,65,83,14,LILAC,4),r(63,192,42,10,CREAM,3),r(148,192,42,10,CREAM,3)]
    elif i==23: m=[p('M28 101 L56 66 H230 V176 L202 211 H28 Z',BLUE),p('M28 101 H202 V211 M202 101 L230 66 M28 161 H202 L230 129',sw=3),r(43,211,16,20,LILAC,3),r(186,211,16,20,LILAC,3)]; a=[poly([(91,102),(128,77),(162,102),(128,127)],CREAM),poly([(59,144),(82,121),(105,144),(82,156)],MINT),poly([(139,144),(162,121),(185,144),(162,156)],LILAC)]; d=[sparkle(38,50),sparkle(205,46)]
    else: m=[r(29,83,199,143,BLUE,4),p('M24 83 L52 44 H205 L233 83 Z',LILAC),r(45,111,62,93,CREAM,1),r(125,111,85,93,CREAM,1)]; a=[r(60,131,32,24,MINT,3),p('M125 111 H210 V140 H125 Z',LILAC),bottle(153,193,43,19,MINT),jar(185,194,32,25,BLUE)]; d=[r(79,53,98,19,CREAM,5),r(50,211,49,10,LILAC,3),l(115,96,115,225)]
    return fin(m,a,d)

SPEC=[
 ('Product display stages',stages,'Halo cylinder hero|Twin product stairs|Arch alcove pedestal|Floating shelf hero|Sloped runway stage|Folded paper corner set|Circular mirror platform|Triangular canopy stage|Three tier podium lineup|Suspended ring stage|Monolith shelf display|Wave backdrop plinth|Open cube product stage|Bridge platform hero|Scallop awning pedestal|Facet stone podium|Stacked booklet plinth|Transparent rail display|Carousel disc stage|Staircase showroom|Double niche shelf|Origami fan stage|Ribbon podium stage|Wall peg product stage|Infinity bridge stage', ['product hero reveal','premium product explainer','catalogue showcase']),
 ('Packaging and unboxing assemblies',packaging,'Hinged gift box assembly|Sliding drawer unboxing|Book style package opening|Shipping carton insert reveal|Bottle insert presentation|Sealed pouch pair|Gable gift carton|Paper carry bag display|Window carton reveal|Mixed packaging gift bundle|Round hatbox unboxing|Handled pouch package|Twin jar carton insert|Lift off ribbon gift box|Handled top carton|Tube sleeve unboxing|Divided gift insert tray|Twin shopping bag assembly|Ribbon wrapped delivery box|Window bakery package|Product sampler compartment|Flat top carry carton|Handled hamper assembly|Dispatch carton label|Hexagonal gift box reveal', ['unboxing sequence','packaging demonstration','digital commerce product scene']),
 ('Beauty and food promotion props',props,'Serum and dropper tray|Skincare pump and jar tray|Compact lipstick and brush setup|Crystal perfume atomizer|Citrus cosmetic tube stage|Spa candle and pebble tray|Cream jar and spatula splash|Lipstick trio on podium|Reed diffuser with vases|Makeup brush storage roll|Bento meal promotion tray|Coffee cup and bean setup|Pastry with bakery bag|Fresh fruit bowl arrangement|Layered cake on stand|Honey jar and dipper|Tea tin and cup arrangement|Herb produce basket|Coffee bag and French press|Ice cream sundae pedestal|Cereal bowl with milk carton|Pasta plate with cutlery|Chilled citrus beverage can|Glass cloche food display|Burger meal on serving tray', ['beauty product promotion','food product promotion','social commerce hero scene']),
 ('Retail showcase structures',retail,'Awning product counter|Three bay boutique window|Checkout terminal display|Beauty shelf wall|Glass beverage refrigerator|Apparel hanging rail|Handbag podium display|Bakery glass showcase|Stacked beverage tower|Popup promotion tent|Circular retail kiosk|Product vending machine|Checkout belt and shopping bag|Mobile retail cart|Book merchandising rack|Rotating cosmetics tower|Florist bucket stand|Houseware shelf display|Market produce crate stack|Arch storefront kiosk|Corner exhibition booth|Retail peg grid wall|Hanging bag showroom|Jewellery showcase cabinet|Small retail street facade', ['retail explainer','shop promotion scene','product catalogue environment']),
]

MOTION_GUIDES={
 'Product display stages':[
  ('Scale the halo gently from its centre; raise the hero bottle onto the podium.','Drift sparkle details at 2–3 pixels; keep the product still.','Push into the product label for a match cut.'),
  ('Reveal each riser from the lowest step; follow with its product silhouette.','Parallax the far pedestal more slowly than the near pedestal.','Lower the products first, then retract the steps.'),
  ('Draw the arch outline, fill the alcove, then rise the product.','Move the backdrop by 2 pixels opposite the foreground.','Close the alcove with a soft iris transition.'),
  ('Extend the floating shelf horizontally before placing the two products.','Use a slow camera slide along the shelf.','Slide the shelf and products beyond the right edge.'),
  ('Wipe the runway along its diagonal, then reveal products in depth order.','Use a small diagonal camera glide following the ramp.','Whip along the runway into the next scene.')
 ],
 'Packaging and unboxing assemblies':[
  ('Reveal the package base; rotate the lid open around its hinge; reveal the insert.','Hold the open package with a small 2.5D camera orbit.','Close the lid before fading the package.'),
  ('Reveal the outer sleeve, slide out the drawer, then reveal the product insert.','Use subtle opposing parallax between sleeve and drawer.','Push the drawer back into its sleeve.'),
  ('Rotate the book style panel open around its vertical hinge.','Keep package panels still; shimmer only small detail accents.','Fold the panel closed with eased perspective.'),
  ('Open carton flaps in sequence and raise the contained product.','Let the insert rise 2 pixels, then settle.','Lower the product and fold the carton flaps closed.'),
  ('Reveal the pack shell, then separate the product and its insert.','Float the detached product slowly above the insert.','Match cut from the product silhouette to a close-up.')
 ],
 'Beauty and food promotion props':[
  ('Raise the tray first; stagger the products and botanical accents.','Move botanical details softly; keep product labels readable.','Fade the props while pushing into the hero product.'),
  ('Use a gentle slide-up for the larger product and a scale reveal for the smaller prop.','Use a slow 2.5D push-in with a small side drift.','Slide the foreground down as the next background appears.'),
  ('Reveal the main vessel, then lift its accessory or lid into place.','Add a subtle hover only to detached accessories.','Close or lower the accessory before fading the scene.'),
  ('Sweep light across the main vessel, then reveal decorative props.','Parallax the front props against the main vessel.','Cut through the central label or serving surface.'),
  ('Reveal the serving surface; stagger food or product components upward.','Use a very small breathing scale on the decorative accents.','Remove components in reverse order with a soft wipe.')
 ],
 'Retail showcase structures':[
  ('Build the counter from its base; reveal the canopy and product lineup.','Use a slow storefront camera push-in.','Wipe through the counter into the product close-up.'),
  ('Reveal each display bay in sequence, then raise the displayed products.','Parallax the near products against the rear wall.','Zoom into one bay for the next product scene.'),
  ('Raise the retail structure, unfold its display panel, then reveal the products.','Keep shelves stable while detail highlights drift gently.','Fold the display panel down before the structure fades.'),
  ('Reveal the shelf levels from bottom to top; stagger the inventory.','Move the camera vertically along the shelf wall.','Pan out through the upper shelf into the next shot.'),
  ('Reveal the cabinet body, then the glass and contained product silhouettes.','Use a subtle glass reflection sweep without obscuring products.','Zoom through the cabinet door into a hero product.')
 ]
}

def generate():
    OUT.mkdir(parents=True,exist_ok=True); items=[]; serial=1301
    for category,fn,names,uses in SPEC:
        names=names.split('|'); assert len(names)==25
        for local,title in enumerate(names):
            ident=f'SV{serial:04d}'; layers=fn(local)
            body=''.join(f'<g id="{name}">{"".join(v)}</g>' for name,v in zip(['main','accent','details'],layers))
            svg=f'<svg xmlns="{NS}" width="256" height="256" viewBox="0 0 256 256" role="img" aria-labelledby="title"><title id="title">{title}</title>{body}</svg>\n'
            ET.fromstring(svg); (OUT/f'{ident}.svg').write_text(svg)
            entrance,ambient,exit_motion=MOTION_GUIDES[category][local%5]
            items.append({'id':ident,'title':title,'category':category,'tags':['promotion','premium','pastel','product',category.lower(),*title.lower().split()], 'svg':f'svg/files/{ident}.svg','viewBox':'0 0 256 256','license':'Original generated SVG; reusable','layers':['main','accent','details'],'collection':'promotion','use_cases':uses,'suggested_motion':{'entrance':entrance,'ambient':ambient,'exit':exit_motion}})
            serial+=1
    assert len(items)==100 and serial==1401
    (ROOT/'svg_promo_stages_index.json').write_text(json.dumps(items,indent=2,ensure_ascii=False)+'\n')
    return items

def qa(items,folder):
    import cairosvg
    from PIL import Image,ImageDraw,ImageFont
    folder=Path(folder); folder.mkdir(parents=True,exist_ok=True); rows=[]
    for x in items:
        f=OUT/f'{x["id"]}.svg'; s=f.read_text(); node=ET.fromstring(s)
        assert not re.search(r'<script|<image|href=|onload=|onclick=|foreignObject',s,re.I),x['id']
        assert all(node.find(f'.//{{{NS}}}g[@id="{v}"]') is not None for v in x['layers'])
        out=folder/f'{x["id"]}.png'; cairosvg.svg2png(url=str(f),write_to=str(out),output_width=256,output_height=256)
        im=Image.open(out).convert('RGBA'); bounds=im.getchannel('A').getbbox(); assert bounds
        body=re.sub(r'<title[^>]*>.*?</title>','',s)
        rows.append({'id':x['id'],'bbox':list(bounds),'margin_pass':bounds[0]>=12 and bounds[1]>=12 and bounds[2]<=244 and bounds[3]<=244,'geometry_hash':hashlib.sha256(body.encode()).hexdigest()})
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
    for k,(category,*_) in enumerate(SPEC):
        sheet=Image.new('RGB',(900,950),'#edf1f6'); draw=ImageDraw.Draw(sheet)
        for n,x in enumerate(items[k*25:(k+1)*25]):
            xx=(n%5)*180; yy=(n//5)*190; im=Image.open(folder/f'{x["id"]}.png').convert('RGBA').resize((170,170),Image.Resampling.LANCZOS)
            sheet.paste(im,(xx+5,yy+2),im); draw.text((xx+59,yy+174),x['id'],font=font,fill=INK)
        sheet.save(folder/f'contact_sheet_{k+1}.jpg',quality=94)
    summary={'collection':'promotion stages','first':'SV1301','last':'SV1400','count':len(rows),'categories':4,'per_category':25,'xml_valid':len(rows),'raster_valid':len(rows),'unique_geometry':len(set(v['geometry_hash'] for v in rows)),'security_valid':len(rows),'named_layers_valid':len(rows),'margin_pass':sum(v['margin_pass'] for v in rows),'margin_fail':[v for v in rows if not v['margin_pass']],'qa_folder':str(folder),'items':rows}
    (ROOT/'svg_promo_stages_qa.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='items'},indent=2))
    return summary

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--qa',action='store_true'); ap.add_argument('--qa-dir',default='/workspace/scratch/52cf302c2e1c/assets1500_stages_qa'); args=ap.parse_args()
    items=generate(); print(f'Generated {len(items)} original promotion SVG assets SV1301–SV1400.')
    if args.qa: qa(items,args.qa_dir)
