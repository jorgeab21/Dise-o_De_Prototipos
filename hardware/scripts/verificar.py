#!/usr/bin/env python3
"""Verificacion unica de un proyecto KiCad por terminal (sin abrir la GUI).

Uso:   python scripts/verificar.py [carpeta_del_proyecto]      (por defecto: carpeta actual)

Hace, en orden:
  1. ERC del esquematico.
  2. DRC del PCB con paridad esquematico-PCB. Rellena las zonas y GUARDA el .kicad_pcb
     (cierra KiCad antes de ejecutarlo, si no la GUI se queda con una copia vieja).
  3. Comprueba que los minimos DFM del .kicad_pro no esten en 0 (un DRC con minimos en 0 no verifica nada).
  4. Estadisticas de la placa (pistas, vias, agujeros).
  5. Imagenes para revisar: verificacion/esquematico.svg, F_Cu.svg, B_Cu.svg, 3d_top.png, 3d_bottom.png.

Sale con codigo 1 si hay errores o pads sin conectar. Los avisos se listan pero no bloquean.
Requiere Python 3.8+ sin dependencias. Ruta de kicad-cli: variable de entorno KICAD_CLI o rutas por defecto.
"""
import glob
import json
import os
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):  # consola Windows con cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CANDIDATOS = [
    os.environ.get("KICAD_CLI"),
    r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe",
    r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe",
    "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli",
    shutil.which("kicad-cli"),
]
CLI = next((c for c in CANDIDATOS if c and os.path.exists(c)), None)
if not CLI:
    sys.exit("No encuentro kicad-cli. Define la variable de entorno KICAD_CLI con la ruta completa al ejecutable.")

# Minimos que el DRC solo comprueba si son > 0. Valores de referencia: JLCPCB 2 capas, soldadura manual.
MINIMOS_DFM = {
    "min_clearance": 0.2,
    "min_track_width": 0.2,
    "min_via_diameter": 0.6,
    "min_via_annular_width": 0.15,
    "min_through_hole_diameter": 0.3,
    "min_copper_edge_clearance": 0.3,
    "min_hole_to_hole": 0.25,
}

if any(a in ("-h", "--help") for a in sys.argv[1:]):
    print(__doc__)
    sys.exit(0)

carpeta = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")


def unico(ext):
    archivos = glob.glob(os.path.join(carpeta, "*" + ext))
    if len(archivos) != 1:
        sys.exit(f"Esperaba exactamente un archivo {ext} en {carpeta} y hay {len(archivos)}.")
    return archivos[0]


sch, pcb, pro = unico(".kicad_sch"), unico(".kicad_pcb"), unico(".kicad_pro")
salida = os.path.join(carpeta, "verificacion")
os.makedirs(salida, exist_ok=True)
errores = []


def cli(*args):
    r = subprocess.run([CLI, *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        errores.append(f"kicad-cli fallo ({' '.join(args[:3])}): {(r.stdout + r.stderr).strip()[-800:]}")
    return r


def leer_json(ruta):
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def mostrar(titulo, items, maximo=15):
    print(f"  {titulo}: {len(items)}")
    for v in items[:maximo]:
        items = v.get("items") or [{}]
        pos = items[0].get("pos", {})
        donde = f" @({pos.get('x')}, {pos.get('y')}) mm" if pos else ""
        detalle = "; ".join(i.get("description", "") for i in items if i.get("description"))
        print(f"    - [{v.get('type')}] {v.get('description')}{donde}" + (f" ({detalle})" if detalle else ""))
    if len(items) > maximo:
        print(f"    ... y {len(items) - maximo} mas (ver JSON en verificacion/)")


# 1. ERC ---------------------------------------------------------------------------
print(f"== kicad-cli: {CLI}\n== Proyecto: {carpeta}\n\n[1/5] ERC {os.path.basename(sch)}")
erc_json = os.path.join(salida, "erc.json")
cli("sch", "erc", "--format", "json", "--severity-all", "-o", erc_json, sch)
erc = leer_json(erc_json)
if erc:
    viol = [v for s in erc.get("sheets", []) for v in s.get("violations", [])]
    err = [v for v in viol if v.get("severity") == "error"]
    mostrar("errores", err)
    mostrar("avisos", [v for v in viol if v.get("severity") != "error"])
    if err:
        errores.append(f"ERC: {len(err)} errores")

# 2. DRC + paridad + relleno de zonas ------------------------------------------------
print(f"\n[2/5] DRC {os.path.basename(pcb)} (rellena zonas y guarda el PCB)")
drc_json = os.path.join(salida, "drc.json")
cli("pcb", "drc", "--format", "json", "--severity-all", "--schematic-parity",
    "--refill-zones", "--save-board", "-o", drc_json, pcb)
drc = leer_json(drc_json)
if drc:
    viol = drc.get("violations", [])
    err = [v for v in viol if v.get("severity") == "error"]
    sin_conectar = drc.get("unconnected_items", [])
    paridad = drc.get("schematic_parity", [])
    mostrar("errores DRC", err)
    mostrar("avisos DRC", [v for v in viol if v.get("severity") != "error"])
    mostrar("sin conectar", sin_conectar)
    mostrar("paridad esquematico-PCB", paridad)
    if err:
        errores.append(f"DRC: {len(err)} errores")
    if sin_conectar:
        errores.append(f"DRC: {len(sin_conectar)} elementos sin conectar")
    if any(p.get("severity") == "error" for p in paridad):
        errores.append("DRC: errores de paridad esquematico-PCB")

# 3. Minimos DFM en el .kicad_pro ----------------------------------------------------
print(f"\n[3/5] Minimos DFM en {os.path.basename(pro)}")
proj = leer_json(pro) or {}
reglas = proj.get("board", {}).get("design_settings", {}).get("rules", {})
for clave, referencia in MINIMOS_DFM.items():
    valor = reglas.get(clave)
    estado = "OK" if isinstance(valor, (int, float)) and valor > 0 else "SIN DEFINIR (el DRC no comprueba este limite)"
    print(f"  {clave:28} = {valor!s:6}  ref. JLCPCB >= {referencia}  {estado}")
    if estado != "OK":
        errores.append(f"DFM: {clave} no definido en .kicad_pro")
clases = proj.get("net_settings", {}).get("classes", [])
if clases:
    c = clases[0]
    print(f"  net class '{c.get('name')}': clearance={c.get('clearance')} track={c.get('track_width')} "
          f"via={c.get('via_diameter')}/{c.get('via_drill')}")

# 4. Estadisticas -------------------------------------------------------------------
print("\n[4/5] Estadisticas")
stats_txt = os.path.join(salida, "stats.txt")
cli("pcb", "export", "stats", "-o", stats_txt, pcb)
if os.path.exists(stats_txt):
    with open(stats_txt, encoding="utf-8", errors="replace") as f:
        for linea in f:
            if any(k in linea.lower() for k in ("width", "height", "ancho", "alto", "via", "track", "pista",
                                                "clearance", "drill", "taladro", "pad", "front", "back")):
                print("  " + linea.rstrip())

# 5. Imagenes -----------------------------------------------------------------------
print("\n[5/5] Imagenes en verificacion/")
cli("pcb", "export", "svg", "--mode-single", "--page-size-mode", "2", "--exclude-drawing-sheet",
    "--layers", "F.Cu,F.SilkS,Edge.Cuts", "-o", os.path.join(salida, "F_Cu.svg"), pcb)
cli("pcb", "export", "svg", "--mode-single", "--page-size-mode", "2", "--exclude-drawing-sheet", "--mirror",
    "--layers", "B.Cu,B.SilkS,Edge.Cuts", "-o", os.path.join(salida, "B_Cu.svg"), pcb)
cli("sch", "export", "svg", "--exclude-drawing-sheet", "-o", salida, sch)
for f in glob.glob(os.path.join(salida, "*.svg")):  # kicad-cli nombra el svg como el esquematico
    if os.path.basename(f) == os.path.basename(sch).replace(".kicad_sch", ".svg"):
        os.replace(f, os.path.join(salida, "esquematico.svg"))
cli("pcb", "render", "--side", "top", "-o", os.path.join(salida, "3d_top.png"), pcb)
cli("pcb", "render", "--side", "bottom", "-o", os.path.join(salida, "3d_bottom.png"), pcb)
for nombre in ("esquematico.svg", "F_Cu.svg", "B_Cu.svg", "3d_top.png", "3d_bottom.png"):
    print(f"  {'OK ' if os.path.exists(os.path.join(salida, nombre)) else 'NO '} {nombre}")

# Resultado -------------------------------------------------------------------------
print("\n" + "=" * 70)
if errores:
    print("RESULTADO: CON ERRORES")
    for e in errores:
        print("  - " + e)
    sys.exit(1)
print("RESULTADO: SIN ERRORES (revisa igualmente los avisos y las imagenes)")
