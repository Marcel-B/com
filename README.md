# marcelbenders.com

Die Website [marcelbenders.com](https://marcelbenders.com/): Marcels Projekte mit ihrem Wasserstand (wie weit sie sind,
was geplant ist) und Anleitungen, wie man sie selbst aufsetzt und nutzt.

**Inhalte ergänzen:** siehe [CONTRIBUTING.md](CONTRIBUTING.md). Jedes Projekt kann dort eigene Wasserstandsmeldungen
und Anleitungen als Markdown einreichen.

## Aufbau

| Ordner | Inhalt |
| --- | --- |
| `content/projekte/<projekt>/` | `projekt.md`, `stand/*.md` (Wasserstandsmeldungen), `anleitungen/*.md` |
| `content/seiten/` | Impressum, Datenschutz |
| `static/` | wird unverändert übernommen: `style.css`, `main.js`, Schrift, Bilder, `og.png`, `CNAME` |
| `scripts/build.py` | baut alles nach `_site/` (Python mit Markdown und PyYAML aus `requirements.txt`) |
| `scripts/check-site.sh` | prüft `_site/`: Links, Rechtliches, SEO-Angaben, Sitemap, JSON-LD |

Wie bei [tonwerk.studio](https://github.com/Marcel-B/Synth/tree/main/website): statisch, auf Deutsch, ohne Cookies,
Tracker und Anfragen an Dritte.

```sh
pip install -r requirements.txt
python3 scripts/build.py && scripts/check-site.sh
python3 -m http.server -d _site 8000    # lokal ansehen: http://localhost:8000
```

## Schrift

Überschriften sind in **Ubuntu** gesetzt (Copyright 2011 Canonical Ltd., [Ubuntu Font Licence 1.0](static/fonts/ubuntu/LICENCE.txt)).
Die Dateien kommen unverändert aus `@fontsource/ubuntu` 5.3.0 (Zeichensatz latin, Schnitte 500 und 700) und liegen
auf der Seite selbst, damit kein Besuch Google oder einen anderen Anbieter erreicht. Die Lizenz verlangt, dass jede
Kopie der Schrift den Copyright-Vermerk und den Lizenztext mitbringt: Beides steht in
`static/fonts/ubuntu/LICENCE.txt`, das mit veröffentlicht wird, und das Impressum verweist darauf. Die Dateien dürfen
nicht verändert (etwa weiter beschnitten) werden, ohne die Schrift umzubenennen; neue Schnitte also wieder unverändert
von Fontsource übernehmen.

## Suchmaschinen

Jede Seite bekommt einen eigenen Titel, eine Beschreibung, eine `canonical`-Adresse, Open Graph mit `og.png`
(1200 × 630) und strukturierte Daten nach schema.org (Startseite: `WebSite`, `Person`, `ItemList`; Projekte:
`SoftwareSourceCode`, bei Apps `SoftwareApplication`; Meldungen: `BlogPosting`; Anleitungen: `TechArticle`; dazu
`BreadcrumbList`). `sitemap.xml`, `robots.txt` und der Atom-Feed `feed.xml` entstehen beim Bauen. Nach dem ersten
Deploy die Seite in der [Google Search Console](https://search.google.com/search-console) anmelden und die Sitemap
einreichen.

## Veröffentlichen

Jeder Push auf `main` baut und veröffentlicht die Seite über GitHub Pages (`.github/workflows/pages.yml`); Pull
Requests bauen und prüfen nur.

Einmalig einzurichten:

- GitHub: *Settings → Pages → Source: GitHub Actions*, danach unter *Custom domain* `marcelbenders.com` eintragen und
  *Enforce HTTPS* einschalten, sobald das Zertifikat da ist.
- DNS bei STRATO (erlaubt nur einen A-Record; einer genügt):
  - `marcelbenders.com` A: `185.199.108.153` (weitere wären `.109`, `.110`, `.111`)
  - `www.marcelbenders.com` als Subdomain mit CNAME `marcel-b.github.io`
