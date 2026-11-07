# CLAUDE.md — Agromaterials Research Group website

Read this file first, then `HANDOFF.md` (current status and next steps).

## What this repo is

A static **Jekyll** website for the **Agromaterials Research Group**, Politeknik ATI Makassar (main field: composite materials
engineering; also agro-processing machinery, manufacturing/CNC, energy and drive systems), published with **GitHub Pages**.
The layout follows a clean academic-lab template (hero, research areas, featured research, news, team, filterable publications,
grants, blog, about, contact). CSS and JS are original; nothing was copied from the reference site.

- Live: https://material-research.github.io/web/ (repo `material-research/web`, published branch `main`)
- Planned domain: `material-research.atim.ac.id` (needs a CNAME from campus IT; then set
  `url: https://material-research.atim.ac.id` and `baseurl: ""` in `_config.yml` and add a `CNAME` file)
- Owner's preferred language for chat: Indonesian. The website is **bilingual (English default, Indonesian via the EN | ID button)**. Current status, open questions, and recipes are in `HANDOFF.md`.

## Where things live

| Change | File |
|---|---|
| Group name, email, address, social links, site URL | `_config.yml` |
| Colours | `:root` in `assets/css/main.css` |
| Home hero text | `_data/i18n.yml` (`hero_title`, `hero_tagline`) |
| Research themes | `_data/research.yml` |
| Projects (home cards) | `_data/projects.yml` |
| News | `_data/news.yml` |
| Team and alumni | `_data/team.yml` (photos: `assets/img/team/`) |
| Publications and filter themes | `_data/publications.yml`, `_data/pub_themes.yml` |
| Grants (funder, scheme, amount, period, status) | `_data/grants.yml` |
| Resources | `_data/resources.yml` |
| Calendar | `_data/deadlines.yml` |
| Blog | `_posts/YYYY-MM-DD-title.md` |
| Interface strings (menu, buttons, headings) in EN and ID | `_data/i18n.yml` |
| Shared layout | `_layouts/`, `_includes/nav.html`, `_includes/footer.html` |

Content is data-driven: prefer editing `_data/*.yml` over editing HTML.

## Bilingual (EN | ID) system

- Every translated string is rendered twice, `<span data-lang="en">` and `<span data-lang="id">`; CSS shows
  only the language set on `<html lang>`. The choice is stored in `localStorage` (`lang`). Default is English for every visitor (no browser-language detection, by the owner's decision).
- UI text: add a key to `_data/i18n.yml` (`{ en: ..., id: ... }`) and use `{% include t.html key="..." %}`.
- Content data: add `field_id` next to `field` (e.g. `desc` / `desc_id`) and use
  `{% include tt.html en=x.desc id=x.desc_id %}`. If the `_id` value is empty, English is shown.
- Page titles/subtitles/ledes use `title_id`, `subtitle_id`, `lede_id` in front matter.
- Jekyll 3 `include` params cannot contain `[ ]`; assign to a variable first.
- `_includes/t.html` and `tt.html` must have **no trailing newline** (it would add a stray space before punctuation).
- Not translated by design: publication titles/venues and personal names. **Blog posts are bilingual** (see "Posts" below), so each language mode shows only its own language.
- JS strings (counts, calendar) live in `_data/i18n.yml` under `js_*` keys.
- **Every new piece of text needs both languages.**

## Optional / hidden pages

`resources.html`, `deadlines.html` (Calendar) and `apply.html` are hidden for now (Grants is visible). In `_config.yml`:
`show_pages.<name>: false` hides the menu links, and the three files are listed under `exclude:` so they
are not built. To bring one back, set its flag to `true` and delete its file name from `exclude:`.
Do not delete these pages or their data files unless the owner asks.

## Blog covers

Every post always has a cover. If the post has `thumbnail: file.jpg` in front matter (file in `assets/img/`), the photo is used.
**Photo sizes (keep the site fast):** use **WebP** for every photo and logo (owner already works in WebP; quality about 65-80, `method=6`). Keep JPEG/PNG only where WebP is not reliable (the social preview `og-logo.jpg`, favicon and apple-touch PNGs). `thumbnail` = article hero, about 1100 px wide, under about 120 KB.
`thumbnail_card` = blog list card, 640x360, under about 50 KB (the list uses it; the first card loads eagerly, the rest lazily). Inline
photos about 1000 px wide, under about 120 KB. Team photos square about 240 px (director portrait about 490x612), under about 40 KB. Never put a full-size camera photo in the repo. Use a new file name when replacing a photo (browser cache).
A post can also set `cover: logo` in front matter to show the group logo centred on the hexagon tile (used by the welcome post). Otherwise `_includes/post-cover.html` shows a **static** illustration (bamboo / coffee / coconut) chosen by front-matter `illus:`,
then by tags (bamboo, composite, fiber / coffee, agro, machine / coconut, ginger), then by title length. Never leave a post without a cover.

## Posts, news links, and dates

- `_config.yml` has `future: true`, so posts dated later than today are still published.
- **Every post has both languages.** Front matter: `title`, `title_id`, `summary`, `summary_id` (card text), `tags`, `tags_id`. Body: one
  `<div data-lang="en" markdown="1">...</div>` and one `<div data-lang="id" markdown="1">...</div>` (translated paragraph for paragraph). An inline
  figure sits between the blocks, with its caption written as two `<span data-lang>` spans. Dates are formatted per language by
  `_includes/date-long.html` and `date-short.html` (Indonesian month names). Do not publish a post in only one language.
- Inline photos in a post: `<figure class="post-figure"><img src="{{ '/assets/img/blog/x.jpg' | relative_url }}" alt="..."><figcaption>...</figcaption></figure>`.
- Links to site pages inside `_data/news.yml` use the placeholder `@BASE@` (replaced by `site.baseurl` in `index.html`), e.g. `href="@BASE@/blog/..."`.

## Research page

`research.html` renders each area of `_data/research.yml` as a detail card (jump menu, number, "Main field" badge on the entry with `main: true`,
same illustration as Home, same description as Home). Extra optional fields per area, each with an `_id` twin for Indonesian: `short`, `anchor`,
`topics`, `materials` (items `{ en, id, planned: true }`; `materials_label: commodities` for non-material lists), `apps`, `next`.
It deliberately has **no publications, grants, or featured projects** (they have their own pages). The Home page template is not touched by this page.
Add a new area by adding an entry (with `illus` and an SVG include plus an `elsif` in both `index.html` and `research.html`).

## Grants total

The Grants page shows a **Total funding awarded** card computed from `_data/grants.yml`. Every grant needs `amount_value` (plain number, IDR, no dots)
next to the free-text `amount`; only `status: active` or `completed` grants in rupiah are summed (add `currency: USD` etc. to leave a grant out). There is no "under review"
category: grants with `status: submitted` are not shown at all, so do not add them until they are awarded. Adding a grant with `amount_value` updates the total automatically.

Optional near-real-time rate: `lab.usd_idr_sheet` in `_config.yml` = URL of a Google Sheet published to the web as CSV (A1 `=GOOGLEFINANCE("CURRENCY:USDIDR")`, B1 optional `=NOW()`); tried first, then the public services.

Grants total card: Rupiah (from data) counts up, plus an approximate US-dollar total computed in the browser from a live USD/IDR rate (Frankfurter, backup open.er-api.com; code in `main.js`, "Grants total"). If both fail, the reference rate `lab.usd_idr_fallback` / `usd_idr_fallback_date` in `_config.yml` is used and labelled as such; refresh it now and then. The checker reads the Rupiah figure from `id="gtIdr"`.

## Copyright

The owner chose **all rights reserved** (2026-11-05, option A): `LICENSE` and the notice in `README.md` say content, photos, logo, illustrations, and code may not be reused
without written permission (requests to agromaterialsrg@atim.ac.id). Keep both files. Do not add third-party code or media with licences that require attribution or
sharing without telling the owner. `LICENSE` is excluded from the build.

## Shared pieces added in the UI round

`_includes/cta.html` (call-to-action band, used at the end of Research, Team, Grants), back-to-top button (`#toTop` in `_layouts/default.html`, logic in `main.js`), Publications "show 10 first" limit (`PUB_LIMIT` in `main.js`), per-page `description:` front matter (used for meta and Open Graph; posts fall back to `summary`). Every new page needs a `description:`.

## Contact form

`contact.html` shows a Web3Forms form only when `lab.contact_form_key` (in `_config.yml`) is non-empty; otherwise just the email address. Logic is in `main.js` ("Contact form"), strings are the `form_*` keys in `i18n.yml`, styles `.contact-form*` in `main.css`. Do not add a second service or store messages in the repo (privacy). The key is public by design, not a secret.

## News items

`_data/news.yml` items are shown on Home as the same cards as the Blog page (`_includes/post-card.html` is shared by `blog.html` and Home: cover, date, bold title, summary, "Read more"; do not fork the two designs), **the 3 newest only**, followed by a "See all articles" button to the Blog. A `url` makes the whole card a link; when it is a blog post, the card shows that post's cover, title, and summary (the news `html` text is then not displayed); a news item without a post uses its `html` text as the title, with `image` (WebP, under 60 KB) or a patterned placeholder. With a `url` the text must not contain `<a>` links. The checker enforces this.

## Email links

Every `mailto:` link also copies the address and shows a small notice (`main.js`, "Email links"; strings `copied`), because `mailto:` does nothing on devices or in-app browsers (for example WhatsApp) that have no mail app. Keep using plain `mailto:` links; the script adds the behaviour.

## Isometric illustrations

The Home hero and the composites research area use isometric 3D animated SVGs generated by Python (`tools/gen_iso_hero.py`, `tools/gen_iso_composites.py`, shared `tools/iso_lib.py`); do not hand-edit the generated `_includes/illus/*-iso.html` or `hero-iso.html`, change the generator and re-run it. Featured Research cards use `iso: true` in `_data/projects.yml` (generator `tools/gen_iso_featured.py`). Research areas switch with `iso: true` in `_data/research.yml` (all four are on; generators `gen_iso_composites|agro|cnc|energy.py`, shared `iso_lib.py`). Home uses zigzag rows (`.research-row`, odd rows flipped); a new area needs its `{% if t.iso %}` branch in both `index.html` and `research.html`. Rules from the owner: blue and yellow only, labels in English only and hidden on phones, no glass box or tile behind the scene, keep the text small. CSS is the `.iso-*` block in `main.css`.

## Home flow map, site search, charts

`_data/flow.yml` drives the Home "From plant to product" map (exactly 5 steps, EN/ID twins). `search.json` is the site-search index (add new content types there). The Publications charts are plain Liquid counts; do not add a chart library.

## Naming

The group's name on the site is **Agromaterials Research Group** (no "ATIM" prefix); the campus is **Politeknik ATI Makassar**.
The logo image itself still contains the text "ATIM" (owner's artwork). Email domain `atim.ac.id` is unchanged.

## Rules

1. **Links must use `relative_url`** (`{{ '/research/' | relative_url }}`), never a bare `/research`,
   so the site works under `/web/` and on a custom domain.
2. **Safari/iPhone safety.** The owner uses iPhone Safari and only Chromium is available for testing. Never use the keyword `transparent` as a gradient stop (write the same colour at alpha 0, otherwise Safari shows grey/black), avoid `filter: drop-shadow` on animated SVG, prefix `backdrop-filter` with `-webkit-`, and prefer explicit `top/right/bottom/left` over `inset`.
3. Keep dependencies at zero: plain CSS and vanilla JS. Icons/fonts load from CDNs.
4. **Placeholders**: entries marked `[Example]`, "Your Name", `TODO`, or `example.ac.id` are fake.
   Never present them as real data; replace them when the owner provides real information.
5. **Privacy**: the repo is public. Do not commit unpublished manuscripts, raw research data,
   credentials, or personal contact details without the owner's consent.
6. Do not invent publications, people, grants, or results.
7. Do not create a pull request unless asked.
8. **Publishing branch: `main`.** The owner gave standing permission (2026-11-05, "Ya, push langsung ke main") to commit and push **directly to `main`**
   for this repo; GitHub Pages publishes `main`, so every push goes live. Work on `main`, no pull request or merge step. Do not force-push or
   rewrite history on `main` (exceptions: on 2026-11-05 and again on 2026-11-07 the owner explicitly asked for the whole history to be squashed into a single "Initial release" commit holding the current site; force-push only when the owner asks for it again). Test the build locally before pushing.

## Data checker (run before every push)

```bash
python3 tools/check.py --build
```

Needs PyYAML and Jekyll. It checks publications (theme, year, DOI format, duplicates), grants (`amount_value`, status, EN/ID twins), research areas
(topics/apps length vs `_id`, illustration file), projects, team (photos exist), news links (`@BASE@`), every `i18n` key (EN and ID), blog posts
(both languages, summary, tags, cover files), image sizes (blog 130 KB max, card 60 KB, team 50 KB, WebP), placeholder text, the no-colon style rule, and with
`--build` also internal links and that the numbers shown on the site (hero stats, grants total) match the data. **ERROR means do not push.** WARN items
(no DOI yet, `TODO` in the config) are reminders for the owner. If you add a new kind of data, extend the checker.

## Preview and test

```bash
bundle install && bundle exec jekyll serve   # http://localhost:4000/web/
```

Quick build check without bundler (as used in cloud sessions):
`gem install jekyll -v 3.10.0 kramdown-parser-gfm jekyll-sitemap webrick`, then
`JEKYLL_NO_BUNDLER_REQUIRE=1 jekyll build -d /tmp/site`.
After changes, check there are no broken internal links and no JS console errors.

## Deployment

`main.css` and `main.js` are linked with `?v=<build time>` in `_layouts/default.html` (cache-busting), so a new deploy always loads fresh styles. Do not remove it.

GitHub Pages builds automatically on every push to `main` (the published branch). A change appears on
the web 1–3 minutes after it is pushed to that branch. Check the Actions tab for the
"pages build and deployment" run.

## Session handoff protocol

At the end of every work session, **update `HANDOFF.md`**:
- what was done (with the files touched),
- what is still pending or blocked,
- decisions made and why,
- which branch is published by Pages,
- anything the owner must do (settings, DNS, content they promised to send).

At the start of a session, read `HANDOFF.md`, then `git log --oneline -10`, before changing
anything. Commit `HANDOFF.md` together with the work.
