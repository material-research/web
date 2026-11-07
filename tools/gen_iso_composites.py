#!/usr/bin/env python3
"""Isometric illustration for the research area "Composite Materials Engineering" (no background, no text).

Usage: python3 tools/gen_iso_composites.py > _includes/illus/composites-iso.html
Scene: bamboo and ramie (plant fibre) -> alkaline treatment tank with a dipping fibre bundle ->
an exploded composite laminate that breathes -> flame test with a shield.
Made for a WHITE page: faces use light-to-mid blues and yellow accents, soft blue shadows on the ground, no floor slab.
Animation CSS (.iso-*) lives in assets/css/main.css.
"""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iso_lib as I
from iso_lib import P, f, pts, poly, box, hexagon, ell, hull, bamboo
from iso_lib import YEL, YEL_L, YEL_D, YEL_DD, DEEP, BLUE

I.OX, I.OY = 252.0, 62.0

# light-page palette
TOPC, LEFTC, RIGHTC = "#f4f8ff", "#a9c3f2", "#6b92dc"       # light top, mid left, deeper right
STEM, STEM_HI, NODE = "#7fa3ea", "#a9c3f2", "#0b3d91"
INK_L, INK_R = "#2a56b8", "#0b3d91"                          # dark metal (hoist)
OUT = 'stroke="#0b3d91" stroke-opacity=".18" stroke-width=".8" stroke-linejoin="round"'

o = []
o.append('<svg class="hv-iso iso-scene" viewBox="108 5 322 227" role="img" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">')
o.append('<defs><clipPath id="isoDipClip"><rect x="0" y="-200" width="600" height="%s"/></clipPath></defs>' % f(P(96, 98, 26)[1] + 206))


# ---------------------------------------------------------------- soft ground shadows (two layers each)
def blob(cx, cy, rx, ry):
    return (poly(ell(cx, cy, 0, rx + 5, ry + 5, 24), DEEP, 'fill-opacity=".05"') + poly(ell(cx, cy, 0, rx, ry, 24), DEEP, 'fill-opacity=".10"'))


o.append(blob(160, 52, 38, 34))     # under the floating laminate
o.append(blob(96, 98, 22, 22))      # tank
o.append(blob(157, 118, 14, 20))    # flame sample
o.append(blob(30, 132, 26, 16))     # plants

# ---------------------------------------------------------------- exploded laminate (back right), layers breathe apart
LX0, LX1, LY0, LY1 = 128, 190, 20, 72
LCX, LCY = (LX0 + LX1) / 2, (LY0 + LY1) / 2


def layer_bottom():
    return box(LX0, LY0, 36, LX1, LY1, 41, TOPC, LEFTC, RIGHTC, OUT)


def layer_core():
    g = box(LX0, LY0, 47, LX1, LY1, 55, "#dbe7ff", LEFTC, RIGHTC, OUT)
    hx = []
    for r_, cy in enumerate((26, 38, 50, 62)):
        for k in range(4 if r_ % 2 == 0 else 3):
            cx = 140 + k * 15 + (0 if r_ % 2 == 0 else 7.5)
            hx.append(poly(hexagon(cx, cy, 55, 5.6), YEL, 'fill-opacity=".95" stroke="%s" stroke-width=".6" stroke-linejoin="round"' % YEL_D))
    return g + "".join(hx)


def layer_fibre():
    g = box(LX0, LY0, 61, LX1, LY1, 65, "#fff3a6", YEL_D, YEL_DD)
    lx, ly = [], []
    for yy in range(LY0 + 5, LY1, 7):
        a, b = P(LX0 + 1, yy, 65), P(LX1 - 1, yy, 65)
        lx.append("M%s %sL%s %s" % (f(a[0]), f(a[1]), f(b[0]), f(b[1])))
    for xx in range(LX0 + 6, LX1, 8):
        a, b = P(xx, LY0 + 1, 65), P(xx, LY1 - 1, 65)
        ly.append("M%s %sL%s %s" % (f(a[0]), f(a[1]), f(b[0]), f(b[1])))
    g += '<path d="%s" fill="none" stroke="%s" stroke-width="2.2" stroke-linecap="round"/>' % (" ".join(lx), YEL)
    g += '<path d="%s" fill="none" stroke="#ffffff" stroke-width="1.3" stroke-linecap="round" stroke-opacity=".9"/>' % " ".join(ly)
    return g


def layer_top():
    g = box(LX0, LY0, 71, LX1, LY1, 77, TOPC, LEFTC, RIGHTC, OUT)
    g += poly(hexagon(LCX, LCY, 77, 9), "none", 'stroke="%s" stroke-width="1.6" stroke-linejoin="round"' % BLUE)
    g += poly(hexagon(LCX, LCY, 77, 4.5), YEL, 'stroke="%s" stroke-width=".8" stroke-linejoin="round"' % YEL_D)
    return g


for (gx, gy) in ((LX0, LY1), (LX1, LY1), (LX1, LY0)):
    a, b = P(gx, gy, 41), P(gx, gy, 71)
    o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#0b3d91" stroke-width="1" stroke-dasharray="2 3" stroke-opacity=".35"/>' % (f(a[0]), f(a[1]), f(b[0]), f(b[1])))
o.append('<g class="iso-lay iso-lay-0">%s</g>' % layer_bottom())
o.append('<g class="iso-lay iso-lay-1">%s</g>' % layer_core())
o.append('<g class="iso-lay iso-lay-2">%s</g>' % layer_fibre())
o.append('<g class="iso-lay iso-lay-3">%s</g>' % layer_top())

# ---------------------------------------------------------------- plant fibres (left): bamboo and ramie
LEAVES = (YEL, YEL, YEL_L, "#a9c3f2")
o.append(bamboo(14, 124, 92, 0, main=STEM, hi=STEM_HI, node=NODE, leaves=LEAVES))
o.append(bamboo(28, 138, 76, .7, main=STEM, hi=STEM_HI, node=NODE, leaves=LEAVES))


def ramie(x, y, delay):
    bx, by = P(x, y, 0)
    s = ['<g transform="translate(%s,%s)"><g class="iso-sway iso-sway-slow" style="animation-delay:%ss">' % (f(bx), f(by), f(delay))]
    s.append('<path d="M0 0 C1 -14 -1 -28 1 -46" fill="none" stroke="%s" stroke-width="3.2" stroke-linecap="round"/>' % STEM)
    for (cx, cy, rx, ry, rot, c) in ((-11, -22, 13, 5.2, -35, "#a9c3f2"), (12, -28, 13, 5.2, 35, YEL_L), (-10, -38, 12, 4.8, -28, YEL_L), (11, -44, 12, 4.8, 30, "#a9c3f2"), (0, -54, 11, 4.6, 90, YEL)):
        s.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(%s %s %s)"/>' % (f(cx), f(cy), f(rx), f(ry), c, rot, f(cx), f(cy)))
        s.append('<path d="M%s %s L%s %s" stroke="%s" stroke-width=".9" stroke-linecap="round" transform="rotate(%s %s %s)"/>' % (f(cx - rx + 2), f(cy), f(cx + rx - 2), f(cy), NODE, rot, f(cx), f(cy)))
    s.append('</g></g>')
    return "".join(s)


o.append(ramie(50, 134, .4))

# ---------------------------------------------------------------- alkaline treatment tank with a dipping fibre bundle
TCX, TCY, TR, TH = 96, 98, 17, 30
rb = ell(TCX, TCY, 0, TR, TR, 26)
rt = ell(TCX, TCY, TH, TR, TR, 26)
o.append(poly(hull(rb + rt), LEFTC, OUT))
half_b = [P(TCX + TR * math.cos(t), TCY + TR * math.sin(t), 0) for t in [math.radians(a) for a in range(-80, 81, 10)]]
half_t = [P(TCX + TR * math.cos(t), TCY + TR * math.sin(t), TH) for t in [math.radians(a) for a in range(-80, 81, 10)]]
o.append(poly(half_t + list(reversed(half_b)), RIGHTC, 'fill-opacity=".9"'))
o.append(poly(rt, TOPC, OUT))
o.append(poly(ell(TCX, TCY, TH - 4, TR - 2.4, TR - 2.4, 26), "#6b92dc"))
o.append('<polygon class="iso-ripple" points="%s" fill="none" stroke="#ffffff" stroke-width="1" stroke-opacity=".95"/>' % pts(ell(TCX, TCY, TH - 4, TR - 6, TR - 6, 20)))
for i, (bx_, by_) in enumerate(((-5, -3), (4, 2), (-2, 6), (7, -5))):
    p = P(TCX + bx_, TCY + by_, TH - 4)
    o.append('<circle class="iso-bubble" cx="%s" cy="%s" r="1.7" fill="#fff" style="animation-delay:%ss"/>' % (f(p[0]), f(p[1]), f(i * .55)))
o.append(box(90, 74, 0, 95, 79, 78, "#8fb0f0", INK_L, INK_R))
o.append(box(88, 74, 78, 106, 79, 83, "#8fb0f0", INK_L, INK_R))
bundle = box(TCX - 5, TCY - 5, 36, TCX + 5, TCY + 5, 46, YEL_L, YEL_D, YEL_DD)
sp = []
for k in range(1, 4):
    a, b = P(TCX - 4, TCY - 5 + k * 2.5, 46), P(TCX + 4, TCY - 5 + k * 2.5, 46)
    sp.append("M%s %sL%s %s" % (f(a[0]), f(a[1]), f(b[0]), f(b[1])))
bundle += '<path d="%s" fill="none" stroke="#fff" stroke-width=".9"/>' % " ".join(sp)
rod = box(TCX - 1.2, TCY - 1.2, 46, TCX + 1.2, TCY + 1.2, 80, "#8fb0f0", INK_L, INK_R)
arm = box(TCX - 1.5, 74, 79, TCX + 1.5, TCY + 1.5, 83, "#8fb0f0", INK_L, INK_R)
o.append('<g clip-path="url(#isoDipClip)"><g class="iso-dip">%s%s</g></g>' % (rod, bundle))
o.append(arm)

# ---------------------------------------------------------------- flame test (front right)
SX0, SX1, SY0, SY1 = 150, 164, 108, 128
o.append(box(SX0, SY0, 0, SX1, SY1, 36, TOPC, LEFTC, RIGHTC, OUT))
fx, fy = P(SX1, SY1, 36)
o.append('<g transform="matrix(%s,%s,0,1,%s,%s)"><polygon points="10,8 14.5,12.5 14.5,19 10,23.5 5.5,19 5.5,12.5" fill="%s" stroke="%s" stroke-width=".8"/></g>' % (f(I.K), f(-0.5), f(fx), f(fy), YEL, YEL_D))
fp = P(157, 134, 0)
o.append('<g transform="translate(%s,%s)"><g class="iso-flame">' % (f(fp[0]), f(fp[1])))
o.append('<path d="M0 0 C-9 -3 -11 -12 -6 -20 C-5 -15 -2 -14 -1 -24 C5 -18 10 -9 6 -2 C4 0 2 0 0 0 Z" fill="%s"/>' % YEL)
o.append('<path d="M0 -1 C-5 -3 -6 -9 -3 -13 C-1 -9 1 -9 2 -14 C5 -9 6 -4 3 -1 Z" fill="#fff"/></g></g>')
sp_ = P(174, 116, 68)
o.append('<g transform="translate(%s,%s)"><g class="iso-badge">' % (f(sp_[0]), f(sp_[1])))
o.append('<circle class="iso-ring" r="20" fill="none" stroke="%s" stroke-width="1.8"/>' % YEL_D)
o.append('<path d="M0 -13 L11.5 -8.5 V1 C11.5 8 6 12 0 15 C-6 12 -11.5 8 -11.5 1 V-8.5 Z" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (YEL, YEL_D))
o.append('<path d="M-5.5 0 L-1.5 4 L6 -5" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></g></g>' % DEEP)


# ---------------------------------------------------------------- labels for the four key components (English only, hidden on phones)
def label(cx, cy, text, tx, ty, delay):
    """navy chip centred at (cx, cy) with a leader to the target (tx, ty)"""
    w = 4.3 * len(text) + 12
    return ('<g class="iso-tag" style="--t:%ss"><line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#0b3d91" stroke-width="1" stroke-opacity=".7"/><circle cx="%s" cy="%s" r="2.2" fill="%s"/>'
            '<rect x="%s" y="%s" width="%s" height="12" rx="6" fill="#0b3d91"/>'
            '<text x="%s" y="%s" font-family="Inter,sans-serif" font-weight="600" font-size="7.1" fill="#fff" text-anchor="middle">%s</text></g>'
            % (f(delay), f(tx), f(cy + (6 if ty > cy else -6)), f(tx), f(ty), f(tx), f(ty), YEL, f(cx - w / 2), f(cy - 6), f(w), f(cx), f(cy + 2.5), text))


bam = P(14, 124, 92)
o.append(label(bam[0] + 2, 17, "Bamboo and ramie", bam[0], bam[1] + 1, .3))
o.append(label(252, 33, "Alkaline treatment", 236, 120, .5))
lam = P(159, 46, 77)
o.append(label(lam[0] + 2, 46, "Fibre-resin laminate", lam[0], lam[1] - 2, .7))
fl2 = P(157, 134, 0)
o.append(label(fl2[0], 220, "Flame retardancy", fl2[0], fl2[1] + 1, .9))

o.append('</svg>')
sys.stdout.write("".join(o))
