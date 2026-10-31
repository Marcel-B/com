---
titel: 3d-o-mat auf einem Mac einrichten
beschreibung: Schritt für Schritt die Website von 3d-o-mat auf einem Mac starten, ohne Docker, zum Entwickeln, Ausprobieren oder für den Betrieb direkt auf dem Rechen-Mac.
datum: 2026-10-31
reihenfolge: 1
---

3d-o-mat besteht aus zwei Teilen: der Website (eine Python-App mit React-Oberfläche) und der Rechenseite auf einem Mac
mit Apple Silicon, wo TRELLIS.2, SkinTokens, Gemma und die Bildmodelle hinter einer gemeinsamen Schranke laufen. Diese
Anleitung bringt die Website auf einem Mac zum Laufen. Am Ende erreichst du sie im Browser unter
`http://localhost:8090`, kannst Bilder hochladen und freistellen und, sobald die Schranke die Modelle freigibt, auch
prüfen, malen, in 3D umwandeln und Skelette einsetzen.

Die Einrichtung der Rechenseite selbst (Schranke, MLX-Serve, Rig-Dienst) beschreibt das
[README im Projekt](https://github.com/Marcel-B/3d-o-mat#einrichten). Die ausführliche Fassung dieser Anleitung liegt
als [docs/mac.md](https://github.com/Marcel-B/3d-o-mat/blob/main/docs/mac.md) im Repository.

## Was du brauchst

- einen Mac mit macOS und Terminal; für die Website allein braucht es kein Apple Silicon
- etwa 2 GB Platz für Python-Pakete, Node-Module und das Freistellmodell
- für Prüfen, Malen und 3D die Adresse einer laufenden Schranke im selben Netz, bei der du die Modelle freigeben kannst

## 1. Werkzeuge installieren

Git kommt mit den Entwicklerwerkzeugen von Apple, Python 3.12 und Node 22 über [Homebrew](https://brew.sh):

```sh
xcode-select --install
brew install python@3.12 node@22
```

Das Python, das macOS mitbringt (3.9), ist für die App zu alt; sie braucht mindestens 3.10. Node brauchst du nur, um
die Oberfläche zu bauen. Mit `python3.12 --version` und `node --version` siehst du, dass beides da ist. Findet das
Terminal `node` nicht, nennt `brew info node@22` die Zeile für `~/.zprofile`.

## 2. Projekt holen und bauen

```sh
git clone https://github.com/Marcel-B/3d-o-mat.git ~/repos/3d-o-mat && cd ~/repos/3d-o-mat
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt -r requirements-rembg.txt
(cd frontend && npm ci && npm run build)
```

Die virtuelle Umgebung `.venv` hält alle Python-Pakete im Projektordner. `requirements-rembg.txt` bringt rembg zum
Freistellen von Fotos; ohne das Paket entfernt die App nur einfarbige Hintergründe. `npm run build` legt die
Oberfläche nach `frontend/dist`, von wo die App sie ausliefert. Wenn ein späteres `git pull` etwas in `frontend/`
ändert, baust du sie noch einmal.

## 3. Ablage anlegen

Bilder, Aufträge und Modelle landen in einem Ordner. Die App benutzt ihn nur, wenn darin die Kennzeichen-Datei
`.3d-o-mat` liegt; so landet nie etwas auf der falschen Platte, wenn eine externe gerade fehlt.

```sh
mkdir -p ~/3d-o-mat-daten && touch ~/3d-o-mat-daten/.3d-o-mat
```

Liegt der Ordner auf einer externen Platte, fragt macOS beim ersten Zugriff, ob das Terminal auf Wechseldatenträger
zugreifen darf. Bis du „Erlauben“ klickst, wartet die App ohne Fehlermeldung.

## 4. Einstellung

```sh
cp config.example.json config.json
```

In `config.json` änderst du zwei Stellen:

- `store` auf deinen Ordner, mit absolutem Pfad: `"store": {"folder": "/Users/<du>/3d-o-mat-daten"}`
- `gate.url` auf die Adresse der Schranke, etwa `http://<rechen-mac>:1235`, oder `http://127.0.0.1:1235`, wenn die
  Website auf dem Rechen-Mac selbst läuft

`config.json` bleibt lokal und kommt nicht ins Repository. Die übrigen Felder erklärt das README.

## 5. Starten

```sh
.venv/bin/python -m omat3d
```

Öffne `http://localhost:8090`. Lade ein Bild hoch: Es erscheint freigestellt in der Liste, und im Ordner aus Schritt 3
liegt jetzt `images/…`. Beim ersten Foto lädt rembg einmal sein Modell (etwa 170 MB).

Beim Start meldet sich die App bei der Schranke als `3d-o-mat` an. Ist die Schranke nicht erreichbar, steht das im
Terminal, und die App versucht es alle 10 Sekunden wieder. Nach der Anmeldung gibst du in der Oberfläche der Schranke
unter `/gate` bei 3d-o-mat TRELLIS.2, SkinTokens, Gemma und die Bildmodelle frei; bis dahin werden Prüfen, Malen und
3D mit „nicht freigegeben“ abgelehnt. Wie weit alles ist, zeigt `http://localhost:8090/api/status`: ob die Ablage da
ist, ob rembg geladen ist und welche Modelle frei sind.

Beenden mit Ctrl-C. Was lief oder wartete, kommt beim nächsten Start wieder in die Schlange.

## 6. Entwickeln

```sh
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest
cd frontend && npm run dev
```

Die Tests brauchen weder die Rechenseite noch Netz; Schranke und Ablage sind darin nachgestellt. `npm run dev` zeigt
die Oberfläche mit Neuladen unter `http://localhost:5173` und reicht `/api` an die laufende App auf Port 8090 weiter.

## Wenn es hakt

- **`TypeError: unsupported operand type(s) for |` beim Start:** Die virtuelle Umgebung ist mit dem Python von macOS
  angelegt. `.venv` löschen und Schritt 2 mit `python3.12` wiederholen.
- **Die Seite meldet, die Ablage sei nicht erreichbar:** `.3d-o-mat` fehlt im Ordner aus `store.folder`, oder der Pfad stimmt nicht.
  Die App prüft die Ablage höchstens alle 20 Sekunden neu.
- **Seite bleibt leer:** `frontend/dist` fehlt; die Oberfläche bauen (Schritt 2).
- **Fotos schlecht freigestellt:** rembg fehlt, `/api/status` zeigt `"rembg": false`. Die Pakete aus
  `requirements-rembg.txt` nachinstallieren.
- **`address already in use`:** Port 8090 ist belegt, zum Beispiel von einer zweiten Instanz. `port` in `config.json`
  ändern.
