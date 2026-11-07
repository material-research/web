#!/usr/bin/env python3
"""Isometric illustrations for the three Featured Research cards on Home (16:9, no background, two small English labels each).

Usage: python3 tools/gen_iso_featured.py     (writes _includes/illus/feat-bamboo-iso.html, feat-coffee-iso.html, feat-coconut-iso.html)
Scenes: bamboo = floating laminate + safety cabin + flame and shield; coffee = wet-processing tank + agitator + control box;
coconut = coconut skin peeler + ginger press. Same light palette and animation classes as the research-area scenes.
"""
import math, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import iso_lib as I
from iso_lib import P, f, pts, poly, box, hexagon, ell, lbox, blob, cylinder, label, face_x, face_y
from iso_lib import YEL, YEL_L, YEL_D, YEL_DD, DEEP, BLUE, TOPC, LEFTC, RIGHTC, INK_L, INK_R, INK_T, OUT, STEM, STEM_HI, NODE

VB = "-18 -16 292 164"   # extra margin on every side so nothing touches the frame
SC, CX0, CY0 = 0.82, 128.0, 70.0     # objects are scaled to fit the 16:9 frame; label targets use the same transform


def T(pt):
    return (CX0 + (pt[0] - CX0) * SC, CY0 + (pt[1] - CY0) * SC)


def wrap(body):
    return '<g transform="translate(%s,%s) scale(%s) translate(%s,%s)">%s</g>' % (f(CX0), f(CY0), SC, f(-CX0), f(-CY0), body)

ROOT = os.path.dirname(HERE)


def svg(body):
    return '<svg class="hv-iso iso-scene" viewBox="%s" role="img" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">%s</svg>' % (VB, body)


# ------------------------------------------------------------------ shared parts
def laminate(x0, y0, x1, y1, z0):
    """exploded laminate whose layers breathe apart (4 layers, base at z0)"""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    out = ""
    # bottom skin, core with hexagons, fibre weave, top skin
    out += '<g class="iso-lay iso-lay-0">%s</g>' % box(x0, y0, z0, x1, y1, z0 + 5, TOPC, LEFTC, RIGHTC, OUT)
    core = box(x0, y0, z0 + 11, x1, y1, z0 + 19, "#dbe7ff", LEFTC, RIGHTC, OUT)
    for k in range(3):
        for j in range(3):
            core += poly(hexagon(x0 + (k + .6) * (x1 - x0) / 3.3 + (3 if j % 2 else 0), y0 + (j + .6) * (y1 - y0) / 3.3, z0 + 19, 4.2), YEL, 'fill-opacity=".95" stroke="%s" stroke-width=".5"' % YEL_D)
    out += '<g class="iso-lay iso-lay-1">%s</g>' % core
    fib = box(x0, y0, z0 + 25, x1, y1, z0 + 29, "#fff3a6", YEL_D, YEL_DD)
    ls = []
    for yy in range(int(y0) + 4, int(y1), 6):
        a, b = P(x0 + 1, yy, z0 + 29), P(x1 - 1, yy, z0 + 29)
        ls.append("M%s %sL%s %s" % (f(a[0]), f(a[1]), f(b[0]), f(b[1])))
    fib += '<path d="%s" fill="none" stroke="%s" stroke-width="1.8" stroke-linecap="round"/>' % (" ".join(ls), YEL)
    out += '<g class="iso-lay iso-lay-2">%s</g>' % fib
    top = box(x0, y0, z0 + 35, x1, y1, z0 + 40, TOPC, LEFTC, RIGHTC, OUT)
    top += poly(hexagon(cx, cy, z0 + 40, 7), "none", 'stroke="%s" stroke-width="1.3"' % BLUE) + poly(hexagon(cx, cy, z0 + 40, 3.6), YEL, 'stroke="%s" stroke-width=".7"' % YEL_D)
    out += '<g class="iso-lay iso-lay-3">%s</g>' % top
    return out


def shield(x, y, z):
    p = P(x, y, z)
    return ('<g transform="translate(%s,%s)"><g class="iso-badge"><circle class="iso-ring" r="17" fill="none" stroke="%s" stroke-width="1.6"/>'
            '<path d="M0 -11 L9.5 -7 V1 C9.5 7 5 10 0 12.5 C-5 10 -9.5 7 -9.5 1 V-7 Z" fill="%s" stroke="%s" stroke-width="1.8" stroke-linejoin="round"/>'
            '<path d="M-4.5 0 L-1.2 3.4 L5 -4.2" fill="none" stroke="%s" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></g></g>' % (f(p[0]), f(p[1]), YEL_D, YEL, YEL_D, DEEP))


def flame(x, y, z=0):
    p = P(x, y, z)
    return ('<g transform="translate(%s,%s)"><g class="iso-flame"><path d="M0 0 C-9 -3 -11 -12 -6 -20 C-5 -15 -2 -14 -1 -24 C5 -18 10 -9 6 -2 C4 0 2 0 0 0 Z" fill="%s"/>'
            '<path d="M0 -1 C-5 -3 -6 -9 -3 -13 C-1 -9 1 -9 2 -14 C5 -9 6 -4 3 -1 Z" fill="#fff"/></g></g>' % (f(p[0]), f(p[1]), YEL))


def tank(x0, x1, y0, y1, h):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    out = lbox(x0, y0, 0, x1, y1, h)
    water = [P(x0 + 4, y0 + 4, h + .1), P(x1 - 4, y0 + 4, h + .1), P(x1 - 4, y1 - 4, h + .1), P(x0 + 4, y1 - 4, h + .1)]
    out += poly(water, "#6b92dc") + poly(water, "none", 'stroke="#ffffff" stroke-opacity=".6" stroke-width=".9"')
    c0 = P(cx, cy, h + .5)
    rr = min(x1 - x0, y1 - y0) / 2 - 6
    out += '<g transform="translate(%s,%s) scale(1,.5)"><g class="iso-orbit iso-orbit-fast">%s</g></g>' % (f(c0[0]), f(c0[1]), "".join('<circle cx="%s" cy="%s" r="3.4" fill="%s" stroke="%s" stroke-width=".7"/>' % (f(rr * math.cos(a)), f(rr * math.sin(a)), YEL, YEL_D) for a in [i * math.pi / 3 for i in range(6)]))
    out += '<g transform="translate(%s,%s) scale(1,.5)"><g class="iso-orbit iso-orbit-slow2">%s</g></g>' % (f(c0[0]), f(c0[1]), "".join('<circle cx="%s" cy="%s" r="2.4" fill="#ffffff"/>' % (f(rr * .55 * math.cos(a)), f(rr * .55 * math.sin(a))) for a in [i * math.pi / 2 + .4 for i in range(4)]))
    out += lbox(cx - 1.3, cy - 1.3, h, cx + 1.3, cy + 1.3, h + 26, "ink") + lbox(cx - 5, cy - 5, h + 26, cx + 5, cy + 5, h + 34, "ink")
    b0 = P(cx, cy, h + 21)
    out += '<g transform="translate(%s,%s) scale(1,.5)"><g class="iso-spin"><rect x="-13" y="-1.6" width="26" height="3.2" rx="1.6" fill="%s"/></g></g>' % (f(b0[0]), f(b0[1]), INK_T)
    return out


def peeler(x0, x1, y0, y1):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    out = lbox(x0, y0, 0, x1, y1, 20) + lbox(x0 + 5, y0 + 4, 20, x1 - 5, y1 - 4, 32, "ink")
    wh = P(cx, y1, 10)
    out += '<g transform="translate(%s,%s)"><g transform="matrix(%s,.5,0,1,0,0)"><circle r="7.6" fill="%s" stroke="%s" stroke-width="1.2"/><g class="iso-spin">%s<circle r="1.8" fill="%s"/></g></g></g>' % (
        f(wh[0]), f(wh[1]), f(I.K), TOPC, INK_L, "".join('<line x1="0" y1="0" x2="%s" y2="%s" stroke="%s" stroke-width="1.6" stroke-linecap="round"/>' % (f(6.2 * math.cos(a)), f(6.2 * math.sin(a)), YEL_D) for a in [i * math.pi / 3 for i in range(6)]), INK_L)
    cc = P(cx, cy, 41)
    out += '<g transform="translate(%s,%s)"><g class="iso-bob"><circle r="7.4" fill="#dbe7ff" stroke="#0b3d91" stroke-opacity=".25" stroke-width=".8"/><ellipse cx="-2.4" cy="-2.6" rx="2.2" ry="1.3" fill="#fff" fill-opacity=".9"/><circle cx="-1.6" cy="1.2" r=".9" fill="%s"/><circle cx="1.8" cy="1.8" r=".9" fill="%s"/><circle cx="1.6" cy="-.8" r=".9" fill="%s"/></g></g>' % (f(cc[0]), f(cc[1]), INK_R, INK_R, INK_R)
    hp = P(x1, cy, 24)
    for i, (dx, dy, d) in enumerate(((3, 0, 0), (9, 6, .5), (5, 10, 1.0))):
        out += '<ellipse class="iso-husk" cx="%s" cy="%s" rx="4" ry="1.6" fill="%s" transform="rotate(%s %s %s)" style="animation-delay:%ss"/>' % (f(hp[0] + dx), f(hp[1] + dy), YEL, -25 + i * 22, f(hp[0] + dx), f(hp[1] + dy), f(d))
    return out, cc


def press(cx, cy):
    out = lbox(cx - 24, cy - 24, 0, cx + 24, cy + 24, 8)
    out += lbox(cx - 4, cy - 24, 8, cx + 4, cy - 18, 62, "ink") + lbox(cx - 4, cy + 18, 8, cx + 4, cy + 24, 62, "ink")
    out += box(cx - 8, cy - 8, 8, cx + 8, cy + 8, 15, "#fff3a6", YEL_D, YEL_DD)
    rod = lbox(cx - 2, cy - 2, 42, cx + 2, cy + 2, 62, "ink")
    plat = lbox(cx - 10, cy - 12, 28, cx + 10, cy + 12, 38, "light")
    out += '<g class="iso-rod iso-rod-s">%s</g><g class="iso-platen">%s</g>' % (rod, plat)
    out += lbox(cx - 8, cy - 26, 62, cx + 8, cy + 26, 70, "ink")
    out += cylinder(cx - 2, cy + 38, 7, 0, 10, LEFTC, RIGHTC, "#dbe7ff") + poly(ell(cx - 2, cy + 38, 8, 5.2, 5.2, 18), "#6b92dc")
    dp = P(cx + 10, cy + 18, 20)
    for i, d in enumerate((0, .6)):
        out += '<path class="iso-fall iso-fall-s" d="M%s %s c-2 3 -2.5 5 0 6.2 c2.5 -1.2 2 -3.2 0 -6.2z" fill="#6b92dc" style="animation-delay:%ss"/>' % (f(dp[0] - 6 + i * 6), f(dp[1] + i * 2), f(d))
    return out


# ------------------------------------------------------------------ scene 1: bamboo composite safety cabin
I.OX, I.OY = 118.0, 52.0
b = blob(50, 62, 36, 28) + blob(112, 60, 26, 22)
b += laminate(24, 38, 84, 90, 34)
# safety cabin with door and window, flame at its foot and a shield above
cx0, cx1, cy0, cy1 = 98, 128, 52, 76
b += lbox(cx0, cy0, 0, cx1, cy1, 28)
b += box(cx0 - 2, cy0 - 2, 28, cx1 + 2, cy1 + 2, 32, YEL_L, YEL_D, YEL_DD)
b += poly([P(104, cy1, 0), P(116, cy1, 0), P(116, cy1, 20), P(104, cy1, 20)], BLUE)
b += poly([P(cx1, 58, 12), P(cx1, 70, 12), P(cx1, 70, 22), P(cx1, 58, 22)], BLUE)
b += flame(112, 84, 0) + shield(120, 66, 56)
lam = T(P(54, 64, 74))
sh = T(P(120, 66, 56))
b = wrap(b) + label(74, 18, "Bamboo fibre laminate", lam[0], lam[1] - 1, .3, fs=8.6) + label(206, 18, "Flame-retardant", sh[0], sh[1] - 14, .5, fs=8.6)
open(os.path.join(ROOT, "_includes/illus/feat-bamboo-iso.html"), "w").write(svg(b))

# ------------------------------------------------------------------ scene 2: wet coffee processing
I.OX, I.OY = 124.0, 42.0
b = blob(62, 62, 52, 40) + blob(128, 70, 14, 14)
b += tank(24, 100, 34, 92, 30)
# control box (automation) with a blinking lamp and a pipe from the tank
b += lbox(112, 56, 0, 128, 72, 20, "ink") + lbox(114, 58, 20, 126, 70, 26, "light")
lp = P(120, 72, 12)
b += '<circle class="iso-lamp" cx="%s" cy="%s" r="2.2" fill="%s"/>' % (f(lp[0]), f(lp[1]), YEL)
b += lbox(100, 60, 14, 112, 66, 20, "light")
c1 = T(P(24, 70, 28))
a1 = T(P(120, 64, 26))
b = wrap(b) + label(c1[0] - 4, 18, "Cherry grading", c1[0], c1[1], .3, fs=8.6) + label(a1[0] + 56, a1[1] + 14, "Automation", a1[0] + 2, a1[1] + 1, .5, side="left", fs=8.6)
open(os.path.join(ROOT, "_includes/illus/feat-coffee-iso.html"), "w").write(svg(b))

# ------------------------------------------------------------------ scene 3: coconut and ginger machines
I.OX, I.OY = 112.0, 38.0
b = blob(36, 70, 30, 24) + blob(104, 44, 34, 32)
pe, cc = peeler(10, 56, 52, 90)
b += pe
b += press(104, 46)
ccT = T(cc)
g1 = T(P(104, 46, 70))
b = wrap(b) + label(ccT[0], 18, "Coconut skin peeler", ccT[0], ccT[1] - 6, .3, fs=8.6) + label(g1[0] + 38, 18, "Ginger press", g1[0], g1[1] - 2, .5, fs=8.6)
open(os.path.join(ROOT, "_includes/illus/feat-coconut-iso.html"), "w").write(svg(b))
print("ok")
