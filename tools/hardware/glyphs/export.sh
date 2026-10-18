#!/bin/sh
# Compile the glyph exporter against the app's TabletFigure sources and write
# one SVG per family in devices.json into this folder.
#
# Usage (from the repo root): tools/hardware/glyphs/export.sh [slug=0xPID ...]
# APP defaults to ../mocktab-app; OUT, to this folder.
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$DIR/../../.." && pwd)"
APP="${APP:-$ROOT/../mocktab-app}"
OUT="${OUT:-$DIR}"
AREA="$APP/MockTab/UI/Panes/TabletArea"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT

swiftc -O "$AREA/TabletFigure.swift" "$AREA/TabletLayoutTable.swift" \
    "$APP/MockTab/Settings/Model/TabletOrientation.swift" "$DIR/main.swift" -o "$T/export"
"$T/export" "$ROOT/tools/hardware/devices.json" "$APP/TabletKit/registry.json" "$OUT" "$@"
