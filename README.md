# Plainview–Old Bethpage Soccer Club website

Static site served by GitHub Pages at https://sth2258.github.io/pob-soccer-site/.

## Editing

Page content lives in `src/pages/` — one HTML fragment per page. Edit the fragment, then rebuild:

```bash
python3 build.py
```

`build.py` wraps each fragment in the shared header, menus and footer and writes the finished pages to the repo root. Commit both the fragment and the generated page, then push; GitHub Pages redeploys in a minute or two.

- **Menus / adding a page:** create `src/pages/<name>.html` and add it to `NAV` in `build.py`.
- **Styles:** `assets/site.css`. **Home page intro animation:** `assets/home.js`.
- **Documents and images:** `assets/docs/` and `assets/img/`.

## Preview locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.
