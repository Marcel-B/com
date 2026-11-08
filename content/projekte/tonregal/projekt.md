---
name: Tonregal
untertitel: Die eigene Musikbibliothek
reihenfolge: 40
vision: Die eigene Musiksammlung soll sich so bequem anfühlen wie ein Streamingdienst und trotzdem ganz die eigene bleiben.
  Tonregal räumt neue Musik von selbst ein, kennt jedes Stück genau und spielt es überall ab, wo man hört.
kurz: 'Sortiert neue Musik ein (Fingerprint, MusicBrainz, Cover, Tags, feste Ordner), analysiert BPM und Tonart und spielt
  alles im eigenen Player ab, im Browser und auf dem iPhone.'
technik:
- ASP.NET Core
- Vue 3
- SwiftUI
- SQLite
links:
- text: Quelltext auf GitHub
  url: https://github.com/Marcel-B/Tonregal
features:
- titel: Inbox
  wozu: Neue Musik ablegen und nicht mehr von Hand taggen und sortieren.
  verhalten:
  - Neue Dateien und Ordner, auch per Drag & Drop im Browser hochgeladen, werden per Audio-Fingerprint (AcoustID) und
    MusicBrainz erkannt.
  - Eindeutige Treffer sind sofort bereit, alles andere landet mit Begründung in einer Prüfliste.
  - Die Prüfliste lässt sich per Tastatur abarbeiten und bleibt dank Seiten auch bei tausend Dateien flüssig.
  - "*Alle zu prüfenden übernehmen* fasst die Prüfliste nach Grund zusammen, etwa „Dauer passt zu keinem Treffer“. Nach
    einer Bestätigung gehen die gewählten Gründe mit ihrem Vorschlag in die Bibliothek, Dateien ohne Vorschlag auf Wunsch
    mit ihren eigenen Tags. Jede Datei wird dabei noch einmal geprüft."
- titel: Übernehmen
  wozu: Jedes Stück liegt an seinem festen Platz, richtig getaggt und mit Cover.
  verhalten:
  - Tonregal schreibt Tags und Cover und legt die Datei unter `Künstler/Jahr - Album/NN - Titel` ab.
  - Das Original wird erst gelöscht, wenn die neue Datei geprüft ist.
  - Scheitert die Übernahme, steht der Grund gesammelt über der Liste, und die Datei lässt sich mit ihren eigenen Tags
    übernehmen.
  - Beschädigte alte Dateien (ein kaputtes Cover im Tag, Lücken vor dem Ton, eine falsche Endung wie ein MP3 namens
    `.wav`) liest Tonregal trotzdem und verpackt sie beim Übernehmen neu, ohne den Klang anzufassen; die Endung passt
    danach zum Inhalt. Steckt gar kein Ton in der Datei, sagt die Prüfliste, was stattdessen drin ist, etwa nur
    Nullbytes oder eine Webseite.
- titel: Altbestand
  wozu: Alte MP3-Kopien in einem Rutsch einbringen, ohne das Durcheinander noch größer zu machen.
  verhalten:
  - Der Altbestand wird abgeglichen, ohne dass dort etwas verändert wird.
  - "*Erledigtes aufräumen* verschiebt nach einer Bestätigung genau die alten Dateien in den Papierkorb, die nachweislich
    in der Bibliothek angekommen sind."
  - Was sich seit dem Abgleich geändert hat oder in der Bibliothek nicht mehr zu finden ist, bleibt liegen.
- titel: Dubletten
  wozu: Jedes Stück nur einmal, und zwar in der besseren Fassung.
  verhalten:
  - Gefunden über gleiche Dateien, gleiche Aufnahmen oder gleiche Titel mit gleicher Länge.
  - Jede Fassung lässt sich kurz anhören, bevor man entscheidet.
  - "*Alle Vorschläge übernehmen* entscheidet nach einer Bestätigung mit Anzahl alle Gruppen auf einmal nach dem Vorschlag.
    Selbst geänderte Gruppen bleiben dabei unberührt, nur über Titel und Länge gefundene nur auf ausdrücklichen Wunsch."
  - Aussortiertes geht für 30 Tage in einen Papierkorb.
- titel: Analyse
  wozu: Tempo, Tonart und Lautstärke kennen, ohne nachzumessen.
  verhalten:
  - Nachts bestimmt Tonregal BPM und Tonart jedes Stücks und gleicht die Lautstärke an (ReplayGain).
  - Alles steht direkt in den Tags.
- titel: Backup
  wozu: Die Sammlung geht nicht verloren, wenn eine Platte ausfällt.
  verhalten:
  - Jede Nacht spiegelt ein Backup Bibliothek und Datenbanken in die Nextcloud.
  - Eine Sperre verhindert, dass eine leere Platte die Sicherung löscht.
- titel: Web-Player
  wozu: Die eigene Musik hören wie in einer Musik-App, im Browser und auf dem Handy.
  verhalten:
  - Warteschlange, Sterne, Zufall für Album, Interpret oder die ganze Bibliothek und Wiederholen.
  - Steuerung über Sperrbildschirm und Kopfhörertasten.
  - Lässt sich im iPhone-Safari auf den Home-Bildschirm legen.
- titel: Großer Player
  wozu: Ein Bildschirm nur für das, was gerade läuft.
  verhalten:
  - Das Cover groß auf einem unscharfen Hintergrund in seinen Farben, dazu Sterne und Fortschritt mit Restzeit.
  - Songtext neben oder statt des Covers, eine Warteschlange zum Umsortieren per Ziehen.
  - Nach dem Neuladen geht es an derselben Stelle im Stück weiter.
- titel: Songtexte
  wozu: Mitlesen, wo man im Stück ist.
  verhalten:
  - Synchronisierte Texte laufen mit; ein Tipp auf eine Zeile springt dorthin.
  - Sie kommen aus der Datei selbst, einer `.lrc` daneben oder von [lrclib.net](https://lrclib.net).
- titel: Smart Playlists
  wozu: Musik nach Stimmung und Anlass finden, statt Listen von Hand zu pflegen.
  verhalten:
  - Regeln wie BPM-Bereich, Tonart (auch passende Tonarten zum Mixen), Genre, neu, nie gehört oder Sterne.
  - Tonregal spielt sie selbst ab.
- titel: Download
  wozu: Die Musik dorthin mitnehmen, wo Tonregal nicht ist.
  verhalten:
  - Ein Titel als Originaldatei oder ein ganzes Album als ZIP.
- titel: App fürs iPhone und iPad
  wozu: Hören, auch wenn der Bildschirm aus ist.
  verhalten:
  - Spielt im Hintergrund, im Kontrollzentrum, mit AirPods und AirPlay zuverlässig weiter.
  - Mit Songtexten, Sternen und Zufall.
- titel: Schnittstelle zum Übernehmen
  wozu: Eigene Stücke landen direkt in der Bibliothek.
  verhalten:
  - Songs kommen ohne Abgleich herein, zum Beispiel aus [Tonwerk-AI](/projekte/tonwerk-ai/) mit Cover, Songtext, Tempo
    und Tonart.
  - Die Seite *Verbindungen* zeigt und erneuert den Schlüssel dafür.
roadmap:
  jetzt:
  - Der große Player im Browser wird ausprobiert
  - Die iPhone- und iPad-App im Test über TestFlight
  - Den abgearbeiteten Altbestand mit einem Knopf aufräumen, nur was nachweislich in der Bibliothek liegt
  - 'Überwachung: Inbox, Scans, Analyse, Backup und das Protokoll auf einer gemeinsamen Übersicht, mit Alarm, wenn das
    Backup ausbleibt; gebaut, noch nicht im Betrieb'
  - Beschädigte alte Dateien lesen und beim Übernehmen neu verpacken; gebaut, mit den echten Dateien noch nicht erprobt
  als_naechstes:
  - 'Eigene Playlists: von Hand zusammenstellen, sortieren und abspielen, neben den Smart Playlists'
  - 'Tag-Editor: Titel, Interpret, Album, Jahr, Genre und Cover im Browser ändern, für einen Titel oder ein ganzes
    Album; die Änderung landet in der Datei'
  - 'Bewertung ohne Navidrome: Tonregal hält die Sterne selbst und schreibt sie in die Datei, die vorhandenen werden
    übernommen'
  - In der iPhone-App Playlists, Offline-Wiedergabe und CarPlay
  - 'Lokalisierung: Web-Player und App in weiteren Sprachen'
steckbrief:
- name: Plattform
  wert: Mac mini im Heimnetz, Web und iPhone, Zugriff nur über Tailscale
- name: Lizenz
  wert: GNU AGPL v3 oder später
---

## Leitprinzip

Die Dateien sind die Wahrheit. Alle Metadaten stehen in den Tags der Audiodatei, die Datenbank ist nur ein Index und
lässt sich jederzeit aus der Bibliothek neu aufbauen.

## Technik

ASP.NET Core (.NET 10) mit EF Core und SQLite, SignalR für Live-Updates, ein Vue-3-Frontend mit Pinia, Tailwind CSS und
PrimeVue, eine SwiftUI-App. Fingerprint, Analyse und Sicherung laufen über eigenständige Werkzeuge wie Chromaprint,
librosa, ffmpeg, rsgain und rclone. Im Hintergrund zählt Navidrome die Wiedergaben und hält die Sterne. Neue Versionen
spielt der Mac mini von selbst ein, sobald gerade nichts importiert, analysiert oder gesichert wird; die iPhone-App geht
dabei automatisch an TestFlight.
