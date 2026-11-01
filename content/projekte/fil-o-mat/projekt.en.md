---
untertitel: Filament spools with NFC
vision: Every filament spool should know where it is and how much is left on it. fil-o-mat is meant to make the filament
  store as effortless as a label, with a scan instead of a spreadsheet.
kurz: Manage containers and filament spools with RFID/NFC tags, store and take them out with an app, book consumption
  straight from the 3D printer.
links:
- text: Source on GitHub
  url: https://github.com/Marcel-B/fil-o-mat
features:
- titel: Containers and spools
  wozu: Recognise every spool and every box without doubt.
  verhalten:
  - Containers and spools are created and fitted with RFID/NFC tags.
- titel: Storing and taking out
  wozu: Know where a spool is without writing anything down.
  verhalten:
  - One scan is enough, first the container, then the spool, or the other way round.
- titel: Open tags
  wozu: Tags that are not tied to one app.
  verhalten:
  - Tags are read and written in the open OpenSpool format.
  - The Android and iOS apps recognise tags by the same UID.
- titel: NFC readers at the printer
  wozu: Consumption lands on the right spool by itself.
  verhalten:
  - An ESP32 reports which sample chip sits in which slot.
  - The backend books the consumption that PrusaLink, Bambu or Anycubic report to the matching spool.
- titel: Web interface
  wozu: Keep an eye on the store at the computer too.
  verhalten:
  - An interface in the browser, shipped with the backend.
  - Apps, web interface and notifications are available in German and English.
  - Apps and web interface appear light, dark or following the system, chosen in the settings.
roadmap:
  als_naechstes:
  - 'Public TestFlight link: anyone who likes can try the iOS app early'
steckbrief:
- name: Platform
  wert: Android, iOS, web; backend in Docker
- name: Licence
  wert: Apache 2.0
---

## Technology

An Android app in Kotlin with Jetpack Compose, an iOS app in Swift with SwiftUI and CoreNFC, a web interface with Vue 3 and
PrimeVue. The shared backend is ASP.NET Core (.NET 10) with SQLite in a Docker container. The readers at the printer are
ESP32 boards with RC522 or PN532 modules, configured with ESPHome.
