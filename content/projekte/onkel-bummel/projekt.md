---
name: Onkel Bummel
untertitel: Eigene Benachrichtigungen mit Verlauf und Bildern
reihenfolge: 100
vision: Wenn ein Druck fertig ist, eine Kamera etwas sieht oder ein Alarm anschlägt, soll die Nachricht sicher ankommen
  und auffindbar bleiben. Onkel Bummel soll der eigene Briefkasten für alle Meldungen der eigenen Dienste werden, mit
  Bildern und einem Verlauf, in dem man nachsehen kann.
kurz: Eigener Benachrichtigungsdienst mit Push aufs iPhone, Web-Oberfläche, durchsuchbarem Verlauf, Bildern und
  Action-Buttons, betrieben zu Hause.
technik:
- ASP.NET Core
- SQLite
- Vue 3
- SwiftUI
links:
- text: Quelltext auf GitHub
  url: https://github.com/Marcel-B/onkel-bummel
features:
- titel: Senden aus Skripten und Diensten
  wozu: Jeder eigene Dienst kann mit einer einfachen Anfrage Bescheid geben.
  verhalten:
  - Nachrichten kommen als JSON, als Formular mit Dateien oder als Webhook von Grafana an.
  - Jeder Sender hat einen eigenen Schlüssel, der nur für seine Topics gilt und nur einmal angezeigt wird.
  - Schickt ein Sender dieselbe Nachricht noch einmal, etwa nach einem Fehler, entsteht trotzdem nur eine.
- titel: Push aufs iPhone
  wozu: Wichtiges sofort sehen, Unwichtiges später.
  verhalten:
  - Jede Nachricht geht als Mitteilung an alle Geräte, die ihr Topic abonniert haben, außer bei stummen Topics.
  - Die Priorität bestimmt, ob die Mitteilung leise kommt, normal oder auch durch einen Fokus.
  - Bilder erscheinen als Vorschau direkt in der Mitteilung.
  - Das App-Symbol zeigt, wie viele Nachrichten ungelesen sind.
- titel: Verlauf und Suche
  wozu: Auch nach Tagen noch finden, was passiert ist.
  verhalten:
  - Alle Nachrichten bleiben nach Topics geordnet erhalten, mit Gelesen-Status und Zählern.
  - Die Volltextsuche durchsucht Titel, Text und Tags und lässt sich nach Topic, Priorität, Zeitraum, Ungelesen und Bildern
    filtern.
  - Wie lange ein Topic seine Nachrichten behält, ist pro Topic einstellbar.
- titel: Bilder
  wozu: Ein Foto sagt mehr als „Bewegung an der Einfahrt“.
  verhalten:
  - Zu jeder Nachricht gehören bis zu zehn Anhänge, Bilder bekommen ein Vorschaubild.
  - Eine Galerie zeigt die Bilder pro Topic und über alle Topics, das Original lässt sich laden und teilen.
- titel: Actions
  wozu: Auf eine Meldung gleich reagieren, ohne eine andere App zu öffnen.
  verhalten:
  - Eine Nachricht trägt bis zu drei Buttons, in der Mitteilung, in der App und im Browser.
  - Den Aufruf dahinter führt der Server zu Hause aus, so dass er sein Ziel auch erreicht, wenn das Handy es nicht kann.
  - Das letzte Ergebnis steht an der Nachricht.
- titel: Web-Oberfläche
  wozu: Alles auch am Rechner oder auf einem Android-Handy im Browser.
  verhalten:
  - Neue Nachrichten erscheinen live, ohne neu zu laden.
  - Nachrichten lassen sich im Browser schreiben, mit Bildern per Auswählen, Hineinziehen oder Einfügen.
  - Topics, Schlüssel der Sender und Geräte werden hier verwaltet; ein QR-Code mit der Server-Adresse hilft beim Einrichten der App.
  - Hell und dunkel nach der Einstellung des Systems.
- titel: Betrieb zu Hause
  wozu: Die eigenen Meldungen bleiben im eigenen Netz.
  verhalten:
  - Der Server läuft in einem Container auf einem Proxmox-Host und ist nur über Tailscale erreichbar.
  - Angemeldet wird über einen eigenen Identity-Server, für die Web-Oberfläche und die App.
  - Neue Versionen spielt der Server selbst ein; kommt eine nicht hoch, läuft wieder die vorige.
  - Auf Wunsch sichert er Datenbank und Bilder jede Nacht verschlüsselt in eine Nextcloud.
roadmap:
  als_naechstes:
  - 'Kurzbefehle und ein Widget „Ungelesen“ für das iPhone'
  - 'Suche: „ss“ findet auch „ß“'
  - Alarme aus Grafana übersichtlicher darstellen
  - 'Lokalisierung: Web-Oberfläche und App auch auf Englisch'
  spaeter:
  - Eine Meldung über einen zweiten Weg, wenn zu Hause Strom oder Internet ausfallen
steckbrief:
- name: Plattform
  wert: iOS, Web; Server in Docker
- name: Ersetzt
  wert: ntfy für Slipways, fil-o-mat und die Grafana-Alarme
---

## Technik

Der Server ist ASP.NET Core (.NET 10) mit SQLite und deren Volltextsuche FTS5 im Docker-Container. Die Web-Oberfläche
ist Vue 3 mit TypeScript und Tailwind und wird vom Server mit ausgeliefert. Die iOS-App ist in SwiftUI geschrieben,
mit einem lokalen Zwischenspeicher und einer Erweiterung, die Bilder und Buttons an die Mitteilungen hängt. Pushes
gehen direkt an Apples Push-Dienst, angemeldet wird über OpenID Connect.

## Der Name

Onkel Bummel war mein erster Postbote.
