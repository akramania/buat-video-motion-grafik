#!/usr/bin/env python3
"""Reusable procedural 2.5D planet engine for the Solar System video.

The module is deliberately independent of the scene renderer.  It returns PIL
RGBA sprites which can be placed by either the existing Pillow renderer or a
Cairo scene compositor.

High-value differences from the earlier renderer:

* Equirectangular textures are mapped to a sphere with bilinear sampling.
* Every planet has its own artistic spin period, direction and axial tilt.
* Rotation is interpolated between cached phase images, avoiding phase jumps.
* The cache is lazy and bounded.  At 512 px and 192 entries it remains below
  roughly 210 MiB rather than retaining every frame for every planet.
* Earth's cloud layer rotates independently from the surface.
* Saturn/Uranus rings are split into rear/front layers and cast a soft shadow
  over the planet.  Ring brightness also follows the light direction.

Typical use::

    engine = Planet25DEngine(size=512, phases=72, max_cache_frames=192)
    sprite = engine.render_planet("saturn", t_seconds, diameter=620,
                                  light_angle=-2.45)
    frame.alpha_composite(sprite, (cx-sprite.width//2, cy-sprite.height//2))
"""

from __future__ import annotations

import argparse
import math
from collections import OrderedDict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter


TAU = math.tau


@dataclass(frozen=True)
class PlanetStyle:
    tilt_deg: float
    spin_direction: int
    spin_period: float
    glow_rgb: tuple[int, int, int]
    specular: float


PLANET_STYLES = {
    "sun": PlanetStyle(7.25, 1, 34.0, (255, 154, 38), 0.00),
    "mercury": PlanetStyle(0.03, 1, 25.0, (188, 200, 225), 0.10),
    "venus": PlanetStyle(177.4, -1, 38.0, (255, 172, 67), 0.12),
    "earth": PlanetStyle(23.4, 1, 24.0, (55, 207, 240), 0.42),
    "moon": PlanetStyle(6.7, 1, 31.0, (200, 210, 224), 0.08),
    "mars": PlanetStyle(25.2, 1, 25.5, (255, 101, 57), 0.10),
    "jupiter": PlanetStyle(3.1, 1, 16.0, (244, 188, 126), 0.20),
    "saturn": PlanetStyle(26.7, 1, 18.5, (255, 221, 145), 0.18),
    "uranus": PlanetStyle(97.8, -1, 27.0, (105, 236, 236), 0.32),
    "neptune": PlanetStyle(28.3, 1, 17.5, (76, 120, 255), 0.35),
}


def _clamp01(a: np.ndarray) -> np.ndarray:
    return np.clip(a, 0.0, 1.0)


def make_equirectangular_texture(kind: str, height: int = 256, width: int = 512) -> np.ndarray:
    """Return deterministic float32 RGB albedo in equirectangular form."""
    y = np.linspace(-1.0, 1.0, height, dtype=np.float32)[:, None]
    x = np.linspace(0.0, TAU, width, endpoint=False, dtype=np.float32)[None, :]
    tex = np.zeros((height, width, 3), dtype=np.float32)

    if kind == "sun":
        a = np.sin(x * 8 + np.sin(y * 10) * 1.6) * np.cos(y * 9 + np.cos(x * 6))
        b = 0.5 * np.sin(x * 18 - y * 14) + 0.5 * np.cos(x * 25 + y * 20)
        g = _clamp01(0.56 + 0.29 * a + 0.20 * b)
        tex[..., 0] = 1.0
        tex[..., 1] = 0.40 + 0.55 * g
        tex[..., 2] = 0.04 + 0.43 * g**2.1

    elif kind in ("mercury", "moon"):
        seed = 101 if kind == "mercury" else 211
        base = 0.54 + 0.10 * np.sin(x * 4) * np.cos(y * 5) + 0.07 * np.sin(x * 13 + y * 11)
        rng = np.random.default_rng(seed)
        for _ in range(44 if kind == "mercury" else 36):
            cx, cy = rng.uniform(0.15, TAU - 0.15), rng.uniform(-0.82, 0.82)
            radius = rng.uniform(0.035, 0.18)
            # Longitude wraps at both edges of the texture.
            dx = np.minimum(np.abs(x - cx), TAU - np.abs(x - cx)) * np.cos(cy * 0.75)
            dist = np.sqrt(dx * dx + (y - cy) ** 2)
            rim = np.exp(-((dist - radius) / max(radius * 0.20, 0.008)) ** 2) * 0.18
            bowl = np.where(dist < radius * 0.84, -0.14 * (1 - (dist / (radius * 0.84)) ** 2), 0)
            base += rim + bowl
        base = np.clip(base, 0.20, 0.94)
        tint = np.array([0.97, 0.95, 1.01] if kind == "mercury" else [0.92, 0.95, 1.00], np.float32)
        tex[:] = base[..., None] * tint

    elif kind == "venus":
        swirl = y * 7.6 + 0.36 * np.sin(x * 2 + y * 4) + 0.19 * np.cos(x * 5 - y * 6)
        bands = _clamp01(0.50 + 0.34 * np.sin(swirl) + 0.16 * np.cos(swirl * 2.3 + x))
        tex[..., 0] = 0.87 + 0.12 * bands
        tex[..., 1] = 0.56 + 0.30 * bands
        tex[..., 2] = 0.16 + 0.25 * bands**1.5

    elif kind == "earth":
        tex[..., 0] = 0.035
        tex[..., 1] = 0.30 + 0.15 * (1 - np.abs(y))
        tex[..., 2] = 0.74 + 0.20 * (1 - np.abs(y))
        cont = (
            np.sin(x * 1.5 + 0.8) * np.cos(y * 2.6)
            + 0.55 * np.sin(x * 3.0 - y * 2.2 + 1.4)
            + 0.35 * np.cos(x * 5 + y * 4.5)
            + 0.22 * np.sin(x * 9 - y * 7)
        )
        land, high = cont > 0.22, cont > 0.64
        tex[..., 0] = np.where(land, np.where(high, 0.59, 0.14), tex[..., 0])
        tex[..., 1] = np.where(land, np.where(high, 0.52, 0.62), tex[..., 1])
        tex[..., 2] = np.where(land, np.where(high, 0.28, 0.20), tex[..., 2])
        polar = np.abs(y) > 0.81 + 0.035 * np.sin(x * 4)
        tex[polar] = (0.94, 0.98, 1.00)

    elif kind == "mars":
        terrain = 0.55 + 0.22 * np.sin(x * 2 + y * 3) + 0.14 * np.cos(x * 5 - y * 4) + 0.08 * np.sin(x * 11 + y * 9)
        dark = np.exp(-((y + 0.15) ** 2) / 0.06) * (0.5 + 0.5 * np.sin(x * 2)) * 0.28
        olympus = np.exp(-(((x - 2.6) / 0.19) ** 2 + ((y + 0.22) / 0.16) ** 2)) * 0.28
        v = np.clip(terrain - dark + olympus, 0.18, 0.98)
        tex[..., 0] = np.clip(0.53 + 0.45 * v, 0, 1)
        tex[..., 1] = np.clip(0.18 + 0.34 * v**1.3, 0, 1)
        tex[..., 2] = np.clip(0.07 + 0.21 * v**1.8, 0, 1)
        polar = np.abs(y) > 0.88 + 0.025 * np.cos(x * 3)
        tex[polar] = (0.95, 0.92, 0.89)

    elif kind in ("jupiter", "saturn"):
        freq = 19.0 if kind == "jupiter" else 16.0
        wave = y + (0.025 if kind == "jupiter" else 0.012) * np.sin(x * 6)
        zones = _clamp01(0.52 + 0.31 * np.sin(wave * freq) + 0.16 * np.cos(wave * freq * 1.94 + 0.6))
        if kind == "jupiter":
            tex[..., 0] = 0.70 + 0.28 * zones
            tex[..., 1] = 0.43 + 0.40 * zones
            tex[..., 2] = 0.22 + 0.39 * zones**1.5
            dx, dy = (x - math.pi) / 0.53, (y - 0.28) / 0.22
            r = np.sqrt(dx * dx + dy * dy)
            spot = np.clip(1 - r**2.4, 0, 1)
            swirl = 0.84 + 0.16 * np.sin(r * 12)
            target = np.stack((0.94 * swirl, 0.27 * swirl, 0.16 * swirl), axis=-1)
            tex = tex * (1 - spot[..., None]) + target * spot[..., None]
        else:
            tex[..., 0] = 0.81 + 0.17 * zones
            tex[..., 1] = 0.68 + 0.22 * zones
            tex[..., 2] = 0.39 + 0.24 * zones

    elif kind == "uranus":
        bands = _clamp01(0.55 + 0.16 * np.cos(y * 9) + 0.055 * np.sin(x * 3 + y * 5))
        tex[..., 0] = 0.27 + 0.25 * bands
        tex[..., 1] = 0.78 + 0.17 * bands
        tex[..., 2] = 0.84 + 0.14 * bands

    elif kind == "neptune":
        wave = y + 0.021 * np.sin(x * 5)
        bands = _clamp01(0.50 + 0.26 * np.sin(wave * 12) + 0.12 * np.cos(wave * 24))
        tex[..., 0] = 0.08 + 0.17 * bands
        tex[..., 1] = 0.27 + 0.30 * bands
        tex[..., 2] = 0.76 + 0.22 * bands
        storm = np.exp(-(((x - 2.8) / 0.45) ** 2 + ((y - 0.20) / 0.20) ** 2)) * 0.36
        tex -= storm[..., None] * np.array([0.35, 0.45, 0.24], np.float32)
        for sx, sy, sw in ((1.8, -0.35, 0.60), (3.4, 0.05, 0.70), (4.5, 0.42, 0.50)):
            streak = np.exp(-(((x - sx) / sw) ** 2 + ((y - sy) / 0.045) ** 2)) * 0.72
            tex += streak[..., None]
    else:
        raise KeyError(f"Unknown planet kind: {kind}")

    return _clamp01(tex).astype(np.float32)


def make_earth_cloud_texture(height: int = 256, width: int = 512) -> np.ndarray:
    y = np.linspace(-1.0, 1.0, height, dtype=np.float32)[:, None]
    x = np.linspace(0.0, TAU, width, endpoint=False, dtype=np.float32)[None, :]
    a = np.sin(x * 4 + np.cos(y * 6) * 1.8) * np.sin(y * 7 + x * 2)
    b = np.cos(x * 9 - y * 11) * 0.30
    return np.clip((a + b - 0.20) * 1.20, 0.0, 0.78).astype(np.float32)


class Planet25DEngine:
    """Lazy, memory-bounded planet sprite generator."""

    def __init__(self, size: int = 512, phases: int = 72, max_cache_frames: int = 192, light_bins: int = 48):
        self.size = int(size)
        self.phases = int(phases)
        self.max_cache_frames = int(max_cache_frames)
        self.light_bins = int(light_bins)
        self._textures: dict[str, np.ndarray] = {}
        self._geometry: dict[str, tuple[np.ndarray, ...]] = {}
        self._body_cache: OrderedDict[tuple, Image.Image] = OrderedDict()
        self._cloud_cache: OrderedDict[int, Image.Image] = OrderedDict()
        self._prepare_common_geometry()

    @property
    def approximate_cache_mib(self) -> float:
        return self.max_cache_frames * self.size * self.size * 4 / (1024**2)

    def _prepare_common_geometry(self) -> None:
        lin = np.linspace(-1.0, 1.0, self.size, dtype=np.float32)
        gy, gx = np.meshgrid(lin, lin, indexing="ij")
        r2 = gx * gx + gy * gy
        inside = r2 <= 1.0
        gz = np.sqrt(np.maximum(0.0, 1.0 - r2))
        feather = 2.3 / (self.size * 0.5)
        alpha = np.clip((1.0 - np.sqrt(r2)) / feather, 0, 1) * inside
        self.gx, self.gy, self.gz = gx, gy, gz
        self.inside, self.alpha = inside, alpha.astype(np.float32)
        self.fresnel = ((1.0 - gz) ** 2.55 * inside).astype(np.float32)

    def _get_geometry(self, kind: str) -> tuple[np.ndarray, np.ndarray]:
        cached = self._geometry.get(kind)
        if cached is not None:
            return cached
        tilt = math.radians(PLANET_STYLES[kind].tilt_deg)
        # Rotate the sphere coordinate system about the viewing axis.  This
        # visibly tilts the latitude bands while preserving the circular limb.
        tx = self.gx * math.cos(tilt) - self.gy * math.sin(tilt)
        ty = self.gx * math.sin(tilt) + self.gy * math.cos(tilt)
        lat = np.arcsin(np.clip(ty, -1, 1))
        lon = np.arctan2(tx, self.gz)
        self._geometry[kind] = (lat.astype(np.float32), lon.astype(np.float32))
        return self._geometry[kind]

    def _get_texture(self, kind: str) -> np.ndarray:
        if kind not in self._textures:
            self._textures[kind] = make_equirectangular_texture(kind)
        return self._textures[kind]

    @staticmethod
    def _bilinear(texture: np.ndarray, u: np.ndarray, v: np.ndarray) -> np.ndarray:
        h, w = texture.shape[:2]
        x0 = np.floor(u).astype(np.int32) % w
        y0 = np.clip(np.floor(v).astype(np.int32), 0, h - 1)
        x1, y1 = (x0 + 1) % w, np.minimum(y0 + 1, h - 1)
        fx, fy = (u - np.floor(u))[..., None], (v - np.floor(v))[..., None]
        a = texture[y0, x0] * (1 - fx) + texture[y0, x1] * fx
        b = texture[y1, x0] * (1 - fx) + texture[y1, x1] * fx
        return a * (1 - fy) + b * fy

    def _remember(self, cache: OrderedDict, key, value: Image.Image, limit: int) -> Image.Image:
        cache[key] = value
        cache.move_to_end(key)
        while len(cache) > limit:
            cache.popitem(last=False)
        return value

    def _body_frame(self, kind: str, phase_index: int, light_bin: int) -> Image.Image:
        key = (kind, phase_index % self.phases, light_bin % self.light_bins)
        hit = self._body_cache.get(key)
        if hit is not None:
            self._body_cache.move_to_end(key)
            return hit

        texture = self._get_texture(kind)
        th, tw = texture.shape[:2]
        lat, lon = self._get_geometry(kind)
        u = (lon / TAU + 0.5) * tw + (phase_index % self.phases) * tw / self.phases
        v = (lat / math.pi + 0.5) * (th - 1)
        sampled = self._bilinear(texture, u, v)

        style = PLANET_STYLES[kind]
        light_angle = (light_bin % self.light_bins) * TAU / self.light_bins
        lx, ly = math.cos(light_angle) * 0.55, math.sin(light_angle) * 0.55
        lz = math.sqrt(max(0.0, 1.0 - lx * lx - ly * ly))
        ndotl = np.maximum(0, self.gx * lx + self.gy * ly + self.gz * lz)

        if kind == "sun":
            limb = 0.42 + 0.58 * self.gz**0.52
            rgb = sampled * limb[..., None]
            rgb += self.fresnel[..., None] * np.array([0.32, 0.11, 0.01], np.float32)
        else:
            diffuse = 0.13 + 0.87 * ndotl**0.84
            hx, hy, hz = lx, ly, lz + 1.0
            hnorm = math.sqrt(hx * hx + hy * hy + hz * hz)
            hx, hy, hz = hx / hnorm, hy / hnorm, hz / hnorm
            ndoth = np.maximum(0, self.gx * hx + self.gy * hy + self.gz * hz)
            spec = ndoth**30 * style.specular
            glow = np.asarray(style.glow_rgb, np.float32) / 255.0
            rgb = sampled * diffuse[..., None] + spec[..., None]
            rgb += self.fresnel[..., None] * glow * 0.45

        arr = np.empty((self.size, self.size, 4), np.uint8)
        arr[..., :3] = np.clip(rgb * 255, 0, 255).astype(np.uint8)
        arr[..., 3] = np.clip(self.alpha * 255, 0, 255).astype(np.uint8)
        return self._remember(self._body_cache, key, Image.fromarray(arr, "RGBA"), self.max_cache_frames)

    def _cloud_frame(self, phase_index: int) -> Image.Image:
        key = phase_index % self.phases
        hit = self._cloud_cache.get(key)
        if hit is not None:
            self._cloud_cache.move_to_end(key)
            return hit
        cloud = make_earth_cloud_texture()
        th, tw = cloud.shape
        lat, lon = self._get_geometry("earth")
        u = (lon / TAU + 0.5) * tw + key * tw / self.phases
        v = (lat / math.pi + 0.5) * (th - 1)
        sampled = self._bilinear(cloud[..., None], u, v)[..., 0]
        alpha = sampled * self.alpha * (0.50 + 0.50 * self.gz)
        arr = np.zeros((self.size, self.size, 4), np.uint8)
        arr[..., :3] = (238, 249, 255)
        arr[..., 3] = np.clip(alpha * 255, 0, 255).astype(np.uint8)
        return self._remember(self._cloud_cache, key, Image.fromarray(arr, "RGBA"), min(48, self.max_cache_frames // 3))

    def _phase(self, kind: str, t_seconds: float, period: float | None = None) -> tuple[int, int, float]:
        style = PLANET_STYLES[kind]
        period = float(period or style.spin_period)
        phase = (t_seconds / period * self.phases * style.spin_direction) % self.phases
        i0 = int(math.floor(phase))
        return i0, (i0 + 1) % self.phases, phase - i0

    def get_body(self, kind: str, t_seconds: float, light_angle: float = -2.45) -> Image.Image:
        """Return a smoothly rotating RGBA sphere at the engine's native size."""
        if kind not in PLANET_STYLES:
            raise KeyError(kind)
        light_bin = int(round((light_angle % TAU) / TAU * self.light_bins)) % self.light_bins
        i0, i1, mix = self._phase(kind, t_seconds)
        a = self._body_frame(kind, i0, light_bin)
        b = self._body_frame(kind, i1, light_bin)
        body = Image.blend(a, b, mix) if mix > 0.002 else a.copy()

        if kind == "earth":
            # Clouds complete a deliberately different artistic cycle, making
            # the atmosphere visibly independent from the surface.
            cphase = (t_seconds / 19.2 * self.phases) % self.phases
            c0 = int(math.floor(cphase))
            clouds = Image.blend(self._cloud_frame(c0), self._cloud_frame(c0 + 1), cphase - c0)
            body.alpha_composite(clouds)
        return body

    def render_planet(self, kind: str, t_seconds: float, diameter: int,
                      light_angle: float = -2.45, include_glow: bool = True) -> Image.Image:
        """Return a complete planet sprite, including rings and their shadows."""
        diameter = max(8, int(round(diameter)))
        body = self.get_body(kind, t_seconds, light_angle)
        if body.width != diameter:
            body = body.resize((diameter, diameter), Image.Resampling.LANCZOS)

        ring_kind = kind if kind in ("saturn", "uranus") else None
        pad_factor = 2.75 if ring_kind == "saturn" else (2.30 if ring_kind == "uranus" else 1.46)
        side = int(math.ceil(diameter * pad_factor))
        if side % 2:
            side += 1
        canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        center = side // 2

        if include_glow:
            glow = _planet_glow(diameter, PLANET_STYLES[kind].glow_rgb,
                                150 if kind == "sun" else 82)
            canvas.alpha_composite(glow, (center - glow.width // 2, center - glow.height // 2))

        back = front = None
        if ring_kind:
            light_bin = int(round((light_angle % TAU) / TAU * 24)) % 24
            # Quantisation prevents an animated entrance scale from filling the
            # ring cache with dozens of near-identical multi-megabyte images.
            ring_diameter = max(16, int(round(diameter / 16.0)) * 16)
            back, front = _ring_layers(ring_kind, ring_diameter, light_bin)
            canvas.alpha_composite(back, (center - back.width // 2, center - back.height // 2))

        bx, by = center - diameter // 2, center - diameter // 2
        canvas.alpha_composite(body, (bx, by))

        if ring_kind:
            shadow_diameter = max(16, int(round(diameter / 16.0)) * 16)
            shadow = _ring_shadow(shadow_diameter, ring_kind)
            if shadow.size != body.size:
                shadow = shadow.resize(body.size, Image.Resampling.BILINEAR)
            canvas.alpha_composite(shadow, (bx, by))
            canvas.alpha_composite(front, (center - front.width // 2, center - front.height // 2))
        return canvas


@lru_cache(maxsize=32)
def _planet_glow(diameter: int, rgb: tuple[int, int, int], peak_alpha: int) -> Image.Image:
    size = int(diameter * 1.40)
    if size % 2:
        size += 1
    yy, xx = np.mgrid[-1:1:complex(0, size), -1:1:complex(0, size)]
    radius = np.sqrt(xx * xx + yy * yy)
    alpha = np.clip(1 - radius, 0, 1) ** 2.4 * peak_alpha
    arr = np.empty((size, size, 4), np.uint8)
    arr[..., :3] = rgb
    arr[..., 3] = alpha.astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


@lru_cache(maxsize=12)
def _ring_layers(kind: str, diameter: int, light_bin: int) -> tuple[Image.Image, Image.Image]:
    """Build cached rear/front ring layers with directional light shading."""
    if kind == "saturn":
        width, height, flatten, angle = int(diameter * 2.62), int(diameter * 1.36), 0.34, -18.0
        bands = (
            (2.22, 11, (174, 144, 96, 105)),
            (2.06, 24, (245, 218, 157, 220)),
            (1.78, 17, (219, 183, 122, 190)),
            (1.52, 10, (250, 233, 191, 155)),
        )
    else:
        width, height, flatten, angle = int(diameter * 2.20), int(diameter * 2.20), 0.27, 82.0
        bands = (
            (1.79, 5, (156, 240, 248, 125)),
            (1.62, 4, (113, 215, 235, 100)),
            (1.45, 3, (208, 255, 255, 90)),
        )
    width += width % 2
    height += height % 2
    ring = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ring, "RGBA")
    cx, cy = width / 2, height / 2
    radius = diameter / 2
    for mult, line_width, color in bands:
        rx = radius * mult
        ry = rx * flatten
        draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=color,
                     width=max(2, int(line_width * diameter / 512)))

    # Shade the ring itself: the side opposite the light is subtly darker.
    light_angle = light_bin * TAU / 24
    yy, xx = np.mgrid[0:height, 0:width]
    nx = (xx - cx) / max(cx, 1)
    ny = (yy - cy) / max(cy, 1)
    directional = np.clip(0.72 + 0.28 * (nx * math.cos(light_angle) + ny * math.sin(light_angle)), 0.52, 1.0)
    arr = np.asarray(ring).copy()
    arr[..., :3] = np.clip(arr[..., :3].astype(np.float32) * directional[..., None], 0, 255).astype(np.uint8)
    ring = Image.fromarray(arr, "RGBA")

    # In local ring coordinates, the upper half is behind the planet and the
    # lower half is in front.  Rotate only after splitting, preserving depth.
    upper = Image.new("L", ring.size, 0)
    ImageDraw.Draw(upper).rectangle((0, 0, width, int(cy)), fill=255)
    lower = ImageChops.invert(upper)
    back, front = ring.copy(), ring.copy()
    back.putalpha(ImageChops.multiply(ring.getchannel("A"), upper))
    front.putalpha(ImageChops.multiply(ring.getchannel("A"), lower))
    back = back.rotate(angle, Image.Resampling.BICUBIC, expand=False)
    front = front.rotate(angle, Image.Resampling.BICUBIC, expand=False)
    return back, front


@lru_cache(maxsize=12)
def _ring_shadow(diameter: int, kind: str) -> Image.Image:
    """Soft ring-on-globe shadow, clipped naturally by the planet sprite."""
    yy, xx = np.mgrid[-1:1:complex(0, diameter), -1:1:complex(0, diameter)]
    angle = math.radians(-18 if kind == "saturn" else 82)
    y_rot = -xx * math.sin(angle) + yy * math.cos(angle)
    sigma = 0.045 if kind == "saturn" else 0.028
    offset = 0.075 if kind == "saturn" else 0.035
    band = np.exp(-((y_rot - offset) / sigma) ** 2)
    sphere = xx * xx + yy * yy <= 0.985
    # A broad blur prevents the band from looking like a flat painted stripe.
    alpha = np.clip(band * sphere * (102 if kind == "saturn" else 68), 0, 255).astype(np.uint8)
    arr = np.zeros((diameter, diameter, 4), np.uint8)
    arr[..., 3] = alpha
    return Image.fromarray(arr, "RGBA").filter(ImageFilter.GaussianBlur(max(1, diameter // 170)))


def orbit_position(theta: float, rx: float, ry: float) -> tuple[float, float, float]:
    """Return x/y plus depth.  Draw z<0 before the planet, z>=0 after it."""
    return math.cos(theta) * rx, math.sin(theta) * ry, math.sin(theta)


__all__ = [
    "Planet25DEngine",
    "PlanetStyle",
    "PLANET_STYLES",
    "make_equirectangular_texture",
    "orbit_position",
]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render one deterministic 2.5D planet styleframe."
    )
    parser.add_argument("--kind", choices=sorted(PLANET_STYLES), default="earth")
    parser.add_argument("--time", type=float, default=0.0, help="Animation time in seconds")
    parser.add_argument("--diameter", type=int, default=640)
    parser.add_argument("--engine-size", type=int, default=512)
    parser.add_argument("--phases", type=int, default=72)
    parser.add_argument("--light-angle", type=float, default=-2.45)
    parser.add_argument("--no-glow", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("planet_styleframe.png"))
    return parser.parse_args()


def _main() -> None:
    args = _parse_args()
    if args.diameter < 8 or args.engine_size < 64 or args.phases < 8:
        raise SystemExit("diameter >= 8, engine-size >= 64 and phases >= 8 are required")
    engine = Planet25DEngine(size=args.engine_size, phases=args.phases)
    image = engine.render_planet(
        args.kind,
        args.time,
        args.diameter,
        light_angle=args.light_angle,
        include_glow=not args.no_glow,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)
    print(
        f"Rendered {args.kind}: {image.width}x{image.height} RGBA -> {args.output} "
        f"(cache budget ~{engine.approximate_cache_mib:.1f} MiB)"
    )


if __name__ == "__main__":
    _main()
