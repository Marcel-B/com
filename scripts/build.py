#!/usr/bin/env python3
"""Builds marcelbenders.com from content/ and static/ into one folder (default _site), in German at / and in English
under /en/.

content/projekte/<slug>/projekt.md            a project: front matter (see CONTRIBUTING.md) and more of its page as Markdown
content/projekte/<slug>/projekt.en.md         the same in English (required)
content/projekte/<slug>/stand/<datum>.md      a status report ("Wasserstandsmeldung"), newest first on the project page
content/projekte/<slug>/stand/<datum>.en.md   its English version (optional)
content/projekte/<slug>/anleitungen/*.md      tutorials of that project, English beside them as <name>.en.md (optional)
content/seiten/*.md, *.en.md                  plain pages (Impressum, Datenschutz), both languages
content/links.yml                             proper names (tools, products) linked where they first appear in a page's text
static/                                       copied as it is (styles, script, fonts, pictures, CNAME)

An English page has the German one's path under /en/. A report or tutorial without an English version is listed on
the English pages in German, marked as such, and links to the German page.

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
from markdown.treeprocessors import Treeprocessor
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://marcelbenders.com"
AUTHOR = "Marcel Benders"
LANGS = ("de", "en")
PREFIX = {"de": "", "en": "/en"}
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MONTHS = {
    "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
}
LANES = ("fertig", "in_arbeit", "geplant")
PHASES = ("jetzt", "als_naechstes", "spaeter")

# Every text the templates write, in both languages. Content brings its own.
T = {
    "de": {
        "locale": "de_DE", "skip": "Zum Inhalt", "main_nav": "Hauptnavigation", "legal_nav": "Rechtliches",
        "projects": "Projekte", "status": "Wasserstand", "guides": "Anleitungen", "imprint": "Impressum",
        "privacy": "Datenschutz", "feed": "Feed", "source": "Quelltext dieser Seite", "switch": "English",
        "switch_title": "Diese Seite auf Englisch", "theme": "Farbschema", "system": "System", "light": "Hell", "dark": "Dunkel",
        "feed_title": "Neues von Marcel Benders", "feed_name": "Marcel Benders: Wasserstand und Anleitungen",
        "all_projects": "← Alle Projekte", "more": "Mehr erfahren", "gauge": "Wasserstand {p} Prozent",
        "gauge_of": "Wasserstand vom {d}", "fertig": "Fertig", "in_arbeit": "In Arbeit", "geplant": "Geplant",
        "earlier": "Frühere Meldungen", "as_of": "Stand", "features": "Funktionen", "roadmap": "Roadmap",
        "roadmap_lead": "Was als Nächstes kommt. Ein Plan, kein Versprechen.",
        "jetzt": "Jetzt", "als_naechstes": "Als Nächstes", "spaeter": "Später", "facts": "Steckbrief", "tech": "Technik",
        "report": "Wasserstandsmeldung", "guide": "Anleitung", "updated": "aktualisiert", "other_lang": "",
        "report_default": "Wie weit {n} ist: was fertig ist, woran gearbeitet wird und was geplant ist.",
        "newest_reports": "Neueste Wasserstandsmeldungen", "all_reports": "Alle Meldungen", "all_guides": "Alle Anleitungen",
        "also": "Außerdem", "also_text": '<a href="https://b-velop.com/">b-velop.com</a>: freiberufliche Softwareentwicklung.',
        "hero_eyebrow": "Softwareentwickler aus Krefeld",
        "hero_lead": "Hier stehen die Projekte, an denen ich in meiner freien Zeit baue: Musik, Werkstatt, Wasser und Heimnetz. "
                     "Zu jedem gibt es einen Wasserstand, wie weit es ist, und Anleitungen, wie du es selbst aufsetzt und nutzt. "
                     "Fast alles mit Quelltext auf GitHub.",
        "see_projects": "Projekte ansehen", "home_title": "Marcel Benders: Softwareentwickler und seine Projekte",
        "home_description": "Marcel Benders, Softwareentwickler aus Krefeld: Projekte wie {n}, mit Wasserstand, Anleitungen und Quelltext auf GitHub.",
        "job": "Softwareentwickler",
        "status_lead": "Wie weit die Projekte sind: was fertig ist, woran ich gerade arbeite und was als Nächstes kommt. Der Pegel zeigt den Anteil des Erledigten.",
        "status_description": "Wasserstandsmeldungen zu Marcel Benders' Projekten: was fertig ist, woran gearbeitet wird und was geplant ist.",
        "guides_lead": "Wie du die Projekte selbst aufsetzt und nutzt, Schritt für Schritt.",
        "guides_description": "Anleitungen zu Marcel Benders' Projekten: einrichten, betreiben und nutzen.",
        "no_reports": "Noch keine Meldungen.", "no_guides": "Noch keine Anleitungen.",
        "notfound": "Seite nicht gefunden", "notfound_lead": "Diese Adresse gibt es hier nicht (mehr).",
        "notfound_button": "Zur Startseite mit allen Projekten", "notfound_description": "Diese Seite gibt es auf marcelbenders.com nicht.",
        "ad": "Anzeige", "ad_title": "Partnerlink",
        "partner_note": "Mit „Anzeige“ markierte Links sind Partnerlinks: Kaufst du darüber etwas, bekomme ich eine kleine "
                        "Provision. Für dich ändert sich am Preis nichts, und was ich empfehle, hängt nicht davon ab. "
                        'Mehr dazu im <a href="/datenschutz.html#partnerlinks">Datenschutz</a>.',
    },
    "en": {
        "locale": "en_GB", "skip": "Skip to content", "main_nav": "Main navigation", "legal_nav": "Legal",
        "projects": "Projects", "status": "Water level", "guides": "Guides", "imprint": "Legal notice",
        "privacy": "Privacy", "feed": "Feed", "source": "Source of this site", "switch": "Deutsch",
        "switch_title": "This page in German", "theme": "Colour scheme", "system": "System", "light": "Light", "dark": "Dark",
        "feed_title": "News from Marcel Benders", "feed_name": "Marcel Benders: water levels and guides",
        "all_projects": "← All projects", "more": "Learn more", "gauge": "Water level {p} percent",
        "gauge_of": "Water level of {d}", "fertig": "Done", "in_arbeit": "In progress", "geplant": "Planned",
        "earlier": "Earlier reports", "as_of": "As of", "features": "Features", "roadmap": "Roadmap",
        "roadmap_lead": "What comes next. A plan, not a promise.",
        "jetzt": "Now", "als_naechstes": "Next", "spaeter": "Later", "facts": "Fact sheet", "tech": "Technology",
        "report": "Water level report", "guide": "Guide", "updated": "updated", "other_lang": "in German",
        "report_default": "How far {n} has come: what is done, what is being worked on and what is planned.",
        "newest_reports": "Latest water level reports", "all_reports": "All reports", "all_guides": "All guides",
        "also": "Also", "also_text": '<a href="https://b-velop.com/">b-velop.com</a>: freelance software development.',
        "hero_eyebrow": "Software developer from Krefeld, Germany",
        "hero_lead": "These are the projects I build in my spare time: music, workshop, water and home network. "
                     "Each one has a water level showing how far it has come, and guides on how to set it up and use it yourself. "
                     "Almost all of them with their source on GitHub.",
        "see_projects": "See the projects", "home_title": "Marcel Benders: software developer and his projects",
        "home_description": "Marcel Benders, software developer from Krefeld, Germany: projects like {n}, with water levels, guides and source code on GitHub.",
        "job": "Software developer",
        "status_lead": "How far the projects have come: what is done, what I am working on and what comes next. The gauge shows the share that is done.",
        "status_description": "Water level reports on Marcel Benders' projects: what is done, what is being worked on and what is planned.",
        "guides_lead": "How to set up and use the projects yourself, step by step.",
        "guides_description": "Guides to Marcel Benders' projects: set up, run and use them.",
        "no_reports": "No reports yet.", "no_guides": "No guides yet.",
        "notfound": "Page not found", "notfound_lead": "This address does not exist here (any more).",
        "notfound_button": "To the start page with all projects", "notfound_description": "This page does not exist on marcelbenders.com.",
        "ad": "ad", "ad_title": "Affiliate link",
        "partner_note": "Links marked “ad” are affiliate links: if you buy something through one, I receive a small commission. "
                        "The price stays the same for you, and it does not decide what I recommend. "
                        'More in the <a href="/en/datenschutz.html#partnerlinks">privacy notice</a>.',
    },
}


def person(lang):
    return {
        "@type": "Person",
        "@id": f"{SITE}/#person",
        "name": AUTHOR,
        "url": f"{SITE}/",
        "jobTitle": T[lang]["job"],
        "address": {"@type": "PostalAddress", "addressLocality": "Krefeld", "addressCountry": "DE"},
        "sameAs": ["https://github.com/Marcel-B", "https://b-velop.com/", "https://tonwerk.studio/", "https://slipways.de/"],
    }


def asset(name):
    """The address of a file in static/ with a hash of its content, so a browser that cached the old one (GitHub Pages
    allows ten minutes) loads a changed style or script at once instead of mixing it with new markup."""
    digest = hashlib.sha256((ROOT / "static" / name).read_bytes()).hexdigest()[:10]
    return f"/{name}?v={digest}"


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


def render(text, lang=None):
    """Markdown to HTML. With a language, the text is prose of a project, report or tutorial: the proper names from
    content/links.yml are linked where they first appear, and a page with an affiliate link says what that is."""
    if lang is None:
        return markdown.markdown(text, extensions=["extra", "sane_lists", "toc"], output_format="html")
    linker = NameLinker(lang)
    md = markdown.Markdown(extensions=["extra", "sane_lists", "toc"], output_format="html")
    md.treeprocessors.register(linker, "names", 5)  # after the inline patterns (20), so existing links are elements
    result = md.convert(text)
    if linker.partner:
        result += f'\n<p class="partner-note">{T[lang]["partner_note"]}</p>'
    return result


# Proper names (content/links.yml), loaded by load_names() before anything is rendered.
NAMES = []
NAME_PATTERN = None
NO_LINKS = {"a", "code", "pre", "kbd", "h1", "h2", "h3", "h4", "h5", "h6"}


def load_names():
    """The names to link: each entry has `name`, `url`, optionally `auch` (further spellings) and `partner: true` for an
    affiliate link, which is marked as an ad (and needs the privacy page's section on affiliate links)."""
    global NAMES, NAME_PATTERN
    path = ROOT / "content/links.yml"
    if not path.exists():
        return
    try:
        entries = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    except yaml.YAMLError as error:
        fail(path, f"kein gültiges YAML: {error}")
    if not isinstance(entries, list):
        fail(path, "muss eine Liste von Einträgen mit 'name' und 'url' sein")
    seen = {}
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict) or not entry.get("name") or not entry.get("url"):
            fail(path, f"Eintrag {i + 1} braucht 'name' und 'url'")
        if not re.match(r"^https://[^\s]+$", str(entry["url"])):
            fail(path, f"'{entry['name']}': die Adresse muss mit https:// beginnen")
        if set(entry) - {"name", "url", "auch", "partner"}:
            fail(path, f"'{entry['name']}' kennt nur name, url, auch und partner")
        spellings = [str(entry["name"])] + [str(n) for n in entry.get("auch") or []]
        for spelling in spellings:
            if spelling in seen:
                fail(path, f"'{spelling}' steht zweimal drin")
            seen[spelling] = entry
        entry["names"] = spellings
        entry["partner"] = entry.get("partner") is True
    if any(entry["partner"] for entry in entries):
        for privacy in ("datenschutz.md", "datenschutz.en.md"):
            if 'id="partnerlinks"' not in render((ROOT / "content/seiten" / privacy).read_text(encoding="utf-8")):
                fail(path, f"Partnerlinks brauchen in content/seiten/{privacy} einen Abschnitt '## … {{#partnerlinks}}'")
    NAMES = entries
    if seen:
        # Longest first, so "Docker Desktop" wins over "Docker". A name may be followed by a hyphen ("ESPHome-Datei").
        alternatives = "|".join(re.escape(n) for n in sorted(seen, key=len, reverse=True))
        NAME_PATTERN = (re.compile(rf"(?<![\w-])({alternatives})(?!\w)"), seen)


class NameLinker(Treeprocessor):
    """Links the first appearance of every known name in a page's text, outside code, headings and existing links. A
    name the text already links (by address or link text) is left alone."""

    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.partner = False

    def run(self, root):
        if NAME_PATTERN is None:
            return
        self.done = set()
        for a in root.iter("a"):
            href = (a.get("href") or "").rstrip("/")
            text = "".join(a.itertext())
            for entry in NAMES:
                if str(entry["url"]).rstrip("/") == href or text in entry["names"]:
                    self.done.add(entry["name"])
        self.walk(root)

    def walk(self, element):
        if element.text:
            element.text = self.link(element, element.text, 0)
        index = 0
        while index < len(element):
            child = element[index]
            if child.tag not in NO_LINKS:
                self.walk(child)
            index += 1
            if child.tail:
                before = len(element)
                child.tail = self.link(element, child.tail, index)
                index += len(element) - before

    def link(self, parent, text, index):
        """Links names in text that sits at position index of parent; returns what stays in front of the first link."""
        pattern, entries = NAME_PATTERN
        for match in pattern.finditer(text):
            entry = entries[match.group(1)]
            if entry["name"] in self.done:
                continue
            self.done.add(entry["name"])
            a = ElementTree.Element("a", {"href": str(entry["url"])})
            a.text = match.group(1)
            new = [a]
            if entry["partner"]:
                self.partner = True
                a.set("rel", "sponsored nofollow")
                mark = ElementTree.Element("small", {"class": "ad", "title": T[self.lang]["ad_title"]})
                mark.text = T[self.lang]["ad"]
                new.append(mark)
            for offset, item in enumerate(new):
                parent.insert(index + offset, item)
            new[-1].tail = (new[-1].tail or "") + self.link(parent, text[match.end():], index + len(new))
            return text[:match.start()]
        return text


def inline(text):
    return re.sub(r"^<p>(.*)</p>$", r"\1", render(str(text)).strip(), flags=re.S)


def date_of(path, value):
    if isinstance(value, datetime.date):
        return value
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError:
        fail(path, f"'{value}' ist kein Datum der Form JJJJ-MM-TT")


def day_text(day, lang):
    if lang == "en":
        return f"{day.day} {MONTHS['en'][day.month - 1]} {day.year}"
    return f"{day.day}. {MONTHS['de'][day.month - 1]} {day.year}"


def e(text):
    return html.escape(str(text), quote=True)


def at(lang, url):
    return PREFIX[lang] + url


def originals(folder):
    """The German files of a folder; their English versions sit beside them as <name>.en.md."""
    return [p for p in sorted(folder.glob("*.md")) if not p.name.endswith(".en.md")]


def english_of(path):
    other = path.with_name(path.stem + ".en.md")
    return other if other.exists() else None


# Content


def project_text(path, meta, body, german=None):
    """The texts of a project in one language. The English file translates them; anything that is not text
    (technology, order, app data) comes from the German one."""
    for key in ("features",):
        for i, feature in enumerate(meta[key]):
            if not isinstance(feature, dict) or not feature.get("titel") or not feature.get("wozu"):
                fail(path, f"Funktion {i + 1} braucht 'titel' und 'wozu'")
            if not isinstance(feature.get("verhalten") or [], list):
                fail(path, f"'verhalten' von Funktion {i + 1} muss eine Liste sein")
    roadmap = meta.get("roadmap") or {}
    if not isinstance(roadmap, dict) or set(roadmap) - set(PHASES):
        fail(path, f"'roadmap' kennt nur {', '.join(PHASES)}")
    if german is not None:
        if bool(german["roadmap"]) != bool(roadmap):
            fail(path, "die Roadmap muss in beiden Sprachen da sein oder in keiner")
        if len(meta["features"]) != len(german["features"]):
            fail(path, "hat nicht so viele Funktionen wie die deutsche Fassung")
    return {
        "untertitel": meta["untertitel"], "vision": meta["vision"], "kurz": meta["kurz"], "links": meta["links"],
        "features": meta["features"], "roadmap": {k: [str(i) for i in roadmap.get(k) or []] for k in PHASES if roadmap.get(k)},
        "steckbrief": meta.get("steckbrief") or [], "body": body,
    }


def load():
    projects = []
    required = ["name", "untertitel", "vision", "kurz", "technik", "links", "features"]
    for folder in sorted((ROOT / "content/projekte").iterdir()):
        if not folder.is_dir():
            continue
        path = folder / "projekt.md"
        if not path.exists():
            fail(folder, "projekt.md fehlt")
        if not SLUG.match(folder.name):
            fail(folder, "Ordnername nur aus Kleinbuchstaben, Ziffern und Bindestrichen")
        meta, body = read(path, required)
        de = project_text(path, meta, body)
        en_path = folder / "projekt.en.md"
        if not en_path.exists():
            fail(folder, "projekt.en.md fehlt (die englische Fassung)")
        en_meta, en_body = read(en_path, ["untertitel", "vision", "kurz", "links", "features"])
        en = project_text(en_path, en_meta, en_body, german=de)
        repo = next((link["url"] for link in meta["links"] if "github.com/" in link.get("url", "")), None)
        project = {"slug": folder.name, "name": meta["name"], "technik": meta["technik"], "app": meta.get("app"),
                   "reihenfolge": meta.get("reihenfolge", 1000), "repo": repo, "de": de, "en": en,
                   "reports": [], "guides": [], "path": f"/projekte/{folder.name}/"}

        for report_path in originals(folder / "stand"):
            m, b = read(report_path, ["titel"])
            day = date_of(report_path, m.get("datum") or report_path.stem[:10])
            slug = f"stand-{day.isoformat()}"
            if any(r["slug"] == slug for r in project["reports"]):
                fail(report_path, f"es gibt schon eine Meldung vom {day.isoformat()}")
            report = {"date": day, "slug": slug, "project": project, "path": f"/projekte/{folder.name}/{slug}.html",
                      "de": report_text(report_path, m, b), "en": None}
            other = english_of(report_path)
            if other:
                report["en"] = report_text(other, *read(other, ["titel"]))
            project["reports"].append(report)
        project["reports"].sort(key=lambda r: r["date"], reverse=True)

        for guide_path in originals(folder / "anleitungen"):
            if not SLUG.match(guide_path.stem):
                fail(guide_path, "Dateiname nur aus Kleinbuchstaben, Ziffern und Bindestrichen")
            m, b = read(guide_path, ["titel", "beschreibung", "datum"])
            guide = {"date": date_of(guide_path, m["datum"]), "updated": None, "slug": guide_path.stem, "project": project,
                     "path": f"/projekte/{folder.name}/{guide_path.stem}.html", "order": m.get("reihenfolge", 1000),
                     "de": {"titel": m["titel"], "beschreibung": m["beschreibung"], "body": b}, "en": None}
            if m.get("aktualisiert"):
                guide["updated"] = date_of(guide_path, m["aktualisiert"])
            other = english_of(guide_path)
            if other:
                em, eb = read(other, ["titel", "beschreibung"])
                guide["en"] = {"titel": em["titel"], "beschreibung": em["beschreibung"], "body": eb}
            project["guides"].append(guide)
        project["guides"].sort(key=lambda g: (g["order"], g["de"]["titel"]))
        projects.append(project)
    projects.sort(key=lambda p: (p["reihenfolge"], p["name"]))

    pages = []
    for path in originals(ROOT / "content/seiten"):
        meta, body = read(path, ["titel", "beschreibung"])
        other = english_of(path)
        if not other:
            fail(path, f"{path.stem}.en.md fehlt (die englische Fassung)")
        en_meta, en_body = read(other, ["titel", "beschreibung"])
        pages.append({"path": f"/{path.stem}.html", "de": dict(meta, body=body), "en": dict(en_meta, body=en_body)})
    return projects, pages


def report_text(path, meta, body):
    lists = {key: [str(item) for item in (meta.get(key) or [])] for key in LANES}
    if not any(lists.values()):
        fail(path, "mindestens eine der Listen 'fertig', 'in_arbeit', 'geplant' braucht einen Eintrag")
    return dict(lists, titel=meta["titel"], zusammenfassung=meta.get("zusammenfassung"), body=body)


def version(item, lang):
    """An item's texts in this language, else in German, with the language they are in and where they live."""
    if item[lang]:
        return item[lang], lang, at(lang, item["path"])
    return item["de"], "de", item["path"]


# Layout


THEME_SCRIPT = ('try{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")'
                'document.documentElement.dataset.theme=t}catch(e){}')


def layout(lang, path, title, description, main, nav=None, jsonld=None, og_type="website", index=True, alternates=LANGS):
    """One page. path is the address without the language prefix; alternates are the languages it exists in."""
    t = T[lang]
    url = at(lang, path)
    canonical = SITE + url
    ld = ""
    if jsonld:
        ld = f'\n  <script type="application/ld+json">\n{json.dumps(jsonld, ensure_ascii=False, indent=2)}\n  </script>'
    robots = "" if index else '\n  <meta name="robots" content="noindex">'
    hreflang = ""
    if index and len(alternates) > 1:
        hreflang = "".join(f'\n  <link rel="alternate" hreflang="{l}" href="{SITE}{at(l, path)}">' for l in alternates)
        hreflang += f'\n  <link rel="alternate" hreflang="x-default" href="{SITE}{path}">'
    other = "en" if lang == "de" else "de"
    switch_to = at(other, path) if other in alternates else at(other, "/")
    og_alt = T[other]["locale"]

    def link(href, text, key):
        current = ' aria-current="page"' if nav == key else ""
        return f'<a href="{href}"{current}>{text}</a>'

    def theme(value, icon):
        return (f'<button type="button" data-theme-choice="{value}" aria-pressed="false" title="{t[value]}">'
                f'<svg viewBox="0 0 24 24" aria-hidden="true">{icon}</svg><span class="visually-hidden">{t[value]}</span></button>')

    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">{robots}
  <meta name="author" content="{AUTHOR}">
  <meta name="theme-color" content="#f6f6f3" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0e1014" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{canonical}">{hreflang}
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{AUTHOR}">
  <meta property="og:locale" content="{t["locale"]}">
  <meta property="og:locale:alternate" content="{og_alt}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <script>{THEME_SCRIPT}</script>
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="/fonts/ubuntu/ubuntu-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{asset('style.css')}">
  <link rel="alternate" type="application/atom+xml" title="{t["feed_title"]}" href="{at(lang, "/feed.xml")}">{ld}
  <script src="{asset('main.js')}" defer></script>
</head>
<body>
  <a class="skip" href="#inhalt">{t["skip"]}</a>
  <header class="top">
    <div class="wrap">
      <a class="brand" href="{at(lang, "/")}"><span class="brand-mark" aria-hidden="true">M</span>Marcel Benders</a>
      <nav aria-label="{t["main_nav"]}">
        {link(at(lang, "/#projekte"), t["projects"], "projekte")}
        {link(at(lang, "/wasserstand.html"), t["status"], "wasserstand")}
        {link(at(lang, "/anleitungen.html"), t["guides"], "anleitungen")}
        <a href="https://github.com/Marcel-B">GitHub</a>
      </nav>
      <div class="tools">
        <a class="lang" href="{switch_to}" hreflang="{other}" lang="{other}" title="{t["switch_title"]}" aria-label="{t["switch"]}">{other.upper()}</a>
        <div class="theme" role="group" aria-label="{t["theme"]}" hidden>
          {theme("system", '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>')}
          {theme("light", '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>')}
          {theme("dark", '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>')}
        </div>
      </div>
    </div>
  </header>

  <main id="inhalt">
{main}
  </main>

  <footer class="foot">
    <div class="wrap">
      <span>© {datetime.date.today().year} Marcel Benders</span>
      <nav aria-label="{t["legal_nav"]}">
        <a href="{at(lang, "/impressum.html")}">{t["imprint"]}</a>
        <a href="{at(lang, "/datenschutz.html")}">{t["privacy"]}</a>
        <a href="{at(lang, "/feed.xml")}">{t["feed"]}</a>
        <a href="https://github.com/Marcel-B/com">{t["source"]}</a>
      </nav>
    </div>
  </footer>
</body>
</html>
"""


def level(text):
    done, doing, planned = (len(text[k]) for k in LANES)
    return round(100 * (done + 0.5 * doing) / (done + doing + planned))


def gauge(text, lang, small=False):
    percent = level(text)
    css = "gauge small" if small else "gauge"
    return (f'<div class="{css}" role="img" aria-label="{T[lang]["gauge"].format(p=percent)}">'
            f'<div class="water" style="--level:{percent}%"></div><span>{percent}&nbsp;%</span></div>')


def lanes(columns, lang, css="lanes"):
    """Columns of lists: (key, items) pairs, each list coloured by its key."""
    html_columns = []
    for key, items in columns:
        if items:
            entries = "".join(f"<li>{inline(item)}</li>" for item in items)
            html_columns.append(f'<div class="lane {key}"><h3>{T[lang][key]}</h3><ul>{entries}</ul></div>')
    return f'<div class="{css}">{"".join(html_columns)}</div>'


def foreign(text_lang, lang):
    """Marks an entry shown in another language than the page's."""
    if text_lang == lang:
        return ""
    return f' <span class="other-lang" lang="{lang}">({T[lang]["other_lang"]})</span>'


def report_card(report, lang, with_project=False):
    project = report["project"]
    text, text_lang, url = version(report, lang)
    who = f'<a class="eyebrow" href="{at(lang, project["path"])}">{e(project["name"])}</a>' if with_project else ""
    summary = f'<p lang="{text_lang}">{inline(text["zusammenfassung"])}</p>' if text.get("zusammenfassung") else ""
    return f"""      <article class="report reveal">
        {gauge(text, lang, small=True)}
        <div>
          {who}
          <h3><a href="{url}" lang="{text_lang}">{e(text["titel"])}</a>{foreign(text_lang, lang)}</h3>
          <p class="date"><time datetime="{report["date"].isoformat()}">{day_text(report["date"], lang)}</time></p>
          {summary}
        </div>
      </article>"""


def guide_item(guide, lang, with_project=False):
    text, text_lang, url = version(guide, lang)
    who = f'<span class="eyebrow">{e(guide["project"]["name"])}</span>' if with_project else ""
    return f"""      <a class="guide reveal" href="{url}">
        {who}
        <h3 lang="{text_lang}">{e(text["titel"])}{foreign(text_lang, lang)}</h3>
        <p lang="{text_lang}">{e(text["beschreibung"])}</p>
      </a>"""


def breadcrumb(lang, *items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + url} for i, (name, url) in enumerate(items)]}


# Pages


def features(project, lang):
    cards = []
    for feature in project[lang]["features"]:
        rules = "".join(f"<li>{inline(rule)}</li>" for rule in feature.get("verhalten") or [])
        rules = f'<ul class="rules">{rules}</ul>' if rules else ""
        cards.append(f"""      <div class="feature reveal">
        <h3>{inline(feature["titel"])}</h3>
        <p>{inline(feature["wozu"])}</p>
        {rules}
      </div>""")
    return f"""
    <section id="funktionen">
      <h2>{T[lang]["features"]}</h2>
      <div class="features">
{chr(10).join(cards)}
      </div>
    </section>"""


def roadmap(project, lang):
    phases = project[lang]["roadmap"]
    if not phases:
        return ""
    return f"""
    <section class="roadmap reveal" id="roadmap">
      <h2>{T[lang]["roadmap"]}</h2>
      <p class="hint">{T[lang]["roadmap_lead"]}</p>
      {lanes(((key, phases.get(key)) for key in PHASES), lang, css="lanes phases")}
    </section>"""


def project_page(project, lang):
    t = T[lang]
    text = project[lang]
    url = at(lang, project["path"])
    links = "\n".join(f'      <li><a href="{e(l["url"])}">{e(l["text"])}</a></li>' for l in text["links"])
    facts = "".join(f'<dt>{e(f["name"])}</dt><dd>{inline(f["wert"])}</dd>' for f in text["steckbrief"])
    status = ""
    if project["reports"]:
        latest = project["reports"][0]
        report, report_lang, report_url = version(latest, lang)
        older = "".join(f'<li><a href="{version(r, lang)[2]}">{e(version(r, lang)[0]["titel"])}</a>{foreign(version(r, lang)[1], lang)}'
                        f' · {day_text(r["date"], lang)}</li>' for r in project["reports"][1:])
        older = f'<h3>{t["earlier"]}</h3><ul class="plain">{older}</ul>' if older else ""
        status = f"""
    <section class="status reveal" id="wasserstand">
      <div class="status-head">
        {gauge(report, lang)}
        <div>
          <h2>{t["status"]}</h2>
          <p class="date">{t["as_of"]} <time datetime="{latest["date"].isoformat()}">{day_text(latest["date"], lang)}</time> · <a href="{report_url}">{e(report["titel"])}</a>{foreign(report_lang, lang)}</p>
        </div>
      </div>
      <div lang="{report_lang}">{lanes(((key, report[key]) for key in LANES), report_lang)}</div>
      {older}
    </section>"""
    guides = ""
    if project["guides"]:
        guides = f"""
    <section id="anleitungen">
      <h2>{t["guides"]}</h2>
      <div class="guides">
{chr(10).join(guide_item(g, lang) for g in project["guides"])}
      </div>
    </section>"""
    prose = f'\n    <div class="prose">\n{render(text["body"], lang)}\n    </div>' if text["body"].strip() else ""
    main = f"""  <article class="wrap page">
    <a class="back" href="{at(lang, "/#projekte")}">{t["all_projects"]}</a>
    <p class="eyebrow">{e(text["untertitel"])}</p>
    <h1>{e(project["name"])}</h1>
    <p class="lead vision">{inline(text["vision"])}</p>
    <ul class="links">
{links}
    </ul>{features(project, lang)}{roadmap(project, lang)}{status}{prose}{guides}
    <h2>{t["facts"]}</h2>
    <dl class="facts"><dt>{t["tech"]}</dt><dd>{e(", ".join(project["technik"]))}</dd>{facts}</dl>
  </article>"""
    graph = [{"@type": "SoftwareSourceCode", "name": project["name"], "description": text["kurz"], "url": SITE + url,
              "codeRepository": project["repo"], "keywords": ", ".join(project["technik"]), "inLanguage": lang,
              "author": {"@id": f"{SITE}/#person"}}]
    if project["app"]:
        app = project["app"]
        entry = {"@type": "SoftwareApplication", "name": project["name"], "description": text["kurz"],
                 "url": app.get("url", SITE + url), "applicationCategory": app.get("kategorie", "Application"),
                 "operatingSystem": app.get("plattformen", ""), "author": {"@id": f"{SITE}/#person"}}
        if app.get("kostenlos"):
            entry["offers"] = {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}
        if app.get("store"):
            entry["downloadUrl"] = app["store"]
        graph.append(entry)
    graph += [breadcrumb(lang, (t["projects"], at(lang, "/")), (project["name"], url)), person(lang)]
    return layout(lang, project["path"], f'{project["name"]}: {text["untertitel"]} · {AUTHOR}', text["kurz"], main,
                  nav="projekte", jsonld={"@context": "https://schema.org", "@graph": graph}, og_type="article")


def report_page(report, lang):
    t = T[lang]
    project = report["project"]
    text = report[lang]
    url = at(lang, report["path"])
    summary = text.get("zusammenfassung") or t["report_default"].format(n=project["name"])
    main = f"""  <article class="wrap page">
    <a class="back" href="{at(lang, project["path"])}">← {e(project["name"])}</a>
    <p class="eyebrow">{t["report"]} · <time datetime="{report["date"].isoformat()}">{day_text(report["date"], lang)}</time></p>
    <h1>{e(text["titel"])}</h1>
    <div class="status-head">{gauge(text, lang)}<p class="lead">{inline(summary)}</p></div>
    {lanes(((key, text[key]) for key in LANES), lang)}
    <div class="prose">
{render(text["body"], lang)}
    </div>
  </article>"""
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": text["titel"], "description": summary, "datePublished": report["date"].isoformat(),
         "inLanguage": lang, "url": SITE + url, "author": {"@id": f"{SITE}/#person"}, "about": project["name"]},
        breadcrumb(lang, (t["projects"], at(lang, "/")), (project["name"], at(lang, project["path"])), (text["titel"], url)),
        person(lang)]}
    return layout(lang, report["path"], f'{text["titel"]} · {t["status"]} {project["name"]} · {AUTHOR}', summary, main,
                  nav="wasserstand", jsonld=ld, og_type="article", alternates=available(report))


def guide_page(guide, lang):
    t = T[lang]
    project = guide["project"]
    text = guide[lang]
    url = at(lang, guide["path"])
    meta = f'<time datetime="{guide["date"].isoformat()}">{day_text(guide["date"], lang)}</time>'
    if guide["updated"]:
        meta += f' · {t["updated"]} <time datetime="{guide["updated"].isoformat()}">{day_text(guide["updated"], lang)}</time>'
    main = f"""  <article class="wrap page">
    <a class="back" href="{at(lang, project["path"])}">← {e(project["name"])}</a>
    <p class="eyebrow">{t["guide"]} · {meta}</p>
    <h1>{e(text["titel"])}</h1>
    <p class="lead">{e(text["beschreibung"])}</p>
    <div class="prose">
{render(text["body"], lang)}
    </div>
  </article>"""
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "TechArticle", "headline": text["titel"], "description": text["beschreibung"],
         "datePublished": guide["date"].isoformat(), "dateModified": (guide["updated"] or guide["date"]).isoformat(),
         "inLanguage": lang, "url": SITE + url, "author": {"@id": f"{SITE}/#person"}, "about": project["name"]},
        breadcrumb(lang, (t["projects"], at(lang, "/")), (project["name"], at(lang, project["path"])), (text["titel"], url)),
        person(lang)]}
    return layout(lang, guide["path"], f'{text["titel"]} · {project["name"]} · {AUTHOR}', text["beschreibung"], main,
                  nav="anleitungen", jsonld=ld, og_type="article", alternates=available(guide))


def available(item):
    return tuple(lang for lang in LANGS if item[lang])


def home(projects, reports, guides, lang):
    t = T[lang]
    cards = []
    for p in projects:
        text = p[lang]
        tags = "".join(f"<li>{e(tag)}</li>" for tag in p["technik"])
        badge = ""
        if p["reports"]:
            r = p["reports"][0]
            percent = level(version(r, lang)[0])
            badge = (f'<span class="badge" title="{t["gauge_of"].format(d=day_text(r["date"], lang))}">'
                     f'<i style="--level:{percent}%"></i>{percent}&nbsp;%</span>')
        cards.append(f"""      <a class="card reveal" href="{at(lang, p["path"])}">
        <div class="card-top"><h3>{e(p["name"])}</h3>{badge}</div>
        <p class="what">{e(text["untertitel"])}</p>
        <p>{inline(text["vision"])}</p>
        <ul class="tags">{tags}</ul>
        <span class="more">{t["more"]} <span aria-hidden="true">→</span></span>
      </a>""")
    news = ""
    if reports:
        news = f"""
    <section class="wrap" id="neu">
      <h2 class="section">{t["newest_reports"]}</h2>
      <div class="reports">
{chr(10).join(report_card(r, lang, with_project=True) for r in reports[:4])}
      </div>
      <p class="all"><a href="{at(lang, "/wasserstand.html")}">{t["all_reports"]}</a></p>
    </section>"""
    tutorials = ""
    if guides:
        tutorials = f"""
    <section class="wrap">
      <h2 class="section">{t["guides"]}</h2>
      <div class="guides">
{chr(10).join(guide_item(g, lang, with_project=True) for g in guides[:6])}
      </div>
      <p class="all"><a href="{at(lang, "/anleitungen.html")}">{t["all_guides"]}</a></p>
    </section>"""
    main = f"""    <div class="hero">
      <div class="hero-bg" aria-hidden="true"><span></span><span></span><span></span></div>
      <div class="wrap">
        <p class="eyebrow">{t["hero_eyebrow"]}</p>
        <h1>Marcel <span class="accent">Benders</span></h1>
        <p class="lead">{t["hero_lead"]}</p>
        <div class="actions">
          <a class="button" href="#projekte">{t["see_projects"]}</a>
          <a class="button ghost" href="https://github.com/Marcel-B">GitHub</a>
        </div>
      </div>
    </div>

    <section class="wrap" id="projekte">
      <h2 class="section">{t["projects"]}</h2>
      <div class="grid">
{chr(10).join(cards)}
      </div>
    </section>{news}{tutorials}

    <section class="wrap">
      <h2 class="section">{t["also"]}</h2>
      <ul class="also">
        <li>{t["also_text"]}</li>
      </ul>
    </section>"""
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": f"{SITE}/#site", "url": f"{SITE}/", "name": AUTHOR, "inLanguage": list(LANGS),
         "publisher": {"@id": f"{SITE}/#person"}},
        person(lang),
        {"@type": "ItemList", "name": t["projects"], "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": SITE + at(lang, p["path"]), "name": p["name"]}
            for i, p in enumerate(projects)]}]}
    names = ", ".join(p["name"] for p in projects[:6])
    return layout(lang, "/", t["home_title"], t["home_description"].format(n=names), main, jsonld=ld)


def list_page(lang, path, title, lead, description, body, nav):
    main = f"""  <div class="wrap page wide">
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
{body}
  </div>"""
    return layout(lang, path, f"{title} · {AUTHOR}", description, main, nav=nav)


def feed(reports, guides, lang):
    """Only what exists in this language, so a reader of the English feed gets no German entries."""
    entries = sorted([(r["date"], r[lang]["titel"] + " · " + r["project"]["name"], at(lang, r["path"]),
                       r[lang].get("zusammenfassung") or T[lang]["report"]) for r in reports if r[lang]] +
                     [(g["date"], g[lang]["titel"] + " · " + g["project"]["name"], at(lang, g["path"]), g[lang]["beschreibung"])
                      for g in guides if g[lang]], reverse=True)
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
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="{lang}">
  <title>{T[lang]["feed_name"]}</title>
  <link href="{SITE}{at(lang, "/")}"/>
  <link rel="self" href="{SITE}{at(lang, "/feed.xml")}"/>
  <id>{SITE}{at(lang, "/")}</id>
  <updated>{updated}T00:00:00Z</updated>
  <author><name>{AUTHOR}</name></author>
{items}</feed>
"""


def build(out):
    load_names()
    projects, pages = load()
    reports = sorted((r for p in projects for r in p["reports"]), key=lambda r: r["date"], reverse=True)
    guides = sorted((g for p in projects for g in p["guides"]), key=lambda g: g["date"], reverse=True)

    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(ROOT / "static", out)
    files = []

    def write(url, text, sitemap=True):
        path = out / (url.lstrip("/") + ("index.html" if url.endswith("/") else ""))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        if sitemap:
            files.append(url)

    for lang in LANGS:
        t = T[lang]
        write(at(lang, "/"), home(projects, reports, guides, lang))
        for p in projects:
            write(at(lang, p["path"]), project_page(p, lang))
            for r in p["reports"]:
                if r[lang]:
                    write(at(lang, r["path"]), report_page(r, lang))
            for g in p["guides"]:
                if g[lang]:
                    write(at(lang, g["path"]), guide_page(g, lang))

        if reports:
            body = "      <div class=\"reports\">\n" + "\n".join(report_card(r, lang, with_project=True) for r in reports) + "\n      </div>"
        else:
            body = f'      <p class="empty">{t["no_reports"]}</p>'
        write(at(lang, "/wasserstand.html"), list_page(lang, "/wasserstand.html", t["status"], t["status_lead"],
                                                        t["status_description"], body, "wasserstand"))
        if guides:
            body = "      <div class=\"guides\">\n" + "\n".join(guide_item(g, lang, with_project=True) for g in guides) + "\n      </div>"
        else:
            body = f'      <p class="empty">{t["no_guides"]}</p>'
        write(at(lang, "/anleitungen.html"), list_page(lang, "/anleitungen.html", t["guides"], t["guides_lead"],
                                                        t["guides_description"], body, "anleitungen"))

        (out / at(lang, "/feed.xml").lstrip("/")).write_text(feed(reports, guides, lang), encoding="utf-8")
        for page in pages:
            text = page[lang]
            main = f'  <article class="wrap page">\n    <h1>{e(text["titel"])}</h1>\n    <div class="prose">\n{render(text["body"])}\n    </div>\n  </article>'
            write(at(lang, page["path"]), layout(lang, page["path"], f'{text["titel"]} · {AUTHOR}', text["beschreibung"], main))

        if lang != "de":
            continue
        # GitHub Pages serves one 404 page for every address, so it exists only once, in German.
        notfound = f"""  <div class="wrap page">
    <h1>{t["notfound"]}</h1>
    <p class="lead">{t["notfound_lead"]}</p>
    <p><a class="button" href="{at(lang, "/")}">{t["notfound_button"]}</a></p>
  </div>"""
        write("/404.html", layout(lang, "/404.html", f'{t["notfound"]} · {AUTHOR}', t["notfound_description"],
                                  notfound, index=False, alternates=("de",)), sitemap=False)

    today = datetime.date.today().isoformat()
    urls = "".join(f"  <url><loc>{SITE}{url}</loc><lastmod>{today}</lastmod></url>\n" for url in files)
    (out / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    translated = sum(1 for r in reports if r["en"]) + sum(1 for g in guides if g["en"])
    print(f"{len(projects)} Projekte, {len(reports)} Meldungen, {len(guides)} Anleitungen ({translated} davon auf Englisch) nach {out}")


if __name__ == "__main__":
    try:
        build(Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "_site")
    except ContentError as error:
        print(f"Fehler: {error}", file=sys.stderr)
        sys.exit(1)
