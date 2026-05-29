#!/usr/bin/env bash
#
# Regenerate sitemap.xml from current file mtimes.
#
# Usage: ./tools/regen-sitemap.sh   (run from repo root)
#
# Each entry below names a public URL, the on-disk file it maps to, and
# its sitemap priority. `lastmod` comes from the file's mtime converted
# to UTC. Adding a new page means appending one line to `entries`.

set -euo pipefail

cd "$(dirname "$0")/.."

# loc | path-on-disk | priority
entries=(
    "https://mocktab.org/|index.html|1.00"
    "https://mocktab.org/hardware.html|hardware.html|0.80"
    "https://mocktab.org/configuration.html|configuration.html|0.80"
    "https://mocktab.org/guide.html|guide.html|0.80"
    "https://mocktab.org/notes/|notes/index.html|0.80"
)

{
    cat <<'HEADER'
<?xml version="1.0" encoding="UTF-8"?>
<urlset
      xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">

HEADER

    for entry in "${entries[@]}"; do
        IFS='|' read -r loc path priority <<<"$entry"
        if [[ ! -f $path ]]; then
            echo "regen-sitemap: missing file: $path" >&2
            exit 1
        fi
        epoch=$(stat -f '%m' "$path")
        lastmod=$(date -u -r "$epoch" +'%Y-%m-%dT%H:%M:%S+00:00')
        cat <<URL
<url>
  <loc>$loc</loc>
  <lastmod>$lastmod</lastmod>
  <priority>$priority</priority>
</url>
URL
    done

    echo "</urlset>"
} > sitemap.xml

echo "regen-sitemap: wrote sitemap.xml"
