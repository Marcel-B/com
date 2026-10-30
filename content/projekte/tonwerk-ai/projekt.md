---
name: Tonwerk-AI
untertitel: Musik mit lokalen KI-Modellen
reihenfolge: 10
kurz: Songs, Stimmen, Cover und Videos mit Modellen, die auf dem eigenen Mac laufen, bedient vom Handy, aus dem Browser oder
  mit nativen Apps.
einleitung: Eine Oberfläche für Musikmodelle, die auf dem eigenen Mac mit Apple Silicon rechnen. Sie lässt sich unterwegs
  vom iPhone aus bedienen, über Tailscale und ohne Cloud.
technik:
- ASP.NET Core
- Vue 3
- SwiftUI
- Python
- MLX
links:
- text: Tonwerk-AI auf tonwerk.studio
  url: https://tonwerk.studio/ai/
- text: Mac-App laden (DMG)
  url: https://github.com/Marcel-B/Tonwerk-AI/releases/latest/download/Tonwerk-AI.dmg
- text: Quelltext auf GitHub
  url: https://github.com/Marcel-B/Tonwerk-AI
steckbrief:
- name: Plattform
  wert: Mac mit Apple Silicon als Server; Browser, iPhone, iPad, Mac als Oberfläche
- name: Lizenz
  wert: PolyForm Noncommercial 1.0.0
app:
  kategorie: MultimediaApplication
  plattformen: macOS, iOS, iPadOS, Web
  url: https://tonwerk.studio/ai/
  kostenlos: true
---

## Was es kann

- **Songs erzeugen** mit YuE2 und ACE-Step 1.5: Stil, Songtext und Partitur rein, Fortschritt live verfolgen, Entwürfe später in voller Qualität rendern.
- **Songtexte** entwerfen und überarbeiten, mit einem lokalen Modell in LM Studio oder mit Claude, auch aus einem Foto.
- **Als Logic-Projekt laden:** Die Partitur wird zu MIDI und einem fertigen Logic-Pro-Projekt mit Audiospur, Begleitstimmen und Klängen.
- **Stimmen und Stems:** Songs in Stems zerlegen, mit einer anderen Stimme neu singen lassen (Seed-VC), Audio zu MIDI mit Basic Pitch.
- **Sprachlabor und Gesang:** lokale Text-to-Speech-Modelle ausprobieren, Noten und Text mit SoulX-Singer singen lassen.
- **Cover und Musikvideos:** Cover mit lokalen Bildmodellen malen, Videos mit Analyzer, Songtext-Untertiteln und Fotos im Takt schneiden.
- **Bibliothek und Player:** Bewertungen, Playlists (auch offline), Benachrichtigungen, Datensicherung in die Nextcloud.
- **Apps** für Mac, iPhone und iPad, die denselben Server steuern.

Alles, was die Modelle erzeugen, ist maschinenlesbar als KI-erzeugt gekennzeichnet.

## Technik

ASP.NET Core Minimal API (.NET 10) mit SQLite, ein Vue-3-Frontend mit PrimeVue, native Apps in SwiftUI. Die Modelle laufen als Python-Prozesse daneben (PyTorch, MLX, acestep.cpp), immer nur so viele, wie in den Speicher passen.
