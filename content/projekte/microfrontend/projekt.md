---
name: Microfrontend-Plattform
untertitel: Microfrontends mit Vue, React und .NET
reihenfolge: 80
kurz: Eine Plattform für Microfrontends mit .NET-BFFs, Module Federation, Anmeldung über OpenID Connect und zwei gleichwertigen
  Varianten in Vue und React.
einleitung: 'Eine Referenzplattform für Microfrontends: Eine Shell bindet unabhängig gebaute und betriebene Teile ein, jedes
  mit eigenem Backend for Frontend, einmal in Vue und einmal in React.'
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
steckbrief:
- name: Art
  wert: Referenzarchitektur, Lern- und Demoprojekt
---

## Was drin steckt

- **Host mit eigenem BFF:** liefert die Shell, kümmert sich um Anmeldung per OpenID Connect (Code + PKCE), Navigation, Fehlerseiten und eine Debugseite. Die Session liegt im Cookie, Tokens sieht der Browser nie.
- **Remotes mit eigenem BFF:** bringen ihre Oberfläche und API mit und melden sich selbst mit API-Key und Heartbeat beim Host an; der Host leitet dann per YARP weiter und zeigt ihre Seiten.
- **Komponenten-Bibliothek** als eigenes Remote, das andere Remotes per Module Federation einbinden, samt gemeinsamem Wortschatz.
- Alles **zweisprachig** (Deutsch, Englisch), Rollen aus dem eigenen Identity Server (OpenIddict).
- Ein Remote lässt sich **lokal gegen eine Test-Stage** entwickeln.

## Technik

BFFs in ASP.NET Core (.NET 10) mit YARP, OpenID Connect und JWT Bearer. Die Vue-Variante nutzt Vue 3, Pinia, PrimeVue und vue-i18n, die React-Variante React 19, shadcn/ui und react-i18next, beide Vite mit `@module-federation/vite` und Tailwind CSS 4. End-to-End-Tests mit Playwright.
