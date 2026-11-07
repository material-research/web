#!/usr/bin/env python3
"""Generate the isometric hero illustration (inline SVG, CSS-animated) for the ARG site.

Usage: python3 tools/gen_iso_hero.py > _includes/illus/hero-iso.html
The animation CSS (.iso-*) lives in assets/css/main.css.
World coordinates: x runs down-right, y runs down-left, z is up. The conveyor runs along y,
from the front-left (large y, plant-based inputs) to the back-right (y = 0, products).
Labels are English only (owner's decision).
"""
import math, sys

K = 0.8660254          # cos 30
OX, OY = 300.0, 82.0   # screen position of the world origin


def P(x, y, z=0):
    return (OX + (x - y) * K, OY + (x + y) * 0.5 - z)


def f(v):
    s = ("%.1f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def pts(points):
    return " ".join(f(a) + "," + f(b) for a, b in points)


def poly(points, fill, extra=""):
    return '<polygon points="%s" fill="%s"%s/>' % (pts(points), fill, (" " + extra) if extra else "")


def box(x0, y0, z0, x1, y1, z1, top, left, right, extra=""):
    """left = face at y1 (faces down-left), right = face at x1 (faces down-right)."""
    t = [P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)]
    l = [P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)]
    r = [P(x1, y0, z0), P(x1, y1, z0), P(x1, y1, z1), P(x1, y0, z1)]
    return poly(l, left, extra) + poly(r, right, extra) + poly(t, top, extra)


def hexagon(cx, cy, z, R):
    return [P(cx + R * math.cos(math.radians(60 * i)), cy + R * math.sin(math.radians(60 * i)), z) for i in range(6)]


def ell(cx, cy, z, rx, ry, n=24):
    return [P(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n), z) for i in range(n)]


# palette (blue + yellow only; white as the light colour)
WHITE, PALE, SOFT, MID, BLUE, DEEP, DARK, NAVY = "#ffffff", "#dbe7ff", "#8fb0f0", "#5f86d6", "#2a56b8", "#0b3d91", "#082d6e", "#061f52"
YEL, YEL_L, YEL_D = "#ffd60a", "#ffe45c", "#d9b000"
FACE_L, FACE_R = "#e3ebfb", "#c3d4f4"          # soft white faces (left / right)

o = []
o.append('<svg class="hv hv-iso" viewBox="28 6 478 290" role="img" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">')
o.append('<defs><radialGradient id="isoOrb" cx="38%" cy="35%" r="70%"><stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#ffe45c"/><stop offset="1" stop-color="#e0a800"/></radialGradient></defs>')

# ---------------------------------------------------------------- geometry
BX0, BX1 = 44, 80      # belt x
BY0, BY1 = 0, 300      # belt y (end, start)
BZ0, BZ1 = 14, 24      # belt z
MX0, MX1, MY0, MY1, MZ = 36, 88, 106, 172, 80   # machine
CUBE = 22
CUBE_Y0 = [268, 238, 208, 178]                  # nearest the start first

# ---------------------------------------------------------------- ground shadow
o.append(poly([P(34, 308), P(98, 308), P(98, 2), P(34, 2)], DARK, 'fill-opacity=".30"'))
o.append(poly([P(92, 94), P(138, 94), P(138, -8), P(92, -8)], DARK, 'fill-opacity=".28"'))

# ---------------------------------------------------------------- belt legs, belt
for ly in (20, 90, 160, 230):
    o.append(box(BX1 - 5, ly, 0, BX1 - 1, ly + 5, BZ0, MID, SOFT, BLUE))
    o.append(box(BX0 + 1, ly, 0, BX0 + 5, ly + 5, BZ0, MID, SOFT, BLUE))
o.append(box(BX0, BY0, BZ0, BX1, BY1, BZ1, NAVY, "#12347a", "#0d2a68"))
# belt rails (lighter top edges)
o.append(poly([P(BX0, BY0, BZ1), P(BX0 + 2.5, BY0, BZ1), P(BX0 + 2.5, BY1, BZ1), P(BX0, BY1, BZ1)], SOFT, 'fill-opacity=".55"'))
o.append(poly([P(BX1 - 2.5, BY0, BZ1), P(BX1, BY0, BZ1), P(BX1, BY1, BZ1), P(BX1 - 2.5, BY1, BZ1)], SOFT, 'fill-opacity=".55"'))
# moving stripes on the belt top (clipped), they run toward y = 0
bt = [P(BX0 + 2.5, BY0, BZ1), P(BX1 - 2.5, BY0, BZ1), P(BX1 - 2.5, BY1, BZ1), P(BX0 + 2.5, BY1, BZ1)]
o.append('<clipPath id="isoBeltClip"><polygon points="%s"/></clipPath>' % pts(bt))
stripes = []
step = 14
for i in range(-1, int(BY1 / step) + 2):
    y = i * step + 3
    a, b = P(BX0 + 2.5, y, BZ1), P(BX1 - 2.5, y, BZ1)
    stripes.append("M%s %sL%s %s" % (f(a[0]), f(a[1]), f(b[0]), f(b[1])))
o.append('<g clip-path="url(#isoBeltClip)"><path class="iso-stripes" d="%s" fill="none" stroke="#3b64b5" stroke-width="1.6"/></g>' % " ".join(stripes))

# ---------------------------------------------------------------- orb at the belt end
oc = P(62, -4, 66)
o.append('<g transform="translate(%s,%s)">' % (f(oc[0]), f(oc[1])))
o.append('<circle class="iso-halo" r="30" fill="%s" fill-opacity=".16"/><circle class="iso-halo iso-halo-2" r="21" fill="%s" fill-opacity=".24"/>' % (YEL, YEL))
o.append('<g transform="scale(1,.5)"><g class="iso-orbit"><circle cx="26" cy="0" r="2.4" fill="%s"/><circle cx="-26" cy="0" r="1.8" fill="#fff"/></g></g>' % YEL)
o.append('<circle class="iso-orb" r="12" fill="url(#isoOrb)"/>')
o.append('<ellipse cx="-4" cy="-5" rx="3.6" ry="2.2" fill="#fff" fill-opacity=".85" transform="rotate(-25 -4 -5)"/>')
o.append('</g>')

# ---------------------------------------------------------------- output panels riding the belt (hidden behind the machine at first)
def panel():
    x0, x1, y0, y1, z0 = BX0 + 8, BX1 - 8, 76, 98, BZ1
    out = box(x0, y0, z0, x1, y1, z0 + 5, WHITE, SOFT, MID)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for (dx, dy) in ((0, -6), (0, 0), (0, 6)):
        out += poly(hexagon(cx + dx, cy + dy, z0 + 5, 3.6), YEL, 'stroke="%s" stroke-width=".5" stroke-linejoin="round"' % YEL_D)
    return out
for i in range(3):
    o.append('<g class="iso-out" style="--d:%ss">%s</g>' % (f(-1.7 * i), panel()))

# ---------------------------------------------------------------- output showcase (right of the belt)
# drawn back to front: flame-retardant panel (y small, farthest), safety cabin, grain storage (y large, nearest)
o.append(box(94, -8, 0, 132, 100, 5, PALE, SOFT, MID))
# flame-retardant panel standing on the showcase, flame icon on its right face
o.append(box(106, 0, 5, 118, 24, 40, WHITE, FACE_L, FACE_R))
fl = P(118, 24, 40)
o.append('<g transform="matrix(%s,%s,0,1,%s,%s)">' % (f(K), f(-0.5), f(fl[0]), f(fl[1])))
o.append('<path d="M11 8 C14 13 18 15 18 21 C18 26 15 29 11 29 C7 29 4 26 4 21 C4 17 7 16 8 12 C9 14 10 14 11 8 Z" fill="%s"/>' % YEL)
o.append('<path d="M11 18 C12.5 20.5 14 21.5 14 24 C14 26 12.8 27 11 27 C9.2 27 8 26 8 24 C8 22 10 21.5 11 18 Z" fill="#fff"/></g>')
# safety cabin (flat roof, door, window)
cx0, cx1, cy0, cy1 = 100, 124, 36, 60
o.append(box(cx0, cy0, 5, cx1, cy1, 27, WHITE, FACE_L, FACE_R))
o.append(box(cx0 - 2, cy0 - 2, 27, cx1 + 2, cy1 + 2, 30, YEL, YEL_D, "#b58f00"))
o.append(poly([P(104, cy1, 5), P(113, cy1, 5), P(113, cy1, 20), P(104, cy1, 20)], BLUE))   # door
o.append(poly([P(cx1, 42, 13), P(cx1, 53, 13), P(cx1, 53, 22), P(cx1, 42, 22)], BLUE))      # window (right face)
# grain storage building (gable roof along y)
wx0, wx1, wy0, wy1 = 98, 126, 68, 96
o.append(poly([P(wx0, wy1, 5), P(wx1, wy1, 5), P(wx1, wy1, 21), P(112, wy1, 31), P(wx0, wy1, 21)], FACE_L))
o.append(poly([P(wx1, wy0, 5), P(wx1, wy1, 5), P(wx1, wy1, 21), P(wx1, wy0, 21)], FACE_R))
o.append(poly([P(wx0, wy0, 21), P(wx0, wy1, 21), P(112, wy1, 31), P(112, wy0, 31)], "#f4f8ff"))
o.append(poly([P(wx1, wy0, 21), P(wx1, wy1, 21), P(112, wy1, 31), P(112, wy0, 31)], YEL))
o.append(poly([P(106, wy1, 5), P(118, wy1, 5), P(118, wy1, 16), P(106, wy1, 16)], BLUE))   # door

# ---------------------------------------------------------------- machine
o.append(box(MX0, MY0, 0, MX1, MY1, MZ, WHITE, FACE_L, FACE_R, 'stroke-linejoin="round"'))
# tunnel opening on the front-left face (belt enters here)
tun = [P(50, MY1, BZ1), P(74, MY1, BZ1), P(74, MY1, 54), P(50, MY1, 54)]
o.append(poly(tun, NAVY))
inner = [P(53, MY1, BZ1), P(71, MY1, BZ1), P(71, MY1, 50), P(53, MY1, 50)]
o.append('<polygon class="iso-tunnel" points="%s" fill="%s"/>' % (pts(inner), YEL))
o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.4" stroke-linejoin="round"/>' % (pts([P(50, MY1, BZ1), P(50, MY1, 54), P(74, MY1, 54), P(74, MY1, BZ1)]), SOFT))
# indicator dots above the tunnel
for dx in (54, 62, 70):
    p = P(dx, MY1, 66)
    o.append('<circle class="iso-lamp" cx="%s" cy="%s" r="2" fill="%s" style="animation-delay:%ss"/>' % (f(p[0]), f(p[1]), YEL, f((dx - 54) / 8 * 0.4)))
# lettering on the right face (runs up-right)
tp = P(MX1, MY1, MZ - 12)
o.append('<g transform="matrix(%s,%s,0,1,%s,%s)" fill="%s" font-family="Poppins,Inter,sans-serif" font-weight="700">' % (f(K), f(-0.5), f(tp[0]), f(tp[1]), DEEP))
o.append('<text x="4" y="10" font-size="9.4" textLength="52" lengthAdjust="spacingAndGlyphs">COMPOSITE</text>')
o.append('<text x="4" y="22" font-size="9.4" textLength="30" lengthAdjust="spacingAndGlyphs">PANEL</text>')
o.append('<text x="4" y="34" font-size="9.4" textLength="57" lengthAdjust="spacingAndGlyphs">PRODUCTION</text>')
o.append('<rect x="4" y="40" width="22" height="3" rx="1.5" fill="%s"/></g>' % YEL)
# vent box on top (dark) with a status lamp
o.append(box(54, 122, MZ, 72, 142, MZ + 9, NAVY, "#12347a", "#0d2a68"))
lp = P(63, 142, MZ + 4.5)
o.append('<circle class="iso-lamp" cx="%s" cy="%s" r="2.2" fill="%s"/>' % (f(lp[0]), f(lp[1]), YEL))
# yellow accent strip on top
o.append(poly([P(MX0 + 4, MY1 - 8, MZ), P(MX1 - 4, MY1 - 8, MZ), P(MX1 - 4, MY1 - 4, MZ), P(MX0 + 4, MY1 - 4, MZ)], YEL))

# ---------------------------------------------------------------- input cubes with icons (in front of the machine)
names = ["Bamboo", "Ramie", "Rice husk", "Coconut"]
def icon(kind):
    """flat 20x20 pictogram in the cube's top plane (local u along +x, v along +y)"""
    c = DEEP
    if kind == 0:   # bamboo: three culms with nodes
        s = ''.join('<rect x="%s" y="2" width="3.4" height="16" rx="1.4" fill="%s"/>' % (3 + 6 * i, c) for i in range(3))
        s += ''.join('<rect x="%s" y="%s" width="5.4" height="1.2" fill="%s"/>' % (2 + 6 * i, 7 + 4 * (i % 2), YEL) for i in range(3))
        return s
    if kind == 1:   # ramie: leaf with a vein
        return '<path d="M10 2 C17 6 17 14 10 18 C3 14 3 6 10 2 Z" fill="%s"/><path d="M10 4 V17" stroke="%s" stroke-width="1.2"/>' % (c, YEL)
    if kind == 2:   # rice husk: grains
        return ''.join('<ellipse cx="%s" cy="%s" rx="2" ry="4.2" fill="%s" transform="rotate(%s %s %s)"/>' % (x, y, c if i % 2 == 0 else YEL_D, r, x, y) for i, (x, y, r) in enumerate(((6, 6, -25), (14, 6, 25), (10, 13, 0), (4, 14, 20), (16, 14, -20))))
    if kind == 3:   # coconut trunk: log end rings
        return '<circle cx="10" cy="10" r="8" fill="%s"/><circle cx="10" cy="10" r="5" fill="none" stroke="%s" stroke-width="1.3"/><circle cx="10" cy="10" r="1.6" fill="%s"/>' % (c, YEL, YEL)
    return '<path d="M2 6 Q6 2 10 6 T18 6" fill="none" stroke="%s" stroke-width="1.8" stroke-linecap="round"/><path d="M2 11 Q6 7 10 11 T18 11" fill="none" stroke="%s" stroke-width="1.8" stroke-linecap="round"/><path d="M2 16 Q6 12 10 16 T18 16" fill="none" stroke="%s" stroke-width="1.8" stroke-linecap="round"/>' % (c, YEL_D, c)

CX0 = (BX0 + BX1) / 2 - CUBE / 2
chips = []
for i, y0 in enumerate(CUBE_Y0):
    y1 = y0 + CUBE
    z0, z1 = BZ1, BZ1 + CUBE
    g = '<g class="iso-cube" style="--i:%d">' % i
    g += box(CX0, y0, z0, CX0 + CUBE, y1, z1, WHITE, FACE_L, FACE_R, 'stroke="#ffffff" stroke-width="1.6" stroke-linejoin="round"')
    # icon on the top face: local (u,v) -> screen via the top-plane matrix
    o0 = P(CX0 + 1.5, y0 + 1.5, z1)
    sc = (CUBE - 3) / 20.0
    g += '<g transform="matrix(%s,%s,%s,%s,%s,%s)">%s</g>' % (f(K * sc), f(0.5 * sc), f(-K * sc), f(0.5 * sc), f(o0[0]), f(o0[1]), icon(i))
    g += '</g>'
    o.append(g)
    # label chip with a leader line (chip sits up-left of the cube, right-aligned at the leader)
    ax, ay = P(CX0 + CUBE / 2, y0 + CUBE / 2, z1)
    lx, ly = ax - 10, ay - 29 - i * 5
    label = names[i]
    w = 5.25 * len(label) + 13
    chips.append((ax, ay, lx, ly, label, w, i))

# ---------------------------------------------------------------- chips (drawn last, above everything)
def chip(x, y, label, w, delay, anchor="end", minor=True):
    x0 = x - w if anchor == "end" else x
    return ('<g class="iso-tag%s" style="--t:%ss"><rect x="%s" y="%s" width="%s" height="14" rx="7" fill="#fff"/>'
            '<text x="%s" y="%s" font-family="Inter,sans-serif" font-weight="600" font-size="9" fill="%s" text-anchor="middle">%s</text></g>'
            % (" iso-tag--minor" if minor else "", f(delay), f(x0), f(y - 7), f(w), f(x0 + w / 2), f(y + 3.1), DEEP, label))
for (ax, ay, lx, ly, label, w, i) in chips:
    t = 0.3 + i * 0.18
    o.append('<g class="iso-tag iso-tag--minor" style="--t:%ss"><line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#fff" stroke-width="1" stroke-opacity=".9"/><circle cx="%s" cy="%s" r="2.2" fill="%s"/></g>' % (f(t), f(ax), f(ay), f(lx), f(ly + 7), f(ax), f(ay), YEL))
    o.append(chip(lx, ly, label, w, t))

# output callouts (chips aligned to the right edge, leaders run to the props)
outs = [("Flame-retardant", P(118, 12, 40), 76), ("Safety cabins", P(124, 48, 30), 104), ("Grain storage", P(126, 82, 21), 132)]
for k, (label, a, row) in enumerate(outs):
    w = 5.25 * len(label) + 13
    left = 498 - w
    t = 1.5 + k * 0.18
    o.append('<g class="iso-tag iso-tag--minor" style="--t:%ss"><line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#fff" stroke-width="1" stroke-opacity=".9"/><circle cx="%s" cy="%s" r="2.2" fill="%s"/></g>' % (f(t), f(a[0]), f(a[1]), f(left), f(row), f(a[0]), f(a[1]), YEL))
    o.append(chip(left, row, label, w, t, anchor="start"))

# IN / OUT badges
bx, by = 190.0, 246.0
o.append('<g class="iso-tag" style="--t:.1s"><rect x="%s" y="%s" width="26" height="17" rx="8.5" fill="%s"/><text x="%s" y="%s" font-family="Poppins,Inter,sans-serif" font-weight="700" font-size="9.5" fill="%s" text-anchor="middle">IN</text>'
         '<text x="%s" y="%s" font-family="Poppins,Inter,sans-serif" font-weight="600" font-size="11" fill="#fff">Plant-based resources</text>'
         '<text class="iso-tag--minor" x="%s" y="%s" font-family="Inter,sans-serif" font-size="8.6" fill="#dbe7ff">fibre, husk, and trunk</text></g>'
         % (f(bx - 150), f(by + 12), YEL, f(bx - 137), f(by + 24), NAVY, f(bx - 117), f(by + 24.5), f(bx - 117), f(by + 36.5)))
bx, by = 350.0, 34.0
o.append('<g class="iso-tag" style="--t:1.2s"><rect x="%s" y="%s" width="32" height="17" rx="8.5" fill="%s"/><text x="%s" y="%s" font-family="Poppins,Inter,sans-serif" font-weight="700" font-size="9.5" fill="%s" text-anchor="middle">OUT</text>'
         '<text x="%s" y="%s" font-family="Poppins,Inter,sans-serif" font-weight="600" font-size="11" fill="#fff">Composite products</text>'
         '<text class="iso-tag--minor" x="%s" y="%s" font-family="Inter,sans-serif" font-size="8.6" fill="#dbe7ff">panels, cabins, and storage</text></g>'
         % (f(bx - 190), f(by - 14), YEL, f(bx - 174), f(by - 2), NAVY, f(bx - 152), f(by - 1.5), f(bx - 152), f(by + 10.5)))

o.append('</svg>')
sys.stdout.write("".join(o))
