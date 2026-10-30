---
titel: Tonwerk-AI auf einem Mac einrichten
beschreibung: Von einem frischen Mac mit Apple Silicon bis zum ersten Song, erreichbar vom iPhone über Tailscale.
datum: 2026-10-30
reihenfolge: 1
---

## Was du brauchst

- einen Mac mit Apple Silicon und macOS 14 oder neuer, mindestens 16 GB Speicher (24 GB und mehr sind angenehm)
- rund 20 GB freien Platz
- für den Zugriff von unterwegs: [Tailscale](https://tailscale.com) auf dem Mac und dem iPhone

## 1. Einrichten mit einem Skript

Auf einem Mac, auf dem außer macOS nichts installiert ist, richtet ein Skript alles ein:

```sh
xcode-select --install
git clone https://github.com/Marcel-B/Tonwerk-AI.git ~/repos/Tonwerk-AI
~/repos/Tonwerk-AI/deploy/setup-mac.sh
```

Es prüft den Mac und installiert, was fehlt: Homebrew, uv, ffmpeg, Node.js und das .NET 10 SDK. Dann holt es YuE2 in einer geprüften Version, lädt die Modelle (etwa 7 GB), veröffentlicht Tonwerk-AI als Dienst und startet das Modell einmal zur Probe. Das Skript kann beliebig oft laufen; was schon da ist, überspringt es.

Mehr Funktionen kommen mit Optionen dazu, zum Beispiel `--voices` für andere Stimmen, `--images` für gemalte Cover, `--ace` für ACE-Step als zweites Songmodell oder `--all` für alles.

## 2. Vom iPhone aus erreichen

Der Server lauscht nur auf dem Mac selbst. Erreichbar wird er über Tailscale, nur für deine eigenen Geräte und mit HTTPS:

```sh
tailscale serve --bg --https=8443 5090
```

Danach öffnest du auf dem iPhone `https://<mac-name>.<tailnet>.ts.net:8443/` und legst die Seite über **Teilen → Zum Home-Bildschirm** ab. Mit `tailscale funnel` solltest du sie nicht ins offene Internet stellen, denn die Oberfläche hat kein eigenes Login.

## 3. Der erste Song

Auf der Seite **Erstellen** gibst du einen Stil ein (die Bausteine helfen dabei) und einen Songtext. Wenn du keinen hast, entwirft LM Studio einen aus ein paar Stichworten. Mit **Erzeugen** wandert der Auftrag in die Warteschlange, und den Fortschritt siehst du live. Fertige Songs liegen in der Bibliothek, wo du sie bewerten, als Logic-Projekt laden oder teilen kannst.

## 4. Updates

Am Ende schaltet `setup-mac.sh` automatische Updates ein. Alle fünf Minuten sieht ein Dienst nach neuen Versionen und spielt sie ein, sobald Tonwerk-AI gerade nichts rechnet:

```sh
~/repos/Tonwerk-AI/deploy/update.sh status
```

## Apps statt Browser

Für Mac, iPhone und iPad gibt es native Apps, die denselben Server steuern. Die Mac-App lädst du [als DMG](https://github.com/Marcel-B/Tonwerk-AI/releases/latest/download/Tonwerk-AI.dmg), wie du sie verbindest, steht auf [tonwerk.studio/ai](https://tonwerk.studio/ai/einrichtung.html).
