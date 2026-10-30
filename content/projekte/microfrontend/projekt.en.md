---
untertitel: Microfrontends with Vue, React and .NET
vision: Large web applications should be buildable like many small ones. Teams ship their parts independently, and to users
  the whole still feels like one application. The platform shows how to do that cleanly with Vue, React and .NET.
kurz: A platform for microfrontends with .NET BFFs, Module Federation, sign-in via OpenID Connect and two equivalent
  variants in Vue and React.
links:
- text: Source on GitHub
  url: https://github.com/Marcel-B/Microfrontend
- text: Identity server
  url: https://github.com/Marcel-B/Identity
features:
- titel: Host with its own BFF
  wozu: A frame in which all parts become one application.
  verhalten:
  - Serves the shell and handles sign-in via OpenID Connect (code + PKCE), navigation, error pages and a debug page.
  - The session lives in a cookie; the browser never sees tokens.
- titel: Remotes with their own BFF
  wozu: Every team builds and runs its part itself.
  verhalten:
  - A remote brings its interface and API and registers with the host by API key and heartbeat.
  - The host then forwards through YARP and shows its pages.
- titel: Component library
  wozu: All parts look alike and speak the same language.
  verhalten:
  - A remote of its own that others include through Module Federation.
  - With a shared vocabulary for translations.
- titel: Bilingual, with roles
  wozu: Ready for real users.
  verhalten:
  - Everything in German and English.
  - Roles come from a dedicated identity server (OpenIddict).
- titel: Locally against a test stage
  wozu: A team develops its part without starting the whole platform.
  verhalten:
  - A remote can be developed locally against a test stage.
roadmap:
  als_naechstes:
  - 'Localisation: more languages besides German and English'
steckbrief:
- name: Kind
  wert: Reference architecture, learning and demo project
---

## Technology

BFFs in ASP.NET Core (.NET 10) with YARP, OpenID Connect and JWT Bearer. The Vue variant uses Vue 3, Pinia, PrimeVue and
vue-i18n, the React variant React 19, shadcn/ui and react-i18next, both Vite with `@module-federation/vite` and Tailwind
CSS 4. End-to-end tests with Playwright.
