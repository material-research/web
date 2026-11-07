"""Small helpers for the isometric illustrations (shared by tools/gen_iso_*.py).

World coordinates: x runs down-right, y runs down-left, z is up. Set iso_lib.OX / iso_lib.OY to move the origin on screen.
"""
import math

K = 0.8660254          # cos 30
OX, OY = 250.0, 60.0

# palette (blue + yellow only; white as the light colour)
WHITE, PALE, SOFT, MID, BLUE, DEEP, DARK, NAVY = "#ffffff", "#dbe7ff", "#8fb0f0", "#5f86d6", "#2a56b8", "#0b3d91", "#082d6e", "#061f52"
YEL, YEL_L, YEL_D, YEL_DD = "#ffd60a", "#ffe45c", "#d9b000", "#b58f00"
FACE_L, FACE_R = "#e3ebfb", "#c3d4f4"
FLOOR, FLOOR_L, FLOOR_R = "#4a7ce0", "#1a4bb0", "#0e3a8c"


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


def hull(points):
    pts_ = sorted(set((round(a, 2), round(b, 2)) for a, b in points))

    def cross(o_, a_, b_):
        return (a_[0] - o_[0]) * (b_[1] - o_[1]) - (a_[1] - o_[1]) * (b_[0] - o_[0])
    lo = []
    for p in pts_:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts_):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def platform(W, D, T=12, hex_r=11.0):
    """floor slab with a honeycomb pattern; returns SVG string"""
    o = []
    top = [P(0, 0), P(W, 0), P(W, D), P(0, D)]
    o.append(poly([P(0, D, 0), P(W, D, 0), P(W, D, -T), P(0, D, -T)], FLOOR_L))
    o.append(poly([P(W, 0, 0), P(W, D, 0), P(W, D, -T), P(W, 0, -T)], FLOOR_R))
    o.append(poly(top, FLOOR))
    R = hex_r
    hexes, row, y = [], 0, R
    while y < D - R + 0.1:
        x = R + (1.5 * R if row % 2 else 0)
        while x < W - R + 0.1:
            hexes.append((x, y))
            x += 3 * R
        y += math.sqrt(3) * R / 2
        row += 1
    d = []
    for hx, hy in hexes:
        h = hexagon(hx, hy, 0, R - 0.6)
        d.append("M" + " L".join(f(a) + " " + f(b) for a, b in h) + "Z")
    o.append('<path d="%s" fill="none" stroke="#dbe7ff" stroke-opacity=".5" stroke-width=".9" stroke-linejoin="round"/>' % " ".join(d))
    o.append('<polygon points="%s" fill="none" stroke="#dbe7ff" stroke-opacity=".85" stroke-width="1.4" stroke-linejoin="round"/>' % pts(top))
    return "".join(o)


def shadow(x0, y0, x1, y1, dx=6, dy=6, op=.3):
    return poly([P(x0 + dx, y0 + dy), P(x1 + dx, y0 + dy), P(x1 + dx, y1 + dy), P(x0 + dx, y1 + dy)], DARK, 'fill-opacity="%s"' % op)


def bamboo(x, y, h, delay, extra_leaves=True, main=None, hi=None, node=None, leaves=None):
    """a bamboo culm standing at world (x, y); sways from its base"""
    main, hi, node = main or PALE, hi or SOFT, node or BLUE
    leaves = leaves or ((YEL, YEL, YEL_L, PALE))
    bx, by = P(x, y, 0)
    s = ['<g transform="translate(%s,%s)"><g class="iso-sway" style="animation-delay:%ss">' % (f(bx), f(by), f(delay))]
    s.append('<rect x="-3.2" y="%s" width="6.4" height="%s" rx="2.6" fill="%s"/>' % (f(-h), f(h), main))
    s.append('<rect x="0.4" y="%s" width="2.8" height="%s" rx="1.4" fill="%s"/>' % (f(-h + 2), f(h - 3), hi))
    n = int(h // 26)
    for k in range(1, n + 1):
        s.append('<ellipse cx="0" cy="%s" rx="4" ry="1.7" fill="%s"/>' % (f(-k * (h / (n + 1))), node))
    if extra_leaves:
        for (dx, dy, rot, c) in ((12, 8, -32, leaves[0]), (-12, 20, 28, leaves[1]), (11, 34, -24, leaves[2]), (-11, 46, 30, leaves[3])):
            s.append('<ellipse cx="%s" cy="%s" rx="12" ry="3.8" fill="%s" transform="rotate(%s %s %s)"/>' % (f(dx), f(-h + dy), c, rot, f(dx), f(-h + dy)))
    s.append('</g></g>')
    return "".join(s)


# ---------------------------------------------------------------- light-page palette and shared parts (used by gen_iso_agro / cnc / energy)
TOPC, LEFTC, RIGHTC = "#f4f8ff", "#a9c3f2", "#6b92dc"
STEM, STEM_HI, NODE = "#7fa3ea", "#a9c3f2", "#0b3d91"
INK_L, INK_R, INK_T = "#2a56b8", "#0b3d91", "#8fb0f0"
OUT = 'stroke="#0b3d91" stroke-opacity=".18" stroke-width=".8" stroke-linejoin="round"'


def lbox(x0, y0, z0, x1, y1, z1, kind="light", extra=OUT):
    """box in the light palette: kind light (white/blue) or ink (dark blue) or yellow"""
    if kind == "ink":
        return box(x0, y0, z0, x1, y1, z1, INK_T, INK_L, INK_R)
    if kind == "yellow":
        return box(x0, y0, z0, x1, y1, z1, YEL_L, YEL_D, YEL_DD)
    return box(x0, y0, z0, x1, y1, z1, TOPC, LEFTC, RIGHTC, extra)


def blob(cx, cy, rx, ry):
    """soft two-layer ground shadow"""
    return (poly(ell(cx, cy, 0, rx + 5, ry + 5, 24), DEEP, 'fill-opacity=".05"') + poly(ell(cx, cy, 0, rx, ry, 24), DEEP, 'fill-opacity=".10"'))


def cylinder(cx, cy, r, z0, z1, body=LEFTC, shade=RIGHTC, top=TOPC):
    """vertical cylinder"""
    rb, rt = ell(cx, cy, z0, r, r, 26), ell(cx, cy, z1, r, r, 26)
    angs = [math.radians(a) for a in range(-80, 81, 10)]
    half_b = [P(cx + r * math.cos(t), cy + r * math.sin(t), z0) for t in angs]
    half_t = [P(cx + r * math.cos(t), cy + r * math.sin(t), z1) for t in angs]
    return (poly(hull(rb + rt), body, OUT) + poly(half_t + list(reversed(half_b)), shade, 'fill-opacity=".9"') + poly(rt, top, OUT))


def label(cx, cy, text, tx, ty, delay, side=None, fs=7.1):
    """small navy chip centred at (cx, cy) with a leader line to the target (tx, ty); English only, hidden on phones.
    side=None draws the leader straight down or up from the chip at x = tx; side="left"/"right" starts it at the chip's edge."""
    k = fs / 7.1
    w = (4.3 * len(text) + 12) * k
    h = 12 * k
    if side == "left":
        x1, y1 = cx - w / 2, cy
    elif side == "right":
        x1, y1 = cx + w / 2, cy
    else:
        x1, y1 = tx, cy + (h / 2 if ty > cy else -h / 2)
    return ('<g class="iso-tag" style="--t:%ss"><line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#0b3d91" stroke-width="1" stroke-opacity=".7"/><circle cx="%s" cy="%s" r="2.2" fill="%s"/>'
            '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="#0b3d91"/>'
            '<text x="%s" y="%s" font-family="Inter,sans-serif" font-weight="600" font-size="%s" fill="#fff" text-anchor="middle">%s</text></g>'
            % (f(delay), f(x1), f(y1), f(tx), f(ty), f(tx), f(ty), YEL, f(cx - w / 2), f(cy - h / 2), f(w), f(h), f(h / 2), f(cx), f(cy + 0.35 * fs), fs, text))


def svg_open(vb="108 -8 322 226"):
    return '<svg class="hv-iso iso-scene" viewBox="%s" role="img" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">' % vb


def face_x(x, y, z):
    """matrix string for a flat drawing on a face with constant x (local u runs up-right along -y, v runs down)"""
    px, py = P(x, y, z)
    return "matrix(%s,%s,0,1,%s,%s)" % (f(K), f(-0.5), f(px), f(py))


def face_y(x, y, z):
    """matrix string for a flat drawing on a face with constant y (local u runs down-right along +x, v runs down)"""
    px, py = P(x, y, z)
    return "matrix(%s,%s,0,1,%s,%s)" % (f(K), f(0.5), f(px), f(py))
