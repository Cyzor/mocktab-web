#!/bin/bash
# Copies the release and snapshot disk images that latest.json lists with
# a sha256 from GitHub releases into <site>/download/, and points the
# published latest.json at the copy. An entry without a checksum keeps its GitHub address. A copy
# that doesn't match its checksum stops the deploy, so the live site stays
# as it was.
#
# Each image sits under its checksum, so a cached old copy can never
# answer for a new one.
#
#   mirror-downloads.sh <site-dir>
set -euo pipefail

SITE=${1:?site directory}
FEED=$SITE/latest.json
SOURCE=https://github.com/Cyzor/tablet-driver/releases/download/
BASE=https://mocktab.org/download/

sha256() { if command -v sha256sum >/dev/null; then sha256sum "$1"; else shasum -a 256 "$1"; fi | cut -d' ' -f1; }

[[ -f $FEED ]] || { echo "no $FEED" >&2; exit 1; }
feed=$(cat "$FEED")
tmp=$(mktemp -d)
trap '/bin/rm -rf "$tmp"' EXIT

for entry in release snapshot; do
    path="[\"$entry\"]"
    url=$(jq -r --argjson p "$path" 'getpath($p).url // empty' <<<"$feed")
    sum=$(jq -r --argjson p "$path" 'getpath($p).sha256 // empty' <<<"$feed")
    if [[ -z $sum || $url != "$SOURCE"* ]]; then
        echo "$path: kept $url"
        continue
    fi
    [[ $sum =~ ^[0-9a-f]{64}$ ]] || { echo "$path: unreadable sha256" >&2; exit 1; }
    name=${url##*/}
    dest=download/${sum:0:16}/$name
    if [[ ! -f $SITE/$dest ]]; then
        curl -fsSL --retry 3 -o "$tmp/$name" "$url"
        got=$(sha256 "$tmp/$name")
        [[ $got == "$sum" ]] || { echo "$path: $url has sha256 $got, feed says $sum" >&2; exit 1; }
        mkdir -p "$SITE/${dest%/*}"
        mv "$tmp/$name" "$SITE/$dest"
    fi
    feed=$(jq --argjson p "$path" --arg u "$BASE${dest#download/}" 'setpath($p + ["url"]; $u)' <<<"$feed")
    echo "$path: $BASE${dest#download/}"
done

printf '%s\n' "$feed" > "$FEED"
