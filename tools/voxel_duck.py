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
# BACK VIEW: camera behind & above, head/bill leads UP the screen (swims forward).
PITCH = math.radians(-42)
SIDE_PITCH = math.radians(-30)
# 7-frame bank yaw sweep: 0=hard left .. 3=straight .. 6=hard right. Signs verified
# against the render so the head leans toward travel direction.
BANK_YAW = [34, 22, 11, 0, -11, -22, -34]
SIDE_YAW = 70


# ---- palettes ----------------------------------------------------------------
def palette(hen):
    if hen:
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
    return dict(
        back=(132, 126, 110), body=(170, 164, 148), belly=(214, 208, 192),
        verm_d=(116, 110, 96), verm_l=(198, 192, 176),
        nape=(22, 96, 54), head=(40, 142, 80), headh=(96, 196, 128),
        crown=(20, 84, 48), glint=(150, 232, 182),
        chest=(150, 86, 52), chestd=(112, 64, 40), chestl=(176, 104, 64),
        bill=(246, 184, 70), billd=(208, 150, 48), nail=(150, 108, 40), nostril=(120, 90, 40),
        white=(240, 238, 230), collar=(240, 238, 230),
        wing=(152, 144, 126), wingd=(118, 110, 94), primary=(74, 70, 62),
        specw=(236, 236, 228), spec=(58, 108, 172), specd=(40, 76, 128),
        tail=(44, 40, 52), tailhi=(92, 88, 100), eye=(20, 18, 22),
    )


# ---- voxel model -------------------------------------------------------------
def build(hen=False, wings="folded"):
    """Return {(x,y,z): rgb}.  x=right, y=up, z=head(+).  Detailed mallard drake / hen."""
    P = palette(hen)
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
    # ---- wings: folded (with bordered speculum + primaries) or spread (hops) ----
    if wings == "folded":
        for s in (1, -1):
            ellip(5.6 * s, 1.0, -0.5, 1.7, 2.9, 7, P["wing"])
            ellip(6.0 * s, -0.2, -2.5, 1.2, 2.0, 4.5, P["wingd"], only_empty=True)
            box(5 * s, 6 * s, -1, 1, -8, -6, P["primary"], only_empty=True)   # dark tips
            for z in (-5, -4, -3):                                   # speculum, white-bordered
                put(6 * s, 2, z, P["specw"]); put(6 * s, 1, z, P["spec"])
                put(6 * s, 0, z, P["specd"]); put(6 * s, -1, z, P["specw"])
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
    if not hen:
        put(0, 4, -10, P["tail"]); put(0, 5, -11, P["tail"]); put(0, 5, -10, P["tail"])  # curl
    # ---- neck + head ----
    ellip(0, 3.4, 7, 2.7, 3.0, 2.7, P["head"])
    ellip(0, 6.6, 10, 3.7, 3.7, 3.6, P["head"])
    ellip(0, 4.0, 10.2, 3.6, 1.6, 3.2, P["nape"], only_empty=True)     # dark underside/nape
    ellip(0, 8.2, 10.6, 2.7, 2.1, 2.6, P["headh"], only_empty=True)    # sheen
    ellip(0, 9.0, 11.0, 1.5, 1.2, 1.6, P["glint"], only_empty=True)    # bright glint
    if hen:
        ellip(0, 8.6, 9.6, 3.4, 1.8, 3.2, P["crown"], only_empty=True)  # dark cap
        for z in range(8, 13):                                          # eye-line
            put(3, 6, z, P["crown"], only_empty=True); put(-3, 6, z, P["crown"], only_empty=True)
    # ---- white collar ring at neck base ----
    for a in range(0, 360, 14):
        x = round(2.9 * math.cos(math.radians(a)))
        y = round(3.4 + 2.9 * math.sin(math.radians(a)))
        if (x, y, 7) in V:
            put(x, y, 7, P["collar"])
    # ---- bill: long, flat, spatulate ----
    box(-2, 2, 4, 5, 11, 16, P["bill"])
    box(-1, 1, 4, 5, 17, 17, P["bill"])               # rounded tip
    box(-2, 2, 6, 6, 10, 12, P["billd"], only_empty=True)  # base shade under head
    box(-2, 2, 5, 5, 12, 16, P["billd"], only_empty=True)  # top ridge
    box(-1, 1, 4, 5, 17, 17, P["nail"])               # nail at tip
    put(1, 5, 13, P["nostril"]); put(-1, 5, 13, P["nostril"])
    # ---- eyes (+ glint) ----
    for sx in (3, -3):
        put(sx, 7, 10, P["eye"]); put(sx, 8, 10, P["eye"]); put(sx, 7, 11, P["eye"])
        put(sx, 8, 11, P["white"], only_empty=True)
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
def _crisp_outline(hi, out):
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


def render(SH, yaw, pitch, out=BODY_CANVAS, scale=1.45, cy_frac=0.5):
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
    return _crisp_outline(img, out)


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

    for sp, hen in (("mallard", False), ("hen", True)):
        SH = shade(build(hen, "folded"))
        # idle (gentle head-bob via slight pitch change, since back view is symmetric)
        save(render(SH, 0, PITCH), "%s_idle_0.png" % sp)
        save(render(SH, 0, PITCH + math.radians(4)), "%s_idle_1.png" % sp)
        # menu HERO + duck-select: front 3/4 so you see his face/chest (gameplay is back view)
        save(render(SH, math.radians(158), math.radians(30)), "%s_hero.png" % sp)
        # 7-frame banking sweep
        for i, yv in enumerate(BANK_YAW):
            save(render(SH, math.radians(yv), PITCH), "%s_bank_%d.png" % (sp, i))
        # back-compat aliases (duck-select turntable uses turn/side keys)
        save(render(SH, math.radians(-22), PITCH), "%s_turn_left.png" % sp)
        save(render(SH, math.radians(22), PITCH), "%s_turn_right.png" % sp)
        save(render(SH, math.radians(-SIDE_YAW), SIDE_PITCH), "%s_side_left.png" % sp)
        save(render(SH, math.radians(SIDE_YAW), SIDE_PITCH), "%s_side_right.png" % sp)
        # hops: wings spread (out / out_up flap)
        save(render(shade(build(hen, "out")), 0, PITCH), "%s_hop_0.png" % sp)
        save(render(shade(build(hen, "out_up")), 0, PITCH), "%s_hop_1.png" % sp)
        # face: close-up head, front-on (used at mega-hop apex + menus)
        save(render(SH, math.radians(180), math.radians(14), out=FACE_CANVAS,
                    scale=2.5, cy_frac=0.46), "%s_face.png" % sp)
        # real 3D slices for the mega-hop sprite-stack
        Vf = build(hen, "folded")
        for i, sl in enumerate(stack_slices(Vf, shade(Vf))):
            save(sl, "%s_stack_%02d.png" % (sp, i))
    print("ducks generated ->", art_dir)


if __name__ == "__main__":
    import os
    generate_ducks(os.path.join(os.path.dirname(__file__), "..", "art"))
