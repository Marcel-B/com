---
name: Tonwerk-AI
untertitel: Musik mit lokalen KI-Modellen
reihenfolge: 10
vision: Eigene Songs machen, ohne dass etwas davon in eine Cloud muss. Tonwerk-AI soll das Studio sein, in dem KI-Modelle auf
  dem eigenen Mac komponieren, singen, malen und schneiden, und das sich dabei so leicht bedienen lässt wie eine Musik-App
  auf dem Handy.
kurz: Songs, Stimmen, Cover und Videos mit Modellen, die auf dem eigenen Mac laufen, bedient vom Handy, aus dem Browser oder
  mit nativen Apps.
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
features:
- titel: Songs erzeugen
  wozu: Aus einer Idee wird ein Song. Stil und Songtext reichen, wer mag, gibt eine Partitur mit.
  verhalten:
  - Zwei Songmodelle stehen zur Wahl, YuE2 und ACE-Step 1.5.
  - Der Fortschritt jedes Songs ist live zu sehen, auch nach dem Neuladen der Seite.
  - Ein Entwurf lässt sich später in voller Qualität rendern.
- titel: Eine Warteschlange für alles
  wozu: Ein Auftrag wird nie abgelehnt, nur weil gerade ein anderes Modell rechnet.
  verhalten:
  - Es ist immer nur so viel geladen, wie in den Speicher passt; die anderen Aufträge warten.
  - Wartende Aufträge überstehen einen Neustart.
- titel: Songtexte
  wozu: Ein Songtext im richtigen Format, auch wenn man gerade keinen hat.
  verhalten:
  - Entwürfe auf Deutsch oder Englisch aus Stichworten, lokal mit LM Studio oder mit Claude.
  - Ein Foto kann die Stichworte ersetzen oder ergänzen.
  - Eine Überarbeitung ändert nur, was verlangt war; der Rest bleibt Wort für Wort stehen.
- titel: Als Logic-Projekt laden
  wozu: Ein erzeugter Song soll in Logic Pro weiterleben, nicht nur als Audiodatei.
  verhalten:
  - Die Partitur wird zu MIDI und einem fertigen Logic-Pro-Projekt mit der Audiospur.
  - Auf Wunsch kommen Begleitstimmen dazu, parallel, als Bordun oder als Chor.
  - Die Partitur gibt es auch als MusicXML.
- titel: Stimmen und Stems
  wozu: Einen Song in seine Teile zerlegen und mit einer anderen Stimme neu singen lassen.
  verhalten:
  - Songs und eigene Dateien werden in Stems getrennt, der Gesang auch ohne Hall.
  - Seed-VC singt den Gesang mit einer Referenzstimme neu; der Rest wird wieder daruntergemischt.
  - Aus einer Spur wird MIDI mit Basic Pitch.
- titel: Sprachlabor und Gesang
  wozu: Lokale Sprach- und Gesangsmodelle ausprobieren, mit der eigenen Stimme.
  verhalten:
  - Mehrere Text-to-Speech-Modelle lassen sich mit demselben Text vergleichen.
  - Eine eigene Aufnahme dient als Stimme zum Klonen.
  - SoulX-Singer singt Noten und Text.
- titel: Cover und Musikvideos
  wozu: Ein Song soll mit Bild und Video veröffentlicht werden können.
  verhalten:
  - Cover malen lokale Bildmodelle, auf Wunsch im Stil eigener Vorlagen.
  - Videos zeigen Analyzer und Songtext-Untertitel oder Fotos, im Takt geschnitten.
  - Zum Teilen gibt es eine kleine Fassung, zum Hochladen die volle.
- titel: Bibliothek und Player
  wozu: Hören, bewerten und wiederfinden, was entstanden ist, auch unterwegs.
  verhalten:
  - Sterne, Notizen, Suche und Playlists, die auch offline spielen.
  - Eine Benachrichtigung meldet, wenn ein Song fertig ist.
  - Jede Nacht geht eine Sicherung in die Nextcloud.
- titel: Apps für Mac, iPhone und iPad
  wozu: Dieselbe Arbeit nativ statt im Browser.
  verhalten:
  - Die Mac-App ist signiert und aktualisiert sich selbst.
  - iPhone und iPad bekommen die App über TestFlight.
  - Ohne eigenen Server lässt sich eine Demo ausprobieren.
- titel: Als KI-erzeugt gekennzeichnet
  wozu: Es soll immer klar sein, was von einem Modell stammt.
  verhalten:
  - Audio, Videos und gemalte Cover tragen die Kennzeichnung maschinenlesbar in ihren Metadaten.
  - Eigene Aufnahmen, Fotos, MIDI und Partituren bleiben ungekennzeichnet.
roadmap:
  jetzt:
  - ACE-Step, Singen mit SoulX-Singer, gemalte Cover, Fotovideos und Songtext mit Zeitmarken auf dem Mac mit den echten
    Modellen prüfen
  - Ein zweiter Mac als Helfer für Aufträge
  als_naechstes:
  - Eine gesungene Fassung statt der Originalstimme ins Logic-Projekt übernehmen
  - 'Lokalisierung: die Apps für Mac, iPhone und iPad auch auf Englisch (die Web-Oberfläche kann es schon)'
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

## Technik

ASP.NET Core Minimal API (.NET 10) mit SQLite, ein Vue-3-Frontend mit PrimeVue, native Apps in SwiftUI. Die Modelle laufen
als Python-Prozesse daneben (PyTorch, MLX, acestep.cpp), immer nur so viele, wie in den Speicher passen.
