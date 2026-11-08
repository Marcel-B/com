---
titel: Privacy of the Onkel Bummel app
beschreibung: Privacy policy of the iOS app Onkel Bummel, which data the app processes and where it goes
---

This is a translation; the [German privacy policy](/datenschutz-onkel-bummel.html) is the binding one.

## In short

Onkel Bummel is the app for a notification service you run on your own server. The app only talks to that server, to the
sign-in service your server names, and to Apple for notifications. It sends nothing to me, the developer: no analytics,
no advertising, no crash reports, no third-party libraries. I see neither your messages nor your sign-in nor your
devices.

## Controller

For the app itself: Marcel Benders, address in the [legal notice](/en/impressum.html). For the data on your server, you
are responsible, or whoever runs the server.

## What the app processes

- **Server address:** You type it or scan it as a QR code. The app remembers it on the device.
- **Sign-in:** The app signs you in at the sign-in service (identity server) your server names. The key that keeps you
  signed in is stored in the device's keychain.
- **Device and notifications:** So that notifications arrive, the app registers the device with your server, with the
  device name from the iOS settings, Apple's push token and the subscribed topics.
- **Messages and pictures:** The app loads them from your server and keeps a copy on the device so they show up quickly.
  The copy goes away with the app.
- **Camera:** only to scan the QR code with the server address. The image stays on the device and is not stored.
- **Photos:** The app only asks for permission to add pictures, and only when you save a picture from a message. It does
  not read your library.

## Notifications through Apple

Your server sends notifications through the Apple Push Notification service of Apple Inc., One Apple Park Way,
Cupertino, CA 95014, USA. For this, Apple receives the device's push token and the content of the notification (title,
text and, for pictures, a time-limited link to the preview). The device loads the preview directly from your server.
Details are in [Apple's privacy policy](https://www.apple.com/legal/privacy/en-ww/).

## What else Apple learns

Downloads and updates go through the App Store, test versions through TestFlight; Apple's privacy policy applies to
those. If you agreed in the iOS settings to share analytics with app developers, Apple gives me anonymous crash reports
and usage figures, without anything that points to you.

## Your rights

You have the right to access, rectification, erasure and restriction of processing, to object, and to lodge a complaint
with a data protection authority, in North Rhine-Westphalia the State Commissioner for Data Protection and Freedom of
Information. As I receive no data from the app, please contact whoever runs your server about the data stored there.
When you sign out in the app's settings, it removes the device from your server and deletes the copy of the messages;
when you delete the app, everything on the device goes with it. I'm happy to answer questions:
[marcel.benders@b-velop.com](mailto:marcel.benders@b-velop.com).

As of: November 2026
