"""Reusable deterministic showcase layers; no project media or product copy.

Draw words first, then project an actual source frame over them. The 15 named
mechanisms are custom adaptations, not registered Atlas preset IDs. Pillow,
NumPy and OpenCV are required. Angles use degrees; coordinates use canvas pixels.
"""
from pathlib import Path
from functools import lru_cache
from types import SimpleNamespace
import math
import numpy as np
import cv2
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps

MECHANISMS=('stomp','ribbon_split','hinge','orbit','card_snap','fold','window',
            'domino','depth','tracking','brush','magnet','rolling_word','arc','stencil')
_DEFAULT_FONT=Path(__file__).resolve().parents[1]/'assets/motion_presets/fonts/DejaVuSans-Bold.ttf'
def clamp(x):return max(0.,min(1.,x))
def ease(x):return 1-(1-clamp(x))**3
def back(q):
    q=clamp(q);c=1.70158;return 1+(c+1)*(q-1)**3+c*(q-1)**2
@lru_cache(128)
def _font(size,path=''):
    return ImageFont.truetype(path or str(_DEFAULT_FONT),max(1,int(size)))
def _round_rect(im,box,fill,r=20):
    ImageDraw.Draw(im).rounded_rectangle(tuple(round(x) for x in box),r,fill)
def _paste(dst,src,x,y,alpha=1,scale=1):
    if alpha<=0 or scale<=0:return
    if abs(scale-1)>.001:src=src.resize((max(1,round(src.width*scale)),max(1,round(src.height*scale))),Image.Resampling.BICUBIC)
    if alpha<.999:src=src.copy();src.putalpha(src.getchannel('A').point(lambda v:round(v*clamp(alpha))))
    dst.alpha_composite(src,(round(x-src.width/2),round(y-src.height/2)))
B=SimpleNamespace(rr=_round_rect,put=_paste)

@lru_cache(128)
def word_sprite(word,size,color,plate='',plate_ink='',font_path=''):
    f=_font(size,font_path);adv=f.getlength(word);pad=17 if plate else 5
    z=Image.new('RGBA',(round(adv+2*pad),round(size*1.32)))
    if plate:B.rr(z,(0,6,z.width-1,z.height-7),plate,12)
    ImageDraw.Draw(z).text((pad,round(size*.06)),word,font=f,fill=plate_ink or color,stroke_width=0)
    return z

@lru_cache(128)
def layout(rows,nominal,max_width,font_path,max_height,line_gap,plate_padding):
    f=_font(nominal,font_path)
    extra=max(len(row.split()) for row in rows)*plate_padding
    adv=max(f.getlength(row) for row in rows)
    width_fit=nominal*max(1,max_width-extra)/max(1,adv)
    height_fit=max_height/((len(rows)-1)*line_gap+1.32)
    fs=max(8,int(min(nominal,width_fit,height_fit)))
    f=_font(fs,font_path);gap=fs*line_gap;words=[];idx=0
    actual_width=max(sum(f.getlength(w)+plate_padding for w in row.split())+f.getlength(' ')*(len(row.split())-1) for row in rows)
    if actual_width>max_width+1 or (len(rows)-1)*gap+fs*1.32>max_height+1:
        raise ValueError('text cannot fit at the minimum font size; split it into shorter rows')
    for j,row in enumerate(rows):
        split=row.split();widths=[f.getlength(w)+plate_padding for w in split];space=f.getlength(' ')
        x=-(sum(widths)+space*(len(widths)-1))/2
        for word,ww in zip(split,widths):
            words.append(dict(word=word,x=x+ww/2,y=(j-(len(rows)-1)/2)*gap,fs=fs,idx=idx,row=j))
            idx+=1;x+=ww+space
    return words,fs

def rot_put(dst,src,x,y,scale=1,angle=0,alpha=1,shadow=False):
    if alpha<=0 or scale<=0:return
    if shadow:
        sh=Image.new('RGBA',src.size,(0,0,0,0));sh.putalpha(src.getchannel('A').point(lambda v:int(v*.22)))
        B.put(dst,sh.filter(ImageFilter.GaussianBlur(4)),x+5,y+7,alpha,scale)
    if angle:src=src.rotate(angle,Image.Resampling.BICUBIC,expand=True)
    B.put(dst,src,x,y,alpha,scale)

def shifted_crop(src,q,vertical=True):
    q=clamp(q);out=Image.new('RGBA',src.size)
    if q<=0:return out
    if vertical:
        off=round(src.height*(1-q));out.alpha_composite(src,(0,off))
    else:
        cut=round(src.width*q);out.alpha_composite(src.crop((0,0,cut,src.height)),(0,0))
    return out

def tracked(word,fs,color,gap,font_path):
    f=_font(fs,font_path);ww=sum(f.getlength(c) for c in word)+max(0,len(word)-1)*gap
    z=Image.new('RGBA',(max(1,round(ww+10)),round(fs*1.32)));d=ImageDraw.Draw(z);x=5
    for ch in word:d.text((x,round(fs*.06)),ch,font=f,fill=color);x+=f.getlength(ch)+gap
    return z

def _draw_words(dst,scene,u,cx,cy,scale=1,alpha=1,angle=0):
    words,fs=layout(tuple(scene['rows']),scene['fs'],scene['max_width'],scene['font_path'],scene['max_height'],scene['line_gap'],scene['plate_padding']);n=len(words)
    total=scene['ready'];dur=total*(.66 if n<3 else .56);delay=max(0.,(total-dur)/max(1,n-1))
    style=scene['style']
    for j,w in enumerate(words):
        tu=u+scene['lead_in']
        q=clamp((tu-j*delay)/dur);e=ease(q);settle=back(q)
        if q<=0:continue
        c=scene['accent'] if (j==n-1 or (w['row']%2==1 and n>3)) else scene['ink']
        plate='';plateink=''
        if style in {'card_snap','magnet'}:
            colors=scene['plates'];plate=colors[w['row']%len(colors)];plateink=scene['plate_ink']
        sp=word_sprite(w['word'],fs,c,plate,plateink,scene['font_path'])
        dx=dy=rot=0.;sc=1.;a=e
        if style=='stomp':
            dy=140*(1-settle);sc=1.28-.28*settle;rot=(-5 if j%2 else 5)*(1-e);a=min(1,q*6)
        elif style=='ribbon_split':
            z=Image.new('RGBA',sp.size);h=sp.height//2;off=round(110*(1-e))
            z.alpha_composite(sp.crop((0,0,sp.width,h)),(-off,0));z.alpha_composite(sp.crop((0,h,sp.width,sp.height)),(off,h));sp=z
            sc=.93+.07*e;rot=(1-e)*(-8 if j%2 else 8)
        elif style=='hinge':
            sy=max(.05,math.cos((1-e)*math.pi*.48));sp=sp.resize((sp.width,max(1,round(sp.height*sy))),Image.Resampling.BICUBIC)
            dy=-65*(1-e);rot=-12*(1-e);a=min(1,q*5)
        elif style=='orbit':
            phase=(1-e)*math.pi*1.55;rad=(160+j*9)*(1-e)
            dx=math.sin(phase+j*.45)*rad;dy=math.cos(phase+j*.45)*rad;rot=(1-e)*(-65 if j%2 else 65);sc=.5+.5*e
        elif style=='card_snap':
            dx=(-90 if j%2 else 90)*(1-e);dy=90*(1-e);rot=(17 if j%2 else -17)*(1-settle);sc=.5+.5*settle
        elif style=='fold':
            sx=max(.04,math.cos((1-e)*math.pi*.49));sp=sp.resize((max(1,round(sp.width*sx)),sp.height),Image.Resampling.BICUBIC)
            dx=-(sp.width/3)*(1-e);rot=8*(1-e);a=min(1,q*5)
        elif style=='window':
            sp=shifted_crop(sp,e,True);dx=32*(1-e);a=1
        elif style=='domino':
            rot=-88*(1-e);dx=-sp.width*.30*(1-e);dy=sp.width*.42*(1-e);a=min(1,q*7)
        elif style=='depth':
            sc=2.75-1.75*e;dy=-32*(1-e);a=min(1,q*4)
            if q<.7:sp=sp.filter(ImageFilter.GaussianBlur((1-e)*7))
        elif style=='tracking':
            sp=tracked(w['word'],fs,c,fs*.28*(1-e),scene['font_path']);sc=.85+.15*e;dy=20*(1-e)
        elif style=='brush':
            mask=np.zeros((sp.height,sp.width),np.uint8);yy=np.arange(sp.height);front=sp.width*e+9*(1-e)*np.sin(yy*.21+j)
            mask[:]=np.uint8(np.arange(sp.width)[None,:]<=front[:,None])*255
            sp=sp.copy();sp.putalpha(Image.fromarray(np.minimum(np.array(sp.getchannel('A')),mask)))
            dy=18*(1-e);a=1
        elif style=='magnet':
            dx=(-260 if j%2 else 260)*(1-settle);dy=(130 if j%2 else -130)*(1-settle);rot=(35 if j%2 else -35)*(1-e);sc=.72+.28*e
        elif style=='rolling_word':
            z=Image.new('RGBA',sp.size);shift=round(sp.height*(1-e))
            z.alpha_composite(sp,(0,shift));z.alpha_composite(sp,(0,shift-sp.height));sp=z;dx=50*(1-e);rot=5*(1-e);a=min(1,q*6)
        elif style=='arc':
            # Cubic path with a rotating tangent; one independent path per word.
            p=1-e;dx=(220-90*j)*p*p;dy=-210*p+170*p*p;rot=(26-13*j)*p;sc=.65+.35*e
        elif style=='stencil':
            ar=np.array(sp);xx=np.arange(sp.width);phase=(xx//10)%2
            prog=np.where(phase==0,min(1,q*2),max(0,(q-.22)/.78));ar[:,:,3]=np.uint8(ar[:,:,3]*prog[None,:]);sp=Image.fromarray(ar)
            dy=-34*(1-e);sc=.92+.08*e;a=1
        arad=math.radians(angle);px=(w['x']+dx)*scale;py=(w['y']+dy)*scale
        x=cx+px*math.cos(arad)-py*math.sin(arad);y=cy+px*math.sin(arad)+py*math.cos(arad)
        rot_put(dst,sp,x,y,scale*sc,rot+angle,alpha*a,shadow=bool(plate))

def draw_word_group(canvas,rows,time,*,mechanism='stomp',complete_at=.7,
                    centre=None,font_size=96,font_path='',max_width=None,
                    max_height=None,line_gap=None,lead_in=0.,scale=1.,angle=0.,
                    opacity=1.,ink='#F8F1E5',accent='#DDFA94',
                    plates=('#DDFA94','#C8B8F0','#FFA990','#B9DBEB'),
                    plate_ink='#201C2D',audit=None,cue_id='words'):
    """Draw independent word entrances, then apply the caller's parent transform.

    `complete_at` is the upper bound for entrance completion, in local seconds.
    `lead_in` is explicit pre-roll. Use caller timing to hold complete words before
    footage arrives. Parent `centre/scale/angle/opacity` can then relocate the text.
    Returns the fitted font size and word count. Use an external frame audit dict.
    """
    if canvas.mode!='RGBA':raise ValueError('canvas must be RGBA')
    rows=tuple(x.strip() for x in (rows.splitlines() if isinstance(rows,str) else rows) if x.strip())
    if not rows:raise ValueError('provide at least one nonempty text row')
    if mechanism not in MECHANISMS:raise ValueError(f'unknown word mechanism: {mechanism}')
    values=[time,complete_at,font_size,lead_in,scale,angle,opacity]
    if not all(math.isfinite(float(v)) for v in values):raise ValueError('timing and transforms must be finite')
    if complete_at<=0 or font_size<8 or scale<=0:raise ValueError('use positive completion time, font size >=8 and positive scale')
    if not plates:raise ValueError('provide at least one plate colour')
    centre=centre or (canvas.width/2,canvas.height/2)
    max_width=float(canvas.width*.84 if max_width is None else max_width)
    max_height=float(canvas.height*.55 if max_height is None else max_height)
    if not all(math.isfinite(v) and v>0 for v in (max_width,max_height)):raise ValueError('text bounds must be finite and positive')
    plate_style=mechanism in {'card_snap','magnet'}
    cfg=dict(rows=rows,style=mechanism,ready=float(complete_at),fs=int(font_size),
             font_path=str(font_path),max_width=max_width,max_height=max_height,
             line_gap=float(line_gap or (1.4 if plate_style else 1.15)),
             plate_padding=34 if plate_style else 0,lead_in=float(lead_in),
             ink=ink,accent=accent,plates=plates,plate_ink=plate_ink)
    _draw_words(canvas,cfg,float(time),*centre,float(scale),float(opacity),float(angle))
    words,actual_size=layout(rows,cfg['fs'],max_width,cfg['font_path'],max_height,cfg['line_gap'],cfg['plate_padding'])
    if audit is not None:
        item=audit.setdefault(cue_id,{'mechanism':mechanism,'implementation_fn':'showcase_layers.draw_word_group/'+mechanism,'frames':0,'words':[w['word'] for w in words]})
        if item['mechanism']!=mechanism:raise ValueError('one cue_id must identify one mechanism')
        item['frames']+=1
    return {'font_size':actual_size,'word_count':len(words),'complete_by':max(0.,complete_at-lead_in)}


def perspective_quad(centre,width,height,yaw=0.,pitch=0.,roll=0.,depth=1900.):
    """Return TL, TR, BR, BL after a common projected plane transform."""
    values=[*centre,width,height,yaw,pitch,roll,depth]
    if not all(math.isfinite(float(v)) for v in values) or min(width,height,depth)<=0:raise ValueError('use finite coordinates and positive dimensions/depth')
    pts=np.array([[-width/2,-height/2,0],[width/2,-height/2,0],[width/2,height/2,0],[-width/2,height/2,0]],float)
    a,b,c=np.radians([yaw,pitch,roll])
    ry=np.array([[math.cos(a),0,math.sin(a)],[0,1,0],[-math.sin(a),0,math.cos(a)]])
    rx=np.array([[1,0,0],[0,math.cos(b),-math.sin(b)],[0,math.sin(b),math.cos(b)]])
    rz=np.array([[math.cos(c),-math.sin(c),0],[math.sin(c),math.cos(c),0],[0,0,1]])
    p=pts@(rz@ry@rx).T
    if np.any(depth+p[:,2]<=1):raise ValueError('projected plane crosses the camera')
    f=depth/(depth+p[:,2])
    return np.float32(np.column_stack([centre[0]+p[:,0]*f,centre[1]+p[:,1]*f]))


@lru_cache(1)
def _phone_shell():
    z=Image.new('RGBA',(460,942));d=ImageDraw.Draw(z)
    for box,col,r in [((4,0,455,941),'#B8B3C5',56),((8,3,452,938),'#47414F',53),((12,7,448,934),'#09090D',49),((1,163,7,219),'#918B9E',3),((1,239,7,316),'#918B9E',3),((453,220,459,330),'#A49BAC',3)]:_round_rect(z,box,col,r)
    d.line((35,8,423,8),fill='#F3EDF5',width=1);d.line((10,91,10,845),fill='#D2CCDA',width=1)
    return z


def phone_texture(screen,*,fit='contain',camera_slot=True):
    """Place a real source image in generic hardware without altering its UI.

    `contain` preserves the entire input and letterboxes. Choose `cover` only
    after checking the resulting source crop against the requested framing.
    """
    if fit not in {'contain','cover'}:raise ValueError('fit must be contain or cover')
    if screen.width<1 or screen.height<1:raise ValueError('screen cannot be empty')
    source=screen.convert('RGBA')
    viewport=Image.new('RGBA',(420,884),'#000000')
    image=ImageOps.contain(source,viewport.size,Image.Resampling.LANCZOS) if fit=='contain' else ImageOps.fit(source,viewport.size,Image.Resampling.LANCZOS)
    viewport.alpha_composite(image,((420-image.width)//2,(884-image.height)//2))
    mask=Image.new('L',viewport.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,419,883),radius=32,fill=255);viewport.putalpha(mask)
    tex=_phone_shell().copy();tex.alpha_composite(viewport,(20,26));d=ImageDraw.Draw(tex)
    if camera_slot:
        d.rounded_rectangle((166,31,294,48),9,fill='#030306');d.ellipse((303,34,313,44),fill='#1C2333',outline='#5A586B')
    d.rounded_rectangle((193,920,269,924),2,fill='#BBB5C5');d.line((16,105,16,837),fill=(240,236,255,75),width=2)
    return tex


def project_phone(canvas,screen,*,centre=None,width=400.,yaw=8.,pitch=0.,
                  roll=-2.,depth=1900.,fit='contain',camera_slot=True,
                  opacity=1.,shadow=True):
    """Project screen, rim, buttons and camera together; return the common quad.

    Call after draw_word_group to make the device overlap already-read words.
    Caller controls entrance and hold coordinates, and checks the quad bounds.
    """
    if canvas.mode!='RGBA':raise ValueError('canvas must be RGBA')
    if not math.isfinite(float(opacity)) or not 0<=opacity<=1:raise ValueError('opacity must be in 0..1')
    centre=centre or (canvas.width/2,canvas.height/2)
    tex=phone_texture(screen,fit=fit,camera_slot=camera_slot)
    q=perspective_quad(centre,width,width*tex.height/tex.width,yaw,pitch,roll,depth)
    if shadow and opacity>0:
        shade=Image.new('RGBA',canvas.size);ImageDraw.Draw(shade).polygon([tuple(p+[10,20]) for p in q],fill=(0,0,0,round(120*opacity)))
        canvas.alpha_composite(shade.filter(ImageFilter.GaussianBlur(15)))
    mat=cv2.getPerspectiveTransform(np.float32([[0,0],[460,0],[460,942],[0,942]]),q)
    ar=cv2.warpPerspective(np.asarray(tex),mat,canvas.size,flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
    if opacity<1:ar[:,:,3]=np.uint8(ar[:,:,3]*opacity)
    canvas.alpha_composite(Image.fromarray(ar))
    return q.tolist()
