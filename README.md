# Agromaterials Research Group website

Website of the **Agromaterials Research Group**, Politeknik ATI Makassar. Main field is composite materials engineering, with agro-processing machinery, manufacturing and CNC, and energy and drive systems.
Static [Jekyll](https://jekyllrb.com/) site on GitHub Pages, bilingual (English and Indonesian).

- Live site: https://material-research.github.io/web/ (planned domain `material-research.atim.ac.id`)
- Publishing branch: `main` (every push goes live in 1 to 3 minutes)

## Copyright and reuse

© 2026 Agromaterials Research Group, Politeknik ATI Makassar. **All rights reserved.** The content, photographs, logo, illustrations, and code are shared for viewing only and may not be copied or reused without written permission. See [LICENSE](LICENSE). Permission requests: agromaterialsrg@atim.ac.id

**Hak cipta.** Konten, foto, logo, ilustrasi, dan kode dilindungi dan tidak boleh disalin atau dipakai ulang tanpa izin tertulis. Lihat [LICENSE](LICENSE). Permintaan izin ke agromaterialsrg@atim.ac.id

## For maintainers

Read `CLAUDE.md` (rules and file map) and `HANDOFF.md` (current status, open questions, recipes) first.

| What | Where |
|---|---|
| Group name, email, address, site URL | `_config.yml` |
| Colours | `:root` in `assets/css/main.css` |
| Research areas, projects, news | `_data/research.yml`, `projects.yml`, `news.yml` |
| Team and photos | `_data/team.yml`, `assets/img/team/` |
| Publications and grants | `_data/publications.yml`, `pub_themes.yml`, `grants.yml` |
| Blog posts | `_posts/` (always English and Indonesian) |
| Interface text in both languages | `_data/i18n.yml` |

Before every push run the data checker:

```bash
python3 tools/check.py --build
```

Local preview:

```bash
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000/web/ (use the `baseurl` from `_config.yml`).

## Notes

- Do not commit unpublished manuscripts, raw research data, credentials, or personal contact details to this public repository.
- Photos of people are published only with their consent.
