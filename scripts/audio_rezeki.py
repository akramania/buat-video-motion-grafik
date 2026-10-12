#!/usr/bin/env python3
"""Original 160-second score and sound effects for 8 Pintu Rezeki.

No samples, soundfonts, downloads, or copyrighted melodies are used. Every
instrument and effect is generated from oscillators and seeded noise. Scene
boundaries follow the 12 + 8*16 + 20 second motion graphic edit.

Usage:
    python3 audio_rezeki.py
    python3 audio_rezeki.py --output output/custom.wav
"""

from __future__ import annotations

import argparse
import math
import wave
from pathlib import Path

import numpy as np
from scipy.signal import lfilter


SR = 44_100
DURATION = 160.0
SCENE_STARTS = [12.0 + 16.0 * i for i in range(8)]
OUTRO = 140.0
BPM = 100.0
BEAT = 60.0 / BPM

# In MIDI note numbers. D major / B minor with a reflective middle passage.
CHORDS = [
    [(59, 62, 66, 69), (55, 59, 62, 66), (50, 54, 57, 62)],
    [(55, 59, 62, 66), (50, 54, 57, 62), (57, 61, 64, 69), (59, 62, 66, 69)],
    [(50, 54, 57, 62), (57, 61, 64, 69), (59, 62, 66, 69), (55, 59, 62, 66)],
    [(55, 59, 62, 66), (57, 61, 64, 69), (50, 54, 57, 62), (59, 62, 66, 69)],
    [(59, 62, 66, 69), (55, 59, 62, 66), (50, 54, 57, 62), (57, 61, 64, 69)],
    [(52, 55, 59, 64), (59, 62, 66, 69), (55, 59, 62, 66), (57, 61, 64, 69)],
    [(55, 59, 62, 66), (50, 54, 57, 62), (52, 55, 59, 64), (57, 61, 64, 69)],
    [(50, 54, 57, 62), (55, 59, 62, 66), (59, 62, 66, 69), (57, 61, 64, 69)],
    [(50, 54, 57, 62), (57, 61, 64, 69), (55, 59, 62, 66), (50, 54, 57, 62)],
    [(59, 62, 66, 69), (55, 59, 62, 66), (50, 54, 57, 62), (57, 61, 64, 69), (50, 54, 57, 62)],
]


def hz(midi: int | float) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12.0)


class Mixer:
    def __init__(self, duration: float = DURATION, sr: int = SR, seed: int = 20260924):
        self.sr = sr
        self.length = int(round(duration * sr))
        self.audio = np.zeros((self.length, 2), dtype=np.float32)
        self.rng = np.random.default_rng(seed)

    def put(self, x: np.ndarray, at: float, gain: float = 1.0, pan: float = 0.0):
        """pan -1 left, 0 center, +1 right; equal-power law."""
        start = round(at * self.sr)
        if start >= self.length or start + len(x) <= 0:
            return
        xx = np.asarray(x, dtype=np.float32)
        low = max(0, -start)
        high = min(len(xx), self.length - start)
        if low >= high:
            return
        p = np.clip(pan, -1.0, 1.0)
        left = math.cos((p + 1.0) * math.pi / 4.0)
        right = math.sin((p + 1.0) * math.pi / 4.0)
        self.audio[max(start, 0):start + high, 0] += xx[low:high] * (gain * left)
        self.audio[max(start, 0):start + high, 1] += xx[low:high] * (gain * right)

    def note(self, at: float, midi: int, seconds: float, instr: str,
             gain: float = 0.1, pan: float = 0.0):
        n = max(4, round(seconds * self.sr))
        t = np.arange(n, dtype=np.float32) / self.sr
        f = hz(midi)
        phase = 2 * math.pi * f * t
        if instr == 'wood':
            # Marimba-like struck bar, with fading harmonics and a tiny click.
            env = (1 - np.exp(-t / .003)) * np.exp(-t / .23)
            carrier = (np.sin(phase) + .30 * np.sin(2.01 * phase) * np.exp(-t / .11)
                       + .13 * np.sin(3.93 * phase) * np.exp(-t / .055))
            x = carrier * env
        elif instr == 'kalimba':
            env = (1 - np.exp(-t / .002)) * np.exp(-t / .38)
            carrier = (.85 * np.sin(phase) + .22 * np.sin(2.02 * phase) * np.exp(-t / .09)
                       + .12 * np.sin(4.09 * phase) * np.exp(-t / .04))
            x = carrier * env
        elif instr == 'bell':
            env = (1 - np.exp(-t / .002)) * np.exp(-t / .76)
            x = env * (.72 * np.sin(phase) + .22 * np.sin(2.76 * phase) * np.exp(-t / .31)
                       + .13 * np.sin(5.38 * phase) * np.exp(-t / .15))
        elif instr == 'flute':
            vibrato = .003 * np.sin(2 * math.pi * 5.0 * t)
            wave_ = np.sin(phase + vibrato) + .10 * np.sin(2 * phase)
            env = (1 - np.exp(-t / .085)) * np.minimum(1.0, (seconds - t) / .20)
            x = wave_ * np.clip(env, 0, 1)
        elif instr == 'pad':
            # Slow soft harmonics, detuned across the stereo field later.
            x = (np.sin(phase) + .13 * np.sin(2 * phase) + .06 * np.sin(3 * phase))
            attack = 1 - np.exp(-t / .42)
            release = np.minimum(1, np.maximum(0, seconds - t) / .48)
            x *= attack * release
        elif instr == 'bass':
            x = (np.sin(phase) + .20 * np.sin(2 * phase))
            x *= (1 - np.exp(-t / .012)) * np.exp(-t / 1.0)
        else:
            raise ValueError(instr)
        self.put(x, at, gain, pan)

    def pop(self, at: float, pan: float = 0, pitch: float = 1.0,
            gain: float = .07):
        n = round(.19 * self.sr)
        t = np.arange(n, dtype=np.float32) / self.sr
        # Bouncy bubble pop: descending pitched sine and short noise tick.
        phase = 2 * math.pi * ((390 * pitch) * t - 130 * pitch * t * t)
        x = (np.sin(phase) * np.exp(-t * 22.0)
             + self.rng.standard_normal(n).astype('float32') * np.exp(-t * 120) * .15)
        self.put(x, at, gain, pan)

    def kick(self, at: float, gain: float = .08):
        n = round(.30 * self.sr)
        t = np.arange(n, dtype=np.float32) / self.sr
        phase = 2 * math.pi * (58 * t + 40 * .035 * (1 - np.exp(-t / .035)))
        x = np.sin(phase) * np.exp(-t * 17)
        self.put(x, at, gain, 0)

    def brush(self, at: float, gain: float = .040, pan: float = 0):
        n = round(.22 * self.sr)
        t = np.arange(n, dtype=np.float32) / self.sr
        noise = self.rng.standard_normal(n).astype('float32')
        # Gentle frame drum / brushed snare with low woody body.
        high = noise - lfilter([.018], [1, -.982], noise).astype('float32')
        x = .42 * high * np.exp(-t * 33) + .48 * np.sin(2 * math.pi * 180 * t) * np.exp(-t * 18)
        self.put(x, at, gain, pan)

    def shaker(self, at: float, gain: float = .016, pan: float = 0):
        n = round(.12 * self.sr)
        t = np.arange(n, dtype=np.float32) / self.sr
        noise = self.rng.standard_normal(n).astype('float32')
        high = noise - lfilter([.025], [1, -.975], noise).astype('float32')
        x = high * np.exp(-t * 42)
        self.put(x, at, gain, pan)

    def whoosh(self, at: float, dur: float = .62, gain: float = .045,
               pan_start: float = -.55, pan_end: float = .55):
        n = round(dur * self.sr)
        t = np.arange(n, dtype=np.float32) / self.sr
        noise = self.rng.standard_normal(n).astype('float32')
        smooth = lfilter([.15], [1, -.85], noise).astype('float32')
        body = noise * .21 + smooth * .6
        env = np.sin(np.pi * np.arange(n, dtype=np.float32) / n) ** 1.8
        x = body * env
        # Pan actually moves through the sweep rather than remaining fixed.
        start = round(at * self.sr)
        a = max(0, start)
        b = min(self.length, start + n)
        if b <= a:
            return
        lo = a - start
        hi = lo + b - a
        p = np.linspace(pan_start, pan_end, n, dtype=np.float32)[lo:hi]
        self.audio[a:b, 0] += x[lo:hi] * gain * np.cos((p + 1) * np.pi / 4)
        self.audio[a:b, 1] += x[lo:hi] * gain * np.sin((p + 1) * np.pi / 4)

    def door(self, at: float, index: int):
        # Doors open over roughly .8 s in picture.
        lr = -.55 if index % 2 == 0 else .55
        self.whoosh(at + .01, dur=.57, gain=.10, pan_start=lr, pan_end=-lr)
        self.pop(at + .37, pan=lr * .6, pitch=.72, gain=.11)
        self.pop(at + .48, pan=-lr * .6, pitch=.81, gain=.08)
        note = [74, 78, 81, 69, 74, 76, 78, 81][index]
        self.note(at + .64, note, 1.4, 'bell', gain=.092, pan=lr * .25)

    def bird(self, at: float, pan: float = .4, gain: float = .09):
        # A short original FM chirp, rising then falling in two phrases.
        sr = self.sr
        for offset, base, sweep in ((0.0, 1230., 520.), (.145, 1500., -310.)):
            n = round(.13 * sr)
            t = np.arange(n, dtype=np.float32) / sr
            freq = base + sweep * t / .13
            phi = 2 * math.pi * np.cumsum(freq) / sr
            x = (np.sin(phi) + .18 * np.sin(phi * 2)) * np.sin(np.pi * t / .13) ** 2
            self.put(x, at + offset, gain, pan)

    def rain(self, start: float, seconds: float, gain: float = .012):
        n = round(seconds * self.sr)
        t = np.arange(n, dtype=np.float32) / self.sr
        fade = np.minimum(1, t / .9) * np.minimum(1, (seconds - t) / .9)
        for pan in (-.6, .6):
            white = self.rng.standard_normal(n).astype('float32')
            filtered = lfilter([.019], [1, -.981], white).astype('float32')
            self.put(filtered * fade, start, gain, pan)
        for k in range(46):
            when = start + self.rng.uniform(.3, seconds - .35)
            n_midi = int(self.rng.choice([86, 88, 90, 93, 95]))
            self.note(when, n_midi, .28, 'kalimba', gain=.009, pan=float(self.rng.uniform(-.9,.9)))

    def finish(self):
        # Quiet, short stereo ambience made by delay, with no external sample.
        wet = self.audio.copy()
        delay_l = round(.231 * self.sr)
        delay_r = round(.281 * self.sr)
        self.audio[delay_l:, 0] += .16 * wet[:-delay_l, 1]
        self.audio[delay_r:, 1] += .14 * wet[:-delay_r, 0]
        # Smooth saturation catches transients while keeping the score airy.
        self.audio = np.tanh(self.audio * 1.9) / np.tanh(1.9)
        # Music-only social edit: approximately -19 LUFS / -2 dBTP.
        self.audio *= 2.26
        max_amp = float(np.max(np.abs(self.audio)))
        if max_amp > .93:
            self.audio *= .93 / max_amp
        # Final one-second taper; room and ambience fade smoothly.
        fade_n = min(round(1.4 * self.sr), len(self.audio))
        self.audio[-fade_n:] *= np.linspace(1, 0, fade_n, dtype=np.float32)[:, None]

    def write(self, output: Path):
        output.parent.mkdir(parents=True, exist_ok=True)
        pcm = np.int16(np.clip(self.audio, -1, 1) * 32767)
        with wave.open(str(output), 'wb') as f:
            f.setnchannels(2)
            f.setsampwidth(2)
            f.setframerate(self.sr)
            f.writeframes(pcm.tobytes())
        rms = float(np.sqrt(np.mean(self.audio ** 2)))
        peak = float(np.max(np.abs(self.audio)))
        print(f'Wrote {output} | {self.length/self.sr:.2f}s | 44.1 kHz stereo '
              f'| peak {20*math.log10(peak):.1f} dBFS | RMS {20*math.log10(rms):.1f} dBFS')


def build_score(m: Mixer):
    # Scene-shaped bed: 4-second harmony panels, with more energy in the arc.
    ranges = [(0., 12., .57, .35)]
    for i, at in enumerate(SCENE_STARTS):
        soft = (i == 4)
        ranges.append((at, at + 16., .74 if not soft else .49,
                       .73 if i in [1, 2, 6, 7] else .53 if not soft else .24))
    ranges.append((OUTRO, DURATION, .43, .11))

    patterns = [
        [0, 2, 1, 3, 1, 2], [0, 1, 2, 3, 2, 1], [0, 2, 3, 2, 1, 3],
        [0, 1, 3, 2, 1, 0], [0, 2, 1, 2, 3, 1], [0, 2, 3, 1, 2, 3],
        [0, 1, 3, 2, 3, 1], [0, 2, 3, 2, 1, 3],
    ]

    for idx, (start, end, pad_energy, percussion) in enumerate(ranges):
        chord_list = CHORDS[idx]
        # 4 s chord changes match scene artwork's four visual movements.
        chord_span = 4.0
        for ci in range(int(math.ceil((end-start) / chord_span))):
            at = start + ci * chord_span
            if at >= end: break
            chord = chord_list[min(ci, len(chord_list) - 1)]
            hold = min(chord_span + .45, DURATION - at)
            root = chord[0]
            for ni in chord[1:]:
                m.note(at, ni, hold, 'pad', gain=.015 * pad_energy,
                       pan=[-.6, 0, .6][(ni-chord[1]) % 3])
            m.note(at, root - 12, min(1.45, DURATION - at), 'bass',
                   gain=.086 * pad_energy)
            if start <= at + 2.1 < end:
                m.note(at + 2.1, root - 12, min(1.35, DURATION - (at+2.1)),
                       'bass', gain=.048 * pad_energy)

        # Celesta / wood arpeggios, left-to-right call and response.
        tick = 0
        for at in np.arange(start + .2, end - .16, .4):
            chord_index = min(int((at-start)//4.0), len(chord_list)-1)
            chord = chord_list[chord_index]
            note_index = patterns[(idx-1) % 8][tick % 6] if idx in range(1,9) else [0,2,1,3,2,1][tick%6]
            midi = chord[note_index] + (12 if idx == 8 and tick % 8 == 0 else 0)
            if idx == 9:  # Prayer / outro breathes.
                if tick % 3 != 0:
                    tick += 1
                    continue
            if idx == 5 and tick % 2:  # Istighfar is deliberately sparse.
                tick += 1
                continue
            m.note(float(at), midi + 12, .52, 'kalimba',
                   gain=(.026 if idx < 5 else .022) * pad_energy,
                   pan=(-.35 if tick % 2 else .35))
            tick += 1

        # Distinct, memorable 4-second melody phrase on each chapter.
        if 1 <= idx <= 8:
            motif = [0, 2, 1, 3, 2, 1, 0]
            if idx in (2, 7): motif = [0, 1, 2, 3, 2, 3, 1]
            if idx in (4, 5): motif = [2, 1, 0, 1, 2, 3, 1]
            for ci in range(4):
                chord = chord_list[ci]
                t0 = start + ci * 4
                times = [0.28, .87, 1.51, 2.1, 2.56, 3.12, 3.56]
                for ni, pos in enumerate(times):
                    if idx == 5 and ni % 2: continue
                    midi = chord[motif[ni]] + 12
                    inst = 'flute' if idx in (1, 4, 5) else 'wood'
                    gain = (.043 if idx == 5 else .066) * pad_energy
                    m.note(t0 + pos, midi, .38 if inst != 'flute' else .52,
                           inst, gain=gain, pan=(-.15 if ci % 2 == 0 else .15))

        # Percussion uses soft organic textures, with an 8-scene energy arc.
        if percussion > .14:
            for bi, beat in enumerate(np.arange(start+.03, end-.2, BEAT)):
                if bi % 4 in (0, 2) and idx != 5:
                    m.kick(float(beat), .045 * percussion)
                if bi % 4 == 2:
                    m.brush(float(beat), .047 * percussion, .12)
                if idx not in (0, 5, 9):
                    m.shaker(float(beat + BEAT / 2), .019 * percussion,
                             pan=-.35 if bi%2 else .35)

    # Opening: birds on electrical wire, as in the supplied story.
    for at, pan in ((1.05,-.36),(1.85,.52),(3.25,-.10),(7.05,.62),(12.95,-.55),(20.65,.4)):
        m.bird(at, pan, gain=.055 if at < 10 else .04)
    m.whoosh(9.7, .64, .042, -.5, .5)

    # Eight doors. Section change gets a tiny percussive landing and chime.
    for i, at in enumerate(SCENE_STARTS):
        m.door(at, i)

    # Supporting action cues, specifically tied to the illustrated vignettes.
    for at in (31.15, 31.7, 32.3, 36.0, 36.55, 37.10):
        m.pop(at, pan=(-.28 if at < 34 else .26), pitch=.66, gain=.042)
    for at, note in ((47.05,83),(48.78,86),(53.3,90),(56.2,86)):
        m.note(at, note, 1.15, 'bell', gain=.042, pan=-.2 if int(at)%2 else .2)
    m.whoosh(66.7, .72, .044, .5, -.5)
    m.note(67.1, 81, 1.6, 'bell', gain=.045)
    m.rain(78.0, 12.2, gain=.018)
    for at in (98.45, 99.05):
        m.note(at, 83 if at < 99 else 86, 2.1, 'bell', gain=.046, pan=-.33 if at < 99 else .33)
    m.bird(113.1, .25, gain=.031)
    for at, pan in ((129.25,-.5),(130.0,.12),(131.25,.52),(135.0,-.3)):
        m.note(at, 86, 1.1, 'bell', gain=.052, pan=pan)

    # Outro begins with a gentle transition, then lets the prayer breathe.
    m.whoosh(140.15, 1.2, .038, .6, -.6)
    for at, midi in ((143.5,78),(147.6,81),(152.1,74),(157.0,78)):
        m.note(at, midi, 2.0, 'bell', gain=.038)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path,
                   default=Path('output/8_Pintu_Rezeki_music_sfx_160s.wav'))
    args = p.parse_args()
    mixer = Mixer()
    build_score(mixer)
    mixer.finish()
    mixer.write(args.output)


if __name__ == '__main__':
    main()
