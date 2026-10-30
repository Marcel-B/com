# marcelbenders.com

Die Website [marcelbenders.com](https://marcelbenders.com/): Marcels Projekte im Überblick, eine Seite pro Projekt.

Kein Build-Schritt und kein Generator, wie bei [tonwerk.studio](https://github.com/Marcel-B/Synth/tree/main/website):
reines HTML und CSS in `site/`, auf Deutsch, ohne Web-Fonts, Cookies und Tracker.

```sh
scripts/check-site.sh                  # prüft Links, Impressum/Datenschutz und dass jedes Projekt auf der Startseite steht
python3 -m http.server -d site 8000    # lokal ansehen: http://localhost:8000
```

## Ein Projekt hinzufügen

1. `site/projekte/<name>.html` aus einer vorhandenen Projektseite kopieren und anpassen, auch Titel, Beschreibung,
   `canonical`, `og:*` und die strukturierten Daten (`application/ld+json`) im Kopf.
2. In `site/index.html` eine Karte (`<a class="card" href="projekte/<name>.html">`) und einen Eintrag in der `ItemList`
   der strukturierten Daten dazulegen.
3. Die Adresse in `site/sitemap.xml` eintragen.
4. `scripts/check-site.sh` laufen lassen.

## Suchmaschinen

Jede Seite hat einen eigenen Titel, eine Beschreibung, eine `canonical`-Adresse, Open-Graph-Angaben mit dem Vorschaubild
`site/og.png` (1200 × 630) und strukturierte Daten nach schema.org (Startseite: `WebSite`, `Person`, `ItemList`;
Projektseiten: `SoftwareSourceCode`, bei Apps `SoftwareApplication`, `BreadcrumbList`). `site/sitemap.xml` und
`site/robots.txt` liegen daneben, `site/404.html` ist die Fehlerseite (`noindex`). Nach dem ersten Deploy die Seite
in der [Google Search Console](https://search.google.com/search-console) anmelden und die Sitemap einreichen.

## Veröffentlichen

Jeder Push auf `main` veröffentlicht `site/` über GitHub Pages (`.github/workflows/pages.yml`); Pull Requests prüfen nur.
Die Domain steht in `site/CNAME`.

Einmalig einzurichten:

- GitHub: *Settings → Pages → Source: GitHub Actions*, danach unter *Custom domain* `marcelbenders.com` eintragen und
  *Enforce HTTPS* einschalten, sobald das Zertifikat da ist.
- DNS bei STRATO (erlaubt nur einen A-Record; einer genügt, die vier sind nur Redundanz):
  - `marcelbenders.com` A: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
  - `marcelbenders.com` AAAA (optional): `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
  - `www.marcelbenders.com` CNAME: `marcel-b.github.io`
