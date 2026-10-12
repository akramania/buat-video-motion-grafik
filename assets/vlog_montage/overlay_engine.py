"""Original black-neutral RGB overlays. Screen blend onto footage; frame() is deterministic.

The normalized recipe is resolution-independent. All motions repeat every duration
seconds, using integer turns or periodic crossfades. Grain and dust are simulated,
not scans from third-party stock. No external images, fonts or footage are required.
"""
from functools import lru_cache
import math
import numpy as np

TAU = 2 * math.pi
PALETTES = {
    "amber": ((1,.47,.08), (1,.83,.32), (.98,.15,.04)),
    "rose": ((1,.16,.36), (1,.63,.46), (.71,.14,.91)),
    "teal": ((.12,.85,.94), (.13,.39,1), (.57,1,.76)),
    "violet": ((.53,.24,1), (1,.22,.74), (.13,.78,1)),
    "silver": ((.85,.93,1), (.49,.65,.82), (1,1,1)),
}

@lru_cache(maxsize=10)
def _grid(w, h):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return (xx + .5) / w, (yy + .5) / h

@lru_cache(maxsize=256)
def _randoms(seed, n=64):
    return np.random.default_rng(seed).random((n, 8)).astype(np.float32)

@lru_cache(maxsize=2)
def _noise(seed, w, h):
    rng = np.random.default_rng(seed)
    return rng.random((3,h,w), dtype=np.float32)

def _blob(x, y, cx, cy, sx, sy):
    return np.exp(-.5 * (((x-cx)/sx)**2 + ((y-cy)/sy)**2))

def frame(recipe, t, w, h):
    """Return (h,w,3) uint8 RGB pixels; t in seconds and w/h positive integers.

    recipe keys: family, variant (1..5), seed, palette, duration. Black is neutral
    for screen blending. Use overlay opacity around 0.15..0.65 on your footage.
    """
    if not (isinstance(w,int) and isinstance(h,int) and 1 <= w <= 8192 and 1 <= h <= 8192):
        raise ValueError("Width and height must be integers in 1..8192")
    duration = float(recipe.get("duration",2))
    if not math.isfinite(duration) or duration <= 0 or not math.isfinite(float(t)):
        raise ValueError("Duration must be positive and t must be finite")
    v = int(recipe.get("variant",1))
    if not 1 <= v <= 5: raise ValueError("variant must be 1..5")
    seed = int(recipe.get("seed",2031))
    p = TAU * (float(t) % duration) / duration
    x,y = _grid(w,h)
    z = np.zeros((h,w,3),dtype=np.float32)
    palette = np.array(PALETTES.get(recipe.get("palette","amber"),PALETTES["amber"]),dtype=np.float32)
    pts = _randoms(seed)
    family = recipe["family"]
    def add(mask, color=0, gain=1):
        nonlocal z
        z += mask[...,None] * palette[color % 3] * gain

    if family in ("warm_leak","cool_leak"):
        # Five placements: side spill, top arc, corner bloom, opposing pair, low haze.
        centers = [(.02,.48),(.52,-.05),(.02,.02),(.94,.35),(.5,1.07)]
        cx,cy=centers[v-1]
        for k in range(3):
            dx=.09*math.sin(p+k*1.6); dy=.1*math.cos(p+k*.7)
            add(_blob(x,y,cx+dx,cy+dy,.13+.035*k,.27-.04*k),k,.43+.12*math.sin(p+k))
        if v==4:
            add(_blob(x,y,.05+.06*math.cos(p),.8,.16,.19),1,.45)
    elif family=="prism_sweep":
        angle=[-.4,.5,1.25,-1.1,.1][v-1]
        u=(x-.5)*math.cos(angle)+(y-.5)*math.sin(angle)
        center=.37*math.sin(p)
        for k in range(3):
            add(np.exp(-((u-center+(k-1)*.09)/(.018+.006*v))**2),k,.45)
        add(_blob(x,y,.5+.3*math.sin(p),.45+.12*math.cos(p),.17,.23),1,.12)
    elif family=="anamorphic_flare":
        cy=[.3,.48,.66,.22,.79][v-1]+.035*math.sin(p)
        cx=.5+.28*math.cos(p)
        line=np.exp(-((y-cy)/(.006+.002*v))**2)*np.exp(-((x-cx)/.55)**2)
        add(line,0,.6)
        add(_blob(x,y,cx,cy,.04,.11),2,.7)
        for k in range(2+v):
            add(_blob(x,y,(cx+.15*k+.25)%1,cy,.025+.007*k,.025),k,.18)
    elif family=="lens_ring":
        cx=.5+.2*math.sin(p);cy=.5+.15*math.cos(p)
        radius=np.sqrt(((x-cx)*w/h)**2+(y-cy)**2)
        for k in range(2+(v%3)):
            r=.17+k*.13+.03*math.sin(p+k)
            add(np.exp(-((radius-r)/(.007+.002*v))**2),k,.25)
        add(_blob(x,y,cx,cy,.035,.05),2,.55)
    elif family=="bokeh_drift":
        for k,a in enumerate(pts[:8+v*2]):
            cx=a[0]+.13*math.sin(p+a[2]*TAU); cy=a[1]+.1*math.cos(p+a[3]*TAU)
            r=.022+.04*a[4]
            d=np.sqrt(((x-cx)*w/h)**2+(y-cy)**2)
            disk=1/(1+np.exp(np.clip((d-r)*90,-40,40)))
            ring=np.exp(-((d-r)/.004)**2)
            add(disk*.14+ring*.08,k,.55+.35*math.sin(p+a[5]*TAU)**2)
    elif family=="dust_gate":
        for k,a in enumerate(pts[:15+v*4]):
            cx=a[0]+.025*math.sin(p+a[2]*TAU);cy=a[1]+.04*math.cos(p+a[3]*TAU)
            pulse=math.sin(p*(1+k%2)+a[4]*TAU)**6
            add(_blob(x,y,cx,cy,.0012+.0015*a[5],.002+.002*a[6]),2,.35*pulse)
        if v in (2,4,5):
            sx=.13+.16*v+.02*math.sin(p)
            add(np.exp(-((x-sx)/.0008)**2)*(.1+.12*math.sin(p)**2),2,.4)
    elif family=="film_grain":
        n=_noise(seed,w,h)
        # Periodic morph between fixed grain fields avoids non-looping randomness.
        grain=(n[0]*(1+math.cos(p*(19+2*v)))/2+n[1]*(1-math.cos(p*(19+2*v)))/2)
        grain=grain*(.035+.012*v)
        if v==3: grain*=.5+.5*np.sin(x*w*.28)**2
        if v==4: grain+=(n[2]>.988).astype(np.float32)*.08*math.sin(p)**2
        if v==5: grain*=.6+.4*np.cos(y*8+p)**2
        add(grain,2,1)
    elif family=="projector_flicker":
        gate=np.exp(-((x-.5)/.67)**4-((y-.5)/.62)**4)
        flick=.015+.017*v*(.5+.5*math.sin(p*(3+v)))
        add(gate*flick,1,1)
        for k,a in enumerate(pts[:6+v]):
            cx=a[0]+.006*math.sin(p*2+a[2]*TAU)
            scratch=np.exp(-((x-cx)/.0009)**2)
            add(scratch*.1*(.5+.5*math.sin(p+a[4]*TAU)),2,1)
        add(np.exp(-((y-(.5+.45*math.sin(p)))/.02)**2),2,.035)
    elif family=="scanline_roll":
        spacing=[.014,.023,.038,.058,.085][v-1]
        line=(.5+.5*np.cos(TAU*y/spacing-p*(1+v%2)))**14
        band=np.exp(-((y-(.5+.6*math.sin(p+.4)))/(.065+.008*v))**2)
        add(line,0,.055+.009*v)
        add(band,1,.13)
    elif family=="chromatic_glitch":
        for k,a in enumerate(pts[:4+v]):
            cy=a[0]; thick=.008+.034*a[1]
            mask=np.exp(-((y-cy)/thick)**8)
            bars=(np.sin((x*12+a[2])*TAU+p*(2+k%2))>.55).astype(np.float32)
            blink=math.sin(p*(2+k%3)+a[3]*TAU)**12
            add(mask*bars*blink,k,.5)
        add((np.sin(y*h*.8+p)> .96).astype(np.float32),2,.015)
    elif family=="rain_window":
        # Long beads travel through the frame at integer full turns per loop.
        for k,a in enumerate(pts[:10+v*2]):
            cy=(a[1]+float(t)/duration*(1+k%2))%1
            cx=a[0]+.025*math.sin(p+a[2]*TAU)
            add(_blob(x,y,cx,cy,.0018+.001*a[3],.025+.035*a[4]),0,.17)
            add(_blob(x,y,cx,cy+.025,.0035,.007),2,.21)
    elif family=="snowfall":
        for k,a in enumerate(pts[:15+v*4]):
            cy=(a[1]+float(t)/duration)%1
            cx=a[0]+.03*math.sin(p+a[2]*TAU)
            r=.0014+.004*a[4]
            add(_blob(x,y,cx,cy,r*h/w,r),2,.12+.35*a[5])
    elif family=="sparkle_trail":
        for k,a in enumerate(pts[:8+v]):
            cx=.5+.4*math.sin(p+a[0]*TAU);cy=.5+.32*math.cos(p+a[1]*TAU)
            twinkle=(.5+.5*math.sin(p*2+a[2]*TAU))**5
            star=_blob(x,y,cx,cy,.002,.024)+_blob(x,y,cx,cy,.023,.002)
            add(star,k,.43*twinkle)
            add(_blob(x,y,cx,cy,.01,.017),1,.15*twinkle)
    elif family=="ember_rise":
        for k,a in enumerate(pts[:13+v*3]):
            cy=(a[1]-float(t)/duration)%1
            cx=a[0]+.03*math.sin(p+a[2]*TAU)
            add(_blob(x,y,cx,cy,.002+.002*a[3],.007+.006*a[4]),k,.2+.2*a[5])
            add(_blob(x,y,cx,cy+.012,.0015,.017),0,.12)
    elif family=="neon_ribbons":
        for k in range(2+v%3):
            cy=.5+.22*np.sin(x*TAU*(1+v%2)+p+k*1.5)
            ribbon=np.exp(-((y-cy)/(.002+.0007*v))**2)
            glow=np.exp(-((y-cy)/.028)**2)
            add(ribbon*.55+glow*.1,k,1)
    elif family=="edge_glow":
        edge=np.minimum(np.minimum(x,1-x),np.minimum(y,1-y))
        ring=np.exp(-edge/(.015+.012*v))
        mod=.25+.25*np.sin(x*TAU+y*TAU+p)**2
        add(ring*mod,0,1)
        add(ring*(.08+.15*(.5+.5*math.cos(p))),1,1)
    elif family=="crt_grid":
        dot=(.5+.5*np.cos(x*w*TAU/(4+v)))**8 * (.5+.5*np.cos(y*h*TAU/(4+v)))**8
        mod=.5+.5*np.cos(y*TAU*2+p)
        add(dot*mod,0,.13+.035*v)
        add(np.exp(-((y-.5-.42*math.sin(p))/.025)**2),1,.08)
    elif family=="film_burn":
        wave=.11*np.sin(y*9+p)+.06*np.sin(y*21-p*2)
        edge=[.03,.94,.04,.92,.5][v-1]+.07*math.sin(p)
        dist=np.abs(x-edge-wave)
        burn=np.exp(-(dist/(.025+.005*v))**2)
        haze=np.exp(-(dist/.12)**2)
        add(burn,1,.8)
        add(haze,0,.25)
        add(np.exp(-((dist-.03)/.012)**2),2,.2)
    elif family=="speed_streaks":
        angle=[0,.15,-.18,.42,-.4][v-1]
        u=x*math.cos(angle)+y*math.sin(angle)
        q=-x*math.sin(angle)+y*math.cos(angle)
        for k,a in enumerate(pts[:8+v*2]):
            cx=(a[0]+float(t)/duration*(1+k%2))%1
            cy=a[1]
            add(np.exp(-((u-cx)/(.04+.06*a[2]))**2-((q-cy)/(.001+.002*a[3]))**2),k,.24+.25*a[4])
    else:
        raise ValueError(f"Unknown overlay family: {family}")
    return np.clip(z*255,0,255).astype(np.uint8)

