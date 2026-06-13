#!/usr/bin/env python3
"""Voxel-first duck art for DUCKODUCKO.

ONE voxel model is the single source of truth.  We render it from chosen camera
angles to produce every 2D gameplay sprite (idle / 7 banks / side / hop / face),
AND export its real horizontal cross-sections as the mega-hop sprite-stack slices.
Tweak the model once -> all views + the 3D mega-hop regenerate, always consistent.

Camera: 3/4 tilted hero angle (chosen by playtest) -- you see the eye, the green
head sheen and the chestnut chest.  "Good lookin' duck", not baby-kawaii.

Run:  python3 tools/voxel_duck.py        (writes duck PNGs into ../art/)
"""
import math
from PIL import Image, ImageDraw

S = 5                       # supersample
BODY_CANVAS = 64            # square canvas for idle/bank/side/hop frames
FACE_CANVAS = 40
# BACK VIEW: camera ABOVE & BEHIND (base yaw 180 + positive pitch) so you see his
# BACK (green crown, vermiculated back, tail-curl), head leading UP the screen.
# (A negative pitch instead flips him belly-up -- that was the bug.)
GAME_YAW = 180
PITCH = math.radians(48)
SIDE_PITCH = math.radians(40)
SIDE_YAW = 70               # side_left = GAME_YAW+SIDE_YAW (head leans screen-left)
# 7-frame bank sweep as yaw OFFSETS from GAME_YAW: 0=hard left .. 3=straight .. 6=hard
# right. +offset leans the head screen-LEFT (toward travel for a left steer). Verified.
BANK_OFF = [34, 22, 11, 0, -11, -22, -34]
HERO_YAW, HERO_PITCH = 20, 28   # menu/select front 3/4: full face + chest


# ---- species -------------------------------------------------------------------
# Each species = a palette (same keys, shared geometry recolors automatically) +
# geometry flags + a render "size" (bufflehead is just plain small).
SPECIES = dict(
    mallard=dict(dark_rump=True),
    hen=dict(hen=True, bill_saddle=True),
    wood=dict(crest=True, face_paint="wood", red_eye=True, chest_speckles=True, flank_bars=True),
    # head_scale must leave the stubby bill poking out past the head ellipsoid
    bufflehead=dict(head_scale=1.18, bill_len=16, face_paint="bufflehead", size=0.85),
    pintail=dict(pin_tail=True, face_paint="pintail", long_neck=True, bill_stripe=True),
    hoodie=dict(crest=True, big_crest=True, face_paint="hoodie", eye_col=(244, 196, 60), bill_thin=True),
    canvasback=dict(red_eye=True, dark_rump=True),
    eider=dict(face_paint="eider", bill_len=15),
    golden=dict(chest_speckles=True, dark_rump=True),
    shoveler=dict(bill_len=19, bill_wide=True, eye_col=(238, 198, 60)),
    ruddy=dict(pin_tail=True, face_paint="ruddy"),
    harlequin=dict(face_paint="harlequin"),
    rubberduck=dict(size=0.95),
)


def palette(sp):
    if sp == "hen":
        return dict(
            back=(140, 114, 84), body=(174, 148, 112), belly=(206, 184, 148),
            verm_d=(120, 96, 68), verm_l=(196, 174, 138),
            nape=(128, 100, 66), head=(170, 144, 106), headh=(202, 178, 138),
            crown=(110, 84, 54), glint=(216, 196, 160),
            chest=(184, 152, 114), chestd=(150, 122, 88), chestl=(206, 182, 146),
            bill=(210, 156, 80), billd=(150, 106, 56), nail=(96, 74, 48), nostril=(120, 92, 56),
            white=(234, 226, 208), collar=(150, 120, 84),
            wing=(150, 124, 92), wingd=(118, 92, 62), primary=(96, 76, 54),
            specw=(228, 224, 210), spec=(70, 116, 168), specd=(46, 82, 128),
            tail=(112, 88, 62), tailhi=(150, 124, 92), eye=(22, 18, 20),
        )
    if sp == "wood":  # the show-off: iridescent crested head, burgundy chest, buffy flanks
        return dict(
            back=(64, 60, 76), body=(192, 162, 104), belly=(214, 200, 164),
            verm_d=(50, 46, 60), verm_l=(94, 88, 106),
            nape=(66, 48, 104), head=(36, 112, 72), headh=(92, 172, 112),
            crown=(70, 50, 110), glint=(144, 222, 162),
            chest=(124, 48, 58), chestd=(96, 34, 46), chestl=(152, 70, 80),
            bill=(216, 92, 70), billd=(160, 52, 42), nail=(46, 34, 32), nostril=(120, 50, 40),
            white=(242, 240, 232), collar=(242, 240, 232),
            wing=(70, 92, 88), wingd=(52, 70, 66), primary=(40, 50, 54),
            specw=(236, 234, 226), spec=(58, 108, 172), specd=(40, 76, 128),
            tail=(40, 36, 48), tailhi=(82, 72, 92), eye=(20, 18, 22),
        )
    if sp == "bufflehead":  # tiny: black-and-white, big head wedge patch
        return dict(
            back=(32, 30, 38), body=(228, 226, 220), belly=(240, 238, 232),
            verm_d=(26, 24, 32), verm_l=(52, 50, 60),
            nape=(40, 34, 58), head=(38, 34, 54), headh=(90, 62, 124),
            crown=(30, 26, 44), glint=(124, 182, 144),
            chest=(234, 232, 226), chestd=(204, 202, 196), chestl=(246, 244, 238),
            bill=(122, 132, 142), billd=(92, 100, 110), nail=(60, 66, 74), nostril=(80, 88, 98),
            white=(244, 242, 238), collar=(244, 242, 238),
            wing=(46, 44, 52), wingd=(34, 32, 40), primary=(26, 24, 30),
            specw=(238, 238, 240), spec=(226, 226, 230), specd=(186, 186, 194),
            tail=(92, 94, 102), tailhi=(132, 134, 142), eye=(18, 16, 20),
        )
    if sp == "hoodie":  # hooded merganser: black head, white fan hood, rusty flanks
        return dict(
            back=(30, 28, 34), body=(154, 92, 56), belly=(214, 198, 174),
            verm_d=(126, 72, 42), verm_l=(176, 112, 70),
            nape=(34, 30, 40), head=(30, 28, 36), headh=(58, 50, 66),
            crown=(24, 22, 30), glint=(82, 72, 92),
            chest=(238, 236, 230), chestd=(206, 204, 198), chestl=(248, 246, 240),
            bill=(64, 66, 74), billd=(44, 46, 52), nail=(30, 32, 36), nostril=(52, 54, 62),
            white=(246, 244, 240), collar=(246, 244, 240),
            wing=(42, 40, 48), wingd=(32, 30, 38), primary=(24, 22, 28),
            specw=(238, 238, 240), spec=(214, 214, 218), specd=(180, 180, 186),
            tail=(74, 58, 44), tailhi=(112, 92, 70), eye=(20, 18, 22),
        )
    if sp == "canvasback":  # the racer: chestnut head, black chest, canvas body
        return dict(
            back=(198, 196, 188), body=(218, 216, 208), belly=(234, 232, 226),
            verm_d=(190, 188, 180), verm_l=(232, 230, 222),
            nape=(106, 38, 26), head=(148, 54, 36), headh=(182, 78, 52),
            crown=(122, 44, 30), glint=(198, 98, 66),
            chest=(34, 32, 36), chestd=(24, 22, 26), chestl=(46, 44, 50),
            bill=(38, 36, 40), billd=(26, 24, 28), nail=(20, 18, 22), nostril=(48, 46, 50),
            white=(240, 238, 232), collar=(240, 238, 232),
            wing=(182, 180, 172), wingd=(152, 150, 144), primary=(112, 110, 106),
            tail=(62, 60, 58), tailhi=(110, 108, 104),
            specw=(238, 236, 230), spec=(168, 166, 158), specd=(140, 138, 132), eye=(20, 18, 22),
        )
    if sp == "eider":  # the king: pearl crown, green cheeks, orange shield, black body
        return dict(
            back=(30, 28, 32), body=(38, 36, 40), belly=(52, 50, 54),
            verm_d=(24, 22, 26), verm_l=(50, 48, 52),
            nape=(122, 170, 126), head=(226, 224, 216), headh=(152, 178, 198),
            crown=(140, 168, 190), glint=(192, 212, 226),
            chest=(242, 234, 216), chestd=(224, 210, 186), chestl=(250, 246, 236),
            bill=(240, 140, 60), billd=(202, 102, 42), nail=(60, 40, 28), nostril=(170, 90, 40),
            white=(246, 244, 238), collar=(246, 244, 238),
            wing=(34, 32, 38), wingd=(26, 24, 30), primary=(20, 18, 24),
            specw=(238, 238, 240), spec=(214, 214, 218), specd=(180, 180, 186),
            tail=(28, 26, 30), tailhi=(70, 68, 72), eye=(20, 18, 22),
        )
    if sp == "golden":  # the myth. do not question the golden mallard.
        return dict(
            back=(182, 150, 66), body=(206, 176, 92), belly=(232, 212, 142),
            verm_d=(160, 128, 52), verm_l=(226, 200, 120),
            nape=(150, 110, 30), head=(214, 164, 42), headh=(238, 198, 74),
            crown=(178, 132, 34), glint=(252, 232, 142),
            chest=(192, 142, 42), chestd=(160, 112, 30), chestl=(216, 170, 64),
            bill=(255, 216, 92), billd=(220, 174, 56), nail=(170, 130, 40), nostril=(190, 146, 48),
            white=(252, 244, 200), collar=(252, 244, 200),
            wing=(196, 166, 82), wingd=(168, 138, 60), primary=(132, 104, 42),
            specw=(252, 246, 210), spec=(58, 108, 172), specd=(40, 76, 128),
            tail=(150, 116, 44), tailhi=(244, 226, 150), eye=(24, 20, 16),
        )
    if sp == "shoveler":  # green head, white chest, rust flanks, THAT bill
        return dict(
            back=(42, 46, 42), body=(172, 98, 58), belly=(196, 128, 84),
            verm_d=(146, 80, 46), verm_l=(192, 120, 76),
            nape=(22, 96, 54), head=(40, 142, 80), headh=(96, 196, 128),
            crown=(20, 84, 48), glint=(150, 232, 182),
            chest=(240, 238, 230), chestd=(212, 210, 202), chestl=(250, 248, 242),
            bill=(44, 42, 46), billd=(30, 28, 32), nail=(22, 20, 24), nostril=(56, 54, 58),
            white=(240, 238, 230), collar=(240, 238, 230),
            wing=(120, 140, 150), wingd=(92, 110, 120), primary=(60, 72, 80),
            specw=(236, 236, 228), spec=(58, 130, 92), specd=(40, 96, 66),
            tail=(38, 40, 38), tailhi=(208, 206, 198), eye=(20, 18, 22),
        )
    if sp == "ruddy":  # chestnut body, black cap, white cheek, BLUE bill. iconic.
        return dict(
            back=(128, 66, 38), body=(154, 84, 48), belly=(186, 130, 92),
            verm_d=(110, 56, 32), verm_l=(174, 102, 62),
            nape=(28, 26, 30), head=(36, 32, 36), headh=(52, 46, 52),
            crown=(24, 22, 26), glint=(66, 60, 66),
            chest=(160, 92, 54), chestd=(132, 72, 40), chestl=(182, 112, 70),
            bill=(96, 150, 210), billd=(66, 112, 168), nail=(44, 74, 112), nostril=(70, 118, 174),
            white=(242, 240, 234), collar=(154, 84, 48),
            wing=(120, 64, 38), wingd=(96, 50, 30), primary=(70, 38, 24),
            specw=(170, 100, 60), spec=(140, 76, 44), specd=(110, 58, 34),
            tail=(40, 32, 26), tailhi=(80, 62, 48), eye=(18, 16, 18),
        )
    if sp == "harlequin":  # slate blue, white crescents, chestnut flanks. the painting.
        return dict(
            back=(58, 70, 94), body=(72, 86, 112), belly=(150, 88, 52),
            verm_d=(50, 60, 82), verm_l=(88, 102, 128),
            nape=(44, 54, 74), head=(64, 78, 104), headh=(84, 98, 124),
            crown=(38, 46, 64), glint=(104, 118, 144),
            chest=(70, 84, 110), chestd=(56, 68, 92), chestl=(88, 102, 128),
            bill=(120, 128, 140), billd=(90, 96, 108), nail=(60, 64, 72), nostril=(100, 106, 118),
            white=(244, 244, 240), collar=(244, 244, 240),
            wing=(52, 64, 86), wingd=(42, 52, 70), primary=(30, 38, 52),
            specw=(238, 238, 236), spec=(96, 110, 136), specd=(70, 82, 104),
            tail=(36, 42, 56), tailhi=(70, 80, 100), eye=(20, 18, 22),
        )
    if sp == "rubberduck":  # it is a rubber ducky. it squeaks. it has earned this.
        return dict(
            back=(238, 196, 52), body=(250, 212, 64), belly=(254, 230, 110),
            verm_d=(230, 186, 44), verm_l=(254, 224, 92),
            nape=(238, 196, 52), head=(250, 212, 64), headh=(254, 228, 100),
            crown=(244, 204, 58), glint=(255, 240, 150),
            chest=(250, 212, 64), chestd=(238, 196, 52), chestl=(254, 228, 100),
            bill=(244, 130, 40), billd=(206, 100, 28), nail=(180, 86, 24), nostril=(214, 106, 32),
            white=(254, 240, 150), collar=(250, 212, 64),
            wing=(244, 202, 56), wingd=(232, 188, 46), primary=(220, 176, 40),
            specw=(254, 230, 110), spec=(246, 208, 60), specd=(234, 192, 48),
            tail=(240, 198, 54), tailhi=(254, 228, 100), eye=(24, 22, 22),
        )
    if sp == "pintail":  # the gymnast: chocolate head, white neck stripe, long pin tail
        return dict(
            back=(122, 122, 124), body=(172, 172, 170), belly=(214, 212, 206),
            verm_d=(98, 98, 100), verm_l=(196, 196, 194),
            nape=(64, 40, 28), head=(94, 60, 42), headh=(124, 84, 60),
            crown=(72, 46, 32), glint=(142, 102, 72),
            chest=(238, 236, 228), chestd=(208, 206, 198), chestl=(248, 246, 240),
            bill=(112, 126, 142), billd=(72, 82, 96), nail=(32, 34, 40), nostril=(60, 68, 80),
            white=(242, 240, 234), collar=(242, 240, 234),
            wing=(142, 142, 140), wingd=(110, 110, 108), primary=(72, 72, 70),
            specw=(228, 222, 192), spec=(96, 120, 76), specd=(66, 86, 54),
            tail=(36, 36, 40), tailhi=(92, 92, 98), eye=(20, 18, 22),
        )
    return dict(  # mallard drake
        back=(132, 126, 110), body=(170, 164, 148), belly=(214, 208, 192),
        verm_d=(116, 110, 96), verm_l=(198, 192, 176),
        nape=(22, 96, 54), head=(40, 142, 80), headh=(96, 196, 128),
        crown=(20, 84, 48), glint=(150, 232, 182),
        chest=(150, 86, 52), chestd=(112, 64, 40), chestl=(176, 104, 64),
        bill=(246, 184, 70), billd=(208, 150, 48), nail=(150, 108, 40), nostril=(120, 90, 40),
        white=(240, 238, 230), collar=(240, 238, 230),
        wing=(152, 144, 126), wingd=(118, 110, 94), primary=(74, 70, 62),
        specw=(236, 236, 228), spec=(58, 108, 172), specd=(40, 76, 128),
        tail=(44, 40, 52), tailhi=(226, 223, 213), eye=(20, 18, 22),
    )


# ---- voxel model -------------------------------------------------------------
def build(sp="mallard", wings="folded", beak_open=False):
    """Return {(x,y,z): rgb}.  x=right, y=up, z=head(+).  Shared duck geometry,
    species palette + flags (crest / head patch / pin tail / face paint)."""
    spec = SPECIES[sp]
    hen = spec.get("hen", False)
    P = palette(sp)
    V = {}

    def put(x, y, z, c, only_empty=False):
        if only_empty and (x, y, z) in V:
            return
        V[(x, y, z)] = c

    def ellip(cx, cy, cz, rx, ry, rz, c, only_empty=False):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            for y in range(int(cy - ry - 1), int(cy + ry + 2)):
                for z in range(int(cz - rz - 1), int(cz + rz + 2)):
                    if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + ((z - cz) / rz) ** 2 <= 1.0:
                        put(x, y, z, c, only_empty)

    def box(x0, x1, y0, y1, z0, z1, c, only_empty=False):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    put(x, y, z, c, only_empty)

    # ---- body: teardrop, fuller at chest, tapering to tail ----
    ellip(0, 0, 0, 6, 4.5, 10, P["body"])
    ellip(0, 2.0, -0.5, 5.2, 3.2, 9.2, P["back"], only_empty=True)   # darker back
    ellip(0, -2.2, 1, 5.0, 3.2, 8.5, P["belly"], only_empty=True)    # pale belly
    # vermiculation: fine speckle over the back (texture detail)
    for (x, y, z) in list(V.keys()):
        if y >= 1 and V[(x, y, z)] in (P["back"], P["body"]):
            h = (x * 131 + y * 17 + z * 101) % 9
            if h == 0:
                V[(x, y, z)] = P["verm_d"]
            elif h == 1:
                V[(x, y, z)] = P["verm_l"]
    # ---- chest / breast ----
    ellip(0, -0.5, 6.5, 4.4, 3.6, 3.6, P["chest"], only_empty=True)
    ellip(0, -1.6, 7.0, 3.2, 2.6, 2.6, P["chestd"], only_empty=True)
    ellip(0, 1.6, 6.5, 3.4, 1.6, 2.6, P["chestl"], only_empty=True)
    if spec.get("chest_speckles"):
        # wood-duck burgundy chest is stippled with little white arrowheads
        for (x, y, z) in list(V.keys()):
            if V[(x, y, z)] in (P["chest"], P["chestd"], P["chestl"]) and (x * 53 + y * 29 + z * 71) % 7 == 0:
                V[(x, y, z)] = P["white"]
    if spec.get("dark_rump"):
        # drake mallard: black rump/undertail between the gray body and the tail
        for (x, y, z) in list(V.keys()):
            if z <= -7 and V[(x, y, z)] in (P["back"], P["body"], P["belly"], P["verm_d"], P["verm_l"]):
                V[(x, y, z)] = (38, 36, 44)
    # ---- wings: folded (with bordered speculum + primaries) or spread (hops) ----
    if wings == "folded":
        for s in (1, -1):
            ellip(5.6 * s, 1.0, -0.5, 1.7, 2.9, 7, P["wing"])
            ellip(6.0 * s, -0.2, -2.5, 1.2, 2.0, 4.5, P["wingd"], only_empty=True)
            box(5 * s, 6 * s, -1, 1, -8, -6, P["primary"], only_empty=True)   # dark tips
            for z in (-5, -4, -3):                                   # speculum, white-bordered
                put(6 * s, 2, z, P["specw"]); put(6 * s, 1, z, P["spec"])
                put(6 * s, 0, z, P["specd"]); put(6 * s, -1, z, P["specw"])
        if spec.get("flank_bars"):
            # wood duck: black-and-white barring along the wing's leading edge
            for (x, y, z) in list(V.keys()):
                if V[(x, y, z)] in (P["wing"], P["wingd"]) and z >= 4:
                    V[(x, y, z)] = P["white"] if y % 2 == 0 else (30, 28, 34)
        if sp == "bufflehead":
            # bright white flanks below the dark folded wing
            for (x, y, z) in list(V.keys()):
                if V[(x, y, z)] in (P["wing"], P["wingd"]) and y < 1:
                    V[(x, y, z)] = P["body"]
    else:
        up = 2 if wings == "out_up" else 0
        for s in (1, -1):
            for w in range(0, 9):
                yy = 1 + up + (w // 3)
                col = P["primary"] if w >= 6 else P["wing"]
                box((5 + w) * s, (5 + w) * s, yy, yy + 1, -3, 4, col)
            for z in (-1, 0, 1):
                put(7 * s, 2 + up, z, P["spec"]); put(7 * s, 3 + up, z, P["specw"])
    # ---- tail: lifted, dark, drake curl + pale edges ----
    box(-2, 2, 0, 2, -13, -10, P["tail"])
    box(-1, 1, 2, 3, -12, -10, P["tail"])
    put(-2, 1, -11, P["tailhi"]); put(2, 1, -11, P["tailhi"])
    if sp == "mallard":
        put(0, 4, -10, P["tail"]); put(0, 5, -11, P["tail"]); put(0, 5, -10, P["tail"])  # curl
        for z in (-12, -11, -10):                     # white outer tail feathers
            put(-3, 1, z, P["tailhi"]); put(3, 1, z, P["tailhi"])
    if spec.get("pin_tail"):
        # the pintail's pin: a long thin point raked up behind the tail
        box(-1, 1, 2, 3, -15, -13, P["tail"])
        box(0, 0, 3, 4, -18, -15, P["tail"])
        put(0, 4, -18, P["tailhi"])
    # ---- neck + head (pintail carries its head on an elegant long neck) ----
    hs = spec.get("head_scale", 1.0)
    NY = 2 if spec.get("long_neck") else 0
    ellip(0, 3.4 + NY * 0.5, 7, 2.5 if NY else 2.7, 3.0 + NY * 0.8, 2.5 if NY else 2.7, P["head"])
    ellip(0, 6.6 + NY, 10, 3.7 * hs, 3.7 * hs, 3.6 * hs, P["head"])
    ellip(0, 4.0 + NY * 0.6, 10.2, 3.6, 1.6, 3.2, P["nape"], only_empty=True)  # dark underside/nape
    ellip(0, 8.2 + NY, 10.6, 2.7 * hs, 2.1 * hs, 2.6 * hs, P["headh"], only_empty=True)  # sheen
    ellip(0, 9.0 + NY, 11.0, 1.5, 1.2, 1.6, P["glint"], only_empty=True)  # bright glint
    if hen:
        ellip(0, 8.6, 9.6, 3.4, 1.8, 3.2, P["crown"], only_empty=True)  # dark cap
        for z in range(8, 13):                                          # eye-line
            put(3, 6, z, P["crown"], only_empty=True); put(-3, 6, z, P["crown"], only_empty=True)
    if spec.get("crest"):
        # wood-duck crest: an iridescent mane sweeping back/down off the head
        ellip(0, 7.4, 7.2, 2.4, 2.6, 2.6, P["crown"])
        ellip(0, 5.4, 5.6, 1.7, 1.9, 1.9, P["crown"])
        ellip(0, 8.8, 8.4, 1.9, 1.6, 2.2, P["nape"], only_empty=True)
    if spec.get("big_crest"):
        # hooded merganser: the raised FAN — a tall round disc atop/behind the head
        ellip(0, 9.0, 8.2, 2.3, 3.2, 3.4, P["crown"])
    fp = spec.get("face_paint")
    if fp == "wood":
        # two thin white face lines: over the eye to the crest tip + white throat
        for (x, y, z) in list(V.keys()):
            if V[(x, y, z)] in (P["head"], P["headh"], P["crown"], P["nape"]):
                if abs(x) >= 2 and y == 9 and 6 <= z <= 11:
                    V[(x, y, z)] = P["white"]
                elif abs(x) >= 2 and y == 6 and 5 <= z <= 9:
                    V[(x, y, z)] = P["white"]
                elif y <= 5 and z >= 10:                       # chin/throat patch
                    V[(x, y, z)] = P["white"]
    elif fp == "bufflehead":
        # the signature wedge: a huge white patch wrapping the back half of the head
        for (x, y, z) in list(V.keys()):
            if V[(x, y, z)] in (P["head"], P["headh"], P["glint"]) and z <= 9.5 and y >= 5.0:
                V[(x, y, z)] = P["white"]
    elif fp == "hoodie":
        # THE HOOD: a big white fan centered in the raised crest, black rim on
        # every side (the paint window stops short of the crest's edges)
        for (x, y, z) in list(V.keys()):
            if V[(x, y, z)] in (P["head"], P["headh"], P["glint"], P["crown"], P["nape"]) \
                    and 5.0 <= z <= 9.5 and 6.0 <= y <= 10.5 and abs(x) <= 2:
                V[(x, y, z)] = P["white"]
        # two black spur bars between the white chest and rusty flank
        for s in (1, -1):
            for y in range(-1, 3):
                for z in (4, 5):
                    if (3 * s, y, z) in V:
                        V[(3 * s, y, z)] = (26, 24, 30)
    elif fp == "eider":
        # the king's orange-yellow frontal shield, black-rimmed, atop the bill base
        for x in range(-1, 2):
            for y in (6, 7):
                for z in (10, 11, 12):
                    V[(x, y, z)] = (250, 192, 72)
        for x in range(-2, 3):
            for z in (9, 13):
                if (x, 6, z) in V:
                    V[(x, 6, z)] = (30, 28, 32)
    elif fp == "ruddy":
        # the ruddy's bright white cheeks, below the black cap
        for (x, y, z) in list(V.keys()):
            if V[(x, y, z)] in (P["head"], P["headh"]) and abs(x) >= 2 \
                    and 4.5 <= y <= 7.0 and 9.0 <= z <= 13.0:
                V[(x, y, z)] = P["white"]
    elif fp == "harlequin":
        # the harlequin's paint job: white crescent before the eye, ear dot,
        # and a thin white collar slash at the neck base
        for (x, y, z) in list(V.keys()):
            if V[(x, y, z)] in (P["head"], P["headh"], P["glint"], P["crown"]):
                if z >= 12.0 and y >= 5.0:
                    V[(x, y, z)] = P["white"]          # face crescent
                elif abs(x) >= 3 and 6.5 <= y <= 7.5 and 8.0 <= z <= 9.0:
                    V[(x, y, z)] = P["white"]          # ear dot
        for a in range(0, 360, 12):
            x = round(2.9 * math.cos(math.radians(a)))
            y = round(3.4 + 2.9 * math.sin(math.radians(a)))
            if (x, y, 6) in V:
                V[(x, y, 6)] = P["white"]              # collar slash
    elif fp == "pintail":
        # white breast finger running up each side of the neck toward the head
        for y in range(1, 7 + NY):
            for z in (6, 7):
                if (2, y, z) in V:
                    V[(2, y, z)] = P["white"]
                if (-2, y, z) in V:
                    V[(-2, y, z)] = P["white"]
    # ---- white collar ring at neck base (mallards only) ----
    if sp in ("mallard", "hen"):
        for a in range(0, 360, 14):
            x = round(2.9 * math.cos(math.radians(a)))
            y = round(3.4 + 2.9 * math.sin(math.radians(a)))
            if (x, y, 7) in V:
                put(x, y, 7, P["collar"])
    # ---- bill: long, flat, spatulate (stubby on a bufflehead, a spike on a merganser) ----
    bl = spec.get("bill_len", 17)
    bw = 1 if spec.get("bill_thin") else (3 if spec.get("bill_wide") else 2)
    if beak_open:
        # mid-QUACK: upper mandible tips up, lower swings down, dark mouth at the hinge
        box(-bw, bw, 5 + NY, 6 + NY, 11, bl - 1, P["bill"])
        box(-1, 1, 6 + NY, 6 + NY, bl, bl, P["bill"])
        box(-1, 1, 6 + NY, 6 + NY, bl, bl, P["nail"])
        mw = max(0, bw - 1)
        box(-mw, mw, 4 + NY, 4 + NY, 11, 13, (44, 26, 28))         # open mouth
        span = max(1, bl - 12)
        for z in range(11, bl):
            drop = 1 + (z - 11) * 3 // span
            box(-bw, bw, 4 + NY - drop, 4 + NY - drop, z, z, P["billd"])
    else:
        box(-bw, bw, 4 + NY, 5 + NY, 11, bl - 1, P["bill"])
        box(-1, 1, 4 + NY, 5 + NY, bl, bl, P["bill"])     # rounded tip
        box(-2, 2, 6 + NY, 6 + NY, 10, 12, P["billd"], only_empty=True)  # base shade under head
        box(-2, 2, 5 + NY, 5 + NY, 12, bl - 1, P["billd"], only_empty=True)  # top ridge
        box(-1, 1, 4 + NY, 5 + NY, bl, bl, P["nail"])     # nail at tip
        put(1, 5 + NY, 13, P["nostril"]); put(-1, 5 + NY, 13, P["nostril"])
        if spec.get("bill_saddle"):
            # hen mallard: dark saddle blotch on the orange bill
            box(-1, 1, 5 + NY, 5 + NY, 13, 15, (96, 70, 46))
        if spec.get("bill_stripe"):
            # pintail: black culmen stripe down the blue-gray bill
            for z in range(11, bl + 1):
                put(0, 5 + NY, z, P["nail"])
    # ---- eyes (+ glint) ----
    ex = 3 if hs <= 1.0 else 4                        # bigger head -> eyes sit wider
    eye = spec.get("eye_col", (196, 44, 32) if spec.get("red_eye") else P["eye"])
    for sx in (ex, -ex):
        put(sx, 7 + NY, 10, eye); put(sx, 8 + NY, 10, eye); put(sx, 7 + NY, 11, eye)
        put(sx, 8 + NY, 11, P["white"], only_empty=True)
    return V


def shade(V):
    """Camera-independent voxel shading: exposed + top-lit faces brighten."""
    SH = {}
    for (x, y, z), c in V.items():
        opens = sum(1 for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0),
                                (0, -1, 0), (0, 0, 1), (0, 0, -1))
                    if (x + d[0], y + d[1], z + d[2]) not in V)
        f = 0.62 + 0.05 * opens
        if (x, y + 1, z) not in V:
            f += 0.14
        if (x - 1, y + 1, z + 1) not in V:
            f += 0.04
        f = max(0.5, min(1.18, f))
        SH[(x, y, z)] = tuple(max(0, min(255, int(v * f))) for v in c)
    return SH


# ---- rendering ---------------------------------------------------------------
def _crisp_outline(hi, out, outline=True):
    pal = list({hi.getpixel((a, b)) for b in range(hi.height) for a in range(hi.width)
                if hi.getpixel((a, b))[3] == 255})
    if not pal:
        return Image.new("RGBA", (out, out), (0, 0, 0, 0))
    sm = hi.resize((out, out), Image.LANCZOS)
    o = Image.new("RGBA", (out, out), (0, 0, 0, 0))
    sp, op = sm.load(), o.load()
    for b in range(out):
        for a in range(out):
            r, g, bb, al = sp[a, b]
            if al < 150:
                continue
            best, bd = pal[0], 1e18
            for pc in pal:
                dd = (pc[0] - r) ** 2 + (pc[1] - g) ** 2 + (pc[2] - bb) ** 2
                if dd < bd:
                    bd, best = dd, pc
            op[a, b] = (best[0], best[1], best[2], 255)
    if not outline:                       # fire has no ink line — it's light, not a thing
        return o
    o2 = o.copy()
    op2 = o2.load()
    for b in range(out):
        for a in range(out):
            if o.getpixel((a, b))[3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    na, nb = a + dx, b + dy
                    if 0 <= na < out and 0 <= nb < out and o.getpixel((na, nb))[3] > 0:
                        op2[a, b] = (36, 28, 28, 255)
                        break
    return o2


def render(SH, yaw, pitch, out=BODY_CANVAS, scale=1.45, cy_frac=0.5, outline=True):
    cy_, sy_ = math.cos(yaw), math.sin(yaw)
    cp, sp_ = math.cos(pitch), math.sin(pitch)
    pts = []
    for (x, y, z), c in SH.items():
        x1 = x * cy_ + z * sy_
        z1 = -x * sy_ + z * cy_
        y2 = y * cp - z1 * sp_
        z2 = y * sp_ + z1 * cp
        pts.append((z2, x1, y2, c))
    pts.sort(key=lambda p: p[0])
    H = out * S
    img = Image.new("RGBA", (H, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cyc, vs = H / 2.0, H * cy_frac, scale * S
    r = vs * 0.62
    for _, x1, y2, c in pts:
        sx, syy = cx + x1 * vs, cyc - y2 * vs
        d.rectangle([sx - r, syy - r, sx + r, syy + r], fill=c + (255,))
    return _crisp_outline(img, out, outline)


def stack_slices(V, SH, canvas=30):
    """Real horizontal cross-sections (bottom->top) for in-game sprite-stacking."""
    xs = [p[0] for p in V]; zs = [p[2] for p in V]; ys = [p[1] for p in V]
    xmin, xmax, zmin, zmax = min(xs), max(xs), min(zs), max(zs)
    w, h = xmax - xmin + 1, zmax - zmin + 1
    sc = max(1, (canvas - 4) // max(w, h))
    ox = (canvas - w * sc) // 2
    oz = (canvas - h * sc) // 2
    out = []
    for yv in range(min(ys), max(ys) + 1):
        im = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
        dd = ImageDraw.Draw(im)
        for (x, y, z), c in SH.items():
            if y != yv:
                continue
            ix = ox + (x - xmin) * sc
            iy = oz + (zmax - z) * sc          # head(+z) toward top of image
            dd.rectangle([ix, iy, ix + sc - 1, iy + sc - 1], fill=c + (255,))
        out.append(im)
    return out


# ---- generate everything -----------------------------------------------------
def generate_ducks(art_dir):
    import os

    def save(img, name):
        img.save(os.path.join(art_dir, name))

    for sp in SPECIES:
        size = SPECIES[sp].get("size", 1.0)        # bufflehead renders plain small
        sc = 1.45 * size
        SH = shade(build(sp, "folded"))
        gy = math.radians(GAME_YAW)
        # idle (gentle head-bob via slight pitch change)
        save(render(SH, gy, PITCH, scale=sc), "%s_idle_0.png" % sp)
        save(render(SH, gy, PITCH - math.radians(4), scale=sc), "%s_idle_1.png" % sp)
        # menu HERO + duck-select: front 3/4 so you see his face/chest (gameplay is back view)
        save(render(SH, math.radians(HERO_YAW), math.radians(HERO_PITCH), scale=sc), "%s_hero.png" % sp)
        # mid-QUACK hero frame: shown when the menu duck is tapped
        save(render(shade(build(sp, "folded", beak_open=True)),
                    math.radians(HERO_YAW), math.radians(HERO_PITCH), scale=sc), "%s_quack.png" % sp)
        # 24-frame turntable at hero pitch: free rotation on the duck-select screen
        for i in range(24):
            save(render(SH, math.radians(i * 15), math.radians(HERO_PITCH), scale=sc), "%s_spin_%02d.png" % (sp, i))
        # 7-frame banking sweep (offsets from the back-view base)
        for i, off in enumerate(BANK_OFF):
            save(render(SH, math.radians(GAME_YAW + off), PITCH, scale=sc), "%s_bank_%d.png" % (sp, i))
        # back-compat aliases (duck-select uses side keys; -1=left=head leans screen-left)
        save(render(SH, math.radians(GAME_YAW + 15), PITCH, scale=sc), "%s_turn_left.png" % sp)
        save(render(SH, math.radians(GAME_YAW - 15), PITCH, scale=sc), "%s_turn_right.png" % sp)
        save(render(SH, math.radians(GAME_YAW + SIDE_YAW), SIDE_PITCH, scale=sc), "%s_side_left.png" % sp)
        save(render(SH, math.radians(GAME_YAW - SIDE_YAW), SIDE_PITCH, scale=sc), "%s_side_right.png" % sp)
        # hops: wings spread (out / out_up flap), same back-view camera
        save(render(shade(build(sp, "out")), gy, PITCH, scale=sc), "%s_hop_0.png" % sp)
        save(render(shade(build(sp, "out_up")), gy, PITCH, scale=sc), "%s_hop_1.png" % sp)
        # face: close-up head, front-on (used at mega-hop apex + menus)
        save(render(SH, math.radians(0), math.radians(15), out=FACE_CANVAS,
                    scale=2.5 * size, cy_frac=0.46), "%s_face.png" % sp)
        # real 3D slices for the mega-hop sprite-stack
        Vf = build(sp, "folded")
        for i, sl in enumerate(stack_slices(Vf, shade(Vf))):
            save(sl, "%s_stack_%02d.png" % (sp, i))
    print("ducks generated ->", art_dir)


# ---- critters: the heron (baddie) + ducklings (the heart-melter) ---------------
def _vox_helpers(V):
    def put(x, y, z, c, only_empty=False):
        if only_empty and (x, y, z) in V:
            return
        V[(x, y, z)] = c

    def ellip(cx, cy, cz, rx, ry, rz, c, only_empty=False):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            for y in range(int(cy - ry - 1), int(cy + ry + 2)):
                for z in range(int(cz - rz - 1), int(cz + rz + 2)):
                    if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + ((z - cz) / rz) ** 2 <= 1.0:
                        put(x, y, z, c, only_empty)

    def box(x0, x1, y0, y1, z0, z1, c, only_empty=False):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    put(x, y, z, c, only_empty)
    return put, ellip, box


def build_heron(flap=0):
    """Great blue heron in a strike dive, seen from above. Head points +z
    (rendered yaw=0 so it dives DOWN the screen toward the duck)."""
    BODY = (134, 150, 170); BODYD = (100, 114, 134); COVERT = (120, 136, 156)
    COVERT2 = (110, 124, 144); SEC = (74, 84, 102); PRIM = (34, 38, 50)
    WHITE = (246, 248, 250); CREST = (20, 22, 30)
    BILL = (240, 198, 86); BILLD = (198, 152, 54)
    RUST = (162, 100, 60); LEG = (70, 60, 50); EYE = (252, 212, 70)
    V = {}
    put, ellip, box = _vox_helpers(V)
    # body: sleeker, pale belly, dark mantle line down the spine
    ellip(0, 0, 0, 3.4, 2.7, 6.0, BODY)
    ellip(0, 1.5, -0.5, 2.7, 1.8, 5.2, BODYD, only_empty=True)
    ellip(0, -1.7, 1.0, 2.6, 1.5, 4.4, WHITE, only_empty=True)
    for z in range(-5, 4):
        put(0, 3, z, CREST, only_empty=True)               # spine stripe
    # rust shoulder patches where the wings meet the body
    for s in (1, -1):
        put(3 * s, 2, 2, RUST); put(3 * s, 2, 1, RUST); put(4 * s, 2, 1, RUST)
    # huge spread wings: covert gradient -> slate secondaries -> black primaries,
    # a thin white wing-bar along the leading edge. Three flap poses for a slow,
    # SWOOPING beat: 0 = glide, 1 = upstroke (raised high), 2 = downstroke (bowed under)
    for s in (1, -1):
        for w in range(12):
            x = (3 + w) * s
            if flap == 1:
                lift = 2 + (w // 3)         # wings swept up and out
            elif flap == 2:
                lift = 1 - (w // 3)         # wings bowed beneath the body
            else:
                lift = 1 + (w // 5)         # level glide
            z0 = -4 + (w // 2)          # trailing edge sweeps forward
            z1 = 3 - (w // 4)           # leading edge sweeps back
            if w >= 9:
                col = PRIM
            elif w >= 6:
                col = SEC
            else:
                col = COVERT if w % 2 else COVERT2
            box(x, x, lift, lift + 1, z0, z1, col)
            if w < 9:
                put(x, lift + 1, z1, WHITE)                # white wing-bar
            if w >= 9:                                     # feather notches on tips
                put(x, lift, z0 - 1, PRIM)
    # extended strike neck: white with slate side-stripes, slight S-kink
    box(-1, 1, 1, 2, 5, 8, BODY)
    box(0, 0, 0, 1, 5, 9, WHITE)
    box(0, 0, 1, 2, 9, 11, WHITE)
    put(1, 2, 9, RUST); put(-1, 2, 9, RUST)                # rusty neck streak
    # head: white crown, bold black brow band sweeping to a long trailing plume
    ellip(0, 2.8, 12, 2.0, 1.8, 2.2, WHITE)
    for z in (11, 12, 13):
        put(1, 4, z, CREST); put(-1, 4, z, CREST)
        put(1, 5, z, CREST, only_empty=True); put(-1, 5, z, CREST, only_empty=True)
    for i, z in enumerate((10, 9, 8, 7)):                  # the plume, trailing up
        put(0, 4 + (i + 1) // 2, z, CREST)
    # dagger bill: bright yellow, dark tip
    box(0, 0, 2, 3, 14, 18, BILL)
    box(0, 0, 2, 2, 17, 18, BILLD)
    put(0, 2, 19, BILLD)
    # fierce yellow eyes, black pupil forward
    put(2, 3, 12, EYE); put(-2, 3, 12, EYE)
    put(2, 3, 13, CREST); put(-2, 3, 13, CREST)
    # rusty thighs + long trailing legs with toes
    for s in (1, -1):
        put(s, -1, -5, RUST); put(s, 0, -6, RUST)
        for z in range(-12, -6):
            put(s, 0 if z > -10 else 1, z, LEG)
        put(s * 2, 1, -12, LEG); put(0, 1, -13, LEG)       # toes
    return V


def build_duckling(wings="folded"):
    """A fuzzy duckling: yellow puff, dark cap, stubby everything."""
    BUFF = (244, 216, 122); BUFFD = (212, 182, 94); BELLY = (252, 240, 186)
    CAP = (176, 144, 62); BILL = (240, 162, 72); EYE = (26, 22, 18)
    V = {}
    put, ellip, box = _vox_helpers(V)
    ellip(0, 0, 0, 3.2, 2.8, 4.0, BUFF)
    ellip(0, -1.4, 0.5, 2.6, 1.8, 3.2, BELLY, only_empty=True)
    ellip(0, 1.6, -0.5, 2.4, 1.6, 3.2, BUFFD, only_empty=True)
    # fuzz speckles
    for (x, y, z) in list(V.keys()):
        if V[(x, y, z)] == BUFF and (x * 37 + y * 13 + z * 59) % 8 == 0:
            V[(x, y, z)] = BUFFD
    if wings == "out":                       # stubby flailing wing nubs
        for s in (1, -1):
            box(3 * s, 4 * s, 1, 1, -1, 1, BUFFD)
    # big head, dark cap
    ellip(0, 2.6, 2.6, 2.7, 2.5, 2.5, BUFF)
    ellip(0, 4.0, 2.2, 2.2, 1.4, 2.2, CAP, only_empty=True)
    # eyes + tiny bill
    put(2, 3, 4, EYE); put(-2, 3, 4, EYE)
    box(-1, 1, 2, 2, 5, 6, BILL)
    put(0, 1, -4, BUFFD)                     # tail tuft
    return V


def _fhash(x, z, k=0):
    """Deterministic per-column chaos for flame tongues (loops cleanly, no RNG)."""
    h = (x * 374761393 + z * 668265263 + k * 1274126177) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1103515245) & 0xFFFFFFFF
    return ((h >> 16) & 1023) / 1023.0


def build_fire(frame, nf=6):
    """ON FIRE, the Hitz way: a flame VOLUME grown from the duck's own voxels.
    A 1-voxel shell cloaks the body, then per-column tongues lick upward with
    looping noise; color runs ember red (base) to white-hot (tips). Emissive —
    no shading, no outline. Returns (whole volume, front licks that wrap OVER
    the sprite so the duck reads properly engulfed)."""
    duck = set(build("mallard", "folded").keys())
    ph = frame / float(nf) * 2.0 * math.pi
    ys = [p[1] for p in duck]
    ymin, ymax = min(ys), max(ys)
    cols = {}
    for (x, y, z) in duck:
        cols[(x, z)] = max(y, cols.get((x, z), -99))
    flame = {}
    # the cloak: shell hugging the body (skip the underwater belly rows)
    for (x, y, z) in duck:
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)):
            p = (x + dx, y + dy, z + dz)
            if p in duck or p[1] < ymin + 2:
                continue
            flame[p] = 0.15
    # tongues: every column flickers to its own beat, swaying as it rises
    for (x, z), top in cols.items():
        n1 = _fhash(x, z, 1)
        n2 = _fhash(x, z, 2)
        hgt = max(1, int(2.0 + 4.5 * n1 + 3.5 * math.sin(ph + n2 * 6.283) * n1))
        sway = math.sin(ph * 2.0 + n1 * 6.283)
        for i in range(hgt):
            t = (i + 1.0) / hgt
            wx = x + int(round(sway * t * (1.0 + n2)))
            p = (wx, top + 1 + i, z)
            if p not in duck:
                flame[p] = max(flame.get(p, 0.0), t)
    # color by tip-ness + per-voxel jitter
    V = {}
    for (x, y, z), t in flame.items():
        tt = min(1.0, t + _fhash(x, z, y) * 0.18)
        if tt < 0.25:
            c = (186, 32, 8)
        elif tt < 0.5:
            c = (234, 90, 10)
        elif tt < 0.75:
            c = (252, 158, 26)
        elif tt < 0.9:
            c = (255, 214, 70)
        else:
            c = (255, 248, 200)
        V[(x, y, z)] = c
    front = {p: c for p, c in V.items()
             if p[2] <= 0 and p[1] <= ymin + (ymax - ymin) * 0.55}
    return V, front


def build_sadie(frame=0):
    """Sadie: chocolate lab, red collar, swimming with just head/shoulders/tail out of
    the water. Faces +z (game draws her in profile crossing the river). Built from the
    reference photo: wet near-black chocolate coat, bright red collar."""
    COAT = (58, 40, 30); COATL = (84, 60, 44); COATD = (40, 27, 21)
    COLLAR = (196, 44, 38); EYE = (22, 18, 16); NOSE = (24, 20, 18)
    V = {}
    put, ellip, box = _vox_helpers(V)
    bob = 0 if frame == 0 else -1
    # shoulders/back hump: the only body above the waterline (flat-bottomed)
    for (cx, cy, cz, rx, ry, rz, c) in [
            (0, 0.5, -2, 3.6, 2.6, 6.0, COAT),
            (0, 1.8, -1, 2.8, 1.6, 4.4, COATL)]:
        for x in range(-5, 6):
            for y in range(0, 5):
                for z in range(-9, 5):
                    if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + ((z - cz) / rz) ** 2 <= 1.0:
                        put(x, y, z, c, c == COATL)
    # neck + blocky lab head
    ellip(0, 3 + bob, 4, 2.2, 2.4, 2.2, COAT)
    ellip(0, 5.2 + bob, 6, 2.6, 2.4, 2.6, COAT)
    ellip(0, 6.4 + bob, 6.4, 2.0, 1.4, 2.0, COATL, only_empty=True)   # wet sheen crown
    # square snout
    box(-1, 1, 3 + bob, 5 + bob, 8, 10, COAT)
    box(-1, 1, 4 + bob, 4 + bob, 10, 10, NOSE)
    # floppy ears, hanging
    for s in (1, -1):
        box(3 * s, 3 * s, 3 + bob, 6 + bob, 5, 7, COATD)
        put(3 * s, 2 + bob, 6, COATD)
    # the famous RED collar
    for a in range(0, 360, 16):
        x = round(2.3 * math.cos(math.radians(a)))
        y = round(3 + bob + 2.3 * math.sin(math.radians(a)))
        if (x, y, 4) in V or (x, y, 3) in V:
            put(x, y, 4, COLLAR)
    # kind eyes
    put(2, 5 + bob, 8, EYE); put(-2, 5 + bob, 8, EYE)
    # tail up like a rudder, wagging frame-to-frame
    tx = 0 if frame == 0 else 1
    for i, z in enumerate(range(-9, -13, -1)):
        put(tx * (i // 2), 1 + i, z, COAT)
    return V


def make_chuckit():
    """Sadie's beloved ball: orange with the blue band (from the photo)."""
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (12, 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ORANGE = (240, 118, 36, 255)
    ORANGED = (198, 88, 24, 255)
    BLUE = (66, 118, 200, 255)
    d.ellipse([1, 1, 10, 10], fill=ORANGE)
    d.ellipse([2, 2, 6, 6], fill=(252, 152, 70, 255))
    d.arc([1, 1, 10, 10], 110, 250, fill=ORANGED)
    d.line([(3, 9), (9, 3)], fill=BLUE, width=2)
    o = img.copy()
    px, opx = img.load(), o.load()
    for y in range(12):
        for x in range(12):
            if px[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 12 and 0 <= ny < 12 and px[nx, ny][3] > 0:
                        opx[x, y] = (30, 24, 20, 255)
                        break
    return o


def generate_critters(art_dir):
    import os

    def save(img, name):
        img.save(os.path.join(art_dir, name))

    # heron: dive pose, three flap poses (glide / upstroke / downstroke)
    for f in (0, 1, 2):
        SH = shade(build_heron(f))
        save(render(SH, math.radians(0), math.radians(55), out=76, scale=1.55),
             "heron_%d.png" % f)
    # GERALD THE IMMENSE: the boss heron, rendered big & crisp at a fiercer head-on tilt
    for f in (0, 1, 2):
        save(render(shade(build_heron(f)), math.radians(0), math.radians(42), out=132, scale=2.7),
             "gerald_%d.png" % f)
    # duckling: back view to match gameplay camera
    gy = math.radians(GAME_YAW)
    SHd = shade(build_duckling("folded"))
    save(render(SHd, gy, PITCH, out=32, scale=1.5), "duckling_idle_0.png")
    save(render(SHd, gy, PITCH - math.radians(5), out=32, scale=1.5), "duckling_idle_1.png")
    SHo = shade(build_duckling("out"))
    save(render(SHo, gy, PITCH, out=32, scale=1.5), "duckling_hop_0.png")
    save(render(SHo, gy, PITCH - math.radians(6), out=32, scale=1.5), "duckling_hop_1.png")
    # Sadie: profile view (yaw 90 = facing screen-right), two paddle frames + her ball
    for f in (0, 1):
        save(render(shade(build_sadie(f)), math.radians(90), math.radians(40), out=64, scale=1.7),
             "sadie_%d.png" % f)
    make_chuckit().save(os.path.join(art_dir, "chuckit.png"))
    # ON FIRE flame volume: 6-frame loop at the gameplay camera, emissive (no
    # shade/outline). fire_duck = whole volume (behind), fire_lick = front wrap (over)
    for f in range(6):
        Vf, Vfront = build_fire(f, 6)
        save(render(Vf, gy, PITCH, out=76, scale=1.45, outline=False), "fire_duck_%d.png" % f)
        save(render(Vfront, gy, PITCH, out=76, scale=1.45, outline=False), "fire_lick_%d.png" % f)
    print("critters generated ->", art_dir)


if __name__ == "__main__":
    import os
    generate_ducks(os.path.join(os.path.dirname(__file__), "..", "art"))
    generate_critters(os.path.join(os.path.dirname(__file__), "..", "art"))
