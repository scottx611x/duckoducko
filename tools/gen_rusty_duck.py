#!/usr/bin/env python3
"""RUSTY as a PLAYABLE: the full duck-species sprite set rendered from his own
voxel model. He doesn't paddle — he GLIDES over the water, so 'idle' is his
level glide and hops are real wingbeats. Mirrors generate_ducks' output list
exactly (idle/hero/quack/spin/spinq/bank/turn/side/hop/flap/face/stack)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from voxel_duck import (shade, render, build_hawk, stack_slices,   # noqa: E402
                        GAME_YAW, PITCH, HERO_YAW, HERO_PITCH,
                        SIDE_YAW, SIDE_PITCH, BANK_OFF, FACE_CANVAS)

ART = os.path.join(os.path.dirname(__file__), "..", "art")
SP = "rusty"
SC = 1.05          # wingspan is wide — body lands near duck-size at this scale


def save(img, name):
    img.save(os.path.join(ART, name))


def main():
    gy = math.radians(GAME_YAW)
    SH = shade(build_hawk(0))                 # level glide = his 'floating'
    SHq = shade(build_hawk(0, beak_open=True))
    SHup = shade(build_hawk(1))               # upstroke
    SHdn = shade(build_hawk(2))               # downstroke
    # idle: glide with a gentle pitch bob (same trick as the ducks' head-bob)
    save(render(SH, gy, PITCH, scale=SC), "%s_idle_0.png" % SP)
    save(render(SH, gy, PITCH - math.radians(4), scale=SC), "%s_idle_1.png" % SP)
    save(render(SH, math.radians(HERO_YAW), math.radians(HERO_PITCH), scale=SC), "%s_hero.png" % SP)
    save(render(SHq, math.radians(HERO_YAW), math.radians(HERO_PITCH), scale=SC), "%s_quack.png" % SP)
    for i in range(24):
        save(render(SH, math.radians(i * 15), math.radians(HERO_PITCH), scale=SC), "%s_spin_%02d.png" % (SP, i))
        save(render(SHq, math.radians(i * 15), math.radians(HERO_PITCH), scale=SC), "%s_spinq_%02d.png" % (SP, i))
    for i, off in enumerate(BANK_OFF):
        save(render(SH, math.radians(GAME_YAW + off), PITCH, scale=SC), "%s_bank_%d.png" % (SP, i))
    save(render(SH, math.radians(GAME_YAW + 15), PITCH, scale=SC), "%s_turn_left.png" % SP)
    save(render(SH, math.radians(GAME_YAW - 15), PITCH, scale=SC), "%s_turn_right.png" % SP)
    save(render(SH, math.radians(GAME_YAW + SIDE_YAW), SIDE_PITCH, scale=SC), "%s_side_left.png" % SP)
    save(render(SH, math.radians(GAME_YAW - SIDE_YAW), SIDE_PITCH, scale=SC), "%s_side_right.png" % SP)
    # hops are honest WINGBEATS
    save(render(SHup, gy, PITCH, scale=SC), "%s_hop_0.png" % SP)
    save(render(SHdn, gy, PITCH, scale=SC), "%s_hop_1.png" % SP)
    for i in range(24):
        save(render(SHup, math.radians(i * 15), math.radians(HERO_PITCH), scale=SC), "%s_flap_%02d.png" % (SP, i))
    # the fierce close-up
    save(render(SH, math.radians(0), math.radians(15), out=FACE_CANVAS,
                scale=1.8, cy_frac=0.46), "%s_face.png" % SP)
    # mega-hop sprite stack from his real voxels
    Vf = build_hawk(0)
    for i, sl in enumerate(stack_slices(Vf, shade(Vf))):
        save(sl, "%s_stack_%02d.png" % (SP, i))
    print("rusty playable set rendered.")


if __name__ == "__main__":
    main()
