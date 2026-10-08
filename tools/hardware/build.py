#!/usr/bin/env python3
"""
Rebuild the device tables in hardware.html from TabletKit's registry.

The registry supplies each device's name, pressure, button count, and
confidence. tools/hardware/devices.json supplies what it lacks: which table a
device belongs in, its year, its position among devices of the same year,
and any wording the page should use instead. Status always comes from the
registry. Prose outside the marked tables is left alone.

Usage (from the repo root):
  tools/hardware/build.py [--registry PATH] [--check]

--registry defaults to ../mocktab-app/TabletKit/registry.json.
--check changes nothing and exits 1 if the page is out of date or a
registry device has no table.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "hardware.html"
DATA = Path(__file__).with_name("devices.json")
DEFAULT_REGISTRY = ROOT.parent / "mocktab-app" / "TabletKit" / "registry.json"

STATUS = {"verified": "Works", "crossReferenced": "Likely works", "experimental": "Untested"}
SYMBOL = {"Works": "&#10003;", "Likely works": "&#8776;", "Untested": "&#8230;", "Out of scope": "&#8856;"}
BITS = {255: 8, 511: 9, 1023: 10, 2047: 11, 4095: 12, 8191: 13}


def pid_of(d):
    p = d["productID"]
    return p if isinstance(p, int) else int(p, 16)


def defaults(d):
    """Row values derived from a registry entry alone."""
    name = d["name"]
    bluetooth = "Bluetooth" in name or name.endswith(" BT")
    if name.startswith("Wacom "):
        name = name[len("Wacom "):]
    if bluetooth:
        name = name.replace(", Bluetooth", "").replace(" BT", "")
    p = d.get("maxPressure") or 0
    pressure = f"{p} ({BITS[p]}-bit)" if p in BITS else (str(p) if p else "—")
    b = d.get("buttonCount") or 0
    return {
        "name": name,
        "pressure": pressure,
        "buttons": f"{b} keys" if b else "—",
        "transport": "Bluetooth" if bluetooth else "USB",
        "status": "Out of scope" if d.get("outOfScope") else STATUS[d["confidence"]],
    }


def render_row(pid, rec, reg):
    row = defaults(reg) if reg else {"status": "Untested", "pressure": "—", "buttons": "—", "transport": "USB"}
    for k in ("name", "pressure", "buttons", "transport"):
        if k in rec:
            row[k] = rec[k]
    st = row["status"]
    pid_cell = rec.get("pidCell") or f"<code>{pid}</code>"
    e = html.escape
    return f"""                            <tr>
                                <td>
                                    <span class="visually-hidden"
                                        >{st}</span
                                    ><span aria-hidden="true">{SYMBOL[st]}</span>
                                </td>
                                <td>{e(row['name'], quote=False)}</td>
                                <td>{pid_cell}</td>
                                <td>{e(rec.get('year', '—'))}</td>
                                <td>{e(row['pressure'], quote=False)}</td>
                                <td>{e(row['buttons'], quote=False)}</td>
                                <td>{e(row['transport'], quote=False)}</td>
                            </tr>
"""


def build(page, data, registry):
    by_pid = {pid_of(d): d for d in registry}
    covered = set(data["exclude"])
    sections = {}
    for pid, rec in data["devices"].items():
        sections.setdefault(rec["section"], []).append(pid)
        covered.add(pid)
        covered.update(rec.get("also", []))
    unassigned = sorted(f"0x{p:04X}" for p in by_pid if f"0x{p:04X}" not in covered)

    def sort_key(pid):
        rec = data["devices"][pid]
        reg = by_pid.get(int(pid, 16))
        name = rec.get("name") or (defaults(reg)["name"] if reg else "")
        year = rec.get("year", "9999").lstrip("~")
        # Hand ordering within a year (S, M, L) wins; new devices sort by name.
        return (year, rec.get("order", 999), name.lower(), pid)

    def fill(m):
        slug = m.group(1)
        rows = "".join(
            render_row(pid, data["devices"][pid], by_pid.get(int(pid, 16)))
            for pid in sorted(sections.get(slug, []), key=sort_key))
        return f"<!-- hardware:{slug} -->\n{rows}<!-- /hardware:{slug} -->"

    new = re.sub(r"<!-- hardware:([a-z0-9-]+) -->.*?<!-- /hardware:\1 -->", fill, page, flags=re.S)
    missing = set(sections) - set(re.findall(r"<!-- hardware:([a-z0-9-]+) -->", page))
    return new, unassigned, sorted(missing)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not args.registry.exists():
        sys.exit(f"registry not found: {args.registry} (pass --registry)")
    registry = json.loads(args.registry.read_text())
    registry = registry if isinstance(registry, list) else registry["devices"]
    data = json.loads(DATA.read_text())
    page = PAGE.read_text()

    new, unassigned, missing = build(page, data, registry)
    problems = 0
    for pid in unassigned:
        name = next(d["name"] for d in registry if f"0x{pid_of(d):04X}" == pid)
        print(f"unassigned: {pid} {name} — add it to devices.json with a section, or to exclude")
        problems += 1
    for slug in missing:
        print(f"no table marked for section '{slug}' in hardware.html")
        problems += 1

    if args.check:
        if new != page:
            print("hardware.html is out of date; run tools/hardware/build.py")
            problems += 1
        sys.exit(1 if problems else 0)
    if new != page:
        PAGE.write_text(new)
        print("hardware.html updated")
    else:
        print("hardware.html already up to date")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
