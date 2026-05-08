# mocktab-web

Source for [mocktab.org](https://mocktab.org) — the project website for **MockTab**, a native macOS driver for older Wacom tablets.

Plain HTML/CSS, no build step. Push to `main` and GitHub Pages serves it.

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
