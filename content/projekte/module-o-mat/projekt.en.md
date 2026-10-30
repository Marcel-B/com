---
untertitel: Keeping track of Eurorack modules
vision: A Eurorack grows module by module. module-o-mat is meant to keep track along the way of what is in the rack,
  whether space and power still suffice and what the collection is worth.
kurz: An inventory of your own Eurorack modules with maker, HP width, type and power draw, plus videos and price tracking.
links:
- text: Source on GitHub
  url: https://github.com/Marcel-B/module-o-mat
features:
- titel: Recording modules
  wozu: Everything about a module in one place.
  verhalten:
  - Maker, name, HP width, type and power draw.
  - Grouped by type and sorted by maker.
  - Modules can be duplicated.
- titel: Filters and statistics
  wozu: Find what you are looking for quickly and see the collection as a whole.
  verhalten:
  - Filter by text, type and width.
  - Statistics about the collection.
- titel: Videos and prices
  wozu: Know what a module sounds like and what it is worth right now.
  verhalten:
  - YouTube videos and price tracking for every module.
- titel: Backup
  wozu: Never lose the collection.
  verhalten:
  - Export a backup as a ZIP and import it again.
roadmap:
  als_naechstes:
  - 'Localisation: the interface in more languages'
steckbrief:
- name: Platform
  wert: Docker on the home network
---

## Technology

Started as an Elixir/Phoenix application with LiveView, Ecto and SQLite. Alongside it there is a REST API with an OpenAPI
description, two Vue 3 interfaces and a port of the backend to ASP.NET Core, published as a Docker image.
