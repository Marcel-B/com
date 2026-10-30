#!/usr/bin/env python3
"""Builds marcelbenders.com from content/ and static/ into one folder (default _site).

content/projekte/<slug>/projekt.md         a project: front matter (see CONTRIBUTING.md) and its page as Markdown
content/projekte/<slug>/stand/<datum>.md   a status report ("Wasserstandsmeldung"), newest first on the project page
content/projekte/<slug>/anleitungen/*.md   tutorials of that project
content/seiten/*.md                        plain pages (Impressum, Datenschutz)
static/                                    copied as it is (styles, script, fonts, pictures, CNAME)

Every content error stops the build with the file's name, so a pull request with a broken file stays red.

    python3 scripts/build.py [folder]
"""

import datetime
import hashlib
import html
import json
import re
import shutil
import sys
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://marcelbenders.com"
AUTHOR = "Marcel Benders"
PERSON = {
    "@type": "Person",
    "@id": f"{SITE}/#person",
    "name": AUTHOR,
    "url": f"{SITE}/",
    "jobTitle": "Softwareentwickler",
    "address": {"@type": "PostalAddress", "addressLocality": "Krefeld", "addressCountry": "DE"},
    "sameAs": ["https://github.com/Marcel-B", "https://b-velop.com/", "https://tonwerk.studio/", "https://slipways.de/"],
}
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def asset(name):
    """The address of a file in static/ with a hash of its content, so a browser that cached the old one (GitHub Pages
    allows ten minutes) loads a changed style or script at once instead of mixing it with new markup."""
    digest = hashlib.sha256((ROOT / "static" / name).read_bytes()).hexdigest()[:10]
    return f"/{name}?v={digest}"


MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]


class ContentError(Exception):
    pass


def fail(path, message):
    raise ContentError(f"{path.relative_to(ROOT)}: {message}")


def read(path, required):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not match:
        fail(path, "Front Matter fehlt (die Datei muss mit --- beginnen und der Kopf mit --- enden)")
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as error:
        fail(path, f"Front Matter ist kein gültiges YAML: {error}")
    for key in required:
        if meta.get(key) in (None, "", []):
            fail(path, f"Feld '{key}' fehlt")
    return meta, match.group(2)


def render(text):
    return markdown.markdown(text, extensions=["extra", "sane_lists", "toc"], output_format="html")


def inline(text):
    return re.sub(r"^<p>(.*)</p>$", r"\1", render(str(text)).strip(), flags=re.S)


def date_of(path, value):
    if isinstance(value, datetime.date):
        return value
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError:
        fail(path, f"'{value}' ist kein Datum der Form JJJJ-MM-TT")


def german(day):
    return f"{day.day}. {MONTHS[day.month - 1]} {day.year}"


def e(text):
    return html.escape(str(text), quote=True)


# Content


def load():
    projects = []
    for folder in sorted((ROOT / "content/projekte").iterdir()):
        if not folder.is_dir():
            continue
        path = folder / "projekt.md"
        if not path.exists():
            fail(folder, "projekt.md fehlt")
        if not SLUG.match(folder.name):
            fail(folder, "Ordnername nur aus Kleinbuchstaben, Ziffern und Bindestrichen")
        meta, body = read(path, ["name", "untertitel", "kurz", "einleitung", "technik", "links"])
        repo = next((link["url"] for link in meta["links"] if "github.com/" in link.get("url", "")), None)
        project = dict(meta, slug=folder.name, body=body, repo=repo, reports=[], guides=[], url=f"/projekte/{folder.name}/")
        project.setdefault("reihenfolge", 1000)
        project.setdefault("steckbrief", [])

        for report_path in sorted((folder / "stand").glob("*.md")):
            m, b = read(report_path, ["titel"])
            day = date_of(report_path, m.get("datum") or report_path.stem[:10])
            lists = {key: [str(item) for item in (m.get(key) or [])] for key in ("fertig", "in_arbeit", "geplant")}
            if not any(lists.values()):
                fail(report_path, "mindestens eine der Listen 'fertig', 'in_arbeit', 'geplant' braucht einen Eintrag")
            slug = f"stand-{day.isoformat()}"
            if any(r["slug"] == slug for r in project["reports"]):
                fail(report_path, f"es gibt schon eine Meldung vom {day.isoformat()}")
            project["reports"].append(dict(m, **lists, date=day, body=b, slug=slug, project=project,
                                           url=f"/projekte/{folder.name}/{slug}.html"))
        project["reports"].sort(key=lambda r: r["date"], reverse=True)

        for guide_path in sorted((folder / "anleitungen").glob("*.md")):
            if not SLUG.match(guide_path.stem):
                fail(guide_path, "Dateiname nur aus Kleinbuchstaben, Ziffern und Bindestrichen")
            m, b = read(guide_path, ["titel", "beschreibung", "datum"])
            project["guides"].append(dict(m, date=date_of(guide_path, m["datum"]), body=b, slug=guide_path.stem,
                                          project=project, url=f"/projekte/{folder.name}/{guide_path.stem}.html"))
        project["guides"].sort(key=lambda g: (g.get("reihenfolge", 1000), g["titel"]))
        projects.append(project)
    projects.sort(key=lambda p: (p["reihenfolge"], p["name"]))

    pages = []
    for path in sorted((ROOT / "content/seiten").glob("*.md")):
        meta, body = read(path, ["titel", "beschreibung"])
        pages.append(dict(meta, body=body, url=f"/{path.stem}.html"))
    return projects, pages


# Layout


def layout(url, title, description, main, nav=None, jsonld=None, og_type="website", index=True):
    canonical = SITE + url
    ld = ""
    if jsonld:
        ld = f'\n  <script type="application/ld+json">\n{json.dumps(jsonld, ensure_ascii=False, indent=2)}\n  </script>'
    robots = "" if index else '\n  <meta name="robots" content="noindex">'

    def link(href, text, key):
        current = ' aria-current="page"' if nav == key else ""
        return f'<a href="{href}"{current}>{text}</a>'

    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">{robots}
  <meta name="author" content="{AUTHOR}">
  <meta name="theme-color" content="#0e1014">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{AUTHOR}">
  <meta property="og:locale" content="de_DE">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="/fonts/ubuntu/ubuntu-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{asset('style.css')}">
  <link rel="alternate" type="application/atom+xml" title="Neues von Marcel Benders" href="/feed.xml">{ld}
  <script src="{asset('main.js')}" defer></script>
</head>
<body>
  <a class="skip" href="#inhalt">Zum Inhalt</a>
  <header class="top">
    <div class="wrap">
      <a class="brand" href="/"><span class="brand-mark" aria-hidden="true">M</span>Marcel Benders</a>
      <nav aria-label="Hauptnavigation">
        {link("/#projekte", "Projekte", "projekte")}
        {link("/wasserstand.html", "Wasserstand", "wasserstand")}
        {link("/anleitungen.html", "Anleitungen", "anleitungen")}
        <a href="https://github.com/Marcel-B">GitHub</a>
      </nav>
    </div>
  </header>

  <main id="inhalt">
{main}
  </main>

  <footer class="foot">
    <div class="wrap">
      <span>© {datetime.date.today().year} Marcel Benders</span>
      <nav aria-label="Rechtliches">
        <a href="/impressum.html">Impressum</a>
        <a href="/datenschutz.html">Datenschutz</a>
        <a href="/feed.xml">Feed</a>
        <a href="https://github.com/Marcel-B/com">Quelltext dieser Seite</a>
      </nav>
    </div>
  </footer>
</body>
</html>
"""


def level(report):
    done, doing, planned = (len(report[k]) for k in ("fertig", "in_arbeit", "geplant"))
    return round(100 * (done + 0.5 * doing) / (done + doing + planned))


def gauge(report, small=False):
    percent = level(report)
    css = "gauge small" if small else "gauge"
    return (f'<div class="{css}" role="img" aria-label="Wasserstand {percent} Prozent">'
            f'<div class="water" style="--level:{percent}%"></div><span>{percent}&nbsp;%</span></div>')


def report_lists(report):
    columns = []
    for key, label in (("fertig", "Fertig"), ("in_arbeit", "In Arbeit"), ("geplant", "Geplant")):
        if report[key]:
            items = "".join(f"<li>{inline(item)}</li>" for item in report[key])
            columns.append(f'<div class="lane {key}"><h3>{label}</h3><ul>{items}</ul></div>')
    return f'<div class="lanes">{"".join(columns)}</div>'


def report_card(report, with_project=False):
    project = report["project"]
    who = f'<a class="eyebrow" href="{project["url"]}">{e(project["name"])}</a>' if with_project else ""
    summary = f'<p>{inline(report["zusammenfassung"])}</p>' if report.get("zusammenfassung") else ""
    return f"""      <article class="report reveal">
        {gauge(report, small=True)}
        <div>
          {who}
          <h3><a href="{report["url"]}">{e(report["titel"])}</a></h3>
          <p class="date"><time datetime="{report["date"].isoformat()}">{german(report["date"])}</time></p>
          {summary}
        </div>
      </article>"""


def guide_item(guide, with_project=False):
    who = f'<span class="eyebrow">{e(guide["project"]["name"])}</span>' if with_project else ""
    return f"""      <a class="guide reveal" href="{guide["url"]}">
        {who}
        <h3>{e(guide["titel"])}</h3>
        <p>{e(guide["beschreibung"])}</p>
      </a>"""


def breadcrumb(*items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + url} for i, (name, url) in enumerate(items)]}


# Pages


def project_page(project):
    links = "\n".join(f'      <li><a href="{e(l["url"])}">{e(l["text"])}</a></li>' for l in project["links"])
    facts = "".join(f'<dt>{e(f["name"])}</dt><dd>{inline(f["wert"])}</dd>' for f in project["steckbrief"])
    status = ""
    if project["reports"]:
        latest = project["reports"][0]
        older = "".join(f'<li><a href="{r["url"]}">{e(r["titel"])}</a> · {german(r["date"])}</li>' for r in project["reports"][1:])
        older = f'<h3>Frühere Meldungen</h3><ul class="plain">{older}</ul>' if older else ""
        status = f"""
    <section class="status reveal" id="wasserstand">
      <div class="status-head">
        {gauge(latest)}
        <div>
          <h2>Wasserstand</h2>
          <p class="date">Stand <time datetime="{latest["date"].isoformat()}">{german(latest["date"])}</time> · <a href="{latest["url"]}">{e(latest["titel"])}</a></p>
        </div>
      </div>
      {report_lists(latest)}
      {older}
    </section>"""
    guides = ""
    if project["guides"]:
        guides = f"""
    <section id="anleitungen">
      <h2>Anleitungen</h2>
      <div class="guides">
{chr(10).join(guide_item(g) for g in project["guides"])}
      </div>
    </section>"""
    main = f"""  <article class="wrap page">
    <a class="back" href="/#projekte">← Alle Projekte</a>
    <p class="eyebrow">{e(project["untertitel"])}</p>
    <h1>{e(project["name"])}</h1>
    <p class="lead">{e(project["einleitung"])}</p>
    <ul class="links">
{links}
    </ul>{status}
    <div class="prose">
{render(project["body"])}
    </div>{guides}
    <h2>Steckbrief</h2>
    <dl class="facts"><dt>Technik</dt><dd>{e(", ".join(project["technik"]))}</dd>{facts}</dl>
  </article>"""
    graph = [{"@type": "SoftwareSourceCode", "name": project["name"], "description": project["kurz"], "url": SITE + project["url"],
              "codeRepository": project["repo"], "keywords": ", ".join(project["technik"]), "inLanguage": "de",
              "author": {"@id": PERSON["@id"]}}]
    if project.get("app"):
        app = project["app"]
        entry = {"@type": "SoftwareApplication", "name": project["name"], "description": project["kurz"],
                 "url": app.get("url", SITE + project["url"]), "applicationCategory": app.get("kategorie", "Application"),
                 "operatingSystem": app.get("plattformen", ""), "author": {"@id": PERSON["@id"]}}
        if app.get("kostenlos"):
            entry["offers"] = {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}
        if app.get("store"):
            entry["downloadUrl"] = app["store"]
        graph.append(entry)
    graph += [breadcrumb(("Projekte", "/"), (project["name"], project["url"])), PERSON]
    return layout(project["url"], f'{project["name"]}: {project["untertitel"]} · {AUTHOR}', project["kurz"], main,
                  nav="projekte", jsonld={"@context": "https://schema.org", "@graph": graph}, og_type="article")


def report_page(report):
    project = report["project"]
    summary = report.get("zusammenfassung") or f'Wie weit {project["name"]} ist: was fertig ist, woran gearbeitet wird und was geplant ist.'
    title = f'{report["titel"]} · Wasserstand {project["name"]}'
    main = f"""  <article class="wrap page">
    <a class="back" href="{project["url"]}">← {e(project["name"])}</a>
    <p class="eyebrow">Wasserstandsmeldung · <time datetime="{report["date"].isoformat()}">{german(report["date"])}</time></p>
    <h1>{e(report["titel"])}</h1>
    <div class="status-head">{gauge(report)}<p class="lead">{inline(summary)}</p></div>
    {report_lists(report)}
    <div class="prose">
{render(report["body"])}
    </div>
  </article>"""
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": report["titel"], "description": summary, "datePublished": report["date"].isoformat(),
         "inLanguage": "de", "url": SITE + report["url"], "author": {"@id": PERSON["@id"]}, "about": project["name"]},
        breadcrumb(("Projekte", "/"), (project["name"], project["url"]), (report["titel"], report["url"])), PERSON]}
    return layout(report["url"], f"{title} · {AUTHOR}", summary, main, nav="wasserstand", jsonld=ld, og_type="article")


def guide_page(guide):
    project = guide["project"]
    updated = guide.get("aktualisiert")
    meta = f'<time datetime="{guide["date"].isoformat()}">{german(guide["date"])}</time>'
    if updated:
        meta += f' · aktualisiert <time datetime="{date_of(ROOT, updated).isoformat()}">{german(date_of(ROOT, updated))}</time>'
    main = f"""  <article class="wrap page">
    <a class="back" href="{project["url"]}">← {e(project["name"])}</a>
    <p class="eyebrow">Anleitung · {meta}</p>
    <h1>{e(guide["titel"])}</h1>
    <p class="lead">{e(guide["beschreibung"])}</p>
    <div class="prose">
{render(guide["body"])}
    </div>
  </article>"""
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "TechArticle", "headline": guide["titel"], "description": guide["beschreibung"], "datePublished": guide["date"].isoformat(),
         "dateModified": (date_of(ROOT, updated) if updated else guide["date"]).isoformat(), "inLanguage": "de",
         "url": SITE + guide["url"], "author": {"@id": PERSON["@id"]}, "about": project["name"]},
        breadcrumb(("Projekte", "/"), (project["name"], project["url"]), (guide["titel"], guide["url"])), PERSON]}
    return layout(guide["url"], f'{guide["titel"]} · {project["name"]} · {AUTHOR}', guide["beschreibung"], main,
                  nav="anleitungen", jsonld=ld, og_type="article")


def home(projects, reports, guides):
    cards = []
    for p in projects:
        tags = "".join(f"<li>{e(t)}</li>" for t in p["technik"])
        badge = ""
        if p["reports"]:
            r = p["reports"][0]
            badge = f'<span class="badge" title="Wasserstand vom {german(r["date"])}"><i style="--level:{level(r)}%"></i>{level(r)}&nbsp;%</span>'
        cards.append(f"""      <a class="card reveal" href="{p["url"]}">
        <div class="card-top"><h3>{e(p["name"])}</h3>{badge}</div>
        <p class="what">{e(p["untertitel"])}</p>
        <p>{e(p["kurz"])}</p>
        <ul class="tags">{tags}</ul>
        <span class="more">Mehr erfahren <span aria-hidden="true">→</span></span>
      </a>""")
    news = ""
    if reports:
        news = f"""
    <section class="wrap" id="neu">
      <h2 class="section">Neueste Wasserstandsmeldungen</h2>
      <div class="reports">
{chr(10).join(report_card(r, with_project=True) for r in reports[:4])}
      </div>
      <p class="all"><a href="/wasserstand.html">Alle Meldungen</a></p>
    </section>"""
    tutorials = ""
    if guides:
        tutorials = f"""
    <section class="wrap">
      <h2 class="section">Anleitungen</h2>
      <div class="guides">
{chr(10).join(guide_item(g, with_project=True) for g in guides[:6])}
      </div>
      <p class="all"><a href="/anleitungen.html">Alle Anleitungen</a></p>
    </section>"""
    main = f"""    <div class="hero">
      <div class="hero-bg" aria-hidden="true"><span></span><span></span><span></span></div>
      <div class="wrap">
        <p class="eyebrow">Softwareentwickler aus Krefeld</p>
        <h1>Marcel <span class="accent">Benders</span></h1>
        <p class="lead">Hier stehen die Projekte, an denen ich in meiner freien Zeit baue: Musik, Werkstatt, Wasser und Heimnetz. Zu jedem gibt es einen Wasserstand, wie weit es ist, und Anleitungen, wie du es selbst aufsetzt und nutzt. Fast alles mit Quelltext auf GitHub.</p>
        <div class="actions">
          <a class="button" href="#projekte">Projekte ansehen</a>
          <a class="button ghost" href="https://github.com/Marcel-B">GitHub</a>
        </div>
      </div>
    </div>

    <section class="wrap" id="projekte">
      <h2 class="section">Projekte</h2>
      <div class="grid">
{chr(10).join(cards)}
      </div>
    </section>{news}{tutorials}

    <section class="wrap">
      <h2 class="section">Außerdem</h2>
      <ul class="also">
        <li><a href="https://b-velop.com/">b-velop.com</a>: freiberufliche Softwareentwicklung.</li>
      </ul>
    </section>"""
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": f"{SITE}/#site", "url": f"{SITE}/", "name": AUTHOR, "inLanguage": "de", "publisher": {"@id": PERSON["@id"]}},
        PERSON,
        {"@type": "ItemList", "name": "Projekte", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": SITE + p["url"], "name": p["name"]} for i, p in enumerate(projects)]}]}
    names = ", ".join(p["name"] for p in projects[:6])
    return layout("/", f"{AUTHOR}: Softwareentwickler und seine Projekte",
                  f"Marcel Benders, Softwareentwickler aus Krefeld: Projekte wie {names}, mit Wasserstand, Anleitungen und Quelltext auf GitHub.",
                  main, jsonld=ld)


def list_page(url, title, lead, description, body, nav):
    main = f"""  <div class="wrap page wide">
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
{body}
  </div>"""
    return layout(url, f"{title} · {AUTHOR}", description, main, nav=nav)


def feed(reports, guides):
    entries = sorted([(r["date"], r["titel"] + " · " + r["project"]["name"], r["url"], r.get("zusammenfassung") or "Wasserstandsmeldung") for r in reports] +
                     [(g["date"], g["titel"] + " · " + g["project"]["name"], g["url"], g["beschreibung"]) for g in guides], reverse=True)
    updated = (entries[0][0] if entries else datetime.date.today()).isoformat()
    items = "".join(f"""  <entry>
    <title>{e(title)}</title>
    <link href="{SITE}{url}"/>
    <id>{SITE}{url}</id>
    <updated>{day.isoformat()}T00:00:00Z</updated>
    <summary>{e(summary)}</summary>
  </entry>
""" for day, title, url, summary in entries[:30])
    return f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="de">
  <title>Marcel Benders: Wasserstand und Anleitungen</title>
  <link href="{SITE}/"/>
  <link rel="self" href="{SITE}/feed.xml"/>
  <id>{SITE}/</id>
  <updated>{updated}T00:00:00Z</updated>
  <author><name>{AUTHOR}</name></author>
{items}</feed>
"""


def build(out):
    projects, pages = load()
    reports = sorted((r for p in projects for r in p["reports"]), key=lambda r: r["date"], reverse=True)
    guides = sorted((g for p in projects for g in p["guides"]), key=lambda g: g["date"], reverse=True)

    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(ROOT / "static", out)
    files = {}

    def write(url, text, sitemap=True):
        path = out / (url.lstrip("/") + ("index.html" if url.endswith("/") else ""))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        if sitemap:
            files[url] = text

    write("/", home(projects, reports, guides))
    for p in projects:
        write(p["url"], project_page(p))
        for r in p["reports"]:
            write(r["url"], report_page(r))
        for g in p["guides"]:
            write(g["url"], guide_page(g))

    if reports:
        body = "      <div class=\"reports\">\n" + "\n".join(report_card(r, with_project=True) for r in reports) + "\n      </div>"
    else:
        body = '      <p class="empty">Noch keine Meldungen.</p>'
    write("/wasserstand.html", list_page("/wasserstand.html", "Wasserstand",
          "Wie weit die Projekte sind: was fertig ist, woran ich gerade arbeite und was als Nächstes kommt. Der Pegel zeigt den Anteil des Erledigten.",
          "Wasserstandsmeldungen zu Marcel Benders' Projekten: was fertig ist, woran gearbeitet wird und was geplant ist.", body, "wasserstand"))
    if guides:
        body = "      <div class=\"guides\">\n" + "\n".join(guide_item(g, with_project=True) for g in guides) + "\n      </div>"
    else:
        body = '      <p class="empty">Noch keine Anleitungen.</p>'
    write("/anleitungen.html", list_page("/anleitungen.html", "Anleitungen",
          "Wie du die Projekte selbst aufsetzt und nutzt, Schritt für Schritt.",
          "Anleitungen zu Marcel Benders' Projekten: einrichten, betreiben und nutzen.", body, "anleitungen"))

    for page in pages:
        main = f'  <article class="wrap page">\n    <h1>{e(page["titel"])}</h1>\n    <div class="prose">\n{render(page["body"])}\n    </div>\n  </article>'
        write(page["url"], layout(page["url"], f'{page["titel"]} · {AUTHOR}', page["beschreibung"], main))

    notfound = """  <div class="wrap page">
    <h1>Seite nicht gefunden</h1>
    <p class="lead">Diese Adresse gibt es hier nicht (mehr).</p>
    <p><a class="button" href="/">Zur Startseite mit allen Projekten</a></p>
  </div>"""
    write("/404.html", layout("/404.html", f"Seite nicht gefunden · {AUTHOR}", "Diese Seite gibt es auf marcelbenders.com nicht.",
                              notfound, index=False), sitemap=False)

    (out / "feed.xml").write_text(feed(reports, guides), encoding="utf-8")
    today = datetime.date.today().isoformat()
    urls = "".join(f"  <url><loc>{SITE}{url}</loc><lastmod>{today}</lastmod></url>\n" for url in files)
    (out / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"{len(projects)} Projekte, {len(reports)} Meldungen, {len(guides)} Anleitungen nach {out}")


if __name__ == "__main__":
    try:
        build(Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "_site")
    except ContentError as error:
        print(f"Fehler: {error}", file=sys.stderr)
        sys.exit(1)
