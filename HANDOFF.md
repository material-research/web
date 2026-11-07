# HANDOFF — read this first in a new session

Last updated: 2026-11-05 (end of the first long session, after the first monthly review). Read `CLAUDE.md` (rules and file map) and this file, then `git log --oneline -10`, before changing anything. To start a session the owner can say: "Lanjutkan website ARG, baca HANDOFF.md dulu" or "Tinjauan bulanan situs ARG".

## 1. Where things stand

- **Site:** Agromaterials Research Group, Politeknik ATI Makassar. Jekyll on GitHub Pages, bilingual EN | ID (English is the default for everyone).
- **Repo / branch:** `material-research/web`. Pages publishes **`main`** (root). The owner gave standing permission to **push directly to `main`** (CLAUDE.md rule 8), so every push goes live in 1-3 minutes. No pull requests. `main` is also the GitHub default branch (set by the owner 2026-11-05). The old branch `claude/keen-feynman-58w2jt` was deleted by the owner (only `main` exists). Two pushes close together cancel the first build (harmless).
- **Live URL:** https://material-research.github.io/web/ (`url: https://material-research.github.io`, `baseurl: /web`). The custom domain is NOT connected yet (section 5).
- **Owner:** Dr. Massriyady Massaguni, S.ST., M.T. (Research Director). Chats in Indonesian. **Uses iPhone Safari and often opens links inside WhatsApp's in-app browser** (aggressive cache).
- **Menu:** Home, About Us, Research, Team, Publications, Grants, Blog, Contact (+ EN|ID). Resources, Calendar, Apply exist but are hidden.
- **Before every push:** `python3 tools/check.py --build` (0 errors required). Current warnings are only the 17 publications without a DOI.

### Content status

| Area | Status |
|---|---|
| Identity (`_config.yml`) | Real. Name "Agromaterials Research Group" (no "ATIM" prefix anywhere in text), Politeknik ATI Makassar, public email **agromaterialsrg@atim.ac.id** (Contact page, footer, and the contact form; the director's own address massriyady.massaguni@atim.ac.id appears only on her Team profile, by the owner's decision 2026-11-05), campus site https://atim.ac.id, Makassar. |
| Home (`index.html`) | Split hero (isometric 3D animated illustration, section 5d): eyebrow = institution, headline "Composite materials from plant-based resources" (ID "Material komposit dari sumber daya nabati", keyword in yellow), short tagline, yellow primary button, **static** stats strip (publications, awarded grants, research areas, computed from data), animated panel-making illustration. Then "What We Study" (4 areas with illustrations), Featured Research (3 animated cards), Recent News. The owner likes Home; change it only on request. |
| Research page | Jump menu + four detail cards (same illustration and description as Home, plus key topics, materials/commodities with a "planned" tag for oil palm, glugu, coconut coir, applications, next directions for Composites only). No publications, grants, or projects there (owner decision). |
| Research areas (`research.yml`) | **Main field: Composite Materials Engineering** (bamboo, ramie, rice husk now; oil palm, coconut trunk/glugu, coconut coir are *planned*), then agro-processing machinery, manufacturing/CNC, energy & drives. |
| Publications | 25 from Google Scholar in 4 themes. DOIs for 8 (from ORCID), 17 without. One paper skipped (disk runner 20 kW, no year/venue). Agrikultura year: Scholar 2025 vs ORCID 2026 (site uses 2025). |
| Grants | 3 real (ICARE 2026, SPIRIT 2025, SPIRIT 2024). **Total funding awarded** card = Rp 688.613.150 (ongoing + completed, rupiah, from `amount_value`). No "Our role" line is shown on grants (the owner asked to remove it on 2026-11-05; do not re-add). No "under review" category (such grants are not listed). |
| Team | Director + 3 members: Muhammad Fadli Azis, S.T., M.Sc. (Electrical Power Systems), Muhammad Nawir, S.T., M.T. (Industrial Automation), and Syardah Ugra Al' Adawiyah, M.Sc. (Environmental Chemistry). Education/Experience data is kept in `team.yml` but not shown. Alumni empty (hidden). |
| About | Built from verified data (identity, counts, funders from grants, co-author institutions from Scholar). **Vision/Mission stay hidden by owner decision; do not ask again.** |
| News / Blog | News: launch + Bimtek item. Blog: welcome post (5 Nov) and the Bimtek ICARE Soppeng article (dated 6 Nov, published early at the owner's request). Both posts are bilingual. |
| Contact | Shows the director as "Research Director" with the group email; the social column is hidden while no accounts are set. |

### Design system

- Colours: **blue `#0b3d91` + yellow `#ffd60a` only** (red appears only as a publication-theme dot). Variables in `:root` of `assets/css/main.css`.
- Pattern: **hexagonal honeycomb** (`--pattern-lattice`, `--pattern-lattice-dark`, `--pattern-hex-row`); tile ratio 1:1.732, keep it in every `background-size`.
- Illustrations: animated inline SVG per research area, per featured card, and in the hero (`_includes/illus/*.html`, CSS `.il-*`, `.hv-*`, and `.iso-*`; the hero is isometric, the other illustrations are still the flat style), all pure CSS and paused under reduced motion. **Blog covers are static** (automatic when no photo, `_includes/post-cover.html`).
- Mobile navbar: the hamburger and close icons are ARG blue on a transparent button (the owner confirmed it looks good on iPhone). The bar itself is still translucent white; options "solid white" or "transparent over the hero" were offered and not chosen.
- Logo files in `assets/img/` (the artwork still contains "ATIM", owner's design). All photos are WebP; social preview is `og-logo.jpg`.

## 2. Open questions for the owner

0. **Contact form key** still points to fadli@atim.ac.id; swap to a key registered with the unit email when the owner sends it (section 5c).

Decided at the first monthly review (2026-11-05): group email, degrees in the profile, no vision/mission, campus site `https://atim.ac.id`, no new publications or grants.

1. **Bimtek article** (`_posts/2026-11-06-bimtek-icare-soppeng.md`): changed to past tense on 2026-11-07 (day 3 now reads as having happened, closing evaluation included as scheduled). Still open: outcomes (for example how many participants completed practice) and day-3 photos if the owner sends them. Speakers' affiliations, officials' names (Babinsa, Bhabinkamtibmas, BPP, PPL), and the expansion of "ESF" were never given and are omitted.
2. More members (name with degrees, role, focus, photo with consent), real news, DOIs and full author names for the other 17 papers, year/venue of the 20 kW disk runner paper, next directions for research areas 2-4, lab methods/equipment (only if the owner supplies real lists).
3. The owner should review the Indonesian text written by Claude (research descriptions, bio, About, and both translations of the blog posts).
4. **Domain `material-research.atim.ac.id`:** waiting for campus IT (section 5). The owner created and deleted a `CNAME` file once on 2026-11-05; the repo has none now, which is correct for the moment. Optional later: `main` as the GitHub default branch, Search Console.
5. Security: enable **2FA** on all org GitHub accounts, limit org Owners, verify the domain in the org Pages settings (TXT record), ask IT whether login cookies are scoped to all of `.atim.ac.id`.

## 3. How to do common things

- **Add a member:** `members:` in `_data/team.yml` (name with degrees, `role`/`role_id`, `focus`/`focus_id`, WebP photo in `assets/img/team/`, square about 240 px, new file name).
- **Add a publication / grant / news item:** `_data/publications.yml` (theme 1-4, DOI as `https://doi.org/...`), `grants.yml` (always `amount_value`, status `active` or `completed`), `news.yml` (links use `@BASE@`). Every text needs EN and ID.
- **Add a blog post:** `_posts/YYYY-MM-DD-title.md` with `title`, `title_id`, `summary`, `summary_id`, `tags`, `tags_id`, bilingual body blocks, optional `thumbnail` and `thumbnail_card` (WebP, sizes in CLAUDE.md). Without a photo a static illustration is used.
- **Restore a hidden page:** set `show_pages.<name>: true` and remove the file from `exclude:` in `_config.yml`.
- **Local build and screenshots:** `JEKYLL_NO_BUNDLER_REQUIRE=1 jekyll build --baseurl "" -d <outdir>` (gems in CLAUDE.md). Playwright/Chromium is preinstalled; serve the output with a tiny node server and inject `.fade-in{opacity:1!important}` to avoid mid-animation shots. WebKit/Safari is not available in the sandbox.

## 4. Working rules learned in this project

- Never invent data (people, papers, grants, results, quotes). Mark unknowns and ask.
- Planned research (new plant materials) is written as planned, not as done.
- News: ordinary news style, no logistics (times, session hours); speakers are named when the owner asks.
- **No colon (:) in site prose** (bio, descriptions); use "is"/"adalah" or split the sentence. Paper titles are left as written.
- **EN mode shows only English, ID mode only Indonesian** (posts, dates, tags included). English is the default; auto language detection was tried and removed.
- Copyright decision (2026-11-05): all rights reserved, see `LICENSE` and `README.md`. The repo stays public (the owner has no budget for a private-repo plan; Pages from a private repo needs a paid plan and would otherwise unpublish the site).
- Repo is public: no unpublished manuscripts, raw data, or personal phone/email without consent; photos of people only with consent.
- **Do not re-propose** the count-up animation on the hero stats (tried, owner found it odd).
- Safari/iPhone: never use `transparent` as a gradient stop, avoid `filter: drop-shadow` on animated SVG, prefix `backdrop-filter`. After a deploy, if the owner reports odd styling on the phone, first suspect a stale cache: `main.css`/`main.js` are cache-busted with `?v=<build time>`, but the HTML itself can be cached; ask for one reload in Safari (not inside WhatsApp).
- Sandbox limits: `scholar.google.com`, `orcid.org`, `pub.orcid.org` are blocked (the owner pastes data); `github.io` is not reachable (check deploys through GitHub Actions); the shell blocks `rm -rf`-style commands (avoid removals in scripts, build into a fresh folder name instead).
- After each push tell the owner the deploy takes 1-3 minutes and to hard refresh.

### Periodic update routine (owner agreed)

Update whenever something notable happens (new grant, paper, field activity) plus a light review at the end of each month (about 10 minutes). Ask the five questions and accept "none":
1. New or updated publications, new DOIs (Scholar/ORCID paste)?
2. New grants or status changes (rupiah amount; only awarded grants)?
3. New members, alumni, roles, photos (with consent)?
4. News or blog posts (both languages; photos as WebP)?
5. Changes to titles, affiliations, contact details, group email?
Then run `python3 tools/check.py --build`, fix errors, push to `main`, update the "Last updated" line and the content table here.

## 5. Custom domain: status and exact steps

- **Status:** not connected. Waiting for campus IT to create the DNS record. The owner has the one-page SOP (`docs/SOP-subdomain-github-pages.pdf`, source `.md`; folder `docs` is excluded from the build).
- **IT must create only a DNS record:** `CNAME material-research -> material-research.github.io` (Cloudflare: "DNS only"). **No hosting, no WordPress** (the campus normally creates a subdomain and installs WordPress; not wanted here). Fallback: four A records 185.199.108.153 / .109.153 / .110.153 / .111.153. The DNS may be at Cloudflare or an Indonesian host (`nslookup -type=NS atim.ac.id` shows which).
- **When the owner says DNS is active** (`nslookup material-research.atim.ac.id` shows `material-research.github.io`):
  1. add a `CNAME` file at the repo root containing only `material-research.atim.ac.id`;
  2. in `_config.yml` set `url: https://material-research.atim.ac.id` and `baseurl: ""`;
  3. build with `--baseurl ""`, run the checker, push to `main`;
  4. ask the owner to open Settings -> Pages, wait for the green DNS check, and tick **Enforce HTTPS**;
  5. update the "Live URL" here and in CLAUDE.md.
  Do steps 1-2 **only after** DNS works; earlier they break the live site (assets are served under `/web/`).
- Result: `https://material-research.atim.ac.id/team/` etc.; the old github.io address redirects. It is a DNS pointer, not a redirect or campus hosting. If the site is ever retired, ask IT to delete the CNAME.

## 5b. UI/UX round (2026-11-05, after the first review)

Done in one push: Publications shows 10 items first with "Show more" (filters or search show all matches), year filter is a dropdown, theme chips scroll sideways on phones, papers without a DOI get a "Find on Scholar" link, and the page carries schema.org `ScholarlyArticle` data; Featured Research is a 3-column grid; Home "What We Study" lede no longer repeats the first card; Contact gained Maps and campus links, a "helpful to include" list, and the research areas; footer Connect has a campus link; round "back to top" button; shared call-to-action band (`_includes/cta.html`) at the end of Research, Team, Grants; per-page meta descriptions (English, posts use their `summary`); visible keyboard focus and darker small grey text. New UI strings are in `i18n.yml` (bottom block). Recent News on Home shows the 3 newest items as the same cards as the Blog (shared include `post-card.html`, "Read more" on both) (whole card clickable when `url` is set; thumbnail from the linked post; button to the Blog). Older news is no longer listed on Home, so important items should also be Blog posts. The Home hero fills the first screen (`min-height` = viewport minus the 65 px navbar, `svh` for iPhone) and "What We Study" fades in on scroll (owner's choice; do not drop the fade to fix empty space). Not done on purpose: sticky filter bar on phones (too much screen space), site search (site is small).

## 5c. Contact form (live; key set 2026-11-05)

Status: the access key is in `_config.yml` and the form is shown. It was created in the Web3Forms panel from the account fadli@atim.ac.id with website URL `material-research.github.io/web/contact` (change that URL in the panel when the custom domain goes live). **Confirmed by a test message: messages currently arrive at fadli@atim.ac.id** (the key is tied to the account email; there is no recipient setting). The owner accepted this for now and will later register Web3Forms with agromaterialsrg@atim.ac.id and give Claude the new key; then replace `lab.contact_form_key`, update the website URL in the Web3Forms panel if the domain changed, push, and ask for one test message. Original build notes follow.

The Contact page has a real form (name, email, institution, topic, message, bilingual, honeypot against bots, in-page success and error messages with a mailto fallback). It uses **Web3Forms** (free, no server of our own) and is **hidden until `lab.contact_form_key` in `_config.yml` is filled**; with an empty key the page shows the email address only, so nothing is broken meanwhile. The checker warns "contact form is OFF" until then.
To switch it on: the owner opens https://web3forms.com, enters `agromaterialsrg@atim.ac.id` to get the access key by email (the key is public by design), then gives the key to Claude, who pastes it into `lab.contact_form_key`, runs the checker, pushes to `main`, and sends one test message. Messages arrive at the group email (reply-to is the sender). Free plan about 250 messages a month. The message passes through Web3Forms, which the form note says is "not published" (it is not). Test mode used mocked responses only; the real endpoint was not reachable from the sandbox.

## 5d. Isometric hero (live on Home since 2026-11-05)

The Home hero illustration is an **isometric 3D animated scene** (generated by `tools/gen_iso_hero.py` into `_includes/illus/hero-iso.html`; animation CSS `.iso-*` in `main.css`; hero layout `.hero--iso` gives a 500 px text column and an illustration that bleeds to the right screen edge). Style follows the owner's reference image (one diagonal conveyor, white cubes with icons and labels, a lettered machine, glowing yellow orb, IN/OUT badges) in blue and yellow only. Four input cubes (Bamboo, Ramie, Rice husk, Coconut), three outputs (Flame-retardant, Safety cabins, Grain storage), machine lettered "COMPOSITE PANEL PRODUCTION" (generic on purpose; hot press is what the ICARE Bimtek used, other studies may use hand lay-up). **English labels only; no labels at all on phones (width 640 px or less)**; no glass box; no "planned" tag by the owner's choice (the Research page still marks coconut trunk and coir as planned). The old animated hero (`_includes/illus/hero.html`, `.hv-*` CSS) is unused and can be deleted; it also lives in git history.
**Live since 2026-11-05:** the composites research-area illustration is isometric (`_includes/illus/composites-iso.html`, generated by `tools/gen_iso_composites.py` with the shared helpers in `tools/iso_lib.py`), switched on by `iso: true` in `_data/research.yml`; Home (`research-grid-figure--iso`) and the Research page (`res-figure--iso`) show it with no tile, no border, no floor. Owner's rules for these scenes: no background, soft ground shadows, light-to-mid blue faces with yellow accents so they read on the white page, a few small **English-only** labels (hidden on phones), same 322:226 viewBox so the layout stays the same for all four. The old flat `illus/composites.html` is unused (kept for rollback). On phones the Research card order is illustration, description and topics, then materials and next directions.
**All four research areas are isometric now** (agro, cnc, energy added 2026-11-05 with `tools/gen_iso_agro.py`, `gen_iso_cnc.py`, `gen_iso_energy.py`; the owner asked for them directly, in the style of the first one). Each has 3-4 small English-only labels hidden on phones. The old flat files `illus/composites|agro|cnc|energy.html` are unused (kept for rollback). **Zigzag layout** (owner's idea): on Home each area is a `.research-row`; odd rows put the illustration on the left (`research-row--flip`); on the Research page every even card mirrors its columns; on phones the illustration always sits above its heading. Not done: a drill bit for the composites scene (drilling behavior), the owner has not decided.
**Featured Research cards are isometric too** (`tools/gen_iso_featured.py` writes `illus/feat-bamboo-iso.html`, `feat-coffee-iso.html`, `feat-coconut-iso.html`; `iso: true` in `_data/projects.yml`; no tinted tile and no card frame (`project-card--open`, owner said illustrations look bad inside a frame); two English-only labels each, hidden on phones). The category links under each card are button-style pills (`.thrust-pill`) that open the matching area on the Research page (matched by `short` in `research.yml`). The welcome article's cover is the group logo on the hexagon tile (`cover: logo` in its front matter, also shown on the Blog list and in the Home news card). Blog covers without a photo still use the old flat bamboo, coffee, and coconut illustrations on a tile (to restyle only if the owner asks).
Optional (owner's wish, done): restyle the remaining research-area illustrations (`illus/agro|cnc|energy.html`) and the featured-card illustrations in the same isometric style; owner approves each step before it goes live.

## 5e. Phone polish (2026-11-05)

Audit at 360 and 390 px: no horizontal scroll on any page. Fixed in the last block of `main.css`: touch targets at least 40 px (profile links, filters, contact links, footer links, language buttons), small text no smaller than 12 px, Grants summary cards in one row of three, bio text left aligned on phones, every isometric research illustration has the same box on phones (322:215, max 440 px) so they look equally big, and the Home hero scene is cropped to its real content (labels are hidden on phones) and runs edge to edge so it is about 1.5x bigger.

Tablet check (768, 820, 1024 px): no horizontal scroll on any page. The Home hero scene was too small, so portrait tablets (641 to 900 px) show it up to 700 px wide and the two-column hero layout now starts at 901 px (title 2.55rem and a 420 px text column between 901 and 1099 px).

## 6. History (short)

- Prototype `fadhlyid/material-lab` (placeholder content) moved into this repo; Pages enabled by the owner.
- 2026-11-05: branding from the logo, real data (Scholar, ORCID, grants), About page, flat navbar, members, animated and static illustrations, hexagon pattern, composite-materials focus, name without "ATIM", English default, first news and article (Bimtek ICARE Soppeng), WebP image audit and cache-busting, Research page redesign, new hero, data checker, `main` as publishing branch, domain SOP for campus IT, first monthly review, mobile navbar icons.
- 2026-11-05 (end of day): at the owner's request the 78 earlier commits were squashed into one "Initial release" commit so the public history starts clean (archive bundle sent to the owner). From here on, every change is a normal commit on `main`; do not rewrite history again unless the owner asks.
- Details are in `git log`.


### 5f. Grants total card (2026-11-06)
Count-up animation for the total; second column shows the US-dollar equivalent from a live USD/IDR rate with an update note (fallback rate in `_config.yml`, `lab.usd_idr_fallback`, now 18100 (Frankfurter value of 2026-11-06); refresh now and then). Live fetch was tested only with a mocked response (sandbox has no external network). Added team member Syardah Ugra Al' Adawiyah; Fadli's focus changed to Electrical Power Systems.

### 5g. Home funding stat (2026-11-07)
Home hero third stat is now the approximate total funding in US dollars (`38K` with label "Funding awarded (USD)", always USD, both languages, not a link). Total comes from `_includes/grant-calc.html` (shared by Home and Grants, single source = `_data/grants.yml`), rate from the same JS as the Grants card; the checker verifies the Home total equals the data. Optional Google Sheet rate (`lab.usd_idr_sheet`) still waiting for the owner's published CSV link; reference rate `usd_idr_fallback` is still a guess now 18100 (Frankfurter value of 2026-11-06); refresh now and then.

### 5h. Motion polish, stage 1 (2026-11-07)
Added in `main.js` ("Motion polish") and the end of `main.css`: scroll progress bar, hero parallax (isometric scene and hexagon pattern follow the pointer, desktop only), 3D tilt and yellow glow on cards (`.tilt`), leaning buttons, staggered reveal of cards that enter together, cross-document page transition (`@view-transition`), new share image `assets/img/og-card.jpg` (1200x630, generated once with Pillow; `twitter:card` is now `summary_large_image`). All pointer effects need `(hover: hover) and (pointer: fine)` and are off for "reduce motion". Weight check (Home, local assets): 310 KB before, 316 KB after (JS +4 KB, CSS +1 KB). Next: stage 2 (plant-to-product flow map, search, dark mode, charts).

### 5i. Stage 2 (2026-11-07)
- **From plant to product** map on Home (`_data/flow.yml`, `_includes/flow-map.html`, JS "From plant to product"): 5 selectable steps, auto-advance until the visitor interacts. Text is generic and based on topics already on the site; edit `flow.yml` (EN and ID twins, exactly 5 steps). Checker validates it.
- **Site search**: magnifier in the nav (and in the bar on phones), Ctrl/Cmd+K or "/". Index is `search.json` (Liquid, built from pages, research, team, grants, posts, publications), loaded only when the box is first opened. Publication results without a DOI open `/publications/?q=title`.
- **Publication charts** (per year, per research area) above the filters on Publications; clicking a bar sets the existing filter.
- Nav logo text now ellipsizes and shrinks on phones so the menu button stays on screen with the search icon.
- Dark mode was deliberately NOT done: the isometric scenes and many fixed colours are designed for a light page; would need a full re-palette. Revisit only if the owner insists.

### 5j. Hero typing word (2026-11-07)
The highlighted word in the Home hero title types, deletes, and rotates through 3 words forever (EN: plant-based, renewable, agricultural; ID: nabati, terbarukan, pertanian). Words live in `hero_title` in `_data/i18n.yml` as `data-words="a|b|c"` on `.typer`; logic in `main.js` ("Hero title"), cursor CSS at the end of `main.css`. The h1 keeps the tallest height so nothing jumps; it pauses when the hero is off screen or the tab is hidden; "reduce motion" or no JS shows the first word only; changing EN/ID restarts it.

### 5k. History squashed again (2026-11-07)
At the owner's explicit request the git history of `main` was replaced by one "Initial release" commit containing the site exactly as it was (stage 1 and 2 polish, typing hero, Syardah in Team, etc.). Earlier commits no longer exist on GitHub (the owner keeps an older bundle from 2026-11-05 only).
