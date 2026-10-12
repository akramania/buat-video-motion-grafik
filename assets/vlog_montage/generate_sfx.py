#!/usr/bin/env python3
"""Build 100 original, deterministic, sample-free vlog/montage sound effects.

Requires numpy, scipy and Pillow. PCM audio is stereo, 48 kHz, 16-bit.
Foley names describe stylized synthesized gestures, never recorded samples.
"""
from __future__ import annotations

import hashlib
import json
import math
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.signal import butter, sosfilt

ROOT = Path(__file__).resolve().parent
RATE = 48000
FAMILIES = [
    ("air-whoosh", "Air Whoosh", "transition", ["Quick Air", "Double Sweep", "Wide Soft Air", "Low Wind Sweep", "Long Lift"]),
    ("swish", "Swish", "transition", ["Fine Brush", "Twin Flick", "Bright Brush", "Soft Fabric", "Triple Brush"]),
    ("riser", "Riser", "build-up", ["Short Lift", "Stepped Lift", "Shimmer Lift", "Bass Lift", "Accelerating Lift"]),
    ("bass-impact", "Bass Impact", "impact", ["Tight Sub", "Double Thump", "Metallic Thump", "Soft Sub Drop", "Deep Tail"]),
    ("soft-hit", "Soft Hit", "impact", ["Muted Knock", "Twin Knock", "Wooden Tap", "Felt Tap", "Three Soft Taps"]),
    ("pop", "Pop", "graphic-accent", ["Bubble Pop", "Twin Bubbles", "Bright Drop", "Rounded Pop", "Bubble Cascade"]),
    ("ui-click", "UI Click", "interface", ["Small Select", "Double Select", "Glass Select", "Soft Toggle", "Triple Select"]),
    ("notification", "Notification", "interface", ["Gentle Ping", "Two Note Alert", "Bright Bell", "Warm Reminder", "Three Note Success"]),
    ("camera-shutter", "Camera Shutter", "camera", ["Compact Snap", "Double Shot", "Crisp Snap", "Soft Mirror Snap", "Burst Capture"]),
    ("page-flip", "Page Flip", "storytelling", ["Single Turn", "Double Turn", "Crisp Paper", "Soft Page", "Notebook Shuffle"]),
    ("typing", "Typing", "storytelling", ["Short Word", "Two Word Rhythm", "Crisp Keyboard", "Soft Keys", "Fast Sentence"]),
    ("ticking", "Ticking", "rhythm", ["Two Ticks", "Four Tick Count", "Bright Timer", "Muted Clock", "Accelerating Timer"]),
    ("reverse-swell", "Reverse Swell", "transition", ["Short Reverse", "Twin Reverse", "Shimmer Reverse", "Low Reverse", "Reverse To Hit"]),
    ("glitch", "Glitch", "digital", ["Data Skip", "Double Dropout", "Bright Pixel Tear", "Low Buffer", "Fragment Burst"]),
    ("digital-scan", "Digital Scan", "digital", ["Quick Scan", "Double Scan", "Laser Sweep", "Low Scanner", "Progress Scan"]),
    ("transition-accent", "Transition Accent", "transition", ["Swoop Tap", "Two Beat Cut", "Spark Cut", "Soft Slide Tap", "Three Beat Reveal"]),
    ("sparkle", "Sparkle", "graphic-accent", ["Single Twinkle", "Twin Stars", "Bright Glimmer", "Warm Shine", "Star Cascade"]),
    ("tape-stop", "Tape Stop", "digital", ["Quick Stop", "Stutter Stop", "Bright Reel Stop", "Low Reel Stop", "Slow Reel Stop"]),
    ("whip", "Whip", "transition", ["Fast Whip", "Double Whip", "Sharp Whip", "Soft Whip", "Whip And Snap"]),
    ("cinematic-boom", "Cinematic Boom", "impact", ["Short Boom", "Two Stage Boom", "Bright Cinematic Hit", "Warm Low Boom", "Wide Boom Tail"]),
]


def filtered_noise(rng, n, low, high):
    raw = rng.standard_normal(n)
    low = max(25.0, float(low))
    high = min(RATE * .46, float(high))
    if low >= high:
        low = high * .25
    sos = butter(3, [low, high], fs=RATE, btype="bandpass", output="sos")
    y = sosfilt(sos, raw)
    return y / max(float(np.std(y)), 1e-9)


def tone(t, frequency, start_frequency=None, harmonics=0):
    if start_frequency is None:
        phase = 2 * np.pi * frequency * t
    else:
        slope = (frequency - start_frequency) / max(float(t[-1]), 1 / RATE)
        phase = 2 * np.pi * (start_frequency * t + .5 * slope * t * t)
    y = np.sin(phase)
    for h in range(2, harmonics + 2):
        y += np.sin(h * phase) * (.23 / h)
    return y


def add_event(out, start, event):
    at = max(0, int(round(start * RATE)))
    count = min(len(event), len(out) - at)
    if count > 0:
        out[at:at + count] += event[:count]


def soft_edges(n, fade=.007):
    edge = min(int(RATE * fade), n // 3)
    e = np.ones(n)
    if edge > 0:
        ramp = np.sin(np.linspace(0, np.pi / 2, edge)) ** 2
        e[:edge] = ramp
        e[-edge:] = ramp[::-1]
    e[0] = e[-1] = 0
    return e


def decaying_note(duration, freq, decay, rng, noise=0, harmonic=0):
    t = np.arange(max(48, round(duration * RATE))) / RATE
    y = tone(t, freq, harmonics=harmonic)
    if noise:
        y += noise * filtered_noise(rng, len(t), 800, 9000)
    envelope = (1 - np.exp(-t / .0012)) * np.exp(-t / decay)
    return y * envelope * soft_edges(len(t), .004)


def synthesize(family, variant, ordinal):
    """Variant changes event structure, envelope, frequency range and texture."""
    rng = np.random.default_rng(860000 + ordinal)
    v = variant
    bright = [1.0, .9, 1.8, .58, 1.16][v]
    count = [1, 2, 1, 1, 3][v]
    if family in {"air-whoosh", "swish", "whip", "page-flip"}:
        durations = {
            "air-whoosh": [.52, .94, .67, .86, 1.28],
            "swish": [.28, .57, .32, .49, .83],
            "whip": [.24, .52, .28, .39, .68],
            "page-flip": [.36, .74, .39, .54, 1.06],
        }
        duration = durations[family][v]
        y = np.zeros(round(duration * RATE))
        spacing = duration / (count + .2)
        for k in range(count):
            length = spacing * .92
            t = np.arange(round(length * RATE)) / RATE
            progress = t / max(t[-1], .001)
            noise = filtered_noise(rng, len(t), 160 * bright, min(16000, 6400 * bright))
            env = np.sin(np.pi * progress) ** (1.5 if family == "air-whoosh" else 3.0)
            modulation = .65 + .35 * np.sin(2 * np.pi * (2 + 4 * progress) * t)
            event = noise * env * modulation
            if family == "whip":
                event += .35 * tone(t, 1000 * bright, 160 * bright) * env
                event += .25 * filtered_noise(rng, len(t), 2200, 17000) * np.exp(-((progress - .74) / .065) ** 2)
            elif family == "page-flip":
                event *= .6 + .4 * np.sin(2 * np.pi * (26 + v * 7) * t) ** 2
                event += .22 * filtered_noise(rng, len(t), 1400, 14000) * np.exp(-((progress - .63) / .024) ** 2)
            elif family == "swish":
                event *= .75 + .25 * np.sin(2 * np.pi * (55 + 15 * v) * t)
            add_event(y, k * spacing, event)
        if family == "whip" and v == 4:
            add_event(y, duration * .75, decaying_note(.15, 640, .025, rng, .7))
    elif family in {"riser", "reverse-swell"}:
        duration = ([.85, 1.4, 1.2, 1.8, 2.3] if family == "riser" else [.6, 1.05, .9, 1.3, 1.6])[v]
        t = np.arange(round(duration * RATE)) / RATE
        p = t / duration
        y = tone(t, 900 * bright, 100 * bright, 2) * p ** 1.9
        y += filtered_noise(rng, len(t), 180 * bright, 8000 * bright) * p ** 2.7 * .5
        if v == 1:
            y *= .5 + .5 * np.sin(2 * np.pi * 3 * t) ** 2
        if v == 2:
            y += tone(t, 4200, 1300, 1) * p ** 2 * .32
        if v == 4:
            y *= .35 + .65 * np.sin(2 * np.pi * (2 * t + 4 * t * t)) ** 2
        if family == "reverse-swell":
            note = decaying_note(duration, 280 * bright, duration * .21, rng, .5, 3)[::-1]
            y = .55 * y + note
            if v == 1:
                midpoint = len(y) // 2
                y[:midpoint] *= soft_edges(midpoint, .018)
                y[midpoint:] *= soft_edges(len(y) - midpoint, .018)
            if v == 4:
                y *= np.clip((duration - .2 - t) / .08, 0, 1)
                add_event(y, duration - .23, decaying_note(.23, 95, .065, rng, .15, 1))
    elif family in {"bass-impact", "soft-hit", "pop", "ui-click", "notification", "sparkle", "cinematic-boom"}:
        duration_sets = {
            "bass-impact": [.48, .83, .62, .78, 1.18],
            "soft-hit": [.2, .4, .26, .31, .65],
            "pop": [.2, .44, .27, .33, .7],
            "ui-click": [.14, .29, .19, .24, .46],
            "notification": [.7, 1.02, .95, 1.12, 1.48],
            "sparkle": [.66, .98, .86, 1.0, 1.48],
            "cinematic-boom": [.92, 1.46, 1.12, 1.5, 2.6],
        }
        duration = duration_sets[family][v]
        y = np.zeros(round(duration * RATE))
        event_count = count if family not in {"notification", "sparkle"} else [1, 2, 2, 1, 4][v]
        for k in range(event_count):
            start = k * min(duration / (event_count + 1), .22)
            available = duration - start
            t = np.arange(round(available * RATE)) / RATE
            if family == "bass-impact":
                freq = 45 * bright * (1 + .1 * k)
                e = np.exp(-t / (.08 + .055 * v)) * (1 - np.exp(-t / .001))
                phase = 2 * np.pi * (freq * t + (110 * bright - freq) * .016 * (1 - np.exp(-t / .016)))
                event = np.sin(phase) * e
                event += .18 * filtered_noise(rng, len(t), 500, 6000 * bright) * np.exp(-t / .012)
                if v == 2:
                    event += .3 * tone(t, 330, harmonics=3) * np.exp(-t / .055)
            elif family == "cinematic-boom":
                freq = 38 * bright
                phase = 2 * np.pi * (freq * t + 55 * .05 * (1 - np.exp(-t / .05)))
                event = np.sin(phase) * np.exp(-t / (.18 + .16 * v))
                event += .55 * filtered_noise(rng, len(t), 70, 3500 * bright) * np.exp(-t / (.06 + .05 * v))
                event += .16 * tone(t, 140 * bright, harmonics=2) * np.exp(-t / (.16 + .07 * v))
            elif family == "soft-hit":
                event = decaying_note(available, 230 * bright, .015 + .005 * v, rng, .35, 2)
                event += .15 * tone(t, 710 * bright) * np.exp(-t / .011)
            elif family == "pop":
                freq = 430 * bright * (1 + .18 * k)
                phase = 2 * np.pi * (freq * t + 350 * bright * .02 * (1 - np.exp(-t / .02)))
                event = np.sin(phase) * np.exp(-t / (.025 + v * .006)) * (1 - np.exp(-t / .0007))
            elif family == "ui-click":
                event = decaying_note(available, 1300 * bright * (1 + .25 * k), .012 + .004 * v, rng, .18, 2)
                event += filtered_noise(rng, len(t), 2600, 15000) * np.exp(-t / .004) * .12
            elif family == "notification":
                intervals = [1, 1.25, 1.5, 2]
                event = decaying_note(available, 660 * bright * intervals[k], .11 + .025 * v, rng, 0, 1)
                event += .16 * tone(t, 1742 * bright * intervals[k]) * np.exp(-t / .06)
            else:
                freq = 1200 * bright * [1, 1.25, 1.5, 2][k]
                event = decaying_note(available, freq, .12 + .03 * v, rng, 0, 1)
                event += .4 * tone(t, freq * 2.71) * np.exp(-t / .075)
            add_event(y, start, event * soft_edges(len(event), .003))
    elif family in {"camera-shutter", "typing", "ticking"}:
        duration = {
            "camera-shutter": [.28, .62, .35, .46, 1.12],
            "typing": [.65, 1.14, .8, .94, 1.95],
            "ticking": [.5, .92, .8, 1.1, 1.7],
        }[family][v]
        y = np.zeros(round(duration * RATE))
        if family == "camera-shutter":
            starts = [k * .27 for k in range([1, 2, 1, 1, 4][v])]
        elif family == "typing":
            steps = [5, 9, 6, 7, 16][v]
            starts = [k * (duration - .12) / steps + rng.uniform(0, .014) for k in range(steps)]
        else:
            steps = [2, 4, 3, 4, 8][v]
            p = np.linspace(0, 1, steps)
            starts = (p ** (.68 if v == 4 else 1.0) * (duration - .15)).tolist()
        for k, start in enumerate(starts):
            length = min(.18 if family == "camera-shutter" else .09, duration - start)
            t = np.arange(round(length * RATE)) / RATE
            n = filtered_noise(rng, len(t), 700 * bright, 12000 * min(bright, 1.2))
            event = n * np.exp(-t / (.008 if family == "typing" else .015))
            event += tone(t, (850 if family == "ticking" else 360) * bright * (1 + .05 * (k % 2)), harmonics=2) * np.exp(-t / .012) * .75
            if family == "camera-shutter":
                event += n * np.exp(-((t - .054) / .012) ** 2) * .6
                event += tone(t, 165 * bright) * np.exp(-t / .034) * .33
            add_event(y, start, event * soft_edges(len(t), .002))
    elif family in {"glitch", "digital-scan", "tape-stop", "transition-accent"}:
        duration = {
            "glitch": [.3, .57, .38, .64, 1.0],
            "digital-scan": [.45, .88, .65, .94, 1.3],
            "tape-stop": [.46, .73, .55, .86, 1.45],
            "transition-accent": [.39, .75, .54, .64, 1.04],
        }[family][v]
        t = np.arange(round(duration * RATE)) / RATE
        p = t / duration
        if family == "glitch":
            y = np.zeros(len(t))
            for k in range([3, 5, 4, 5, 9][v]):
                start = duration * .8 * k / [3, 5, 4, 5, 9][v]
                length = duration / (7 + v * 2)
                z = np.arange(round(length * RATE)) / RATE
                freq = (150 + rng.uniform(0, 1100)) * bright
                event = np.tanh(2.8 * tone(z, freq, harmonics=3)) * .5
                event += .2 * filtered_noise(rng, len(z), 1200, 16000)
                event *= soft_edges(len(z), .002) * np.exp(-z / (length * .5))
                add_event(y, start, event)
        elif family == "digital-scan":
            y = tone(t, 1500 * bright, 250 * bright, 1) * np.sin(np.pi * p) ** 1.5
            y *= .65 + .35 * np.sin(2 * np.pi * (12 + 7 * v) * t) ** 2
            y += .08 * filtered_noise(rng, len(t), 2500, 16000) * np.sin(np.pi * p)
            if v in (1, 4):
                y *= .18 + .82 * np.sin(2 * np.pi * (2 if v == 1 else 4) * p) ** 4
        elif family == "tape-stop":
            freq = 310 * bright * np.maximum(1 - p, 0) ** (1.5 + .25 * v) + 28
            phase = 2 * np.pi * np.cumsum(freq) / RATE
            y = (np.sin(phase) + .22 * np.sin(2 * phase) + .1 * np.sin(3 * phase)) * (1 - p) ** .8
            if v == 1:
                y *= .2 + .8 * np.sin(2 * np.pi * 7 * t) ** 4
            y += .04 * filtered_noise(rng, len(t), 500, 8000) * (1 - p)
        else:
            y = np.zeros(len(t))
            for k in range(count):
                start = k * duration / (count + .25)
                length = min(duration / (count + .1), duration - start)
                z = np.arange(round(length * RATE)) / RATE
                q = z / length
                event = filtered_noise(rng, len(z), 200, 6000 * bright) * np.sin(np.pi * q) ** 2 * .5
                event += tone(z, 750 * bright, 180 * bright) * np.sin(np.pi * q) ** 3 * .25
                add_event(y, start, event)
                add_event(y, start + length * .7, decaying_note(min(.12, duration - start - length * .7), 420 * bright, .018, rng, .18))
    else:
        raise ValueError(family)

    # Gentle stereo spread: preserve a centered core; no artificial hard pans.
    n = len(y)
    delay = max(1, round((.0014 + .00035 * v) * RATE))
    delayed = np.zeros_like(y)
    delayed[delay:] = y[:-delay]
    common_envelope = np.sqrt(np.maximum(sosfilt(butter(1, 22, fs=RATE, output="sos"), y * y), 0))
    side = filtered_noise(rng, n, 600, 10000) * common_envelope * .018
    stereo = np.column_stack((y + side, .9 * y + .1 * delayed - side))
    edge = soft_edges(n, .009 if duration > .4 else .004)
    stereo *= edge[:, None]
    # Weighted DC removal leaves the fade boundaries exactly at zero.
    stereo -= edge[:, None] * (stereo.mean(axis=0) / max(edge.mean(), 1e-9))[None, :]
    rms = float(np.sqrt(np.mean(stereo ** 2)))
    stereo *= .13 / max(rms, 1e-9)
    stereo *= min(1.0, .84 / max(float(np.max(np.abs(stereo))), 1e-9))
    stereo[0] = stereo[-1] = 0
    pcm = np.round(np.clip(stereo, -.84, .84) * 32767).astype("<i2")
    return pcm


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = Path("/usr/share/fonts/truetype/dejavu") / name
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default()


def preview(pcm, record, path):
    image = Image.new("RGB", (640, 360), "#101723")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((20, 20, 620, 340), radius=22, fill="#172131", outline="#2d3e52", width=2)
    draw.text((40, 38), record["id"] + " / ORIGINAL AUDIO", font=font(15, True), fill="#72d9cf")
    title = record["title"]
    title_font = font(25, True)
    while draw.textlength(title, font=title_font) > 552:
        size = title_font.size - 1
        title_font = font(size, True)
    draw.text((40, 76), title, font=title_font, fill="#eff7ff")
    draw.text((40, 113), record["category"].replace("-", " ").upper(), font=font(13), fill="#93a9c1")
    draw.line((40, 217, 598, 217), fill="#36495e", width=1)
    mono = pcm.astype(np.float64).mean(axis=1) / 32768
    bins = np.array_split(mono, 280)
    heights = [max(1, int(np.max(np.abs(b)) * 73 / .84)) for b in bins]
    for i, h in enumerate(heights):
        x = 40 + 2 * i
        draw.line((x, 217 - h, x, 217 + h), fill="#72d9cf" if i % 5 else "#a8eae2", width=1)
    draw.text((40, 306), f'{record["duration"]:.2f} s  •  48 kHz / 16-bit stereo', font=font(14), fill="#b5c6d7")
    image.save(path, "WEBP", quality=88, method=6)


def main():
    (ROOT / "sfx").mkdir(parents=True, exist_ok=True)
    (ROOT / "previews" / "sfx").mkdir(parents=True, exist_ok=True)
    records, qa_rows = [], []
    hashes = set()
    for family_number, (slug, family_title, category, variants) in enumerate(FAMILIES):
        for variant, label in enumerate(variants):
            ordinal = family_number * 5 + variant
            ident = f"VL{501 + ordinal:04d}"
            pcm = synthesize(slug, variant, ordinal)
            target = ROOT / "sfx" / (ident + ".wav")
            with wave.open(str(target), "wb") as wav:
                wav.setnchannels(2)
                wav.setsampwidth(2)
                wav.setframerate(RATE)
                wav.writeframes(pcm.tobytes())
            duration = len(pcm) / RATE
            if category == "transition":
                uses = ["Accent a montage cut or reveal", "Support a vlog scene transition"]
            elif category == "camera":
                uses = ["Photo freeze frame", "Camera or memory montage graphic"]
            elif category == "rhythm":
                uses = ["Countdown and time jump", "Rhythmic vlog montage punctuation"]
            elif category == "interface":
                uses = ["Phone or app overlay", "On-screen selection or notification"]
            elif category == "storytelling":
                uses = ["Journal, chapter or caption reveal", "Travel diary and vlog storytelling"]
            elif category == "build-up":
                uses = ["Build into a montage reveal", "Raise anticipation before a scene change"]
            else:
                uses = ["Accent a title or graphic reveal", "Punctuate a vlog or promotional montage"]
            record = {
                "id": ident, "type": "sfx", "title": f"{family_title} — {label}",
                "category": category, "tags": ["vlog", "montage", "original", "synthesized", slug, label.lower()],
                "use_cases": uses, "format": "wav", "file": f"sfx/{ident}.wav",
                "preview": f"previews/sfx/{ident}.webp", "duration": round(duration, 6),
                "technical": {"sample_rate": RATE, "channels": 2, "bit_depth": 16, "encoding": "PCM signed little-endian", "provenance": "Original deterministic synthesis; no external samples", "intended_use": "Spot sound effect; lower gain to suit dialogue and music"},
            }
            preview(pcm, record, ROOT / record["preview"])
            with wave.open(str(target), "rb") as wav:
                assert (wav.getframerate(), wav.getnchannels(), wav.getsampwidth()) == (48000, 2, 2)
                reloaded = np.frombuffer(wav.readframes(wav.getnframes()), dtype="<i2").reshape(-1, 2)
                assert np.array_equal(reloaded, pcm)
            signal = reloaded.astype(np.float64) / 32768
            peak = float(np.max(np.abs(signal)))
            rms = float(np.sqrt(np.mean(signal ** 2)))
            dc = float(np.max(np.abs(signal.mean(axis=0))))
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            assert digest not in hashes, ident
            hashes.add(digest)
            assert .1 <= duration <= 3, (ident, duration)
            assert np.isfinite(signal).all() and rms > .01
            assert peak <= 10 ** (-1 / 20) and not (np.abs(reloaded) >= 32767).any()
            assert dc < .00005, (ident, dc)
            assert not reloaded[0].any() and not reloaded[-1].any()
            qa_rows.append({"id": ident, "frames": len(signal), "duration": duration, "peak_dbfs": round(20 * math.log10(peak), 4), "rms_dbfs": round(20 * math.log10(rms), 4), "max_channel_dc": dc, "endpoints_zero": True, "sha256": digest})
            records.append(record)
    assert len(records) == len(hashes) == 100
    (ROOT / "index_sfx.json").write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n")
    report = {
        "count": 100, "family_count": 20, "variants_per_family": 5,
        "all_pcm_headers_verified": True, "all_sample_data_reloaded": True,
        "unique_sha256": len(hashes), "duration_range_seconds": [min(r["duration"] for r in qa_rows), max(r["duration"] for r in qa_rows)],
        "highest_peak_dbfs": max(r["peak_dbfs"] for r in qa_rows), "lowest_rms_dbfs": min(r["rms_dbfs"] for r in qa_rows),
        "max_channel_dc": max(r["max_channel_dc"] for r in qa_rows), "all_endpoints_zero": True,
        "sample_provenance": "Original synthesized audio, no third-party samples",
        "validation_limitations": "Signal-level and waveform QA; subjective audition of every effect was not performed.",
        "files": qa_rows,
    }
    (ROOT / "sfx_qa.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "files"}, indent=2))


if __name__ == "__main__":
    main()
