"""Original kinetic typography recipes reconstructed from inspected public previews.
Source motion observations are documented in PRESETS; adapted variants are labelled.
All glyphs and graphics are rendered locally. No paid source artwork is included.
"""
from core import *
from functools import lru_cache

PRESETS = {}


def _rows(value, count=2):
    s=str(value or '')
    rows=[r.strip() for r in s.splitlines() if r.strip()]
    if len(rows)>1: return rows[:5]
    words=s.split()
    if not words: return ['']
    count=min(count,len(words))
    return [' '.join(words[round(j*len(words)/count):round((j+1)*len(words)/count)]) for j in range(count)]


def _cue(cfg, key, default):
    """Cue values use the same normalized 0–5 clock as this module. Render duration retimes the entire motion."""
    return float(cfg.get(key,default))


def _note(im,cfg,p,t,y=561):
    s=str(cfg.get('subtitle',''))
    if s:
        text(im,s,640,y,fit_size(s,1020,22,'sans'),p['muted'],'sans',opacity=life(t,.8,1.2,4.1,4.7))


def _row_size(rows,max_width=960,size=83):
    return min([fit_size(s,max_width,size) for s in rows] or [size])


def _xform(src,sx=1,sy=1,skew=0):
    """Transform local sprite with enough padding to keep shear inside its bounds."""
    out=src.resize((max(1,round(src.width*max(.01,sx))),max(1,round(src.height*max(.01,sy)))),Image.Resampling.BICUBIC)
    if abs(skew)>.002:
        pad=math.ceil(abs(skew)*out.height)+3
        base_im=layer(out.width+2*pad,out.height)
        base_im.alpha_composite(out,(pad,0))
        out=base_im.transform(base_im.size,Image.Transform.AFFINE,(1,skew,-skew*out.height/2,0,1,0),Image.Resampling.BICUBIC)
    return out


@lru_cache(maxsize=128)
def _outline(s,size,color,width=2):
    solid=text_img(s,size,'#FFFFFF')
    mask=solid.getchannel('A')
    expanded=mask.filter(ImageFilter.MaxFilter(max(3,2*int(width)+1)))
    # Expand the local text box before outlining, avoiding clipped stroke extents.
    pad=int(width)+3
    z=layer(solid.width+2*pad,solid.height+2*pad)
    mm=Image.new('L',z.size);mm.paste(mask,(pad,pad))
    ring=Image.fromarray(np.maximum(0,np.asarray(mm.filter(ImageFilter.MaxFilter(2*int(width)+1)),dtype=np.int16)-np.asarray(mm,dtype=np.int16)).astype('uint8'))
    z.paste(rgb(color)+(255,),(0,0,z.width,z.height));z.putalpha(ring)
    return z


def _glow(im,src,x,y,color,opacity=1,radius=9):
    pad=max(4,round(radius*3))
    z=layer(src.width+2*pad,src.height+2*pad)
    tint=Image.new('RGBA',src.size,rgb(color)+(255,));tint.putalpha(src.getchannel('A'))
    z.alpha_composite(tint,(pad,pad))
    paste(im,z.filter(ImageFilter.GaussianBlur(radius)),x,y,opacity*.58)
    paste(im,src,x,y,opacity)


def _glyphs(s,size):
    f=font(size);x=0;out=[]
    for ch in s:
        advance=f.getlength(ch);out.append((ch,x,advance));x+=advance
    return out,x


def _k06(t,cfg):
    p=palette(cfg);im=base(cfg);rows=_rows(cfg.get('text',''),3);size=_row_size(rows,920,85)
    gap=min(90,220/max(1,len(rows)-1));a=1-leave(t)
    strength=clamp(float(cfg.get('elasticity',.65)),.1,.84)
    for j,s in enumerate(rows):
        q=prog(t,.10+j*.11,.88+j*.11);e=pop(q);v=clamp(e)
        sx=1-strength*(1-e);sy=1+.7*(1-e)
        pic=_xform(text_img(s,size,p['accent'] if j==1 else p['text']),sx,sy,.28*(1-e)*(-1 if j%2 else 1))
        y=348+(j-(len(rows)-1)/2)*gap+(1-e)*32*(-1 if j%2 else 1)
        paste(im,pic,640,y,v*a)
    _note(im,cfg,p,t);return im


def _k07(t,cfg):
    p=palette(cfg);im=base(cfg);s=' '.join(str(cfg.get('text','')).split());words=s.split();a=life(t,.15,.8)
    if not words:return im
    key=int(cfg.get('emphasis_index',len(words)//2))%len(words);strength=clamp(float(cfg.get('keyword_scale',1.32)),1.1,2.2)
    u=smooth(prog(t,_cue(cfg,'emphasis_time',1.65),_cue(cfg,'emphasis_time',1.65)+.55));growth=1+(strength-1)*u
    size=fit_size(s,860,68)
    # Reserve the emphasized width before rendering the word, and recompute neighbors.
    advances=[measure(w,size)*(growth if j==key else 1) for j,w in enumerate(words)];space=measure(' ',size);total=sum(advances)+space*(len(words)-1)
    shrink=min(1,1000/max(1,total));x=640-total*shrink/2
    for j,w in enumerate(words):
        z=growth if j==key else 1;img=text_img(w,size,p['accent'] if j==key else p['text'])
        paste(im,img,x+advances[j]*shrink/2,350,opacity=a,scale=z*shrink)
        x+=(advances[j]+space)*shrink
    _note(im,cfg,p,t);return im


def _k08(t,cfg):
    p=palette(cfg);im=base(cfg);rows=_rows(cfg.get('text',''),2)
    if len(rows)==1: rows=rows+['']
    rows=rows[:2];size=_row_size(rows,960,80);pics=[]
    for j,s in enumerate(rows):
        glyph=text_img(s,size,p['bg'] if j==0 else p['text'])
        if j==0 and s:
            pic=layer(glyph.width+36,glyph.height+24)
            rr(pic,(0,0,pic.width-1,pic.height-1),p['accent'],4)
            paste(pic,glyph,pic.width/2,pic.height/2)
        else: pic=glyph
        pics.append(pic)
    dur=max(.55,float(cfg.get('swap_duration',1.25)))
    start=clamp(_cue(cfg,'swap_time',1.7),.85,3.25);q=prog(t,start,min(4.08,start+dur));a=life(t,.13,.65)
    # Three stages: clear horizontal lanes, swap vertically, return to the center.
    # Measured width controls travel scale; both side lanes remain fully on canvas.
    stage1=smooth(prog(q,0,.30));stage2=smooth(prog(q,.30,.70));stage3=smooth(prog(q,.70,1))
    separation=300;lane_width=520
    for j,pic in enumerate(pics):
        side=-1 if j==0 else 1
        side_scale=min(1,lane_width/max(1,pic.width))
        x=640+side*separation*stage1*(1-stage3)
        scale=1-(1-side_scale)*stage1*(1-stage3)
        y0=303 if j==0 else 416;y1=416 if j==0 else 303
        y=mix(y0,y1,stage2)+(1-enter(t,.13,.65))*24*side
        paste(im,pic,x,y,a,scale=scale)
    _note(im,cfg,p,t);return im


def _k09(t,cfg):
    p=palette(cfg);im=base(cfg);s=' '.join(str(cfg.get('text','')).split());size=fit_size(s,800,86);glyphs,w=_glyphs(s,size);a=life(t,.12,.75)
    maxtrack=clamp(float(cfg.get('tracking_amount',24)),0,55)
    # Letter advances breathe as a group, then settle into the designed word shape.
    beat=math.sin(math.pi*prog(t,1.8,2.65))**2 if 1.8<t<2.65 else 0
    tracking=maxtrack*((1-enter(t,.12,.9))+.58*beat)
    total=w+max(0,len(glyphs)-1)*tracking;shrink=min(1,1030/max(1,total));start=640-total*shrink/2
    for j,(ch,x,adv) in enumerate(glyphs):
        pic=text_img(ch,size,p['accent'] if j%3==1 else p['text'])
        paste(im,pic,start+(x+j*tracking+adv/2)*shrink,352,a,scale=shrink)
    _note(im,cfg,p,t);return im


def _k10(t,cfg):
    p=palette(cfg);im=base(cfg);rows=_rows(cfg.get('text',''),3);size=_row_size(rows,900,74);a=life(t,.1,.7)
    start=_cue(cfg,'reflow_time',1.55);q=smooth(prog(t,start,start+.7));gap=min(93,215/max(1,len(rows)-1));width=clamp(float(cfg.get('edge_width',1000)),400,1060);left=640-width/2;right=640+width/2
    for j,s in enumerate(rows):
        anchor_left=j%2==0;color=p['accent'] if j==1 else p['text'];words=s.split()
        fs=max(12,round(size*mix(.86,1,q)));advances=[measure(w,fs) for w in words]
        natural=sum(advances)+measure(' ',fs)*max(0,len(words)-1)
        span=mix(min(width,natural),width,q)
        x=left if anchor_left else right-(span if len(words)>1 else natural)
        spacing=(span-sum(advances))/max(1,len(words)-1)
        for k,w in enumerate(words):
            pic=text_img(w,fs,color)
            paste(im,pic,x+advances[k]/2,348+(j-(len(rows)-1)/2)*gap,a)
            x+=advances[k]+spacing
    _note(im,cfg,p,t);return im


_DX='https://elements.envato.com/text-animation-DXMD7HL'
PRESETS.update({
'K06':dict(name='Elastic Row Compression',description='Baris dipadatkan, condong seketika dan melantun ke bentuk yang jelas.',genre='creator',genres=['creator','promo','corporate'],text='IDEA\nBERGERAK\nPANTAS',subtitle='Tenaga pada gerakan, jelas pada mesej.',compression=.64,source_url=_DX,observed_timestamp='11.00–13.80 s',mechanism='Anisotropic row compression and slant settling on a baseline',variant_basis='observed'),
'K07':dict(name='Inline Emphasis Reflow',description='Satu kata membesar dan kata bersebelahan bergerak mengikut ruang baharu.',genre='promo',genres=['promo','education','corporate'],text='BINA IDEA HEBAT',subtitle='Pilih kata yang menjadi fokus.',emphasis_index=1,emphasis_scale=1.65,emphasis_time=1.65,source_url=_DX,observed_timestamp='21.00–23.50 s',mechanism='Keyword expansion with measured inline neighbor reflow',variant_basis='adapted'),
'K08':dict(name='Highlighted Row Exchange',description='Dua baris bertukar tempat melalui tiga tahap yang mengelakkan teks bertindih.',genre='saas',genres=['saas','promo','education'],text='MESEJ UTAMA\nIDEA SETERUSNYA',subtitle='Tukar penekanan dalam scene yang sama.',swap_time=1.7,swap_duration=1.25,source_url=_DX,observed_timestamp='25.50–26.00 s',mechanism='Highlighted row exchanges position with a companion row',variant_basis='observed'),
'K09':dict(name='Glyph Spacing Accordion',description='Jarak huruf mengembang, mengecil dan kembali ke susunan bacaan.',genre='corporate',genres=['corporate','creator','promo'],text='BERANI MULA',subtitle='Setiap huruf ada ruang dan ritma.',tracking=24,source_url=_DX,observed_timestamp='27.75–30.75 s',mechanism='Per-glyph spacing accordion adapted from row elasticity',variant_basis='adapted'),
'K10':dict(name='Fixed Edge Justification',description='Lebar baris berubah sambil satu tepi kekal pada paksi susunannya.',genre='education',genres=['education','corporate','promo'],text='MULA SEKARANG\nLANGKAH PERTAMA\nCERITA BAHARU',subtitle='Susunan berubah, panduan mata kekal.',reflow_time=1.55,source_url=_DX,observed_timestamp='38.25–40.00 s',mechanism='Alternating fixed-edge squeeze and justification reflow',variant_basis='adapted'),
})

_FUNCS={'K06':_k06,'K07':_k07,'K08':_k08,'K09':_k09,'K10':_k10}
for _metadata in PRESETS.values(): _metadata['family']='kinetic'
def render(pid,t,cfg):
    if pid not in _FUNCS: raise ValueError('Unknown kinetic A preset '+pid)
    return _FUNCS[pid](float(t),cfg)


def _k01(t,cfg):
    p=palette(cfg);im=base(cfg);s=' '.join(str(cfg.get('text','')).split());size=fit_size(s,1030,97);glyphs,w=_glyphs(s,size);a=1-leave(t)
    step=max(.035,float(cfg.get('stencil_step',.075)));spread=min(.60,max(0,len(glyphs)-1)*step)
    for j,(ch,x,adv) in enumerate(glyphs):
        pic=text_img(ch,size,p['accent'] if j%4==2 else p['text']);q=prog(t,.08+spread*j/max(1,len(glyphs)-1),.65+spread*j/max(1,len(glyphs)-1))
        stencil=layer(pic.width,pic.height)
        # Two-dimensional staircase masks. The final state exactly restores the glyph.
        for row in range(3):
            for col in range(3):
                part=clamp((q*6-(row+col))/.8)
                if part<=0: continue
                x0=round(pic.width*col/3);x1=round(pic.width*(col+1)/3)
                y0=round(pic.height*row/3);y1=round(pic.height*(row+1)/3)
                tile=pic.crop((x0,y0,x1,y1))
                if part<1:tile=crop_reveal(tile,part,'left' if row%2 else 'up')
                stencil.alpha_composite(tile,(x0,y0))
        paste(im,stencil,640-w/2+x+adv/2,349,a)
    _note(im,cfg,p,t);return im


def _k02(t,cfg):
    p=palette(cfg);im=base(cfg);s=' '.join(str(cfg.get('text','')).split());size=fit_size(s,980,105);a=life(t,.12,.7)
    slant=clamp(float(cfg.get('slant',.24)),-.50,.50);u=smooth(prog(t,1.35,2.35))
    pic=_xform(text_img(s,size,p['text']),1,1,-slant*u)
    paste(im,pic,640,350,a)
    _note(im,cfg,p,t);return im


def _k03(t,cfg):
    p=palette(cfg);im=base(cfg);s=' '.join(str(cfg.get('text','')).split());pad=clamp(float(cfg.get('badge_padding',46)),18,90);size=fit_size(s,1020-2*pad,92)
    glyph=text_img(s,size,'#FFFFFF');w=round(glyph.width+2*pad);h=round(glyph.height+pad*1.25)
    badge=Image.new('RGBA',(w,h),p['accent']);mask=Image.new('L',(w,h),255);holes=Image.new('L',(w,h))
    holes.paste(glyph.getchannel('A'),(round((w-glyph.width)/2),round((h-glyph.height)/2)))
    mask=Image.fromarray(np.maximum(0,np.asarray(mask,dtype=np.int16)-np.asarray(holes,dtype=np.int16)).astype('uint8'));badge.putalpha(mask)
    q=enter(t,.1,.88);shown=layer(w,h);cx=w/2;half=w*q/2
    if q>0:box=(round(cx-half),0,round(cx+half),h);shown.alpha_composite(badge.crop(box),box[:2])
    paste(im,shown,640,349,1-leave(t),scale=.92+.08*q)
    _note(im,cfg,p,t);return im


def _k04(t,cfg):
    p=palette(cfg);im=base(cfg);s=' '.join(str(cfg.get('text','')).split());size=fit_size(s,1080,146);a=life(t,.12,.75)
    paste(im,text_img(s,size,p['text']),640,350,a)
    label=str(cfg.get('label_text','IDEA PILIHAN'));small=fit_size(label,710,21,'mono');ww=min(800,measure(label,small,'mono')+58)
    u=enter(t,.6,1.35);y=mix(251,350,u)
    # Independent opaque micro-label deliberately pierces the hero's central band.
    band=layer(round(ww),42);rr(band,(0,0,ww-1,41),p['accent'],0);text(band,label,ww/2,21,small,p['bg'],'mono')
    paste(im,band,640,y,a*clamp(u))
    _note(im,cfg,p,t);return im


def _k05(t,cfg):
    p=palette(cfg);im=base(cfg);rows=_rows(cfg.get('text',''),2)
    if len(rows)<2:rows=rows+['']
    a=life(t,.1,.7);start=_cue(cfg,'exchange_time',2.15);q=smooth(prog(t,start,min(4,start+.62)))
    size=_row_size(rows,1000,98);small=size*.43;left=143
    for j,s in enumerate(rows[:2]):
        factor=q if j else 1-q;fs=round(mix(small,size,factor));pic=text_img(s,fs,p['accent'] if j else p['text'])
        # Left edge remains fixed while hierarchy changes independently on two rows.
        paste(im,pic,left+pic.width/2,289+j*130,a)
    _note(im,cfg,p,t);return im


def _k11(t,cfg):
    p=palette(cfg);im=base(cfg);s=' '.join(str(cfg.get('text','')).split());size=fit_size(s,1020,96);src=text_img(s,size,p['secondary']);a=life(t,.1,.72)
    paste(im,src,640,350,a)
    width=clamp(float(cfg.get('scan_width',180)),45,460);q=prog(t,.55,3.65);cx=mix(-width,src.width+width,q)
    if .55<t<3.65:
        wave=np.exp(-((np.arange(src.width)-cx)/(width*.47))**2)
        alpha=np.asarray(src.getchannel('A'),dtype=float)*wave[None,:]
        lit=Image.new('RGBA',src.size,rgb(p['text'])+(255,));lit.putalpha(Image.fromarray(np.uint8(alpha)))
        _glow(im,lit,640,350,p['accent'],a,11)
    _note(im,cfg,p,t);return im


def _k12(t,cfg):
    p=palette(cfg);im=base(cfg);s=' '.join(str(cfg.get('text','')).split());words=s.split();prefix=words[0] if len(words)>1 else '';tail=' '.join(words[1:]) if len(words)>1 else s
    big=96;small=57;space=28
    full=measure(prefix,small)+space+measure(tail,big,'sans');fit=min(1,1040/max(1,full));big=max(14,round(big*fit));small=max(12,round(small*fit));space*=fit
    prefix_img=text_img(prefix,small,p['accent']);thin=text_img(tail,big,p['text'],'sans');bold=text_img(tail,big,p['text'],'bold')
    # Shared width prevents the thin-to-bold crossfade changing dock position.
    dock_w=max(thin.width,bold.width);full=prefix_img.width+space+dock_w
    fit2=min(1,1060/max(1,full));left=640-full*fit2/2;target=left+(prefix_img.width+space+dock_w/2)*fit2
    u=smooth(prog(t,.1,1.35));arc=clamp(float(cfg.get('dock_arc',100)),25,160);a=life(t,.1,.65)
    scale=fit2*(1.13-.13*u);draw_w=dock_w*scale
    start_x=clamp(640-dock_w*.12,85+draw_w/2,1195-draw_w/2)
    x=mix(start_x,target,u)+math.sin(math.pi*u)*min(90,arc*.55)
    x=clamp(x,80+draw_w/2,1200-draw_w/2)
    y=350-arc*(1-u)-math.sin(math.pi*u)*arc*.23
    weight=smooth(prog(t,.8,1.5));thin_aligned=thin.resize(bold.size,Image.Resampling.BICUBIC);weighted=Image.blend(thin_aligned,bold,weight);paste(im,weighted,x,y,a,scale=scale)
    paste(im,prefix_img,left+prefix_img.width*fit2/2,350,life(t,.85,1.5),scale=fit2)
    _note(im,cfg,p,t);return im


def _k13(t,cfg):
    p=palette(cfg);im=base(cfg);s=' '.join(str(cfg.get('text','')).split());size=fit_size(s,860,105);n=int(clamp(int(cfg.get('depth_layers',6)),2,9));a=life(t,.1,.7)
    area=layer(1120,340);u=enter(t,.08,1.5);ghost=_outline(s,size,p['secondary'],2)
    for j in range(n,0,-1):
        depth=j/n;scale=1+depth*3.2*(1-u);opacity=(1-u)*(.16+.28*(1-depth))
        paste(area,ghost,560,169,opacity*a,scale=scale)
    paste(area,text_img(s,size,p['text']),560,169,a,scale=1+.4*(1-u))
    paste(im,area,640,350)
    _note(im,cfg,p,t);return im


def _k14(t,cfg):
    p=palette(cfg);im=base(cfg);s=' '.join(str(cfg.get('text','')).split());size=fit_size(s,980,94);a=life(t,.1,.7)
    glyph=text_img(s,size,p['text']);paste(im,glyph,640,350,a)
    width=clamp(float(cfg.get('veil_width',400)),100,650);q=prog(t,.65,3.8);cx=mix(-width,1120+width,q);h=214
    xx=np.arange(1120);mask=np.clip(1-np.abs(xx-cx)/(width*.55),0,1);mask=smooth_array(mask)*.92
    veil=Image.new('RGBA',(1120,h),rgb(p['text'])+(255,));veil.putalpha(Image.fromarray(np.tile(np.uint8(mask*255),(h,1))))
    # The veil is localized to the title panel and never flashes the full background.
    local=layer(1120,h);paste(local,text_img(s,size,p['bg']),560,h/2)
    aa=np.asarray(local.getchannel('A'),dtype=float)*mask[None,:];local.putalpha(Image.fromarray(np.uint8(aa)));veil.alpha_composite(local)
    paste(im,veil,640,350,a)
    _note(im,cfg,p,t);return im


def smooth_array(v):return v*v*(3-2*v)


def _k15(t,cfg):
    p=palette(cfg);im=base(cfg);s=' '.join(str(cfg.get('text','')).split());size=fit_size(s,1000,92);glyphs,w=_glyphs(s,size);height=clamp(float(cfg.get('wave_height',62)),10,95)
    for j,(ch,x,adv) in enumerate(glyphs):
        delay=.65*j/max(1,len(glyphs)-1);q=prog(t,.08+delay,.90+delay);a=clamp(q*3)*(1-leave(t))
        dy=height*math.sin(j*.65+(1-q)*math.pi*1.7)*(1-smooth(q))
        paste(im,text_img(ch,size,p['accent'] if j%5==0 else p['text']),640-w/2+x+adv/2,350+dy,a)
    _note(im,cfg,p,t);return im


_YV='https://elements.envato.com/text-animation-YVTH2U2'
_NEON='https://elements.envato.com/text-animation-84TY5RP'
PRESETS.update({
'K01':dict(name='Glyph Stencil Steps',description='Setiap huruf terbuka melalui topeng bertangga pada dua paksi.',genre='corporate',genres=['corporate','creator','promo'],text='BINA CERITA',subtitle='Huruf dibina sedikit demi sedikit.',stencil_step=.075,source_url=_YV,observed_timestamp='32.20–33.30 s',mechanism='Per-glyph stepped two-axis mask reveal',variant_basis='observed'),
'K02':dict(name='Upright to Slant',description='Teks tegak berubah ke condongan melalui shear yang berterusan.',genre='creator',genres=['creator','promo','corporate'],text='IDEA PANTAS',subtitle='Beri arah pada tenaga tipografi.',slant=.24,source_url=_YV,observed_timestamp='27.40–28.20 s',mechanism='Continuous affine shear from upright to slanted typography',variant_basis='observed'),
'K03':dict(name='Negative Badge Reveal',description='Lencana berkembang dengan huruf berlubang yang mendedahkan latar.',genre='promo',genres=['promo','creator','education'],text='IDEA HEBAT',subtitle='Kontras membentuk huruf.',badge_padding=46,source_url=_YV,observed_timestamp='81.80–84.20 s',mechanism='Expanding rectangular badge with negative glyph cutouts',variant_basis='observed'),
'K04':dict(name='Pierced Hero Label',description='Label kecil bergerak berasingan lalu merentasi tajuk utama.',genre='education',genres=['education','promo','corporate'],text='BERANI',subtitle='Dua skala tipografi dalam satu fokus.',label_text='IDEA PILIHAN',source_url=_YV,observed_timestamp='93.20–95.00 s',mechanism='Giant hero title independently occluded by a central micro-label',variant_basis='observed'),
'K05':dict(name='Hierarchy Exchange',description='Dua baris bertukar saiz utama dan sokongan pada jajaran kiri yang sama.',genre='corporate',genres=['corporate','education','creator'],text='IDEA BESAR\nLANGKAH KECIL',subtitle='Ubah hierarki tanpa menukar scene.',exchange_time=2.15,source_url=_YV,observed_timestamp='121.30–121.70 s',mechanism='Two rows exchange large-small hierarchy on one left alignment',variant_basis='observed'),
'K11':dict(name='Luminous Glyph Scanner',description='Cahaya lembut melintas pada bentuk huruf yang lengkap.',genre='saas',genres=['saas','creator','promo'],text='CAHAYA IDEA',subtitle='Cahaya bergerak, bentuk kekal jelas.',scan_width=180,source_url=_NEON,observed_timestamp='0.80–1.80 s; 2.40–3.20 s',mechanism='Continuous soft light sweep through complete glyph masks',variant_basis='observed'),
'K12':dict(name='Curved Word Dock',description='Kata besar mengikut lengkung dan bertukar berat sebelum berlabuh di sisi awalan.',genre='creator',genres=['creator','saas','promo'],text='IDEA BERGERAK',subtitle='Dua kata tiba dengan peranan berbeza.',dock_arc=100,source_url=_NEON,observed_timestamp='5.00–5.80 s',mechanism='Large thin word follows a curved dock with weight crossfade beside a prefix',variant_basis='observed'),
'K13':dict(name='Type Depth Tunnel',description='Lapisan teks pada skala berbeza merapat menjadi satu tajuk.',genre='promo',genres=['promo','creator','saas'],text='TERUS MAJU',subtitle='Kedalaman bergerak ke satu fokus.',depth_layers=6,source_url=_NEON,observed_timestamp='7.20–8.60 s',mechanism='Oversized multi-depth text tunnel contracts to one title',variant_basis='observed'),
'K14':dict(name='Light Veil Inversion',description='Tabir cahaya setempat mengubah polariti teks ketika melintas.',genre='corporate',genres=['corporate','creator','saas'],text='UBAH PANDANGAN',subtitle='Kontras berubah pada kawasan yang terkawal.',veil_width=400,source_url=_NEON,observed_timestamp='9.70–10.20 s; 10.60–11.00 s',mechanism='Localized light veil changes text polarity using a smooth mask',variant_basis='adapted'),
'K15':dict(name='Baseline Wave Settle',description='Gelombang bergerak melalui huruf lalu menetap pada garis dasar.',genre='saas',genres=['saas','education','creator'],text='SEIRING SEIRAMA',subtitle='Gerakan berbeza, satu garis yang jelas.',wave_height=62,source_url=_NEON,observed_timestamp='21.00–21.60 s; 23.00–23.30 s',mechanism='Per-glyph traveling wave settles into a straight baseline',variant_basis='observed'),
})
_FUNCS.update({'K01':_k01,'K02':_k02,'K03':_k03,'K04':_k04,'K05':_k05,'K11':_k11,'K12':_k12,'K13':_k13,'K14':_k14,'K15':_k15})
# Retain the public control names established in the prior implementation.
PRESETS['K06'].update(name='Elastic Row Squeeze',elasticity=.65)
PRESETS['K06'].pop('compression',None)
PRESETS['K07'].update(name='Keyword Push Reflow',keyword_scale=1.32)
PRESETS['K07'].pop('emphasis_scale',None)
PRESETS['K08'].update(name='Highlighted Row Swap',swap_time=2.15)
PRESETS['K09']['tracking_amount']=PRESETS['K09'].pop('tracking')
PRESETS['K10'].update(edge_width=1000)
for _metadata in PRESETS.values(): _metadata['family']='kinetic'
PRESETS=dict(sorted(PRESETS.items()))
