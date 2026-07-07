#!/usr/bin/env python3
"""SADIE THE BOUNDLESS — the dedicated render (Scott: "my Sadie girl").

One upgraded voxel model of Sadie (chocolate lab: rich dark-chocolate coat, AMBER
eyes, floppy ears, tan collar, happy pink tongue), rendered two ways:
  - sadieboss_*  : high-res final-boss set (~320px canvas)
  - sadie_greet / sadie_p0..p4 / sadie_spin_00..15 : wardrobe + codex replacements
    at their EXACT existing dimensions (Main.gd anchors depend on them)

Run from repo root:  python3 tools/gen_sadie.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from voxel_duck import shade, render, _vox_helpers, build_sadie_run  # noqa: E402
from PIL import Image  # noqa: E402

ART = os.path.join(os.path.dirname(__file__), "..", "art")

# the real Sadie's palette — dry, warm, loved
COAT = (86, 54, 36)
COATL = (126, 86, 58)      # warm top-light zones
COATD = (56, 36, 24)
CHEST = (112, 74, 50)      # slightly lighter chest (still all-brown — NO white)
PAW = (104, 72, 50)
AMBER = (198, 142, 58)     # her signature eyes
PUPIL = (30, 24, 20)
LID = (48, 32, 22)
NOSE = (34, 26, 22)
TONGUE = (240, 122, 150)
TONGUED = (206, 90, 122)
COLLAR = (196, 58, 52)     # HER red — the muted brick-red of her harness (Scott's photo)
TAG = (234, 194, 88)


def build_boss(pose="idle", bob=0):
    """Seated (or posed) full-body Sadie, ~1.6x the density of the old greeter.
    poses: idle | proud (eyes-closed happy arcs, tongue way out) | crouch (play-bow)
           | pounce (airborne, paws spread) | point (rigid, one paw up)"""
    V = {}
    put, ellip, box = _vox_helpers(V)
    crouch = pose == "crouch"
    pounce = pose == "pounce"
    point = pose == "point"
    proud = pose == "proud"
    run = pose == "run"
    runph = bob if run else 0                            # gallop phase 0..3: stretch, gather, tuck, drive
    if run:
        bob = 0

    # ---- body ----
    if run:
        # full gallop, side-read: one continuous horizontal body (NO segmented lumps — the
        # old swimming-gait render stacked spheres and read like Pokey at boss scale)
        stretch = [1.0, 0.4, 0.0, 0.6][runph]            # 1 = full extension, 0 = tucked
        # a LAB gallops: SHORT back, DEEP chest, LONG legs. (v1 was a hotdog on casters.)
        for zi in range(-8, 9):                           # compact torso, nose to rump
            t = (zi + 8) / 16.0
            ry = 3.4 + 1.6 * math.sin(t * math.pi)        # deep through the ribs
            rx = 2.5 + 1.0 * math.sin(t * math.pi)
            yc = 4.2 + 0.5 * math.cos(t * 2.6)            # HIGH shoulder line — legs get room
            ellip(0, yc, zi * (0.8 + 0.2 * stretch), rx, ry, 0.9, COAT)
        ellip(0, 6.8, -1, 2.4, 1.3, 3.6 + 1.2 * stretch, COATL)   # back highlight
        ellip(0, 2.2, 4.0 + 1.4 * stretch, 2.6, 2.6, 2.2, CHEST)  # the deep lab chest, leading
        fore_z = 6.0 + 3.0 * stretch
        hind_z = -6.0 - 3.0 * stretch
        for s in (1, -1):                                 # forelegs: LONG, reaching in the stretch
            for i in range(7):
                fz = fore_z + i * (0.7 * stretch) - (i * 0.45 * (1.0 - stretch))
                fy = 2.5 - i * (1.15 + 0.25 * stretch)
                ellip(s * 2.0, fy, fz, 1.25 - i * 0.06, 0.9, 1.15 - i * 0.05, COAT if i < 6 else PAW)
        for s in (1, -1):                                 # hind legs: LONG drive off the haunch
            ellip(s * 2.4, 3.0, -6.5, 1.9, 2.4, 2.6, COAT)
            for i in range(7):
                hz2 = hind_z - i * (0.8 * stretch) + (i * 0.4 * (1.0 - stretch))
                hy2 = 2.0 - i * (1.05 + 0.2 * stretch)
                ellip(s * 2.1, hy2, hz2, 1.3 - i * 0.06, 0.9, 1.2 - i * 0.05, COATD if i < 6 else PAW)
    elif pounce:
        # airborne: body stretched level, legs in clean paired diagonals
        ellip(0, 2, -1, 4.4, 3.2, 7.0, COAT)
        ellip(0, 4.0, -1, 3.2, 1.9, 5.4, COATL)                       # sunlit back
        ellip(0, 0.2, 2.5, 3.2, 2.2, 3.8, CHEST, only_empty=True)     # chest
        for sx in (1, -1):                                            # forelegs: reaching forward-down
            for i in range(5):
                ellip(sx * 2.6, 0.5 - i * 0.9, 5.5 + i * 0.7, 1.2, 0.9, 1.2, COAT if i < 4 else PAW)
        for sx in (1, -1):                                            # hind legs: trailing back-down
            for i in range(5):
                ellip(sx * 2.6, 0.5 - i * 0.7, -6.5 - i * 0.8, 1.3, 0.9, 1.3, COATD if i < 4 else PAW)
    elif crouch:
        # play-bow: chest DOWN at the front, rump HIGH at the back, tail flag up
        ellip(0, 4.8, -5, 4.0, 3.0, 3.8, COAT)                        # raised rump (connected, not a ball)
        ellip(0, 6.3, -5, 2.8, 1.5, 2.8, COATL)
        ellip(0, 3.4, -2.8, 3.8, 2.8, 3.4, COAT)                      # upper slope off the rump
        ellip(0, 1.6, -0.5, 3.7, 2.6, 3.4, COAT)                      # sloping back into the chest
        ellip(0, -1.0, 3, 3.8, 2.4, 4.2, COAT)                        # chest low + forward
        ellip(0, -2.0, 4.5, 2.8, 1.6, 2.8, CHEST, only_empty=True)
        for s in (1, -1):                                             # forelegs stretched flat on the water
            for zz in range(5, 10):
                ellip(s * 2.4, -3.4, zz, 1.2, 0.8, 1.0, COAT if zz < 8 else PAW)
        for s in (1, -1):                                             # hind legs planted under the rump
            for yy in range(0, 5):
                ellip(s * 2.6, yy, -7, 1.3, 1.0, 1.4, COATD)
            ellip(s * 2.6, -0.5, -6.2, 1.4, 0.8, 1.5, PAW)
    else:
        # seated tall (idle / proud / point)
        chest_up = 1 if proud else 0
        # she sits TALL: an upright torso column, chest proud, no humped back (the photo)
        # upright torso with the APEX FORWARD + a real neck — the old single column
        # peaked at the rear and read as a hunchback from profile/back
        ellip(0, 2 + chest_up, 0.4, 4.0, 4.7, 3.9, COAT)              # torso, apex shifted forward
        ellip(0, 0.5 + chest_up, -1.6, 3.7, 3.6, 3.2, COAT)           # rear taper (lower than the withers)
        ellip(0, 5.2 + chest_up, 1.1, 2.6, 2.2, 2.6, COATL)           # shoulder light, over the chest
        ellip(0, 6.6 + chest_up, 1.8, 2.3, 2.7, 2.3, COAT)            # NECK: smooth bridge into the skull
        ellip(0, 1.5 + chest_up, 3.0, 2.8, 3.4, 2.0, CHEST)           # the proud chest column
        ellip(0, -3.5, -3.5, 5.0, 3.4, 4.6, COAT)                     # haunches
        ellip(0, -1.8, -5.2, 3.4, 2.0, 2.8, COATL)
        for s in (1, -1):                                             # front legs
            raised = point and s == 1
            top = 1 if raised else -1
            for yy in range(-7, top + 1):
                zz = 4.6 if not raised else 4.6 + (top - yy) * 0.25
                ellip(s * 2.6, yy, zz, 1.4, 1.0, 1.5, COAT if yy > -5 else COATD)
            if raised:
                ellip(s * 2.6, top + 0.5, 6.2, 1.4, 0.9, 1.6, PAW)    # the pointing paw, tucked up
            else:
                ellip(s * 2.6, -7.2, 5.0, 1.5, 0.9, 1.7, PAW)
        for s in (1, -1):
            ellip(s * 3.4, -6.6, -5.0, 1.2, 0.9, 1.4, PAW, only_empty=True)  # rear paws peeking

    # ---- head ----
    hb = bob
    hy = 9.0 + hb + (1 if proud else 0) - (6.5 if crouch else 0) - (4.5 if pounce else 0) - (0.5 if run else 0)
    hz = 2.2 + (3.8 if crouch or pounce else 0) + (2.8 if point else 0) + (8.5 if run else 0)
    ellip(0, hy, hz, 3.4, 3.2, 3.2, COAT)                             # skull
    ellip(0, hy + 1.8, hz + 0.4, 2.6, 1.6, 2.6, COATL)                # solid crown light
    for s in (1, -1):                                                 # brow ridges above the eyes
        put(s * 2, round(hy + 2.6), round(hz + 2.8), COATL)
        put(s * 1, round(hy + 2.8), round(hz + 2.8), COATL)
    # muzzle: blockier lab snout, lighter snoot bridge
    box(-2, 2, round(hy - 1.5), round(hy + 0.8), round(hz + 3), round(hz + 6), COAT)
    for zz in range(round(hz + 3), round(hz + 6)):
        put(0, round(hy + 1.0), zz, COATL, only_empty=True)           # snoot bridge
    box(-1, 1, round(hy + 0.2), round(hy + 1.0), round(hz + 6), round(hz + 6), NOSE)
    put(0, round(hy + 0.6), round(hz + 7), NOSE)                      # nose tip
    # mouth open + the happy tongue (longer when proud)
    tl = 4 if proud else 2
    for i in range(tl):
        ty = round(hy - 2.2 - i * 0.8)
        put(0, ty, round(hz + 5 + (0 if i < 2 else -0.0)), TONGUE if i % 2 == 0 else TONGUED)
        put(-1 if i % 2 else 1, ty, round(hz + 5), TONGUE)
    # eyes: AMBER iris, dark pupil, grounded lower lid — or happy-closed arcs when proud
    for s in (1, -1):
        ex, ey, ez = s * 2, round(hy + 1.6), round(hz + 3.1)
        if proud:
            put(ex, ey, ez, LID)
            put(ex + (0 if s == 1 else 0), ey - 1, ez, LID)           # a little closed arc
            put(ex - s, ey, ez, LID)
        else:
            put(ex, ey, ez, AMBER)
            put(ex - s, ey, ez, AMBER)
            put(ex, ey + 1, ez, LID)
            put(ex - s, ey + 1, ez, LID)
            put(ex, ey, ez + 1, PUPIL)
    # floppy ears: hanging sheets with a darker inner fold (flying when pouncing/running)
    for s in (1, -1):
        if pounce or run:
            for i in range(4):
                for dy in (0, 1):
                    put(s * 3, round(hy + 1 + i * 0.5) + dy, round(hz - 1 - i), COATD)
                    put(s * 4, round(hy + 0.5 + i * 0.5) + dy, round(hz - 1.4 - i), COATD)
        else:
            for yy in range(round(hy - 2), round(hy + 3)):
                put(s * 3, yy, round(hz - 0.5), COATD)
                put(s * 4, yy, round(hz - 1.2), COATD)
                if yy < hy:
                    put(s * 3, yy, round(hz + 0.4), (46, 30, 20))     # inner fold shadow
            put(s * 3, round(hy - 3), round(hz), COATD)               # the droopy tip
    # HER red collar: recolor the actual neck SURFACE at collar height, so it wraps the
    # body it's on — the old free-floating ring was built for pre-rebuild geometry and
    # clipped straight through her throat
    cy0 = round(hy - 3.6)
    front_z = None
    for (vx, vy, vz) in list(V.keys()):
        if vy in (cy0, cy0 + 1) and abs(vx) <= 4 and hz - 4.0 < vz < hz + 4.0:
            exposed = any((vx + dx, vy + dy, vz + dz) not in V
                          for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)))
            if exposed:
                V[(vx, vy, vz)] = COLLAR
                if vx == 0 and vy == cy0 and (front_z is None or vz > front_z):
                    front_z = vz
    if front_z is not None:                                # the tag hangs from the collar's FRONT
        put(0, cy0 - 1, front_z, TAG)
        put(0, cy0 - 2, front_z, TAG)
    # tail: a happy plume (straight back when pointing, up + curled otherwise)
    if run:
        for i in range(6):
            put(0, round(5.5 + i * 0.35), round(-9 - i * 0.9), COAT if i < 4 else COATL)
    elif point:
        for i in range(6):
            put(0, round(2 + i * 0.1), -7 - i, COAT if i < 4 else COATL)
    elif not pounce:
        for i in range(7):
            put(round(i * 0.3) * (1 if bob else -1) if i > 3 else 0,
                round(-2 + i * 1.1), round(-6.5 - i * 0.55), COAT if i < 5 else COATL)
    else:
        for i in range(5):
            put(0, round(3 + i * 0.4), -8 - i, COAT if i < 3 else COATL)
    return V


def fit(img, w, h):
    """center-crop/pad a render onto an exact w x h transparent canvas."""
    bb = img.getbbox()
    if bb:
        img = img.crop(bb)
    if img.width > w or img.height > h:
        img.thumbnail((w, h), Image.NEAREST)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(img, ((w - img.width) // 2, (h - img.height) // 2 + (h - img.height) % 2))
    return canvas


def save(img, name):
    img.save(os.path.join(ART, name))
    print("  ", name, img.size)


def main():
    Y = math.radians
    # ---- BOSS SET (hi-res: the model is rendered LARGE, detail is real) ----
    save(render(shade(build_boss("idle", 0)), Y(14), Y(10), out=320, scale=8.6), "sadieboss_idle_0.png")
    save(render(shade(build_boss("idle", 1)), Y(22), Y(10), out=320, scale=8.6), "sadieboss_idle_1.png")
    save(render(shade(build_boss("point")), Y(-38), Y(8), out=320, scale=8.2), "sadieboss_glance_l.png")
    save(render(shade(build_boss("point")), Y(38), Y(8), out=320, scale=8.2), "sadieboss_glance_r.png")
    save(render(shade(build_boss("crouch")), Y(16), Y(16), out=320, scale=8.2), "sadieboss_crouch.png")
    save(render(shade(build_boss("pounce")), Y(10), Y(30), out=320, scale=7.6), "sadieboss_pounce.png")
    save(render(shade(build_boss("proud", 0)), Y(12), Y(9), out=320, scale=8.6), "sadieboss_proud.png")
    for f in range(4):
        save(fit(render(shade(build_boss("run", f)), Y(90), Y(10), out=230, scale=5.4), 230, 160),
             "sadieboss_run_%d.png" % f)
    # ---- WARDROBE replacements (exact existing dimensions) ----
    save(render(shade(build_boss("proud", 0)), Y(18), Y(11), out=110, scale=3.0), "sadie_greet.png")
    save(render(shade(build_boss("idle", 0)), Y(18), Y(11), out=110, scale=3.0), "sadie_p0.png")
    save(render(shade(build_boss("idle", 1)), Y(18), Y(11), out=110, scale=3.0), "sadie_p1.png")
    save(render(shade(build_boss("idle", 0)), Y(4), Y(11), out=110, scale=3.0), "sadie_p2.png")
    save(render(shade(build_boss("idle", 0)), Y(34), Y(11), out=110, scale=3.0), "sadie_p3.png")
    save(render(shade(build_boss("idle", 0)), Y(18), Y(11), out=110, scale=3.0), "sadie_p4.png")
    # ---- WARDROBE/AMBIENT gallop (exact 86x60): SAME model as the boss dash —
    # the old swimming-gait renders survived here and were, verbatim, "the scariest
    # thing I've ever seen". 8 slots cycle the 4-phase gallop twice. ----
    for f in range(8):
        save(fit(render(shade(build_boss("run", f % 4)), Y(90), Y(10), out=120, scale=2.6), 86, 60),
             "sadie_run_%d.png" % f)
    # ---- CODEX spin (16 yaws, exact 56x40) ----
    SH = shade(build_boss("idle", 0))
    for i in range(16):
        save(fit(render(SH, Y(i * 22.5), Y(30), out=80, scale=1.55), 56, 40), "sadie_spin_%02d.png" % i)
    print("done.")


if __name__ == "__main__":
    main()
