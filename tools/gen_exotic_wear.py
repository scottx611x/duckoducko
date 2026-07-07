#!/usr/bin/env python3
"""TRUE wearable melds for the secret species (rusty, sadiedog): every hat is
TRANSLATED from the mallard's head to the exotic model's actual head, occluded
against that body, rendered at that species' own scale (+ Sadie's waterline
shift), and MEGA hat-stack slices are baked so the tumble stays welded."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from voxel_duck import (shade, render_wear, build, build_hat, build_hawk,   # noqa: E402
                        hat_stack_slices, GAME_YAW, PITCH, HERO_YAW, HERO_PITCH,
                        SIDE_YAW, SIDE_PITCH, BANK_OFF)
from gen_sadie import build_boss  # noqa: E402
from PIL import Image  # noqa: E402

ART = os.path.join(os.path.dirname(__file__), "..", "art")
IDS = ("crown", "pirate", "party", "lilypad", "souwester", "prop", "chef", "bandana",
       "halo", "boombox", "scarf", "goggles", "heron", "turtle", "cape", "vest",
       "jetpack", "satchel", "raccoon")


def head_anchor(V):
    """(x, top-y, z) of the model's head: topmost voxels within the FRONT third (z-max side)."""
    zs = [p[2] for p in V]
    zmin, zmax = min(zs), max(zs)
    zcut = zmax - (zmax - zmin) * 0.34
    front = [p for p in V if p[2] >= zcut]
    ytop = max(p[1] for p in front)
    crown = [p for p in front if p[1] >= ytop - 1]
    return (sum(p[0] for p in crown) / len(crown), ytop,
            sum(p[2] for p in crown) / len(crown))


def dog_anchor(V):
    """Sadie sits upright: her head is simply the TOPMOST voxels, wherever they are."""
    ytop = max(p[1] for p in V)
    crown = [p for p in V if p[1] >= ytop - 1]
    return (sum(p[0] for p in crown) / len(crown), ytop,
            sum(p[2] for p in crown) / len(crown))


def shift(V, d):
    return {(p[0] + d[0], p[1] + d[1], p[2] + d[2]): c for p, c in V.items()}


def waterline(img):
    w, h = img.size
    keep = int(h * 0.74)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(img.crop((0, 0, w, keep)), (0, h - keep))
    return out


def main():
    gy = math.radians(GAME_YAW)
    from voxel_duck import build_sadie
    mal = build("mallard", "folded")
    A = head_anchor(mal)
    # (gameplay body, gameplay anchor) + (menu body, menu anchor) per species —
    # sadie SWIMS in-game (hat on the swimming head) but SITS in menus
    species = [
        ("rusty", build_hawk(0), head_anchor, build_hawk(0), head_anchor, 1.05),
        ("sadiedog", build_sadie(0), head_anchor, build_boss("idle", 0), dog_anchor, 1.5),
    ]
    for sp, Vg, ag, Vm, am, sc in species:
        dg_ = ag(Vg); dm_ = am(Vm)
        dg = (int(round(dg_[0] - A[0])), int(round(dg_[1] - A[1])), int(round(dg_[2] - A[2])))
        dm = (int(round(dm_[0] - A[0])), int(round(dm_[1] - A[1])), int(round(dm_[2] - A[2])))
        SHg = shade(Vg)
        SHm = shade(Vm)
        for hid in IDS:
            H0 = build_hat(hid)
            if not H0:
                continue
            Hg = shift(H0, dg)
            Hm = shift(H0, dm)
            pre = os.path.join(ART, "wear3d_%s_%s_" % (sp, hid))
            render_wear(SHg, Hg, gy, PITCH, out=64, scale=sc).save(pre + "idle.png")
            for i, off in enumerate(BANK_OFF):
                render_wear(SHg, Hg, math.radians(GAME_YAW + off), PITCH, out=64, scale=sc).save(pre + "bank_%d.png" % i)
            render_wear(SHg, Hg, math.radians(GAME_YAW + SIDE_YAW), SIDE_PITCH, out=64, scale=sc).save(pre + "side_left.png")
            render_wear(SHg, Hg, math.radians(GAME_YAW - SIDE_YAW), SIDE_PITCH, out=64, scale=sc).save(pre + "side_right.png")
            render_wear(SHm, Hm, math.radians(HERO_YAW), math.radians(HERO_PITCH), out=64, scale=sc).save(pre + "hero.png")
            for i in range(24):
                render_wear(SHm, Hm, math.radians(i * 15), math.radians(HERO_PITCH), out=64, scale=sc).save(pre + "spin_%02d.png" % i)
            for ii, sl in hat_stack_slices(Vg, Hg, shade(Hg)):   # MEGA meld rides the tumbling body
                sl.save(os.path.join(ART, "wear_%s_%s_stack_%02d.png" % (hid, sp, ii)))
        print("  %s: melds done (game %s, menu %s)" % (sp, dg, dm))


if __name__ == "__main__":
    main()
