# Genera KIDBOX/KIDBOX.kicad_pcb completo segun ESPECIFICACION.md v0.9, secciones 6 a 9:
# contorno 155 x 75 mm (r = 4 mm), agujeros, huellas en sus posiciones (las fijas con "locked"),
# pistas en F.Cu, plano de GND en B.Cu con alivios termicos, serigrafia, y reglas DFM en el .kicad_pro y .kicad_dru.
# v0.9 (26-oct, DECISIONES.md seccion 16): placa 155 x 75 simetrica respecto de x = 77.5; IMAGEN de la pantalla centrada
# (modulo corrido 4.0 mm hacia J3); RP2350-Plus centrado; DAC ADELANTE con huella propia (Connector_KIDBOX, jack
# centrado y al borde inferior); controles simetricos; SW10 arriba a la izquierda por detras; TP1/TP2; C4 en P1.50;
# todo re-ruteado: 3V3 sin pasar entre pines de J3, LRCK fuera de J5 (cruza J2 entre los pines 29 y 30).
# Fase 3: sin H5/H6 (ni KIDBOX.kicad_dru); SW5/SW6 en x = 66.5 / 83.5; DAC horizontal (J5 en columna en x = 59,
# VIN abajo, jack al borde inferior) con I2S, 3V3, C3 y C4 re-ruteados; huellas con hoja, archivo y filtros del
# simbolo para que "Actualizar PCB desde esquematico" (F8) no tenga nada que cambiar.
# Fase 4 (21-oct): pantalla (J3, C2) 3 mm mas arriba, DAC (J5, contorno, jack) 3 mm hacia la cruceta (x = 56) y C3
# vertical entre J5 y SELECT: nada queda bajo el DAC y C3 deja el borde inferior (DECISIONES.md seccion 12).
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
TXT_BOTON, SILK_BOTON = 1.2, 0.18  # rotulos de botones (sugerencia del profesor 4.4)
EJE = 77.5  # eje de simetria de la placa (155 / 2)
# zona de bateria (Bottom): sin componentes ni patas THT. v0.9: corrida +2.5 mm en x igual que el RP2350-Plus
BATERIA = (90.5, 4.0, 126.0, 62.0)


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
    if any(p.get("name") == "exclude_from_board" for p in c.iter("property")):
        continue  # BT1: solo esquematico y BOM
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
        if x.get("ref") in COMP:
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
tb.SetRevision("v0.9")
tb.SetDate("2026-10-26")
tb.SetCompany("Equipo KIDBOX")
tb.SetComment(0, "Basado en Game*Mite v1.3.2 de Thomas Hugo Williams (CC BY 4.0)")
tb.SetComment(1, "ESPECIFICACION.md v0.9 - 155 x 75 mm")
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
    # Connector_KIDBOX = libreria propia del proyecto (KIDBOX/KIDBOX.pretty, ver fp-lib-table y gen_huella_dac.py)
    ruta = os.path.join(CARPETA, "KIDBOX.pretty") if lib == "Connector_KIDBOX" else os.path.join(FP_DIR, lib + ".pretty")
    fp = pcbnew.FootprintLoad(ruta, nombre)
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
    fp.SetExcludedFromBOM("exclude_from_bom" in c["props"])  # TP1/TP2: la huella oficial ya viene excluida
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


# RP2350-Plus por detras: USB-C en y = 0, modulo y 0-51.55. Pin 1 a 1.37 mm del borde de su placa (que empieza en
# y = 0.55 porque el USB-C sobresale 0.55 mm) -> pin 1 en y = 1.92; filas a 17.78 mm (medido 21.0 x 51.55, confirmado).
# v0.9: modulo centrado en el eje x = 77.5 -> columnas en x = 68.61 (J2) y 86.39 (J1).
Y_PIN1 = 1.92
X_J1, X_J2 = round(EJE + 8.89, 2), round(EJE - 8.89, 2)
J1 = colocar("J1", columna(X_J1, Y_PIN1, 20), abajo=True)          # pines 1-20, arriba -> abajo
J2 = colocar("J2", columna(X_J2, Y_PIN1 + 19 * 2.54, 20, -2.54), abajo=True)  # pin 21 abajo -> 40 arriba
# Pantalla: la IMAGEN (48.96 x 36.72, dato del panel) centrada en x = 77.5. Medido con la pieza encendida, el centro de la
# imagen esta 4.0 mm corrido respecto del centro del modulo hacia el lado opuesto a J3 -> modulo centrado en x = 73.5.
# Altura igual que en la v0.8 (centro y = 25): la imagen queda arriba y la franja inferior libre para el DAC.
MOD = (EJE - 4.0 - 77.18 / 2, 25 - 42.72 / 2, EJE - 4.0 + 77.18 / 2, 25 + 42.72 / 2)  # 34.91, 3.64, 112.09, 46.36
IMAGEN = (EJE - 48.96 / 2, 25 - 36.72 / 2, EJE + 48.96 / 2, 25 + 36.72 / 2)          # 53.02, 6.64, 101.98, 43.36
X_J3 = round(MOD[0] + 2.0, 2)                                       # J3 a 2.00 mm del borde izquierdo: 36.91
J3 = colocar("J3", columna(X_J3, 25 - 6.5 * 2.54, 14))             # pin 1 (VCC) arriba, pines y 8.49-41.51
# DAC ADELANTE (v0.9), huella propia: jack centrado en x = 77.5 con la boca al ras del borde inferior (y = 75).
# Medidas reales: placa 31.85 x 17.5; columna a 1.5 mm del borde corto, centrada a lo ancho; eje del jack a 24.9 mm de la
# columna; el jack sobresale 1.4 mm del borde largo. Visto de frente: pines a la izquierda, VIN abajo, SCK arriba.
X_J5 = round(EJE - 24.9, 2)                                          # 52.6
Y_VIN = round(ALTO - 1.4 - (17.5 - 5 * 2.54) / 2, 2)                # 75 - 1.4 - 2.4 = 71.2
J5 = colocar("J5", {str(i + 1): [(X_J5, round(Y_VIN - i * 2.54, 2))] for i in range(6)})
DAC = (X_J5 - 1.5, Y_VIN + 2.4 - 17.5, X_J5 - 1.5 + 31.85, Y_VIN + 2.4)  # 51.1, 56.1, 82.95, 73.6
JACK = (EJE - 2.35, ALTO - 14.0, EJE + 2.35, ALTO)                   # 75.15, 61, 79.85, 75


def boton(ref, cx, cy, pad1_abajo):
    """Pulsador 6x6: patas a 6.5 (x) por 4.5 (y) del centro del cuerpo; pad1_abajo elige la fila del pin 1."""
    y1, y2 = (cy + 2.25, cy - 2.25) if pad1_abajo else (cy - 2.25, cy + 2.25)
    return colocar(ref, {"1": [(cx - 3.25, y1), (cx + 3.25, y1)], "2": [(cx - 3.25, y2), (cx + 3.25, y2)]})


# Controles simetricos respecto de x = 77.5 (propuesta P2 del estudio ergonomico adaptada a 155 mm): cruceta con centro
# (18, 44) y brazos de 10 mm; A/B en espejo (punto medio x = 137); SELECT/START en la franja inferior (41 / 114, y = 67).
CENTROS = {"SW3": (18, 34), "SW1": (18, 54), "SW2": (8, 44), "SW4": (28, 44),
           "SW7": (132, 49), "SW8": (142, 39), "SW5": (41, 67), "SW6": (114, 67)}
PAD1_ABAJO = {"SW3": True, "SW1": False, "SW2": True, "SW4": True, "SW7": False, "SW8": True, "SW5": True, "SW6": False}
SW = {r: boton(r, *CENTROS[r], PAD1_ABAJO[r]) for r in CENTROS}
# SW10 por detras, arriba a la izquierda (fuera de la zona de los indices): pad 1 (central, comun) en (50, 8).
# Pad 2 (GND = OFF) a la derecha visto de frente, es decir, a la izquierda visto desde atras.
SW10 = colocar("SW10", {"1": [(50, 8)], "2": [(52.54, 8)], "3": [(47.46, 8)]}, abajo=True)
# C2 vertical a la izquierda de J3: pad 1 (+3V3) a la altura del pin 1 de J3, pad 2 (GND) 5 mm mas abajo
C2 = colocar("C2", {"1": [(33.1, 8.49)], "2": [(33.1, 13.49)]}, fija=False)
# TP1 (+3V3) y TP2 (GND) a la izquierda de C2, fuera de los modulos (accesibles con todo montado)
TP1 = colocar("TP1", {"1": [(29.8, 8.49)]}, fija=False)
TP2 = colocar("TP2", {"1": [(29.8, 13.49)]}, fija=False)
# C4 (D4, paso 1.5) a la altura de VIN, entre SELECT y el DAC, con el + (pad cuadrado) del lado de J5.
# C3 vertical justo encima: pad 1 (+3V3) abajo. Courtyards: SELECT hasta x 45.8, C3 46.76-49.85, C4 46.0-50.6, DAC desde 50.85.
C4 = colocar("C4", {"1": [(49.05, Y_VIN)], "2": [(47.55, Y_VIN)]}, fija=False)
C3 = colocar("C3", {"1": [(48.3, 67.6)], "2": [(48.3, 62.6)]}, fija=False)
H = {}
for ref, (x, y) in {"H1": (4, 4), "H2": (ANCHO - 4, 4), "H3": (4, ALTO - 4), "H4": (ANCHO - 4, ALTO - 4)}.items():
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
    # Los pines 3-7 de J3 quedan 0.22 mm bajo los huecos de J2: un salto corto a 45 grados en x 45.5.
    ("LCD_CS", SENAL, [(86.39, 1.92), (82.08, 1.92), (70.65, 13.35), (45.5, 13.35), (45.28, 13.57), (36.91, 13.57)]),
    ("LCD_RST", SENAL, [(86.39, 4.46), (82.04, 4.46), (70.61, 15.89), (45.5, 15.89), (45.28, 16.11), (36.91, 16.11)]),
    ("LCD_DC", SENAL, [(86.39, 9.54), (79.46, 9.54), (70.57, 18.43), (45.5, 18.43), (45.28, 18.65), (36.91, 18.65)]),
    ("LCD_MOSI", SENAL, [(86.39, 12.08), (79.42, 12.08), (70.53, 20.97), (45.5, 20.97), (45.28, 21.19),
                         (36.91, 21.19)]),
    ("LCD_SCK", SENAL, [(86.39, 22.24), (71.76, 22.24), (70.49, 23.51), (45.5, 23.51), (45.28, 23.73),
                        (36.91, 23.73)]),
    ("LCD_LED", SENAL, [(68.61, 24.78), (47.0, 24.78), (45.51, 26.27), (36.91, 26.27)]),
    # I2S al DAC. J2 tiene DIN, LRCK, BCK (arriba -> abajo) y J5 tiene BCK, DIN, LCK: el orden esta rotado y VIN cierra la
    # columna por abajo, asi que una de las tres tiene que pasar entre pines. LRCK sale de J2 por la izquierda, sube y
    # entra al interior del modulo entre J2.30 (RUN, sin uso) y J2.29 (DIN): queda por encima de DIN y las tres llegan a J5
    # por la derecha, sin pasar entre sus pines (sugerencia del profesor 3.2). BCK pasa bajo J2.21 a 0.85 mm.
    ("I2S_BCK", SENAL, [(68.61, 37.48), (70.3, 37.48), (70.3, 52.0), (54.0, 52.0), (54.0, 61.04), (52.6, 61.04)]),
    ("I2S_DIN", SENAL, [(68.61, 29.86), (70.9, 29.86), (70.9, 52.6), (54.6, 52.6), (54.6, 63.58), (52.6, 63.58)]),
    ("I2S_LRCK", SENAL, [(68.61, 34.94), (67.0, 34.94), (67.0, 28.59), (71.5, 28.59), (71.5, 53.2), (55.2, 53.2),
                         (55.2, 66.12), (52.6, 66.12)]),
    # 3V3: J2.36 -> J3.1 -> C2 -> TP1. Rama al DAC: baja por la izquierda de J3, pasa BAJO J3.14 (sin pasar entre pines
    # de J3, sugerencia 3.1), sube en diagonal bajo la pantalla, entra al modulo entre J2.31 y J2.30 con 0.25 mm (0.295 mm a
    # cada pad), baja por el interior y llega a VIN por la derecha; de VIN sigue a C4+ y sube a C3.
    ("+3V3", POTENCIA, [(68.61, 12.08), (40.5, 12.08), (36.91, 8.49)]),
    ("+3V3", POTENCIA, [(36.91, 8.49), (29.8, 8.49)]),
    ("+3V3", POTENCIA, [(35.2, 8.49), (35.2, 43.3), (38.5, 43.3), (55.75, 26.05), (66.6, 26.05)]),
    ("+3V3", SENAL, [(66.6, 26.05), (70.6, 26.05)]),
    ("+3V3", POTENCIA, [(70.6, 26.05), (72.4, 26.05), (72.4, 54.0), (56.1, 54.0), (56.1, Y_VIN), (49.05, Y_VIN)]),
    ("+3V3", POTENCIA, [(50.4, Y_VIN), (50.4, 67.6), (48.3, 67.6)]),
    # Cruceta (GP16-19, columna izquierda): sale de J2 hacia la izquierda, baja en diagonales paralelas a y 48-51 (bajo la
    # pantalla, sobre el DAC) y se reparte: RIGHT, UP (sube entre RIGHT y la columna UP/DOWN), LEFT (sobre DOWN) y DOWN.
    ("BTN_RIGHT", SENAL, [(68.61, 40.02), (62.0, 40.02), (54.02, 48.0), (33.0, 48.0), (31.25, 46.25)]),
    ("BTN_UP", SENAL, [(68.61, 42.56), (63.0, 42.56), (56.56, 49.0), (23.0, 49.0), (23.0, 38.0), (21.25, 36.25)]),
    ("BTN_LEFT", SENAL, [(68.61, 47.64), (64.5, 47.64), (62.14, 50.0), (15.0, 50.0), (11.25, 46.25)]),
    ("BTN_DOWN", SENAL, [(68.61, 50.18), (66.0, 50.18), (65.18, 51.0), (22.0, 51.0), (21.25, 51.75)]),
    # SELECT y START bajan por entre las dos filas del modulo. SELECT sigue hasta el borde inferior (bajo J5 y C4) y
    # entra a su pad 1 por abajo; START sale hacia la derecha bajo J1 y baja en diagonal (pistas en la zona de bateria).
    ("BTN_SELECT", SENAL, [(86.39, 40.02), (74.0, 40.02), (74.0, 73.6), (44.25, 73.6), (44.25, 69.25)]),
    ("BTN_START", SENAL, [(86.39, 42.56), (75.0, 42.56), (75.0, 55.5), (101.5, 55.5), (110.75, 64.75)]),
    # B y A cruzan la zona de bateria por F.Cu (permitido: solo pistas); A pasa bajo B y sube por su derecha
    ("BTN_B", SENAL, [(86.39, 47.64), (127.86, 47.64), (128.75, 46.75)]),
    ("BTN_A", SENAL, [(86.39, 50.18), (89.51, 53.3), (137.5, 53.3), (137.5, 42.5), (138.75, 41.25)]),
    # Pulsadores: los dos pads "1" de la huella oficial son pads distintos (el pulsador los une por dentro);
    # se unen con cobre para que la red quede completa sin depender de la pieza ni modificar la huella.
    ("BTN_UP", SENAL, [(14.75, 36.25), (21.25, 36.25)]),
    ("BTN_DOWN", SENAL, [(14.75, 51.75), (21.25, 51.75)]),
    ("BTN_LEFT", SENAL, [(4.75, 46.25), (11.25, 46.25)]),
    ("BTN_RIGHT", SENAL, [(24.75, 46.25), (31.25, 46.25)]),
    ("BTN_SELECT", SENAL, [(37.75, 69.25), (44.25, 69.25)]),
    ("BTN_START", SENAL, [(110.75, 64.75), (117.25, 64.75)]),
    ("BTN_B", SENAL, [(128.75, 46.75), (135.25, 46.75)]),
    ("BTN_A", SENAL, [(138.75, 41.25), (145.25, 41.25)]),
    # PWR_EN: de J2.17 directo a la izquierda hasta el comun de SW10 (y >= 8, lejos del borde superior)
    ("PWR_EN", SENAL, [(68.61, 9.54), (50.0, 9.54), (50.0, 8.0)]),
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


def texto(t, x, y, capa, tam=TXT, ang=0, grosor=SILK):
    s = pcbnew.PCB_TEXT(board)
    s.SetText(t)
    s.SetLayer(capa)
    s.SetTextSize(mm(tam, tam))
    s.SetTextThickness(pcbnew.FromMM(grosor))
    s.SetTextAngleDegrees(ang)
    s.SetPosition(mm(x, y))
    if capa == pcbnew.B_SilkS:
        s.SetMirrored(True)
    board.Add(s)


F, B = pcbnew.F_SilkS, pcbnew.B_SilkS
# Frente: nombres de los botones (1.2/0.18, fuera del cuerpo) y referencia dentro del cuerpo
for ref, nombre, (x, y) in (("SW3", "UP", (18, 29.0)), ("SW1", "DOWN", (18, 59.0)), ("SW2", "LEFT", (8, 39.0)),
                            ("SW4", "RIGHT", (28, 39.0)), ("SW5", "SELECT", (41, 62.2)), ("SW6", "START", (114, 62.2)),
                            ("SW7", "B", (132, 55.0)), ("SW8", "A", (142, 45.0))):
    texto(nombre, x, y, F, tam=TXT_BOTON, grosor=SILK_BOTON)
for ref, (cx, cy) in CENTROS.items():
    ref_en(SW[ref], cx, cy)
# Frente: contorno del modulo de pantalla, imagen (48.96 x 36.72 centrada en x = 77.5) y pin 1 de J3
rect(*MOD, F)
rect(*IMAGEN, F)
texto("PANTALLA TFT 2.4\" (J3)", 52.5, 5.3, F)
texto("IMAGEN", EJE, 39.8, F)  # entre las dos filas del modulo (fuera de los pads de J1/J2)
texto("48.96 x 36.72", EJE, 41.8, F)
texto("1", X_J3, 6.3, F)
ref_en(J3, 39.1, 35.0, 90)
ref_en(C2, 33.1, 15.6)
ref_en(TP1, 29.8, 6.1)
ref_en(TP2, 29.8, 15.9)
texto("3V3", 26.4, 8.49, F)
texto("GND", 26.4, 13.49, F)
# Frente: DAC (el contorno del modulo y del jack vienen en la huella de J5), VIN/GND junto a J5, C3 y C4
texto("DAC PCM5102", 66.0, 58.5, F)
texto("JACK", EJE, 67.0, F)
texto("VIN", 58.6, Y_VIN, F)
texto("GND", 58.6, round(Y_VIN - 2.54, 2), F)
ref_en(J5, 64.6, 54.9)
ref_en(C3, 46.2, 65.1, 90)
ref_en(C4, 45.2, 73.9)
# Frente: creditos, en la franja libre entre el DAC y START (fuera de los modulos y de la zona de bateria)
for i, linea_txt in enumerate(("KIDBOX v0.9 2026", "basado en", "Game*Mite de", "Thomas Hugo", "Williams",
                               "(CC BY 4.0)")):
    texto(linea_txt, 95.0, 59.0 + i * 2.0, F)

# Detras: RP2350-Plus (placa x 67.0-88.0, y 0.55-51.55) con el USB-C, pin 1 de J1 y J2, BOOT/RESET.
# Los lados se dibujan 0.5 mm por fuera para no pisar la serigrafia de las tiras J1/J2; arriba lo marca el USB-C.
# USB-C segun el plano oficial: 8.95 mm de ancho, 6.2 mm desde el borde izquierdo del modulo visto desde el frente.
X_MOD_RP = EJE - 10.5
linea((X_MOD_RP - 0.5, 0.55), (X_MOD_RP - 0.5, 52.0), B)
linea((X_MOD_RP + 21.5, 0.55), (X_MOD_RP + 21.5, 52.0), B)
linea((X_MOD_RP - 0.5, 52.0), (X_MOD_RP + 21.5, 52.0), B)
USB = (X_MOD_RP + 6.2, 0.5, X_MOD_RP + 6.2 + 8.95, 7.3)
rect(*USB, B)
texto("USB-C", (USB[0] + USB[2]) / 2, 8.6, B)
texto("1", X_J1 + 3.11, 1.92, B)
texto("1", X_J2 - 3.11, 50.18, B)
texto("BOOT/RST", EJE, 23.0, B)  # botones del modulo a ~23 mm del extremo del USB-C; marcas por fuera
linea((X_J2 - 3.51, 23.0), (X_J2 - 2.31, 23.0), B)
linea((X_J1 + 2.31, 23.0), (X_J1 + 3.51, 23.0), B)
texto("VISTA POSTERIOR", EJE, 30.0, B)
texto("FILAS ESPEJADAS", EJE, 32.0, B)
texto("RP2350-Plus", EJE, 36.0, B)
ref_en(J1, X_J1 + 3.31, 26.0, 90)
ref_en(J2, X_J2 - 3.21, 15.0, 90)
# Detras: interruptor, zona de bateria y cajetin
ref_en(SW10, 50.0, 4.6)
# Posiciones de la palanca junto a su pad: OFF en el pad 2 (GND, x 52.54) y ON en el pad 3 (x 47.46).
# Visto desde atras (texto espejado) se lee OFF a la izquierda y ON a la derecha (medido: la palanca une el comun con la
# pata de su lado).
texto("OFF", 52.54, 11.3, B)
texto("ON", 47.46, 11.3, B)
rect(*BATERIA, B)
X_BAT = (BATERIA[0] + BATERIA[2]) / 2  # 108.25
texto("BATERÍA 103450", X_BAT, 33.0, B, tam=1.5, ang=90)
texto("sin patas THT", X_BAT + 3.25, 33.0, B, ang=90)
# Lugar para el numero de pedido de JLCPCB ("Order number: Specify a location"): centrado en la zona de bateria
# (y = 33), simetrico con "sin patas THT" respecto del texto BATERIA (x 108.25 -/+ 3.25), sin tocarlo.
texto("JLCJLCJLCJLC", X_BAT - 3.25, 33.0, B, ang=90)
texto("KIDBOX v0.9 - 26-oct-2026", 136.0, 65.0, B)  # bajo la zona de bateria
texto("155 x 75 mm - 1.6 mm - 2 capas", 136.0, 67.0, B)

# ---------------------------------------------------------------- comprobaciones de la v0.9
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

# Nada bajo el DAC (seccion 6): ningun agujero dentro del contorno del modulo salvo los de J5
for fp in board.GetFootprints():
    for p in fp.Pads():
        (x, y) = xy(p.GetPosition())
        r = pcbnew.ToMM(p.GetSize(pcbnew.F_Cu).x) / 2
        if fp.GetReference() != "J5" and DAC[0] - r < x < DAC[2] + r and DAC[1] - r < y < DAC[3] + r:
            sys.exit(f"{fp.GetReference()} pad {p.GetNumber()} ({x:.2f}, {y:.2f}) bajo el contorno del DAC")


def dist_rect(p, r):
    return math.hypot(max(r[0] - p[0], 0, p[0] - r[2]), max(r[1] - p[1], 0, p[1] - r[3]))


# Capuchones redondos D10: >= 1.5 mm de aire al contorno de la pantalla y del DAC; simetria respecto de x = 77.5
for ref, (cx, cy) in CENTROS.items():
    for nombre_mod, caja in (("pantalla", MOD), ("DAC", DAC)):
        aire = dist_rect((cx, cy), caja) - 5.0
        if aire < 1.5:
            sys.exit(f"capuchon de {ref} a {aire:.2f} mm del {nombre_mod} (minimo 1.5)")
if abs((18 + 137) / 2 - EJE) > 1e-9 or abs((CENTROS["SW5"][0] + CENTROS["SW6"][0]) / 2 - EJE) > 1e-9:
    sys.exit("los controles no quedan simetricos respecto de x = 77.5")
if abs((IMAGEN[0] + IMAGEN[2]) / 2 - EJE) > 1e-9 or abs((JACK[0] + JACK[2]) / 2 - EJE) > 1e-9:
    sys.exit("la imagen o el jack no quedan centrados en x = 77.5")
if DAC[1] - MOD[3] < 5:
    sys.exit(f"DAC a {DAC[1] - MOD[3]:.2f} mm de la pantalla (minimo 5)")

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
