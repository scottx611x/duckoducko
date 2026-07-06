#!/usr/bin/env python3
"""HEN MEGA parity: render the voxel sprite-stack slices for every hen variant
so hens tumble as true 3D voxels during MEGA hops exactly like the drakes
(they previously fell back to the flat sprite)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from voxel_duck import shade, build, stack_slices, SPECIES  # noqa: E402

ART = os.path.join(os.path.dirname(__file__), "..", "art")
SKIP = ("hen", "rubberduck", "disco", "shadow")   # no hen variants (same set generate_ducks skips)


def main():
    for sp in SPECIES:
        if sp in SKIP:
            continue
        Vh = build(sp, "folded", hen_override=True)
        n = 0
        for i, sl in enumerate(stack_slices(Vh, shade(Vh))):
            sl.save(os.path.join(ART, "%shen_stack_%02d.png" % (sp, i)))
            n = i + 1
        print("  %shen: %d slices" % (sp, n))


if __name__ == "__main__":
    main()
