---
untertitel: A store for electronic components
vision: Anyone who tinkers with electronics should know what is in their boxes and get ideas for what to build from it.
  Ohmventory is meant to make the parts box talk, with an AI that stays on your own network.
kurz: Record components by photo, storage places with QR labels, and an assistant that suggests projects from your stock.
  With a local LLM.
links:
- text: Source on GitHub
  url: https://github.com/Marcel-B/Ohmventory
features:
- titel: Recording by photo
  wozu: Store a part without typing up data sheets.
  verhalten:
  - A vision model recognises the component or breakout board in the photo.
  - If no type designation is legible, a second pass reads the markings and searches the web for the matching board.
  - The sources are shown.
- titel: Containers
  wozu: Know which box a part is in.
  verhalten:
  - Storage places with short codes like `T-001`, nested as deep as you like.
  - Printable QR labels that open the contents directly.
- titel: Project assistant
  wozu: Turn your stock into ideas, for example by asking "Can I build a thermometer?"
  verhalten:
  - The model searches your stock and the web and suggests projects with a parts list.
  - Whether a part is there is decided not by the model but by a fixed match against the stock.
  - Missing parts go to the shopping list at the press of a button.
roadmap:
  als_naechstes:
  - 'Localisation: the interface in more languages'
steckbrief:
- name: Platform
  wert: Docker, Proxmox LXC; LLM via LM Studio
---

## Technology

ASP.NET Core (.NET 10) with Minimal APIs, EF Core and PostgreSQL, Microsoft.Extensions.AI; a Vue 3 frontend with Tailwind
CSS and PrimeVue. The language model runs in LM Studio on a Mac on the home network and shares its memory with other
applications through a queue; SearXNG handles web search. The whole thing is installed by a script as a Docker stack in a
Proxmox container.
