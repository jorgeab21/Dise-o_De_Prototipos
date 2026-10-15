# Crea KIDBOX/KIDBOX.kicad_pcb solo con el contorno (Edge.Cuts) de 150 x 65 mm y esquinas de radio 4 mm,
# y escribe en KIDBOX/KIDBOX.kicad_pro las reglas DFM de ESPECIFICACION.md seccion 7 (minimos y net class Default)
# mas la net class "Potencia" (pista de 0.5 mm) para +3V3 (seccion 8).
# Origen de la especificacion (esquina superior izquierda = (0,0), Y hacia abajo) = origen absoluto de KiCad.
# Es el PCB minimo de la Fase 1 para que verificar.py pueda correr; la Fase 2 lo reemplaza.
# Se niega a sobrescribir un PCB que ya tenga huellas o pistas (usa --forzar si de verdad quieres).
#
# Uso (Python de KiCad, trae el modulo pcbnew), desde hardware/:
#     "C:\Program Files\KiCad\10.0\bin\python.exe" scripts/gen_pcb_vacio.py
import json
import math
import os
import sys

import pcbnew

PROYECTO = "KIDBOX"
CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", PROYECTO)
PCB = os.path.normpath(os.path.join(CARPETA, PROYECTO + ".kicad_pcb"))
PRO = os.path.normpath(os.path.join(CARPETA, PROYECTO + ".kicad_pro"))
ANCHO, ALTO, RADIO = 150.0, 65.0, 4.0

# ESPECIFICACION.md seccion 7 ("Mi valor")
REGLAS = {
    "min_clearance": 0.20,
    "min_connection": 0.20,  # ancho minimo de conexion (rayos de alivio termico y cobre de zonas)
    "min_track_width": 0.25,
    "min_via_diameter": 0.60,
    "min_through_hole_diameter": 0.30,
    "min_via_annular_width": 0.15,
    "min_copper_edge_clearance": 0.30,
    "min_hole_to_hole": 0.25,
    "min_hole_clearance": 0.25,
    "min_text_thickness": 0.15,
    "min_text_height": 1.0,
}
NETCLASS_DEFAULT = {"clearance": 0.20, "track_width": 0.25, "via_diameter": 0.60, "via_drill": 0.30}
NETCLASS_POTENCIA = {"name": "Potencia", "clearance": 0.20, "track_width": 0.50, "via_diameter": 0.60,
                     "via_drill": 0.30}


def mm(x, y):
    return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))


def contorno(board):
    W, H, R = ANCHO, ALTO, RADIO
    rectas = [((R, 0), (W - R, 0)), ((W, R), (W, H - R)), ((W - R, H), (R, H)), ((0, H - R), (0, R))]
    k = R * (1 - math.cos(math.radians(45)))
    arcos = [((0, R), (k, k), (R, 0)), ((W - R, 0), (W - k, k), (W, R)),
             ((W, H - R), (W - k, H - k), (W - R, H)), ((R, H), (k, H - k), (0, H - R))]
    for a, b in rectas:
        s = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(mm(*a))
        s.SetEnd(mm(*b))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(pcbnew.FromMM(0.1))
        board.Add(s)
    for a, m, b in arcos:
        s = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_ARC)
        s.SetArcGeometry(mm(*a), mm(*m), mm(*b))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(pcbnew.FromMM(0.1))
        board.Add(s)


def escribir_reglas():
    """Escribe las reglas DFM y las net classes en el .kicad_pro (lo usa tambien gen_pcb.py)."""
    # Reglas en el .kicad_pro (se edita el JSON que deja KiCad para conservar el resto de su estructura)
    with open(PRO, encoding="utf-8") as f:
        pro = json.load(f)
    pro.setdefault("board", {}).setdefault("design_settings", {}).setdefault("rules", {}).update(REGLAS)
    ns = pro.setdefault("net_settings", {})
    clases = ns.setdefault("classes", [])
    default = next((c for c in clases if c.get("name") == "Default"), None)
    if default is None:
        default = {"name": "Default"}
        clases.insert(0, default)
    default.update(NETCLASS_DEFAULT)
    pot = next((c for c in clases if c.get("name") == "Potencia"), None)
    if pot is None:
        pot = dict(default, priority=0)
        clases.append(pot)
    pot.update(NETCLASS_POTENCIA)
    ns["netclass_patterns"] = [{"netclass": "Potencia", "pattern": "+3V3"}]
    with open(PRO, "w", encoding="utf-8", newline="\n") as f:
        json.dump(pro, f, indent=2, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    if os.path.exists(PCB) and "--forzar" not in sys.argv:
        viejo = pcbnew.LoadBoard(PCB)
        if len(viejo.GetFootprints()) or len(viejo.GetTracks()):
            sys.exit(f"{PCB} ya tiene huellas o pistas; no lo sobrescribo (usa --forzar).")

    os.makedirs(CARPETA, exist_ok=True)
    board = pcbnew.NewBoard(PCB)
    board.SetCopperLayerCount(2)
    board.GetDesignSettings().SetBoardThickness(pcbnew.FromMM(1.6))
    tb = board.GetTitleBlock()
    tb.SetTitle("KIDBOX")
    tb.SetRevision("v1.0")
    tb.SetDate("2026-10-13")
    tb.SetCompany("Equipo KIDBOX")
    contorno(board)
    pcbnew.SaveBoard(PCB, board)
    escribir_reglas()
    print("ok", PCB)
    print("ok", PRO)
