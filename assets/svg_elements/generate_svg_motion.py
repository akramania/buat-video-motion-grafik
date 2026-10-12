#!/usr/bin/env python3
"""500 original, editable motion-design SVG components (SV0501–SV1000).

These are programmatically drawn original vector assets, not downloaded stock.
Each category contains twenty independently usable structures, not recolours.
Run with Python 3; output is relative to this script so it is reproducible.
"""
from pathlib import Path
import math, json, hashlib, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'files'
INK='#31445E'; BLUE='#BFDCF5'; LILAC='#D8CEF4'; MINT='#C8E8DB'
PEACH='#F4D2BB'; PINK='#F1C9DA'; CREAM='#FFF9ED'; WHITE='#FFFFFF'
COLORS=[BLUE,LILAC,MINT,PEACH,PINK,CREAM]

def attrs(**a): return ' '.join(f'{k.replace("_","-")}="{v}"' for k,v in a.items() if v is not None)
def tag(n,**a): return f'<{n} {attrs(**a)}/>'
def r(x,y,w,h,fill=BLUE,rx=12,stroke=INK,sw=3,**kw): return tag('rect',x=x,y=y,width=w,height=h,rx=rx,fill=fill,stroke=stroke,stroke_width=sw,**kw)
def c(x,y,rad,fill=BLUE,stroke=INK,sw=3,**kw): return tag('circle',cx=x,cy=y,r=rad,fill=fill,stroke=stroke,stroke_width=sw,**kw)
def e(x,y,rx,ry,fill=BLUE,stroke=INK,sw=3,**kw): return tag('ellipse',cx=x,cy=y,rx=rx,ry=ry,fill=fill,stroke=stroke,stroke_width=sw,**kw)
def p(d,fill='none',stroke=INK,sw=3,**kw): return tag('path',d=d,fill=fill,stroke=stroke,stroke_width=sw,stroke_linejoin='round',stroke_linecap='round',**kw)
def l(x1,y1,x2,y2,stroke=INK,sw=3,**kw): return tag('line',x1=x1,y1=y1,x2=x2,y2=y2,stroke=stroke,stroke_width=sw,stroke_linecap='round',**kw)
def poly(points,fill=BLUE,stroke=INK,sw=3,**kw): return tag('polygon',points=' '.join(f'{x:.2f},{y:.2f}' for x,y in points),fill=fill,stroke=stroke,stroke_width=sw,stroke_linejoin='round',**kw)
def txt(x,y,s,size=14,fill=INK,weight=600,**kw): return f'<text {attrs(x=x,y=y,font_family="sans-serif",font_size=size,fill=fill,font_weight=weight,text_anchor="middle",**kw)}>{s}</text>'
def g(body,transform=None): return f'<g{(" transform="+chr(34)+transform+chr(34)) if transform else ""}>{"".join(body) if isinstance(body,list) else body}</g>'
def points(n,cx=128,cy=128,rad=90,rot=-90): return [(cx+rad*math.cos(math.radians(rot+k*360/n)),cy+rad*math.sin(math.radians(rot+k*360/n))) for k in range(n)]
def star(n=5,cx=128,cy=128,ro=70,ri=35,rot=-90,fill=PEACH):
    return poly([(cx+(ro if k%2==0 else ri)*math.cos(math.radians(rot+k*180/n)),cy+(ro if k%2==0 else ri)*math.sin(math.radians(rot+k*180/n))) for k in range(2*n)],fill)
def arrow(x1,y1,x2,y2,col=INK,width=5,head=12):
    ang=math.atan2(y2-y1,x2-x1); a=ang+2.6; b=ang-2.6
    return l(x1,y1,x2,y2,col,width)+poly([(x2,y2),(x2+head*math.cos(a),y2+head*math.sin(a)),(x2+head*math.cos(b),y2+head*math.sin(b))],col,col,1)
def lines(x,y,width=96,n=3,gap=12,col=INK): return ''.join(l(x,y+k*gap,x+width-(k%2)*16,y+k*gap,col,3) for k in range(n))
def dotrow(x,y,n=3,gap=12,col=LILAC): return ''.join(c(x+k*gap,y,3,col,col,1) for k in range(n))
def person(cx=128,cy=120,scale=1): return g([c(0,-22,12,PEACH),p('M -25 28 Q -25 -2 0 -2 Q 25 -2 25 28 Z',BLUE)],f'translate({cx} {cy}) scale({scale})')
def tinycheck(x,y,s=12): return p(f'M{x-s*.5} {y} l{s*.35} {s*.35} l{s*.7} {-s*.75}',stroke=INK,sw=3)
def sparkle(x,y,s=10,fill=PEACH): return p(f'M{x} {y-s} Q{x+2} {y-2} {x+s} {y} Q{x+2} {y+2} {x} {y+s} Q{x-2} {y+2} {x-s} {y} Q{x-2} {y-2} {x} {y-s} Z',fill,INK,2)
def card(x=34,y=44,w=188,h=168,fill='url(#glass)',rx=18): return r(x,y,w,h,fill,rx)
def finish(m,a=None,d=None): return (m,a or [],d or [])

def frames(i):
    m=[]; a=[]; d=[]
    if i==0: m=[r(26,36,204,184,'none',26,INK,7),r(36,46,184,164,'none',20,BLUE,4)]
    elif i==1: m=[r(36,26,184,204,CREAM,0),r(48,38,160,156,BLUE,0)]; d=[l(80,210,176,210)]
    elif i==2: m=[c(128,128,95,'none',INK,8),c(128,128,82,'none',LILAC,4)]
    elif i==3: m=[e(128,128,82,104,'none',INK,8),e(128,128,70,92,'none',PEACH,4)]
    elif i==4: m=[p('M38 212 V113 C38 8 218 8 218 113 V212 Z',BLUE),p('M50 200 V113 C50 28 206 28 206 113 V200 Z','none',WHITE,5)]
    elif i==5: m=[poly(points(6,rad=104,rot=-30),'none',INK,8),poly(points(6,rad=89,rot=-30),'none',MINT,4)]
    elif i==6: m=[poly(points(4,rad=112,rot=-90),'none',INK,8),poly(points(4,rad=96,rot=-90),'none',PINK,4)]
    elif i==7: m=[r(20,62,216,132,'none',0,INK,6)]; a=[r(31,49,44,26,PEACH,3),r(181,181,44,26,LILAC,3)]
    elif i==8: m=[p('M22 68 L200 24 L234 194 L56 232 Z',CREAM),p('M38 79 L190 42 L216 181 L65 215 Z',BLUE)]; d=[l(76,219,167,198)]
    elif i==9: m=[p('M42 52 H214 V202 H42 Z','none',INK,7)]; a=[p('M26 36 H72 M26 36 V82 M230 220 H184 M230 220 V174','none',LILAC,10)]
    elif i==10: m=[r(34,36,188,184,CREAM,5),r(46,48,164,160,BLUE,5)]; a=[r(76,24,104,30,PEACH,4)]; d=[l(84,29,82,44,WHITE,2),l(107,28,105,44,WHITE,2),l(130,28,128,44,WHITE,2)]
    elif i==11: m=[p('M20 68 Q40 20 72 38 Q92 8 128 30 Q162 8 186 40 Q230 22 238 64 Q252 96 227 128 Q252 163 230 194 Q216 228 181 220 Q149 250 120 225 Q84 247 60 217 Q20 225 22 187 Q2 154 28 128 Q0 94 20 68 Z','none',INK,5)]
    elif i==12: m=[r(25,42,206,172,CREAM,0)]; a=[p('M25 42 H231 V78 H25 Z',LILAC)]; d=[r(41,91,174,108,BLUE,0),dotrow(45,60,3)]
    elif i==13: m=[r(28,48,200,160,'none',72,INK,8),r(40,60,176,136,'none',64,MINT,4)]
    elif i==14: m=[p('M34 50 H208 L224 66 V206 H48 L34 192 Z',CREAM),p('M48 64 H204 V192 H48 Z',BLUE)]; d=[p('M208 50 V66 H224',LILAC)]
    elif i==15: m=[r(31,38,194,182,'none',6,INK,7)]; a=[c(31,38,13,PEACH),c(225,38,13,LILAC),c(31,220,13,MINT),c(225,220,13,PINK)]
    elif i==16: m=[poly(points(8,rad=105,rot=-22.5),'none',INK,7),poly(points(8,rad=91,rot=-22.5),'none',BLUE,4)]
    elif i==17: m=[r(20,50,216,154,'none',2,INK,5)]; d=[p('M20 75 H236 M20 179 H236',stroke=INK,sw=3)]+[r(29+k*28,56,16,12,CREAM,2) for k in range(7)]+[r(29+k*28,184,16,12,CREAM,2) for k in range(7)]
    elif i==18: m=[p('M32 40 H224 V216 H32 Z','none',INK,4),p('M22 30 H65 M22 30 V73 M234 30 H191 M234 30 V73 M22 226 H65 M22 226 V183 M234 226 H191 M234 226 V183',stroke=BLUE,sw=8)]
    else: m=[r(28,28,200,200,CREAM,0)]; d=[r(42,42,77,77,BLUE,0),r(137,42,77,77,LILAC,0),r(42,137,77,77,MINT,0),r(137,137,77,77,PEACH,0)]
    if not a: a=[sparkle(222,31,7,PEACH)]
    return finish(m,a,d)

def masks(i):
    ds=['M30 78 Q25 25 85 34 Q128 5 166 37 Q220 23 225 78 Q252 130 214 172 Q198 230 143 219 Q90 249 54 211 Q3 188 29 135 Z',
        'M40 220 V108 C40 15 216 15 216 108 V220 Z','M128 24 L231 128 L128 232 L25 128 Z',
        'M33 73 L111 28 L203 48 L235 127 L203 213 L114 233 L26 178 Z','M20 83 Q20 43 60 43 H196 Q236 43 236 83 V173 Q236 213 196 213 H60 Q20 213 20 173 Z',
        'M32 32 H224 V168 L168 224 H32 Z','M40 32 H216 V224 H72 L40 192 Z',
        'M128 27 C175 5 232 41 228 88 C264 142 220 225 175 222 C116 260 38 216 40 163 C6 106 47 24 91 38 Z',
        'M25 83 Q52 11 128 41 Q204 11 231 83 Q231 132 128 222 Q25 132 25 83 Z',
        'M20 70 H72 V26 H184 V70 H236 V186 H184 V230 H72 V186 H20 Z',
        'M22 42 H234 V170 Q202 158 178 182 Q143 205 115 179 Q78 161 22 205 Z',
        'M26 104 Q26 32 128 32 Q230 32 230 104 V230 H26 Z',
        'M128 21 L222 73 V181 L128 235 L34 181 V73 Z',
        'M41 25 H215 V70 L191 94 V162 L215 186 V231 H41 V186 L65 162 V94 L41 70 Z',
        'M24 53 Q24 24 53 24 H203 Q232 24 232 53 V203 Q232 232 203 232 H53 Q24 232 24 203 Z',
        'M19 65 L213 29 L237 194 L44 231 Z',
        'M128 18 C163 18 147 50 176 50 C227 31 239 79 209 99 C246 136 216 178 183 169 C203 222 149 247 128 210 C100 250 52 211 69 175 C19 181 2 132 45 106 C9 69 54 28 81 48 C95 16 111 18 128 18 Z',
        'M24 70 Q24 30 64 30 H192 Q232 30 232 70 V150 Q232 220 162 220 H94 Q24 220 24 150 Z',
        'M34 34 H222 V126 H128 V222 H34 Z',
        'M20 43 H236 V108 H171 V151 H236 V216 H20 V151 H85 V108 H20 Z']
    m=[p(ds[i],BLUE,INK,4)]
    a=[p('M55 145 L96 101 L134 143 L161 116 L204 165 V191 H55 Z',MINT,INK,2)]
    d=[c(165,72,17,CREAM,INK,2)]
    if i in (2,12): a=[poly(points(3,cx=128,cy=151,rad=51),MINT)]; d=[c(128,82,15,CREAM)]
    if i in (6,18): a=[p('M56 172 L93 123 L116 155 V199 H56 Z',MINT)]; d=[c(94,76,15,CREAM)]
    if i==19: a=[l(47,78,210,78,WHITE,4),l(46,184,211,184,WHITE,4)]; d=[]
    return finish(m,a,d)

def callouts(i):
    ds=['M30 44 H226 V169 H110 L62 212 V169 H30 Z','M30 46 H224 V173 H182 L208 220 L130 173 H30 Z',
        'M40 30 H216 V192 H147 L128 231 L109 192 H40 Z','M36 52 H220 V186 H82 L36 227 Z',
        'M60 45 H221 V196 H60 V154 L22 125 L60 96 Z','M35 45 H190 V95 L235 125 L190 155 V196 H35 Z',
        'M26 48 Q26 27 47 27 H209 Q230 27 230 48 V170 Q230 192 209 192 H92 L43 232 L57 192 H47 Q26 192 26 170 Z',
        'M30 71 Q30 36 66 36 H191 Q226 36 226 71 V155 Q226 190 191 190 H141 L128 226 L115 190 H66 Q30 190 30 155 Z',
        'M45 48 L200 26 L227 168 L113 190 L64 232 L63 199 Z',
        'M30 35 H226 V166 H175 L177 218 L139 166 H30 Z',
        'M30 64 L58 36 H197 L226 64 V158 L197 186 H88 L51 223 V184 L30 158 Z',
        'M48 39 H220 V192 H72 L36 227 V67 Z',
        'M25 69 Q68 11 129 47 Q188 10 230 69 Q245 122 215 170 Q197 203 138 193 L72 225 L93 191 Q22 185 25 69 Z',
        'M33 38 H224 V183 H162 L128 226 L94 183 H33 Z',
        'M26 38 H230 V155 H186 V197 H88 L45 230 V197 H26 Z',
        'M31 47 H218 V174 L161 174 L126 232 L126 174 H31 Z',
        'M24 62 H222 V183 H179 L208 222 L125 183 H24 Z',
        'M57 33 H230 V205 H57 V163 L22 163 V77 H57 Z',
        'M37 40 H225 V192 H64 L26 226 V89 Z',
        'M30 32 H224 V158 H194 L180 218 L143 158 H30 Z']
    m=[p(ds[i],COLORS[i%6],INK,4)]
    a=[r(56,69,144,12,WHITE,6,WHITE,1),r(56,99,112,10,WHITE,5,WHITE,1)]
    d=[lines(58,137,106,2,13)]
    if i==9: a=[c(74,93,20,PEACH),person(74,95,.55)]; d=[lines(110,82,83,3,18)]
    if i==12: a=[c(53,218,7,LILAC),c(37,235,4,BLUE)]; d=[dotrow(98,115,3,30,INK)]
    if i==14: a=[r(27,162,161,32,MINT,2)]; d=[dotrow(73,96,4,28,INK)]
    if i==16: a=[p('M47 49 H222 V73 H47 Z',LILAC)]; d=[lines(55,110,140,3,20)]
    if i==17: a=[p('M22 77 H57 V163 H22 Z',PEACH)]; d=[lines(78,73,116,4,25)]
    if i==19: a=[star(5,78,89,23,10,fill=PEACH)]; d=[lines(112,74,80,3,18)]
    return finish(m,a,d)

def arrows(i):
    m=[]; a=[]; d=[]
    ds=['M27 101 H164 V62 L231 128 L164 194 V155 H27 Z',
        'M42 215 V116 Q42 68 91 68 H157 V32 L224 94 L157 156 V120 H98 V215 Z',
        'M38 211 V99 H144 V37 L215 99 L144 160 V131 H70 V211 Z',
        'M39 213 V100 Q39 38 103 38 H182 V15 L231 64 L182 113 V90 H108 Q91 90 91 110 V213 Z',
        'M40 211 V56 H100 V24 L163 88 L100 152 V120 H92 V211 Z',
        'M32 106 H121 V66 L219 127 L121 190 V150 H32 Z',
        'M30 101 H167 V64 L225 128 L167 193 V155 H30 Z',
        'M29 156 L161 79 L140 44 L230 47 L207 134 L188 101 L56 178 Z',
        'M32 125 L104 53 V91 H225 V159 H104 V198 Z',
        'M90 230 V106 H40 L128 24 L216 106 H166 V230 Z',
        'M32 83 H160 V39 L228 106 L160 173 V132 H79 V214 H32 Z',
        'M26 98 H164 V64 L231 128 L164 192 V156 H26 Z',
        'M33 88 L115 32 V68 H185 L227 128 L185 188 H115 V224 L33 168 L76 128 Z',
        'M37 151 L128 41 L219 151 H169 V218 H88 V151 Z',
        'M25 109 H151 V61 L231 128 L151 195 V148 H25 Z',
        'M34 94 H158 V49 L230 128 L158 207 V162 H34 Z',
        'M37 96 H170 V56 L225 112 L170 167 V129 H87 V205 H37 Z',
        'M33 213 V137 Q33 84 87 84 H160 V43 L225 108 L160 173 V132 H93 Q81 132 81 144 V213 Z',
        'M30 124 Q65 42 152 58 V26 L227 89 L152 152 V116 Q99 93 74 156 Z',
        'M28 144 Q91 68 166 97 V48 L231 126 L160 197 V147 Q95 125 55 177 Z']
    m=[p(ds[i],BLUE,INK,4)]
    if i==6: a=[p('M40 112 H163',stroke=WHITE,sw=8)]
    elif i==11: a=[p('M44 101 L71 156 M83 101 L110 156 M122 101 L149 156',stroke=LILAC,sw=8)]
    elif i==14: a=[l(34,122,135,122,WHITE,7),l(34,137,135,137,WHITE,7)]
    elif i==15: a=[r(40,100,18,55,LILAC,0),r(69,100,18,55,MINT,0),r(98,100,18,55,PEACH,0)]
    else: a=[c(53,225,4,PEACH,PEACH,1)]
    if i==12: d=[poly([(115,98),(175,98),(198,128),(175,158),(115,158)],LILAC)]
    if i==8: d=[arrow(150,179,202,179,INK,3,8)]
    return finish(m,a,d)

def routes(i):
    ds=['M35 206 C35 95 221 180 221 49','M30 193 L75 193 L75 77 L184 77 L184 35',
        'M25 173 C68 44 137 228 228 62','M30 210 L64 158 L122 167 L144 81 L222 42',
        'M31 46 C177 27 41 220 225 208','M32 204 H95 V132 H161 V66 H225',
        'M34 203 C31 63 223 59 221 203','M28 153 H83 L126 83 L172 153 H229',
        'M30 215 V129 H99 V54 H159 V129 H223','M26 202 C70 216 56 151 112 170 C180 184 135 83 222 44',
        'M31 55 H222 V104 H31 V153 H222 V202 H31','M28 128 H228 M128 128 V32 M128 128 V224',
        'M128 222 V170 L49 79 M128 170 L209 79 M128 128 V30','M27 128 H72 L97 58 H158 L183 198 H229',
        'M32 128 C32 26 224 26 224 128 C224 230 32 230 32 128','M35 205 L220 48 M35 48 L220 205',
        'M31 192 Q63 115 128 128 Q190 138 225 57','M24 217 L64 170 L29 124 L88 78 L128 120 L179 62 L229 103',
        'M37 207 Q128 255 219 207 Q128 159 37 207 M128 207 V35','M27 205 L57 173 L92 176 L127 100 L165 111 L194 53 L229 45']
    m=[p(ds[i],stroke=BLUE,sw=18),p(ds[i],stroke=INK,sw=3,stroke_dasharray='6 7')]
    marks=[(35,206),(221,49)]
    if i==11: marks=[(28,128),(228,128),(128,32),(128,224)]
    elif i==12: marks=[(128,222),(49,79),(209,79),(128,30)]
    elif i==14: marks=[(32,128),(128,53),(224,128),(128,204)]
    elif i==15: marks=[(35,205),(220,48),(35,48),(220,205)]
    elif i==18: marks=[(37,207),(219,207),(128,35)]
    else:
        endpoints=[(35,206,221,49),(30,193,184,35),(25,173,228,62),(30,210,222,42),(31,46,225,208),(32,204,225,66),(34,203,221,203),(28,153,229,153),(30,215,223,129),(26,202,222,44),(31,55,31,202),(28,128,228,128),(128,222,128,30),(27,128,229,198),(32,128,32,128),(35,205,220,48),(31,192,225,57),(24,217,229,103),(37,207,128,35),(27,205,229,45)]
        x1,y1,x2,y2=endpoints[i]; marks=[(x1,y1),(x2,y2)]
    a=[c(x,y,9,PEACH,INK,2) for x,y in marks]
    d=[c(x,y,3,WHITE,WHITE,1) for x,y in marks]
    if i in (3,5,7,8,19): d += [c(128,128,9,LILAC,INK,2)]
    return finish(m,a,d)

def markers(i):
    m=[]; a=[]; d=[]
    if i==0: m=[p('M128 230 C115 207 54 147 54 101 A74 74 0 1 1 202 101 C202 147 141 207 128 230 Z',BLUE)]; a=[c(128,99,32,CREAM)]; d=[c(128,99,12,LILAC)]
    elif i==1: m=[p('M128 220 L68 145 A78 78 0 1 1 188 145 Z',LILAC)]; a=[c(128,89,35,CREAM)]; d=[star(5,128,89,23,10,fill=PEACH)]
    elif i==2: m=[r(48,31,160,146,BLUE,16),p('M105 177 L128 224 L151 177 Z',BLUE)]; a=[c(128,95,35,CREAM)]; d=[tinycheck(128,95,31)]
    elif i==3: m=[p('M128 230 L35 120 L128 25 L221 120 Z',MINT)]; a=[c(128,120,37,CREAM)]; d=[c(128,120,13,BLUE)]
    elif i==4: m=[poly(points(6,cy=107,rad=89,rot=-30),LILAC),p('M102 184 L128 231 L154 184 Z',LILAC)]; a=[poly(points(6,cy=107,rad=46,rot=-30),CREAM)]; d=[txt(128,114,'A',25)]
    elif i==5: m=[p('M74 29 H182 L166 135 L128 225 L90 135 Z',PEACH)]; a=[c(128,76,25,CREAM)]; d=[c(128,76,6,INK)]
    elif i==6: m=[c(128,110,70,BLUE),p('M88 172 L128 230 L168 172 Z',BLUE)]; a=[c(128,110,52,CREAM)]; d=[person(128,117,1)]
    elif i==7: m=[p('M47 170 V64 H209 V170 H144 L128 223 L112 170 Z',BLUE)]; a=[r(64,80,128,50,CREAM,0)]; d=[p('M83 95 H171 M83 112 H149'),c(128,150,4,PEACH)]
    elif i==8: m=[p('M48 184 V74 Q48 35 88 35 H168 Q208 35 208 74 V184 L180 213 L128 189 L76 213 Z',MINT)]; a=[c(128,100,43,CREAM)]; d=[tinycheck(128,100,38)]
    elif i==9: m=[p('M128 233 C80 171 32 139 52 77 C75 7 181 7 204 77 C224 139 176 171 128 233 Z',PINK)]; a=[p('M128 62 C163 20 215 76 128 137 C41 76 93 20 128 62 Z',CREAM)]; d=[]
    elif i==10: m=[r(83,26,90,170,PEACH,12),p('M105 196 L128 231 L151 196 Z',PEACH)]; a=[c(128,63,18,PINK),c(128,111,18,CREAM),c(128,159,18,MINT)]; d=[]
    elif i==11: m=[p('M128 228 L63 147 L45 92 L83 36 H173 L211 92 L193 147 Z',BLUE)]; a=[poly([(83,89),(128,44),(173,89),(128,134)],CREAM)]; d=[c(128,89,8,LILAC)]
    elif i==12: m=[c(128,111,76,MINT),l(128,187,128,230,INK,5)]; a=[c(128,111,56,CREAM)]; d=[p('M128 71 V111 L158 130',sw=5)]
    elif i==13: m=[p('M60 31 H194 V180 H147 L128 232 L109 180 H60 Z',LILAC)]; a=[r(81,53,92,76,CREAM,10)]; d=[p('M99 91 L117 110 L154 71',sw=5),lines(88,149,77,1)]
    elif i==14: m=[p('M128 229 L92 179 A78 78 0 1 1 164 179 Z',PEACH)]; a=[c(128,106,54,CREAM)]; d=[p('M88 101 H168 M99 84 H159 M99 118 H159 M99 135 H151',sw=4)]
    elif i==15: m=[p('M36 74 L81 29 H175 L220 74 V154 L174 196 H148 L128 233 L108 196 H82 L36 154 Z',BLUE)]; a=[r(69,78,118,70,CREAM,6)]; d=[p('M84 97 H170 M84 113 H159 M84 129 H143')]
    elif i==16: m=[p('M67 39 H187 V174 L128 231 L67 174 Z',MINT)]; a=[p('M87 79 L128 54 L169 79 V132 L128 157 L87 132 Z',CREAM)]; d=[c(128,105,13,BLUE)]
    elif i==17: m=[c(128,114,86,'none',INK,5),c(128,114,68,'none',LILAC,10),p('M115 200 L128 231 L141 200 Z',PEACH)]; a=[c(128,114,26,BLUE)]; d=[l(128,16,128,46),l(30,114,60,114),l(196,114,226,114)]
    elif i==18: m=[p('M48 168 V71 L88 31 H200 V168 H153 L128 224 L103 168 Z',BLUE)]; a=[p('M48 71 H88 V31 Z',CREAM)]; d=[lines(75,100,108,3,21)]
    else: m=[p('M128 229 L74 174 A79 79 0 1 1 182 174 Z',LILAC)]; a=[c(128,110,50,CREAM)]; d=[p('M88 110 H168 M128 70 V150',sw=6),c(128,110,20,BLUE)]
    return finish(m,a,d)

def glasscards(i):
    m=[card()]; a=[]; d=[]
    if i==0: a=[person(75,102,.8)]; d=[lines(113,78,81,3,19),r(58,153,140,29,LILAC,14)]
    elif i==1: a=[r(51,68,154,60,BLUE,12)]; d=[p('M68 110 L93 83 L116 105 L154 73 L189 98'),lines(57,154,99,2)]
    elif i==2: a=[c(128,109,43,MINT)]; d=[tinycheck(128,109,45),lines(86,173,85,1)]
    elif i==3: a=[r(49,67,66,116,LILAC,10),r(131,67,75,51,BLUE,10),r(131,133,75,50,MINT,10)]; d=[lines(62,89,35,4,22)]
    elif i==4: a=[c(68,88,16,PEACH),c(68,128,16,MINT),c(68,168,16,LILAC)]; d=[lines(99,81,90,2,12),lines(99,121,90,2,12),lines(99,161,90,2,12)]
    elif i==5: a=[r(53,68,150,92,BLUE,6)]; d=[poly([(110,88),(110,140),(156,114)],CREAM),lines(65,186,111,1)]
    elif i==6: a=[c(86,117,41,LILAC),r(145,81,53,71,PEACH,12)]; d=[txt(86,127,'72',28),lines(63,182,126,1)]
    elif i==7: a=[r(52,75,153,92,BLUE,8),r(52,75,153,24,LILAC,8)]; d=[dotrow(65,87),p('M66 114 H190 M66 137 H163 M66 154 H179'),lines(78,190,95,1)]
    elif i==8: a=[r(53,79,97,24,MINT,12),r(99,116,104,24,LILAC,12),r(53,153,118,24,PEACH,12)]; d=[dotrow(70,91),dotrow(117,128),dotrow(70,165)]
    elif i==9: a=[r(55,73,147,108,CREAM,6)]; d=[l(77,97,182,97),l(77,127,160,127),l(77,158,184,158)]+[c(62,y,4,BLUE) for y in (97,127,158)]
    elif i==10: a=[r(51,77,154,84,BLUE,0),r(51,77,154,22,LILAC,0)]; d=[p('M69 119 H184 M69 142 H159'),r(88,179,78,18,MINT,9)]
    elif i==11: a=[c(128,108,44,PEACH)]; d=[star(5,128,108,27,13,fill=CREAM),r(62,172,132,20,LILAC,10)]
    elif i==12: a=[r(50,69,63,66,BLUE,12),r(131,69,74,66,MINT,12)]; d=[txt(81,111,'24',25),txt(168,111,'96',25),p('M60 171 L94 150 L132 180 L195 148',sw=4)]
    elif i==13: a=[r(51,83,104,43,LILAC,21),c(170,146,32,MINT)]; d=[lines(64,68,84,1),tinycheck(170,146,28),lines(60,171,83,2)]
    elif i==14: a=[r(51,69,153,53,BLUE,10),r(51,138,153,53,PEACH,10)]; d=[c(76,95,14,CREAM),c(76,164,14,CREAM),lines(104,86,81,2,15),lines(104,155,81,2,15)]
    elif i==15: a=[c(128,114,49,LILAC)]; d=[p('M106 94 L106 139 L147 116 Z',CREAM),lines(78,184,100,1)]
    elif i==16: a=[r(50,66,154,26,BLUE,13),r(50,106,75,75,MINT,12),r(138,106,66,75,PEACH,12)]; d=[lines(64,79,97,1),tinycheck(86,141,25),p('M157 135 L184 162 M184 135 L157 162')]
    elif i==17: a=[p('M53 183 V146 L90 121 L124 151 L158 94 L202 70 V183 Z',MINT)]; d=[p('M61 102 H137 M61 121 H108'),c(181,90,16,CREAM)]
    elif i==18: a=[r(49,71,74,123,BLUE,8),r(139,71,68,35,LILAC,8),r(139,122,68,72,MINT,8)]; d=[lines(61,88,49,4,20),dotrow(152,87),tinycheck(173,158,26)]
    else: a=[c(79,103,24,PEACH),c(127,103,24,MINT),c(175,103,24,LILAC)]; d=[person(79,110,.5),person(127,110,.5),person(175,110,.5),lines(75,160,105,2,20)]
    return finish(m,a,d)

def charts(i):
    m=[]; a=[]; d=[]
    if i==0: m=[l(35,211,229,211),l(35,211,35,35)]; a=[r(57,153,32,58,BLUE,2),r(111,99,32,112,LILAC,2),r(165,51,32,160,MINT,2)]
    elif i==1: m=[l(35,211,229,211),l(35,211,35,35)]; a=[p('M48 173 L87 121 L131 151 L170 72 L212 41',stroke=BLUE,sw=10)]; d=[c(x,y,7,CREAM) for x,y in [(48,173),(87,121),(131,151),(170,72),(212,41)]]
    elif i==2: m=[c(128,128,88,CREAM)]; a=[p('M128 128 V40 A88 88 0 0 1 210 159 Z',BLUE),p('M128 128 L210 159 A88 88 0 0 1 77 200 Z',LILAC)]; d=[p('M128 128 L77 200 A88 88 0 0 1 128 40 Z',MINT)]
    elif i==3: m=[c(128,128,83,'none',CREAM,26)]; a=[p('M128 45 A83 83 0 1 1 48 151',stroke=BLUE,sw=26)]; d=[txt(128,139,'68%',31)]
    elif i==4: m=[l(36,211,226,211)]; a=[p('M36 211 V174 L82 154 L122 92 L163 108 L213 47 V211 Z',BLUE)]; d=[p('M36 174 L82 154 L122 92 L163 108 L213 47',sw=4)]
    elif i==5: m=[r(34,53,188,146,CREAM,8)]; a=[r(49,71,113,23,BLUE,6),r(49,110,155,23,LILAC,6),r(49,149,77,23,MINT,6)]; d=[l(49,184,204,184)]
    elif i==6: m=[poly(points(6,rad=95),CREAM),poly(points(6,rad=61),'none',INK,1),poly(points(6,rad=30),'none',INK,1)]; a=[poly([(128,49),(190,94),(173,154),(128,200),(83,154),(76,98)],BLUE)]; d=[l(128,33,128,223),l(46,80,210,175),l(46,175,210,80)]
    elif i==7: m=[l(35,212,227,212),l(35,212,35,35)]; a=[r(54,171,28,41,BLUE,2),r(94,144,28,68,LILAC,2),r(134,112,28,100,MINT,2),r(174,66,28,146,PEACH,2)]; d=[p('M54 164 H82 V137 H122 V105 H162 V59 H202',sw=3)]
    elif i==8: m=[l(35,211,229,211),l(35,211,35,35)]; a=[c(72,173,14,BLUE),c(117,139,25,LILAC),c(179,79,38,MINT),c(194,165,12,PEACH)]
    elif i==9: m=[l(36,205,226,205),l(36,205,36,38)]; a=[c(68,178,8,BLUE),c(96,155,8,MINT),c(123,163,8,LILAC),c(157,100,8,PEACH),c(182,109,8,MINT),c(207,58,8,BLUE)]; d=[p('M54 191 L213 57',stroke=INK,sw=3,stroke_dasharray='6 7')]
    elif i==10: m=[l(33,204,226,204)]; a=[r(51,93,39,111,BLUE,0),r(51,151,39,53,LILAC,0),r(107,61,39,143,BLUE,0),r(107,127,39,77,LILAC,0),r(163,112,39,92,BLUE,0),r(163,169,39,35,LILAC,0)]
    elif i==11: m=[p('M40 184 A88 88 0 0 1 216 184',stroke=CREAM,sw=28)]; a=[p('M40 184 A88 88 0 0 1 172 107.79',stroke=MINT,sw=28)]; d=[p('M128 184 L169 125',sw=7),c(128,184,12,LILAC)]
    elif i==12: m=[p('M31 46 H225 L192 90 H64 Z',BLUE),p('M64 102 H192 L169 146 H87 Z',LILAC),p('M87 158 H169 L145 203 H111 Z',MINT)]; d=[lines(93,66,70,1),lines(109,124,38,1)]
    elif i==13: m=[l(29,203,229,203)]; a=[r(36,56,34,70,BLUE,2),r(81,91,34,35,MINT,2),r(126,91,34,83,PEACH,2),r(171,110,34,64,LILAC,2)]; d=[p('M70 91 H81 M115 126 H126 M160 110 H171',stroke=INK,sw=2,stroke_dasharray='3 3')]
    elif i==14: m=[l(128,34,128,224),l(31,196,227,196)]; a=[r(47,55,81,25,BLUE,2),r(128,55,41,25,LILAC,2),r(70,99,58,25,BLUE,2),r(128,99,80,25,LILAC,2),r(91,143,37,25,BLUE,2),r(128,143,49,25,LILAC,2)]
    elif i==15: m=[l(34,209,224,209),l(34,209,34,35)]; a=[p('M44 184 C82 201 96 45 131 66 C163 78 170 122 214 41',stroke=BLUE,sw=8),p('M44 193 C86 168 108 136 136 151 C172 169 191 138 214 130',stroke=PEACH,sw=8)]
    elif i==16: m=[l(35,210,228,210)]; a=[r(58,91,23,88,BLUE,2),r(108,60,23,66,LILAC,2),r(158,119,23,64,MINT,2)]; d=[p('M69 59 V91 M69 179 V207 M119 36 V60 M119 126 V164 M169 92 V119 M169 183 V220',sw=4)]
    elif i==17: m=[c(128,128,84,CREAM),c(128,128,56,BLUE),c(128,128,29,LILAC)]; a=[p('M128 128 V44 A84 84 0 0 1 200 171 Z',MINT),p('M128 128 L200 171 A84 84 0 0 1 56 171 Z',PEACH)]; d=[c(128,128,18,CREAM)]
    elif i==18: m=[r(26,26,204,204,CREAM,4)]; a=[r(38,38,108,108,BLUE,2),r(157,38,61,108,LILAC,2),r(38,157,66,61,MINT,2),r(115,157,103,61,PEACH,2)]
    else: m=[l(34,209,225,209),l(34,209,34,38)]; a=[r(46,129,23,80,BLUE,0),r(77,101,23,108,MINT,0),r(108,60,23,149,LILAC,0),r(139,77,23,132,PEACH,0),r(170,136,23,73,BLUE,0),r(201,165,18,44,MINT,0)]; d=[p('M46 118 Q125 14 218 154',sw=3)]
    return finish(m,a,d)

def matrices(i):
    m=[]; a=[]; d=[]
    if i==0: m=[r(29,29,198,198,CREAM,12)]; a=[r(41,41,78,78,BLUE,8),r(137,41,78,78,LILAC,8),r(41,137,78,78,MINT,8),r(137,137,78,78,PEACH,8)]; d=[txt(80,87,'1',24),txt(176,87,'2',24),txt(80,183,'3',24),txt(176,183,'4',24)]
    elif i==1: m=[r(29,40,198,176,CREAM,3)]; a=[r(29,40,198,35,BLUE,3)]; d=[p('M29 110 H227 M29 145 H227 M29 180 H227 M94 40 V216 M160 40 V216')]
    elif i==2: m=[r(28,28,200,200,CREAM,3)]; a=[r(28,28,66,66,BLUE,3),r(95,95,66,66,LILAC,3),r(162,162,66,66,MINT,3)]; d=[p('M28 94 H228 M28 161 H228 M94 28 V228 M161 28 V228')]
    elif i==3: m=[r(31,43,194,168,CREAM,8)]; a=[r(44,56,166,31,LILAC,4)]; d=[p('M87 56 V198 M148 56 V198 M44 103 H210 M44 134 H210 M44 166 H210')]+[tinycheck(x,y,15) for x,y in [(68,119),(119,151),(180,183)]]
    elif i==4: m=[r(31,31,194,194,CREAM,6)]; a=[poly([(31,31),(225,225),(31,225)],BLUE),poly([(31,31),(225,31),(225,225)],LILAC)]; d=[l(31,31,225,225,INK,4),c(81,170,15,MINT),c(174,83,15,PEACH)]
    elif i==5: m=[l(32,214,229,214),l(32,214,32,27)]; a=[r(45,37,75,75,BLUE,10),r(135,37,75,75,LILAC,10),r(45,128,75,75,MINT,10),r(135,128,75,75,PEACH,10)]; d=[arrow(24,218,24,23,INK,2,8),arrow(30,233,232,233,INK,2,8)]
    elif i==6: m=[r(31,31,194,194,CREAM,8)]; a=[c(68,70,15,BLUE),c(128,70,20,LILAC),c(189,70,11,MINT),c(68,128,22,MINT),c(128,128,11,PEACH),c(189,128,24,BLUE),c(68,188,11,LILAC),c(128,188,23,BLUE),c(189,188,18,PEACH)]
    elif i==7: m=[r(32,42,192,175,CREAM,8)]; a=[r(32,42,192,32,BLUE,8),r(32,86,48,131,LILAC,4)]; d=[p('M94 86 H211 M94 113 H211 M94 141 H211 M94 169 H211 M94 196 H211',sw=2)]
    elif i==8: m=[poly([(128,22),(226,80),(226,176),(128,234),(30,176),(30,80)],CREAM)]; a=[poly([(128,22),(128,128),(30,80)],BLUE),poly([(128,22),(226,80),(128,128)],LILAC),poly([(226,80),(226,176),(128,128)],MINT),poly([(226,176),(128,234),(128,128)],PEACH),poly([(128,234),(30,176),(128,128)],PINK),poly([(30,176),(30,80),(128,128)],BLUE)]
    elif i==9: m=[r(32,32,192,192,CREAM,4)]; a=[r(32,32,64,96,BLUE,3),r(112,32,112,32,LILAC,3),r(112,80,48,128,MINT,3),r(176,80,48,128,PEACH,3),r(32,144,64,80,PINK,3)]
    elif i==10: m=[r(30,30,196,196,CREAM,4)]; a=[c(79,79,30,BLUE),c(177,79,30,LILAC),c(79,177,30,MINT),c(177,177,30,PEACH)]; d=[l(128,30,128,226),l(30,128,226,128),tinycheck(79,79,24),p('M164 67 L190 93 M190 67 L164 93')]
    elif i==11: m=[r(28,33,200,190,CREAM,4)]; a=[r(28,33,55,190,BLUE,4),r(98,50,111,25,LILAC,4),r(98,94,76,25,MINT,4),r(98,138,99,25,PEACH,4),r(98,182,45,25,PINK,4)]; d=[p('M28 83 H83 M28 126 H83 M28 171 H83')]
    elif i==12: m=[r(27,43,202,170,CREAM,4)]; a=[r(27,43,202,43,BLUE,4),r(27,86,50,127,LILAC,3)]; d=[p('M77 129 H229 M77 170 H229 M127 43 V213 M178 43 V213'),txt(52,70,'A',16),txt(101,70,'B',16),txt(153,70,'C',16),txt(203,70,'D',16)]
    elif i==13: m=[r(30,30,196,196,CREAM,4)]; a=[r(42,42,84,35,BLUE,4),r(42,90,58,35,LILAC,4),r(42,138,121,35,MINT,4),r(42,186,166,24,PEACH,4)]; d=[p('M180 42 V173',stroke=INK,sw=2,stroke_dasharray='5 6')]
    elif i==14: m=[c(128,128,97,CREAM)]; a=[p('M128 128 L128 31 A97 97 0 0 1 225 128 Z',BLUE),p('M128 128 H225 A97 97 0 0 1 128 225 Z',LILAC),p('M128 128 V225 A97 97 0 0 1 31 128 Z',MINT),p('M128 128 H31 A97 97 0 0 1 128 31 Z',PEACH)]; d=[c(128,128,26,CREAM)]
    elif i==15: m=[r(29,29,198,198,CREAM,3)]; a=[p('M29 128 H227 V227 H29 Z',BLUE),p('M29 29 H128 V227 H29 Z',LILAC,INK,2,opacity='.65')]; d=[c(78,177,19,MINT),c(177,78,19,PEACH)]
    elif i==16: m=[r(34,38,188,180,CREAM,4)]; a=[r(50,54,156,25,BLUE,4),r(50,94,70,36,LILAC,4),r(136,94,70,36,MINT,4),r(50,145,70,57,PEACH,4),r(136,145,70,57,PINK,4)]; d=[lines(69,65,112,1),tinycheck(85,112,16),tinycheck(171,170,24)]
    elif i==17: m=[r(27,27,202,202,CREAM,6)]; a=[r(41,41,31,174,BLUE,4),r(87,41,128,31,LILAC,4),r(87,87,128,128,MINT,4)]; d=[p('M119 87 V215 M151 87 V215 M183 87 V215 M87 119 H215 M87 151 H215 M87 183 H215',sw=2)]
    elif i==18: m=[poly([(128,24),(232,128),(128,232),(24,128)],CREAM)]; a=[poly([(128,24),(128,128),(24,128)],BLUE),poly([(128,24),(232,128),(128,128)],LILAC),poly([(232,128),(128,232),(128,128)],MINT),poly([(128,232),(24,128),(128,128)],PEACH)]; d=[c(128,128,19,CREAM)]
    else: m=[r(28,28,200,200,CREAM,8)]; a=[r(40,40,90,56,BLUE,6),r(143,40,73,56,LILAC,6),r(40,109,55,107,MINT,6),r(108,109,108,46,PEACH,6),r(108,168,108,48,PINK,6)]; d=[lines(56,66,51,1),lines(158,66,37,1)]
    return finish(m,a,d)

def planners(i):
    m=[card(31,31,194,194,CREAM,12)]; a=[]; d=[]
    if i==0: a=[r(31,31,194,39,BLUE,12)]; d=[l(70,19,70,49,INK,7),l(186,19,186,49,INK,7)]+[r(51+x*40,88+y*35,26,22,COLORS[(x+y)%6],4) for y in range(3) for x in range(4)]
    elif i==1: a=[r(46,51,43,158,BLUE,5),r(105,51,43,158,LILAC,5),r(164,51,43,158,MINT,5)]; d=[r(51,69,33,36,CREAM,3),r(110,113,33,37,CREAM,3),r(169,80,33,60,CREAM,3)]
    elif i==2: a=[r(43,43,170,38,LILAC,8)]; d=[lines(64,64,129,1)]+[c(57,y,8,MINT)+lines(79,y,121,1) for y in (109,149,190)]
    elif i==3: a=[r(47,43,157,36,BLUE,8)]; d=[p('M82 93 V209 M47 128 H207 M47 164 H207 M47 200 H207',sw=2),r(94,100,101,19,MINT,6),r(94,137,56,19,PEACH,6),r(94,172,86,19,LILAC,6)]
    elif i==4: a=[c(128,111,58,BLUE)]; d=[p('M128 67 V111 L160 137',sw=5),c(128,111,6,INK),r(76,184,104,21,LILAC,10)]
    elif i==5: a=[r(43,43,170,45,MINT,8),r(43,106,75,94,BLUE,8),r(136,106,77,94,LILAC,8)]; d=[txt(82,163,'08',32),txt(175,163,'30',32),txt(128,72,'TODAY',14)]
    elif i==6: a=[r(49,45,157,30,BLUE,6)]; d=[l(66,91,66,205,INK,4)]+[c(66,y,8,COLORS[k])+lines(91,y,105,1) for k,y in enumerate((102,144,188))]
    elif i==7: a=[r(42,42,172,42,LILAC,7)]; d=[r(48,102,36,36,MINT,4),r(104,102,36,36,PEACH,4),r(160,102,36,36,BLUE,4),r(48,161,36,36,MINT,4),r(104,161,36,36,BLUE,4),r(160,161,36,36,BLUE,4),tinycheck(66,120,18),tinycheck(122,120,18),tinycheck(66,179,18)]
    elif i==8: a=[r(44,44,168,43,BLUE,8)]; d=[txt(128,73,'WEEK',16),r(46,108,22,96,MINT,4),r(79,134,22,70,LILAC,4),r(112,98,22,106,PEACH,4),r(145,151,22,53,MINT,4),r(178,122,22,82,BLUE,4)]
    elif i==9: a=[p('M128 62 L190 90 V167 L128 198 L66 167 V90 Z',MINT)]; d=[poly(points(6,cy=128,rad=47),'none',INK,2),c(128,128,11,PEACH),lines(71,45,115,1)]
    elif i==10: a=[r(42,47,171,47,PEACH,10)]; d=[txt(128,79,'30 DAYS',17),p('M53 118 H204 M53 156 H204 M53 194 H204',sw=3)]+[c(64+x*29,119+y*38,7,BLUE) for x in range(5) for y in range(3)]
    elif i==11: a=[r(42,44,172,43,BLUE,5)]; d=[p('M42 105 H213 M42 139 H213 M42 173 H213 M77 105 V205 M111 105 V205 M145 105 V205 M179 105 V205',sw=2),r(83,110,23,24,MINT,3),r(150,144,23,24,PEACH,3),r(116,178,23,24,LILAC,3)]
    elif i==12: a=[r(47,53,76,138,LILAC,8),r(139,53,65,138,MINT,8)]; d=[lines(58,77,54,4,23),tinycheck(168,90,23),c(169,142,14,CREAM),lines(55,210,143,1)]
    elif i==13: a=[r(48,49,158,54,BLUE,8),r(48,121,158,24,MINT,12),r(48,163,100,24,LILAC,12)]; d=[txt(128,84,'FOCUS',18),c(184,176,16,PEACH),p('M177 176 H191 M184 169 V183')]
    elif i==14: a=[r(47,44,157,37,PEACH,8)]; d=[p('M49 108 H206 M49 139 H206 M49 170 H206 M49 202 H206',sw=2)]+[r(53,y,15,15,MINT,3)+tinycheck(60,y+7,9) for y in (94,126,157,189)]
    elif i==15: a=[c(128,128,78,'none',BLUE,16)]; d=[p('M128 50 A78 78 0 0 1 196 166',stroke=LILAC,sw=16),txt(128,125,'25',38),txt(128,151,'MIN',15)]
    elif i==16: a=[r(45,51,166,37,BLUE,5),r(45,104,166,40,LILAC,5),r(45,160,166,40,MINT,5)]; d=[txt(77,77,'01',18),txt(77,130,'02',18),txt(77,186,'03',18),lines(109,70,84,1),lines(109,123,84,1),lines(109,179,84,1)]
    elif i==17: a=[r(46,47,162,47,LILAC,8)]; d=[txt(128,77,'MILESTONES',13),l(61,122,195,122),c(61,122,10,MINT),c(128,122,10,MINT),c(195,122,10,PEACH),lines(53,165,145,3,16)]
    elif i==18: a=[r(46,47,164,39,BLUE,8)]; d=[lines(70,67,112,1),r(49,105,43,89,MINT,6),r(107,105,43,89,LILAC,6),r(165,105,43,89,PEACH,6),txt(71,159,'A',23),txt(129,159,'B',23),txt(187,159,'C',23)]
    else: a=[r(47,47,162,46,MINT,8)]; d=[txt(128,77,'AGENDA',17),c(61,121,9,LILAC),c(61,159,9,PEACH),c(61,197,9,BLUE),lines(85,116,111,2,10),lines(85,154,111,2,10),lines(85,192,111,2,10)]
    return finish(m,a,d)

def badges(i):
    m=[]; a=[]; d=[]
    if i==0: m=[p('M34 57 H180 L228 128 L180 199 H34 Z',BLUE)]; a=[c(186,128,9,CREAM)]; d=[txt(112,132,'RM50',31),l(50,165,150,165)]
    elif i==1: m=[star(12,128,128,104,85,fill=LILAC)]; a=[c(128,128,70,CREAM)]; d=[txt(128,121,'SALE',27),txt(128,154,'50%',25)]
    elif i==2: m=[r(26,67,204,122,BLUE,24)]; a=[r(39,81,178,94,CREAM,16)]; d=[txt(128,134,'VIP',42),star(5,54,42,17,8,fill=PEACH)]
    elif i==3: m=[c(128,103,77,PEACH),p('M83 160 L56 235 L101 216 L128 233 L153 158',BLUE),p('M142 160 L156 234 L179 215 L208 232 L183 154',LILAC)]; a=[c(128,103,57,CREAM)]; d=[star(5,128,103,36,17,fill=MINT)]
    elif i==4: m=[p('M28 63 H228 V190 H28 V158 Q55 128 28 98 Z',BLUE)]; a=[p('M173 63 V190',stroke=INK,sw=2,stroke_dasharray='5 6')]; d=[txt(98,116,'SAVE',21),txt(98,153,'50%',31),txt(200,139,'★',22)]
    elif i==5: m=[poly(points(6,rad=103,rot=-30),MINT)]; a=[poly(points(6,rad=83,rot=-30),CREAM)]; d=[txt(128,132,'NEW',33)]
    elif i==6: m=[p('M45 30 H211 V207 L181 188 L155 219 L128 198 L101 219 L75 188 L45 207 Z',BLUE)]; a=[r(59,45,138,106,CREAM,8)]; d=[txt(128,88,'PRICE',19),txt(128,131,'RM50',30)]
    elif i==7: m=[r(31,46,194,164,CREAM,8)]; a=[r(31,46,194,51,LILAC,8),r(50,151,156,38,MINT,19)]; d=[txt(128,79,'OFFER',24),txt(128,135,'RM50',34),txt(128,177,'ACCESS',15)]
    elif i==8: m=[p('M49 36 H184 L216 68 V219 H49 Z',PEACH)]; a=[p('M184 36 V68 H216 Z',CREAM)]; d=[c(78,64,8,CREAM),txt(128,130,'BEST',24),txt(128,164,'VALUE',25)]
    elif i==9: m=[p('M32 45 H224 V177 L128 226 L32 177 Z',BLUE)]; a=[p('M48 61 H208 V166 L128 205 L48 166 Z',CREAM)]; d=[star(5,128,105,29,13,fill=PEACH),txt(128,164,'PREMIUM',16)]
    elif i==10: m=[c(128,128,94,CREAM),p('M24 103 H232 V154 H24 Z',LILAC)]; a=[p('M24 103 L9 118 L24 128 M232 103 L247 118 L232 128',BLUE)]; d=[txt(128,140,'APPROVED',21)]
    elif i==11: m=[p('M32 47 H224 V103 L205 128 L224 153 V209 H32 V153 L51 128 L32 103 Z',MINT)]; a=[r(50,65,156,126,CREAM,4)]; d=[txt(128,122,'SPECIAL',23),txt(128,153,'EDITION',21)]
    elif i==12: m=[p('M32 37 H224 V219 H32 Z',CREAM)]; a=[p('M32 37 H224 V80 H32 Z',BLUE),p('M32 219 H224 V190 H32 Z',LILAC)]; d=[txt(128,65,'MEMBER',19),txt(128,151,'01',59)]
    elif i==13: m=[r(31,65,194,126,PEACH,63)]; a=[c(77,128,42,CREAM)]; d=[star(5,77,128,27,13,fill=MINT),txt(163,138,'PRO',30)]
    elif i==14: m=[p('M21 89 L128 26 L235 89 V167 L128 230 L21 167 Z',BLUE)]; a=[r(51,90,154,76,CREAM,8)]; d=[txt(128,139,'LIMITED',23)]
    elif i==15: m=[p('M32 50 H224 V206 H32 Z',LILAC)]; a=[p('M32 50 H86 L32 104 Z',MINT),p('M224 206 H170 L224 152 Z',PEACH)]; d=[txt(128,116,'BUNDLE',26),txt(128,153,'PACK',27)]
    elif i==16: m=[c(128,128,97,MINT)]; a=[c(128,128,79,CREAM),r(82,177,92,35,BLUE,4)]; d=[tinycheck(128,117,75),txt(128,201,'VERIFIED',12)]
    elif i==17: m=[p('M55 36 H201 V156 L128 224 L55 156 Z',LILAC)]; a=[p('M73 54 H183 V149 L128 202 L73 149 Z',CREAM)]; d=[txt(128,118,'100%',29),txt(128,149,'ACCESS',16)]
    elif i==18: m=[r(26,45,204,168,CREAM,10)]; a=[r(40,61,176,45,BLUE,7),r(40,163,176,36,MINT,18)]; d=[txt(128,91,'LIFETIME',23),txt(128,147,'PASS',30),txt(128,187,'READY',16)]
    else: m=[p('M35 50 H197 L230 83 V206 H35 Z',PEACH)]; a=[p('M197 50 V83 H230 Z',CREAM),r(53,146,155,42,BLUE,21)]; d=[txt(128,112,'DIGITAL',26),txt(128,174,'DOWNLOAD',17)]
    return finish(m,a,d)

def ctas(i):
    m=[]; a=[]; d=[]
    if i==0: m=[r(23,82,210,92,BLUE,46)]; a=[c(184,128,29,CREAM)]; d=[txt(95,138,'START',24),arrow(171,128,197,128,INK,3,9)]
    elif i==1: m=[r(29,70,198,116,LILAC,14)]; a=[p('M29 168 H227 V186 H29 Z',BLUE)]; d=[txt(128,135,'EXPLORE',29)]
    elif i==2: m=[p('M28 80 H185 L231 128 L185 176 H28 Z',MINT)]; d=[txt(115,137,'NEXT',29)]
    elif i==3: m=[r(29,70,198,116,CREAM,12)]; a=[r(39,80,178,96,BLUE,8)]; d=[txt(128,138,'OPEN',32)]
    elif i==4: m=[r(25,84,206,88,'none',44,INK,5)]; a=[c(189,128,32,LILAC)]; d=[txt(99,137,'GO',30),arrow(176,128,203,128,INK,3,9)]
    elif i==5: m=[r(26,69,204,118,BLUE,24)]; a=[r(37,80,65,96,CREAM,16)]; d=[arrow(69,96,69,137,INK,4,12),p('M53 149 H85'),txt(163,137,'GET',31)]
    elif i==6: m=[r(27,80,202,96,LILAC,48)]; a=[c(74,128,31,CREAM)]; d=[poly([(65,109),(65,147),(91,128)],PEACH),txt(158,137,'PLAY',26)]
    elif i==7: m=[p('M28 87 L50 65 H206 L228 87 V169 L206 191 H50 L28 169 Z',BLUE)]; a=[p('M40 94 L59 77 H197 L216 94 V162 L197 179 H59 L40 162 Z','none',WHITE,3)]; d=[txt(128,140,'JOIN',34)]
    elif i==8: m=[r(25,77,206,103,CREAM,10)]; a=[r(25,77,69,103,MINT,10)]; d=[tinycheck(60,129,33),txt(161,138,'DONE',27)]
    elif i==9: m=[r(25,82,206,91,BLUE,0)]; a=[p('M25 82 H54 L25 111 Z',PEACH),p('M231 173 H202 L231 144 Z',LILAC)]; d=[txt(128,139,'CREATE',28)]
    elif i==10: m=[r(28,73,200,110,PEACH,55)]; a=[c(192,128,32,CREAM)]; d=[txt(106,138,'SHOP',28),p('M183 119 H202 L198 139 H184 Z',BLUE),p('M179 112 H183 L185 119'),c(188,146,2,INK),c(198,146,2,INK)]
    elif i==11: m=[r(30,71,196,114,'url(#glass)',16)]; a=[r(42,84,173,17,WHITE,8,WHITE,1)]; d=[txt(128,146,'CONTINUE',22)]
    elif i==12: m=[r(26,80,204,96,BLUE,20)]; a=[r(39,94,178,68,'none',14,WHITE,2)]; d=[txt(115,136,'TRY',29),sparkle(177,128,16,PEACH)]
    elif i==13: m=[p('M28 77 H190 Q230 77 230 128 Q230 179 190 179 H28 Z',LILAC)]; a=[r(28,77,22,102,MINT,0)]; d=[txt(132,138,'LEARN',28)]
    elif i==14: m=[r(27,72,202,112,CREAM,14)]; a=[r(36,81,184,94,LILAC,10)]; d=[txt(128,126,'DOWNLOAD',21),arrow(128,139,128,162,INK,3,8)]
    elif i==15: m=[p('M26 80 H216 L233 97 V175 H44 L26 157 Z',BLUE)]; a=[p('M216 80 V97 H233 Z',CREAM)]; d=[txt(128,137,'SAVE',31)]
    elif i==16: m=[r(22,76,212,104,PEACH,16)]; a=[r(39,91,82,74,CREAM,10)]; d=[p('M62 115 H99 V141 H62 Z',MINT),p('M62 116 L80 130 L99 116'),txt(175,137,'SEND',26)]
    elif i==17: m=[r(24,84,208,88,MINT,44)]; a=[c(190,128,31,CREAM)]; d=[txt(105,137,'MORE',27),dotrow(176,128,3,14,INK)]
    elif i==18: m=[r(27,73,202,110,BLUE,20)]; a=[r(40,86,175,84,'none',13,INK,2,stroke_dasharray='6 5')]; d=[txt(128,139,'SELECT',29)]
    else: m=[r(27,78,202,100,LILAC,0)]; a=[p('M27 78 L42 62 H229 V162 L229 178 H27 Z','none',INK,3),p('M27 78 L42 62 M229 178 L244 162',stroke=INK,sw=3)]; d=[txt(128,140,'BUILD',31)]
    return finish(m,a,d)

def particles(i):
    m=[]; a=[]; d=[]
    if i==0: m=[c(128,128,20,BLUE)]; a=[c(*xy,rad, COL) for xy,rad,COL in [((67,67),9,PEACH),((185,70),13,LILAC),((192,182),10,MINT),((70,193),14,PINK)]]; d=[sparkle(43,132,11),sparkle(131,40,11),sparkle(222,129,11),sparkle(130,219,11)]
    elif i==1: m=[star(5,128,126,38,17,fill=PEACH)]; a=[star(5,52,62,17,8,fill=LILAC),star(5,201,64,23,11,fill=MINT),star(5,186,205,17,8,fill=BLUE),star(5,50,190,25,12,fill=PINK)]; d=[c(99,47,4,INK),c(224,157,4,INK),c(95,219,4,INK)]
    elif i==2: m=[c(128,128,31,'none',BLUE,10)]; a=[c(65,65,19,'none',PEACH,7),c(205,81,13,'none',LILAC,7),c(66,199,17,'none',MINT,7),c(194,194,25,'none',PINK,7)]; d=[c(117,44,4,INK),c(223,143,4,INK)]
    elif i==3: m=[p('M37 128 H77 M179 128 H219 M128 37 V77 M128 179 V219',stroke=BLUE,sw=13)]; a=[p('M63 63 L86 86 M170 170 L193 193 M63 193 L86 170 M170 86 L193 63',stroke=PEACH,sw=10)]; d=[c(128,128,22,LILAC)]
    elif i==4: m=[poly([(42,51),(59,45),(70,77),(53,83)],BLUE),poly([(154,42),(176,36),(166,64)],PEACH),poly([(198,109),(221,127),(193,144)],MINT),poly([(62,188),(76,213),(46,219)],LILAC)]; a=[r(117,99,18,35,PINK,2,transform='rotate(24 126 116)'),r(149,174,35,14,BLUE,2,transform='rotate(-20 166 181)')]; d=[sparkle(47,133,8),sparkle(129,216,8)]
    elif i==5: m=[p('M35 104 Q70 56 108 86',stroke=BLUE,sw=8),p('M140 45 Q197 57 191 111',stroke=LILAC,sw=8),p('M213 163 Q170 220 136 177',stroke=MINT,sw=8),p('M102 210 Q50 212 44 162',stroke=PEACH,sw=8)]; a=[c(128,128,10,PINK)]; d=[sparkle(126,43,10),sparkle(224,131,10),sparkle(110,229,10),sparkle(32,144,10)]
    elif i==6: m=[poly(points(3,cx=64,cy=67,rad=23),BLUE),poly(points(4,cx=190,cy=62,rad=22),LILAC),poly(points(5,cx=128,cy=128,rad=28),PEACH),poly(points(6,cx=59,cy=194,rad=21),MINT),c(194,197,22,PINK)]; d=[c(33,129,4,INK),c(143,35,4,INK)]
    elif i==7: m=[sparkle(128,128,34,LILAC)]; a=[sparkle(63,70,19,BLUE),sparkle(193,66,13,PEACH),sparkle(62,201,12,MINT),sparkle(193,186,23,PINK)]; d=[l(31,145,55,145),l(211,134,230,134)]
    elif i==8: m=[p('M44 201 Q128 39 212 201',stroke=BLUE,sw=5,stroke_dasharray='1 13')]; a=[c(54,179,10,PEACH),c(95,104,8,LILAC),c(148,88,11,MINT),c(199,162,8,PINK)]; d=[star(5,128,63,17,8,fill=PEACH)]
    elif i==9: m=[p('M36 128 Q70 62 128 128 Q180 186 220 128',stroke=LILAC,sw=6)]; a=[c(53,110,10,BLUE),c(106,105,9,MINT),c(151,151,13,PEACH),c(204,150,7,PINK)]; d=[c(56,163,4,INK),c(159,82,4,INK)]
    elif i==10: m=[p('M28 51 L51 37 M94 33 L107 52 M185 42 L162 58 M218 85 L235 99 M219 166 L234 151 M198 215 L176 224 M86 216 L65 230 M30 151 L47 168',stroke=BLUE,sw=9)]; a=[star(5,128,128,50,23,fill=PEACH)]; d=[c(38,102,5,LILAC),c(130,223,5,MINT)]
    elif i==11: m=[r(43,46,21,41,BLUE,0,transform='rotate(-25 54 66)'),r(184,46,21,41,LILAC,0,transform='rotate(25 195 66)'),r(40,174,21,41,MINT,0,transform='rotate(20 50 195)'),r(182,174,21,41,PEACH,0,transform='rotate(-20 192 195)')]; a=[r(111,110,34,34,PINK,0,transform='rotate(45 128 128)')]; d=[sparkle(129,42,11),sparkle(129,217,11)]
    elif i==12: m=[c(93,120,34,BLUE),c(142,90,28,LILAC),c(169,142,33,MINT),c(115,172,27,PEACH)]; a=[c(128,128,22,CREAM)]; d=[sparkle(55,56,9),sparkle(206,61,11),sparkle(204,207,9)]
    elif i==13: m=[p('M34 128 Q128 17 222 128 Q128 239 34 128 Z','none',BLUE,5),p('M61 128 Q128 53 195 128 Q128 204 61 128 Z','none',LILAC,5)]; a=[c(128,128,17,PEACH)]; d=[c(34,128,8,MINT),c(222,128,8,PINK)]
    elif i==14: m=[l(30,213,70,173,BLUE,9),l(44,132,90,86,LILAC,9),l(112,60,154,18,MINT,9),l(138,201,182,157,PEACH,9),l(184,111,230,65,PINK,9)]; a=[star(5,113,125,22,10,fill=PEACH)]; d=[c(44,66,4,INK),c(211,208,4,INK)]
    elif i==15: m=[p('M43 94 A36 36 0 1 1 91 42 M165 53 A34 34 0 1 1 211 99 M212 168 A36 36 0 1 1 168 214 M87 213 A36 36 0 1 1 41 167',stroke=BLUE,sw=8)]; a=[sparkle(128,128,28,LILAC)]; d=[c(129,33,5,PEACH),c(223,130,5,MINT)]
    elif i==16: m=[p('M30 128 L65 66 L105 113 L145 44 L181 92 L226 58',stroke=BLUE,sw=5)]; a=[c(30,128,11,MINT),c(65,66,8,LILAC),c(105,113,13,PEACH),c(145,44,8,PINK),c(181,92,11,MINT),c(226,58,8,LILAC)]; d=[sparkle(128,182,23),sparkle(54,211,10)]
    elif i==17: m=[c(128,128,87,'none',BLUE,4,stroke_dasharray='1 12')]; a=[sparkle(128,41,17,PEACH),sparkle(41,128,11,LILAC),sparkle(215,128,20,MINT),sparkle(128,215,13,PINK)]; d=[c(128,128,18,CREAM)]
    elif i==18: m=[p('M37 191 Q37 119 91 127 Q146 140 128 84 Q121 43 196 42',stroke=LILAC,sw=9)]; a=[c(37,191,10,BLUE),c(91,127,8,PEACH),c(128,84,8,MINT),c(196,42,11,PINK)]; d=[sparkle(193,191,20),c(54,56,5,INK)]
    else: m=[poly([(36,64),(80,45),(73,95)],BLUE),poly([(165,38),(213,64),(165,90)],LILAC),poly([(184,154),(227,193),(174,212)],MINT),poly([(42,162),(85,185),(42,220)],PEACH)]; a=[c(128,128,21,PINK)]; d=[sparkle(128,41,9),sparkle(216,127,9),sparkle(122,218,9),sparkle(33,124,9)]
    return finish(m,a,d)

def abstract(i):
    m=[]; a=[]; d=[]
    if i==0: m=[p('M41 127 C25 43 139 3 191 63 C242 119 214 223 129 216 C61 214 52 165 41 127 Z',BLUE)]; a=[p('M62 133 C48 69 133 38 170 82 C205 119 184 190 132 190 C87 190 71 158 62 133 Z',LILAC)]
    elif i==1: m=[p('M46 158 C18 89 108 43 181 28 C157 106 242 142 210 193 C163 239 69 219 46 158 Z',MINT)]; a=[p('M74 153 C67 99 129 68 166 57 C148 112 203 144 186 177 C149 207 93 194 74 153 Z',CREAM)]
    elif i==2: m=[p('M28 84 Q90 21 137 58 Q191 15 228 89 Q246 144 186 160 Q151 226 79 213 Q22 198 46 142 Q4 130 28 84 Z',LILAC)]; a=[c(128,128,42,PEACH)]
    elif i==3: m=[p('M32 61 H100 V25 H158 V93 H226 V151 H158 V219 H100 V151 H32 Z',BLUE)]; a=[r(111,104,36,36,PEACH,4)]
    elif i==4: m=[p('M30 207 L85 29 L141 207 Z',MINT),p('M112 207 L167 29 L225 207 Z',LILAC)]; a=[poly([(97,135),(128,49),(159,135)],PEACH)]
    elif i==5: m=[p('M30 77 Q128 29 226 77 V178 Q128 226 30 178 Z',BLUE)]; a=[p('M30 101 Q128 53 226 101 M30 127 Q128 79 226 127 M30 153 Q128 105 226 153',stroke=WHITE,sw=6)]
    elif i==6: m=[c(92,128,73,BLUE),c(164,128,73,LILAC,INK,3,opacity='.82')]; a=[p('M128 65 A73 73 0 0 1 128 191 A73 73 0 0 1 128 65 Z',MINT)]; d=[sparkle(128,128,19)]
    elif i==7: m=[p('M43 55 H213 V95 H84 V135 H213 V175 H84 V215 H43 Z',BLUE)]; a=[p('M64 55 V215',stroke=WHITE,sw=5)]
    elif i==8: m=[p('M31 53 H225 V93 H91 V123 H198 V163 H91 V203 H31 Z',LILAC)]; a=[r(147,174,78,29,PEACH,4)]
    elif i==9: m=[p('M26 151 C86 231 174 231 230 151 L128 36 Z',MINT)]; a=[p('M49 149 Q128 210 207 149 L128 67 Z',CREAM)]; d=[c(128,142,20,LILAC)]
    elif i==10: m=[p('M34 57 H91 V104 H138 V151 H185 V198 H231 V231 H152 V184 H105 V137 H58 V90 H34 Z',BLUE)]; a=[poly([(130,22),(228,22),(228,121)],LILAC)]
    elif i==11: m=[poly(points(8,rad=106,rot=-22.5),PEACH)]; a=[poly(points(8,rad=80,rot=-22.5),CREAM),poly(points(8,rad=55,rot=-22.5),LILAC)]; d=[c(128,128,28,BLUE)]
    elif i==12: m=[p('M128 20 Q145 95 220 128 Q145 145 128 236 Q111 145 20 128 Q111 95 128 20 Z',LILAC)]; a=[p('M128 61 Q138 109 181 128 Q138 138 128 194 Q118 138 71 128 Q118 109 128 61 Z',CREAM)]
    elif i==13: m=[p('M28 169 Q128 6 228 169 L188 213 Q128 112 68 213 Z',BLUE)]; a=[p('M51 170 Q128 46 205 170',stroke=WHITE,sw=9)]
    elif i==14: m=[p('M32 44 H224 V76 H97 V108 H192 V140 H97 V172 H224 V204 H32 Z',MINT)]; a=[r(44,54,22,140,CREAM,11)]
    elif i==15: m=[p('M39 45 H98 V99 H158 V158 H212 V217 H158 V158 H98 V99 H39 Z',BLUE)]; a=[r(150,39,67,67,LILAC,0),r(39,150,67,67,PEACH,0)]
    elif i==16: m=[p('M27 129 C27 27 229 27 229 129 C229 229 27 229 27 129 Z',LILAC)]; a=[p('M47 129 C47 56 209 56 209 129 C209 200 47 200 47 129 Z',CREAM),p('M72 129 C72 91 184 91 184 129 C184 164 72 164 72 129 Z',BLUE)]
    elif i==17: m=[p('M128 23 L231 231 H25 Z',PEACH)]; a=[p('M128 65 L198 208 H58 Z',CREAM),p('M128 108 L164 185 H92 Z',LILAC)]
    elif i==18: m=[p('M31 58 H224 V100 H73 V140 H224 V183 H31 Z',BLUE),p('M55 100 H199 V140 H55 Z',LILAC)]; a=[c(220,58,18,PEACH),c(34,183,18,MINT)]
    else: m=[p('M45 29 H104 V94 H169 V159 H228 V218 H169 V159 H104 V94 H45 Z',MINT),p('M29 151 H94 V216 H29 Z',LILAC),p('M151 29 H216 V94 H151 Z',PEACH)]; d=[sparkle(197,197,11),sparkle(61,61,11)]
    return finish(m,a,d)

def flowers(i):
    m=[]; a=[]; d=[]
    if i not in (5,12,15,16,19): d=[p('M128 159 V232',stroke=INK,sw=5),p('M128 205 Q93 166 77 197 Q90 219 128 213 Z',MINT),p('M128 188 Q165 154 179 182 Q161 205 128 202 Z',MINT)]
    if i==0: m=[g(e(0,-39,14,38,CREAM),f'translate(128 104) rotate({k*30})') for k in range(12)]; a=[c(128,104,24,PEACH)]
    elif i==1: m=[p('M77 45 L102 69 L128 40 L154 69 L179 45 V109 Q179 164 128 164 Q77 164 77 109 Z',PINK)]; a=[p('M102 69 Q104 137 128 160 M154 69 Q152 137 128 160',stroke=WHITE,sw=4)]
    elif i==2: m=[p('M128 42 C181 11 221 66 191 110 C227 147 177 190 134 158 C90 192 35 151 69 111 C34 64 88 14 128 42 Z',PINK),p('M128 65 C164 44 191 80 170 112 C196 141 157 164 132 146 C101 170 66 141 90 112 C68 79 106 43 128 65 Z',PEACH)]; a=[p('M128 91 C149 81 160 101 145 112 C160 128 140 147 126 129 C102 143 93 114 115 110 C103 91 115 86 128 91 Z',CREAM)]
    elif i==3: m=[p('M128 37 Q181 94 160 145 Q128 167 97 144 Q73 94 128 37 Z',PINK),p('M53 73 Q112 73 128 151 Q57 165 53 73 Z',LILAC),p('M203 73 Q144 73 128 151 Q199 165 203 73 Z',LILAC),p('M32 110 Q89 96 128 156 Q68 179 32 110 Z',PINK),p('M224 110 Q167 96 128 156 Q188 179 224 110 Z',PINK)]; a=[p('M74 144 Q128 189 182 144',stroke=MINT,sw=7)]
    elif i==4: m=[g(e(0,-35,12,36,PEACH),f'translate(128 106) rotate({k*22.5})') for k in range(16)]; a=[c(128,106,37,CREAM)]; d += [c(112+x*12,90+y*12,2,INK,INK,1) for x in range(3) for y in range(3)]
    elif i==5: m=[g(p('M0 0 C-45 -24 -32 -81 0 -59 C32 -81 45 -24 0 0 Z',PINK),f'translate(128 128) rotate({k*72})') for k in range(5)]; a=[c(128,128,16,PEACH)]; d=[l(128,128,128+25*math.cos(k*math.pi*2/5),128+25*math.sin(k*math.pi*2/5),INK,2)+c(128+25*math.cos(k*math.pi*2/5),128+25*math.sin(k*math.pi*2/5),3,INK,INK,1) for k in range(5)]
    elif i==6: m=[g(p('M0 0 C-56 -1 -71 -41 -36 -63 C2 -96 35 -47 0 0 Z',PINK),f'translate(128 112) rotate({k*72})') for k in range(5)]; a=[p('M125 111 Q149 68 168 44',stroke=INK,sw=4),c(168,44,6,PEACH),c(156,56,4,PEACH),c(148,70,4,PEACH)]
    elif i==7: m=[p('M128 113 C31 114 24 53 79 45 Q126 37 128 113 Z',LILAC),p('M128 113 C225 114 232 53 177 45 Q130 37 128 113 Z',LILAC),p('M128 113 C84 88 88 15 128 36 C168 15 172 88 128 113 Z',PINK),p('M128 113 C92 98 60 147 84 169 Q112 181 128 113 Z',BLUE),p('M128 113 C164 98 196 147 172 169 Q144 181 128 113 Z',BLUE)]; a=[p('M111 103 Q128 91 145 103 L154 133 L128 158 L102 133 Z',CREAM),c(128,119,8,PEACH)]
    elif i==8: m=[p('M88 52 Q127 17 168 52 Q144 94 178 140 Q127 167 78 140 Q112 94 88 52 Z',LILAC)]; a=[p('M78 140 Q101 125 128 141 Q152 126 178 140',stroke=WHITE,sw=4),p('M111 52 L128 81 L145 52',MINT)]; d += [l(128,150,128,177),c(128,177,6,PEACH)]
    elif i==9: m=[g(p('M0 0 C-58 -4 -71 -63 -19 -64 C33 -74 33 -22 0 0 Z',PINK),f'translate(128 111) rotate({k*90})') for k in range(4)]; a=[c(128,111,23,CREAM)]; d += [c(128+15*math.cos(k*.8),111+15*math.sin(k*.8),2,INK,INK,1) for k in range(8)]
    elif i==10: m=[p('M128 27 V217',stroke=INK,sw=4)]; a=[e(113,55,13,21,LILAC),e(140,70,13,21,LILAC),e(111,93,14,21,LILAC),e(141,110,14,21,LILAC),e(112,135,14,21,LILAC),e(141,154,14,21,LILAC)]; d=[p('M128 205 Q79 167 63 190 Q88 218 128 215 Z',MINT),p('M128 199 Q174 177 193 197 Q163 222 128 215 Z',MINT)]
    elif i==11: m=[c(96,89,36,CREAM),c(152,86,37,CREAM),c(126,131,40,CREAM)]; a=[p('M82 125 Q127 154 172 121 L152 160 L104 160 Z',MINT)]; d += [p('M103 60 Q116 87 104 110 M150 58 Q137 88 151 109',stroke=PEACH,sw=3)]
    elif i==12: m=[c(128,128,17,PEACH)]; a=[l(128,128,128+84*math.cos(k*math.pi/9),128+84*math.sin(k*math.pi/9),INK,2)+c(128+84*math.cos(k*math.pi/9),128+84*math.sin(k*math.pi/9),7,CREAM,INK,2) for k in range(18)]; d=[c(128,128,5,LILAC)]
    elif i==13: m=[g(p('M0 0 Q-20 -43 0 -70 Q20 -43 0 0 Z',LILAC),f'translate(128 103) rotate({k*20})') for k in range(18)]; a=[g(p('M0 0 Q-11 -29 0 -45 Q11 -29 0 0 Z',PINK),f'translate(128 103) rotate({k*30+15})') for k in range(12)]+[c(128,103,16,CREAM)]
    elif i==14: m=[p('M128 64 C70 13 18 86 78 132 Q118 169 128 196 Q138 169 178 132 C238 86 186 13 128 64 Z',PINK)]; a=[p('M128 162 Q144 85 155 51',stroke=PEACH,sw=15)]; d += [p('M102 151 Q122 120 140 85',stroke=WHITE,sw=3)]
    elif i==15: m=[]
    elif i==16: m=[g(p('M0 0 C-47 -36 -23 -78 0 -69 C23 -78 47 -36 0 0 Z',CREAM),f'translate(128 128) rotate({k*45})') for k in range(8)]; a=[g(e(0,-22,11,25,PINK),f'translate(128 128) rotate({k*60+15})') for k in range(6)]+[c(128,128,17,PEACH)]
    elif i==17: m=[g(p('M0 0 C-40 -41 -36 -77 0 -70 C36 -77 40 -41 0 0 Z',PINK),f'translate(128 108) rotate({k*45})') for k in range(8)]; a=[g(p('M0 0 C-20 -27 -16 -47 0 -41 C16 -47 20 -27 0 0 Z',PEACH),f'translate(128 108) rotate({k*60+20})') for k in range(6)]+[c(128,108,13,CREAM)]
    elif i==18: m=[g(p('M0 0 Q-39 -52 0 -74 Q39 -52 0 0 Z',CREAM),f'translate(128 112) rotate({k*60})') for k in range(6)]; a=[p('M101 95 L155 95 L151 138 Q128 156 105 138 Z',PEACH),e(128,95,27,10,CREAM)]; d += [c(128,116,8,PINK)]
    else: m=[p('M57 159 Q50 69 128 23 Q206 69 199 159 Q128 228 57 159 Z',PINK)]; a=[p('M70 159 Q65 88 128 41 Q191 88 186 159 Q128 205 70 159 Z',CREAM)]; d=[p('M82 156 L91 103 M106 175 L111 76 M128 185 V56 M150 175 L145 76 M174 156 L165 103',stroke=PEACH,sw=7)]
    if i==15:
        for x,y in [(98,62),(143,48),(176,80),(74,108),(119,110),(165,129),(105,155)]:
            m += [g(e(0,-11,9,14,COLORS[(x+y)%3]),f'translate({x} {y}) rotate({k*90})') for k in range(4)]
            a += [c(x,y,5,CREAM,INK,1)]
        d=[p('M128 170 V234',stroke=INK,sw=5),p('M125 195 Q86 158 69 191 Q82 219 125 215 Z',MINT)]
    return finish(m,a,d)

def leaves(i):
    m=[]; a=[]; d=[]
    if i==0: m=[p('M128 225 V29',sw=5)]+[p(f'M128 {62+k*27} Q{71-k*2} {29+k*28} {47-k*3} {50+k*30} Q83 {83+k*24} 128 {82+k*25} Z',MINT)+p(f'M128 {62+k*27} Q{185+k*2} {29+k*28} {209+k*3} {50+k*30} Q173 {83+k*24} 128 {82+k*25} Z',MINT) for k in range(5)]
    elif i==1: m=[p('M128 226 V78',sw=5)]+[p(f'M128 78 Q{128+math.cos(t)*60:.1f} {78+math.sin(t)*60:.1f} {128+math.cos(t)*101:.1f} {78+math.sin(t)*101:.1f} Q{128+math.cos(t+.2)*56:.1f} {78+math.sin(t+.2)*42:.1f} 128 78 Z',MINT) for t in [0,.5,1,2.1,2.6,3.1,3.7,4.2,5.2,5.7]]; d=[p('M128 81 Q110 55 114 26',sw=2)]
    elif i==2: m=[p('M128 218 C23 186 31 54 100 40 Q122 8 151 37 C224 39 246 178 128 218 Z',MINT)]; a=[p('M128 208 V53',sw=4)]; d=[p('M69 81 L117 111 M55 129 L113 143 M70 169 L111 178 M180 79 L141 107 M198 125 L142 144 M181 171 L144 178',stroke=CREAM,sw=12)]
    elif i==3: m=[p('M128 199 Q18 176 36 58 Q77 15 128 91 Q179 15 220 58 Q238 176 128 199 Z',MINT)]; a=[l(128,199,128,234,INK,5)]; d=[p('M128 199 L63 62 M128 199 L94 58 M128 199 V91 M128 199 L162 58 M128 199 L193 62',stroke=INK,sw=2)]
    elif i==4: m=[p('M128 22 Q107 47 119 67 Q84 37 77 62 Q69 87 99 98 Q55 78 51 111 Q43 139 91 145 Q59 149 71 182 Q80 212 128 218 Q176 212 185 182 Q197 149 165 145 Q213 139 205 111 Q201 78 157 98 Q187 87 179 62 Q172 37 137 67 Q149 47 128 22 Z',MINT)]; d=[p('M128 48 V235 M128 102 L90 78 M128 143 L72 118 M128 179 L88 173 M128 102 L166 78 M128 143 L184 118 M128 179 L168 173',sw=2)]
    elif i==5: m=[p('M128 25 L151 77 L185 47 L182 103 L229 98 L181 151 L207 184 L150 184 L128 226 L106 184 L49 184 L75 151 L27 98 L74 103 L71 47 L105 77 Z',PEACH)]; d=[p('M128 47 V239 M128 156 L79 114 M128 156 L177 114 M128 156 L91 72 M128 156 L165 72',sw=2)]
    elif i==6: m=[p('M129 228 Q115 119 143 27',sw=4)]; a=[e(115,58,28,20,MINT),e(153,94,30,22,BLUE),e(107,129,32,24,MINT),e(149,171,33,24,BLUE),e(112,201,29,20,MINT)]; d=[l(117,58,130,72),l(153,94,127,103),l(108,130,124,140),l(149,171,124,173)]
    elif i==7: m=[p('M72 228 L180 32',sw=4)]; a=[p('M162 64 Q122 8 96 38 Q111 79 156 77 Z',MINT),p('M146 97 Q205 50 216 85 Q194 119 140 110 Z',MINT),p('M125 134 Q68 80 46 112 Q61 151 120 147 Z',MINT),p('M105 173 Q169 125 187 164 Q159 201 99 186 Z',MINT),p('M87 207 Q35 158 26 191 Q48 229 82 219 Z',MINT)]
    elif i==8: m=[p('M111 225 C19 196 56 52 152 23 C237 108 207 219 111 225 Z',MINT)]; d=[p('M111 225 Q149 126 152 23 M122 180 L65 135 M137 124 L86 87 M146 81 L181 113 M132 154 L183 177',sw=2)]
    elif i==9: m=[p('M128 23 L150 71 L197 45 L184 98 L231 108 L187 142 L210 191 L158 180 L128 230 L98 180 L46 191 L69 142 L25 108 L72 98 L59 45 L106 71 Z',MINT)]; d=[p('M128 41 V230 M128 139 L77 80 M128 139 L179 80 M128 139 L62 169 M128 139 L194 169',sw=2)]
    elif i==10: m=[p('M129 224 C45 158 10 77 73 42 Q107 18 128 59 Q154 10 187 44 C248 83 204 163 129 224 Z',MINT)]; d=[p('M129 224 V61 M129 122 L81 67 M129 160 L61 108 M129 122 L179 67 M129 160 L197 108',sw=2)]
    elif i==11: m=[p('M128 226 L26 88 Q86 125 111 207 L87 33 Q135 84 128 211 L169 23 Q168 92 138 210 L231 91 Q188 165 145 226 Z',MINT)]; d=[p('M128 226 L88 132 M128 226 L110 102 M128 226 L154 104 M128 226 L195 135',sw=2)]
    elif i==12: m=[p('M128 42 C194 17 237 61 225 119 Q219 192 128 209 Q37 192 31 119 C19 61 84 19 128 42 Z',MINT)]; a=[p('M128 127 L128 42 L164 50 Z',CREAM)]; d=[p('M128 127 L55 78 M128 127 L45 147 M128 127 L80 186 M128 127 L128 209 M128 127 L192 178 M128 127 L216 115',sw=2)]
    elif i==13: m=[p('M98 225 Q62 161 72 103 Q79 54 142 30 Q203 60 197 120 Q195 195 98 225 Z',MINT)]; a=[p('M98 225 Q165 178 154 114 Q144 73 142 30',stroke=INK,sw=4)]; d=[p('M114 209 Q179 195 194 147',stroke=CREAM,sw=7)]
    elif i==14: m=[p('M63 228 Q156 117 190 30',sw=4)]; a=[p(f'M{80+k*20} {199-k*36} Q{30+k*18} {142-k*30} {51+k*21} {130-k*33} Q{96+k*18} {150-k*32} {80+k*20} {199-k*36} Z',MINT) for k in range(5)]+[p(f'M{88+k*21} {187-k*36} Q{134+k*19} {192-k*32} {160+k*16} {160-k*28} Q{143+k*14} {147-k*28} {88+k*21} {187-k*36} Z',MINT) for k in range(4)]
    elif i==15: m=[g(p('M0 0 Q-39 -59 0 -88 Q39 -59 0 0 Z',MINT),f'translate(128 139) rotate({k*60})') for k in range(6)]; a=[g(p('M0 0 Q-23 -36 0 -55 Q23 -36 0 0 Z',BLUE),f'translate(128 139) rotate({k*60+30})') for k in range(6)]; d=[c(128,139,21,LILAC)]
    elif i==16: m=[p('M128 233 V28',sw=4)]; a=[p(f'M128 {63+k*31} Q86 {30+k*31} 94 {63+k*31} Q100 {83+k*31} 128 {81+k*31} Z',PEACH)+p(f'M128 {81+k*31} Q170 {45+k*31} 164 {81+k*31} Q157 {102+k*31} 128 {100+k*31} Z',PEACH) for k in range(5)]; d=[p('M117 35 L117 22 M137 39 L137 22',sw=2)]
    elif i==17: m=[p('M44 218 Q149 157 197 34',sw=5)]; a=[p('M74 195 Q27 124 71 113 Q93 140 90 178 Z',MINT),p('M113 154 Q97 75 145 77 Q156 113 129 141 Z',BLUE),p('M153 107 Q141 30 182 28 Q198 56 164 87 Z',MINT),p('M104 169 Q157 165 187 205 Q153 231 104 186 Z',BLUE),p('M144 127 Q197 108 224 134 Q209 171 144 145 Z',MINT)]
    elif i==18: m=[r(90,22,27,212,MINT,4),r(137,22,27,212,BLUE,4)]; d=[p('M90 77 H117 M90 132 H117 M90 187 H117 M137 53 H164 M137 108 H164 M137 163 H164 M137 218 H164')]; a=[p('M115 100 Q159 77 204 97 Q174 123 115 117 Z',MINT),p('M137 164 Q91 134 46 151 Q71 177 137 181 Z',MINT)]
    else: m=[p('M128 232 V26',sw=5)]; a=[p(f'M128 {46+k*32} L{96-k*10} {77+k*32} L128 {65+k*32} L{160+k*10} {77+k*32} Z',MINT) for k in range(5)]; d=[p('M128 27 L117 47 H139 Z',PEACH)]
    if i in (1,14):
        m=[g(m,'translate(18 20) scale(.86)')]; a=[g(a,'translate(18 20) scale(.86)')]; d=[g(d,'translate(18 20) scale(.86)')]
    return finish(m,a,d)

def speedlines(i):
    m=[]; a=[]; d=[]
    if i==0: m=[l(28,65,184,65,BLUE,9),l(48,105,228,105,LILAC,9),l(25,147,195,147,MINT,9),l(62,192,226,192,PEACH,9)]
    elif i==1: m=[l(29,47,174,103,BLUE,8),l(25,104,192,125,LILAC,8),l(28,162,187,145,MINT,8),l(35,222,173,169,PEACH,8)]; a=[poly([(184,109),(230,128),(184,148)],CREAM)]
    elif i==2: m=[l(35,35,85,85,BLUE,8),l(128,23,128,74,LILAC,8),l(221,35,171,85,MINT,8),l(232,128,184,128,PEACH,8),l(221,221,171,171,PINK,8),l(128,232,128,184,BLUE,8),l(35,221,85,171,LILAC,8),l(23,128,74,128,MINT,8)]; a=[c(128,128,29,'none',INK,3)]
    elif i==3: m=[p('M27 60 Q128 12 229 60 M27 105 Q128 57 229 105 M27 150 Q128 102 229 150 M27 195 Q128 147 229 195',stroke=BLUE,sw=8)]; a=[c(35,214,4,PEACH)]
    elif i==4: m=[p('M30 213 Q37 81 224 37 M50 230 Q54 99 237 59 M74 239 Q82 125 241 85',stroke=LILAC,sw=8)]; d=[p('M36 191 L26 218 L52 219',PEACH)]
    elif i==5: m=[p('M28 74 H116 L141 98 H228 M28 128 H151 L176 152 H228 M28 183 H93 L118 207 H228',stroke=BLUE,sw=7)]; a=[c(28,74,5,PEACH),c(28,128,5,LILAC),c(28,183,5,MINT)]
    elif i==6: m=[l(31,40,168,40,BLUE,8),l(57,80,211,80,LILAC,8),l(21,120,145,120,MINT,8),l(58,160,231,160,PEACH,8),l(31,200,179,200,PINK,8)]; d=[l(195,40,220,40),l(22,80,35,80),l(167,120,200,120)]
    elif i==7: m=[p('M34 91 Q128 8 222 91 M47 131 Q128 60 209 131 M60 171 Q128 111 196 171 M76 207 Q128 161 180 207',stroke=MINT,sw=8)]
    elif i==8: m=[p('M27 42 L77 95 M95 27 L115 85 M229 42 L179 95 M161 27 L141 85 M27 214 L77 161 M95 229 L115 171 M229 214 L179 161 M161 229 L141 171',stroke=BLUE,sw=7)]; a=[sparkle(128,128,24,PEACH)]
    elif i==9: m=[p('M31 213 L213 31 M58 231 L231 58 M22 186 L186 22',stroke=LILAC,sw=10)]; a=[p('M25 122 L122 25 M132 232 L232 132',stroke=PEACH,sw=5)]
    elif i==10: m=[p('M31 63 H98 L68 105 H165 L121 151 H224 L178 195 H225',stroke=BLUE,sw=12)]; a=[poly([(201,181),(229,195),(201,209)],PEACH)]
    elif i==11: m=[p('M25 60 C107 100 149 21 231 60 M25 105 C107 145 149 66 231 105 M25 150 C107 190 149 111 231 150 M25 195 C107 235 149 156 231 195',stroke=LILAC,sw=6)]
    elif i==12: m=[p('M43 54 L110 106 M35 99 L105 118 M35 156 L105 139 M43 203 L110 151 M213 54 L146 106 M221 99 L151 118 M221 156 L151 139 M213 203 L146 151',stroke=BLUE,sw=9)]; a=[c(128,128,16,PEACH)]
    elif i==13: m=[p('M29 83 H168 L205 119 M43 127 H143 L187 171 M65 171 H119 L150 202',stroke=MINT,sw=8)]; d=[arrow(201,115,227,141,INK,3,10)]
    elif i==14: m=[p('M31 43 C61 202 198 194 226 49 M55 37 C81 167 174 162 201 40 M80 33 C97 128 156 125 176 34',stroke=LILAC,sw=8)]; a=[poly([(209,51),(228,28),(237,60)],PEACH)]
    elif i==15: m=[l(34,42,222,42,BLUE,10),l(52,80,203,80,BLUE,8),l(74,116,183,116,BLUE,6),l(92,152,163,152,BLUE,4),l(112,188,145,188,BLUE,3)]; a=[c(128,214,5,PEACH)]
    elif i==16: m=[p('M35 60 L83 108 L124 66 L169 111 L214 67 M35 130 L83 178 L124 136 L169 181 L214 137',stroke=BLUE,sw=9)]; a=[p('M35 200 L55 220 L77 199',stroke=PEACH,sw=6)]
    elif i==17: m=[p('M31 72 H219 M31 118 H219 M31 164 H219 M31 210 H219',stroke=LILAC,sw=8,stroke_dasharray='30 14')]; a=[l(49,41,201,41,PEACH,4)]
    elif i==18: m=[p('M44 57 Q21 128 44 199 M79 38 Q48 128 79 218 M114 29 Q78 128 114 227 M149 29 Q113 128 149 227',stroke=BLUE,sw=8)]; a=[p('M200 41 Q166 128 200 215',stroke=PEACH,sw=5)]
    else: m=[p('M25 35 L92 96 M79 25 L111 85 M177 25 L145 85 M231 35 L164 96 M25 221 L92 160 M79 231 L111 171 M177 231 L145 171 M231 221 L164 160',stroke=BLUE,sw=7)]; a=[poly([(116,111),(144,111),(144,145),(116,145)],LILAC)]
    return finish(m,a,d)

def camera(i):
    m=[]; a=[]; d=[]
    if i==0: m=[p('M31 87 V31 H87 M169 31 H225 V87 M31 169 V225 H87 M169 225 H225 V169',stroke=BLUE,sw=8)]; d=[c(128,128,12,'none',INK,2),l(108,128,148,128),l(128,108,128,148)]
    elif i==1: m=[r(24,47,208,162,'none',12,INK,4)]; a=[r(35,60,62,24,PEACH,12)]; d=[c(48,72,5,PINK),txt(72,77,'REC',12),txt(191,191,'00:00',13)]
    elif i==2: m=[p('M32 74 V32 H74 M182 32 H224 V74 M32 182 V224 H74 M182 224 H224 V182',sw=4),c(128,128,57,'none',BLUE,5)]; d=[p('M128 54 V95 M128 161 V202 M54 128 H95 M161 128 H202',sw=2)]
    elif i==3: m=[r(22,49,212,157,'none',0,INK,4)]; a=[p('M22 101 H234 M22 153 H234 M93 49 V206 M163 49 V206',stroke=BLUE,sw=3)]
    elif i==4: m=[c(128,128,90,'none',BLUE,6),c(128,128,63,'none',LILAC,4),c(128,128,35,'none',INK,2)]; a=[p('M128 24 V48 M128 208 V232 M24 128 H48 M208 128 H232',sw=4)]
    elif i==5: m=[r(28,28,200,200,'none',24,INK,4)]; a=[r(42,42,172,172,'none',17,BLUE,3,stroke_dasharray='8 6')]; d=[p('M101 128 H155 M128 101 V155',sw=2)]
    elif i==6: m=[r(26,51,204,154,'none',8,INK,4)]; a=[r(47,75,56,36,'none',4,BLUE,4),r(142,113,66,66,'none',8,MINT,4)]; d=[l(47,66,84,66),l(142,104,178,104)]
    elif i==7: m=[p('M28 48 H228 V208 H28 Z','none',INK,4)]; a=[p('M28 48 H228 V77 H28 Z',BLUE),p('M28 179 H228 V208 H28 Z',LILAC)]; d=[c(43,61,5,PINK),txt(72,67,'LIVE',13),txt(186,199,'HD',15)]
    elif i==8: m=[c(128,128,82,'none',INK,4)]; a=[p('M128 26 V47 M128 209 V230 M26 128 H47 M209 128 H230',stroke=BLUE,sw=8)]; d=[p('M128 80 L164 101 V143 L128 164 L92 143 V101 Z','none',LILAC,5)]
    elif i==9: m=[r(28,47,200,164,'none',6,INK,4)]; a=[p('M47 47 L145 211',stroke=BLUE,sw=3),p('M28 114 L228 189',stroke=LILAC,sw=3),p('M96 47 L228 130',stroke=MINT,sw=3)]; d=[c(114,148,10,'none',INK,2)]
    elif i==10: m=[p('M31 69 V31 H69 M187 31 H225 V69 M31 187 V225 H69 M187 225 H225 V187',sw=5)]; a=[l(48,128,208,128,BLUE,5)]; d=[p('M85 128 V104 M128 128 V93 M171 128 V104',sw=3),txt(128,158,'LEVEL',13)]
    elif i==11: m=[r(29,52,198,151,'none',10,INK,4)]; a=[r(46,70,48,22,MINT,4),r(181,70,29,22,CREAM,4)]; d=[txt(70,86,'AF',13),txt(196,86,'4K',12),p('M101 111 H154 V159 H101 Z','none',BLUE,4),lines(49,183,87,1)]
    elif i==12: m=[r(28,28,200,200,'none',0,INK,4)]; a=[r(52,52,152,152,'none',0,BLUE,3),r(77,77,102,102,'none',0,LILAC,3)]; d=[l(128,116,128,140),l(116,128,140,128)]
    elif i==13: m=[c(128,128,98,'none',INK,4)]; a=[p('M128 30 L185 62 L185 194 L128 226 L71 194 L71 62 Z','none',BLUE,4)]; d=[p('M31 128 H225 M128 31 V225',sw=2,stroke_dasharray='4 7')]
    elif i==14: m=[r(23,51,210,154,'none',10,INK,4)]; a=[p('M23 164 H233 V205 H23 Z',BLUE)]; d=[p('M39 184 H108 M40 176 V193 M57 179 V193 M75 176 V193 M91 179 V193',sw=2),txt(181,190,'1/60',15)]
    elif i==15: m=[p('M25 60 H231 V196 H25 Z','none',INK,4)]; a=[p('M25 60 H231 V83 H25 Z',LILAC)]; d=[p('M47 123 H74 L88 103 L105 149 L123 112 L144 158 L162 116 L177 135 H207',stroke=BLUE,sw=4),txt(186,76,'WAVE',10)]
    elif i==16: m=[r(28,46,200,164,'none',10,INK,4)]; a=[r(49,72,19,40,BLUE,3),r(79,96,19,60,LILAC,3),r(109,87,19,77,MINT,3),r(139,73,19,56,PEACH,3),r(169,87,19,85,PINK,3)]; d=[txt(128,194,'EXPOSURE',13)]
    elif i==17: m=[p('M31 70 V31 H70 M186 31 H225 V70 M31 186 V225 H70 M186 225 H225 V186',stroke=BLUE,sw=6)]; a=[c(128,128,70,'none',INK,3,stroke_dasharray='5 6')]; d=[c(128,128,10,PEACH),txt(128,214,'TRACK',13)]
    elif i==18: m=[r(24,61,208,134,'none',12,INK,4)]; a=[p('M24 61 H232 V87 H24 Z',BLUE)]; d=[c(128,141,25,'none',LILAC,5),p('M128 104 V119 M128 163 V178 M91 141 H106 M150 141 H165',sw=3),txt(191,79,'16:9',12)]
    else: m=[p('M31 84 V31 H84 M172 31 H225 V84 M31 172 V225 H84 M172 225 H225 V172',stroke=BLUE,sw=6)]; a=[poly([(92,75),(160,75),(181,112),(160,181),(92,181),(71,112)],'none',INK,3)]; d=[p('M92 75 L140 112 L71 112 M160 75 L140 112 L181 112 M160 181 L140 112 L92 181',stroke=LILAC,sw=4)]
    return finish(m,a,d)

def devices(i):
    m=[]; a=[]; d=[]
    if i==0: m=[r(67,20,122,216,INK,22),r(75,28,106,200,BLUE,17)]; a=[r(107,32,42,10,INK,5),r(111,216,34,4,INK,2)]; d=[r(90,65,76,62,CREAM,9),lines(91,155,70,3,19)]
    elif i==1: m=[r(36,23,184,210,INK,18),r(45,33,166,189,BLUE,12)]; a=[c(128,226,3,CREAM)]; d=[r(59,49,138,52,CREAM,8),r(59,116,63,81,LILAC,8),r(136,116,61,81,MINT,8)]
    elif i==2: m=[r(29,45,198,139,INK,10),r(39,55,178,119,BLUE,5),p('M14 184 H242 L226 211 H30 Z',LILAC)]; a=[r(105,189,46,8,CREAM,4)]; d=[r(53,68,150,22,CREAM,6),lines(55,116,123,3,16)]
    elif i==3: m=[r(23,36,210,147,INK,10),r(33,46,190,127,BLUE,5),p('M103 183 H153 L166 218 H90 Z',LILAC),r(74,218,108,13,CREAM,5)]; d=[r(47,60,162,22,CREAM,5),r(48,99,68,58,LILAC,5),r(130,99,78,58,MINT,5)]
    elif i==4: m=[r(92,19,72,218,LILAC,19),r(65,68,126,120,INK,29),r(75,78,106,100,BLUE,22)]; a=[r(190,107,10,31,PEACH,5)]; d=[c(128,128,34,CREAM),p('M128 106 V128 L148 142',sw=4)]
    elif i==5: m=[r(25,52,206,152,INK,17),r(34,61,188,134,BLUE,12)]; a=[c(42,128,5,CREAM)]; d=[r(60,76,146,34,CREAM,8),r(61,128,69,51,MINT,6),r(144,128,62,51,LILAC,6)]
    elif i==6: m=[r(57,25,142,205,INK,10),r(67,37,122,153,CREAM,2)]; a=[c(128,211,8,BLUE)]; d=[lines(81,60,94,8,14)]
    elif i==7: m=[p('M25 173 V68 L191 39 V176 Z',INK),p('M36 76 L181 50 V160 L36 184 Z',BLUE),p('M25 196 L191 176 L232 191 L65 218 Z',LILAC)]; a=[poly([(106,192),(164,185),(180,192),(123,200)],CREAM)]; d=[p('M52 101 L159 82 M52 129 L153 111 M52 154 L130 141')]
    elif i==8: m=[p('M85 18 L190 49 V239 L85 208 Z',INK),p('M93 29 L180 55 V226 L93 201 Z',BLUE)]; a=[p('M120 39 L155 49 V56 L120 46 Z',INK),p('M119 205 L154 216',stroke=CREAM,sw=3)]; d=[p('M105 75 L168 94 V147 L105 128 Z',CREAM),p('M108 154 L160 170 M108 173 L150 186')]
    elif i==9: m=[r(39,44,178,173,CREAM,8),r(50,55,156,144,BLUE,4)]; a=[p('M192 192 L211 174 L233 196 L214 214 Z',LILAC),p('M173 211 L192 192 L214 214 L189 231 L173 234 Z',PEACH)]; d=[lines(68,78,118,6,18)]
    elif i==10: m=[r(25,73,206,108,INK,20),r(76,86,104,82,BLUE,5)]; a=[c(50,127,14,LILAC),c(207,114,6,PEACH),c(207,141,6,MINT)]; d=[p('M41 127 H59 M50 118 V136',sw=3),poly([(108,103),(108,151),(147,128)],CREAM)]
    elif i==11: m=[r(35,63,186,157,CREAM,7),r(49,78,158,127,BLUE,4),p('M42 50 H214 L221 63 H35 Z',LILAC)]; a=[r(61,21,135,29,PEACH,6)]; d=[p('M66 86 H190 M66 108 H190 M66 130 H190 M66 152 H164 M66 174 H181',sw=3)]
    elif i==12: m=[r(52,54,152,170,CREAM,9),r(73,27,110,159,BLUE,6),r(66,186,124,19,LILAC,4)]; a=[c(182,211,4,MINT)]; d=[lines(87,55,82,6,18)]
    elif i==13: m=[r(73,22,110,212,INK,20),r(80,31,96,194,BLUE,14)]; a=[p('M84 131 H172 V209 H84 Z',LILAC)]; d=[r(94,56,69,55,CREAM,8),p('M102 139 H154 M102 160 H154 M102 181 H134'),l(85,126,171,126,INK,4)]
    elif i==14: m=[r(31,76,194,134,INK,19),r(42,86,172,114,BLUE,10),p('M56 76 L81 46 H136 L153 76 Z',LILAC)]; a=[c(130,143,44,CREAM),c(130,143,28,LILAC)]; d=[c(130,143,12,BLUE),r(48,101,22,11,PEACH,3)]
    elif i==15: m=[r(30,83,196,91,CREAM,23),r(49,99,64,55,BLUE,19),r(142,99,64,55,LILAC,19),p('M112 116 Q128 99 143 116',stroke=INK,sw=8)]; a=[p('M38 83 L56 58 H201 L220 83 Z',MINT)]; d=[p('M48 174 L70 193 M208 174 L186 193',sw=5)]
    elif i==16: m=[r(47,23,162,210,INK,15),r(57,34,142,189,BLUE,10)]; a=[r(71,161,112,41,CREAM,7)]; d=[c(128,91,39,LILAC),c(128,91,24,CREAM),p('M84 177 H172 M84 188 H150')]
    elif i==17: m=[r(51,47,154,173,CREAM,10),p('M76 47 V28 H180 V47',LILAC),r(63,66,130,73,BLUE,8)]; a=[r(69,155,118,46,MINT,7)]; d=[txt(128,112,'READY',18),p('M86 173 H170 M86 186 H147')]
    elif i==18: m=[r(29,91,198,112,INK,16),r(44,104,168,86,BLUE,9),p('M100 91 V45 H157 V91',LILAC),r(86,29,85,26,CREAM,6)]; a=[c(184,74,12,PEACH)]; d=[p('M63 128 H193 M63 151 H157 M63 174 H176')]
    else: m=[r(29,73,93,121,INK,12),r(134,73,93,121,INK,12),r(37,82,77,103,BLUE,8),r(142,82,77,103,LILAC,8)]; a=[p('M122 127 H134',stroke=PEACH,sw=8)]; d=[r(48,99,55,34,CREAM,6),r(153,99,55,34,CREAM,6),lines(49,153,44,2,14),lines(154,153,44,2,14)]
    return finish(m,a,d)

def workflows(i):
    m=[]; a=[]; d=[]
    if i==0: m=[r(44,56,168,144,BLUE,24)]; a=[r(66,82,123,93,CREAM,16)]; d=[p('M88 111 H167 M88 137 H149',sw=4)]
    elif i==1: m=[poly([(128,26),(230,128),(128,230),(26,128)],LILAC)]; a=[poly([(128,54),(202,128),(128,202),(54,128)],CREAM)]; d=[txt(128,139,'?',38)]
    elif i==2: m=[r(25,80,206,96,MINT,48)]; a=[c(76,128,29,CREAM),c(179,128,29,CREAM)]; d=[arrow(109,128,145,128,INK,3,10),txt(76,138,'1',27),txt(179,138,'2',27)]
    elif i==3: m=[r(35,69,186,134,BLUE,3),e(128,69,93,35,BLUE),e(128,203,93,35,BLUE)]; a=[p('M36 109 Q128 164 220 109',stroke=CREAM,sw=4)]; d=[p('M36 152 Q128 207 220 152',sw=3)]
    elif i==4: m=[p('M52 52 H230 L204 204 H26 Z',LILAC)]; a=[p('M71 76 H204 L186 179 H51 Z',CREAM)]; d=[p('M86 103 H173 M81 127 H168 M77 150 H135')]
    elif i==5: m=[r(34,39,188,153,BLUE,8),p('M34 192 Q74 163 128 192 Q182 221 222 192 V39 H34 Z',BLUE)]; a=[r(49,56,158,40,CREAM,5)]; d=[lines(55,122,139,3,19)]
    elif i==6: m=[c(128,128,91,MINT)]; a=[c(128,128,69,CREAM)]; d=[poly([(109,90),(109,166),(170,128)],LILAC)]
    elif i==7: m=[r(35,55,186,147,BLUE,8)]; a=[p('M55 55 V202 M201 55 V202',stroke=INK,sw=3)]; d=[lines(80,91,97,4,23)]
    elif i==8: m=[poly(points(6,rad=104,rot=-30),LILAC)]; a=[c(128,128,58,CREAM)]; d=[p('M94 128 H162 M128 94 V162',sw=6)]
    elif i==9: m=[c(128,48,26,BLUE),r(25,168,65,57,MINT,9),r(166,168,65,57,LILAC,9)]; a=[p('M128 74 V123 H57 V168 M128 123 H199 V168',sw=4)]; d=[txt(57,205,'A',22),txt(199,205,'B',22)]
    elif i==10: m=[r(28,41,62,53,BLUE,10),r(165,41,62,53,LILAC,10),r(96,168,65,56,MINT,10)]; a=[p('M59 94 V126 H128 V168 M196 94 V126 H128',sw=4)]; d=[tinycheck(128,196,23)]
    elif i==11: m=[c(49,128,27,BLUE),r(95,28,66,57,LILAC,10),r(95,171,66,57,MINT,10),c(208,128,27,PEACH)]; a=[p('M76 128 H87 V57 H95 M87 128 V199 H95 M161 57 H172 V128 H181 M161 199 H172 V128',sw=3)]; d=[txt(128,65,'A',22),txt(128,207,'B',22)]
    elif i==12: m=[r(25,88,58,79,BLUE,12),r(99,88,58,79,LILAC,12),r(173,88,58,79,MINT,12)]; a=[arrow(83,128,99,128,INK,3,7),arrow(157,128,173,128,INK,3,7)]; d=[txt(54,137,'1',24),txt(128,137,'2',24),txt(202,137,'3',24)]
    elif i==13: m=[c(128,128,31,CREAM)]+[c(x,y,24,COLORS[k]) for k,(x,y) in enumerate([(128,35),(217,97),(181,207),(75,207),(39,97)])]; a=[l(128,128,x,y,INK,3) for x,y in [(128,35),(217,97),(181,207),(75,207),(39,97)]]; d=[c(128,128,16,LILAC)]
    elif i==14: m=[r(25,41,65,58,BLUE,10),r(164,157,66,58,MINT,10)]; a=[p('M90 70 H195 V157 M164 186 H57 V99',sw=4)]; d=[poly([(187,145),(195,157),(203,145)],INK,INK,1),poly([(49,111),(57,99),(65,111)],INK,INK,1),txt(58,78,'IN',18),txt(197,194,'OUT',15)]
    elif i==15: m=[r(29,29,65,57,BLUE,10),r(161,29,65,57,LILAC,10),poly([(128,105),(180,157),(128,210),(76,157)],MINT)]; a=[p('M62 86 V157 H76 M194 86 V157 H180',sw=4)]; d=[txt(128,170,'?',29)]
    elif i==16: m=[r(28,29,199,58,BLUE,9),r(28,108,84,58,LILAC,9),r(143,108,84,58,MINT,9),r(70,191,115,41,PEACH,9)]; a=[p('M128 87 V98 H70 V108 M128 98 H185 V108 M70 166 V180 H128 V191 M185 166 V180 H128',sw=3)]; d=[lines(48,58,148,1)]
    elif i==17: m=[c(55,55,26,BLUE),c(201,55,26,LILAC),c(55,201,26,MINT),c(201,201,26,PEACH)]; a=[p('M81 55 H175 M201 81 V175 M175 201 H81 M55 175 V81',sw=4)]; d=[c(128,128,25,CREAM),p('M111 128 H145 M128 111 V145',sw=3)]
    elif i==18: m=[r(75,28,106,50,BLUE,10),r(28,109,77,53,LILAC,10),r(151,109,77,53,MINT,10),r(75,194,106,38,PEACH,10)]; a=[p('M128 78 V91 H66 V109 M128 91 H190 V109 M66 162 V182 H128 V194 M190 162 V182 H128',sw=3)]; d=[txt(128,60,'INPUT',16),txt(128,219,'RESULT',15)]
    else: m=[r(23,98,55,62,BLUE,10),c(128,128,33,LILAC),r(178,98,55,62,MINT,10)]; a=[arrow(78,128,95,128,INK,3,7),arrow(161,128,178,128,INK,3,7)]; d=[p('M128 96 V49 H51 V98 M128 160 V209 H205 V160',sw=3),tinycheck(205,129,21)]
    return finish(m,a,d)

def comparisons(i):
    m=[]; a=[]; d=[]
    if i==0: m=[r(27,59,84,138,BLUE,12),r(145,59,84,138,LILAC,12)]; a=[c(128,128,24,CREAM)]; d=[txt(128,134,'VS',16),lines(43,96,50,3,28),lines(161,96,50,3,28)]
    elif i==1: m=[p('M58 42 H29 V214 H58 M198 42 H227 V214 H198',stroke=BLUE,sw=8)]; a=[arrow(65,128,191,128,INK,4,11)]; d=[txt(128,106,'COMPARE',13)]
    elif i==2: m=[p('M95 30 Q65 30 65 67 V91 Q65 114 43 128 Q65 141 65 165 V189 Q65 226 95 226 M161 30 Q191 30 191 67 V91 Q191 114 213 128 Q191 141 191 165 V189 Q191 226 161 226',stroke=LILAC,sw=9)]; d=[c(128,96,8,BLUE),c(128,128,8,MINT),c(128,160,8,PEACH)]
    elif i==3: m=[r(29,42,198,172,CREAM,10)]; a=[r(29,42,99,172,BLUE,10),p('M128 42 V214',stroke=INK,sw=4)]; d=[p('M55 99 L79 123 L108 78',sw=5),p('M150 86 L200 136 M200 86 L150 136',sw=5),txt(78,188,'YES',19),txt(176,188,'NO',19)]
    elif i==4: m=[r(31,28,194,82,BLUE,10),r(31,146,194,82,LILAC,10)]; a=[arrow(128,110,128,146,INK,3,9)]; d=[lines(56,56,145,3,14),lines(56,174,145,3,14)]
    elif i==5: m=[r(25,68,78,120,BLUE,9),r(153,68,78,120,MINT,9)]; a=[p('M116 111 H140 M116 145 H140',stroke=INK,sw=6)]; d=[txt(64,139,'A',31),txt(192,139,'B',31)]
    elif i==6: m=[r(24,41,92,174,BLUE,8),r(140,41,92,174,LILAC,8)]; a=[p('M24 41 H116 V75 H24 Z',MINT),p('M140 41 H232 V75 H140 Z',PEACH)]; d=[txt(70,65,'BEFORE',11),txt(186,65,'AFTER',12),lines(41,108,58,4,24),tinycheck(184,140,42)]
    elif i==7: m=[p('M33 44 H96 M33 44 V213 H96 M160 44 H223 M223 44 V213 H160',stroke=INK,sw=6)]; a=[c(80,128,28,BLUE),c(176,128,28,LILAC)]; d=[arrow(108,128,148,128,INK,3,9)]
    elif i==8: m=[p('M26 76 H95 V47 L134 128 L95 209 V180 H26 Z',BLUE),p('M230 76 H161 V47 L122 128 L161 209 V180 H230 Z',LILAC)]; d=[c(128,128,17,CREAM)]
    elif i==9: m=[c(83,128,68,BLUE),c(173,128,68,LILAC,INK,3,opacity='.86')]; a=[p('M128 77 A68 68 0 0 1 128 179 A68 68 0 0 1 128 77 Z',MINT)]; d=[txt(66,135,'A',24),txt(191,135,'B',24)]
    elif i==10: m=[r(27,39,202,178,CREAM,9)]; a=[r(39,52,77,152,BLUE,6),r(139,52,77,152,LILAC,6)]; d=[p('M53 99 H102 M53 140 H102 M153 99 H202 M153 140 H202',sw=3),c(78,182,13,MINT),c(178,182,13,PEACH)]
    elif i==11: m=[p('M38 39 H128 V217 H38 Z',BLUE),p('M128 39 H218 V217 H128 Z',LILAC)]; a=[p('M128 39 L112 60 L144 83 L112 107 L144 132 L112 155 L144 181 L128 217',stroke=CREAM,sw=7)]; d=[lines(54,87,46,3,34),lines(159,87,43,3,34)]
    elif i==12: m=[r(27,57,84,142,BLUE,11),r(145,57,84,142,LILAC,11)]; a=[p('M66 28 V48 M66 209 V229 M188 28 V48 M188 209 V229',sw=3)]; d=[p('M45 113 L63 131 L93 94',sw=5),p('M163 111 L209 147 M209 111 L163 147',sw=5)]
    elif i==13: m=[p('M30 199 H226 M128 199 V45',sw=5)]; a=[p('M67 80 L25 152 H109 Z',BLUE),p('M189 103 L147 175 H231 Z',LILAC)]; d=[p('M67 80 L67 50 L189 73 V103',sw=4),c(128,62,9,PEACH),r(101,209,54,20,MINT,5)]
    elif i==14: m=[r(26,31,89,194,BLUE,6),r(141,31,89,194,LILAC,6)]; a=[p('M26 80 H115 M141 80 H230',sw=3)]; d=[txt(70,63,'PROS',15),txt(185,63,'CONS',15)]+[tinycheck(43,y,12)+l(57,y,99,y) for y in (111,153,195)]+[l(157,y,170,y,INK,3)+l(179,y,215,y) for y in (111,153,195)]
    elif i==15: m=[r(29,31,198,194,CREAM,7)]; a=[r(42,44,172,43,BLUE,6),r(42,106,79,102,MINT,6),r(136,106,78,102,PEACH,6)]; d=[txt(128,72,'OPTIONS',17),txt(81,166,'A',31),txt(175,166,'B',31)]
    elif i==16: m=[p('M31 65 H225 V102 H31 Z',BLUE),p('M31 151 H225 V188 H31 Z',LILAC)]; a=[arrow(56,112,56,141,INK,3,9),arrow(199,141,199,112,INK,3,9)]; d=[txt(128,91,'PLAN A',20),txt(128,178,'PLAN B',20)]
    elif i==17: m=[r(25,60,92,136,BLUE,10),r(139,60,92,136,LILAC,10)]; a=[p('M51 37 H204 M51 218 H204',stroke=MINT,sw=7)]; d=[p('M44 95 H100 M44 124 H87 M44 154 H102 M157 95 H213 M157 124 H200 M157 154 H213')]
    elif i==18: m=[c(69,128,46,BLUE),c(188,128,46,LILAC)]; a=[p('M73 63 Q128 22 186 63 M73 193 Q128 234 186 193',stroke=MINT,sw=6)]; d=[arrow(98,128,157,128,INK,4,10),txt(69,137,'1',25),txt(188,137,'2',25)]
    else: m=[r(30,42,196,171,CREAM,6)]; a=[p('M30 42 H226 V78 H30 Z',BLUE),p('M95 78 V213 M161 78 V213',sw=3)]; d=[txt(62,67,'ITEM',12),txt(128,67,'A',15),txt(194,67,'B',15),p('M30 123 H226 M30 168 H226',sw=2),tinycheck(128,100,17),tinycheck(194,145,17),tinycheck(128,190,17)]
    return finish(m,a,d)

def collage(i):
    m=[]; a=[]; d=[]
    if i==0: m=[r(38,25,180,211,CREAM,0),r(49,39,158,151,BLUE,0)]; a=[r(80,16,96,24,PEACH,2,transform='rotate(-5 128 28)')]; d=[l(82,216,178,216)]
    elif i==1: m=[r(27,58,202,143,BLUE,0)]; a=[r(19,50,72,30,PEACH,1,transform='rotate(-20 55 65)'),r(171,181,72,30,LILAC,1,transform='rotate(-20 207 196)')]; d=[l(33,67,221,67,WHITE,3)]
    elif i==2: m=[p('M29 42 L70 37 L108 43 L146 37 L185 44 L228 40 L221 78 L229 114 L221 152 L228 190 L224 226 L186 220 L146 227 L108 219 L68 225 L28 218 L35 182 L27 144 L35 105 L29 69 Z',CREAM)]; a=[r(46,59,164,138,BLUE,0)]; d=[l(74,208,180,208)]
    elif i==3: m=[r(22,36,212,187,CREAM,0)]; a=[r(33,48,89,69,BLUE,0),r(134,48,89,69,LILAC,0),r(33,135,89,69,MINT,0),r(134,135,89,69,PEACH,0)]; d=[dotrow(35,30,6,28,INK)]
    elif i==4: m=[r(40,27,176,206,BLUE,0)]; a=[p('M40 27 H216 V59 H40 Z',INK),p('M40 201 H216 V233 H40 Z',INK)]; d=[r(49+k*32,y,16,14,CREAM,1) for y in (35,210) for k in range(5)]
    elif i==5: m=[r(27,41,202,174,CREAM,0)]; a=[p('M27 41 L96 58 L229 41 V97 L162 83 L27 102 Z',BLUE),p('M27 164 L93 180 L229 163 V215 H27 Z',LILAC)]; d=[lines(56,117,143,2,18)]
    elif i==6: m=[r(25,55,145,171,CREAM,0,transform='rotate(-10 98 140)'),r(95,26,137,176,CREAM,0,transform='rotate(8 165 114)')]; a=[r(111,42,105,116,BLUE,0,transform='rotate(8 165 114)')]; d=[l(117,176,191,187)]
    elif i==7: m=[p('M34 30 H222 V224 H34 Z',CREAM)]; a=[p('M34 30 H222 V79 H34 Z',INK)]; d=[p('M44 30 L82 79 M83 30 L121 79 M122 30 L160 79 M161 30 L199 79 M200 30 L222 59',stroke=CREAM,sw=12),lines(58,110,139,4,25)]
    elif i==8: m=[p('M23 72 L215 35 L236 172 L45 209 Z',CREAM)]; a=[p('M37 83 L204 51 L220 160 L55 192 Z',BLUE),r(82,190,102,27,PEACH,2,transform='rotate(-11 133 203)')]; d=[l(67,83,132,70,WHITE,3)]
    elif i==9: m=[p('M34 32 H222 V224 H34 Z',CREAM)]; a=[r(47,46,162,152,BLUE,0)]; d=[p('M34 79 H13 V118 H34 M34 150 H13 V189 H34 M222 79 H243 V118 H222 M222 150 H243 V189 H222',MINT),l(90,213,174,213)]
    elif i==10: m=[r(32,41,192,176,CREAM,0)]; a=[r(48,57,161,72,BLUE,0),r(48,144,71,56,LILAC,0),r(134,144,75,56,MINT,0)]; d=[r(79,22,96,26,PEACH,0),p('M91 26 L89 44 M117 26 L115 44 M143 26 L141 44',stroke=WHITE,sw=2)]
    elif i==11: m=[r(25,63,207,143,BLUE,0)]; a=[p('M25 63 H232 V90 H25 Z',INK),p('M25 178 H232 V206 H25 Z',INK)]; d=[r(35+k*27,y,14,14,CREAM,0) for y in (69,184) for k in range(7)]
    elif i==12: m=[p('M37 30 H220 V225 H37 Z',CREAM)]; a=[p('M37 30 H220 V79 H37 Z',LILAC),r(54,94,149,92,BLUE,0)]; d=[c(x,52,5,CREAM) for x in (60,94,128,162,196)]+[l(66,204,193,204)]
    elif i==13: m=[r(28,43,199,171,CREAM,0)]; a=[p('M28 43 L88 43 L28 103 Z',PEACH),p('M227 214 L166 214 L227 153 Z',LILAC),r(57,72,141,113,BLUE,0)]; d=[l(70,92,179,92,WHITE,3)]
    elif i==14: m=[r(39,27,177,209,CREAM,4)]; a=[r(52,41,151,162,BLUE,0),p('M39 236 H216 V207 H39 Z',LILAC)]; d=[txt(128,227,'POSTCARD',12),r(149,53,42,48,PEACH,0),lines(64,132,89,4,15)]
    elif i==15: m=[r(22,53,212,164,CREAM,0)]; a=[r(36,67,198,150,BLUE,0),r(23,43,31,60,PEACH,2,transform='rotate(-24 38 73)'),r(202,164,31,60,LILAC,2,transform='rotate(-24 217 194)')]; d=[p('M47 87 H115 M47 103 H91',stroke=WHITE,sw=3)]
    elif i==16: m=[r(24,30,208,196,CREAM,2)]; a=[r(37,44,116,167,BLUE,0),r(166,44,52,72,LILAC,0),r(166,129,52,82,MINT,0)]; d=[c(45,21,4,INK),c(80,21,4,INK),c(115,21,4,INK),c(150,21,4,INK),c(185,21,4,INK)]
    elif i==17: m=[p('M31 54 H225 V198 H31 Z',CREAM)]; a=[p('M31 54 H225 V93 H31 Z',BLUE)]; d=[p('M62 93 V198 M99 93 V198 M136 93 V198 M173 93 V198 M210 93 V198',stroke=INK,sw=2),p('M31 123 H225 M31 158 H225',sw=2),txt(128,81,'STORYBOARD',13)]
    elif i==18: m=[p('M33 37 L221 32 L225 75 L217 102 L224 146 L216 178 L225 220 L39 225 L44 189 L31 152 L39 117 L31 79 Z',CREAM)]; a=[p('M52 56 H204 V193 H52 Z',BLUE),p('M171 193 L204 160 V193 Z',LILAC)]; d=[p('M172 193 V160 H204',stroke=INK,sw=2)]
    else: m=[r(31,31,194,194,CREAM,0)]; a=[r(44,44,168,73,BLUE,0),r(44,130,73,82,LILAC,0),r(130,130,82,82,MINT,0)]; d=[r(44,24,54,23,PEACH,1),r(176,201,54,23,PINK,1),l(55,152,106,152,WHITE,3)]
    return finish(m,a,d)

def infoblocks(i):
    m=[]; a=[]; d=[]
    if i==0: m=[poly([(128,26),(224,80),(224,177),(128,230),(32,177),(32,80)],BLUE)]; a=[poly([(128,26),(224,80),(128,136),(32,80)],LILAC),poly([(128,136),(224,80),(224,177),(128,230)],MINT)]; d=[l(128,136,128,230)]
    elif i==1: m=[p('M28 93 H98 V29 H159 V93 H228 V157 H159 V227 H98 V157 H28 Z',BLUE)]; a=[r(104,99,49,52,CREAM,8)]; d=[tinycheck(128,126,30)]
    elif i==2: m=[p('M25 213 L81 153 H175 L231 213 Z',BLUE),p('M49 141 L99 88 H157 L207 141 Z',LILAC),p('M85 76 L128 28 L171 76 Z',MINT)]; d=[lines(102,184,55,1),lines(113,119,31,1)]
    elif i==3: m=[r(25,45,63,166,BLUE,8),r(97,45,63,166,LILAC,8),r(169,45,63,166,MINT,8)]; a=[c(56,79,18,CREAM),c(128,79,18,CREAM),c(200,79,18,CREAM)]; d=[txt(56,86,'1',18),txt(128,86,'2',18),txt(200,86,'3',18),lines(41,121,31,4,23),lines(113,121,31,4,23),lines(185,121,31,4,23)]
    elif i==4: m=[c(128,128,96,BLUE)]; a=[p('M128 128 V32 A96 96 0 0 1 211 176 Z',LILAC),p('M128 128 L211 176 A96 96 0 0 1 45 176 Z',MINT)]; d=[c(128,128,35,CREAM)]
    elif i==5: m=[r(32,46,192,170,CREAM,10)]; a=[r(32,46,192,43,BLUE,10),r(47,107,76,93,LILAC,8),r(139,107,70,93,MINT,8)]; d=[txt(128,75,'DASHBOARD',16),lines(62,134,44,3,22),tinycheck(174,154,36)]
    elif i==6: m=[c(128,128,43,CREAM),c(57,55,31,BLUE),c(199,55,31,LILAC),c(57,201,31,MINT),c(199,201,31,PEACH)]; a=[l(86,84,103,103),l(170,84,153,103),l(86,172,103,153),l(170,172,153,153)]; d=[star(5,128,128,24,12,fill=LILAC)]
    elif i==7: m=[p('M25 87 H160 V43 L231 128 L160 213 V169 H25 Z',BLUE)]; a=[r(38,101,33,54,CREAM,4),r(83,101,33,54,LILAC,4),r(128,101,33,54,MINT,4)]; d=[txt(54,137,'1',21),txt(99,137,'2',21),txt(144,137,'3',21)]
    elif i==8: m=[r(31,31,194,194,CREAM,11)]; a=[r(48,48,162,57,BLUE,8),r(48,121,69,87,LILAC,8),r(132,121,78,87,MINT,8)]; d=[lines(64,72,125,2,17),txt(82,175,'A',29),txt(171,175,'B',29)]
    elif i==9: m=[p('M41 36 H215 V87 H41 Z',BLUE),p('M41 104 H215 V156 H41 Z',LILAC),p('M41 174 H215 V225 H41 Z',MINT)]; a=[c(66,61,15,CREAM),c(66,129,15,CREAM),c(66,199,15,CREAM)]; d=[txt(66,66,'1',14),txt(66,134,'2',14),txt(66,204,'3',14),lines(93,61,102,1),lines(93,129,102,1),lines(93,199,102,1)]
    elif i==10: m=[poly([(128,29),(224,81),(224,177),(128,229),(32,177),(32,81)],BLUE)]; a=[poly([(128,50),(202,92),(202,165),(128,207),(54,165),(54,92)],CREAM)]; d=[lines(82,111,93,3,22)]
    elif i==11: m=[p('M24 147 L79 92 L130 147 L181 92 L232 147 V211 H24 Z',BLUE)]; a=[p('M24 147 L79 92 L79 211 H24 Z',LILAC),p('M130 147 L181 92 L181 211 H130 Z',MINT)]; d=[arrow(51,69,205,69,INK,3,11)]
    elif i==12: m=[r(25,55,206,147,CREAM,10)]; a=[p('M25 55 H92 V202 H25 Z',BLUE)]; d=[txt(60,142,'01',32),lines(111,85,99,5,23)]
    elif i==13: m=[p('M31 40 H225 V102 H158 V156 H92 V214 H31 Z',BLUE)]; a=[p('M225 102 H158 V156 H92 V214 H225 Z',LILAC)]; d=[txt(72,86,'A',24),txt(182,190,'B',24),arrow(117,84,165,130,INK,3,10)]
    elif i==14: m=[r(25,83,206,110,BLUE,55)]; a=[c(81,138,42,CREAM),r(144,109,65,56,LILAC,8)]; d=[txt(81,149,'75',34),lines(154,126,42,2,17)]
    elif i==15: m=[poly([(128,26),(222,187),(34,187)],BLUE)]; a=[poly([(128,64),(188,169),(68,169)],CREAM),r(47,203,162,28,LILAC,8)]; d=[star(5,128,128,26,11,fill=MINT)]
    elif i==16: m=[r(25,30,97,92,BLUE,12),r(136,30,97,92,LILAC,12),r(25,137,97,92,MINT,12),r(136,137,97,92,PEACH,12)]; a=[c(74,76,23,CREAM),c(184,76,23,CREAM),c(74,183,23,CREAM),c(184,183,23,CREAM)]; d=[txt(74,84,'1',21),txt(184,84,'2',21),txt(74,191,'3',21),txt(184,191,'4',21)]
    elif i==17: m=[p('M28 64 H190 L228 128 L190 192 H28 Z',BLUE)]; a=[p('M28 64 H80 L117 128 L80 192 H28 Z',LILAC),p('M80 64 H132 L169 128 L132 192 H80 L117 128 Z',MINT)]; d=[txt(57,136,'1',22),txt(109,136,'2',22),txt(176,136,'3',22)]
    elif i==18: m=[r(25,26,206,205,CREAM,11)]; a=[r(39,40,178,35,BLUE,6),r(39,89,55,128,LILAC,7),r(108,89,109,55,MINT,7),r(108,158,109,59,PEACH,7)]; d=[lines(56,57,143,1),lines(53,115,25,4,23),lines(124,111,78,2,17),lines(124,180,78,2,17)]
    else: m=[c(128,128,93,BLUE)]; a=[p('M128 128 V35 A93 93 0 0 1 221 128 Z',LILAC),p('M128 128 H35 A93 93 0 0 0 128 221 Z',MINT)]; d=[c(128,128,32,CREAM),txt(128,137,'360',22)]
    return finish(m,a,d)

def progress(i):
    m=[]; a=[]; d=[]
    if i==0: m=[r(27,103,202,50,CREAM,25)]; a=[r(35,111,134,34,BLUE,17)]; d=[c(171,128,18,LILAC)]
    elif i==1: m=[c(128,128,85,'none',CREAM,20)]; a=[p('M128 43 A85 85 0 1 1 43 128',stroke=BLUE,sw=20)]; d=[txt(128,140,'75%',34)]
    elif i==2: m=[r(85,24,86,208,CREAM,43)]; a=[r(94,107,68,116,MINT,34)]; d=[txt(128,85,'60',27)]
    elif i==3: m=[r(24,103,208,50,CREAM,8)]; a=[r(32+k*39,111,30,34,COLORS[k],4) for k in range(4)]; d=[r(188,111,30,34,'none',4,INK,2)]
    elif i==4: m=[p('M39 184 A89 89 0 0 1 217 184',stroke=CREAM,sw=25)]; a=[p('M39 184 A89 89 0 0 1 172.5 106.92',stroke=MINT,sw=25)]; d=[txt(128,166,'READY',20)]
    elif i==5: m=[l(34,128,222,128,INK,5)]; a=[c(34,128,17,BLUE),c(96,128,17,LILAC),c(159,128,17,MINT),c(222,128,17,CREAM)]; d=[tinycheck(34,128,15),tinycheck(96,128,15),txt(159,134,'3',15)]
    elif i==6: m=[r(73,34,111,188,CREAM,8),r(110,21,37,13,LILAC,4)]; a=[r(83,151,91,58,MINT,3),r(83,91,91,48,BLUE,3),r(83,47,91,32,LILAC,3)]; d=[p('M135 72 L111 126 H135 L121 184 L155 109 H131 Z',PEACH)]
    elif i==7: m=[c(128,128,90,'none',BLUE,13),c(128,128,66,'none',LILAC,13),c(128,128,42,'none',MINT,13)]; a=[p('M128 38 A90 90 0 0 1 218 128',stroke=CREAM,sw=13),p('M128 62 A66 66 0 0 1 128 194',stroke=CREAM,sw=13)]; d=[c(128,128,10,PEACH)]
    elif i==8: m=[r(72,23,112,210,CREAM,56)]; a=[c(128,177,43,PINK),r(116,48,24,121,PINK,12)]; d=[p('M83 78 H101 M83 112 H101 M83 146 H101')]
    elif i==9: m=[c(128,128,90,CREAM)]; a=[p('M128 128 V38 A90 90 0 1 1 38 128 Z',BLUE)]; d=[c(128,128,27,LILAC),txt(128,137,'3/4',22)]
    elif i==10: m=[r(25,82,206,92,CREAM,10)]; a=[r(36,93,126,70,BLUE,5)]; d=[txt(128,138,'62%',29),p('M174 93 V163 M192 93 V163 M210 93 V163',sw=2)]
    elif i==11: m=[poly(points(6,rad=102,rot=-30),'none',CREAM,18)]; a=[p('M128 26 L216 77 V179 L128 230 L40 179',stroke=LILAC,sw=18)]; d=[txt(128,139,'80%',31)]
    elif i==12: m=[r(45,45,166,166,'none',18,CREAM,18)]; a=[p('M128 45 H193 Q211 45 211 63 V193 Q211 211 193 211 H63 Q45 211 45 193 V128',stroke=BLUE,sw=18)]; d=[txt(128,140,'90%',32)]
    elif i==13: m=[r(27,64,202,127,CREAM,10)]; a=[r(41,110,173,22,BLUE,11),r(41,151,119,22,LILAC,11)]; d=[lines(46,85,123,1),txt(191,169,'68',18)]
    elif i==14: m=[l(128,30,128,227,INK,5)]; a=[c(128,30,18,BLUE),c(128,95,18,LILAC),c(128,161,18,MINT),c(128,227,18,CREAM)]; d=[tinycheck(128,30,16),tinycheck(128,95,16),txt(128,167,'3',15)]
    elif i==15: m=[c(128,128,88,'none',CREAM,12)]; a=[p('M128 40 A88 88 0 0 1 216 128',stroke=BLUE,sw=12)]; d=[c(216,128,14,LILAC),txt(128,140,'LOAD',26)]
    elif i==16: m=[r(28,108,200,40,CREAM,4)]; a=[poly([(36,115),(80,115),(65,141),(36,141)],BLUE),poly([(89,115),(133,115),(118,141),(74,141)],LILAC),poly([(142,115),(186,115),(171,141),(127,141)],MINT)]; d=[txt(128,85,'STEP 3',19)]
    elif i==17: m=[p('M30 213 L64 213 V173 H103 V133 H143 V93 H182 V53 H225',stroke=CREAM,sw=20)]; a=[p('M30 213 L64 213 V173 H103 V133 H143 V93 H182',stroke=BLUE,sw=20)]; d=[c(182,93,14,LILAC)]
    elif i==18: m=[r(27,68,202,119,CREAM,20)]; a=[c(60,128,19,BLUE),c(105,128,19,LILAC),c(150,128,19,MINT),c(195,128,19,'none',INK,3)]; d=[txt(128,93,'PROGRESS',14),tinycheck(60,128,18),tinycheck(105,128,18)]
    else: m=[c(128,128,96,'none',CREAM,15)]; a=[p('M128 32 A96 96 0 1 1 47 180',stroke=MINT,sw=15)]; d=[tinycheck(128,128,71),txt(128,184,'COMPLETE',12)]
    return finish(m,a,d)

def dividers(i):
    m=[]; a=[]; d=[]
    if i==0: m=[l(22,128,101,128,INK,4),l(155,128,234,128,INK,4)]; a=[sparkle(128,128,20,PEACH)]
    elif i==1: m=[p('M23 116 H105 M151 116 H233 M23 140 H105 M151 140 H233',stroke=BLUE,sw=4)]; a=[poly([(128,105),(151,128),(128,151),(105,128)],LILAC)]
    elif i==2: m=[p('M23 145 Q65 96 107 128 M149 128 Q191 96 233 145',stroke=MINT,sw=5)]; a=[p('M107 128 Q128 96 149 128 Q128 160 107 128 Z',PEACH)]
    elif i==3: m=[l(23,128,233,128,INK,3)]; a=[c(71,128,12,BLUE),c(128,128,20,LILAC),c(185,128,12,MINT)]; d=[c(128,128,5,CREAM)]
    elif i==4: m=[p('M22 140 L49 113 L76 140 L103 113 L130 140 L157 113 L184 140 L211 113 L234 137',stroke=BLUE,sw=8)]; a=[c(128,78,5,PEACH)]
    elif i==5: m=[p('M22 151 Q128 75 234 151',stroke=LILAC,sw=6),p('M35 169 Q128 105 221 169',stroke=MINT,sw=3)]; a=[star(5,128,89,22,10,fill=PEACH)]
    elif i==6: m=[l(23,128,89,128,INK,4),l(167,128,233,128,INK,4)]; a=[star(5,105,128,17,8,fill=BLUE),star(5,151,128,17,8,fill=LILAC)]
    elif i==7: m=[p('M22 105 H98 L128 151 L158 105 H234',stroke=BLUE,sw=7)]; a=[c(128,87,14,PEACH)]
    elif i==8: m=[p('M23 130 Q39 103 55 130 Q71 157 87 130 Q103 103 119 130 Q135 157 151 130 Q167 103 183 130 Q199 157 215 130 Q225 111 235 130',stroke=LILAC,sw=7)]
    elif i==9: m=[p('M23 128 H98 M158 128 H233',stroke=INK,sw=4)]; a=[p('M104 145 Q108 118 128 101 Q148 118 152 145 Q128 128 104 145 Z',MINT)]; d=[l(128,106,128,154)]
    elif i==10: m=[p('M23 146 H74 L96 110 H160 L182 146 H233',stroke=BLUE,sw=5)]; a=[r(109,101,38,38,LILAC,3,transform='rotate(45 128 120)')]
    elif i==11: m=[l(23,128,91,128,INK,3),l(165,128,233,128,INK,3)]; a=[c(104,128,7,BLUE),c(128,128,12,LILAC),c(152,128,7,MINT)]
    elif i==12: m=[p('M23 146 C42 79 90 89 94 128 C96 154 62 154 60 134 M233 146 C214 79 166 89 162 128 C160 154 194 154 196 134',stroke=BLUE,sw=5)]; a=[sparkle(128,128,20,PEACH)]
    elif i==13: m=[p('M23 128 H92 M164 128 H233',stroke=INK,sw=3,stroke_dasharray='5 7')]; a=[poly(points(6,cy=128,rad=31,rot=-30),MINT)]; d=[poly(points(6,cy=128,rad=15,rot=-30),CREAM)]
    elif i==14: m=[r(23,117,210,22,BLUE,11)]; a=[r(96,107,64,42,LILAC,21)]; d=[dotrow(112,128,3,16,INK)]
    elif i==15: m=[p('M23 146 L62 107 L101 146 M155 146 L194 107 L233 146',stroke=MINT,sw=6)]; a=[p('M105 130 L128 107 L151 130 L128 153 Z',PEACH)]
    elif i==16: m=[l(23,128,101,128,INK,4),l(155,128,233,128,INK,4)]; a=[p('M128 108 C101 81 88 122 128 150 C168 122 155 81 128 108 Z',PINK)]
    elif i==17: m=[p('M23 112 H101 M155 112 H233 M23 144 H101 M155 144 H233',stroke=INK,sw=3)]; a=[c(128,128,25,CREAM)]; d=[txt(128,135,'01',20)]
    elif i==18: m=[p('M23 144 Q63 113 104 144 M152 144 Q193 113 233 144',stroke=BLUE,sw=6)]; a=[g(e(0,-16,9,19,LILAC),f'translate(128 128) rotate({k*72})') for k in range(5)]; d=[c(128,128,8,PEACH)]
    else: m=[p('M23 128 H233',stroke=BLUE,sw=7)]; a=[poly([(59,128),(79,108),(99,128),(79,148)],LILAC),poly([(157,128),(177,108),(197,128),(177,148)],MINT)]; d=[c(128,128,10,PEACH)]
    return finish(m,a,d)

CATEGORIES=[
 ('Premium frames',frames,'Rounded double frame|Instant photo frame|Circular double ring|Oval gallery frame|Architectural arch frame|Hexagonal gallery frame|Diamond frame|Washi tab frame|Tilted instant frame|Corner bracket frame|Tape top photo frame|Scalloped ornate frame|Browser photo frame|Capsule frame|Folded corner frame|Corner rivet frame|Octagonal frame|Filmstrip frame|Crop corner frame|Four photo frame'),
 ('Photo masks',masks,'Organic blob mask|Tall arch mask|Diamond image mask|Irregular polygon mask|Capsule photo mask|Cut corner photo mask|Notched portrait mask|Fluid silhouette mask|Heart photo mask|Cross shaped mask|Wave bottom mask|Dome image mask|Hexagonal photo mask|Hourglass mask|Soft square mask|Skewed image mask|Petal cloud mask|Deep rounded mask|L shaped photo mask|Ribbon cutout mask'),
 ('Speech and callout panels',callouts,'Left speech bubble|Right speech bubble|Bottom speech bubble|Square corner callout|Left annotation panel|Right annotation panel|Rounded comment bubble|Rounded centered callout|Tilted speech panel|Profile comment panel|Clipped corner comic bubble|Chamfered pointer bubble|Thought cloud bubble|Triangle tail callout|Threaded comment bubble|Long pointer bubble|Header callout panel|Side tab callout|Bracket pointer bubble|Review speech bubble'),
 ('Directional arrows',arrows,'Broad right arrow|Soft elbow arrow|Stepped elbow arrow|Curved turn arrow|Tall upturn arrow|Wide chevron arrow|Inset highlight arrow|Diagonal right arrow|Left pointing arrow|Vertical launch arrow|Rising route arrow|Striped action arrow|Two way decision arrow|Rocket up arrow|Twin line arrow|Three stage arrow|Drop elbow arrow|Rounded pathway arrow|Sweeping up arrow|Fluid forward arrow'),
 ('Route schematics',routes,'S curve journey|Right angle route|Wave journey route|Mountain trail route|Long serpentine route|Staircase route|Horseshoe route|Peak route|Branch loop route|Winding story route|Snake scan route|Crossroads diagram|Tree fork route|Pulse route|Circular station route|Crossing pathways|Gentle ascent route|Switchback hiking route|Hub and ring route|Step ascent route'),
 ('Location markers',markers,'Classic map pin|Star place pin|Verified place callout|Diamond place marker|Hexagon numbered pin|Tapered landmark pin|Profile location marker|Label location marker|Bookmark place marker|Heart location pin|Signal place marker|Cut stone marker|Clock location pin|Checklist place marker|Directory marker|Information card marker|Shield location marker|Radar target marker|Folded place marker|Crosshair location pin'),
 ('Glass UI cards',glasscards,'Profile glass card|Analytics glass card|Success glass card|Bento glass layout|Activity list card|Video glass card|Metric glass card|Browser glass card|Chat glass card|Checklist glass card|Dashboard glass panel|Reward glass card|Dual metric card|Status conversation card|Stacked notification card|Play glass panel|Approval options card|Growth glass panel|Sidebar glass layout|Team glass card'),
 ('Chart components',charts,'Three bar chart|Connected line chart|Three slice pie|Percent donut ring|Area growth chart|Horizontal bar chart|Radar polygon chart|Ascending step bars|Bubble comparison chart|Scatter trend chart|Stacked column chart|Needle gauge chart|Three stage funnel|Waterfall bars|Diverging bar chart|Dual curve chart|Candlestick chart|Concentric segment chart|Treemap chart|Distribution chart'),
 ('Data matrices',matrices,'Four quadrant matrix|Table grid|Diagonal priority matrix|Decision check matrix|Triangular split matrix|Strategy quadrant matrix|Bubble matrix|Sidebar data matrix|Hexagon sectors|Bento data matrix|Choice quadrant matrix|Ranked row matrix|Letter header table|Magnitude matrix|Circular quadrant matrix|Overlapping axis matrix|Option summary matrix|Heatmap grid|Diamond quadrant matrix|Asymmetric bento matrix'),
 ('Planner widgets',planners,'Monthly calendar|Kanban planner|Daily checklist|Timeline schedule|Clock planner|Time appointment card|Milestone timeline|Habit tracker|Weekly capacity planner|Goal radar planner|Thirty day tracker|Booking timetable|Two column checklist|Focus task card|Checked task list|Pomodoro clock|Numbered agenda|Milestone planner|Priority lanes|Meeting agenda'),
 ('Commerce badges',badges,'Price hang tag|Sale burst badge|VIP capsule badge|Award ribbon badge|Coupon ticket|New hexagon badge|Price receipt|Offer card|Folded value tag|Premium shield|Approved ribbon seal|Special edition ticket|Member pass|Pro medal badge|Limited polygon badge|Bundle square badge|Verified seal|Access shield|Lifetime access pass|Digital download tag'),
 ('CTA buttons',ctas,'Start pill button|Raised explore button|Next chevron button|Double framed open button|Outlined go button|Get download button|Play pill button|Chamfered join button|Done icon button|Create corner button|Shop cart button|Glass continue button|Try sparkle button|Learn tab button|Download outline button|Folded save button|Send envelope button|More menu button|Dashed select button|Layered build button'),
 ('Particle clusters',particles,'Dot sparkle cluster|Star confetti cluster|Ring bubble cluster|Radial ray burst|Paper confetti cluster|Arc sparkle cluster|Geometry particle set|Diamond sparkle cluster|Arch trail particles|Wave bead particles|Celebration rays|Rectangle confetti|Cloud bubble cluster|Orbital eye cluster|Diagonal spark streaks|Arc corner confetti|Connected bead trail|Sparkle orbit|Curled particle trail|Triangle confetti'),
 ('Abstract ornaments',abstract,'Layered organic blob|Fluid bean ornament|Petal cloud ornament|Cross geometry ornament|Twin mountain ornament|Layered wave block|Venn petal ornament|Comb geometry ornament|Stepped flag ornament|Fan triangle ornament|Descending staircase block|Octagonal layered target|Four pointed fluid star|Rainbow arch ornament|Striped E block|Intersecting stepped block|Layered ellipse target|Nested triangle ornament|Interlocking ribbon block|Modular step ornament'),
 ('Papercut flowers',flowers,'Papercut daisy|Papercut tulip|Layered rose|Lotus blossom|Sunflower bloom|Cherry blossom|Hibiscus bloom|Orchid blossom|Bellflower bloom|Poppy blossom|Lavender stem|Cotton blossom|Dandelion seed head|Chrysanthemum blossom|Anthurium flower|Hydrangea cluster|Magnolia blossom|Peony blossom|Daffodil bloom|Protea head'),
 ('Botanical leaves',leaves,'Fern frond|Palm crown|Monstera leaf|Ginkgo leaf|Oak leaf|Maple leaf|Eucalyptus branch|Olive branch|Banana leaf|Ivy leaf|Philodendron leaf|Aloe plant|Lotus leaf|Curled leaf|Feather frond|Succulent rosette|Wheat stem|Decorative leaf branch|Bamboo stems|Pine sprig'),
 ('Speed line overlays',speedlines,'Horizontal rush lines|Converging rush lines|Radial speed burst|Arc rush lines|Corner sweep lines|Stepped rush lines|Broken sprint lines|Nested arc trails|Center impact rays|Diagonal sprint trails|Lightning speed line|Wave speed lines|Inward focus rays|Bent chase trails|U turn motion trails|Perspective speed taper|Zigzag rush trails|Dashed lane rush|Side curve trails|Angular impact lines'),
 ('Camera overlays',camera,'Focus corner brackets|Record viewfinder|Target reticle|Rule of thirds grid|Circular target reticle|Safe area frame|Dual focus boxes|Live recording frame|Hexagonal focus overlay|Diagonal composition grid|Horizon level overlay|Autofocus status frame|Nested crop squares|Compass target overlay|Shutter speed overlay|Waveform monitor frame|Exposure monitor frame|Tracking reticle|Widescreen target|Aperture focus overlay'),
 ('Device mockups',devices,'Phone front mockup|Tablet portrait mockup|Laptop front mockup|Desktop monitor|Smartwatch mockup|Tablet landscape mockup|E reader mockup|Perspective laptop|Perspective phone|Drawing tablet|Portable game console|Paper printer|Receipt terminal|Foldable phone mockup|Camera mockup|VR headset mockup|Smart speaker display|Kiosk mockup|Projection monitor|Dual screen mockup'),
 ('Workflow nodes',workflows,'Process node|Decision diamond|Start and end capsule|Database cylinder|Input output node|Document node|Play workflow node|Subprocess panel|Hexagonal operation node|Branch workflow|Merge workflow|Parallel workflow|Three step workflow|Radial hub workflow|Feedback loop workflow|Dual source decision|Three level workflow|Four node cycle|Input output merge|Looped pipeline'),
 ('Comparison guides',comparisons,'Versus panels|Outer comparison brackets|Curly comparison braces|Yes no comparison|Vertical transformation panels|Equals panels|Before after panels|Bracketed transformation|Opposing arrows|Shared feature Venn|Feature comparison cards|Torn split comparison|Check cross panels|Balance scale comparison|Pros cons panels|Option comparison card|Two way plan comparison|Framed comparison panels|Circular exchange comparison|Three column feature table'),
 ('Film and collage',collage,'Taped instant photo|Corner tape collage|Torn paper photo|Four print collage|Portrait film frame|Paper strip collage|Overlapping photo stack|Clapper board card|Tilted taped photo|Tab clip photo|Three print collage|Landscape film frame|Binder photo card|Corner folded collage|Postcard frame|Offset tape photo|Editorial photo collage|Storyboard grid|Torn fold photo|Modular taped collage'),
 ('Infographic blocks',infoblocks,'Isometric cube|Cross infographic block|Three level pyramid|Three column info block|Circular three sectors|Dashboard summary block|Four spoke info hub|Three stage arrow block|Summary bento block|Three numbered rows|Hexagonal content block|Mountain process block|Numbered sidebar block|Stepped comparison block|Metric capsule block|Triangle summary block|Four numbered blocks|Chevron process block|Modular bento board|Three sixty info circle'),
 ('Progress widgets',progress,'Horizontal progress slider|Seventy five percent ring|Vertical progress tank|Segmented progress bar|Ready semicircle gauge|Four milestone tracker|Battery progress widget|Activity triple rings|Thermometer progress|Fraction pie progress|Labeled progress strip|Hexagon progress track|Square progress track|Dual progress card|Vertical milestone tracker|Orbit loading ring|Chevron progress strip|Staircase progress tracker|Step status dots|Completed progress ring'),
 ('Premium dividers',dividers,'Sparkle line divider|Double diamond divider|Leaf wave divider|Triple orb divider|Zigzag divider|Arch star divider|Twin star divider|V crest divider|Wave flourish divider|Botanical line divider|Stepped diamond divider|Three dot divider|Curl sparkle divider|Dashed hexagon divider|Capsule dots divider|Peak diamond divider|Heart line divider|Chapter number divider|Flower wave divider|Diamond linked divider'),
]

DEFS='<defs><linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.97"/><stop offset="1" stop-color="#D8E8F8" stop-opacity="0.86"/></linearGradient></defs>'

def generate():
    OUT.mkdir(parents=True,exist_ok=True)
    idx=[]; serial=501
    for category,fn,names in CATEGORIES:
        names=names.split('|'); assert len(names)==20, (category,len(names))
        for local,title in enumerate(names):
            ident=f'SV{serial:04d}'
            groups=fn(local)
            body=''.join(f'<g id="{name}">{"".join(content)}</g>' for name,content in zip(('main','accent','details'),groups))
            svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" role="img" aria-labelledby="title"><title id="title">{title}</title>{DEFS}{body}</svg>\n'
            ET.fromstring(svg)
            path=OUT/f'{ident}.svg'; path.write_text(svg)
            idx.append({'id':ident,'title':title,'category':category,'tags':[category.lower(),*title.lower().split(), 'pastel','premium','editable','original'], 'svg':f'svg/files/{ident}.svg','viewBox':'0 0 256 256','license':'Original generated SVG; reusable'})
            serial+=1
    assert len(idx)==500 and serial==1001
    (ROOT/'svg_motion_index.json').write_text(json.dumps(idx,indent=2,ensure_ascii=False)+'\n')
    hashes=[hashlib.sha256((OUT/f'{x["id"]}.svg').read_bytes()).hexdigest() for x in idx]
    assert len(set(hashes))==500
    print(json.dumps({'count':len(idx),'categories':len(CATEGORIES),'unique_files':len(set(hashes)),'first':idx[0]['id'],'last':idx[-1]['id'],'index':str(ROOT/'svg_motion_index.json')},indent=2))

if __name__=='__main__': generate()
