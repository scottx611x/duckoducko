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
from voxel_duck import _vox_helpers                      # noqa: E402
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
HEROES = [
    ("hero_buker.png",        build_rowboat,    dict(yaw=34, pitch=44, target=140)),
    ("hero_woodbury.png",     build_dock,       dict(yaw=24, pitch=40, target=118)),
    ("hero_purgatory.png",    build_dreadtree,  dict(yaw=18, pitch=30, target=146)),
    ("hero_sand.png",         build_buoy,       dict(yaw=30, pitch=36, target=110)),
    ("hero_pleasant.png",     build_fountain,   dict(yaw=22, pitch=34, target=118)),
    ("hero_emerald.png",      build_emeraldrock, dict(yaw=15, pitch=40, target=124)),
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
    names = ["env_snag.png"] + [n for n, _, _ in HEROES] + ["hero_cochichewick.png"]
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
    sheet = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ART, "..", "heroes_sheet.png")
    contact_sheet(sheet)
    print("generated %d hero landmarks -> %s" % (len(GENERATED), os.path.abspath(ART)))


if __name__ == "__main__":
    main()
