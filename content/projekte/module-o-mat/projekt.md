---
name: module-o-mat
untertitel: Eurorack-Module erfassen
reihenfolge: 70
vision: Ein Eurorack wächst Modul für Modul. module-o-mat soll dabei den Überblick behalten, was im Rack steckt, ob Platz
  und Strom noch reichen und was die Sammlung wert ist.
kurz: Inventar der eigenen Eurorack-Module mit Hersteller, HP-Breite, Typ und Strombedarf, dazu Videos und Preisbeobachtungen.
technik:
- Elixir
- Phoenix LiveView
- ASP.NET Core
- Vue 3
links:
- text: Quelltext auf GitHub
  url: https://github.com/Marcel-B/module-o-mat
features:
- titel: Module erfassen
  wozu: Alles über ein Modul an einer Stelle.
  verhalten:
  - Hersteller, Name, HP-Breite, Typ und Strombedarf.
  - Nach Typ gruppiert und nach Hersteller sortiert.
  - Module lassen sich duplizieren.
- titel: Filter und Statistik
  wozu: Schnell finden, was man sucht, und die Sammlung als Ganzes sehen.
  verhalten:
  - Filtern nach Text, Typ und Breite.
  - Statistiken über die Sammlung.
- titel: Videos und Preise
  wozu: Wissen, wie ein Modul klingt und was es gerade wert ist.
  verhalten:
  - Zu jedem Modul YouTube-Videos und Preisbeobachtungen.
- titel: Sichern
  wozu: Die Sammlung nicht verlieren.
  verhalten:
  - Sicherung als ZIP exportieren und wieder einspielen.
roadmap:
  als_naechstes:
  - 'Lokalisierung: die Oberfläche in weiteren Sprachen'
steckbrief:
- name: Plattform
  wert: Docker im Heimnetz
---

## Technik

Entstanden als Elixir/Phoenix-Anwendung mit LiveView, Ecto und SQLite. Daneben gibt es eine REST-API mit
OpenAPI-Beschreibung, zwei Vue-3-Oberflächen und einen Port des Backends nach ASP.NET Core, der als Docker-Image
veröffentlicht wird.
