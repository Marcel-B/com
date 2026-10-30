---
name: Ohmventory
untertitel: Lager für Elektronikbauteile
reihenfolge: 50
kurz: Bauteile per Foto erfassen, Lagerorte mit QR-Etiketten, und ein Assistent, der aus dem Bestand Projekte vorschlägt.
  Mit einem lokalen LLM.
einleitung: Eine Lagerverwaltung für Elektronikbauteile, die Bauteile auf Fotos erkennt und aus dem Bestand Projektideen macht,
  mit einem Sprachmodell im eigenen Netz.
technik:
- ASP.NET Core
- Vue 3
- PostgreSQL
- Lokales LLM
links:
- text: Quelltext auf GitHub
  url: https://github.com/Marcel-B/Ohmventory
steckbrief:
- name: Plattform
  wert: Docker, Proxmox-LXC; LLM über LM Studio
---

## Was es kann

- **Erfassen per Foto:** Ein Vision-Modell erkennt Bauteil oder Breakout-Board. Ist keine Typbezeichnung lesbar, liest ein zweiter Durchgang die Aufdrucke und sucht damit im Web nach dem passenden Board; die Quellen werden angezeigt.
- **Container:** Lagerorte mit kurzen Codes wie `T-001`, verschachtelbar, mit druckbaren QR-Etiketten, die direkt den Inhalt zeigen.
- **Projektassistent:** „Kann ich ein Thermometer bauen?“ Das Modell durchsucht Lager und Web und schlägt Projekte mit Stückliste vor. Ob ein Teil da ist, entscheidet nicht das Modell, sondern ein fester Abgleich mit dem Bestand. Fehlendes landet auf Knopfdruck in der Einkaufsliste.

## Technik

ASP.NET Core (.NET 10) mit Minimal APIs, EF Core und PostgreSQL, Microsoft.Extensions.AI; ein Vue-3-Frontend mit Tailwind CSS und PrimeVue. Das Sprachmodell läuft in LM Studio auf einem Mac im Heimnetz und teilt sich den Speicher über eine Warteschlange mit anderen Anwendungen; die Websuche übernimmt SearXNG. Installiert wird das Ganze per Skript als Docker-Stack in einem Proxmox-Container.
