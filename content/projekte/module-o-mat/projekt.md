---
name: module-o-mat
untertitel: Eurorack-Module erfassen
reihenfolge: 70
kurz: Inventar der eigenen Eurorack-Module mit Hersteller, HP-Breite, Typ und Strombedarf, dazu Videos und Preisbeobachtungen.
einleitung: 'Ein Inventar für Eurorack-Module: was im Rack steckt, wie breit es ist, was es an Strom zieht und was es gerade
  wert ist.'
technik:
- Elixir
- Phoenix LiveView
- ASP.NET Core
- Vue 3
links:
- text: Quelltext auf GitHub
  url: https://github.com/Marcel-B/module-o-mat
steckbrief:
- name: Plattform
  wert: Docker im Heimnetz
---

## Was es kann

- Module mit **Hersteller, Name, HP-Breite, Typ und Strombedarf** erfassen, nach Typ gruppiert und nach Hersteller sortiert.
- Filtern nach Text, Typ und Breite, mit Statistiken über die Sammlung.
- Zu jedem Modul **YouTube-Videos** und **Preisbeobachtungen**.
- Module duplizieren, Sicherung als ZIP exportieren und wieder einspielen.

## Technik

Entstanden als Elixir/Phoenix-Anwendung mit LiveView, Ecto und SQLite. Daneben gibt es eine REST-API mit OpenAPI-Beschreibung, zwei Vue-3-Oberflächen und einen Port des Backends nach ASP.NET Core, der als Docker-Image veröffentlicht wird.
