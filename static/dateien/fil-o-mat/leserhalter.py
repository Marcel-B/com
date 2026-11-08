# Tag-Halter mit NFC-Leser: vorn das Fach fürs Musterplättchen, dahinter mit Abstand (sep, je Leser) eine Tasche für die Leser-Platine,
# die von oben eingeschoben wird; Kabel und Stiftleiste gehen oben heraus. Die Magnete sitzen in einem Streifen unter
# dem Leser, also außerhalb der Antenne, nah an der Rückwand.
# Maße in mm. X = Breite, Y = Tiefe (0 = Vorderseite, +Y = Rückseite zur Gehäusewand), Z = Höhe.
# Aufruf: python3 leserhalter.py [name=wert ...]
#   Einzelhalter mit PN532 (MK4S, P1S, Mini):  python3 leserhalter.py
#   5er mit RC522 für die MMU3:                python3 leserhalter.py reader=rc522 count=5
import sys
from manifold3d import Manifold
import numpy as np

# Leser-Platinen: Breite, Höhe, Dicke mit Bauteilen; ant_z = Mitte der Antenne von der Unterkante der Platine
READERS = {
# sep = Abstand Plättchen bis Platine: der PN532 liest erst ab ~1 cm, zuverlässig bei ~26 mm (Test am MK4S, 2026-10-25)
    'pn532': dict(rw=43.0, rh=40.6, rt=4.0, ant_z=20.3, sep=25.0),  # rote PN532-Platine, Antenne rundum am Rand (gemessen)
    'rc522': dict(rw=39.0, rh=59.7, rt=6.05, ant_z=20.0, sep=0.8),  # RC522, Antenne unten, Chip und Leiste oben; Abstand ungetestet
}

P = dict(
    reader='pn532',
    count=1,                                  # Fächer nebeneinander
    slot_w=40.6, slot_h=45.2, slot_d=5.3,     # Platz für ein Plättchen (wie TagHalter.3mf)
    wall=1.0, front=1.3, ledge=2.0,           # Wände, Dicke und Breite der vorderen Leisten
    bottom_ledge=3.0,                         # Leiste unten vorn
    fit=0.4,                                  # Spiel der Leser-Tasche (Breite und Dicke)
    back=1.0,                                 # Rückwand hinter dem Leser
    mag_d=12.0, mag_h=2.66,                   # Magnet
    mag_fit_d=0.15, mag_fit_h=0.05,           # Spiel im Einschub (Variante 2 aus dem Passungstest)
    skin=0.6,                                 # Wand zwischen Magnet und Gehäuse
    mag_gap=1.5,                              # Abstand Magnet-Oberkante bis Leser-Tasche
    magnets=2,                                # Magnete pro Fach (1 oder 2), beim 5er insgesamt 4
    hdr_w=14.0, hdr_h=10.0,                   # Platz oben für die Stiftleiste (Breite, Höhe; gemessen am Druck)
    hdr_d=8.5,                                # Dicke an der Stiftleiste: Platine + Leiste + Biegung der Stifte
    hdr_front=2.0,                            # Kerbe auf der Plättchen-Seite für die Lötstellen der Stifte
    esp=1,                                    # ESP32-C3 oben im Klotz zwischen Plättchen und Leser (nur mit großem Abstand)
    c3_w=20.7, c3_l=25.0, c3_pcb=1.2,         # ESP32-C3 HW-675 ohne USB-Überstand (gemessen)
    c3_back=12.5, c3_lip=1.2, c3_fit=0.4,     # Platz unter der Platine für die Kabel, Leiste über dem Rand, Spiel
    lock='rastnase',                          # ESP sichern: rastnase (Nase in der Nut), stopfen (zweites Teil mit USB-Loch), keine
    c3_end=1.0,                               # zusätzlich so weit lässt sich die Platine einschieben (am Druck gemessen)
)
for a in sys.argv[1:]:
    k, v = a.split('=')
    P[k] = v if k in ('reader', 'lock') else float(v)
R = dict(READERS[P['reader']])
for k in R:
    if k in P: R[k] = P[k]
n = int(P['count'])

def box(x0, y0, z0, x1, y1, z1):
    return Manifold.cube([x1-x0, y1-y0, z1-z0]).translate([x0, y0, z0])

md, mh = P['mag_d'] + P['mag_fit_d'], P['mag_h'] + P['mag_fit_h']
rw, rt = R['rw'] + P['fit'], R['rt'] + P['fit']
cell = max(P['slot_w'], rw)                   # Breite eines Fachs innen
W = n*cell + (n+1)*P['wall']
X0, X1 = -W/2, W/2

# Tiefe: Front, Plättchen, Trennwand, Leser, Rückwand
y_slot0 = P['front']
y_slot1 = y_slot0 + P['slot_d']
y_read0 = y_slot1 + R['sep']
y_read1 = y_read0 + rt
D = max(y_read1, y_read0 + P['hdr_d']) + P['back']
# Magnete müssen in die Tiefe passen
D = max(D, P['skin'] + mh + 2.0)

# Höhe: Magnetstreifen, darüber der Leser; das Plättchen sitzt mittig vor der Antenne
z_read0 = md + P['mag_gap']
ant = z_read0 + R['ant_z']
z_slot0 = ant - P['slot_h']/2
z_slot0 = max(z_slot0, P['wall'])
H_front = z_slot0 + P['slot_h']
H_back = max(H_front, z_read0 + R['rh'])

H_top = max(H_front, H_back)
front = box(X0, 0, 0, X1, y_read0, H_front)
back = box(X0, y_slot1, 0, X1, D, H_back)
body = front + back

for i in range(n):
    cx = X0 + P['wall'] + i*(cell + P['wall']) + cell/2
    sx0, sx1 = cx - P['slot_w']/2, cx + P['slot_w']/2
    body -= box(sx0, y_slot0, z_slot0, sx1, y_slot1, H_front + 1)                         # Fach, oben offen
    body -= box(sx0 + P['ledge'], -1, z_slot0 + P['bottom_ledge'], sx1 - P['ledge'], y_slot0 + 0.01, H_front + 1)  # Fenster vorn
    body -= box(cx - rw/2, y_read0, z_read0, cx + rw/2, y_read1, H_back + 1)              # Leser-Tasche, oben offen
    body -= box(cx - P['hdr_w']/2, y_read1 - 0.01, H_back - P['hdr_h'], cx + P['hdr_w']/2, y_read0 + P['hdr_d'], H_back + 1)  # Stiftleiste
    if R['sep'] > P['hdr_front'] + 0.8:  # bei dünner Trennwand (RC522) ginge die Kerbe bis ins Plättchen-Fach
        body -= box(cx - P['hdr_w']/2, y_read0 - P['hdr_front'], H_back - P['hdr_h'], cx + P['hdr_w']/2, y_read0 + 0.01, H_top + 1)  # Lötstellen

# ESP32-C3 oben im Klotz: wird von links eingeschoben (USB-C schaut links heraus), Display oben; die Kabel laufen unter
# der Platine und durch einen Schlitz nach hinten zur Stiftleiste des Lesers
c3w, c3l = P['c3_w'] + P['c3_fit'], P['c3_l'] + P['c3_fit']
plug = None
y_c3 = (y_slot1 + 1.0 + y_read0 - P['hdr_front'] - 0.8) / 2 - c3w/2 if int(P['esp']) else None
if y_c3 is not None and y_c3 >= y_slot1 + 0.8 and y_c3 + c3w <= y_read0 - P['hdr_front'] - 0.6:
    z_lip = H_front - P['c3_lip']
    z_pcb = z_lip - (P['c3_pcb'] + 1.0)
    z_wire = z_pcb - P['c3_back']
    lip = 1.4
    xe = X0 + c3l + P['c3_end']
    body -= box(X0 - 1, y_c3 + 0.6, z_wire, xe, y_c3 + c3w - 0.6, z_pcb + 0.01)        # Kabel unter der Platine
    body -= box(X0 - 1, y_c3, z_pcb, xe, y_c3 + c3w, z_lip)                             # Nut für die Platine
    body -= box(X0 - 1, y_c3 + lip, z_lip - 0.01, xe - lip, y_c3 + c3w - lip, H_top + 1)  # Fenster fürs Display
    body -= box(xe - 8, y_c3 + c3w - lip - 0.01, z_wire, xe - 2, y_read0 + 0.01, H_top + 1)       # Kabelschlitz zum Leser
    x_board = xe - c3l                     # so weit vorn endet die eingeschobene Platine
    if P['lock'] == 'rastnase':
        # Je eine rautenförmige Nase an den Seiten der Nut, knapp vor der Platine: sie drückt sich beim Einschieben
        # vorbei und hält die Platine dann an ihrer Kante; zum Herausnehmen mit einem Schraubendreher wegdrücken
        a = 0.4 * 2**0.5
        for y in (y_c3, y_c3 + c3w):
            nub = Manifold.cube([a, a, z_lip - z_pcb], True).rotate([0, 0, 45]).translate([x_board - 0.5, y, (z_pcb + z_lip)/2])
            body += nub
    elif P['lock'] == 'stopfen':
        # Stopfen: Platte außen, Zunge in der Nut bis an die Platine, Loch für den USB-C-Stecker
        f, t, depth = 0.1, 1.6, x_board - X0 - 0.2
        zu = z_pcb + P['c3_pcb']           # Unterkante der USB-Buchse (liegt auf der Platine)
        plug = (box(X0 - t, y_c3 - 1.5, z_wire - 1.5, X0, y_c3 + c3w + 1.5, H_top)
                + box(X0 - 0.01, y_c3 + f, z_pcb + f, X0 + depth, y_c3 + c3w - f, z_lip - f)
                + box(X0 - 0.01, y_c3 + 0.6 + f, z_wire + f, X0 + depth, y_c3 + c3w - 0.6 - f, z_pcb + 0.01))
        plug -= box(X0 - t - 1, y_c3 + c3w/2 - 6.5, zu - 2.5, X0 + depth + 1, y_c3 + c3w/2 + 6.5, zu + 3.2 + 2.5)  # Stecker
        # Kabel unter der Platine: Zunge dort nur als Rahmen
        plug -= box(X0 - 0.02, y_c3 + 2.0, z_wire + 1.5, X0 + depth + 1, y_c3 + c3w - 2.0, z_pcb + 0.02)
    print(f"ESP32-C3 oben: Tasche {c3l:.1f} x {c3w:.1f}, Platine ab z={z_pcb:.1f}, Display ragt {P['c3_pcb'] + 4.8 - (H_front - z_pcb):.1f} mm heraus")
elif int(P['esp']):
    print("ESP32-C3 passt nicht in den Klotz (Abstand zu klein), esp_gehaeuse.py nehmen")

# Magnete von unten, bündig mit der Unterkante, nah an der Rückwand
y_mag = D - P['skin'] - mh
def from_below(x):
    z = md/2
    pocket = Manifold.cylinder(mh, md/2, md/2, 96).rotate([-90, 0, 0]).translate([x, y_mag, z])
    return pocket + box(x - md/2, y_mag, -1, x + md/2, y_mag + mh, z)

if n == 1:
    xs = [0] if int(P['magnets']) == 1 else [-cell/4, cell/4]
else:
    a = X1 - 14
    xs = [-a, -a/3, a/3, a]
for x in xs:
    body -= from_below(x)

mesh = body.to_mesh()
v = np.asarray(mesh.vert_properties)[:, :3]; t = np.asarray(mesh.tri_verts)
print("Maße", np.round(v.max(0)-v.min(0), 2), "Volumen cm3", round(body.volume()/1000, 2), "Genus", body.genus())
print(f"Plättchen ab z={z_slot0:.1f}, Leser ab z={z_read0:.1f}, Leser-Tasche {rw:.1f} x {rt:.1f}, Abstand Plättchen-Platine {R['sep']} mm")

def write_3mf(path, parts, title):
    import zipfile
    objs, items = [], []
    for i, (v, t) in enumerate(parts, 1):
        vs = "\n".join(f'<vertex x="{a:.4f}" y="{b:.4f}" z="{c:.4f}"/>' for a, b, c in v)
        ts = "\n".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in t)
        objs.append(f'<object id="{i}" name="{title}-{i}" type="model"><mesh><vertices>\n{vs}\n</vertices><triangles>\n{ts}\n</triangles></mesh></object>')
        items.append(f'<item objectid="{i}"/>')
    model = f'''<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="de-DE" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">
<metadata name="Title">{title}</metadata>
<resources>{"".join(objs)}</resources>
<build>{"".join(items)}</build></model>'''
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('3D/3dmodel.model', model)

# Druckausrichtung: stehend, Boden aufs Bett (Einschübe und Taschen brauchen keine Stützen)
name = f"LeserHalter-{P['reader'].upper()}" + ('' if n == 1 else f'-{n}er')
parts = [(v - v.min(0), t)]
if plug is not None:
    # Stopfen daneben, mit der Platte aufs Bett
    pm = plug.rotate([0, -90, 0]).to_mesh()
    pv = np.asarray(pm.vert_properties)[:, :3]
    pv = pv - pv.min(0) + [v.max(0)[0] - v.min(0)[0] + 8, 0, 0]
    parts.append((pv, np.asarray(pm.tri_verts)))
    print("Stopfen: Maße", np.round(pv.max(0)-pv.min(0), 2), "Genus", plug.genus())
    name += '-Stopfen'
elif int(P['esp']) and n == 1 and P['lock'] == 'rastnase':
    name += '-Rastnase'
write_3mf(name + '.3mf', parts, name)
print(name + '.3mf')
