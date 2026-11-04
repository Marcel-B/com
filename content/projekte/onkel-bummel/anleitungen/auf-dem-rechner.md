---
titel: Onkel Bummel auf dem eigenen Rechner
beschreibung: Den Benachrichtigungsdienst ohne Identity-Server mit Docker starten, mit dem Zugangsschlüssel anmelden und die erste Nachricht aus einem Skript schicken.
datum: 2026-11-04
reihenfolge: 2
---

Für Onkel Bummel brauchst du weder Proxmox noch einen eigenen Identity-Server. Auf jedem Rechner mit Docker läuft der
Server mit einem einzigen Befehl, und angemeldet wird mit einem Zugangsschlüssel, den der Server selbst anlegt. Das
reicht, um Nachrichten aus Skripten und Diensten zu sammeln, im Browser zu lesen und zu durchsuchen. Wie der Betrieb
mit Identity-Server, Tailscale und iPhone-App aussieht, steht in [Onkel Bummel einrichten](/projekte/onkel-bummel/einrichten.html).

## Was du brauchst

- einen Rechner mit Docker, unter macOS oder Windows etwa Docker Desktop
- ein Terminal

## 1. Server starten

Leg einen Ordner an, hol die Compose-Datei hinein und starte den Server:

```sh
mkdir onkel-bummel && cd onkel-bummel
curl -fsSLO https://raw.githubusercontent.com/Marcel-B/onkel-bummel/main/deploy/eigener-server/docker-compose.yml
docker compose up -d
```

Docker lädt das fertige Image und startet den Server. Datenbank und Bilder liegen in einem Docker-Volume und bleiben
auch nach einem Neustart oder Update erhalten.

## 2. Mit dem Zugangsschlüssel anmelden

Beim ersten Start legt der Server einen Zugangsschlüssel an und schreibt ihn einmal ins Log:

```sh
docker compose logs onkel-bummel | grep Zugangsschlüssel
```

Der Schlüssel beginnt mit `obk_`. Heb ihn im Passwortmanager auf. Der Server speichert nur eine Prüfsumme davon und
kann ihn dir nicht noch einmal zeigen. Öffne dann http://localhost:8080 im Browser, gib den Schlüssel ein, und du siehst
die noch leere Timeline.

Ist der Schlüssel weg, legst du einen neuen an. Der alte gilt danach nicht mehr, und jeder Browser muss sich neu
anmelden:

```sh
docker compose exec onkel-bummel dotnet OnkelBummel.Api.dll --new-access-key
```

## 3. Die erste Nachricht schicken

Skripte senden nicht mit dem Zugangsschlüssel, sondern jedes mit einem eigenen Publish-Token. Leg ihn in der
Web-Oberfläche unter **Verwaltung → Publish-Tokens** an und gib die Topics an, an die er senden darf, oder `*` für alle.
Der Token beginnt mit `ob_` und wird nur einmal angezeigt.

```sh
curl -H "Authorization: Bearer ob_…" -H "Content-Type: application/json" \
  -d '{"topic":"test","title":"Hallo","message":"Die erste Nachricht","tags":["tada"]}' \
  http://localhost:8080/api/v1/messages
```

Die Nachricht erscheint sofort im Browser. Bilder, Buttons und den Webhook für Grafana beschreibt
[Onkel Bummel einrichten](/projekte/onkel-bummel/einrichten.html) ab Schritt 4; dort ersetzt du die Tailnet-Adresse
durch `http://localhost:8080`.

## 4. Von anderen Geräten erreichen

So, wie die Compose-Datei eingestellt ist, antwortet der Server nur auf dem eigenen Rechner. Sollen andere Geräte
senden oder lesen, änderst du unter `ports` die Zeile auf `"8080:8080"` und startest mit `docker compose up -d` neu.
Der Zugangsschlüssel geht dann aber unverschlüsselt durchs Netz. Setz deshalb HTTPS davor, etwa mit Tailscale oder einem
Reverse Proxy, bevor du den Server außerhalb deines Rechners erreichbar machst.

## Was noch nicht geht

Die iPhone-App meldet sich bisher nur über einen Identity-Server an, und Pushes aufs iPhone braucht einen
APNs-Schlüssel aus dem Apple-Konto, zu dem die App gehört. Ohne Identity-Server liest du deine Nachrichten deshalb im
Browser, auf dem Handy auch dort.

## Updates

Eine neue Version holst du im selben Ordner mit:

```sh
docker compose pull
docker compose up -d
```
