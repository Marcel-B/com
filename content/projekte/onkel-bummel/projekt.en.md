---
untertitel: Your own notifications with history and pictures
vision: When a print is done, a camera sees something or an alarm goes off, the message should arrive reliably and stay
  easy to find. Onkel Bummel is meant to become the letterbox for every message from your own services, with pictures
  and a history you can look back through.
kurz: Self-hosted notification service with push to the iPhone, a web interface, searchable history, pictures and
  action buttons, run at home.
links:
- text: Source on GitHub
  url: https://github.com/Marcel-B/onkel-bummel
features:
- titel: Sending from scripts and services
  wozu: Every service of your own can report with one simple request.
  verhalten:
  - Messages arrive as JSON, as a form with files or as a webhook from Grafana.
  - Each sender has its own key, which only applies to its topics and is shown only once.
  - If a sender sends the same message again, say after an error, there is still only one.
- titel: Push to the iPhone
  wozu: See what matters at once and the rest later.
  verhalten:
  - Every message goes out as a notification to all devices that have subscribed to its topic, except for muted topics.
  - The priority decides whether a notification arrives quietly, normally or even through a Focus.
  - Pictures appear as a preview right in the notification.
  - The app icon shows how many messages are unread.
- titel: History and search
  wozu: Find out what happened, even days later.
  verhalten:
  - All messages are kept, sorted by topic, with read status and counters.
  - Full-text search covers title, text and tags and can be filtered by topic, priority, period, unread and pictures.
  - How long a topic keeps its messages can be set per topic.
- titel: Pictures
  wozu: A photo says more than “motion at the driveway”.
  verhalten:
  - Each message can carry up to ten attachments, and pictures get a thumbnail.
  - A gallery shows the pictures per topic and across all topics; the original can be downloaded and shared.
- titel: Actions
  wozu: React to a message straight away without opening another app.
  verhalten:
  - A message carries up to three buttons, in the notification, in the app and in the browser.
  - The server at home makes the call behind it, so it reaches its target even when the phone cannot.
  - The last result is shown with the message.
- titel: Web interface
  wozu: Everything on the computer or on an Android phone in the browser too.
  verhalten:
  - New messages appear live without reloading.
  - Messages can be written in the browser, with pictures by choosing, dragging or pasting them.
  - Topics, sender keys and devices are managed here; a QR code with the server address helps to set up the app.
  - Light and dark according to the system setting.
- titel: Running at home
  wozu: Your messages stay in your own network.
  verhalten:
  - The server runs in a container on a Proxmox host and can only be reached through Tailscale.
  - Signing in goes through your own identity server, for the web interface and the app.
  - The server installs new versions by itself; if one does not come up, the previous one runs again.
  - If you like, it backs up the database and pictures to a Nextcloud every night, encrypted.
roadmap:
  als_naechstes:
  - Shortcuts and an “Unread” widget for the iPhone
  - 'Search: “ss” also finds “ß”'
  - Show alarms from Grafana more clearly
  - 'Localisation: web interface and app in English too'
  spaeter:
  - A message by a second route when power or internet fail at home
steckbrief:
- name: Platform
  wert: iOS, web; server in Docker
- name: Replaces
  wert: ntfy for Slipways, fil-o-mat and the Grafana alarms
---

## Technology

The server is ASP.NET Core (.NET 10) with SQLite and its full-text search FTS5 in a Docker container. The web
interface is Vue 3 with TypeScript and Tailwind and is served by the server. The iOS app is written in SwiftUI, with
a local cache and an extension that adds pictures and buttons to notifications. Pushes go straight to Apple's push
service, and signing in uses OpenID Connect.

## The name

Onkel Bummel was my first postman.
