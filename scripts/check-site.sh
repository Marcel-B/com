#!/usr/bin/env bash
# Checks the static site in site/ before it is published: every local link and picture must exist, every page links
# the imprint and the privacy page, and every project page is linked from the start page.
#
#   scripts/check-site.sh
#   python3 -m http.server -d site 8000     # to look at it locally
set -euo pipefail

site="$(cd "$(dirname "$0")/.." && pwd)/site"
failed=0

while IFS= read -r page; do
  dir="$(dirname "$page")"
  name="${page#"$site"/}"
  for target in $(grep -oE '(href|src)="[^"#]*' "$page" | sed -E 's/^(href|src)="//' | grep -vE '^(https?:|mailto:)' || true); do
    [[ -z "$target" ]] && continue
    path="$dir/$target"
    [[ "$target" == */ || "$target" == "./" || "$target" == "../" ]] && path="$path/index.html"
    if [[ ! -e "$path" ]]; then
      echo "$name verlinkt $target, das gibt es nicht." >&2
      failed=1
    fi
  done
  for legal in impressum.html datenschutz.html; do
    if ! grep -q "href=\"\(\.\./\)*$legal\"" "$page"; then
      echo "$name verlinkt $legal nicht." >&2
      failed=1
    fi
  done
done < <(find "$site" -name '*.html' | sort)

for project in "$site"/projekte/*.html; do
  if ! grep -q "href=\"projekte/$(basename "$project")\"" "$site/index.html"; then
    echo "index.html stellt projekte/$(basename "$project") nicht vor." >&2
    failed=1
  fi
done

if [[ $failed -ne 0 ]]; then exit 1; fi
echo "Seite in Ordnung: $site"
