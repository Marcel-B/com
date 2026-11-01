---
name: fil-o-mat
untertitel: Filamentspulen mit NFC
reihenfolge: 60
vision: Jede Filamentspule soll wissen, wo sie liegt und wie viel noch drauf ist. fil-o-mat soll das Filamentlager so
  selbstverständlich machen wie ein Etikett, mit einem Scan statt einer Tabelle.
kurz: Container und Filamentspulen mit RFID/NFC-Tags verwalten, per App einlagern und herausnehmen, Verbrauch direkt vom 3D-Drucker
  buchen.
technik:
- Kotlin
- SwiftUI
- Vue 3
- ASP.NET Core
- ESP32
links:
- text: Quelltext auf GitHub
  url: https://github.com/Marcel-B/fil-o-mat
features:
- titel: Container und Spulen
  wozu: Jede Spule und jede Kiste eindeutig erkennen.
  verhalten:
  - Container und Spulen werden angelegt und mit RFID/NFC-Tags versehen.
- titel: Einlagern und Herausnehmen
  wozu: Wissen, wo eine Spule liegt, ohne etwas aufzuschreiben.
  verhalten:
  - Ein Scan genügt, erst der Container, dann die Spule, oder umgekehrt.
- titel: Offene Tags
  wozu: Tags, die nicht an eine App gebunden sind.
  verhalten:
  - Tags werden im offenen OpenSpool-Format gelesen und beschrieben.
  - Android- und iOS-App erkennen Tags über dieselbe UID.
- titel: NFC-Leser am Drucker
  wozu: Der Verbrauch landet von selbst auf der richtigen Spule.
  verhalten:
  - Ein ESP32 meldet, welches Musterplättchen in welchem Slot steckt.
  - Das Backend bucht den Verbrauch, den PrusaLink, Bambu oder Anycubic melden, auf die passende Spule.
- titel: Web-Oberfläche
  wozu: Das Lager auch am Rechner im Blick haben.
  verhalten:
  - Eine Oberfläche im Browser, ausgeliefert mit dem Backend.
  - Apps, Web-Oberfläche und Meldungen gibt es auf Deutsch und Englisch.
  - Apps und Web-Oberfläche erscheinen hell, dunkel oder wie das System, in den Einstellungen wählbar.
roadmap:
  als_naechstes:
  - 'Öffentlicher TestFlight-Link: wer mag, kann die iOS-App vorab testen'
steckbrief:
- name: Plattform
  wert: Android, iOS, Web; Backend in Docker
- name: Lizenz
  wert: Apache 2.0
---

## Technik

Android-App in Kotlin mit Jetpack Compose, iOS-App in Swift mit SwiftUI und CoreNFC, eine Web-Oberfläche mit Vue 3 und
PrimeVue. Das gemeinsame Backend ist ASP.NET Core (.NET 10) mit SQLite im Docker-Container. Die Leser am Drucker sind
ESP32-Boards mit RC522- oder PN532-Modulen, konfiguriert mit ESPHome.
