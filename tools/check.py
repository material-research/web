#!/usr/bin/env python3
"""Data and content checker for the Agromaterials Research Group site.

Run from the repo root before every push:

    python3 tools/check.py            # data, translations, images, style
    python3 tools/check.py --build    # also builds the site and checks links and numbers

Exit code 1 means at least one ERROR (do not push). WARN items are advice.
Needs PyYAML. --build needs Jekyll (see CLAUDE.md "Preview and test").
"""
import os, re, sys, glob, json, tempfile, subprocess, html
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required (pip install pyyaml)")

ROOT = Path(__file__).resolve().parent.parent
errors, warns = [], []
def err(msg): errors.append(msg)
def warn(msg): warns.append(msg)

def load(name):
    p = ROOT / "_data" / name
    if not p.exists():
        err(f"{name} is missing"); return None
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception as e:
        err(f"{name} is not valid YAML: {e}"); return None

def blank(v): return v is None or (isinstance(v, str) and not v.strip())

def need(obj, keys, where):
    for k in keys:
        if blank(obj.get(k)): err(f"{where}: missing '{k}'")

def twin(obj, key, where, optional=False):
    """a field and its Indonesian twin must both be present (or both absent when optional)"""
    a, b = obj.get(key), obj.get(key + "_id")
    if blank(a) and blank(b):
        if not optional: err(f"{where}: '{key}' and '{key}_id' are both empty")
    elif blank(a): err(f"{where}: '{key}' (English) is empty but '{key}_id' is set")
    elif blank(b): err(f"{where}: '{key}_id' (Indonesian) is missing")

def same_len(obj, key, where):
    a, b = obj.get(key) or [], obj.get(key + "_id") or []
    if len(a) != len(b):
        err(f"{where}: '{key}' has {len(a)} items but '{key}_id' has {len(b)}")

COLON = re.compile(r"(?<![\d/])(?<!https)(?<!http)(?<!mailto):\s")
def no_colon(text, where):
    if isinstance(text, str):
        plain = re.sub(r"<[^>]+>", "", text)
        plain = re.sub(r"https?://\S+", "", plain)
        if COLON.search(plain):
            warn(f"{where}: contains a colon (owner prefers no ':' in site prose) -> {plain.strip()[:70]}")

# ---------------------------------------------------------------- publications
themes = load("pub_themes.yml") or []
theme_ids = {t.get("id") for t in themes}
for t in themes:
    w = f"pub_themes #{t.get('id')}"
    for k in ("name", "short", "desc"): twin(t, k, w)
pubs = load("publications.yml") or []
seen = set()
for i, p in enumerate(pubs, 1):
    w = f"publications #{i} ({str(p.get('title',''))[:40]}...)"
    need(p, ["title", "authors", "venue", "year", "theme"], w)
    if p.get("theme") not in theme_ids: err(f"{w}: theme {p.get('theme')!r} is not in pub_themes.yml")
    y = p.get("year")
    if not isinstance(y, int) or not (1990 <= y <= 2100): err(f"{w}: year {y!r} looks wrong")
    u = p.get("url") or ""
    if u and not u.startswith("https://doi.org/"): warn(f"{w}: url is not a https://doi.org/ link")
    if not u: warn(f"{w}: no DOI/url yet")
    key = re.sub(r"\W+", "", str(p.get("title", "")).lower())
    if key in seen: err(f"{w}: duplicate title")
    seen.add(key)

# ---------------------------------------------------------------- grants
grants = load("grants.yml") or []
counted = []
for i, g in enumerate(grants, 1):
    w = f"grants #{i} ({str(g.get('title',''))[:40]}...)"
    need(g, ["title", "funder", "scheme", "year_start", "year_end", "status", "amount"], w)
    for k in ("title", "funder", "scheme"): twin(g, k, w)
    st = g.get("status")
    if st not in ("active", "completed", "submitted"): err(f"{w}: status must be active or completed (got {st!r})")
    if st == "submitted": warn(f"{w}: status 'submitted' is not shown on the site")
    if st in ("active", "completed"):
        if not isinstance(g.get("amount_value"), int): err(f"{w}: amount_value (plain integer, IDR) is missing, so it is left out of the total")
        elif (g.get("currency") in (None, "IDR")): counted.append(g)
    if isinstance(g.get("year_start"), int) and isinstance(g.get("year_end"), int) and g["year_end"] < g["year_start"]:
        err(f"{w}: year_end is before year_start")
    if not blank(g.get("desc")): twin(g, "desc", w)

# ---------------------------------------------------------------- research
research = load("research.yml") or []
anchors = set()
for i, r in enumerate(research, 1):
    w = f"research #{i} ({r.get('name')})"
    need(r, ["icon", "illus", "anchor"], w)
    twin(r, "name", w); twin(r, "desc", w); twin(r, "short", w)
    if r.get("anchor") in anchors: err(f"{w}: duplicate anchor")
    anchors.add(r.get("anchor"))
    if r.get("illus") and not (ROOT / "_includes" / "illus" / f"{r['illus']}.html").exists():
        err(f"{w}: illustration _includes/illus/{r['illus']}.html does not exist")
    if r.get("iso") and not (ROOT / "_includes" / "illus" / f"{r['illus']}-iso.html").exists():
        err(f"{w}: iso is set but _includes/illus/{r['illus']}-iso.html does not exist")
    for k in ("topics", "apps"):
        if r.get(k): same_len(r, k, w)
    twin(r, "next", w, optional=True)
    for m in r.get("materials") or []:
        if blank(m.get("en")) or blank(m.get("id")): err(f"{w}: a material is missing en or id")
    for k in ("desc", "next"): no_colon(r.get(k), f"{w} {k}")
    for k in ("topics", "apps"):
        for x in r.get(k) or []: no_colon(x, f"{w} {k}")

# ---------------------------------------------------------------- flow map (Home "From plant to product")
flow = load("flow.yml") or []
if len(flow) != 5: err(f"flow.yml must have 5 steps (the map is built for 5), found {len(flow)}")
for i, st in enumerate(flow, 1):
    for f in ("id", "icon", "short", "short_id", "title", "title_id", "text", "text_id"):
        if not st.get(f): err(f"flow step {i}: missing {f}")
    if len(st.get("chips") or []) != len(st.get("chips_id") or []): err(f"flow step {i}: chips and chips_id differ in length")

# ---------------------------------------------------------------- projects
for i, p in enumerate(load("projects.yml") or [], 1):
    w = f"projects #{i} ({p.get('id')})"
    twin(p, "title", w); twin(p, "desc", w)
    same_len(p, "thrusts", w)
    if p.get("illus") and not (ROOT / "_includes" / "illus" / f"{p['illus']}.html").exists():
        err(f"{w}: illustration {p['illus']}.html does not exist")
    if p.get("iso") and not (ROOT / "_includes" / "illus" / f"feat-{p['illus']}-iso.html").exists():
        err(f"{w}: iso is set but _includes/illus/feat-{p['illus']}-iso.html does not exist")
    no_colon(p.get("desc"), f"{w} desc")

# ---------------------------------------------------------------- team
team = load("team.yml") or {}
people = [("director", team.get("director") or {})] + [(f"member {m.get('name')}", m) for m in team.get("members") or []]
for label, m in people:
    w = f"team {label}"
    need(m, ["name"], w); twin(m, "role", w)
    if label != "director": twin(m, "focus", w, optional=True)
    if label == "director": twin(m, "bio", w); twin(m, "label", w); no_colon(m.get("bio"), f"{w} bio")
    ph = m.get("photo")
    if ph and not (ROOT / "assets" / "img" / ph).exists(): err(f"{w}: photo assets/img/{ph} does not exist")
    if not ph: warn(f"{w}: no photo (initials are shown)")

# ---------------------------------------------------------------- news
for i, n in enumerate(load("news.yml") or [], 1):
    w = f"news #{i}"
    need(n, ["date", "html"], w); twin(n, "html", w)
    for k in ("html", "html_id"):
        for href in re.findall(r'href="([^"]*)"', n.get(k) or ""):
            if href.startswith("/") and not href.startswith("//"): err(f"{w}: link {href} must start with @BASE@, not '/'")
        no_colon(n.get(k), f"{w} {k}")
    if n.get("url"):
        if "<a " in (n.get("html") or "") + (n.get("html_id") or ""): err(f"{w}: has a url, so the text must not contain <a> links")
        u = str(n["url"])
        if not (u.startswith("https://") or u.startswith("/")): err(f"{w}: url must start with / or https://")
    if n.get("image"):
        ip = ROOT / "assets" / "img" / str(n["image"])
        if not ip.exists(): err(f"{w}: image {n['image']} not found")
        elif ip.stat().st_size / 1024 > 60: err(f"{w}: image is {ip.stat().st_size/1024:.0f} KB (max about 60 KB)")

# ---------------------------------------------------------------- i18n
i18n = load("i18n.yml") or {}
for k, v in i18n.items():
    if isinstance(v, dict) and "en" in v and "id" in v:
        if blank(v["en"]) and k not in ("post_lang_note",): warn(f"i18n '{k}': English is empty")
        if blank(v["id"]) and not blank(v["en"]): err(f"i18n '{k}': Indonesian is empty")
    elif isinstance(v, dict): err(f"i18n '{k}': needs both 'en' and 'id'")
for k in [k for k in i18n if k.startswith(("about_who", "hero_", "study_", "projects_lede", "news_lede"))]:
    for lang in ("en", "id"): no_colon((i18n[k] or {}).get(lang), f"i18n {k}.{lang}")

# ---------------------------------------------------------------- posts
for f in sorted(glob.glob(str(ROOT / "_posts" / "*.md"))):
    name = os.path.basename(f); text = Path(f).read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m: err(f"{name}: no front matter"); continue
    fm, body = yaml.safe_load(m.group(1)) or {}, m.group(2)
    w = f"post {name}"
    need(fm, ["title", "title_id", "summary", "summary_id"], w)
    if not fm.get("tags"): warn(f"{w}: no tags")
    elif len(fm.get("tags") or []) != len(fm.get("tags_id") or []): err(f"{w}: tags and tags_id differ in length")
    if 'data-lang="en"' not in body or 'data-lang="id"' not in body: err(f"{w}: body needs both an EN and an ID block")
    if re.search(r"<div data-lang=\"(en|id)\">", body): err(f"{w}: data-lang div needs markdown=\"1\"")
    if body.count('data-lang="en"') != body.count('data-lang="id"'):
        err(f"{w}: different number of EN and ID blocks")
    if fm.get("cover") not in (None, "logo"): err(f"{w}: cover must be 'logo' or omitted")
    for k in ("thumbnail", "thumbnail_card"):
        if fm.get(k) and not (ROOT / "assets" / "img" / fm[k]).exists(): err(f"{w}: {k} file is missing")
    if fm.get("thumbnail") and not fm.get("thumbnail_card"): warn(f"{w}: thumbnail_card missing (list card will load the big photo)")
    for k in ("summary", "summary_id", "title", "title_id"): no_colon(fm.get(k), f"{w} {k}")
    prose = re.sub(r"<[^>]+>|^#+ .*$|\{\{.*?\}\}", "", body, flags=re.M)
    prose = re.sub(r"https?://\S+", "", prose)
    for line in prose.splitlines():
        if COLON.search(line): warn(f"{w}: colon in text -> {line.strip()[:70]}"); break

# ---------------------------------------------------------------- images
LIMITS = [("assets/img/blog/", 130, "blog image (hero ~110 KB, card ~45 KB)"), ("assets/img/team/", 50, "team photo"), ("assets/img/", 100, "image")]
KEEP = {"og-logo.jpg", "og-card.jpg", "favicon.png", "logo-small.png"}
for f in sorted(glob.glob(str(ROOT / "assets" / "img" / "**" / "*"), recursive=True)):
    if not os.path.isfile(f): continue
    rel = os.path.relpath(f, ROOT).replace(os.sep, "/"); kb = os.path.getsize(f) / 1024
    if rel.endswith(".svg"): continue
    for prefix, limit, what in LIMITS:
        if rel.startswith(prefix):
            if kb > limit: err(f"{rel}: {kb:.0f} KB is over the {limit} KB limit for a {what}")
            break
    if not rel.endswith(".webp") and os.path.basename(rel) not in KEEP:
        warn(f"{rel}: not WebP (use WebP for photos and logos)")
    if "/blog/" in rel and "-card" in rel and kb > 60: err(f"{rel}: card image is {kb:.0f} KB (max about 60 KB)")

# ---------------------------------------------------------------- contact form
_cfg = yaml.safe_load((ROOT / "_config.yml").read_text(encoding="utf-8")) or {}
_key = (_cfg.get("lab") or {}).get("contact_form_key", "") or ""
if not _key: warn("contact form is OFF (lab.contact_form_key is empty in _config.yml); the Contact page shows the email address only")
elif not re.fullmatch(r"[0-9a-fA-F-]{20,}", str(_key)): err("lab.contact_form_key does not look like a Web3Forms access key")

# ---------------------------------------------------------------- licence notice
if not (ROOT / "LICENSE").exists(): err("LICENSE file is missing (all rights reserved notice)")
elif "All rights reserved" not in (ROOT / "LICENSE").read_text(encoding="utf-8"): err("LICENSE no longer states 'All rights reserved'")
if "All rights reserved" not in (ROOT / "README.md").read_text(encoding="utf-8"): warn("README.md has no copyright notice")

# ---------------------------------------------------------------- placeholders
for pat in ("[Example]", "Your Name", "TODO", "example.ac.id", "Lorem"):
    for f in list((ROOT / "_data").glob("*.yml")) + list((ROOT / "_posts").glob("*.md")) + [ROOT / "_config.yml"]:
        if f.exists() and pat in f.read_text(encoding="utf-8"):
            (warn if pat == "TODO" else err)(f"{f.relative_to(ROOT)}: contains placeholder text {pat!r}")

# ---------------------------------------------------------------- optional: build and check the output
if "--build" in sys.argv:
    out = tempfile.mkdtemp(prefix="sitecheck_")
    env = dict(os.environ, JEKYLL_NO_BUNDLER_REQUIRE="1")
    jk = subprocess.run("jekyll build --baseurl '' -d " + out, shell=True, cwd=ROOT, env=env, capture_output=True, text=True)
    if jk.returncode != 0:
        # fall back to the gem executable path used in cloud sessions
        exe = glob.glob("/opt/rbenv/versions/*/lib/ruby/gems/*/gems/jekyll-3*/exe/jekyll")
        if exe:
            jk = subprocess.run(["ruby", exe[0], "build", "--baseurl", "", "-d", out], cwd=ROOT, env=env, capture_output=True, text=True)
    if jk.returncode != 0:
        err("jekyll build failed: " + (jk.stderr or jk.stdout)[-300:])
    else:
        site = Path(out)
        broken = set()
        for page in site.rglob("*.html"):
            t = page.read_text(encoding="utf-8")
            for attr in re.findall(r'(?:href|src)="([^"#?]+)', t):
                if attr.startswith(("http", "mailto:", "//", "data:", "tel:")) or not attr.startswith("/"): continue
                target = site / attr.lstrip("/")
                if not (target.exists() or (target / "index.html").exists()):
                    broken.add(f"{page.relative_to(site)} -> {attr}")
        for b in sorted(broken)[:15]: err(f"broken internal link {b}")
        # numbers shown on the site must match the data
        home = (site / "index.html").read_text(encoding="utf-8")
        m = re.search(r'class="hero-stats">(.*?)</ul>', home, re.S)
        if m:
            nums = [int(x) for x in re.findall(r"<b>(\d+)</b>", m.group(1))]
            expect = [len(pubs), len([g for g in grants if g.get("status") != "submitted"])]
            if nums != expect: err(f"hero stats {nums} do not match the data {expect}")
        hm = re.search(r'id="hsUsd" data-total="(\d+)"', home)
        if not hm: err("Home funding figure (#hsUsd) is missing")
        else:
            htot = int(hm.group(1)); etot = sum(g["amount_value"] for g in counted)
            if htot != etot: err(f"Home funding total ({htot}) differs from the data ({etot})")
        gp = (site / "grants" / "index.html").read_text(encoding="utf-8")
        tm = re.search(r'id="gtIdr">Rp ([\d.]+)', gp)
        if tm:
            shown = int(tm.group(1).replace(".", "")); expect = sum(g["amount_value"] for g in counted)
            if shown != expect: err(f"grants total on the page ({shown}) differs from the data ({expect})")
        print(f"build ok: {sum(1 for _ in site.rglob('*.html'))} pages checked")

# ---------------------------------------------------------------- report
print(f"\nPublications {len(pubs)} | Grants {len(grants)} (counted in total {len(counted)}) | Research areas {len(research)} | Members {len(team.get('members') or [])} | Posts {len(glob.glob(str(ROOT / '_posts' / '*.md')))}")
for w in warns: print("WARN  ", w)
for e in errors: print("ERROR ", e)
print(f"\n{len(errors)} error(s), {len(warns)} warning(s)")
sys.exit(1 if errors else 0)
