---
name: Tonregal
untertitel: Die eigene Musikbibliothek
reihenfolge: 40
kurz: 'Sortiert neue Musik ein: Fingerprint, MusicBrainz, Cover, Tags, feste Ordnerstruktur, Dubletten, BPM und Tonart. Gestreamt
  wird mit Navidrome.'
einleitung: 'Tonregal verwaltet die eigene Musiksammlung: Was in die Inbox kommt, wird erkannt, getaggt und an seinen festen
  Platz in der Bibliothek gelegt.'
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
  wert: Mac mini im Heimnetz, Zugriff über Tailscale
- name: Lizenz
  wert: GNU AGPL v3 oder später
---

## Was es kann

- Die **Inbox überwachen** und neue Alben per Audio-Fingerprint und MusicBrainz erkennen.
- **Cover und Tags** schreiben und die Dateien in eine feste Ordnerstruktur einsortieren: `Künstler/Jahr - Album/NN - Titel`.
- **Dubletten** erkennen, **BPM, Tonart und ReplayGain** analysieren.
- Alles in die **Nextcloud** sichern.
- Songs aus Tonwerk-AI direkt übernehmen.
- Gestreamt wird die fertige Bibliothek von Navidrome über die Subsonic-API; dazu gibt es einen nativen Player für iPhone und iPad.

## Leitprinzip

Die Dateien sind die Wahrheit. Alle Metadaten stehen in den Tags der Audiodatei, die Datenbank ist nur ein Index und lässt sich jederzeit aus der Bibliothek neu aufbauen.

## Technik

ASP.NET Core (.NET 10) mit EF Core und SQLite, SignalR für Live-Updates, ein Vue-3-Frontend mit Pinia, Tailwind CSS und PrimeVue, eine SwiftUI-App. Fingerprint, Analyse und Sicherung laufen über eigenständige Werkzeuge wie Chromaprint, ffmpeg, rsgain und rclone.
