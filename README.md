# mocktab-web

Source for [mocktab.org](https://mocktab.org) — the project website for **MockTab**, a macOS driver that revives discontinued Wacom tablets on Apple Silicon and Intel Macs.

Plain HTML/CSS, no build step. Push to `main` and GitHub Pages serves it.

## Layout

```
index.html         Landing page
guide.html         User guide
configuration.html App-compatibility reference
hardware.html      Supported tablets matrix
notes/index.html   Project notes
css/style.css      Styles
images/ui/         UI screenshots (light + dark variants)
images/config/     App-compatibility reference shots
CNAME              mocktab.org
robots.txt         Crawl directives
sitemap.xml        Sitemap for search engines
```

## Local preview

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

## Hardware list

The device tables in `hardware.html` are generated from TabletKit's
`registry.json`. Edit the prose around them by hand; for the tables, edit
`tools/hardware/devices.json` and run:

```sh
tools/hardware/build.py
```

`devices.json` assigns each device to a table and holds what the registry
lacks: year, position within that year, and any wording or status that should
differ from the registry's. A stored status is a floor; a later registry
upgrade still shows. New registry devices with no table are reported, not
guessed. `tools/hardware/build.py --check` exits 1 if the page is out of date.

The registry defaults to `../mocktab-app/TabletKit/registry.json`; pass
`--registry` to use another copy.

## App repo

The driver itself lives in [tablet-driver](https://github.com/Cyzor/tablet-driver).
