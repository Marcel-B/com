---
name: Tonregal
untertitel: Die eigene Musikbibliothek
reihenfolge: 40
kurz: 'Sortiert neue Musik ein (Fingerprint, MusicBrainz, Cover, Tags, feste Ordner), analysiert BPM und Tonart und spielt
  alles im eigenen Player ab, im Browser und auf dem iPhone.'
einleitung: 'Tonregal verwaltet die eigene Musiksammlung: Was in die Inbox kommt, wird erkannt, getaggt und an seinen festen
  Platz in der Bibliothek gelegt. Abgespielt wird im eigenen Web-Player und in einer App fürs iPhone.'
technik:
- ASP.NET Core
- Vue 3
- SwiftUI
- SQLite
links:
- text: Quelltext auf GitHub
  url: https://github.com/Marcel-B/Tonregal
steckbrief:
- name: Plattform
  wert: Mac mini im Heimnetz, Web und iPhone, Zugriff nur über Tailscale
- name: Lizenz
  wert: GNU AGPL v3 oder später
---

## Was es kann

### Einsortieren

- Die **Inbox überwachen**: Neue Dateien und Ordner (auch per Drag & Drop im Browser hochgeladen) werden per
  Audio-Fingerprint (AcoustID) und MusicBrainz erkannt. Eindeutige Treffer sind sofort bereit, alles andere landet mit
  Begründung in einer Prüfliste, die sich auch per Tastatur abarbeiten lässt.
- Beim **Übernehmen** schreibt Tonregal Tags und Cover und legt die Datei in eine feste Ordnerstruktur:
  `Künstler/Jahr - Album/NN - Titel`. Das Original wird erst gelöscht, wenn die neue Datei geprüft ist.
- Ein **Altbestand** alter MP3-Kopien lässt sich in einem Rutsch abgleichen, ohne dass dort etwas verändert wird.
- **Dubletten** findet Tonregal über gleiche Dateien, gleiche Aufnahmen oder gleiche Titel mit gleicher Länge. Man hört
  jede Fassung kurz an und behält die bessere; der Rest geht für 30 Tage in einen Papierkorb.

### Analysieren und sichern

- Nachts bestimmt eine **Analyse** BPM und Tonart jedes Stücks und gleicht die Lautstärke an (ReplayGain), alles direkt in
  die Tags.
- Jede Nacht spiegelt ein **Backup** die Bibliothek und die Datenbanken in die Nextcloud, mit einer Sperre gegen
  versehentliches Löschen bei einer leeren Platte.

### Hören

- Ein **Web-Player** mit Warteschlange, Steuerung über Sperrbildschirm und Kopfhörertasten, Sternebewertung, Zufall für
  Album, Interpret oder die ganze Bibliothek und Wiederholen. Im iPhone-Safari lässt er sich auf den Home-Bildschirm legen.
- **Songtexte** laufen mit, wenn es synchronisierte gibt; ein Tipp auf eine Zeile springt dorthin. Sie kommen aus der
  Datei selbst, einer `.lrc` daneben oder von [lrclib.net](https://lrclib.net).
- **Smart Playlists** nach Regeln wie BPM-Bereich, Tonart (auch passende Tonarten zum Mixen), Genre, neu, nie gehört
  oder Sterne. Tonregal spielt sie selbst ab.
- **Download** eines Titels als Originaldatei oder eines ganzen Albums als ZIP.
- Eine **App fürs iPhone und iPad** (SwiftUI), die im Hintergrund, im Kontrollzentrum, mit AirPods und AirPlay zuverlässig
  weiterspielt, mit Songtexten, Sternen und Zufall.

### Verbunden

- Über eine **Schnittstelle zum Übernehmen** kommen eigene Stücke ohne Abgleich direkt in die Bibliothek, zum Beispiel
  Songs aus [Tonwerk-AI](/projekte/tonwerk-ai/) mit Cover, Songtext, Tempo und Tonart. Die Seite *Verbindungen* zeigt
  und erneuert den Schlüssel dafür.

## Leitprinzip

Die Dateien sind die Wahrheit. Alle Metadaten stehen in den Tags der Audiodatei, die Datenbank ist nur ein Index und
lässt sich jederzeit aus der Bibliothek neu aufbauen.

## Technik

ASP.NET Core (.NET 10) mit EF Core und SQLite, SignalR für Live-Updates, ein Vue-3-Frontend mit Pinia, Tailwind CSS und
PrimeVue, eine SwiftUI-App. Fingerprint, Analyse und Sicherung laufen über eigenständige Werkzeuge wie Chromaprint,
librosa, ffmpeg, rsgain und rclone. Im Hintergrund zählt Navidrome die Wiedergaben und hält die Sterne. Neue Versionen
spielt der Mac mini von selbst ein, sobald gerade nichts importiert, analysiert oder gesichert wird; die iPhone-App geht
dabei automatisch an TestFlight.
