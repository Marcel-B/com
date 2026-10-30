---
name: Ohmventory
untertitel: Lager für Elektronikbauteile
reihenfolge: 50
vision: Wer Elektronik bastelt, soll wissen, was in den Kisten liegt, und darauf kommen, was sich daraus bauen lässt.
  Ohmventory soll die Bastelkiste zum Sprechen bringen, mit einer KI, die im eigenen Netz bleibt.
kurz: Bauteile per Foto erfassen, Lagerorte mit QR-Etiketten, und ein Assistent, der aus dem Bestand Projekte vorschlägt.
  Mit einem lokalen LLM.
technik:
- ASP.NET Core
- Vue 3
- PostgreSQL
- Lokales LLM
links:
- text: Quelltext auf GitHub
  url: https://github.com/Marcel-B/Ohmventory
features:
- titel: Erfassen per Foto
  wozu: Ein Bauteil einlagern, ohne Datenblätter abzutippen.
  verhalten:
  - Ein Vision-Modell erkennt Bauteil oder Breakout-Board auf dem Foto.
  - Ist keine Typbezeichnung lesbar, liest ein zweiter Durchgang die Aufdrucke und sucht damit im Web nach dem passenden
    Board.
  - Die Quellen werden angezeigt.
  - Fotos kommen als JPEG, PNG oder WebP, direkt von der Handykamera oder als Datei.
- titel: Container
  wozu: Wissen, in welcher Kiste ein Teil liegt.
  verhalten:
  - Lagerorte mit kurzen Codes wie `T-001`, beliebig verschachtelbar.
  - Druckbare QR-Etiketten, die direkt den Inhalt zeigen.
- titel: Projektassistent
  wozu: Aus dem Bestand Ideen machen, zum Beispiel auf die Frage „Kann ich ein Thermometer bauen?“
  verhalten:
  - Das Modell durchsucht Lager und Web und schlägt Projekte mit Stückliste vor.
  - Ob ein Teil da ist, entscheidet nicht das Modell, sondern ein fester Abgleich mit dem Bestand.
  - Fehlendes landet auf Knopfdruck in der Einkaufsliste.
- titel: Installation und Updates
  wozu: Ohmventory im eigenen Netz betreiben, ohne sich um jede neue Version kümmern zu müssen.
  verhalten:
  - Ein Skript richtet den ganzen Docker-Stack in einem Proxmox-Container ein.
  - Neue Versionen spielt ein Timer alle fünf Minuten ein, aber nur, wenn alle automatischen Tests grün sind.
  - Startet eine neue Version nicht, kehrt der Container von selbst zur vorherigen zurück.
roadmap:
  jetzt:
  - HEIC-Fotos vom iPhone annehmen und umwandeln
  als_naechstes:
  - 'Lokalisierung: die Oberfläche in weiteren Sprachen'
steckbrief:
- name: Plattform
  wert: Docker, Proxmox-LXC oder Mac; LLM über LM Studio
---

## Technik

ASP.NET Core (.NET 10) mit Minimal APIs, EF Core und PostgreSQL, Microsoft.Extensions.AI; ein Vue-3-Frontend mit Tailwind
CSS und PrimeVue. Das Sprachmodell läuft in LM Studio auf einem Mac im Heimnetz und teilt sich den Speicher über eine
Warteschlange mit anderen Anwendungen; die Websuche übernimmt SearXNG. Installiert wird das Ganze per Skript als
Docker-Stack in einem Proxmox-Container. Wer nur einen Mac hat, kann alles darauf laufen lassen, die Anleitung unten
zeigt, wie.
