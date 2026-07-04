#!/usr/bin/env python3
"""HERO LANDMARKS for DUCKODUCKO -> ../art/hero_*.png

One memorable set-piece per pond biome. These drift by RARELY (~every 800ft),
so each is a landmark, not clutter: big (100-150px long axis), strong
silhouette, readable against BOTH mid-blue and dark-navy water.

Style contract (tools/voxel_duck.py + tools/gen_env.py, unchanged):
  * voxel models -> shade() -> painter's render() at S=5 supersample ->
    LANCZOS -> snap to the model's own palette -> 1px (36,28,28) ink outline
  * the one flat piece (the Cochichewick loon) uses gen_env's crisp 2D
    pipeline; its aurora reflection gets NO ink line — it's light, not a thing
    (the voxel_duck fire precedent).

Pixel density is calibrated to the gen_env props (env_snag.png ~= 2.1 px per
voxel), so heroes are BIGGER things, not zoomed-in small things.

Deterministic (fixed seeds / hash speckles). Pillow only.
Run:  python3 tools/gen_heroes.py     (from the repo root)
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voxel_duck import _vox_helpers, shade, render       # noqa: E402
from gen_env import vox, _crisp, _outline, FS            # noqa: E402

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "art")
os.makedirs(ART, exist_ok=True)
GENERATED = []


def save(img, name):
    img.save(os.path.join(ART, name))
    GENERATED.append(name)
    print("  %-24s %dx%d" % (name, img.width, img.height))


def _limb3(V, p0, p1, p2, r0, r1, col, taper=1.0):
    """Quadratic-bezier limb of spheres (gnarl-friendly gen_env limb upgrade)."""
    put, ellip, box = _vox_helpers(V)
    n = int(2.2 * max(abs(p2[0] - p0[0]), abs(p2[1] - p0[1]), abs(p2[2] - p0[2]))) + 2
    for i in range(n + 1):
        t = i / float(n)
        q = [(1 - t) * ((1 - t) * p0[k] + t * p1[k]) + t * ((1 - t) * p1[k] + t * p2[k])
             for k in range(3)]
        r = r0 + (r1 - r0) * (t ** taper)
        ellip(q[0], q[1], q[2], r, r, r, col, only_empty=True)


# =================================================================================
# BUKER POND — a half-sunken wooden rowboat, stern swamped, one oar adrift
# =================================================================================
def build_rowboat():
    HULL = (140, 112, 80); HULLD = (104, 82, 58); HULLL = (174, 146, 108)
    PAINT = (172, 62, 50); PAINTD = (130, 44, 38)
    FLOOR = (92, 72, 50); RIB = (70, 54, 38)
    SEAT = (198, 172, 130); SEATD = (160, 136, 98)
    BILGE = (46, 90, 102); BILGEL = (98, 152, 162)
    WET = (64, 66, 58)
    OAR = (196, 168, 122); OARD = (148, 122, 82)
    V = {}
    put, ellip, box = _vox_helpers(V)
    L = 26                                    # half-length -> 53 voxels stem to stern

    def halfw(t):                             # beam profile: transom -> fat waist -> stem
        if t <= 0.55:
            return 5.4 + 2.4 * math.sin(t / 0.55 * math.pi / 2.0)
        u = (t - 0.55) / 0.45
        return max(0.9, 7.8 * math.cos(u * math.pi / 2.0) ** 0.8)

    for zi in range(-L, L + 1):
        t = (zi + L) / (2.0 * L)              # 0 = stern, 1 = bow
        w = halfw(t)
        yk = int(round(3.5 * max(0.0, (t - 0.72) / 0.28) ** 1.6))   # keel sweeps up at the bow
        ytop = yk + 9 + int(round(2.0 * max(0.0, (t - 0.70) / 0.30) ** 1.2))
        for y in range(yk, ytop + 1):
            frac = (y - yk) / max(1.0, float(ytop - yk))
            xs = int(round(w * (0.30 + 0.70 * frac ** 0.65)))
            lap = HULLL if (y - yk) % 2 else HULL             # lapstrake plank bands
            if (zi * 13 + y * 29) % 11 == 0:
                lap = HULLD                                    # weathering
            c = PAINT if y == ytop else lap                    # one faded-red sheer stripe
            _ = PAINTD
            put(xs, y, zi, c); put(-xs, y, zi, c)
            if y == yk:                                        # hull bottom
                for x in range(-xs, xs + 1):
                    put(x, y, zi, HULLD, only_empty=True)
            if y == yk + 1 and abs(zi) < L - 1:                # interior floorboards
                for x in range(-max(0, xs - 1), max(0, xs - 1) + 1):
                    put(x, y, zi, RIB if zi % 6 == 0 else FLOOR, only_empty=True)
    for y in range(0, 12):                                     # transom plate
        for x in range(-5, 6):
            put(x, y, -L, PAINT if y >= 10 else HULLD, only_empty=True)
    for z0, z1 in ((-8, -5), (8, 11)):                         # two thwart seats
        for zi in range(z0, z1 + 1):
            t = (zi + L) / (2.0 * L)
            xs = int(round(halfw(t))) - 1
            for x in range(-xs, xs + 1):
                put(x, 5, zi, SEATD if x in (-xs, xs) else SEAT)
    # THE SINKING: pitch the whole boat, stern under the waterline, then cut y<0
    V2 = {}
    for (x, y, z), c in V.items():
        y2 = y + int(round((z + L) * 0.30)) - 11
        if y2 < 0:
            continue
        V2[(x, y2, z)] = WET if y2 <= 1 else c
    V = V2
    put, ellip, box = _vox_helpers(V)
    # swamped bilge: pond water standing inside the aft half
    for zi in range(-L + 1, 10):
        t = (zi + L) / (2.0 * L)
        tilt = int(round((zi + L) * 0.30)) - 11
        if tilt + 9 < 2:                       # gunwale underwater here: open pond
            continue
        xs = int(round(halfw(t) * 0.72))
        for x in range(-xs, xs + 1):
            put(x, 1, zi, BILGEL if (x * 31 + zi * 17) % 9 == 0 else BILGE,
                only_empty=True)
    # one oar adrift, clearly APART from the wreck
    for i in range(0, 19):
        zi = -14 + i
        x = 17 + int(round(i * 0.22))
        put(x, 1, zi, OAR if i % 3 else OARD)
    ellip(16.5, 1, -16.5, 1.8, 0.8, 2.8, OAR)                  # blade
    ellip(16.5, 1, -16.5, 1.8, 0.3, 2.8, OARD, only_empty=True)
    put(21, 1, 5, OARD); put(21, 2, 5, OARD)                   # grip
    return V


# =================================================================================
# WOODBURY POND — the end of a little picnic dock: planks, basket, fishing rod
# =================================================================================
def build_dock():
    PLANK = (174, 152, 118); PLANKD = (142, 120, 90); PLANKL = (198, 178, 142)
    SEAM = (106, 90, 66); NAIL = (82, 66, 50)
    POST = (128, 106, 78); POSTD = (96, 78, 56); WETP = (66, 62, 52)
    BASK = (190, 144, 86); BASKD = (148, 106, 58); LID = (206, 162, 102)
    CLOTH = (214, 66, 58); CLOTHW = (240, 234, 222)
    ROD = (124, 86, 50); RODL = (164, 120, 74); REEL = (62, 66, 74)
    LINE = (214, 222, 226); BOB = (224, 58, 48); BOBW = (240, 236, 228)
    V = {}
    put, ellip, box = _vox_helpers(V)
    rng = random.Random(41)
    # deck: planks run along x, 3-voxel boards with seams + per-board weathering
    for zi in range(-15, 16):
        board = (zi + 15) // 3
        c = (PLANK, PLANKD, PLANKL, PLANK)[board % 4]
        for x in range(-22, 23):
            put(x, 7, zi, PLANKD)
            top = SEAM if (zi + 15) % 3 == 0 else c
            if (x * 7 + zi * 13) % 17 == 0:
                top = PLANKD
            put(x, 8, zi, top)
    # pilings: front pair stop under the deck, back pair rise as mooring posts
    for (px, pz, tall) in ((-19, 12, False), (19, 12, False), (-19, -12, True), (19, -12, True)):
        for y in range(0, 14 if tall else 7):
            put(px, y, pz, WETP if y <= 1 else (POST if y % 4 else POSTD))
            put(px + 1, y, pz, WETP if y <= 1 else POSTD, only_empty=True)
        if tall:
            put(px, 14, pz, POSTD); put(px + 1, 14, pz, POSTD)   # weathered cap
        put(px, 9, pz, NAIL, only_empty=True)
    # picnic basket, lid half-open with the checkered cloth puffing out
    for x in range(-16, -3):
        for zi in range(-1, 9):
            for y in range(9, 16):
                put(x, y, zi, BASKD if (x + y // 2 + zi) % 2 else BASK)
    for x in range(-16, -3):                                     # rim + split lid
        for zi in range(-1, 9):
            put(x, 16, zi, LID if zi < 4 else
                (CLOTH if (x // 2 + zi // 2) % 2 else CLOTHW))
    for zi in range(4, 9):                                       # cloth spills over the edge
        put(-2, 15, zi, CLOTH if zi % 2 else CLOTHW)
        put(-2, 14, zi, CLOTHW if zi % 2 else CLOTH, only_empty=True)
    for i in range(13):                                          # wicker handle arc
        hx = -16 + i
        put(hx, 16 + int(round(3.6 * math.sin(i / 12.0 * math.pi))), 4, BASKD)
    # fishing rod leaning out over the water, flexed under its own tip weight
    _limb3(V, (12, 9, 13), (22, 27, 3), (24, 38, -5), 1.15, 0.45, ROD)
    for (x, y, z) in list(V):
        if V[(x, y, z)] == ROD and (x + y + z) % 5 == 0:
            V[(x, y, z)] = RODL                                  # cane wraps
    ellip(15.5, 15.0, 10, 1.7, 1.7, 1.4, REEL)                   # reel + crank nub
    put(18, 14, 10, RODL)
    for y in range(2, 37):                                       # dashed monofilament
        if y % 2:
            put(24, y, -5, LINE, only_empty=True)
    put(24, 1, -5, BOB); put(24, 2, -5, BOBW)                    # red/white bobber
    _ = rng
    return V


# =================================================================================
# PURGATORY POND — a huge gnarled dead tree out of the water, crow on a bough
# =================================================================================
def build_dreadtree():
    BARK = (88, 74, 64); BARKD = (58, 48, 42); BARKL = (122, 106, 90)
    HOLLOW = (32, 26, 24); WET = (48, 46, 42)
    CROW = (22, 22, 28); CROWL = (52, 56, 74); BEAK = (96, 96, 104)
    V = {}
    put, ellip, box = _vox_helpers(V)
    _limb3(V, (0, -3, 0), (5, 14, -2), (1, 30, 1), 6.0, 3.4, BARK)       # twisting trunk
    _limb3(V, (1, 30, 1), (-8, 44, 4), (-2, 60, 2), 3.4, 1.1, BARK)      # dead leader
    _limb3(V, (0, 26, 0), (-15, 34, -5), (-27, 48, -7), 2.6, 0.8, BARK)  # great left bough
    _limb3(V, (-14, 34, -5), (-20, 36, -2), (-24, 41, 3), 1.2, 0.5, BARK)
    _limb3(V, (2, 20, 0), (15, 26, 5), (23, 38, 7), 2.2, 0.7, BARK)      # right bough
    _limb3(V, (14, 25, 4), (18, 32, 2), (17, 40, -1), 1.0, 0.5, BARK)
    _limb3(V, (0, 42, 3), (6, 52, 1), (4, 62, 0), 1.3, 0.5, BARK)        # skyward claw
    _limb3(V, (-3, 14, -2), (-11, 16, -6), (-15, 15, -8), 2.0, 1.0, BARK)  # snapped stub
    for a in (25, 105, 195, 285):                                # root flare at the waterline
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        _limb3(V, (0, 1, 0), (ca * 7, 1, sa * 7), (ca * 14, 0, sa * 14), 4.2, 1.2, BARK)
    for (x, y, z) in list(V):                                    # grain, streaks, shade side
        h = (x * 31 + y * 7 + z * 53) % 13
        if h in (0, 1):
            V[(x, y, z)] = BARKD
        elif h == 2 and x > 2:
            V[(x, y, z)] = BARKL
        if (x * 5 + z * 11) % 9 == 0 and y > 4:
            V[(x, y, z)] = BARKD
        if y <= 1:
            V[(x, y, z)] = WET
    ellip(2, 19, 4.5, 2.2, 3.2, 1.6, HOLLOW)                     # black hollow knot
    # THE CROW, perched out on the right bough tip, clear of the crown
    cx, cy, cz = 23, 41, 7
    ellip(cx, cy + 1.2, cz, 2.1, 1.9, 3.1, CROW)
    box(cx, cx, cy, cy + 1, cz - 5, cz - 4, CROW)                # tail
    ellip(cx, cy + 4.0, cz + 2.6, 1.5, 1.5, 1.6, CROW)           # head
    put(cx, cy + 4, cz + 5, BEAK); put(cx, cy + 4, cz + 4, BEAK)  # bill
    put(cx + 1, cy + 4, cz + 3, (208, 196, 120))                 # eye glint
    for (x, y, z) in list(V):                                    # feather sheen
        if V[(x, y, z)] == CROW and y >= cy + 2 and (x + z) % 3 == 0:
            V[(x, y, z)] = CROWL
    return V


# =================================================================================
# SAND POND — a listing red/white channel buoy, gull on top, little sandbar
# =================================================================================
def build_buoy():
    RED = (198, 52, 44); REDD = (152, 34, 30); WHT = (238, 232, 220); WHTD = (202, 196, 184)
    RUST = (148, 90, 46); WETB = (108, 94, 78)
    CAGE = (54, 58, 64); CAGEL = (88, 94, 102); LIGHT = (255, 212, 86); LIGHTL = (255, 244, 182)
    SAND = (228, 200, 142); SANDD = (198, 166, 110); SANDW = (168, 138, 94)
    SHELL = (246, 240, 228); GRASS = (142, 162, 92)
    GULL = (244, 242, 234); GULLM = (176, 186, 196); GULLD = (62, 68, 76)
    GBILL = (230, 168, 52); GLEG = (226, 160, 60)
    V = {}
    put, ellip, box = _vox_helpers(V)
    # the sandbar, off to port: a proper DOMED hump, wet dark rim at the water
    for x in range(-25, 1):
        for z in range(-9, 10):
            r = math.hypot((x + 13) / 11.5, (z - 1) / 8.5)
            if r > 1.0:
                continue
            put(x, 0, z, SANDW)
            h = (x * 67 + z * 101) % 9
            c = SANDD if h == 0 else SAND
            if r < 0.80:
                put(x, 1, z, c)
            if r < 0.52:
                put(x, 2, z, c)
            if r < 0.28:
                put(x, 3, z, SAND if h else SANDD)
    put(-9, 2, 4, SHELL); put(-18, 2, -4, SHELL)                  # shells
    for i in range(5):                                            # a dune-grass tuft on the crown
        put(-13 + (i % 2), 4 + i, 1 + (1 if i > 2 else 0), GRASS)
        if i in (1, 3):
            put(-15 + i, 4 + i - 1, 2, GRASS)

    def lean(y):                                                  # a proper drunken list
        return int(round(y * 0.30))
    BX = 6                                                        # buoy floats OFF the bar

    def disc(y, rr, c_of):
        for x in range(-int(rr) - 1, int(rr) + 2):
            for z in range(-int(rr) - 1, int(rr) + 2):
                if math.hypot(x, z) <= rr:
                    put(x + BX + lean(y), y, z, c_of(x, y, z))
    for y in range(0, 25):                                        # FAT can body, 3 wide bands
        if y < 4:
            rr = 8.6                                              # flared skirt at the water
        elif y < 16:
            rr = 7.6
        else:
            rr = 7.6 - 4.4 * (y - 16) / 9.0                       # cone shoulder
        band_red = (y // 8) % 2 == 0

        def col(x, yy, z, band_red=band_red):
            if yy <= 1:
                return WETB
            c = RED if band_red else WHT
            h = (x * 43 + yy * 29 + z * 7) % 12
            if h == 0:
                c = REDD if band_red else WHTD
            if not band_red and (x * 7 + z * 3) % 13 == 0 and yy < 14:
                c = RUST                                          # rust weeping down
            return c
        disc(y, rr, col)
    for (cx, cz) in ((-2, -2), (2, -2), (-2, 2), (2, 2)):         # lamp cage posts
        for y in range(25, 29):
            put(BX + cx + lean(y), y, cz, CAGE if y % 2 else CAGEL)
    for y in range(28, 32):                                       # the beacon ON TOP: it glows
        box(BX + lean(y) - 2, BX + lean(y) + 2, y, y, -2, 2,
            LIGHTL if y == 31 else LIGHT)
    put(BX + lean(31), 31, 0, LIGHTL)
    # the gull, perched on the warm lamp: white, grey saddle, dark wingtips
    gx, gy = BX + lean(32), 32
    ellip(gx, gy + 2.6, -0.5, 2.6, 2.2, 3.9, GULL)
    for (x, y, z) in list(V):                                     # grey saddle, BODY only
        if V[(x, y, z)] == GULL and gy + 4 <= y <= gy + 5 and -3 <= z <= 0:
            V[(x, y, z)] = GULLM
    box(gx - 1, gx + 1, gy + 3, gy + 4, -6, -4, GULLD)            # dark wingtips + tail
    ellip(gx, gy + 6.6, 2.8, 1.6, 1.7, 1.9, GULL)                 # head
    box(gx, gx, gy + 5, gy + 6, 5, 6, GBILL)                      # stout yellow bill
    put(gx + 1, gy + 6, 4, (32, 32, 36)); put(gx - 1, gy + 6, 4, (32, 32, 36))
    put(gx - 1, gy, 0, GLEG); put(gx + 1, gy, 0, GLEG)            # legs
    return V


# =================================================================================
# PLEASANT POND — a mossy two-tier stone fountain, still spilling (park remnant)
# =================================================================================
def build_fountain():
    ST = (148, 146, 138); STD = (116, 114, 108); STL = (178, 176, 168)
    MOSS = (94, 126, 70); MOSSD = (68, 100, 52)
    WAT = (86, 152, 186); WATL = (140, 200, 224); FOAM = (224, 244, 250)
    WET = (84, 90, 86)
    V = {}
    put, ellip, box = _vox_helpers(V)

    def hash3(x, y, z):
        return (x * 43 + y * 29 + z * 101) % 12

    def stone(x, y, z):
        h = hash3(x, y, z)
        c = STD if h == 0 else (STL if h == 1 else ST)
        if x < -4 and h in (2, 3):
            c = MOSS if h == 2 else MOSSD                        # mossy shaded side
        put(x, y, z, c)
    R0, R1 = 18.0, 22.5
    for x in range(-24, 25):                                     # pool wall + fat rim cap
        for z in range(-24, 25):
            r = math.hypot(x, z)
            if R0 <= r <= R1:
                for y in range(0, 8):
                    if y <= 1:
                        put(x, y, z, WET)
                    else:
                        stone(x, y, z)
            if R0 - 0.6 <= r <= R1 + 0.8:
                stone(x, 8, z)
                if hash3(x, 1, z) in (4, 5) and x < 2:
                    put(x, 8, z, MOSS)                           # moss creeping over the rim
            if r < R0:                                           # pool water
                c = WATL if int(r * 2) % 7 == 0 else WAT
                put(x, 6, z, c)
    for y in range(5, 18):                                       # pedestal column
        rr = 4.4 if y in (8, 16) else 3.8
        for x in range(-5, 6):
            for z in range(-5, 6):
                if math.hypot(x, z) <= rr:
                    stone(x, y, z) if y not in (8, 16) else put(x, y, z, STD)
    for y, ro in ((17, 6.0), (18, 8.5), (19, 10.5), (20, 12.0), (21, 13.0)):
        for x in range(-14, 15):                                 # lower basin dish shell
            for z in range(-14, 15):
                r = math.hypot(x, z)
                if ro - 2.0 <= r <= ro:
                    stone(x, y, z)
    for x in range(-14, 15):                                     # lower rim + water
        for z in range(-14, 15):
            r = math.hypot(x, z)
            if 10.6 <= r <= 13.2:
                stone(x, 22, z)
            elif r < 10.6:
                put(x, 21, z, WATL if int(r * 2) % 6 == 0 else WAT)
    for y in range(21, 31):                                      # upper column
        for x in range(-4, 5):
            for z in range(-4, 5):
                if math.hypot(x, z) <= (3.6 if y == 29 else 3.0):
                    stone(x, y, z)
    for y, ro in ((30, 4.0), (31, 6.0), (32, 7.5), (33, 8.5)):   # upper basin
        for x in range(-9, 10):
            for z in range(-9, 10):
                r = math.hypot(x, z)
                if ro - 1.8 <= r <= ro:
                    stone(x, y, z)
    for x in range(-9, 10):
        for z in range(-9, 10):
            r = math.hypot(x, z)
            if 6.2 <= r <= 8.6:
                stone(x, 34, z)
            elif r < 6.2:
                put(x, 33, z, WATL if int(r * 2) % 6 == 0 else WAT)
    ellip(0, 36.5, 0, 2.4, 2.8, 2.4, ST)                         # carved finial
    put(0, 39, 0, STL); put(0, 40, 0, STL)

    def spill(a_deg, r_start, y_top, r_land, y_land):            # a falling water rope
        ca, sa = math.cos(math.radians(a_deg)), math.sin(math.radians(a_deg))
        n = y_top - y_land
        for i in range(n + 1):
            t = i / float(n)
            rr = r_start + (r_land - r_start) * t
            x, z = ca * rr, sa * rr
            y = y_top - i
            c = FOAM if (i <= 1 or i == n or y % 3 == 0) else WATL
            put(int(round(x)), y, int(round(z)), c)              # 2-wide, so it READS
            put(int(round(x + abs(sa))), y, int(round(z + abs(ca))), WATL if c == FOAM else c,
                only_empty=True)
            if i == n:                                           # splash
                put(int(round(x)) + 1, y, int(round(z)), FOAM, only_empty=True)
                put(int(round(x)), y, int(round(z)) + 1, FOAM, only_empty=True)
    for a in (35, 155, 275):                                     # upper -> lower basin
        spill(a, 8.0, 33, 9.5, 21)
    for a in (95, 215, 335):                                     # lower basin -> pool
        spill(a, 12.8, 21, 15.5, 6)
    for x in range(-23, 24):                                     # ripple ring in the pool
        for z in range(-23, 24):
            r = math.hypot(x, z)
            if 16.2 <= r <= 17.1 and (x + z) % 3 == 0:
                put(x, 6, z, WATL)
    return V


# =================================================================================
# EMERALD LAKE — a great mossy boulder, ferns on top, glowing teal shrooms below
# =================================================================================
def build_emeraldrock():
    GR = (138, 138, 130); GRD = (106, 106, 100); GRL = (168, 168, 158); CRACK = (78, 78, 74)
    MOSS = (84, 124, 60); MOSSL = (114, 158, 80); MOSSD = (60, 98, 48)
    FERN = (74, 144, 66); FERNL = (112, 182, 88); FERND = (48, 108, 50)
    CAP = (60, 186, 172); CAPL = (150, 236, 220); CAPD = (40, 142, 132)
    STEM = (216, 208, 184); GILL = (46, 110, 104); WET = (72, 82, 84)
    V = {}
    put, ellip, box = _vox_helpers(V)
    ellip(-2, -4, 0, 25, 19, 16, GR)                             # the great dome
    ellip(15, -2, 5, 9, 9, 8, GR, only_empty=True)               # shoulder lump
    ellip(-19, -3, -5, 7, 6, 6, GR, only_empty=True)             # low shelf stone
    for (x, y, z) in list(V):
        if y < 0:
            del V[(x, y, z)]                                     # waterline cut
            continue
        h = (x * 73 + y * 31 + z * 151) % 11
        if h == 0:
            V[(x, y, z)] = GRD
        elif h == 1:
            V[(x, y, z)] = GRL
    tops = {}
    for (x, y, z) in V:
        tops[(x, z)] = max(y, tops.get((x, z), -99))
    rng = random.Random(77)
    cx, cz = -14, -8
    for _ in range(26):                                          # a meandering crack
        if (cx, cz) in tops:
            V[(cx, tops[(cx, cz)], cz)] = CRACK
        cx += 1
        cz += rng.randint(-1, 1)
    for (x, z), top in tops.items():                             # moss in PATCHES, not a pelt
        if top < 6:
            continue
        h = (x * 67 + z * 101) % 10
        blob = math.hypot(x + 8, z - 3) < 6.5 or math.hypot(x - 6, z + 5) < 5.0 \
            or math.hypot(x - 16, z - 6) < 4.0
        if blob and h < 8:
            V[(x, top, z)] = (MOSS, MOSSL, MOSSD, MOSS, MOSSL, MOSS, MOSSD, MOSS)[h]
        elif h == 0:
            V[(x, top, z)] = MOSSD                               # stray lichen flecks
    for (fx, fz, seed) in ((-8, 3, 5), (13, -1, 9)):             # fern clumps on top
        base = tops.get((fx, fz), 10)
        frng = random.Random(seed)
        for i in range(5):
            a = math.radians(i * 72 + frng.uniform(-14, 14))
            reach = frng.uniform(7.5, 10.5)
            for t in range(0, 12):
                tt = t / 11.0
                r = reach * tt
                y = base + 1 + 6.5 * math.sin(tt * 2.2) * (1 - 0.35 * tt)
                x = int(round(fx + r * math.cos(a)))
                z = int(round(fz + r * math.sin(a)))
                put(x, int(round(y)), z, FERND if t % 3 == 0 else FERNL)
                if t >= 3:
                    for s in (1, -1):
                        lx = int(round(x - math.sin(a) * s))
                        lz = int(round(z + math.cos(a) * s))
                        put(lx, int(round(y)), lz,
                            FERNL if (t + s) % 3 == 0 else FERN, only_empty=True)
    # BIG glowing shrooms along the waterline base (the front face)
    for (sx, sh, sr) in ((-8, 6, 4.4), (-1, 3, 2.8), (7, 8, 5.0), (14, 4, 2.6)):
        sz = 0
        for z in range(22, 4, -1):                               # find the rock face
            if (sx, 1, z) in V:
                sz = z + int(sr * 0.8)
                break
        for y in range(0, sh):
            put(sx, y, sz, STEM)
            if sr > 3.5:
                put(sx + 1, y, sz, STEM, only_empty=True)
        ellip(sx, sh + 0.6, sz, sr, sr * 0.62, sr, CAP)
        for (x, y, z) in list(V):
            if abs(x - sx) <= sr and abs(z - sz) <= sr and y == sh and V[(x, y, z)] == CAP:
                V[(x, y, z)] = GILL
        for (x, y, z) in list(V):
            if V[(x, y, z)] == CAP and (x * 47 + y * 13 + z * 89) % 5 == 0:
                V[(x, y, z)] = CAPL
        put(sx, sh + int(sr * 0.62) + 1, sz, CAPL, only_empty=True)
        put(sx - 1, 1, sz + int(sr), CAPD, only_empty=True)      # glow kissing the water
        for gy in range(sh, sh + 3):                             # teal glow ON the rock face
            if (sx, gy, sz - int(sr) - 1) in V:
                V[(sx, gy, sz - int(sr) - 1)] = CAPD
    for (x, y, z) in list(V):                                    # wet band on the granite
        if y <= 1 and V[(x, y, z)] in (GR, GRD, GRL, CRACK):
            V[(x, y, z)] = WET
    return V


# =================================================================================
# LAKE COCHICHEWICK — a loon on dark water, aurora-green reflection (flat, night)
# =================================================================================
def gen_loon():
    W, H = 138, 52
    WATERLINE = 31
    DK = (20, 24, 31, 255); DKL = (36, 42, 52, 255)
    RIM = (168, 196, 214, 255); NECK = (218, 228, 236, 255); CHK = (140, 156, 172, 255)
    EYE = (172, 44, 44, 255)
    AUR = (56, 196, 140, 255); AURL = (130, 240, 188, 255)
    AURD = (22, 116, 94, 255); ADEEP = (12, 70, 62, 255)

    # ---- layer 1: the aurora streak (LIGHT: gets no ink line) ----
    hi_a = Image.new("RGBA", (W * FS, H * FS), (0, 0, 0, 0))
    da = ImageDraw.Draw(hi_a)
    rng = random.Random(303)
    for x in range(5, W - 4):
        yc = WATERLINE + 4 + 2.2 * math.sin(x * 0.085)
        th = (1.0 + 4.2 * math.exp(-((x - 70) / 40.0) ** 2)) * \
             min(1.0, (x - 4) / 14.0, (W - 5 - x) / 14.0)
        da.line([(x * FS, (yc - th) * FS), (x * FS, (yc + th) * FS)], fill=AURD, width=FS)
        if th > 1.8:
            da.line([(x * FS, (yc - th * 0.55) * FS), (x * FS, (yc + th * 0.55) * FS)],
                    fill=AUR, width=FS)
        if th > 3.4:
            da.line([(x * FS, (yc - th * 0.22) * FS), (x * FS, (yc + th * 0.22) * FS)],
                    fill=AURL, width=FS)
    for i in range(14):                                          # shimmer dashes below
        x = 10 + i * 9 + rng.randint(-2, 2)
        yc = WATERLINE + 6 + 2.2 * math.sin(x * 0.085)
        ln = rng.uniform(2, 5)
        da.line([(x * FS, (yc + 2) * FS), (x * FS, (yc + 2 + ln) * FS)],
                fill=AURD if i % 2 else AUR, width=FS)
    for (sx, sy) in ((28, 34), (52, 39), (88, 40), (112, 35), (70, 43)):
        da.rectangle([sx * FS, sy * FS, (sx + 1) * FS - 1, (sy + 1) * FS - 1], fill=AURL)
    # the loon's own dark reflection, swallowed by the streak
    da.ellipse([46 * FS, 32 * FS, 98 * FS, 41 * FS], fill=ADEEP)
    da.ellipse([36 * FS, 32 * FS, 52 * FS, 37 * FS], fill=ADEEP)
    da.arc([34 * FS, 26 * FS, 106 * FS, 40 * FS], 15, 165, fill=AURD, width=FS)  # ripple

    # ---- layer 2: the loon (a THING: crisp + ink outline) ----
    hi_l = Image.new("RGBA", (W * FS, H * FS), (0, 0, 0, 0))
    dl = ImageDraw.Draw(hi_l)
    dl.ellipse([46 * FS, 19 * FS, 100 * FS, 32 * FS], fill=DK)   # low sleek body
    dl.polygon([(94 * FS, 24 * FS), (107 * FS, 19 * FS), (97 * FS, 29 * FS)], fill=DK)  # tail
    for (nx, ny, r) in ((54, 25, 4.4), (50.5, 20, 3.9), (48, 15, 3.5), (47, 11, 3.3)):
        dl.ellipse([(nx - r) * FS, (ny - r) * FS, (nx + r) * FS, (ny + r) * FS], fill=DK)
    dl.ellipse([38 * FS, 5 * FS, 53 * FS, 14 * FS], fill=DK)     # head
    dl.polygon([(41 * FS, 7.4 * FS), (25 * FS, 7.8 * FS), (41 * FS, 11.4 * FS)], fill=DKL)  # bill
    px = hi_l.load()
    for y in range(H * FS):                                      # hard waterline cut
        if y >= (WATERLINE + 1) * FS:
            for x in range(W * FS):
                px[x, y] = (0, 0, 0, 0)
    dl = ImageDraw.Draw(hi_l)
    dl.arc([46 * FS, 19 * FS, 100 * FS, 34 * FS], 195, 320, fill=RIM, width=FS)  # moonlit back
    dl.arc([38 * FS, 5 * FS, 53 * FS, 15 * FS], 175, 320, fill=RIM, width=FS)    # moonlit crown
    for i in range(3):                                           # the white necklace
        dl.rectangle([(44 + i * 2.6) * FS, (14 + i * 1.2) * FS,
                      (45 + i * 2.6) * FS, (17.4 + i * 1.2) * FS], fill=NECK)
    for row, y0 in ((0, 22.0), (1, 24.6)):                       # back checker rows: fine dots
        for k in range(6):
            x0 = 58 + k * 6.5 + (3 if row else 0)
            dl.rectangle([x0 * FS, y0 * FS, (x0 + 1.1) * FS, (y0 + 0.9) * FS], fill=CHK)
    dl.rectangle([44 * FS, 8 * FS, 45.6 * FS, 9.4 * FS], fill=EYE)   # the red eye

    streak = _crisp(hi_a, W, H)                                  # light: NO outline
    loon = _outline(_crisp(hi_l, W, H))                          # thing: ink outline
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.paste(streak, (0, 0), streak)
    out.paste(loon, (0, 0), loon)
    bb = out.getbbox()
    save(out.crop(bb) if bb else out, "hero_cochichewick.png")


# =================================================================================
# generate + contact sheet
# =================================================================================
def build_turtlelog():
    """PLEASANT POND: the classic — a half-sunken log with painted turtles stacked
    on it, sunning. Nothing says New England pond like a turtle traffic jam."""
    LOG = (116, 84, 52); LOGD = (86, 60, 38); LOGL = (142, 108, 68); WET = (72, 82, 84)
    SHELL = (52, 74, 40); SHELLD = (36, 54, 30); SHELLL = (88, 112, 58)
    SKIN = (146, 158, 74); STRIPE = (210, 74, 52); EYE = (24, 20, 18)
    V = {}
    put, ellip, box = _vox_helpers(V)
    for zi in range(-22, 23):                      # the log, gently arched out of the water
        t = (zi + 22) / 44.0
        lift = int(round(5.0 * math.sin(t * math.pi)))
        r = 4.6 - 1.2 * abs(zi) / 22.0
        ellip(0, lift, zi, r, r, 1.0, LOGD if zi % 7 == 0 else LOG)
        if lift > 2:
            put(0, lift + int(r), zi, LOGL, only_empty=True)
    for (x, y, z) in list(V):
        if y < 0:
            V[(x, y, z)] = WET if y > -2 else V[(x, y, z)]
        if y < -1:
            del V[(x, y, z)]
    def turtle(cz, big):
        base = 6 + int(round(4.6 * math.sin((cz + 22) / 44.0 * math.pi)))
        r = 4.6 if big else 3.4
        ellip(0, base + 2, cz, r, r * 0.7, r, SHELL)              # dome, clearly ON TOP of the log
        ellip(0, base + 2 + r * 0.45, cz - 0.5, r * 0.55, r * 0.3, r * 0.55, SHELLL)  # sun-hit crown
        ellip(0, base + 1, cz, r * 1.05, r * 0.2, r * 1.05, SHELLD)   # dark shell rim
        hz = cz + int(r) + 2
        for i in range(3):                                        # neck stretched UP toward the sun
            ellip(0, base + 2 + i, hz + (1 if i > 0 else 0), 1.2, 1.0, 1.3, SKIN)
        put(1, base + 5, hz + 1, EYE)
        put(-1, base + 5, hz + 1, EYE)
        put(1, base + 4, hz + 1, STRIPE)                          # the red ear dash
        put(-1, base + 4, hz + 1, STRIPE)
    turtle(-14, True)
    turtle(0, True)
    turtle(12, False)                                             # the smol one bringing up the rear
    return V


def build_rootball():
    """SAND POND: a weathered driftwood ROOT-BALL beached on a little sandbar,
    the gull moved over from the buoy — wild flotsam, not harbor furniture."""
    WOOD = (150, 128, 96); WOODD = (112, 92, 66); WOODL = (184, 162, 122)
    SAND = (216, 190, 138); SANDD = (188, 160, 112); GRASS = (150, 158, 88)
    GULLW = (238, 238, 232); GULLG = (170, 176, 180); BEAK = (226, 168, 54); EYE = (24, 20, 18)
    V = {}
    put, ellip, box = _vox_helpers(V)
    ellip(0, -2, 0, 20, 5, 14, SAND)                              # the sandbar dome
    ellip(-6, -1, 2, 10, 4, 8, SANDD, only_empty=True)
    for (gx, gz) in ((-16, -6), (14, 8), (12, -9)):               # dune grass tufts
        for i in range(4):
            put(gx + (i % 2), 2 + i, gz, GRASS)
    ellip(2, 3, -1, 7, 6, 6, WOOD)                                # the root-ball heart
    for (dx, dy, dz) in ((14, 9, -4), (11, 12, 6), (-9, 13, 2), (-13, 7, -7), (6, 15, -8), (-4, 10, 10)):
        _limb3(V, (2, 3, -1), ((2 + dx) // 2, (3 + dy) // 2 + 2, (-1 + dz) // 2),
               (2 + dx, 3 + dy, -1 + dz), 2.0, 0.55, WOOD)
    for (x, y, z) in list(V):
        if V[(x, y, z)] == WOOD and (x * 7 + y * 3 + z * 11) % 6 == 0:
            V[(x, y, z)] = WOODD
        elif V[(x, y, z)] == WOOD and y > 8 and (x + z) % 5 == 0:
            V[(x, y, z)] = WOODL                                  # sun-bleached tips
    gx, gy, gz = -9, 14, 2                                        # the gull claims the high root
    ellip(gx, gy + 1, gz, 2.2, 1.8, 2.8, GULLW)
    ellip(gx, gy + 1.6, gz - 0.5, 1.8, 1.0, 2.0, GULLG, only_empty=True)
    ellip(gx, gy + 3.2, gz + 2.2, 1.2, 1.2, 1.2, GULLW)           # head
    put(gx, gy + 3, gz + 4, BEAK)
    put(gx + 1, gy + 4, gz + 3, EYE)
    put(gx - 1, gy + 4, gz + 3, EYE)
    return V


# =================================================================================
# BUKER POND — the boat launch where every trip starts (seen from the water)
# =================================================================================
def build_launch():
    """Gravel/concrete ramp sloping into the shallows, worn tire ruts, a little
    aluminum skiff tied off to a wooden post at the ramp's edge."""
    CONC = (170, 164, 152); CONCD = (138, 132, 122); CONCL = (196, 190, 178)
    GRAV = (152, 142, 124); RUT = (98, 92, 82); RUTD = (76, 72, 64)
    ALGAE = (104, 122, 96); WET = (84, 90, 92)
    ALU = (182, 188, 192); ALUD = (136, 144, 150); ALUL = (220, 226, 230)
    AFLOOR = (150, 156, 160); SEAT = (206, 212, 214)
    POST = (128, 104, 74); POSTD = (96, 76, 54)
    ROPE = (212, 192, 150); ROPED = (176, 156, 118)
    V = {}
    put, ellip, box = _vox_helpers(V)
    # THE RAMP: a broad slab running down into the water (+z = up the bank)
    for zi in range(-6, 20):
        yt = max(0, int(round((zi + 6) * 0.42 - 1.0)))
        for x in range(-11, 12):
            for y in range(max(0, yt - 2), yt + 1):
                h = (x * 43 + y * 7 + zi * 29) % 13
                c = CONC
                if h in (0, 1):
                    c = GRAV                                   # gravel worked into the pour
                elif h == 2:
                    c = CONCD
                elif h == 3:
                    c = CONCL
                if abs(x) >= 10:
                    c = CONCD                                  # cast edge
                if y == yt and abs(abs(x) - 5) <= 1:           # worn tire ruts: CONTINUOUS
                    c = RUTD if abs(x) == 5 else RUT
                if yt <= 1:
                    c = WET                                    # slab slipping under water
                elif yt <= 4 and h in (4, 5) and abs(abs(x) - 5) > 1:
                    c = ALGAE                                  # slick green at the waterline
                put(x, y, zi, c)
        if zi in (5, 13) and yt > 1:                           # expansion seams
            for x in range(-9, 10):
                if abs(abs(x) - 5) > 1:
                    put(x, yt, zi, CONCD)
    # the wooden mooring post at the ramp's water corner, rope-wrapped
    for y in range(0, 11):
        put(-14, y, 2, WET if y <= 1 else (POST if y % 3 else POSTD))
        put(-13, y, 2, WET if y <= 1 else POSTD, only_empty=True)
    put(-14, 11, 2, POSTD)
    put(-15, 8, 2, ROPE); put(-13, 8, 2, ROPE)                 # the wrap
    put(-14, 8, 3, ROPE); put(-14, 8, 1, ROPED)
    # the aluminum skiff, nosed up beside the ramp foot, waiting
    SX, SZ, SL = -21, -6, 9

    def sk_halfw(t):
        if t <= 0.5:
            return 3.2 + 1.2 * math.sin(t / 0.5 * math.pi / 2.0)
        u = (t - 0.5) / 0.5
        return max(0.7, 4.4 * math.cos(u * math.pi / 2.0) ** 0.8)
    for dz in range(-SL, SL + 1):
        t = (dz + SL) / (2.0 * SL)
        w = sk_halfw(t)
        yk = int(round(1.8 * max(0.0, (t - 0.7) / 0.3) ** 1.5))
        for y in range(yk, yk + 5):
            frac = (y - yk) / 4.0
            xs = int(round(w * (0.35 + 0.65 * frac ** 0.7)))
            c = ALU if (y - yk) % 2 else ALUD                  # dull riveted strakes
            if y == yk + 4:
                c = ALUL                                       # bright gunwale rail
            if y == 0:
                c = WET
            put(SX + xs, y, SZ + dz, c); put(SX - xs, y, SZ + dz, c)
            if y == yk:
                for x in range(-xs, xs + 1):
                    put(SX + x, y, SZ + dz, WET if y == 0 else ALUD, only_empty=True)
            if y == yk + 1 and abs(dz) < SL - 1:
                for x in range(-max(0, xs - 1), max(0, xs - 1) + 1):
                    put(SX + x, y, SZ + dz, AFLOOR, only_empty=True)
    for y in range(0, 4):                                      # flat transom
        for x in range(-3, 4):
            put(SX + x, y, SZ - SL, WET if y == 0 else ALUD, only_empty=True)
    for dz0 in (-4, 3):                                        # two bench seats
        for dz in (dz0, dz0 + 1):
            t = (dz + SL) / (2.0 * SL)
            xs = max(1, int(round(sk_halfw(t))) - 1)
            for x in range(-xs, xs + 1):
                put(SX + x, 3, SZ + dz, ALUD if x in (-xs, xs) else SEAT)
    # the bow line, sagging from the post down to the skiff's bow
    for i in range(11):
        t = i / 10.0
        x = -14 + (SX + 1 - -14) * t
        y = 8 + (5 - 8) * t - 2.4 * math.sin(t * math.pi)
        z = 2 + (SZ + SL - 2) * t
        put(int(round(x)), int(round(y)), int(round(z)), ROPE if i % 2 else ROPED)
        put(int(round(x)), int(round(y)) + 1, int(round(z)), ROPED, only_empty=True)
    return V


# =================================================================================
# SAND POND — the camp pontoon boat, moored just off the beach, loved + sun-faded
# =================================================================================
def build_pontoon():
    """Two silver tubes, a railed plank deck, two faded deck chairs, a little
    outboard on the stern, a beach towel drying over the rail."""
    PON = (186, 192, 198); POND = (142, 150, 158); PONL = (226, 232, 236)
    DECK = (200, 176, 136); DECKD = (166, 142, 104); DECKL = (222, 200, 158)
    RAIL = (228, 228, 220); RAILD = (184, 184, 176)
    CH1 = (104, 156, 172); CH1D = (76, 122, 138)               # faded blue chair
    CH2 = (216, 152, 98); CH2D = (176, 114, 66)                # faded orange chair
    MOT = (72, 76, 84); MOTL = (116, 122, 130); PULL = (206, 202, 192)
    TOW = (234, 152, 124); TOWL = (246, 226, 188)              # striped beach towel
    WET = (96, 102, 104)
    V = {}
    put, ellip, box = _vox_helpers(V)
    for px in (-7, 7):                                         # the two pontoon tubes
        for zi in range(-14, 14):
            yc, r = 1.2, 2.8
            if zi > 8:
                yc += (zi - 8) * 0.45                          # upswept nose cones
                r = max(1.1, 2.8 - (zi - 8) * 0.30)
            ellip(px, yc, zi, r, r, 0.9, PON, only_empty=True)
    for (x, y, z) in list(V):                                  # tube shading + waterline
        if y < 0:
            del V[(x, y, z)]
            continue
        if y >= 3 and z <= 9:
            V[(x, y, z)] = PONL                                # sun on top of the tubes
        elif y <= 1:
            V[(x, y, z)] = WET if y == 0 else POND
        if (x * 29 + z * 13) % 17 == 0 and 1 < y < 3:
            V[(x, y, z)] = POND                                # dull riveted seams
    for x in range(-8, 9):                                     # plank deck on cross-members
        for zi in range(-13, 12):                              # (tubes poke out both sides)
            put(x, 5, zi, DECKD)
            c = (DECK, DECKL, DECK, DECKD)[((x + 8) // 3) % 4]
            if (x + 8) % 3 == 0:
                c = DECKD                                      # plank seams run fore-aft
            if (x * 7 + zi * 13) % 19 == 0:
                c = DECKD                                      # sun-faded wear
            put(x, 6, zi, c)
    for x in range(-8, 9):                                     # rail round the deck (stern open)
        for zi in range(-13, 12):
            edge = x in (-8, 8) or zi == 11
            if not edge:
                continue
            put(x, 10, zi, RAIL)                               # top rail
            if (x + zi) % 4 == 0:                              # stanchion posts
                for y in range(7, 10):
                    put(x, y, zi, RAILD)
    # the beach towel over the starboard rail, stripes sun-faded
    for zi in range(2, 8):
        c0 = TOW if zi % 2 else TOWL
        put(8, 10, zi, c0)
        for y in range(7, 10):                                 # hanging outside
            put(9, y, zi, c0 if (y + zi) % 2 else (TOWL if c0 == TOW else TOW))
        put(7, 9, zi, c0)                                      # tucked inside
    # two deck chairs midship, angled at nothing in particular

    def chair(cx, cz, C, CD):
        for x in range(cx - 1, cx + 2):
            for zi in range(cz, cz + 3):
                put(x, 8, zi, C if (x + zi) % 2 else CD)       # webbed seat
            for y in range(9, 13):                             # reclined back
                put(x, y, cz - 1 - (1 if y >= 11 else 0), C if (x + y) % 2 else CD)
        for (lx, lz) in ((cx - 1, cz), (cx + 1, cz), (cx - 1, cz + 2), (cx + 1, cz + 2)):
            put(lx, 7, lz, RAILD)                              # legs
    chair(-4, -1, CH1, CH1D)
    chair(3, -4, CH2, CH2D)
    # the little outboard, tipped on the stern
    box(-2, 2, 6, 8, -15, -14, MOT)
    box(-1, 1, 9, 9, -15, -14, MOTL)                           # cowl top
    put(0, 8, -13, PULL)                                       # pull-start handle
    for y in range(1, 6):
        put(0, y, -15, MOT if y > 1 else WET)                  # lower unit into the water
    put(1, 1, -16, MOT); put(-1, 1, -16, MOT)                  # prop hint at the waterline
    return V


# =================================================================================
# PLEASANT POND — the anchored skiff, fishing all by itself, patiently
# =================================================================================
def build_skiff():
    """Small rowboat at anchor: visible anchor line into the water, one rod
    arcing over the side with a dashed line to a red/white bobber, tackle box
    on the thwart. Nobody aboard."""
    HULL = (146, 118, 84); HULLD = (110, 86, 62); HULLL = (178, 150, 112)
    PAINT = (86, 124, 96)                                      # spruce-green sheer stripe
    FLOOR = (96, 76, 54); RIB = (72, 56, 40)
    SEAT = (200, 174, 132); SEATD = (162, 138, 100)
    WET = (66, 68, 60)
    ROD = (122, 84, 48); RODL = (164, 120, 74); REEL = (60, 64, 72)
    LINE = (216, 224, 228); BOB = (222, 56, 46); BOBW = (240, 236, 228)
    ANCH = (120, 112, 94); ANCHD = (90, 84, 70); RIP = (150, 176, 184)
    TBOX = (58, 116, 96); TBOXL = (96, 156, 132); LATCH = (214, 210, 200)
    V = {}
    put, ellip, box = _vox_helpers(V)
    L = 13

    def halfw(t):                                              # transom -> waist -> stem
        if t <= 0.55:
            return 3.8 + 1.6 * math.sin(t / 0.55 * math.pi / 2.0)
        u = (t - 0.55) / 0.45
        return max(0.8, 5.4 * math.cos(u * math.pi / 2.0) ** 0.8)
    for zi in range(-L, L + 1):
        t = (zi + L) / (2.0 * L)
        w = halfw(t)
        yk = int(round(2.5 * max(0.0, (t - 0.72) / 0.28) ** 1.6))
        ytop = yk + 6 + int(round(1.5 * max(0.0, (t - 0.70) / 0.30)))
        for y in range(yk, ytop + 1):
            frac = (y - yk) / max(1.0, float(ytop - yk))
            xs = int(round(w * (0.32 + 0.68 * frac ** 0.65)))
            lap = HULLL if (y - yk) % 2 else HULL              # lapstrake planks
            if (zi * 13 + y * 29) % 29 == 0:
                lap = HULLD                                    # only the odd weathered patch
            c = PAINT if y == ytop else lap                    # green sheer stripe
            if y == 0:
                c = WET                                        # floating: one wet strake
            put(xs, y, zi, c); put(-xs, y, zi, c)
            if y == yk:
                for x in range(-xs, xs + 1):
                    put(x, y, zi, WET if y == 0 else HULLD, only_empty=True)
            if y == yk + 1 and abs(zi) < L - 1:
                for x in range(-max(0, xs - 1), max(0, xs - 1) + 1):
                    put(x, y, zi, RIB if zi % 5 == 0 else FLOOR, only_empty=True)
    for y in range(0, 8):                                      # transom
        for x in range(-3, 4):
            put(x, y, -L, PAINT if y >= 6 else (WET if y == 0 else HULLD),
                only_empty=True)
    for z0 in (-6, 5):                                         # two thwart seats
        for zi in (z0, z0 + 1):
            t = (zi + L) / (2.0 * L)
            xs = int(round(halfw(t))) - 1
            for x in range(-xs, xs + 1):
                put(x, 4, zi, SEATD if x in (-xs, xs) else SEAT)
    # the tackle box, sitting on the forward thwart like somebody just stepped off
    box(-3, 0, 5, 6, 5, 6, TBOX)
    for x in range(-3, 1):
        for zi in (5, 6):
            put(x, 7, zi, TBOXL if (x + zi) % 2 else TBOX)     # ridged lid
    put(-1, 6, 7, LATCH)                                       # the latch
    # the rod, propped on the gunwale, arcing out over the starboard side
    _limb3(V, (-2, 5, -5), (7, 12, -4), (13, 9, -3), 0.7, 0.35, ROD)
    for (x, y, z) in list(V):
        if V[(x, y, z)] == ROD and (x + y + z) % 4 == 0:
            V[(x, y, z)] = RODL                                # cane wraps
    ellip(-1, 6.2, -5, 1.2, 1.2, 1.0, REEL)                    # the reel at the butt
    for y in range(3, 9):                                      # dashed line straight down
        if y % 2:
            put(13, y, -3, LINE, only_empty=True)
    put(13, 2, -3, BOB); put(13, 1, -3, BOBW)                  # red over white bobber
    put(14, 1, -2, RIP); put(12, 1, -4, RIP)                   # its little ripple
    # the anchor line, off the bow down into the water, dashed + taut-ish
    put(0, 9, L, ANCHD)                                        # bow cleat
    for i in range(10):
        t = i / 9.0
        y = int(round(8 - 7 * t))
        z = int(round(L + 1 + 6 * t))
        if i % 2 == 0:
            put(0, y, z, ANCH if i % 4 == 0 else ANCHD)
    put(1, 1, L + 7, RIP); put(-1, 1, L + 6, RIP)              # where it slips under
    return V


# =================================================================================
# BANK PROPS — Sand Pond camp bonfire, the barred owl, Lizzie the beagle
# =================================================================================
def vox_glow(V_solid, V_glow, yaw, pitch, target):
    """Two-layer vox(): the solid model gets shade + ink outline as usual; the
    glow layer renders emissive with NO outline (the fire precedent) and is
    composited on top. Both share one center/scale so they register."""
    allk = list(V_solid) + list(V_glow)
    xs = [k[0] for k in allk]; ys = [k[1] for k in allk]; zs = [k[2] for k in allk]
    cx = (min(xs) + max(xs)) // 2
    cy = (min(ys) + max(ys)) // 2
    cz = (min(zs) + max(zs)) // 2
    Vs = {(x - cx, y - cy, z - cz): c for (x, y, z), c in V_solid.items()}
    Vg = {(x - cx, y - cy, z - cz): c for (x, y, z), c in V_glow.items()}
    SH = shade(Vs)
    comb = dict(SH)
    comb.update(Vg)
    trial = render(comb, math.radians(yaw), math.radians(pitch), out=320, scale=1.2)
    bb = trial.getbbox()
    cur = max(bb[2] - bb[0], bb[3] - bb[1])
    sc = 1.2 * (target / float(cur))
    out = int(target * 1.7) + 14
    base = render(SH, math.radians(yaw), math.radians(pitch), out=out, scale=sc)
    glow = render(Vg, math.radians(yaw), math.radians(pitch), out=out, scale=sc,
                  outline=False)
    im = Image.new("RGBA", (out, out), (0, 0, 0, 0))
    im.paste(base, (0, 0), base)
    im.paste(glow, (0, 0), glow)
    return im.crop(im.getbbox())


def build_bonfire():
    """The camp fire ring: fieldstones, crossed logs charred in the middle,
    an ash bed. (The flames live in build_bonfire_glow.)"""
    STONE = (146, 142, 134); STONED = (112, 110, 104); STONEL = (176, 172, 162)
    LOG = (122, 92, 58); LOGD = (90, 66, 42); CHAR = (52, 46, 44)
    ASH = (168, 160, 150); ASHD = (134, 128, 120)
    V = {}
    put, ellip, box = _vox_helpers(V)
    for i in range(9):                                         # the stone ring
        a = math.radians(i * 40 + (i * 37) % 13)
        sr = 1.7 + ((i * 5) % 3) * 0.35
        ellip(7.2 * math.cos(a), sr * 0.55, 7.2 * math.sin(a), sr, sr * 0.85, sr, STONE)
    for (x, y, z) in list(V):
        if y < 0:
            del V[(x, y, z)]
            continue
        h = (x * 61 + y * 17 + z * 43) % 9
        if h == 0:
            V[(x, y, z)] = STONED
        elif h == 1:
            V[(x, y, z)] = STONEL
    for x in range(-5, 6):                                     # ash + ember bed
        for z in range(-5, 6):
            if math.hypot(x, z) <= 4.6:
                put(x, 0, z, ASH if (x * 31 + z * 17) % 5 else ASHD, only_empty=True)
    for a_deg in (15, 100, 205, 300):                          # crossed logs leaning in
        ca, sa = math.cos(math.radians(a_deg)), math.sin(math.radians(a_deg))
        _limb3(V, (ca * 7.0, 1.2, sa * 7.0), (ca * 4.0, 3.0, sa * 4.0),
               (ca * 0.6, 4.2, sa * 0.6), 1.35, 0.9, LOG)
    for (x, y, z) in list(V):
        if V[(x, y, z)] == LOG:
            if math.hypot(x, z) < 3.2:
                V[(x, y, z)] = CHAR                            # charred where they meet
            elif (x * 7 + y * 3 + z * 11) % 5 == 0:
                V[(x, y, z)] = LOGD
    return V


def build_bonfire_glow():
    """Emissive layer: flame licks + ember glow + a few climbing sparks."""
    CORE = (255, 240, 170); MID = (255, 186, 64); OUT = (238, 116, 38)
    EMB = (255, 148, 58)
    V = {}
    put, ellip, box = _vox_helpers(V)
    for (fx, fz, h, r0) in ((0, 0, 8, 2.7), (-2, 2, 6, 1.8), (2, -2, 5, 1.5)):
        for y in range(2, 2 + h):                              # tapering flame licks
            t = (y - 2) / float(h)
            rr = r0 * (1 - t) ** 0.8
            wob = int(round(0.9 * math.sin(y * 1.7 + fx)))
            for x in range(-3, 4):
                for z in range(-3, 4):
                    if math.hypot(x - wob * 0.4, z) <= rr:
                        d = math.hypot(x, z) / max(rr, 0.5)
                        c = CORE if (t < 0.45 and d < 0.55) else (MID if d < 0.85 else OUT)
                        put(fx + x + (wob if t > 0.5 else 0), y, fz + z, c)
    for x in range(-4, 5):                                     # ember glow in the bed
        for z in range(-4, 5):
            if math.hypot(x, z) <= 3.6 and (x * 31 + z * 17) % 3:
                put(x, 1, z, EMB if (x + z) % 2 else MID, only_empty=True)
    for (sx, sy, sz) in ((3, 11, 1), (-3, 12, -1), (1, 13, 2)):
        put(sx, sy, sz, MID if sy % 2 else CORE)               # climbing sparks
    return V


def build_barredowl():
    """The barred owl at dusk: round head, NO ear tufts, dark soulful eyes in a
    pale facial disc, barred chest over a streak-bellied front, on a bare stub."""
    BR = (140, 118, 94); BRD = (102, 84, 66); BRL = (170, 150, 122)
    CRM = (240, 232, 212); CRMD = (206, 196, 174)
    STRK = (128, 100, 70)
    EYE = (26, 22, 20); BEAK = (212, 184, 104)
    BARK = (98, 82, 66); BARKD = (72, 60, 48); BARKL = (126, 108, 88)
    TAL = (176, 158, 108)
    V = {}
    put, ellip, box = _vox_helpers(V)
    _limb3(V, (-9, 0, -2), (-2, 1.6, 0), (6, 3, 1), 1.7, 1.1, BARK)  # the bare branch stub
    put(7, 3, 1, BARKD); put(-10, 0, -2, BARKD)                # snapped ends
    for (x, y, z) in list(V):
        h = (x * 47 + y * 13 + z * 71) % 7
        if h == 0:
            V[(x, y, z)] = BARKD
        elif h == 1 and y > 1:
            V[(x, y, z)] = BARKL
    ellip(0, 10, 0, 4.3, 6.0, 3.8, BR)                         # egg body
    ellip(0, 18.3, 0.6, 3.9, 3.5, 3.5, BR)                     # ROUND head — no tufts
    box(-2, 2, 3, 6, -5, -4, BRD)                              # short tail down the back
    put(-1, 3, -5, CRMD); put(1, 4, -5, CRMD); put(0, 5, -5, CRMD)  # tail bands
    for (x, y, z) in list(V):                                  # folded wings: dark panels
        if V[(x, y, z)] == BR and abs(x) >= 3 and z <= 1 and 5 <= y <= 13:
            V[(x, y, z)] = CRMD if (y % 3 == 0 and (x + z) % 2) else BRD
    for (x, y, z) in list(V):                                  # white-spangled brown back
        if V[(x, y, z)] == BR and z < 0 and (x * 31 + y * 17 + z * 11) % 7 == 0:
            V[(x, y, z)] = CRMD if y % 2 else BRD
    for (x, y, z) in list(V):                                  # VERTICAL belly streaks:
        if V[(x, y, z)] == BR and z >= 1 and 4 <= y <= 13:     # soft brown over cream
            V[(x, y, z)] = STRK if x % 2 == 0 else CRM
    for (x, y, z) in list(V):                                  # barred collar under the face
        if V[(x, y, z)] == BR and z >= 1 and 13 < y <= 15:
            V[(x, y, z)] = CRMD if y % 2 else BRD
    for s in (1, -1):                                          # pale facial disc halves
        ellip(s * 1.8, 18.5, 3.3, 2.0, 2.3, 1.2, CRM)
        put(s * 3, 19, 3, BRD); put(s * 3, 18, 3, BRD)         # dark disc rim
        put(s * 3, 20, 3, BRD); put(s * 2, 21, 3, BRD)
        put(s * 2, 18, 5, EYE); put(s * 2, 19, 5, EYE)         # the dark soulful eyes,
        put(s * 2, 18, 4, EYE); put(s * 2, 19, 4, EYE)         # proud of the disc
    put(0, 18, 4, BEAK); put(0, 17, 5, BEAK)                   # small hooked bill
    put(0, 20, 4, CRMD)                                        # pale forehead V
    put(1, 4, 2, TAL); put(-1, 4, 2, TAL); put(0, 4, 3, TAL)   # toes gripping the stub
    return V


def build_lizzie():
    """LIZZIE THE BEAGLE, sitting on the bank watching the water like a very
    good girl: black saddle, brown head + long ears, white chest/paws/tail tip."""
    WHT = (238, 234, 224); WHTD = (206, 202, 192)
    TAN = (176, 120, 62); TAND = (140, 92, 48); TANL = (202, 152, 92)
    BLK = (58, 56, 60); BLKL = (88, 86, 92)
    NOSE = (26, 24, 26); EYE = (36, 28, 22)
    V = {}
    put, ellip, box = _vox_helpers(V)
    ellip(0, 3.6, -3.5, 4.4, 3.8, 4.6, WHT)                    # haunches planted (+z = water)
    ellip(0, 7.5, -1.0, 3.6, 4.6, 3.8, WHT)                    # torso rising
    ellip(0, 10.5, 0.8, 3.0, 3.0, 3.0, WHT, only_empty=True)   # chest + shoulders
    for (x, y, z) in list(V):
        if y < 0:
            del V[(x, y, z)]
    for (x, y, z) in list(V):                                  # the BLACK SADDLE over the back
        if V[(x, y, z)] == WHT and z <= 2 and y >= 5.5 + 0.45 * z:
            V[(x, y, z)] = BLK if (x * 31 + y * 7 + z * 13) % 5 else BLKL
    for (x, y, z) in list(V):                                  # tan bleeding out of the saddle
        if V[(x, y, z)] == WHT and -5 <= z <= 2 and 4.0 + 0.45 * z <= y < 5.5 + 0.45 * z:
            V[(x, y, z)] = TAN if (x + z) % 2 else TANL
    for (x, y, z) in list(V):                                  # soft white shading below
        if V[(x, y, z)] == WHT and y <= 2:
            V[(x, y, z)] = WHTD
    for s in (1, -1):
        box(s * 3, s * 3, 0, 1, -1, 2, WHT)                    # hind feet tucked forward
        put(s * 3, 0, 3, WHTD)
        for y in range(0, 9):                                  # straight proud front legs
            put(s * 2, y, 3, WHT)
            put(s * 1, y, 3, WHT, only_empty=True)
        put(s * 2, 0, 4, WHT); put(s * 2, 0, 5, WHTD)          # front paws
    ellip(0, 15.2, 2.5, 2.9, 2.7, 2.9, TAN)                    # brown head, up + watching
    for (x, y, z) in list(V):                                  # crown shading
        if V[(x, y, z)] == TAN and y >= 17 and (x * 13 + z * 7) % 5 == 0:
            V[(x, y, z)] = TAND
    box(-1, 1, 13, 14, 5, 7, WHT)                              # muzzle
    put(0, 14, 8, NOSE); put(0, 13, 8, NOSE)                   # the nose
    put(0, 15, 5, WHT); put(0, 16, 5, WHT); put(0, 17, 4, WHT)  # white blaze up the face
    for s in (1, -1):
        put(s * 2, 16, 5, EYE)                                 # kind brown eyes
        box(s * 4, s * 4, 10, 16, 1, 3, TAND)                  # LONG hanging ears
        put(s * 4, 9, 2, TAND); put(s * 4, 9, 3, TAND)         # rounded ear tips
        put(s * 4, 16, 2, TAN)                                 # lit ear top
        put(s * 3, 17, 3, TAN, only_empty=True)                # ear roots on the crown
    TAILP = ((4, -7, BLK), (5, -8, BLK), (7, -9, TAND), (9, -9, WHT), (11, -8, WHT))
    for i, (ty, tz, tc) in enumerate(TAILP):                   # tail up like a flag
        put(0, ty, tz, tc)
        put(0, ty + 1, tz, tc if i >= 3 else BLKL, only_empty=True)
    return V


HEROES = [
    ("hero_buker.png",        build_launch,     dict(yaw=206, pitch=46, target=116)),
    ("hero_woodbury.png",     build_turtlelog,  dict(yaw=26, pitch=40, target=108)),
    ("hero_purgatory.png",    build_dreadtree,  dict(yaw=18, pitch=30, target=126)),
    ("hero_sand.png",         build_pontoon,    dict(yaw=246, pitch=40, target=110)),
    ("hero_pleasant.png",     build_skiff,      dict(yaw=30, pitch=42, target=100)),
    ("hero_emerald.png",      build_emeraldrock, dict(yaw=15, pitch=40, target=106)),
]

def build_jetski(alt=False):
    """WOODBURY: a jetski parked at a little float — big-water toys, nosed up and ready."""
    HULL = (206, 60, 44) if not alt else (44, 150, 172)
    HULLD = (158, 40, 30) if not alt else (30, 110, 128)
    HULLL = (235, 96, 74) if not alt else (86, 196, 214)
    SEAT = (40, 38, 42); SEATL = (66, 64, 70)
    BAR = (32, 32, 36); GRIP = (200, 200, 204)
    POST = (108, 82, 54); ROPE = (196, 178, 140)
    WET = (72, 82, 84); FOAM = (168, 196, 204)
    V = {}
    put, ellip, box = _vox_helpers(V)
    # it FLOATS (jetskis don't sit on docks): hull in the water, wet lap at the waterline,
    # a rope back to a mooring post on shore
    for yy in range(0, 6):                               # the mooring post
        put(-8, yy, -6, POST)
    put(-8, 6, -6, (84, 62, 40))
    for i in range(6):                                   # sagging rope to the bow
        put(-7 + i, max(1, 4 - int(round(1.6 * math.sin(i / 5.0 * math.pi)))), -6 + i, ROPE)
    for zi in range(-8, 9):                              # hull: wedge nose-up at the bow
        t = (zi + 8) / 16.0
        w = 3.4 - 2.2 * max(0.0, t - 0.55) / 0.45        # narrows to the nose
        lift = 2 + int(round(2.6 * max(0.0, t - 0.5)))   # bow rises
        for x in range(-int(w), int(w) + 1):
            put(x, lift, zi, HULLD if abs(x) == int(w) else HULL)
            put(x, lift + 1, zi, HULL if abs(x) < int(w) else HULLD, only_empty=True)
    for zi in range(-7, 0):                              # the saddle seat
        put(0, 4, zi, SEAT); put(-1, 4, zi, SEAT); put(1, 4, zi, SEAT)
        put(0, 5, zi, SEATL if zi % 2 else SEAT)
    for x in range(-2, 3):                               # handlebar T at the bow rise
        put(x, 6, 4, BAR)
    put(-2, 6, 4, GRIP); put(2, 6, 4, GRIP)
    put(0, 5, 4, BAR); put(0, 4, 4, BAR)
    for zi in range(-8, 9, 2):                           # sponson stripe
        put(int(3.4 - 2.2 * max(0.0, ((zi + 8) / 16.0) - 0.55) / 0.45), 3, zi, HULLL, only_empty=True)
    for zi in range(-9, 10):                             # waterline lap hugging the hull
        t = (zi + 8) / 16.0
        w = int(3.4 - 2.2 * max(0.0, t - 0.55) / 0.45) + 1
        put(-w, 1, zi, WET, only_empty=True)
        put(w, 1, zi, WET, only_empty=True)
        if zi % 3 == 0:
            put(-w - 1, 1, zi, FOAM, only_empty=True)
            put(w + 1, 1, zi, FOAM, only_empty=True)
    for x in range(-3, 4):                               # stern wash
        put(x, 1, -9, WET, only_empty=True)
    return V


def build_longdock():
    """SAND POND: the camp dock — straight, orange-brown, a LONG runup ending over
    deep water. Built for exactly one purpose, and the dog knows what it is."""
    PLANK = (196, 124, 62); PLANKD = (156, 94, 44); PLANKL = (224, 152, 84)
    POST = (120, 76, 40); POSTD = (92, 56, 28); WET = (72, 82, 84); FOAM = (168, 196, 204)
    V = {}
    put, ellip, box = _vox_helpers(V)
    for zi in range(-30, 31):                            # the runup: straight planking
        for x in range(-4, 5):
            c = PLANK
            if zi % 4 == 0:
                c = PLANKD                               # plank seams
            elif (x + zi) % 9 == 0:
                c = PLANKL                               # sun-worn boards
            put(x, 3, zi, c)
        put(-4, 2, zi, PLANKD); put(4, 2, zi, PLANKD)    # edge shadow line
    for zi in range(-28, 31, 8):                         # post pairs marching out
        for yy in range(0, 3):
            put(-4, yy, zi, POST if yy > 0 else POSTD)
            put(4, yy, zi, POST if yy > 0 else POSTD)
    for zi in range(-30, 31, 3):                         # waterline lap at the pilings
        put(-5, 1, zi, WET, only_empty=True)
        put(5, 1, zi, WET, only_empty=True)
        if zi % 6 == 0:
            put(-6, 1, zi, FOAM, only_empty=True)
            put(6, 1, zi, FOAM, only_empty=True)
    for x in range(-4, 5):                               # the END board — the launch pad
        put(x, 3, 30, PLANKL)
    return V


def build_angler(seated=False):
    """PLEASANT: shore-side anglers. One stands mid-cast; one sits on a bucket the
    way only a person with nowhere better to be can sit."""
    HAT = (110, 122, 82); HATD = (84, 94, 62)
    VEST = (168, 108, 60) if not seated else (86, 110, 138)
    VESTD = (128, 80, 44) if not seated else (62, 82, 106)
    SHIRT = (200, 196, 180); SKIN = (222, 178, 140)
    PANT = (94, 88, 78); BOOT = (52, 48, 44)
    ROD = (120, 90, 56); LINE = (210, 214, 220); BUCKET = (196, 196, 200); BUCKETD = (150, 150, 156)
    V = {}
    put, ellip, box = _vox_helpers(V)
    if seated:
        for yy in range(0, 4):                            # the bucket throne
            for a in range(0, 360, 30):
                put(int(round(2.0 * math.cos(math.radians(a)))), yy,
                    int(round(2.0 * math.sin(math.radians(a)))), BUCKET if yy > 0 else BUCKETD)
        ellip(0, 5, 0, 2.4, 2.2, 2.0, VEST)               # hunched torso
        ellip(0, 6.4, 0.8, 2.0, 1.6, 1.6, VESTD, only_empty=True)
        for zz in range(1, 4):                            # legs folded forward
            put(-1, 2, zz, PANT); put(1, 2, zz, PANT)
        put(-1, 1, 4, BOOT); put(1, 1, 4, BOOT)
        ellip(0, 8.6, 0.6, 1.5, 1.4, 1.4, SKIN)           # head, tucked low
        for a in range(0, 360, 24):                       # bucket hat brim
            put(int(round(2.0 * math.cos(math.radians(a)))), 9.4,
                int(round(0.6 + 2.0 * math.sin(math.radians(a)))), HATD)
        ellip(0, 10, 0.6, 1.4, 0.8, 1.3, HAT)
        for i in range(9):                                # rod held low + lazy
            put(2 + int(i * 0.55), 6 - int(i * 0.2), 2 + i, ROD if i % 3 else HATD)
        for yy2 in range(1, 5):
            if yy2 % 2:
                put(7, yy2, 11, LINE)
    else:
        put(-1, 1, 0, BOOT); put(1, 1, 0, BOOT)           # planted stance
        for yy in range(2, 6):
            put(-1, yy, 0, PANT); put(1, yy, 0, PANT)
        ellip(0, 7.5, 0, 2.2, 2.6, 1.8, VEST)             # vest torso
        ellip(0, 8.6, 0.8, 1.8, 1.6, 1.4, VESTD, only_empty=True)
        put(-2, 8, 0, SHIRT); put(2, 8, 0, SHIRT)         # rolled sleeves
        put(-3, 7, 1, SKIN)                               # forward arm to the rod
        ellip(0, 11.2, 0.4, 1.5, 1.5, 1.4, SKIN)          # head
        for a in range(0, 360, 24):                       # bucket hat
            put(int(round(2.0 * math.cos(math.radians(a)))), 12.0,
                int(round(0.4 + 1.9 * math.sin(math.radians(a)))), HATD)
        ellip(0, 12.6, 0.4, 1.4, 0.8, 1.3, HAT)
        n = 14                                            # the rod, mid-cast arc
        for i in range(n):
            t = i / float(n - 1)
            put(int(round(-3 + 9 * t)), int(round(8 + 8 * t - 3.5 * t * t)), int(round(1 + 8 * t)), ROD if i % 4 else HATD)
        for yy2 in range(1, 12):                          # the cast line, dashed, way out
            if yy2 % 2:
                put(6, yy2, 12, LINE)
    return V


def build_osprey():
    """PURGATORY: an OSPREY roosting on a snag — dark above, WHITE below, the bold
    dark eye-stripe through a white head. The fish-hawk, resting between hunts."""
    BACK = (74, 56, 40); BACKD = (54, 40, 30); BACKL = (96, 76, 54)
    WHITE = (238, 236, 228); WHITED = (208, 204, 192)
    STRIPE = (44, 34, 26); EYE = (238, 196, 60); PUP = (22, 18, 14)
    BILL = (30, 28, 26); TALON = (150, 150, 146)
    SNAG = (96, 78, 58); SNAGD = (70, 56, 42)
    V = {}
    put, ellip, box = _vox_helpers(V)
    for yy in range(0, 7):                                # the bare snag perch
        put(0, yy, 0, SNAG); put(1, yy, 0, SNAGD)
    put(-1, 6, 1, SNAGD); put(2, 5, -1, SNAGD)
    # body: upright roost posture, dark mantle over white breast
    ellip(0.5, 10, 0.5, 2.6, 3.6, 2.4, WHITE)             # breast/underparts
    ellip(0.5, 11, -0.6, 2.7, 3.2, 2.0, BACK)             # dark mantle folded over
    ellip(0.5, 12.4, -0.8, 2.2, 2.0, 1.6, BACKL)
    for yy in range(8, 13):                               # folded wing edge line
        put(-2, yy, 0, BACKD)
        put(3, yy, 0, BACKD)
    # white head with THE eye-stripe
    ellip(0.5, 14.6, 1.2, 1.9, 1.9, 1.8, WHITE)
    ellip(0.5, 15.6, 0.6, 1.5, 1.0, 1.4, WHITED, only_empty=True)
    for zx in range(-1, 3):                               # the dark stripe THROUGH the eye
        put(zx, 14.6, 2, STRIPE)
    put(-1, 14.6, 3, STRIPE); put(2, 14.6, 3, STRIPE)
    put(0, 14.6, 3, EYE); put(1, 14.6, 3, EYE)            # fierce yellow eyes
    put(0, 14.4, 3, PUP)
    put(0.5, 13.6, 3, BILL); put(0.5, 13.2, 3, BILL)      # the hooked bill
    for s2 in (0, 1):                                     # talons gripping the snag
        put(s2, 7, 1, TALON)
    return V


BANKS = [
    ("sand_dock.png",         build_longdock,   dict(yaw=90, pitch=38, target=118)),
    ("bank_osprey.png",       build_osprey,     dict(yaw=14, pitch=22, target=40)),
    ("bank_angler_0.png",     build_angler,     dict(yaw=20, pitch=24, target=40)),
    ("bank_angler_1.png",     (lambda: build_angler(True)), dict(yaw=-16, pitch=24, target=34)),
    ("bank_barredowl.png",    build_barredowl,  dict(yaw=8, pitch=24, target=38)),
    ("bank_lizzie.png",       build_lizzie,     dict(yaw=36, pitch=30, target=30)),
    ("bank_jetski_0.png",     build_jetski,     dict(yaw=28, pitch=30, target=42)),
    ("bank_jetski_1.png",     (lambda: build_jetski(True)), dict(yaw=-24, pitch=30, target=42)),
]


def contact_sheet(path):
    """All heroes on BOTH in-game water tones, next to env_snag for density."""
    water = Image.open(os.path.join(ART, "water.png")).convert("RGBA")

    def toned(w, h, tint, wash, wash_a):
        bg = Image.new("RGBA", (w, h))
        for y in range(0, h, water.height):
            for x in range(0, w, water.width):
                bg.paste(water, (x, y))
        p = bg.load()
        for y in range(h):
            for x in range(w):
                r, g, b, _ = p[x, y]
                r, g, b = r * tint[0], g * tint[1], b * tint[2]
                r = r * (1 - wash_a) + wash[0] * 255 * wash_a
                g = g * (1 - wash_a) + wash[1] * 255 * wash_a
                b = b * (1 - wash_a) + wash[2] * 255 * wash_a
                p[x, y] = (int(r), int(g), int(b), 255)
        return bg
    names = ["env_snag.png"] + [n for n, _, _ in HEROES] + \
        ["hero_cochichewick.png", "bank_umbrella.png", "bank_bonfire.png",
         "bank_barredowl.png", "bank_lizzie.png"]
    sprites = [Image.open(os.path.join(ART, n)) for n in names]
    pad, label_h = 12, 14
    cell_h = max(s.height for s in sprites) + pad * 2 + label_h
    widths = [s.width + pad * 2 for s in sprites]
    sheet_w = sum(widths)
    rows = [
        toned(sheet_w, cell_h, (1.0, 1.0, 1.0), (0.18, 0.40, 0.60), 0.16),        # mid-blue
        toned(sheet_w, cell_h, (0.54, 0.68, 0.94), (0.09, 0.17, 0.45), 0.32),     # dark navy
    ]
    sheet = Image.new("RGBA", (sheet_w, cell_h * 2))
    for ri, row in enumerate(rows):
        d = ImageDraw.Draw(row)
        x = 0
        for s, nm, w in zip(sprites, names, widths):
            row.paste(s, (x + (w - s.width) // 2, cell_h - pad - label_h - s.height), s)
            d.text((x + 4, cell_h - label_h), nm.replace(".png", ""),
                   fill=(255, 255, 255, 220))
            x += w
        sheet.paste(row, (0, ri * cell_h))
    sheet.save(path)
    print("sheet ->", path)


def main():
    for name, build, cam in HEROES:
        save(vox(build(), **cam), name)
    gen_loon()
    for name, build, cam in BANKS:
        save(vox(build(), **cam), name)
    save(vox_glow(build_bonfire(), build_bonfire_glow(), yaw=22, pitch=38, target=30),
         "bank_bonfire.png")
    sheet = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ART, "..", "heroes_sheet.png")
    contact_sheet(sheet)
    print("generated %d hero landmarks -> %s" % (len(GENERATED), os.path.abspath(ART)))


if __name__ == "__main__":
    main()
