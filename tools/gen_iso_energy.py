#!/usr/bin/env python3
"""Isometric illustration for the research area "Energy & Drive Systems" (no background; four small English labels).

Usage: python3 tools/gen_iso_energy.py > _includes/illus/energy-iso.html
Scene: wind turbine (rotor spins) | drive motor with a spinning coupling -> pump with a flowing pipe and a sensor |
standby generator with an automatic-start lamp and an energy line to the motor.
"""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iso_lib as I
from iso_lib import P, f, pts, poly, box, hexagon, ell, hull, lbox, blob, cylinder, label, svg_open, face_x, face_y
from iso_lib import YEL, YEL_L, YEL_D, YEL_DD, DEEP, BLUE, TOPC, LEFTC, RIGHTC, INK_L, INK_R, INK_T, OUT

I.OX, I.OY = 262.0, 46.0
o = [svg_open("108 10 322 221")]
SC, CX0, CY0 = 0.88, 262.0, 128.0          # the whole scene is scaled a little so that everything fits the frame


def T(pt):
    return (CX0 + (pt[0] - CX0) * SC, CY0 + (pt[1] - CY0) * SC)


o.append('<g transform="translate(%s,%s) scale(%s) translate(%s,%s)">' % (f(CX0), f(CY0), SC, f(-CX0), f(-CY0)))

o.append(blob(48, 140, 24, 22))      # turbine
o.append(blob(100, 99, 36, 26))      # motor
o.append(blob(140, 80, 20, 40))      # pump and pipe
o.append(blob(208, 133, 28, 24))     # generator


def ring_yz(x, yc, zc, r, n=22):
    return [P(x, yc + r * math.cos(2 * math.pi * i / n), zc + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


# ---------------------------------------------------------------- pipe from the pump to the back, with flowing dashes and a sensor
o.append(lbox(137, 30, 6, 143, 92, 14))
pf = [P(140, 90, 14.2), P(140, 32, 14.2)]
o.append('<path class="iso-flow" d="M%s %sL%s %s" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 8"/>' % (f(pf[0][0]), f(pf[0][1]), f(pf[1][0]), f(pf[1][1])))
o.append(lbox(134, 52, 14, 146, 62, 24, "ink"))
lp = P(140, 62, 24)
o.append('<circle class="iso-lamp" cx="%s" cy="%s" r="2.2" fill="%s"/>' % (f(lp[0]), f(lp[1]), YEL))
o.append(lbox(139, 56, 24, 141, 58, 33, "light"))
sg = P(140, 57, 35)
o.append('<g transform="translate(%s,%s)"><path d="M-4 0 Q 0 -4 4 0 M-7 -2 Q 0 -9 7 -2" fill="none" stroke="%s" stroke-width="1.3" stroke-linecap="round" class="iso-wave"/></g>' % (f(sg[0]), f(sg[1]), YEL_D))

# ---------------------------------------------------------------- wind turbine (left); the rotor spins in the plane facing down-left
o.append(lbox(45, 137, 0, 51, 143, 58))
o.append(lbox(43, 132, 56, 53, 148, 66, "light"))
hub = (48, 149, 61)
hp = P(*hub)
blades = ""
for a in (0, 120, 240):
    blades += '<g transform="rotate(%d)"><path d="M-3 0 C-4 -9 -3 -19 0 -26 C3 -19 4 -9 3 0 Z" fill="%s" stroke="%s" stroke-width=".9" stroke-linejoin="round"/><path d="M-1 -20 L0 -26 L1 -20Z" fill="%s"/></g>' % (a, TOPC, INK_L, YEL)
o.append('<g transform="%s"><g class="iso-spin iso-spin-slow">%s<circle r="3.6" fill="%s" stroke="%s" stroke-width=".9"/></g></g>' % (I.face_y(*hub), blades, YEL, YEL_D))

# ---------------------------------------------------------------- drive motor (cylinder along x) with a spinning coupling
o.append(lbox(72, 84, 0, 114, 116, 4, "ink"))
yc, zc, R = 100, 14, 11
b0, b1 = ring_yz(76, yc, zc, R), ring_yz(110, yc, zc, R)
o.append(poly(hull(b0 + b1), LEFTC, OUT))
# right-hand shading of the cylinder
o.append(poly(hull(ring_yz(76, yc + 3, zc - 6, 5) + ring_yz(110, yc + 3, zc - 6, 5)), RIGHTC, 'fill-opacity=".85"'))
# cooling fins on top
for k in range(7):
    xx = 80 + k * 4.6
    o.append(box(xx, 95, zc + R - 1, xx + 2, 105, zc + R + 3, TOPC, LEFTC, RIGHTC, OUT))
o.append(poly(b1, TOPC, OUT))
o.append(poly(ring_yz(110, yc, zc, R * .55), "#dbe7ff", 'stroke="#0b3d91" stroke-opacity=".25" stroke-width=".8"'))
# shaft and the spinning coupling (a gear in the plane x = const)
o.append(lbox(110, 98.5, 12.5, 124, 101.5, 15.5, "ink"))
cp = (124, 100, 14)
gear = "".join('<rect x="-1.4" y="-9" width="2.8" height="4" rx="1" fill="%s" transform="rotate(%d)"/>' % (YEL_D, a) for a in range(0, 360, 45))
o.append('<g transform="%s"><g class="iso-spin">%s<circle r="6.4" fill="%s" stroke="%s" stroke-width="1"/><circle r="2" fill="%s"/></g></g>' % (I.face_x(*cp), gear, YEL, YEL_D, INK_R))

# ---------------------------------------------------------------- pump (vertical volute) at the end of the shaft
o.append(cylinder(140, 100, 11, 4, 20, LEFTC, RIGHTC, TOPC))
o.append(poly(ell(140, 100, 20.3, 5, 5, 16), YEL, 'stroke="%s" stroke-width=".8"' % YEL_D))
o.append(lbox(137, 88, 8, 143, 94, 14, "light"))

# ---------------------------------------------------------------- standby generator (front right) with an auto-start lamp
GX0, GX1, GY0, GY1 = 188, 228, 118, 148
o.append(lbox(GX0, GY0, 0, GX1, GY1, 22))
o.append(poly([P(GX0, GY0, 22), P(GX1, GY0, 22), P(GX1, GY0 + 5, 22), P(GX0, GY0 + 5, 22)], YEL))
o.append(lbox(GX0 + 4, GY0 + 4, 22, GX0 + 9, GY0 + 9, 34, "ink"))               # exhaust
o.append(lbox(GX1 - 12, GY1 - 10, 22, GX1 - 4, GY1 - 3, 28, "yellow"))           # control box
gl = P(GX1 - 8, GY1 - 6.5, 28.5)
o.append('<circle class="iso-lamp" cx="%s" cy="%s" r="2.2" fill="%s" stroke="%s" stroke-width=".7"/>' % (f(gl[0]), f(gl[1]), "#ffffff", YEL_D))
bolt = '<path d="M17 3 L9 15 H15 L12 25 L22 11 H16 Z" fill="%s" stroke="%s" stroke-width="1" stroke-linejoin="round"/>' % (YEL, YEL_D)
fx = P(GX1, GY1, 22)
o.append('<g transform="matrix(%s,%s,0,1,%s,%s)">%s</g>' % (f(I.K), f(-0.5), f(fx[0]), f(fx[1]), bolt))
# energy line from the generator to the motor
e0, e1 = P(GX0, 132, 14), P(112, 108, 4)
o.append('<path class="iso-flow iso-flow-y" d="M%s %s L%s %s" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round" stroke-dasharray="5 6"/>' % (f(e0[0]), f(e0[1]), f(e1[0]), f(e1[1]), YEL))

o.append('</g>')

# ---------------------------------------------------------------- labels
w1 = T(P(*hub))
o.append(label(w1[0] - 6, 22, "Wind turbine", w1[0], w1[1], .3))
m1 = T(P(92, 100, 26))
o.append(label(m1[0], 40, "Drive motor", m1[0], m1[1], .5))
s1 = T(P(140, 57, 36))
o.append(label(s1[0] + 40, 26, "Pump and sensors", s1[0], s1[1], .7))
g1 = T(P(GX1 - 4, GY0 + 4, 22))
o.append(label(g1[0] + 30, 170, "Standby generator", g1[0], g1[1], .9, side="left"))

o.append('</svg>')
sys.stdout.write("".join(o))
