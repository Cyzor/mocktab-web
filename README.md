# mocktab-web

Source for [mocktab.org](https://mocktab.org) — the project website for **MockTab**, a native macOS driver that revives discontinued Wacom tablets on Apple Silicon and Intel Macs.

Plain HTML/CSS, no build step. Push to `main` and GitHub Pages serves it.

> **Status:** repo is private; Pages not yet enabled. The site goes live once the app and pages are both ready.

## Layout

```
index.html        Landing page
hardware.html     Supported tablets matrix
css/style.css     Styles
images/ui/        UI screenshots (light + dark variants)
images/compat/    App-compatibility reference shots
CNAME             mocktab.org
```

## Local preview

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

## App repo

The driver itself lives in [mocktab-app](https://github.com/Cyzor/mocktab-app) (internal name: `tablet-driver`).
