---
titel: Tonregal auf einem Mac neu aufsetzen
beschreibung: Von einem leeren Mac mit externer SSD bis zur laufenden Bibliothek mit Navidrome, Tailscale, nächtlichem Nextcloud-Backup und iPhone-App, auch zum Wiederherstellen nach einem Ausfall.
datum: 2026-10-30
reihenfolge: 1
---

Tonregal läuft als Dienst auf einem Mac im Heimnetz. Die Musik, die Datenbank, die App selbst und ihre Logs liegen auf
einer externen SSD, damit die interne Platte frei bleibt. Erreichbar ist alles nur über
[Tailscale](https://tailscale.com), also nur für deine eigenen Geräte. Diese Anleitung führt durch das Einrichten in
der Reihenfolge, in der die Teile aufeinander aufbauen. Wenn du nach einem Plattenausfall oder auf einem neuen Mac
wiederherstellst, holst du in Schritt 4 die Daten aus der Nextcloud zurück; alles andere ist gleich.

## Was du brauchst

- einen Mac mit Apple Silicon (die App wird für `osx-arm64` gebaut), der dauerhaft läuft, zum Beispiel einen Mac mini
- eine externe SSD für die Musik, groß genug für die ganze Sammlung
- ein [Tailscale](https://tailscale.com)-Konto, Tailscale auf dem Mac und auf dem iPhone
- eine Nextcloud mit einem App-Passwort für das Backup
- einen kostenlosen AcoustID-Schlüssel von [acoustid.org](https://acoustid.org/new-application) für das Erkennen per
  Fingerprint
- für die iPhone-App: Zugang zur TestFlight-Version oder ein eigenes Apple-Entwicklerkonto

## 1. Den Mac vorbereiten

Im Terminal die Entwicklerwerkzeuge, [Homebrew](https://brew.sh) und was der Build braucht installieren:

```sh
xcode-select --install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install git node rclone
brew install --cask dotnet-sdk
```

Tonregal braucht das .NET 10 SDK und Node.js 22 oder neuer; `dotnet --version` und `node --version` zeigen, ob das
passt. Den Rest (Chromaprint, rsgain, uv, ffmpeg, Navidrome) installieren die Skripte später selbst.

Dazu kommt Tailscale als App aus dem App Store oder von [tailscale.com](https://tailscale.com/download). Melde den Mac
in deinem Tailnet an und schalte unter **DNS** in der Tailscale-Verwaltung **HTTPS Certificates** ein, sonst kann
Tailscale später kein Zertifikat ausstellen.

Damit der Mac nicht einschläft: **Systemeinstellungen → Energie** (je nach Modell **Energie sparen**), den
Ruhezustand verhindern und nach einem Stromausfall automatisch starten lassen.

## 2. Die SSD einrichten

Formatiere die SSD im Festplattendienstprogramm als **APFS** und nenne sie `T7`. Die Skripte erwarten alles unter
`/Volumes/T7/Musik`:

```sh
mkdir -p /Volumes/T7/Musik
```

Eine anders benannte Platte geht auch: Dann setzt du vor jedem Skript `export MUSIC_ROOT=/Volumes/<Name>/Musik` und
musst die Pfade in dieser Anleitung entsprechend lesen. Einfacher ist der Name `T7`.

Unter `Musik` entstehen mit der Zeit diese Ordner:

| Ordner | Inhalt |
| --- | --- |
| `Inbox/` | neue Musik, die Tonregal erkennen und einsortieren soll |
| `Library/` | die fertige Bibliothek, in die nur Tonregal schreibt |
| `Altbestand/` | alte MP3-Kopien, die Tonregal nur liest (optional) |
| `app/` | die veröffentlichte App, `tonregal.db` und deine Einstellungen |
| `navidrome/` | Navidromes Einstellungen und Datenbank |
| `logs/`, `update/`, `tools/`, `backups/` | Logs, Stand der automatischen Updates, Analyse-Werkzeuge, Datenbank-Sicherungen vor jedem Update |

## 3. Den Quelltext holen

```sh
git clone https://github.com/Marcel-B/Tonregal.git ~/repos/Tonregal
cd ~/repos/Tonregal
```

Der Checkout bleibt auf `main`; die automatischen Updates aus Schritt 9 rollen nur von dort aus.

## 4. Daten aus dem Backup zurückholen (nur beim Wiederherstellen)

Richtest du Tonregal zum ersten Mal ein, überspringst du diesen Schritt.

Zuerst den Zugang zur Nextcloud einrichten, wie in Schritt 8 beschrieben (`rclone config create …`), dann prüfen, ob
die Sicherung da ist:

```sh
rclone lsd nextcloud:Musik            # zeigt Library und _state
rclone lsf --dirs-only nextcloud:Musik/_state
```

Unter `_state/` liegt pro Tag ein Ordner mit `tonregal.db` und `navidrome.db`, die letzten sieben Tage. Nimm den
neuesten und hol Datenbanken und Bibliothek zurück:

```sh
stand=$(rclone lsf --dirs-only nextcloud:Musik/_state | sort | tail -n1)
mkdir -p /Volumes/T7/Musik/{app,navidrome,Library}
rclone copy "nextcloud:Musik/_state/$stand" /Volumes/T7/Musik/app/ --include tonregal.db
rclone copy "nextcloud:Musik/_state/$stand" /Volumes/T7/Musik/navidrome/ --include navidrome.db
rclone copy nextcloud:Musik/Library /Volumes/T7/Musik/Library --progress
```

Die Bibliothek kann je nach Größe und Leitung Stunden dauern; der Befehl lässt sich abbrechen und erneut starten, er
macht dort weiter. Die Pfade müssen dieselben sein wie vorher (`/Volumes/T7/Musik/…`), weil Navidrome sie in seiner
Datenbank absolut speichert.

Was zurückkommt: alle Musikdateien mit Tags, Covern, Songtexten (`.lrc`) und Smart Playlists, aus `tonregal.db` die
Import-Geschichte, die Schlüssel für die Schnittstelle (etwa für Tonwerk-AI) und die Smart-Playlist-Regeln, aus
`navidrome.db` dein Navidrome-Konto, Sterne und Wiedergabezahlen. Nicht in der Sicherung sind die Inbox, der Altbestand
und `appsettings.Production.json`; die Werte daraus (AcoustID-Schlüssel, Navidrome-Passwort) hebst du am besten im
Passwortmanager auf.

Fehlt `tonregal.db` ganz, ist das kein Drama: Die Datenbank ist nur ein Index, Tonregal liest beim Start die Bibliothek
ein und baut ihn neu auf.

## 5. Navidrome einrichten

Navidrome liefert im Hintergrund das Audio, zählt Wiedergaben und hält die Sterne. Tailscale muss dafür schon laufen,
weil Navidrome auf der Tailscale-Adresse des Macs lauscht:

```sh
./deploy/navidrome/setup-navidrome.sh
```

Das Skript installiert Navidrome und ffmpeg, legt die Ordner an, schreibt `navidrome.toml` und richtet den Dienst
`org.navidrome.server` ein.

**Festplattenvollzugriff:** Beim ersten Mal startet der Dienst meist nicht, weil macOS ihm die externe SSD verweigert.
Das Skript sagt dann, welches Programm die Freigabe braucht. Unter **Systemeinstellungen → Datenschutz & Sicherheit →
Festplattenvollzugriff** mit **+** genau diesen Pfad hinzufügen (im Dateidialog führt **Cmd+Shift+G** zu einem Pfad) und
das Skript noch einmal starten. Nach einem `brew upgrade navidrome` ändert sich der Pfad; dann die Freigabe erneuern.

Zum Schluss nennt das Skript Navidromes Adresse. Öffne sie im Browser und lege beim ersten Aufruf den Admin-Benutzer an.
Nach einer Wiederherstellung gibt es ihn schon.

## 6. Tonregal ausrollen

```sh
./deploy/deploy-tonregal.sh
```

Das Skript installiert Chromaprint, rsgain, uv und rclone, legt eine Python-Umgebung für die Tempo- und Tonart-Analyse
auf der SSD an, baut Tonregal mit seiner Web-Oberfläche, kopiert es nach `Musik/app` und richtet den Dienst
`de.bvelop.tonregal` ein. Tonregal lauscht nur auf `http://localhost:5100`. Am Ende fragt das Skript
`/api/health` ab und bricht mit einer Meldung ab, wenn Tonregal nicht antwortet. Auch hier kann beim ersten Mal die
Freigabe für die SSD fehlen; dann wie in Schritt 5 den genannten Pfad (`…/Musik/app/Tonregal.Web`) freigeben und das
Skript wiederholen.

Deine eigenen Einstellungen kommen in `/Volumes/T7/Musik/app/appsettings.Production.json`. Das Skript lässt diese Datei
bei jedem Update in Ruhe, und sie gehört nie ins Repository:

```json
{
  "Tonregal": {
    "Metadata": { "AcoustIdApiKey": "<dein AcoustID-Schlüssel>" },
    "Navidrome": { "User": "<Navidrome-Admin>", "Password": "<Passwort>" }
  }
}
```

Ohne den AcoustID-Schlüssel erkennt Tonregal keine Stücke am Fingerprint, ohne Navidrome-Zugang gehen Sterne und
Wiedergabezahlen nicht. Nach einer Änderung den Dienst neu starten:

```sh
launchctl kickstart -k gui/$(id -u)/de.bvelop.tonregal
curl http://localhost:5100/api/health
```

## 7. Über Tailscale erreichbar machen

Tailscale Serve stellt Tonregal mit HTTPS ins Tailnet:

```sh
tailscale serve --bg 5100
tailscale serve status
```

Findet das Terminal `tailscale` nicht, liegt das Programm in der App unter
`/Applications/Tailscale.app/Contents/MacOS/Tailscale`. Danach ist Tonregal auf all deinen Geräten im Tailnet unter
`https://<mac-name>.<tailnet>.ts.net` erreichbar, ohne Port. Den genauen Namen zeigt `tailscale serve status`. Prüfen
kannst du das von einem anderen Gerät:

```sh
curl https://<mac-name>.<tailnet>.ts.net/api/health
```

Mit `tailscale funnel` solltest du Tonregal nicht ins offene Internet stellen, denn die Oberfläche hat kein eigenes
Login. Auf dem iPhone kannst du die Seite in Safari über **Teilen → Zum Home-Bildschirm** wie eine App ablegen.

## 8. Das nächtliche Backup einrichten

Tonregal spiegelt jede Nacht um 03:00 die Bibliothek in die Nextcloud und legt Kopien beider Datenbanken daneben. Lege
in der Nextcloud einen Nutzer mit App-Passwort an, der nur den Ordner `Musik` sieht, und gib rclone den Zugang. Er
bleibt in `~/.config/rclone/rclone.conf` auf dem Mac:

```sh
rclone config create nextcloud webdav vendor=nextcloud \
  url=https://<deine-nextcloud>/remote.php/dav/files/<nutzer>/ user=<nutzer> pass='<app-passwort>'
rclone lsd nextcloud:Musik    # muss ohne Fehler antworten
```

Ein erster Lauf geht sofort mit **Jetzt sichern** auf der Übersicht oder im Terminal:

```sh
curl -X POST http://localhost:5100/api/backup/run
```

Die Übersicht zeigt die letzten Läufe; zwei Fehlschläge hintereinander werden rot. Würde ein Lauf mehr als 500 Dateien
in der Nextcloud löschen, bricht er ab, damit eine leere oder falsch eingehängte Platte die Sicherung nicht leert.

## 9. Automatische Updates einschalten

Ab jetzt soll der Mac neue Versionen selbst einspielen. Aus einem Terminal, in dem `brew`, `dotnet` und `npm`
funktionieren (der Befehl merkt sich dessen `PATH`):

```sh
./deploy/update-tonregal.sh on
```

Ein Hintergrunddienst schaut alle fünf Minuten nach neuen Commits auf `main`. Gibt es welche, wartet er, bis gerade
nichts importiert, analysiert oder gesichert wird, sichert `tonregal.db` nach `Musik/backups/deploy/` und rollt mit
`deploy-tonregal.sh` aus.

Der Dienst läuft als `/bin/bash` und braucht dafür einmal **Festplattenvollzugriff**: in den Systemeinstellungen wie in
Schritt 5 mit **+**, **Cmd+Shift+G** und `/bin/bash`. Ob es geklappt hat, zeigt

```sh
./deploy/update-tonregal.sh status
cat /Volumes/T7/Musik/update/deployed    # der zuletzt ausgerollte Commit
```

Steht dort nach ein paar Minuten kein Log und kein Commit, fehlt meist die Freigabe für `/bin/bash`.

## 10. Kurze Befehle für den Alltag

Die Shell-Funktionen kommen in `~/.zshrc`:

```sh
echo 'source ~/repos/Tonregal/deploy/shell/tonregal.zsh' >> ~/.zshrc
```

Danach gibt es `tonregal-status`, `tonregal-log`, `tonregal-restart`, `tonregal-backup-now` und `tonregal-update`.
Auf einem zweiten Mac laufen dieselben Befehle per SSH auf dem Tonregal-Mac; dafür `TONREGAL_HOST` auf dessen Namen
setzen.

## 11. iPhone, iPad und Tonwerk-AI verbinden

- **App:** Installiere Tonregal über TestFlight. Mit Tailscale an trägst du beim ersten Start die Adresse aus Schritt 7
  ein, `https://<mac-name>.<tailnet>.ts.net`. Wer die App selbst bauen will, findet die Schritte im
  [README der App](https://github.com/Marcel-B/Tonregal/blob/main/apple/README.md).
- **Tonwerk-AI:** Die Seite **Verbindungen** in Tonregal zeigt den Schlüssel für `tonwerk-ai` und kopiert die zwei
  Zeilen, die in Tonwerk-AIs Einstellungen gehören. Nach einer Wiederherstellung mit `tonregal.db` gilt der alte
  Schlüssel weiter; ohne sie erzeugst du dort einen neuen und trägst ihn in [Tonwerk-AI](/projekte/tonwerk-ai/) ein.

## Prüfen, ob alles läuft

- `tonregal-status` zeigt beide Dienste als `running` und die Antwort von `/api/health`.
- Die Oberfläche öffnet sich unter `https://<mac-name>.<tailnet>.ts.net`, die Bibliothek zeigt deine Alben.
- Ein Stück in `Musik/Inbox` taucht nach etwa zehn Sekunden auf der Inbox-Seite auf.
- Am nächsten Morgen steht auf der Übersicht ein erfolgreiches Backup.

Läuft ein Dienst nicht, hilft fast immer der Blick in sein Log (`tonregal-log` oder
`~/Library/Logs/Tonregal/`). Steht dort „Operation not permitted“, fehlt die Freigabe für die externe SSD. Startet
Tonregal ohne eingehängte SSD, wartet der Dienst, bis sie wieder da ist, und legt nie eine leere Bibliothek auf der
internen Platte an. Mehr zu den einzelnen Funktionen steht im
[README von Tonregal](https://github.com/Marcel-B/Tonregal#readme).
