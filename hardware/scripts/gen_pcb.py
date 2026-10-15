# Genera KIDBOX/KIDBOX.kicad_pcb completo (Fase 2) segun ESPECIFICACION.md v0.7, secciones 6 a 9:
# contorno 150 x 65 mm (r = 4 mm), agujeros, huellas oficiales en sus posiciones (las fijas con "locked"),
# pistas en F.Cu, plano de GND en B.Cu con alivios termicos, serigrafia, y reglas DFM en el .kicad_pro.
# Fase 3: sin H5/H6 (ni KIDBOX.kicad_dru); SW5/SW6 en x = 66.5 / 83.5; DAC horizontal (J5 en columna en x = 59,
# VIN abajo, jack al borde inferior) con I2S, 3V3, C3 y C4 re-ruteados; huellas con hoja, archivo y filtros del
# simbolo para que "Actualizar PCB desde esquematico" (F8) no tenga nada que cambiar.
# Las huellas, sus redes y su enlace con el esquematico (path = uuid del simbolo) salen de la netlist real
# que exporta kicad-cli, asi que la paridad esquematico-PCB queda en 0. Las pistas son una lista fija de
# polilineas (ruteo manual planificado, sin autorouter); ver DECISIONES.md seccion 6.
# Los UUID del archivo se reescriben de forma determinista: re-ejecutarlo da el mismo .kicad_pcb.
#
# Uso (Python de KiCad, trae pcbnew), desde hardware/, con KiCad CERRADO:
#     "C:\Program Files\KiCad\10.0\bin\python.exe" scripts/gen_pcb.py
# Despues: python scripts/verificar.py KIDBOX
import math
import os
import re
import subprocess
import sys
import tempfile
import uuid
import xml.etree.ElementTree as ET

import pcbnew

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from gen_pcb_vacio import ANCHO, ALTO, CARPETA, PCB, PROYECTO, contorno, escribir_reglas  # noqa: E402

CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
FP_DIR = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"
SCH = os.path.join(CARPETA, PROYECTO + ".kicad_sch")
NS = uuid.UUID("6b1d0c52-6a1e-4f43-9a8e-4b49d0f2a002")

SENAL, POTENCIA, SILK, TXT = 0.25, 0.50, 0.15, 1.0
BATERIA = (88.0, 4.0, 123.5, 62.0)  # zona de bateria (Bottom): sin componentes ni patas THT


def mm(x, y):
    return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))


def xy(v):
    return pcbnew.ToMM(v.x), pcbnew.ToMM(v.y)


# ---------------------------------------------------------------- netlist real del esquematico
tmp = os.path.join(tempfile.mkdtemp(), "kidbox.xml")
subprocess.run([CLI, "sch", "export", "netlist", "--format", "kicadxml", "-o", tmp, SCH], check=True,
               capture_output=True)
raiz = ET.parse(tmp).getroot()
COMP = {}
for c in raiz.find("components"):
    campos = {f.get("name"): (f.text or "") for f in c.iter("field")}
    COMP[c.get("ref")] = dict(valor=c.findtext("value"), huella=c.findtext("footprint"),
                              desc=campos.get("Description", c.findtext("description") or ""),
                              datasheet=campos.get("Datasheet", ""),
                              path="/" + c.findtext("tstamps").strip(),
                              hoja=c.find("sheetpath").get("names"),
                              props={p.get("name"): p.get("value") or "" for p in c.iter("property")},
                              campos=campos,
                              unidades=[(u.get("name"), [x.get("num") for x in u.iter("pin")])
                                        for u in c.iter("unit")])
NODO = {}  # (ref, pad) -> nombre de red exacto
for n in raiz.iter("net"):
    for x in n.iter("node"):
        NODO[(x.get("ref"), x.get("pin"))] = n.get("name")
REDES = sorted(set(NODO.values()))

# ---------------------------------------------------------------- tablero
board = pcbnew.NewBoard(PCB)
board.SetCopperLayerCount(2)
ds = board.GetDesignSettings()
ds.SetBoardThickness(pcbnew.FromMM(1.6))
ds.m_TentViasFront = True  # seccion 7: vias tapadas (no hay vias en este ruteo, pero queda configurado)
ds.m_TentViasBack = True
tb = board.GetTitleBlock()
tb.SetTitle("KIDBOX")
tb.SetRevision("v1.0")
tb.SetDate("2026-10-14")
tb.SetCompany("Equipo KIDBOX")
tb.SetComment(0, "Basado en Game*Mite v1.3.2 de Thomas Hugo Williams (CC BY 4.0)")
tb.SetComment(1, "ESPECIFICACION.md v0.7 - Fase 2")
contorno(board)

NET = {}
for nombre in REDES:
    ni = pcbnew.NETINFO_ITEM(board, nombre)
    board.Add(ni)
    NET[nombre] = ni


def red(nombre):
    """Red por su nombre funcional (las etiquetas locales llegan como '/NOMBRE')."""
    return NET.get(nombre) or NET["/" + nombre]


# ---------------------------------------------------------------- huellas
def cargar(ref):
    lib, nombre = COMP[ref]["huella"].split(":")
    fp = pcbnew.FootprintLoad(os.path.join(FP_DIR, lib + ".pretty"), nombre)
    if fp is None:
        sys.exit(f"no encuentro la huella {COMP[ref]['huella']}")
    return fp


def pads(fp):
    return [(p.GetNumber(), xy(p.GetPosition())) for p in fp.Pads()]


def enlazar(fp, ref):
    """Deja la huella como la dejaria F8 (Actualizar PCB desde esquematico): referencia, valor, huella, enlace al
    simbolo, hoja y archivo de hoja, filtros de huella, mismos campos que el simbolo (se quitan los que trae la
    libreria y el simbolo no tiene, p. ej. KiLib_Generator) y atributos BOM / archivos de posicion."""
    c = COMP[ref]
    fp.SetReference(ref)
    fp.SetValue(c["valor"])
    fp.SetFPIDAsString(c["huella"])
    fp.SetPath(pcbnew.KIID_PATH(c["path"]))
    fp.SetSheetname(c["hoja"])
    fp.SetSheetfile(c["props"].get("Sheetfile", ""))
    fp.SetFilters(c["props"].get("ki_fp_filters", ""))
    for f in list(fp.GetFields()):
        nombre = f.GetName()
        if nombre in ("Reference", "Value"):
            continue
        if nombre in c["campos"] and nombre != "Footprint":
            f.SetText(c["campos"][nombre])
        elif not f.IsMandatory():
            fp.Remove(f)
    if "exclude_from_bom" in c["props"]:
        fp.SetExcludedFromBOM(True)
    fp.SetExcludedFromPosFiles("exclude_from_pos_files" in c["props"])


def colocar(ref, quiero, abajo=False, fija=True):
    """Coloca la huella para que sus pads queden donde dice `quiero` = {numero: [(x, y), ...]} (coordenadas
    de la especificacion, vistas desde el frente). Prueba los 4 giros y falla si ninguno encaja."""
    fp = cargar(ref)
    enlazar(fp, ref)
    board.Add(fp)
    if abajo:
        fp.Flip(fp.GetPosition(), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
    num0, (pos0,) = next((n, v[:1]) for n, v in quiero.items())
    for ang in (0, 90, 180, 270):
        fp.SetOrientationDegrees(ang)
        actual = [p for n, p in pads(fp) if n == num0]
        ax, ay = actual[0]
        # se prueba cada pad con ese numero como ancla (los pulsadores tienen dos pads "1")
        for ax, ay in actual:
            fp.Move(mm(pos0[0] - ax, pos0[1] - ay))
            ok = all(any(math.dist(q, p) < 0.01 for nn, p in pads(fp) if nn == n)
                     for n, lista in quiero.items() for q in lista)
            if ok:
                break
            fp.Move(mm(ax - pos0[0], ay - pos0[1]))
        if ok:
            break
    else:
        sys.exit(f"{ref}: ningun giro deja los pads en {quiero}")
    for p in fp.Pads():
        if p.GetNumber():
            p.SetNet(NET[NODO[(ref, p.GetNumber())]])
    fp.SetLocked(fija)
    fp.Reference().SetTextSize(mm(TXT, TXT))
    fp.Reference().SetTextThickness(pcbnew.FromMM(SILK))
    return fp


def ref_en(fp, x, y, ang=0, visible=True):
    r = fp.Reference()
    r.SetVisible(visible)
    r.SetTextAngleDegrees(ang)
    r.SetPosition(mm(x, y))


def columna(x, y0, n, paso=2.54):
    return {str(i + 1): [(x, round(y0 + i * paso, 4))] for i in range(n)}


# RP2350-Plus por detras: USB-C en y = 0, modulo y 0-51.55 (centro 25.8). Pin 1 a 1.37 mm del borde de su
# placa (que empieza en y = 0.55 porque el USB-C sobresale 0.55 mm) -> pin 1 en y = 1.92; filas a 17.78 mm.
Y_PIN1 = 1.92
J1 = colocar("J1", columna(83.89, Y_PIN1, 20), abajo=True)          # pines 1-20, arriba -> abajo
J2 = colocar("J2", columna(66.11, Y_PIN1 + 19 * 2.54, 20, -2.54), abajo=True)  # pin 21 abajo -> 40 arriba
J3 = colocar("J3", columna(38.41, 28 - 6.5 * 2.54, 14))             # pin 1 (VCC) arriba
# J5 (DAC horizontal, por detras): columna vertical junto a J2, VIN (pin 1) abajo en y = 59.8 y SCK (pin 6) arriba
# en y = 47.1. En x = 59 (1 mm hacia la cruceta respecto de x = 60 de la especificacion): en x = 60 la pista de
# DOWN, que pasa por encima de J5, quedaba a 0.07 mm de la esquina del pin 6 (ver DECISIONES.md seccion 8).
X_J5 = 59.0
J5 = colocar("J5", {str(i + 1): [(X_J5, round(59.8 - i * 2.54, 4))] for i in range(6)}, abajo=True)


def boton(ref, cx, cy, pad1_abajo):
    """Pulsador 6x6: patas a 6.5 (x) por 4.5 (y) del centro del cuerpo; pad1_abajo elige la fila del pin 1."""
    y1, y2 = (cy + 2.25, cy - 2.25) if pad1_abajo else (cy - 2.25, cy + 2.25)
    return colocar(ref, {"1": [(cx - 3.25, y1), (cx + 3.25, y1)], "2": [(cx - 3.25, y2), (cx + 3.25, y2)]})


SW = {"SW3": boton("SW3", 18, 20, True), "SW1": boton("SW1", 18, 40, True), "SW2": boton("SW2", 8, 30, True),
      "SW4": boton("SW4", 28, 30, True), "SW8": boton("SW8", 138, 25, True), "SW7": boton("SW7", 128, 35, True),
      "SW5": boton("SW5", 66.5, 58, False), "SW6": boton("SW6", 83.5, 58, False)}
# SW10 por detras, centro del cuerpo (134, 8) = pad 1 (central, comun). Pad 2 (GND) queda a la derecha.
SW10 = colocar("SW10", {"1": [(134, 8)], "2": [(136.54, 8)], "3": [(131.46, 8)]}, abajo=True)
C2 = colocar("C2", {"1": [(34.6, 11.49)], "2": [(34.6, 13.99)]}, fija=False)
# C3 y C4 junto a VIN pero fuera del contorno del DAC (x 28.65-60.5, y 44.2-62): C3 bajo el modulo, en la franja
# y 62-65 junto al borde; C4 (D5 mm, mas alto que la separacion bajo el modulo) no cabe mas cerca: entre J5 y SELECT
# hay 2.4 mm, bajo el modulo no puede ir, y entre las patas de SW5 sus pads caen dentro del courtyard de SW5
# (error pth_inside_courtyard). Va entre SELECT y START, alimentado desde C3 por la franja inferior.
C3 = colocar("C3", {"1": [(60.6, 63.3)], "2": [(58.1, 63.3)]}, abajo=True, fija=False)
C4 = colocar("C4", {"1": [(74.0, 59.0)], "2": [(76.0, 59.0)]}, abajo=True, fija=False)
H = {}
for ref, (x, y) in {"H1": (4, 4), "H2": (146, 4), "H3": (4, 61), "H4": (146, 61)}.items():
    fp = cargar(ref)
    enlazar(fp, ref)
    board.Add(fp)
    fp.SetPosition(mm(x, y))
    fp.Reference().SetVisible(False)  # un agujero no necesita referencia en la serigrafia
    fp.SetLocked(True)
    H[ref] = fp

# ---------------------------------------------------------------- pistas (F.Cu salvo que se indique)
PISTAS = [
    # SPI y control de la pantalla: de J1 (columna derecha del modulo) cruzan entre los pines de J2
    # (huecos y 13.35-23.51) y llegan a J3 en paralelo, a 2.54 mm. Mismo orden arriba-abajo en ambos extremos.
    ("LCD_CS", SENAL, [(83.89, 1.92), (79.58, 1.92), (68.15, 13.35), (45.5, 13.35), (42.28, 16.57), (38.41, 16.57)]),
    ("LCD_RST", SENAL, [(83.89, 4.46), (79.54, 4.46), (68.11, 15.89), (45.5, 15.89), (42.28, 19.11), (38.41, 19.11)]),
    ("LCD_DC", SENAL, [(83.89, 9.54), (76.96, 9.54), (68.07, 18.43), (45.5, 18.43), (42.28, 21.65), (38.41, 21.65)]),
    ("LCD_MOSI", SENAL, [(83.89, 12.08), (76.92, 12.08), (68.03, 20.97), (45.5, 20.97), (42.28, 24.19),
                         (38.41, 24.19)]),
    ("LCD_SCK", SENAL, [(83.89, 22.24), (69.26, 22.24), (67.99, 23.51), (45.5, 23.51), (42.28, 26.73),
                        (38.41, 26.73)]),
    ("LCD_LED", SENAL, [(66.11, 24.78), (47.0, 24.78), (42.51, 29.27), (38.41, 29.27)]),
    # I2S al DAC (J5 en columna, de arriba abajo SCK, BCK, DIN, LCK, GND, VIN). El haz de la cruceta sale de J2
    # hacia la izquierda por encima de J5, asi que el I2S sale de J2 hacia la DERECHA, baja por dentro del modulo
    # (entre J2 y SELECT), pasa bajo J2.1 y llega a J5 por la derecha. LCK cruza entre los pines 5 y 4 de J5 y entra
    # al pin 3 por la izquierda: es el unico orden sin cruces ni vias.
    ("I2S_BCK", SENAL, [(66.11, 37.48), (67.5, 37.48), (67.5, 51.4), (61.2, 51.4), (61.2, 49.64), (X_J5, 49.64)]),
    ("I2S_LRCK", SENAL, [(66.11, 34.94), (68.1, 34.94), (68.1, 51.95), (60.4, 51.95), (60.4, 50.91), (57.7, 50.91),
                         (57.7, 54.72), (X_J5, 54.72)]),
    ("I2S_DIN", SENAL, [(66.11, 29.86), (68.7, 29.86), (68.7, 52.6), (59.42, 52.6), (X_J5, 52.18)]),
    # 3V3: J2.16 -> J3.1 -> C2 -> por la izquierda de J3, entre sus pines 9 y 10 (sin uso), -> entra al modulo
    # entre J2.10 (RUN, sin uso) y J2.9 -> baja por fuera del I2S -> J5.1 (VIN) -> C3 -> bajo SW5 -> C4+.
    # Los huecos de 0.84 mm entre pines (J3 y J2) obligan a 0.40 mm en esos dos tramos.
    ("+3V3", POTENCIA, [(66.11, 12.08), (39.0, 12.08), (38.41, 11.49)]),
    ("+3V3", POTENCIA, [(38.41, 11.49), (34.6, 11.49)]),
    ("+3V3", POTENCIA, [(36.2, 11.49), (36.2, 33.08)]),
    ("+3V3", 0.40, [(36.2, 33.08), (40.2, 33.08)]),
    ("+3V3", POTENCIA, [(40.2, 33.08), (57.7, 33.08), (62.19, 28.59), (64.0, 28.59)]),
    ("+3V3", 0.40, [(64.0, 28.59), (68.0, 28.59)]),
    ("+3V3", POTENCIA, [(68.0, 28.59), (69.5, 28.59), (69.5, 53.4), (60.6, 53.4), (60.6, 63.3)]),
    ("+3V3", POTENCIA, [(60.6, 59.8), (X_J5, 59.8)]),
    ("+3V3", POTENCIA, [(60.6, 63.3), (61.5, 62.4), (74.0, 62.4), (74.0, 59.0)]),
    # Cruceta (GP16-19, columna izquierda): el haz pasa por encima de J5 (y 44.1-45.6), baja bajo el DAC
    # (permitido, seccion 8) a y 48.6-51.6 y sigue como antes por debajo de J3, repartiendose de derecha a izquierda
    ("BTN_RIGHT", SENAL, [(66.11, 40.02), (64.0, 40.02), (59.92, 44.1), (54.5, 44.1), (50.0, 48.6), (34.5, 48.6),
                          (34.5, 35.5), (31.25, 32.25)]),
    ("BTN_UP", SENAL, [(66.11, 42.56), (64.0, 42.56), (61.96, 44.6), (55.0, 44.6), (50.0, 49.6), (23.4, 49.6),
                       (23.4, 22.25), (21.25, 22.25)]),
    ("BTN_LEFT", SENAL, [(66.11, 47.64), (64.5, 47.64), (61.96, 45.1), (55.5, 45.1), (50.0, 50.6), (22.7, 50.6),
                         (22.7, 35.0), (14.0, 35.0), (11.25, 32.25)]),
    ("BTN_DOWN", SENAL, [(66.11, 50.18), (64.5, 50.18), (59.92, 45.6), (56.0, 45.6), (50.0, 51.6), (14.75, 51.6),
                         (14.75, 42.25)]),
    # SELECT y START bajan por entre las dos filas del modulo
    ("BTN_SELECT", SENAL, [(83.89, 40.02), (72.5, 40.02), (72.5, 53.0), (69.75, 55.75)]),
    ("BTN_START", SENAL, [(83.89, 42.56), (78.0, 42.56), (78.0, 53.5), (80.25, 55.75)]),
    # B y A cruzan la zona de bateria por F.Cu (permitido: solo pistas)
    ("BTN_B", SENAL, [(83.89, 47.64), (114.36, 47.64), (124.75, 37.25)]),
    ("BTN_A", SENAL, [(83.89, 50.18), (123.6, 50.18), (134.75, 39.03), (134.75, 27.25)]),
    # Pulsadores: los dos pads "1" de la huella oficial son pads distintos (el pulsador los une por dentro);
    # se unen con cobre para que la red quede completa sin depender de la pieza ni modificar la huella.
    ("BTN_UP", SENAL, [(14.75, 22.25), (21.25, 22.25)]),
    ("BTN_DOWN", SENAL, [(14.75, 42.25), (21.25, 42.25)]),
    ("BTN_LEFT", SENAL, [(4.75, 32.25), (11.25, 32.25)]),
    ("BTN_RIGHT", SENAL, [(24.75, 32.25), (31.25, 32.25)]),
    ("BTN_SELECT", SENAL, [(63.25, 55.75), (69.75, 55.75)]),
    ("BTN_START", SENAL, [(80.25, 55.75), (86.75, 55.75)]),
    ("BTN_B", SENAL, [(124.75, 37.25), (131.25, 37.25)]),
    ("BTN_A", SENAL, [(134.75, 27.25), (141.25, 27.25)]),
    # PWR_EN: de J2.17 sube por fuera de J2 y cruza por encima de J2.20 y J1.1 (y = 0.6) hasta SW10.
    # Es el unico camino en F.Cu que no corta el haz SPI.
    ("PWR_EN", SENAL, [(66.11, 9.54), (64.3, 9.54), (64.3, 1.3), (65.0, 0.6), (85.0, 0.6), (86.4, 2.0),
                       (132.0, 2.0), (134.0, 4.0), (134.0, 8.0)]),
]
for item in PISTAS:
    nombre, ancho, pts = item[:3]
    capa = pcbnew.B_Cu if len(item) > 3 else pcbnew.F_Cu
    for a, b in zip(pts, pts[1:]):
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(mm(*a))
        t.SetEnd(mm(*b))
        t.SetWidth(pcbnew.FromMM(ancho))
        t.SetLayer(capa)
        t.SetNet(red(nombre))
        board.Add(t)

# ---------------------------------------------------------------- plano de GND en B.Cu
z = pcbnew.ZONE(board)
z.SetLayer(pcbnew.B_Cu)
z.SetNet(red("GND"))
z.SetZoneName("GND_B")
ol = z.Outline()
ol.NewOutline()
for x, y in ((0, 0), (ANCHO, 0), (ANCHO, ALTO), (0, ALTO)):
    ol.Append(pcbnew.FromMM(x), pcbnew.FromMM(y))
z.SetLocalClearance(pcbnew.FromMM(0.30))
z.SetMinThickness(pcbnew.FromMM(0.25))
z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
z.SetThermalReliefGap(pcbnew.FromMM(0.50))
z.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.50))
z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
board.Add(z)


# ---------------------------------------------------------------- serigrafia
def pads_en(capa_cu):
    out = []
    for fp in board.GetFootprints():
        for p in fp.Pads():
            if p.IsOnLayer(capa_cu) or p.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH:
                r = max(pcbnew.ToMM(p.GetSize(pcbnew.F_Cu).x), pcbnew.ToMM(p.GetSize(pcbnew.F_Cu).y)) / 2
                out.append((xy(p.GetPosition()), r))
    return out


def linea(a, b, capa, ancho=SILK, libre=0.4):
    """Linea de serigrafia cortada alrededor de los pads (no se imprime sobre el cobre expuesto)."""
    cu = pcbnew.F_Cu if capa == pcbnew.F_SilkS else pcbnew.B_Cu
    obst = pads_en(cu)
    L = math.dist(a, b)
    n = max(1, int(L / 0.05))
    libres = []
    for i in range(n + 1):
        t = i / n
        p = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        libres.append(all(math.dist(p, c) > r + libre + ancho / 2 for c, r in obst))
    i = 0
    while i <= n:
        if libres[i]:
            j = i
            while j + 1 <= n and libres[j + 1]:
                j += 1
            if j > i:
                s = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
                ta, tb_ = i / n, j / n
                s.SetStart(mm(a[0] + (b[0] - a[0]) * ta, a[1] + (b[1] - a[1]) * ta))
                s.SetEnd(mm(a[0] + (b[0] - a[0]) * tb_, a[1] + (b[1] - a[1]) * tb_))
                s.SetLayer(capa)
                s.SetWidth(pcbnew.FromMM(ancho))
                board.Add(s)
            i = j + 1
        else:
            i += 1


def rect(x1, y1, x2, y2, capa):
    for a, b in (((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)), ((x2, y2), (x1, y2)), ((x1, y2), (x1, y1))):
        linea(a, b, capa)


def texto(t, x, y, capa, tam=TXT, ang=0):
    s = pcbnew.PCB_TEXT(board)
    s.SetText(t)
    s.SetLayer(capa)
    s.SetTextSize(mm(tam, tam))
    s.SetTextThickness(pcbnew.FromMM(SILK))
    s.SetTextAngleDegrees(ang)
    s.SetPosition(mm(x, y))
    if capa == pcbnew.B_SilkS:
        s.SetMirrored(True)
    board.Add(s)


F, B = pcbnew.F_SilkS, pcbnew.B_SilkS
# Frente: nombres de los botones (fuera del cuerpo) y referencia dentro del cuerpo
for ref, nombre, (x, y) in (("SW3", "UP", (18, 15.3)), ("SW1", "DOWN", (18, 44.8)), ("SW2", "LEFT", (8, 25.3)),
                            ("SW4", "RIGHT", (28, 25.3)), ("SW5", "SELECT", (66.5, 53.4)),
                            ("SW6", "START", (83.5, 53.4)), ("SW7", "B", (128, 41.0)), ("SW8", "A", (138, 31.0))):
    texto(nombre, x, y, F)
for ref, (cx, cy) in {"SW3": (18, 20), "SW1": (18, 40), "SW2": (8, 30), "SW4": (28, 30), "SW5": (66.5, 58),
                      "SW6": (83.5, 58), "SW7": (128, 35), "SW8": (138, 25)}.items():
    ref_en(SW[ref], cx, cy)
# Frente: contorno del modulo de pantalla (77.18 x 42.72 centrado en (75, 28)) y pin 1 de J3
rect(36.41, 6.64, 113.59, 49.36, F)
texto("PANTALLA TFT 2.4\" (J3)", 53.5, 9.0, F)
texto("1", 38.41, 9.3, F)
ref_en(J3, 40.6, 38.0, 90)
ref_en(C2, 33.0, 12.74, 90)
# Frente: creditos (fuera de los modulos y de la zona de bateria)
for i, linea_txt in enumerate(("KIDBOX v1.0 2026", "basado en", "Game*Mite de", "Thomas Hugo", "Williams",
                               "(CC BY 4.0)")):
    texto(linea_txt, 136.5, 44.0 + i * 2.0, F)

# Detras: RP2350-Plus (x 64.5-85.5, placa y 0.55-51.55) con el USB-C, pin 1 de J1 y J2, BOOT/RESET.
# Los lados se dibujan 0.5 mm por fuera para no pisar la serigrafia de las tiras J1/J2; arriba lo marca el USB-C.
linea((64.0, 0.55), (64.0, 52.0), B)
linea((86.0, 0.55), (86.0, 52.0), B)
linea((64.0, 52.0), (86.0, 52.0), B)
rect(70.7, 0.5, 79.6, 7.3, B)
texto("USB-C", 75.15, 8.6, B)
texto("1", 87.0, 1.92, B)
texto("1", 63.0, 50.18, B)
texto("BOOT/RST", 75, 23.0, B)  # botones del modulo a ~23 mm del extremo del USB-C; marcas por fuera
linea((62.6, 23.0), (63.8, 23.0), B)
linea((86.2, 23.0), (87.4, 23.0), B)
texto("VISTA POSTERIOR", 75, 30.0, B)
texto("FILAS ESPEJADAS", 75, 32.0, B)
texto("RP2350-Plus", 75, 36.0, B)
ref_en(J1, 87.2, 26.0, 90)
ref_en(J2, 62.9, 15.0, 90)
# Detras: DAC horizontal 31.85 x 17.78 (columna J5 a 1.5 mm del lado corto derecho y centrada en el): placa en
# x 28.65-60.5, y 44.56-62.34 -> se usa y 44.2-61.98 de la especificacion. Jack (estimado de fotos) con la boca al
# borde inferior y centro en x = 33.
DAC = (X_J5 + 1.5 - 31.85, 44.2, X_J5 + 1.5, 44.2 + 17.78)
rect(*DAC, B)
rect(30.0, 52.0, 36.0, 64.3, B)
texto("JACK", 33.0, 58.0, B)
texto("DAC PCM5102", 45.0, 53.0, B)
texto("VIN", 55.9, 59.8, B)
texto("GND", 55.9, 57.26, B)
ref_en(J5, 56.0, 48.4)
ref_en(C3, 55.8, 63.3)
ref_en(C4, 75.0, 63.0)
# Detras: interruptor y zona de bateria
ref_en(SW10, 134.0, 4.6)
# Posiciones de la palanca junto a su pad: OFF en el pad 2 (GND, x 136.54) y ON en el pad 3 (x 131.46).
# Visto desde atras (texto espejado) se lee OFF a la izquierda y ON a la derecha.
texto("OFF", 136.54, 11.3, B)
texto("ON", 131.46, 11.3, B)
rect(*BATERIA, B)
texto("BATERÍA 103450", 105.75, 33.0, B, tam=1.5, ang=90)
texto("sin patas THT", 109.0, 33.0, B, ang=90)
# Lugar para el numero de pedido de JLCPCB ("Order number: Specify a location"): centrado en la zona de bateria
# (y = 33), simetrico con "sin patas THT" respecto del texto BATERIA (x 105.75 -/+ 3.25), sin tocarlo.
texto("JLCJLCJLCJLC", 102.5, 33.0, B, ang=90)

# ---------------------------------------------------------------- comprobacion de la zona de bateria
avisos = []
for fp in board.GetFootprints():
    for p in fp.Pads():
        if not p.HasHole():
            continue
        (x, y) = xy(p.GetPosition())
        r = pcbnew.ToMM(p.GetSize(pcbnew.F_Cu).x) / 2
        x1, y1, x2, y2 = BATERIA
        if x1 <= x <= x2 and y1 <= y <= y2:
            sys.exit(f"{fp.GetReference()} pad {p.GetNumber()} ({x:.2f}, {y:.2f}) DENTRO de la zona de bateria")
        if x1 - r < x < x2 + r and y1 - r < y < y2 + r:
            avisos.append(f"{fp.GetReference()} pad {p.GetNumber()} en ({x:.2f}, {y:.2f}): el cobre del pad "
                          f"(r = {r:.2f}) entra en el margen de la zona de bateria")

# ---------------------------------------------------------------- relleno, guardado y UUID deterministas
# KiCad ordena las huellas por UUID al guardar: con UUID deterministas el archivo sale siempre igual
def uid(clave):
    return pcbnew.KIID(str(uuid.uuid5(NS, clave)))


for fp in board.GetFootprints():
    fp.SetUuidDirect(uid("fp/" + fp.GetReference()))
    for i, p in enumerate(fp.Pads()):
        p.SetUuidDirect(uid(f"pad/{fp.GetReference()}/{i}"))
    for i, g in enumerate(fp.GraphicalItems()):
        g.SetUuidDirect(uid(f"fpgr/{fp.GetReference()}/{i}"))
for i, t in enumerate(board.GetTracks()):
    t.SetUuidDirect(uid(f"pista/{i}"))
for i, g in enumerate(board.GetDrawings()):
    g.SetUuidDirect(uid(f"dibujo/{i}"))
for i, zz in enumerate(board.Zones()):
    zz.SetUuidDirect(uid(f"zona/{i}"))
pcbnew.ZONE_FILLER(board).Fill(board.Zones())
pcbnew.SaveBoard(PCB, board)
with open(PCB, encoding="utf-8") as f:
    texto_pcb = f.read()


# Metadatos de unidad del simbolo, (units (unit (name "A") (pins "1" "2"))), que KiCad 10 copia de la netlist en
# cada huella al hacer F8 (formato tomado de demos/pic_programmer, version 20260206). El API de Python no puede
# escribir la lista de pines (m_pins no esta expuesto), asi que se inserta tras (sheetfile ...) en el archivo.
def con_unidades(m):
    bloque_fp = m.group(0)
    ref = re.search(r'\(property "Reference" "([^"]+)"', bloque_fp).group(1)
    ind = re.search(r'\n(\t+)\(sheetfile ', bloque_fp).group(1)
    lineas = [f"{ind}(units"]
    for nombre_u, pines in COMP[ref]["unidades"]:
        lista = " ".join(f'"{x}"' for x in pines)
        lineas += [f"{ind}\t(unit", f'{ind}\t\t(name "{nombre_u}")', f"{ind}\t\t(pins{' ' + lista if lista else ''})",
                   f"{ind}\t)"]
    lineas.append(f"{ind})")
    return re.sub(r'(\n\t+\(sheetfile "[^"]*"\))', lambda mm: mm.group(1) + "\n" + "\n".join(lineas), bloque_fp,
                  count=1)


assert "(units" not in texto_pcb  # SaveBoard no las escribe: no se duplican
texto_pcb = re.sub(r'\n\t\(footprint ".*?\n\t\)(?=\n)', con_unidades, texto_pcb, flags=re.S)
cuenta = iter(range(10 ** 6))
texto_pcb = re.sub(r'\(uuid "[0-9a-f-]+"\)', lambda m: f'(uuid "{uuid.uuid5(NS, str(next(cuenta)))}")', texto_pcb)
with open(PCB, "w", encoding="utf-8", newline="\n") as f:
    f.write(texto_pcb)
escribir_reglas()

print("ok", PCB, f"({len(board.GetFootprints())} huellas, {len(board.GetTracks())} pistas)")
for a in avisos:
    print("AVISO:", a)
