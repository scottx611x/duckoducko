#!/usr/bin/env python3
"""Render RUSTY's LEAD frames: back view (tail to camera, head up-river) for
when he flies the Thermals course ahead of you — same shading/scale as the
front-facing tip-drop frames, just spun to the gameplay camera's yaw."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from voxel_duck import shade, render, build_hawk, GAME_YAW  # noqa: E402

ART = os.path.join(os.path.dirname(__file__), "..", "art")


def main():
    yaw = math.radians(GAME_YAW + 20)   # back view w/ the same 20-degree 3/4 twist as his front set
    imgs = [render(shade(build_hawk(f)), yaw, math.radians(22), out=160, scale=3.4)
            for f in (0, 1, 2)]
    bb = None
    for im in imgs:
        b = im.getbbox()
        if b:
            bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    bb = (max(0, bb[0] - 3), max(0, bb[1] - 3), min(160, bb[2] + 3), min(160, bb[3] + 3))
    for f, im in enumerate(imgs):
        p = os.path.join(ART, "hawk_lead_%d.png" % f)
        im.crop(bb).save(p)
        print("  hawk_lead_%d.png" % f, im.crop(bb).size)


if __name__ == "__main__":
    main()
