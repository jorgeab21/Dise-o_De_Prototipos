# Dos comprobaciones que verificar.py no hace (no lo reemplaza: se corre despues de el):
#  1. ERC y DRC (con paridad) con TODOS los tests, incluidos los que el .kicad_pro deja en "ignore"
#     (footprint_filters_mismatch, footprint_type_mismatch, missing_courtyard, ...). Se hace sobre una copia
#     temporal del proyecto con esas reglas pasadas a "error"; el proyecto real no se toca.
#  2. "F8 en seco": compara cada huella del PCB con lo que le dejaria "Actualizar PCB desde esquematico"
#     (valor, huella, enlace, hoja y archivo de hoja, filtros, campos, atributos BOM / archivos de posicion / DNP,
#     y metadatos de unidad "(units (unit (name ..) (pins ..)))", leidos del archivo porque Python no los expone).
#     kicad-cli no tiene la actualizacion por linea de comandos, asi que se emula con la netlist que usa F8.
#  3. Esquinas de pista: une los segmentos de cada red y capa, mide el giro en cada vertice donde se juntan dos pistas y
#     falla si alguno es de 90 grados (v1.0: todas las esquinas a 45; los tramos colineales se permiten). Tambien
#     falla si una pista llega en T a 90 grados a otra de la misma red.
#
# Uso (Python de KiCad, trae pcbnew), desde hardware/:
#     "C:\Program Files\KiCad\10.0\bin\python.exe" scripts/verificar_extra.py KIDBOX
import glob
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

import pcbnew

CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
carpeta = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
pro = glob.glob(os.path.join(carpeta, "*.kicad_pro"))[0]
nombre = os.path.splitext(os.path.basename(pro))[0]
fallos = 0

# ---------------------------------------------------------------- 1. tests ignorados
tmp = tempfile.mkdtemp()
for ext in (".kicad_pro", ".kicad_sch", ".kicad_pcb", ".kicad_dru"):
    if os.path.exists(os.path.join(carpeta, nombre + ext)):
        shutil.copy(os.path.join(carpeta, nombre + ext), tmp)
# libreria propia del proyecto (v0.9): sin ella el DRC no encuentra la huella del DAC
if os.path.exists(os.path.join(carpeta, "fp-lib-table")):
    shutil.copy(os.path.join(carpeta, "fp-lib-table"), tmp)
for lib in glob.glob(os.path.join(carpeta, "*.pretty")):
    shutil.copytree(lib, os.path.join(tmp, os.path.basename(lib)))
ruta_pro = os.path.join(tmp, nombre + ".kicad_pro")
with open(ruta_pro, encoding="utf-8") as f:
    datos = json.load(f)
activados = []
for seccion in (datos["board"]["design_settings"]["rule_severities"], datos.get("erc", {}).get("rule_severities", {})):
    for k, v in seccion.items():
        if v == "ignore":
            seccion[k] = "error"
            activados.append(k)
with open(ruta_pro, "w", encoding="utf-8") as f:
    json.dump(datos, f, indent=2)
print("[1/3] Tests que el proyecto ignora, activados como error:", ", ".join(activados) or "(ninguno)")
erc = os.path.join(tmp, "erc.json")
subprocess.run([CLI, "sch", "erc", "--format", "json", "--severity-all", "-o", erc,
                os.path.join(tmp, nombre + ".kicad_sch")], check=True, capture_output=True)
with open(erc, encoding="utf-8") as f:
    v_erc = [v for s in json.load(f)["sheets"] for v in s["violations"]]
drc = os.path.join(tmp, "drc.json")
subprocess.run([CLI, "pcb", "drc", "--format", "json", "--severity-all", "--schematic-parity", "--refill-zones",
                "-o", drc, os.path.join(tmp, nombre + ".kicad_pcb")], check=True, capture_output=True)
with open(drc, encoding="utf-8") as f:
    d = json.load(f)
for titulo, lista in (("ERC", v_erc), ("DRC", d["violations"]), ("sin conectar", d["unconnected_items"]),
                      ("paridad", d["schematic_parity"])):
    print(f"  {titulo}: {len(lista)}")
    for v in lista[:15]:
        print(f"    - [{v['type']}] {v['description']} "
              + "; ".join(i["description"] for i in v.get("items", [])))
    fallos += len(lista)

# ---------------------------------------------------------------- 2. F8 en seco
net = os.path.join(tmp, "f8.net")
subprocess.run([CLI, "sch", "export", "netlist", "--format", "kicadsexpr", "-o", net,
                os.path.join(carpeta, nombre + ".kicad_sch")], check=True, capture_output=True)
with open(net, encoding="utf-8") as f:
    texto = f.read()


def bloque(t, i):
    n = 0
    for j in range(i, len(t)):
        n += {"(": 1, ")": -1}.get(t[j], 0)
        if n == 0:
            return t[i:j + 1]


def unidades(b, patron_pin):
    """[(nombre, [pines])] del bloque (units ...) de un componente de la netlist o de una huella del PCB."""
    m = re.search(r"\(units\s", b)
    if not m:
        return None
    u = bloque(b, m.start())
    out = []
    for x in re.finditer(r'\(unit\s*\(name "([^"]*)"\)', u):
        un = bloque(u, x.start())
        out.append((x.group(1), re.findall(patron_pin, bloque(un, un.index("(pins")))))
    return out


simbolos = {}
for m in re.finditer(r"\(comp\s", texto):
    b = bloque(texto, m.start())
    ref = re.search(r'\(ref "([^"]*)"\)', b).group(1)
    campos = dict(re.findall(r'\(field\s*\(name "([^"]*)"\)\s*(?:"((?:[^"\\]|\\.)*)")?', b))
    props = {k: v for k, v in re.findall(r'\(property\s*\(name "([^"]*)"\)\s*(?:\(value "((?:[^"\\]|\\.)*)"\))?', b)}
    if "exclude_from_board" in props:
        continue  # BT1: F8 no crea huella para un simbolo excluido de la placa
    simbolos[ref] = dict(
        valor=re.search(r'\(value "([^"]*)"\)', b).group(1),
        huella=re.search(r'\(footprint "([^"]*)"\)', b).group(1),
        path="/" + re.findall(r'\(tstamps "([^"]*)"\)', b)[-1],
        hoja=re.search(r'\(sheetpath\s*\(names "([^"]*)"\)', b).group(1),
        campos={k: v for k, v in campos.items() if k != "Footprint"}, props=props,
        unidades=unidades(b, r'\(pin\s*\(num "([^"]*)"\)'))

board = pcbnew.LoadBoard(os.path.join(carpeta, nombre + ".kicad_pcb"))
with open(os.path.join(carpeta, nombre + ".kicad_pcb"), encoding="utf-8") as f:
    texto_pcb = f.read()
unidades_pcb = {}
for m in re.finditer(r"\n\t\(footprint ", texto_pcb):
    b = bloque(texto_pcb, m.start() + 2)
    ref = re.search(r'\(property "Reference" "([^"]*)"', b).group(1)
    unidades_pcb[ref] = unidades(b, r'"([^"]*)"')  # en el PCB los pines van como (pins "1" "2")
cambios = []
huellas = {fp.GetReference(): fp for fp in board.GetFootprints()}
for ref in sorted(set(simbolos) | set(huellas)):
    s, fp = simbolos.get(ref), huellas.get(ref)
    if s is None or fp is None:
        cambios.append(f"{ref}: {'sobra en el PCB' if s is None else 'falta en el PCB'}")
        continue
    campos_fp = {f.GetName(): f.GetText() for f in fp.GetFields() if f.GetName() not in ("Reference", "Value")}
    comparar = [
        ("valor", fp.GetValue(), s["valor"]),
        ("huella", fp.GetFPIDAsString(), s["huella"]),
        ("enlace", fp.GetPath().AsString(), s["path"]),
        ("Sheetname", fp.GetSheetname(), s["hoja"]),
        ("Sheetfile", fp.GetSheetfile(), s["props"].get("Sheetfile", "")),
        ("filtros", fp.GetFilters(), s["props"].get("ki_fp_filters", "")),
        ("campos", campos_fp, s["campos"]),
        ("excluir de BOM", fp.IsExcludedFromBOM(), "exclude_from_bom" in s["props"]),
        ("excluir de archivos de posicion", fp.IsExcludedFromPosFiles(), "exclude_from_pos_files" in s["props"]),
        ("DNP", fp.IsDNP(), "dnp" in s["props"]),
        ("metadatos de unidad", unidades_pcb.get(ref), s["unidades"]),
    ]
    for que, en_pcb, en_sch in comparar:
        if en_pcb != en_sch:
            cambios.append(f"{ref}: {que}: PCB {en_pcb!r} -> esquematico {en_sch!r}")
print(f"[2/3] F8 en seco ({len(simbolos)} simbolos, {len(huellas)} huellas): {len(cambios)} cambios")
for c in cambios:
    print("    - " + c)
fallos += len(cambios)

# ---------------------------------------------------------------- 3. esquinas a 90 grados
salidas = {}  # (red, capa, punto) -> angulos de las pistas que salen de ese punto
for t in board.GetTracks():
    if t.GetClass() != "PCB_TRACK":
        continue
    a = (round(pcbnew.ToMM(t.GetStart().x), 3), round(pcbnew.ToMM(t.GetStart().y), 3))
    b = (round(pcbnew.ToMM(t.GetEnd().x), 3), round(pcbnew.ToMM(t.GetEnd().y), 3))
    for p, q in ((a, b), (b, a)):
        salidas.setdefault((t.GetNetname(), t.GetLayer(), p), []).append(math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])))
giros, rectas = {}, []
for (red, _, p), angs in salidas.items():
    pares = [(angs[i], angs[j]) for i in range(len(angs)) for j in range(i + 1, len(angs))]
    for u, v in pares:
        entre = abs(u - v) % 360
        giro = round(180 - min(entre, 360 - entre))  # 0 = colineal, 45 = chaflan, 90 = esquina recta
        if len(angs) == 2:
            giros[giro] = giros.get(giro, 0) + 1
        if giro == 90:
            rectas.append(f"{red} en {p}" + ("" if len(angs) == 2 else " (union en T)"))
print(f"[3/3] Esquinas de pista: {sum(giros.values())} vertices; por giro en grados {dict(sorted(giros.items()))}; "
      f"a 90 grados: {len(rectas)}")
for r in rectas:
    print("    - " + r)
fallos += len(rectas)
shutil.rmtree(tmp, ignore_errors=True)
print("RESULTADO EXTRA:", "SIN ERRORES" if fallos == 0 else f"{fallos} problemas")
sys.exit(1 if fallos else 0)
