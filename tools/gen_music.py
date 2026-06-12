#!/usr/bin/env python3
"""Procedural music for DUCKODUCKO -> ../sfx/music.wav

v2: a lazy 16-bar river tune at 94 BPM (~41s before it repeats).
- warm pad chords (slow-attack sines) carry the harmony
- soft bass on the one and the and-of-two, lightly swung
- sparse Karplus-Strong plucks (lowpassed so they don't clang)
- the lead is a breathy sine 'flute' with vibrato, NOT a pluck
- whisper-quiet shaker only in the back half
Note tails wrap to the start of the buffer so the loop is seamless.

Run:  python3 tools/gen_music.py && godot --headless --path . --import
"""
import math
import os
import random
import struct
import wave

SR = 22050
BPM = 94.0
BEAT = 60.0 / BPM
BARS = 16
SWING = 0.12                    # odd eighths land late, lazily
TOTAL = int(SR * BEAT * 4 * BARS)
random.seed(7)

mix = [0.0] * TOTAL


def add(samples, start_t, vol=1.0):
    s0 = int(start_t * SR)
    for i, v in enumerate(samples):
        mix[(s0 + i) % TOTAL] += v * vol      # wrap tails -> seamless loop


def eighth_t(bar, e):
    """Time of eighth-note e in a bar, with swing on the odd eighths."""
    return bar * 4 * BEAT + e * BEAT / 2.0 + (SWING * BEAT / 2.0 if e % 2 else 0.0)


def pluck(f, dur):
    """Karplus-Strong, then a one-pole lowpass to soften the attack clang."""
    n = max(2, int(SR / f))
    buf = [random.uniform(-1, 1) for _ in range(n)]
    raw = []
    for i in range(int(SR * dur)):
        j = i % n
        raw.append(buf[j])
        buf[j] = 0.5 * (buf[j] + buf[(j + 1) % n]) * 0.995
    out = []
    lp = 0.0
    for v in raw:
        lp += (v - lp) * 0.35
        out.append(lp)
    return out


def pad_tone(f, dur):
    """Slow-attack warm sine for chord pads."""
    out = []
    atk = 0.45
    rel = 0.6
    for i in range(int(SR * dur)):
        t = i / SR
        env = min(1.0, t / atk) * min(1.0, max(0.0, (dur - t) / rel))
        s = math.sin(2 * math.pi * f * t) + 0.22 * math.sin(2 * math.pi * f * 2 * t)
        out.append(s * env)
    return out


def bass(f, dur):
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        env = max(0.0, 1.0 - t / dur) ** 1.4
        out.append((math.sin(2 * math.pi * f * t)
                    + 0.25 * math.sin(2 * math.pi * f * 2 * t)) * env)
    return out


def flute(f, dur):
    """The lead: breathy sine with vibrato and a soft swell."""
    out = []
    atk = 0.05
    for i in range(int(SR * dur)):
        t = i / SR
        vib = 1.0 + 0.006 * math.sin(2 * math.pi * 5.2 * t)
        env = min(1.0, t / atk) * (max(0.0, 1.0 - t / dur) ** 0.9)
        s = math.sin(2 * math.pi * f * vib * t) + 0.18 * math.sin(2 * math.pi * f * 2 * t)
        s += random.uniform(-1, 1) * 0.015          # breath
        out.append(s * env)
    return out


def shaker(dur=0.04):
    out = []
    lp = 0.0
    for i in range(int(SR * dur)):
        lp += (random.uniform(-1, 1) - lp) * 0.55
        out.append(lp * max(0.0, 1.0 - i / (SR * dur)) ** 2)
    return out


# ---- the tune --------------------------------------------------------------------
C2, E2, F2, G2, A2 = 65.41, 82.41, 87.31, 98.0, 110.0
C3, G3 = 130.81, 196.0
C4, D4, E4, F4, G4, A4, B3 = 261.63, 293.66, 329.63, 349.23, 392.0, 440.0, 246.94
C5, A3 = 523.25, 220.0

# (voicing, bass root) per bar — A: C G Am F x2; B: Am F C G, F G C C
PROG = [
    ([C4, E4, G4], C2), ([B3, D4, G4], G2), ([A3, C4, E4], A2), ([A3, C4, F4], F2),
    ([C4, E4, G4], C2), ([B3, D4, G4], G2), ([A3, C4, E4], A2), ([A3, C4, F4], F2),
    ([A3, C4, E4], A2), ([A3, C4, F4], F2), ([C4, E4, G4], C2), ([B3, D4, G4], G2),
    ([A3, C4, F4], F2), ([B3, D4, G4], G2), ([C4, E4, G4], C2), ([C4, E4, G4], C2),
]

# lead phrases: (eighth, freq, eighths_held) per bar; gentle, lots of rests
MELODY = [
    [(0, G4, 3), (4, A4, 2)],
    [(0, E4, 2), (2, G4, 2), (4, C5, 3)],
    [(0, A4, 2), (2, G4, 2), (4, E4, 3)],
    [(0, D4, 5)],
    [(0, G4, 3), (4, A4, 2)],
    [(0, E4, 2), (2, G4, 2), (4, A4, 3)],
    [(0, G4, 2), (2, E4, 2), (4, D4, 2), (6, C4, 2)],
    [(0, C4, 6)],
    [(0, C5, 3), (4, A4, 2)],
    [(0, A4, 2), (2, G4, 2), (4, E4, 3)],
    [(0, G4, 4), (4, A4, 2)],
    [(0, G4, 2), (2, E4, 2), (4, D4, 3)],
    [(0, A4, 3), (4, C5, 2)],
    [(0, A4, 2), (2, G4, 2), (4, E4, 2)],
    [(0, D4, 2), (2, E4, 2), (4, G4, 3)],
    [(0, C4, 7)],
]

ARP = [(0, 0), (3, 1), (4, 2), (7, 1)]      # sparse plucked figure (eighth, tone idx)

for bar in range(BARS):
    t0 = bar * 4 * BEAT
    voicing, root = PROG[bar]
    # pad: the whole chord breathes under everything
    for f in voicing:
        add(pad_tone(f, BEAT * 4.2), t0, 0.045)
    # bass: the one, then the and-of-two (swung)
    add(bass(root, BEAT * 1.7), t0, 0.26)
    add(bass(root * (1.5 if bar % 4 == 3 else 1.0), BEAT * 1.1), t0 + BEAT * 2.5 + SWING * BEAT * 0.5, 0.15)
    # plucks: only under the A sections, quietly
    if bar < 8:
        for (e, tone) in ARP:
            add(pluck(voicing[tone], BEAT * 1.2), eighth_t(bar, e), 0.10)
    # lead
    for (e, f, held) in MELODY[bar]:
        add(flute(f, BEAT / 2.0 * held * 1.05), eighth_t(bar, e), 0.13)
    # shaker: back half only, offbeats, barely there
    if bar >= 8:
        for e in (1, 3, 5, 7):
            add(shaker(), eighth_t(bar, e), 0.018)

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
