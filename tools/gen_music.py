#!/usr/bin/env python3
"""Procedural music for DUCKODUCKO -> ../sfx/music.wav

v3: cozy lofi river beat at 86 BPM, 16 bars (~44s before it repeats).
- soft thumpy kick + rim-snap head-nod (very quiet, more felt than heard)
- Rhodes-ish tremolo chords, two lazy hits a bar
- round sine bass: root on the one, fifth sneaks in on the and-of-two
- KALIMBA lead: pure decaying tones with a soft inharmonic partial
Note tails wrap to the start of the buffer so the loop is seamless.

Run:  python3 tools/gen_music.py && godot --headless --path . --import
"""
import math
import os
import random
import struct
import wave

SR = 22050
BPM = 86.0
BEAT = 60.0 / BPM
BARS = 16
SWING = 0.14
TOTAL = int(SR * BEAT * 4 * BARS)
random.seed(11)

mix = [0.0] * TOTAL


def add(samples, start_t, vol=1.0):
    s0 = int(start_t * SR)
    for i, v in enumerate(samples):
        mix[(s0 + i) % TOTAL] += v * vol      # wrap tails -> seamless loop


def eighth_t(bar, e):
    return bar * 4 * BEAT + e * BEAT / 2.0 + (SWING * BEAT / 2.0 if e % 2 else 0.0)


def kick(dur=0.13):
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        f = 52.0 * (1.0 + 2.2 * max(0.0, 1.0 - t / 0.04))    # pitch drop
        env = max(0.0, 1.0 - t / dur) ** 1.8
        out.append(math.sin(2 * math.pi * f * t) * env)
    return out


def rim(dur=0.05):
    out = []
    lp = 0.0
    for i in range(int(SR * dur)):
        t = i / SR
        lp += (random.uniform(-1, 1) - lp) * 0.5
        env = max(0.0, 1.0 - t / dur) ** 2
        out.append((lp * 0.7 + math.sin(2 * math.pi * 820.0 * t) * 0.4) * env)
    return out


def rhodes(f, dur):
    """Warm tremolo chord tone."""
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        trem = 0.8 + 0.2 * math.sin(2 * math.pi * 4.3 * t)
        env = min(1.0, t / 0.03) * (max(0.0, 1.0 - t / dur) ** 1.2)
        s = math.sin(2 * math.pi * f * t) + 0.35 * math.sin(2 * math.pi * f * 2 * t) * max(0.0, 1.0 - t * 2.2)
        out.append(s * env * trem)
    return out


def bass(f, dur):
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        env = min(1.0, t / 0.02) * (max(0.0, 1.0 - t / dur) ** 1.3)
        out.append((math.sin(2 * math.pi * f * t)
                    + 0.18 * math.sin(2 * math.pi * f * 2 * t)) * env)
    return out


def kalimba(f, dur=1.1):
    """Plucked-tine: a pure tone with fast decay + a soft 2.41x inharmonic partial."""
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        env1 = math.exp(-t * 5.5)
        env2 = math.exp(-t * 10.0)
        s = math.sin(2 * math.pi * f * t) * env1 \
            + 0.28 * math.sin(2 * math.pi * f * 2.41 * t) * env2
        out.append(s * min(1.0, t / 0.004))
    return out


# ---- the tune --------------------------------------------------------------------
C2, E2, F2, G2, A2 = 65.41, 82.41, 87.31, 98.0, 110.0
A3, B3, C4, D4, E4, F4, G4, A4 = 220.0, 246.94, 261.63, 293.66, 329.63, 349.23, 392.0, 440.0
C5, D5, E5, G5 = 523.25, 587.33, 659.26, 783.99

# (voicing, root) per bar — A: C Am F G x2; B: Am Em F G, F G C C
PROG = [
    ([C4, E4, G4], C2), ([A3, C4, E4], A2), ([A3, C4, F4], F2), ([B3, D4, G4], G2),
    ([C4, E4, G4], C2), ([A3, C4, E4], A2), ([A3, C4, F4], F2), ([B3, D4, G4], G2),
    ([A3, C4, E4], A2), ([B3, E4, G4], E2), ([A3, C4, F4], F2), ([B3, D4, G4], G2),
    ([A3, C4, F4], F2), ([B3, D4, G4], G2), ([C4, E4, G4], C2), ([C4, E4, G4], C2),
]

# kalimba phrases: (eighth, freq, _) — short motifs, lots of air
MELODY = [
    [(0, E5, 0), (3, G5, 0), (4, C5, 0)],
    [(0, A4, 0), (2, C5, 0), (5, E5, 0)],
    [(0, G4, 0), (3, A4, 0), (4, C5, 0)],
    [(0, D5, 0), (2, C5, 0), (4, A4, 0)],
    [(0, E5, 0), (3, G5, 0), (4, C5, 0)],
    [(0, A4, 0), (2, C5, 0), (5, E5, 0)],
    [(0, C5, 0), (2, A4, 0), (4, G4, 0), (6, A4, 0)],
    [(0, C5, 0)],
    [(0, A4, 0), (4, E5, 0)],
    [(0, G4, 0), (2, B3 * 2, 0), (4, E4 * 2, 0)],
    [(0, A4, 0), (3, C5, 0), (4, D5, 0)],
    [(0, D5, 0), (2, C5, 0), (4, A4, 0), (6, G4, 0)],
    [(0, A4, 0), (4, C5, 0)],
    [(0, D5, 0), (2, E5, 0), (4, G5, 0)],
    [(0, E5, 0), (2, C5, 0), (4, D5, 0)],
    [(0, C5, 0)],
]

for bar in range(BARS):
    t0 = bar * 4 * BEAT
    voicing, root = PROG[bar]
    # the head-nod: kick on 1 and 3, rim on 2 and 4 (skip bar 0 — ease in)
    if bar > 0:
        add(kick(), t0, 0.24)
        add(kick(), t0 + 2 * BEAT, 0.20)
        add(rim(), t0 + 1 * BEAT, 0.085)
        add(rim(), t0 + 3 * BEAT, 0.085)
    # chords: the one, then the lazy and-of-two
    for f in voicing:
        add(rhodes(f, BEAT * 1.9), t0, 0.060)
        add(rhodes(f, BEAT * 1.5), t0 + BEAT * 2.5 + SWING * BEAT * 0.5, 0.045)
    # bass
    add(bass(root, BEAT * 1.8), t0, 0.30)
    add(bass(root * 1.5, BEAT * 1.0), t0 + BEAT * 2.5 + SWING * BEAT * 0.5, 0.14)
    # kalimba
    for (e, f, _h) in MELODY[bar]:
        add(kalimba(f), eighth_t(bar, e), 0.16)

# ---- normalize + write -----------------------------------------------------------
peak = max(abs(v) for v in mix)
scale = 0.6 / peak
out = os.path.join(os.path.dirname(__file__), "..", "sfx", "music.wav")
with wave.open(out, "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    frames = bytearray()
    for v in mix:
        frames += struct.pack("<h", int(math.tanh(v * scale * 1.3) * 32000))
    w.writeframes(bytes(frames))
print("sfx/music.wav  (%.1fs loop)" % (TOTAL / SR))
