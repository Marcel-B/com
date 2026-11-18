---
titel: 3d-o-mat mit Agents benutzen
beschreibung: 3d-o-mat als MCP-Server in Claude Code einbinden, damit ein Agent aus einem Bild ein 3D-Modell macht, ein Skelett einsetzt und das Ergebnis in dein Projekt legt.
datum: 2026-11-18
reihenfolge: 2
---

3d-o-mat lässt sich nicht nur im Browser bedienen. Über das Model Context Protocol (MCP) kann auch ein Agent damit
arbeiten, etwa Claude Code beim Bauen eines Spiels: ein Bild hochladen oder malen lassen, in 3D umwandeln, warten, ein
Skelett einsetzen und das Modell als GLB, 3MF, STL oder FBX holen. Der MCP-Server ist Teil von 3d-o-mat selbst und läuft
unter derselben Adresse wie die Seite, unter `/mcp`. Auf deinem Rechner musst du nichts installieren außer dem Eintrag
in Claude Code.

## Was du brauchst

- ein laufendes 3d-o-mat, das dein Rechner erreicht, im Heimnetz oder über ein privates Netz wie Tailscale
- Claude Code auf diesem Rechner

3d-o-mat fragt nach keiner Anmeldung. Es gehört deshalb nicht ins offene Internet, und der MCP-Server auch nicht. Aus
demselben Grund erreichen ihn Agents, die in der Cloud laufen, nicht.

## 1. Den Server eintragen

Im Terminal, mit der Adresse deines 3d-o-mat:

```sh
claude mcp add --transport http --scope user 3d-o-mat https://<adresse-von-3d-o-mat>/mcp
```

`--scope user` macht 3d-o-mat in allen deinen Projekten verfügbar. Soll es nur in einem Projekt gelten, und dort für
alle, die es auschecken, leg stattdessen eine Datei `.mcp.json` ins Repository:

```json
{ "mcpServers": { "3d-o-mat": { "type": "http", "url": "https://<adresse-von-3d-o-mat>/mcp" } } }
```

## 2. Prüfen, ob er antwortet

```sh
claude mcp list
```

Hinter `3d-o-mat` sollte `Connected` stehen. Steht dort ein Fehler, öffne dieselbe Adresse ohne `/mcp` im Browser:
Kommt die Seite von 3d-o-mat nicht, liegt es am Netz, nicht an Claude Code. In einer laufenden Sitzung zeigt `/mcp` die
Werkzeuge von 3d-o-mat.

## 3. Benutzen

Sag dem Agent einfach, was du willst, zum Beispiel:

> Mach aus `bilder/ritter.png` ein 3D-Modell mit Skelett und leg das GLB unter `assets/figuren/` ab.

Der Agent lädt das Bild hoch, startet den Auftrag, wartet und holt die Datei. Ein Auftrag dauert je nach Größe einige
Minuten, das Skelett etwa eine weitere. Was er anlegt, steht auch auf der Seite in der Liste, und Aufträge aus dem
Browser und vom Agent warten in derselben Schlange.

Die Werkzeuge im Überblick:

| Werkzeug | Was es tut |
| --- | --- |
| `get_status` | sagt, ob 3d-o-mat gerade arbeiten kann und wie viele Aufträge warten |
| `upload_image`, `list_images`, `show_image` | Bilder hochladen, auflisten und ansehen |
| `check_image` | Gemma prüft, ob ein Bild für 3D taugt |
| `write_image_prompts`, `paint_images`, `get_painting` | aus einer Idee Prompts schreiben und Bilder malen lassen |
| `create_model`, `get_job`, `list_jobs`, `cancel_job` | Bild zu 3D, auf das Ergebnis warten, Aufträge ansehen und einen wartenden abbrechen |
| `add_skeleton` | ein Skelett mit Mixamo-Namen einsetzen |
| `export_model` | eine Download-Adresse für GLB, FBX (Unity oder Unreal) oder eine Druckdatei (3MF, STL) |

Große Dateien gehen nicht durch das Gespräch mit dem Agent: Er bekommt eine Adresse und lädt die Datei selbst herunter,
und ein Bild von der Platte lädt er am besten ebenso direkt hoch.

## Was noch nicht geht

Animationen aus der Bewegungsbibliothek, Haltungen und der Gelenk-Editor gibt es nur im Browser, weil die Bewegungen
dort auf die Figur übertragen werden. Ein eigenes Modell importieren und Löschen geht ebenfalls nur dort. Der
MCP-Server ist mit einem nachgestellten Rechner ausprobiert, mit Claude Code und dem offiziellen MCP-Client; mit dem
echten Dienst und echten Modellen steht das noch aus.
