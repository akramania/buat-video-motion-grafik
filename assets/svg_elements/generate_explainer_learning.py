#!/usr/bin/env python3
"""100 original explainer compositions, SV1001–SV1100; no downloaded art.
Standalone, deterministic, transparent, grouped SVGs. Motion suggestions are
authoring guidance, not embedded animation. Run with --qa to validate/raster.
"""
from pathlib import Path
import math,json,html,hashlib,re,sys
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'files'
QA=Path('/workspace/scratch/52cf302c2e1c/assets1500_learning_qa')
INK='#2C465C';BLUE='#AED8F1';MINT='#B3E1D2';LILAC='#CBC4EE';CREAM='#F6E5B6';PINK='#EFC3D4';WHITE='#FBFCFF';PEACH='#E8BEA0'
def a(fill=BLUE,stroke=INK,w=3.4):return f'fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'
def R(x,y,w,h,f=BLUE,rx=5):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" {a(f)}/>'
def C(x,y,r,f=BLUE,w=3.4):return f'<circle cx="{x}" cy="{y}" r="{r}" {a(f,w=w)}/>'
def E(x,y,rx,ry,f=BLUE):return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" {a(f)}/>'
def P(d,f='none',stroke=INK,w=3.4):return f'<path d="{d}" {a(f,stroke,w)}/>'
def L(x,y,x2,y2,co=INK,w=3.4):return f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" {a("none",co,w)}/>'
def PL(points,f=BLUE):return f'<polygon points="{points}" {a(f)}/>'
def lines(x,y,n=3,length=44,step=12):return ''.join(L(x,y+k*step,x+length-(k%2)*8,y+k*step) for k in range(n))
def check(x,y,s=12):return P(f'M{x-s} {y} l{s*.65} {s*.65} l{s*1.35} {-s*1.4}',w=4)
def star(x,y,s=9,f=CREAM):return PL(' '.join(f'{x+math.cos(-math.pi/2+k*math.pi/5)*(s if k%2==0 else s*.45):.2f},{y+math.sin(-math.pi/2+k*math.pi/5)*(s if k%2==0 else s*.45):.2f}' for k in range(10)),f)
def obj(name,x,y,size=100,co=BLUE):
 # Furniture spans the stage horizontally without oversized vertical legs.
 ratio={'desk':.52,'counter':.52,'bench':.60,'mountain':.78}.get(name,1)
 return f'<g transform="translate({x} {y}) scale({size/100} {size/100*ratio})">'+SHAPES[name](co)+'</g>'
def arr(x,y,x2,y2,co=INK,curved=False):
 angle=math.atan2(y2-y,x2-x);s=7
 if curved: body=P(f'M{x} {y} Q{(x+x2)/2} {min(y,y2)-18} {x2} {y2}',stroke=co)
 else:body=L(x,y,x2,y2,co)
 return body+P(f'M{x2-math.cos(angle-.55)*s:.2f} {y2-math.sin(angle-.55)*s:.2f} L{x2} {y2} L{x2-math.cos(angle+.55)*s:.2f} {y2-math.sin(angle+.55)*s:.2f}',stroke=co)
def baseline(y=224):return L(20,y,236,y,MINT,5)
def dots(points,co=CREAM):return ''.join(C(x,y,3,co,w=1) for x,y in points)

SHAPES={
 'book':lambda co:P('M50 23 Q27 10 6 19 V75 Q26 67 50 82 Q74 67 94 75 V19 Q72 10 50 23 Z',WHITE)+L(50,24,50,82)+lines(16,32,3,24,12)+lines(61,32,3,24,12)+P('M7 83 Q28 78 48 91 Q73 78 93 83',stroke=co),
 'doc':lambda co:P('M19 5 H66 L83 23 V94 H19 Z',WHITE)+PL('66,5 66,23 83,23',co)+lines(30,36,4,43,12)+R(31,80,30,6,co,2),
 'folder':lambda co:P('M5 29 H38 L49 40 H96 L85 90 H6 Z',co)+P('M7 27 V15 H37 L49 27 H89 V39',CREAM)+R(26,55,39,17,WHITE),
 'cards':lambda co:R(18,8,63,78,LILAC)+R(10,19,63,78,WHITE)+R(21,30,42,32,co)+star(42,47,10,CREAM)+L(23,77,58,77),
 'pencil':lambda co:PL('14,73 67,9 83,23 30,87',co)+PL('14,73 7,94 30,87',CREAM)+PL('67,9 77,1 92,14 83,23',PINK)+L(22,78,75,17),
 'bulb':lambda co:P('M30 63 Q11 44 23 22 Q39 1 60 7 Q87 14 81 42 Q78 54 65 65 V78 H31 Z',CREAM)+R(33,79,30,9,co)+P('M36 91 Q48 101 60 91')+P('M37 33 L49 48 L61 33 M49 48 V70'),
 'clock':lambda co:C(50,50,42,WHITE)+C(50,50,33,co)+P('M50 28 V51 L69 64')+L(49,7,49,15)+L(49,85,49,92),
 'calendar':lambda co:R(8,20,85,72,WHITE)+R(8,20,85,21,co)+L(29,8,29,27)+L(74,8,74,27)+''.join(R(20+x*23,51+y*21,14,12,MINT if x==1 and y==1 else BLUE,2) for y in range(2) for x in range(3)),
 'person':lambda co:C(50,22,13,PEACH)+P('M35 40 Q50 34 65 40 L73 80 H27 Z',co)+P('M38 81 V96 M62 81 V96 M32 47 L20 72 M68 47 L80 72'),
 'speech':lambda co:P('M9 13 H90 V65 H61 L36 87 V65 H9 Z',WHITE)+C(29,39,4,co)+C(50,39,4,co)+C(71,39,4,co),
 'board':lambda co:R(5,9,90,59,WHITE)+P('M19 50 L38 34 L59 47 L81 23',stroke=co,w=5)+P('M29 69 L19 93 M71 69 L81 93 M50 69 V96'),
 'target':lambda co:C(47,55,39,co)+C(47,55,28,WHITE)+C(47,55,15,MINT)+C(47,55,5,CREAM)+P('M47 55 L83 18')+PL('74,25 74,6 94,6 94,25',LILAC),
 'gear':lambda co:P('M40 5 H58 L62 16 L75 22 L86 19 L95 34 L87 44 V57 L95 66 L85 82 L73 78 L61 85 L58 96 H40 L36 85 L24 78 L12 82 L3 66 L12 57 V44 L3 34 L12 19 L24 22 L37 16 Z',co)+C(49,51,23,WHITE)+C(49,51,10,CREAM),
 'parcel':lambda co:PL('9,28 50,7 91,28 50,49',CREAM)+PL('9,28 50,49 50,94 9,73',co)+PL('50,49 91,28 91,73 50,94',MINT)+P('M30 18 L72 39 V83')+R(20,45,18,14,WHITE,2),
 'door':lambda co:R(22,5,61,89,CREAM)+PL('27,10 74,17 74,88 27,91',co)+C(62,52,3,LILAC)+R(6,94,88,5,MINT,1),
 'house':lambda co:PL('7,43 50,8 93,43 84,43 84,92 17,92 17,43',co)+R(40,62,20,30,LILAC)+R(24,46,13,13,WHITE,2)+R(65,46,13,13,WHITE,2)+P('M10 43 L50 12 L90 43',CREAM),
 'phone':lambda co:R(25,4,50,91,co,10)+R(31,16,38,61,INK,4)+R(40,8,20,4,LILAC,2)+C(50,85,3,WHITE)+R(39,31,23,22,MINT),
 'desk':lambda co:R(4,45,92,9,CREAM)+R(13,54,29,38,co)+L(87,55,87,94)+L(14,73,40,73)+C(27,65,2,INK)+C(27,84,2,INK),
 'cup':lambda co:P('M13 31 H73 V69 Q73 91 43 91 Q13 91 13 69 Z',WHITE)+P('M73 36 Q96 29 96 50 Q96 72 74 70',co)+E(43,32,30,7,CREAM)+P('M32 18 Q22 8 32 1 M52 18 Q42 8 52 1'),
 'plant':lambda co:PL('29,70 72,70 63,96 38,96',CREAM)+P('M50 70 V28 M50 52 Q21 51 14 22 Q42 18 50 52 M50 37 Q58 8 85 9 Q82 35 50 37',MINT),
 'umbrella':lambda co:P('M6 46 Q50 1 94 46 Q80 60 65 46 Q50 60 35 46 Q20 60 6 46 Z',co)+P('M50 13 V87 Q50 100 65 92')+P('M35 46 Q32 30 50 13 Q68 30 65 46'),
 'bench':lambda co:R(5,15,90,13,co)+R(5,36,90,13,co)+R(7,57,87,10,CREAM)+P('M17 68 V95 M84 68 V95 M17 49 V58 M84 49 V58'),
 'sign':lambda co:L(49,7,49,95)+PL('8,20 72,20 92,38 72,56 8,56',co)+PL('94,62 29,62 10,79 29,95 94,95',MINT),
 'compass':lambda co:C(50,50,42,CREAM)+C(50,50,31,WHITE)+PL('61,24 43,44 37,78 56,55',co)+C(50,50,4,LILAC),
 'boat':lambda co:PL('8,70 92,70 75,92 25,92',co)+L(48,8,48,70)+PL('44,14 15,64 44,64',MINT)+PL('54,25 83,64 54,64',LILAC),
 'magnifier':lambda co:C(42,40,31,WHITE)+C(42,40,22,co)+PL('64,61 92,87 84,96 55,70',CREAM)+P('M29 35 Q33 24 43 23',stroke=WHITE,w=5),
 'frame':lambda co:R(8,8,84,84,co)+R(17,17,66,66,WHITE)+PL('18,72 39,44 54,57 68,36 82,72',MINT)+C(34,30,7,CREAM),
 'pedestal':lambda co:R(15,12,71,8,CREAM)+PL('23,22 77,22 70,91 30,91',co)+R(11,91,79,7,LILAC)+P('M38 28 L43 86 M61 28 L56 86'),
 'gate':lambda co:P('M10 96 V34 Q50 -5 91 34 V96 H77 V42 Q50 16 24 42 V96 Z',co)+R(6,94,88,5,CREAM,1),
 'bowl':lambda co:P('M9 43 H91 Q88 85 50 85 Q12 85 9 43 Z',co)+P('M16 40 Q23 17 34 35 Q45 8 55 34 Q68 12 81 40',WHITE)+R(35,87,30,7,LILAC),
 'lantern':lambda co:P('M30 27 H70 L81 47 V84 L70 95 H30 L19 84 V47 Z',CREAM)+R(30,45,40,42,co)+P('M50 27 V8 Q31 4 36 20')+P('M50 53 Q64 65 50 80 Q35 65 50 53 Z',PINK),
 'key':lambda co:C(29,31,21,CREAM)+C(29,31,9,WHITE)+PL('43,46 85,89 94,80 84,70 92,62 82,53 75,61 59,44',co),
 'suitcase':lambda co:R(16,26,70,65,co)+P('M37 26 V10 H65 V26')+P('M30 39 V77 M72 39 V77')+R(42,45,18,21,WHITE)+C(31,97,3,INK)+C(74,97,3,INK),
 'window':lambda co:R(8,6,84,87,co)+R(16,14,68,70,WHITE)+L(50,14,50,84)+L(16,48,84,48)+PL('16,57 33,38 48,57',MINT)+PL('55,75 70,56 84,76',MINT)+R(3,93,94,6,CREAM),
 'counter':lambda co:R(5,45,90,52,co)+R(1,37,98,10,CREAM)+R(20,59,60,23,WHITE)+L(20,90,80,90),
 'receipt':lambda co:P('M25 4 L32 10 L39 4 L46 10 L53 4 L60 10 L67 4 L74 10 V94 L67 88 L60 94 L53 88 L46 94 L39 88 L32 94 L25 88 Z',WHITE)+lines(34,27,4,31,13)+R(35,81,27,4,co,1),
 'battery':lambda co:R(8,25,79,50,WHITE)+R(88,40,7,20,LILAC)+R(17,34,43,31,co)+PL('52,20 38,51 54,51 46,82 70,44 54,44',CREAM),
 'chain':lambda co:P('M40 25 L20 45 Q5 60 22 73 Q36 86 52 70 L71 50',stroke=co,w=10)+P('M61 74 L81 54 Q97 39 80 25 Q65 13 50 28 L30 48',stroke=INK,w=7),
 'funnel':lambda co:PL('4,8 96,8 65,49 61,92 39,92 35,49',co)+L(20,25,80,25)+L(35,45,65,45),
 'cloud':lambda co:P('M24 73 C2 73 3 43 27 43 C30 13 70 7 80 37 C102 35 109 75 82 75 Z',co)+P('M30 88 H72',stroke=MINT),
 'mountain':lambda co:PL('3,92 40,17 61,59 78,36 99,92',co)+PL('28,43 40,17 52,46 42,39 34,48',WHITE)+PL('70,50 78,36 87,55 78,48',WHITE),
 'scale':lambda co:L(50,9,50,85)+L(25,93,77,93)+L(15,30,85,30)+PL('15,33 3,62 29,62',co)+PL('85,33 72,62 98,62',MINT)+C(50,29,6,CREAM),
 'puzzle':lambda co:P('M9 12 H34 Q31 -3 45 0 Q61 1 56 12 H84 V38 Q98 33 99 49 Q99 64 84 61 V88 H57 Q61 100 45 100 Q30 100 34 88 H9 V62 Q-3 67 -2 51 Q-2 36 9 39 Z',co),
 'bucket':lambda co:P('M16 36 H84 L73 95 H28 Z',co)+P('M18 39 Q13 0 50 0 Q86 0 84 39')+R(11,33,78,10,CREAM)+R(32,58,31,19,WHITE),
 'lighthouse':lambda co:PL('34,32 66,32 79,96 21,96',WHITE)+R(34,57,33,15,co)+R(26,24,48,11,LILAC)+PL('29,23 50,7 72,23',CREAM)+R(43,81,14,15,INK)+P('M22 29 L5 15 M78 29 L96 15'),
 'wave':lambda co:P('M4 90 V66 Q45 18 79 33 Q98 41 77 60 Q57 73 81 90 Z',co)+P('M12 75 Q44 47 70 53 Q44 74 66 88',WHITE),
 'chair':lambda co:R(26,7,48,49,co)+R(18,59,64,13,CREAM)+P('M25 73 V96 M74 73 V96 M26 55 V60 M74 55 V60'),
 'bottle':lambda co:R(27,31,49,66,co)+R(32,12,39,18,LILAC)+R(34,53,34,24,WHITE)+P('M50 59 V72 M44 66 H57'),
 'tube':lambda co:P('M28 10 H70 V19 H65 V75 Q65 94 49 94 Q33 94 33 75 V19 H28 Z',WHITE)+P('M35 55 H63 V75 Q63 90 49 90 Q35 90 35 75 Z',co)+L(40,35,57,35),
 'bag':lambda co:PL('19,29 81,29 87,95 12,95',co)+P('M34 31 V18 Q50 0 66 18 V31')+R(30,55,40,24,WHITE)+C(50,67,8,CREAM),
 'cart':lambda co:P('M3 14 H15 L29 70 H81 L94 32 H21',co)+L(30,53,87,53)+L(48,32,48,69)+L(69,32,69,69)+C(36,90,8,LILAC)+C(77,90,8,LILAC),
 'wallet':lambda co:R(8,20,84,67,co)+P('M12 24 L71 10 L80 24',CREAM)+R(53,39,41,29,WHITE)+C(65,54,4,CREAM),
 'monitor':lambda co:R(5,8,90,64,co)+R(12,15,76,44,INK)+P('M39 73 V91 H62 V73')+R(24,91,53,7,LILAC),
 'ticket':lambda co:P('M5 23 H95 V39 Q81 50 95 62 V78 H5 V62 Q19 50 5 39 Z',co)+L(71,25,71,75)+star(39,49,17,WHITE),
 'train':lambda co:P('M22 12 Q50 0 79 12 V78 L69 92 H32 L22 78 Z',co)+R(29,23,43,31,INK)+C(35,69,5,CREAM)+C(64,69,5,CREAM)+P('M26 92 L17 99 M75 92 L85 99'),
 'menu':lambda co:P('M15 8 H85 V94 H15 Z',WHITE)+R(24,18,52,20,co)+lines(26,51,3,47,12)+C(50,28,6,CREAM),
 'stamp':lambda co:R(15,77,70,17,co)+P('M29 76 Q36 67 38 54 V33 Q29 24 36 13 Q50 3 66 13 Q73 24 64 33 V54 Q65 67 72 76 Z',LILAC)+R(8,95,84,4,MINT,1),
 'toolbox':lambda co:R(5,35,90,61,co)+P('M30 35 V19 H70 V35')+L(5,57,95,57)+R(42,48,16,17,CREAM)+R(18,72,63,13,WHITE),
 'heart':lambda co:P('M50 25 Q26 -1 8 22 Q-5 44 50 91 Q105 44 92 22 Q74 -1 50 25 Z',PINK),
 'shield':lambda co:P('M50 6 L87 22 V54 Q85 82 50 98 Q15 82 13 54 V22 Z',co)+check(50,50,17),
 'frame_pair':lambda co:R(6,10,53,69,LILAC)+R(41,26,53,69,co)+R(49,35,37,47,WHITE)+C(66,47,9,CREAM)+PL('51,76 64,57 83,76',MINT),
}

def step_cards(x=34,y=82):
 return ''.join(R(x+k*64,y+k*36,53,32,[BLUE,MINT,LILAC][k])+C(x+12+k*64,y+16+k*36,6,CREAM)+L(x+24+k*64,y+16+k*36,x+42+k*64,y+16+k*36) for k in range(3))
def sheet(x=55,y=40,w=138,h=170,co=WHITE):return R(x,y,w,h,co)+lines(x+16,y+25,4,w-33,22)
def portal(x=102,y=36):return R(x,y,93,158,CREAM)+P(f'M{x+13} {y+14} L{x+79} {y+25} V{y+146} L{x+13} {y+156} Z',BLUE)+C(x+67,y+90,4,LILAC)
def loop_arrows(x=130,y=120,rad=73):return P(f'M{x-rad} {y} Q{x-rad} {y-rad} {x} {y-rad} Q{x+rad} {y-rad} {x+rad} {y-10}',stroke=MINT)+P(f'M{x+rad} {y} Q{x+rad} {y+rad} {x} {y+rad} Q{x-rad} {y+rad} {x-rad} {y+10}',stroke=LILAC)+PL(f'{x+rad-9},{y-18} {x+rad},{y-3} {x+rad+9},{y-18}',MINT)+PL(f'{x-rad-9},{y+18} {x-rad},{y+3} {x-rad+9},{y+18}',LILAC)

def learning(i):
 if i==0:return obj('book',40,79,156),obj('pencil',167,130,68)+obj('bulb',155,5,77),baseline()+arr(182,86,164,108,MINT)
 if i==1:return obj('cards',69,48,121),obj('clock',177,143,61)+obj('target',17,150,68),loop_arrows()+dots([(45,51),(216,41)])
 if i==2:return step_cards(23,65),obj('bulb',164,7,68)+obj('doc',25,174,58),arr(70,102,99,132,MINT)+arr(138,137,165,168,MINT)+baseline()
 if i==3:return R(26,43,204,139,WHITE)+''.join(R(41+k*61,65,49,81,[BLUE,MINT,LILAC][k])+obj(n,42+k*61,83,48) for k,n in enumerate(['book','pencil','target'])),R(55,181,146,16,CREAM),arr(82,161,105,161)+arr(145,161,168,161)+baseline(211)
 if i==4:return R(28,50,91,135,BLUE)+R(139,66,91,135,MINT),obj('speech',43,63,64)+obj('shield',152,82,64),arr(110,35,157,49,LILAC,True)+R(43,152,59,14,WHITE)+R(152,171,59,14,WHITE)+baseline()
 if i==5:return obj('person',14,118,84)+obj('person',88,114,86)+obj('person',165,118,84),obj('speech',18,47,79)+obj('speech',151,44,86),obj('book',89,34,73)+baseline()
 if i==6:return obj('calendar',34,24,145),obj('book',120,139,113)+obj('pencil',20,153,73),P('M178 74 Q231 72 220 121')+arr(219,121,209,144,MINT)+baseline()
 if i==7:return obj('folder',34,109,159),obj('cards',111,30,110)+obj('bulb',18,17,70),arr(127,129,154,96,LILAC)+baseline()+check(193,197,14)
 if i==8:return ''.join(obj('puzzle',27+(k%2)*93,32+(k//2)*88,86,[BLUE,MINT,LILAC,CREAM][k]) for k in range(4)),obj('book',158,162,84),arr(113,124,156,124)+baseline()
 if i==9:return obj('board',19,24,188),obj('pencil',165,119,77)+obj('cards',34,163,67),P('M83 93 L105 70 L129 86')+C(83,93,5,MINT)+baseline()
 if i==10:return sheet(75,51,123,151),obj('speech',4,16,108)+obj('stamp',151,149,90),check(110,165,15)+loop_arrows(128,124,92)+baseline()
 if i==11:return obj('doc',29,52,105)+obj('doc',132,69,105),obj('pencil',105,146,86),arr(88,40,160,47,MINT,True)+arr(170,206,88,205,LILAC)+baseline()
 if i==12:return obj('book',82,79,101),''.join(obj('speech',x,y,69,co) for x,y,co in [(12,15,BLUE),(177,20,MINT),(13,160,LILAC),(174,164,CREAM)]),P('M68 66 L91 94 M191 73 L167 96 M66 174 L92 142 M191 177 L169 143')
 if i==13:return obj('book',27,139,134),obj('clock',148,17,90)+obj('cup',165,141,70),obj('pencil',41,70,68)+R(39,222,183,9,MINT)+dots([(93,21),(217,114)])
 if i==14:return P('M31 188 H224 M38 191 V221 M215 191 V221 M52 190 Q128 104 205 190',CREAM),obj('book',9,87,112)+obj('target',138,7,108),P('M48 191 L95 134 M161 133 L206 191')+arr(93,103,145,70,MINT)+baseline(230)
 if i==15:return obj('pedestal',69,135,121)+R(38,26,146,126,BLUE),obj('shield',148,29,82)+obj('speech',47,46,85),P('M180 70 L204 62 V156 L180 165 Z',LILAC)+baseline()
 if i==16:return P('M31 225 L79 26 M167 225 L132 26',stroke=INK,w=5)+''.join(L(55+k*5,58+k*39,140+k*6,58+k*39,CREAM,7) for k in range(4)),obj('doc',151,69,81)+obj('target',70,16,65),obj('stamp',9,159,68)+baseline(230)
 if i==17:return R(48,22,145,195,WHITE)+R(48,22,25,195,LILAC)+lines(86,56,6,83,22),''.join(R(184,46+k*38,29,22,[BLUE,MINT,CREAM,PINK][k]) for k in range(4))+obj('pencil',8,146,86),P('M119 23 V89 L133 79 L148 89 V23',BLUE)+baseline()
 if i==18:return R(21,41,214,153,WHITE)+L(127,42,127,193),obj('plant',28,70,88)+obj('bulb',140,70,80),P('M112 114 H139 M129 104 L139 114 L129 124')+R(38,168,69,12,BLUE)+R(147,168,69,12,MINT)+baseline(216)
 if i==19:return obj('tube',18,58,112)+sheet(118,27,109,178),obj('bottle',58,150,67),check(153,153,15)+arr(92,68,111,88,MINT)+baseline()
 if i==20:return obj('person',15,93,136)+obj('board',124,32,120),obj('speech',15,16,105),P('M99 153 L145 97')+obj('book',132,176,95)+baseline()
 if i==21:return R(17,43,222,15,CREAM)+R(17,129,222,15,CREAM)+R(17,217,222,15,CREAM),obj('book',25,68,73)+obj('folder',139,65,79)+obj('cards',28,155,66)+obj('plant',143,150,75),P('M29 59 V129 M227 59 V129 M29 144 V216 M227 144 V216')
 if i==22:return P('M48 143 V82 Q48 14 128 14 Q208 14 208 82 V143',stroke=INK,w=8)+R(31,100,46,72,BLUE)+R(180,100,46,72,BLUE),obj('doc',96,112,107),P('M94 50 L106 34 M116 62 V36 M137 61 V34 M158 52 L148 34',stroke=MINT,w=5)+baseline()
 if i==23:return obj('folder',17,102,165),obj('doc',103,14,111)+obj('shield',163,127,79),star(74,61,18)+star(33,39,11,LILAC)+baseline()
 return P('M22 201 Q70 172 64 123 Q70 80 129 97 Q200 119 219 44',stroke=MINT,w=13),obj('book',12,174,65)+obj('pencil',42,70,55)+obj('bulb',125,93,56)+obj('target',171,6,67),''.join(C(x,y,5,WHITE) for x,y in [(40,174),(64,123),(129,97),(211,61)])+baseline(236)
def story(i):
 if i==0:return R(27,77,146,103,WHITE)+PL('28,79 100,131 172,79',BLUE),obj('cup',168,131,75)+obj('book',18,170,96),obj('heart',146,18,70)+baseline()
 if i==1:return obj('window',22,17,109)+obj('desk',21,143,213),obj('book',113,126,86)+obj('plant',181,84,64),obj('clock',161,14,67)+baseline(238)
 if i==2:return obj('suitcase',18,60,145),obj('ticket',127,19,111)+obj('clock',164,136,82),arr(143,114,184,114,MINT)+baseline()
 if i==3:return R(26,81,204,11,CREAM)+R(26,145,204,81,BLUE)+P('M20 82 L47 30 H210 L236 82 Z',LILAC),obj('bag',17,123,91)+obj('bowl',127,94,102),P('M44 32 V78 M82 32 V78 M120 32 V78 M158 32 V78 M196 32 V78')+R(137,174,76,33,WHITE)+baseline(234)
 if i==4:return obj('bench',13,132,166),obj('umbrella',80,13,138)+obj('speech',170,133,73),''.join(L(x,y,x-5,y+12,BLUE,3) for x,y in [(38,33),(50,73),(211,67),(227,97)])+baseline()
 if i==5:return portal(125,20),obj('parcel',19,113,113)+obj('lantern',25,19,78),obj('key',132,157,89)+baseline()
 if i==6:return ''.join(R(23+k*43,26+(k%2)*16,31,86-(k%2)*16,[BLUE,MINT,LILAC,CREAM,BLUE][k])+R(31+k*43,40+(k%2)*16,11,12,WHITE,2) for k in range(5))+P('M16 150 H238 L198 227 H48 Z',WHITE),obj('person',93,101,121),''.join(PL(f'{34+k*40},172 {56+k*40},172 {49+k*40},196 {27+k*40},196',LILAC) for k in range(5))+baseline(235)
 if i==7:return obj('sign',105,55,126),obj('compass',19,139,92)+obj('suitcase',12,17,91),P('M117 173 L132 213 L218 219 M117 172 L97 222 L22 223',stroke=MINT,w=6)+baseline(236)
 if i==8:return obj('boat',25,86,159),obj('compass',153,19,92)+R(159,155,72,57,CREAM),P('M164 176 Q190 161 224 177 M190 158 V211')+P('M16 223 Q32 213 48 223 T80 223 T112 223 T144 223 T176 223 T208 223 T240 223',stroke=BLUE)
 if i==9:return R(30,76,166,102,WHITE)+PL('30,77 113,136 196,77',BLUE),obj('magnifier',138,140,98)+obj('key',29,16,87),C(113,119,15,CREAM)+star(212,58,13)+baseline()
 if i==10:return R(91,42,126,165,LILAC)+R(102,52,102,143,WHITE)+lines(115,78,4,70,22),obj('frame_pair',17,89,114)+obj('pencil',154,132,75),R(142,43,20,55,BLUE)+baseline()
 if i==11:return obj('desk',15,131,222),obj('clock',149,12,93)+obj('doc',21,43,102)+obj('cards',80,102,85),R(167,124,65,17,CREAM)+R(167,145,54,16,MINT)+baseline(239)
 if i==12:return obj('pedestal',63,119,138)+R(63,17,139,112,WHITE),obj('lantern',94,24,75)+obj('menu',10,158,63),P('M74 32 L187 105',stroke=BLUE,w=4)+R(90,141,85,16,LILAC)+baseline()
 if i==13:return obj('gate',90,15,154),obj('book',14,141,119)+obj('key',157,157,81),arr(96,125,138,109,MINT)+star(55,39,18)+baseline()
 if i==14:return E(128,122,106,35,CREAM)+L(44,145,44,218)+L(212,145,212,218),obj('bowl',30,53,80)+obj('bowl',146,53,80)+obj('chair',88,138,78),obj('cup',94,64,67)+baseline(234)
 if i==15:return obj('counter',33,126,183),obj('umbrella',11,15,112)+obj('cards',152,27,97),obj('speech',114,4,60)+R(55,160,109,25,WHITE)+baseline()
 if i==16:return obj('lantern',15,43,88)+obj('lantern',151,32,93),obj('parcel',79,127,123),P('M26 14 Q128 57 230 14',stroke=INK)+''.join(PL(f'{x},26 {x+15},42 {x+30},26',co) for x,co in [(49,PINK),(97,MINT),(149,CREAM)])+baseline()
 if i==17:return obj('chair',15,125,95)+obj('chair',127,125,95),obj('clock',75,17,99)+obj('plant',92,144,69),baseline()+R(22,24,40,15,BLUE)+R(190,24,39,15,LILAC)
 if i==18:return obj('desk',92,115,145)+obj('bag',17,77,130),obj('cards',121,13,81)+obj('pencil',161,42,70),R(28,21,73,28,WHITE)+C(44,35,7,CREAM)+L(59,35,89,35)+baseline()
 if i==19:return obj('toolbox',10,120,127)+obj('door',139,12,103),obj('person',64,25,114),R(152,150,79,48,WHITE)+P('M165 172 L215 172 M181 160 V185')+baseline()
 if i==20:return obj('counter',71,110,166),obj('key',21,47,103)+obj('calendar',134,10,96),R(91,165,103,24,WHITE)+arr(42,186,76,172,MINT)+baseline()
 if i==21:return obj('window',106,8,130),obj('lantern',15,99,107)+obj('clock',115,137,95),P('M131 66 C132 37 165 35 167 65 Q151 91 131 66 Z',LILAC)+dots([(193,37),(204,74),(211,113)],CREAM)+baseline()
 if i==22:return obj('plant',73,52,138),obj('frame_pair',11,110,99)+obj('bucket',159,139,85),P('M193 153 Q172 134 165 106',stroke=BLUE)+''.join(C(x,y,3,BLUE,w=1) for x,y in [(163,111),(156,116),(168,122)])+baseline()
 if i==23:return obj('phone',71,46,147),obj('speech',17,15,104)+obj('speech',137,9,104),star(30,150,15)+star(215,187,17)+arr(43,211,96,203,MINT)+baseline()
 return P('M85 226 V168 Q83 148 62 127 L21 86 L61 53 L119 111 Q128 124 138 111 L196 53 L236 86 L195 127 Q174 148 174 168 V226 Z',BLUE),obj('doc',2,2,72)+obj('target',164,4,76),PL('99,217 118,217 118,179 99,179',WHITE)+PL('138,217 157,217 157,179 138,179',WHITE)+baseline(234)
def metaphors(i):
 if i==0:return P('M12 217 V162 H86 V217 M170 217 V162 H243 V217',LILAC)+P('M66 161 H188',stroke=CREAM,w=17),obj('person',20,36,117)+obj('lighthouse',176,59,81),P('M115 165 L109 216 M143 165 L149 216')+baseline(230)
 if i==1:return P('M19 95 Q68 32 103 109 Q141 184 193 107 Q223 50 229 118 Q232 184 157 173 Q85 164 136 97 Q174 47 194 70',stroke=LILAC,w=11),obj('pencil',26,150,70)+obj('shield',163,160,72),arr(50,214,143,214,MINT)+baseline(232)
 if i==2:return obj('bucket',32,57,167),obj('shield',160,118,84)+obj('bottle',154,15,79),P('M86 196 Q99 178 104 203 Q93 220 86 196 Z',BLUE)+R(107,162,34,27,CREAM)+check(124,174,8)+baseline()
 if i==3:return R(43,8,171,12,CREAM)+C(126,57,28,LILAC)+P('M98 56 V135 M154 56 V189'),obj('parcel',27,120,106)+obj('person',164,90,91),P('M126 37 V76 M105 59 H147')+PL('138,188 171,188 177,225 133,225',BLUE)+baseline(232)
 if i==4:return obj('funnel',62,39,131),obj('cards',7,16,74)+obj('cards',163,145,75),arr(25,105,71,79,LILAC)+arr(144,166,171,190,MINT)+P('M27 221 H222',stroke=CREAM,w=8)
 if i==5:return obj('cloud',11,10,130)+obj('window',106,109,132),obj('bulb',157,6,79),arr(51,102,103,144,MINT)+C(46,154,8,LILAC)+C(32,182,5,LILAC)+baseline()
 if i==6:return obj('chain',22,20,152),obj('toolbox',129,128,105),P('M37 190 Q76 211 117 182',stroke=MINT,w=10)+R(98,168,25,19,CREAM)+arr(139,67,199,107,LILAC)+baseline()
 if i==7:return obj('door',126,38,118),obj('key',10,70,113)+obj('key',13,166,72,MINT),P('M27 44 L53 20 M27 20 L53 44',stroke=PINK,w=5)+check(162,200,17)+baseline()
 if i==8:return obj('doc',5,21,78)+obj('cards',55,63,95)+obj('folder',121,129,121),obj('gear',151,18,85),arr(72,140,130,157,MINT)+baseline()+check(194,220,9)
 if i==9:return P('M20 46 Q92 15 105 72 Q124 116 61 122 Q4 133 49 180 Q77 208 111 179 Q139 156 145 217',stroke=LILAC,w=10),obj('compass',140,20,92)+obj('target',139,141,94),arr(29,217,112,217,MINT)+baseline(236)
 if i==10:return obj('mountain',15,112,175),obj('plant',71,9,153),P('M73 197 L102 179 L121 212 L143 196',stroke=WHITE,w=6)+C(209,75,15,CREAM)+baseline()
 if i==11:return portal(112,22),obj('key',15,144,105)+obj('bulb',17,12,103),P('M138 182 L149 150 M163 182 L168 150',stroke=CREAM,w=4)+arr(70,123,123,100,MINT)+baseline()
 if i==12:return R(17,29,193,156,LILAC)+''.join(R(31+(k%4)*42,44+(k//4)*39,28,25,WHITE) for k in range(12)),obj('magnifier',119,106,117),check(161,158,14)+baseline()+dots([(213,45),(229,72)])
 if i==13:return obj('mountain',16,61,226),P('M39 218 H76 V179 H112 V143 H148 V106 H184',stroke=CREAM,w=13),obj('target',154,1,83)+''.join(C(x,y,4,WHITE) for x,y in [(58,208),(95,169),(130,132)])+baseline(233)
 if i==14:return obj('scale',40,33,181),obj('book',21,66,73)+obj('clock',160,67,74),R(89,225,79,7,LILAC)+dots([(25,23),(217,23)])
 if i==15:return R(32,35,172,166,WHITE)+P('M120 79 H172 V133 H147 Q157 150 135 150 Q113 150 123 133 H120 Z',LILAC),obj('puzzle',135,137,99),arr(218,79,188,112,MINT)+baseline()
 if i==16:return obj('battery',33,68,173),obj('gear',159,9,75),P('M129 198 V218 H227 V171',stroke=INK,w=7)+R(213,144,29,28,MINT)+L(219,132,219,144)+L(237,132,237,144)+baseline(235)
 if i==17:return obj('lighthouse',85,8,158),obj('wave',4,110,147)+obj('wave',137,164,108),P('M148 32 L204 17 M129 33 L96 17',stroke=CREAM,w=6)+baseline(235)
 if i==18:return obj('gear',19,46,131)+obj('gear',139,126,94),obj('bottle',147,3,87),P('M140 110 C134 119 124 129 126 138 Q140 153 152 138 Q154 129 140 110 Z',BLUE)+arr(111,193,130,193,MINT)+baseline()
 if i==19:return P('M13 71 L26 101 L38 44 L49 128 L61 62 L73 94 L86 59 L98 106',stroke=LILAC,w=5)+obj('funnel',100,25,109),P('M213 163 Q221 128 227 163 T241 163',stroke=MINT,w=5),arr(41,174,99,174)+baseline()
 if i==20:return obj('speech',25,56,106)+obj('speech',132,128,109),obj('person',147,4,91),arr(71,172,125,187,MINT)+arr(178,96,104,70,LILAC,True)+baseline()
 if i==21:return R(11,176,232,33,LILAC)+''.join(C(29+k*29,193,9,WHITE) for k in range(8)),obj('cards',9,79,110)+obj('gear',137,9,89)+obj('doc',167,99,82),arr(95,153,163,153,MINT)+baseline(229)
 if i==22:return obj('scale',43,35,173),obj('bag',6,18,91)+obj('wallet',158,17,96),obj('heart',91,146,82)+baseline(237)
 if i==23:return P('M13 214 H64 V170 H113 V135 H164 V96 H224',stroke=CREAM,w=14),obj('plant',133,9,105)+obj('book',3,130,84),arr(36,110,92,77,MINT,True)+baseline(236)
 return P('M20 33 H69 V136 Q72 182 128 182 Q184 182 187 136 V33 H236 V139 Q230 228 128 228 Q25 228 20 139 Z',LILAC),obj('plant',71,65,112)+obj('bulb',93,0,79),P('M54 95 H81 M175 95 H202',stroke=CREAM,w=6)+star(127,35,12)+baseline(238)
def services(i):
 if i==0:return obj('counter',80,125,156)+obj('person',3,82,122),obj('ticket',114,38,86)+obj('chair',179,176,64),R(97,71,47,37,WHITE)+P('M112 88 H129 M120 80 V97')+baseline()
 if i==1:return obj('calendar',69,22,155),obj('phone',4,112,115)+obj('compass',166,145,79),arr(67,73,100,69,MINT)+baseline()
 if i==2:return R(61,56,168,125,WHITE)+R(81,81,128,60,BLUE),obj('ticket',4,116,125)+obj('clock',144,169,71),C(116,110,14,CREAM)+P('M107 115 L116 99 L125 115')+C(173,110,14,MINT)+P('M164 101 H180 L166 117 H181')+baseline(238)
 if i==3:return obj('chair',5,120,101)+obj('chair',149,120,101),obj('doc',88,93,83)+obj('speech',41,3,118),R(84,160,92,8,CREAM)+L(94,169,94,222)+L(166,169,166,222)+baseline(234)
 if i==4:return obj('counter',26,127,197),obj('bag',140,44,104)+obj('bottle',56,22,110),obj('doc',14,118,80)+arr(121,65,146,74,MINT)+baseline()
 if i==5:return obj('tube',20,49,132)+obj('counter',113,133,128),obj('cards',131,26,103),P('M74 186 H159',stroke=CREAM,w=12)+check(169,109,14)+baseline(229)
 if i==6:return obj('doc',15,33,137)+obj('house',124,116,118),obj('key',142,17,93),arr(119,189,150,209,MINT)+check(91,146,15)+baseline()
 if i==7:return obj('monitor',23,33,196),obj('cart',131,137,112),R(55,59,45,44,MINT)+obj('bag',59,61,39)+R(122,59,51,44,LILAC)+obj('bottle',127,62,37)+arr(85,167,144,177,MINT)+baseline()
 if i==8:return obj('monitor',13,29,136)+obj('wallet',138,119,103),obj('receipt',131,16,115),arr(94,178,146,170,MINT)+check(196,86,11)+baseline()
 if i==9:return obj('door',117,13,124)+obj('person',5,80,142),obj('parcel',80,116,114),P('M75 171 L98 151 M206 174 L180 155')+baseline()
 if i==10:return obj('parcel',69,90,154),obj('receipt',6,7,105)+obj('suitcase',174,24,69),arr(107,69,199,74,LILAC,True)+arr(80,210,31,198,MINT)+baseline()
 if i==11:return obj('counter',69,128,169)+obj('person',1,89,135),obj('wallet',96,72,91)+obj('cards',155,11,85),C(67,43,23,CREAM)+P('M66 28 V58 M78 32 Q53 27 54 40 Q54 47 76 47 Q84 63 56 56')+baseline()
 if i==12:return obj('train',127,23,124)+R(36,130,67,96,CREAM),obj('cards',2,9,98),P('M25 152 H87 L112 173',stroke=MINT,w=9)+R(49,144,28,19,INK)+arr(101,216,140,216)+baseline(235)
 if i==13:return obj('counter',72,126,169),obj('suitcase',3,83,122)+obj('key',116,39,106),R(174,11,47,39,WHITE)+C(197,29,8,LILAC)+R(107,165,97,29,WHITE)+baseline()
 if i==14:return R(11,155,231,40,LILAC)+''.join(C(29+k*29,176,9,WHITE) for k in range(8))+obj('gate',119,18,112),obj('suitcase',22,66,113)+obj('shield',177,143,70),arr(47,212,135,212,MINT)+baseline(235)
 if i==15:return obj('menu',1,27,129)+obj('bowl',118,125,131),obj('speech',133,18,109),arr(91,164,143,184,MINT)+check(180,66,11)+baseline(233)
 if i==16:return obj('counter',17,130,224),obj('cup',133,30,104)+obj('ticket',9,33,123),R(47,168,151,27,WHITE)+arr(119,102,161,112,MINT)+baseline(235)
 if i==17:return obj('doc',36,27,157),obj('book',126,141,121)+obj('cards',3,147,90),check(104,139,14)+R(160,20,72,28,BLUE)+C(175,34,8,CREAM)+L(189,34,217,34)+baseline(239)
 if i==18:return obj('book',15,21,146)+obj('counter',57,144,176),obj('stamp',159,65,90)+obj('cards',9,131,78),P('M116 128 L172 132')+check(202,126,12)+baseline(236)
 if i==19:return obj('monitor',12,30,162),obj('speech',122,6,112)+obj('toolbox',134,140,112),obj('gear',38,150,85)+arr(176,105,184,142,MINT)+baseline(237)
 if i==20:return obj('doc',30,42,154),obj('pencil',144,132,96),''.join(star(51+k*38,28,14,[BLUE,MINT,CREAM,LILAC,PINK][k]) for k in range(5))+check(100,169,15)+baseline()
 if i==21:return obj('toolbox',93,91,153),obj('receipt',11,5,113)+obj('phone',161,5,88),arr(60,176,112,192,MINT)+check(187,166,13)+baseline()
 if i==22:return obj('counter',19,130,219),obj('parcel',131,15,108)+obj('heart',17,22,113),R(71,174,121,22,WHITE)+arr(104,80,144,80,MINT)+baseline(236)
 if i==23:return obj('gate',100,10,143),obj('ticket',4,64,131)+obj('cards',25,151,89),arr(124,182,157,182,MINT)+check(168,99,17)+baseline(236)
 return obj('calendar',32,36,151),obj('cards',136,146,98)+obj('stamp',153,9,82),loop_arrows(132,129,92)+check(92,120,12)+baseline(239)

CATALOG=[
 ('learning','Learning actions and teaching kits',learning,[
 'Guided reading with an idea cue','Flashcard practice and review cycle','Concept scaffold steps','Three stage lesson sequence','Question to answer reveal','Think pair share discussion kit','Spaced revision calendar','Active recall resource drawer','Knowledge puzzle with reading anchor','Worked example teaching board','Feedback loop on a worksheet','Peer review document exchange','Mind map branch planning','Timeboxed study station','Learning goal bridge','Quiz answer reveal podium','Skill ladder and certification','Revision notebook with bookmarks','Compare and contrast teaching board','Experiment and observation record','Teach back presentation kit','Learning resource shelf','Focused listening and notes','Progress portfolio and achievement','Learning journey roadmap']),
 ('story','Story setup props',story,[
 'Invitation letter and tea','Morning workspace and window','Travel departure with time cue','Market stall opening scene','Rainy conversation at a bench','Village doorstep arrival','City crossing and daily commute','Forest fork and travel choice','Harbor departure and navigation','Hidden clue in an envelope','Memory diary and photographs','Deadline desk and waiting tasks','Museum artifact display','A new chapter through a gate','Shared meal conversation setting','Lost and found welcome booth','Festival preparation with gifts','Waiting room moment','First day classroom belongings','Workshop welcome and equipment','Shop opening day','Night watch by the window','Garden memory and care','Unexpected message on a phone','Crossroads decision setup']),
 ('metaphor','Problem-solution metaphors',metaphors,[
 'Bridge the gap to support','Untangle a complex thread','Patch the leaking bucket','Lift a heavy load with support','Release a workflow bottleneck','Move from confusion to clarity','Repair a disconnected chain','Find the key that fits','Sort overload into a system','Turn tangled routes into direction','Growth through a difficult crack','Unlock a blocked opportunity','Find evidence inside data fog','Reach a goal through small steps','Balance knowledge and time','Complete the missing puzzle','Restore depleted energy','Resilience through strong waves','Reduce friction between gears','Filter noise into a clear signal','Use a feedback conversation loop','Automate a repetitive work stack','Balance cost and human value','Grow beyond a learning plateau','Create inside a constraint']),
 ('service','Everyday service journeys',services,[
 'Clinic arrival and reception','Plan an appointment by phone','Queue ticket and waiting time','Consultation room conversation','Prescription collection journey','Laboratory sample handover','Discharge plan and return home','Select an item in an online store','Checkout and payment receipt','Delivery at the doorstep','Parcel return and service record','Bank counter service','Tap into public transport','Hotel check in and room key','Airport luggage screening','Food order and menu choice','Cafe pickup counter','School registration and materials','Library borrowing and approval','Help desk issue resolution','Customer feedback and review','Repair handover and receipt','Community volunteering booth','Event ticket and entry','Renewal and approval cycle'])
]
ENTRANCES=['Slide the main props upward in staggered layers','Reveal the central object with a soft scale and settle','Draw the connector first, then fade in each prop','Unfold the primary panel, then pop in the secondary cue','Bring the foreground props in from opposite sides','Reveal the main group behind a paper wipe','Drop the hero prop gently into its resting position']
AMBIENTS=['Float the accent group slowly by 2–3 pixels','Pulse the focus cue once while the main group stays steady','Move a small highlight across the primary panel','Trace the connector path in a gentle recurring loop','Tilt the secondary prop by 2 degrees and return','Alternate emphasis between the supporting props','Use a subtle depth parallax between main and accent']
EXITS=['Gather the props toward the main group and fade out','Slide the layers downward with a short stagger','Shrink the focus cue, then fade the composition','Wipe the secondary props away before the main group','Fold the central panel closed and fade the details','Track along the connector into the next scene','Let each group drift out with a gentle opacity fall']
USE_CASES={
 'learning':['Educational explainer','Course introduction','Study technique tutorial'],
 'story':['Story opening','Context setting','Narrative transition'],
 'metaphor':['Problem explanation','Solution comparison','Change management explainer'],
 'service':['Service onboarding','Process walkthrough','Customer journey explainer']}

def build():
 OUT.mkdir(parents=True,exist_ok=True);index=[]
 for slug,category,fn,titles in CATALOG:
  assert len(titles)==25
  for k,title in enumerate(titles):
   parts=fn(k);assert len(parts)==3
   sid=f'SV{1001+len(index):04d}'
   layers=''.join(f'<g id="{name}" transform="translate(19.2 19.2) scale(.85)">{art}</g>' for name,art in zip(['main','accent','details'],parts))
   desc='Original layered pastel composition: '+title+'. Main, accent and details are separate animation targets; motion guidance is provided in the index.'
   svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc>{layers}</svg>'
   ET.fromstring(svg);(OUT/f'{sid}.svg').write_text(svg)
   index.append({'id':sid,'title':title,'category':category,'category_slug':slug,'tags':['explainer',slug,'original','layered','pastel','composition']+title.lower().split()[:4],'svg':f'svg/files/{sid}.svg','viewBox':'0 0 256 256','license':'Original generated SVG; reusable','layers':['main','accent','details'],'collection':'explainer','use_cases':USE_CASES[slug]+[title],'suggested_motion':{'entrance':ENTRANCES[k%7],'ambient':AMBIENTS[(k+2)%7],'exit':EXITS[(k+4)%7]}})
 assert len(index)==100 and index[0]['id']=='SV1001' and index[-1]['id']=='SV1100'
 (ROOT/'svg_explainer_learning_index.json').write_text(json.dumps(index,indent=2))
 print(f'Created {len(index)} compositions SV1001–SV1100')

def qa():
 import cairosvg
 from PIL import Image,ImageDraw,ImageFont
 QA.mkdir(parents=True,exist_ok=True);(QA/'png').mkdir(exist_ok=True)
 index=json.loads((ROOT/'svg_explainer_learning_index.json').read_text());hashes=set();bboxes=[];failure=[]
 for row in index:
  path=OUT/f'{row["id"]}.svg';s=path.read_text();ET.fromstring(s)
  assert not any(term in s for term in ['<script','href=','<image','foreignObject'])
  art=s[s.index('<g'):];art=re.sub(r' (?:fill|stroke)="[^"]*"','',art);h=hashlib.sha256(art.encode()).hexdigest();assert h not in hashes;hashes.add(h)
  dest=QA/'png'/f'{row["id"]}.png';cairosvg.svg2png(url=str(path),write_to=str(dest),output_width=256,output_height=256)
  im=Image.open(dest).convert('RGBA');alpha=im.getchannel('A');bbox=alpha.getbbox();assert bbox
  assert alpha.getextrema()[0]==0
  bboxes.append({'id':row['id'],'bbox':list(bbox),'margin':min(bbox[0],bbox[1],256-bbox[2],256-bbox[3])})
  if min(bbox[0],bbox[1],256-bbox[2],256-bbox[3])<12:failure.append(bboxes[-1])
 for slug,category,fn,titles in CATALOG:
  sheet=Image.new('RGB',(1000,1150),'#F1F5F8');d=ImageDraw.Draw(sheet)
  d.text((20,14),category,fill=INK)
  rows=[row for row in index if row['category_slug']==slug]
  for k,row in enumerate(rows):
   x=15+(k%5)*196;y=42+(k//5)*215
   im=Image.open(QA/'png'/f'{row["id"]}.png');im.thumbnail((170,170));sheet.paste(im,(x+10,y),im)
   words=row['title'].split();line='';text=[]
   for word in words:
    if len(line)+len(word)+1>30:text.append(line);line=word
    else:line=(line+' '+word).strip()
   if line:text.append(line)
   d.text((x,y+171),row['id'],fill=INK)
   d.multiline_text((x,y+185),'\n'.join(text[:2]),fill=INK,spacing=2)
  sheet.save(QA/f'contact_{slug}.jpg',quality=93)
 overview=Image.new('RGB',(1600,1840),'white')
 for k,(slug,category,fn,titles) in enumerate(CATALOG):
  im=Image.open(QA/f'contact_{slug}.jpg');im.thumbnail((800,920));overview.paste(im,((k%2)*800,(k//2)*920))
 overview.save(QA/'explainer_learning_100_overview.jpg',quality=93)
 (QA/'bbox_report.json').write_text(json.dumps(bboxes,indent=2))
 report={'count':100,'id_range':'SV1001–SV1100','categories':4,'compositions_per_category':25,'valid_xml':100,'raster_rendered':100,'geometry_unique_ignoring_colours':len(hashes),'transparent':100,'forbidden_content':0,'bbox_margin_required_px':12,'bbox_margin_min_px':min(x['margin'] for x in bboxes),'bbox_failures':failure,'qa_directory':str(QA),'contact_sheets':4,'motion_status':'suggested_motion is authoring guidance only; assets have no embedded animations','viewBox':'0 0 256 256'}
 (ROOT/'svg_explainer_learning_qa.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
 assert not failure,failure
if __name__=='__main__':
 build()
 if '--qa' in sys.argv:qa()
