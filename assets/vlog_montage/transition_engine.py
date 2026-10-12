"""Original spatial-reveal transition engine (NumPy only).

Usage:
    recipe = json.load(open('transitions/VL0101.json'))
    matte = mask_frame(recipe, t=0.5, width=1920, height=1080)
    result = A * (1-matte[..., None]) + B * matte[..., None]

``t`` is NORMALIZED transition time, clamped to [0,1]. White reveals B.
Returns an H×W float32 array in [0,1]. Endpoints are exactly zero and one.
The source JSON is resolution independent; MP4 mattes are 640×360 previews.
Use the analytic engine, rather than upscaling a lossy matte, for final output.
All mechanisms are progressive spatial reveals, not camera/motion-blur effects.
No third-party footage or effects are bundled. Commercial reuse is permitted.
"""

from functools import lru_cache
import json
import math
import numpy as np


def _normalize(a):
    lo, hi = float(a.min()), float(a.max())
    return (a-lo) / max(hi-lo, 1e-8)


def _triangle(a):
    return 1-abs((a % 1)*2-1)


@lru_cache(maxsize=256)
def _threshold(family, params_json, width, height):
    p = json.loads(params_json)
    y, x = np.mgrid[0:height, 0:width].astype(np.float32)
    x, y = (x+.5)/width, (y+.5)/height
    cx, cy = p.get('cx', .5), p.get('cy', .5)
    a = math.radians(p.get('angle', 0))
    u = (x-cx)*math.cos(a)+(y-cy)*math.sin(a)
    v = -(x-cx)*math.sin(a)+(y-cy)*math.cos(a)
    radial = np.sqrt((u*p.get('aspect', 1))**2+v*v)
    theta = np.arctan2(v, u)
    seed = p.get('seed', 0)

    if family == 'linear':
        f = u
    elif family == 'angular':
        f = u + p['bend']*abs(v) + .07*np.sin(v*p['frequency'])
    elif family == 'iris':
        f = radial
    elif family == 'diamond':
        f = abs(u)*p['aspect']+abs(v)
    elif family == 'clock':
        f = ((theta/(2*math.pi) + p['start']) * p['direction']) % 1
    elif family == 'spiral':
        f = (theta/(2*math.pi) + radial*p['twists'] + p['start']) % 1
    elif family == 'venetian':
        z = u*p['bands']
        f = (z % 1)*.72 + _normalize(v)*p['stagger']
    elif family == 'shutter':
        z = u*p['bands']
        f = abs((z % 1)-.5)*1.5 + _normalize(v)*p['stagger']
    elif family == 'mosaic':
        cols, rows = p['cols'], p['rows']
        gx, gy = np.floor(x*cols), np.floor(y*rows)
        rank = ((gx*37+gy*19+seed*11) % (cols*rows))/(cols*rows)
        local = np.maximum(abs((x*cols)%1-.5), abs((y*rows)%1-.5))*2
        f = rank*.82+local*.18
    elif family == 'checker':
        cols, rows = p['cols'], p['rows']
        gx, gy = np.floor(x*cols), np.floor(y*rows)
        parity = (gx+gy+seed) % 2
        local = np.sqrt(((x*cols)%1-.5)**2+((y*rows)%1-.5)**2)
        f = parity*.48+local*.55+gy/rows*.14
    elif family == 'waves':
        f = u+p['amplitude']*np.sin(v*p['frequency']+p['phase'])
    elif family == 'ripple':
        f = radial+p['amplitude']*np.sin(radial*p['frequency']+p['phase'])
    elif family == 'hex':
        # Axial hexagonal coordinates and cube rounding yield real hex cells.
        size = p['size']
        hx, hy = (x-.5)*(width/height), y-.5
        q = (math.sqrt(3)/3*hx-hy/3)/size
        r = (2*hy/3)/size
        s = -q-r
        rq, rr, rs = np.round(q), np.round(r), np.round(s)
        dq, dr, ds = abs(rq-q), abs(rr-r), abs(rs-s)
        qm, rm = (dq>dr)&(dq>ds), (~((dq>dr)&(dq>ds)))&(dr>ds)
        rq = np.where(qm,-rr-rs,rq)
        rr = np.where(rm,-rq-rs,rr)
        hc_x = size*math.sqrt(3)*(rq+rr/2)
        hc_y = size*1.5*rr
        local = np.sqrt((hx-hc_x)**2+(hy-hc_y)**2)/size
        ranks = (np.sin(rq*12.9898+rr*78.233+seed)*43758.5453)%1
        f = ranks*.82+local*.18
    elif family == 'chevron':
        f = u+p['slope']*abs(v)+p['depth']*np.maximum(abs(v)-.2,0)
    elif family == 'zigzag':
        f = u+p['amplitude']*_triangle(v*p['teeth']+p['phase'])
    elif family == 'film_gate':
        edge = (abs(u)>.39).astype(np.float32)
        f = abs(v)*p['opening'] + edge*p['rail_delay'] + edge*.09*np.cos(v*p['perforations'])
    elif family == 'cloud':
        f = u + p['amplitude']*(np.sin(v*9+seed)+.45*np.sin(v*21-u*5)+.2*np.sin(v*41+u*13))
    elif family == 'ink':
        noise = np.sin(u*17+v*11+seed)*np.cos(v*23-u*7)+.4*np.sin(u*39+v*33)
        f = radial+noise*p['roughness'] + p['drip']*v
    elif family == 'petal':
        f = radial/(1+p['depth']*np.cos(theta*p['petals']+p['phase']))
    elif family == 'split':
        f = np.maximum(abs(u)*p['aspect'], abs(v))+p['skew']*u*v
    else:
        raise ValueError('Unknown transition family: '+str(family))
    if p.get('reverse', False):
        f = -f
    return _normalize(f).astype(np.float32)


def mask_frame(recipe, t, width, height):
    """Return a monotone, feathered reveal matte for normalized time ``t``."""
    width, height = int(width), int(height)
    if width < 1 or height < 1 or width > 8192 or height > 8192:
        raise ValueError('Dimensions must be 1..8192')
    t = float(t)
    if not math.isfinite(t):
        raise ValueError('Normalized time must be finite')
    if t <= 0:
        return np.zeros((height, width), dtype=np.float32)
    if t >= 1:
        return np.ones((height, width), dtype=np.float32)
    f = _threshold(recipe['family'], json.dumps(recipe['parameters'],sort_keys=True),width,height)
    t = t*t*(3-2*t)
    edge = float(recipe.get('feather', .045))
    if not 0 < edge <= .3:
        raise ValueError('Feather must be in (0,.3]')
    z = np.clip((t*(1+2*edge)-edge-f)/edge+.5,0,1)
    return (z*z*(3-2*z)).astype(np.float32)
