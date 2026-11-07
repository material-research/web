#!/usr/bin/env python3
"""Isometric illustration for the research area "Manufacturing, CNC & Simulation" (no background; three small English labels).

Usage: python3 tools/gen_iso_cnc.py > _includes/illus/cnc-iso.html
Scene: a CNC gantry whose spindle carriage sweeps across a clamped workpiece while a serpentine toolpath is drawn,
and a floating FEM mesh plate with a pulsing stress hotspot (simulation).
"""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iso_lib as I
from iso_lib import P, f, pts, poly, box, hexagon, ell, lbox, blob, label, svg_open
from iso_lib import YEL, YEL_L, YEL_D, YEL_DD, DEEP, BLUE, TOPC, LEFTC, RIGHTC, INK_L, INK_R, INK_T, OUT

I.OX, I.OY = 252.0, 46.0
o = [svg_open("108 12 322 172")]

o.append(blob(80, 85, 58, 44))       # machine
o.append(blob(177, 33, 36, 30))      # under the floating mesh

# ---------------------------------------------------------------- machine bed, workpiece, clamps
o.append(lbox(30, 48, 0, 130, 122, 14))
o.append(lbox(54, 64, 14, 118, 106, 22))
# serpentine toolpath on the workpiece (drawn progressively)
path_pts = [(66, 70), (66, 100), (78, 100), (78, 70), (90, 70), (90, 100), (102, 100), (102, 70)]
sc = [P(x, y, 22.2) for (x, y) in path_pts]
length = sum(math.hypot(sc[i + 1][0] - sc[i][0], sc[i + 1][1] - sc[i][1]) for i in range(len(sc) - 1))
d = "M" + " L".join(f(a) + " " + f(b) for a, b in sc)
o.append('<path d="%s" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" stroke-opacity=".28"/>' % (d, YEL_D))
o.append('<path class="iso-draw" d="%s" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" style="--len:%s;stroke-dasharray:%s;stroke-dashoffset:%s"/>' % (d, YEL, f(length), f(length), f(length)))
for (cx, cy) in ((50, 68), (50, 102), (122, 68), (122, 102)):
    o.append(lbox(cx - 4, cy - 4, 14, cx + 4, cy + 4, 21, "ink"))

# ---------------------------------------------------------------- gantry (fixed) with a moving spindle carriage
GX0, GX1 = 60, 72
o.append(lbox(GX0, 38, 0, GX1, 46, 70, "ink"))                      # back post
o.append(lbox(GX0 - 2, 38, 64, GX1 + 2, 132, 74, "light"))           # beam
# carriage with spindle and a bright tool, sliding along y
car = []
car.append(lbox(GX0 + 1, 82, 52, GX1 - 1, 94, 64, "ink"))
car.append(lbox(GX0 + 3, 85, 38, GX1 - 3, 91, 52, "light"))
car.append(lbox(GX0 + 4.6, 86.6, 28, GX1 - 4.6, 89.4, 38, "yellow"))
tip = P((GX0 + GX1) / 2, 88, 27)
car.append('<circle class="iso-spark" cx="%s" cy="%s" r="2.2" fill="%s"/>' % (f(tip[0]), f(tip[1] + 1), YEL))
o.append('<g class="iso-carriage">%s</g>' % "".join(car))
o.append(lbox(GX0, 124, 0, GX1, 132, 70, "ink"))                    # front post

# ---------------------------------------------------------------- FEM mesh plate floating at the back right
FX0, FX1, FY0, FY1, FZ = 150, 206, 8, 60, 52
o.append(box(FX0, FY0, FZ - 3, FX1, FY1, FZ, TOPC, LEFTC, RIGHTC, OUT))
cells = []
nx, ny = 8, 7
for i in range(nx):
    for j in range(ny):
        x0 = FX0 + i * (FX1 - FX0) / nx
        y0 = FY0 + j * (FY1 - FY0) / ny
        dx = (x0 + (FX1 - FX0) / (2 * nx) - 178)
        dy = (y0 + (FY1 - FY0) / (2 * ny) - 34)
        r2 = dx * dx + dy * dy
        if r2 < 120:
            col, op = YEL, ".95"
        elif r2 < 340:
            col, op = YEL_L, ".75"
        elif r2 < 700:
            col, op = "#dbe7ff", "1"
        else:
            col = None
        if col:
            cells.append(poly([P(x0, y0, FZ), P(x0 + (FX1 - FX0) / nx, y0, FZ), P(x0 + (FX1 - FX0) / nx, y0 + (FY1 - FY0) / ny, FZ), P(x0, y0 + (FY1 - FY0) / ny, FZ)], col, 'fill-opacity="%s"' % op))
o.append("".join(cells))
hot = poly(ell(178, 34, FZ + .2, 9, 9, 18), YEL, 'fill-opacity=".9"')
o.append('<g class="iso-hot">%s</g>' % hot)
grid = []
for i in range(nx + 1):
    a, b = P(FX0 + i * (FX1 - FX0) / nx, FY0, FZ), P(FX0 + i * (FX1 - FX0) / nx, FY1, FZ)
    grid.append("M%s %sL%s %s" % (f(a[0]), f(a[1]), f(b[0]), f(b[1])))
for j in range(ny + 1):
    a, b = P(FX0, FY0 + j * (FY1 - FY0) / ny, FZ), P(FX1, FY0 + j * (FY1 - FY0) / ny, FZ)
    grid.append("M%s %sL%s %s" % (f(a[0]), f(a[1]), f(b[0]), f(b[1])))
o.append('<path d="%s" fill="none" stroke="#2a56b8" stroke-width=".8" stroke-opacity=".75"/>' % " ".join(grid))
for (nx_, ny_) in ((FX0, FY0), (FX1, FY0), (FX1, FY1), (FX0, FY1)):
    p = P(nx_, ny_, FZ)
    o.append('<circle cx="%s" cy="%s" r="2" fill="%s"/>' % (f(p[0]), f(p[1]), INK_R))

# ---------------------------------------------------------------- labels
a1 = P(66, 132, 74)
o.append(label(a1[0] - 14, 24, "CNC machining", a1[0], a1[1] - 1, .3))
a2 = P(102, 70, 22)
o.append(label(a2[0] + 80, 138, "Toolpath", a2[0] + 1, a2[1] + 1, .5, side="left"))
a3 = P(178, 34, FZ)
o.append(label(a3[0], 24, "FEM simulation", a3[0], a3[1], .7))

o.append('</svg>')
sys.stdout.write("".join(o))
