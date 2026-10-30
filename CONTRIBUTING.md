# Die Seite aus einem Projekt heraus ergänzen

Diese Anleitung gilt für jedes Projekt auf [marcelbenders.com](https://marcelbenders.com/) und für jeden, der daran
arbeitet, auch für Claude in einem anderen Repository. Zu einem Projekt gehören drei Arten von Inhalt, jede als
Markdown-Datei in `content/projekte/<projekt>/`:

| Was | Datei | Erscheint auf |
| --- | --- | --- |
| Projektseite | `projekt.md` | Startseite (Karte) und `/projekte/<projekt>/` |
| Wasserstandsmeldung | `stand/<JJJJ-MM-TT>.md` | Projektseite (die neueste ganz), `/wasserstand.html`, Startseite, Feed |
| Anleitung | `anleitungen/<name>.md` | Projektseite, `/anleitungen.html`, Startseite, Feed |

Die Seite baut sich aus diesen Dateien selbst. Du schreibst kein HTML, und Titel, Vorschaubild, strukturierte Daten für
Suchmaschinen, Sitemap und Feed entstehen automatisch.

## Ablauf

1. Dieses Repository klonen (`git clone https://github.com/Marcel-B/com`) und einen Branch anlegen.
2. Die Datei anlegen oder ändern, wie unten beschrieben.
3. Lokal bauen und prüfen:

   ```sh
   pip install -r requirements.txt
   python3 scripts/build.py && scripts/check-site.sh
   python3 -m http.server -d _site 8000     # ansehen unter http://localhost:8000
   ```

4. Einen Pull Request öffnen. Der Workflow baut und prüft die Seite noch einmal. Nach dem Merge auf `main` ist sie
   nach etwa einer Minute online.

Der Build bricht mit Dateiname und Grund ab, wenn ein Pflichtfeld fehlt oder ein Datum nicht stimmt. Die Prüfung
meldet kaputte Links.

## Wasserstandsmeldung

Eine Wasserstandsmeldung sagt, wie weit ein Projekt ist: was fertig ist, woran gerade gearbeitet wird und was geplant
ist. Schreib eine neue, wenn sich daran etwas Nennenswertes geändert hat, etwa nach einem Release, einem größeren
Feature oder wenn sich ein Plan ändert. Alte Meldungen bleiben stehen; sie sind die Geschichte des Projekts.

`content/projekte/<projekt>/stand/2026-11-15.md`:

```markdown
---
titel: Fotos sind da, die Karte lädt nur noch den Ausschnitt
datum: 2026-11-15
zusammenfassung: Ein Satz für Übersichten, Feed und Suchmaschinen.
fertig:
  - Fotos zu Slipanlagen und Marinas
  - Karte lädt nur den sichtbaren Ausschnitt
in_arbeit:
  - Großbritannien und Finnland importieren
geplant:
  - Pegel für weitere Länder
---

Optional ein paar Absätze Text: was sich geändert hat, was dabei schwierig war, was als Nächstes kommt.
```

- **Pflicht:** `titel` und mindestens eine der Listen `fertig`, `in_arbeit`, `geplant`. Ohne `datum` gilt das Datum
  aus dem Dateinamen. Eine Meldung pro Projekt und Tag.
- **Listen** beschreiben den Stand des ganzen Projekts, nicht nur die Änderungen seit der letzten Meldung. Aus ihnen
  berechnet die Seite den Pegel: fertig zählt ganz, in Arbeit halb, geplant gar nicht. Einträge dürfen Markdown
  enthalten (`**fett**`, `[Link](https://…)`, `` `Code` ``).
- Schreib für Besucher: was jemand davon hat, nicht welche Klasse sich geändert hat. Keine internen Adressen,
  IPs, Tailnet-Namen, Hostnamen oder Schlüssel.
- Ehrlich bleiben: Was nur in einer Testumgebung lief, steht unter `in_arbeit`, nicht unter `fertig`.

## Anleitung

Eine Anleitung zeigt Schritt für Schritt, wie man ein Projekt selbst aufsetzt, betreibt oder benutzt.

`content/projekte/<projekt>/anleitungen/mac-einrichten.md`:

~~~markdown
---
titel: Tonwerk-AI auf einem Mac einrichten
beschreibung: Ein Satz, worum es geht und für wen. Steht in Listen, im Feed und bei Suchmaschinen.
datum: 2026-10-30
aktualisiert: 2026-11-20
reihenfolge: 1
---

## Was du brauchst

- …

## 1. Installieren

```sh
…
```
~~~

- **Pflicht:** `titel`, `beschreibung`, `datum`. `aktualisiert` setzen, wenn die Anleitung später überarbeitet wird.
  `reihenfolge` sortiert die Anleitungen eines Projekts (kleinere Zahl zuerst, sonst alphabetisch).
- Der Dateiname wird die Adresse (`/projekte/<projekt>/<name>.html`): nur Kleinbuchstaben, Ziffern und Bindestriche,
  und später nicht mehr umbenennen, sonst brechen Links.
- Überschriften ab `##`, die Seite setzt den Titel als `#`. Befehle in Codeblöcke mit Sprache (` ```sh `).
- Eine Anleitung soll ohne das Repository verständlich sein: was man braucht, was jeder Schritt tut, wie man sieht,
  dass er geklappt hat. Für Details darf sie auf das README im Projekt verlinken.
- Bilder: unter `static/img/<projekt>/` ablegen und als `![Beschreibung](/img/<projekt>/bild.png)` einbinden, mit
  einem Text, der sagt, was zu sehen ist.

## Projektseite

`content/projekte/<projekt>/projekt.md` stellt das Projekt vor. Der Ordnername ist die Adresse
(`/projekte/<projekt>/`).

```markdown
---
name: Slipways
untertitel: Slipanlagen und Marinas in Europa
reihenfolge: 30
kurz: Ein bis zwei Sätze für die Karte auf der Startseite und für Suchmaschinen (höchstens etwa 160 Zeichen).
einleitung: Ein Absatz unter dem Titel der Projektseite.
technik: [ASP.NET Core, React, Kotlin, SwiftUI]
links:
  - text: slipways.de
    url: https://slipways.de/
  - text: Quelltext auf GitHub
    url: https://github.com/Marcel-B/Slipways
steckbrief:
  - name: Plattform
    wert: Web, Android, iOS
  - name: Lizenz
    wert: PolyForm Strict 1.0.0
app:                          # nur für Apps, die man laden oder nutzen kann
  kategorie: TravelApplication    # schema.org: MultimediaApplication, DeveloperApplication, UtilitiesApplication, …
  plattformen: Web, Android, iOS
  url: https://slipways.de/
  kostenlos: true
  store: https://apps.apple.com/…   # optional
---

## Was es kann

- …

## Technik

…
```

- **Pflicht:** `name`, `untertitel`, `kurz`, `einleitung`, `technik`, `links`. Ein Link auf das GitHub-Repository
  gehört in `links`; er wird für Suchmaschinen als Quelltext-Adresse angegeben.
- `reihenfolge` legt den Platz auf der Startseite fest (kleiner zuerst, in Zehnerschritten, damit dazwischen Platz
  bleibt).
- Für ein neues Projekt den Ordner anlegen; die Karte auf der Startseite und alle Verweise entstehen von selbst.
- Die Projektseite beschreibt, was das Projekt ist. Was gerade passiert, gehört in eine Wasserstandsmeldung, wie man es
  benutzt, in eine Anleitung.

## Für Claude in einem anderen Repository

Wenn du in einem Projekt-Repository arbeitest und die Seite ergänzen sollst:

1. Lies diese Datei und die vorhandenen Dateien des Projekts unter `content/projekte/<projekt>/`.
2. Nimm den Stand aus dem Projekt selbst: README, Roadmap, offene Punkte, letzte Commits und Releases. Erfinde
   nichts; was du nicht belegen kannst, lässt du weg.
3. Schreib auf Deutsch, in der Du-Form, in ganzen Sätzen und für Besucher, nicht für Entwickler des Projekts.
4. Baue und prüfe lokal (siehe Ablauf) und öffne einen Pull Request in `Marcel-B/com` mit einem deutschen Titel wie
   „Wasserstand Slipways November 2026“.
