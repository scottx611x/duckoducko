#!/usr/bin/env python3
"""Procedural music for DUCKODUCKO -> ../sfx/music.wav

A chill 8-bar pluck loop (Karplus-Strong strings = ukulele-adjacent), soft sine
bass, and feather-light offbeat hats. C-major pentatonic melody over C-G-Am-F.
Note tails wrap around to the start of the buffer so the loop is seamless.

Run:  python3 tools/gen_music.py
Then: godot --headless --path . --import
"""
import math
import os
import random
import struct
import wave

SR = 22050                      # lo-fi on purpose; Godot resamples
BPM = 108.0
BEAT = 60.0 / BPM
BARS = 8
TOTAL = int(SR * BEAT * 4 * BARS)
random.seed(42)

mix = [0.0] * TOTAL


def add(samples, start_t, vol=1.0):
    s0 = int(start_t * SR)
    for i, v in enumerate(samples):
        mix[(s0 + i) % TOTAL] += v * vol      # wrap tails -> seamless loop


def pluck(f, dur):
    """Karplus-Strong plucked string."""
    n = max(2, int(SR / f))
    buf = [random.uniform(-1, 1) for _ in range(n)]
    out = []
    for i in range(int(SR * dur)):
        j = i % n
        v = buf[j]
        buf[j] = 0.5 * (buf[j] + buf[(j + 1) % n]) * 0.996
        out.append(v)
    return out


def bass(f, dur):
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        env = max(0.0, 1.0 - t / dur) ** 1.6
        out.append((math.sin(2 * math.pi * f * t)
                    + 0.3 * math.sin(2 * math.pi * f * 2 * t)) * env)
    return out


def hat(dur=0.03):
    return [random.uniform(-1, 1) * max(0.0, 1.0 - i / (SR * dur)) ** 2
            for i in range(int(SR * dur))]


# ---- the tune --------------------------------------------------------------------
C2, F2, G2, A2 = 65.41, 87.31, 98.0, 110.0
C4, D4, E4, F4, G4, A4, B3 = 261.63, 293.66, 329.63, 349.23, 392.0, 440.0, 246.94
C5, D5, E5, G5, A5 = 523.25, 587.33, 659.26, 783.99, 880.0

CHORDS = [                       # (name, voicing, bass root) per bar: C G Am F x2-ish
    ([C4, E4, G4], C2), ([B3, D4, G4], G2), ([A4, E4, C4], A2), ([F4, A4, C4], F2),
    ([C4, E4, G4], C2), ([B3, D4, G4], G2), ([F4, A4, C4], F2), ([C4, E4, G4], C2),
]
ARP = [0, 1, 2, 1, 0, 1, 2, 1]   # eighth-note arpeggio indices

# melody: (eighth_index, freq, duration_in_eighths) per bar
MELODY = [
    [(0, E5, 2), (2, G5, 2), (4, A5, 3)],
    [(0, G5, 2), (2, E5, 2), (4, D5, 4)],
    [(0, C5, 2), (2, D5, 2), (4, E5, 3)],
    [(0, D5, 6)],
    [(0, E5, 2), (2, G5, 2), (4, A5, 3)],
    [(0, G5, 2), (2, E5, 2), (4, D5, 4)],
    [(0, A5, 2), (2, G5, 2), (4, E5, 2), (6, D5, 2)],
    [(0, C5, 8)],
]

EIGHTH = BEAT / 2.0
for bar in range(BARS):
    t0 = bar * 4 * BEAT
    voicing, root = CHORDS[bar]
    add(bass(root, BEAT * 1.4), t0, 0.30)                    # downbeat bass
    add(bass(root, BEAT * 1.0), t0 + 2 * BEAT, 0.22)
    for e in range(8):
        add(pluck(voicing[ARP[e]], EIGHTH * 1.8), t0 + e * EIGHTH, 0.15)
        if e % 2 == 1:
            add(hat(), t0 + e * EIGHTH, 0.045)               # offbeat tick
    for (e, f, dur) in MELODY[bar]:
        add(pluck(f, EIGHTH * dur * 1.15), t0 + e * EIGHTH, 0.26)

# ---- normalize + write -----------------------------------------------------------
peak = max(abs(v) for v in mix)
scale = 0.62 / peak
out = os.path.join(os.path.dirname(__file__), "..", "sfx", "music.wav")
with wave.open(out, "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    frames = bytearray()
    for v in mix:
        frames += struct.pack("<h", int(math.tanh(v * scale * 1.4) * 32000))
    w.writeframes(bytes(frames))
print("sfx/music.wav  (%.1fs loop)" % (TOTAL / SR))
