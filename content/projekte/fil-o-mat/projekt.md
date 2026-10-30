---
name: fil-o-mat
untertitel: Filamentspulen mit NFC
reihenfolge: 60
kurz: Container und Filamentspulen mit RFID/NFC-Tags verwalten, per App einlagern und herausnehmen, Verbrauch direkt vom 3D-Drucker
  buchen.
einleitung: Apps für Android, iOS und das Web, mit denen sich Filamentspulen und ihre Behälter über NFC-Tags verwalten lassen,
  bis hin zum Verbrauch am Drucker.
technik:
- Kotlin
- SwiftUI
- Vue 3
- ASP.NET Core
- ESP32
links:
- text: Quelltext auf GitHub
  url: https://github.com/Marcel-B/fil-o-mat
steckbrief:
- name: Plattform
  wert: Android, iOS, Web; Backend in Docker
- name: Lizenz
  wert: Apache 2.0
---

## Was es kann

- **Container und Spulen** anlegen und mit RFID/NFC-Tags versehen.
- **Einlagern und Herausnehmen** per Scan: erst den Container, dann die Spule, oder umgekehrt.
- Tags **lesen und beschreiben**, im offenen OpenSpool-Format; beide Apps erkennen Tags über dieselbe UID.
- **NFC-Leser am Drucker:** Ein ESP32 meldet, welches Musterplättchen in welchem Slot steckt. Das Backend bucht den Verbrauch, den PrusaLink, Bambu oder Anycubic melden, auf die passende Spule.

## Technik

Android-App in Kotlin mit Jetpack Compose, iOS-App in Swift mit SwiftUI und CoreNFC, eine Web-Oberfläche mit Vue 3 und PrimeVue. Das gemeinsame Backend ist ASP.NET Core (.NET 10) mit SQLite im Docker-Container. Die Leser am Drucker sind ESP32-Boards mit RC522- oder PN532-Modulen, konfiguriert mit ESPHome.
