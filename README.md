# mocktab-web

Source for [mocktab.org](https://mocktab.org) — the project website for **MockTab**, a native macOS driver that revives discontinued Wacom tablets on Apple Silicon and Intel Macs.

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

## App repo

The driver itself lives in [tablet-driver](https://github.com/cyzor/tablet-driver).
