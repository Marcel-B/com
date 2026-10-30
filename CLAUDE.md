# CLAUDE.md

The website marcelbenders.com: Marcel's projects, their status reports ("Wasserstandsmeldungen") and tutorials.
Content is Markdown with YAML front matter in `content/`, built by `scripts/build.py` (Markdown, PyYAML, pinned in
`requirements.txt`) into `_site/`, checked by `scripts/check-site.sh`, published by `.github/workflows/pages.yml` on
GitHub Pages from main. `static/` is copied as it is; `static/CNAME` holds the domain.

- How projects add content is `CONTRIBUTING.md` (German, also addressed to Claude sessions in other repositories);
  keep it in step with the front matter `build.py` reads.
- `python3 scripts/build.py && scripts/check-site.sh` must pass. The build stops on missing fields or bad dates with the
  file's name; the check covers local links, imprint/privacy links, project cards, title/description/canonical/og:image
  per page, sitemap entries, unique titles, valid JSON-LD, sitemap and feed XML.
- All markup lives in `build.py`'s templates and `static/style.css`; links are absolute (`/…`). German, du-form, system
  fonts for text, Ubuntu (self-hosted, `static/fonts/ubuntu/` with its licence; never change those files) for headings.
  No cookies, trackers or third-party requests.
- Motion stays subtle (slow hero blobs, reveal on scroll in `static/main.js`, hover lifts) and stops under
  `prefers-reduced-motion`; without JavaScript nothing is hidden.
- Texts are for visitors. Never internal hostnames, IPs, Tailnet names or keys; nothing stated as done that only ran in a
  test environment.
- Commit messages and branch names are German.
