---
untertitel: Slipways and marinas in Europe
vision: Anyone taking a boat to the water should know before setting off where it can go in and whether the water level is
  right. Slipways is meant to become the reliable map of slipways and marinas in Europe, kept up by the people who use it.
kurz: Boat ramps and marinas in Germany and Europe on a map, with current water levels, waterways and contributions from
  users. Web, Android and iOS.
links:
- text: slipways.de
  url: https://slipways.de/
- text: Source on GitHub
  url: https://github.com/Marcel-B/Slipways
features:
- titel: Map and lists
  wozu: See at a glance what the area has to offer.
  verhalten:
  - Slipways, marinas, waters and engine services on one map.
  - The list always shows what lies within the map section.
- titel: Water levels
  wozu: Know whether there is enough water for the ramp before you set off.
  verhalten:
  - New readings every 15 minutes from PEGELONLINE.
  - For the Netherlands from Rijkswaterstaat.
- titel: Waterways
  wozu: See where you can go from where you launch.
  verhalten:
  - Rivers, canals and lakes from OpenStreetMap.
- titel: Europe
  wozu: Find the nearest slipway on holiday too.
  verhalten:
  - Slipways and marinas from OpenStreetMap for twelve countries, from Norway to Spain and Croatia.
  - Details from the marinas' own websites add to the data.
- titel: Contributions without an account
  wozu: Anyone who has been there can share what they know without signing up.
  verhalten:
  - Add details, tick off facilities, leave tips and suggest missing slipways.
  - Nothing goes online before it is approved.
  - A proof of work protects against abuse, without cookies and without third-party services.
- titel: Apps for Android and iOS
  wozu: The map where you need it, at the water.
  verhalten:
  - The same content and features as on the web.
roadmap:
  jetzt:
  - Check the details taken from the marinas' websites
  - Names for slipways that have none in OpenStreetMap
  als_naechstes:
  - Photos of slipways and marinas
  - The map loads only the visible section, then more countries such as Great Britain, Finland, Portugal and Greece
  - 'Localisation: web and apps in more languages'
  spaeter:
  - Water levels for more countries
  - A calmer map style (not decided yet)
steckbrief:
- name: Platform
  wert: Web, Android, iOS
- name: Licence
  wert: PolyForm Strict 1.0.0 (source available)
---

## Technology

A backend with ASP.NET Core Minimal APIs (.NET 10), EF Core and SQLite; the web with React 19, Vite, TanStack Query and
Leaflet, served with titles and structured data for search engines. The Android app is written in Kotlin with Jetpack
Compose, the iOS app in SwiftUI with MapKit. Runs in Docker.
