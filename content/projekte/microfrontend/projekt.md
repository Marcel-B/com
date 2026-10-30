---
name: Microfrontend-Plattform
untertitel: Microfrontends mit Vue, React und .NET
reihenfolge: 80
vision: Große Webanwendungen sollen sich bauen lassen wie viele kleine. Teams liefern ihre Teile unabhängig aus, und für die
  Nutzer fühlt sich das Ganze trotzdem wie eine Anwendung an. Die Plattform zeigt, wie das mit Vue, React und .NET sauber
  geht.
kurz: Eine Plattform für Microfrontends mit .NET-BFFs, Module Federation, Anmeldung über OpenID Connect und zwei gleichwertigen
  Varianten in Vue und React.
technik:
- ASP.NET Core
- YARP
- Vue 3
- React
- Module Federation
links:
- text: Quelltext auf GitHub
  url: https://github.com/Marcel-B/Microfrontend
- text: Identity Server
  url: https://github.com/Marcel-B/Identity
features:
- titel: Host mit eigenem BFF
  wozu: Ein Rahmen, in dem alle Teile zu einer Anwendung werden.
  verhalten:
  - Liefert die Shell und kümmert sich um Anmeldung per OpenID Connect (Code + PKCE), Navigation, Fehlerseiten und eine
    Debugseite.
  - Die Session liegt im Cookie; Tokens sieht der Browser nie.
- titel: Remotes mit eigenem BFF
  wozu: Jedes Team baut und betreibt seinen Teil selbst.
  verhalten:
  - Ein Remote bringt Oberfläche und API mit und meldet sich mit API-Key und Heartbeat beim Host an.
  - Der Host leitet dann per YARP weiter und zeigt seine Seiten.
- titel: Komponenten-Bibliothek
  wozu: Alle Teile sehen gleich aus und sprechen dieselbe Sprache.
  verhalten:
  - Ein eigenes Remote, das andere per Module Federation einbinden.
  - Mit gemeinsamem Wortschatz für die Übersetzungen.
- titel: Zweisprachig, mit Rollen
  wozu: Bereit für echte Nutzer.
  verhalten:
  - Alles auf Deutsch und Englisch.
  - Rollen kommen aus dem eigenen Identity Server (OpenIddict).
- titel: Lokal gegen eine Test-Stage
  wozu: Ein Team entwickelt seinen Teil, ohne die ganze Plattform zu starten.
  verhalten:
  - Ein Remote lässt sich lokal gegen eine Test-Stage entwickeln.
roadmap:
  als_naechstes:
  - 'Lokalisierung: weitere Sprachen neben Deutsch und Englisch'
steckbrief:
- name: Art
  wert: Referenzarchitektur, Lern- und Demoprojekt
---

## Technik

BFFs in ASP.NET Core (.NET 10) mit YARP, OpenID Connect und JWT Bearer. Die Vue-Variante nutzt Vue 3, Pinia, PrimeVue und
vue-i18n, die React-Variante React 19, shadcn/ui und react-i18next, beide Vite mit `@module-federation/vite` und Tailwind
CSS 4. End-to-End-Tests mit Playwright.
