# Mandelbrot-Python

Interactive Mandelbrot set viewer built with Flask. Users drag a selection box over the rendered image to zoom into any region. Deployed at https://fractal.rickapps.com.

## Project layout

```
scripts/
  main.py            # Flask routes
  mandelbrot.py      # Image generation class
  requirements.txt   # Pillow, numpy, flask, mpmath
  templates/
    index.html       # Bootstrap 4 UI with jQuery UI draggable selection box
  static/
    css/style.css
    js/custom.js     # Selection box drag logic, form submission, spinner
    js/jquery.ui.touch-punch.js  # Makes jQuery UI draggable work on touch screens
    img/mandelbrot.png           # Pre-rendered default image (served statically for speed)
jupyter/
  MandelbrotSet.ipynb  # Exploratory notebook
.venv/               # Local virtual environment (gitignored; create per machine)
```

## How to run locally

```bash
# First time on a machine (.venv is gitignored):
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt

cd scripts
source ../.venv/bin/activate
flask --app main run
```

`--app main` is needed because Flask only auto-discovers `app.py` or `wsgi.py`.

Set `GA_MEASUREMENT_ID` to enable the Google Analytics tag. Leave it unset locally; set it only on the production server.

## Architecture

### Image generation (`mandelbrot.py`)

The `Mandelbrot` class takes a center point `(xc, yc)` and a `domain` (width of the complex plane view) and renders a PNG, returned as a base64-encoded data URI — nothing is ever written to disk.

The iteration loop is vectorized with numpy. The core is a masked-array approach: `M` tracks which pixels haven't yet diverged, and only those pixels are updated each iteration. `I` records the escape iteration count per pixel for coloring.

**Precision:** `xc`, `yc`, and `domain` are stored as `mpmath.mpf` with `mp.dps = 30` (30 decimal places). All zoom arithmetic runs at that precision. Only at `makeImage()` time are coordinates converted to `float64` for numpy. This eliminates floating-point accumulation errors across successive zooms. Supports approximately 8 deep zooms comfortably; increase `mp.dps` if deeper zoom support is needed.

**Iteration scaling:** `self.iterations` is computed per-render in `setScale()` using `max(100, int(100 * log2(3.4 / domain + 1)))`. This scales logarithmically with zoom depth so boundary detail stays sharp — roughly doubling iterations for each halving of domain. The constant `3.4` is the initial domain.

**Color:** HSV color model. Escape iteration fraction maps to hue; saturation and brightness are class-level constants. Points inside the set are black.

### Session / zoom history (`main.py`)

Flask session stores parallel lists `xc[]`, `yc[]`, `domain[]` indexed by page number. Each zoom appends to these lists. The `/page/<num>` route allows back/forward navigation by reconstructing the `Mandelbrot` object from the stored parameters.

Session values are stored as plain Python `float` (not `mpf`) because Flask sessions serialize to JSON. Precision is sufficient for session storage since the mpmath-computed result is already the best achievable float64 approximation.

### Zoom flow

1. User drags the selection box in the browser
2. On submit, `custom.js` populates hidden form fields: `xtopLeft`, `ytopLeft`, `xcenter`, `ycenter`. The image scales with the screen (responsive CSS, max 720px wide, 4:3), so the selection box position is converted to pixels of the full size 720x540 image. y is measured from the bottom of the image, negative going up
3. POST to `/` — `main.py` reads the previous center/domain from the form, constructs `Mandelbrot`, calls `zoom()`, then `makeImage()`
4. New base64 image and updated center/domain are passed to the template as the next state

Note: `ycenter` increases downward in pixel space but the Mandelbrot y-axis increases upward, so `yScale` is negated in `setScale()`.

## Deployment

Self-hosted at https://fractal.rickapps.com. Live files are at `/home/rickapps/NASDrive/vhosts/mandelbrot`, which is **not** a git checkout: it holds the contents of `scripts/` copied in flat (no `scripts/` directory), with its own `.venv`. Deploy by copying `scripts/*` there, installing requirements into that `.venv`, and making sure `GA_MEASUREMENT_ID` is set in the server environment.

Earlier deployments (PythonAnywhere, Google Cloud) are retired.

## Git

Always use signed commits (`git commit -S`). Each development machine (desktop, laptop) has its own GPG key set as `user.signingkey` in its global git config, so commits may be signed by different keys.

## Known limitations / future work

- Touch screen double-click to submit does not work (noted in `custom.js`); mouse double-click works fine
- The template notes precision degrades with repeated zoom — this is now partially mitigated by mpmath but numpy float64 is still the bottleneck beyond ~48 zoom halvings
- No tests; behavior is verified manually in the browser
