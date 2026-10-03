# mocktab-web

Source for [mocktab.org](https://mocktab.org), the website for **MockTab**, a Mac driver that revives discontinued Wacom tablets.

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

## Hardware list

The device tables in `hardware.html` come from TabletKit's `registry.json`.
Edit the prose around them by hand. For the tables, edit
`tools/hardware/devices.json` and run:

```sh
tools/hardware/build.py
```

`devices.json` places each device in a table and holds what the registry
lacks: year, order within that year, and any wording or status that differs
from the registry. A stored status is a minimum, so a later registry upgrade
still shows. The script lists new registry devices that have no table rather
than guessing. `--check` exits 1 if the page is out of date.

By default the script reads `../mocktab-app/TabletKit/registry.json`. Pass
`--registry` to use another copy.

## App repo

The driver itself lives in [tablet-driver](https://github.com/Cyzor/tablet-driver).
