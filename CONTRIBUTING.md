# Die Seite aus einem Projekt heraus ergänzen

Diese Anleitung gilt für jedes Projekt auf [marcelbenders.com](https://marcelbenders.com/) und für jeden, der daran
arbeitet, auch für Claude in einem anderen Repository. Zu einem Projekt gehören drei Arten von Inhalt, jede als
Markdown-Datei in `content/projekte/<projekt>/`:

| Was | Datei | Englisch | Erscheint auf |
| --- | --- | --- | --- |
| Projektseite | `projekt.md` | `projekt.en.md` (Pflicht) | Startseite (Karte mit der Vision) und `/projekte/<projekt>/` |
| Wasserstandsmeldung | `stand/<JJJJ-MM-TT>.md` | `stand/<JJJJ-MM-TT>.en.md` | Projektseite (die neueste ganz), `/wasserstand.html`, Startseite, Feed |
| Anleitung | `anleitungen/<name>.md` | `anleitungen/<name>.en.md` | Projektseite, `/anleitungen.html`, Startseite, Feed |

Die Seite baut sich aus diesen Dateien selbst. Du schreibst kein HTML, und Titel, Vorschaubild, strukturierte Daten für
Suchmaschinen, Sitemap und Feed entstehen automatisch.

## Zwei Sprachen

Die Seite ist zweisprachig: Deutsch unter `/`, Englisch unter `/en/` mit denselben Pfaden dahinter
(`/en/projekte/<projekt>/`). Die englische Fassung einer Datei liegt als `<name>.en.md` direkt neben der deutschen.

- **Projektseiten** gibt es immer in beiden Sprachen; ohne `projekt.en.md` bricht der Build ab.
- **Wasserstandsmeldungen und Anleitungen** sollen ebenfalls eine englische Fassung bekommen. Fehlt sie, erscheint der
  Eintrag auf den englischen Seiten auf Deutsch, mit dem Hinweis „in German“, und verlinkt die deutsche Seite.
- Die englische Datei übersetzt nur die Texte. Was keine Sprache hat (`name`, `technik`, `reihenfolge`, `app`, Datum),
  steht nur in der deutschen.
- Links innerhalb der Seite zeigen in der englischen Fassung auf `/en/…`, also `[Tonwerk-AI](/en/projekte/tonwerk-ai/)`.
- Englisch in britischer Schreibweise (*colour*, *licence*), in ganzen Sätzen und in der Du-Form des Englischen (*you*).

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
- Englisch daneben als `stand/2026-11-15.en.md` mit `titel`, den Listen und, falls vorhanden, `zusammenfassung` und Text;
  das Datum kommt aus der deutschen Datei.
- Passt die Meldung den Plan an, ändere auch die `roadmap` in `projekt.md` und `projekt.en.md`.

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
- Englisch daneben als `anleitungen/<name>.en.md` mit `titel`, `beschreibung` und dem Text; Datum, `aktualisiert` und
  `reihenfolge` kommen aus der deutschen Datei.
- Bilder: unter `static/img/<projekt>/` ablegen und als `![Beschreibung](/img/<projekt>/bild.png)` einbinden, mit
  einem Text, der sagt, was zu sehen ist.

## Projektseite

`content/projekte/<projekt>/projekt.md` stellt das Projekt vor. Der Ordnername ist die Adresse
(`/projekte/<projekt>/`). Die Seite hat drei Teile, jeder aus einer eigenen Perspektive:

1. **Vision** (Karte auf der Startseite und Einleitung der Projektseite): was das Projekt sein soll, aus der Sicht
   eines Product Owners. Nicht, was es heute kann, sondern wofür es da ist und wem es hilft. Zwei, höchstens drei Sätze,
   ohne Fachbegriffe, so dass jemand ohne Vorwissen versteht, warum es das Projekt gibt.
2. **Funktionen**: was es heute kann, wie in einer Spezifikation. Jede Funktion hat einen Titel, einen Satz `wozu`
   (welchen Nutzen sie stiftet) und unter `verhalten` die Zusagen, die sie einhält: kurze, überprüfbare Sätze im
   Präsens („Das Original wird erst gelöscht, wenn die neue Datei geprüft ist.“). Nur, was wirklich läuft.
3. **Roadmap**: was als Nächstes kommt, in den Spalten `jetzt`, `als_naechstes` und `spaeter`. Ein Plan, kein
   Versprechen; leere Spalten weglassen.

```markdown
---
name: Slipways
untertitel: Slipanlagen und Marinas in Europa
reihenfolge: 30
vision: Wer ein Boot ins Wasser bringen will, soll schon vor der Fahrt wissen, wo das geht und ob der Pegel passt. Slipways
  soll die verlässliche Karte für Slipanlagen und Marinas in Europa werden.
kurz: Ein bis zwei sachliche Sätze für Suchmaschinen und Vorschauen (höchstens etwa 160 Zeichen).
technik: [ASP.NET Core, React, Kotlin, SwiftUI]
links:
  - text: slipways.de
    url: https://slipways.de/
  - text: Quelltext auf GitHub
    url: https://github.com/Marcel-B/Slipways
features:
  - titel: Pegelstände
    wozu: Wissen, ob das Wasser für die Rampe reicht, bevor man losfährt.
    verhalten:
      - Neue Werte alle 15 Minuten aus PEGELONLINE.
      - Für die Niederlande von Rijkswaterstaat.
roadmap:
  jetzt:
    - Namen für Slipanlagen, die in OpenStreetMap keinen haben
  als_naechstes:
    - Fotos zu Slipanlagen und Marinas
    - 'Lokalisierung: Web und Apps in weiteren Sprachen'
  spaeter:
    - Pegel für weitere Länder
steckbrief:
  - name: Plattform
    wert: Web, Android, iOS
app:                          # nur für Apps, die man laden oder nutzen kann
  kategorie: TravelApplication    # schema.org: MultimediaApplication, DeveloperApplication, UtilitiesApplication, …
  plattformen: Web, Android, iOS
  url: https://slipways.de/
  kostenlos: true
  store: https://apps.apple.com/…   # optional
---

## Technik

Optional weitere Abschnitte als Markdown, etwa Technik oder ein Leitprinzip. Sie stehen unter Roadmap und Wasserstand.
```

`projekt.en.md` daneben enthält dieselben Felder übersetzt: `untertitel`, `vision`, `kurz`, `links`, `features`, dazu
`roadmap` und `steckbrief`, wenn die deutsche Fassung sie hat, und den Markdown-Teil.

- **Pflicht:** `name`, `untertitel`, `vision`, `kurz`, `technik`, `links`, `features`; in der englischen Datei
  `untertitel`, `vision`, `kurz`, `links`, `features`. Beide Fassungen haben gleich viele Funktionen, und die Roadmap gibt
  es in beiden oder in keiner.
- Ein Link auf das GitHub-Repository gehört in `links`; er wird für Suchmaschinen als Quelltext-Adresse angegeben.
- `reihenfolge` legt den Platz auf der Startseite fest (kleiner zuerst, in Zehnerschritten, damit dazwischen Platz
  bleibt).
- **Lokalisierung gehört auf jede Roadmap**, solange die Oberfläche des Projekts nicht in mehreren Sprachen vorliegt,
  in der Regel unter `als_naechstes`. Ausnahmen sind Projekte ohne übersetzbare Oberfläche.
- Die Roadmap darf sich mit der neuesten Wasserstandsmeldung überschneiden. Die Meldung hält einen Stand fest, die Roadmap
  ist immer der aktuelle Plan; bei einer neuen Meldung die Roadmap mit anpassen.
- Für ein neues Projekt den Ordner mit beiden Dateien anlegen; die Karten auf beiden Startseiten und alle Verweise
  entstehen von selbst.

## Für Claude in einem anderen Repository

Wenn du in einem Projekt-Repository arbeitest und die Seite ergänzen sollst:

1. Lies diese Datei und die vorhandenen Dateien des Projekts unter `content/projekte/<projekt>/`, deutsch und englisch.
2. Nimm den Stand aus dem Projekt selbst: README, Roadmap, offene Punkte, letzte Commits und Releases. Erfinde
   nichts; was du nicht belegen kannst, lässt du weg.
3. Schreib auf Deutsch, in der Du-Form, in ganzen Sätzen und für Besucher, nicht für Entwickler des Projekts, und leg
   die englische Fassung gleich daneben. Ändert sich, was das Projekt kann oder vorhat, pass `features` und `roadmap` in
   `projekt.md` und `projekt.en.md` mit an.
4. Baue und prüfe lokal (siehe Ablauf) und öffne einen Pull Request in `Marcel-B/com` mit einem deutschen Titel wie
   „Wasserstand Slipways November 2026“.
