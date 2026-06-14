#!/usr/bin/env python3
"""Procedural SFX for DUCKODUCKO -> ../sfx/*.wav

Same philosophy as gen_sprites.py: zero external assets, everything authored in
code so it can be tweaked and regenerated. Pure stdlib (wave + math), 44.1kHz
16-bit mono. Sounds are kazoo-adjacent and soft on purpose -- WHIMSY.md says the
game must read fully with sound OFF, so these are juice, not information.

Run:  python3 tools/gen_sfx.py
Then: godot --headless --path . --import   (so Godot picks up new WAVs)
"""
import math
import os
import random
import struct
import wave

SR = 44100
SFX = os.path.join(os.path.dirname(__file__), "..", "sfx")
os.makedirs(SFX, exist_ok=True)
random.seed(1207)  # deterministic output -> stable git diffs


def save(name, samples):
    # soft-clip + 16-bit pack
    with wave.open(os.path.join(SFX, name), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        frames = bytearray()
        for s in samples:
            s = math.tanh(s)
            frames += struct.pack("<h", int(s * 32000))
        w.writeframes(bytes(frames))
    print("  sfx/%s  (%.2fs)" % (name, len(samples) / SR))


def env(t, dur, attack=0.005, curve=3.0):
    """Fast attack, curved decay envelope in [0,1]."""
    if t < attack:
        return t / attack
    p = (t - attack) / max(dur - attack, 1e-6)
    return max(0.0, (1.0 - p)) ** curve


def n_samples(dur):
    return int(SR * dur)


def sine(f, t):
    return math.sin(TAU * f * t)


TAU = 2.0 * math.pi


# ---- the sounds ----------------------------------------------------------------
def hop():
    """Boing: quick upward sine sweep with a touch of vibrato. The hero sound."""
    dur = 0.16
    out = []
    for i in range(n_samples(dur)):
        t = i / SR
        p = t / dur
        f = 300.0 + 340.0 * p * p          # accelerating rise
        f *= 1.0 + 0.02 * math.sin(TAU * 38.0 * t)
        s = sine(f, t) * 0.8 + sine(f * 2.0, t) * 0.15
        out.append(s * env(t, dur, 0.004, 2.2) * 0.75)
    return out


def splash(big=False):
    """Soft water splash: smoothed noise burst + a low 'bloop'."""
    dur = 0.55 if big else 0.26
    out = []
    lp = 0.0
    lp_a = 0.12 if big else 0.18           # lowpass amount (smaller = darker)
    for i in range(n_samples(dur)):
        t = i / SR
        lp += (random.uniform(-1, 1) - lp) * lp_a
        noise = lp * env(t, dur, 0.002, 3.5)
        bloop_f = (90.0 if big else 150.0) * (1.0 + 0.6 * env(t, dur * 0.4))
        bloop = sine(bloop_f, t) * env(t, dur * 0.5, 0.004, 2.0) * (0.55 if big else 0.35)
        out.append(noise * (1.1 if big else 0.8) + bloop)
    return out


def bonk():
    """The sad squeak. Descending, deflating, comedic -- never harsh."""
    dur = 0.34
    out = []
    for i in range(n_samples(dur)):
        t = i / SR
        p = t / dur
        f = 560.0 * (1.0 - 0.65 * p)        # droop
        f *= 1.0 + 0.06 * math.sin(TAU * 26.0 * t) * p   # wobble grows as it dies
        s = sine(f, t) * 0.7 + sine(f * 1.5, t) * 0.2    # slightly reedy
        out.append(s * env(t, dur, 0.006, 1.6) * 0.6)
    return out


def collect():
    """Sparkle: two quick soft pings, a fifth apart."""
    dur = 0.16
    out = []
    for i in range(n_samples(dur)):
        t = i / SR
        s = sine(990.0, t) * env(t, 0.09, 0.002, 2.5)
        if t > 0.05:
            t2 = t - 0.05
            s += sine(1485.0, t2) * env(t2, 0.10, 0.002, 2.5) * 0.8
        out.append(s * 0.42)
    return out


def chime():
    """Milestone bell. Pitched UP in-game each 100m so progress climbs a scale."""
    dur = 0.55
    out = []
    for i in range(n_samples(dur)):
        t = i / SR
        s = sine(660.0, t) + sine(1320.0, t) * 0.4 + sine(1980.0, t) * 0.12
        out.append(s * env(t, dur, 0.002, 2.8) * 0.4)
    return out


def mega():
    """MEGA HOP launch: a rising whoosh + heroic sweep. ~the loft duration's start."""
    dur = 0.9
    out = []
    lp = 0.0
    for i in range(n_samples(dur)):
        t = i / SR
        p = t / dur
        lp += (random.uniform(-1, 1) - lp) * (0.08 + 0.25 * p)   # noise opens up
        whoosh = lp * (0.25 + 0.75 * p) * 0.9
        f = 220.0 * (1.0 + 2.2 * p * p)
        tone = (sine(f, t) * 0.5 + sine(f * 1.5, t) * 0.2) * (0.3 + 0.5 * p)
        a = env(t, dur, 0.05, 1.2)
        out.append((whoosh + tone) * a * 0.8)
    return out


def laser():
    """DUCK LASER: descending pew with grit."""
    dur = 0.45
    out = []
    for i in range(n_samples(dur)):
        t = i / SR
        p = t / dur
        f = 1500.0 * (1.0 - 0.85 * p) + 120.0
        # cheap saw via two detuned sines + a square-ish 3rd harmonic
        s = sine(f, t) * 0.55 + sine(f * 1.01, t) * 0.35 + sine(f * 3.0, t) * 0.15
        s += random.uniform(-1, 1) * 0.08
        out.append(s * env(t, dur, 0.003, 1.4) * 0.6)
    return out


def quack():
    """One judgmental quack. Nasal AM saw with a pitch droop at the end."""
    dur = 0.22
    out = []
    for i in range(n_samples(dur)):
        t = i / SR
        p = t / dur
        f = 170.0 * (1.0 - 0.25 * max(0.0, p - 0.6))     # droops in the last 40%
        # buzzy: stacked harmonics ~ saw
        s = 0.0
        for k in range(1, 7):
            s += math.sin(TAU * f * k * t) / k
        s *= 0.45
        s *= 0.65 + 0.35 * math.sin(TAU * 27.0 * t)      # nasal AM flutter
        out.append(s * env(t, dur, 0.012, 1.3) * 0.7)
    return out


def unlock():
    """New duck fanfare: quick ascending major arpeggio."""
    notes = [523.25, 659.25, 783.99, 1046.5]   # C5 E5 G5 C6
    step = 0.085
    dur = step * len(notes) + 0.35
    out = [0.0] * n_samples(dur)
    for ni, f in enumerate(notes):
        start = ni * step
        ndur = 0.32 if ni < len(notes) - 1 else 0.5
        for i in range(n_samples(ndur)):
            t = i / SR
            idx = int((start + t) * SR)
            if idx < len(out):
                s = sine(f, t) * 0.8 + sine(f * 2.0, t) * 0.2
                out[idx] += s * env(t, ndur, 0.003, 2.4) * 0.35
    return out


def fwoosh():
    """Fireball whump for the mega-landing blast."""
    dur = 0.55
    out = []
    lp = 0.0
    for i in range(n_samples(dur)):
        t = i / SR
        p = t / dur
        lp += (random.uniform(-1, 1) - lp) * (0.10 + 0.28 * (1.0 - p))
        rumble = sine(62.0 * (1.0 - 0.3 * p), t) * 0.5
        a = env(t, dur, 0.015, 1.8)
        out.append((lp * 1.1 + rumble) * a * 0.9)
    return out


def ribbit():
    """A startled frog. Low, wet, brief."""
    dur = 0.16
    out = []
    for i in range(n_samples(dur)):
        t = i / SR
        p = t / dur
        f = 96.0 * (1.0 + 0.18 * math.sin(TAU * 11.0 * t)) * (1.0 - 0.2 * p)
        s = 0.0
        for k in range(1, 6):
            s += math.sin(TAU * f * k * t) / k
        s *= 0.5 * (0.6 + 0.4 * math.sin(TAU * 42.0 * t))
        out.append(s * env(t, dur, 0.008, 1.4) * 0.65)
    return out


def crunch():
    """Woody log-splinter thunk for the landing shockwave."""
    dur = 0.22
    out = []
    lp = 0.0
    for i in range(n_samples(dur)):
        t = i / SR
        lp += (random.uniform(-1, 1) - lp) * 0.35
        thump = sine(95.0 * (1.0 - 0.3 * t / dur), t) * 0.5 * env(t, dur * 0.6, 0.002, 2.0)
        out.append(lp * env(t, dur, 0.001, 3.0) * 0.9 + thump)
    return out


def peep():
    """A duckling's tiny chirp."""
    dur = 0.12
    out = []
    for i in range(n_samples(dur)):
        t = i / SR
        p = t / dur
        f = 1500.0 + 500.0 * math.sin(p * math.pi)      # chirp up then down
        s = sine(f, t) * 0.8 + sine(f * 2.0, t) * 0.1
        out.append(s * env(t, dur, 0.004, 2.0) * 0.4)
    return out


def squeak():
    """A real rubber-duck squeak: a reedy two-part 'eee-EEP'. The pitch swoops UP
    on the squeeze and snaps higher on release -- bright, breathy, comedic."""
    dur = 0.20
    out = []
    for i in range(n_samples(dur)):
        t = i / SR
        p = t / dur
        # pitch contour: swoop up through the squeeze, then a higher release chirp
        if p < 0.62:
            f = 720.0 + 900.0 * (p / 0.62)               # 720 -> 1620 squeeze
        else:
            f = 1500.0 + 360.0 * math.sin((p - 0.62) / 0.38 * math.pi)
        # reedy square-ish tone (odd harmonics), a touch of breath
        s = 0.0
        for k in (1, 3, 5, 7):
            s += math.sin(TAU * f * k * t) / k
        s *= 0.5
        s += 0.12 * random.uniform(-1, 1) * max(0.0, 1.0 - p)   # airy squeeze hiss
        # two little amplitude lobes (the in/out of a squeeze)
        lobe = 0.55 + 0.45 * abs(math.sin(p * math.pi))
        out.append(s * lobe * env(t, dur, 0.004, 1.6) * 0.8)
    return out


def gutlaugh():
    """SNAPZ's big guttural villain laugh: HUH-HUH-HUH-HUHHH, low, rough and gleeful."""
    bursts = [(0.00, 132, 0.13), (0.18, 120, 0.13), (0.36, 110, 0.14), (0.54, 98, 0.34)]
    dur = 1.0
    out = [0.0] * n_samples(dur)
    for (start, f0, blen) in bursts:
        for i in range(n_samples(blen)):
            t = i / SR
            f = f0 * (1.0 - 0.08 * (t / blen))               # each HUH sags downward
            ph = TAU * f * t
            s = 0.0
            for k in range(1, 9):                            # rough sawtooth voice
                s += math.sin(k * ph) / k
            s *= 0.5
            s += 0.18 * random.uniform(-1, 1)                # throat gravel
            s *= 0.6 + 0.4 * math.sin(TAU * 22.0 * t)        # guttural AM warble
            idx = int((start + t) * SR)
            if idx < len(out):
                out[idx] += s * env(t, blen, 0.01, 1.6) * 0.5
    for i in range(len(out)):                                # a low sub-rumble underneath
        t = i / SR
        out[i] += math.sin(TAU * 55.0 * t) * 0.18 * max(0.0, 1.0 - t / dur)
    return out


def click():
    """UI tick."""
    dur = 0.05
    out = []
    for i in range(n_samples(dur)):
        t = i / SR
        out.append(sine(1100.0, t) * env(t, dur, 0.001, 3.0) * 0.3)
    return out


if __name__ == "__main__":
    save("hop.wav", hop())
    save("splash.wav", splash(False))
    save("splash_big.wav", splash(True))
    save("bonk.wav", bonk())
    save("collect.wav", collect())
    save("chime.wav", chime())
    save("mega.wav", mega())
    save("laser.wav", laser())
    save("quack.wav", quack())
    save("unlock.wav", unlock())
    save("click.wav", click())
    save("peep.wav", peep())
    save("crunch.wav", crunch())
    save("ribbit.wav", ribbit())
    save("fwoosh.wav", fwoosh())
    save("squeak.wav", squeak())
    save("laugh.wav", gutlaugh())
    print("done.")
