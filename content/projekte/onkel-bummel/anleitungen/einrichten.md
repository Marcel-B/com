---
titel: Onkel Bummel einrichten
beschreibung: Den eigenen Benachrichtigungsdienst in einem Proxmox-Container aufsetzen, mit Anmeldung über den Identity-Server, Zugriff über Tailscale, ersten Nachrichten aus Skripten und Grafana und der iPhone-App.
datum: 2026-11-04
reihenfolge: 1
---

Onkel Bummel nimmt Nachrichten von deinen Skripten und Diensten an, hebt sie mit Bildern auf und schickt sie als
Push aufs iPhone. Der Server läuft zu Hause in einem Container auf Proxmox und ist nur in deinem Tailnet erreichbar.
Diese Anleitung führt vom leeren Proxmox-Host bis zur ersten Nachricht auf dem Handy. Alle Einzelheiten stehen im
[README](https://github.com/Marcel-B/onkel-bummel#readme) und in der
[Spezifikation](https://github.com/Marcel-B/onkel-bummel/blob/main/docs/SPEC.md).

## Was du brauchst

- einen Proxmox-Host mit Zugang zur Shell als `root`; der Container braucht 2 Kerne, 1 GB Speicher und 8 GB Platte
- ein Tailscale-Konto
- einen Identity-Server mit OpenID Connect, der Rollen im Token mitgibt, etwa
  [Identity](https://github.com/Marcel-B/Identity), selbst im Tailnet erreichbar
- für die iPhone-App: einen Mac mit Xcode und ein Konto im Apple Developer Program
- optional: eine Nextcloud für die nächtliche Sicherung

Ohne Proxmox und Identity-Server geht es auch: [Onkel Bummel auf dem eigenen Rechner](/projekte/onkel-bummel/auf-dem-rechner.html)
startet den Server mit Docker und einem Zugangsschlüssel.

## 1. Tailnet vorbereiten

Schalte in der Admin-Konsole von Tailscale unter **DNS** MagicDNS und HTTPS-Zertifikate ein. Damit bekommt Onkel
Bummel eine Adresse der Form `https://onkel-bummel.<dein-tailnet>.ts.net` mit gültigem Zertifikat. Leg unter
**Settings → Keys** einen Auth Key an. Ohne Key zeigt das Skript später einen Link zum Anmelden.

## 2. Anmeldung im Identity-Server vorbereiten

Onkel Bummel hat keine eigenen Benutzer, sondern fragt den Identity-Server. Leg dort einmal an:

| Was | Werte |
| --- | --- |
| Scope `onkel-bummel-api` | Ressource bzw. Audience `onkel-bummel-api` |
| Rolle `onkel-bummel` | deinem eigenen Benutzer zuweisen |
| Client `onkel-bummel-web` | vertraulich, Authorization Code, Redirect `https://onkel-bummel.<dein-tailnet>.ts.net/auth/callback`, nach dem Abmelden `https://onkel-bummel.<dein-tailnet>.ts.net/auth/signed-out`, Scopes `profile` und `roles` |
| Client `onkel-bummel-ios` | öffentlich mit PKCE, Authorization Code und Refresh Token, Redirect `com.b-velop.onkel-bummel:/oauth/callback`, Scope `onkel-bummel-api` |

Merk dir das Secret von `onkel-bummel-web`, es kommt im nächsten Schritt in den Container.

## 3. Container anlegen

Das Skript `create-lxc.sh` legt einen unprivilegierten Debian-Container an, installiert Docker und Tailscale, holt
den Server und startet ihn. Starte es in der Shell des Proxmox-Hosts:

```sh
TS_AUTHKEY=tskey-auth-... \
OIDC_ISSUER=https://identity.<dein-tailnet>.ts.net \
OIDC_WEB_CLIENT_SECRET=<secret-von-onkel-bummel-web> \
bash <(curl -fsSL https://raw.githubusercontent.com/Marcel-B/onkel-bummel/main/deploy/proxmox/create-lxc.sh)
```

Ohne weitere Angaben bekommt der Container die nächste freie ID, den Namen `onkel-bummel` und seine Adresse per DHCP.
Weitere Variablen wie `CTID`, `IP` und `GATEWAY` stehen im
[README zu Proxmox](https://github.com/Marcel-B/onkel-bummel/blob/main/deploy/proxmox/README.md). Bricht das Skript ab,
rufst du es mit derselben `CTID=…` noch einmal auf; es macht dort weiter, wo es stehen geblieben ist.

Am Ende stehen die Adressen da. Öffne die App-Adresse im Browser: Du landest beim Identity-Server, und nach der
Anmeldung siehst du die noch leere Timeline. Die Einstellungen liegen danach im Container in
`/etc/onkel-bummel/onkel-bummel.env`. Nach einer Änderung dort übernimmt sie

```sh
pct exec <CTID> -- docker compose -f /opt/onkel-bummel/deploy/docker-compose.yml up -d
```

## 4. Die erste Nachricht schicken

Jeder Sender braucht einen Publish-Token. Leg ihn in der Web-Oberfläche unter **Verwaltung → Publish-Tokens** an und
gib die Topics an, an die er senden darf, oder `*` für alle. Der Token beginnt mit `ob_` und wird nur dieses eine Mal
angezeigt. Ein Topic entsteht mit seiner ersten Nachricht:

```sh
curl -H "Authorization: Bearer ob_…" -H "Content-Type: application/json" \
  -d '{"topic":"garage","title":"Tor","message":"Das Tor ist offen","priority":4,"tags":["warning"]}' \
  https://onkel-bummel.<dein-tailnet>.ts.net/api/v1/messages
```

Mit Bild und einem Button geht es als Formular:

```sh
curl -H "Authorization: Bearer ob_…" -F topic=kamera -F message="Bewegung an der Einfahrt" -F file=@snap.jpg \
  -F 'actions=[{"label":"Licht an","url":"http://haus/licht","method":"POST","clear":true}]' \
  https://onkel-bummel.<dein-tailnet>.ts.net/api/v1/messages
```

Die Nachricht erscheint sofort in der Web-Oberfläche. Den Button führt später der Server aus, nicht das Handy.

## 5. Grafana anbinden

Leg in Grafana einen Kontaktpunkt vom Typ **Webhook** an, mit der Adresse
`https://onkel-bummel.<dein-tailnet>.ts.net/api/v1/webhooks/grafana?topic=alarme`. Unter **Authorization Header**
kommt das Schema `Bearer` und als Credentials ein Token, der für das Topic `alarme` gilt. **Test** schickt eine
Probe.

## 6. Die iPhone-App

Die App gibt es nicht im App Store. Du baust sie mit Xcode und XcodeGen selbst:

```sh
brew install xcodegen
git clone https://github.com/Marcel-B/onkel-bummel
cd onkel-bummel/ios
xcodegen
open OnkelBummel.xcodeproj
```

Das Projekt ist auf Marcels Apple-Konto eingestellt. Für dein eigenes passt du Team, Bundle-ID, App Group und
Redirect-URI an: in `ios/project.yml`, in den Entitlements und im Code der App (die Fundstellen findest du mit einer
Suche nach `b-velop`). Die neue Redirect-URI kommt dann auch in den Client `onkel-bummel-ios`, die Bundle-ID in die
Einstellung `Apns__BundleId` des Servers. Beim ersten Start gibst du die
Server-Adresse ein oder scannst den QR-Code aus **Verwaltung → App einrichten**, meldest dich an und abonnierst die
Topics, die aufs Handy sollen. Die App erreicht den Server über Tailscale; am besten stellst du Tailscale auf dem
iPhone auf „On Demand“.

Damit Pushes ankommen, braucht der Server einen APNs-Schlüssel. Leg ihn im Apple-Developer-Konto unter
**Certificates, Identifiers & Profiles → Keys** an und kopier die `.p8`-Datei in den Container:

```sh
pct push <CTID> AuthKey_XXXXXXXXXX.p8 /etc/onkel-bummel/secrets/apns.p8
pct exec <CTID> -- chown root:1654 /etc/onkel-bummel/secrets/apns.p8
pct exec <CTID> -- chmod 640 /etc/onkel-bummel/secrets/apns.p8
```

Trag dann in `/etc/onkel-bummel/onkel-bummel.env` `Apns__KeyPath=/run/secrets/apns.p8`, `Apns__KeyId` und
`Apns__TeamId` ein und starte den Server wie in Schritt 3 neu. Die nächste Nachricht kommt als Mitteilung, Bilder
mit Vorschau.

## 7. Sicherung in die Nextcloud

Leg in der Nextcloud unter **Einstellungen → Sicherheit → Geräte & Sitzungen** ein App-Passwort an und trag in
`/etc/onkel-bummel/onkel-bummel.env` ein:

```sh
Backup__NextcloudWebDavUrl=https://cloud.example.de/remote.php/dav/files/<benutzer>/Backups/onkel-bummel
Backup__NextcloudUserName=<benutzer>
Backup__NextcloudAppPassword=<app-passwort>
Backup__Passphrase=<optional, verschlüsselt die Archive>
```

Der Ordner `Backups` muss es schon geben. Jede Nacht um 03:30 lädt der Server Datenbank und Anhänge als ZIP hoch, eines
pro Wochentag und eines pro Monat. Heb die Passphrase außerhalb des Containers auf, etwa im Passwortmanager. Wie du
eine Sicherung zurückspielst, steht im
[README zu Proxmox](https://github.com/Marcel-B/onkel-bummel/blob/main/deploy/proxmox/README.md#sicherung-in-die-nextcloud).

## Updates

Um Updates musst du dich nicht kümmern. Alle fünf Minuten sieht der Container nach, ob es eine neue Version gibt,
holt das fertige Image, sichert vorher die Datenbank und startet neu. Antwortet der Server danach nicht, laufen wieder
die vorige Version und die alte Datenbank. Was zuletzt passiert ist, zeigt

```sh
pct exec <CTID> -- journalctl -u onkel-bummel-update -n 30
```
