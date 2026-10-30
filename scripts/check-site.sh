#!/usr/bin/env bash
# Checks the built site before it is published: every local link and picture exists, every page links the imprint and
# the privacy page, every project has a card on the start page, and every page has what search engines read
# (title, description, canonical address, Open Graph picture, an entry in sitemap.xml, valid JSON-LD).
#
#   python3 scripts/build.py && scripts/check-site.sh [folder]
set -euo pipefail

site="$(cd "${1:-$(dirname "$0")/../_site}" && pwd)"
failed=0

while IFS= read -r page; do
  dir="$(dirname "$page")"
  name="${page#"$site"/}"
  for target in $(grep -oE '(href|src)="[^"#?]*' "$page" | sed -E 's/^(href|src)="//' | grep -vE '^(https?:|mailto:)' || true); do
    [[ -z "$target" ]] && continue
    if [[ "$target" == /* ]]; then path="$site$target"; else path="$dir/$target"; fi
    [[ -d "$path" ]] && path="$path/index.html"
    if [[ ! -e "$path" ]]; then
      echo "$name verlinkt $target, das gibt es nicht." >&2
      failed=1
    fi
  done
  for legal in impressum.html datenschutz.html; do
    if ! grep -q "href=\"/$legal\"" "$page"; then
      echo "$name verlinkt $legal nicht." >&2
      failed=1
    fi
  done
  for tag in 'name="description"' 'property="og:image"' '<title>' 'rel="canonical"'; do
    if ! grep -q "$tag" "$page"; then
      echo "$name hat kein $tag." >&2
      failed=1
    fi
  done
  canonical="$(grep -oE 'rel="canonical" href="[^"]*"' "$page" | sed -E 's/.*href="//; s/"$//')"
  if [[ "$name" != 404.html ]] && ! grep -q "<loc>$canonical</loc>" "$site/sitemap.xml"; then
    echo "sitemap.xml fehlt $canonical ($name)." >&2
    failed=1
  fi
done < <(find "$site" -name '*.html' | sort)

for project in "$site"/projekte/*/; do
  slug="$(basename "$project")"
  if ! grep -q "href=\"/projekte/$slug/\"" "$site/index.html"; then
    echo "index.html stellt $slug nicht vor." >&2
    failed=1
  fi
done

for file in og.png robots.txt sitemap.xml feed.xml CNAME fonts/ubuntu/LICENCE.txt; do
  if [[ ! -f "$site/$file" ]]; then
    echo "$file fehlt." >&2
    failed=1
  fi
done

titles="$(find "$site" -name '*.html' -exec grep -h -o '<title>[^<]*</title>' {} + | sort | uniq -d)"
if [[ -n "$titles" ]]; then
  echo "Doppelte Titel: $titles" >&2
  failed=1
fi

if ! python3 - "$site" <<'PY'
import json, re, sys, pathlib, xml.dom.minidom
ok = True
for page in pathlib.Path(sys.argv[1]).rglob("*.html"):
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page.read_text(), re.S):
        try:
            json.loads(block)
        except ValueError as error:
            print(f"{page.name}: JSON-LD kaputt: {error}", file=sys.stderr)
            ok = False
for name in ("sitemap.xml", "feed.xml"):
    xml.dom.minidom.parse(str(pathlib.Path(sys.argv[1]) / name))
sys.exit(0 if ok else 1)
PY
then
  failed=1
fi

if [[ $failed -ne 0 ]]; then exit 1; fi
echo "Seite in Ordnung: $site"
