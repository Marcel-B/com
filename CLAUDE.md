# CLAUDE.md

The website marcelbenders.com: Marcel's projects (vision, features as a light specification, roadmap), their status
reports ("Wasserstandsmeldungen") and tutorials, in German at `/` and English under `/en/` (same paths; a file's English
version is `<name>.en.md` beside it, required for projects and the pages in `content/seiten/`).
Content is Markdown with YAML front matter in `content/`, built by `scripts/build.py` (Markdown, PyYAML, pinned in
`requirements.txt`) into `_site/`, checked by `scripts/check-site.sh`, published by `.github/workflows/pages.yml` on
GitHub Pages from main. `static/` is copied as it is; `static/CNAME` holds the domain.

- How projects add content is `CONTRIBUTING.md` (German, also addressed to Claude sessions in other repositories);
  keep it in step with the front matter `build.py` reads.
- `python3 scripts/build.py && scripts/check-site.sh` must pass. The build stops on missing fields or bad dates with the
  file's name; the check covers local links, imprint/privacy links, project cards, title/description/canonical/og:image
  per page, sitemap entries, unique titles, valid JSON-LD, sitemap and feed XML.
- Template texts live in `build.py`'s `T` in both languages; content brings its own. Localisation stays on every
  project's roadmap until its interface is translated (Marcel's rule from 2026-10-30).
- Proper names in prose are linked by `build.py` from `content/links.yml` (first appearance per page; `partner: true` marks
  an affiliate link as an ad and needs the privacy page's `#partnerlinks` section). Code blocks get a copy button from
  `static/main.js`.
- The colour scheme (system, light, dark) is set by the inline script in every page's head from `localStorage.theme`
  and switched in `static/main.js`; dark tokens exist twice in `style.css` (media query and `[data-theme="dark"]`).
- All markup lives in `build.py`'s templates and `static/style.css`; links are absolute (`/…`). German, du-form, system
  fonts for text, Ubuntu (self-hosted, `static/fonts/ubuntu/` with its licence; never change those files) for headings.
  No cookies, trackers or third-party requests.
- Motion stays subtle (slow hero blobs, reveal on scroll in `static/main.js`, hover lifts) and stops under
  `prefers-reduced-motion`; without JavaScript nothing is hidden.
- Texts are for visitors. Never internal hostnames, IPs, Tailnet names or keys; nothing stated as done that only ran in a
  test environment.
- Commit messages and branch names are German.
