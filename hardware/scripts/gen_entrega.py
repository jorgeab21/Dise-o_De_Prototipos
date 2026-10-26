# Arma la carpeta de entrega entrega/KIDBOX_PCB_v0.9/ y su zip entrega/KIDBOX_PCB_v0.9.zip con la MISMA estructura
# del repositorio, para que la tabla "Archivos" del README valga tal cual:
#   README.md, ESPECIFICACION.md, DECISIONES.md
#   KIDBOX/        proyecto KiCad (.kicad_pro, .kicad_sch, .kicad_pcb, .kicad_dru, fp-lib-table, KIDBOX.pretty/),
#                  BOM.csv, BOM_compra.csv, netlist.csv y verificacion/
#   fabricacion/   Gerbers, taladros, zip para JLCPCB y PDF 1:1 (A4 y Carta)
#   scripts/       todos los generadores y verificaciones (sin __pycache__)
# No incluye datasheets/, AGENTS.md, PROMPTS.md ni archivos locales de KiCad (.kicad_prl, respaldos, bloqueos).
# La carpeta entrega/ no se versiona (.gitignore): se regenera con este script.
#
# Uso (Python 3.8+ del sistema), desde la carpeta raiz, despues de gen_fabricacion.py:
#     python scripts/gen_entrega.py
import os
import shutil
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, ".."))
VERSION = "v0.9"
NOMBRE = f"KIDBOX_PCB_{VERSION}"
DESTINO = os.path.join(RAIZ, "entrega", NOMBRE)
ZIP = os.path.join(RAIZ, "entrega", NOMBRE + ".zip")
IGNORAR = shutil.ignore_patterns("__pycache__", "*.pyc", "*.kicad_prl", "*.lck", "*-backups", "fp-info-cache",
                                 "_autosave-*", ".history")

shutil.rmtree(DESTINO, ignore_errors=True)
os.makedirs(DESTINO)
for archivo in ("README.md", "ESPECIFICACION.md", "DECISIONES.md"):
    shutil.copy2(os.path.join(RAIZ, archivo), DESTINO)
for carpeta in ("KIDBOX", "fabricacion", "scripts"):
    shutil.copytree(os.path.join(RAIZ, carpeta), os.path.join(DESTINO, carpeta), ignore=IGNORAR)

# comprobaciones: lo que el README promete tiene que estar
esperados = ["README.md", "ESPECIFICACION.md", "DECISIONES.md", "KIDBOX/KIDBOX.kicad_pro", "KIDBOX/KIDBOX.kicad_sch",
             "KIDBOX/KIDBOX.kicad_pcb", "KIDBOX/KIDBOX.kicad_dru", "KIDBOX/fp-lib-table",
             "KIDBOX/KIDBOX.pretty/GY-PCM5102_1x06_P2.54mm.kicad_mod", "KIDBOX/BOM.csv", "KIDBOX/BOM_compra.csv",
             "KIDBOX/netlist.csv", f"fabricacion/KIDBOX_gerbers_{VERSION}_PRELIMINAR.zip",
             "fabricacion/KIDBOX_1a1_frente_A4.pdf", "fabricacion/KIDBOX_1a1_reverso_A4.pdf",
             "fabricacion/KIDBOX_1a1_frente_Carta.pdf", "fabricacion/KIDBOX_1a1_reverso_Carta.pdf",
             "scripts/gen_pcb.py", "scripts/verificar.py"]
faltan = [e for e in esperados if not os.path.exists(os.path.join(DESTINO, e))]
if faltan:
    raise SystemExit(f"faltan en la entrega: {faltan}")

if os.path.exists(ZIP):
    os.remove(ZIP)
n = 0
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for base, _, archivos in os.walk(DESTINO):
        for a in sorted(archivos):
            ruta = os.path.join(base, a)
            z.write(ruta, os.path.join(NOMBRE, os.path.relpath(ruta, DESTINO)))
            n += 1
print(f"ok {DESTINO} ({n} archivos)")
print(f"ok {ZIP} ({os.path.getsize(ZIP)} bytes)")
