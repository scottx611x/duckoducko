#!/usr/bin/env python3
"""Environment / scenery sprites for DUCKODUCKO -> ../art/.

Water scenery (env_*) drifts in the river as non-colliding set dressing; bank
props (bank_*) sit on the grassy banks (bottom-center anchored). Plus a proper
voxel HERON: a 16-frame standing turntable for the compendium and 2 swoop
frames for gameplay.

Style contract (matches tools/voxel_duck.py exactly):
  * voxel models -> shade() (exposed-face + top-light) -> painter's-algorithm
    render() at S=5 supersample -> LANCZOS -> snap to the model's own palette
    -> 1px (36,28,28) ink outline   (all imported from voxel_duck)
  * flat/simple props use the legacy 2D pipeline: author at 4x supersample ->
    LANCZOS -> palette snap -> same ink outline.

Deterministic: fixed seeds / hash speckles only.  Zero deps beyond Pillow.
Run:  python3 tools/gen_env.py     (from the repo root)
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voxel_duck import shade, render, _vox_helpers, build_heron  # noqa: E402

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "art")
os.makedirs(ART, exist_ok=True)

INK = (36, 28, 28, 255)          # the game's ink outline
FS = 4                           # flat-pipeline supersample (gen_sprites.py convention)
GENERATED = []


def save(img, name):
    img.save(os.path.join(ART, name))
    GENERATED.append(name)


# ---- flat 2D pipeline (legacy gen_sprites.py approach, non-square friendly) ----
def _crisp(hi, w, h, alpha_cut=150):
    """LANCZOS downscale + snap every pixel to the authored palette."""
    pal = list({hi.getpixel((x, y)) for y in range(hi.height) for x in range(hi.width)
                if hi.getpixel((x, y))[3] == 255})
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if not pal:
        return out
    small = hi.resize((w, h), Image.LANCZOS)
    sp, op = small.load(), out.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = sp[x, y]
            if a < alpha_cut:
                continue
            best, bd = pal[0], 1e18
            for c in pal:
                d = (c[0] - r) ** 2 + (c[1] - g) ** 2 + (c[2] - b) ** 2
                if d < bd:
                    bd, best = d, c
            op[x, y] = (best[0], best[1], best[2], 255)
    return out


def _outline(img):
    px = img.load()
    w, h = img.size
    out = img.copy()
    op = out.load()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] > 0:
                        op[x, y] = INK
                        break
    return out


def flat(w, h, build_fn, rot=0.0):
    """Author build_fn(d) in FSx coords on a (w*FS, h*FS) canvas -> crisp sprite."""
    hi = Image.new("RGBA", (w * FS, h * FS), (0, 0, 0, 0))
    build_fn(ImageDraw.Draw(hi))
    if rot:
        hi = hi.rotate(rot, resample=Image.BICUBIC, expand=True,
                       fillcolor=(0, 0, 0, 0))
        w, h = hi.width // FS, hi.height // FS
    im = _outline(_crisp(hi, w, h))
    bb = im.getbbox()
    return im.crop(bb) if bb else im


# ---- voxel pipeline helpers ------------------------------------------------------
def _center(V):
    xs = [p[0] for p in V]; ys = [p[1] for p in V]; zs = [p[2] for p in V]
    cx = (min(xs) + max(xs)) // 2
    cy = (min(ys) + max(ys)) // 2
    cz = (min(zs) + max(zs)) // 2
    return {(x - cx, y - cy, z - cz): c for (x, y, z), c in V.items()}


def vox(V, yaw, pitch, target):
    """Render a voxel model so its longest screen dimension ~= target px, crop tight.
    Auto-solves the scale, keeping voxel chunkiness proportional to model size."""
    SH = shade(_center(V))
    trial = render(SH, math.radians(yaw), math.radians(pitch), out=320, scale=1.2)
    bb = trial.getbbox()
    cur = max(bb[2] - bb[0], bb[3] - bb[1])
    sc = 1.2 * (target / float(cur))
    out = int(target * 1.7) + 14
    im = render(SH, math.radians(yaw), math.radians(pitch), out=out, scale=sc)
    return im.crop(im.getbbox())


def vox_frames(models, yaw, pitch, target, pad=2):
    """Render several poses of one model with a SHARED scale + crop box so the
    frames animate without jitter (spin_set convention from voxel_duck)."""
    SHs = [shade(_center(V)) for V in models]
    trial = render(SHs[0], math.radians(yaw), math.radians(pitch), out=340, scale=1.2)
    bb = trial.getbbox()
    cur = max(bb[2] - bb[0], bb[3] - bb[1])
    sc = 1.2 * (target / float(cur))
    out = int(target * 2.0) + 16
    imgs = [render(SH, math.radians(yaw), math.radians(pitch), out=out, scale=sc)
            for SH in SHs]
    box = None
    for im in imgs:
        b = im.getbbox()
        if b:
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]),
                                         max(box[2], b[2]), max(box[3], b[3]))
    box = (max(0, box[0] - pad), max(0, box[1] - pad),
           min(out, box[2] + pad), min(out, box[3] + pad))
    return [im.crop(box) for im in imgs]


# =================================================================================
# WATER SCENERY (drifts in the river)
# =================================================================================
# -- lily pads: flat top-down discs with a notch, veins + a wet rim ---------------
PAD_D = (52, 104, 56, 255); PAD = (78, 142, 74, 255); PAD_L = (110, 176, 96, 255)
PAD_V = (62, 120, 62, 255)


def _lilypad(d, cx, cy, r, notch_at, notch_w, rng):
    d.pieslice([(cx - r) * FS, (cy - r) * FS, (cx + r) * FS, (cy + r) * FS],
               notch_at + notch_w, notch_at + 360, fill=PAD)
    r2 = r - 1.6
    d.pieslice([(cx - r2) * FS, (cy - r2) * FS, (cx + r2) * FS, (cy + r2) * FS],
               notch_at + notch_w + 6, notch_at + 354, fill=PAD_L)
    # radial veins back to the notch point
    for a in range(notch_at + notch_w + 25, notch_at + 355, 46):
        ex = cx + (r - 1.6) * math.cos(math.radians(a))
        ey = cy + (r - 1.6) * math.sin(math.radians(a))
        d.line([(cx * FS, cy * FS), (ex * FS, ey * FS)], fill=PAD_V, width=FS)
    # a couple of nicks in the rim (real ponds chew their pads)
    for _ in range(2):
        a = math.radians(rng.uniform(notch_at + notch_w + 30, notch_at + 330))
        nx, ny = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([(nx - 1.4) * FS, (ny - 1.4) * FS, (nx + 1.4) * FS, (ny + 1.4) * FS],
                  fill=(0, 0, 0, 0))
    d.ellipse([(cx - r) * FS, (cy - r) * FS, (cx + r) * FS, (cy + r) * FS],
              outline=PAD_D, width=FS)


def gen_lilies():
    rng = random.Random(101)
    save(flat(32, 32, lambda d: _lilypad(d, 16, 16, 14.5, 205, 52, rng)), "env_lily_0.png")
    rng2 = random.Random(202)
    save(flat(28, 28, lambda d: _lilypad(d, 14, 14, 12.5, 20, 55, rng2)), "env_lily_1.png")

    def blossom(d):
        rng3 = random.Random(303)
        _lilypad(d, 15, 15, 13.5, 150, 44, rng3)
        PET_D = (198, 92, 128, 255); PET = (234, 138, 168, 255); PET_L = (248, 186, 204, 255)
        cx, cy = 15.5, 14.5
        for rr, col, n, off in ((6.2, PET_D, 8, 0), (4.6, PET, 8, 22), (3.0, PET_L, 6, 10)):
            for i in range(n):
                a = math.radians(off + i * 360.0 / n)
                px_, py_ = cx + rr * 0.62 * math.cos(a), cy + rr * 0.62 * math.sin(a)
                d.ellipse([(px_ - rr * 0.42) * FS, (py_ - rr * 0.42) * FS,
                           (px_ + rr * 0.42) * FS, (py_ + rr * 0.42) * FS], fill=col)
        d.ellipse([(cx - 1.5) * FS, (cy - 1.5) * FS, (cx + 1.5) * FS, (cy + 1.5) * FS],
                  fill=(246, 208, 92, 255))
    save(flat(31, 31, blossom), "env_lilyflower.png")


# -- duckweed: loose speckly mats, irregular edges --------------------------------
def gen_duckweed():
    DW_D = (84, 138, 52, 255); DW = (112, 170, 66, 255); DW_L = (140, 196, 86, 255)
    for idx, (seed, w, h, n) in enumerate(((11, 28, 24, 46), (12, 22, 20, 34))):
        rng = random.Random(seed)

        def speck(d, rng=rng, w=w, h=h, n=n):
            cx, cy = w / 2.0, h / 2.0
            # lumpy cluster: blobs biased to a noisy radius so the edge is ragged
            for i in range(n):
                a = rng.uniform(0, 2 * math.pi)
                rad = (0.15 + 0.85 * rng.random() ** 0.6) * (w / 2.0 - 2.5)
                rad *= 0.75 + 0.45 * math.sin(a * 3 + rng.random() * 2)
                x = cx + rad * math.cos(a)
                y = cy + rad * math.sin(a) * (h / float(w))
                r = rng.uniform(1.1, 2.4)
                col = (DW_D, DW, DW, DW_L)[rng.randrange(4)]
                d.ellipse([(x - r) * FS, (y - r) * FS, (x + r) * FS, (y + r) * FS], fill=col)
            for _ in range(6):     # stray outlying specks
                a = rng.uniform(0, 2 * math.pi)
                x = cx + (w / 2.0 - 1.5) * rng.uniform(0.85, 1.0) * math.cos(a)
                y = cy + (h / 2.0 - 1.5) * rng.uniform(0.85, 1.0) * math.sin(a)
                d.ellipse([(x - 1) * FS, (y - 1) * FS, (x + 1) * FS, (y + 1) * FS],
                          fill=DW if _ % 2 else DW_L)
            for _ in range(3):     # punch holes so the mat reads loose + speckly
                a = rng.uniform(0, 2 * math.pi)
                rr = rng.uniform(0.25, 0.6) * (w / 2.0)
                x, y = cx + rr * math.cos(a), cy + rr * math.sin(a) * (h / float(w))
                hr = rng.uniform(1.6, 2.6)
                d.ellipse([(x - hr) * FS, (y - hr) * FS, (x + hr) * FS, (y + hr) * FS],
                          fill=(0, 0, 0, 0))
        save(flat(w, h, speck), "env_duckweed_%d.png" % idx)


# -- half-submerged granite stones -------------------------------------------------
def build_stone(seed, wide=False):
    GRAN = (152, 150, 144); GRAND = (122, 120, 116); GRANL = (180, 178, 170)
    WET = (92, 96, 104); MOSS = (108, 132, 82)
    V = {}
    put, ellip, box = _vox_helpers(V)
    rng = random.Random(seed)
    rx, ry, rz = (9.0, 5.0, 6.5) if wide else (6.5, 6.5, 5.5)
    ellip(0, 0, 0, rx, ry, rz, GRAN)
    if wide:
        ellip(rx * 0.7, 1.0, -rz * 0.5, 3.4, 3.0, 3.0, GRAN)   # a shoulder lump
    for (x, y, z) in list(V):
        if y < 0:
            del V[(x, y, z)]                       # waterline cut: only the dome shows
            continue
        h = (x * 73 + y * 31 + z * 151 + seed) % 11
        if h == 0:
            V[(x, y, z)] = GRAND
        elif h == 1:
            V[(x, y, z)] = GRANL
        if y == 0:
            V[(x, y, z)] = WET                     # dark wet band at the waterline
        elif y == 1 and (x * 31 + z * 17) % 3 == 0:
            V[(x, y, z)] = WET
    # a little moss/lichen on the shaded shoulder
    for _ in range(4 if wide else 3):
        mx = rng.randint(-int(rx * 0.6), int(rx * 0.6))
        mz = rng.randint(-int(rz * 0.6), int(rz * 0.6))
        top = max((y for (x, y, z) in V if x == mx and z == mz), default=None)
        if top is not None and top > 1:
            V[(mx, top, mz)] = MOSS
    return V


# -- gnarled driftwood snag ---------------------------------------------------------
def build_snag():
    WOOD = (148, 126, 96); WOODD = (112, 92, 68); WOODL = (178, 158, 128)
    WET = (86, 72, 58)
    V = {}
    put, ellip, box = _vox_helpers(V)

    def limb(x0, y0, z0, x1, y1, z1, r):
        n = int(max(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)) * 2) + 1
        for i in range(n + 1):
            t = i / float(n)
            cx = x0 + (x1 - x0) * t
            cy = y0 + (y1 - y0) * t
            cz = z0 + (z1 - z0) * t
            rr = r * (1.0 - 0.45 * t)
            ellip(cx, cy, cz, rr, rr, rr, WOOD, only_empty=True)
    limb(-1, 0, -2, 4, 15, 2, 2.4)          # main spar, rearing UP out of the river
    limb(2, 8, 0, -3, 15, 4, 1.2)           # gnarled fork
    limb(1, 5, -1, 6, 7, -4, 1.0)           # low broken stub
    limb(-1, 0, -2, -6, 1, -5, 1.9)         # waterlogged root hump at the surface
    put(4, 16, 2, WOODD); put(-3, 16, 4, WOODD)   # weathered snapped tips
    for (x, y, z) in list(V):
        h = (x * 61 + y * 97 + z * 41) % 9
        if h == 0:
            V[(x, y, z)] = WOODD
        elif h == 1 and y > 3:
            V[(x, y, z)] = WOODL
        if y <= 1:
            V[(x, y, z)] = WET               # wet at the waterline
    return V


# -- message in a bottle --------------------------------------------------------------
def build_bottle():
    GLASS = (138, 188, 168); GLASSD = (102, 148, 132); SHINE = (208, 238, 222)
    CORK = (196, 152, 92); CORKD = (158, 118, 66); NOTE = (240, 230, 198); NOTED = (208, 194, 156)
    V = {}
    put, ellip, box = _vox_helpers(V)
    for z in range(-6, 5):                   # bottle lying on its side, floating
        r = 2.6 if z < 3 else 1.9
        ellip(0, 0, z, r, r, 0.6, GLASS, only_empty=True)
    ellip(0, 0, -6.5, 2.2, 2.2, 0.8, GLASSD)             # butt of the bottle
    box(-1, 1, -1, 1, 5, 6, GLASSD)                      # neck
    ellip(0, 0, 8, 1.6, 1.6, 1.4, CORK)                  # fat cork, proud of the neck
    put(0, 2, 8, CORKD); put(0, -2, 8, CORKD); put(0, 0, 9.6, CORKD)
    # the rolled note fills the glass amidships — recolor the SHELL so it shows
    for (x, y, z) in list(V):
        if -5 <= z <= 1 and V[(x, y, z)] in (GLASS, GLASSD) and y < 2:
            V[(x, y, z)] = NOTE if (x + z * 2) % 3 else NOTED
    for z in range(-5, 5):                               # glass highlight streak on top
        if (1, 2, z) in V:
            V[(1, 2, z)] = SHINE
    put(0, 1, -6, SHINE)
    return V


# -- a single rogue flip-flop (flat, slightly askew) ----------------------------------
def gen_flipflop():
    SOLE_D = (198, 84, 66, 255); SOLE = (234, 112, 88, 255); BED = (248, 158, 128, 255)
    STRAP = (52, 118, 150, 255); STRAPL = (74, 152, 186, 255)

    def ff(d):
        d.rounded_rectangle([4 * FS, 2 * FS, 13 * FS, 21 * FS], radius=4 * FS, fill=SOLE)
        d.rounded_rectangle([5 * FS, 3 * FS, 12 * FS, 20 * FS], radius=3 * FS, fill=BED)
        d.ellipse([3.7 * FS, 13 * FS, 13.3 * FS, 21.3 * FS], outline=SOLE_D, width=FS)  # heel rim
        # V thong strap from the toe post
        d.line([(8.5 * FS, 6.5 * FS), (5 * FS, 13 * FS)], fill=STRAP, width=2 * FS)
        d.line([(8.5 * FS, 6.5 * FS), (12 * FS, 13 * FS)], fill=STRAP, width=2 * FS)
        d.line([(8.5 * FS, 6.5 * FS), (6 * FS, 11.5 * FS)], fill=STRAPL, width=FS)
        d.ellipse([7.6 * FS, 5.6 * FS, 9.6 * FS, 7.6 * FS], fill=SOLE_D)  # toe post
    save(flat(17, 24, ff, rot=22), "env_flipflop.png")


# -- tiny toy sailboat -----------------------------------------------------------------
def build_sailboat():
    HULL = (186, 66, 50); HULLD = (146, 46, 36); DECK = (214, 182, 128)
    SAIL = (244, 242, 232); SAILD = (212, 210, 198); MAST = (118, 90, 58)
    FLAG = (222, 150, 44)
    V = {}
    put, ellip, box = _vox_helpers(V)
    for z in range(-6, 7):                       # hull, tapering to the bow (+z)
        w = 3 if abs(z) <= 2 else (2 if abs(z) <= 4 else 1)
        box(-w, w, 0, 2, z, z, HULL)
        box(-w, w, 0, 0, z, z, HULLD)
    box(-2, 2, 3, 3, -5, 5, DECK)                # deck plank
    box(0, 0, 4, 15, 0, 0, MAST)                 # mast
    box(0, 0, 4, 4, -4, -1, MAST)                # boom
    for y in range(5, 14):                       # main sail: a white triangle
        ln = int((13 - y) * 0.55) + 1
        for z in range(-ln - 0, 0):
            put(0, y, z, SAIL if (y + z) % 4 else SAILD)
    for y in range(6, 13):                       # jib, forward of the mast
        ln = int((12 - y) * 0.4) + 1
        for z in range(1, 1 + ln):
            put(0, y, z, SAIL)
    put(0, 15, -1, FLAG); put(0, 15, -2, FLAG)   # pennant
    return V


# -- rubber raft with a sunbathing frog -------------------------------------------------
def build_raft():
    TUBE = (232, 120, 62); TUBED = (188, 86, 44); TUBEL = (250, 158, 96)
    FLOOR = (108, 140, 158); FLOORD = (84, 112, 130)
    FROG = (92, 176, 74); FROGD = (64, 136, 52); BELLY = (214, 232, 168); EYEW = (240, 240, 230)
    V = {}
    put, ellip, box = _vox_helpers(V)
    rx, rz = 7.5, 9.5
    for a in range(0, 360, 3):                   # the ring: a rounded-rect torus
        t = math.radians(a)
        px_ = rx * math.copysign(abs(math.cos(t)) ** 0.7, math.cos(t))
        pz_ = rz * math.copysign(abs(math.sin(t)) ** 0.7, math.sin(t))
        ellip(px_, 1.2, pz_, 1.9, 1.8, 1.9, TUBE, only_empty=True)
    for (x, y, z) in list(V):
        if y >= 3:
            V[(x, y, z)] = TUBEL                 # sun on top of the tube
        elif y <= 0:
            V[(x, y, z)] = TUBED
    for x in range(-5, 6):                       # floor
        for z in range(-7, 8):
            if (x, 1, z) not in V:
                put(x, 1, z, FLOOR if (x * 31 + z * 17) % 5 else FLOORD)
    # the frog, flat on his back mid-sunbathe, belly up
    ellip(0, 3.2, -1.5, 3.0, 1.8, 4.2, FROG)
    ellip(0, 4.4, -1.5, 2.1, 1.1, 3.0, BELLY)                     # pale belly up top
    ellip(0, 3.8, 3.6, 2.3, 1.8, 2.3, FROG)                       # head
    box(-2, 2, 5, 5, 3, 4, (40, 38, 44))                          # sunglasses band :)
    for s in (1, -1):
        put(s * 2, 5, 5, FROG); put(s * 2, 6, 4, FROG)            # eye bumps over the shades
        # lazy legs draped over the stern tube
        put(s * 2, 3, -5, FROGD); put(s * 3, 4, -7, FROGD)
        put(s * 3, 4, -8, FROGD); put(s * 4, 3, -9, FROGD)
        put(s * 3, 4, 1, FROGD); put(s * 4, 5, 2, FROGD)          # arms up behind the head
    return V


# =================================================================================
# BANK PROPS (bottom-center anchored on the grass)
# =================================================================================
def build_cattails(seed):
    STALK = (108, 142, 66); LEAF = (90, 128, 58); LEAFL = (128, 166, 82)
    HEAD = (124, 84, 50); HEADD = (96, 62, 38); SPIKE = (206, 186, 136)
    rng = random.Random(seed)
    V = {}
    put, ellip, box = _vox_helpers(V)
    n = rng.choice((3, 4))
    xs = [-5, -1, 3, 6][:n]
    for i, x in enumerate(xs):
        h = rng.randint(15, 21)
        z = rng.randint(-2, 2)
        lean = rng.choice((-1, 0, 1))
        for y in range(0, h):                     # stalk, with a gentle lean
            put(x + (lean if y > h // 2 else 0), y, z, STALK)
        hx = x + lean
        box(hx, hx, h - 6, h - 1, z, z + 1, HEAD)   # the brown cigar head
        box(hx, hx, h - 6, h - 3, z, z, HEADD, only_empty=True)
        put(hx, h, z, SPIKE); put(hx, h + 1, z, SPIKE)
        # arcing blade leaves off the base
        for t in range(7 + rng.randint(0, 3)):
            lx = x + int(round(t * 0.6)) * (1 if i % 2 else -1)
            ly = int(t * 1.1) + 1
            put(lx, ly, z + (1 if i % 2 else -1), LEAF if t % 2 else LEAFL)
    return V


def build_umbrella():
    RED = (204, 58, 50); REDD = (162, 40, 36); WHT = (242, 238, 228); WHTD = (214, 210, 200)
    POLE = (150, 148, 144); POLED = (112, 110, 108)
    V = {}
    put, ellip, box = _vox_helpers(V)
    for y in range(0, 15):
        put(0, y, 0, POLE if y % 4 else POLED)
    R = 11.0
    for x in range(-11, 12):                      # canopy dome, striped in 8 wedges
        for z in range(-11, 12):
            rr = math.hypot(x, z)
            if rr > R:
                continue
            y = 13 + int(round(math.sqrt(max(0.0, R * R - rr * rr)) * 0.42))
            wedge = int(((math.atan2(x, z) + math.pi) / (2 * math.pi)) * 8.0) % 2
            top = wedge == 0
            c = (RED if top else WHT)
            if rr > R - 2.2:
                c = (REDD if top else WHTD)       # darker scalloped rim
            put(x, y, z, c)
            if rr > R - 1.4:
                put(x, y - 1, z, REDD if top else WHTD)   # rim drop
    put(0, 19, 0, POLED); put(0, 20, 0, RED)      # finial
    return V


def gen_blanket():
    RED = (198, 62, 56, 255); REDL = (222, 96, 88, 255)
    WHT = (240, 234, 222, 255); WHTD = (216, 210, 198, 255)

    def bl(d):
        cols, rows = 8, 6
        w0, w1, hh, y0 = 40.0, 30.0, 22.0, 2.0     # flat perspective trapezoid
        for r in range(rows):
            for c in range(cols):
                t0, t1 = r / float(rows), (r + 1) / float(rows)
                wa, wb = w0 + (w1 - w0) * t0, w0 + (w1 - w0) * t1
                xa0 = 21 - wa / 2 + wa * c / cols
                xa1 = 21 - wa / 2 + wa * (c + 1) / cols
                xb0 = 21 - wb / 2 + wb * c / cols
                xb1 = 21 - wb / 2 + wb * (c + 1) / cols
                ya, yb = y0 + hh * t0, y0 + hh * t1
                red = (r + c) % 2 == 0
                shade_row = r in (2, 3)            # a soft fold shadow band
                col = (RED if not shade_row else REDD_(RED)) if red else \
                      (WHT if not shade_row else WHTD)
                d.polygon([(xa0 * FS, ya * FS), (xa1 * FS, ya * FS),
                           (xb1 * FS, yb * FS), (xb0 * FS, yb * FS)], fill=col)
        # picnic accents: lighter worn patches
        d.ellipse([8 * FS, 5 * FS, 12 * FS, 8 * FS], fill=REDL)

    def REDD_(c):
        return (172, 48, 44, 255)
    save(flat(42, 27, bl), "bank_blanket.png")


def build_grave():
    STONE = (148, 146, 140); STONED = (116, 114, 110); STONEL = (176, 174, 166)
    CARVE = (86, 84, 82); MOSS = (104, 128, 78)
    LOG = (140, 102, 62); LOGD = (104, 74, 44); LOGL = (176, 138, 92)
    V = {}
    put, ellip, box = _vox_helpers(V)

    def lean(y):                                   # the crooked lean
        return int(y * 0.22)
    for y in range(0, 15):
        half = 6 if y < 11 else (5 if y < 13 else 3)   # rounded top
        for x in range(-half, half + 1):
            for z in range(-1, 2):
                c = STONE
                if z < 1:                          # keep the inscribed face clean
                    h = (x * 43 + y * 29 + z * 7) % 10
                    if h == 0:
                        c = STONED
                    elif h == 1:
                        c = STONEL
                put(x + lean(y), y, z, c)
    box(-8, 8, 0, 1, -3, 3, STONED)                # plinth
    put(-6, 2, 3, MOSS); put(-5, 2, 3, MOSS); put(6, 2, 3, MOSS)   # a few moss tufts
    # THE INSCRIPTION (proud of the front face): a carved log over two text lines
    for ly in (10, 11):
        for x in range(-4, 4):                     # the dearly departed log
            put(x + lean(ly), ly, 2, LOGL if ly == 11 and x % 3 else LOG)
    for ly in (10, 11):                            # end grain + bark cracks
        put(-4 + lean(ly), ly, 2, LOGD); put(3 + lean(ly), ly, 2, LOGD)
    put(lean(10), 10, 2, LOGD); put(1 + lean(11), 11, 2, LOGD)
    for x in range(-4, 5, 2):                      # "HERE LIES"
        put(x + lean(7), 7, 2, CARVE)
    for x in range(-3, 4, 2):                      # "A LOG"
        put(x + lean(5), 5, 2, CARVE)
    return V


def build_deadtree():
    BARK = (108, 90, 72); BARKD = (82, 66, 52); BARKL = (138, 120, 98)
    V = {}
    put, ellip, box = _vox_helpers(V)

    def limb(x0, y0, z0, x1, y1, z1, r0, r1):
        n = int(max(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)) * 2) + 1
        for i in range(n + 1):
            t = i / float(n)
            rr = r0 + (r1 - r0) * t
            ellip(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, z0 + (z1 - z0) * t,
                  rr, rr, rr, BARK, only_empty=True)
    limb(0, 0, 0, 1, 12, 0, 3.0, 1.8)              # trunk
    limb(1, 12, 0, -5, 21, 1, 1.7, 0.7)            # main gnarled bough
    limb(1, 12, 0, 7, 19, -1, 1.5, 0.6)            # opposite bough
    limb(-3, 17, 1, -8, 18, 2, 0.8, 0.5)           # crook
    limb(4, 16, 0, 6, 23, 0, 0.9, 0.5)             # skyward claw
    limb(1, 13, 0, 2, 25, 1, 1.1, 0.5)             # dead leader
    limb(0, 3, 0, -6, 1, -2, 1.4, 0.6)             # root flare
    limb(0, 2, 0, 5, 0, 2, 1.3, 0.6)
    for (x, y, z) in list(V):
        h = (x * 53 + y * 89 + z * 37) % 8
        if h == 0:
            V[(x, y, z)] = BARKD
        elif h == 1 and x < 0:
            V[(x, y, z)] = BARKD                   # shaded side
        elif h == 2 and y > 6:
            V[(x, y, z)] = BARKL
    return V


def build_sandcastle():
    SAND = (224, 194, 134); SANDD = (192, 158, 104); SANDL = (244, 222, 168)
    DOOR = (110, 88, 58); FLAG = (206, 60, 52); POLE = (150, 126, 92)
    V = {}
    put, ellip, box = _vox_helpers(V)

    def tier(cy0, cy1, r):
        for y in range(cy0, cy1 + 1):
            for x in range(-r, r + 1):
                for z in range(-r, r + 1):
                    if math.hypot(x, z) <= r + 0.3:
                        h = (x * 67 + y * 13 + z * 101) % 9
                        c = SANDD if h == 0 else (SANDL if h == 1 else SAND)
                        put(x, y, z, c)
        # crenellations round the rim
        for a in range(0, 360, 45):
            cx = int(round((r - 0.4) * math.cos(math.radians(a))))
            cz = int(round((r - 0.4) * math.sin(math.radians(a))))
            box(cx, cx, cy1 + 1, cy1 + 2, cz, cz, SANDL)
    tier(0, 4, 8)
    for x in range(-7, 8):                         # shadow ring where the keep meets the base
        for z in range(-7, 8):
            if 4.3 < math.hypot(x, z) <= 6.8:
                put(x, 5, z, SANDD, only_empty=True)
    tier(6, 12, 4)                                 # the keep, clearly narrower + taller
    box(-1, 1, 0, 3, 7, 8, DOOR)                   # arched doorway in the outer wall
    put(0, 4, 8, DOOR)
    put(-2, 8, 4, DOOR); put(2, 8, 4, DOOR)        # arrow-slit windows on the keep
    for y in range(12, 19):
        put(0, y, 0, POLE)
    for dy, dzs in ((18, (1, 2, 3)), (17, (1, 2)), (16, (1,))):   # snapping pennant
        for dz in dzs:
            put(0, dy, dz, FLAG)
    return V


def build_lamp():
    IRON = (56, 60, 66); IROND = (40, 44, 50); IRONL = (84, 90, 98)
    GLOW = (255, 224, 118); GLOWL = (255, 246, 198); GLOWD = (232, 178, 64)
    V = {}
    put, ellip, box = _vox_helpers(V)
    box(-2, 2, 0, 1, -2, 2, IROND)                 # base plinth
    ellip(0, 2, 0, 1.8, 1.2, 1.8, IRON)
    for y in range(3, 20):
        put(0, y, 0, IRON if y % 5 else IRONL)     # fluted post
    ellip(0, 20, 0, 1.4, 0.8, 1.4, IROND)          # collar
    for y in range(21, 26):                        # the lamp box, glowing warm
        r = 2 if y in (22, 23, 24) else 1
        for x in range(-r, r + 1):
            for z in range(-r, r + 1):
                core = abs(x) < r and abs(z) < r and y in (22, 23, 24)
                put(x, y, z, GLOWL if core else (GLOW if y in (22, 23, 24) else GLOWD))
    box(-2, 2, 26, 26, -2, 2, IRON)                # cap
    put(0, 27, 0, IRON); put(0, 28, 0, IRONL)      # finial
    for s in (1, -1):                              # little scroll arms under the cap
        put(s * 2, 21, 0, IRON); put(s * 3, 22, 0, IRON)
    return V


def build_fern():
    F_D = (54, 110, 56); F = (82, 148, 72); F_L = (118, 184, 94); STEM = (66, 122, 60)
    V = {}
    put, ellip, box = _vox_helpers(V)
    rng = random.Random(7)
    for i in range(6):
        a = math.radians(i * 60 + rng.uniform(-10, 10))
        reach = rng.uniform(9.0, 12.0)
        droop = rng.uniform(0.25, 0.4)
        for t in range(0, 14):
            tt = t / 13.0
            r = reach * tt
            y = 1 + 9.5 * math.sin(tt * 2.1) * (1 - tt * droop)   # arch up, then droop
            x = int(round(r * math.cos(a)))
            z = int(round(r * math.sin(a)))
            put(x, int(round(y)), z, STEM if t % 3 == 0 else F)
            if t >= 3:                             # paired leaflets off the rib
                lw = 2 if 4 <= t <= 10 else 1      # widest mid-frond
                for s in (1, -1):
                    for k in range(1, lw + 1):
                        lx = int(round(x - math.sin(a) * s * k))
                        lz = int(round(z + math.cos(a) * s * k))
                        col = F_L if (t + k) % 3 == 0 else (F if k == 1 else F_D)
                        put(lx, int(round(y - 0.4 * k)), lz, col, only_empty=True)
    ellip(0, 1, 0, 1.8, 1.3, 1.8, F_D)             # rooty crown
    return V


def build_shrooms():
    CAP = (66, 182, 170); CAPD = (44, 142, 134); CAPL = (148, 232, 216)
    STEMC = (222, 214, 192); STEMD = (186, 178, 156); GILL = (52, 110, 106)
    V = {}
    put, ellip, box = _vox_helpers(V)
    for (cx, cz, h, r) in ((-3, 0, 7, 4.4), (3, 1, 4, 3.2), (0, -3, 3, 2.4)):
        for y in range(0, h):
            put(cx, y, cz, STEMC if y % 2 else STEMD)
            if r > 3:
                put(cx + 1, y, cz, STEMD, only_empty=True)
        ellip(cx, h + 0.6, cz, r, r * 0.62, r, CAP)
        for (x, y, z) in list(V):                  # trim cap underside + gills
            if abs(x - cx) <= r and abs(z - cz) <= r and y == h and V[(x, y, z)] == CAP:
                V[(x, y, z)] = GILL
        # glow spots
        for (x, y, z) in list(V):
            if V[(x, y, z)] == CAP and (x * 47 + y * 13 + z * 89) % 7 == 0:
                V[(x, y, z)] = CAPL
        put(cx, h + int(r * 0.62) + 1, cz, CAPL, only_empty=True)  # crown glint
    return V


def build_pine():
    PINE = (46, 96, 60); PINED = (32, 72, 46); SNOW = (238, 242, 248); SNOWD = (208, 218, 232)
    TRUNK = (104, 78, 52)
    V = {}
    put, ellip, box = _vox_helpers(V)
    box(-1, 1, 0, 3, -1, 1, TRUNK)
    for i, (cy, r, hh) in enumerate(((4, 8.5, 4), (8, 6.8, 4), (12, 5.0, 4), (16, 3.2, 4))):
        for y in range(cy, cy + hh):
            rr = r * (1.0 - (y - cy) / float(hh + 1))
            for x in range(-int(rr), int(rr) + 1):
                for z in range(-int(rr), int(rr) + 1):
                    if math.hypot(x, z) <= rr + 0.3:
                        put(x, y, z, PINED if (x * 31 + y * 7 + z * 53) % 6 == 0 else PINE)
    put(0, 20, 0, PINE); put(0, 21, 0, SNOW)
    # snow dusting: every column's topmost pine voxel goes white (heavier outboard)
    cols = {}
    for (x, y, z) in V:
        if V[(x, y, z)] in (PINE, PINED):
            cols[(x, z)] = max(y, cols.get((x, z), -99))
    for (x, z), top in cols.items():
        d2 = math.hypot(x, z)
        h = (x * 71 + z * 43) % 5
        if d2 > 1.5 and h < 4:
            V[(x, top, z)] = SNOW if h < 3 else SNOWD
    return V


def build_snowduck():
    SNOW = (242, 246, 252); SNOWD = (212, 222, 236); SNOWL = (252, 254, 255)
    CARROT = (236, 140, 44); COAL = (40, 38, 40); STICK = (122, 92, 58)
    SCARF = (198, 62, 56); SCARFD = (162, 44, 40)
    V = {}
    put, ellip, box = _vox_helpers(V)
    ellip(0, 4, 0, 6.0, 4.6, 6.6, SNOW)            # body snowball
    ellip(0, 3, 0, 6.2, 3.4, 6.8, SNOWD, only_empty=True)
    ellip(0, 10.5, 3.0, 3.8, 3.6, 3.8, SNOW)       # head snowball
    ellip(0, 12, 3.4, 2.6, 1.9, 2.6, SNOWL, only_empty=True)
    # the all-important snow tail-curl (it is a DUCK)
    put(0, 7, -6, SNOW); put(0, 8, -7, SNOW); put(0, 9, -7, SNOWL); put(0, 9, -8, SNOW)
    ellip(0, 6.8, -5.8, 1.7, 1.4, 1.7, SNOWD)
    # cozy red scarf tucked between head and body, tail flapping down the chest
    ellip(0, 8.2, 2.6, 3.1, 1.0, 3.1, SCARF)
    put(2, 7, 5, SCARFD); put(2, 6, 5, SCARF); put(2, 5, 6, SCARFD)
    box(-1, 1, 9, 10, 6, 9, CARROT)                # carrot bill (flat + wide, ducklike)
    put(0, 9, 10, (196, 106, 30)); put(0, 10, 9, (250, 176, 84))
    for s in (1, -1):
        put(s * 3, 11, 5, COAL); put(s * 3, 12, 5, COAL)   # coal eyes, on the surface
        for t in range(4):                         # stick wings
            put(s * (6 + t // 2), 5 + t % 2, 1 - t, STICK)
    return V


def build_cow():
    HIDE = (240, 236, 226); HIDED = (212, 208, 198); PATCH = (46, 44, 48); PATCHL = (72, 70, 76)
    MUZZLE = (224, 164, 152); UDDER = (232, 180, 168); HOOF = (52, 46, 44)
    HORN = (218, 204, 172); EYE = (30, 28, 30); TAIL = (216, 212, 202)
    V = {}
    put, ellip, box = _vox_helpers(V)
    ellip(0, 11, -1, 4.6, 4.8, 9.0, HIDE)          # barrel body
    ellip(0, 8.6, -1, 4.2, 2.4, 8.0, HIDED, only_empty=True)
    # Holstein patches: fixed hash blobs
    for (bx, by, bz, r) in ((-3, 12, -6, 3.4), (4, 12, 2, 3.0), (-2, 10, 4, 2.6),
                            (3, 13, -4, 2.8), (0, 14, -1, 2.2)):
        for (x, y, z) in list(V):
            if (x - bx) ** 2 + (y - by) ** 2 + (z - bz) ** 2 <= r * r:
                V[(x, y, z)] = PATCH if (x * 31 + z * 17) % 7 else PATCHL
    for s in (1, -1):                              # legs
        for (lz,) in ((-6,), (5,)):
            box(int(s * 2.5) - 0, int(s * 2.5), 1, 7, lz, lz + 1, HIDE)
            box(int(s * 2.5), int(s * 2.5), 0, 1, lz, lz + 1, HOOF)
    ellip(0, 6.4, -3, 2.2, 1.7, 2.4, UDDER)        # udder
    # neck + head, raised, placidly watching the river
    ellip(0, 15, 8, 2.6, 3.0, 2.6, HIDE)
    ellip(0, 17.5, 10, 2.7, 2.5, 3.2, HIDE)        # head
    box(-1, 1, 15, 16, 12, 13, MUZZLE)             # pink muzzle
    put(-1, 15, 13, (150, 96, 88)); put(1, 15, 13, (150, 96, 88))   # nostrils
    for s in (1, -1):
        put(s * 3, 18, 9, EYE)                     # calm eyes
        box(s * 3, s * 4, 19, 19, 8, 9, HIDE)      # ears out sideways
        put(s * 4, 19, 8, HIDED)
        put(s * 2, 20, 9, HORN); put(s * 2, 21, 9, HORN)   # little horns
    for (x, y, z) in list(V):                      # head patch over one eye
        if x >= 1 and y >= 16 and z >= 9 and V[(x, y, z)] == HIDE:
            V[(x, y, z)] = PATCH
    for i in range(7):                             # tail down the rump
        put(0, 14 - i, -10 - (1 if i > 3 else 0), TAIL)
    put(0, 7, -11, PATCH); put(0, 6, -11, PATCH)   # tail tuft
    return V


# =================================================================================
# THE HERON (standing model + turntable + swoop frames)
# =================================================================================
def build_heron_standing(plume_up=True):
    """Great blue heron STANDING: stilt legs, S-neck, dagger bill, black plume."""
    BODY = (134, 150, 170); BODYD = (100, 114, 134); COVERT = (120, 136, 156)
    SEC = (74, 84, 102); PRIM = (34, 38, 50); WHITE = (246, 248, 250)
    CREST = (20, 22, 30); BILL = (240, 198, 86); BILLD = (198, 152, 54)
    RUST = (162, 100, 60); LEG = (70, 60, 50); EYE = (252, 212, 70)
    V = {}
    put, ellip, box = _vox_helpers(V)
    # stilt legs + big toes (y=0 is the ground)
    for s in (1, -1):
        for y in range(0, 10):
            put(s * 2, y, -1 if y < 5 else 0, LEG)
        put(s * 2, 5, -1, RUST)                        # knee
        for t in (-2, 0, 2):
            put(s * 2 + (1 if t > 0 else (-1 if t < 0 else 0)), 0, t + 1, LEG)
        put(s * 2, 0, 3, LEG)
    # body: horizontal teardrop, tail high at the back
    ellip(0, 12.5, 0, 3.6, 3.2, 6.4, BODY)
    ellip(0, 14, -1, 3.0, 2.2, 5.6, COVERT, only_empty=True)
    ellip(0, 10.8, 1.5, 2.9, 1.9, 4.6, WHITE, only_empty=True)     # pale breast-belly
    # folded wing slabs down the flanks, slate -> black primaries at the tail
    for s in (1, -1):
        ellip(s * 3.2, 13, -1.5, 1.3, 2.4, 4.8, SEC)
        box(s * 2, s * 3, 12, 14, -8, -6, PRIM)
        put(s * 3, 14, -5, PRIM); put(s * 2, 15, -6, PRIM)
        put(s * 3, 12, 2, RUST); put(s * 3, 13, 3, RUST)           # rust shoulder
    box(-1, 1, 13, 15, -9, -7, PRIM)                                # short dark tail
    put(0, 15, -10, SEC)
    # THE S-NECK: swept back off the chest, then up and forward to the head
    neck = [(15.0, 4.5), (16.4, 5.4), (17.8, 5.8), (19.2, 5.4),
            (20.6, 4.6), (22.0, 4.2), (23.4, 4.6)]
    for i, (ny, nz) in enumerate(neck):
        r = 1.6 if i < 3 else 1.3
        ellip(0, ny, nz, r, 1.1, r, BODY)
        if i < 6:
            put(0, int(ny), int(nz) + 2, WHITE, only_empty=True)   # white throat stripe
    put(1, 17, 6, RUST); put(-1, 17, 6, RUST)                       # rusty neck streaks
    put(1, 19, 5, CREST); put(-1, 19, 5, CREST)                     # neck dashes
    # head: white crown, black brow band -> trailing plume
    ellip(0, 25.2, 5.5, 2.0, 1.9, 2.4, WHITE)
    for z in (4, 5, 6):
        put(1, 26.5, z, CREST); put(-1, 26.5, z, CREST)
        put(1, 27, z, CREST, only_empty=True); put(-1, 27, z, CREST, only_empty=True)
    if plume_up:
        for i, z in enumerate((3, 2, 1, 0)):                        # the plume, trailing back
            put(0, 27 - (i + 1) // 2, z, CREST)
    # dagger bill, aimed level over the water
    box(0, 0, 24, 25, 7, 12, BILL)
    box(0, 0, 24, 24, 10, 12, BILLD)
    put(0, 25, 13, BILLD)
    put(2, 25, 6, EYE); put(-2, 25, 6, EYE)                         # fierce yellow eye
    put(2, 25, 7, CREST); put(-2, 25, 7, CREST)
    return V


def gen_heron():
    # 16-frame compendium turntable (spin_set convention: shared bbox crop)
    SH = shade(build_heron_standing())
    out = 200
    imgs = [render(SH, math.radians(i * 22.5), math.radians(26), out=out, scale=3.4)
            for i in range(16)]
    bb = None
    for im in imgs:
        b = im.getbbox()
        if b:
            bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]),
                                       max(bb[2], b[2]), max(bb[3], b[3]))
    bb = (max(0, bb[0] - 4), max(0, bb[1] - 4), min(out, bb[2] + 4), min(out, bb[3] + 4))
    for i, im in enumerate(imgs):
        save(im.crop(bb), "heron_spin_%02d.png" % i)
    # gameplay swoop: the strike-dive model (wings out, legs trailing), 2 flap
    # poses, top-down-ish, head diving DOWN the screen like the existing heron_*.
    fr = vox_frames([build_heron(1), build_heron(2)], yaw=0, pitch=62, target=48)
    save(fr[0], "heron_swoop_0.png")
    save(fr[1], "heron_swoop_1.png")


# =================================================================================
# generate everything + contact sheet
# =================================================================================
def main():
    # ---- water scenery ----
    gen_lilies()
    gen_duckweed()
    save(vox(build_stone(1), yaw=20, pitch=48, target=26), "env_stone_0.png")
    save(vox(build_stone(5, wide=True), yaw=155, pitch=48, target=30), "env_stone_1.png")
    save(vox(build_snag(), yaw=30, pitch=36, target=37), "env_snag.png")
    save(vox(build_bottle(), yaw=118, pitch=52, target=22), "env_bottle.png")
    gen_flipflop()
    save(vox(build_sailboat(), yaw=52, pitch=38, target=30), "env_sailboat.png")
    save(vox(build_raft(), yaw=14, pitch=58, target=33), "env_raft.png")
    # ---- bank props ----
    save(vox(build_cattails(21), yaw=8, pitch=30, target=30), "bank_cattail_0.png")
    save(vox(build_cattails(35), yaw=-12, pitch=30, target=34), "bank_cattail_1.png")
    save(vox(build_umbrella(), yaw=15, pitch=40, target=40), "bank_umbrella.png")
    gen_blanket()
    save(vox(build_grave(), yaw=6, pitch=28, target=29), "bank_grave.png")
    save(vox(build_deadtree(), yaw=25, pitch=30, target=46), "bank_deadtree.png")
    save(vox(build_sandcastle(), yaw=18, pitch=38, target=32), "bank_sandcastle.png")
    save(vox(build_lamp(), yaw=10, pitch=28, target=46), "bank_lamp.png")
    save(vox(build_fern(), yaw=12, pitch=32, target=32), "bank_fern.png")
    save(vox(build_shrooms(), yaw=20, pitch=36, target=23), "bank_shroom.png")
    save(vox(build_pine(), yaw=12, pitch=30, target=48), "bank_pine.png")
    save(vox(build_snowduck(), yaw=24, pitch=32, target=28), "bank_snowduck.png")
    save(vox(build_cow(), yaw=78, pitch=30, target=50), "bank_cow.png")
    # ---- the heron ----
    gen_heron()

    print("generated %d sprites -> %s" % (len(GENERATED), os.path.abspath(ART)))
    for n in GENERATED:
        im = Image.open(os.path.join(ART, n))
        print("  %-24s %dx%d" % (n, im.width, im.height))


if __name__ == "__main__":
    main()
