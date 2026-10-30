# Gehäuse für die ESPs der NFC-Leser, mit Magneten im Boden (haften am Rahmen wie die Tag-Halter).
# Maße in mm. X = Breite, Y = Länge (0 = USB-Seite), Z = Höhe (0 = Boden, der am Drucker anliegt).
#
#   board=c3      ESP32-C3 mit 0,42"-OLED: Schiene, die Platine wird von oben eingeschoben, Display schaut vorn heraus,
#                 USB-C unten frei, die beiden Tasten oben bleiben erreichbar. Die 4 Kabel direkt anlöten (keine
#                 Stiftleisten), sie gehen oben heraus.
#   board=devkit  ESP32-DevKit für die MMU3 mit Dupont-Kabeln: Kasten mit Deckel, USB-Öffnung, Kabelschlitz am anderen Ende.
#
# Aufruf: python3 esp_gehaeuse.py [board=c3|devkit] [name=wert ...]
import sys
from manifold3d import Manifold
import numpy as np

P = dict(
    board='c3',
    # ESP32-C3 HW-675 (Platine ohne USB-Überstand)
    c3_w=20.7, c3_l=25.0, c3_pcb=1.2,   # gemessen: 20,7 x 25, 6 hoch samt Display
    c3_back=2.5,            # Platz unter der Platine für die angelöteten Kabel
    c3_top=4.8,             # Display über der Platine
    c3_lip=1.2,             # Leiste, die die Platine vorn hält (links, rechts, unten)
    usb_w=9.5, usb_h=3.6,   # USB-C-Öffnung
    # ESP32-DevKit (AZ-Delivery, 38 Pins)
    dk_w=27.8, dk_l=55.0,   # gemessen: 55 x 27,8, mit Stiften 13 hoch
    dk_depth=24.0,          # Platine, Stifte (8,3 mm) und Dupont-Stecker darauf
    slot_w=16.0, slot_h=8.0,  # Kabelschlitz am Ende gegenüber USB
    fit=0.4, wall=1.6,
    mag_d=12.0, mag_h=2.66, mag_fit_d=0.15, mag_fit_h=0.05, inner=0.8,
)
for a in sys.argv[1:]:
    k, v = a.split('=')
    P[k] = v if k == 'board' else float(v)

def box(x0, y0, z0, x1, y1, z1):
    return Manifold.cube([x1-x0, y1-y0, z1-z0]).translate([x0, y0, z0])

md, mh = P['mag_d'] + P['mag_fit_d'], P['mag_h'] + P['mag_fit_h']
floor = mh + P['inner']

def magnet(x, y):
    """Magnet von unten bündig eingepresst (Spiel wie Variante 2 aus dem Passungstest), liegt direkt am Rahmen an."""
    return Manifold.cylinder(mh + 0.01, md/2, md/2, 96).translate([x, y, -0.01])

def write_3mf(path, parts, title):
    import zipfile
    objs, items = [], []
    for i, (part, offset) in enumerate(parts, 1):
        mesh = part.translate(offset).to_mesh()
        v = np.asarray(mesh.vert_properties)[:, :3]; t = np.asarray(mesh.tri_verts)
        vs = "\n".join(f'<vertex x="{a:.4f}" y="{b:.4f}" z="{c:.4f}"/>' for a, b, c in v)
        ts = "\n".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in t)
        objs.append(f'<object id="{i}" name="{title}-{i}" type="model"><mesh><vertices>\n{vs}\n</vertices><triangles>\n{ts}\n</triangles></mesh></object>')
        items.append(f'<item objectid="{i}"/>')
        print(f"Teil {i}: Maße", np.round(v.max(0)-v.min(0), 2), "Genus", part.genus())
    model = f'''<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="de-DE" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">
<metadata name="Title">{title}</metadata>
<resources>{"".join(objs)}</resources>
<build>{"".join(items)}</build></model>'''
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('3D/3dmodel.model', model)
    print(path)

w = P['wall']
if P['board'] == 'c3':
    bw, bl = P['c3_w'] + P['fit'], P['c3_l'] + P['fit']
    groove = P['c3_pcb'] + 1.0                      # Nut für die Platine, Platz für Lötstellen vorn
    z_pcb = floor + P['c3_back']
    z_lip = z_pcb + groove
    H = z_lip + P['c3_lip']
    lip = 1.4                                      # so weit greift die Leiste über den Rand der Platine
    W, L = bw + 2*w, bl + w                        # oben offen: dort wird eingeschoben
    body = box(0, 0, 0, W, L, H)
    # Raum unter der Platine (für Kabel), Nut für die Platine, Fenster vorn
    body -= box(w + 0.6, w, floor, W - w - 0.6, L + 1, z_pcb)   # nur 0,6 mm Auflage, die Kabel sitzen an den Pins
    body -= box(w, w, z_pcb, W - w, L + 1, z_lip)
    body -= box(w + lip, w + lip, z_lip - 0.01, W - w - lip, L + 1, H + 1)
    # USB-C unten mittig
    body -= box(W/2 - P['usb_w']/2, -1, z_pcb, W/2 + P['usb_w']/2, w + lip + 0.5, H + 1)   # auch die Leiste über der Buchse
    body -= magnet(W/2, L/2)
    write_3mf('ESP-Gehaeuse-C3.3mf', [(body, [0, 0, 0])], 'ESP-Gehaeuse-C3')
else:
    bw, bl = P['dk_w'] + 2*P['fit'], P['dk_l'] + 2*P['fit'] + 4.0   # 4 mm für den Bogen der Kabel am Schlitz
    W, L = bw + 2*w, bl + 2*w
    H = floor + P['dk_depth']
    body = box(0, 0, 0, W, L, H) - box(w, w, floor, W - w, L - w, H + 1)
    # USB (Micro-USB oder USB-C) an der Stirnseite, Kabelschlitz gegenüber, beide von oben offen
    body -= box(W/2 - 6, -1, H - 9, W/2 + 6, w + 0.01, H + 1)
    body -= box(W/2 - P['slot_w']/2, L - w - 0.01, H - P['slot_h'], W/2 + P['slot_w']/2, L + 1, H + 1)
    for y in (L*0.28, L*0.72):
        body -= magnet(W/2, y)
    # Deckel mit umlaufendem Rand, der innen klemmt
    rim, t = 2.0, 1.6
    lid = box(0, 0, 0, W, L, t) + box(w + 0.2, w + 0.2, t - 0.01, W - w - 0.2, L - w - 0.2, t + rim)
    lid -= box(w + 1.4, w + 1.4, t, W - w - 1.4, L - w - 1.4, t + rim + 1)
    # Aussparungen im Rand über USB und Schlitz
    lid -= box(W/2 - 6.5, w - 1, t, W/2 + 6.5, w + 2, t + rim + 1)
    lid -= box(W/2 - P['slot_w']/2 - 0.5, L - w - 2, t, W/2 + P['slot_w']/2 + 0.5, L - w + 1, t + rim + 1)
    write_3mf('ESP-Gehaeuse-DevKit.3mf', [(body, [0, 0, 0]), (lid, [W + 8, 0, 0])], 'ESP-Gehaeuse-DevKit')
