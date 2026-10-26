# Genera KIDBOX/BOM.csv, KIDBOX/BOM_compra.csv (lista de compra completa, desde COMPRA de kidbox_datos.py) y
# KIDBOX/netlist.csv a partir del esquematico REAL (kicad-cli sch export netlist),
# y comprueba que cada red coincide con scripts/kidbox_datos.py (ESPECIFICACION.md seccion 5). Si algo no
# coincide, lo dice y sale con codigo 1 (el esquematico y la especificacion se han separado).
#
# Uso (Python 3.8+ del sistema), desde hardware/:
#     python scripts/gen_bom_netlist.py
import csv
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from kidbox_datos import COMPONENTES, COMPRA, PROYECTO  # noqa: E402

CARPETA = os.path.normpath(os.path.join(AQUI, "..", PROYECTO))
CLI = next(c for c in (os.environ.get("KICAD_CLI"), r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe",
                       shutil.which("kicad-cli")) if c and os.path.exists(c))

DESCRIPCION = {  # (lib_id, prefijo de huella) -> descripcion para la BOM
    "Connector_Generic": "Tira de pines hembra 1x{n}, paso 2.54 mm, recta",
    "Switch:SW_Push": "Pulsador tactil 6x6 mm, 4 patas",
    "Switch:SW_SPDT_312": "Interruptor deslizante 1 polo 2 posiciones, recto, paso 2.54 mm (Wuerth WS-SLTV 450301014042 o equivalente)",
    "Device:C": "Condensador ceramico de disco, paso 5 mm",
    "Device:C_Polarized": "Condensador electrolitico radial D4 mm, paso 1.5 mm",
    "Connector:TestPoint": "Punto de prueba THT, pad D2.0 mm (no se compra)",
    "Device:Battery_Cell": "Bateria LiPo de una celda (no va en la placa)",
    "Mechanical:MountingHole": "Agujero de montaje sin metalizar (no se compra)",
}


def descripcion(lib, huella):
    if lib.startswith("Connector_Generic"):
        return DESCRIPCION["Connector_Generic"].format(n=int(lib.split("x")[1]))
    return DESCRIPCION[lib]


def orden_ref(r):
    letras = r.rstrip("0123456789")
    return letras, int(r[len(letras):])


tmp = os.path.join(tempfile.mkdtemp(), "kidbox.xml")
subprocess.run([CLI, "sch", "export", "netlist", "--format", "kicadxml", "-o", tmp,
                os.path.join(CARPETA, PROYECTO + ".kicad_sch")], check=True, capture_output=True)
raiz = ET.parse(tmp).getroot()

# Componentes reales del esquematico
reales = {}
for c in raiz.find("components"):
    lib = c.find("libsource")
    reales[c.get("ref")] = dict(valor=c.findtext("value"), huella=c.findtext("footprint") or "",
                                lib=f"{lib.get('lib')}:{lib.get('part')}")
errores = []
if set(reales) != set(COMPONENTES):
    errores.append(f"referencias distintas: {sorted(set(reales) ^ set(COMPONENTES))}")

# Redes reales
redes = {}
for n in raiz.iter("net"):
    nombre = n.get("name").lstrip("/")
    redes[nombre] = sorted(((x.get("ref"), x.get("pin")) for x in n.iter("node")), key=lambda t: (orden_ref(t[0]), int(t[1])))
esperado = {}
for ref, c in COMPONENTES.items():
    for num, (_, red) in (c["pines"] or {}).items():
        if red:
            esperado.setdefault(red, []).append((ref, str(num)))
for red, nodos in esperado.items():
    if sorted(nodos) != sorted(redes.get(red, [])):
        errores.append(f"red {red}: esperado {sorted(nodos)}, esquematico {redes.get(red)}")
for red, nodos in redes.items():
    if red.startswith("unconnected-"):
        ref, pin = nodos[0]
        if COMPONENTES[ref]["pines"][int(pin)][1] is not None:
            errores.append(f"{ref}.{pin} quedo sin conectar en el esquematico")
    elif red not in esperado:
        errores.append(f"red inesperada en el esquematico: {red}")

# netlist.csv: Red, Componente, Pin, Funcion (una fila por pin, incluidos los sin conectar)
filas = []
for red, nodos in redes.items():
    for ref, pin in nodos:
        funcion = COMPONENTES[ref]["pines"][int(pin)][0]
        if ref in ("J1", "J2"):
            n_mod = int(pin) + (0 if ref == "J1" else 20)
            funcion = f"RP2350-Plus pin {n_mod} ({funcion})"
        elif ref == "J3":
            funcion = f"Pantalla {funcion}"
        elif ref == "J5":
            funcion = f"DAC {funcion}"
        elif ref.startswith("SW") and ref != "SW10":
            funcion = f"Pulsador {COMPONENTES[ref]['valor']}, pata {pin}"
        elif ref == "SW10":
            funcion = f"Interruptor ON/OFF, {funcion}"
        elif ref.startswith("TP"):
            funcion = f"Punto de prueba {COMPONENTES[ref]['valor']}"
        elif ref == "BT1":
            funcion = f"Bateria, polo {funcion} (al conector BAT del RP2350-Plus)"
        elif ref.startswith("C"):
            funcion = f"Condensador {COMPONENTES[ref]['valor']}, pata {funcion}"
        filas.append(("(sin conectar)" if red.startswith("unconnected-") else red, ref, pin, funcion))
filas.sort(key=lambda f: (f[0] == "(sin conectar)", f[0], orden_ref(f[1]), int(f[2])))
with open(os.path.join(CARPETA, "netlist.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Red", "Componente", "Pin", "Funcion"])
    w.writerows(filas)

# BOM.csv: agrupado por huella + cara + notas; el valor se une si difiere (p. ej. nombres de botones)
grupos = {}
for ref in sorted(reales, key=orden_ref):
    c, r = COMPONENTES[ref], reales[ref]
    if r["huella"] != c["huella"] or r["valor"] != c["valor"]:
        errores.append(f"{ref}: huella/valor del esquematico ({r['huella']}, {r['valor']}) != datos")
    clave = (r["huella"], c["cara"], c["notas"], r["lib"])
    grupos.setdefault(clave, []).append((ref, r["valor"]))
with open(os.path.join(CARPETA, "BOM.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Referencia", "Cantidad", "Valor", "Descripcion", "Huella KiCad", "THT/SMD", "Cara", "Notas"])
    for (huella, cara, notas, lib), refs in grupos.items():
        valores = list(dict.fromkeys(v for _, v in refs))
        w.writerow([" ".join(r for r, _ in refs), len(refs), "/".join(valores), descripcion(lib, huella), huella,
                    "NPTH" if lib == "Mechanical:MountingHole" else "-" if lib == "Device:Battery_Cell" else "THT",
                    cara, notas])

# BOM_compra.csv: todo lo que hay que tener para armar una consola (modulos, bateria, capuchones, tornillos...)
CAMPOS = [("ref", "Referencia"), ("item", "Articulo"), ("por", "Cant. por consola"), ("comprar", "Cant. a comprar"),
          ("fab", "Fabricante"), ("mpn", "MPN"), ("prov", "Proveedor"), ("cod", "Codigo proveedor / link"),
          ("precio", "Precio unitario (CLP)"), ("estado", "Estado"), ("notas", "Notas")]
with open(os.path.join(CARPETA, "BOM_compra.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow([t for _, t in CAMPOS])
    for fila in COMPRA:
        w.writerow([fila[k] for k, _ in CAMPOS])
print(f"ok {os.path.join(CARPETA, 'BOM_compra.csv')} ({len(COMPRA)} filas)")

print(f"ok {os.path.join(CARPETA, 'BOM.csv')} ({len(grupos)} filas)")
print(f"ok {os.path.join(CARPETA, 'netlist.csv')} ({len(filas)} filas, "
      f"{len([r for r in redes if not r.startswith('unconnected-')])} redes con nombre)")
if errores:
    print("DIFERENCIAS ESQUEMATICO / ESPECIFICACION:")
    for e in errores:
        print("  - " + e)
    sys.exit(1)
print("Esquematico = especificacion (seccion 5): todas las redes coinciden.")
