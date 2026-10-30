---
name: Slipways
untertitel: Slipanlagen und Marinas in Europa
reihenfolge: 30
kurz: Bootsrampen und Marinas in Deutschland und Europa auf der Karte, mit aktuellen Pegelständen, Gewässerverläufen und Beiträgen
  der Nutzer. Web, Android und iOS.
einleitung: Slipways sammelt Slipanlagen (Bootsrampen) und Marinas in Deutschland und weiteren Ländern Europas, damit man
  vor der Fahrt weiß, wo das Boot ins Wasser kommt und wie hoch das Wasser gerade steht.
technik:
- ASP.NET Core
- React
- Kotlin
- SwiftUI
- OpenStreetMap
links:
- text: slipways.de
  url: https://slipways.de/
- text: Quelltext auf GitHub
  url: https://github.com/Marcel-B/Slipways
steckbrief:
- name: Plattform
  wert: Web, Android, iOS
- name: Lizenz
  wert: PolyForm Strict 1.0.0 (Quelltext einsehbar)
app:
  kategorie: TravelApplication
  plattformen: Web, Android, iOS
  url: https://slipways.de/
  kostenlos: true
---

## Was es kann

- **Karte und Listen** mit Slipanlagen, Marinas, Gewässern und Motorservices, die Liste immer passend zum Kartenausschnitt.
- **Pegelstände** alle 15 Minuten aus PEGELONLINE und, für die Niederlande, von Rijkswaterstaat.
- **Gewässerverläufe** von Flüssen, Kanälen und Seen aus OpenStreetMap.
- Slipanlagen und Marinas aus **OpenStreetMap** importiert und mit Angaben von den Webseiten der Marinas ergänzt.
- **Beiträge ohne Konto:** Angaben ergänzen, Ausstattung ankreuzen, Tipps geben, fehlende Slipanlagen vorschlagen. Alles geht erst nach Freigabe online, gegen Missbrauch schützt ein Proof of Work ohne Cookies und ohne fremde Dienste.
- **Apps für Android und iOS** mit denselben Inhalten.

## Technik

Backend mit ASP.NET Core Minimal APIs (.NET 10), EF Core und SQLite; das Web mit React 19, Vite, TanStack Query und Leaflet, für Suchmaschinen serverseitig mit Titeln und strukturierten Daten versorgt. Die Android-App ist in Kotlin mit Jetpack Compose geschrieben, die iOS-App in SwiftUI mit MapKit. Betrieb in Docker.
