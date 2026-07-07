#!/usr/bin/env python3
"""PLAYABLE SADIE: the full duck-species sprite set ("sadiedog_*") rendered from
her one true voxel model (gen_sadie.build_boss). She SWIMS — gameplay back-view
frames are cropped at the waterline (chest-deep lab), hops are her POUNCE
(airborne, paws spread), and menus show the full seated good girl."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from voxel_duck import (shade, render, stack_slices,   # noqa: E402
                        GAME_YAW, PITCH, HERO_YAW, HERO_PITCH,
                        SIDE_YAW, SIDE_PITCH, BANK_OFF, FACE_CANVAS)
from gen_sadie import build_boss  # noqa: E402
from PIL import Image  # noqa: E402

ART = os.path.join(os.path.dirname(__file__), "..", "art")
SP = "sadiedog"
SC = 1.5
OUT = 64


def save(img, name):
    img.save(os.path.join(ART, name))


def waterline(img):
    """Crop the bottom ~26% (submerged legs) — she's swimming, not standing."""
    w, h = img.size
    keep = int(h * 0.74)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(img.crop((0, 0, w, keep)), (0, h - keep))
    return out


def main():
    gy = math.radians(GAME_YAW)
    SH0 = shade(build_boss("idle", 0))
    SH1 = shade(build_boss("idle", 1))
    SHq = shade(build_boss("proud"))       # tongue out = her "quack"
    SHp = shade(build_boss("pounce"))
    # gameplay back views: chest-deep swimmer
    save(waterline(render(SH0, gy, PITCH, out=OUT, scale=SC)), "%s_idle_0.png" % SP)
    save(waterline(render(SH1, gy, PITCH - math.radians(4), out=OUT, scale=SC)), "%s_idle_1.png" % SP)
    for i, off in enumerate(BANK_OFF):
        save(waterline(render(SH0, math.radians(GAME_YAW + off), PITCH, out=OUT, scale=SC)), "%s_bank_%d.png" % (SP, i))
    save(waterline(render(SH0, math.radians(GAME_YAW + 15), PITCH, out=OUT, scale=SC)), "%s_turn_left.png" % SP)
    save(waterline(render(SH0, math.radians(GAME_YAW - 15), PITCH, out=OUT, scale=SC)), "%s_turn_right.png" % SP)
    save(waterline(render(SH0, math.radians(GAME_YAW + SIDE_YAW), SIDE_PITCH, out=OUT, scale=SC)), "%s_side_left.png" % SP)
    save(waterline(render(SH0, math.radians(GAME_YAW - SIDE_YAW), SIDE_PITCH, out=OUT, scale=SC)), "%s_side_right.png" % SP)
    # hops: the POUNCE, whole dog airborne
    save(render(SHp, gy, PITCH, out=OUT, scale=SC * 0.92), "%s_hop_0.png" % SP)
    save(render(SHp, gy, PITCH - math.radians(6), out=OUT, scale=SC * 0.92), "%s_hop_1.png" % SP)
    # menus: the full seated good girl
    save(render(SH0, math.radians(HERO_YAW), math.radians(HERO_PITCH), out=OUT, scale=SC), "%s_hero.png" % SP)
    save(render(SHq, math.radians(HERO_YAW), math.radians(HERO_PITCH), out=OUT, scale=SC), "%s_quack.png" % SP)
    for i in range(24):
        save(render(SH0, math.radians(i * 15), math.radians(HERO_PITCH), out=OUT, scale=SC), "%s_spin_%02d.png" % (SP, i))
        save(render(SHq, math.radians(i * 15), math.radians(HERO_PITCH), out=OUT, scale=SC), "%s_spinq_%02d.png" % (SP, i))
        save(render(SHp, math.radians(i * 15), math.radians(HERO_PITCH), out=OUT, scale=SC * 0.92), "%s_flap_%02d.png" % (SP, i))
    # the face: those amber eyes, close up
    save(render(SH0, math.radians(0), math.radians(12), out=FACE_CANVAS, scale=1.1, cy_frac=0.30), "%s_face.png" % SP)
    # mega-hop voxel stack
    Vf = build_boss("idle", 0)
    n = 0
    for i, sl in enumerate(stack_slices(Vf, shade(Vf))):
        save(sl, "%s_stack_%02d.png" % (SP, i))
        n = i + 1
    print("sadiedog set rendered (%d stack slices)" % n)


if __name__ == "__main__":
    main()
