---
titel: Building the NFC reader for the printer
beschreibung: An ESP32 with an NFC reader recognises which swatch sits at the printer and reports it to the server. With parts list, wiring, ESPHome and holders to print.
---

The Snapmaker U1 reads the NFC tags of its spools itself. Other printers cannot, and there you would have to tap
**Load into printer** in the app after every spool change. The NFC reader does that for you: a
holder with one slot per printer slot hangs on the printer. You put the swatch of the type you are loading into
it, an ESP32 reads it and tells the server which swatch sits in which slot. The server puts a spool of that type into the
slot and books the next print's usage onto it.

This guide is the third part after [the server](/en/projekte/fil-o-mat/server-einrichten.html) and
[the apps](/en/projekte/fil-o-mat/apps-einrichten.html). The swatches must already be assigned to a type in the
app.

The reader's display still shows German texts; this guide gives their meaning in brackets.

## Which variant for which printer

| Printer | Build | ESPHome file |
| --- | --- | --- |
| one slot, e.g. Prusa MK4S, Mini or Bambu P1S with external spool | ESP32-C3 with display and one PN532, one pocket | `fach-1x-pn532.yaml` |
| Prusa Core One with MMU3 | ESP32 DevKit and five RC522, one reader per pocket | `fach-5x-rc522.yaml` |
| many slots, e.g. Anycubic Kobra X with ACE | ESP32-C3 with display and one PN532 in tap mode: tap the swatch, choose the slot with a button | `tippen-pn532.yaml` |

So far the variant with one pocket has been tried on a Prusa MK4S. The MMU3 variant with five readers and tap mode are
fully built and compile without errors, but have not yet run on a printer. So it is best to start with a printer with
one slot.

## What you need

For a printer with one slot or for tap mode:

- an ESP32-C3 board with a built-in 0.42" OLED (often sold as HW-675, 20.7 × 25 mm)
- a PN532 NFC module (the red board with two small switches for I²C and SPI)
- four wires, such as female Dupont wires
- a USB-C cable for flashing and a USB power supply for continuous use

For the MMU3 with five pockets:

- an ESP32 DevKit with 38 pins (ESP32-WROOM-32)
- five RC522 modules
- wires for the shared SPI bus, most conveniently on a piece of perfboard
- a micro USB cable and a USB power supply

For the holders:

- neodymium disc magnets 12 mm in diameter and a good 2.6 mm high; they hold the holder on the printer's frame
- filament without metal or carbon fibre, so PLA or PETG for example; fibres with metal or carbon can dampen the radio
  field

You also need a computer with Python 3, a soldering iron and your swatches with NTAG tags.

## 1. Wiring

**PN532 on the ESP32-C3.** First set the two switches on the PN532 to I²C: switch 1 ON, switch 2 OFF. The reader shares
the I²C bus with the C3's display, so four wires are enough:

| PN532 | VCC | GND | SDA | SCL |
| --- | --- | --- | --- | --- |
| ESP32-C3 | 3V3 | GND | GPIO5 | GPIO6 |

On the C3 you solder the four wires on directly, without a pin header, so it fits into the holder later. On the PN532
you plug them onto the four-pin header.

**Five RC522 on the ESP32 DevKit.** All readers are connected in parallel to power and to the three data lines of the
SPI bus. Only the SDA line (used here as chip select) goes to each reader separately. RST goes to 3.3 V, IRQ stays
free.

| RC522 | 3.3V | GND | SCK | MOSI | MISO | RST |
| --- | --- | --- | --- | --- | --- | --- |
| ESP32 DevKit (all readers) | 3V3 | GND | GPIO18 | GPIO23 | GPIO19 | 3V3 |

| Slot | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| SDA to | GPIO26 | GPIO17 | GPIO16 | GPIO4 | GPIO13 |

Never connect the readers to 5 V. Both PN532 and RC522 run on 3.3 V here.

## 2. Install ESPHome

The readers run on [ESPHome](https://esphome.io). Install it once in a Python environment of its own and fetch the
repository with the ready-made configurations:

```sh
python3 -m venv ~/esphome
~/esphome/bin/pip install esphome
git clone https://github.com/Marcel-B/fil-o-mat.git
cd fil-o-mat/reader
```

After that the command is `~/esphome/bin/esphome`. If you want to call it simply as `esphome`, add an alias once:

```sh
echo 'alias esphome=~/esphome/bin/esphome' >> ~/.zshrc && source ~/.zshrc
```

The ESP32-C3 needs no driver. If your computer does not recognise the DevKit, it is usually missing Silicon Labs'
CP210x driver.

## 3. Enter credentials and printer

Copy the example file and enter your Wi-Fi and the server's address:

```sh
cp secrets.example.yaml secrets.yaml
```

```yaml
wifi_ssid: "MyWiFi"
wifi_password: "…"
filomat_url: "http://192.168.1.50:8080"
filomat_api_key: ""
ota_password: ""
```

For `filomat_url` use the address in your home network with `http`, not the Tailscale address: the ESP32 does not join
the tailnet. If an API key is set on the server, it goes into `filomat_api_key`. The file `secrets.yaml` stays on your
computer and is not added to the repository.

Now you need the printer's ID. Open `http://192.168.1.50:8080/api/printers` in your browser. Each printer has
`"id": "…"` next to its name. With an API key it works in the terminal:

```sh
curl -H "X-Api-Key: …" http://192.168.1.50:8080/api/printers
```

Create a small file of its own for each printer that includes the shared configuration, here `mk4s.yaml`:

```yaml
substitutions:
  name: filomat-mk4s
  friendly_name: fil-O-mat MK4S
  printer_id: "ID from /api/printers"

packages:
  fach: !include fach-1x-pn532.yaml
```

For the MMU3 you include `fach-5x-rc522.yaml`, for tap mode `tippen-pn532.yaml`. Because your file only contains the
three values, later improvements arrive by themselves with `git pull`.

## 4. Flash and check

Connect the ESP32 by USB and run:

```sh
esphome run mk4s.yaml
```

The first run downloads the tools and takes five to ten minutes. If ESPHome asks for the port, choose the USB entry,
such as `/dev/cu.usbmodem…` for the C3 or `/dev/cu.usbserial…` for the DevKit. If none appears, hold down the BOOT
button while plugging in the cable. Later, once the ESP32 is on your Wi-Fi, updates work without a cable: then choose
the “Over The Air” entry.

After uploading, the log keeps running. It shows you whether everything is right:

- `Connected` with an IP address: the ESP32 is on your Wi-Fi.
- In the I²C scan, `Found device at address 0x24` (PN532) and `0x3C` (display).
- Hold a swatch to the reader. A line with `Backend: HTTP 200` and `"state":"known"` follows.

```text
Backend: HTTP 200 {"slots":[{"slot":0,"tag":"0423BC53CB2A81","state":"known","label":"eSun PLA #1",…}]}
```

The display shows “Eingelegt” (loaded) with the type and the spool number, and in the app the spool is now in the
printer. With the MMU3 you hold a swatch to each reader in turn. It must appear in the right slot in the log; if it shows
up elsewhere, two SDA lines are swapped.

You can look at the log again at any time:

```sh
esphome logs mk4s.yaml
```

## 5. Print the holders

The holders have a pocket for the swatch at the front and a compartment for the reader behind it. Magnets in the
base hold them on the printer's frame. They sit below the reader and so outside its antenna, because right behind it
they would disturb reception. They are printed standing, base on the bed; you need no supports.

An important measure is the distance between swatch and reader. The PN532 reads a swatch only from about one centimetre
away and reliably from a good two centimetres. The holder for the PN532 therefore keeps a distance of 25 mm and is 41 mm
deep as a result. The ESP32-C3 sits right in the block in between: it slides in from the left, the display looks out at
the top, the USB-C socket on the left. Below it there is room for the wires, and a slot leads them back to the reader.

| Part | For | Size (W × D × H) | Files |
| --- | --- | --- | --- |
| PN532 reader holder with snap catch: two catches hold the C3 | one slot, tap mode | 45 × 41 × 57 mm | [3MF](/dateien/fil-o-mat/LeserHalter-PN532-Rastnase.3mf), [STL](/dateien/fil-o-mat/LeserHalter-PN532-Rastnase.stl) |
| PN532 reader holder with plug: a second part with a USB hole closes the opening | one slot, tap mode | 45 × 41 × 57 mm, plug beside it | [3MF](/dateien/fil-o-mat/LeserHalter-PN532-Stopfen.3mf), [STL](/dateien/fil-o-mat/LeserHalter-PN532-Stopfen.stl) |
| RC522 reader holder, five pockets | MMU3 | 209 × 17 × 73 mm | [3MF](/dateien/fil-o-mat/LeserHalter-RC522-5er.3mf), [STL](/dateien/fil-o-mat/LeserHalter-RC522-5er.stl) |
| Case for the ESP32 DevKit, box with lid | MMU3 | 72 × 63 × 28 mm | [3MF](/dateien/fil-o-mat/ESP-Gehaeuse-DevKit.3mf), [STL](/dateien/fil-o-mat/ESP-Gehaeuse-DevKit.stl) |
| Tag holder without reader, one pocket | just keeping swatches, e.g. at the U1 | 43 × 11 × 46 mm | [3MF](/dateien/fil-o-mat/TagHalter-CoreOne.3mf), [STL](/dateien/fil-o-mat/TagHalter-CoreOne.stl) |
| Tag holder without reader, five pockets | MMU3 without reader | 209 × 11 × 46 mm | [3MF](/dateien/fil-o-mat/TagHalter-5er.3mf), [STL](/dateien/fil-o-mat/TagHalter-5er.stl) |
| Fit test for the magnets: five slots, tighter from left to right | before the first holder | 85 × 4 × 18 mm | [3MF](/dateien/fil-o-mat/Magnet-Passungstest.3mf), [STL](/dateien/fil-o-mat/Magnet-Passungstest.stl) |

You open the 3MF files directly in your slicer; for the holder with plug and the DevKit case both parts already lie
side by side. The STL files contain the same parts.

The holders with a built-in C3 and the RC522 holder are new and not yet proven in continuous use. Print the fit test
first and check with a reader whether the range reaches through the printed holder.

This is how you assemble the PN532 holder:

1. Press the magnets into their slots from below.
2. Slide the PN532 into the rear compartment from above, components facing back, the smooth side towards the swatch.
   The pin header sticks out at the top.
3. Slide the C3 with its soldered wires into the block from the left until the catches engage or the plug sits, and
   lead the wires through the slot to the pin header.
4. Put the holder on the frame and insert a swatch into the pocket.

## 6. Adapt the holders to your parts

All parts are generated by small Python scripts. Every measure is a parameter in them that you can change when calling
the script. You need the packages `manifold3d` and `numpy`:

```sh
python3 -m venv ~/halter
~/halter/bin/pip install manifold3d numpy
~/halter/bin/python leserhalter.py                          # PN532 with snap catch
~/halter/bin/python leserhalter.py lock=stopfen             # PN532 with plug
~/halter/bin/python leserhalter.py reader=rc522 count=5     # five RC522 for the MMU3
~/halter/bin/python leserhalter.py sep=20                   # less distance between swatch and reader
```

| Script | Generates |
| --- | --- |
| [leserhalter.py](/dateien/fil-o-mat/leserhalter.py) | reader holder with PN532 or RC522, optionally with built-in C3 |
| [esp_gehaeuse.py](/dateien/fil-o-mat/esp_gehaeuse.py) | case for the DevKit (`board=devkit`) or a single rail for the C3 (`board=c3`) |
| [taghalter_coreone.py](/dateien/fil-o-mat/taghalter_coreone.py) | tag holder without reader, `count=5` for five pockets |
| [magnet_passungstest.py](/dateien/fil-o-mat/magnet_passungstest.py) | fit test for the magnets |

The parameters are explained at the top of each script, such as `mag_d` and `mag_h` for other magnets or `slot_w` and
`slot_h` for larger swatches. The result is a 3MF file in the current folder each time.

## 7. How you work with it

- **One pocket per slot:** load the spool, put the swatch into the pocket, done. The display shows the type with the
  spool number. Pulling the swatch out changes nothing in the stock. The spool stays loaded until another swatch comes or
  you move it in the app.
- **Tap mode:** hold the swatch to the reader, the display shows the type. With the BOOT button you choose the slot, each
  press one further (on the Kobra X 1–4 in the printer, 5–8 in the ACE). Four seconds after the last press the spool
  goes into that slot. Without a button press the reader gives up after 15 seconds.
- **Unknown swatch:** the display shows “Unbekannt” (unknown), and with ntfy set up a notification arrives on your phone.
  Assign the swatch to a type in the app and insert it again.

## When something does not work

| What you see | Cause | What helps |
| --- | --- | --- |
| `command not found: esphome` | ESPHome is not on the path | call `~/esphome/bin/esphome` or add the alias |
| ESP32 does not appear when flashing | not in flash mode, or a charge-only cable | hold BOOT while plugging in, try another cable |
| no `0x24` in the I²C scan | PN532 switches not set to I²C, or SDA and SCL swapped | switch 1 ON, 2 OFF; swap the wires on GPIO5 and GPIO6 |
| swatch is not recognised | too close to the reader, or a magnet in front of the antenna | increase the distance, keep magnets outside the antenna |
| display “nicht erreichbar” (unreachable) | wrong address, or the Tailscale address entered | home network address in `secrets.yaml`, then flash again |
| display “Fehler 404” (error 404) | server too old, or wrong `printer_id` | update the server, check the ID under `/api/printers` |
| display “Fehler 401” (error 401) | API key missing or wrong | `filomat_api_key` in `secrets.yaml` |
| one MMU3 slot flickers in the log | neighbouring RC522 interfere with each other | more distance between the readers |

The address and all other values are written into the firmware when it is built. So after every change to
`secrets.yaml` or your printer file, flash again with `esphome run`. More details on the wiring and on how the server
behaves are in the [reader's README](https://github.com/Marcel-B/fil-o-mat/blob/main/reader/README.md) (in German).
