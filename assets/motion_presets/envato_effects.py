from envato_common import *

@lru_cache(maxsize=20)
def media(path,index):
    if not path:return demo_media(index)
    with Image.open(path) as src:
        pic=ImageOps.contain(src.convert('RGBA'),(W,H),Image.Resampling.LANCZOS)
    im=Image.new('RGBA',(W,H),'#0D1828');paste(im,pic,640,360);return im

def effects(t,cfg):
    p=palette(cfg);mode=cfg['mode'];paths=cfg.get('image_paths',[])
    a=media(paths[0] if paths else '',0);b=media(paths[1] if len(paths)>1 else '',1)
    u=smooth(prog(t,1.85,3.2));im=layer()
    if mode.startswith('camera'):
        v=min(1,u*2) if u<.5 else min(1,(1-u)*2);src=a if u<.5 else b
        if mode=='camera_whip':
            x=1280*u;paste(im,a,640-x,360);paste(im,b,1920-x,360)
            if .03<u<.97:
                blur=layer();paste(blur,im,640+v*15,360,opacity=.25);paste(blur,im,640-v*15,360,opacity=.25);im=Image.alpha_composite(im,blur)
        elif mode=='camera_roll':paste(im,src,640,360,scale=1+.8*v,angle=(u if u<.5 else u-1)*180)
        elif mode=='camera_stretch':
            stretched=src.resize((round(W*(1+v*1.8)),round(H*(1+.4*v))),Image.Resampling.BICUBIC);paste(im,stretched,640,360)
        else:
            paste(im,src,640,360,scale=1+v*1.3)
            if v>.1:
                blur=im.filter(ImageFilter.GaussianBlur(v*7));im=Image.blend(im,blur,.65)
    else:
        mask=Image.new('L',(W,H));d=ImageDraw.Draw(mask);rng=random.Random(715);jag=[rng.randrange(-15,16) for _ in range(66)]
        if mode=='rip_horizontal':
            edge=[(i*20,H*u+jag[i]) for i in range(65)];d.polygon([(0,0),(W,0)]+list(reversed(edge)),fill=255)
            im=Image.composite(b,a,mask);line(im,edge,'#EFEADB',13);line(im,[(x,y+6) for x,y in edge],'#CCC3B7',3)
        elif mode=='rip_diagonal':
            xx=-H+(W+H)*u;edge=[(xx+y+jag[i],y) for i,y in enumerate(range(0,H+1,20))]
            d.polygon([(0,0),(xx,0)]+edge+[(0,H)],fill=255);im=Image.composite(b,a,mask);line(im,edge,'#ECE5D8',13)
        elif mode=='rip_shards':
            for i in range(8):
                vv=ease(prog(t,1.8+i*.11,2.75+i*.11));x=i*160
                pts=[(x,0),(x+160,0)]+[(x+160-j*20,H*vv+jag[(i*7+j)%66]) for j in range(9)]
                d.polygon(pts,fill=255)
            im=Image.composite(b,a,mask)
            if 0<u<1:
                rim=mask.filter(ImageFilter.MaxFilter(13));rim=ImageChops.subtract(rim,mask);paper=Image.new('RGBA',(W,H),'#EDE7DC');paper.putalpha(rim);im=Image.alpha_composite(im,paper)
        else:
            im=Image.blend(a,b,u);v=pop(prog(t,1.1,2.3))*(1-prog(t,3.2,4.3))
            cut=layer(270,370);d=ImageDraw.Draw(cut)
            d.ellipse((75,10,195,130),fill=p['accent']);d.rounded_rectangle((35,115,235,345),radius=45,fill=p['accent'])
            outline=cut.getchannel('A').filter(ImageFilter.MaxFilter(17));white=Image.new('RGBA',cut.size,'#F6F0DD');white.putalpha(outline);white.alpha_composite(cut)
            paste(im,white,640,390,scale=max(.001,v*(1+.35*u)),angle=-8+16*u)
    if cfg.get('show_titles',True):
        title_palette=dict(p);title_palette.update(text='#FFFFFF',muted='#C5D3E3');heading(im,cfg,title_palette)
    return im
