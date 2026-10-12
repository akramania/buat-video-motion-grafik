"""Seven original motion recipes informed by inspected public reference previews.
No source footage, paid templates, native expressions or source artwork included.
"""
from core import *
from functools import lru_cache
from pathlib import Path
import random

PRESETS={
 'A01':dict(name='Neon Scribble Caption',description='Perkataan muncul berurutan dengan garis neon yang dilukis mengikut cue.',genre='creator',genres=['creator','education','promo'],text='Setiap idea berhak bersinar',subtitle='Tekankan kata penting. Biar mesej mudah diikuti.',source_url='https://elements.envato.com/subtitles-captions-text-animations-XNKHM6X',observed_timestamp='4.75–6.25 s'),
 'A02':dict(name='Sticker Keyword Loops',description='Frasa rapat, jalur tipografi senget dan gelung penanda pada kata pilihan.',genre='promo',genres=['creator','promo','education'],text='FOKUS PADA\nPROSES ANDA',subtitle='Satu mesej. Dua titik penekanan.',source_url='https://elements.envato.com/text-animation-W3Y3XNA',observed_timestamp='16.00–19.25 s'),
 'A03':dict(name='Type Scale Focus',description='Huruf menaip pada skala besar, mengecil ke saiz bacaan dan keluar dengan blur.',genre='saas',genres=['saas','corporate','promo'],text='Penyelesaian',subtitle='Daripada idea besar kepada hasil yang jelas.',source_url='https://elements.envato.com/text-animation-GNG3GYE',observed_timestamp='3.00–5.75 s'),
 'A04':dict(name='Search Bar Typing',description='Bingkai carian dilukis, ikon berubah dan caret mengikuti teks yang ditaip.',genre='saas',genres=['saas','corporate','education'],text='Cari idea anda yang seterusnya',subtitle='Taip pertanyaan. Terokai kemungkinan.',source_url='https://elements.envato.com/typewriter-N25CE6N',observed_timestamp='14.75–17.75 s'),
 'A05':dict(name='Graphic Editorial Opener',description='Bukaan mendatar, tajuk gema besar, jubin grafik dan gerakan kamera pantas.',genre='corporate',genres=['promo','creator','corporate'],text='CERITA BERMULA',subtitle='Cipta ruang untuk pandangan yang baharu.',source_url='https://elements.envato.com/intro-opener-U2Q448Q',observed_timestamp='0.00–4.75 s'),
 'A06':dict(name='Notebook Ink Notes',description='Tajuk buku nota dengan baris berturutan dan dakwat yang melingkari kata.',genre='education',genres=['education','documentary','creator'],text='Belajar sedikit\nfahami lebih\namalkan selalu',subtitle='Catatan kecil, perubahan besar.',source_url='https://elements.envato.com/diary-titles-dr-Y74AGUM',observed_timestamp='0.00–4.50 s'),
 'A07':dict(name='Compressed Depth Stack',description='Perkataan masuk berasingan, bertindan rapat dengan bayang kedalaman, kemudian berpecah.',genre='promo',genres=['promo','creator','corporate'],text='IMPIAN\nJADI\nTINDAKAN',subtitle='Bergerak satu langkah pada satu masa.',source_url='https://elements.envato.com/text-animation-EU7UMQT',observed_timestamp='2.25–5.75 s'),
}


def _lines(s,n=2):
 explicit=[x.strip() for x in s.splitlines() if x.strip()]
 if 1<len(explicit)<=5:return explicit
 words=s.split()
 if not words:return ['']
 n=min(n,len(words));out=[];start=0
 for i in range(n):
  stop=round((i+1)*len(words)/n);out.append(' '.join(words[start:stop]));start=stop
 return out


def _note(im,s,p,t,y=558):
 if not s:return
 text(im,s,640,y,fit_size(s,1000,22,'sans'),p['muted'],'sans',opacity=life(t,.9,1.4,4.05,4.6))


def _trim(points,p):
 if p<=0:return []
 n=(len(points)-1)*clamp(p);k=int(n);out=points[:k+1]
 if k<len(points)-1:
  out.append((mix(points[k][0],points[k+1][0],n-k),mix(points[k][1],points[k+1][1],n-k)))
 return out


def _stroke(im,points,p,color,width=3,glow=False,opacity=1):
 pts=_trim(points,p)
 if len(pts)<2:return
 if glow:
  lay=layer();line(lay,pts,rgba(color,180*opacity),width+5)
  im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(11)))
 line(im,pts,rgba(color,255*opacity),width)


def _loop(cx,cy,rx,ry,turns=1.12):
 return [(cx+rx*math.cos(-.35+i/160*math.tau*turns),cy+ry*math.sin(-.35+i/160*math.tau*turns)+2*math.sin(i*.17)) for i in range(161)]


def _star(im,x,y,r,color,angle=0):
 pts=[]
 for i in range(8):
  a=angle+i*math.pi/4;rrr=r if i%2==0 else r*.22
  pts.append((x+rrr*math.cos(a),y+rrr*math.sin(a)))
 target=layer(*im.size);ImageDraw.Draw(target).polygon(pts,fill=color);im.alpha_composite(target)


@lru_cache(maxsize=64)
def _gradient_text(s,size,left,right):
 mask=text_img(s,size,'#FFFFFF').getchannel('A');w,h=mask.size
 a=np.linspace(0,1,w)[None,:,None];c=np.array(rgb(left))[None,None,:]*(1-a)+np.array(rgb(right))[None,None,:]*a
 arr=np.repeat(np.uint8(c),h,axis=0);im=Image.fromarray(arr).convert('RGBA');im.putalpha(mask);return im


@lru_cache(maxsize=16)
def _paper(panel_color,accent):
 im=layer(948,406);rr(im,(0,0,947,405),'#F7F4EC',24)
 overlay=layer(948,406);d=ImageDraw.Draw(overlay)
 for x in range(28,948,26):d.line((x,0,x,406),fill=rgba(accent,19),width=1)
 for y in range(16,406,26):d.line((0,y,948,y),fill=rgba(accent,19),width=1)
 # Fold creases drawn by hand here, not a sampled source texture.
 d.polygon([(0,276),(560,120),(948,177),(948,220),(570,143),(0,291)],fill=(228,225,218,45))
 d.line([(0,276),(560,120),(948,177)],fill=(207,206,199,90),width=1)
 d.line([(110,0),(460,406)],fill=(255,255,255,160),width=3)
 d.line([(113,0),(463,406)],fill=(200,194,183,28),width=2)
 im.alpha_composite(overlay);return im


@lru_cache(maxsize=12)
def _architecture(accent,secondary):
 """Original graphic city, intentionally illustrative; image_path may replace it."""
 im=Image.new('RGBA',(1420,480),'#142039');d=ImageDraw.Draw(im);overlay=layer(1420,480);gl=ImageDraw.Draw(overlay);rng=random.Random(18)
 for i in range(26):
  x=i*60-30;y=rng.randrange(24,260);w=rng.randrange(40,95)
  fill=(20+i%4*7,33+i%5*6,56+i%3*12,255)
  d.rectangle((x,y,x+w,480),fill=fill)
  d.polygon([(x+w,y),(x+w+25,y+22),(x+w+25,480),(x+w,480)],fill=(9,19,35,255))
  for yy in range(y+15,480,23):
   for xx in range(x+10,x+w-5,16):
    if rng.random()>.25:gl.rectangle((xx,yy,xx+5,yy+8),fill=rgba(accent,65 if rng.random()>.45 else 25))
 for j in range(18):
  xx=j*95;gl.line((xx,0,xx-100,480),fill=(175,200,240,11),width=2)
 im.alpha_composite(overlay);return im


@lru_cache(maxsize=4)
def _image_asset(path):
 if not path:return None
 src=Image.open(Path(path).expanduser()).convert('RGB')
 ratio=max(1420/src.width,480/src.height);src=src.resize((round(src.width*ratio),round(src.height*ratio)),Image.Resampling.LANCZOS)
 return src.crop(((src.width-1420)//2,(src.height-480)//2,(src.width+1420)//2,(src.height+480)//2)).convert('RGBA')


def _a01(t,cfg):
 p=palette(cfg);im=base(cfg);a=1-leave(t);words=cfg['text'].split();groups=_lines(cfg['text'].replace('\n',' '),2);size=min(fit_size(s,890,62) for s in groups)
 idx=0
 for j,s in enumerate(groups):
  row=s.split();width=measure(s,size);x=640-width/2;y=285+j*84
  for k,w in enumerate(row):
   u=pop(prog(t,.18+idx*.075,.75+idx*.075));alpha=clamp(u)*a;ink=p['accent'] if idx==len(words)-1 else p['text'];img=text_img(w,size,ink)
   blur=(1-clamp(u))*7
   if blur>.2:img=img.filter(ImageFilter.GaussianBlur(blur))
   paste(im,img,x,y+(1-u)*35,opacity=alpha,anchor='left');x+=measure(w+' ',size);idx+=1
 last=groups[-1];w=measure(last,size);yy=380+(len(groups)-2)*84
 pts=[(640-w/2+u*w,yy+19+14*math.sin(u*math.pi*2.5)) for u in np.linspace(0,1,120)]
 # A flowing return loop continues after the first underline stroke.
 pts += [(640+w/2-u*w*.7,yy+26+21*math.sin(u*math.pi)) for u in np.linspace(0,1,65)]
 _stroke(im,pts,ease(prog(t,.62,1.55)),p['accent'],3,True,a)
 star=layer(110,110);_star(star,55,55,29,p['accent'],t*.16);_star(star,85,24,9,p['secondary']);paste(im,star,1080,320,life(t,.72,1.2),pop(prog(t,.72,1.2)))
 _note(im,cfg['subtitle'],p,t,513);return im


def _a02(t,cfg):
 p=palette(cfg);im=base(cfg);rows=_lines(cfg['text'],2);size=min(min(fit_size(s,900,68) for s in rows),int(220/max(1,len(rows))));gap=min(94,230/max(1,len(rows)-1));a=1-leave(t)
 for j,s in enumerate(rows):
  u=pop(prog(t,.18+j*.18,.82+j*.18));y=320+(j-(len(rows)-1)/2)*gap+(1-u)*(90 if j%2 else -70)
  glyph=text_img(s,size,p['bg']);strip=layer(glyph.width+30,glyph.height+23);rr(strip,(0,0,strip.width-1,strip.height-1),p['text'],2);paste(strip,glyph,strip.width/2,strip.height/2)
  paste(im,strip,640,y,clamp(u)*a,scale=.85+.15*u,angle=-3 if j%2 else 2)
  words=s.split();key=words[-1] if j==0 else words[0];full=measure(s,size);kw=measure(key,size)
  cx=640+full/2-kw/2 if j==0 else 640-full/2+kw/2
  _stroke(im,_loop(cx,y,kw/2+22,size*.54),ease(prog(t,.78+j*.23,1.3+j*.23)),p['accent'],4,False,a)
 _note(im,cfg['subtitle'],p,t,518);return im


def _a03(t,cfg):
 p=palette(cfg);im=base(cfg);s=cfg['text'].replace('\n',' ');n=min(len(s),int(prog(t,.25,1.2)*(len(s)+1)));size=fit_size(s,650,82);scale=mix(1.62,1,smooth(prog(t,1.18,2.15)))
 pic=_gradient_text(s[:n],size,p['secondary'],p['accent']);a=life(t,.17,.45);out=leave(t);blur=(1-enter(t,.18,.5))*6+out*14
 if blur>.2:pic=pic.filter(ImageFilter.GaussianBlur(blur))
 paste(im,pic,640,340-out*32,a,scale=scale*(1-out*.1))
 # Two focus rails close to frame the final word without obscuring it.
 width=measure(s,size)*scale/2+40;u=smooth(prog(t,1.25,2.1))*a
 for side in [-1,1]:
  x=640+side*width;line(im,[(x,302),(x,378)],rgba(p['accent'],130*u),2)
  line(im,[(x,302),(x-side*13,302)],rgba(p['accent'],130*u),2);line(im,[(x,378),(x-side*13,378)],rgba(p['accent'],130*u),2)
 _note(im,cfg['subtitle'],p,t,503);return im


def _search_path():
 pts=[]
 # Rounded rect path begins at the upper-right edge and sweeps around.
 for cx,cy,a0,a1 in [(1068,327,-90,0),(1068,365,0,90),(212,365,90,180),(212,327,180,270)]:
  pts.extend([(cx+46*math.cos(a),cy+46*math.sin(a)) for a in np.linspace(math.radians(a0),math.radians(a1),28)])
 return pts+[pts[0]]
_SEARCH_PATH=_search_path()

def _a04(t,cfg):
 p=palette(cfg);im=base(cfg);a=1-leave(t);u=enter(t,.15,.82);shell=layer();rr(shell,(166,281,1114,411),rgba(p['panel'],180),65);paste(im,shell,640,360,clamp(u)*a)
 _stroke(im,_SEARCH_PATH,ease(prog(t,.15,.94)),p['accent'],2,True,a)
 ic=life(t,.45,.85)*a
 if t<1.18:
  _star(im,218,346,18,rgba(p['accent'],255*ic),t)
 else:
  circle(im,217,340,10,None,rgba(p['text'],255*a),3);line(im,[(225,349),(235,359)],rgba(p['text'],255*a),3)
 s=cfg['text'].replace('\n',' ');size=fit_size(s,790,42,'sans');n=min(len(s),int(prog(t,.95,2.45)*(len(s)+1)));shown=s[:n];text(im,shown,263,346,size,p['text'],'sans',opacity=a,anchor='left')
 caret_x=263+measure(shown,size,'sans')+5
 if t>.8 and (t<2.45 or int((t-2.45)*2.3)%2==0):line(im,[(caret_x,321),(caret_x,371)],rgba(p['accent'],255*a),2)
 # Selected suggestion demonstrates a separate secondary layer, not typing jitter.
 w=measure('IDEA DIPILIH',15,'mono')+44;v=life(t,2.5,2.85,4.05,4.65)
 rr(im,(640-w/2,438,640+w/2,470),rgba(p['accent'],25*v),16,rgba(p['accent'],70*v));text(im,'IDEA DIPILIH',640,454,15,p['accent'],'mono',opacity=v)
 _note(im,cfg['subtitle'],p,t,537);return im


def _a05(t,cfg):
 p=palette(cfg);im=base(cfg);a=1-leave(t);v=enter(t,.12,.8);scene=layer(1120,414);asset=_image_asset(cfg.get('image_path','')) or _architecture(p['accent'],p['secondary'])
 # Original city drawing is replaceable with an authorized image_path.
 drift=round(42*math.sin(t*.48)+18*math.sin(t*1.2));scene.alpha_composite(asset,(-150+drift,-34));veil=layer(1120,414);rr(veil,(0,0,1119,413),(6,14,29,70),0);scene.alpha_composite(veil)
 title=cfg['text'].replace('\n',' ').upper();size=fit_size(title,820,76);fg=cfg.get('text_color','#F4F7FC');echo=text_img(title,size*2,fg);paste(scene,echo,560+24*math.sin(t*.8),199,opacity=.085,scale=1.12)
 # Small marks are at fixed seeded locations and animate by their own timing.
 for j,(x,y) in enumerate([(65,54),(202,319),(890,51),(1033,282),(730,340),(386,83),(966,177)]):
  pulse=.45+.4*math.sin(t*1.3+j);rr(scene,(x,y,x+12+j%3*7,y+12+j%3*7),rgba(p['accent'],130*life(t,.2+j*.065,.7+j*.065)*pulse),0)
 for x0,y0 in [(38,238),(951,60)]:
  for row in range(5):
   for col in range(8):circle(scene,x0+col*10,y0+row*10,.9,rgba(p['text'],70))
 # A short track-in repeats on two editorial beats; text is readable between them.
 beat=max(0,1-abs(t-1.65)/.16,max(0,1-abs(t-3.0)/.16));intro=enter(t,.3,.95);glyph=text_img(title,size,fg);paste(scene,glyph,560,199,opacity=intro,scale=1+(1-intro)*.25+beat*.09)
 streak=layer(1120,414);line(streak,[(240+35*math.sin(t),220),(980,220)],rgba(p['secondary'],85*beat),2);scene.alpha_composite(streak.filter(ImageFilter.GaussianBlur(3)))
 # Horizontal aperture provides a clear entrance and closing motion.
 mask=Image.new('L',scene.size);dd=ImageDraw.Draw(mask);hh=round(207*v*(1-leave(t)));
 if hh>0:dd.rectangle((0,207-hh,1120,207+hh),fill=255)
 scene.putalpha(mask);paste(im,scene,640,359)
 _note(im,cfg['subtitle'],p,t,598);return im


def _a06(t,cfg):
 p=palette(cfg);im=base(cfg);a=life(t,.15,.72);card=_paper(p['panel'],p['accent']);paste(im,card,640,359,a,scale=.97+.03*enter(t,.15,.72),angle=.3*math.sin(t*.5))
 rows=_lines(cfg['text'],3);size=min(min(fit_size(s,745,48,'sans') for s in rows),int(225/max(1,len(rows))));step=min(72,246/max(1,len(rows)));start=343-step*(len(rows)-1)/2
 for j,s in enumerate(rows):
  u=enter(t,.2+j*.18,.73+j*.18);out=leave(t,4.2+j*.06,4.76+j*.04);pic=text_img(s,size,'#243249','sans');blur=(1-u)*10+out*10
  if blur>.2:pic=pic.filter(ImageFilter.GaussianBlur(blur))
  paste(im,pic,640,start+j*step+(1-u)*-23+out*22,u*(1-out))
  width=measure(s,size,'sans');inkp=ease(prog(t,.8+j*.23,1.36+j*.23))*(1-smooth(prog(t,3.85+j*.08,4.34+j*.06)))
  if j%2==0:pts=_loop(640,start+j*step+2,width/2+19,size*.64,1.06)
  else:pts=[(640-width/2+z*width,start+j*step+size*.58+1.8*math.sin(z*math.pi*3)) for z in np.linspace(0,1,120)]
  _stroke(im,pts,inkp,p['accent'],2,False,a)
 _note(im,cfg['subtitle'],p,t,592);return im


def _a07(t,cfg):
 p=palette(cfg);im=base(cfg);rows=_lines(cfg['text'],3);size=min(min(fit_size(s,800,83) for s in rows),int(255/max(1,len(rows))));step=min(84,240/max(1,len(rows)-1));center=335;out=leave(t)
 for j,s in enumerate(rows):
  u=pop(prog(t,.18+j*.18,.77+j*.18));y=center+(j-(len(rows)-1)/2)*step+(1-u)*(90 if j%2 else -110);dx=(1-u)*(130 if j%2 else -130)
  ex=leave(t,4.13+j*.085,4.67+j*.08);x=640+dx+ex*(520 if j%2 else -520);y+=ex*(55 if j%2 else -55)
  pic=text_img(s,size,p['text']);vol=layer(pic.width+20,pic.height+20)
  shadow=text_img(s,size,p['secondary'])
  for k in range(9,0,-1):paste(vol,shadow,k+pic.width/2,k+pic.height/2,opacity=.13)
  paste(vol,pic,pic.width/2,pic.height/2)
  paste(im,vol,x,y,clamp(u)*(1-ex),scale=.93+.07*u,angle=(1-u)*(-8 if j%2 else 8))
 # Editorial rule slides independently during the phrase hold.
 q=life(t,1.05,1.6,4.05,4.6);line(im,[(585,507),(585+110*q,507)],rgba(p['accent'],255*q),4)
 _note(im,cfg['subtitle'],p,t,556);return im

_FUNCS={'A01':_a01,'A02':_a02,'A03':_a03,'A04':_a04,'A05':_a05,'A06':_a06,'A07':_a07}
def render(pid,t,cfg):
 if pid not in _FUNCS:raise ValueError('Unknown new reference preset '+pid)
 return _FUNCS[pid](t,cfg)
