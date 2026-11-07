#!/usr/bin/env python3
"""Isometric illustration for the research area "Agro-Processing Machinery" (no background; four small English labels).

Usage: python3 tools/gen_iso_agro.py > _includes/illus/agro-iso.html
Scene (left to right): wet coffee-cherry tank (cherries circulate, agitator spins) ->
coconut skin peeler (roller spins, coconut bobs, husk flies off) -> ginger grating and pressing (platen presses, juice drops).
"""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iso_lib as I
from iso_lib import P, f, pts, poly, box, hexagon, ell, lbox, blob, cylinder, label, svg_open, face_y, face_x
from iso_lib import YEL, YEL_L, YEL_D, YEL_DD, DEEP, BLUE, TOPC, LEFTC, RIGHTC, INK_L, INK_R, INK_T, OUT

I.OX, I.OY = 252.0, 42.0
o = [svg_open("108 12 322 174")]

# ground shadows
o.append(blob(46, 120, 36, 30))
o.append(blob(115, 96, 30, 24))
o.append(blob(172, 52, 34, 30))

# ---------------------------------------------------------------- A) wet coffee tank with circulating cherries and an agitator
TX0, TX1, TY0, TY1 = 20, 74, 98, 142
o.append(lbox(TX0, TY0, 0, TX1, TY1, 24))
water = [P(TX0 + 4, TY0 + 4, 24.1), P(TX1 - 4, TY0 + 4, 24.1), P(TX1 - 4, TY1 - 4, 24.1), P(TX0 + 4, TY1 - 4, 24.1)]
o.append(poly(water, "#6b92dc"))
o.append(poly([water[0], water[1], water[2], water[3]], "none", 'stroke="#ffffff" stroke-opacity=".6" stroke-width=".9"'))
cx, cy = (TX0 + TX1) / 2, (TY0 + TY1) / 2
c0 = P(cx, cy, 24.5)
o.append('<g transform="translate(%s,%s) scale(1,.5)"><g class="iso-orbit iso-orbit-fast">%s</g></g>' % (f(c0[0]), f(c0[1]), "".join('<circle cx="%s" cy="%s" r="3.4" fill="%s" stroke="%s" stroke-width=".7"/>' % (f(19 * math.cos(a)), f(19 * math.sin(a)), YEL, YEL_D) for a in [i * math.pi / 2.5 for i in range(5)])))
o.append('<g transform="translate(%s,%s) scale(1,.5)"><g class="iso-orbit iso-orbit-slow2">%s</g></g>' % (f(c0[0]), f(c0[1]), "".join('<circle cx="%s" cy="%s" r="2.6" fill="%s"/>' % (f(11 * math.cos(a)), f(11 * math.sin(a)), "#ffffff") for a in [i * math.pi / 2 + .4 for i in range(4)])))
# agitator
o.append(lbox(cx - 1.3, cy - 1.3, 24, cx + 1.3, cy + 1.3, 50, "ink"))
o.append(lbox(cx - 5, cy - 5, 50, cx + 5, cy + 5, 58, "ink"))
b0 = P(cx, cy, 45)
o.append('<g transform="translate(%s,%s) scale(1,.5)"><g class="iso-spin"><rect x="-13" y="-1.6" width="26" height="3.2" rx="1.6" fill="%s"/></g></g>' % (f(b0[0]), f(b0[1]), INK_T))

# ---------------------------------------------------------------- B) coconut skin peeler
PX0, PX1, PY0, PY1 = 95, 135, 80, 112
o.append(lbox(PX0, PY0, 0, PX1, PY1, 20))
o.append(lbox(PX0 + 5, PY0 + 4, 20, PX1 - 5, PY1 - 4, 32, "ink"))
# roller wheel on the front-left face (spins)
wh = P(115, PY1, 10)
o.append('<g transform="translate(%s,%s)"><g transform="matrix(%s,.5,0,1,0,0)"><circle r="7.6" fill="%s" stroke="%s" stroke-width="1.2"/><g class="iso-spin">%s<circle r="1.8" fill="%s"/></g></g></g>' % (
    f(wh[0]), f(wh[1]), f(I.K), TOPC, INK_L,
    "".join('<line x1="0" y1="0" x2="%s" y2="%s" stroke="%s" stroke-width="1.6" stroke-linecap="round"/>' % (f(6.2 * math.cos(a)), f(6.2 * math.sin(a)), YEL_D) for a in [i * math.pi / 3 for i in range(6)]), INK_L))
# coconut (bobs) with three small eyes
cc = P(115, 96, 41)
o.append('<g transform="translate(%s,%s)"><g class="iso-bob"><circle r="7.4" fill="#dbe7ff" stroke="#0b3d91" stroke-opacity=".25" stroke-width=".8"/><ellipse cx="-2.4" cy="-2.6" rx="2.2" ry="1.3" fill="#fff" fill-opacity=".9"/><circle cx="-1.6" cy="1.2" r=".9" fill="%s"/><circle cx="1.8" cy="1.8" r=".9" fill="%s"/><circle cx="1.6" cy="-.8" r=".9" fill="%s"/></g></g>' % (f(cc[0]), f(cc[1]), INK_R, INK_R, INK_R))
# husk pieces flying off
hp = P(135, 96, 24)
for i, (dx, dy, d) in enumerate(((3, 0, 0), (9, 6, .5), (5, 10, 1.0))):
    o.append('<ellipse class="iso-husk" cx="%s" cy="%s" rx="4" ry="1.6" fill="%s" transform="rotate(%s %s %s)" style="animation-delay:%ss"/>' % (f(hp[0] + dx), f(hp[1] + dy), YEL, -25 + i * 22, f(hp[0] + dx), f(hp[1] + dy), f(d)))

# ---------------------------------------------------------------- C) ginger grating and pressing
GX0, GX1, GY0, GY1 = 148, 196, 28, 76
o.append(lbox(GX0, GY0, 0, GX1, GY1, 8))
o.append(lbox(168, 28, 8, 176, 34, 62, "ink"))
o.append(lbox(168, 70, 8, 176, 76, 62, "ink"))
# ginger piece on the base
o.append(box(164, 44, 8, 180, 60, 15, "#fff3a6", YEL_D, YEL_DD))
o.append('<polygon points="%s" fill="%s"/>' % (pts([P(168, 48, 15), P(172, 46, 15), P(176, 50, 15), P(172, 55, 15)]), YEL))
rod = lbox(170, 50, 42, 174, 54, 62, "ink")
plat = lbox(162, 40, 28, 182, 64, 38, "light")
o.append('<g class="iso-rod iso-rod-s">%s</g><g class="iso-platen">%s</g>' % (rod, plat))
o.append(lbox(164, 26, 62, 180, 78, 70, "ink"))
# juice cup and drops
o.append(cylinder(170, 90, 7, 0, 10, LEFTC, RIGHTC, "#dbe7ff"))
o.append(poly(ell(170, 90, 8, 5.2, 5.2, 18), "#6b92dc"))
dp = P(182, 66, 20)
for i, d in enumerate((0, .6)):
    o.append('<path class="iso-fall iso-fall-s" d="M%s %s c-2 3 -2.5 5 0 6.2 c2.5 -1.2 2 -3.2 0 -6.2z" fill="#6b92dc" style="animation-delay:%ss"/>' % (f(dp[0] - 6 + i * 6), f(dp[1] + i * 2), f(d)))

# ---------------------------------------------------------------- labels
t1 = P(22, 118, 22)
o.append(label(t1[0] - 4, 24, "Coffee cherry grading", t1[0], t1[1], .3))
o.append(label(cc[0], 40, "Coconut skin peeler", cc[0], cc[1] - 8, .5))
g1 = P(170, 48, 70)
o.append(label(g1[0], 24, "Ginger grating and pressing", g1[0], g1[1], .7))

o.append('</svg>')
sys.stdout.write("".join(o))
