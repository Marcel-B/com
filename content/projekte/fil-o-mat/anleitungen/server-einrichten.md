---
titel: Den fil-O-mat-Server einrichten
beschreibung: Das Backend mit Web-Oberfläche in einem Proxmox-Container oder auf einem beliebigen Docker-Rechner aufsetzen, mit Tailscale für unterwegs, Updates per App und nächtlicher Sicherung in die Nextcloud.
datum: 2026-10-30
reihenfolge: 1
---

Der Server ist das Herz von fil-O-mat. Er hält Sorten, Spulen und Container für alle Geräte zusammen, fragt die Drucker
ab, bucht den Verbrauch und liefert die Web-Oberfläche aus. Er läuft als Docker-Container und braucht wenig: ein Kern
und 1 GB Speicher reichen. Diese Anleitung ist der erste von drei Teilen. Danach kommen
[die Apps](/projekte/fil-o-mat/apps-einrichten.html) und [der NFC-Leser am Drucker](/projekte/fil-o-mat/nfc-leser-bauen.html).

## Was du brauchst

- einen Rechner, der immer läuft und im selben Netz wie deine Drucker hängt, zum Beispiel einen
  [Proxmox](https://www.proxmox.com/)-Server, ein NAS mit Docker oder einen Raspberry Pi
- für den Weg mit Proxmox: Zugang zur Shell des Proxmox-Hosts als `root`
- optional: ein [Tailscale](https://tailscale.com)-Konto, wenn du auch von unterwegs zugreifen willst
- optional: eine Nextcloud für die nächtliche Sicherung

## 1. Container auf Proxmox anlegen

Das Skript `create-lxc.sh` erledigt alles in einem Rutsch. Es legt einen unprivilegierten Debian-12-Container an,
installiert darin Docker, holt fil-O-mat nach `/opt/fil-o-mat`, baut das Image und startet es. Lade es in der Shell
des Proxmox-Hosts herunter und starte es:

```sh
curl -fsSLO https://raw.githubusercontent.com/Marcel-B/fil-o-mat/main/deploy/proxmox/create-lxc.sh
bash create-lxc.sh
```

Ohne weitere Angaben bekommt der Container die nächste freie ID, den Namen `filomat` und seine Adresse per DHCP.
Alles lässt sich über Umgebungsvariablen vor dem Aufruf einstellen. Eine feste Adresse ist sinnvoll, weil die
Apps und die NFC-Leser sie später fest eingetragen bekommen:

```sh
CTID=150 IP=192.168.1.50/24 GATEWAY=192.168.1.1 bash create-lxc.sh
```

| Variable | Standard | Wofür |
| --- | --- | --- |
| `CTID` | nächste freie | ID des Containers |
| `CT_HOSTNAME` | `filomat` | Name des Containers |
| `IP`, `GATEWAY` | DHCP | feste Adresse, z. B. `192.168.1.50/24` |
| `STORAGE`, `BRIDGE` | `local-lvm`, `vmbr0` | Speicher und Netzwerk-Bridge |
| `DISK_GB`, `MEMORY_MB`, `CORES` | 8, 1024, 2 | Größe des Containers |
| `PORT` | 8080 | Port des Servers |
| `FILOMAT_API_KEY` | leer | Schlüssel, den Apps und Leser mitschicken müssen |
| `TAILSCALE`, `TS_AUTHKEY`, `TS_SERVE` | aus | Zugriff über Tailscale (siehe Schritt 3) |
| `NEXTCLOUD_WEBDAV_URL`, `NEXTCLOUD_USERNAME`, `NEXTCLOUD_APP_PASSWORD` | leer | nächtliche Sicherung (siehe Schritt 5) |

Der erste Lauf dauert ein paar Minuten, weil das Image gebaut wird. Am Ende steht die Adresse da, zum Beispiel
`Backend: http://192.168.1.50:8080`. Das Skript wartet, bis der Server antwortet, und zeigt sonst die letzten
Log-Zeilen.

Der API-Schlüssel ist ein einfacher Schutz: Ist er gesetzt, muss jede Anfrage ihn im Header `X-Api-Key` mitschicken.
Eine Anmeldung mit Benutzern gibt es nicht. Stell den Server deshalb nie offen ins Internet, sondern nimm für den
Zugriff von unterwegs Tailscale.

## 1b. Ohne Proxmox: auf einem Docker-Rechner

Auf jedem Rechner mit Docker und Docker Compose geht es auch von Hand. Das Image baut die Web-Oberfläche mit, deshalb
brauchst du das ganze Repository und nicht nur den Ordner `backend`:

```sh
git clone https://github.com/Marcel-B/fil-o-mat.git
cd fil-o-mat/backend
docker compose up -d --build
```

Einstellungen wie `FILOMAT_API_KEY` oder die Nextcloud-Zugangsdaten kommen in die Datei `backend/.env` neben der
`docker-compose.yml`. Die Datenbank liegt im Docker-Volume `filomat-data` und übersteht jedes Neubauen.

## 2. Prüfen, ob er läuft

Öffne im Browser `http://<adresse>:8080/`. Du siehst die Web-Oberfläche von fil-O-mat. Sie kann alles außer NFC:
Drucker mit Zustand, Sorten, Spulen, Container, Statistik, Meldungen, Sicherung und Update. Ist ein API-Schlüssel
gesetzt, trägst du ihn dort unter **Einstellungen** ein. Ein kurzer Test im Terminal geht so:

```sh
curl http://192.168.1.50:8080/health
```

Kommt eine Antwort, läuft der Server. Er legt seine Datenbank beim ersten Start selbst an.

## 3. Von unterwegs erreichen mit Tailscale

Im Heimnetz erreichen die Apps den Server direkt. Damit das auch unterwegs klappt, läuft Tailscale direkt im
Container. Bei einem neuen Container gibst du einfach `TAILSCALE=1` mit:

```sh
TAILSCALE=1 bash create-lxc.sh
```

Für einen Container, der schon läuft, gibt es ein eigenes Skript. Auch das läuft in der Shell des Proxmox-Hosts:

```sh
curl -fsSLO https://raw.githubusercontent.com/Marcel-B/fil-o-mat/main/deploy/proxmox/add-tailscale.sh
CTID=150 bash add-tailscale.sh
```

Es reicht das Tunnel-Gerät an den Container durch (dafür startet er einmal neu), installiert Tailscale und meldet
ihn im Tailnet an. Mit `TS_AUTHKEY=tskey-auth-…` geht das ohne Rückfrage, sonst zeigt es einen Link zum Anmelden.
Am Ende stehen die Adressen da, unter denen der Server im Tailnet erreichbar ist, etwa
`http://filomat.<dein-tailnet>.ts.net:8080`. Mit `TS_SERVE=1` gibt es zusätzlich HTTPS ohne Port; dafür müssen in
deinem Tailnet MagicDNS und HTTPS-Zertifikate eingeschaltet sein.

Die Drucker im Heimnetz erreicht der Server weiterhin direkt, Tailscale lenkt diesen Verkehr nicht um. Die
NFC-Leser kommen dagegen nicht ins Tailnet. Sie brauchen immer die Adresse im Heimnetz.

## 4. Updates

Im Container prüft ein Zeitplan alle 15 Minuten, ob es neue Versionen gibt. Die Apps zeigen das unter **Backend**
an, die Web-Oberfläche unter **Einstellungen**. Nach deiner Bestätigung holt der Server den neuen Stand, baut das Image
neu und startet sich neu. Lässt sich das neue Image nicht bauen, läuft die bisherige Version einfach weiter.

Von Hand geht es in der Shell des Proxmox-Hosts:

```sh
pct exec 150 -- /opt/fil-o-mat/deploy/updater/filomat-update.sh check   # nur nachsehen
pct exec 150 -- /opt/fil-o-mat/deploy/updater/filomat-update.sh apply   # aktualisieren
pct exec 150 -- journalctl -u filomat-update -n 50                      # Log des letzten Updates
```

Scheitert ein Update beim Bauen, ist oft kurz das Netz weg oder die Platte voll. Dann hilft im Container:

```sh
df -h /
cd /opt/fil-o-mat && git pull && cd backend && docker compose build && docker compose up -d
```

Ist die Platte fast voll, räumt `docker system prune -af` alte Images und den Build-Cache weg. Die Datenbank liegt in
einem Volume und bleibt dabei erhalten.

## 5. Nächtliche Sicherung in die Nextcloud

Jede Nacht um 3 Uhr packt der Server die Datenbank als ZIP und lädt sie per WebDAV in einen Ordner deiner Nextcloud.
Es entstehen sieben Tagesdateien (`filomat-mon.zip` bis `filomat-sun.zip`) und eine Datei pro Monat
(`filomat-2026-10.zip`). In der Nextcloud wird nie etwas gelöscht.

1. In der Nextcloud unter **Einstellungen → Sicherheit → Geräte & Sitzungen** ein App-Passwort anlegen.
2. Einen Ordner wie `Backups` anlegen. Den Unterordner `fil-o-mat` legt der Server selbst an.
3. Die drei Werte beim Anlegen des Containers mitgeben oder nachträglich in `/opt/fil-o-mat/backend/.env` eintragen.

```sh
NEXTCLOUD_WEBDAV_URL=https://cloud.example.de/remote.php/dav/files/<benutzer>/Backups/fil-o-mat
NEXTCLOUD_USERNAME=<benutzer>
NEXTCLOUD_APP_PASSWORD=<app-passwort>
```

Danach startest du den Server im Container neu und stößt eine Sicherung sofort an:

```sh
cd /opt/fil-o-mat/backend
docker compose up -d
curl -X POST http://localhost:8080/api/backup
curl http://localhost:8080/api/backup
```

Die zweite Abfrage zeigt, wie die letzte Sicherung lief. Dasselbe siehst du in der App unter **Backend**. Mit
API-Schlüssel brauchen beide `curl` noch `-H "X-Api-Key: …"`. Wie du eine Sicherung zurückspielst, steht im
[README des Backends](https://github.com/Marcel-B/fil-o-mat/blob/main/backend/README.md#sicherung-in-die-nextcloud).

## 6. Meldungen aufs Handy mit ntfy

Der Server kann dir über [ntfy](https://ntfy.sh) Bescheid geben, wenn ein Druck fertig ist oder abbricht, wenn eine
Spule für den laufenden Druck nicht reicht und wenn ein unbekanntes Plättchen in einem Leser steckt. Bei Bambu- und
Klipper-Druckern mit Kamera kommt ein Foto mit. Ein Thema auf ntfy.sh mit einem schwer zu erratenden Namen reicht,
etwa `https://ntfy.sh/filomat-7f3k2q`. Abonniere es in der ntfy-App und trag die Adresse in der fil-O-mat-App unter
**Drucker → Meldungen** ein. Dort schickt **Testmeldung schicken** eine Probe. Die ntfy-App kommt auch ohne Google-Dienste aus.

Weiter geht es mit [den Apps](/projekte/fil-o-mat/apps-einrichten.html).
