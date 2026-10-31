# Tag-Halter: Hülse(n) hochkant für Musterplättchen, Magnete (Neodym) in Einschüben in der Rückwand.
# Maße in mm. X = Breite, Y = Tiefe (0 = Vorderseite, +Y = Rückseite zur Gehäusewand), Z = Höhe.
# Aufruf: python3 taghalter_coreone.py [name=wert ...]
#   Einzelhalter (Core One / MK4):  python3 taghalter_coreone.py
#   5er für die MMU3:               python3 taghalter_coreone.py count=5
import sys
from manifold3d import Manifold
import numpy as np

P = dict(
    count=1,                                  # Fächer nebeneinander
    slot_w=40.6, slot_h=45.2, slot_d=5.3,     # Platz für ein Plättchen (wie TagHalter.3mf)
    wall=1.0, front=1.3, ledge=2.0,           # Wände, Dicke und Breite der vorderen Leisten
    bottom_ledge=3.0,                         # Leiste unten vorn
    mag_d=12.0, mag_h=2.66,                   # Magnet
    mag_fit_d=0.15, mag_fit_h=0.05,           # Spiel im Einschub (Variante 2 aus dem Passungstest)
    skin=0.6,                                 # Wand zwischen Magnet und Gehäuse
    inner=0.8,                                # Wand zwischen Magnet und Plättchen
    end_inset=14,                             # Abstand der äußeren Magnetmitten vom Rand (nur count > 1)
)
for a in sys.argv[1:]:
    k, v = a.split('='); P[k] = float(v)
n = int(P['count'])

def box(x0, y0, z0, x1, y1, z1):
    return Manifold.cube([x1-x0, y1-y0, z1-z0]).translate([x0, y0, z0])

W = n*P['slot_w'] + (n+1)*P['wall']
X0, X1 = -W/2, W/2
yb = P['front'] + P['slot_d']                       # Beginn Rückwand
md, mh = P['mag_d'] + P['mag_fit_d'], P['mag_h'] + P['mag_fit_h']
D = yb + P['inner'] + mh + P['skin']
H = P['wall'] + P['slot_h']
y0 = yb + P['inner']                                # Vorderseite der Magnettaschen

body = box(X0, 0, 0, X1, D, H)
for i in range(n):
    sx0 = X0 + P['wall'] + i*(P['slot_w'] + P['wall'])
    sx1 = sx0 + P['slot_w']
    body -= box(sx0, P['front'], P['wall'], sx1, yb, H+1)                                # Fach, oben offen
    body -= box(sx0+P['ledge'], -1, P['bottom_ledge'], sx1-P['ledge'], P['front']+0.01, H+1)  # Fenster vorn

def pocket(x, z):
    return Manifold.cylinder(mh, md/2, md/2, 96).rotate([-90, 0, 0]).translate([x, y0, z])

def from_below(x):
    """Einschub von unten: Magnet schließt bündig mit der Unterkante ab."""
    z = md/2
    return pocket(x, z) + box(x - md/2, y0, -1, x + md/2, y0 + mh, z)

def from_side(x, direction):
    """Einschub von der Seite (direction -1 = links, 1 = rechts), Magnet 1 mm über dem Boden."""
    z = 1.0 + md/2
    end = X0 - 1 if direction < 0 else X1 + 1
    return pocket(x, z) + box(min(x, end), y0, z - md/2, max(x, end), y0 + mh, z + md/2)

if n == 1:
    cuts = [from_below(0)]
else:
    # vier Magnete gleichmäßig: außen seitlich, dazwischen zwei von unten
    a = X1 - P['end_inset']
    cuts = [from_side(-a, -1), from_below(-a/3), from_below(a/3), from_side(a, 1)]
for c in cuts:
    body -= c

mesh = body.to_mesh()
v = np.asarray(mesh.vert_properties)[:, :3]; t = np.asarray(mesh.tri_verts)
print("Maße", np.round(v.max(0)-v.min(0), 2), "Volumen cm3", round(body.volume()/1000, 2), "Genus", body.genus())

def write_3mf(path, v, t, title):
    import zipfile
    vs = "\n".join(f'<vertex x="{a:.4f}" y="{b:.4f}" z="{c:.4f}"/>' for a, b, c in v)
    ts = "\n".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in t)
    model = f'''<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="de-DE" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">
<metadata name="Title">{title}</metadata>
<resources><object id="1" name="{title}" type="model"><mesh><vertices>
{vs}
</vertices><triangles>
{ts}
</triangles></mesh></object></resources>
<build><item objectid="1"/></build></model>'''
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('3D/3dmodel.model', model)

# Druckausrichtung: stehend, Boden aufs Bett (Einschübe brauchen keine Stützen)
name = 'TagHalter-CoreOne' if n == 1 else f'TagHalter-{n}er'
write_3mf(name + '.3mf', v - v.min(0), t, name)
print(name + '.3mf')
