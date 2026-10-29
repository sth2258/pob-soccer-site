#!/usr/bin/env python3
"""Build the POBSC site.

Each file in src/pages/ is an HTML fragment that starts with a comment block:

    <!--
    title: Club By-Laws
    lead: Optional one-line intro shown under the page title
    layout: page            (or "home" for index.html)
    -->

This script wraps every fragment in the shared header, navigation and footer
and writes the finished page to the repository root (where GitHub Pages serves
it). Run it after editing anything in src/:

    python3 build.py
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src" / "pages"

# Site navigation: (menu label, [(page name, link text), ...]).
# A page's section (for breadcrumbs and the sidebar) is the menu it's listed under.
NAV = [
    ("Programs", [
        ("register", "Registration"),
        ("intramural", "Intramural & Little Nuggets"),
        ("schedule", "Intramural Schedule & Locations"),
        ("participation-rules", "Participation Rules & Guidelines"),
        ("u9-u10-rules", "U9/U10 Rules"),
        ("topsoccer", "TOPSoccer"),
        ("topsoccer-schedule", "TOPSoccer Schedule"),
    ]),
    ("Travel", [
        ("travel-tryouts", "Club-Led Tryout Q&A"),
        ("travel-uniforms", "Travel Uniform Ordering"),
        ("player-pass", "Player Pass Information"),
    ]),
    ("Referees", [
        ("referees", "Referee Program"),
        ("referee-pre-game", "Pre-Game Responsibilities"),
        ("referee-first-impression", "Making a Good First Impression"),
    ]),
    ("Club", [
        ("officials", "Club Officials"),
        ("by-laws", "Club By-Laws"),
        ("policies", "Policies & Procedures"),
        ("code-of-conduct", "Code of Conduct"),
        ("zero-tolerance", "Zero Tolerance Policy"),
        ("concussion", "U.S. Soccer Concussion Initiative"),
        ("sponsorship", "Sponsorship"),
    ]),
    ("Info", [
        ("news", "News"),
        ("fields", "Field Locations"),
        ("forms", "Online Forms"),
        ("contact", "Contact Us"),
    ]),
]
SECTION_OF = {name: label for label, items in NAV for name, _ in items}

LOGO = """<a id="logo"{cls} href="{href}" aria-label="Plainview–Old Bethpage Soccer Club home">
  <div class="inner"><img src="assets/pobsc-shield.png" alt="" draggable="false"></div>
</a>"""


def cur(n, current):
    return ' aria-current="page"' if n == current else ""


def esc(s):
    return html.escape(s, quote=True)


def parse(path):
    text = path.read_text()
    m = re.match(r"<!--\n(.*?)\n-->\n", text, re.S)
    if not m:
        raise SystemExit(f"{path}: missing <!-- title: ... --> header")
    meta = dict(
        (k.strip(), v.strip())
        for k, v in (line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
    )
    return meta, text[m.end():]


def nav_html(current):
    out = []
    for label, items in NAV:
        active = " active" if SECTION_OF.get(current) == label else ""
        links = "".join(
            f'<a href="{n}.html"{cur(n, current)}>{esc(t)}</a>'
            for n, t in items
        )
        out.append(
            f'<div class="nav-item{active}"><button class="nav-top" aria-expanded="false">{label}</button>'
            f'<div class="dropdown">{links}</div></div>'
        )
    out.append('<a class="btn" href="register.html">Register</a>')
    return "\n    ".join(out)


def header(current, home):
    brand_cls = "" if home else " show"
    return f"""<header id="header"{'' if home else ' class="solid"'}>
  <a class="brand{brand_cls}" id="brand" href="index.html">
    <b>Plainview–Old Bethpage</b>
    <span>Soccer Club</span>
  </a>
  <nav id="nav"{'' if home else ' class="show"'} aria-label="Main">
    {nav_html(current)}
  </nav>
  <button class="menu-btn" id="menuBtn" aria-label="Open menu" aria-expanded="false">☰</button>
</header>"""


def footer():
    cols = "".join(
        f'<div><h4>{label}</h4>' + "".join(f'<a href="{n}.html">{esc(t)}</a>' for n, t in items) + "</div>"
        for label, items in NAV
    )
    return f"""<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <h4>POB Soccer Club</h4>
        <p style="line-height:1.6;margin:0">Promoting and developing youth soccer in Plainview–Old Bethpage since 1974.<br>P.O. Box 212, Old Bethpage, NY 11804<br><a href="mailto:contact@pobsc.com" style="display:inline">contact@pobsc.com</a></p>
      </div>
      {cols}
    </div>
    <div class="legal"><span>© 2026 Plainview–Old Bethpage Soccer Club · 501(c)(3) non-profit</span><span>Prototype</span></div>
  </div>
</footer>"""


def page_body(name, meta, content):
    section = SECTION_OF.get(name)
    crumbs = '<a href="index.html">Home</a>'
    if section:
        crumbs += f" <span>/</span> {section}"
    lead = f'<p class="lead">{meta["lead"]}</p>' if meta.get("lead") else ""
    side = ""
    if section:
        items = dict(NAV)[section]
        links = "".join(
            f'<a href="{n}.html"{cur(n, name)}>{esc(t)}</a>' for n, t in items
        )
        side = f"""<aside class="side">
      <div class="side-box"><h4>{section}</h4>{links}</div>
      <div class="side-cta"><b>2026–27 registration is open</b><a class="btn" href="register.html">Register</a></div>
    </aside>"""
    return f"""<section class="page-hero">
  <div class="wrap">
    <div class="crumbs">{crumbs}</div>
    <h1>{esc(meta["title"])}</h1>
    {lead}
  </div>
</section>
<main class="page" id="top">
  <div class="wrap page-grid">
    <article class="prose">
{content.strip()}
    </article>
    {side}
  </div>
</main>"""


def render(name, meta, content):
    home = meta.get("layout") == "home"
    title = meta["title"] if home else f'{meta["title"]} · Plainview–Old Bethpage Soccer Club'
    desc = meta.get("description") or meta.get("lead") or (
        "Youth soccer for Plainview and Old Bethpage, New York, since 1974."
    )
    if home:
        top = '<div id="curtain"></div>\n<button class="skip-intro" id="skip">Skip intro</button>\n\n'
        top += LOGO.format(cls="", href="#top")
        body = content.strip()
        script = '<script src="assets/site.js"></script>\n<script src="assets/home.js"></script>'
    else:
        top = LOGO.format(cls=' class="static"', href="index.html")
        body = page_body(name, meta, content)
        script = '<script src="assets/site.js"></script>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(re.sub(r'<[^>]+>', '', desc))}">
<link rel="icon" href="assets/pobsc-shield.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body{' class="locked home"' if home else ''}>
<!-- Generated by build.py from src/pages/{name}.html — edit that file, not this one. -->

{top}

{header(name, home)}

{body}

{footer()}

{script}
</body>
</html>
"""


def main():
    names = []
    for path in sorted(SRC.glob("*.html")):
        meta, content = parse(path)
        (ROOT / path.name).write_text(render(path.stem, meta, content))
        names.append(path.stem)
    missing = [n for n in SECTION_OF if n not in names]
    if missing:
        print("warning: in NAV but no src page:", ", ".join(missing))
    print(f"built {len(names)} pages")


if __name__ == "__main__":
    main()
