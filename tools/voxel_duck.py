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
    bufflehead=dict(head_scale=1.18, bill_len=16, face_paint="bufflehead"),
    pintail=dict(pin_tail=True, face_paint="pintail", long_neck=True, bill_stripe=True),
    hoodie=dict(crest=True, big_crest=True, face_paint="hoodie", eye_col=(244, 196, 60), bill_thin=True),
    canvasback=dict(red_eye=True, dark_rump=True),
    eider=dict(face_paint="eider", bill_len=15),
    golden=dict(chest_speckles=True, dark_rump=True),
    shoveler=dict(bill_len=19, bill_wide=True, eye_col=(238, 198, 60)),
    ruddy=dict(pin_tail=True, face_paint="ruddy"),
    harlequin=dict(face_paint="harlequin"),
    rubberduck=dict(),
    disco=dict(chest_speckles=True, dark_rump=True),     # SECRET unlocks
    shadow=dict(dark_rump=True, red_eye=False),
    merganser=dict(bill_thin=True, dark_rump=True),      # sleek fish-hunter: green head, red bill
    teal=dict(dark_rump=True, size=0.82),                # tiny + fast: chestnut head, green patch
    goldeneye=dict(head_scale=1.1, dark_rump=True, eye_col=(250, 210, 60)),  # gold-eyed diver
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
    if sp == "disco":  # SECRET: a neon party duck, all boogie
        return dict(
            back=(120, 40, 150), body=(214, 48, 154), belly=(250, 150, 210),
            verm_d=(96, 32, 128), verm_l=(244, 120, 196),
            nape=(40, 150, 170), head=(40, 196, 214), headh=(140, 244, 255),
            crown=(30, 140, 160), glint=(190, 250, 255),
            chest=(250, 176, 40), chestd=(220, 130, 28), chestl=(255, 210, 90),
            bill=(255, 214, 60), billd=(220, 170, 36), nail=(180, 130, 28), nostril=(210, 150, 30),
            white=(250, 235, 255), collar=(255, 240, 120),
            wing=(60, 180, 160), wingd=(40, 140, 124), primary=(150, 60, 190),
            specw=(255, 240, 120), spec=(230, 60, 160), specd=(150, 40, 120),
            tail=(96, 40, 140), tailhi=(214, 120, 230), eye=(20, 16, 24),
        )
    if sp == "shadow":  # SECRET: a midnight drake with a cold glowing stare
        return dict(
            back=(26, 26, 34), body=(40, 40, 52), belly=(64, 64, 80),
            verm_d=(20, 20, 28), verm_l=(58, 58, 76),
            nape=(30, 28, 44), head=(38, 34, 56), headh=(78, 70, 110),
            crown=(22, 20, 34), glint=(120, 110, 170),
            chest=(46, 44, 58), chestd=(30, 30, 40), chestl=(62, 60, 78),
            bill=(64, 70, 84), billd=(44, 48, 60), nail=(28, 30, 38), nostril=(40, 44, 54),
            white=(150, 160, 190), collar=(70, 74, 92),
            wing=(34, 34, 46), wingd=(22, 22, 32), primary=(14, 14, 20),
            specw=(120, 200, 230), spec=(40, 120, 150), specd=(28, 80, 104),
            tail=(20, 20, 28), tailhi=(80, 78, 104), eye=(120, 230, 255),
        )
    if sp == "merganser":  # common merganser: glossy green head, thin RED bill, crisp white body
        return dict(
            back=(28, 30, 36), body=(238, 234, 224), belly=(248, 246, 240),
            verm_d=(206, 202, 192), verm_l=(248, 244, 236),
            nape=(26, 56, 44), head=(28, 64, 48), headh=(64, 120, 86),
            crown=(22, 50, 40), glint=(120, 184, 140),
            chest=(244, 238, 226), chestd=(214, 208, 196), chestl=(250, 248, 242),
            bill=(212, 64, 48), billd=(168, 44, 34), nail=(120, 30, 24), nostril=(150, 40, 32),
            white=(248, 246, 240), collar=(248, 246, 240),
            wing=(40, 42, 50), wingd=(30, 32, 40), primary=(22, 24, 30),
            specw=(244, 242, 238), spec=(214, 214, 220), specd=(180, 180, 188),
            tail=(60, 62, 70), tailhi=(110, 112, 120), eye=(150, 30, 26),
        )
    if sp == "teal":  # green-winged teal: chestnut head w/ green eye-patch, grey body, buff vent
        return dict(
            back=(120, 122, 128), body=(176, 178, 184), belly=(206, 208, 212),
            verm_d=(110, 112, 120), verm_l=(196, 198, 204),
            nape=(54, 92, 64), head=(150, 66, 46), headh=(186, 92, 64),
            crown=(46, 84, 58), glint=(96, 150, 104),
            chest=(196, 178, 150), chestd=(168, 150, 122), chestl=(214, 198, 170),
            bill=(48, 46, 52), billd=(34, 32, 38), nail=(24, 22, 26), nostril=(44, 42, 48),
            white=(238, 236, 230), collar=(238, 236, 230),
            wing=(150, 152, 158), wingd=(120, 122, 128), primary=(92, 94, 100),
            specw=(236, 234, 228), spec=(58, 132, 92), specd=(40, 96, 66),
            tail=(90, 80, 64), tailhi=(150, 138, 116), eye=(22, 18, 20),
        )
    if sp == "goldeneye":  # common goldeneye: green-black head, bright GOLD eye, white body
        return dict(
            back=(30, 32, 38), body=(240, 238, 230), belly=(248, 246, 242),
            verm_d=(210, 208, 200), verm_l=(248, 246, 238),
            nape=(24, 44, 36), head=(26, 50, 40), headh=(50, 92, 66),
            crown=(20, 40, 34), glint=(86, 140, 100),
            chest=(244, 242, 234), chestd=(214, 212, 204), chestl=(250, 248, 244),
            bill=(40, 42, 48), billd=(28, 30, 36), nail=(20, 22, 26), nostril=(40, 42, 48),
            white=(248, 246, 242), collar=(248, 246, 242),
            wing=(44, 46, 54), wingd=(32, 34, 42), primary=(24, 26, 32),
            specw=(246, 244, 240), spec=(220, 220, 226), specd=(186, 186, 192),
            tail=(58, 60, 68), tailhi=(108, 110, 118), eye=(250, 210, 60),
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
# REAL female plumage, authored per species from the field guide. Most hens share a mottled-brown
# DABBLER body or a clean grey DIVER body; the HEAD is the big tell (and a few keep the speculum/eye).
def _drab(c):
    g = c[0] * 0.3 + c[1] * 0.59 + c[2] * 0.11
    return (min(255, int(c[0] * 0.58 + g * 0.34 + 12)),
            min(255, int(c[1] * 0.58 + g * 0.34 + 9)),
            min(255, int(c[2] * 0.58 + g * 0.30 + 5)))

# a clean blue-grey DIVER hen body (merganser/goldeneye/bufflehead/canvasback females)
_GREY_BODY = dict(back=(98, 102, 110), body=(160, 164, 172), belly=(232, 230, 226),
                  verm_d=(88, 92, 100), verm_l=(156, 160, 168), chest=(180, 184, 190),
                  chestd=(150, 154, 160), chestl=(220, 220, 222), wing=(92, 96, 104),
                  wingd=(70, 74, 82), primary=(52, 56, 64), tail=(78, 76, 74), tailhi=(118, 116, 114))

# per-species HEAD (+ a few extras). the body comes from the hen-mallard base unless grey-bodied.
_HEN_HEAD = {
    "wood":       dict(head=(112, 114, 120), headh=(142, 144, 150), crown=(94, 96, 102), nape=(98, 100, 106), glint=(186, 188, 192)),   # grey, white teardrop
    "merganser":  dict(head=(180, 100, 66), headh=(212, 132, 92), crown=(150, 82, 52), nape=(150, 84, 56), glint=(228, 152, 110)),       # rusty shaggy crest
    "goldeneye":  dict(head=(110, 82, 60), headh=(140, 108, 80), crown=(92, 68, 50), nape=(96, 72, 54), glint=(168, 140, 108)),          # chocolate brown
    "bufflehead": dict(head=(78, 74, 80), headh=(106, 102, 108), crown=(66, 62, 68), nape=(72, 68, 74), glint=(142, 140, 146)),          # dark grey, white cheek
    "canvasback": dict(head=(150, 132, 108), headh=(184, 166, 140), crown=(132, 114, 92), nape=(140, 122, 98), glint=(200, 184, 158)),   # pale grey-brown
    "hoodie":     dict(head=(124, 104, 90), headh=(154, 130, 110), crown=(156, 96, 62), nape=(146, 94, 62), glint=(190, 152, 112)),      # grey + tawny crest
    "ruddy":      dict(head=(150, 130, 104), headh=(186, 166, 138), crown=(84, 68, 52), nape=(110, 92, 70), glint=(200, 182, 150)),      # dark cap, pale cheek
    "eider":      dict(head=(150, 116, 80), headh=(182, 148, 108), crown=(120, 90, 62), nape=(132, 100, 70), glint=(196, 166, 124)),     # warm barred brown
}
_GREY_HEN = ("merganser", "goldeneye", "bufflehead", "canvasback")

def hen_palette(sp):
    if sp == "mallard":
        return palette("hen")                        # the hand-tuned hen mallard
    p = dict(palette("hen"))                          # mottled-brown DABBLER body as the base
    if sp in _GREY_HEN:
        p.update(_GREY_BODY)                          # diver hens get a clean grey body instead
    src = palette(sp)
    for k in ("bill", "billd", "nail", "nostril", "spec", "specd", "specw", "eye"):
        if k in src:
            p[k] = src[k]                             # keep the drake's bill, speculum + eye colour
    if sp in _HEN_HEAD:
        p.update(_HEN_HEAD[sp])
    else:                                             # golden/harlequin/shoveler/pintail/teal: subtle brown hen head
        p.update(dict(head=(132, 112, 84), headh=(162, 142, 112), crown=(106, 88, 64), nape=(116, 96, 70), glint=(182, 162, 132)))
    return p


def feminize(P):                                     # legacy shim -> the real per-species path is hen_palette
    return P


def build(sp="mallard", wings="folded", beak_open=False, elder=False, hen_override=False):
    """Return {(x,y,z): rgb}.  x=right, y=up, z=head(+).  Shared duck geometry,
    species palette + flags (crest / head patch / pin tail / face paint)."""
    spec = SPECIES[sp]
    hen = spec.get("hen", False)
    P = palette(sp)
    if hen_override and sp != "hen":                 # render this drake as his HEN (real per-species plumage)
        P = hen_palette(sp)
        if sp == "mallard":
            hen = True                               # the hen mallard also gets her drab-head geometry
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

    if elder:
        # THE ANCIENT DUCK: a long flowing white beard draped from the chin over
        # the chest to a forked tip, plus two bushy brows. Built last so it sits
        # proud of the body.
        BW = (238, 240, 248); BS = (198, 202, 218); BH = (254, 254, 255)
        for yy in range(-13, 5):
            p = (yy + 13) / 18.0               # 0 = dangling tip, 1 = up at the chin
            cz = 8.0 + 5.0 * p                 # sits PROUD on the chest, up to the chin
            rad = 1.1 + 3.8 * p                # broad mane at the face, tapering to a point
            for xx in range(-6, 7):
                for zz in range(int(cz - rad * 1.7), int(cz + rad * 1.7) + 1):
                    if (xx / max(rad, 0.7)) ** 2 + ((zz - cz) / max(rad * 1.3, 0.7)) ** 2 <= 1.0:
                        c = BW
                        if xx <= -3:                       # soft form shadow on one side
                            c = BS
                        if abs(xx) <= 1 and yy >= -8:      # bright comb down the middle
                            c = BH
                        put(xx, yy, zz, c)
        # a gently forked, curling tip dangling below
        for (tx, ty, tz, tc) in [(-2, -13, 9, BW), (2, -14, 8, BW), (0, -12, 10, BH),
                                  (-3, -12, 8, BS), (3, -13, 8, BS), (0, -15, 8, BW)]:
            put(tx, ty, tz, tc)
        # bushy white eyebrows perched over the eyes
        for sx in (ex, -ex):
            ellip(sx, 9 + NY, 11.0, 1.9, 1.0, 1.4, BW)
            put(sx, 10 + NY, 11, BH)
            put(sx - 1, 9 + NY, 12, BS)
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


def render_wear(Vduck_sh, Vhat, yaw, pitch, out=BODY_CANVAS, scale=1.45, cy_frac=0.5):
    """Render the HAT depth-sorted against the duck, keeping ONLY pixels where a hat voxel is
    frontmost. The head correctly occludes the hat's far side, and — unlike a duck-vs-(duck+hat)
    diff — not a single duck pixel survives, so there are no stray green-head specks around it."""
    cy_, sy_ = math.cos(yaw), math.sin(yaw)
    cp, sp_ = math.cos(pitch), math.sin(pitch)
    pts = []
    for src, is_hat in ((Vduck_sh, False), (Vhat, True)):
        for (x, y, z), c in src.items():
            x1 = x * cy_ + z * sy_
            z1 = -x * sy_ + z * cy_
            y2 = y * cp - z1 * sp_
            z2 = y * sp_ + z1 * cp
            pts.append((z2, x1, y2, c, is_hat))
    pts.sort(key=lambda p: p[0])
    H = out * S
    img = Image.new("RGBA", (H, H), (0, 0, 0, 0))
    msk = Image.new("L", (H, H), 0)
    d = ImageDraw.Draw(img); dm = ImageDraw.Draw(msk)
    cx, cyc, vs = H / 2.0, H * cy_frac, scale * S
    r = vs * 0.62
    for _, x1, y2, c, is_hat in pts:
        sx, syy = cx + x1 * vs, cyc - y2 * vs
        box = [sx - r, syy - r, sx + r, syy + r]
        d.rectangle(box, fill=c + (255,))
        dm.rectangle(box, fill=(255 if is_hat else 0))   # a duck voxel in front UN-marks the hat
    res = Image.new("RGBA", (H, H), (0, 0, 0, 0))
    res.paste(img, (0, 0), msk)                          # keep only where the hat is frontmost
    return _crisp_outline(res, out, True)


def _stack_frame(V, canvas=30):
    """The canvas mapping (sc, offsets, bounds) a voxel set slices into — shared so a
    HAT slices into the exact same frame as its duck and rides the tumble pixel-locked."""
    xs = [p[0] for p in V]; zs = [p[2] for p in V]; ys = [p[1] for p in V]
    xmin, xmax, zmin, zmax = min(xs), max(xs), min(zs), max(zs)
    w, h = xmax - xmin + 1, zmax - zmin + 1
    sc = max(1, (canvas - 4) // max(w, h))
    return dict(xmin=xmin, zmax=zmax, ymin=min(ys), ymax=max(ys), sc=sc,
                ox=(canvas - w * sc) // 2, oz=(canvas - h * sc) // 2, canvas=canvas)


def _slice_at(SH, yv, fr):
    """One cross-section image at height yv, using a fixed frame `fr`. Returns (img, any_px)."""
    im = Image.new("RGBA", (fr["canvas"], fr["canvas"]), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    any_px = False
    for (x, y, z), c in SH.items():
        if y != yv:
            continue
        ix = fr["ox"] + (x - fr["xmin"]) * fr["sc"]
        iy = fr["oz"] + (fr["zmax"] - z) * fr["sc"]   # head(+z) toward top of image
        dd.rectangle([ix, iy, ix + fr["sc"] - 1, iy + fr["sc"] - 1], fill=c + (255,))
        any_px = True
    return im, any_px


def stack_slices(V, SH, canvas=30):
    """Real horizontal cross-sections (bottom->top) for in-game sprite-stacking."""
    fr = _stack_frame(V, canvas)
    out = []
    for yv in range(fr["ymin"], fr["ymax"] + 1):
        im, _ = _slice_at(SH, yv, fr)
        out.append(im)
    return out


def hat_stack_slices(Vduck, Hhat, SHhat, canvas=30):
    """Slice a HAT into the DUCK's stack frame, so each hat slice rides the same MEGA
    tumble as the duck slice at the same index. Returns [(index, img), ...] non-empty only.
    index = yv - duck_ymin, so it lines up with (and can climb ABOVE) the duck's own slices."""
    fr = _stack_frame(Vduck, canvas)
    ytop = max(fr["ymax"], max(p[1] for p in Hhat))
    out = []
    for yv in range(fr["ymin"], ytop + 1):
        im, any_px = _slice_at(SHhat, yv, fr)
        if any_px:
            out.append((yv - fr["ymin"], im))
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
        SHq = shade(build(sp, "folded", beak_open=True))   # same body, beak agape
        for i in range(24):
            save(render(SH, math.radians(i * 15), math.radians(HERO_PITCH), scale=sc), "%s_spin_%02d.png" % (sp, i))
            # beak-open twin of every angle, so a quack reads in ANY orientation
            save(render(SHq, math.radians(i * 15), math.radians(HERO_PITCH), scale=sc), "%s_spinq_%02d.png" % (sp, i))
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
        # --- the HEN variant: same body, feminized plumage (the toggle renders these) ---
        if sp not in ("hen", "rubberduck", "disco", "shadow"):
            hp = sp + "hen"
            SHh = shade(build(sp, "folded", hen_override=True))
            SHhq = shade(build(sp, "folded", beak_open=True, hen_override=True))
            save(render(SHh, gy, PITCH, scale=sc), "%s_idle_0.png" % hp)
            save(render(SHh, gy, PITCH - math.radians(4), scale=sc), "%s_idle_1.png" % hp)
            save(render(SHh, math.radians(HERO_YAW), math.radians(HERO_PITCH), scale=sc), "%s_hero.png" % hp)
            save(render(SHhq, math.radians(HERO_YAW), math.radians(HERO_PITCH), scale=sc), "%s_quack.png" % hp)
            for i in range(24):
                save(render(SHh, math.radians(i * 15), math.radians(HERO_PITCH), scale=sc), "%s_spin_%02d.png" % (hp, i))
                save(render(SHhq, math.radians(i * 15), math.radians(HERO_PITCH), scale=sc), "%s_spinq_%02d.png" % (hp, i))
            for i, off in enumerate(BANK_OFF):
                save(render(SHh, math.radians(GAME_YAW + off), PITCH, scale=sc), "%s_bank_%d.png" % (hp, i))
            save(render(SHh, math.radians(GAME_YAW + 15), PITCH, scale=sc), "%s_turn_left.png" % hp)
            save(render(SHh, math.radians(GAME_YAW - 15), PITCH, scale=sc), "%s_turn_right.png" % hp)
            save(render(SHh, math.radians(GAME_YAW + SIDE_YAW), SIDE_PITCH, scale=sc), "%s_side_left.png" % hp)
            save(render(SHh, math.radians(GAME_YAW - SIDE_YAW), SIDE_PITCH, scale=sc), "%s_side_right.png" % hp)
            save(render(shade(build(sp, "out", hen_override=True)), gy, PITCH, scale=sc), "%s_hop_0.png" % hp)
            save(render(shade(build(sp, "out_up", hen_override=True)), gy, PITCH, scale=sc), "%s_hop_1.png" % hp)
            save(render(SHh, math.radians(0), math.radians(15), out=FACE_CANVAS, scale=2.5 * size, cy_frac=0.46), "%s_face.png" % hp)
    # THE ANCIENT DUCK: a golden elder with a flowing white beard, for the shrine.
    # two frames so his beak flaps while he talks.
    elder = shade(build("golden", "folded", elder=True))
    save(render(elder, math.radians(HERO_YAW), math.radians(HERO_PITCH), scale=1.45), "elder.png")
    elder_talk = shade(build("golden", "folded", beak_open=True, elder=True))
    save(render(elder_talk, math.radians(HERO_YAW), math.radians(HERO_PITCH), scale=1.45), "elder_talk.png")
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


def build_heron(flap=0, beak_open=False):
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
    # dagger bill: bright yellow, dark tip (GAPES open when beak_open — a menacing squawk)
    if beak_open:
        box(0, 0, 3, 4, 14, 18, BILL)                      # upper mandible, raised
        box(0, 0, 0, 1, 15, 18, BILL)                      # lower mandible, dropped wide
        box(0, 0, 4, 4, 17, 18, BILLD); put(0, 0, 19, BILLD)
        box(0, 0, 2, 2, 14, 15, (190, 60, 50))             # red gullet inside the gape
    else:
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


def build_chuckit():
    """The CHUCK-IT ball — a bright orange sphere with a blue equator band + glossy shine."""
    ORANGE = (240, 110, 30); ORANGEH = (255, 158, 84); BLUE = (40, 98, 204); BLUEH = (96, 156, 240)
    V = {}
    put, ellip, box = _vox_helpers(V)
    R = 5
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            for z in range(-R, R + 1):
                if (x * x + y * y + z * z) ** 0.5 <= R + 0.25:
                    c = BLUE if abs(y) <= 1 else ORANGE        # blue equator band
                    put(x, y, z, c, c == BLUE)
    for (x, y, z) in [(-2, 3, -2), (-1, 4, -2), (-2, 4, -1), (-1, 3, -3), (0, 4, -2)]:
        if (x, y, z) in V: V[(x, y, z)] = ORANGEH               # glossy top highlight
    for (x, y, z) in [(-1, 0, -3), (-2, 0, -2)]:
        if (x, y, z) in V: V[(x, y, z)] = BLUEH
    return V

def build_sadie_run(frame=0):
    """Sadie TROTTING — side profile chocolate lab, 8-frame SMOOTH cycle. Body + head stay put;
    each leg traces a CONTINUOUS gait (front + rear half a cycle out of phase) so the motion flows
    instead of snapping between stiff poses. Faces +z (rendered facing right)."""
    COAT = (80, 51, 34); COATL = (112, 76, 52); COATD = (54, 34, 23)
    COLLAR = (176, 138, 84); NOSE = (26, 20, 18); PAW = (96, 66, 46)
    AMBER = (158, 110, 56); EYE = (22, 18, 16); TONGUE = (236, 120, 150)
    V = {}
    put, ellip, box = _vox_helpers(V)
    TAU = 2 * math.pi
    ph = (frame % 8) / 8.0 * TAU
    ellip(0, 5, 0, 3.2, 3.0, 5.8, COAT)
    ellip(0, 4.8, -5, 3.4, 3.2, 2.6, COAT)
    ellip(0, 5.2, 6, 3.2, 3.0, 2.4, COAT)
    ellip(0, 7.3, 0, 2.6, 1.2, 5.4, COATL, only_empty=True)
    ellip(0, 7.2, 7.6, 2.4, 2.6, 1.8, COAT)
    ellip(0, 9.4, 10.2, 2.7, 2.6, 2.7, COAT)
    box(-1, 1, 8, 10, 11, 13, COAT)
    box(-1, 1, 7, 8, 13, 13, NOSE)
    ellip(0, 10.5, 10.4, 2.0, 1.3, 2.0, COATL, only_empty=True)
    edown = round(math.sin(ph) * 1.0)                   # ears bob gently with the stride
    for s in (1, -1):
        box(2 * s, 3 * s, 7 - edown, 10 - edown, 8, 9, COATD)
    for s in (1, -1):                                   # small DARK kind eyes (no glowing-yellow amber blob)
        put(s * 2, 9, 11, EYE); put(s * 2, 9, 12, EYE)
    put(0, 6, 13, TONGUE); put(0, 6, 14, TONGUE)
    for a in range(0, 360, 16):
        x = round(2.3 * math.cos(math.radians(a))); y = round(6 + 2.3 * math.sin(math.radians(a)))
        if (x, y, 6) in V:
            put(x, y, 6, COLLAR)
    def leg(theta, z_fwd, z_back, hip):
        t = theta % TAU
        if t < math.pi:                                 # STANCE: paw planted, sweeping back
            pz = z_fwd + (z_back - z_fwd) * (t / math.pi); py = -5.0
        else:                                           # SWING: paw lifted, swinging forward (knee folds up)
            u = (t - math.pi) / math.pi
            pz = z_back + (z_fwd - z_back) * u; py = -5.0 + 2.6 * math.sin(u * math.pi)
        for s in (1, -1):
            for k in range(0, 5):
                kk = k / 4.0
                fold = math.sin(kk * math.pi) * (1.5 if py > -4 else 0.5)   # knee bow, more while swinging
                zz = round(pz + (hip - pz) * kk + (fold if hip > 0 else -fold))
                yy = round(py + (1 - py) * kk)
                rad = 0.6 + 0.4 * kk
                ellip(s * 2.1, yy, zz, rad, rad, rad, COAT if k >= 2 else COATD)
            ellip(s * 2.1, round(py), round(pz) + (1 if pz > 0 else -1), 0.9, 0.7, 1.1, PAW)
    leg(ph, 7, 4, 5)                                     # front pair
    leg(ph + math.pi, -4, -7, -5)                        # rear pair, out of phase
    for i in range(6):
        put(0, round(6 - i * 0.4), -6 - i, COAT if i < 4 else COATD)
    return V

def build_sadie(frame=0, ball=True, dry=False, legs=False):
    """Sadie: chocolate lab, red collar, swimming with just head/shoulders/tail out of
    the water. Faces +z (game draws her in profile crossing the river). Built from the
    reference photo: wet near-black chocolate coat, bright red collar."""
    if ball and not dry:
        COAT = (58, 40, 30); COATL = (84, 60, 44); COATD = (40, 27, 21)   # wet, near-black (the river enemy)
    else:
        COAT = (80, 51, 34); COATL = (112, 76, 52); COATD = (54, 34, 23)  # rich DARK chocolate (dry — the real Sadie)
    COLLAR = (210, 52, 46) if ball else (176, 138, 84); EYE = (22, 18, 16); NOSE = (26, 20, 18)
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
    if legs:                                             # SITTING lab: front legs + the haunches she rests on (for the land greeter)
        PAW = (104, 72, 50)   # chocolate paws (she's all brown — NO white feet)
        ellip(0, -3, -5, 3.8, 3.6, 3.2, COAT)            # the seated rump / haunches
        ellip(0, -1.5, -6.0, 2.8, 2.4, 2.2, COATL, only_empty=True)
        for s in (1, -1):                                # two front legs reaching down to the floor
            for yy in range(-7, 1):
                ellip(s * 2.5, yy, 4.0, 1.2, 1.0, 1.3, COAT if yy > -5 else COATD)
            ellip(s * 2.5, -7, 4.3, 1.2, 0.8, 1.3, PAW)  # the paw (trimmer — no clown feet)
            ellip(s * 3.0, -6, -5.5, 1.0, 0.8, 1.2, PAW, only_empty=True)   # smaller back paw peeking from the haunch
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
        x = round(1.9 * math.cos(math.radians(a)))
        y = round(1 + bob + 1.9 * math.sin(math.radians(a)))   # low on the throat, clear of the face
        if (x, y, 4) in V or (x, y, 3) in V:
            put(x, y, 4, COLLAR)
    if ball:
        # her beloved CHUCK-IT ball, clamped PROUDLY in her jaws (orange w/ blue band)
        BALL = (240, 118, 36); BALLH = (252, 152, 70); BAND = (66, 118, 200)
        ellip(0, 3 + bob, 11.5, 1.7, 1.7, 1.7, BALL)
        put(-1, 4 + bob, 12, BALLH); put(0, 4 + bob, 12, BALLH)      # glossy highlight
        put(1, 3 + bob, 13, BAND); put(0, 2 + bob, 13, BAND); put(-1, 3 + bob, 13, BAND)   # blue band
    else:
        # ball-free: a CLOSED snoot — a real lower jaw fills the mouth (no gaping maw) + a tiny tongue tip
        box(-1, 1, 1 + bob, 2 + bob, 8, 11, COAT)                    # lower jaw, closing the mouth
        put(0, 2 + bob, 11, COAT); put(0, 3 + bob, 11, NOSE)        # rounded chin + nose tip
        put(0, 1 + bob, 12, (236, 120, 150))                        # just a tiny tongue tip peeking out
        for zz in range(8, 11):                                      # a lighter SNOOT so her face pops
            put(0, 4 + bob, zz, COATL, only_empty=True)
        put(0, 5 + bob, 10, COATL, only_empty=True)                  # bridge of the nose
    # small KIND eyes: a dark base + a warm AMBER iris (her signature — warm, NOT a startled white glint)
    put(2, 5 + bob, 8, EYE); put(-2, 5 + bob, 8, EYE)
    if not ball:
        put(2, 5 + bob, 9, (158, 110, 56)); put(-2, 5 + bob, 9, (158, 110, 56))   # warm amber iris
        put(2, 4 + bob, 9, EYE); put(-2, 4 + bob, 9, EYE)                          # a dark lower lid grounds it
    # tail up like a rudder, wagging frame-to-frame
    tx = 0 if frame == 0 else 1
    for i, z in enumerate(range(-9, -13, -1)):
        put(tx * (i // 2), 1 + i, z, COAT)
    return V


def build_hawk(frame=0, beak_open=False):
    """RUSTY the red-tailed hawk: the game's friendly know-it-all GUIDE, caught
    mid glide-flap as he swoops across the sky to drop a tip. Built to read as a
    red-tail at a glance from a 3/4 side angle: dark-brown back & head, a pale
    belly with a smudged dark belly-band, the SIGNATURE rusty-red fanned tail, a
    bright yellow hooked beak + yellow talons, and one fierce dark eye under a
    heavy brow. Faces +z (he travels head-first across the top of the screen).
    3 frames: 0 = level glide, 1 = wings up (upstroke), 2 = wings down."""
    BROWN = (108, 74, 46); BROWND = (78, 52, 32); BROWNL = (140, 100, 64)
    PALE = (238, 228, 206); PALED = (208, 196, 170); BAND = (120, 86, 58)
    RUST = (176, 80, 44); RUSTH = (206, 108, 60); RUSTD = (138, 58, 32)
    PRIM = (46, 36, 30); SEC = (84, 60, 42)
    BEAK = (244, 198, 70); BEAKD = (40, 34, 30); CERE = (240, 198, 70)
    TALON = (240, 204, 80); CLAW = (34, 30, 28)
    EYE = (40, 30, 24); EYEW = (228, 196, 80); BROW = (54, 38, 26)
    V = {}
    put, ellip, box = _vox_helpers(V)
    # ---- body: brown back over a pale streaked belly ----
    ellip(0, 0, 0, 2.8, 2.4, 5.2, BROWN)
    ellip(0, 1.4, -0.4, 2.2, 1.5, 4.4, BROWND, only_empty=True)        # dark mantle
    ellip(0, -1.6, 0.6, 2.4, 1.4, 4.2, PALE, only_empty=True)          # pale underside
    # the red-tail's smudgy dark BELLY-BAND across the lower breast
    for x in range(-3, 4):
        if (x * 7) % 3 != 0:
            put(x, -2, 1, BAND); put(x, -1, 0, BAND, only_empty=True)
    # fine dark streaks down the pale breast
    for x in range(-2, 3):
        if x % 2 == 0:
            put(x, -1, 3, BROWND); put(x, -2, 2, BROWND)
    # ---- broad rounded buteo wings, fingered primaries, 3 flap poses ----
    for s in (1, -1):
        for w in range(11):
            x = (2 + w) * s
            if frame == 1:
                lift = 2 + (w // 2)         # raised high on the upstroke
            elif frame == 2:
                lift = -1 - (w // 3)        # bowed beneath on the downstroke
            else:
                lift = 1 + (w // 6)         # near-level glide, wings held flat & wide
            z0 = -4 + (w // 2)              # trailing edge sweeps forward
            z1 = 3 - (w // 3)              # broad leading edge, swept back at the tips
            if w >= 8:
                col = PRIM                  # dark fingered primaries
            elif w >= 5:
                col = SEC
            else:
                col = BROWN if w % 2 else BROWNL
            box(x, x, lift, lift + 1, z0, z1, col)
            if 3 <= w <= 7:                 # pale covert bar along the forewing
                put(x, lift + 1, z1, PALED)
            if w >= 8:                      # splayed "fingers" at the wingtip
                put(x, lift, z0 - 1, PRIM)
                if w == 10:
                    put(round(x * 1.12), lift, z0 - 2, PRIM)
    # ---- the SIGNATURE rusty-red fanned tail (short & broad, behind the body) ----
    for i, z in enumerate(range(-6, -12, -1)):
        spread = 1 + i                      # fans out wider toward the tip
        for x in range(-spread, spread + 1):
            c = RUSTH if x == 0 else (RUST if abs(x) < spread else RUSTD)
            put(x, 0, z, c)
            put(x, -1, z, RUSTD, only_empty=True)
    for x in range(-5, 6):                  # dark terminal band on the tail tip
        if abs(x) <= 5:
            put(x, 0, -11, BROWND, only_empty=True)
    # ---- short neck + compact rounded raptor head, mostly dark brown ----
    ellip(0, 1.4, 5.8, 2.0, 1.9, 2.2, BROWN)
    ellip(0, 2.6, 6.2, 1.6, 1.4, 1.7, BROWND, only_empty=True)         # dark crown cap
    # heavy brow ridge giving the fierce raptor scowl
    for s in (1, -1):
        put(2 * s, 2, 6, BROW); put(2 * s, 2, 7, BROW)
    # fierce forward-set eye: bright gold rim hugging a dark pupil, peeking out
    # high on the head so the glint reads from the 3/4 top-down camera
    for s in (1, -1):
        put(2 * s, 2, 7, EYEW); put(2 * s, 2, 8, EYE)
        put(2 * s, 1, 8, EYE)
    # ---- small yellow cere + a short forward beak that curls to a dark HOOK ----
    put(0, 1, 8, CERE); put(1, 1, 8, CERE, only_empty=True); put(-1, 1, 8, CERE, only_empty=True)
    put(0, 1, 9, BEAK)                                                 # beak juts forward
    put(0, 0, 10, BEAKD)                                              # tip curls down to a dark hook
    if beak_open:                                                     # SCREECH: lower mandible drops, red maw gapes
        MAW = (164, 54, 52)
        put(0, -1, 9, BEAK); put(0, -2, 9, BEAKD)                    # dropped lower beak
        put(0, 0, 9, MAW); put(0, -1, 8, MAW)                        # the open red gape
    # ---- yellow legs + grabby TALONS tucked under in flight ----
    for s in (1, -1):
        put(s, -2, 0, BROWNL)                                          # feathered thigh
        put(s, -3, 1, TALON); put(s, -3, 2, TALON)
        put(s, -4, 2, CLAW); put(s * 2, -3, 3, CLAW)                  # curled claws
        put(s, -4, 0, CLAW)
    return V


def build_boat():
    """CHRISSY — a LONG, sleek CHRIS-CRAFT runabout from above: near-black varnished hull, a rich
    mahogany deck striped with thin GOLD plank-seams, GREEN leather cockpits, a chrome split
    windshield, chrome hardware, and the stars-&-stripes flying off the transom. ~3:1 length:beam."""
    HULL = (32, 21, 17); HULLH = (58, 40, 30); KEEL = (18, 12, 10)
    MAH = (138, 60, 36); MAHH = (170, 88, 54); MAHD = (108, 50, 30); GOLD = (208, 174, 104)
    GREEN = (46, 86, 62); GREENH = (70, 116, 86)
    CHROME = (216, 222, 232); GLASS = (150, 202, 216)
    FLAGR = (202, 48, 48); FLAGW = (238, 238, 242); FLAGB = (44, 56, 124); POLE = (150, 112, 62)
    V = {}
    put, ellip, box = _vox_helpers(V)

    def plank(x, z):                                       # mahogany deck w/ THIN gold plank-seams (run bow->stern)
        if x % 4 == 0:
            return GOLD
        return MAHH if (x % 2 == 1) else MAH

    BOW, STERN = 18, -14                                   # 33 long over an 11 beam = sleek ~3:1
    for z in range(STERN, BOW + 1):
        if z >= 13:                                        # long raked BOW, tapering to a fine point
            half = max(0, 5 - (z - 13))
        elif z <= -11:                                     # gentle barrel-back STERN
            half = max(3, 5 + (z + 11))
        else:
            half = 5
        if half <= 0:
            put(0, 0, z, HULLH); put(0, 1, z, MAHH)        # the very bow tip
            continue
        for x in range(-half, half + 1):
            put(x, -1, z, KEEL)                            # dark underbody
            put(x, 0, z, HULLH if abs(x) == half else HULL)  # near-black varnished topsides
            if abs(x) == half - 1:
                put(x, 1, z, GOLD)                         # a gold SHEER stripe just inside the hull
            else:
                put(x, 1, z, plank(x, z))                  # planked mahogany deck
    for (z0, z1) in [(2, 6), (-6, -2)]:                    # FORWARD + AFT cockpits — recessed GREEN openings
        for z in range(z0, z1 + 1):
            for x in range(-3, 4):
                put(x, 1, z, GREEN if abs(x) < 3 else GREENH)
                put(x, 0, z, GREENH, only_empty=True)
    for x in range(-3, 4):                                 # green seat-back between the cockpits
        put(x, 2, -1, GREENH)
    for x in range(-4, 5):                                 # chrome-framed split WINDSHIELD ahead of the helm
        put(x, 2, 8, GLASS); put(x, 3, 8, GLASS); put(x, 4, 8, CHROME)
    for yy in (2, 3):
        put(-4, yy, 8, CHROME); put(0, yy, 8, CHROME); put(4, yy, 8, CHROME)   # posts incl. the centre split
    put(0, 2, 16, CHROME); put(0, 1, 15, CHROME)           # chrome bow cleat
    for s in (-3, 3):
        put(s, 2, 11, CHROME); put(s, 2, -10, CHROME)      # chrome vents fore + aft
    for y in range(1, 7):                                  # the FLAG: a short varnished pole at the transom
        put(0, y, -14, POLE)
    for yy in (5, 6):
        for zz in (-14, -13, -12):
            c = FLAGB if (yy == 6 and zz == -14) else (FLAGR if yy == 5 else FLAGW)
            put(0, yy, zz, c)
    return V

def build_icon(iid):
    """A small voxel object per power-up/boon id. Built facing +z; rendered at a slight tilt."""
    V = {}
    put, ellip, box = _vox_helpers(V)
    GOLD = (244, 202, 70); GOLDD = (198, 150, 44); GOLDH = (255, 234, 150)
    STEEL = (150, 172, 202); STEELD = (92, 112, 152); STEELH = (206, 220, 240)
    RED = (214, 72, 60); WHITE = (240, 240, 244); YEL = (250, 222, 84)
    FLAME = (246, 142, 44); FLAMEY = (252, 214, 96); FLAMER = (214, 70, 40)
    GREEN = (96, 202, 112); CREAM = (246, 232, 202); CYAN = (108, 210, 255)
    BROWN = (150, 100, 60); GREY = (120, 124, 134); PINK = (240, 120, 150)

    def plate(shape, col, cold, depth=2):           # extrude a 2D (x,y)->bool shape along z
        for x in range(-8, 9):
            for y in range(-8, 9):
                if shape(x, y):
                    for z in range(depth):
                        put(x, y, z, col if z == depth - 1 else cold)

    if iid == "shield":
        def sh(x, y):
            w = 6.0 if y >= -1 else 6.0 * (1.0 - (abs(y + 1) / 7.0) ** 1.3)
            return abs(x) <= w and -7 <= y <= 6
        plate(sh, STEEL, STEELD, 2)
        ellip(0, 1, 2, 2.0, 2.0, 1.0, GOLD); put(0, 1, 3, GOLDH)
        for y in range(-6, 6):
            put(0, y, 2, STEELH, only_empty=True)
    elif iid == "coin":
        ellip(0, 0, 0, 6.4, 6.4, 1.6, GOLD)
        ellip(0, 0, 1.7, 3.6, 3.6, 0.6, GOLDD)
        box(-1, 1, -3, 3, 2, 2, GOLDH)              # a little duck/$ emboss
        box(-2, 2, 0, 0, 2, 2, GOLDH)
    elif iid == "bolt":
        for (a, b) in [((3, 7), (-2, 1)), ((-2, 1), (2, 1)), ((2, 1), (-3, -7))]:   # a connected zigzag
            n = 14
            for k in range(n):
                t = k / (n - 1)
                bx = int(round(a[0] + (b[0] - a[0]) * t)); by = int(round(a[1] + (b[1] - a[1]) * t))
                for dx in (-1, 0, 1):
                    put(bx + dx, by, 0, GOLDD); put(bx + dx, by, 1, YEL)
    elif iid == "magnet":
        for a in range(0, 181, 12):                 # the horseshoe arc
            ang = math.radians(a)
            mx = int(round(math.cos(ang) * 5.0)); my = int(round(math.sin(ang) * 5.0))
            ellip(mx, my, 0, 1.4, 1.4, 1.2, RED)
        for side in (-5, 5):                         # the two pole tips (steel)
            box(side - 1, side + 1, -7, -4, 0, 1, STEEL)
    elif iid == "egg":
        for y in range(-7, 8):
            r = 4.6 * math.sqrt(max(0.0, 1.0 - (y / 7.2) ** 2))
            if y > 0:
                r *= 1.0 - 0.18 * (y / 7.0)          # gently narrowed top
            ellip(0, y, 0, r, 0.1, r, CREAM)
        for (sx, sy) in [(-2, 2), (1, -1), (2, 3)]:  # speckles
            put(sx, sy, int(2.0), BROWN)
    elif iid == "flame":
        for y in range(-7, 7):
            t = (y + 7) / 14.0
            r = 4.4 * math.sin(t * math.pi) * (1.0 if y < 3 else 0.7)
            col = FLAMER if y < -3 else (FLAME if y < 2 else FLAMEY)
            ellip(0, y, 0, max(0.6, r), 0.1, max(0.6, r), col)
    elif iid == "arrow":
        def ar(x, y):
            return (abs(x) <= (5 - max(0, y) ) and y >= 0 and abs(x) <= 5 - y * 0 and y <= 3 and abs(x) <= (5 - (y))) \
                or (abs(x) <= 2 and -7 <= y <= 0)
        plate(lambda x, y: (y >= 0 and y <= 5 and abs(x) <= 5 - y) or (abs(x) <= 2 and y < 0 and y >= -7), CYAN, STEELD, 2)
    elif iid == "star":
        n = 5
        for k in range(n * 2):
            ang = -math.pi / 2 + k * math.pi / n
            rr = 7.0 if k % 2 == 0 else 3.0
            x = int(round(math.cos(ang) * rr)); y = int(round(math.sin(ang) * rr))
            ellip(x, y, 0, 1.6, 1.6, 1.2, YEL if k % 2 == 0 else GOLDD)
        ellip(0, 0, 0, 3.0, 3.0, 1.4, GOLDH)
    elif iid == "clover":
        for (lx, ly) in [(0, 4), (4, 0), (0, -4), (-4, 0)]:
            ellip(lx, ly, 0, 2.8, 2.8, 1.2, GREEN)
        box(0, 0, -8, -4, 0, 1, (70, 150, 80))      # stem
    elif iid == "chick":
        ellip(0, -1, 0, 4.4, 4.0, 3.2, YEL)         # body
        ellip(0, 4, 1, 2.6, 2.6, 2.4, YEL)          # head
        put(1, 5, 3, (30, 30, 36))                  # eye
        box(2, 4, 4, 4, 1, 2, FLAME)                # beak
    elif iid == "crown":
        for x in range(-7, 8):                       # the band
            for z in range(2):
                put(x, -4, z, GOLDD if z == 0 else GOLD)
            put(x, -3, 1, GOLD)
        for (px, ph) in [(-7, 3), (-3, 5), (0, 6), (3, 5), (7, 3)]:   # five spikes
            for k in range(ph):
                put(px, -3 + k, 1, GOLD); put(px, -3 + k, 0, GOLDD)
            put(px, -3 + ph, 1, GOLDH)               # tipped highlight
        for (jx, jy) in [(-3, 2), (0, 3), (3, 2)]:   # jewels on the spikes
            put(jx, jy, 2, RED)
    elif iid == "heart":
        def hh(x, y):
            xf = x / 6.0; yf = -y / 6.0
            return (xf * xf + yf * yf - 1.0) ** 3 - xf * xf * yf * yf * yf < 0.0 and abs(x) <= 7 and -7 <= y <= 6
        plate(hh, RED, (160, 40, 40), 2)
    elif iid == "fork":
        box(-1, 1, -7, 4, 0, 1, STEEL)
        for fx in (-3, 0, 3):
            box(fx, fx, 4, 7, 0, 1, STEEL)
    elif iid == "wing":
        for k in range(6):                          # a fanned wing of feathers
            box(-6 + k * 2, -6 + k * 2 + 1, -2 - k, 3 - k, 0, 1, WHITE if k % 2 else STEEL)
    elif iid == "spring":
        for k in range(40):                          # a dense steel helix coil
            ang = k * math.radians(34)
            yy = -7.0 + k * 0.36
            ellip(math.cos(ang) * 4.0, yy, math.sin(ang) * 2.6, 1.3, 0.9, 1.3,
                  STEEL if math.sin(ang) > -0.2 else STEELD)
    elif iid == "cookie":
        ellip(0, 0, 0, 6.2, 6.2, 1.8, (196, 146, 86))
        ellip(0, 0, 1.4, 5.2, 5.2, 0.6, (214, 168, 108))
        for (cx, cy) in [(-3, 2), (2, 3), (3, -2), (-2, -3), (0, 0), (-4, -1)]:   # choc chips
            put(cx, cy, 2, (70, 44, 30)); put(cx, cy, 1, (70, 44, 30))
    elif iid == "cannon":
        box(-2, 6, -2, 2, 0, 3, (54, 56, 66))        # the barrel
        ellip(6, 0, 1.5, 1.6, 1.6, 1.6, (40, 40, 48))
        ellip(-5, -1, 1.5, 3.0, 3.0, 2.6, (30, 30, 36))   # the cannonball
        ellip(-6, 0, 3.0, 1.0, 1.0, 0.6, (90, 90, 100))
    elif iid == "die":
        box(-5, 5, -5, 5, 0, 4, WHITE)               # the cube
        for (px, py) in [(-3, 3), (0, 0), (3, -3), (3, 3), (-3, -3)]:   # pips
            put(px, py, 4, (40, 40, 48))
    elif iid == "ball":
        ellip(0, 1, 0, 5.2, 5.2, 5.2, (236, 96, 80))
        ellip(-1.6, 2.6, 3.2, 1.6, 1.6, 0.8, (252, 180, 160))   # highlight
        for x in range(-5, 6):
            put(x, 1, 0, (180, 60, 50), only_empty=True)
    elif iid == "loaf":
        ellip(0, 0, 0, 6.0, 4.0, 4.0, (198, 144, 76))
        ellip(0, 1.6, 0, 5.0, 2.6, 3.2, (230, 182, 112), only_empty=True)
        for cz in (-2, 2):                           # score marks
            for x in range(-4, 5):
                put(x, 4, cz, (140, 92, 46))
    elif iid == "burst":
        ellip(0, 0, 0, 3.0, 3.0, 2.5, YEL)
        for a in range(0, 360, 45):                  # radiating spikes
            ang = math.radians(a)
            for r in (4, 5, 6):
                put(int(round(math.cos(ang) * r)), int(round(math.sin(ang) * r)), 0, FLAME if r < 6 else FLAMEY)
    elif iid == "bowl":
        for y in range(-5, 2):                        # an empty bowl (hollow)
            r = 6.0 * math.sqrt(max(0.0, 1.0 - ((y - 1) / 7.0) ** 2))
            for a in range(0, 360, 14):
                ang = math.radians(a)
                if y <= 0:
                    put(int(round(math.cos(ang) * r)), y, int(round(math.sin(ang) * r * 0.7)), (170, 120, 80))
    elif iid == "gem":
        for y in range(-7, 6):                        # a faceted crystal
            r = 5.0 * (1.0 - abs(y) / 8.0) if y < 0 else 5.0 * (1.0 - y / 6.0)
            ellip(0, y, 0, max(0.5, r), 0.1, max(0.5, r), CYAN if y % 2 == 0 else (140, 200, 240))
        ellip(-1.5, 2.0, 1.5, 1.4, 1.4, 0.6, WHITE)   # glint
    elif iid == "gust":
        for (yy, ln) in [(3, 6), (0, 8), (-3, 5)]:    # swirling wind lines
            for x in range(-ln, ln):
                put(x, yy, 0, STEELH); put(x, yy, 1, STEEL)
            put(ln - 1, yy + 2, 0, STEELH); put(ln, yy + 1, 0, STEELH)   # the curl
    elif iid == "birds":
        for (bx, by) in [(0, 3), (-4, 0), (4, 0)]:    # a little V-formation
            put(bx, by, 0, (40, 44, 54)); put(bx - 2, by - 1, 0, (40, 44, 54)); put(bx + 2, by - 1, 0, (40, 44, 54))
            put(bx - 1, by, 1, STEELD); put(bx + 1, by, 1, STEELD)
    elif iid == "zen":
        for a in range(0, 360, 45):                   # a calm lotus flower
            ang = math.radians(a)
            ellip(int(round(math.cos(ang) * 4)), int(round(math.sin(ang) * 4)), 0, 2.0, 0.1, 2.0, PINK)
        ellip(0, 0, 0.5, 2.4, 0.1, 2.4, (250, 220, 120))   # the golden centre
    elif iid == "tiny":
        ellip(0, -1, 0, 3.2, 2.8, 2.6, YEL)           # a wee duck body
        ellip(1.5, 2.5, 1, 2.0, 2.0, 1.8, YEL)        # head
        put(3, 3, 2, (30, 30, 36))                    # eye
        box(3, 4, 2, 2, 1, 2, FLAME)                  # tiny beak
    elif iid == "feathershield":                     # _shield charge — shield + feather crest
        def _fs(x, y):
            w = 6.0 if y >= -1 else 6.0 * (1.0 - (abs(y + 1) / 7.0) ** 1.3)
            return abs(x) <= w and -7 <= y <= 6
        plate(_fs, STEELH, STEEL, 2)
        for i in range(8):
            put(0, 5 - i, 2, CYAN)
        for i in range(1, 4):
            put(-i, 4 - i, 2, CYAN); put(i, 4 - i, 2, CYAN)
    elif iid == "lifevest":                          # jacket — an orange LIFE JACKET
        box(-5, 5, -6, 5, 0, 2, (240, 130, 40))
        box(-1, 1, -6, 5, 0, 3, (36, 40, 50))
        box(-5, 5, -4, -3, 2, 3, (250, 214, 96)); box(-5, 5, 1, 2, 2, 3, (250, 214, 96))
        box(-6, -3, 4, 6, 0, 2, (236, 120, 36)); box(3, 6, 4, 6, 0, 2, (236, 120, 36))
    elif iid == "goslingguard":                      # gosling_guard — a duckling holding a little shield
        ellip(0, -1, 0, 3.4, 3.6, 2.8, YEL)           # gosling body, front + centre
        ellip(0, 3, 1, 2.4, 2.4, 2.2, YEL)            # head
        put(1, 4, 3, (30, 30, 36)); box(2, 4, 3, 3, 2, 3, FLAME)   # eye + beak
        plate(lambda x, y: -7 <= x <= -3 and -5 <= y <= 4, STEEL, STEELD, 3)   # shield it carries
        put(-5, 0, 3, GOLDH)
    elif iid == "snackwing":                         # snackhawk — a fanned wing gripping a snack
        for i in range(6):                            # primaries fanning down-right
            box(-6 + i, -6 + i, 5 - i * 2, 5, 1, 2, STEELH if i % 2 else WHITE)
        ellip(-2, 3, 1, 2.6, 2.2, 2.0, STEELD)        # the wing shoulder
        ellip(4, -5, 2, 2.4, 2.4, 2.0, (224, 170, 96))  # the snagged snack (clear + big)
        put(4, -5, 4, CREAM)
    elif iid == "vformation":                        # wingducks — a V of three little flyers
        for (cx, cy) in [(0, 4), (-4, -1), (4, -1)]:
            put(cx, cy, 1, WHITE)
            put(cx - 1, cy - 1, 1, STEELH); put(cx + 1, cy - 1, 1, STEELH)
            put(cx - 2, cy - 2, 1, WHITE); put(cx + 2, cy - 2, 1, WHITE)
    elif iid == "earlybird":                         # earlybird — a sunrise + a perky bird
        ellip(0, -5, 0, 6.0, 0.8, 1.0, GOLD)
        for a in (30, 65, 100, 150):
            ang = math.radians(a)
            put(int(round(math.cos(ang) * 6)), -5 + int(round(math.sin(ang) * 6)), 0, GOLDH)
        ellip(-1, 0, 1, 3.0, 3.0, 2.6, (120, 92, 60))
        ellip(1, 3, 2, 2.0, 2.0, 1.8, (120, 92, 60))
        put(2, 4, 3, WHITE); box(3, 5, 3, 3, 2, 2, FLAME)
    elif iid == "wildfire":                          # wildfire — a spreading triple blaze
        for fx in (-4, 0, 4):
            for i in range(6):
                ellip(fx, -4 + i, 0, 2.4 - i * 0.3, 1.4, 1.6, FLAMER if i < 2 else (FLAME if i < 4 else FLAMEY))
    elif iid == "phoenix":                           # phoenix — a bird made of flame
        ellip(0, 0, 0, 2.4, 3.4, 2.2, FLAMER)
        for s in (1, -1):
            for i in range(5):
                put(s * (2 + i), i - 1, 0, FLAME if i < 3 else FLAMEY)
                put(s * (2 + i), i, 1, FLAMEY)
        for i in range(4):
            put(0, 4 + i, 0, FLAME if i < 2 else FLAMEY)
        put(1, 1, 2, YEL); put(-1, 1, 2, YEL)
    elif iid == "thermal":                           # thermal — a thermometer + heat waves
        box(-1, 1, -6, 3, 0, 2, WHITE)
        ellip(0, -5, 0, 2.4, 2.4, 1.6, RED)
        for y in range(-5, 2):
            put(0, y, 1, RED)
        for s in (1, -1):
            for y in (3, 5):
                put(s * 4, y, 0, FLAME); put(s * 5, y + 1, 0, FLAMEY); put(s * 5, y - 1, 0, FLAMEY)
    elif iid == "loftgauge":                         # loft — a gauge bar filling up
        box(-3, 3, -7, 7, 0, 1, STEELD)
        for y in range(-6, 5):
            box(-2, 2, y, y, 1, 2, GREEN if y < 2 else GOLD)
        put(0, 6, 2, GOLDH)
    elif iid == "hourglass":                         # warmup — an hourglass
        for y in range(-6, 7):
            w = max(1, abs(y) // 2)
            box(-w, w, y, y, 0, 2, GOLD if abs(y) > 4 else CREAM)
        box(-5, 5, 6, 7, 0, 2, BROWN); box(-5, 5, -7, -6, 0, 2, BROWN)
        ellip(0, -2, 1, 1.0, 1.0, 1.0, GOLDH)
    elif iid == "doublearrow":                       # double — two up-arrows
        for off in (-3, 3):
            for i in range(5):
                box(off - (4 - i), off + (4 - i), -6 + i, -6 + i, 0, 2, CYAN)
            box(off - 1, off + 1, -3, 4, 0, 2, CYAN)
    elif iid == "paperplane":                        # flyer — a paper airplane
        plate(lambda x, y: (y <= 4 - abs(x) and y >= -2) or (abs(x) <= 1 and -6 <= y <= 4), WHITE, STEELD, 2)
        for i in range(6):
            put(0, 4 - i, 2, STEELD)
    elif iid == "flag":                              # trailblazer — a planted pennant
        for y in range(-7, 6):
            put(-3, y, 0, BROWN)
        plate(lambda x, y: -3 < x <= 4 and 1 <= y <= 5, RED, (170, 50, 44), 2)
        put(4, 6, 0, GOLDH)
    elif iid == "swoosh":                            # slipstream — speed lines
        for i in range(11):
            x = -6 + i
            put(x, 3, 0, CYAN); put(x, 0, 0, CYAN if i < 9 else WHITE); put(x, -3, 0, CYAN)
        for y in (-3, 0, 3):
            put(5, y, 0, WHITE)
    elif iid == "clutch":                            # clutch — three eggs in a nest
        for (cx, cy) in [(-3, -1), (0, 1), (3, -1)]:
            ellip(cx, cy, 0, 2.6, 3.0, 2.2, CREAM)
        for x in range(-6, 7):
            put(x, -4, 0, BROWN)
    elif iid == "egghead":                           # egghead — a brainy egg with specs
        ellip(0, 0, 0, 4.4, 5.4, 3.6, CREAM)
        ellip(-2, 1, 3, 1.4, 1.4, 0.6, STEELD); ellip(2, 1, 3, 1.4, 1.4, 0.6, STEELD)
        put(-2, 1, 4, CYAN); put(2, 1, 4, CYAN)
        for x in range(-2, 3):
            put(x, -2, 3, (120, 90, 60))
    elif iid == "trio":                              # trio — three little chicks
        for cx in (-4, 0, 4):
            ellip(cx, -1, 0, 2.2, 2.4, 1.8, YEL)
            ellip(cx, 2, 1, 1.5, 1.5, 1.4, YEL)
            put(cx + 1, 3, 2, (30, 30, 36))
    elif iid == "conga":                             # school — a conga line trailing behind a leader
        for i, cx in enumerate((-6, -1, 4)):
            ellip(cx, 2 - i * 2, 0, 1.9 - i * 0.2, 2.0, 1.5, YEL)   # shrinking, descending = a line in tow
            put(cx + 2, 3 - i * 2, 2, (30, 30, 36))
            if i < 2:
                put(cx + 3, 1 - i * 2, 1, GOLDD)      # a little dotted trail between them
    elif iid == "pouch":                             # pockets — a coin pouch
        ellip(0, -1, 0, 5.0, 5.4, 4.4, BROWN)
        for x in range(-3, 4):
            put(x, 5, 1, (110, 74, 44))
        ellip(0, 6, 0, 1.6, 1.2, 1.4, BROWN)
        ellip(0, 0, 3, 2.4, 2.4, 0.6, GOLD); box(-1, 1, -1, 1, 4, 4, GOLDH)
    elif iid == "warhelm":                           # warlord — a spiked war helm
        ellip(0, 1, 0, 5.0, 4.4, 4.4, STEELD)
        box(-6, 6, -1, 0, 0, 3, GREY)
        for i in range(5):
            put(0, 5 + i, 0, RED if i < 3 else FLAMEY)
        box(-1, 1, -4, 0, 4, 5, (30, 30, 36))
    elif iid == "trampoline":                        # springy — a duckling on a trampoline
        box(-6, 6, -1, 0, 0, 2, STEEL)
        for x in range(-5, 6):
            put(x, 0, 2, CYAN)
        box(-6, -5, -5, -1, 0, 2, STEELD); box(5, 6, -5, -1, 0, 2, STEELD)
        ellip(0, 4, 1, 2.0, 2.0, 1.8, YEL); put(1, 5, 2, (30, 30, 36))
    elif iid == "breadbasket":                       # basket — a basket of loaves
        for x in range(-5, 6):
            put(x, -3, 0, BROWN); put(x, -5, 0, (120, 80, 48))
        box(-5, 5, -5, -2, 0, 2, BROWN)
        ellip(-2, 0, 1, 2.4, 2.0, 2.0, (210, 150, 80)); ellip(2, 1, 1, 2.2, 1.8, 1.8, (224, 170, 96))
        ellip(0, 2, 2, 2.0, 1.6, 1.6, CREAM)
    elif iid == "shockring":                         # aftershock — concentric shock rings
        for r in (2.0, 4.0, 6.0):
            for a in range(0, 360, 24):
                ang = math.radians(a)
                put(int(round(math.cos(ang) * r)), int(round(math.sin(ang) * r)), 0, FLAMEY if r < 3 else (FLAME if r < 5 else FLAMER))
        ellip(0, 0, 1, 1.4, 1.4, 1.0, WHITE)
    elif iid == "trashcan":                          # TRASH MAGNET — a dented tin BIN
        for y in range(-7, 4):
            ellip(0, y, 0, 4.4, 0.5, 4.4, GREY if y % 2 == 0 else STEELD)   # ribbed body
        ellip(0, 4, 0, 5.0, 0.9, 5.0, STEEL)         # lid
        ellip(0, 5.4, 0, 1.5, 1.0, 1.5, STEELH)      # knob
        put(3, 4, 3, GREEN); put(-2, 5, 2, CREAM)    # junk poking out
    elif iid == "sack":                              # PACK RAT — a bulging burlap SACK of hoarded junk
        ellip(0, -1, 0, 5.2, 5.6, 5.0, BROWN)
        ellip(0, -1, 3, 3.4, 3.6, 0.6, (120, 80, 48))
        for x in range(-2, 3):
            put(x, 5, 1, (110, 74, 44))              # cinched neck
        ellip(0, 6.5, 0, 1.8, 1.4, 1.6, BROWN)       # tied top
        put(2, 7, 2, GREY); put(-1, 8, 1, STEEL)     # junk sticking out
    elif iid == "slingshot":                         # JUNK SLINGER — a Y-fork slingshot + a loaded pebble
        for y in range(-7, 1):
            put(0, y, 0, BROWN); put(0, y, 1, (120, 80, 48))   # handle
        for i in range(5):
            put(-1 - i // 2, i, 0, BROWN); put(1 + i // 2, i, 0, BROWN)   # forks
        for x in range(-3, 4):
            put(x, 4, 1, (60, 50, 44))               # the band
        ellip(0, 3, 2, 1.4, 1.4, 1.4, GREY)          # the junk pebble
    elif iid == "tire":                              # DUMPSTER DIVE — a black TIRE w/ a steel hubcap
        for a in range(0, 360, 18):
            ang = math.radians(a)
            ellip(int(round(math.cos(ang) * 4.6)), int(round(math.sin(ang) * 4.6)), 0, 1.7, 1.7, 1.6, (40, 40, 48))
        ellip(0, 0, 0.5, 2.6, 2.6, 1.2, STEEL)       # hubcap
        ellip(0, 0, 1.6, 1.2, 1.2, 0.6, STEELH)
    elif iid == "junkshield":                        # SCRAP SHELL — a riveted hubcap shield (NOT the clean steel one)
        ellip(0, 0, 0, 6.2, 6.2, 1.8, GREY)
        ellip(0, 0, 1.8, 4.0, 4.0, 0.6, STEELD)
        for a in range(0, 360, 45):
            ang = math.radians(a)
            put(int(round(math.cos(ang) * 5)), int(round(math.sin(ang) * 5)), 2, STEELH)   # rivets
        box(-2, 1, -1, 2, 2, 2, (150, 90, 50))       # a rusty patch
        ellip(0, 0, 2.2, 1.5, 1.5, 0.6, FLAMER)      # red boss
    else:
        ellip(0, 0, 0, 5.5, 5.5, 2.5, STEEL)        # fallback gem
        ellip(0, 0, 2.0, 3.0, 3.0, 0.8, STEELH)
    return V


# which voxel icon each power-up / boon id uses (ids sharing a look point at one model)
ICON_MAP = {
    "shield": "shield", "_shield": "shield", "jacket": "shield", "goosedown": "wing", "gosling_guard": "shield",
    "gold": "coin", "pockets": "coin", "nestegg": "egg", "clutch": "egg", "egghead": "egg",
    "thunder": "bolt", "magnet": "magnet", "hotwheels": "flame", "wildfire": "flame", "phoenix": "flame", "thermal": "flame",
    "mega": "arrow", "loft": "arrow", "warmup": "arrow", "double": "arrow", "wild": "star", "lucky": "clover",
    "duckling": "chick", "trio": "chick", "school": "chick", "apex": "crown", "warlord": "crown",
    "secondwind": "heart", "buffet": "fork", "snackhawk": "wing", "wingducks": "wing", "earlybird": "wing",
}


def build_thwomp(slam=False):
    """A DEADFALL — a heavy gnarled hardwood log that drops on your lane. Thicker, darker and knottier
    than a normal river log, with splintered cut-ends + a little moss. (no faces, no stone — it's WOOD.)"""
    BARK = (98, 68, 42); BARKD = (64, 44, 28); BARKL = (130, 94, 60)
    KNOT = (48, 32, 20); MOSS = (96, 128, 78); RING = (158, 120, 80); SPLINTER = (176, 138, 96)
    V = {}
    put, ellip, box = _vox_helpers(V)
    R = 4.6
    for x in range(-11, 12):                               # a thick log cylinder lying along x
        rr = R if abs(x) < 10 else R - 1.4                 # ends taper a touch
        for y in range(-6, 7):
            for z in range(-6, 7):
                if (y / rr) ** 2 + (z / rr) ** 2 <= 1.0:
                    c = BARKL if y > 1.8 else (BARKD if y < -1.8 else BARK)
                    put(x, y, z, c)
    for ex in (-11, 11):                                   # end-grain rings on the splintered cut faces
        for y in range(-5, 6):
            for z in range(-5, 6):
                d = math.sqrt(y * y + z * z)
                if d <= 4.4:
                    put(ex, y, z, RING if int(d) % 2 == 0 else BARKD)
        put(ex + (1 if ex > 0 else -1), 0, 0, SPLINTER)    # a poking splinter
    for (kx, ky, kz) in [(-5, 3, 1), (2, 2, 4), (6, -2, 3), (-2, -3, 2), (8, 1, -2), (-8, 0, 3)]:
        put(kx, ky, kz, KNOT); put(kx, ky - 1, kz, KNOT, only_empty=True)   # dark knots
    for gx in range(-9, 10, 2):                            # bark grain ridges along the top
        put(gx, 4, 1, BARKD, only_empty=True)
    for (mx, mz) in [(-7, 4), (1, 5), (4, 4), (-3, 5), (7, 4), (-1, 4)]:    # moss clumps
        put(mx, 5, mz, MOSS); put(mx, 4, mz, (74, 104, 64), only_empty=True)
    if slam:                                               # the slam frame: a few stress cracks split the bark
        for (cx, cz) in [(-2, 3), (3, 4), (-6, 2), (5, 3)]:
            put(cx, 5, cz, KNOT); put(cx, 4, cz, KNOT)
    return V
def build_bread():
    """THE MAGIC BREAD — a plump round artisan SOURDOUGH BOULE: deep golden crust shading dark at the
    hearth-base, a clean cross-score bloomed open to a pale crumb, and a light dusting of flour."""
    CRUST = (190, 130, 66); CRUSTD = (142, 90, 44); CRUSTH = (216, 162, 96)
    CRUMB = (244, 222, 178); BLOOM = (226, 188, 134); FLOUR = (240, 232, 214)
    RX, RY, RZ = 8.0, 5.2, 8.0
    V = {}
    put, ellip, box = _vox_helpers(V)
    for x in range(-9, 10):                                     # the round domed loaf, flat-ish hearth base
        for y in range(-5, 8):
            for z in range(-9, 10):
                if (x / RX) ** 2 + (y / RY) ** 2 + (z / RZ) ** 2 <= 1.0 and y >= -4:
                    c = CRUSTH if y >= 3 else (CRUSTD if y <= -2 else CRUST)   # lighter crown, dark base
                    put(x, y, z, c)
    for x in range(-7, 8):                                      # seal a flat bottom so it sits like a hearth loaf
        for z in range(-7, 8):
            if (x / RX) ** 2 + (z / RZ) ** 2 <= 0.82:
                put(x, -4, z, CRUSTD)
    for x in range(-9, 10):                                     # paint the TOP surface: cross-score + flour
        for z in range(-9, 10):
            ty = None
            for y in range(7, -5, -1):
                if (x, y, z) in V:
                    ty = y; break
            if ty is None:
                continue
            r = math.sqrt((x / RX) ** 2 + (z / RZ) ** 2)
            if (abs(x) <= 1 or abs(z) <= 1) and r < 0.8:        # the cross-score, bloomed open + a raised ear
                put(x, ty, z, BLOOM)
                put(x, ty + 1, z, CRUMB, only_empty=True)
            elif r < 0.66 and (x * 7 + z * 3) % 5 == 0:         # clean flour speckle on the crown
                put(x, ty, z, FLOUR)
    return V


def build_loon(bob=0):
    """LUCIEN — a common loon DJ, 3/4 front (head toward +z). Glossy black, white-checkered
    back, the signature white necklace, a dagger bill, deep-red eyes, and DJ headphones."""
    BLK = (26, 28, 36); BLKH = (44, 48, 60); WHT = (238, 242, 248)
    BILL = (20, 22, 28); EYE = (214, 38, 34); HP = (40, 36, 58); CYAN = (120, 212, 255)
    V = {}
    put, ellip, box = _vox_helpers(V)
    ny = bob                                                # head-bob offset (DJ nod)
    # sleek body, low and elongated
    ellip(0, 0, 0, 3.6, 2.7, 6.4, BLK)
    ellip(0, 1.6, -0.4, 3.0, 1.8, 5.4, BLKH, only_empty=True)   # glossy back sheen
    ellip(0, -1.9, 0.6, 3.0, 1.5, 4.8, WHT, only_empty=True)    # white breast/belly
    # checkered back — the loon's giveaway
    for (x, z) in [(-2, 3), (1, 2), (2, 4), (-1, 0), (0, 5), (2, -2), (-2, -3), (1, -4)]:
        put(x, 3, z, WHT); put(x, 2, z, WHT, only_empty=True)
    # neck rising from the front, curving up toward the head
    for i in range(5):
        ellip(0, 2 + i + ny * (i / 4.0), int(4 - i * 0.2), 1.9 - i * 0.06, 1.8, 1.9 - i * 0.06, BLK)
    # white NECKLACE banding the lower neck
    for a in range(10):
        ang = a * (math.tau / 10.0)
        put(int(round(math.cos(ang) * 2.0)), 3 + ny, int(round(4 + math.sin(ang) * 2.0)), WHT if a % 2 == 0 else BLK)
    # head + dagger bill
    hy = 8 + ny; hz = 3
    ellip(0, hy, hz, 2.8, 2.8, 3.0, BLK)
    ellip(0, hy + 1.4, hz - 1.0, 2.0, 1.6, 2.0, BLKH, only_empty=True)
    for i in range(10):                                     # the long dagger bill, tapering to a point
        zz = hz + 2 + i
        put(0, hy, zz, BILL)
        if i < 6:
            put(0, hy - 1, zz, BILL)
        if i < 3:
            put(0, hy + 1, zz, BILL, only_empty=True); put(1, hy, zz, BILL, only_empty=True); put(-1, hy, zz, BILL, only_empty=True)
    for s in (1, -1):                                       # deep red eyes
        put(s * 2, hy + 1, hz + 1, EYE); put(s * 2, hy + 1, hz + 2, EYE)
    # DJ HEADPHONES: ear cups + a band over the crown, one cup glowing
    for s in (1, -1):
        ellip(s * 3, hy, hz, 1.3, 1.7, 1.4, HP)
    for x in range(-3, 4):
        put(x, hy + 3, hz, HP); put(x, hy + 3, hz - 1, HP, only_empty=True)
    put(3, hy, hz + 1, CYAN); put(3, hy, hz, CYAN); put(-3, hy, hz + 1, CYAN)
    return V


def build_lucien_dj(pose="scratch_r_d", gape=False):
    """LUCIEN at his DECKS — an upright BLACK loon DJ behind a detailed voxel console. `pose` choreographs
    his wings: scratch either platter, tap the mixer, or throw a wing (or both) UP for the drop."""
    BLK = (24, 26, 34); BLKH = (66, 74, 100); WHT = (246, 248, 252)
    BILL = (22, 24, 32); EYE = (236, 60, 52); HP = (54, 52, 78); CYAN = (130, 222, 255)
    WOOD = (96, 72, 128); WOODH = (146, 116, 184); WOODD = (64, 46, 88)
    REC = (52, 52, 66); RED = (224, 72, 70); CHROME = (216, 222, 232); LIME = (150, 240, 120); PINK = (250, 120, 200)
    V = {}
    put, ellip, box = _vox_helpers(V)
    # === the DJ CONSOLE — chunky, detailed ===
    box(-11, 11, -11, -1, 3, 11, WOOD)                      # body
    box(-12, 12, -1, 0, 2, 12, WOODH)                       # top, slight overhang
    box(-11, 11, -11, -10, 3, 11, WOODD)                    # dark base
    for x in range(-12, 13, 2):                             # glowing LED strip along the front lip
        put(x, -1, 12, CYAN if x % 4 == 0 else PINK)
    for x in range(-10, 11, 2):                             # a little EQUALIZER on the console face
        bh = 1 + (abs(x) % 5)
        for y in range(-9, -9 + bh):
            put(x, y, 11, LIME if y < -7 else (CYAN if y < -5 else PINK))
    for sx in (-14, 14):                                    # SPEAKERS flanking the console
        box(sx - 1, sx + 1, -10, 2, 4, 10, (40, 38, 52))
        ellip(sx, 3, 7, 1.6, 2.2, 1.6, (26, 26, 34))       # the woofer cone
        ellip(sx, 4, 7, 0.7, 0.9, 0.7, CHROME)
    # twin turntables
    for rx in (-6, 6):
        ellip(rx, 0, 7, 3.4, 0.5, 3.4, REC)
        ellip(rx, 0.6, 7, 1.1, 0.4, 1.1, RED)
        for a in range(0, 360, 60):
            ang = math.radians(a)
            put(rx + int(round(math.cos(ang) * 2.6)), 1, 7 + int(round(math.sin(ang) * 2.6)), CHROME)
    # the MIXER between the decks: knobs + faders
    box(-2, 2, 0, 1, 5, 10, (34, 34, 44))
    for kx in (-1, 1):
        put(kx, 2, 6, CHROME); put(kx, 2, 8, CYAN)         # two knobs
    for fx in (-1, 0, 1):
        put(fx, 2, 9, CHROME)                              # fader caps
    # === LUCIEN, upright behind the decks ===
    ellip(0, 6, -2, 3.2, 4.4, 2.8, BLK)
    ellip(0, 4, -1, 2.4, 2.4, 2.2, WHT, only_empty=True)   # white breast
    for (x, z) in [(-2, -3), (1, -3), (2, -1), (-1, -2), (0, -4)]:
        put(x, 8, z, WHT, only_empty=True)                 # checkered back
    for i in range(3):
        ellip(0, 9 + i, -2 + int(i * 0.2), 1.7, 1.7, 1.7, BLK)
    hy = 13
    # a head TILT for the hype poses (chin up on the drop)
    htilt = 2 if gape else (1 if ("up" in pose or pose == "drop") else 0)   # chin UP on a gape so the open mouth faces us
    ellip(0, hy + htilt, -1, 2.7, 2.7, 2.8, BLK)
    ellip(0, hy + 1.2 + htilt, -2.0, 1.9, 1.5, 1.8, BLKH, only_empty=True)
    BILLH = (92, 100, 122); TONGUE = (244, 110, 150); TONGUED = (210, 70, 116)   # steel ridge so the bill reads
    g = 2 if gape else 0
    for i in range(10):                                    # UPPER mandible — longer, lit top ridge + a little width
        yy = hy - i // 3 + htilt + g
        put(0, yy, 1 + i, BILLH if i < 6 else BILL)
        put(1, yy, 1 + i, BILL, only_empty=True); put(-1, yy, 1 + i, BILL, only_empty=True)
    for i in range(6):                                     # LOWER mandible (drops wide open on a gape)
        put(0, hy - 1 - i // 3 + htilt - g, 1 + i, BILL)
    if gape:                                               # a bright PINK TONGUE filling the open gape
        for i in range(4):
            put(0, hy - 1 + htilt, 2 + i, TONGUE if i < 3 else TONGUED)
    put(2, hy + 1 + htilt, 0, EYE); put(-2, hy + 1 + htilt, 0, EYE)
    for s in (1, -1):
        ellip(s * 3, hy + htilt, -1, 1.3, 1.7, 1.4, HP)
    for x in range(-3, 4):
        put(x, hy + 3 + htilt, -1, HP)
    put(3, hy + htilt, 0, CYAN); put(-3, hy + htilt, 0, CYAN)
    for x in range(-2, 3):
        put(x, 9, 0, WHT, only_empty=True)                 # necklace

    def wing(shoulder, target):                            # a tapering feathered wing arm
        for i in range(7):
            f = i / 6.0
            ellip(int(round(shoulder[0] + (target[0] - shoulder[0]) * f)),
                  int(round(shoulder[1] + (target[1] - shoulder[1]) * f)),
                  int(round(shoulder[2] + (target[2] - shoulder[2]) * f)),
                  1.6 - f * 0.5, 1.1 - f * 0.3, 1.6 - f * 0.5, BLKH if i < 5 else BLK)

    TUCK_R = (5, 3, -3); TUCK_L = (-5, 3, -3)              # wings folded at the sides
    DECK_R = (6, 1, 7); DECK_L = (-6, 1, 7); MIXER = (1, 2, 7)
    UP_R = (7, 17, 1); UP_L = (-7, 17, 1)                  # thrown up for the drop
    targets = {
        "scratch_r_d": ((3, 6, -1), DECK_R, (-3, 6, -1), TUCK_L),
        "scratch_r_u": ((3, 6, -1), (6, 2, 9), (-3, 6, -1), TUCK_L),
        "scratch_l_d": ((3, 6, -1), TUCK_R, (-3, 6, -1), DECK_L),
        "scratch_l_u": ((3, 6, -1), TUCK_R, (-3, 6, -1), (-6, 2, 9)),
        "tap": ((3, 6, -1), MIXER, (-3, 6, -1), TUCK_L),
        "wing_up": ((3, 6, -1), UP_R, (-3, 6, -1), TUCK_L),
        "drop": ((3, 6, -1), UP_R, (-3, 6, -1), UP_L),
    }
    rsh, rtg, lsh, ltg = targets.get(pose, targets["scratch_r_d"])
    wing(rsh, rtg)
    wing(lsh, ltg)
    return V


def build_snapz(frame=0, variant="boss"):
    """SNAPZ: a BOLD, stylized snapping-turtle — big blocky head, a strong hooked
    beak, huge angry eyes, a jagged keeled shell with a serrated rim, and a thick
    spiked tail. Reads as a snapper at a glance. Gapes wider per frame. Faces +z.

    variant="boss": SNAPZ himself — a hulking MUDDY brown snapper with burning RED eyes.
    variant="turtle": the lesser river hazard — a smaller mossy-GREEN snapper, gold-eyed."""
    if variant == "turtle":                              # the common river snapping turtle: mossy green
        SHELL = (52, 96, 56); SHELLH = (90, 140, 82); SHELLD = (30, 58, 36); SPIKE = (38, 72, 46)
        SKIN = (138, 156, 96); SKIND = (98, 116, 68); SKINH = (176, 194, 128)
        EYEW = (250, 248, 236); EYE = (250, 210, 50); PUP = (16, 16, 20); BROW = (34, 58, 38)
        TAIL = (58, 100, 60)
    else:                                                # SNAPZ the boss: muddy brown, RED-eyed
        SHELL = (84, 64, 42); SHELLH = (122, 98, 64); SHELLD = (52, 40, 26); SPIKE = (66, 50, 32)
        SKIN = (112, 96, 70); SKIND = (80, 66, 48); SKINH = (150, 130, 98)
        EYEW = (250, 226, 214); EYE = (224, 40, 30); PUP = (60, 8, 8); BROW = (40, 30, 20)
        TAIL = (78, 60, 40)
    BEAK = (238, 222, 152); BEAKD = (196, 178, 110); HOOK = (214, 198, 132)
    MAW = (184, 62, 72); TONGUE = (214, 112, 122)
    CLAW = (244, 238, 212)
    V = {}
    put, ellip, box = _vox_helpers(V)
    gape = [0, 2, 4][frame]                               # a modest jaw drop, not a dangling box
    # ---- thick SPIKED tail jutting out the back ----
    for i, z in enumerate(range(-22, -10)):
        t = i / 11.0
        r = 1.2 + 2.6 * t
        ellip(0, 0.4 + t * 1.2, z, r, r, 1.4, TAIL)
        if i % 2 == 0:                                    # dorsal spikes
            put(0, round(2.0 + t * 2.4), z, SPIKE)
            put(0, round(2.8 + t * 2.4), z, SHELLD)
    # ---- bold domed shell with a hex-scute pattern, keel spikes + serrated rim ----
    for x in range(-12, 13):
        for y in range(-1, 12):
            for z in range(-14, 4):
                if (x / 10.5) ** 2 + ((y - 1) / 7.0) ** 2 + ((z + 5) / 8.5) ** 2 <= 1.0:
                    put(x, y, z, SHELL)
    ellip(0, 6.5, -5, 8.0, 4.6, 6.6, SHELLH, only_empty=True)   # top sheen
    for (x, y, z) in list(V.keys()):                      # bold plate seams (big hexes)
        if V[(x, y, z)] in (SHELL, SHELLH):
            if (x + 30) % 5 == 0 or (z + 30) % 5 == 0:
                V[(x, y, z)] = SHELLD
    for z in range(-12, 2, 2):                            # central keel of spikes
        yk = round(9.0 - (z + 12) * 0.06)
        put(0, yk, z, SPIKE); put(0, yk + 1, z, SHELLH)
    # serrated rim: pointed scutes sticking out around the shell's edge
    import math as _m
    for a in range(0, 360, 24):
        rx = round(10.5 * _m.cos(_m.radians(a)))
        rz = round(8.0 * _m.sin(_m.radians(a))) - 5
        put(rx, 1, rz, SPIKE)
        put(round(rx * 1.12), 1, round((rz + 5) * 1.12) - 5, SHELLD)
    # ---- short thick neck + BIG blocky head ----
    for z in range(3, 7):
        ellip(0, 2.8, z, 4.4, 3.6, 1.6, SKIN)
    for i, z in enumerate(range(6, 15)):
        t = i / 8.0
        ellip(0, 3.0 + t * 1.4, z, 5.2 - 1.8 * t, 4.4 - 1.2 * t, 1.6, SKIN)
    ellip(0, 6.6, 11, 3.4, 1.8, 3.0, SKINH, only_empty=True)   # lit crown
    for (x, y, z) in list(V.keys()):                          # scaly skin speckle
        if V[(x, y, z)] == SKIN and (x * 13 + y * 7 + z * 5) % 7 == 0:
            V[(x, y, z)] = SKIND
        elif V[(x, y, z)] == SKIN and (x * 11 + z * 17) % 19 == 0:
            V[(x, y, z)] = SKINH

    # ---- BIG angry eyes: white sclera, black pupil, gold rim, down-angled brow ----
    for s in (1, -1):
        for (bx, by, bz) in [(5, 8, 10), (4, 8, 11), (3, 7, 12)]:   # angry brow
            put(bx * s, by, bz, BROW); put(bx * s, by - 1, bz, BROW)
        for (ex, ey) in [(4, 5), (4, 6), (5, 5), (5, 6)]:           # white eyeball
            put(ex * s, ey, 11, EYEW)
        put(5 * s, 6, 12, EYE)                                      # gold rim
        put(4 * s, 5, 12, PUP); put(5 * s, 5, 12, PUP)              # mean low pupil

    # ---- strong cream HOOKED beak (upper fixed, lower drops into a tidy gape) ----
    box(-2, 2, 3, 4, 14, 16, BEAK)            # upper mandible
    box(-1, 1, 2, 3, 16, 17, BEAK)           # narrows forward
    put(0, 1, 18, HOOK); put(1, 2, 17, BEAK); put(-1, 2, 17, BEAK)   # the down-curled hook
    put(0, 4, 15, BEAKD); put(0, 4, 16, BEAKD)                       # nostril line
    box(-2, 2, 1 - gape, 2 - gape, 14, 17, BEAK)                    # lower jaw drops by gape
    put(0, 1 - gape, 18, BEAKD)
    if gape > 0:                                                     # contained red gape between jaws
        box(-2, 2, 2 - gape, 2, 14, 16, MAW)
        box(-1, 1, 2 - gape, 1, 13, 13, (120, 36, 44))             # dark throat at the back
        put(0, 2 - gape, 16, TONGUE); put(0, 2 - gape, 15, TONGUE)  # tongue tip

    # ---- stubby clawed feet: a FRONT pair and a REAR pair (he's a four-legged brute) ----
    for s in (1, -1):
        ellip(9 * s, -0.5, 1, 2.2, 1.8, 2.6, SKIN)          # front foot
        for c in range(3):
            put(round((9 + c * 0.6) * s), -2, 3 + c, CLAW)  # front claws, forward
        # REAR LEGS: muscular hind limbs splayed OUT past the shell rim so they actually read
        ellip(8.6 * s, 1.4, -6, 2.2, 3.0, 2.2, SKIND)        # the thick scaly THIGH against the shell
        ellip(10.8 * s, -0.4, -5, 2.7, 2.2, 2.9, SKIN)       # the splayed rear foot, out past the rim
        ellip(11.0 * s, 0.5, -5, 1.5, 1.2, 1.7, SKINH, only_empty=True)  # lit top of the foot
        for c in range(4):                                   # four splayed hind claws
            put(round((11 + c * 0.35) * s), -2, -7 + c, CLAW)
    return V


def build_pike(frame=0):
    """PIKE the Lurker: a long lean ambush fish - a torpedo body, a broad flattened
    duck-bill snout packed with needle teeth, a wide gaping maw, low-set fins and a
    forked tail. Olive-green with pale bean-spots and gold eyes. Faces +z; gapes per frame."""
    BACK=(50,82,50); BACKH=(84,124,72); BACKD=(34,56,36)
    FLANK=(120,150,92); BELLY=(222,224,196); SPOT=(206,222,168)
    FIN=(92,118,68); FIND=(62,84,48); FINH=(140,168,100)
    MAW=(150,50,60); TONGUE=(202,102,112); THROAT=(94,30,38); TOOTH=(246,246,232)
    EYEW=(250,244,220); EYE=(242,202,42); PUP=(14,14,16); BROW=(38,54,34)
    V={}; put,ellip,box=_vox_helpers(V)
    gape=[1,5,9][frame]
    # torpedo body, fattest mid, tapering to the tail (-z)
    for i,z in enumerate(range(-26,4)):
        t=i/29.0
        f=(t**0.6)*(1.0-0.28*t)
        rx=0.8+4.6*f; ry=1.0+5.4*f; cy=0.8+1.4*t
        ellip(0,cy,z,rx,ry,1.35,BACK)
    for k in list(V.keys()):
        x,y,z=k
        if V[k]==BACK:
            if y<0.0: V[k]=BELLY
            elif y<2.5 and abs(x)>=2: V[k]=FLANK
    ellip(0,6.0,-12,2.4,1.8,11.0,BACKH,only_empty=True)
    for k in list(V.keys()):
        x,y,z=k
        if V[k] in (FLANK,BACK) and y>0 and (x*7+z*5)%13==0:
            V[k]=SPOT
    # broad flattened head + long snout (+z)
    for i,z in enumerate(range(3,15)):
        t=i/11.0
        ellip(0,2.0+0.8*(1-t),z,4.8-2.4*t,2.6-1.1*t,1.3,BACK)
    box(-3,3,3,4,9,16,BACKD); box(-2,2,3,4,16,18,BACKD)
    for tx in range(-3,4):
        put(tx,2,15,TOOTH)
        if tx%2==0: put(tx,2,12,TOOTH)
    box(-3,3,2-gape,3-gape,9,17,BACKD)
    for tx in range(-3,4):
        put(tx,3-gape,15,TOOTH)
        if tx%2==0: put(tx,3-gape,12,TOOTH)
    if gape>1:
        box(-2,2,3-gape,2,9,15,MAW)
        box(-1,1,3-gape,1,8,10,THROAT)
        put(0,3-gape,13,TONGUE); put(0,3-gape,12,TONGUE)
    for s in (1,-1):
        put(4*s,6,8,BROW); put(4*s,6,9,BROW)
        put(4*s,5,8,EYEW); put(4*s,5,9,EYEW); put(5*s,5,9,EYE)
        put(5*s,4,9,PUP); put(4*s,4,9,PUP)
    # dorsal fin set FAR back (pike trait)
    for i,z in enumerate(range(-19,-8)):           # tall dorsal sail
        h=int(5.0-abs(i-5)*0.55)
        for yy in range(max(1,h)):
            put(0,6+yy,z, FIN if yy<2 else FINH)
    for z in range(-17,-10):
        put(0,-3,z,FIND); put(0,-4,z,FIN)
    for s in (1,-1):
        for i in range(4):
            put(round((4+i*0.7)*s),0,-i,FIN)
            put(round((4+i*0.7)*s),-1,-i,FIND)
    for yy in range(-8,10):                        # big forked caudal tail
        zz=-26-abs(yy)//3
        put(0,yy,zz, FIN if abs(yy)<5 else FINH)
        put(0,yy,zz-1,FIND)
        if abs(yy)>=5: put(0,yy,zz-2,FINH)
    return V

def build_beaver(frame=0):
    """BEAVER: a stout brown bruiser, FRONT-facing - broad flat head, big orange
    buck-teeth, beady eyes, round ears, chunky body, clawed paws, flat paddle tail.
    Faces +z so it reads head-on in the top-down view. frame opens the mouth."""
    FUR=(112,74,46); FURH=(152,106,68); FURD=(80,52,32)
    BELLY=(156,120,84); MUZZ=(176,140,102)
    TOOTH=(250,184,72); TOOTHH=(255,216,124)
    NOSE=(38,26,22); EYE=(16,12,12); EYEW=(242,238,230)
    TAIL=(74,52,38); TAILD=(50,34,24)
    CLAW=(234,226,202); MAW=(140,64,68)
    V={}; put,ellip,box=_vox_helpers(V)
    gape=[0,2,3][frame]
    for zi,z in enumerate(range(-20,-8)):            # flat paddle TAIL behind + low
        t=zi/11.0; w=int(2.0+6.0*t)
        for x in range(-w,w+1):
            put(x,-2+int(t*1.5),z,TAIL); put(x,-3+int(t*1.5),z,TAILD)
    for z in range(-19,-9,2):                        # cross-hatch seams
        for x in range(-6,7,3):
            put(x,-1,z,TAILD)
    for x in range(-8,9):                            # chunky body
        for y in range(-2,11):
            for z in range(-9,7):
                if (x/7.5)**2+((y-3)/5.5)**2+((z-1)/6.0)**2<=1.0:
                    put(x,y,z,FUR)
    ellip(0,7,0,5,3.5,5,FURH,only_empty=True)
    for k in list(V.keys()):
        x,y,z=k
        if V[k]==FUR and y<2 and z>0: V[k]=BELLY
    for zi,z in enumerate(range(6,14)):              # broad flat HEAD forward+up
        t=zi/7.0
        ellip(0,6.5,z,5.2-1.6*t,3.6-1.0*t,1.4,FUR)
    ellip(0,8.5,10,3.0,1.6,2.4,FURH,only_empty=True)
    for s in (1,-1):                                 # round EARS
        ellip(4*s,10,7,1.6,1.6,1.2,FURD)
        ellip(4*s,10,7,0.9,0.9,0.8,MUZZ,only_empty=True)
    ellip(0,5.0,13,3.2,2.4,1.6,MUZZ)                 # lighter MUZZLE
    for nx in (-1,0,1):
        put(nx,6.6,15,NOSE)
    put(0,7.2,15,NOSE)
    for tx in (-2,-1,1,2):                           # bold orange BUCK TEETH (the beaver signature)
        for ty in range(4+gape):
            put(tx,4-ty,14,TOOTH if ty<3 else TOOTHH)
            put(tx,4-ty,15,TOOTH if ty<3 else TOOTHH)
        put(tx,4,16,TOOTHH)
    if gape>0:
        box(-2,2,2-gape,3,12,13,MAW)
    for s in (1,-1):                                 # bigger, softer EYES (less beady)
        put(3*s,9,11,FURD)
        for (ex,ey) in [(3,8),(4,8),(5,8),(3,7),(4,7),(5,7)]:
            put(ex*s,ey,13,EYEW)
        put(4*s,7,14,EYE)
        put(4*s,8,14,(255,255,255))
    for s in (1,-1):                                 # clawed PAWS
        ellip(5*s,-1,6,1.8,1.6,2.0,FUR)
        for c in range(3):
            put(round((5+c*0.5)*s),-2,7+c,CLAW)
    return V

def build_bongo(frame=0):
    """BONGO: a colossal, deadpan bullfrog, FRONT-facing. Wide squat green body, pale
    throat, two big bulging eyes domed up on top, a broad downturned grumpy mouth that
    gapes per frame, stubby front feet. He'd rather be napping. Faces +z (head-on)."""
    SKIN=(96,162,74); SKINH=(126,190,98); SKIND=(66,120,52)
    BELLY=(180,200,140); THROAT=(150,184,112)
    SPOT=(58,104,46); EYE=(18,16,14); EYEW=(244,240,228)
    LID=(80,134,60); NOSE=(40,60,34); MAW=(150,72,76); GOLD=(214,176,70)
    V={}; put,ellip,box=_vox_helpers(V)
    gape=[0,2,3][frame]
    # wide squat BODY — low and broad, frog-fat
    for x in range(-10,11):
        for y in range(-2,9):
            for z in range(-9,10):
                if (x/9.5)**2+((y-2)/4.6)**2+((z-0.5)/7.0)**2<=1.0:
                    put(x,y,z,SKIN)
    # pale THROAT/BELLY underneath + front
    for k in list(V.keys()):
        x,y,z=k
        if V[k]==SKIN and y<2 and z>-2: V[k]=BELLY if y<0 else THROAT
    # darker mottled SPOTS along the back
    for (sx,sz) in [(-5,-3),(5,-4),(0,-6),(-7,2),(7,1),(3,4),(-3,5)]:
        ellip(sx,6.0,sz,1.8,0.8,1.8,SPOT,only_empty=True)
    ellip(0,6.5,1,8.0,2.0,6.0,SKINH,only_empty=True)        # sun-lit dome on the back
    # broad flat HEAD-front rises a touch toward the brow
    for zi,z in enumerate(range(8,13)):
        t=zi/4.0
        ellip(0,3.0+t*1.5,z,7.5-2.0*t,3.2-0.6*t,1.3,SKIN)
    # the big GRUMPY MOUTH — a wide downturned line across the front, gaping down per frame
    for x in range(-7,8):
        droop=int(abs(x)*0.32)                              # corners turn DOWN -> permanent frown
        put(x,1+droop,12,SKIND); put(x,1+droop,13,SKIND)
    if gape>0:
        box(-6,6,1-gape,1,11,13,MAW)                        # open maw (dark) when he lashes / gulps
        for x in range(-6,7,2):
            put(x,1-gape,13,(120,54,58))
    # two big bulging EYES domed up on TOP of the head (the bullfrog signature)
    for s in (1,-1):
        ellip(5*s,8.5,7,2.6,2.6,2.4,SKIN)                   # the bulging mound
        ellip(5*s,9.6,8,1.9,1.9,1.7,EYEW)                   # white of the eye
        ellip(5*s,9.8,9.2,1.0,1.0,0.9,GOLD)                 # gold iris (sleepy)
        put(5*s,9.8,10,EYE); put(5*s+1*s,9.8,10,EYE)        # flat unimpressed pupil
        ellip(5*s,11.0,7,2.4,0.7,2.2,LID,only_empty=True)   # heavy droopy LID over the top
    # NOSTRILS up front
    for nx in (-1,1):
        put(nx,4.5,13,NOSE)
    # stubby front FEET poking forward
    for s in (1,-1):
        ellip(6*s,-2,8,2.0,1.2,2.4,SKIND)
        for c in range(3):
            put(round((5+c)*s),-2,10+c,THROAT)
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
    save(render(shade(build_heron(0, beak_open=True)), math.radians(0), math.radians(42), out=132, scale=2.7),
         "gerald_open.png")   # BEAK-OPEN frame for squawks / taunts / stomps
    # SNAPZ: the bold snapping-turtle boss — a front-3/4 view so his face (big eyes,
    # hooked beak, gaping maw) reads, with the scuted shell + spiky tail behind.
    # Crop all frames to a shared tight bbox so they stay aligned + frame the turtle.
    snapz_imgs = [render(shade(build_snapz(f)), math.radians(20), math.radians(14), out=260, scale=4.0)
                  for f in (0, 1, 2)]
    bb = None
    for im in snapz_imgs:
        b = im.getbbox()
        if b:
            bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    bb = (max(0, bb[0] - 4), max(0, bb[1] - 4), min(260, bb[2] + 4), min(260, bb[3] + 4))
    for f, im in enumerate(snapz_imgs):
        save(im.crop(bb), "snapz_%d.png" % f)
    # the COMMON river snapping turtle (the lesser hazard): a smaller mossy-GREEN snapper,
    # clearly NOT the hulking muddy boss. Same poses, its own shared crop.
    turtle_imgs = [render(shade(build_snapz(f, "turtle")), math.radians(20), math.radians(14), out=260, scale=3.2)
                   for f in (0, 1, 2)]
    tbb = None
    for im in turtle_imgs:
        b = im.getbbox()
        if b:
            tbb = b if tbb is None else (min(tbb[0], b[0]), min(tbb[1], b[1]), max(tbb[2], b[2]), max(tbb[3], b[3]))
    tbb = (max(0, tbb[0] - 4), max(0, tbb[1] - 4), min(260, tbb[2] + 4), min(260, tbb[3] + 4))
    for f, im in enumerate(turtle_imgs):
        save(im.crop(tbb), "turtle_%d.png" % f)
    # PIKE the Lurker: a long ambush fish, front-3/4 so the gaping toothy maw reads
    pike_imgs = [render(shade(build_pike(f)), math.radians(80), math.radians(12), out=340, scale=3.4)
                 for f in (0, 1, 2)]
    pbb = None
    for im in pike_imgs:
        b = im.getbbox()
        if b:
            pbb = b if pbb is None else (min(pbb[0], b[0]), min(pbb[1], b[1]), max(pbb[2], b[2]), max(pbb[3], b[3]))
    pbb = (max(0, pbb[0] - 4), max(0, pbb[1] - 4), min(340, pbb[2] + 4), min(340, pbb[3] + 4))
    for f, im in enumerate(pike_imgs):
        save(im.crop(pbb), "pike_%d.png" % f)
    # BEAVER: a stout FRONT-facing bruiser (buck-teeth + paddle tail read head-on)
    # BONGO the giant bullfrog: front-3/4, big enough that his domed eyes + grumpy maw read
    bongo_imgs = [render(shade(build_bongo(f)), math.radians(10), math.radians(20), out=320, scale=5.0)
                  for f in (0, 1, 2)]
    bgb = None
    for im in bongo_imgs:
        b = im.getbbox()
        if b:
            bgb = b if bgb is None else (min(bgb[0], b[0]), min(bgb[1], b[1]), max(bgb[2], b[2]), max(bgb[3], b[3]))
    bgb = (max(0, bgb[0] - 4), max(0, bgb[1] - 4), min(320, bgb[2] + 4), min(320, bgb[3] + 4))
    for f, im in enumerate(bongo_imgs):
        save(im.crop(bgb), "bongo_%d.png" % f)
    save(render(shade(build_bongo(2)), math.radians(10), math.radians(20), out=320, scale=5.0).crop(bgb), "bongo_open.png")
    beaver_imgs = [render(shade(build_beaver(f)), math.radians(8), math.radians(18), out=320, scale=5.2)
                   for f in (0, 1, 2)]
    bvb = None
    for im in beaver_imgs:
        b = im.getbbox()
        if b:
            bvb = b if bvb is None else (min(bvb[0], b[0]), min(bvb[1], b[1]), max(bvb[2], b[2]), max(bvb[3], b[3]))
    bvb = (max(0, bvb[0] - 4), max(0, bvb[1] - 4), min(320, bvb[2] + 4), min(320, bvb[3] + 4))
    for f, im in enumerate(beaver_imgs):
        save(im.crop(bvb), "beaver_%d.png" % f)
    # RUSTY the red-tailed hawk GUIDE: soaring 3/4 top-down so his spread wings,
    # brown back, dark fingered tips and that signature rusty-red fanned tail all
    # read. 3 flap frames (glide / upstroke / downstroke); cropped to a shared
    # bbox so he holds position while the wings beat.
    hawk_imgs = [render(shade(build_hawk(f)), math.radians(20), math.radians(22), out=160, scale=3.4)
                 for f in (0, 1, 2)]
    hbb = None
    for im in hawk_imgs:
        b = im.getbbox()
        if b:
            hbb = b if hbb is None else (min(hbb[0], b[0]), min(hbb[1], b[1]), max(hbb[2], b[2]), max(hbb[3], b[3]))
    hbb = (max(0, hbb[0] - 3), max(0, hbb[1] - 3), min(160, hbb[2] + 3), min(160, hbb[3] + 3))
    for f, im in enumerate(hawk_imgs):
        save(im.crop(hbb), "hawk_%d.png" % f)
    # a beak-agape SCREECH pose (level glide), cropped to the SAME bbox so he holds still
    screech = render(shade(build_hawk(0, beak_open=True)), math.radians(20), math.radians(22), out=160, scale=3.4)
    save(screech.crop(hbb), "hawk_screech.png")
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
    save(render(shade(build_sadie(0, ball=True, dry=True, legs=True)), math.radians(18), math.radians(11), out=110, scale=3.4), "sadie_greet.png")
    save(render(shade(build_sadie(0, ball=True, dry=True, legs=True)), math.radians(18), math.radians(11), out=110, scale=3.4), "sadie_p0.png")
    save(render(shade(build_sadie(1, ball=True, dry=True, legs=True)), math.radians(18), math.radians(11), out=110, scale=3.4), "sadie_p1.png")
    save(render(shade(build_sadie(0, ball=True, dry=True, legs=True)), math.radians(6), math.radians(11), out=110, scale=3.4), "sadie_p2.png")
    save(render(shade(build_sadie(0, ball=True, dry=True, legs=True)), math.radians(36), math.radians(11), out=110, scale=3.4), "sadie_p3.png")
    save(render(shade(build_sadie(0, ball=False, legs=True)), math.radians(18), math.radians(11), out=110, scale=3.4), "sadie_p4.png")
    save(render(shade(build_chuckit()), math.radians(35), math.radians(22), out=46, scale=2.8), "sadie_ball.png")
    _runims = [render(shade(build_sadie_run(_rf)), math.radians(90), math.radians(10), out=130, scale=3.2) for _rf in range(8)]
    _ru = None                                                # UNION bbox so the 8 frames share one canvas (no jitter)
    for _im in _runims:
        _b = _im.getbbox()
        if _b: _ru = _b if _ru is None else (min(_ru[0],_b[0]),min(_ru[1],_b[1]),max(_ru[2],_b[2]),max(_ru[3],_b[3]))
    for _rf, _im in enumerate(_runims):
        save(_im.crop(_ru), "sadie_run_%d.png" % _rf)
    make_chuckit().save(os.path.join(art_dir, "chuckit.png"))
    # LUCIEN the loon DJ: a hero portrait + a head-bobbed frame (his sprite matches the voxel art style)
    save(render(shade(build_loon(0)), math.radians(62), math.radians(22), out=128, scale=2.6), "loon.png")
    save(render(shade(build_loon(2)), math.radians(62), math.radians(22), out=128, scale=2.6), "loon_bob.png")
    # LUCIEN frames: 7 poses + a GAPE (beak open + pink tongue) + 2 head-turn yaws (subtle sway)
    _lframes = [("scratch_r_d", False, 22), ("scratch_r_u", False, 22), ("scratch_l_d", False, 22),
                ("scratch_l_u", False, 22), ("tap", False, 22), ("wing_up", False, 22), ("drop", False, 22),
                ("scratch_r_d", True, 22), ("scratch_r_d", False, 13), ("scratch_r_d", False, 31)]
    _ldimgs = [render(shade(build_lucien_dj(_po, gape=_g)), math.radians(_y), math.radians(30), out=180, scale=3.0)
               for (_po, _g, _y) in _lframes]
    _ldbb = None                                            # p0-6 routine, p7 gape, p8/p9 head-turn L/R
    for _im in _ldimgs:
        _b = _im.getbbox()
        if _b: _ldbb = _b if _ldbb is None else (min(_ldbb[0], _b[0]), min(_ldbb[1], _b[1]), max(_ldbb[2], _b[2]), max(_ldbb[3], _b[3]))
    _ldbb = (max(0, _ldbb[0] - 4), max(0, _ldbb[1] - 4), min(180, _ldbb[2] + 4), min(180, _ldbb[3] + 4))
    for _i, _im in enumerate(_ldimgs): save(_im.crop(_ldbb), "lucien_dj_p%d.png" % _i)
    # THE MAGIC BREAD + DONNI the speedboat, as voxel sprites (consistent pixel-art style)
    save(render(shade(build_bread()), math.radians(24), math.radians(36), out=128, scale=5.5), "magicbread.png")
    save(render(shade(build_boat()), math.radians(180), math.radians(46), out=160, scale=3.4), "donni.png")
    save(render(shade(build_thwomp(False)), math.radians(180), math.radians(48), out=140, scale=2.4), "thwomp.png")
    save(render(shade(build_thwomp(True)), math.radians(180), math.radians(48), out=140, scale=2.4), "thwomp_slam.png")
    # COMPENDIUM turntables: 16-frame yaw spins so each character can be rotated in
    # the codex detail view, just like the ducks. Cropped to a shared per-character bbox.
    def spin_set(SH, name, pitch_deg, scale, out=220, n=16):
        imgs = [render(SH, math.radians(i * 360.0 / n), math.radians(pitch_deg), out=out, scale=scale)
                for i in range(n)]
        bb = None
        for im in imgs:
            b = im.getbbox()
            if b:
                bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
        bb = (max(0, bb[0] - 4), max(0, bb[1] - 4), min(out, bb[2] + 4), min(out, bb[3] + 4))
        for i, im in enumerate(imgs):
            save(im.crop(bb), "%s_spin_%02d.png" % (name, i))
    spin_set(shade(build_heron(0)), "gerald", 30, 2.6, out=200)
    spin_set(shade(build_snapz(0)), "snapz", 18, 3.6, out=240)
    spin_set(shade(build_snapz(0, "turtle")), "turtle", 18, 3.0, out=240)   # the lesser green snapper
    # OPEN-MOUTH turntables so the codex tap-reaction works at ANY spin angle (not just frontal)
    spin_set(shade(build_heron(0, beak_open=True)), "gerald_open", 30, 2.6, out=200)
    spin_set(shade(build_snapz(2)), "snapz_open", 18, 3.6, out=240)
    spin_set(shade(build_snapz(2, "turtle")), "turtle_open", 18, 3.0, out=240)
    spin_set(shade(build_pike(0)), "pike", 12, 3.4, out=340)
    spin_set(shade(build_pike(2)), "pike_open", 12, 3.4, out=340)
    spin_set(shade(build_beaver(0)), "beaver", 20, 5.2, out=320)
    spin_set(shade(build_beaver(2)), "beaver_open", 20, 5.2, out=320)
    spin_set(shade(build_bongo(0)), "bongo", 20, 5.0, out=320)
    spin_set(shade(build_bongo(2)), "bongo_open", 20, 5.0, out=320)
    spin_set(shade(build_hawk(0)), "rusty", 24, 3.2, out=180)
    spin_set(shade(build_sadie(0)), "sadie", 34, 1.7, out=80)
    spin_set(shade(build_loon(0)), "loon", HERO_PITCH, 2.6, out=128)
    _dboat = shade(build_boat())                           # DONNI turntable, offset 40deg to a hero 3/4
    _dimgs = [render(_dboat, math.radians(40 + i * 22.5), math.radians(33), out=176, scale=3.2) for i in range(16)]
    _dbb = None
    for _im in _dimgs:
        _b = _im.getbbox()
        if _b: _dbb = _b if _dbb is None else (min(_dbb[0], _b[0]), min(_dbb[1], _b[1]), max(_dbb[2], _b[2]), max(_dbb[3], _b[3]))
    _dbb = (max(0, _dbb[0] - 4), max(0, _dbb[1] - 4), min(176, _dbb[2] + 4), min(176, _dbb[3] + 4))
    for _i, _im in enumerate(_dimgs): save(_im.crop(_dbb), "donni_spin_%02d.png" % _i)
    spin_set(shade(build_bread()), "bread", 30, 5.0, out=176)
    spin_set(shade(build("golden", "folded", elder=True)), "elder", HERO_PITCH, 1.45, out=110)
    # ON FIRE flame volume: 6-frame loop at the gameplay camera, emissive (no
    # shade/outline). fire_duck = whole volume (behind), fire_lick = front wrap (over)
    for f in range(6):
        Vf, Vfront = build_fire(f, 6)
        save(render(Vf, gy, PITCH, out=76, scale=1.45, outline=False), "fire_duck_%d.png" % f)
        save(render(Vfront, gy, PITCH, out=76, scale=1.45, outline=False), "fire_lick_%d.png" % f)
    print("critters generated ->", art_dir)


# ============ WEARABLES as voxels — rendered at the duck's camera angles ===========
# Each hat is its own little voxel model sitting at the duck's CANONICAL head. We render
# it from the SAME yaws/pitches as the duck's gameplay frames, so it banks / leans / tumbles
# in 3D lockstep with the bird and composites pixel-registered on top. Shared across species
# (a small per-species head nudge happens at runtime). The head centre is ~(0, 7, 10),
# radius ~3.7, so its crown is around y=10..11.
WC = dict(
    gold=(244, 198, 70), goldh=(255, 226, 120), red=(208, 52, 56), redh=(236, 96, 96),
    black=(48, 46, 56), white=(242, 240, 234), cyan=(120, 214, 228), pink=(236, 118, 168),
    yellow=(242, 208, 74), blue=(74, 116, 204), grey=(112, 116, 126), greyd=(68, 72, 82),
    orange=(242, 132, 84), brown=(150, 100, 56), teal=(70, 196, 214), skull=(236, 236, 228),
    pomp=(248, 248, 252), whited=(206, 206, 200), tealr=(40, 150, 170),
)


def _ring(d, y, rad, col, cz=10, thick=0.55):
    for x in range(-6, 7):
        for z in range(cz - 6, cz + 7):
            rr = math.sqrt(x * x + (z - cz) ** 2)
            if rad - thick <= rr <= rad + thick:
                d[(x, y, z)] = col


def _disc(d, y, rad, col, cz=10):
    for x in range(-6, 7):
        for z in range(cz - 6, cz + 7):
            if math.sqrt(x * x + (z - cz) ** 2) <= rad:
                d[(x, y, z)] = col


def build_hat(hid):
    d = {}
    cz = 10
    if hid == "crown":
        for y in (10, 11):
            _ring(d, y, 3.1, WC["gold"], cz, 0.8)
        for a in range(6):                                  # five-ish points around the band
            ang = a * (math.tau / 6)
            sx = int(round(math.cos(ang) * 2.7)); sz = cz + int(round(math.sin(ang) * 2.7))
            for y in range(11, 15):
                d[(sx, y, sz)] = WC["goldh"] if y >= 13 else WC["gold"]
        d[(0, 11, cz + 3)] = WC["red"]; d[(0, 12, cz + 3)] = WC["redh"]   # front gem
    elif hid == "pirate":
        for y in (11, 12):                                  # flat black bicorne, wider front-to-back
            for x in range(-3, 4):
                for z in range(cz - 5, cz + 6):
                    if (x / 3.0) ** 2 + ((z - cz) / 5.0) ** 2 <= 1.0:
                        d[(x, y, z)] = WC["black"]
        for (px, pz) in [(0, cz + 6), (0, cz - 6)]:         # the two upswept points
            d[(px, 13, pz)] = WC["black"]; d[(px, 12, pz)] = WC["black"]
        sf = cz + 4                                          # white skull on the front, no red
        for (sx, sy) in [(0, 12), (-1, 12), (1, 12), (0, 11)]:
            d[(sx, sy, sf)] = WC["skull"]
        d[(-1, 12, sf + 1)] = WC["black"]; d[(1, 12, sf + 1)] = WC["black"]   # eye sockets
    elif hid == "party":
        for i, y in enumerate(range(11, 19)):               # tall striped cone
            rad = max(0.4, 2.8 - i * 0.34)
            cols = [WC["pink"], WC["cyan"], WC["yellow"]]
            _disc(d, y, rad, cols[i % 3], cz)
        for yy in (19, 20):                                  # pom-pom
            d[(0, yy, cz)] = WC["pomp"]
    elif hid == "prop":
        for i, y in enumerate((9, 10, 11)):                 # taller two-tone beanie dome
            _disc(d, y, 3.2 - i * 0.55, [WC["red"], WC["blue"], WC["red"]][i], cz)
        d[(0, 12, cz)] = WC["yellow"]                        # button + propeller post
        d[(0, 13, cz)] = WC["greyd"]                         # (the spinning blades are drawn live in-game)
    elif hid == "chef":
        for y in (9, 10, 11):                               # short pleated band
            _ring(d, y, 2.6, WC["white"], cz, 1.1)
        for a in range(8):                                  # vertical pleat shadows on the band
            ang = a * (math.tau / 8)
            px = int(round(math.cos(ang) * 2.6)); pz = cz + int(round(math.sin(ang) * 2.6))
            for y in (9, 10, 11):
                d[(px, y, pz)] = WC["whited"]
        for y, r in {12: 3.2, 13: 3.7, 14: 3.5, 15: 2.6, 16: 1.5}.items():   # wide bulbous puff
            _disc(d, y, r, WC["white"], cz)
        for x in range(-4, 5):                              # shaded underside of the puff = it reads round
            for z in range(cz - 4, cz + 5):
                if 2.7 <= math.sqrt(x * x + (z - cz) ** 2) <= 3.7:
                    d[(x, 12, z)] = WC["whited"]
    elif hid == "bandana":
        for y in (8, 9, 10):                                # low red wrap
            _ring(d, y, 3.4, WC["red"], cz, 0.7)
        import math as _m                                   # white polka dots all the way round
        for a in range(10):
            ang = a * (_m.tau / 10)
            dx = int(round(_m.cos(ang) * 3.2)); dz = cz + int(round(_m.sin(ang) * 3.2))
            d[(dx, 9 if a % 2 else 10, dz)] = WC["white"]
        d[(0, 9, cz - 4)] = WC["red"]; d[(1, 8, cz - 5)] = WC["redh"]; d[(-1, 8, cz - 5)] = WC["redh"]  # knot tails (back)
    elif hid == "raccoon":
        # RACCOON BANDIT MASK: a black eye-band (white-rimmed beady eyes) + perky grey ears + a striped snout
        BLK = (34, 30, 38); GRY = (152, 150, 160); GRYD = (108, 106, 118); WHT = WC["white"]
        for sx in range(-5, 6):                       # the black mask band across both eyes (sits proud)
            for yy in (6, 7, 8):
                d[(sx, yy, 14)] = BLK
                d[(sx, yy, 15)] = BLK
        for side in (1, -1):                          # white-rimmed beady eyes peeking through
            ctr = side * 3
            for (ox, oy) in [(0, 1), (-1, 0), (1, 0), (0, -1)]:
                d[(ctr + ox, 7 + oy, 16)] = WHT
            d[(ctr, 7, 17)] = (18, 18, 22)
        for side in (1, -1):                          # perky grey ears on top of the head
            ex = side * 3
            for (ey, ez) in [(13, 14), (14, 14), (14, 13), (15, 14)]:   # up on the head-top, right by the mask
                d[(ex, ey, ez)] = GRY
            d[(ex, 16, 14)] = WHT
            d[(ex, 13, 14)] = GRYD
    elif hid == "halo":
        for y in (14, 15):
            _ring(d, y, 3.0, WC["goldh"] if y == 15 else WC["gold"], cz, 0.6)
    elif hid == "boombox":
        for y in range(12, 16):                             # the box
            for x in range(-3, 4):
                d[(x, y, cz)] = WC["grey"]; d[(x, y, cz - 1)] = WC["greyd"]
        for sx in (-2, 2):                                  # speakers
            d[(sx, 14, cz + 1)] = WC["black"]; d[(sx, 13, cz + 1)] = WC["black"]
        for y in range(16, 19):                             # antenna
            d[(3, y, cz)] = WC["greyd"]
    elif hid == "scarf":
        # a chunky knit COWL wrapping the neck + shoulders right under the head (around the head/body
        # junction; kept high at y2-5 and OFF the rump so it reads as a scarf collar, not a back cape).
        # bold + thick so the band — not just side-dots — shows from every angle. the ring TILTS
        # FORWARD up the neck (higher rows ride further forward, z+) to follow the neck's lean.
        for y in (2, 3, 4, 5):
            czy = 6.0 + (y - 3) * 1.0               # tilt FORWARD up the neck (higher rows ride forward)
            for x in range(-6, 7):
                for z in range(1, 12):
                    rr = math.sqrt((x / 1.3) ** 2 + (z - czy) ** 2)
                    if 3.1 <= rr <= 4.5:
                        d[(x, y, z)] = WC["white"] if y == 3 else (WC["red"] if (x + z) % 2 else WC["redh"])
        for y in (-3, -2, -1, 0, 1):                        # two knit tails dangling down the chest
            d[(2, y, 9)] = WC["red"]; d[(2, y, 10)] = WC["redh"]
            d[(-2, y, 9)] = WC["white"]; d[(-2, y, 10)] = WC["red"]
    elif hid == "goggles":
        # big, bold AVIATORS worn human-style on the face: gold frames + dark glinting teardrop
        # lenses covering the upper face. they sit PROUD (z14-15) so the head can't occlude them.
        lens = (40, 86, 92); glint = WC["cyan"]; gold = WC["gold"]; goldh = WC["goldh"]
        for side in (1, -1):
            ctr = side * 3                                  # each lens centred on an eye, 3 wide
            for dx in (-1, 0, 1):
                sx = ctr + dx
                for yy in (6, 7, 8, 9):                     # tall teardrop lens
                    if yy == 6 and abs(ctr + dx) >= 4:      # taper the lower OUTER corner -> teardrop
                        continue
                    d[(sx, yy, 14)] = lens
                    d[(sx, yy, 15)] = lens
                d[(sx, 9, 15)] = glint                      # bright glint along the top (faces the camera)
                d[(sx, 10, 14)] = gold                      # gold brow bar across the top
                d[(sx, 5, 14)] = gold                       # gold rim along the bottom
            d[(ctr + side, 7, 14)] = gold; d[(ctr + side, 8, 14)] = gold   # gold outer edge
        for xx in (-1, 0, 1):                               # gold bridge across the bill base
            d[(xx, 9, 15)] = goldh
            d[(xx, 9, 14)] = gold
    elif hid == "heron":
        # a great-blue-heron HOOD: a slate cowl sheathing the crown, back and sides of the head
        # (covering the mallard's green so it reads as heron plumage), leaving the face bare,
        # with the heron's signature black head-plume streaming off the back. no second beak.
        hgrey = (126, 140, 156); hslate = (90, 108, 128); plume = (30, 34, 44)
        hcy = 7.0; hr = 3.9                                 # the canonical mallard head sphere
        for x in range(-5, 6):
            for y in range(5, 13):
                for z in range(5, 15):
                    dx = float(x); dy = float(y - hcy); dz = float(z - cz)
                    dist = math.sqrt(dx * dx + dy * dy + dz * dz)
                    if dist < hr - 1.05 or dist > hr + 0.5:
                        continue
                    if dz >= 0.5 and dy < 1.0:              # leave the FACE/bill zone bare
                        continue
                    d[(x, y, z)] = hgrey if dy >= -0.2 else hslate
        for i in range(6):                                  # the black plume sweeping off the crown, back & down
            zz = 9 - i
            yy = 11 - i // 2
            d[(0, yy, zz)] = plume
            d[(0, max(yy - 1, 5), zz)] = plume
            if 1 <= i <= 4:
                d[(1, yy - 1, zz)] = hslate; d[(-1, yy - 1, zz)] = hslate
        # the heron's signature long yellow DAGGER-BEAK, jutting forward off the crest above the
        # duck's own bill so the hat reads unmistakably as a heron
        for i in range(5):
            zz = cz + 4 + i
            col = WC["yellow"] if i < 4 else WC["gold"]
            d[(0, 8, zz)] = col
            if i < 3:
                d[(0, 9, zz)] = col                         # thickness near the base, tapering to a point
        d[(0, 9, cz + 3)] = hslate                          # slate brow connecting the beak to the hood
    elif hid == "turtle":
        # a domed TURTLE SHELL worn on the BACK (a body item): olive scutes, deep seams, a tan rim.
        # sits LOW (y3-6) and slightly back of centre so it caps the duck's back, not her head.
        shell = (104, 146, 84); shellh = (146, 184, 108); shellm = (116, 156, 90)
        shelld = (84, 118, 64); seam = (46, 68, 38); rim = (198, 178, 102)
        cz = -4                                                 # over the back/rump (body centre z=0; head z~9)
        prof = {6: 5.4, 7: 5.0, 8: 4.2, 9: 3.0, 10: 1.7}        # y -> radius; a BIGGER dome that caps the back
        for y, r in prof.items():
            _disc(d, y, r, shell, cz)
        def top_y(rr):                                          # the exposed top voxel at radius rr
            if rr <= 1.8: return 10
            if rr <= 3.0: return 9
            if rr <= 4.2: return 8
            if rr <= 5.0: return 7
            return 6
        # paint the exposed top surface into DISTINCT scute plates: a light central scute ringed
        # by six outer scutes in alternating olive shades — that's what makes it read as a shell
        ring = [shellh, shellm, shelld, shellh, shellm, shelld]
        for x in range(-6, 7):
            for z in range(cz - 6, cz + 7):
                dz = z - cz
                rr = math.sqrt(x * x + dz * dz)
                if rr > 4.6:
                    continue
                ty = top_y(rr)
                if (x, ty, z) not in d:
                    continue
                if rr < 1.9:
                    d[(x, ty, z)] = shellh                      # the central scute, brightest
                else:
                    sec = int(((math.atan2(dz, x) % math.tau) / (math.tau / 6.0)))
                    d[(x, ty, z)] = ring[sec % 6]
        for a in range(6):                                      # deep seams BETWEEN the outer scutes
            ang = a * (math.tau / 6.0) + (math.tau / 12.0)
            for rr in (2.2, 3.0, 3.8, 4.4):
                sx = int(round(math.cos(ang) * rr)); sz = cz + int(round(math.sin(ang) * rr))
                d[(sx, top_y(rr), sz)] = seam
        for a in range(8):                                      # a ring of seam framing the central scute
            ang = a * (math.tau / 8.0)
            sx = int(round(math.cos(ang) * 2.1)); sz = cz + int(round(math.sin(ang) * 2.1))
            d[(sx, top_y(2.1), sz)] = seam
        for x in range(-6, 7):                                  # tan rim hugging the base of the shell
            for z in range(cz - 6, cz + 7):
                if 3.9 <= math.sqrt(x * x + (z - cz) ** 2) <= 5.4:
                    d[(x, 6, z)] = rim
    elif hid == "cape":
        # a HERO CAPE clasped at the shoulders, sweeping back over the rump and trailing past the tail
        cape = WC["red"]; capeh = WC["redh"]; caped = (150, 28, 32)
        for y in range(3, 9):                               # sits ON TOP of the back so it clears the body
            rad = 2.6 + (8 - y) * 0.5
            for x in range(-7, 8):
                for z in range(-12, 1):
                    if math.sqrt((x / 1.5) ** 2 + ((z + 6) / 1.7) ** 2) <= rad:   # mass over the rump (z=-6)
                        d[(x, y, z)] = capeh if x <= -3 else (caped if x >= 3 else cape)
        for x in range(-3, 4):                              # a collar standing at the shoulders
            d[(x, 8, 2)] = caped; d[(x, 7, 2)] = caped
        d[(0, 9, 2)] = WC["gold"]
    elif hid == "vest":
        # a LIFE JACKET: bright safety-orange foam panels over the back + shoulders, reflective band, straps
        lj = (242, 132, 40); ljh = (255, 184, 78); ljd = (198, 96, 30); strap = (38, 38, 44); refl = (246, 232, 132)
        for y in range(3, 8):                               # foam blocks riding high on the back
            for x in range(-6, 7):
                for z in range(-3, 5):
                    rr = math.sqrt((x / 1.25) ** 2 + ((z + 1) / 1.4) ** 2)
                    if 2.8 <= rr <= 4.4:
                        d[(x, y, z)] = ljh if y >= 6 else (lj if (x + z) % 2 else ljd)
        for z in range(-2, 5):                              # shoulder straps front-to-back
            d[(2, 7, z)] = strap; d[(-2, 7, z)] = strap
        for x in range(-5, 6):                              # reflective stripe
            d[(x, 7, 1)] = refl
    elif hid == "jetpack":
        # a POCKET JET: twin thrusters towering off the back, blue flame roaring out behind
        tank = WC["grey"]; tankh = (190, 194, 202); tankd = WC["greyd"]; nose = WC["red"]
        for tx in (-3, 3):
            for y in range(4, 12):
                d[(tx, y, -6)] = tank; d[(tx, y, -7)] = tankd; d[(tx, y, -5)] = tankh
            for y in (12, 13):
                d[(tx, y, -6)] = nose
            d[(tx, 3, -7)] = WC["blue"]; d[(tx, 2, -8)] = WC["cyan"]; d[(tx, 1, -9)] = WC["yellow"]
        for y in (7, 6, 5):                                 # harness strap across the back
            for x in range(-3, 4):
                d[(x, y, -5)] = tankd
    elif hid == "satchel":
        # a CHARGE PACK: a leather rucksack riding high on the rump, straps over the shoulders, glowing buckle
        bag = WC["brown"]; bagh = (188, 132, 80); bagd = (110, 72, 40); strap = (90, 60, 34)
        for y in range(3, 10):
            for x in range(-5, 6):
                for z in range(-7, -2):
                    d[(x, y, z)] = bagh if y >= 8 else (bag if (x + z) % 2 else bagd)
        for x in (-3, 3):                                   # straps up over the shoulders
            for y in (9, 8, 7, 6):
                d[(x, y, 0)] = strap
        for x in (-1, 0, 1):                                # glowing charge buckle on the flap
            d[(x, 5, -7)] = WC["gold"]; d[(x, 6, -7)] = WC["goldh"]
    return d


# the PROP BEANIE's propeller as its own voxel, spun around the vertical axis by `phase` degrees.
# rendered at the duck's camera angles for 4 phases so it MELDS (attached + scaled) AND spins.
def build_propeller(phase):
    d = {}
    cz = 10
    a = math.radians(phase)
    for t in range(-4, 5):                              # a single line = both blades of a 2-blade prop
        x = int(round(math.cos(a) * t)); z = cz + int(round(math.sin(a) * t))
        d[(x, 13, z)] = WC["cyan"] if abs(t) < 3 else WC["teal"]
    d[(0, 13, cz)] = WC["yellow"]                       # hub
    d[(0, 12, cz)] = WC["greyd"]                        # post
    return d


def generate_wearables3d(art_dir):
    def save(img, name):
        img.save(os.path.join(art_dir, name))
    gy = math.radians(GAME_YAW)
    # OCCLUSION: render each hat MERGED with the (canonical mallard) head so the head's depth
    # hides the hat's far side, then DIFF out the duck so only the visible hat pixels remain.
    # This is what stops goggles/scarf wrapping THROUGH the head when composited in-game.
    mallard_sh = shade(build("mallard", "folded"))

    def occ(Vhat, yaw, pitch, **kw):
        return render_wear(mallard_sh, Vhat, yaw, pitch, **kw)

    _WEAR3D_IDS = ("crown", "pirate", "party", "prop", "chef", "bandana", "halo", "boombox", "scarf", "goggles", "heron", "turtle", "cape", "vest", "jetpack", "satchel", "raccoon")
    for hid in _WEAR3D_IDS:                              # SINGLE SOURCE — the MEGA-hop meld below reuses this exact list so they can never drift
        V = build_hat(hid)
        if not V:
            continue
        save(occ(V, gy, PITCH), "wear3d_%s_idle.png" % hid)
        for i, off in enumerate(BANK_OFF):
            save(occ(V, math.radians(GAME_YAW + off), PITCH), "wear3d_%s_bank_%d.png" % (hid, i))
        save(occ(V, math.radians(GAME_YAW + SIDE_YAW), SIDE_PITCH), "wear3d_%s_side_left.png" % hid)
        save(occ(V, math.radians(GAME_YAW - SIDE_YAW), SIDE_PITCH), "wear3d_%s_side_right.png" % hid)
        save(occ(V, math.radians(HERO_YAW), math.radians(HERO_PITCH)), "wear3d_%s_hero.png" % hid)
        for i in range(24):                                 # turntable, matching the duck-select spin
            save(occ(V, math.radians(i * 15), math.radians(HERO_PITCH)), "wear3d_%s_spin_%02d.png" % (hid, i))
    # the prop beanie's spinning propeller: 4 phases at every camera angle
    for ph in range(4):
        P = build_propeller(ph * 45)
        pre = "wear3d_propblade_%d_" % ph
        save(render(P, gy, PITCH), pre + "idle.png")
        for i, off in enumerate(BANK_OFF):
            save(render(P, math.radians(GAME_YAW + off), PITCH), pre + "bank_%d.png" % i)
        save(render(P, math.radians(GAME_YAW + SIDE_YAW), SIDE_PITCH), pre + "side_left.png")
        save(render(P, math.radians(GAME_YAW - SIDE_YAW), SIDE_PITCH), pre + "side_right.png")
        save(render(P, math.radians(HERO_YAW), math.radians(HERO_PITCH)), pre + "hero.png")
        for i in range(24):
            save(render(P, math.radians(i * 15), math.radians(HERO_PITCH)), pre + "spin_%02d.png" % i)
    # MEGA-HOP MELD: bake each hat into every species' sprite-stack frame so it rides the
    # tumbling voxel duck welded to the head (no more flat hat floating around the spin).
    hats = {hid: build_hat(hid) for hid in _WEAR3D_IDS}   # SAME list as the worn sprites -> meld can't drift (raccoon etc. always included)
    for sp in SPECIES:
        Vf = build(sp, "folded")
        for hid, Hf in hats.items():
            if not Hf:
                continue
            for ii, sl in hat_stack_slices(Vf, Hf, shade(Hf)):
                save(sl, "wear_%s_%s_stack_%02d.png" % (hid, sp, ii))
    print("wearables3d generated ->", art_dir)


def generate_icons(art_dir):
    """render every unique boon/power-up voxel icon to boon_<model>.png"""
    models = ["shield", "coin", "bolt", "magnet", "egg", "flame", "arrow", "star",
              "clover", "chick", "crown", "heart", "fork", "wing",
              "spring", "cookie", "cannon", "die", "ball", "loaf", "burst", "bowl", "gem", "gust", "birds", "zen", "tiny",
              "trashcan", "sack", "slingshot", "tire", "junkshield",
              "feathershield", "lifevest", "goslingguard", "snackwing", "vformation", "earlybird",
              "wildfire", "phoenix", "thermal", "loftgauge", "hourglass", "doublearrow",
              "paperplane", "flag", "swoosh", "clutch", "egghead", "trio", "conga", "pouch",
              "warhelm", "trampoline", "breadbasket", "shockring"]
    for m in models:
        im = render(shade(build_icon(m)), math.radians(16), math.radians(16), out=72, scale=3.2)
        b = im.getbbox()
        if b:
            pad = ((max(0, b[0] - 3), max(0, b[1] - 3), min(72, b[2] + 3), min(72, b[3] + 3)))
            im = im.crop(pad)
        im.save(os.path.join(art_dir, "boon_%s.png" % m))
    print("boon icons generated ->", art_dir)


if __name__ == "__main__":
    import os
    art = os.path.join(os.path.dirname(__file__), "..", "art")
    import sys
    if "--wear" in sys.argv:
        generate_wearables3d(art)
    elif "--icons" in sys.argv:
        generate_icons(art)
    elif "--critters" in sys.argv:
        generate_critters(art)
    else:
        generate_ducks(art)
        generate_critters(art)
        generate_wearables3d(art)
        generate_icons(art)
