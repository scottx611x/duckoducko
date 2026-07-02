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
BARS = 24
SWING = 0.10
TOTAL = int(SR * BEAT * 4 * BARS)
XF = int(SR * 0.35)                          # crossfade length for a truly seamless loop
random.seed(21)

# render into a buffer with OVERHANG room: we play 2 extra bars PAST the loop point, then
# crossfade that continuation back over the loop start so end -> start is musically continuous.
OVER = int(SR * BEAT * 4 * 2)
mix = [0.0] * (TOTAL + OVER)


def add(samples, start_t, vol=1.0):
    s0 = int(start_t * SR)
    for i, v in enumerate(samples):
        j = s0 + i
        if 0 <= j < len(mix):                # no wrap — the overhang region catches the tails
            mix[j] += v * vol


def seamless_loop(buf, total, xf):
    """Crossfade the rendered overhang [total, total+xf) back over the start so the loop is seamless."""
    out = list(buf[:total])
    for i in range(xf):
        f = 0.5 - 0.5 * math.cos(math.pi * i / xf)   # 0 -> 1 raised cosine
        out[i] = out[i] * f + buf[total + i] * (1.0 - f)
    return out


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


def pad(freqs, dur):
    """A soft sustained organ pad — a constant energy bed so the loop never surges or drops out."""
    out = []
    n = int(SR * dur)
    for i in range(n):
        t = i / SR
        env = min(1.0, t / 0.06) * min(1.0, (dur - t) / 0.06)
        s = sum(math.sin(2 * math.pi * f * t) + 0.3 * math.sin(2 * math.pi * f * 2 * t) for f in freqs) / len(freqs)
        out.append(s * env)
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
    # A': a faithful REPRISE of the opening (C F G C x2) so the extension stays the SAME good tune,
    # then lands clean on C — a tidy turnaround straight back into bar 0 for a seamless loop.
    ([C4, E4, G4], C2), ([A3, C4, F4], F2), ([B3, D4, G4], G2), ([C4, E4, G4], C2),
    ([C4, E4, G4], C2), ([A3, C4, F4], F2), ([B3, D4, G4], G2), ([C4, E4, G4], C2),
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
    # A': the opening kazoo hook sung again (lightly varied) so the back half is instantly familiar,
    # closing on a held C that resolves cleanly into bar 0.
    [(0, E5, 1), (1, G5, 1), (2, E5, 1), (4, C5, 2), (6, D5, 1)],
    [(0, A4, 1), (2, C5, 1), (3, D5, 1), (4, E5, 2)],
    [(0, D5, 1), (1, E5, 1), (2, D5, 1), (4, G4, 2), (6, A4, 1)],
    [(0, E5, 1), (4, G5, 1), (5, E5, 1), (6, C5, 2)],
    [(0, E5, 1), (1, G5, 1), (2, E5, 1), (4, C5, 2), (6, D5, 1)],
    [(0, A4, 1), (2, C5, 1), (3, D5, 1), (4, E5, 2)],
    [(0, G5, 1), (2, E5, 1), (4, D5, 1), (5, C5, 1), (6, A4, 1)],
    [(0, E5, 1), (1, G5, 1), (2, E5, 1), (3, C5, 1), (4, D5, 1), (5, E5, 1), (6, C5, 1), (7, D5, 1)],   # ...D5 leads up into bar 0's E5
]

for bar in range(BARS + 2):                  # +2 overhang bars (bar 0,1 again) for the crossfade loop
    t0 = bar * 4 * BEAT
    voicing, root = PROG[bar % BARS]
    # a sustained chord PAD under everything (overlaps into the next bar -> seamless energy floor)
    add(pad([f for f in voicing], 4 * BEAT * 1.06), t0, 0.16)
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
    for (e, f, held) in MELODY[bar % BARS]:
        add(kazoo(f, BEAT / 2.0 * held * 0.92), eighth_t(bar, e), 0.115)

# ---- seamless crossfade loop, then normalize + write -----------------------------
mix = seamless_loop(mix, TOTAL, XF)          # end now flows continuously into the start
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


# ---- SUBTLE PER-REGION TINTS -----------------------------------------------------
# The river changes scenery, but it's the SAME song — each region just gets a gentle
# tonal tint (warmer / hushed / brighter / shimmery). Identical length & format to
# music.wav, so the game can swap them while PRESERVING playback position: the melody
# continues unbroken, only the timbre shifts. Truly subtle, never a hard cut.
def _write_variant(buf, out_name, drive=1.3):
    peak = max(abs(v) for v in buf) or 1.0
    sc = 0.6 / peak
    p = os.path.join(os.path.dirname(__file__), "..", "sfx", out_name)
    with wave.open(p, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        fr = bytearray()
        for v in buf:
            fr += struct.pack("<h", int(math.tanh(v * sc * drive) * 32000))
        w.writeframes(bytes(fr))
    print("sfx/%s  (tint)" % out_name)


def _lowpass(src, alpha):
    lp = 0.0
    for v in src:                       # prime so the loop point stays seamless
        lp += (v - lp) * alpha
    out = [0.0] * len(src)
    for i, v in enumerate(src):
        lp += (v - lp) * alpha
        out[i] = lp
    return out


# warm: gently roll off the highs -> cozy (Park Picnic, Sand Pond)
_write_variant(_lowpass(mix, 0.42), "music_warm.wav")
# hush: a hair quieter + softened -> subdued (Spooky Bog)
_write_variant([v * 0.85 for v in _lowpass(mix, 0.5)], "music_hush.wav")
# bright: add a sparkle of highs (signal minus its lowpass) -> crisp (City Fountain)
_lp_b = _lowpass(mix, 0.5)
_write_variant([mix[i] + (mix[i] - _lp_b[i]) * 0.55 for i in range(TOTAL)], "music_brisk.wav")
# shimmer: a slow loop-aligned tremolo -> glimmery (Aurora Lake)
_cyc = 12
_write_variant([mix[i] * (1.0 + 0.10 * math.sin(2 * math.pi * _cyc * i / TOTAL)) for i in range(TOTAL)], "music_shimmer.wav")


# ---- BOSS THEMES -----------------------------------------------------------------
# Menacing duel music: minor key, driving four-on-the-floor bass, snarling lead.
# Same kazoo/pluck/bass palette, but darker harmony + heavier drive so it reads as
# "oh no, a boss". A separate, even darker theme for GERALD THE ETERNAL.
def render_track(bpm, prog, melody, out_name, drive=1.6, lead_vol=0.13):
    beat = 60.0 / bpm
    bars = len(prog)
    total = int(SR * beat * 4 * bars)
    buf = [0.0] * total

    def addb(samples, start_t, vol=1.0):
        s0 = int(start_t * SR)
        for i, v in enumerate(samples):
            buf[(s0 + i) % total] += v * vol

    def e8(bar, e):
        return bar * 4 * beat + e * beat / 2.0 + (0.05 * beat / 2.0 if e % 2 else 0.0)

    for bar in range(bars):
        t0 = bar * 4 * beat
        voicing, root = prog[bar]
        for e in (1, 3, 5, 7):                          # tense offbeat chord stabs
            for f in voicing:
                addb(pluck(f, beat * 0.4), e8(bar, e), 0.06)
        for b in range(4):                              # pounding root bass on every beat
            addb(bass(root, beat * 0.55), t0 + b * beat, 0.46)
            addb(bass(root, beat * 0.22), t0 + b * beat + beat * 0.5, 0.20)
        for b in range(4):                              # driving woodblock + shaker
            addb(woodblock(), t0 + b * beat, 0.13)
        for e in (1, 3, 5, 7):
            addb(shaker(), e8(bar, e), 0.045)
        for (e, f, held) in melody[bar % len(melody)]:  # the snarling lead
            addb(kazoo(f, beat / 2.0 * held * 0.9), e8(bar, e), lead_vol)

    peak = max(abs(v) for v in buf) or 1.0
    scale = 0.62 / peak
    out = os.path.join(os.path.dirname(__file__), "..", "sfx", out_name)
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        frames = bytearray()
        for v in buf:
            frames += struct.pack("<h", int(math.tanh(v * scale * drive) * 32000))
        w.writeframes(bytes(frames))
    print("sfx/%s  (%.1fs loop)" % (out_name, total / SR))


# extra notes for the minor keys
Bb1, A1, B2, Bb3, Cs4, Bb4 = 58.27, 55.0, 123.47, 233.08, 277.18, 466.16
Am3 = [A3, C4, E4]; Fmaj = [A3, C4, F4]; Gmaj = [B3, D4, G4]; Emaj = [B3, Cs4 / 2, E4]
# GERALD / SNAPZ duel — A natural minor, 138 BPM, tense and propulsive
PROG_BOSS = [(Am3, A2), (Fmaj, F2), (Gmaj, G2), (Am3, A2),
             (Am3, A2), (Fmaj, F2), (Emaj, E2), (Am3, A2)]
MELODY_BOSS = [
    [(0, A4, 1), (2, C5, 1), (4, E5, 1), (6, D5, 1)],
    [(0, A4, 1), (2, F4, 1), (4, A4, 2)],
    [(0, G4, 1), (2, Bb4 / 2 * 2, 1), (4, D5, 2)],
    [(0, A4, 2), (4, E5, 1), (5, C5, 1), (6, A4, 1)],
]
render_track(138, PROG_BOSS, MELODY_BOSS, "boss_music.wav", drive=1.7)

# GERALD THE ETERNAL — D minor, 150 BPM, lower + the harmonic-minor menace (A major)
Dm = [D4, F4, A4]; Bbmaj = [D4, F4, Bb3]; Cmaj = [C4, E4, G4]; Amaj = [A3, Cs4, E4]
PROG_ETERNAL = [(Dm, D2), (Bbmaj, Bb1), (Cmaj, C2), (Amaj, A1),
                (Dm, D2), (Bbmaj, Bb1), (Amaj, A1), (Amaj, A1)]
MELODY_ETERNAL = [
    [(0, D5, 1), (2, F4, 1), (4, A4, 1), (6, Bb4, 1)],
    [(0, A4, 2), (4, F4, 1), (6, D4, 1)],
    [(0, C5, 1), (2, E5, 1), (4, G4, 2)],
    [(0, Cs4 * 2, 1), (2, A4, 1), (4, E5, 2)],
]
render_track(150, PROG_ETERNAL, MELODY_ETERNAL, "boss_eternal.wav", drive=1.85, lead_vol=0.14)

# SADIE THE BOUNDLESS — C MAJOR, 160 BPM: the only boss theme in a HAPPY key.
# It should feel like the biggest game of fetch ever played, not a battle.
Cmaj4 = [C4, E4, G4]; Fmaj4 = [F4, A4, C5]; Gmaj4 = [G4, B3 * 2, D5]; Am4 = [A4, C5, E5]
PROG_SADIE = [(Cmaj4, C2), (Cmaj4, C2), (Fmaj4, F2), (Gmaj4, G2),
              (Am4, A2), (Fmaj4, F2), (Gmaj4, G2), (Cmaj4, C2)]
MELODY_SADIE = [
    [(0, E5, 1), (1, G5, 1), (2, C5, 1), (4, E5, 1), (6, G5, 2)],
    [(0, G5, 1), (2, E5, 1), (4, C5, 1), (6, D5, 1)],
    [(0, F4 * 2, 1), (2, A4 * 2 / 2 * 2, 1), (4, C5, 2)],
    [(0, D5, 1), (2, B3 * 4 / 2, 1), (4, G4 * 2, 2)],
]
render_track(160, PROG_SADIE, MELODY_SADIE, "boss_sadie.wav", drive=1.6, lead_vol=0.16)


# ---- AMBIENT BIOME THEMES --------------------------------------------------------
# Looping background variants so different scenery areas get their own mood.
# These are GENTLER than the boss themes: softer bass, sparser percussion, low
# drive — tasteful background beds for a whimsical duck game. Same SR/format and
# the same wrap-the-tail-for-seamless-loop trick as music.wav, so they swap in
# directly under the existing AudioStreamPlayer + loop_mode setup.
def render_ambient(bpm, prog, melody, out_name,
                   lead_vol=0.10, lead_dur=0.92, bass_vol=0.26,
                   stab_vol=0.07, perc=True, perc_vol=0.07, shaker_vol=0.022,
                   drive=1.15, target=0.55, swing=0.08, reps=2):
    beat = 60.0 / bpm
    bars = len(prog)
    eff_bars = bars * reps                   # repeat the phrase so the loop isn't jarringly short
    total = int(SR * beat * 4 * eff_bars)
    over = int(SR * beat * 4 * 2)            # overhang for the crossfade loop
    buf = [0.0] * (total + over)

    def addb(samples, start_t, vol=1.0):
        s0 = int(start_t * SR)
        for i, v in enumerate(samples):
            j = s0 + i
            if 0 <= j < len(buf):            # no wrap — overhang catches the tails
                buf[j] += v * vol

    def e8(bar, e):
        return bar * 4 * beat + e * beat / 2.0 + (swing * beat / 2.0 if e % 2 else 0.0)

    for bar in range(eff_bars + 2):          # +2 overhang bars for the crossfade
        t0 = bar * 4 * beat
        voicing, root = prog[bar % bars]
        # soft offbeat chord shimmer (gentle, low volume)
        for e in (2, 6):
            for f in voicing:
                addb(pluck(f, beat * 0.7), e8(bar, e), stab_vol)
        # easy-going bass: root on the 1, fifth on the 3 — no pounding
        addb(bass(root, beat * 1.7), t0, bass_vol)
        addb(bass(root * 1.5, beat * 1.7), t0 + 2 * beat, bass_vol * 0.85)
        # light percussion: a soft woodblock on beats 1 & 3, airy shaker offbeats
        if perc:
            addb(woodblock(), t0, perc_vol)
            addb(woodblock(), t0 + 2 * beat, perc_vol * 0.7)
            for e in (1, 3, 5, 7):
                addb(shaker(), e8(bar, e), shaker_vol)
        # the lead melody (kazoo) — the character of each mood
        for (e, f, held) in melody[bar % len(melody)]:
            addb(kazoo(f, beat / 2.0 * held * lead_dur), e8(bar, e), lead_vol)

    buf = seamless_loop(buf, total, XF)      # crossfade the overhang -> seamless loop
    peak = max(abs(v) for v in buf) or 1.0
    scale = target / peak
    out = os.path.join(os.path.dirname(__file__), "..", "sfx", out_name)
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        frames = bytearray()
        for v in buf:
            frames += struct.pack("<h", int(math.tanh(v * scale * drive) * 32000))
        w.writeframes(bytes(frames))
    print("sfx/%s  (%.1fs loop)" % (out_name, total / SR))


# extra notes used by the ambient palettes
F3, G3 = 174.61, 196.0
Eb4, Bb4n, Eb5, F5amb = 311.13, 466.16, 622.25, 698.46

# --- CALM: slow 90 BPM C-major lullaby, long sustained kazoo, lots of air ---------
# Suits LAZY POND (and PARK PICNIC's relaxed feel). Sleepy, warm, unhurried.
PROG_CALM = [
    ([C4, E4, G4], C2), ([A3, C4, E4], A2), ([A3, C4, F4], F2),
    ([B3, D4, G4], G2), ([C4, E4, G4], C2), ([B3, D4, G4], G2),
]
MELODY_CALM = [
    [(0, E4, 4), (4, G4, 4)],
    [(0, C5, 4), (4, A4, 4)],
    [(0, F4, 4), (4, A4, 3)],
    [(0, D4, 4), (4, G4, 4)],
    [(0, G4, 4), (4, E4, 4)],
    [(0, D4, 4), (4, B3, 4)],
]
render_ambient(90, PROG_CALM, MELODY_CALM, "music_calm.wav",
               lead_vol=0.11, lead_dur=0.95, bass_vol=0.24,
               stab_vol=0.05, perc_vol=0.05, shaker_vol=0.018, swing=0.04)

# --- SPOOKY: 100 BPM A natural minor, minor-key drift, hollow & a touch eerie -----
# Suits SPOOKY BOG. Wandering minor melody, sparse, low woodblock thud.
PROG_SPOOKY = [
    ([A3, C4, E4], A2), ([A3, C4, F4], F2), ([B3, D4, G4], G2),
    ([D4, F4, A4], D2), ([B3, Cs4 / 2, E4], E2), ([A3, C4, E4], A2),
]
MELODY_SPOOKY = [
    [(0, A4, 2), (2, C5, 1), (4, E4, 3)],
    [(0, F4, 2), (4, A4, 2), (6, G4, 1)],
    [(0, G4, 2), (4, D4, 2), (6, B3, 1)],
    [(0, D5, 2), (4, A4, 2)],
    [(0, E4, 2), (4, Cs4, 2)],
    [(0, A4, 4)],
]
render_ambient(100, PROG_SPOOKY, MELODY_SPOOKY, "music_spooky.wav",
               lead_vol=0.10, lead_dur=0.88, bass_vol=0.28,
               stab_vol=0.055, perc_vol=0.06, shaker_vol=0.016, swing=0.05)

# --- BRIGHT: lively 124 BPM C-major, bouncy hooky kazoo — cheerful & sunny --------
# Suits PARK PICNIC and CITY FOUNTAIN. Upbeat, skipping, the happiest of the set.
PROG_BRIGHT = [
    ([C4, E4, G4], C2), ([B3, D4, G4], G2), ([A3, C4, F4], F2), ([C4, E4, G4], C2),
    ([C4, E4, G4], C2), ([A3, C4, E4], A2), ([A3, C4, F4], F2), ([B3, D4, G4], G2),
]
MELODY_BRIGHT = [
    [(0, G4, 1), (1, C5, 1), (2, E5, 1), (4, G4, 1), (5, E5, 2)],
    [(0, D5, 1), (2, G4, 1), (4, B3 * 2, 1), (5, D5, 2)],
    [(0, C5, 1), (2, A4, 1), (4, F4, 1), (6, A4, 1)],
    [(0, G4, 1), (1, E4, 1), (2, C5, 2), (4, E5, 2)],
    [(0, E5, 1), (1, G4, 1), (2, C5, 1), (4, E5, 1), (5, G5, 2)],
    [(0, A4, 1), (2, C5, 1), (4, E5, 2)],
    [(0, F4, 1), (1, A4, 1), (2, C5, 1), (4, A4, 1), (6, F4, 1)],
    [(0, G4, 1), (2, D5, 1), (4, B3 * 2, 1), (6, G4, 1)],
]
render_ambient(124, PROG_BRIGHT, MELODY_BRIGHT, "music_bright.wav",
               lead_vol=0.11, lead_dur=0.85, bass_vol=0.26,
               stab_vol=0.07, perc_vol=0.075, shaker_vol=0.024, swing=0.10)

# --- COLD: airy 96 BPM, shimmering Eb-major-ish, glassy high kazoo — icy/serene ---
# Suits AURORA LAKE, EMERALD LAKE, SAND POND. Crystalline, spacious, gently glinting.
PROG_COLD = [
    ([Eb4, G4, Bb4n], Eb4 / 4), ([C4, Eb4, G4], C2), ([Bb3, D4, F4], Bb1 * 2),
    ([Eb4, G4, Bb4n], Eb4 / 4), ([G3, Bb3, D4], G2), ([C4, Eb4, G4], C2),
]
MELODY_COLD = [
    [(0, Bb4n, 3), (4, Eb5, 3)],
    [(0, G4, 3), (4, C5, 3)],
    [(0, F4, 3), (4, Bb4n, 3)],
    [(0, Eb5, 3), (4, Bb4n, 3)],
    [(0, D4, 3), (4, G4, 3)],
    [(0, Eb5, 4)],
]
render_ambient(96, PROG_COLD, MELODY_COLD, "music_cold.wav",
               lead_vol=0.105, lead_dur=0.96, bass_vol=0.22,
               stab_vol=0.06, perc=True, perc_vol=0.04, shaker_vol=0.02, swing=0.03)


# --- BOOMBOX: a HEAVY hip-hop beat the boombox blasts during a run --------------------
def kick808(dur=0.42, f0=150.0, f1=44.0):
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        f = f1 + (f0 - f1) * math.exp(-t * 30.0)        # punchy pitch drop -> deep 808
        env = math.exp(-t * 5.0)
        out.append(math.sin(2 * math.pi * f * t) * env)
    return out


def snare_hh(dur=0.2):
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        env = math.exp(-t * 24.0)
        out.append((random.uniform(-1, 1) * 0.85 + math.sin(2 * math.pi * 190.0 * t) * 0.45) * env)
    return out


def hat(dur=0.045, decay=46.0):
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        out.append(random.uniform(-1, 1) * math.exp(-t * decay))
    return out


def sub808(f, dur):
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        env = min(1.0, t / 0.01) * math.exp(-t * 1.6)
        out.append((math.sin(2 * math.pi * f * t) + 0.25 * math.sin(2 * math.pi * f * 2 * t)) * env)
    return out


def render_boombox():
    bpm = 86.0; beat = 60.0 / bpm; bars = 8
    total = int(SR * beat * 4 * bars)
    over = int(SR * beat * 4 * 2)
    buf = [0.0] * (total + over)

    def addb(s, t, vol=1.0):
        s0 = int(t * SR)
        for i, v in enumerate(s):
            j = s0 + i
            if 0 <= j < len(buf):
                buf[j] += v * vol

    # a dark minor riff (Cm) for the bassline + a brassy stab
    Cm = [130.81, 155.56, 196.0]
    bassline = [65.41, 65.41, 77.78, 87.31]      # C C Eb F per bar, varied
    for bar in range(bars + 2):
        t0 = bar * 4 * beat
        b16 = beat / 4.0                          # sixteenth
        # KICK: boom-bap pattern (1, the "and" of 2, 3-ish) — heavy
        for k in (0, 3, 6, 10):
            addb(kick808(), t0 + k * b16, 0.95)
        addb(kick808(dur=0.3), t0 + 14 * b16, 0.7)
        # SNARE: hard backbeat on 2 and 4
        addb(snare_hh(), t0 + 4 * b16, 0.7)
        addb(snare_hh(), t0 + 12 * b16, 0.7)
        # HI-HATS: steady 16ths with occasional fast rolls + accents
        for h in range(16):
            v = 0.16 if h % 2 == 0 else 0.10
            if (bar % 4 == 3) and h >= 12:        # a little roll into the next bar
                addb(hat(dur=0.03, decay=70), t0 + h * b16 + b16 * 0.5, 0.12)
            addb(hat(dur=0.05 if h % 4 == 0 else 0.035), t0 + h * b16, v)
        # 808 BASS following the riff
        f = bassline[bar % len(bassline)]
        addb(sub808(f, beat * 2.2), t0, 0.6)
        addb(sub808(f * 1.5, beat * 1.4), t0 + 2.5 * beat, 0.4)
        # a dark brass-ish chord stab on the offbeats (every other bar)
        if bar % 2 == 0:
            for f2 in Cm:
                addb(pluck(f2, beat * 0.5), t0 + 2 * beat, 0.10)

    buf = seamless_loop(buf, total, XF)
    peak = max(abs(v) for v in buf) or 1.0
    sc = 0.72 / peak
    out = os.path.join(os.path.dirname(__file__), "..", "sfx", "music_boombox.wav")
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        fr = bytearray()
        for v in buf:
            fr += struct.pack("<h", int(math.tanh(v * sc * 1.5) * 32000))
        w.writeframes(bytes(fr))
    print("sfx/music_boombox.wav  (%.1fs heavy beat)" % (total / SR))


render_boombox()

print("done.")
