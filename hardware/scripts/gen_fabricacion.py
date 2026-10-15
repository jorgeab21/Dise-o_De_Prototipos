# Fase 4: genera el paquete de fabricacion para JLCPCB (2 capas) en hardware/fabricacion/ SIN tocar el .kicad_pcb:
#   - Gerbers (kicad-cli, extensiones Protel, X2): F.Cu, B.Cu, F.Mask, B.Mask, F.SilkS, B.SilkS, Edge.Cuts
#   - Taladros Excellon en mm, origen absoluto, PTH y NPTH en archivos separados, mapa PDF y reporte
#   - PDF a escala 1:1 (frente, y reverso espejado) para la prueba de impresion con las piezas reales
#   - fabricacion/KIDBOX_gerbers_PRELIMINAR.zip con todo lo anterior (sin los PDF) y la lista de su contenido
# Comprueba al final que el .kicad_pcb sigue igual (md5) y que hay un archivo por capa.
#
# Uso (Python 3.8+ del sistema), desde hardware/:
#     python scripts/gen_fabricacion.py
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, ".."))
PCB = os.path.join(RAIZ, "KIDBOX", "KIDBOX.kicad_pcb")
SALIDA = os.path.join(RAIZ, "fabricacion")
GERBERS = os.path.join(SALIDA, "gerbers")
ZIP = os.path.join(SALIDA, "KIDBOX_gerbers_PRELIMINAR.zip")
CLI = next(c for c in (os.environ.get("KICAD_CLI"), r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe",
                       shutil.which("kicad-cli")) if c and os.path.exists(c))
CAPAS = ["F.Cu", "B.Cu", "F.Mask", "B.Mask", "F.SilkS", "B.SilkS", "Edge.Cuts"]
EXT = {"F.Cu": ".gtl", "B.Cu": ".gbl", "F.Mask": ".gts", "B.Mask": ".gbs", "F.SilkS": ".gto", "B.SilkS": ".gbo",
       "Edge.Cuts": ".gm1"}


def md5(ruta):
    with open(ruta, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def cli(*args):
    r = subprocess.run([CLI, *args], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"kicad-cli fallo: {' '.join(args)}\n{r.stdout}\n{r.stderr}")
    return r.stdout


antes = md5(PCB)
shutil.rmtree(GERBERS, ignore_errors=True)
os.makedirs(GERBERS)
cli("pcb", "export", "gerbers", "-o", GERBERS + os.sep, "--layers", ",".join(CAPAS), "--check-zones", PCB)
cli("pcb", "export", "drill", "-o", GERBERS + os.sep, "--format", "excellon", "--drill-origin", "absolute",
    "--excellon-units", "mm", "--excellon-zeros-format", "decimal", "--excellon-separate-th",
    "--generate-map", "--map-format", "pdf", "--generate-report",
    "--report-path", os.path.join(GERBERS, "KIDBOX-drill_report.txt"), PCB)

# PDF 1:1 para imprimir y apoyar las piezas reales encima (reverso espejado = como se ve la placa desde atras).
# Fuera del zip: no son para el fabricante. Con escala exactamente 1 KiCad deja la placa en su posicion absoluta,
# pegada a la esquina de la hoja (la impresora recorta ~4 mm y el reverso espejado se sale de la hoja); con 1.0001
# la centra. El error es 0.015 mm en 150 mm, muy por debajo de la precision de una impresora.
for nombre_pdf, capas, extra in (("KIDBOX_1a1_frente.pdf", "F.Cu,F.SilkS,Edge.Cuts", []),
                                 ("KIDBOX_1a1_reverso.pdf", "B.SilkS,Edge.Cuts", ["--mirror"])):
    cli("pcb", "export", "pdf", "--mode-single", "-o", os.path.join(SALIDA, nombre_pdf), "--layers", capas,
        "--scale", "1.0001", "--black-and-white", "--drill-shape-opt", "2", *extra, PCB)

archivos = sorted(os.listdir(GERBERS))
faltan = [c for c in CAPAS if not any(a.endswith(EXT[c]) for a in archivos)]
faltan += [t for t in ("-PTH.drl", "-NPTH.drl") if not any(a.endswith(t) for a in archivos)]
if faltan:
    sys.exit(f"faltan archivos: {faltan}")

# Al zip van Gerbers + Excellon (+ el .gbrjob, que JLCPCB ignora); los mapas PDF y el reporte quedan fuera
if os.path.exists(ZIP):
    os.remove(ZIP)
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for a in archivos:
        if not a.endswith((".pdf", ".txt")):
            z.write(os.path.join(GERBERS, a), a)

if md5(PCB) != antes:
    sys.exit("ERROR: el .kicad_pcb cambio durante la exportacion")
print(f"ok {ZIP} ({os.path.getsize(ZIP)} bytes); .kicad_pcb sin cambios (md5 {antes})")
print(f"{'Archivo':40} {'Bytes':>9}  (dentro del zip)")
with zipfile.ZipFile(ZIP) as z:
    for i in z.infolist():
        print(f"{i.filename:40} {i.file_size:>9}")
print("Fuera del zip, en fabricacion/gerbers/:", ", ".join(a for a in archivos if a.endswith((".pdf", ".txt"))))
