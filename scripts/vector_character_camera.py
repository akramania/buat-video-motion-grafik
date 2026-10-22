#!/usr/bin/env python3
"""
Reusable Cinematic 2D/2.5D Vector Camera, plus an optional "Seni Mengira Cukup" example
- Zero Kinetic Typography overlays (ONLY bottom full subtitles + Quranic Verse in S15 & Hadith in S16).
- Refined, smooth, expressive vector characters (tapered capsule limbs with seamless joint circles,
  2-tone soft shading, expressive eyes with catchlights, animated tears, detailed hijabs/outfits).
- Rich environmental props in every scene.
- True Mathematical Vector Camera with smooth Zoom-In to Characters & Zoom-In to Objects.
"""
import argparse
import json
import math
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# No project files are read and no folders are created at import time.
# The original 16-scene example is opt-in via configure_project().
PROJ_DIR = INTER_DIR = OUT_DIR = None
FONT_SANS = ImageFont.truetype("DejaVuSans.ttf", 12).path
FONT_BOLD = ImageFont.truetype("DejaVuSans-Bold.ttf", 12).path
FONT_ARABIC = FONT_SANS  # Standalone demo contains no Arabic; project mode requires a supplied Arabic font.
NORM_RMS = np.zeros(1, dtype=float)
FPS = 30
TOTAL_FRAMES = 1
DURATION = 0.0

# Internal canvas 1280x720 (upscaled cleanly to 1920x1080 in FFmpeg, while camera zoom renders vector shapes natively)
W, H = 1280, 720

# Harmonic Cream & Warm Cinematic Palette
C_CREAM = (248, 243, 232)      # #F8F3E8
C_CREAM_DARK = (232, 224, 207) # #E8E0CF
C_SAND = (216, 204, 182)
C_INK = (38, 54, 69)           # #263645
C_MUTED = (88, 104, 120)
C_TEAL = (63, 122, 123)        # #3F7A7B
C_TEAL_DARK = (44, 92, 94)
C_TEAL_LIGHT = (98, 154, 155)
C_NAVY = (64, 76, 94)
C_NAVY_DARK = (46, 56, 70)
C_GOLD = (218, 176, 98)        # #DAB062
C_GOLD_LIGHT = (246, 218, 154)
C_TERRA = (192, 104, 78)       # #C0684E
C_SAGE = (92, 138, 114)        # #5C8A72
C_SAGE_DARK = (66, 106, 86)
C_SAGE_LIGHT = (146, 182, 160)
C_SKY = (225, 238, 246)
C_PEACH = (252, 234, 218)
C_WHITE = (255, 253, 249)

# Character Skin & Outfit Palettes
SKIN_AMIR = (190, 132, 94)
SKIN_AMIR_SHADE = (162, 108, 72)
SKIN_LIGHT = (216, 166, 130)
SKIN_LIGHT_SHADE = (192, 142, 108)
HAIR_DARK = (38, 34, 32)
HAIR_SILVER = (186, 182, 176)

@lru_cache(maxsize=64)
def get_font(kind: str, size: int):
    path = {"arabic": FONT_ARABIC, "sans": FONT_SANS, "bold": FONT_BOLD}[kind]
    return ImageFont.truetype(path, max(8, int(size)))

def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))

def smoothstep(edge0, edge1, x):
    if edge1 <= edge0:
        return 1.0 if x >= edge1 else 0.0
    t = clamp((x - edge0) / (edge1 - edge0))
    return t * t * (3.0 - 2.0 * t)

def lerp(a, b, t):
    return a + (b - a) * t

def ease_out_back(t):
    t = clamp(t)
    c1 = 1.70158
    c3 = c1 + 1.0
    return 1.0 + c3 * ((t - 1.0) ** 3) + c1 * ((t - 1.0) ** 2)

class CamCanvas:
    """
    Mathematical Vector Camera wrapping Pillow ImageDraw.
    Transforms world coordinates (wx, wy) around camera center (cx, cy) with zoom factor `z`,
    so zooming in 2.5x onto a character's face or an object renders razor-sharp vector geometry!
    """
    def __init__(self, im: Image.Image, cx: float = 640.0, cy: float = 360.0, zoom: float = 1.0):
        self.im = im
        self.d = ImageDraw.Draw(im, "RGBA")
        self.cx = float(cx)
        self.cy = float(cy)
        self.z = float(zoom) * min(im.width / 1280.0, im.height / 720.0)

    def tx(self, x: float) -> float:
        return self.im.width * 0.5 + (x - self.cx) * self.z

    def ty(self, y: float) -> float:
        return self.im.height * 0.5 + (y - self.cy) * self.z

    def tr(self, r: float) -> float:
        return max(1.0, r * self.z)

    def tw(self, w: float) -> int:
        return max(1, int(round(w * self.z)))

    def rect(self, box, fill=None, outline=None, width=2, radius=0):
        x0, y0, x1, y1 = box
        b = (int(round(self.tx(x0))), int(round(self.ty(y0))), int(round(self.tx(x1))), int(round(self.ty(y1))))
        if b[2] < b[0]: b = (b[2], b[1], b[0], b[3])
        if b[3] < b[1]: b = (b[0], b[3], b[2], b[1])
        sw = self.tw(width) if outline else 0
        if radius > 0:
            self.d.rounded_rectangle(b, radius=int(round(radius * self.z)), fill=fill, outline=outline, width=sw)
        else:
            self.d.rectangle(b, fill=fill, outline=outline, width=sw)

    def ellipse(self, box, fill=None, outline=None, width=2):
        x0, y0, x1, y1 = box
        b = (int(round(self.tx(x0))), int(round(self.ty(y0))), int(round(self.tx(x1))), int(round(self.ty(y1))))
        sw = self.tw(width) if outline else 0
        self.d.ellipse(b, fill=fill, outline=outline, width=sw)

    def circle(self, x, y, r, fill=None, outline=None, width=2):
        self.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=outline, width=width)

    def poly(self, pts, fill=None, outline=None, width=2):
        tpts = [(int(round(self.tx(px))), int(round(self.ty(py)))) for px, py in pts]
        if fill and len(tpts) >= 3:
            self.d.polygon(tpts, fill=fill)
        if outline and len(tpts) >= 2:
            self.d.line(tpts + [tpts[0]], fill=outline, width=self.tw(width), joint="curve")

    def line(self, pts, fill=C_INK, width=2):
        if len(pts) >= 2 and isinstance(pts[0], (int, float)):
            it = iter(pts)
            pts = list(zip(it, it))
        tpts = [(int(round(self.tx(px))), int(round(self.ty(py)))) for px, py in pts]
        self.d.line(tpts, fill=fill, width=self.tw(width), joint="curve")

    def arc(self, box, start, end, fill=C_INK, width=2):
        x0, y0, x1, y1 = box
        b = (int(round(self.tx(x0))), int(round(self.ty(y0))), int(round(self.tx(x1))), int(round(self.ty(y1))))
        self.d.arc(b, start=start, end=end, fill=fill, width=self.tw(width))

    def pieslice(self, box, start, end, fill=None, outline=None, width=2):
        x0, y0, x1, y1 = box
        b = (int(round(self.tx(x0))), int(round(self.ty(y0))), int(round(self.tx(x1))), int(round(self.ty(y1))))
        self.d.pieslice(b, start=start, end=end, fill=fill, outline=outline, width=self.tw(width) if outline else 0)

    def capsule(self, p0, p1, w0, w1, fill, outline=C_INK, width=2.2):
        """Draw a smooth tapered capsule between p0 and p1 with rounded joint ends (no pointy corners!)."""
        x0, y0 = p0
        x1, y1 = p1
        dx, dy = x1 - x0, y1 - y0
        dist = math.hypot(dx, dy)
        r0, r1 = w0 * 0.5, w1 * 0.5
        if dist < 1e-3:
            self.circle(x0, y0, r0, fill=fill, outline=outline, width=width)
            return
        nx, ny = -dy / dist, dx / dist
        pts = [
            (x0 + nx * r0, y0 + ny * r0),
            (x1 + nx * r1, y1 + ny * r1),
            (x1 - nx * r1, y1 - ny * r1),
            (x0 - nx * r0, y0 - ny * r0),
        ]
        # Fill caps & body first, then draw side outlines so joints blend seamlessly
        self.poly(pts, fill=fill, outline=None)
        self.circle(x0, y0, r0, fill=fill, outline=None)
        self.circle(x1, y1, r1, fill=fill, outline=None)
        if outline:
            self.line([pts[0], pts[1]], fill=outline, width=width)
            self.line([pts[3], pts[2]], fill=outline, width=width)

    def text(self, x, y, s, size=18, kind="bold", fill=C_INK, anchor="mm", rtl=False):
        f = get_font(kind, round(size * self.z))
        sx, sy = int(round(self.tx(x))), int(round(self.ty(y)))
        if rtl:
            self.d.text((sx, sy), s, font=f, fill=fill, anchor=anchor, direction="rtl", language="ar")
        else:
            self.d.text((sx, sy), s, font=f, fill=fill, anchor=anchor)

def solve_ik(p0, p1, l1, l2, mode="elbow", f_dir=1.0):
    """Gravity-aware two-bone IK: elbows always hang downward (+y); knees always bend forward (f_dir)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    d = clamp(math.hypot(dx, dy), abs(l1 - l2) + 0.01, l1 + l2 - 0.01)
    ang = math.atan2(dy, dx)
    cos_a = clamp((l1 * l1 + d * d - l2 * l2) / (2.0 * l1 * d), -1.0, 1.0)
    off = math.acos(cos_a)
    j1 = (p0[0] + l1 * math.cos(ang + off), p0[1] + l1 * math.sin(ang + off))
    j2 = (p0[0] + l1 * math.cos(ang - off), p0[1] + l1 * math.sin(ang - off))
    if mode == "elbow":
        return j1 if j1[1] >= j2[1] else j2
    else:
        return j1 if (j1[0] - p0[0]) * f_dir >= (j2[0] - p0[0]) * f_dir else j2

def draw_character(
    cam: CamCanvas,
    x: float,
    ground_y: float,
    scale: float = 1.0,
    t: float = 0.0,
    role: str = "amir",
    pose: str = "stand",
    mood: str = "calm",
    facing: int = 1,
    view: str = "auto",
    lanyard: bool = True,
    tear: float = 0.0,
    speaking: float = 0.0,
):
    """
    Multi-Angle 2D Vector Character Rig supporting true body + head orientations:
    - view: 'front', 'back', 'side_right', 'side_left', 'three_quarter_right', 'three_quarter_left', or 'auto'
      When 'auto', selects orientation naturally from pose & facing:
        * 'walk', 'sit_table', 'sit_warung' -> 'side_right' / 'side_left'
        * 'carry_box', 'dua_stand', 'dua_sit', 'phone_call', 'phone_look' -> 'three_quarter_right' / 'three_quarter_left'
        * 'back_look' -> 'back'
        * otherwise -> 'front'
    """
    s = scale
    if view == "auto":
        if pose in ("walk", "sit_table", "sit_warung"):
            view = "side_right" if facing >= 0 else "side_left"
        elif pose in ("carry_box", "dua_stand", "dua_sit", "phone_call", "phone_look"):
            view = "three_quarter_right" if facing >= 0 else "three_quarter_left"
        elif pose == "back_look":
            view = "back"
        else:
            view = "front"

    is_side = view in ("side_right", "side_left")
    is_3q = view in ("three_quarter_right", "three_quarter_left")
    is_back = (view == "back")
    is_front = (view == "front")

    if view in ("side_right", "three_quarter_right"):
        f_dir = 1.0
    elif view in ("side_left", "three_quarter_left"):
        f_dir = -1.0
    else:
        f_dir = 1.0 if facing >= 0 else -1.0

    # Palettes per character role
    if role == "amir":
        skin, skin_sh = SKIN_AMIR, SKIN_AMIR_SHADE
        shirt, shirt_sh = C_TEAL, C_TEAL_DARK
        pants, pants_sh = C_NAVY, C_NAVY_DARK
        hair_col = HAIR_DARK
    elif role == "mak":
        skin, skin_sh = SKIN_LIGHT, SKIN_LIGHT_SHADE
        shirt, shirt_sh = (176, 124, 130), (148, 98, 104)
        pants, pants_sh = (122, 96, 114), (98, 74, 90)
        hair_col = HAIR_SILVER
    elif role == "abah":
        skin, skin_sh = SKIN_AMIR, SKIN_AMIR_SHADE
        shirt, shirt_sh = C_SAGE, C_SAGE_DARK
        pants, pants_sh = (72, 88, 84), (54, 68, 64)
        hair_col = HAIR_SILVER
    elif role == "exec":
        skin, skin_sh = SKIN_LIGHT, SKIN_LIGHT_SHADE
        shirt, shirt_sh = (104, 138, 168), (82, 112, 140)
        pants, pants_sh = (62, 74, 90), (46, 56, 70)
        hair_col = HAIR_DARK
    else: # salma
        skin, skin_sh = SKIN_AMIR, SKIN_AMIR_SHADE
        shirt, shirt_sh = (142, 122, 158), (116, 98, 132)
        pants, pants_sh = (112, 96, 126), (90, 74, 104)
        hair_col = HAIR_DARK

    breath = math.sin(t * 2.2) * 2.2 * s
    is_walking = (pose == "walk")
    walk_ph = (t * 2.4) % 1.0 if is_walking else 0.0
    bob_y = abs(math.sin(walk_ph * math.pi * 2.0)) * 5.5 * s if is_walking else breath
    if pose == "sigh":
        bob_y = -math.sin(t * 1.6) * 4.5 * s

    # Ground shadow
    if pose not in ("sleep",):
        sw_rad = 34 * s if is_side else 42 * s
        cam.ellipse((x - sw_rad, ground_y - 7 * s, x + sw_rad, ground_y + 7 * s), fill=(38, 54, 69, 42), outline=None)

    # Hip & Shoulder positions according to body orientation
    if pose in ("sit_table", "sit_warung"):
        hip_y = ground_y - 95 * s
        hip_x = x - 10 * s * f_dir
    elif pose == "dua_sit":
        hip_y = ground_y - 38 * s
        hip_x = x
    else:
        hip_y = ground_y - 128 * s - bob_y * 0.4
        hip_x = x

    lean = 0.0
    if pose == "sigh":
        lean = 5.0 * s * f_dir
    elif pose == "carry_box":
        lean = -4.0 * s * f_dir
    elif is_walking:
        lean = 4.5 * s * f_dir

    sh_x = hip_x + lean
    sh_y = hip_y - 102 * s + (bob_y * 0.6 if not is_walking else 0.0)
    if pose == "sigh":
        sh_y += 6.0 * s

    # Shoulder & Hip widths depend on view angle (front/back = wide, 3/4 = medium, side = narrow profile!)
    if is_side:
        torso_hw_top = 18 * s
        torso_hw_bot = 16 * s
        sh_back = (sh_x - 3 * s * f_dir, sh_y + 10 * s)
        sh_front = (sh_x - 1 * s * f_dir, sh_y + 12 * s)
        leg_offsets = [(-2 * s * f_dir, pants_sh, 0.5), (2 * s * f_dir, pants, 0.0)]
    elif is_3q:
        torso_hw_top = 25 * s
        torso_hw_bot = 23 * s
        sh_back = (sh_x + 12 * s * f_dir, sh_y + 9 * s)   # far shoulder on leading side
        sh_front = (sh_x - 14 * s * f_dir, sh_y + 10 * s) # near shoulder on trailing side
        leg_offsets = [(7 * s * f_dir, pants_sh, 0.5), (-7 * s * f_dir, pants, 0.0)]
    else:
        # front or back
        torso_hw_top = 31 * s
        torso_hw_bot = 27 * s
        sh_back = (sh_x - 28 * s * f_dir, sh_y + 9 * s)
        sh_front = (sh_x + 28 * s * f_dir, sh_y + 9 * s)
        leg_offsets = [(-10 * s, pants_sh, 0.5), (10 * s, pants, 0.0)]

    # 1. LEGS
    thigh_l = (63 * s if (is_walking or pose == "carry_box") else 58.5 * s)
    shin_l = thigh_l
    if pose == "dua_sit":
        w_sit = 32 * s if is_side else 40 * s
        cam.rect((hip_x - w_sit, ground_y - 36 * s, hip_x + w_sit + 8 * s * f_dir, ground_y - 4 * s), fill=pants, outline=C_INK, width=2.2, radius=16)
        if role in ("mak", "salma"):
            cam.rect((hip_x - w_sit - 4 * s, ground_y - 48 * s, hip_x + w_sit + 10 * s * f_dir, ground_y - 3 * s), fill=pants, outline=C_INK, width=2.2, radius=14)
    elif pose in ("sit_table", "sit_warung"):
        for leg_i, (ox, col_p, _) in enumerate(leg_offsets):
            knee = (hip_x + 48 * s * f_dir + ox * 0.5, hip_y + 6 * s)
            ankle = (hip_x + 50 * s * f_dir + ox * 0.5, ground_y - 12 * s)
            cam.capsule((hip_x + ox * 0.5, hip_y), knee, 24 * s, 20 * s, col_p)
            cam.capsule(knee, ankle, 20 * s, 15 * s, col_p)
            sx0, sy0 = ankle
            cam.poly([
                (sx0 - 7 * s * f_dir, sy0),
                (sx0 + 24 * s * f_dir, sy0 + 2 * s),
                (sx0 + 26 * s * f_dir, sy0 + 12 * s),
                (sx0 - 9 * s * f_dir, sy0 + 12 * s)
            ], fill=(68, 58, 54), outline=C_INK, width=2)
    else:
        for leg_i, (ox, col_p, phase_off) in enumerate(leg_offsets):
            hip_pt = (hip_x + ox, hip_y)
            if is_walking:
                ph = (walk_ph + phase_off) % 1.0
                stride = math.sin(ph * math.pi * 2.0) * 34 * s * f_dir
                lift = max(0.0, -math.cos(ph * math.pi * 2.0)) * 18 * s
                ankle_pt = (hip_x + ox + stride, ground_y - 12 * s - lift)
            else:
                ankle_pt = (hip_x + ox, ground_y - 12 * s)
            knee_pt = solve_ik(hip_pt, ankle_pt, thigh_l, shin_l, mode="knee", f_dir=f_dir)
            if role in ("mak", "salma"):
                if leg_i == 1:
                    cam.poly([
                        (hip_x - torso_hw_bot, hip_y - 10 * s),
                        (hip_x + torso_hw_bot, hip_y - 10 * s),
                        (hip_x + (torso_hw_bot + 10 * s), ground_y - 12 * s),
                        (hip_x - (torso_hw_bot + 10 * s), ground_y - 12 * s),
                    ], fill=pants, outline=C_INK, width=2.2)
            else:
                w_th = 22 * s if is_side else 25 * s
                w_sh = 18 * s if is_side else 20 * s
                cam.capsule(hip_pt, knee_pt, w_th, w_sh, col_p)
                cam.capsule(knee_pt, ankle_pt, w_sh, 15 * s, col_p)
            ax, ay = ankle_pt
            if is_back:
                # Rear shoe heel view
                cam.rect((ax - 9 * s, ay, ax + 9 * s, ay + 12 * s), fill=(68, 58, 54), outline=C_INK, width=2, radius=4)
            else:
                cam.poly([
                    (ax - 9 * s * f_dir, ay),
                    (ax + 22 * s * f_dir, ay + 2 * s),
                    (ax + 24 * s * f_dir, ay + 12 * s),
                    (ax - 11 * s * f_dir, ay + 12 * s)
                ], fill=(68, 58, 54), outline=C_INK, width=2)

    # 2. HAND TARGETS & BACK ARM (drawn behind torso)
    ua_l, fa_l = (43.5 * s, 43.5 * s) if pose == "stand" else (48 * s, 46 * s)
    if pose == "touch_lanyard":
        hand_back = (sh_back[0] - 6 * s * f_dir, hip_y - 6 * s)
        hand_front = (sh_x + (14 if (is_side or is_3q) else 4) * s * f_dir, sh_y + 44 * s)
    elif pose == "phone_look":
        hand_back = (sh_back[0] - 4 * s * f_dir, hip_y - 6 * s)
        hand_front = (sh_x + 36 * s * f_dir, sh_y + 38 * s)
    elif pose == "phone_call":
        hand_back = (sh_back[0] - 4 * s * f_dir, hip_y - 6 * s)
        hand_front = (sh_x - 16 * s * f_dir, sh_y - 26 * s)
    elif pose == "carry_box":
        hand_back = (sh_x + 36 * s * f_dir, sh_y + 50 * s)
        hand_front = (sh_x + 38 * s * f_dir, sh_y + 54 * s)
    elif pose in ("dua_stand", "dua_sit"):
        hand_back = (sh_x + 30 * s * f_dir, sh_y + 24 * s + breath * 0.5)
        hand_front = (sh_x + 36 * s * f_dir, sh_y + 28 * s + breath * 0.5)
    elif pose == "wipe_tear":
        wipe_p = 0.5 + 0.5 * math.sin(t * 3.0)
        hand_back = (sh_back[0] - 4 * s * f_dir, hip_y - 6 * s)
        hand_front = (sh_x + (16 - 6 * wipe_p) * s * f_dir, sh_y - (20 + 10 * wipe_p) * s)
    elif pose in ("sit_table", "sit_warung"):
        lift = 0.5 - 0.5 * math.cos(t * 2.2) if pose == "sit_warung" else 0.0
        hand_back = (sh_x + 34 * s * f_dir, sh_y + 52 * s)
        hand_front = (sh_x + (44 - 16 * lift) * s * f_dir, sh_y + (52 - 58 * lift) * s)
    elif is_walking:
        swing = math.sin(walk_ph * math.pi * 2.0) * 26 * s * f_dir
        hand_back = (sh_x - swing, hip_y - 10 * s)
        hand_front = (sh_x + swing, hip_y - 10 * s)
    else:
        hand_back = (sh_back[0] - 5 * s * f_dir, hip_y - 4 * s)
        hand_front = (sh_front[0] + 5 * s * f_dir, hip_y - 4 * s)

    elb_back = solve_ik(sh_back, hand_back, ua_l, fa_l, mode="elbow", f_dir=f_dir)
    cam.capsule(sh_back, elb_back, 19 * s, 16 * s, shirt_sh)
    cam.capsule(elb_back, hand_back, 16 * s, 13 * s, shirt_sh)
    cam.circle(hand_back[0], hand_back[1], 7 * s, fill=skin_sh, outline=C_INK, width=1.8)

    # 3. NECK & MULTI-ANGLE TORSO
    neck_x = sh_x + (3 * s * f_dir if is_side else (2 * s * f_dir if is_3q else 0.0))
    neck_top = (neck_x, sh_y - 11 * s)
    cam.capsule((neck_x, sh_y + 6 * s), neck_top, 16 * s, 14 * s, skin_sh)

    if is_side:
        # Side Profile Torso: chest curve in front (+f_dir), straighter back (-f_dir)
        t_left = min(sh_x, hip_x) - 16 * s if f_dir > 0 else min(sh_x, hip_x) - 20 * s
        t_right = max(sh_x, hip_x) + 20 * s if f_dir > 0 else max(sh_x, hip_x) + 16 * s
        cam.rect((t_left, sh_y - 2 * s, t_right, hip_y + 10 * s), fill=shirt, outline=C_INK, width=2.4, radius=15)
        # Back spine shadow strip
        if f_dir > 0:
            cam.rect((t_left + 2 * s, sh_y + 2 * s, t_left + 11 * s, hip_y + 7 * s), fill=shirt_sh, outline=None, radius=6)
        else:
            cam.rect((t_right - 11 * s, sh_y + 2 * s, t_right - 2 * s, hip_y + 7 * s), fill=shirt_sh, outline=None, radius=6)
        # Side collar wrap
        cam.poly([
            (neck_x - 8 * s * f_dir, sh_y - 3 * s),
            (neck_x + 12 * s * f_dir, sh_y + 6 * s),
            (neck_x + 4 * s * f_dir, sh_y + 15 * s),
            (neck_x - 9 * s * f_dir, sh_y + 6 * s),
        ], fill=shirt_sh, outline=C_INK, width=1.6)
        # Side lanyard hanging along front chest edge
        if role == "amir" and lanyard:
            lx = sh_x + 17 * s * f_dir + math.sin(t * 2.1) * 2.0 * s
            ly = sh_y + 42 * s
            cam.line([(neck_x - 4 * s * f_dir, sh_y - 1 * s), (lx, ly)], fill=(134, 152, 172), width=3.2)
            cam.rect((lx - 4 * s, ly - 2 * s, lx + 4 * s, ly + 6 * s), fill=(216, 222, 228), outline=C_INK, width=1.3, radius=2)
            cam.line([(lx - 3 * s, ly), (lx + 3 * s, ly + 5 * s)], fill=C_TERRA, width=1.5)
            cam.rect((lx - 9 * s, ly + 6 * s, lx + 9 * s, ly + 34 * s), fill=C_WHITE, outline=C_INK, width=1.6, radius=3)
            cam.rect((lx - 7 * s, ly + 9 * s, lx + 7 * s, ly + 15 * s), fill=C_TEAL, outline=None)

    elif is_3q:
        # 3/4 View Torso: collar, buttons, pocket & lanyard shifted toward leading side (+f_dir)
        t_left = min(sh_x, hip_x) - 24 * s
        t_right = max(sh_x, hip_x) + 24 * s
        cam.rect((t_left, sh_y - 2 * s, t_right, hip_y + 10 * s), fill=shirt, outline=C_INK, width=2.4, radius=16)
        # Trailing side shadow
        if f_dir > 0:
            cam.rect((t_left + 2 * s, sh_y + 2 * s, t_left + 13 * s, hip_y + 7 * s), fill=shirt_sh, outline=None, radius=6)
        else:
            cam.rect((t_right - 13 * s, sh_y + 2 * s, t_right - 2 * s, hip_y + 7 * s), fill=shirt_sh, outline=None, radius=6)
        cx_torso = sh_x + 8 * s * f_dir
        if role in ("amir", "exec", "abah"):
            cam.poly([(cx_torso - 11 * s, sh_y - 2 * s), (cx_torso, sh_y + 15 * s), (cx_torso - 16 * s, sh_y + 11 * s)], fill=shirt_sh, outline=C_INK, width=1.6)
            cam.poly([(cx_torso + 11 * s, sh_y - 2 * s), (cx_torso, sh_y + 15 * s), (cx_torso + 16 * s, sh_y + 11 * s)], fill=shirt_sh, outline=C_INK, width=1.6)
            cam.line([(cx_torso, sh_y + 15 * s), (cx_torso, hip_y + 6 * s)], fill=shirt_sh, width=1.8)
            if role == "amir":
                px0 = cx_torso + 5 * s * f_dir
                cam.rect((px0, sh_y + 26 * s, px0 + 13 * s * f_dir, sh_y + 42 * s), fill=shirt_sh, outline=C_INK, width=1.4, radius=3)
        if role == "amir" and lanyard:
            lx = cx_torso + math.sin(t * 2.1) * 2.5 * s
            ly = sh_y + 42 * s
            cam.line([(neck_x - 10 * s, sh_y), (lx - 2 * s, ly)], fill=(134, 152, 172), width=3.0)
            cam.line([(neck_x + 10 * s, sh_y), (lx + 2 * s, ly)], fill=(134, 152, 172), width=3.0)
            cam.rect((lx - 5 * s, ly - 2 * s, lx + 5 * s, ly + 7 * s), fill=(216, 222, 228), outline=C_INK, width=1.4, radius=2)
            cam.line([(lx - 4 * s, ly), (lx + 4 * s, ly + 6 * s)], fill=C_TERRA, width=1.6)
            cam.rect((lx - 12 * s, ly + 7 * s, lx + 12 * s, ly + 36 * s), fill=C_WHITE, outline=C_INK, width=1.8, radius=3)
            cam.rect((lx - 9 * s, ly + 10 * s, lx + 9 * s, ly + 16 * s), fill=C_TEAL, outline=None)
            cam.circle(lx, ly + 23 * s, 3.8 * s, fill=SKIN_AMIR, outline=None)

    elif is_back:
        # Rear View Torso: back yoke seam across shoulders, back collar band, no front buttons/card
        t_left = min(sh_x, hip_x) - 31 * s
        t_right = max(sh_x, hip_x) + 31 * s
        cam.rect((t_left, sh_y - 2 * s, t_right, hip_y + 10 * s), fill=shirt, outline=C_INK, width=2.4, radius=16)
        cam.rect((t_left + 3 * s, sh_y + 2 * s, t_left + 15 * s, hip_y + 7 * s), fill=shirt_sh, outline=None, radius=6)
        # Back collar band & shoulder yoke line
        cam.rect((sh_x - 15 * s, sh_y - 5 * s, sh_x + 15 * s, sh_y + 5 * s), fill=shirt_sh, outline=C_INK, width=1.6, radius=4)
        cam.line([(t_left + 4 * s, sh_y + 22 * s), (t_right - 4 * s, sh_y + 22 * s)], fill=shirt_sh, width=2.0)
        if role == "amir" and lanyard:
            # Lanyard strap visible only looping around back of collar
            cam.arc((sh_x - 16 * s, sh_y - 6 * s, sh_x + 16 * s, sh_y + 8 * s), start=0, end=180, fill=(134, 152, 172), width=3.2)

    else:
        # Front View Torso
        t_left = min(sh_x, hip_x) - 31 * s
        t_right = max(sh_x, hip_x) + 31 * s
        cam.rect((t_left, sh_y - 2 * s, t_right, hip_y + 10 * s), fill=shirt, outline=C_INK, width=2.4, radius=16)
        cam.rect((t_left + 3 * s, sh_y + 2 * s, t_left + 15 * s, hip_y + 7 * s), fill=shirt_sh, outline=None, radius=6)
        if role in ("amir", "exec", "abah"):
            cam.poly([(sh_x - 13 * s, sh_y - 2 * s), (sh_x, sh_y + 15 * s), (sh_x - 20 * s, sh_y + 12 * s)], fill=shirt_sh, outline=C_INK, width=1.6)
            cam.poly([(sh_x + 13 * s, sh_y - 2 * s), (sh_x, sh_y + 15 * s), (sh_x + 20 * s, sh_y + 12 * s)], fill=shirt_sh, outline=C_INK, width=1.6)
            cam.line([(sh_x, sh_y + 15 * s), (hip_x, hip_y + 6 * s)], fill=shirt_sh, width=1.8)
            if role == "amir":
                px0 = sh_x + 8 * s
                cam.rect((px0, sh_y + 26 * s, px0 + 16 * s, sh_y + 44 * s), fill=shirt_sh, outline=C_INK, width=1.5, radius=3)
        if role == "amir" and lanyard:
            sway_l = math.sin(t * 2.1) * 3.0 * s
            lx, ly = sh_x + sway_l, sh_y + 42 * s
            cam.line([(sh_x - 14 * s, sh_y), (lx - 3 * s, ly)], fill=(134, 152, 172), width=3.2)
            cam.line([(sh_x + 14 * s, sh_y), (lx + 3 * s, ly)], fill=(134, 152, 172), width=3.2)
            cam.rect((lx - 5 * s, ly - 2 * s, lx + 5 * s, ly + 7 * s), fill=(216, 222, 228), outline=C_INK, width=1.4, radius=2)
            cam.line([(lx - 4 * s, ly), (lx + 4 * s, ly + 6 * s)], fill=C_TERRA, width=1.6)
            cam.rect((lx - 13 * s, ly + 7 * s, lx + 13 * s, ly + 38 * s), fill=C_WHITE, outline=C_INK, width=1.8, radius=3)
            cam.rect((lx - 10 * s, ly + 10 * s, lx + 10 * s, ly + 16 * s), fill=C_TEAL, outline=None)
            cam.circle(lx, ly + 23 * s, 4 * s, fill=SKIN_AMIR, outline=None)

    # Hijab drape for Mak & Kak Salma (adapts to side / 3q / front / back)
    if role in ("mak", "salma"):
        hijab_col = (224, 208, 186) if role == "mak" else (196, 182, 210)
        hijab_sh = (204, 186, 162) if role == "mak" else (172, 158, 188)
        hw_h = 22 * s if is_side else (28 * s if is_3q else 35 * s)
        cam.poly([
            (sh_x - hw_h, sh_y - 28 * s),
            (sh_x + hw_h, sh_y - 28 * s),
            (sh_x + hw_h + 4 * s, sh_y + 46 * s),
            (sh_x + (6 * s * f_dir if not is_back else 0), sh_y + 62 * s),
            (sh_x - hw_h - 4 * s, sh_y + 46 * s),
        ], fill=hijab_col, outline=C_INK, width=2.2)
        cam.arc((sh_x - hw_h + 6 * s, sh_y + 6 * s, sh_x + hw_h - 6 * s, sh_y + 46 * s), start=15, end=165, fill=hijab_sh, width=2.0)

    # 4. MULTI-ANGLE HEAD & EXPRESSIVE FACE
    head_cx = neck_top[0] + (3 * s * f_dir if (is_side or is_3q) else 0.0)
    head_cy = neck_top[1] - 20 * s + (3 * s if pose in ("sigh", "phone_look", "touch_lanyard") else 0.0)
    blink = ((t + (0.3 if role == "mak" else 0.0)) % 4.2) > 4.02

    if is_back:
        # REAR HEAD VIEW: Ears on both sides, full hair/hijab/kopiah on back of head, zero face features
        if role not in ("mak", "salma"):
            cam.ellipse((head_cx - 26 * s, head_cy - 4 * s, head_cx - 16 * s, head_cy + 10 * s), fill=skin, outline=C_INK, width=1.8)
            cam.ellipse((head_cx + 16 * s, head_cy - 4 * s, head_cx + 26 * s, head_cy + 10 * s), fill=skin, outline=C_INK, width=1.8)
            cam.rect((head_cx - 21 * s, head_cy - 24 * s, head_cx + 21 * s, head_cy + 22 * s), fill=skin_sh, outline=C_INK, width=2.2, radius=18)
            # Full back hair covering cranium down to nape
            cam.rect((head_cx - 23 * s, head_cy - 28 * s, head_cx + 23 * s, head_cy + 14 * s), fill=hair_col, outline=C_INK, width=2.2, radius=16)
            if role == "abah":
                cam.pieslice((head_cx - 23 * s, head_cy - 31 * s, head_cx + 23 * s, head_cy - 2 * s), start=180, end=360, fill=C_WHITE, outline=C_INK, width=2.0)
                cam.line([(head_cx - 22 * s, head_cy - 16 * s), (head_cx + 22 * s, head_cy - 16 * s)], fill=C_GOLD, width=2.0)
        else:
            hijab_col = (224, 208, 186) if role == "mak" else (196, 182, 210)
            cam.ellipse((head_cx - 26 * s, head_cy - 30 * s, head_cx + 26 * s, head_cy + 26 * s), fill=hijab_col, outline=C_INK, width=2.2)

    elif is_side:
        # PURE SIDE PROFILE HEAD VIEW: Projecting nose, profile eye, single ear on side, chin goatee
        if role in ("mak", "salma"):
            hijab_col = (224, 208, 186) if role == "mak" else (196, 182, 210)
            cam.ellipse((head_cx - 24 * s, head_cy - 30 * s, head_cx + 22 * s, head_cy + 26 * s), fill=hijab_col, outline=C_INK, width=2.2)
        else:
            # Back of hair in profile
            hx_b = head_cx - 22 * s if f_dir > 0 else head_cx - 10 * s
            cam.ellipse((hx_b, head_cy - 29 * s, hx_b + 32 * s, head_cy + 15 * s), fill=hair_col, outline=C_INK, width=2.0)

        # Profile head base + projecting nose triangle
        cam.rect((head_cx - 18 * s, head_cy - 23 * s, head_cx + 18 * s, head_cy + 23 * s), fill=skin, outline=C_INK, width=2.2, radius=16)
        nose_tip_x = head_cx + 23 * s * f_dir
        cam.poly([
            (head_cx + 14 * s * f_dir, head_cy - 6 * s),
            (nose_tip_x, head_cy + 4 * s),
            (head_cx + 14 * s * f_dir, head_cy + 7 * s),
        ], fill=skin, outline=C_INK, width=1.8)

        # Single Side Ear (behind center of head)
        if role not in ("mak", "salma"):
            ear_x = head_cx - 6 * s * f_dir
            cam.ellipse((ear_x - 5 * s, head_cy - 4 * s, ear_x + 5 * s, head_cy + 9 * s), fill=skin, outline=C_INK, width=1.8)

        # Hair cap / Kopiah in side profile
        if role == "abah":
            cam.pieslice((head_cx - 21 * s, head_cy - 31 * s, head_cx + 21 * s, head_cy - 4 * s), start=180, end=360, fill=C_WHITE, outline=C_INK, width=2.0)
            cam.line([(head_cx - 20 * s, head_cy - 17 * s), (head_cx + 20 * s, head_cy - 17 * s)], fill=C_GOLD, width=2.0)
        elif role in ("amir", "exec"):
            cam.pieslice((head_cx - 21 * s, head_cy - 31 * s, head_cx + 22 * s, head_cy - 4 * s), start=175, end=365, fill=hair_col, outline=C_INK, width=2.0)

        # Single Profile Eye & Eyebrow on leading side
        ex = head_cx + 10 * s * f_dir
        ey = head_cy - 4 * s
        brow_tilt = -2.5 * s if mood in ("sad", "tired", "tearful") else 0.0
        cam.line([(ex - 5 * s * f_dir, ey - 8 * s + brow_tilt), (ex + 4 * s * f_dir, ey - 9 * s - brow_tilt)], fill=hair_col, width=2.4)
        if blink or pose in ("sigh", "sleep"):
            cam.line([(ex - 4 * s, ey), (ex + 4 * s, ey)], fill=C_INK, width=2.0)
        else:
            cam.ellipse((ex - 3.8 * s, ey - 3.6 * s, ex + 3.8 * s, ey + 3.6 * s), fill=C_WHITE, outline=C_INK, width=1.4)
            cam.circle(ex + 1.2 * s * f_dir, ey, 2.2 * s, fill=C_INK)
            cam.circle(ex + 0.4 * s * f_dir, ey - 1.0 * s, 0.8 * s, fill=C_WHITE)

        if role in ("mak", "exec"):
            g_col = C_GOLD if role == "mak" else C_INK
            cam.circle(ex, ey, 6.2 * s, fill=None, outline=g_col, width=1.6)
            cam.line([(ex - 6.2 * s * f_dir, ey), (head_cx - 5 * s * f_dir, ey - 2 * s)], fill=g_col, width=1.5)

        # Profile Mouth & Chin Goatee
        mx = head_cx + 12 * s * f_dir
        my = head_cy + 13 * s
        if speaking > 0.12:
            cam.ellipse((mx - 4 * s, my - 3 * s, mx + 4 * s, my + 3 * s), fill=(128, 62, 58), outline=C_INK, width=1.5)
        elif mood in ("sad", "tired", "worried", "tearful"):
            cam.line([(mx - 3 * s * f_dir, my + 2 * s), (mx + 4 * s * f_dir, my)], fill=C_INK, width=1.8)
        else:
            cam.line([(mx - 3 * s * f_dir, my - 1 * s), (mx + 4 * s * f_dir, my + 1 * s)], fill=C_INK, width=1.8)

        if role == "amir":
            gx = head_cx + 13 * s * f_dir
            cam.ellipse((gx - 5 * s, head_cy + 17 * s, gx + 5 * s, head_cy + 25 * s), fill=HAIR_DARK, outline=None)

    else:
        # FRONT OR THREE-QUARTER (3/4) HEAD VIEW
        shift_face = 5.5 * s * f_dir if is_3q else 0.0
        if role in ("mak", "salma"):
            hijab_col = (224, 208, 186) if role == "mak" else (196, 182, 210)
            cam.ellipse((head_cx - 27 * s, head_cy - 31 * s, head_cx + 27 * s, head_cy + 27 * s), fill=hijab_col, outline=C_INK, width=2.2)
        else:
            cam.ellipse((head_cx - 24 * s, head_cy - 30 * s, head_cx + 24 * s, head_cy + 14 * s), fill=hair_col, outline=C_INK, width=2.0)

        # Ears: both ears in front view; only trailing near ear in 3/4 view
        if role not in ("mak", "salma"):
            cam.ellipse((head_cx - 21 * s * f_dir - 5 * s, head_cy - 5 * s, head_cx - 21 * s * f_dir + 5 * s, head_cy + 9 * s), fill=skin, outline=C_INK, width=1.8)
            if is_front:
                cam.ellipse((head_cx + 21 * s * f_dir - 5 * s, head_cy - 5 * s, head_cx + 21 * s * f_dir + 5 * s, head_cy + 9 * s), fill=skin, outline=C_INK, width=1.8)

        hw_head = 19.5 * s if is_3q else 21 * s
        cam.rect((head_cx - hw_head, head_cy - 23 * s, head_cx + hw_head, head_cy + 23 * s), fill=skin, outline=C_INK, width=2.2, radius=17)
        # Cheek blush shifted with face orientation
        cam.ellipse((head_cx + shift_face - 15 * s, head_cy + 2 * s, head_cx + shift_face - 6 * s, head_cy + 8 * s), fill=skin_sh, outline=None)
        cam.ellipse((head_cx + shift_face + 6 * s, head_cy + 2 * s, head_cx + shift_face + 15 * s, head_cy + 8 * s), fill=skin_sh, outline=None)

        if role == "abah":
            cam.pieslice((head_cx - 22 * s, head_cy - 32 * s, head_cx + 22 * s, head_cy - 4 * s), start=180, end=360, fill=C_WHITE, outline=C_INK, width=2.0)
            cam.line([(head_cx - 21 * s, head_cy - 17 * s), (head_cx + 21 * s, head_cy - 17 * s)], fill=C_GOLD, width=2.0)
        elif role in ("amir", "exec"):
            cam.pieslice((head_cx - 22 * s, head_cy - 32 * s, head_cx + 23 * s, head_cy - 4 * s), start=175, end=365, fill=hair_col, outline=C_INK, width=2.0)
            cam.arc((head_cx - 11 * s, head_cy - 27 * s, head_cx + 11 * s, head_cy - 15 * s), start=200, end=330, fill=(78, 72, 68), width=1.8)

        ex_l = head_cx + shift_face - 7.5 * s
        ex_r = head_cx + shift_face + 7.5 * s
        ey = head_cy - 4 * s
        brow_tilt = -2.5 * s if mood in ("sad", "tired", "tearful") else (-1.0 * s if mood == "worried" else 0.0)
        cam.line([(ex_l - 4.5 * s, ey - 8 * s - brow_tilt), (ex_l + 4.5 * s, ey - 9 * s + brow_tilt)], fill=hair_col, width=2.4)
        cam.line([(ex_r - 4.5 * s, ey - 9 * s + brow_tilt), (ex_r + 4.5 * s, ey - 8 * s - brow_tilt)], fill=hair_col, width=2.4)

        if blink or pose in ("sigh", "sleep"):
            cam.line([(ex_l - 4 * s, ey), (ex_l + 4 * s, ey)], fill=C_INK, width=2.0)
            cam.line([(ex_r - 4 * s, ey), (ex_r + 4 * s, ey)], fill=C_INK, width=2.0)
        else:
            for ex in (ex_l, ex_r):
                cam.ellipse((ex - 4.0 * s, ey - 3.5 * s, ex + 4.0 * s, ey + 3.5 * s), fill=C_WHITE, outline=C_INK, width=1.4)
                cam.circle(ex + 0.6 * s * f_dir, ey, 2.2 * s, fill=C_INK)
                cam.circle(ex - 0.5 * s, ey - 1.0 * s, 0.85 * s, fill=C_WHITE)

        if tear > 0.05:
            ty_off = (tear % 1.0) * 8.0 * s
            cam.circle(ex_r + 3 * s, ey + 4 * s + ty_off, 2.6 * s, fill=(130, 200, 235), outline=C_TEAL, width=1.0)

        if role in ("mak", "exec"):
            g_col = C_GOLD if role == "mak" else C_INK
            cam.circle(ex_l, ey, 6.2 * s, fill=None, outline=g_col, width=1.6)
            cam.circle(ex_r, ey, 6.2 * s, fill=None, outline=g_col, width=1.6)
            cam.line([(ex_l + 6.2 * s, ey), (ex_r - 6.2 * s, ey)], fill=g_col, width=1.5)

        nx = head_cx + shift_face + 1.5 * s * f_dir
        cam.line([(nx, ey + 2 * s), (nx + 2.5 * s * f_dir, ey + 9 * s), (nx - 1 * s * f_dir, ey + 10 * s)], fill=skin_sh, width=1.8)

        my = head_cy + 12 * s
        if speaking > 0.12:
            mh = max(2.0, speaking * 6.5) * s
            cam.ellipse((nx - 4.5 * s, my - mh * 0.5, nx + 4.5 * s, my + mh * 0.5), fill=(128, 62, 58), outline=C_INK, width=1.5)
        elif mood in ("sad", "tired", "worried", "tearful"):
            cam.arc((nx - 5.5 * s, my - 1 * s, nx + 5.5 * s, my + 6 * s), start=195, end=345, fill=C_INK, width=1.8)
        else:
            cam.arc((nx - 5.5 * s, my - 4 * s, nx + 5.5 * s, my + 4 * s), start=15, end=165, fill=C_INK, width=1.8)

        if role == "amir":
            cam.pieslice((nx - 6 * s, head_cy + 16 * s, nx + 6 * s, head_cy + 24 * s), start=0, end=180, fill=HAIR_DARK, outline=None)
        elif role == "abah":
            cam.arc((nx - 7 * s, my - 5 * s, nx + 7 * s, my + 2 * s), start=190, end=350, fill=HAIR_SILVER, width=3.0)

    # 5. PROPS HELD IN HANDS (Box, Phone) & NEAR/FRONT ARM
    if pose == "carry_box":
        bx, by = sh_x + 38 * s * f_dir, sh_y + 36 * s
        cam.rect((bx - 34 * s, by - 28 * s, bx + 34 * s, by + 26 * s), fill=(198, 154, 106), outline=C_INK, width=2.4, radius=4)
        cam.line([(bx - 34 * s, by - 2 * s), (bx + 34 * s, by - 2 * s)], fill=(158, 116, 72), width=2.0)
        cam.rect((bx - 12 * s, by - 28 * s, bx + 12 * s, by - 12 * s), fill=(228, 214, 188), outline=C_INK, width=1.4)

    elb_front = solve_ik(sh_front, hand_front, ua_l, fa_l, mode="elbow", f_dir=f_dir)
    cam.capsule(sh_front, elb_front, 20 * s, 17 * s, shirt)
    cam.capsule(elb_front, hand_front, 17 * s, 14 * s, shirt)
    cam.circle(hand_front[0], hand_front[1], 7.5 * s, fill=skin, outline=C_INK, width=1.8)

    if pose in ("dua_stand", "dua_sit") and not is_back:
        cam.poly([
            (hand_front[0] - 4 * s, hand_front[1] + 4 * s),
            (hand_front[0] + 12 * s * f_dir, hand_front[1] - 10 * s),
            (hand_front[0] + 15 * s * f_dir, hand_front[1] - 4 * s),
            (hand_front[0] + 2 * s, hand_front[1] + 6 * s),
        ], fill=skin, outline=C_INK, width=1.6)

    if pose in ("phone_look", "phone_call") and not is_back:
        px = hand_front[0] + (4 * s * f_dir if pose == "phone_look" else -2 * s * f_dir)
        py = hand_front[1] - 8 * s
        cam.rect((px - 7 * s, py - 14 * s, px + 7 * s, py + 14 * s), fill=(42, 52, 64), outline=C_INK, width=1.8, radius=3)
        cam.rect((px - 5 * s, py - 11 * s, px + 5 * s, py + 11 * s), fill=(168, 214, 232), outline=None)

# ==============================================================================
# DETAILED VECTOR PROPS & ENVIRONMENTAL ELEMENTS
# ==============================================================================

def draw_potted_plant(cam: CamCanvas, x: float, y: float, s: float = 1.0, t: float = 0.0, pot_col=C_TERRA):
    """Lush indoor/outdoor potted plant with swaying leaves."""
    cam.ellipse((x - 24 * s, y - 4 * s, x + 24 * s, y + 5 * s), fill=(38, 54, 69, 36), outline=None)
    # Leaf stems
    for i, ang_base in enumerate([-38, -18, 0, 20, 40]):
        sway = math.sin(t * 1.4 + i * 0.9) * 3.5
        ang = math.radians(ang_base + sway)
        lx = x + math.sin(ang) * 44 * s
        ly = y - 26 * s - math.cos(ang) * 46 * s
        cam.line([(x, y - 24 * s), (lx, ly)], fill=C_SAGE_DARK, width=2.5 * s)
        col_l = C_SAGE if i % 2 == 0 else C_TEAL
        cam.ellipse((lx - 13 * s, ly - 18 * s, lx + 13 * s, ly + 8 * s), fill=col_l, outline=C_INK, width=1.6)
    # Terracotta pot
    cam.poly([
        (x - 20 * s, y - 28 * s),
        (x + 20 * s, y - 28 * s),
        (x + 15 * s, y),
        (x - 15 * s, y),
    ], fill=pot_col, outline=C_INK, width=2.0)
    cam.rect((x - 23 * s, y - 34 * s, x + 23 * s, y - 26 * s), fill=pot_col, outline=C_INK, width=2.0, radius=3)

def draw_tree(cam: CamCanvas, x: float, y: float, s: float = 1.0, t: float = 0.0, kind: str = "round"):
    sway = math.sin(t * 1.1 + x * 0.01) * 4.0 * s
    cam.ellipse((x - 45 * s, y - 5 * s, x + 45 * s, y + 6 * s), fill=(38, 54, 69, 32), outline=None)
    # Trunk & branches
    cam.poly([
        (x - 12 * s, y),
        (x - 7 * s + sway * 0.4, y - 105 * s),
        (x + 7 * s + sway * 0.4, y - 105 * s),
        (x + 13 * s, y),
    ], fill=(122, 96, 74), outline=C_INK, width=2.2)
    if kind == "palm":
        # Coconut palm fronds for kampung scene
        top_x, top_y = x + sway * 0.6, y - 105 * s
        for f_ang in [-65, -35, -10, 15, 42, 68]:
            rad = math.radians(f_ang + sway * 0.8)
            fx = top_x + math.cos(rad) * 68 * s
            fy = top_y + math.sin(rad) * 38 * s
            cam.poly([(top_x, top_y), ((top_x + fx) * 0.5, top_y - 18 * s), (fx, fy)], fill=C_SAGE, outline=C_INK, width=1.8)
    else:
        # Layered foliage canopy with highlight
        cam.circle(x - 28 * s + sway, y - 110 * s, 38 * s, fill=C_SAGE_DARK, outline=C_INK, width=2.0)
        cam.circle(x + 28 * s + sway, y - 112 * s, 36 * s, fill=C_SAGE_DARK, outline=C_INK, width=2.0)
        cam.circle(x + sway, y - 134 * s, 46 * s, fill=C_SAGE, outline=C_INK, width=2.2)
        cam.arc((x - 28 * s + sway, y - 165 * s, x + 28 * s + sway, y - 120 * s), start=200, end=340, fill=C_SAGE_LIGHT, width=3.0)

def draw_bird(cam: CamCanvas, x: float, y: float, s: float = 1.0, t: float = 0.0):
    flap = math.sin(t * 7.5 + x * 0.03) * 8.0 * s
    cam.line([(x - 12 * s, y - flap), (x, y), (x + 12 * s, y - flap)], fill=C_INK, width=2.2)

def draw_lantern(cam: CamCanvas, x: float, y: float, s: float = 1.0, t: float = 0.0, lit: bool = True):
    if lit:
        r_glow = (44 + math.sin(t * 3.2) * 4) * s
        cam.circle(x, y, r_glow, fill=(246, 218, 154, 65), outline=None)
    cam.line([(x, y - 42 * s), (x, y - 22 * s)], fill=C_INK, width=2.2)
    cam.poly([
        (x - 14 * s, y - 22 * s),
        (x + 14 * s, y - 22 * s),
        (x + 20 * s, y + 16 * s),
        (x - 20 * s, y + 16 * s),
    ], fill=(52, 72, 76), outline=C_INK, width=2.0)
    cam.rect((x - 10 * s, y - 16 * s, x + 10 * s, y + 11 * s), fill=C_GOLD_LIGHT if lit else C_MUTED, outline=C_INK, width=1.4, radius=3)
    cam.rect((x - 22 * s, y + 14 * s, x + 22 * s, y + 20 * s), fill=C_GOLD, outline=C_INK, width=1.8, radius=3)

def draw_rehal_quran(cam: CamCanvas, x: float, y: float, s: float = 1.0):
    """Raised wooden reading table + X-shaped rehal + open Mushaf Al-Quran (never on the floor!)."""
    # Raised table
    cam.rect((x - 58 * s, y, x + 58 * s, y + 10 * s), fill=(158, 122, 84), outline=C_INK, width=2.0, radius=4)
    cam.rect((x - 48 * s, y + 10 * s, x - 38 * s, y + 68 * s), fill=(132, 98, 66), outline=C_INK, width=1.8)
    cam.rect((x + 38 * s, y + 10 * s, x + 48 * s, y + 68 * s), fill=(132, 98, 66), outline=C_INK, width=1.8)
    # Rehal stand
    cam.line([(x - 26 * s, y), (x + 22 * s, y - 22 * s)], fill=(122, 86, 54), width=3.5)
    cam.line([(x + 26 * s, y), (x - 22 * s, y - 22 * s)], fill=(122, 86, 54), width=3.5)
    # Open Mushaf pages
    cam.poly([
        (x, y - 14 * s),
        (x - 34 * s, y - 26 * s),
        (x - 34 * s, y - 6 * s),
        (x, y + 2 * s),
        (x + 34 * s, y - 6 * s),
        (x + 34 * s, y - 26 * s),
    ], fill=C_CREAM, outline=C_INK, width=2.0)
    cam.line([(x, y - 14 * s), (x, y + 2 * s)], fill=C_GOLD, width=2.0)

def draw_kapcai_detailed(cam: CamCanvas, cx: float, cy: float, s: float = 1.0, t: float = 0.0, moving: bool = True, with_rider: bool = True):
    """Detailed Malaysian kapcai motorcycle with front basket, side mirror, key slot, scratched seat & exhaust."""
    vib = math.sin(t * 40.0) * 1.4 * s if moving else 0.0
    y0 = cy + vib
    cam.ellipse((cx - 95 * s, cy + 44 * s, cx + 95 * s, cy + 58 * s), fill=(38, 54, 69, 48), outline=None)

    # Wheels rotating with road distance
    ang_deg = (t * 340.0) % 360.0 if moving else 15.0
    for wx in (cx - 58 * s, cx + 62 * s):
        wy = cy + 20 * s
        cam.circle(wx, wy, 29 * s, fill=(48, 54, 60), outline=C_INK, width=3.0)
        cam.circle(wx, wy, 19 * s, fill=(224, 220, 210), outline=C_INK, width=1.8)
        for sp in range(4):
            r_a = math.radians(ang_deg + sp * 45.0)
            dx, dy = math.cos(r_a) * 18 * s, math.sin(r_a) * 18 * s
            cam.line([(wx - dx, wy - dy), (wx + dx, wy + dy)], fill=C_MUTED, width=1.6)
        cam.circle(wx, wy, 5 * s, fill=C_GOLD, outline=C_INK, width=1.4)

    # Exhaust pipe & smoke puffs
    cam.rect((cx - 82 * s, y0 + 12 * s, cx - 6 * s, y0 + 21 * s), fill=(156, 164, 172), outline=C_INK, width=1.8, radius=4)
    if moving:
        for p_i in range(3):
            ph = (t * 2.4 + p_i * 0.33) % 1.0
            px = cx - (90 + ph * 48) * s
            py = y0 + (14 - ph * 16) * s
            pr = (5 + ph * 9) * s
            cam.circle(px, py, pr, fill=(225, 222, 214, int(190 * (1.0 - ph))), outline=None)

    # Chassis & front fairing
    cam.poly([
        (cx - 54 * s, y0 + 8 * s),
        (cx - 12 * s, y0 - 16 * s),
        (cx + 30 * s, y0 - 14 * s),
        (cx + 54 * s, y0 - 44 * s),
        (cx + 68 * s, y0 - 40 * s),
        (cx + 46 * s, y0 + 16 * s),
    ], fill=(68, 108, 132), outline=C_INK, width=2.4)
    # Front wire basket (raga motor)
    cam.rect((cx + 58 * s, y0 - 36 * s, cx + 78 * s, y0 - 14 * s), fill=(180, 188, 196, 160), outline=C_INK, width=1.8, radius=3)
    # Scratched black seat
    cam.rect((cx - 48 * s, y0 - 26 * s, cx + 10 * s, y0 - 10 * s), fill=(44, 48, 54), outline=C_INK, width=2.0, radius=7)
    cam.line([(cx - 38 * s, y0 - 22 * s), (cx - 24 * s, y0 - 14 * s)], fill=(176, 180, 186), width=1.8)
    cam.line([(cx - 22 * s, y0 - 23 * s), (cx - 10 * s, y0 - 15 * s)], fill=(176, 180, 186), width=1.8)

    # Handlebar, ignition key slot, side mirror & headlight
    cam.line([(cx + 42 * s, y0 - 58 * s), (cx + 58 * s, y0 - 40 * s)], fill=C_INK, width=3.5)
    # Side mirror
    cam.line([(cx + 45 * s, y0 - 58 * s), (cx + 40 * s, y0 - 72 * s)], fill=C_INK, width=2.0)
    cam.ellipse((cx + 33 * s, y0 - 78 * s, cx + 47 * s, y0 - 68 * s), fill=C_SKY, outline=C_INK, width=1.8)
    # Ignition key with red tag
    cam.circle(cx + 44 * s, y0 - 34 * s, 3.5 * s, fill=C_GOLD, outline=C_INK, width=1.2)
    cam.rect((cx + 38 * s, y0 - 30 * s, cx + 44 * s, y0 - 21 * s), fill=C_TERRA, outline=C_INK, width=1.0, radius=2)
    # Headlight
    cam.pieslice((cx + 52 * s, y0 - 56 * s, cx + 76 * s, y0 - 36 * s), start=-45, end=55, fill=C_GOLD_LIGHT, outline=C_INK, width=2.0)

    if with_rider:
        # Rider legs, torso, arm & scratched helmet
        hip = (cx - 18 * s, y0 - 24 * s)
        knee = (cx + 12 * s, y0 - 6 * s)
        ankle = (cx + 8 * s, y0 + 22 * s)
        cam.capsule(hip, knee, 22 * s, 18 * s, C_NAVY)
        cam.capsule(knee, ankle, 18 * s, 14 * s, C_NAVY)
        cam.rect((cx + 2 * s, y0 + 18 * s, cx + 22 * s, y0 + 27 * s), fill=(68, 58, 54), outline=C_INK, width=1.8, radius=3)
        # Torso
        sh = (cx - 10 * s, y0 - 82 * s)
        cam.capsule(hip, sh, 32 * s, 34 * s, C_TEAL)
        # Arm gripping handlebar
        elb = (cx + 14 * s, y0 - 58 * s)
        hand = (cx + 44 * s, y0 - 56 * s)
        cam.capsule(sh, elb, 17 * s, 15 * s, C_TEAL)
        cam.capsule(elb, hand, 15 * s, 13 * s, C_TEAL)
        cam.circle(hand[0], hand[1], 7 * s, fill=SKIN_AMIR, outline=C_INK, width=1.6)
        # Head & scratched helmet
        hx, hy = cx - 6 * s, y0 - 110 * s
        cam.circle(hx, hy, 22 * s, fill=(78, 118, 144), outline=C_INK, width=2.4)
        cam.pieslice((hx - 22 * s, hy - 20 * s, hx + 24 * s, hy + 18 * s), start=-30, end=38, fill=(210, 232, 242), outline=C_INK, width=1.8)
        cam.line([(hx - 12 * s, hy - 10 * s), (hx - 2 * s, hy - 2 * s)], fill=C_CREAM, width=1.8)
        cam.line([(hx - 7 * s, hy - 14 * s), (hx + 3 * s, hy - 6 * s)], fill=C_CREAM, width=1.8)

def draw_luxury_car(cam: CamCanvas, x: float, y: float, s: float = 1.0, col=(48, 62, 78)):
    """Detailed glossy SUV / Executive Sedan with alloy wheels, grille, headlights, and window reflections."""
    cam.ellipse((x - 15 * s, y + 62 * s, x + 275 * s, y + 78 * s), fill=(38, 54, 69, 45), outline=None)
    # Cabin roof & windows
    cam.poly([
        (x + 36 * s, y + 4 * s),
        (x + 78 * s, y - 44 * s),
        (x + 206 * s, y - 44 * s),
        (x + 242 * s, y + 4 * s),
    ], fill=col, outline=C_INK, width=2.4)
    cam.poly([
        (x + 48 * s, y + 2 * s),
        (x + 82 * s, y - 38 * s),
        (x + 138 * s, y - 38 * s),
        (x + 138 * s, y + 2 * s),
    ], fill=(186, 214, 230), outline=C_INK, width=1.8)
    cam.poly([
        (x + 146 * s, y + 2 * s),
        (x + 146 * s, y - 38 * s),
        (x + 200 * s, y - 38 * s),
        (x + 230 * s, y + 2 * s),
    ], fill=(186, 214, 230), outline=C_INK, width=1.8)
    # Glossy window shine lines
    cam.line([(x + 88 * s, y - 32 * s), (x + 68 * s, y - 4 * s)], fill=C_WHITE, width=2.5)
    cam.line([(x + 178 * s, y - 32 * s), (x + 158 * s, y - 4 * s)], fill=C_WHITE, width=2.5)
    # Lower body chassis
    cam.rect((x, y, x + 265 * s, y + 54 * s), fill=col, outline=C_INK, width=2.4, radius=14)
    # Chrome door trim & handles
    cam.line([(x + 24 * s, y + 26 * s), (x + 240 * s, y + 26 * s)], fill=C_GOLD, width=2.0)
    cam.rect((x + 248 * s, y + 10 * s, x + 264 * s, y + 24 * s), fill=C_GOLD_LIGHT, outline=C_INK, width=1.6, radius=4)
    # Alloy wheels
    for wx in (x + 52 * s, x + 212 * s):
        wy = y + 50 * s
        cam.circle(wx, wy, 24 * s, fill=(34, 38, 44), outline=C_INK, width=2.5)
        cam.circle(wx, wy, 14 * s, fill=(212, 216, 222), outline=C_GOLD, width=1.8)
        cam.circle(wx, wy, 4 * s, fill=C_INK, outline=None)

# ==============================================================================
# FULL SUBTITLES & WAVEFORM (BOTTOM SAFE AREA ONLY)
# ==============================================================================

SUBTITLES = [
    (0.10, 3.20, "Aku pandang tali lanyard di leher."),
    (3.40, 6.50, "Warnanya sudah lama pudar."),
    (6.80, 10.20, "Klip plastiknya pun sudah retak."),
    (10.70, 13.10, "Hari ini hari gaji."),
    (13.25, 16.20, "Hari yang patutnya meriah bagi ramai orang."),
    (16.50, 22.10, "Tapi untuk orang biasa macam aku, tak selalu begitu."),
    (22.50, 24.60, "Gaji masuk pagi tadi."),
    (24.90, 29.10, "Tengah hari, separuh daripadanya sudah selamat keluar."),
    (29.30, 32.70, "Bayar sewa bilik. Bayar ansuran motor."),
    (33.00, 37.00, "Selesai hutang kawan yang dipinjam pertengahan bulan lepas."),
    (37.80, 42.50, "Dan yang wajib, hantar sedikit ke kampung untuk Mak dan Abah."),
    (42.90, 46.20, "Baki di tangan, cukup untuk bernafas."),
    (47.20, 50.90, "Bernafas perlahan-lahan untuk tiga puluh hari ke depan."),
    (51.20, 54.00, "Aku bersandar pada dinding tepi bank."),
    (54.30, 59.10, "Matahari di luar sana tegak di atas kepala. Panas merelit."),
    (59.70, 61.60, "Bahu aku jatuh sedikit."),
    (61.90, 65.10, "Ada keluhan kecil terlepas dari celah bibir."),
    (65.40, 67.10, "Penat."),
    (67.50, 71.20, "Kadang-kadang terfikir juga di sudut hati."),
    (71.60, 74.30, "Kenapa hidup orang lain nampak sangat mudah?"),
    (74.50, 79.30, "Kerja di pejabat berhawa dingin. Gaji besar, kereta besar."),
    (79.60, 82.20, "Hujung minggu makan di tempat mewah."),
    (82.50, 86.90, "Sedangkan aku di sini, hari-hari bergelut dengan jalan sesak."),
    (87.10, 89.80, "Hujan basah, panas berpeluh."),
    (90.00, 93.30, "Kerja angkat barang dan susun fail dari pagi ke petang."),
    (93.50, 96.40, "Tapi poket tetap nipis."),
    (96.70, 102.30, "Tiba-tiba rasa sunyi merayap masuk. Sunyi di tengah bandar yang bising."),
    (103.00, 108.80, "Kalau kau pernah rasa macam ni, tak apa. Normal untuk rasa tertinggal."),
    (109.10, 116.30, "Kita manusia biasa. Hati kita diperbuat daripada tanah yang rapuh, bukan besi yang kebal."),
    (116.80, 122.60, "Aku tarik nafas panjang. Cuba halau rasa gelap yang mula meracun fikiran."),
    (122.90, 128.60, "Aku berjalan menuju ke motor lama aku. Tempat duduknya sudah calar sedikit."),
    (129.00, 135.10, "Aku sarung helmet yang calar-balar. Kunci dipulas. Enjin dihidupkan."),
    (135.60, 142.30, "Bunyi enjin kasar, tapi dia tetap hidup. Sama macam aku."),
    (142.60, 146.20, "Dalam perjalanan balik, jalan sangat sesak."),
    (146.50, 152.00, "Banyak kereta mewah di kiri dan kanan jalan. Berkilat. Selesa."),
    (152.60, 157.40, "Aku terselit di tengah-tengah. Kecil. Tidak kelihatan."),
    (158.50, 165.80, "Tapi masa itulah, aku terpandang tangan sendiri. Tangan yang menggenggam pemegang motor."),
    (166.00, 173.40, "Kulitnya gelap dimakan panas matahari. Ada parut kecil terkena minyak hitam. Kasar."),
    (174.50, 180.90, "Tangan ini mungkin tak pegang duit ribu-ribu, atau stereng kereta mahal."),
    (181.30, 188.30, "Tapi tangan ini tak pernah ambil hak orang. Tangan ini cari rezeki halal."),
    (189.00, 197.10, "Air mata tiba-tiba bergenang panas. Cepat-cepat aku lap dengan hujung lengan baju."),
    (197.90, 208.70, "Tuhan, Engkau Maha Melihat. Rupanya kita selalu salah kira tentang makna rezeki."),
    (209.50, 217.60, "Kita ingat rezeki itu cuma angka di dalam akaun bank. Kita lupa rezeki itu juga ketenangan."),
    (218.20, 226.40, "Ketenangan bila tidur malam tak fikir hutang haram. Bila suap nasi ke mulut, tahu ia suci."),
    (226.70, 235.60, "Ada orang tidur atas tilam empuk, tapi matanya celik sampai ke pagi mencari tenang."),
    (236.30, 243.20, "Ada orang tidur atas tilam nipis, tapi dengkurannya lena. Hatinya penuh rasa cukup."),
    (244.10, 250.60, "Gaji basic bukan bermaksud hidup kita gagal. Ia cuma bermaksud jalan kita berbeza."),
    (251.30, 257.70, "Tuhan tak pernah ukur kejayaan kita dengan slip gaji. Tuhan tak minta kita jadi kaya-raya."),
    (258.00, 265.10, "Tuhan cuma minta kita berusaha, jujur, dan sedar bahawa kita fakir kepada-Nya."),
    (265.40, 272.20, "Telefon bergetar dalam poket seluar. Aku berhenti di tepi jalan berteduh bawah pokok."),
    (272.60, 278.20, "Nama 'Mak' tertera di skrin retak. Aku tekan butang hijau."),
    (279.00, 288.80, "\"Assalamualaikum, abang. Duit abang hantar tadi dah masuk. Abang cukup ke belanja tu?\""),
    (291.00, 300.20, "Dada aku rasa sebak. Padahal yang aku hantar itu cuma secebis."),
    (300.80, 304.30, "Tapi bagi Mak, itu macam satu rahmat besar."),
    (304.50, 310.30, "\"Cukup, Mak. Rezeki abang bulan ni lebih sikit.\" Aku terpaksa berbohong sunat."),
    (310.70, 315.00, "Biarlah perut aku lapar sedikit, asalkan hati Mak tenang di kampung."),
    (315.90, 323.00, "\"Alhamdulillah. Mak sentiasa doakan abang. Biar tak banyak, asalkan berkat. Kerja baik-baik ya, nak.\""),
    (323.50, 330.30, "Talian dimatikan. Rasa berat di dada tadi tiba-tiba hilang, terganti dengan rasa hangat."),
    (330.80, 340.90, "Bila penat, itu tanda kita sedang berjuang. Peluh mencari rezeki halal itu saksi di akhirat nanti."),
    (341.20, 347.80, "Aku singgah di kedai makan tepi jalan. Pesan teh O ais satu dan sebungkus nasi lemak kosong."),
    (348.40, 354.20, "Duduk di meja bucu. Kipas siling lama berbunyi pusing lambat di atas kepala."),
    (354.40, 357.60, "Krek... krek... krek..."),
    (357.80, 363.80, "Aku buka bungkusan daun pisang itu. Wangi bau pandan dan sambal naik ke hidung."),
    (364.40, 368.80, "Aku suap nasi perlahan-lahan. Hirup teh O ais yang sejuk."),
    (369.30, 375.50, "Alhamdulillah. Nikmat yang sangat murah, tapi rasanya pada hari ini sangat mahal."),
    (376.20, 383.30, "Mungkin bulan ini aku tak dapat beli baju baru. Mungkin terpaksa ikat perut lagi."),
    (383.70, 391.80, "Tapi aku sihat. Aku masih boleh bernafas. Mak dan Abah di kampung masih mendoakan aku."),
    (392.10, 395.80, "Itu kekayaan yang orang paling kaya pun tak boleh beli."),
    (396.10, 405.50, "Kaya itu bukan bila kita ada semua benda, tapi bila kita pandai menghargai apa yang ada."),
    (405.80, 417.00, "Biarlah dunia pandang kita biasa-biasa, asalkan di mata penduduk langit nama kita harum dengan doa orang tua."),
    (417.40, 424.40, "Kalau hari ini kau rasa penat cari duit, rehatlah sekejap. Tarik nafas. Kau dah buat yang terbaik."),
    (424.70, 435.30, "Jangan hukum diri sendiri. Dunia tempat untuk kita diuji; syurga nanti tempat kita berehat selamanya."),
    (435.60, 443.00, "Selagi esok matahari masih terbit, kita teruskan langkah. Satu demi satu. Perlahan pun tidak mengapa."),
    (443.10, 452.70, "Yang penting, tangan ini terus memegang sumber yang halal, dan hati terus bergantung pada Tuhan."),
    (453.00, 462.50, "\"Ya Allah, ampunkanlah kami yang selalu mengeluh apabila diuji, dan sering buta menilai nikmat-Mu.\""),
    (463.10, 473.20, "\"Luaskanlah rezeki buat saudara kami yang bergelut mencari sesuap nasi, dan tenangkanlah jiwa mereka.\""),
    (474.00, 489.20, "\"Jadikanlah setiap titis peluh lelah kami penggugur dosa, dan berkatilah rezeki kami hingga ke syurga. Amin.\""),
    (489.70, 497.10, "Daripada al-Miqdam RA, daripada Rasulullah SAW, Baginda bersabda:"),
    (497.50, 506.20, "\"Tiada siapa yang memakan satu makanan yang lebih baik daripada hasil kerja tangannya sendiri.\""),
    (506.60, 516.67, "\"Sesungguhnya Nabi Allah Daud AS makan daripada hasil kerja tangannya sendiri.\" (Al-Bukhari, 2072)")
]

@lru_cache(maxsize=128)
def render_subtitle_bar(text: str):
    bar = Image.new("RGBA", (1060, 72), (0, 0, 0, 0))
    d = ImageDraw.Draw(bar)
    d.rounded_rectangle((0, 0, 1059, 71), radius=16, fill=(38, 54, 69, 232), outline=(218, 176, 98, 195), width=2)
    f = get_font("sans", 22)
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textbbox((0, 0), test, font=f)[2] <= 980:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    lines = lines[:2]
    if len(lines) == 1:
        d.text((530, 36), lines[0], font=f, fill=C_CREAM, anchor="mm")
    else:
        d.text((530, 22), lines[0], font=f, fill=C_CREAM, anchor="mm")
        d.text((530, 50), lines[1], font=f, fill=C_CREAM, anchor="mm")
    return bar

@lru_cache(maxsize=8)
def make_gradient_bg(top_rgb, bot_rgb):
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    a = np.array(top_rgb, dtype=np.float32)[None, None, :]
    b = np.array(bot_rgb, dtype=np.float32)[None, None, :]
    arr = np.broadcast_to(np.clip(a * (1.0 - y) + b * y, 0, 255).astype(np.uint8), (H, W, 3)).copy()
    return Image.fromarray(arr, "RGB")

def draw_waveform_widget(d: ImageDraw.ImageDraw, frame_idx: int):
    wx, wy, ww, wh = 26, 625, 166, 70
    d.rounded_rectangle((wx, wy, wx + ww, wy + wh), radius=14, fill=(38, 54, 69, 228), outline=C_GOLD, width=2)
    n_bars = 24
    for b in range(n_bars):
        sample_idx = min(TOTAL_FRAMES - 1, max(0, frame_idx + (b - 12)))
        amp = float(NORM_RMS[sample_idx])
        mod = 0.75 + 0.25 * math.sin(frame_idx * 0.25 + b * 0.55)
        bh = int(max(4, min(46, amp * 50.0 * mod)))
        bx = wx + 11 + b * 6
        by0 = wy + 35 - bh // 2
        by1 = wy + 35 + bh // 2
        col = C_GOLD if amp > 0.30 else C_TEAL_LIGHT
        d.line((bx, by0, bx, by1), fill=col, width=3)

# ==============================================================================
# 16 PURE VECTOR STORYTELLING SCENES WITH DYNAMIC CAMERA ZOOMS
# ==============================================================================

def render_frame(frame_idx: int) -> Image.Image:
    t = frame_idx / FPS
    speak_amp = float(NORM_RMS[min(TOTAL_FRAMES - 1, frame_idx)])

    # ------------------------------------------------------------------
    # S01 (0.0 - 10.5s): Koridor Pejabat & Zoom-In ke Tali Lanyard Retak
    # ------------------------------------------------------------------
    if t < 10.5:
        im = make_gradient_bg(C_CREAM, C_CREAM_DARK).copy()
        # Camera keyframes: starts medium-wide (640,340,1.0), zooms in to lanyard clip (640,295,2.45) at 3.5-7.8s, then pulls to Amir's face (640,220,1.85)
        z1 = smoothstep(1.2, 4.2, t)
        z2 = smoothstep(7.2, 9.8, t)
        cam_cx = 640.0
        cam_cy = lerp(lerp(330.0, 292.0, z1), 225.0, z2)
        cam_z = lerp(lerp(1.05, 2.45, z1), 1.80, z2)
        cam = CamCanvas(im, cam_cx, cam_cy, cam_z)

        # Corridor walls, wainscoting, floor, windows, clock, water dispenser, hand-trolley with boxes & plants
        cam.rect((-200, 490, 1480, 800), fill=C_SAND, outline=None)
        cam.line([(-200, 490), (1480, 490)], fill=C_INK, width=2.5)
        # Corridor windows with morning sunbeams
        for wx in (160, 960):
            cam.rect((wx, 120, wx + 180, 360), fill=C_SKY, outline=C_INK, width=3.0, radius=8)
            cam.line([(wx + 90, 120), (wx + 90, 360)], fill=C_INK, width=2.5)
            cam.line([(wx, 240), (wx + 180, 240)], fill=C_INK, width=2.5)
        # Wall clock (08:05)
        cam.circle(460, 155, 28, fill=C_WHITE, outline=C_INK, width=2.5)
        cam.line([(460, 155), (460, 136)], fill=C_INK, width=2.2)
        cam.line([(460, 155), (474, 162)], fill=C_TERRA, width=2.0)
        # Hand trolley with stacked boxes on left
        cam.rect((355, 385, 435, 490), fill=(198, 154, 106), outline=C_INK, width=2.2, radius=4)
        cam.rect((365, 325, 428, 385), fill=(212, 170, 122), outline=C_INK, width=2.2, radius=4)
        cam.circle(365, 490, 14, fill=C_INK, outline=C_GOLD, width=2.0)
        # Potted plants
        draw_potted_plant(cam, 240, 495, 1.05, t)
        draw_potted_plant(cam, 880, 495, 1.0, t + 1.0)
        # Protagonist Amir touching his faded lanyard with cracked plastic clip
        draw_character(cam, 640, 515, scale=1.22, t=t, role="amir", pose="touch_lanyard", mood="worried", view="three_quarter_right" if t < 6.8 else "front", lanyard=True)

    # ------------------------------------------------------------------
    # S02 (10.5 - 22.3s): Tepi Bank & Mesin ATM — Zoom-In ke Amir & Telefon
    # ------------------------------------------------------------------
    elif t < 22.3:
        lt = t - 10.5
        im = make_gradient_bg(C_SKY, C_CREAM).copy()
        # Camera zooms from wide street (640,350,1.0) into Amir looking at his phone (745,305,1.88)
        z = smoothstep(2.5, 8.5, lt)
        cam = CamCanvas(im, lerp(640.0, 735.0, z), lerp(350.0, 295.0, z), lerp(1.0, 1.88, z))

        # Sidewalk & road
        cam.rect((-200, 510, 1480, 800), fill=(208, 198, 180))
        cam.line([(-200, 510), (1480, 510)], fill=C_INK, width=2.5)
        # Bank building facade & ATM machine on left
        cam.rect((110, 95, 580, 510), fill=C_CREAM_DARK, outline=C_INK, width=3.0, radius=6)
        cam.rect((110, 95, 580, 155), fill=C_TEAL, outline=C_INK, width=2.5)
        cam.text(345, 125, "BANK SIMPANAN", size=22, kind="bold", fill=C_CREAM)
        # Glass doors & glowing ATM booth
        cam.rect((155, 210, 315, 510), fill=(188, 218, 232), outline=C_INK, width=2.5)
        cam.rect((365, 220, 515, 480), fill=(64, 82, 98), outline=C_INK, width=2.5, radius=8)
        cam.rect((390, 255, 490, 335), fill=(148, 218, 198), outline=C_INK, width=2.0, radius=4)
        cam.text(440, 238, "ATM 24 JAM", size=13, kind="bold", fill=C_GOLD_LIGHT)
        # Streetlamp, bollards & trees
        draw_tree(cam, 1040, 510, 1.05, t)
        draw_potted_plant(cam, 610, 512, 0.9, t)
        for bx in (220, 340, 560, 920):
            cam.rect((bx - 7, 468, bx + 7, 512), fill=C_NAVY, outline=C_INK, width=1.8, radius=3)
        # Amir standing outside bank checking salary on phone
        draw_character(cam, 455, 512, scale=0.92, t=t, role="exec", pose="stand", mood="calm", view="back", lanyard=False)
        draw_character(cam, 735, 522, scale=1.18, t=t, role="amir", pose="phone_look", mood="sad", facing=-1, view="three_quarter_left", lanyard=True)

    # ------------------------------------------------------------------
    # S03 (22.3 - 51.0s): Meja Bilik Sewa — Zoom-In ke Objek Komitmen & Wajah Amir
    # ------------------------------------------------------------------
    elif t < 51.0:
        lt = t - 22.3
        im = make_gradient_bg(C_CREAM, C_CREAM_DARK).copy()
        # Multi-target camera:
        # 22.3-28.5s: Medium shot of Amir at table (640,350,1.08)
        # 28.5-36.8s: Zoom in to Bill Envelopes & Motorcycle Key on table (690,415,2.15)
        # 36.8-42.8s: Pan/Zoom to Framed Mak & Abah Photo + Phone Transfer on right of table (835,395,2.20)
        # 42.8-51.0s: Zoom to Amir's face & remaining banknote (475,285,1.85)
        p1 = smoothstep(5.5, 7.5, lt)
        p2 = smoothstep(14.0, 16.0, lt)
        p3 = smoothstep(20.0, 22.5, lt)
        cx = lerp(lerp(lerp(640.0, 635.0, p1), 695.0, p2), 515.0, p3)
        cy = lerp(lerp(lerp(345.0, 385.0, p1), 375.0, p2), 295.0, p3)
        cz = lerp(lerp(lerp(1.08, 1.72, p1), 1.82, p2), 1.85, p3)
        cam = CamCanvas(im, cx, cy, cz)

        # Room interior: floor, window with curtains, wall calendar (30 Hari), standing fan
        cam.rect((-200, 505, 1480, 800), fill=(204, 188, 162))
        cam.line([(-200, 505), (1480, 505)], fill=C_INK, width=2.5)
        # Window
        cam.rect((150, 95, 360, 330), fill=C_SKY, outline=C_INK, width=2.5, radius=6)
        cam.line([(255, 95), (255, 330)], fill=C_INK, width=2.0)
        cam.line([(150, 212), (360, 212)], fill=C_INK, width=2.0)
        # Wall Calendar ("30 HARI")
        cam.rect((965, 115, 1085, 245), fill=C_WHITE, outline=C_INK, width=2.2, radius=6)
        cam.rect((965, 115, 1085, 152), fill=C_TERRA, outline=C_INK, width=2.0)
        cam.text(1025, 134, "BULAN INI", size=12, kind="bold", fill=C_WHITE)
        cam.text(1025, 195, "30 HARI", size=20, kind="bold", fill=C_INK)

        # Amir seated at chair behind wooden desk
        cam.rect((415, 360, 520, 515), fill=(138, 102, 68), outline=C_INK, width=2.2, radius=4)
        draw_character(cam, 465, 515, scale=1.15, t=t, role="amir", pose="sit_table", mood="worried", facing=1, lanyard=True)

        # Wooden Desk in foreground
        cam.rect((520, 438, 960, 458), fill=(168, 122, 80), outline=C_INK, width=2.5, radius=5)
        cam.rect((545, 458, 568, 535), fill=(138, 98, 62), outline=C_INK, width=2.0)
        cam.rect((912, 458, 935, 535), fill=(138, 98, 62), outline=C_INK, width=2.0)

        # Detailed Props on the Table:
        # 1) Rent envelope & house key (Sewa Bilik)
        cam.rect((565, 412, 650, 438), fill=C_CREAM, outline=C_INK, width=1.8, radius=3)
        cam.line([(565, 412), (607, 426), (650, 412)], fill=C_TERRA, width=1.6)
        cam.text(607, 431, "SEWA BILIK", size=8, kind="bold", fill=C_INK)
        # 2) Motorcycle key & installment slip (Ansuran Motor)
        cam.rect((665, 415, 742, 438), fill=(235, 242, 248), outline=C_INK, width=1.8, radius=3)
        cam.circle(685, 405, 7, fill=C_GOLD, outline=C_INK, width=1.6)
        cam.line([(692, 405), (712, 405)], fill=C_MUTED, width=2.5)
        cam.text(704, 428, "MOTOR", size=8, kind="bold", fill=C_TEAL)
        # 3) Friend debt notebook & pen (Hutang Kawan)
        cam.rect((755, 408, 818, 438), fill=C_SAGE_LIGHT, outline=C_INK, width=1.8, radius=3)
        cam.text(786, 424, "HUTANG", size=8, kind="bold", fill=C_INK)
        # 4) Framed photo of Mak & Abah + Smartphone transfer on right of table
        cam.rect((838, 362, 912, 438), fill=C_GOLD, outline=C_INK, width=2.2, radius=6)
        cam.rect((846, 370, 904, 430), fill=C_PEACH, outline=C_INK, width=1.4)
        # Mini portrait of Mak & Abah inside frame
        cam.circle(864, 396, 11, fill=C_WHITE, outline=C_INK, width=1.4)
        cam.circle(886, 398, 11, fill=(224, 208, 186), outline=C_INK, width=1.4)
        cam.text(875, 421, "MAK & ABAH", size=7, kind="bold", fill=C_INK)
        # Smartphone beside frame
        cam.rect((802, 392, 830, 438), fill=(42, 52, 64), outline=C_INK, width=1.8, radius=4)
        cam.rect((806, 397, 826, 432), fill=(154, 218, 182), outline=None)

    # ------------------------------------------------------------------
    # S04 (51.0 - 67.0s): Bersandar di Tepi Bank — Zoom-In ke Bahu & Wajah Penat
    # ------------------------------------------------------------------
    elif t < 67.0:
        lt = t - 51.0
        im = make_gradient_bg(C_PEACH, C_CREAM).copy()
        # Zoom in from wide scorching sun shot (640,350,1.0) to close-up of Amir's slumped shoulders & sigh (450,275,2.15)
        z = smoothstep(5.0, 12.5, lt)
        cam = CamCanvas(im, lerp(620.0, 445.0, z), lerp(340.0, 275.0, z), lerp(1.0, 2.15, z))

        # Blazing sun & heat shimmer rays
        sun_r = 72 + math.sin(t * 2.5) * 5
        cam.circle(880, 115, sun_r + 28, fill=(246, 218, 154, 85), outline=None)
        cam.circle(880, 115, sun_r, fill=C_GOLD_LIGHT, outline=C_GOLD, width=2.0)

        # Sidewalk & Brick wall of bank on left with AC outdoor compressor dripping water
        cam.rect((-200, 515, 1480, 800), fill=(212, 198, 176))
        cam.line([(-200, 515), (1480, 515)], fill=C_INK, width=2.5)
        cam.rect((80, 60, 395, 515), fill=(218, 202, 182), outline=C_INK, width=3.0)
        for by in range(100, 500, 42):
            cam.line([(80, by), (395, by)], fill=(196, 180, 160), width=1.8)
        # AC compressor box mounted on wall
        cam.rect((155, 185, 295, 285), fill=C_CREAM, outline=C_INK, width=2.2, radius=6)
        cam.circle(210, 235, 34, fill=C_MUTED, outline=C_INK, width=2.0)
        # Street bench & potted agave
        cam.rect((740, 455, 960, 472), fill=(158, 116, 76), outline=C_INK, width=2.0, radius=4)
        cam.rect((765, 472, 782, 515), fill=C_INK)
        cam.rect((925, 472, 942, 515), fill=C_INK)
        draw_potted_plant(cam, 1060, 515, 1.05, t)

        # Amir leaning tiredly against the bank wall, shoulders dropping & sighing
        draw_character(cam, 445, 522, scale=1.20, t=t, role="amir", pose="sigh", mood="tired", facing=1, view="three_quarter_right" if t < 59.0 else "front", lanyard=True)
        # Visible small sigh cloud at 61.5 - 66.5s
        if t >= 61.5:
            ph_s = clamp((t - 61.5) / 3.5)
            cam.circle(475 + ph_s * 35, 255 - ph_s * 18, 8 + ph_s * 8, fill=(255, 255, 255, int(160 * (1.0 - ph_s))), outline=None)

    # ------------------------------------------------------------------
    # S05 (67.0 - 96.5s): Kontras Pejabat Dingin vs Angkat Kotak & Susun Fail
    # ------------------------------------------------------------------
    elif t < 96.5:
        if t < 82.2:
            # S05A (67.0 - 82.2s): Cool Air-Conditioned Executive Office & Luxury Car outside window
            lt = t - 67.0
            im = make_gradient_bg(C_SKY, C_CREAM).copy()
            z = smoothstep(3.0, 11.5, lt)
            cam = CamCanvas(im, lerp(640.0, 585.0, z), lerp(350.0, 315.0, z), lerp(1.0, 1.72, z))

            # Office floor, panoramic city window, wall AC blowing cool breeze
            cam.rect((-200, 510, 1480, 800), fill=(214, 222, 228))
            cam.line([(-200, 510), (1480, 510)], fill=C_INK, width=2.5)
            # Panoramic window showing luxury car parked outside
            cam.rect((680, 110, 1140, 420), fill=(204, 228, 242), outline=C_INK, width=3.0, radius=8)
            draw_luxury_car(cam, 760, 315, s=0.85, col=(44, 62, 82))
            # Wall Air-Conditioner unit with cool airflow waves
            cam.rect((220, 95, 450, 148), fill=C_WHITE, outline=C_INK, width=2.2, radius=8)
            for w_i in range(3):
                wy_air = 165 + w_i * 18 + math.sin(t * 3.0 + w_i) * 4
                cam.line([(260 - w_i * 12, wy_air), (420 + w_i * 12, wy_air + 14)], fill=(130, 198, 228), width=2.2)

            # Executive Faris seated at modern desk with monitor & espresso cup
            draw_character(cam, 520, 515, scale=1.15, t=t, role="exec", pose="sit_table", mood="calm", facing=1, lanyard=False)
            cam.rect((555, 395, 860, 415), fill=(120, 92, 68), outline=C_INK, width=2.4, radius=4)
            cam.rect((580, 415, 602, 515), fill=C_INK)
            cam.rect((815, 415, 837, 515), fill=C_INK)
            # Computer monitor & coffee cup on desk
            cam.rect((665, 305, 775, 382), fill=(48, 58, 68), outline=C_INK, width=2.2, radius=6)
            cam.rect((710, 382, 730, 395), fill=C_MUTED, outline=C_INK, width=1.8)
            cam.rect((605, 368, 632, 395), fill=C_WHITE, outline=C_INK, width=1.8, radius=4)
            draw_potted_plant(cam, 260, 512, 1.1, t, pot_col=C_TEAL)
        else:
            # S05B (82.2 - 96.5s): Amir Lifting Heavy Boxes & Stacking Files in Heat/Rain
            lt = t - 82.2
            im = make_gradient_bg(C_PEACH, C_SAND).copy()
            # Zoom in to Amir straining with the heavy box (560,295,1.88)
            z = smoothstep(2.5, 10.5, lt)
            cam = CamCanvas(im, lerp(640.0, 545.0, z), lerp(350.0, 295.0, z), lerp(1.0, 1.88, z))

            cam.rect((-200, 515, 1480, 800), fill=(192, 182, 166))
            cam.line([(-200, 515), (1480, 515)], fill=C_INK, width=2.5)
            # Metal shelving racks stacked with file binders & boxes on right
            for rx in (780, 980):
                cam.rect((rx, 130, rx + 165, 515), fill=None, outline=C_INK, width=3.0)
                for sy in (220, 320, 420):
                    cam.line([(rx, sy), (rx + 165, sy)], fill=C_INK, width=3.0)
                    # File binders & boxes on shelf
                    for f_i in range(4):
                        col_f = [C_TEAL, C_GOLD, C_TERRA, C_SAGE][f_i % 4]
                        cam.rect((rx + 14 + f_i * 35, sy - 64, rx + 42 + f_i * 35, sy - 2), fill=col_f, outline=C_INK, width=1.6, radius=2)

            # Yellow hand truck & stack of boxes on left
            cam.rect((210, 360, 340, 515), fill=(196, 150, 102), outline=C_INK, width=2.2, radius=4)
            cam.rect((225, 265, 325, 360), fill=(214, 168, 118), outline=C_INK, width=2.2, radius=4)

            # Amir carrying heavy box
            draw_character(cam, 530, 520, scale=1.18, t=t, role="amir", pose="carry_box", mood="tired", facing=1, lanyard=True)

    # ------------------------------------------------------------------
    # S06 (96.5 - 122.7s): Sunyi di Tengah Bandar yang Bising — Slow Zoom-In ke Amir
    # ------------------------------------------------------------------
    elif t < 122.7:
        lt = t - 96.5
        im = make_gradient_bg((226, 222, 234), C_CREAM).copy()
        # Slow dramatic push-in from wide city street (640,350,1.0) right into Amir's face & chest (640,265,2.10)
        z = smoothstep(2.0, 22.0, lt)
        cam = CamCanvas(im, 640.0, lerp(355.0, 265.0, z), lerp(1.0, 2.10, z))

        # City buildings, streetlamps, traffic light & zebra crossing
        for b_i in range(9):
            bx = b_i * 160 - 60
            bh = 220 + (b_i * 53) % 160
            cam.rect((bx, 500 - bh, bx + 135, 500), fill=(198, 194, 208), outline=C_MUTED, width=1.8)
            for wy in range(520 - bh, 470, 42):
                cam.rect((bx + 20, wy, bx + 52, wy + 24), fill=C_CREAM, outline=None)
                cam.rect((bx + 76, wy, bx + 108, wy + 24), fill=C_CREAM, outline=None)

        cam.rect((-200, 500, 1480, 800), fill=(154, 158, 166))
        for zx in range(120, 1180, 110):
            cam.rect((zx, 520, zx + 65, 542), fill=C_CREAM, outline=None, radius=2)

        # Traffic light pole on right
        cam.line([(920, 210), (920, 500)], fill=C_INK, width=4.0)
        cam.rect((902, 185, 938, 275), fill=C_INK, outline=C_GOLD, width=2.0, radius=6)
        cam.circle(920, 205, 8, fill=C_TERRA)
        cam.circle(920, 230, 8, fill=C_GOLD)
        cam.circle(920, 255, 8, fill=C_SAGE)

        # Fast-moving translucent commuter silhouettes rushing past
        for c_i in range(6):
            dir_c = 1 if c_i % 2 == 0 else -1
            cx_p = ((c_i * 230 + t * 85 * dir_c) % 1480) - 100
            cam.circle(cx_p, 385, 18, fill=(142, 138, 154, 115), outline=None)
            cam.rect((cx_p - 22, 405, cx_p + 22, 505), fill=(142, 138, 154, 115), outline=None, radius=10)

        # Warm breathing glow when Amir inhales deeply (116.5 - 122.7s)
        if t >= 116.5:
            r_glow = (85 + math.sin((t - 116.5) * 2.2) * 22)
            cam.circle(640, 295, r_glow, fill=(246, 218, 154, 90), outline=C_GOLD, width=2.5)

        draw_character(cam, 640, 520, scale=1.20, t=t, role="amir", pose="stand", mood="calm" if t >= 116.5 else "sad", view="back" if t < 108.5 else ("three_quarter_right" if t < 116.0 else "front"), lanyard=True)

    # ------------------------------------------------------------------
    # S07 (122.7 - 142.4s): Parkir Motor Lama — Zoom-In ke Tempat Duduk Calar & Kunci Enjin
    # ------------------------------------------------------------------
    elif t < 142.4:
        lt = t - 122.7
        im = make_gradient_bg(C_CREAM, C_CREAM_DARK).copy()
        # Camera keyframes:
        # 0-5.5s: Tracking Amir walking to parked kapcai (620,350,1.08)
        # 5.5-11.5s: Zoom-in to scratched seat & ignition key turning (720,385,2.25)
        # 11.5-19.7s: Pull back slightly to show vibrating kapcai & Amir with scarred helmet (680,365,1.55)
        p1 = smoothstep(4.5, 6.8, lt)
        p2 = smoothstep(11.8, 14.2, lt)
        cx = lerp(lerp(600.0, 725.0, p1), 675.0, p2)
        cy = lerp(lerp(350.0, 395.0, p1), 360.0, p2)
        cz = lerp(lerp(1.05, 2.25, p1), 1.55, p2)
        cam = CamCanvas(im, cx, cy, cz)

        # Parking shed roof, pillars, trees & road
        cam.rect((-200, 505, 1480, 800), fill=(138, 144, 152))
        cam.line([(-200, 505), (1480, 505)], fill=C_GOLD, width=3.0)
        draw_tree(cam, 220, 505, 1.05, t)
        draw_tree(cam, 1060, 505, 0.95, t + 1.5)
        # Covered parking shed pillars
        cam.rect((450, 140, 478, 505), fill=C_SAND, outline=C_INK, width=2.2)
        cam.rect((920, 140, 948, 505), fill=C_SAND, outline=C_INK, width=2.2)
        cam.poly([(410, 145), (990, 145), (1020, 105), (380, 105)], fill=C_TEAL_DARK, outline=C_INK, width=2.5)

        if t < 130.5:
            # Amir walks toward his parked kapcai
            wx_amir = lerp(260.0, 545.0, clamp(lt / 7.5))
            draw_character(cam, wx_amir, 520, scale=1.15, t=t, role="amir", pose="walk", mood="calm", facing=1, lanyard=True)
            draw_kapcai_detailed(cam, 705, 472, s=1.35, t=t, moving=False, with_rider=False)
        else:
            # Amir mounted with scarred helmet, turning key & engine vibrating alive
            draw_kapcai_detailed(cam, 690, 472, s=1.38, t=t, moving=(t >= 133.2), with_rider=True)

    # ------------------------------------------------------------------
    # S08 (142.4 - 157.8s): Terselit di Tengah Kereta Mewah — Zoom-In ke Amir di Celah Kereta
    # ------------------------------------------------------------------
    elif t < 157.8:
        lt = t - 142.4
        im = make_gradient_bg(C_SKY, C_CREAM).copy()
        # Zoom in from wide highway (640,360,1.0) onto Amir squeezed between the luxury cars (640,415,1.88)
        z = smoothstep(4.5, 12.0, lt)
        cam = CamCanvas(im, 640.0, lerp(360.0, 415.0, z), lerp(1.0, 1.88, z))

        # Moving parallax hills, trees & highway
        dist = t * 95.0
        for i in range(7):
            tx = ((i * 230 - dist * 0.55) % 1560) - 140
            draw_tree(cam, tx, 475, 0.85, t)
        cam.rect((-200, 475, 1480, 800), fill=(108, 116, 126))
        cam.line([(-200, 480), (1480, 480)], fill=C_GOLD, width=3.0)
        for i in range(10):
            rx = ((i * 170 - dist) % 1640) - 160
            cam.rect((rx, 545, rx + 85, 554), fill=C_CREAM, outline=None, radius=2)

        # Luxury SUV on left & Executive Sedan on right
        c1_x = 125 + math.sin(t * 1.1) * 16
        c2_x = 815 + math.cos(t * 0.95) * 16
        draw_luxury_car(cam, c1_x, 435, s=1.12, col=(42, 58, 76))
        draw_luxury_car(cam, c2_x, 435, s=1.12, col=(58, 72, 88))
        # Amir squeezed in the middle lane on his small kapcai
        draw_kapcai_detailed(cam, 640, 470, s=1.18, t=t, moving=True, with_rider=True)

    # ------------------------------------------------------------------
    # S09 (157.8 - 197.5s): Turning Point — Zoom-In ke Tangan Berparut & Lap Air Mata
    # ------------------------------------------------------------------
    elif t < 197.5:
        lt = t - 157.8
        im = make_gradient_bg(C_PEACH, C_SAND).copy()

        if t < 188.5:
            # S09A (157.8 - 188.5s): POV Handlebar & Slow Zoom-In onto Amir's Sun-Darkened Hand with Oil Scar
            z = smoothstep(2.0, 24.0, lt)
            cam = CamCanvas(im, lerp(640.0, 745.0, z), lerp(360.0, 355.0, z), lerp(1.05, 2.25, z))

            # Moving road surface below handlebar
            cam.rect((-200, 0, 1480, 800), fill=(128, 134, 142))
            for r_i in range(9):
                ry = ((r_i * 95 + int(t * 240)) % 820) - 60
                cam.rect((615, ry, 665, ry + 55), fill=C_CREAM, outline=None, radius=3)

            # Detailed Kapcai Handlebar, Speedometer Cluster, Side Mirror & Ignition Key
            cam.line([(160, 410), (490, 355), (790, 355), (1120, 410)], fill=(48, 54, 62), width=28)
            cam.line([(760, 330), (1080, 305)], fill=C_INK, width=8) # brake lever
            # Speedometer housing
            cam.poly([(460, 420), (510, 285), (770, 285), (820, 420)], fill=(62, 98, 122), outline=C_INK, width=3.5)
            cam.circle(640, 345, 54, fill=C_CREAM, outline=C_INK, width=3.0)
            # Speedometer needle vibrating around 60 km/h
            ang_sp = math.radians(-35 + math.sin(t * 12.0) * 4.0)
            cam.line([(640, 345), (640 + math.cos(ang_sp) * 40, 345 + math.sin(ang_sp) * 40)], fill=C_TERRA, width=3.0)
            cam.circle(640, 345, 6, fill=C_INK)

            # Right Throttle Grip & Amir's Sun-Darkened Hand (#AD7553) with Oil Scar (#6E4730)
            vib = math.sin(t * 36.0) * 1.4
            hx, hy = 875, 368 + vib
            cam.rect((780, 340 + vib, 995, 392 + vib), fill=(36, 40, 46), outline=C_INK, width=3.0, radius=10)
            # Forearm & teal cuff entering from bottom right
            cam.poly([(hx - 58, hy + 42), (hx + 64, hy + 32), (hx + 115, 680), (hx - 95, 680)], fill=SKIN_AMIR, outline=C_INK, width=3.0)
            cam.poly([(hx - 85, 505), (hx + 95, 495), (hx + 125, 690), (hx - 110, 690)], fill=C_TEAL, outline=C_INK, width=3.5)
            # Hand back & 4 articulated knuckles gripping throttle
            cam.rect((hx - 68, hy - 38, hx + 68, hy + 52), fill=SKIN_AMIR, outline=C_INK, width=3.0, radius=22)
            for k_i in range(4):
                kx = hx - 54 + k_i * 28
                cam.rect((kx, hy - 50, kx + 24, hy - 8), fill=SKIN_AMIR_SHADE, outline=C_INK, width=2.4, radius=9)
            # Prominent dark oil-burn scar (#6E4730) on the back of the hand
            cam.line([(hx - 26, hy - 4), (hx + 12, hy + 14), (hx + 28, hy + 4)], fill=(102, 62, 40), width=4.5)
            cam.line([(hx - 8, hy - 14), (hx + 4, hy + 20)], fill=(102, 62, 40), width=3.0)
        else:
            # S09B (188.5 - 197.5s): Close-Up Zoom-In on Amir's Tearful Face Wiping Eyes with Teal Sleeve
            lt_b = t - 188.5
            z = smoothstep(0.0, 6.5, lt_b)
            cam = CamCanvas(im, 640.0, lerp(285.0, 235.0, z), lerp(1.55, 2.25, z))
            cam.rect((-200, 515, 1480, 800), fill=C_SAND)
            draw_tree(cam, 280, 515, 1.0, t)
            draw_tree(cam, 1020, 515, 1.0, t)
            draw_character(cam, 640, 530, scale=1.28, t=t, role="amir", pose="wipe_tear", mood="tearful", lanyard=True, tear=lt_b * 0.45)

    # ------------------------------------------------------------------
    # S10 (197.5 - 265.2s): Makna Rezeki — Tilam Empuk vs Tilam Nipis
    # ------------------------------------------------------------------
    elif t < 265.2:
        lt = t - 197.5
        if t < 226.5:
            # S10A (197.5 - 226.5s): Peaceful Night Reflection — Zoom-In to Amir under Starlight
            im = make_gradient_bg((42, 64, 82), (88, 118, 128)).copy()
            z = smoothstep(3.0, 22.0, lt)
            cam = CamCanvas(im, 640.0, lerp(350.0, 275.0, z), lerp(1.0, 1.82, z))
            # Crescent moon, stars, glowing lantern & garden bench
            cam.circle(960, 135, 42, fill=C_GOLD_LIGHT)
            cam.circle(976, 122, 36, fill=(48, 72, 90))
            for s_i in range(16):
                sx = (s_i * 83 + 50) % 1200
                sy = (s_i * 47 + 40) % 280
                cam.circle(sx, sy, 2.0 + (s_i % 2), fill=C_GOLD_LIGHT)
            cam.rect((-200, 515, 1480, 800), fill=(68, 88, 84))
            draw_tree(cam, 220, 515, 1.05, t)
            draw_lantern(cam, 460, 390, 1.0, t, lit=True)
            draw_character(cam, 640, 525, scale=1.20, t=t, role="amir", pose="stand", mood="calm", view="back" if t < 212.0 else "three_quarter_right", lanyard=False, speaking=speak_amp)

        elif t < 243.8:
            # S10B (226.5 - 243.8s): Two Bedrooms — Zoom from Restless Plush Bed to Amir's Peaceful Thin Mattress
            lt_b = t - 226.5
            im = make_gradient_bg(C_CREAM_DARK, C_CREAM).copy()
            # Pan & zoom from Left Room (Tilam Empuk, 340,340,1.45) to Right Room (Tilam Nipis, 940,365,1.65)
            p_pan = smoothstep(6.5, 10.5, lt_b)
            cam = CamCanvas(im, lerp(360.0, 920.0, p_pan), lerp(340.0, 375.0, p_pan), lerp(1.42, 1.68, p_pan))

            # Left Room: Luxury Bedroom with Chandelier, Digital Clock 03:15 & Thick Plush Mattress
            cam.rect((0, 0, 635, 720), fill=(54, 66, 84))
            cam.rect((65, 360, 565, 495), fill=(182, 192, 208), outline=C_INK, width=2.5, radius=14)
            cam.rect((65, 290, 115, 495), fill=(96, 72, 54), outline=C_INK, width=2.5, radius=6)
            # Restless man wide awake
            cam.circle(155, 338, 22, fill=SKIN_LIGHT, outline=C_INK, width=2.0)
            cam.circle(162, 332, 5, fill=C_WHITE, outline=C_INK, width=1.4)
            cam.circle(163, 332, 2, fill=C_INK)
            # Nightstand with glowing red clock 03:15
            cam.rect((460, 295, 545, 335), fill=C_INK, outline=C_GOLD, width=1.8, radius=4)
            cam.text(502, 315, "03:15 AM", size=12, kind="bold", fill=C_TERRA)

            # Divider wall
            cam.line([(640, 0), (640, 720)], fill=C_GOLD, width=5.0)

            # Right Room: Amir's Humble Peaceful Room with Thin Mattress, Window, Sejadah & Fan
            cam.rect((645, 0, 1280, 720), fill=C_CREAM)
            cam.rect((645, 495, 1280, 720), fill=(208, 192, 166))
            # Window with moon
            cam.rect((980, 110, 1150, 290), fill=(48, 72, 92), outline=C_INK, width=2.5, radius=6)
            cam.circle(1090, 165, 20, fill=C_GOLD_LIGHT)
            # Folded sejadah on wooden rack & standing fan
            cam.rect((700, 365, 775, 495), fill=(142, 104, 68), outline=C_INK, width=2.0)
            cam.rect((708, 355, 768, 415), fill=C_SAGE, outline=C_INK, width=1.8, radius=4)
            # Thin mattress on floor with Amir sleeping peacefully
            cam.rect((795, 468, 1185, 502), fill=C_TEAL_LIGHT, outline=C_INK, width=2.2, radius=8)
            cam.rect((808, 452, 875, 476), fill=C_WHITE, outline=C_INK, width=1.8, radius=8)
            br_s = math.sin(t * 1.8) * 3.0
            cam.circle(845, 442 + br_s * 0.4, 22, fill=SKIN_AMIR, outline=C_INK, width=2.0)
            cam.line([(838, 438), (850, 438)], fill=C_INK, width=2.0) # closed peaceful eye
            cam.arc((842, 444, 856, 452), start=15, end=165, fill=C_INK, width=1.8) # peaceful smile
            cam.rect((870, 440 + br_s, 1085, 482), fill=C_TEAL, outline=C_INK, width=2.2, radius=14)
        else:
            # S10C (243.8 - 265.2s): Jalan Berbeza — Amir Walking Humbly with Nature & Birds
            lt_c = t - 243.8
            im = make_gradient_bg(C_CREAM, C_PEACH).copy()
            z = smoothstep(2.0, 16.0, lt_c)
            cam = CamCanvas(im, 640.0, lerp(355.0, 290.0, z), lerp(1.0, 1.72, z))
            cam.rect((-200, 510, 1480, 800), fill=C_SAND)
            draw_tree(cam, 240, 510, 1.05, t)
            draw_tree(cam, 1020, 510, 1.10, t + 1.2)
            draw_bird(cam, 420 + (lt_c * 24) % 450, 155, 1.1, t)
            draw_bird(cam, 380 + (lt_c * 24) % 450, 175, 0.9, t + 0.5)
            draw_character(cam, 640, 520, scale=1.20, t=t, role="amir", pose="walk" if t < 255.0 else "stand", mood="calm", view="side_right" if t < 255.0 else "three_quarter_right", lanyard=True)

    # ------------------------------------------------------------------
    # S11 (265.2 - 341.0s): Panggilan Telefon Mak — Zoom ke Skrin Retak, Mak di Kampung & Amir
    # ------------------------------------------------------------------
    elif t < 341.0:
        lt = t - 265.2
        im = make_gradient_bg((236, 244, 232), C_CREAM).copy()

        if t < 278.8:
            # S11A (265.2 - 278.8s): Berhenti Bawah Pokok & Zoom-In ke Skrin Telefon Retak ("Mak")
            z = smoothstep(3.5, 10.5, lt)
            cam = CamCanvas(im, lerp(640.0, 540.0, z), lerp(355.0, 355.0, z), lerp(1.05, 2.35, z))
            cam.rect((-200, 510, 1480, 800), fill=(198, 190, 172))
            draw_tree(cam, 260, 510, 1.35, t)
            draw_kapcai_detailed(cam, 880, 475, s=1.15, t=t, moving=False, with_rider=False)
            draw_character(cam, 460, 520, scale=1.18, t=t, role="amir", pose="phone_look", mood="worried", facing=1, lanyard=True)

            # Detailed Cracked Smartphone Prop in Foreground when zooming in
            px, py = 595, 355
            vib_x = math.sin(t * 45.0) * 2.0 if t < 276.5 else 0.0
            cam.rect((px - 42 + vib_x, py - 78, px + 42 + vib_x, py + 78), fill=(38, 46, 56), outline=C_INK, width=2.5, radius=10)
            cam.rect((px - 36 + vib_x, py - 64, px + 36 + vib_x, py + 64), fill=C_CREAM, outline=C_INK, width=1.5, radius=6)
            # Crack lines across top-right corner of screen
            cam.line([(px + 8 + vib_x, py - 64), (px + 22 + vib_x, py - 38), (px + 36 + vib_x, py - 32)], fill=C_MUTED, width=1.5)
            cam.line([(px + 22 + vib_x, py - 38), (px + 12 + vib_x, py - 18)], fill=C_MUTED, width=1.2)
            cam.circle(px + vib_x, py - 24, 16, fill=C_SAGE_LIGHT, outline=C_INK, width=1.5)
            cam.text(px + vib_x, py + 4, "Mak", size=14, kind="bold", fill=C_INK)
            # Pulsing Green Answer Button
            btn_r = 14 + math.sin(t * 6.0) * 2.0
            cam.circle(px + vib_x, py + 38, btn_r, fill=C_SAGE, outline=C_INK, width=1.8)
        else:
            # S11B (278.8 - 341.0s): Two-World Split — Amir under Roadside Tree & Mak on Kampung House Veranda
            # Dynamic Camera alternates between Two-Shot (640,350,1.0), Zoom-In on Mak (935,295,1.68), and Zoom-In on Amir (335,285,1.72)
            if 279.0 <= t < 290.0 or 315.5 <= t < 323.5:
                # Mak speaking -> Zoom in toward Mak in Kampung
                p_m = smoothstep(0.0, 2.5, (t - 279.0) if t < 290.0 else (t - 315.5))
                cam = CamCanvas(im, lerp(640.0, 920.0, p_m), lerp(350.0, 295.0, p_m), lerp(1.0, 1.65, p_m))
            elif 291.0 <= t < 315.0 or t >= 324.0:
                # Amir feeling sebak / replying -> Zoom in toward Amir
                p_a = smoothstep(0.0, 2.5, (t - 291.0) if t < 315.0 else (t - 324.0))
                cam = CamCanvas(im, lerp(640.0, 355.0, p_a), lerp(350.0, 285.0, p_a), lerp(1.0, 1.72, p_a))
            else:
                cam = CamCanvas(im, 640.0, 350.0, 1.0)

            # Left Half: Shady Roadside Tree & Amir
            cam.rect((-200, 510, 635, 800), fill=(198, 190, 172))
            draw_tree(cam, 185, 510, 1.35, t)
            draw_potted_plant(cam, 495, 512, 0.85, t)
            amir_speaking = speak_amp if (304.5 <= t <= 310.5) else 0.0
            draw_character(cam, 355, 520, scale=1.18, t=t, role="amir", pose="phone_call" if t < 323.8 else "touch_lanyard", mood="tearful" if t < 323.8 else "calm", facing=1, lanyard=True, tear=0.6 if 291.0 <= t <= 316.0 else 0.0, speaking=amir_speaking)

            # Warm Golden Divider Line
            cam.line([(640, 0), (640, 720)], fill=C_GOLD, width=5.0)

            # Right Half: Traditional Kampung Wooden House Veranda with Mak (P10)
            cam.rect((645, 0, 1480, 720), fill=C_PEACH)
            cam.rect((645, 505, 1480, 800), fill=(178, 134, 94)) # wooden veranda floor
            # Wooden veranda railing, Louver window, hanging fern plant & lantern
            for rx in range(665, 1260, 42):
                cam.rect((rx, 415, rx + 16, 505), fill=(154, 112, 74), outline=C_INK, width=1.6)
            cam.rect((645, 405, 1280, 420), fill=(138, 96, 60), outline=C_INK, width=2.0)
            # Kampung house wooden window & batik curtain
            cam.rect((710, 125, 865, 325), fill=(122, 86, 54), outline=C_INK, width=2.5, radius=4)
            for wy in range(145, 315, 22):
                cam.line([(718, wy), (857, wy)], fill=C_CREAM_DARK, width=2.0)
            draw_lantern(cam, 1095, 165, 0.95, t, lit=True)
            draw_potted_plant(cam, 1135, 505, 1.0, t, pot_col=C_SAGE)

            mak_speaking = speak_amp if (279.0 <= t <= 289.0 or 315.8 <= t <= 323.2) else 0.0
            draw_character(cam, 955, 515, scale=1.12, t=t, role="mak", pose="phone_call", mood="calm", facing=-1, lanyard=False, speaking=mak_speaking)

    # ------------------------------------------------------------------
    # S12 (341.0 - 375.8s): Warung Tepi Jalan — Zoom ke Kipas Siling, Nasi Lemak Daun Pisang & Amir
    # ------------------------------------------------------------------
    elif t < 375.8:
        lt = t - 341.0
        im = make_gradient_bg(C_CREAM, C_CREAM_DARK).copy()
        # Multi-target camera:
        # 341.0-353.0s: Wide Warung interior (640,355,1.05)
        # 353.0-357.8s: Zoom-In Upward to the creaking Old Ceiling Fan (580,125,2.20)
        # 357.8-368.8s: Zoom-In Downward onto Tabletop Nasi Lemak Daun Pisang & Teh O Ais (675,415,2.35)
        # 368.8-375.8s: Zoom-In to Amir's grateful face (495,285,1.82)
        p_fan = smoothstep(352.5, 354.2, t) * (1.0 - smoothstep(357.2, 358.8, t))
        p_food = smoothstep(357.4, 359.2, t) * (1.0 - smoothstep(368.2, 370.0, t))
        p_face = smoothstep(368.5, 370.5, t)

        cx = 640.0 * (1.0 - max(p_fan, p_food, p_face)) + 580.0 * p_fan + 615.0 * p_food + 515.0 * p_face
        cy = 355.0 * (1.0 - max(p_fan, p_food, p_face)) + 145.0 * p_fan + 365.0 * p_food + 295.0 * p_face
        cz = 1.05 * (1.0 - max(p_fan, p_food, p_face)) + 1.95 * p_fan + 1.78 * p_food + 1.82 * p_face
        cam = CamCanvas(im, cx, cy, cz)

        # Warung ceiling beam, floor, food counter cabinet & hanging warm bulbs
        cam.rect((-200, 0, 1480, 78), fill=(208, 192, 166))
        cam.rect((-200, 515, 1480, 800), fill=(196, 180, 154))
        cam.line([(-200, 515), (1480, 515)], fill=C_INK, width=2.5)

        # Background Warung Counter & Glass Food Display Cabinet (Almari Lauk)
        cam.rect((95, 355, 365, 515), fill=(156, 116, 78), outline=C_INK, width=2.4, radius=4)
        cam.rect((110, 235, 350, 355), fill=(214, 234, 242), outline=C_INK, width=2.2, radius=4)
        # Trays of food & metal kettle on counter
        cam.rect((130, 325, 195, 348), fill=C_TERRA, outline=C_INK, width=1.6, radius=3)
        cam.rect((210, 325, 275, 348), fill=C_GOLD, outline=C_INK, width=1.6, radius=3)
        draw_character(cam, 235, 515, scale=0.95, t=t, role="salma", pose="stand", mood="calm", facing=1, lanyard=False)

        # Spinning Old 3-Blade Ceiling Fan overhead ("Krek... krek... krek...")
        fan_x, fan_y = 580, 118
        cam.line([(fan_x, 0), (fan_x, fan_y)], fill=C_INK, width=5.0)
        w_blade = math.cos(t * 2.4) * 125.0
        cam.rect((fan_x - abs(w_blade) - 24, fan_y - 7, fan_x + abs(w_blade) + 24, fan_y + 7), fill=(122, 112, 98), outline=C_INK, width=2.0, radius=5)
        cam.ellipse((fan_x - 24, fan_y - 14, fan_x + 24, fan_y + 14), fill=C_GOLD, outline=C_INK, width=2.2)

        # Amir seated at corner wooden table
        cam.rect((445, 365, 535, 520), fill=(132, 94, 60), outline=C_INK, width=2.2, radius=4)
        draw_character(cam, 495, 520, scale=1.16, t=t, role="amir", pose="sit_warung", mood="calm", facing=1, lanyard=True)

        # Corner Wooden Table & Detailed Tabletop Props
        cam.rect((525, 435, 920, 456), fill=(166, 120, 78), outline=C_INK, width=2.5, radius=6)
        cam.rect((555, 456, 578, 525), fill=(138, 98, 62), outline=C_INK, width=2.0)
        cam.rect((865, 456, 888, 525), fill=(138, 98, 62), outline=C_INK, width=2.0)

        # Props on Table:
        # 1) Opened Green Banana Leaf (Daun Pisang) Nasi Lemak with White Rice, Sambal, Egg, Cucumber & Steam
        cam.poly([(585, 435), (618, 404), (725, 404), (755, 435)], fill=C_SAGE, outline=C_INK, width=2.0)
        cam.pieslice((628, 392, 712, 454), start=180, end=360, fill=C_WHITE, outline=C_INK, width=2.0)
        cam.ellipse((655, 396, 692, 415), fill=C_TERRA, outline=C_INK, width=1.4) # Sambal
        cam.ellipse((632, 412, 654, 428), fill=C_GOLD_LIGHT, outline=C_INK, width=1.4) # Half egg
        # Fragrant Pandan Steam waves rising
        for s_i in range(3):
            sx = 650 + s_i * 22 + math.sin(t * 3.0 + s_i) * 5.0
            sy = 376 - ((t * 20.0 + s_i * 14.0) % 38.0)
            cam.arc((sx - 8, sy - 14, sx + 8, sy + 14), start=0, end=180, fill=C_WHITE, width=2.2)

        # 2) Tall Glass of Teh O Ais with Ice Cubes & Straw
        cam.rect((775, 382, 815, 435), fill=(204, 128, 52), outline=C_INK, width=2.0, radius=5)
        cam.rect((781, 388, 793, 400), fill=(245, 248, 252), outline=None, radius=2) # ice cube
        cam.rect((796, 392, 808, 404), fill=(245, 248, 252), outline=None, radius=2) # ice cube
        cam.line([(800, 386), (816, 360)], fill=C_TEAL, width=3.2)

        # 3) Chili Sauce Bottle & Tissue Box at corner of table
        cam.rect((845, 390, 868, 435), fill=C_TERRA, outline=C_INK, width=1.8, radius=4)
        cam.rect((850, 376, 863, 390), fill=C_WHITE, outline=C_INK, width=1.5)
        cam.rect((876, 410, 912, 435), fill=C_SKY, outline=C_INK, width=1.8, radius=3)
        cam.poly([(886, 410), (894, 396), (904, 410)], fill=C_WHITE, outline=C_INK, width=1.2)

    # ------------------------------------------------------------------
    # S13 (375.8 - 417.2s): Senja Kampung — Zoom-In ke Mak & Abah Berdoa di Atas Sejadah
    # ------------------------------------------------------------------
    elif t < 417.2:
        lt = t - 375.8
        im = make_gradient_bg((244, 198, 154), C_CREAM).copy()
        # Slow reverent zoom-in from wide kampung sunset (640,355,1.0) onto Mak & Abah praying on sejadah (615,345,1.78)
        z = smoothstep(4.0, 32.0, lt)
        cam = CamCanvas(im, lerp(640.0, 615.0, z), lerp(355.0, 345.0, z), lerp(1.0, 1.78, z))

        # Sunset sun, distant mountains, paddy fields & coconut palms
        cam.circle(960, 215, 78, fill=C_GOLD_LIGHT)
        cam.poly([(-200, 465), (180, 355), (540, 425), (920, 340), (1480, 455), (1480, 600), (-200, 600)], fill=(192, 166, 146))
        cam.rect((-200, 455, 1480, 520), fill=(154, 178, 138)) # paddy fields
        draw_tree(cam, 165, 510, 1.15, t, kind="palm")
        draw_tree(cam, 1085, 510, 1.10, t + 1.0, kind="palm")
        draw_bird(cam, 340 + (lt * 18) % 500, 165, 1.0, t)
        draw_bird(cam, 380 + (lt * 18) % 500, 182, 0.85, t + 0.6)

        # Kampung veranda prayer space
        cam.rect((-200, 510, 1480, 800), fill=(182, 142, 104))
        cam.line([(-200, 510), (1480, 510)], fill=C_INK, width=2.5)
        draw_lantern(cam, 360, 220, 1.0, t, lit=True)

        # Patterned Prayer Mats (Sejadah) + Raised Rehal with Al-Quran + Shoes neatly OFF the mat
        cam.poly([(420, 505), (780, 505), (820, 555), (380, 555)], fill=C_SAGE, outline=C_GOLD, width=2.5)
        cam.poly([(440, 512), (760, 512), (790, 548), (410, 548)], fill=None, outline=C_GOLD_LIGHT, width=1.6)
        # Shoes placed neatly outside the prayer mat boundary on the right
        cam.ellipse((855, 528, 892, 544), fill=(76, 62, 54), outline=C_INK, width=1.8)
        cam.ellipse((900, 528, 936, 544), fill=(76, 62, 54), outline=C_INK, width=1.8)
        # Raised Rehal & Mushaf beside Abah
        draw_rehal_quran(cam, 325, 452, s=0.95)

        # Abah (L09) and Mak (P10) seated on sejadah raising hands in dua
        draw_character(cam, 520, 535, scale=1.15, t=t, role="abah", pose="dua_sit", mood="calm", facing=1, lanyard=False)
        draw_character(cam, 685, 538, scale=1.08, t=t, role="mak", pose="dua_sit", mood="calm", facing=1, lanyard=False)

    # ------------------------------------------------------------------
    # S14 (417.2 - 452.8s): Matahari Terbit — Tracking & Zoom-In ke Langkah Amir
    # ------------------------------------------------------------------
    elif t < 452.8:
        lt = t - 417.2
        im = make_gradient_bg(C_PEACH, C_CREAM).copy()
        # Tracking camera zooming in from full-body stride (640,355,1.0) to medium close-up of Amir's determined face (640,275,1.88)
        z = smoothstep(4.0, 28.0, lt)
        cam = CamCanvas(im, 640.0, lerp(355.0, 275.0, z), lerp(1.0, 1.88, z))

        dist = lt * 45.0
        # Rising morning sun with warm golden halo
        sun_y = lerp(285.0, 175.0, clamp(lt / 30.0))
        cam.circle(920, sun_y, 95, fill=(246, 218, 154, 75), outline=None)
        cam.circle(920, sun_y, 56, fill=C_GOLD_LIGHT, outline=C_GOLD, width=2.0)

        # Moving hills, trees & road
        pts_h = [(-200, 520)]
        for hx in range(-200, 1520, 80):
            wx = hx + dist * 0.25
            hy = 415 + math.sin(wx * 0.005) * 32.0
            pts_h.append((hx, hy))
        pts_h.append((1520, 520))
        cam.poly(pts_h, fill=C_SAGE_LIGHT, outline=None)

        for i in range(7):
            tx = ((i * 240 - dist * 0.65) % 1620) - 160
            draw_tree(cam, tx, 505, 0.95, t)

        cam.rect((-200, 505, 1480, 800), fill=(212, 198, 174))
        cam.rect((-200, 525, 1480, 615), fill=(124, 132, 140))
        for i in range(9):
            rx = ((i * 180 - dist) % 1620) - 160
            cam.rect((rx, 566, rx + 82, 574), fill=C_CREAM, outline=None, radius=2)

        draw_bird(cam, 380 + (lt * 25) % 520, 145, 1.05, t)
        draw_character(cam, 640, 525, scale=1.22, t=t, role="amir", pose="walk", mood="calm", facing=1, lanyard=True)

    # ------------------------------------------------------------------
    # S15 (452.8 - 489.4s): Doa Khusyuk & Ayat Al-Quran (Surah At-Talaq 65:2-3)
    # ------------------------------------------------------------------
    elif t < 489.4:
        lt = t - 452.8
        im = make_gradient_bg(C_CREAM, C_CREAM_DARK).copy()
        # Slow khusyuk push-in (1.0 -> 1.32) keeping both Amir in prayer and the Quranic Verse plaque in frame
        z = smoothstep(2.0, 30.0, lt)
        cam = CamCanvas(im, lerp(640.0, 610.0, z), lerp(350.0, 325.0, z), lerp(1.0, 1.28, z))

        # Prayer room floor, mihrab arch, hanging lantern, raised Rehal & Mushaf, Sejadah & Shoes off mat
        cam.rect((-200, 515, 1480, 800), fill=C_SAND)
        cam.line([(-200, 515), (1480, 515)], fill=C_INK, width=2.5)
        draw_lantern(cam, 185, 165, 1.05, t, lit=True)
        draw_potted_plant(cam, 145, 515, 1.05, t)
        draw_rehal_quran(cam, 265, 448, s=1.0)

        # Prayer mat (Sejadah) & shoes placed neatly outside mat
        cam.poly([(335, 510), (545, 510), (575, 555), (305, 555)], fill=C_TEAL, outline=C_GOLD, width=2.5)
        cam.ellipse((205, 532, 240, 546), fill=(76, 62, 54), outline=C_INK, width=1.8)
        cam.ellipse((246, 532, 280, 546), fill=(76, 62, 54), outline=C_INK, width=1.8)

        # Floating golden light dust motes
        for p_i in range(14):
            px = (p_i * 89 + int(t * 12)) % 1200 + 40
            py = (p_i * 53 - int(t * 18)) % 480 + 40
            cam.circle(px, py, 2.5 + (p_i % 2), fill=C_GOLD)

        draw_character(cam, 435, 538, scale=1.22, t=t, role="amir", pose="dua_sit", mood="calm", facing=1, lanyard=False, speaking=speak_amp * 0.6)

        # Sacred Quranic Verse Frame on the right (Surah At-Talaq 65:2-3 & Surah Hud 11:6)
        cam.rect((615, 95, 1175, 475), fill=C_WHITE, outline=C_GOLD, width=3.5, radius=20)
        cam.rect((627, 107, 1163, 463), fill=None, outline=C_TEAL, width=1.6, radius=14)
        cam.rect((745, 122, 1045, 156), fill=C_TEAL, outline=None, radius=10)
        cam.text(895, 139, "FIRMAN ALLAH SWT • SURAH AT-TALAQ 65:3", size=13, kind="bold", fill=C_CREAM)

        # Vowelized Arabic Quranic Verse rendered with FT0002 Amiri Quran + RAQM RTL
        cam.text(895, 212, "وَيَرْزُقْهُ مِنْ حَيْثُ لَا يَحْتَسِبُ ۚ", size=30, kind="arabic", fill=C_INK, rtl=True)
        cam.text(895, 272, "وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ", size=30, kind="arabic", fill=C_TEAL, rtl=True)
        cam.line([(685, 315), (1105, 315)], fill=C_GOLD, width=2.0)
        cam.text(895, 355, "\"...Serta memberinya rezeki dari jalan yang tidak terlintas di hatinya.", size=15, kind="sans", fill=C_INK)
        cam.text(895, 385, "Dan sesiapa berserah diri bulat-bulat kepada Allah,", size=15, kind="sans", fill=C_INK)
        cam.text(895, 415, "maka Allah cukuplah baginya.\"", size=16, kind="bold", fill=C_TEAL)
        cam.text(895, 444, "(Surah At-Talaq, 65:3 — Terjemahan Abdullah Muhammad Basmeih)", size=12, kind="sans", fill=C_TERRA)

    # ------------------------------------------------------------------
    # S16 (489.4 - 516.67s): Hadis Riwayat al-Bukhari No. 2072
    # ------------------------------------------------------------------
    else:
        lt = t - 489.4
        im = make_gradient_bg(C_CREAM, C_CREAM_DARK).copy()
        z = smoothstep(0.0, 24.0, lt)
        cam = CamCanvas(im, 640.0, 330.0, lerp(1.0, 1.08, z))

        # Sanctuary background props: hanging lanterns, potted plants & raised Rehal
        cam.rect((-200, 520, 1480, 800), fill=C_SAND)
        draw_lantern(cam, 105, 145, 0.95, t, lit=True)
        draw_lantern(cam, 1175, 145, 0.95, t + 1.0, lit=True)
        draw_potted_plant(cam, 95, 525, 1.0, t)
        draw_potted_plant(cam, 1185, 525, 1.0, t + 0.8)

        # Central Illuminated Hadith Panel
        cam.rect((165, 52, 1115, 515), fill=C_WHITE, outline=C_GOLD, width=4.0, radius=22)
        cam.rect((179, 66, 1101, 501), fill=None, outline=C_TEAL, width=1.8, radius=16)
        cam.rect((415, 82, 865, 118), fill=C_TEAL, outline=None, radius=12)
        cam.text(640, 100, "HADIS KEMULIAAN KERJA TANGAN SENDIRI", size=15, kind="bold", fill=C_CREAM)

        # Full Vowelized Arabic Matan (Amiri Quran FT0002 + RAQM RTL)
        ar1 = "عَنْ الْمِقْدَامِ رَضِيَ اللَّهُ عَنْهُ عَنْ رَسُولِ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ قَالَ :"
        ar2 = "مَا أَكَلَ أَحَدٌ طَعَامًا قَطُّ خَيْرًا مِنْ أَنْ يَأْكُلَ مِنْ عَمَلِ يَدِهِ ،"
        ar3 = "وَإِنَّ نَبِيَّ اللَّهِ دَاوُدَ عَلَيْهِ السَّلَام كَانَ يَأْكُلُ مِنْ عَمَلِ يَدِهِ"
        cam.text(640, 165, ar1, size=28, kind="arabic", fill=C_INK, rtl=True)
        cam.text(640, 224, ar2, size=29, kind="arabic", fill=C_TEAL, rtl=True)
        cam.text(640, 282, ar3, size=29, kind="arabic", fill=C_TEAL, rtl=True)

        cam.line([(260, 324), (1020, 324)], fill=C_GOLD, width=2.0)
        cam.circle(640, 324, 5, fill=C_GOLD)

        # Malay Translation & Sahih al-Bukhari Citation
        cam.text(640, 356, "\"Daripada al-Miqdam RA, daripada Rasulullah SAW, Baginda bersabda:", size=17, kind="sans", fill=C_INK)
        cam.text(640, 386, "Tiada siapa yang memakan satu makanan yang lebih baik daripada makanan yang dimakan", size=17, kind="sans", fill=C_INK)
        cam.text(640, 416, "daripada hasil kerja tangannya sendiri. Dan sesungguhnya Nabi Allah Daud AS", size=17, kind="sans", fill=C_INK)
        cam.text(640, 444, "makan daripada hasil kerja tangannya sendiri.\"", size=17, kind="sans", fill=C_INK)
        cam.text(640, 476, "— Riwayat al-Bukhari, No. 2072", size=18, kind="bold", fill=C_TERRA)

    # ------------------------------------------------------------------
    # SCREEN-SPACE BOTTOM SAFE AREA: WAVEFORM + FULL SUBTITLE ONLY
    # ------------------------------------------------------------------
    d_screen = ImageDraw.Draw(im)
    draw_waveform_widget(d_screen, frame_idx)

    active_sub = None
    for s0, s1, stext in SUBTITLES:
        if s0 - 0.08 <= t <= s1 + 0.12:
            active_sub = stext
            break
    if active_sub:
        sbar = render_subtitle_bar(active_sub)
        im.paste(sbar, (202, 624), sbar)

    return im

def test_styleframes():
    samples = [
        ("v2_S01_zoom_lanyard.png", 5.5),
        ("v2_S03_zoom_meja_komitmen.png", 39.5),
        ("v2_S04_zoom_amir_penat.png", 63.0),
        ("v2_S05_angkat_kotak_rak_fail.png", 91.0),
        ("v2_S07_zoom_kunci_motor.png", 131.5),
        ("v2_S09_zoom_tangan_parut.png", 175.0),
        ("v2_S11_panggilan_mak_kampung.png", 283.0),
        ("v2_S12_zoom_nasi_lemak_warung.png", 362.0),
        ("v2_S15_doa_ayat_quran.png", 470.0),
        ("v2_S16_hadis_bukhari.png", 502.0),
        ("v3_back_view_S10A.png", 205.0),
        ("v3_side_walk_S07.png", 126.0),
        ("v3_3q_left_S02.png", 18.0),
    ]
    for fname, sec in samples:
        fidx = int(sec * FPS)
        im = render_frame(fidx).resize((1920, 1080), Image.Resampling.LANCZOS)
        out_p = INTER_DIR / fname
        im.save(out_p)
        print("Saved V2 styleframe:", out_p)

def render_segment_worker(args):
    seg_idx, start_f, end_f = args
    out_seg = PROJ_DIR / f"v2_seg_{seg_idx:02d}.mp4"
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-",
        "-vf", "scale=1920:1080:flags=fast_bilinear,format=yuv420p",
        "-an", "-c:v", "libx264", "-preset", "ultrafast", "-tune", "animation",
        "-crf", "20", "-threads", "1",
        str(out_seg)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, bufsize=8 * 1024 * 1024)
    t0 = time.time()
    for fidx in range(start_f, end_f):
        im = render_frame(fidx)
        proc.stdin.write(im.tobytes())
        if (fidx - start_f) % 900 == 0 and fidx > start_f:
            el = time.time() - t0
            print(f"[V2 Worker {seg_idx}] Frame {fidx}/{end_f} ({(fidx-start_f)/el:.1f} fps)", flush=True)
    proc.stdin.close()
    ret = proc.wait()
    if ret != 0:
        raise RuntimeError(f"V2 Segment {seg_idx} failed with code {ret}")
    print(f"[V2 Worker {seg_idx}] Completed {out_seg} in {time.time() - t0:.1f}s", flush=True)
    return str(out_seg)

def render_full_video():
    step = TOTAL_FRAMES // 4
    tasks = [
        (0, 0, step),
        (1, step, step * 2),
        (2, step * 2, step * 3),
        (3, step * 3, TOTAL_FRAMES),
    ]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=2) as ex:
        seg_files = list(ex.map(render_segment_worker, tasks))

    concat_list = PROJ_DIR / "v2_concat_list.txt"
    concat_list.write_text("".join(f"file '{p}'\n" for p in seg_files))

    final_mp4 = OUT_DIR / "Seni_Mengira_Cukup_Animasi_Penuh.mp4"
    master_wav = PROJ_DIR / "master_audio.wav"
    cmd_mux = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-i", str(master_wav),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-shortest", "-movflags", "+faststart",
        str(final_mp4)
    ]
    subprocess.run(cmd_mux, check=True)
    print(f"FINAL V2 MP4 READY: {final_mp4} (Total render time: {time.time() - t0:.1f}s)")


def configure_project(project_dir, intermediate_dir, out_dir):
    """Load the optional original project only after its paths were supplied."""
    global PROJ_DIR, INTER_DIR, OUT_DIR, FONT_SANS, FONT_BOLD, FONT_ARABIC, NORM_RMS, TOTAL_FRAMES, DURATION
    PROJ_DIR = Path(project_dir).resolve()
    INTER_DIR = Path(intermediate_dir).resolve()
    OUT_DIR = Path(out_dir).resolve()
    meta = json.loads((PROJ_DIR / "fonts.json").read_text())
    fonts = {}
    for key in ("sans", "bold", "arabic"):
        f = Path(meta[key])
        f = f if f.is_absolute() else PROJ_DIR / f
        if not f.is_file():
            raise ValueError("Missing project font: " + str(f))
        fonts[key] = str(f)
    FONT_SANS, FONT_BOLD, FONT_ARABIC = (fonts[k] for k in ("sans", "bold", "arabic"))
    get_font.cache_clear()
    NORM_RMS = np.load(INTER_DIR / "vo_norm_rms_30fps.npy", allow_pickle=False)
    if NORM_RMS.ndim != 1 or not len(NORM_RMS) or not np.all(np.isfinite(NORM_RMS)):
        raise ValueError("RMS must be a nonempty finite one-dimensional array")
    TOTAL_FRAMES = len(NORM_RMS)
    DURATION = TOTAL_FRAMES / FPS
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def demo_frame(t, duration=4.0, width=1280, height=720):
    """Original neutral camera demo. Project roles below are not the L/P bank IDs."""
    im = Image.new("RGB", (width, height), C_CREAM)
    u = clamp(t / duration)
    zoom = 1.0 + 0.7 * smoothstep(.3, .9, u)
    cam = CamCanvas(im, lerp(640, 750, smoothstep(.3, .9, u)), 360, zoom)
    cam.rect((-500, 585, 1800, 1000), fill=C_CREAM_DARK)
    draw_tree(cam, 150, 590, .8, t)
    draw_potted_plant(cam, 1010, 590, 1.0, t)
    views = ("front", "three_quarter_right", "side_right", "back", "side_left", "three_quarter_left")
    view = views[min(5, int(u * 6))]
    draw_character(cam, 570, 590, 1.0, t, role="amir", pose="stand", view=view, lanyard=False)
    draw_character(cam, 760, 590, .88, t, role="mak", pose="phone_call", view="three_quarter_left", lanyard=False)
    cam.rect((895, 468, 951, 505), fill=C_GOLD, outline=C_INK, radius=5)
    return im


def main():
    ap = argparse.ArgumentParser(description="Reusable Pillow vector camera/IK and optional original storytelling project")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--demo", action="store_true", help="Render a standalone silent vector camera MP4")
    mode.add_argument("--frame", action="store_true", help="Render one standalone demo PNG")
    mode.add_argument("--test-styleframes", action="store_true", help="Original project: requires explicit project files")
    mode.add_argument("--render-full", action="store_true", help="Original 16-scene project: requires explicit project files and master_audio.wav")
    ap.add_argument("--output", type=Path)
    ap.add_argument("--duration", type=float, default=4.0)
    ap.add_argument("--time", type=float, default=1.0)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--font-sans", type=Path)
    ap.add_argument("--font-bold", type=Path)
    ap.add_argument("--project-dir", type=Path)
    ap.add_argument("--intermediate-dir", type=Path)
    ap.add_argument("--out-dir", type=Path)
    a = ap.parse_args()
    if not any((a.demo,a.frame,a.test_styleframes,a.render_full)):
        ap.print_help();return
    if not math.isfinite(a.duration) or not 0 < a.duration <= 1800 or not 1 <= a.fps <= 120:
        ap.error("duration must be finite in (0,1800]; fps in [1,120]")
    if not math.isfinite(a.time):ap.error("time must be finite")
    if not 2 <= a.width <= 4096 or not 2 <= a.height <= 4096:ap.error("width/height must be2..4096")
    global FONT_SANS,FONT_BOLD
    if a.font_sans:FONT_SANS=str(a.font_sans.resolve())
    if a.font_bold:FONT_BOLD=str(a.font_bold.resolve())
    get_font.cache_clear()
    if a.demo or a.frame:
        if not a.output:ap.error("--output is required")
        if a.frame:
            if a.output.suffix.lower()!='.png':ap.error("--frame output must be .png")
            a.output.parent.mkdir(parents=True,exist_ok=True)
            demo_frame(a.time,a.duration,a.width,a.height).save(a.output)
        else:
            if a.width%2 or a.height%2 or a.output.suffix.lower()!='.mp4':ap.error("MP4 requires even dimensions and .mp4 output")
            a.output.parent.mkdir(parents=True,exist_ok=True)
            tmp=a.output.with_name('.'+a.output.stem+'.part.mp4')
            cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{a.width}x{a.height}','-r',str(a.fps),'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart',str(tmp)]
            proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
            try:
                for i in range(math.ceil(a.duration*a.fps)):
                    proc.stdin.write(demo_frame(i/a.fps,a.duration,a.width,a.height).tobytes())
                proc.stdin.close()
                if proc.wait()!=0:raise RuntimeError("FFmpeg failed")
                tmp.replace(a.output)
            except BaseException:
                proc.kill();proc.wait();tmp.unlink(missing_ok=True);raise
        print(a.output.resolve());return
    if not all((a.project_dir,a.intermediate_dir,a.out_dir)):
        ap.error("Original example requires --project-dir, --intermediate-dir and --out-dir")
    if a.fps!=30:ap.error("Original example uses its30fps RMS timeline")
    configure_project(a.project_dir,a.intermediate_dir,a.out_dir)
    if a.render_full and not (PROJ_DIR/'master_audio.wav').is_file():ap.error("Missing master_audio.wav")
    if a.test_styleframes:test_styleframes()
    if a.render_full:render_full_video()


if __name__ == "__main__":
    main()
