#!/usr/bin/env python3
"""Generate DUCKODUCKO pixel-art sprites into ../art/.

Anti-jank pipeline: every sprite is authored in FINAL pixel coordinates but drawn
onto a 4x SUPERSAMPLED canvas (HiDraw), then downscaled with LANCZOS and SNAPPED
back to the exact authored palette (crisp()).  Supersampling smooths the silhouette;
the palette-snap re-crisps the edges so it reads as deliberate pixel art instead of
ellipse mush.  Banking angles come from rotating the high-res master before crisping,
so turn frames are clean instead of NEAREST-rotated garbage.

Run:  python3 tools/gen_sprites.py    (from the project root)
Then: Godot --headless --path . --import   (so Godot picks up new PNGs)
"""
import os
import math
from PIL import Image, ImageDraw

ART = os.path.join(os.path.dirname(__file__), "..", "art")
os.makedirs(ART, exist_ok=True)
S = 4  # supersample factor

# ---- palette -----------------------------------------------------------------
OUT    = (30, 24, 20, 255)
# drake head (iridescent green: glint -> light -> mid -> dark nape)
GLINT  = (120, 210, 150, 255)
HEADH  = (70, 178, 104, 255)
HEADG  = (32, 120, 64, 255)
HEADD  = (20, 80, 44, 255)
# collar / white
WHITE  = (238, 238, 230, 255)
# chestnut breast
CHESTL = (160, 92, 54, 255)
CHEST  = (132, 74, 44, 255)
CHESTD = (104, 58, 34, 255)
# drake body greys (light -> mid -> dark)
BODYL  = (198, 190, 170, 255)
BODY   = (164, 154, 134, 255)
BODYD  = (126, 116, 98, 255)
WING   = (142, 132, 112, 255)
WINGD  = (108, 98, 82, 255)
PRIM   = (78, 70, 58, 255)
# blue speculum
SPEC   = (62, 112, 170, 255)
SPECD  = (40, 78, 122, 255)
# bill
BEAK   = (242, 184, 64, 255)
BEAKD  = (196, 140, 34, 255)
EYE    = (16, 16, 16, 255)
TAILD  = (44, 42, 52, 255)
# hen palette
HBUFF  = (196, 166, 122, 255)
HBODY  = (172, 142, 104, 255)
HBODYM = (150, 122, 88, 255)
HBODYD = (120, 94, 64, 255)
HWING  = (150, 122, 88, 255)
HWINGD = (118, 92, 62, 255)
HCROWN = (116, 88, 56, 255)
HBILL  = (212, 154, 74, 255)
HBILLD = (150, 104, 56, 255)
HCHEEK = (208, 180, 138, 255)


# ---- supersampled drawing ----------------------------------------------------
class HiDraw:
    """ImageDraw wrapper: author in final coords, render at S x resolution."""
    def __init__(self, img):
        self.img = img
        self.d = ImageDraw.Draw(img)

    def _b(self, box):
        return [v * S for v in box]

    def _p(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def ellipse(self, box, fill):
        self.d.ellipse(self._b(box), fill=fill)

    def rectangle(self, box, fill):
        self.d.rectangle(self._b(box), fill=fill)

    def rounded_rectangle(self, box, radius, fill):
        self.d.rounded_rectangle(self._b(box), radius=radius * S, fill=fill)

    def polygon(self, pts, fill):
        self.d.polygon(self._p(pts), fill=fill)

    def line(self, pts, fill, width=1):
        self.d.line(self._p(pts), fill=fill, width=max(1, width * S))

    def px(self, xy, col):
        x, y = xy
        self.d.rectangle([x * S, y * S, (x + 1) * S - 1, (y + 1) * S - 1], fill=col)


def _nearest(pal, rgb):
    br, bg, bb = rgb
    best, bd = pal[0], 1e18
    for c in pal:
        dr, dg, db = c[0] - br, c[1] - bg, c[2] - bb
        dist = dr * dr + dg * dg + db * db
        if dist < bd:
            bd, best = dist, c
    return best


def crisp(hi, w, h, alpha_cut=140):
    """Downscale a high-res master and snap every pixel to the authored palette."""
    pal = list({hi.getpixel((x, y)) for y in range(hi.height) for x in range(hi.width)
                if hi.getpixel((x, y))[3] == 255})
    if not pal:
        return Image.new("RGBA", (w, h), (0, 0, 0, 0))
    small = hi.resize((w, h), Image.LANCZOS)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sp, op = small.load(), out.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = sp[x, y]
            if a < alpha_cut:
                continue
            c = _nearest(pal, (r, g, b))
            op[x, y] = (c[0], c[1], c[2], 255)
    return out


def add_outline(img, col=OUT):
    px = img.load()
    w, h = img.size
    out = img.copy()
    opx = out.load()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] > 0:
                        opx[x, y] = col
                        break
    return out


def render(w, h, build):
    """Author build(g) in final w x h coords; get back a crisp, supersampled sprite."""
    hi = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    build(HiDraw(hi))
    return add_outline(crisp(hi, w, h))


# ---- the duck ----------------------------------------------------------------
TD = 44  # top-down canvas (square, leaves margin for banking rotation)


def _duck_master(hen=False, bob=0):
    """Detailed top-down duck on a TD*S canvas, head toward -y, centered x=22.
    Returned as a HIGH-RES master (not yet crisped) so it can be rotated for banking."""
    hi = Image.new("RGBA", (TD * S, TD * S), (0, 0, 0, 0))
    g = HiDraw(hi)
    if hen:
        body, bodym, bodyd = HBODY, HBODYM, HBODYD
        wing, wingd = HWING, HWINGD
    else:
        body, bodym, bodyd = BODY, BODYL, BODYD
        wing, wingd = WING, WINGD
    # tail (behind body), pointed
    g.polygon([(17, 33), (27, 33), (22, 39)], TAILD if not hen else bodyd)
    if not hen:
        g.rectangle([20, 33, 24, 35], WHITE)        # white vent
    # body teardrop
    g.ellipse([11, 17, 33, 36], body)
    g.ellipse([13, 20, 31, 33], bodym)
    g.ellipse([15, 25, 29, 35], bodyd)              # belly shade
    # folded wings down the flanks
    g.ellipse([10, 20, 19, 35], wing)
    g.ellipse([25, 20, 34, 35], wing)
    g.ellipse([11, 22, 17, 33], wingd)
    g.ellipse([27, 22, 33, 33], wingd)
    # dark primary tips near the tail
    g.polygon([(12, 34), (18, 30), (15, 37)], PRIM)
    g.polygon([(32, 34), (26, 30), (29, 37)], PRIM)
    # white-bordered blue speculum on each wing
    for sx in (12, 26):
        g.rectangle([sx, 26, sx + 5, 26], WHITE)
        g.rectangle([sx, 27, sx + 5, 29], SPEC)
        g.rectangle([sx, 30, sx + 5, 30], SPECD)
        g.rectangle([sx, 31, sx + 5, 31], WHITE)
    # mottle flecks
    for fx, fy in [(16, 24), (22, 23), (28, 24), (19, 31), (25, 31)]:
        g.px((fx, fy), bodyd)
    # chest
    if not hen:
        g.ellipse([15, 16 + bob, 29, 26 + bob], CHESTL)
        g.ellipse([17, 18 + bob, 27, 25 + bob], CHEST)
        g.ellipse([19, 21 + bob, 25, 26 + bob], CHESTD)
        g.rectangle([16, 19 + bob, 28, 20 + bob], WHITE)     # collar
    # head
    if hen:
        g.ellipse([16, 7 + bob, 28, 20 + bob], HBUFF)
        g.ellipse([18, 7 + bob, 26, 12 + bob], HCROWN)       # crown cap
        g.line([(16, 14 + bob), (28, 14 + bob)], HCROWN)     # eye-line
        g.px((19, 12 + bob), EYE)
        g.px((25, 12 + bob), EYE)
    else:
        g.ellipse([16, 7 + bob, 28, 20 + bob], HEADG)
        g.ellipse([17, 9 + bob, 23, 15 + bob], HEADH)        # sheen
        g.ellipse([23, 13 + bob, 28, 19 + bob], HEADD)       # nape
        g.ellipse([18, 8 + bob, 22, 11 + bob], GLINT)        # bright glint
        g.px((19, 13 + bob), EYE)
        g.px((25, 13 + bob), EYE)
    # bill, pointing up
    bill = HBILL if hen else BEAK
    billd = HBILLD if hen else BEAKD
    g.polygon([(19, 3 + bob), (25, 3 + bob), (27, 9 + bob), (17, 9 + bob)], bill)
    g.rectangle([17, 8 + bob, 27, 9 + bob], billd)
    g.px((22, 5 + bob), billd)
    return hi


def duck_topdown(hen=False, bob=0):
    return add_outline(crisp(_duck_master(hen, bob), TD, TD))


def duck_bank(angle, hen=False):
    """Banked top-down frame: rotate the high-res master, then crisp."""
    hi = _duck_master(hen).rotate(angle, resample=Image.BICUBIC, expand=False)
    return add_outline(crisp(hi, TD, TD))


def duck_side(facing, hen=False):
    """Side profile facing LEFT (facing=-1); mirrored for right."""
    def build(g):
        flank = HBODY if hen else (202, 196, 184, 255)
        flankd = HBODYD if hen else (164, 158, 146, 255)
        g.ellipse([9, 11, 34, 25], flank)
        g.ellipse([12, 18, 33, 26], flankd)
        if not hen:
            g.ellipse([6, 11, 19, 24], CHESTL)
            g.ellipse([7, 16, 17, 24], CHEST)
            rump = TAILD
            g.polygon([(30, 11), (41, 9), (41, 17), (31, 21)], rump)
            g.rectangle([37, 12, 41, 14], WHITE)
            g.ellipse([32, 5, 37, 9], rump)               # drake tail curl
            g.line([(31, 10), (34, 7)], rump, width=2)
        else:
            g.polygon([(30, 12), (40, 11), (40, 18), (31, 21)], flankd)
            for fx, fy in [(16, 16), (22, 20), (27, 16)]:
                g.px((fx, fy), HCROWN)
        # folded wing + speculum
        g.ellipse([15, 11, 31, 20], flankd if hen else WING)
        g.line([(16, 12), (30, 12)], WHITE)
        g.rectangle([20, 14, 27, 18], SPEC)
        g.line([(20, 18), (27, 18)], SPECD)
        g.line([(19, 19), (28, 19)], WHITE)
        if hen:
            g.polygon([(7, 12), (14, 12), (13, 17), (6, 17)], HBUFF)
            g.ellipse([2, 2, 15, 14], HBUFF)
            g.ellipse([4, 2, 12, 7], HCROWN)
            g.line([(3, 8), (13, 8)], HCROWN)
            g.px((8, 6), EYE)
            g.polygon([(0, 6), (6, 4), (6, 9)], HBILL)
            g.rectangle([0, 8, 6, 9], HBILLD)
        else:
            g.polygon([(7, 12), (14, 12), (13, 17), (6, 17)], HEADG)
            g.rectangle([11, 12, 14, 17], WHITE)
            g.ellipse([2, 2, 15, 14], HEADG)
            g.ellipse([4, 3, 10, 8], HEADH)
            g.ellipse([10, 7, 15, 13], HEADD)
            g.px((8, 6), EYE)
            g.px((9, 6), EYE)
            g.polygon([(0, 6), (6, 4), (6, 9)], BEAK)
            g.rectangle([0, 8, 6, 9], BEAKD)
    img = render(42, 30, build)
    if facing > 0:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img


def duck_hop(flap, hen=False):
    def build(g):
        wing = HBODYD if hen else WING
        wingd = HCROWN if hen else WINGD
        if flap == 0:
            wy = [(1, 17, 16, 31), (24, 17, 39, 31), (3, 20, 13, 29), (27, 20, 37, 29)]
            sp = [(4, 24, 8, 27), (32, 24, 36, 27)]
        else:
            wy = [(2, 7, 16, 22), (24, 7, 38, 22), (4, 10, 13, 20), (27, 10, 36, 20)]
            sp = [(5, 12, 9, 15), (31, 12, 35, 15)]
        g.ellipse(list(wy[0]), wing)
        g.ellipse(list(wy[1]), wing)
        g.ellipse(list(wy[2]), wingd)
        g.ellipse(list(wy[3]), wingd)
        for s in sp:
            g.rectangle(list(s), SPEC)
        g.ellipse([13, 14, 27, 33], HBODY if hen else BODY)
        g.ellipse([15, 22, 25, 32], HBODYD if hen else BODYD)
        if not hen:
            g.ellipse([14, 13, 26, 23], CHEST)
            g.ellipse([16, 15, 24, 22], CHESTD)
        g.polygon([(17, 32), (23, 32), (20, 37)], TAILD)
        if hen:
            g.ellipse([14, 5, 26, 16], HBUFF)
            g.ellipse([16, 5, 24, 9], HCROWN)
            g.px((17, 9), EYE)
            g.px((23, 9), EYE)
            g.polygon([(19, 1), (21, 1), (23, 5), (17, 5)], HBILL)
        else:
            g.rectangle([15, 14, 25, 15], WHITE)
            g.ellipse([14, 5, 26, 16], HEADG)
            g.ellipse([16, 6, 21, 11], HEADH)
            g.px((17, 9), EYE)
            g.px((23, 9), EYE)
            g.polygon([(19, 1), (21, 1), (23, 5), (17, 5)], BEAK)
            g.rectangle([17, 5, 23, 5], BEAKD)
    return render(40, 40, build)


def duck_face(hen=False):
    def build(g):
        if hen:
            g.ellipse([4, 4, 27, 28], HBUFF)
            g.ellipse([6, 4, 25, 11], HCROWN)
            cheek, bill, billd = HCHEEK, HBILL, HBILLD
        else:
            g.ellipse([4, 4, 27, 28], HEADG)
            g.ellipse([7, 6, 18, 16], HEADH)
            g.ellipse([16, 8, 26, 22], HEADD)
            cheek, bill, billd = (232, 150, 120, 255), BEAK, BEAKD
        g.ellipse([4, 17, 10, 22], cheek)
        g.ellipse([21, 17, 27, 22], cheek)
        g.ellipse([8, 8, 14, 17], (245, 245, 240, 255))
        g.ellipse([17, 8, 23, 17], (245, 245, 240, 255))
        g.ellipse([10, 10, 13, 15], EYE)
        g.ellipse([18, 10, 21, 15], EYE)
        g.px((11, 11), (255, 255, 255, 255))
        g.px((19, 11), (255, 255, 255, 255))
        g.polygon([(12, 19), (19, 19), (21, 24), (10, 24)], bill)
        g.polygon([(12, 24), (19, 24), (17, 27), (14, 27)], billd)
    return render(32, 32, build)


def make_duck_slices(sprite, nz=14):
    """Extrude a top-down sprite into a dome -> stacked cross-sections (1:1 voxel)."""
    w, h = sprite.size
    px = sprite.load()
    slices = [Image.new("RGBA", (w, h), (0, 0, 0, 0)) for _ in range(nz)]
    cx, cy = w / 2.0, h * 0.6
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            dome = 1.0 - (((x - cx) / (w * 0.52)) ** 2 + ((y - cy) / (h * 0.58)) ** 2)
            top = int(2 + max(0.0, dome) * (nz - 5))
            if y < h * 0.45:
                top = min(nz - 1, top + 3)
            for z in range(top + 1):
                slices[z].putpixel((x, y), (r, g, b, a))
    return slices


# ---- shared (non-duck) assets ------------------------------------------------
def make_shadow():
    img = Image.new("RGBA", (32, 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([1, 1, 30, 12], fill=(0, 0, 0, 90))
    d.ellipse([4, 3, 27, 10], fill=(0, 0, 0, 70))
    return img


def make_log():
    img = Image.new("RGBA", (48, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([1, 3, 46, 20], radius=6, fill=(116, 78, 48, 255))
    d.rectangle([1, 4, 46, 8], fill=(140, 98, 62, 255))
    d.rectangle([1, 16, 46, 19], fill=(92, 60, 36, 255))
    for x in range(6, 44, 9):
        d.rectangle([x, 11, x + 4, 12], fill=(96, 64, 40, 255))
    d.ellipse([2, 5, 9, 18], fill=(132, 92, 58, 255))
    d.ellipse([4, 8, 7, 15], fill=(104, 70, 44, 255))
    return add_outline(img)


def make_feather():
    img = Image.new("RGBA", (14, 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([2, 1, 11, 17], fill=(248, 226, 120, 255))
    d.ellipse([3, 5, 10, 16], fill=(255, 244, 180, 255))
    d.line([7, 2, 6, 19], fill=(190, 150, 60, 255), width=1)
    return add_outline(img)


def make_bug():
    img = Image.new("RGBA", (16, 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([1, 4, 7, 8], fill=(206, 232, 236, 200))
    d.ellipse([9, 4, 15, 8], fill=(206, 232, 236, 200))
    d.ellipse([3, 7, 7, 10], fill=(206, 232, 236, 200))
    d.ellipse([9, 7, 13, 10], fill=(206, 232, 236, 200))
    d.ellipse([6, 2, 10, 12], fill=(70, 172, 160, 255))
    d.ellipse([6, 1, 10, 4], fill=(40, 120, 112, 255))
    img.putpixel((7, 2), EYE)
    img.putpixel((9, 2), EYE)
    return add_outline(img)


def make_bread():
    img = Image.new("RGBA", (16, 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    crust = (198, 142, 74, 255)
    crust_d = (150, 100, 48, 255)
    crumb = (236, 204, 142, 255)
    d.ellipse([1, 1, 14, 11], fill=crust)
    d.rectangle([1, 6, 14, 11], fill=crust)
    d.ellipse([1, 7, 14, 13], fill=crust)
    d.ellipse([3, 8, 12, 12], fill=crumb)
    for sx in (5, 8, 11):
        d.line([sx, 3, sx - 2, 6], fill=crust_d, width=1)
    return add_outline(img)


def make_berry():
    img = Image.new("RGBA", (12, 13), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([1, 4, 9, 12], fill=(206, 52, 72, 255))
    d.ellipse([3, 6, 6, 9], fill=(236, 120, 130, 255))
    d.polygon([(6, 0), (10, 3), (5, 4)], fill=(86, 156, 74, 255))
    return add_outline(img)


def make_frog():
    img = Image.new("RGBA", (14, 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([2, 4, 11, 11], fill=(96, 162, 74, 255))
    d.ellipse([3, 8, 10, 11], fill=(66, 120, 52, 255))
    d.ellipse([2, 1, 5, 5], fill=(96, 162, 74, 255))
    d.ellipse([8, 1, 11, 5], fill=(96, 162, 74, 255))
    img.putpixel((3, 3), EYE)
    img.putpixel((9, 3), EYE)
    return add_outline(img)


def make_heron(frame=0):
    HERON = (124, 138, 156, 255)
    HEROND = (92, 104, 122, 255)
    HCREST = (58, 66, 82, 255)
    HRBEAK = (232, 180, 56, 255)
    img = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    wy0, wy1 = (6, 19) if frame == 0 else (1, 15)
    d.ellipse([0, wy0, 19, wy1], fill=HERON)
    d.ellipse([21, wy0, 40, wy1], fill=HERON)
    d.ellipse([2, wy0 + 3, 15, wy1 - 2], fill=HEROND)
    d.ellipse([25, wy0 + 3, 38, wy1 - 2], fill=HEROND)
    d.polygon([(0, wy0 + 7), (9, wy0 + 4), (3, wy1)], fill=HCREST)
    d.polygon([(40, wy0 + 7), (31, wy0 + 4), (37, wy1)], fill=HCREST)
    d.ellipse([16, 6, 24, 30], fill=HERON)
    d.ellipse([18, 16, 23, 30], fill=HEROND)
    d.ellipse([16, 27, 24, 36], fill=(150, 160, 176, 255))
    d.line([21, 28, 24, 24], fill=HCREST, width=2)
    d.polygon([(20, 39), (17, 34), (23, 34)], fill=HRBEAK)
    img.putpixel((18, 31), (190, 44, 44, 255))
    img.putpixel((22, 31), (190, 44, 44, 255))
    return add_outline(img)


def make_water():
    img = Image.new("RGBA", (64, 64), (46, 102, 130, 255))
    px = img.load()
    crest = (70, 132, 160, 255)
    crest_hi = (96, 158, 184, 255)
    trough = (36, 86, 112, 255)
    for y in range(64):
        for x in range(64):
            s = (x + y)
            if s % 16 == 0 and (x * 3 + y) % 32 < 7:
                px[x, y] = crest
            elif s % 16 == 1 and (x * 3 + y) % 32 < 5:
                px[x, y] = crest_hi
            elif (x - y) % 16 == 0 and (x + y * 2) % 32 < 4:
                px[x, y] = trough
    return img


def save(img, name):
    img.save(os.path.join(ART, name))


# ---- output ------------------------------------------------------------------
# Ducks now come from the VOXEL model (single source of truth for 2D views + the
# 3D mega-hop slices); see tools/voxel_duck.py.  The make_duck_* helpers above are
# retained only as the prior 2D-only fallback and are no longer wired up.
from voxel_duck import generate_ducks
generate_ducks(ART)

save(make_shadow(), "shadow.png")
save(make_log(), "log.png")
save(make_feather(), "feather.png")
save(make_bug(), "bug.png")
save(make_bread(), "bread.png")
save(make_berry(), "berry.png")
save(make_frog(), "frog.png")
save(make_heron(0), "heron_0.png")
save(make_heron(1), "heron_1.png")
save(make_water(), "water.png")
print("done.")
