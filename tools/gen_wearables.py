#!/usr/bin/env python3
"""Generate DUCKODUCKO duck-head COSMETIC sprites into ../art/.

Ten little wearables (crown, pirate hat, party hat, etc.) drawn to match the
game's chunky pixel/voxel look.  Reuses the supersampled-author -> LANCZOS
downscale -> palette-snap (crisp) -> 1px dark outline pipeline from
gen_sprites.py so the silhouettes are clean and nearest-neighbour friendly.

Each sprite is designed so its natural REST POINT is BOTTOM-CENTER of the
canvas, so it can be anchored straight onto a duck's head.

Run:  python3 tools/gen_wearables.py   (from the project root)
Then: Godot --headless --path . --import
"""
import os
from PIL import Image, ImageDraw

ART = os.path.join(os.path.dirname(__file__), "..", "art")
os.makedirs(ART, exist_ok=True)
S = 4  # supersample factor (matches gen_sprites.py)

# ---- palette (saturated-but-slightly-muted, matches game feel) ---------------
OUT = (30, 24, 20, 255)
WHITE = (240, 238, 230, 255)
WHITED = (208, 206, 196, 255)
EYE = (16, 16, 16, 255)
# golds
GOLD = (244, 198, 70, 255)
GOLDH = (252, 226, 130, 255)
GOLDD = (196, 150, 40, 255)
# reds
RED = (206, 60, 64, 255)
REDD = (164, 42, 48, 255)
REDH = (232, 96, 98, 255)
# blues / cyans / teals
BLUE = (66, 110, 174, 255)
BLUED = (44, 78, 130, 255)
CYAN = (90, 198, 214, 255)
CYAND = (54, 150, 168, 255)
TEAL = (70, 172, 160, 255)
TEALD = (44, 120, 112, 255)
# pinks / yellows
PINK = (236, 118, 168, 255)
PINKD = (198, 84, 130, 255)
YEL = (250, 222, 96, 255)
YELD = (214, 178, 56, 255)
# browns / leather
LEATH = (150, 100, 56, 255)
LEATHL = (186, 134, 84, 255)
LEATHD = (108, 70, 40, 255)
# greys / dark
GREY = (150, 154, 162, 255)
GREYD = (104, 108, 118, 255)
BLK = (44, 42, 50, 255)
BLKD = (28, 26, 34, 255)
# warm orange-red (scarf)
ORG = (224, 96, 56, 255)
ORGL = (242, 132, 84, 255)
ORGD = (180, 68, 40, 255)
# halo glow
GLOWA = (255, 232, 150, 90)
GLOWB = (255, 244, 200, 150)
# heron slate + turtle olive/tan
SLATE = (120, 128, 140, 255)
SLATEL = (156, 164, 176, 255)
SLATED = (84, 92, 104, 255)
OLIVE = (110, 134, 72, 255)
OLIVEL = (146, 172, 100, 255)
OLIVED = (70, 90, 44, 255)
SEAM = (48, 60, 30, 255)
TAN = (196, 172, 112, 255)
TAND = (152, 128, 78, 255)


# ---- supersampled drawing (verbatim helper set from gen_sprites.py) ----------
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

    def arc(self, box, start, end, fill, width=1):
        self.d.arc(self._b(box), start, end, fill=fill, width=max(1, width * S))

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
    """Downscale a high-res master and snap every opaque pixel to the authored palette."""
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


def render(w, h, build, outline=True):
    """Author build(g) in final w x h coords; get back a crisp supersampled sprite."""
    hi = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    build(HiDraw(hi))
    img = crisp(hi, w, h)
    return add_outline(img) if outline else img


def save(img, name):
    img.save(os.path.join(ART, name))


# ---- the wearables -----------------------------------------------------------
def make_crown():
    """Tiny gold crown, 3 points, small red gem.  28x22."""
    def build(g):
        # crown band sits along the bottom (rest point bottom-center)
        g.rectangle([5, 15, 22, 20], GOLD)
        g.rectangle([5, 15, 22, 16], GOLDH)        # top sheen of band
        g.rectangle([5, 19, 22, 20], GOLDD)        # base shade
        # three spikes rising from the band
        g.polygon([(5, 15), (8, 5), (11, 15)], GOLD)
        g.polygon([(11, 15), (14, 2), (17, 15)], GOLD)
        g.polygon([(17, 15), (20, 5), (23, 15)], GOLD)
        # spike highlights
        g.polygon([(6, 15), (8, 7), (8, 15)], GOLDH)
        g.polygon([(12, 15), (14, 4), (14, 15)], GOLDH)
        g.polygon([(18, 15), (20, 7), (20, 15)], GOLDH)
        # ball-tips
        for tx, ty in [(8, 5), (14, 2), (20, 5)]:
            g.ellipse([tx - 1, ty - 1, tx + 1, ty + 1], GOLDH)
        # centre red gem on the band
        g.ellipse([12, 16, 16, 19], RED)
        g.px((13, 16), REDH)
    return render(28, 22, build)


def make_pirate():
    """Black bicorne pirate hat with white skull patch.  34x24."""
    def build(g):
        # wide swept brim across the bottom, upturned bicorne points
        g.polygon([(2, 20), (10, 9), (24, 9), (32, 20), (28, 22), (6, 22)], BLK)
        # crown bump in the middle
        g.ellipse([11, 6, 23, 18], BLK)
        # upturned tips highlighted
        g.polygon([(2, 20), (8, 11), (9, 13), (6, 21)], BLKD)
        g.polygon([(32, 20), (26, 11), (25, 13), (28, 21)], BLKD)
        # gold trim along the lower brim
        g.line([(6, 21), (28, 21)], GOLD)
        g.line([(10, 10), (4, 19)], GOLD)
        g.line([(24, 10), (30, 19)], GOLD)
        # white skull patch centred
        g.ellipse([14, 10, 20, 16], WHITE)
        g.px((15, 12), BLK)        # eye
        g.px((18, 12), BLK)        # eye
        g.rectangle([15, 14, 19, 15], WHITE)
        g.px((16, 15), BLK)        # tooth gaps
        g.px((18, 15), BLK)
        # crossbones hint
        g.line([(13, 16), (21, 17)], WHITED)
    return render(34, 24, build)


def make_party():
    """Tall cone party hat, diagonal pink/cyan/yellow stripes, pom-pom on top.  22x30."""
    def build(g):
        apex = (11, 1)
        base_l, base_r, base_y = 4, 18, 26
        g.polygon([apex, (base_l, base_y), (base_r, base_y)], YEL)
        # diagonal stripes painted as slanted bands clipped by the cone via px scan
        cols = [PINK, CYAN, YEL]
        for y in range(1, base_y + 1):
            # cone half-width at this y
            t = (y - 1) / float(base_y - 1)
            hw = (base_r - base_l) / 2.0 * t
            cx = apex[0]
            xl, xr = int(round(cx - hw)), int(round(cx + hw))
            for x in range(xl, xr + 1):
                band = ((x + y) // 3) % 3      # diagonal stripe index
                g.px((x, y), cols[band])
        # shade the right side a touch for volume
        for y in range(2, base_y):
            t = (y - 1) / float(base_y - 1)
            hw = (base_r - base_l) / 2.0 * t
            xr = int(round(apex[0] + hw))
            g.px((xr, y), CYAND)
        # pom-pom on top
        g.ellipse([8, 0, 14, 6], WHITE)
        g.ellipse([9, 1, 12, 4], WHITED)
    return render(22, 30, build)


def make_prop():
    """Beanie (red/blue panels, yellow button) with a 2-blade propeller on top.  30x24."""
    def build(g):
        # beanie dome along the bottom
        g.ellipse([7, 10, 23, 26], RED)
        g.rectangle([7, 18, 23, 22], RED)
        # blue alternating panels
        g.polygon([(15, 11), (11, 22), (15, 22)], BLUE)
        g.polygon([(15, 11), (19, 22), (15, 22)], RED)
        g.polygon([(8, 16), (11, 22), (8, 22)], BLUE)
        g.polygon([(22, 16), (19, 22), (22, 22)], BLUE)
        # ribbed band at the brim
        g.rectangle([7, 21, 23, 23], BLUED)
        g.line([(7, 22), (23, 22)], REDD)
        # little stalk + yellow button on top
        g.rectangle([14, 7, 16, 11], GREYD)
        g.ellipse([13, 6, 17, 10], YEL)
        g.px((14, 7), GOLDH)
        # 2-blade propeller crossing the top
        g.polygon([(2, 6), (14, 8), (2, 9)], CYAN)
        g.polygon([(28, 6), (16, 8), (28, 9)], CYAND)
        g.line([(2, 7), (14, 8)], CYAND)
        g.ellipse([13, 6, 17, 9], GREY)     # hub over blades
    return render(30, 24, build)


def make_chef():
    """Classic white pleated chef toque, puffy top.  26x30."""
    def build(g):
        # band at the bottom
        g.rectangle([6, 21, 20, 27], WHITE)
        g.rectangle([6, 21, 20, 22], WHITED)
        g.line([(6, 26), (20, 26)], WHITED)
        # the puffy crown: clustered ellipses
        g.ellipse([4, 6, 14, 20], WHITE)
        g.ellipse([12, 6, 22, 20], WHITE)
        g.ellipse([8, 2, 18, 16], WHITE)
        g.ellipse([3, 10, 11, 22], WHITE)
        g.ellipse([15, 10, 23, 22], WHITE)
        # pleat shading (vertical creases) on the band
        for px_ in (9, 13, 17):
            g.line([(px_, 22), (px_, 26)], WHITED)
        # soft volume shading on the puff
        g.ellipse([14, 8, 21, 18], WHITED)
        g.ellipse([7, 12, 11, 19], WHITED)
    return render(26, 30, build)


def make_bandana():
    """Red polka-dot kerchief tied around head, knotted tails.  30x18 (low profile)."""
    def build(g):
        # main triangular cloth across the head, point down-ish at sides
        g.polygon([(4, 4), (26, 4), (24, 13), (6, 13)], RED)
        g.rectangle([4, 4, 26, 8], RED)
        # top fold highlight
        g.rectangle([4, 4, 26, 5], REDH)
        # lower shade
        g.line([(6, 12), (24, 12)], REDD)
        # knot on the right + two trailing tails
        g.ellipse([23, 8, 28, 13], RED)
        g.polygon([(26, 11), (30, 14), (27, 15), (25, 13)], REDD)
        g.polygon([(26, 12), (29, 16), (26, 16)], RED)
        # polka dots
        for dx, dy in [(8, 7), (13, 9), (18, 7), (11, 11), (20, 11), (16, 6)]:
            g.px((dx, dy), WHITE)
            g.px((dx + 1, dy), WHITE)
    return render(30, 18, build)


def make_halo():
    """Glowing gold ring floating above head, faint warm bloom.  30x16.

    Drawn at FINAL resolution (not via the supersample->crisp path) so the
    semi-transparent warm bloom survives — crisp() snaps to opaque-only palette
    and would discard the glow.  The solid ring is built crisply, outlined,
    then composited over the soft bloom.
    """
    w, h = 30, 16
    # 1) the crisp gold ring, supersampled + outlined like the other wearables
    def ring(g):
        g.ellipse([5, 4, 25, 12], GOLD)
        g.ellipse([8, 6, 22, 10], (0, 0, 0, 0))     # punch the hole
        g.line([(9, 5), (16, 4)], GOLDH)
        g.line([(7, 7), (8, 9)], GOLDD)
        g.line([(22, 7), (23, 9)], GOLDD)
    ring_img = render(w, h, ring)        # crisp + outlined
    # 2) soft warm bloom drawn straight at final res
    bloom = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bloom)
    bd.ellipse([2, 1, 27, 15], fill=GLOWA)
    bd.ellipse([6, 3, 24, 13], fill=GLOWB)
    # 3) bloom underneath, crisp outlined ring on top
    bloom.alpha_composite(ring_img)
    return bloom


def make_boombox():
    """Little 80s boombox, two speaker circles, antenna.  30x22."""
    def build(g):
        # antenna sticking up-left
        g.line([(8, 9), (4, 1)], GREY, width=1)
        g.px((4, 1), GREY)
        # body
        g.rounded_rectangle([3, 8, 27, 20], 2, GREYD)
        g.rectangle([3, 8, 27, 10], GREY)            # top lighter strip
        # handle
        g.arc([8, 4, 22, 12], 180, 360, GREY, width=1)
        # two speaker circles
        for cx in (9, 21):
            g.ellipse([cx - 4, 11, cx + 4, 19], BLK)
            g.ellipse([cx - 3, 12, cx + 3, 18], GREYD)
            g.ellipse([cx - 1, 14, cx + 1, 16], GREY)
        # centre cassette/eq panel
        g.rectangle([12, 12, 18, 18], BLKD)
        g.line([(13, 14), (17, 14)], CYAN)            # eq lights
        g.line([(13, 16), (17, 16)], RED)
        g.px((13, 13), YEL)
    return render(30, 22, build)


def make_scarf():
    """Knitted cozy scarf wrapped at neck, trailing fringed tail.  32x24 (sits lower)."""
    def build(g):
        # wrap band across the neck (full width, lower in canvas)
        g.rounded_rectangle([3, 8, 29, 17], 2, ORG)
        g.rectangle([3, 8, 29, 10], ORGL)             # top sheen
        g.line([(3, 16), (29, 16)], ORGD)             # lower shade
        # knit ribs (vertical dashes)
        for x in range(5, 29, 3):
            g.line([(x, 9), (x, 16)], ORGD)
            g.line([(x + 1, 9), (x + 1, 16)], ORGL)
        # the trailing tail dropping down-right
        g.rounded_rectangle([18, 14, 25, 23], 2, ORG)
        g.line([(18, 14), (18, 23)], ORGD)
        g.line([(24, 14), (24, 23)], ORGL)
        for x in range(19, 25, 2):
            g.line([(x, 15), (x, 22)], ORGD)
        # fringe at the bottom of the tail
        for fx in (19, 21, 23):
            g.line([(fx, 22), (fx, 24)], ORGL)
    return render(32, 24, build)


def make_goggles():
    """Brown leather aviator goggles, two round cyan/teal tinted lenses.  28x16."""
    def build(g):
        # leather strap band across the whole width
        g.rectangle([0, 6, 27, 10], LEATH)
        g.rectangle([0, 6, 27, 7], LEATHL)
        g.line([(0, 9), (27, 9)], LEATHD)
        # two round lens housings (leather rims)
        for cx in (7, 20):
            g.ellipse([cx - 6, 3, cx + 6, 13], LEATH)
            g.ellipse([cx - 5, 4, cx + 5, 12], LEATHD)
            # tinted glass lens
            g.ellipse([cx - 4, 5, cx + 4, 11], TEAL)
            g.ellipse([cx - 4, 5, cx + 1, 9], CYAN)      # reflective glint
            g.line([(cx - 3, 6), (cx + 2, 6)], (215, 245, 248, 255))
        # nose bridge connecting the two lenses
        g.rectangle([12, 7, 16, 9], LEATHL)
    return render(28, 16, build)


def make_raccoon():
    """Raccoon bandit mask: grey ears, a black eye-band, white-rimmed beady eyes, a snout stripe.  28x20."""
    BLK = (40, 36, 44, 255); GRY = (150, 154, 162, 255); GRYD = (104, 108, 118, 255)
    WHT = (238, 238, 242, 255); DK = (20, 20, 26, 255)
    def build(g):
        for cx in (7, 20):                               # perky grey ears
            g.polygon([(cx - 4, 9), (cx + 4, 9), (cx, 1)], GRY)
            g.polygon([(cx - 2, 8), (cx + 2, 8), (cx, 4)], GRYD)
        g.rectangle([3, 8, 24, 15], BLK)                 # the black bandit eye-band
        g.ellipse([0, 8, 7, 15], BLK)
        g.ellipse([20, 8, 27, 15], BLK)
        for cx in (8, 19):                               # white-rimmed beady eyes
            g.ellipse([cx - 3, 9, cx + 3, 14], WHT)
            g.ellipse([cx - 2, 10, cx + 1, 13], DK)
        g.rectangle([12, 15, 15, 19], BLK)               # a short snout stripe
    return render(28, 20, build)


def make_heron():
    """Great-blue-heron crest: a sleek slate head in PROFILE with a long POINTED yellow
    dagger beak and black plumes streaming off the crown.  30x20."""
    def build(g):
        # the slate head, set right-of-centre so the beak has room to spear left
        g.ellipse([13, 4, 27, 17], SLATE)
        g.ellipse([14, 4, 26, 10], SLATEL)            # crown sheen
        g.line([(14, 15), (26, 15)], SLATED)
        # a long, sharp POINTED beak — a clean triangle tapering to a single point at the left
        g.polygon([(14, 8), (1, 11), (14, 12)], YEL)        # upper mandible -> the point
        g.polygon([(14, 11), (4, 12), (14, 13)], YELD)      # lower mandible, shaded
        g.line([(3, 11), (13, 11)], (150, 110, 24, 255))    # the bill seam
        # the signature black head-plumes trailing off the back of the crown
        g.line([(24, 5), (31, 2)], BLK)
        g.line([(24, 7), (31, 5)], BLK)
        g.line([(23, 6), (30, 4)], BLKD)
        # a small white cheek + a beady eye
        g.line([(15, 12), (21, 12)], WHITED)
        g.px((18, 9), EYE)
        g.px((17, 8), WHITE)
    return render(30, 20, build)


def make_turtle():
    """Domed turtle-shell helmet: a bright olive carapace with a clean central hexagonal
    scute, six outer plates, and a tan rim.  30x22."""
    def build(g):
        # the domed carapace
        g.ellipse([3, 3, 27, 19], OLIVE)
        g.ellipse([4, 3, 26, 10], OLIVEL)             # top highlight band
        # the central hexagonal scute, crisp and centred
        g.polygon([(15, 5), (20, 9), (20, 13), (15, 17), (10, 13), (10, 9)], OLIVED)
        g.polygon([(15, 6), (19, 9), (19, 13), (15, 15), (11, 13), (11, 9)], OLIVE)
        g.px((14, 9), OLIVEL)
        # six tidy seams fanning from the hex corners to the rim = a ring of outer plates
        for (x1, y1, x2, y2) in [(10, 9, 4, 7), (20, 9, 26, 7), (10, 13, 4, 15),
                                 (20, 13, 26, 15), (15, 5, 15, 3), (15, 17, 15, 18)]:
            g.line([(x1, y1), (x2, y2)], SEAM)
        # tan rim hugging the lower edge
        g.arc([3, 3, 27, 19], 12, 168, TAND, width=2)
        g.line([(6, 16), (24, 16)], TAN)
    return render(30, 22, build)


# ---- output ------------------------------------------------------------------
def make_cape():
    """A flowing HERO CAPE with a gold clasp."""
    def build(g):
        g.polygon([(12, 4), (20, 4), (28, 27), (4, 27)], RED)
        g.polygon([(12, 4), (16, 4), (13, 27), (4, 27)], REDH)
        g.polygon([(16, 4), (20, 4), (28, 27), (19, 27)], REDD)
        for x in range(6, 28, 4):
            g.line([(x, 26), (x + 2, 28)], REDD)
        g.rounded_rectangle([13, 2, 19, 7], 2, GOLD)
        g.rectangle([14, 3, 18, 4], GOLDH)
    return render(32, 28, build)


def make_vest():
    """A FORAGER VEST with pockets."""
    def build(g):
        g.polygon([(4, 5), (13, 5), (11, 24), (4, 24)], ORG)
        g.polygon([(24, 5), (15, 5), (17, 24), (24, 24)], ORG)
        g.line([(4, 5), (4, 24)], ORGD)
        g.line([(24, 5), (24, 24)], ORGD)
        g.rectangle([4, 5, 24, 7], ORGL)
        for px in (6, 17):
            g.rounded_rectangle([px, 16, px + 5, 22], 1, ORGD)
            g.line([(px, 16), (px + 5, 16)], LEATH)
    return render(28, 26, build)


def make_jetpack():
    """Twin thrusters with blue flame."""
    def build(g):
        for tx in (5, 16):
            g.rounded_rectangle([tx, 4, tx + 7, 22], 3, GREY)
            g.rectangle([tx + 1, 5, tx + 3, 21], GREYD)
            g.ellipse([tx, 2, tx + 7, 8], REDH)
            g.polygon([(tx + 1, 22), (tx + 6, 22), (tx + 3, 30)], BLUE)
            g.polygon([(tx + 2, 22), (tx + 5, 22), (tx + 3, 27)], CYAN)
    return render(28, 30, build)


def make_satchel():
    """A leather CHARGE PACK with a gold buckle."""
    def build(g):
        g.line([(7, 8), (7, 2)], LEATHD)
        g.line([(21, 8), (21, 2)], LEATHD)
        g.rounded_rectangle([5, 9, 23, 24], 2, LEATH)
        g.rectangle([5, 9, 23, 11], LEATHL)
        g.rounded_rectangle([5, 6, 23, 14], 2, LEATHD)
        g.rectangle([6, 7, 22, 9], LEATH)
        g.rounded_rectangle([12, 11, 16, 15], 1, GOLD)
        g.rectangle([13, 12, 15, 14], GOLDD)
    return render(28, 26, build)


ASSETS = [
    (make_crown, "wear_crown.png"),
    (make_pirate, "wear_pirate.png"),
    (make_party, "wear_party.png"),
    (make_prop, "wear_prop.png"),
    (make_chef, "wear_chef.png"),
    (make_bandana, "wear_bandana.png"),
    (make_halo, "wear_halo.png"),
    (make_boombox, "wear_boombox.png"),
    (make_scarf, "wear_scarf.png"),
    (make_goggles, "wear_goggles.png"),
    (make_heron, "wear_heron.png"),
    (make_turtle, "wear_turtle.png"),
    (make_cape, "wear_cape.png"),
    (make_vest, "wear_vest.png"),
    (make_jetpack, "wear_jetpack.png"),
    (make_satchel, "wear_satchel.png"),
    (make_raccoon, "wear_raccoon.png"),
]

if __name__ == "__main__":
    for fn, name in ASSETS:
        save(fn(), name)
        print(f"  wrote {name}")
    print(f"done. {len(ASSETS)} wearables -> {os.path.abspath(ART)}")
