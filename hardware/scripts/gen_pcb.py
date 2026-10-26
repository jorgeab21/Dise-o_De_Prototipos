# Genera KIDBOX/KIDBOX.kicad_pcb completo segun ESPECIFICACION.md v0.9, secciones 6 a 9:
# contorno 150 x 70 mm (r = 4 mm), agujeros, huellas en sus posiciones (las fijas con "locked"),
# pistas en F.Cu, plano de GND en B.Cu con alivios termicos, serigrafia, y reglas DFM en el .kicad_pro y .kicad_dru.
# v0.9 (26-oct, DECISIONES.md secciones 16 y 17): placa 150 x 70 simetrica respecto de x = 75; IMAGEN de la pantalla centrada
# (modulo corrido 4.0 mm hacia J3); RP2350-Plus centrado; DAC ADELANTE con huella propia (Connector_KIDBOX, jack
# centrado y al borde inferior); controles simetricos; SW10 arriba a la izquierda por detras; TP1/TP2; C4 en P1.50;
# todo re-ruteado: 3V3 sin pasar entre pines de J3, LRCK fuera de J5 (cruza J2 entre los pines 29 y 30).
# Ajuste tras la prueba 1:1 (seccion 17): 150 x 70, controles compactos (capuchones D9), DAC 5 mm mas arriba, franja de
# 4.74 mm para un muro colgante de la carcasa entre pantalla y DAC, bateria en la carcasa (zona solo de referencia).
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
EJE = ANCHO / 2  # eje de simetria de la placa: x = 75
# zona de bateria (Bottom), solo referencia: la bateria va en la carcasa. Se permiten patas THT; no componentes altos.
BATERIA = (88.0, 4.0, 123.5, 62.0)


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
tb.SetComment(1, "ESPECIFICACION.md v0.9 - 150 x 70 mm")
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
# v0.9 (150 x 70): modulo centrado en el eje x = 75 -> columnas en x = 66.11 (J2) y 83.89 (J1).
Y_PIN1 = 1.92
X_J1, X_J2 = round(EJE + 8.89, 2), round(EJE - 8.89, 2)
J1 = colocar("J1", columna(X_J1, Y_PIN1, 20), abajo=True)          # pines 1-20, arriba -> abajo
J2 = colocar("J2", columna(X_J2, Y_PIN1 + 19 * 2.54, 20, -2.54), abajo=True)  # pin 21 abajo -> 40 arriba
# Pantalla: la IMAGEN (48.96 x 36.72, dato del panel) centrada en x = 75. Medido con la pieza encendida, el centro de la
# imagen esta 4.0 mm corrido respecto del centro del modulo hacia el lado opuesto a J3 -> modulo centrado en x = 71.
# Altura igual que en la v0.8 (centro y = 25): la imagen queda arriba y la franja inferior libre para el DAC.
MOD = (EJE - 4.0 - 77.18 / 2, 25 - 42.72 / 2, EJE - 4.0 + 77.18 / 2, 25 + 42.72 / 2)  # 32.41, 3.64, 109.59, 46.36
IMAGEN = (EJE - 48.96 / 2, 25 - 36.72 / 2, EJE + 48.96 / 2, 25 + 36.72 / 2)          # 50.52, 6.64, 99.48, 43.36
X_J3 = round(MOD[0] + 2.0, 2)                                       # J3 a 2.00 mm del borde izquierdo: 34.41
J3 = colocar("J3", columna(X_J3, 25 - 6.5 * 2.54, 14))             # pin 1 (VCC) arriba, pines y 8.49-41.51
# DAC ADELANTE, huella propia: jack centrado en x = 75 con la boca al ras del borde inferior (y = 70).
# Medidas reales: placa 31.85 x 17.5; columna a 1.5 mm del borde corto, centrada a lo ancho; eje del jack a 24.9 mm de la
# columna; el jack sobresale 1.4 mm del borde largo. Visto de frente: pines a la izquierda, VIN abajo, SCK arriba.
X_J5 = round(EJE - 24.9, 2)                                          # 50.1
Y_VIN = round(ALTO - 1.4 - (17.5 - 5 * 2.54) / 2, 2)                # 70 - 1.4 - 2.4 = 66.2
J5 = colocar("J5", {str(i + 1): [(X_J5, round(Y_VIN - i * 2.54, 2))] for i in range(6)})
DAC = (X_J5 - 1.5, Y_VIN + 2.4 - 17.5, X_J5 - 1.5 + 31.85, Y_VIN + 2.4)  # 48.6, 51.1, 80.45, 68.6
JACK = (EJE - 2.35, ALTO - 14.0, EJE + 2.35, ALTO)                   # 72.65, 56, 77.35, 70
# Franja del muro de la carcasa entre la pantalla y el DAC (4.74 mm): el muro es colgante desde la tapa frontal y termina
# >= 4 mm sobre la PCB, asi que pasa por encima de las soldaduras de J2.21/J2.22 y J1.19/J1.20 (~2 mm de alto).
MURO = (DAC[0], MOD[3], DAC[2], DAC[1])
Y_MURO = round((MOD[3] + DAC[1]) / 2, 2)                             # 48.73


def boton(ref, cx, cy, pad1_abajo):
    """Pulsador 6x6: patas a 6.5 (x) por 4.5 (y) del centro del cuerpo; pad1_abajo elige la fila del pin 1."""
    y1, y2 = (cy + 2.25, cy - 2.25) if pad1_abajo else (cy - 2.25, cy + 2.25)
    return colocar(ref, {"1": [(cx - 3.25, y1), (cx + 3.25, y1)], "2": [(cx - 3.25, y2), (cx + 3.25, y2)]})


# Controles simetricos respecto de x = 75, compactos (capuchones redondos D9): cruceta con centro (16.5, 39) y brazos de
# 9 mm; A/B en espejo (punto medio x = 133.5, diagonal de 9 mm); SELECT/START en la franja inferior (38.5 / 111.5, y = 62).
R_CAP = 4.5
CENTROS = {"SW3": (16.5, 30), "SW1": (16.5, 48), "SW2": (7.5, 39), "SW4": (25.5, 39),
           "SW7": (129, 43.5), "SW8": (138, 34.5), "SW5": (38.5, 62), "SW6": (111.5, 62)}
PAD1_ABAJO = {"SW3": True, "SW1": False, "SW2": True, "SW4": True, "SW7": False, "SW8": True, "SW5": True, "SW6": False}
SW = {r: boton(r, *CENTROS[r], PAD1_ABAJO[r]) for r in CENTROS}
# SW10 por detras, arriba a la izquierda (fuera de la zona de los indices): pad 1 (central, comun) en (47.5, 8).
# Pad 2 (GND = OFF) a la derecha visto de frente, es decir, a la izquierda visto desde atras.
SW10 = colocar("SW10", {"1": [(47.5, 8)], "2": [(50.04, 8)], "3": [(44.96, 8)]}, abajo=True)
# C2 vertical a la izquierda de J3: pad 1 (+3V3) a la altura del pin 1 de J3, pad 2 (GND) 5 mm mas abajo
X_C2 = round(X_J3 - 3.81, 2)                                         # 30.6
C2 = colocar("C2", {"1": [(X_C2, 8.49)], "2": [(X_C2, 13.49)]}, fija=False)
# TP1 (+3V3) y TP2 (GND) a la izquierda de C2, fuera de los modulos (accesibles con todo montado)
X_TP = round(X_C2 - 3.3, 2)                                          # 27.3
TP1 = colocar("TP1", {"1": [(X_TP, 8.49)]}, fija=False)
TP2 = colocar("TP2", {"1": [(X_TP, 13.49)]}, fija=False)
# C4 (D4, paso 1.5) a la altura de VIN, entre SELECT y el DAC, con el + (pad cuadrado) del lado de J5.
# C3 vertical justo encima: pad 1 (+3V3) abajo. (Mismo grupo que antes, corrido -2.5 / -5 mm junto con SELECT y el DAC.)
C4 = colocar("C4", {"1": [(46.55, Y_VIN)], "2": [(45.05, Y_VIN)]}, fija=False)
C3 = colocar("C3", {"1": [(45.8, 62.6)], "2": [(45.8, 57.6)]}, fija=False)
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
    # Los pines 3-7 de J3 quedan 0.22 mm bajo los huecos de J2: un salto corto a 45 grados en x 43.
    ("LCD_CS", SENAL, [(83.89, 1.92), (79.58, 1.92), (68.15, 13.35), (43.0, 13.35), (42.78, 13.57), (34.41, 13.57)]),
    ("LCD_RST", SENAL, [(83.89, 4.46), (79.54, 4.46), (68.11, 15.89), (43.0, 15.89), (42.78, 16.11), (34.41, 16.11)]),
    ("LCD_DC", SENAL, [(83.89, 9.54), (76.96, 9.54), (68.07, 18.43), (43.0, 18.43), (42.78, 18.65), (34.41, 18.65)]),
    ("LCD_MOSI", SENAL, [(83.89, 12.08), (76.92, 12.08), (68.03, 20.97), (43.0, 20.97), (42.78, 21.19),
                         (34.41, 21.19)]),
    ("LCD_SCK", SENAL, [(83.89, 22.24), (69.26, 22.24), (67.99, 23.51), (43.0, 23.51), (42.78, 23.73),
                        (34.41, 23.73)]),
    ("LCD_LED", SENAL, [(66.11, 24.78), (44.5, 24.78), (43.01, 26.27), (34.41, 26.27)]),
    # I2S al DAC. J2 tiene DIN, LRCK, BCK (arriba -> abajo) y J5 tiene BCK, DIN, LCK: el orden esta rotado y VIN cierra la
    # columna por abajo, asi que una de las tres tiene que pasar entre pines. LRCK sale de J2 por la izquierda, sube y
    # entra al interior del modulo entre J2.30 (RUN, sin uso) y J2.29 (DIN): queda por encima de DIN y las tres llegan a J5
    # por la derecha, sin pasar entre sus pines (sugerencia del profesor 3.2). Pasan bajo J2.21 y bajo el DAC.
    ("I2S_BCK", SENAL, [(66.11, 37.48), (68.0, 37.48), (68.0, 52.6), (51.5, 52.6), (51.5, 56.04), (50.1, 56.04)]),
    ("I2S_DIN", SENAL, [(66.11, 29.86), (68.6, 29.86), (68.6, 53.2), (52.1, 53.2), (52.1, 58.58), (50.1, 58.58)]),
    ("I2S_LRCK", SENAL, [(66.11, 34.94), (64.5, 34.94), (64.5, 28.59), (69.2, 28.59), (69.2, 53.8), (52.7, 53.8),
                         (52.7, 61.12), (50.1, 61.12)]),
    # 3V3: J2.36 -> J3.1 -> C2 -> TP1. Rama al DAC: baja por la izquierda de J3, pasa BAJO J3.14 (sin pasar entre pines
    # de J3, sugerencia 3.1), sube en diagonal bajo la pantalla, entra al modulo entre J2.31 y J2.30 con 0.25 mm (0.295 mm a
    # cada pad), baja por el interior y llega a VIN por la derecha; de VIN sigue a C4+ y sube a C3.
    ("+3V3", POTENCIA, [(66.11, 12.08), (38.0, 12.08), (34.41, 8.49)]),
    ("+3V3", POTENCIA, [(34.41, 8.49), (X_TP, 8.49)]),
    ("+3V3", POTENCIA, [(32.7, 8.49), (32.7, 42.92), (36.0, 42.92), (52.87, 26.05), (64.1, 26.05)]),
    ("+3V3", SENAL, [(64.1, 26.05), (68.1, 26.05)]),
    ("+3V3", POTENCIA, [(68.1, 26.05), (70.1, 26.05), (70.1, 54.6), (53.6, 54.6), (53.6, Y_VIN), (46.55, Y_VIN)]),
    ("+3V3", POTENCIA, [(47.9, Y_VIN), (47.9, 62.6), (45.8, 62.6)]),
    # Cruceta (GP16-19). Con brazos de 9 mm entre las columnas de pads solo quedan 0.5 mm, pero entre las filas quedan dos
    # canales horizontales de 2.5 mm (y 33.25-35.75 sobre LEFT/RIGHT y y 42.25-44.75 bajo ellos).
    # RIGHT, LEFT y DOWN salen de J2 por la izquierda, convergen a y 43.6 / 44.2 / 44.8 y van por el canal inferior:
    # RIGHT sube a su pad este, DOWN baja a su pad superior y LEFT sigue hasta su pad este.
    ("BTN_RIGHT", SENAL, [(66.11, 40.02), (62.0, 40.02), (58.42, 43.6), (30.1, 43.6), (28.75, 42.25), (28.75, 41.25)]),
    ("BTN_LEFT", SENAL, [(66.11, 47.64), (65.4, 47.64), (61.96, 44.2), (13.7, 44.2), (10.75, 41.25)]),
    ("BTN_DOWN", SENAL, [(66.11, 50.18), (64.0, 50.18), (58.62, 44.8), (20.7, 44.8), (19.75, 45.75)]),
    # UP sale de J2 hacia el interior del modulo, baja pegado a J2 (0.315 mm de sus pads), pasa bajo J2.21 y bajo la
    # cruceta (y 52), sube por el borde izquierdo (x 2) y entra por el canal superior a su pad oeste.
    ("BTN_UP", SENAL, [(66.11, 42.56), (67.4, 42.56), (67.4, 52.0), (2.0, 52.0), (2.0, 34.5), (11.0, 34.5),
                       (13.25, 32.25)]),
    # SELECT y START bajan por entre las dos filas del modulo. SELECT sigue hasta el borde inferior (bajo J5 y C4) y
    # entra a su pad 1 por abajo; START sale hacia la derecha bajo J1 y baja en diagonal.
    ("BTN_SELECT", SENAL, [(83.89, 40.02), (71.7, 40.02), (71.7, 68.6), (41.75, 68.6), (41.75, 64.25)]),
    ("BTN_START", SENAL, [(83.89, 42.56), (72.7, 42.56), (72.7, 52.5), (101.0, 52.5), (108.25, 59.75)]),
    # B entra por la izquierda a su fila superior; A pasa bajo B y sube por la derecha de A (x 144) hasta su fila inferior
    ("BTN_B", SENAL, [(83.89, 47.64), (119.36, 47.64), (125.75, 41.25)]),
    ("BTN_A", SENAL, [(83.89, 50.18), (144.0, 50.18), (144.0, 38.0), (142.75, 36.75), (141.25, 36.75)]),
    # Pulsadores: los dos pads "1" de la huella oficial son pads distintos (el pulsador los une por dentro);
    # se unen con cobre para que la red quede completa sin depender de la pieza ni modificar la huella.
    ("BTN_UP", SENAL, [(13.25, 32.25), (19.75, 32.25)]),
    ("BTN_DOWN", SENAL, [(13.25, 45.75), (19.75, 45.75)]),
    ("BTN_LEFT", SENAL, [(4.25, 41.25), (10.75, 41.25)]),
    ("BTN_RIGHT", SENAL, [(22.25, 41.25), (28.75, 41.25)]),
    ("BTN_SELECT", SENAL, [(35.25, 64.25), (41.75, 64.25)]),
    ("BTN_START", SENAL, [(108.25, 59.75), (114.75, 59.75)]),
    ("BTN_B", SENAL, [(125.75, 41.25), (132.25, 41.25)]),
    ("BTN_A", SENAL, [(134.75, 36.75), (141.25, 36.75)]),
    # PWR_EN: de J2.17 directo a la izquierda hasta el comun de SW10 (y >= 8, lejos del borde superior)
    ("PWR_EN", SENAL, [(66.11, 9.54), (47.5, 9.54), (47.5, 8.0)]),
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
for ref, nombre, (x, y) in (("SW3", "UP", (16.5, 25.2)), ("SW1", "DOWN", (16.5, 53.0)), ("SW2", "LEFT", (7.5, 34.2)),
                            ("SW4", "RIGHT", (25.5, 34.2)), ("SW5", "SELECT", (38.5, 57.2)),
                            ("SW6", "START", (111.5, 57.2)), ("SW7", "B", (129, 49.2)), ("SW8", "A", (138, 40.0))):
    texto(nombre, x, y, F, tam=TXT_BOTON, grosor=SILK_BOTON)
for ref, (cx, cy) in CENTROS.items():
    ref_en(SW[ref], cx, cy)
# Frente: contorno del modulo de pantalla, imagen (48.96 x 36.72 centrada en x = 75) y pin 1 de J3
rect(*MOD, F)
rect(*IMAGEN, F)
texto("PANTALLA TFT 2.4\" (J3)", 50.0, 5.3, F)
texto("IMAGEN", EJE, 39.8, F)  # entre las dos filas del modulo (fuera de los pads de J1/J2)
texto("48.96 x 36.72", EJE, 41.8, F)
texto("1", X_J3, 6.3, F)
ref_en(J3, X_J3 + 2.19, 35.0, 90)
ref_en(C2, X_C2, 15.6)
ref_en(TP1, X_TP, 6.1)
ref_en(TP2, X_TP, 15.9)
texto("3V3", X_TP - 3.4, 8.49, F)
texto("GND", X_TP - 3.4, 13.49, F)
# Frente: DAC (el contorno del modulo y del jack vienen en la huella de J5), VIN/GND junto a J5, C3 y C4
texto("DAC PCM5102", 63.5, 58.0, F)
texto("JACK", EJE, 62.0, F)
texto("VIN", 56.1, Y_VIN, F)
texto("GND", 56.1, round(Y_VIN - 2.54, 2), F)
ref_en(J5, 63.5, 60.0)
ref_en(C3, 43.7, 60.1, 90)
ref_en(C4, 42.7, 68.9)
# Frente (F.Fab): linea del muro de la carcasa al centro de la franja pantalla-DAC
s = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
s.SetStart(mm(MURO[0], Y_MURO))
s.SetEnd(mm(MURO[2], Y_MURO))
s.SetLayer(pcbnew.F_Fab)
s.SetWidth(pcbnew.FromMM(0.1))
board.Add(s)
texto("muro carcasa (colgante, termina >= 4 mm sobre la PCB; ancho ~ 2 mm)", (MURO[0] + MURO[2]) / 2, Y_MURO - 0.8,
      pcbnew.F_Fab, tam=0.6, grosor=0.1)
# Frente: creditos, en la franja libre entre el DAC y START
for i, linea_txt in enumerate(("KIDBOX v0.9 2026", "basado en", "Game*Mite de", "Thomas Hugo", "Williams",
                               "(CC BY 4.0)")):
    texto(linea_txt, 93.5, 54.0 + i * 2.0, F)

# Detras: RP2350-Plus (placa x 64.5-85.5, y 0.55-51.55) con el USB-C, pin 1 de J1 y J2, BOOT/RESET.
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
# Detras: interruptor, referencia de la bateria y cajetin
ref_en(SW10, 47.5, 4.6)
# Posiciones de la palanca junto a su pad: OFF en el pad 2 (GND, x 50.04) y ON en el pad 3 (x 44.96).
# Visto desde atras (texto espejado) se lee OFF a la izquierda y ON a la derecha (medido: la palanca une el comun con la
# pata de su lado).
texto("OFF", 50.04, 11.3, B)
texto("ON", 44.96, 11.3, B)
# Bateria: va en la CARCASA (bolsillo con fondo de plastico), no pegada a la PCB. La zona es solo una referencia de donde
# queda, al lado derecho del RP2350-Plus; se permiten patas THT, pero no componentes altos de la cara Bottom.
rect(*BATERIA, B)
X_BAT = (BATERIA[0] + BATERIA[2]) / 2  # 105.75
texto("BATERÍA 103450", X_BAT, 33.0, B, tam=1.5, ang=90)
texto("va en la carcasa, no pegar a la PCB", X_BAT + 3.25, 33.0, B, ang=90)
# Lugar para el numero de pedido de JLCPCB ("Order number: Specify a location"): centrado en la zona de bateria
texto("JLCJLCJLCJLC", X_BAT - 3.25, 33.0, B, ang=90)
# Flecha hacia el conector BAT del modulo (extremo inferior del RP2350-Plus, junto a los pines 20/21)
Y_FLECHA = 54.0
linea((BATERIA[0] - 0.6, Y_FLECHA), (EJE + 5.5, Y_FLECHA), B)
linea((EJE + 5.5, Y_FLECHA), (EJE + 6.7, Y_FLECHA - 0.7), B)
linea((EJE + 5.5, Y_FLECHA), (EJE + 6.7, Y_FLECHA + 0.7), B)
texto("BAT", EJE + 9.0, Y_FLECHA + 1.6, B)
texto("KIDBOX v0.9 - 26-oct-2026", 130.0, 66.0, B)
texto("150 x 70 mm - 1.6 mm - 2 capas", 130.0, 68.0, B)

# ---------------------------------------------------------------- comprobaciones de la v0.9
avisos = []
# Bateria en la carcasa: en su zona se permiten patas THT, pero ninguna pieza de la cara Bottom (salvo el propio
# RP2350-Plus, J1/J2, que queda al lado) puede tener el cuerpo dentro.
for fp in board.GetFootprints():
    if not fp.IsFlipped() or fp.GetReference() in ("J1", "J2"):
        continue
    cy = fp.GetCourtyard(pcbnew.B_CrtYd).BBox()
    x1, y1 = pcbnew.ToMM(cy.GetLeft()), pcbnew.ToMM(cy.GetTop())
    x2, y2 = pcbnew.ToMM(cy.GetRight()), pcbnew.ToMM(cy.GetBottom())
    if x1 < BATERIA[2] and x2 > BATERIA[0] and y1 < BATERIA[3] and y2 > BATERIA[1]:
        sys.exit(f"{fp.GetReference()} (cara Bottom) dentro de la zona de bateria: ahi no van componentes altos")

# Nada bajo el DAC (seccion 6): ningun agujero dentro del contorno del modulo salvo los de J5
for fp in board.GetFootprints():
    for p in fp.Pads():
        (x, y) = xy(p.GetPosition())
        r = pcbnew.ToMM(p.GetSize(pcbnew.F_Cu).x) / 2
        if fp.GetReference() != "J5" and DAC[0] - r < x < DAC[2] + r and DAC[1] - r < y < DAC[3] + r:
            sys.exit(f"{fp.GetReference()} pad {p.GetNumber()} ({x:.2f}, {y:.2f}) bajo el contorno del DAC")

# Franja del muro: >= 4.5 mm y ninguna pieza de la cara Top con patas dentro (las soldaduras de J1/J2, cara Bottom,
# quedan bajo el muro colgante, que termina >= 4 mm sobre la PCB)
if MURO[3] - MURO[1] < 4.5:
    sys.exit(f"franja del muro de {MURO[3] - MURO[1]:.2f} mm (minimo 4.5)")
for fp in board.GetFootprints():
    if fp.IsFlipped():
        continue
    for p in fp.Pads():
        (x, y) = xy(p.GetPosition())
        r = pcbnew.ToMM(p.GetSize(pcbnew.F_Cu).x) / 2
        if MOD[0] - r < x < MOD[2] + r and MURO[1] - r < y < MURO[3] + r and fp.GetReference() != "J5":
            sys.exit(f"{fp.GetReference()} pad {p.GetNumber()} ({x:.2f}, {y:.2f}) en la franja del muro")


def dist_rect(p, r):
    return math.hypot(max(r[0] - p[0], 0, p[0] - r[2]), max(r[1] - p[1], 0, p[1] - r[3]))


# Capuchones redondos D9: >= 1.5 mm de aire al contorno de la pantalla y del DAC; simetria respecto de x = 75
for ref, (cx, cy) in CENTROS.items():
    for nombre_mod, caja in (("pantalla", MOD), ("DAC", DAC)):
        aire = dist_rect((cx, cy), caja) - R_CAP
        if aire < 1.5:
            sys.exit(f"capuchon de {ref} a {aire:.2f} mm del {nombre_mod} (minimo 1.5)")
if abs((16.5 + 133.5) / 2 - EJE) > 1e-9 or abs((CENTROS["SW5"][0] + CENTROS["SW6"][0]) / 2 - EJE) > 1e-9:
    sys.exit("los controles no quedan simetricos respecto de x = 75")
if abs((IMAGEN[0] + IMAGEN[2]) / 2 - EJE) > 1e-9 or abs((JACK[0] + JACK[2]) / 2 - EJE) > 1e-9:
    sys.exit("la imagen o el jack no quedan centrados en x = 75")

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
