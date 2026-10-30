---
titel: Ohmventory auf einem Mac einrichten
beschreibung: Schritt für Schritt von einem Mac mit Apple Silicon bis zum ersten erkannten Bauteil, mit LM Studio als lokalem Sprachmodell und Docker Desktop.
datum: 2026-10-30
reihenfolge: 1
---

Ohmventory besteht aus einer Datenbank, einer Websuche, dem Server und der Oberfläche. Alles vier läuft in Docker. Das
Sprachmodell, das Fotos erkennt und Projekte vorschlägt, läuft daneben in LM Studio, direkt auf dem Mac, weil es dort den
Grafikspeicher nutzen kann. Am Ende erreichst du Ohmventory im Browser auf dem Mac und vom Handy im selben WLAN.

## Was du brauchst

- einen Mac mit Apple Silicon (M1 oder neuer) und macOS 14 oder neuer
- Speicher: 32 GB für beide Modelle; mit 16 GB geht es mit dem kleinen Modell allein (siehe Schritt 2)
- rund 30 GB freien Platz für Modelle und Docker-Abbilder
- eine Internetverbindung für die Downloads und die Websuche

## 1. Werkzeuge installieren

Öffne das Terminal. Git kommt mit den Entwicklerwerkzeugen von Apple:

```sh
xcode-select --install
```

Dann lädst du zwei Programme und installierst sie wie jede andere Mac-App:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) in der Fassung für Apple Silicon. Starte es einmal
  und warte, bis in der Menüleiste „Docker Desktop is running“ steht.
- [LM Studio](https://lmstudio.ai/). Starte es einmal, damit es seinen Modellordner anlegt.

LM Studio bringt das Kommandozeilenwerkzeug `lms` mit. Damit das Terminal es findet:

```sh
~/.lmstudio/bin/lms bootstrap
```

Danach ein neues Terminalfenster öffnen. So siehst du, dass alles da ist:

```sh
git --version
docker version
lms version
```

## 2. Die Modelle laden

Ohmventory nutzt zwei Modelle: ein kleines für den Projektassistenten und die Websuche und ein größeres für die
Fotoerkennung.

```sh
lms get lmstudio-community/gemma-4-e4b-it-mlx
```

Das größere Modell suchst du in LM Studio unter **Discover** nach `gemma-4-26b-a4b-it-qat` und lädst die MLX-Fassung
(etwa 16 GB). Mit `lms ls` siehst du danach die Namen beider Modelle; genau diese Namen braucht Ohmventory. Weichen sie
von `gemma-4-e4b-it-mlx` und `gemma-4-26b-a4b-it-qat-mlx` ab, trägst du sie in Schritt 3 ein.

**Mac mit 16 GB:** Lass das große Modell weg. Das kleine kann Bilder auch erkennen, nur etwas weniger treffsicher.

Jetzt startest du den Server von LM Studio und lädst das kleine Modell mit dem Kontext, für den Ohmventory seine
Anfragen bemisst:

```sh
lms server start
lms load gemma-4-e4b-it-mlx --context-length 8192
```

Prüfen kannst du das so; die Antwort listet die Modelle auf:

```sh
curl http://localhost:1234/v1/models
```

Das große Modell lädt LM Studio von selbst, sobald die erste Fotoerkennung kommt. Damit es dabei nicht mit einem zu
kleinen Kontext startet, stellst du in LM Studio unter **My Models** bei beiden Modellen die Kontextlänge auf 8192.

## 3. Ohmventory holen und einstellen

```sh
git clone https://github.com/Marcel-B/Ohmventory.git ~/Ohmventory
cd ~/Ohmventory
cp .env.example .env
```

Die Datei `.env` hält die Einstellungen. Die folgenden Zeilen setzen zufällige Passwörter, verbinden Ohmventory mit
LM Studio auf dem Mac und tragen die Adresse ein, unter der das Handy den Mac erreicht:

```sh
sed -i '' \
  -e "s|^POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=$(openssl rand -hex 16)|" \
  -e "s|^SEARXNG_SECRET=.*|SEARXNG_SECRET=$(openssl rand -hex 32)|" \
  -e "s|^LLM_GATE_URL=.*|LLM_GATE_URL=http://host.docker.internal:1234|" \
  -e "s|^PUBLIC_BASE_URL=.*|PUBLIC_BASE_URL=http://$(ipconfig getifaddr en0):8080|" \
  .env
grep -E '^(LLM_GATE_URL|PUBLIC_BASE_URL)=' .env
```

Zeigt `PUBLIC_BASE_URL` keine Adresse wie `http://192.168.….:8080`, hängt der Mac nicht über WLAN am Netz. Dann nimm
`ipconfig getifaddr en1` und trag die Adresse von Hand ein (`open -e .env`).

Was die Einstellungen bedeuten:

- `LLM_GATE_URL` ist die Adresse des Sprachmodells. Ohmventory ist dafür gebaut, sich das Modell über eine Warteschlange
  mit anderen Anwendungen zu teilen. Auf deinem eigenen Mac spricht es LM Studio direkt an, `host.docker.internal` ist
  aus Docker heraus der Mac selbst.
- `LLM_MODEL` und `LLM_VISION_MODEL` sind die Modellnamen aus `lms ls`. Leer lassen, wenn sie zu Schritt 2 passen. Auf
  einem Mac mit 16 GB setzt du `LLM_VISION_MODEL=gemma-4-e4b-it-mlx`.
- `PUBLIC_BASE_URL` steht in den QR-Etiketten. Ändert sich die Adresse des Macs, druckst du die Etiketten neu, oder du
  gibst dem Mac im Router eine feste Adresse.

## 4. Starten

```sh
docker compose up -d --build
```

Beim ersten Mal baut Docker Server und Oberfläche, das dauert einige Minuten. Danach siehst du, ob alles läuft:

```sh
docker compose ps
curl http://localhost:8080/api/health
```

Alle vier Dienste stehen auf „running“ (die Datenbank auf „healthy“), und die zweite Zeile antwortet mit
`{"status":"ok"}`. Im Log des Servers darf eine Warnung stehen, dass die LLM-Schranke nicht erreichbar ist; die
Warteschlange gibt es nur in einer größeren Installation, auf dem Mac brauchst du sie nicht.

Ist ein Port schon belegt, startet ein Dienst nicht. Die Oberfläche legst du mit `WEB_PORT=8081` in `.env` auf einen
anderen Port; die Datenbank braucht Port 5432 und die Websuche Port 8888 frei, beende also ein lokal laufendes PostgreSQL.

## 5. Das erste Bauteil

Öffne <http://localhost:8080>.

1. Leg unter **Container** einen Lagerort an, zum Beispiel deine Sortierbox. Er bekommt einen Code wie `T-001`, und das
   Etikett mit QR-Code kannst du gleich drucken.
2. Unter **Erfassen** lädst du ein Foto eines Bauteils oder Breakout-Boards hoch. Die erste Erkennung dauert länger,
   weil LM Studio das Modell erst lädt. Du bestätigst den Vorschlag, gibst die Menge an und wählst den Container.
3. Im **Assistenten** fragst du zum Beispiel „Kann ich ein Thermometer bauen?“. Was fehlt, legst du in die Einkaufsliste.

Klappt die Erkennung nicht, sieh in LM Studio unter **Developer** ins Log, ob die Anfrage ankommt, und vergleiche die
Modellnamen mit `lms ls`. Die Meldungen von Ohmventory selbst zeigt `docker compose logs -f api`.

## 6. Vom Handy aus

Im selben WLAN öffnest du auf dem Handy die Adresse aus `PUBLIC_BASE_URL`, also `http://<Adresse des Macs>:8080`. Fragt
macOS, ob Docker eingehende Verbindungen annehmen darf, erlaubst du das. Ein QR-Etikett auf einer Box öffnet von da an
direkt ihren Inhalt, und unter **Erfassen** nimmt das Handy das Foto gleich mit der Kamera auf.

Die Oberfläche hat kein eigenes Login. Stell sie deshalb nicht per Portfreigabe ins Internet.

## 7. Aktualisieren und anhalten

Eine neue Version holst du so; Bestand und Fotos liegen in Docker-Volumes und bleiben erhalten:

```sh
cd ~/Ohmventory
git pull
docker compose up -d --build
```

`docker compose stop` hält Ohmventory an, `docker compose start` startet es wieder. LM Studio muss laufen, damit
Erkennung und Assistent antworten; der Rest geht auch ohne. Wenn du mit `docker compose down -v` aufräumst, löscht das
auch Datenbank und Fotos.

Wie Ohmventory auf einem Proxmox-Server mit automatischen Updates läuft, steht im
[README des Projekts](https://github.com/Marcel-B/Ohmventory#installation-auf-proxmox-empfohlen).
