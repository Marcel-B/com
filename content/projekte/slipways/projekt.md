---
name: Slipways
untertitel: Slipanlagen und Marinas in Europa
reihenfolge: 30
vision: Wer ein Boot ins Wasser bringen will, soll schon vor der Fahrt wissen, wo das geht und ob der Pegel passt. Slipways
  soll die verlässliche Karte für Slipanlagen und Marinas in Europa werden, gepflegt von denen, die sie nutzen.
kurz: Bootsrampen und Marinas in Deutschland und Europa auf der Karte, mit aktuellen Pegelständen, Gewässerverläufen und Beiträgen
  der Nutzer. Web, Android und iOS.
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
features:
- titel: Karte und Listen
  wozu: Auf einen Blick sehen, was es in der Gegend gibt.
  verhalten:
  - Slipanlagen, Marinas, Gewässer und Motorservices auf einer Karte.
  - Die Liste zeigt immer, was im Kartenausschnitt liegt.
- titel: Pegelstände
  wozu: Wissen, ob das Wasser für die Rampe reicht, bevor man losfährt.
  verhalten:
  - Neue Werte alle 15 Minuten aus PEGELONLINE.
  - Für die Niederlande von Rijkswaterstaat.
- titel: Gewässerverläufe
  wozu: Sehen, wohin man vom Einsetzen aus fahren kann.
  verhalten:
  - Flüsse, Kanäle und Seen aus OpenStreetMap.
- titel: Europa
  wozu: Auch im Urlaub die nächste Slipanlage finden.
  verhalten:
  - Slipanlagen und Marinas aus OpenStreetMap für zwölf Länder, von Norwegen bis Spanien und Kroatien.
  - Angaben von den Webseiten der Marinas ergänzen die Daten.
- titel: Beiträge ohne Konto
  wozu: Wer vor Ort war, kann sein Wissen teilen, ohne sich anzumelden.
  verhalten:
  - Angaben ergänzen, Ausstattung ankreuzen, Tipps geben und fehlende Slipanlagen vorschlagen.
  - Alles geht erst nach Freigabe online.
  - Gegen Missbrauch schützt ein Proof of Work, ohne Cookies und ohne fremde Dienste.
- titel: Apps für Android und iOS
  wozu: Die Karte dort, wo man sie braucht, am Wasser.
  verhalten:
  - Dieselben Inhalte und Funktionen wie im Web.
roadmap:
  jetzt:
  - Die Angaben von den Webseiten der Marinas prüfen
  - Namen für Slipanlagen, die in OpenStreetMap keinen Namen haben
  als_naechstes:
  - Fotos zu Slipanlagen und Marinas
  - Die Karte lädt nur den sichtbaren Ausschnitt, danach weitere Länder wie Großbritannien, Finnland, Portugal und Griechenland
  - 'Lokalisierung: Web und Apps in weiteren Sprachen'
  spaeter:
  - Pegel für weitere Länder
  - Ein ruhigerer Kartenstil (Entscheidung steht noch aus)
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

## Technik

Backend mit ASP.NET Core Minimal APIs (.NET 10), EF Core und SQLite; das Web mit React 19, Vite, TanStack Query und Leaflet,
für Suchmaschinen serverseitig mit Titeln und strukturierten Daten versorgt. Die Android-App ist in Kotlin mit Jetpack Compose
geschrieben, die iOS-App in SwiftUI mit MapKit. Betrieb in Docker.
