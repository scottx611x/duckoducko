#!/usr/bin/env python3
"""Re-render ONLY Bongo + Barry art after voxel model edits (mirrors the exact
calls in voxel_duck's main generate — same yaws, pitches, scales, crops)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from voxel_duck import shade, render, build_bongo, build_beaver  # noqa: E402

ART = os.path.join(os.path.dirname(__file__), "..", "art")


def save(img, name):
    img.save(os.path.join(ART, name))
    print("  ", name, img.size)


def shared_crop(imgs, out):
    bb = None
    for im in imgs:
        b = im.getbbox()
        if b:
            bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    return (max(0, bb[0] - 4), max(0, bb[1] - 4), min(out, bb[2] + 4), min(out, bb[3] + 4))


def spin_set(SH, name, pitch_deg, scale, out=220, n=16):
    imgs = [render(SH, math.radians(i * 360.0 / n), math.radians(pitch_deg), out=out, scale=scale)
            for i in range(n)]
    bb = shared_crop(imgs, out)
    for i, im in enumerate(imgs):
        save(im.crop(bb), "%s_spin_%02d.png" % (name, i))


def main():
    bongo_imgs = [render(shade(build_bongo(f)), math.radians(10), math.radians(20), out=320, scale=5.0)
                  for f in (0, 1, 2)]
    bgb = shared_crop(bongo_imgs, 320)
    for f, im in enumerate(bongo_imgs):
        save(im.crop(bgb), "bongo_%d.png" % f)
    save(render(shade(build_bongo(2)), math.radians(10), math.radians(20), out=320, scale=5.0).crop(bgb), "bongo_open.png")

    beaver_imgs = [render(shade(build_beaver(f)), math.radians(8), math.radians(18), out=320, scale=5.2)
                   for f in (0, 1, 2)]
    bvb = shared_crop(beaver_imgs, 320)
    for f, im in enumerate(beaver_imgs):
        save(im.crop(bvb), "beaver_%d.png" % f)

    spin_set(shade(build_beaver(0)), "beaver", 20, 5.2, out=320)
    spin_set(shade(build_beaver(2)), "beaver_open", 20, 5.2, out=320)
    spin_set(shade(build_bongo(0)), "bongo", 20, 5.0, out=320)
    spin_set(shade(build_bongo(2)), "bongo_open", 20, 5.0, out=320)
    print("done.")


if __name__ == "__main__":
    main()
