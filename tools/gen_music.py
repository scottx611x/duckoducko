#!/usr/bin/env python3
"""Procedural music for DUCKODUCKO -> ../sfx/music.wav

v4: UPBEAT & QUIRKY — a bouncy 112 BPM river-ska tune, 16 bars (~34s loop).
- offbeat chord stabs (the ska skank) on plucked strings
- bouncy root-fifth bass, walking up at turnarounds
- the lead is a soft square-wave KAZOO with vibrato, staccato and cheeky
- woodblock tick + tiny shaker keep it skipping along
Note tails wrap to the start of the buffer so the loop is seamless.

Run:  python3 tools/gen_music.py && godot --headless --path . --import
"""
import math
import os
import random
import struct
import wave

SR = 22050
BPM = 112.0
BEAT = 60.0 / BPM
BARS = 16
SWING = 0.10
TOTAL = int(SR * BEAT * 4 * BARS)
random.seed(21)

mix = [0.0] * TOTAL


def add(samples, start_t, vol=1.0):
    s0 = int(start_t * SR)
    for i, v in enumerate(samples):
        mix[(s0 + i) % TOTAL] += v * vol      # wrap tails -> seamless loop


def eighth_t(bar, e):
    return bar * 4 * BEAT + e * BEAT / 2.0 + (SWING * BEAT / 2.0 if e % 2 else 0.0)


def pluck(f, dur):
    """Karplus-Strong, lowpassed — the skank chord stab."""
    n = max(2, int(SR / f))
    buf = [random.uniform(-1, 1) for _ in range(n)]
    raw = []
    for i in range(int(SR * dur)):
        j = i % n
        raw.append(buf[j])
        buf[j] = 0.5 * (buf[j] + buf[(j + 1) % n]) * 0.994
    out = []
    lp = 0.0
    for v in raw:
        lp += (v - lp) * 0.4
        out.append(lp)
    return out


def bass(f, dur):
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        env = min(1.0, t / 0.015) * (max(0.0, 1.0 - t / dur) ** 1.2)
        out.append((math.sin(2 * math.pi * f * t)
                    + 0.22 * math.sin(2 * math.pi * f * 2 * t)) * env)
    return out


def kazoo(f, dur):
    """Soft square-ish lead with vibrato — cheerful, slightly rude."""
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        vib = 1.0 + 0.010 * math.sin(2 * math.pi * 6.0 * t)
        env = min(1.0, t / 0.015) * (max(0.0, 1.0 - t / dur) ** 0.8)
        ph = 2 * math.pi * f * vib * t
        # rounded square: stacked odd harmonics, gently
        s = math.sin(ph) + 0.32 * math.sin(3 * ph) + 0.16 * math.sin(5 * ph)
        out.append(s * env * 0.8)
    return out


def woodblock(dur=0.04):
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        env = max(0.0, 1.0 - t / dur) ** 2.2
        out.append(math.sin(2 * math.pi * 1180.0 * t) * env)
    return out


def shaker(dur=0.035):
    out = []
    lp = 0.0
    for i in range(int(SR * dur)):
        lp += (random.uniform(-1, 1) - lp) * 0.6
        out.append(lp * max(0.0, 1.0 - i / (SR * dur)) ** 2)
    return out


# ---- the tune --------------------------------------------------------------------
C2, D2, E2, F2, G2, A2 = 65.41, 73.42, 82.41, 87.31, 98.0, 110.0
A3, B3, C4, D4, E4, F4, G4, A4 = 220.0, 246.94, 261.63, 293.66, 329.63, 349.23, 392.0, 440.0
C5, D5, E5, G5, A5 = 523.25, 587.33, 659.26, 783.99, 880.0

# (voicing, root) per bar — A: C F G C x2; B: Am F C G, F G C C(turnaround)
PROG = [
    ([C4, E4, G4], C2), ([A3, C4, F4], F2), ([B3, D4, G4], G2), ([C4, E4, G4], C2),
    ([C4, E4, G4], C2), ([A3, C4, F4], F2), ([B3, D4, G4], G2), ([C4, E4, G4], C2),
    ([A3, C4, E4], A2), ([A3, C4, F4], F2), ([C4, E4, G4], C2), ([B3, D4, G4], G2),
    ([A3, C4, F4], F2), ([B3, D4, G4], G2), ([C4, E4, G4], C2), ([C4, E4, G4], C2),
]

# kazoo phrases: (eighth, freq, eighths_held) — chipper staccato motifs
MELODY = [
    [(0, E5, 1), (1, G5, 1), (2, E5, 1), (4, C5, 2), (6, D5, 1)],
    [(0, A4, 1), (2, C5, 1), (3, D5, 1), (4, E5, 2)],
    [(0, D5, 1), (1, E5, 1), (2, D5, 1), (4, G4, 2), (6, A4, 1)],
    [(0, C5, 3), (4, E5, 1), (5, G5, 2)],
    [(0, E5, 1), (1, G5, 1), (2, E5, 1), (4, C5, 2), (6, D5, 1)],
    [(0, A4, 1), (2, C5, 1), (3, D5, 1), (4, E5, 2)],
    [(0, G5, 1), (2, E5, 1), (4, D5, 1), (5, C5, 1), (6, A4, 1)],
    [(0, G4, 3), (4, C5, 3)],
    [(0, A4, 1), (2, C5, 1), (4, E5, 2), (6, D5, 1)],
    [(0, C5, 1), (2, A4, 1), (4, F4 * 2, 2)],
    [(0, G4, 1), (1, A4, 1), (2, C5, 1), (4, E5, 2)],
    [(0, D5, 1), (2, B3 * 2, 1), (4, G4, 2)],
    [(0, A4, 1), (1, C5, 1), (2, D5, 1), (4, A5, 2)],
    [(0, G5, 1), (2, E5, 1), (4, D5, 1), (6, E5, 1)],
    [(0, G5, 1), (1, E5, 1), (2, C5, 1), (4, D5, 2), (6, B3 * 2, 1)],
    [(0, C5, 4)],
]

for bar in range(BARS):
    t0 = bar * 4 * BEAT
    voicing, root = PROG[bar]
    # the skank: chord stabs on every OFFBEAT eighth
    for e in (1, 3, 5, 7):
        for f in voicing:
            add(pluck(f, BEAT * 0.45), eighth_t(bar, e), 0.085)
    # bouncy bass: root, fifth, root, fifth (walks up into the next bar)
    add(bass(root, BEAT * 0.9), t0, 0.32)
    add(bass(root * 1.5, BEAT * 0.9), t0 + BEAT, 0.24)
    add(bass(root, BEAT * 0.9), t0 + 2 * BEAT, 0.30)
    if bar % 4 == 3:
        add(bass(root * 1.26, BEAT * 0.45), t0 + 3 * BEAT, 0.22)            # walk...
        add(bass(root * 1.5, BEAT * 0.45), t0 + 3.5 * BEAT, 0.22)           # ...up!
    else:
        add(bass(root * 1.5, BEAT * 0.9), t0 + 3 * BEAT, 0.24)
    # percussion: woodblock on the beats, shaker filling the offbeats
    for b in range(4):
        add(woodblock(), t0 + b * BEAT, 0.10 if b % 2 == 0 else 0.06)
    for e in (1, 3, 5, 7):
        add(shaker(), eighth_t(bar, e), 0.030)
    # the kazoo speaks
    for (e, f, held) in MELODY[bar]:
        add(kazoo(f, BEAT / 2.0 * held * 0.92), eighth_t(bar, e), 0.115)

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
