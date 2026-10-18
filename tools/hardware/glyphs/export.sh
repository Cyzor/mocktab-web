#!/bin/sh
# Compile the glyph exporter against the app's TabletFigure sources and write
# one SVG per family in devices.json into this folder, plus light and dark
# copies into images/hardware.
#
# Usage (from the repo root): tools/hardware/glyphs/export.sh [slug=0xPID ...]
# APP defaults to ../mocktab-app; OUT, to this folder; VARIANTS, to
# images/hardware.
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$DIR/../../.." && pwd)"
APP="${APP:-$ROOT/../mocktab-app}"
OUT="${OUT:-$DIR}"
VARIANTS="${VARIANTS:-$ROOT/images/hardware}"
AREA="$APP/MockTab/UI/Panes/TabletArea"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT

swiftc -O "$AREA/TabletFigure.swift" "$AREA/TabletLayoutTable.swift" \
    "$APP/MockTab/Settings/Model/TabletOrientation.swift" "$DIR/main.swift" -o "$T/export"
"$T/export" "$ROOT/tools/hardware/devices.json" "$APP/TabletKit/registry.json" "$OUT" "$VARIANTS" "$@"
