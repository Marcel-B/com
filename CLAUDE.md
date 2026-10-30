# CLAUDE.md

The website marcelbenders.com: Marcel's projects, one page each. Plain static HTML/CSS in `site/` (German, du-form,
system fonts only, no web fonts, cookies, trackers or third-party requests), set up like tonwerk.studio in Marcel-B/Synth.
Published by `.github/workflows/pages.yml` on GitHub Pages from main; `site/CNAME` holds the domain.

- `scripts/check-site.sh` must pass: every local link exists, every page links `impressum.html` and `datenschutz.html`,
  every `site/projekte/*.html` has a card in `site/index.html`.
- Every page carries the same header and footer; change them on all pages together. Styles live only in `site/style.css`
  (light and dark through `prefers-color-scheme`).
- Project texts are written from the projects' READMEs for visitors: what it does, then the technology. Leave out
  internal hostnames, IPs, Tailnet names and keys.
- Commit messages and branch names are German.
