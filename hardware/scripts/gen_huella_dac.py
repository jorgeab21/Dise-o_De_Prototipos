# Genera la huella propia del DAC GY-PCM5102 (v0.9) y la tabla de librerias del proyecto:
#   - KIDBOX/KIDBOX.pretty/GY-PCM5102_1x06_P2.54mm.kicad_mod
#   - KIDBOX/fp-lib-table   (libreria "Connector_KIDBOX" -> ${KIPRJMOD}/KIDBOX.pretty)
# La huella es la tira hembra 1x6 (mismos pads que la oficial PinSocket_1x06: 1.7 mm, taladro 1.0, pad 1 cuadrado)
# mas el contorno del modulo (31.85 x 17.5 mm) y del jack (4.7 x 14 mm, sobresale 1.4 mm del borde largo), medidos por el
# alumno. Asi el contorno se mueve junto con los pads y el DRC ve el courtyard del modulo completo.
# Geometria (vista desde el frente, origen = pad 1 = VIN, abajo): pads hacia arriba cada 2.54 mm (pad 6 = SCK arriba);
# columna a 1.5 mm del borde corto izquierdo y centrada en los 17.5 mm; eje del jack a 24.9 mm de la columna, a la derecha;
# boca del jack hacia abajo.
# El nombre de la libreria empieza por "Connector" para cumplir el filtro de huellas del simbolo Conn_01x06
# ("Connector*:*_1x??_*"); la carpeta se llama KIDBOX.pretty.
#
# Uso (Python 3.8+ del sistema), desde hardware/:
#     python scripts/gen_huella_dac.py
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.normpath(os.path.join(AQUI, "..", "KIDBOX"))
LIB = os.path.join(CARPETA, "KIDBOX.pretty")
NOMBRE = "GY-PCM5102_1x06_P2.54mm"

# Medidas del modulo (ESPECIFICACION.md v0.9, seccion 6), relativas al pad 1
L, A = 31.85, 17.5                     # largo (x) y ancho (y) de la placa del modulo
COL_BORDE = 1.5                        # centro de la columna -> borde corto izquierdo
PASO = 2.54
MARGEN_Y = (A - 5 * PASO) / 2          # columna centrada a lo ancho: 2.4 mm del pad extremo a cada borde largo
JACK_EJE, JACK_ANCHO, JACK_LARGO, JACK_SALE = 24.9, 4.7, 14.0, 1.4

X1, X2 = -COL_BORDE, -COL_BORDE + L               # -1.5 .. 30.35
Y2 = MARGEN_Y                                      # borde largo del lado de la boca (abajo): +2.4
Y1 = Y2 - A                                        # borde largo de arriba: -15.1
JX1, JX2 = JACK_EJE - JACK_ANCHO / 2, JACK_EJE + JACK_ANCHO / 2   # 22.55 .. 27.25
JY2 = Y2 + JACK_SALE                               # boca: +3.8
JY1 = JY2 - JACK_LARGO                             # -10.2
CY = 0.25                                          # margen del courtyard


def f(v):
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def linea(a, b, capa, ancho):
    return (f'\t(fp_line\n\t\t(start {f(a[0])} {f(a[1])})\n\t\t(end {f(b[0])} {f(b[1])})\n'
            f'\t\t(stroke\n\t\t\t(width {ancho})\n\t\t\t(type solid)\n\t\t)\n\t\t(layer "{capa}")\n\t)')


def poli(puntos, capa, ancho, cerrado=True):
    pares = list(zip(puntos, puntos[1:] + (puntos[:1] if cerrado else [])))
    return [linea(a, b, capa, ancho) for a, b in pares]


def texto(t, x, y, capa, ang=0, tam=1.0, prop=None, oculto=False):
    cab = f'\t(property "{prop}" "{t}"' if prop else f'\t(fp_text user "{t}"'
    h = "\n\t\t(hide yes)" if oculto else ""
    return (f'{cab}\n\t\t(at {f(x)} {f(y)} {f(ang)})\n\t\t(layer "{capa}"){h}\n\t\t(effects\n\t\t\t(font\n'
            f'\t\t\t\t(size {tam} {tam})\n\t\t\t\t(thickness {f(tam * 0.15)})\n\t\t\t)\n\t\t)\n\t)')


cuerpo = []
# Serigrafia: contorno del modulo, la parte del jack que queda sobre el modulo (lo que sobresale va solo en F.Fab,
# porque llega al borde de la placa) y una marca de pin 1 a la izquierda del pad cuadrado.
cuerpo += poli([(X1, Y1), (X2, Y1), (X2, Y2), (X1, Y2)], "F.SilkS", 0.12)
cuerpo += poli([(JX1, Y2), (JX1, JY1), (JX2, JY1), (JX2, Y2)], "F.SilkS", 0.12, cerrado=False)
cuerpo.append(linea((X1 - 0.6, -0.9), (X1 - 0.6, 0.9), "F.SilkS", 0.12))
# Fab: modulo y jack completos (con la boca)
cuerpo += poli([(X1, Y1), (X2, Y1), (X2, Y2), (X1, Y2)], "F.Fab", 0.1)
cuerpo += poli([(JX1, JY1), (JX2, JY1), (JX2, JY2), (JX1, JY2)], "F.Fab", 0.1)
# Courtyard: modulo + boca del jack, a 0.25 mm
cuerpo += poli([(X1 - CY, Y1 - CY), (X2 + CY, Y1 - CY), (X2 + CY, Y2 + CY), (JX2 + CY, Y2 + CY), (JX2 + CY, JY2 + CY),
                (JX1 - CY, JY2 + CY), (JX1 - CY, Y2 + CY), (X1 - CY, Y2 + CY)], "F.CrtYd", 0.05)
cuerpo.append(texto("${REFERENCE}", 12, Y1 + 2.0, "F.Fab"))
cuerpo.append(texto("JACK", JACK_EJE, JY1 + 2.0, "F.Fab", tam=0.8))
pads = []
for n in range(1, 7):
    forma = "rect" if n == 1 else "circle"
    pads.append(f'\t(pad "{n}" thru_hole {forma}\n\t\t(at 0 {f(-(n - 1) * PASO)})\n\t\t(size 1.7 1.7)\n\t\t(drill 1)\n'
                f'\t\t(layers "*.Cu" "*.Mask")\n\t\t(remove_unused_layers no)\n\t)')

mod = "\n".join([
    f'(footprint "{NOMBRE}"',
    "\t(version 20260206)",
    '\t(generator "pcbnew")',
    '\t(generator_version "10.0")',
    '\t(layer "F.Cu")',
    '\t(descr "Modulo DAC GY-PCM5102 (PCM5102A) sobre tira hembra 1x06 de 2.54 mm: contorno 31.85 x 17.5 mm y jack de '
    '3.5 mm (4.7 x 14 mm, sobresale 1.4 mm). Pad 1 = VIN. Generada por scripts/gen_huella_dac.py (proyecto KIDBOX)")',
    '\t(tags "GY-PCM5102 PCM5102A DAC I2S socket 1x06 2.54mm")',
    texto("REF**", 12, Y1 - 1.2, "F.SilkS", prop="Reference"),
    texto(NOMBRE, 12, Y2 + 1.4, "F.Fab", prop="Value"),
    texto("", 0, 0, "F.Fab", prop="Datasheet", oculto=True),
    texto("", 0, 0, "F.Fab", prop="Description", oculto=True),
    "\t(attr through_hole)",
    "\t(duplicate_pad_numbers_are_jumpers no)",
    *cuerpo,
    *pads,
    "\t(embedded_fonts no)",
    # modelo 3D de la tira hembra oficial, girado 180 grados (aqui los pines van hacia arriba)
    '\t(model "${KICAD10_3DMODEL_DIR}/Connector_PinSocket_2.54mm.3dshapes/PinSocket_1x06_P2.54mm_Vertical.step"\n'
    '\t\t(offset\n\t\t\t(xyz 0 0 0)\n\t\t)\n\t\t(scale\n\t\t\t(xyz 1 1 1)\n\t\t)\n\t\t(rotate\n\t\t\t(xyz 0 0 180)\n\t\t)\n\t)',
    ")",
]) + "\n"

os.makedirs(LIB, exist_ok=True)
with open(os.path.join(LIB, NOMBRE + ".kicad_mod"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(mod)
with open(os.path.join(CARPETA, "fp-lib-table"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write('(fp_lib_table\n\t(version 7)\n\t(lib (name "Connector_KIDBOX") (type "KiCad") (uri "${KIPRJMOD}/KIDBOX.pretty") '
             '(options "") (descr "Huellas propias del proyecto KIDBOX (scripts/gen_huella_dac.py)"))\n)\n')
print("ok", os.path.join(LIB, NOMBRE + ".kicad_mod"))
print(f"   modulo x {f(X1)}..{f(X2)}, y {f(Y1)}..{f(Y2)}; jack x {f(JX1)}..{f(JX2)}, y {f(JY1)}..{f(JY2)} (relativo al pad 1)")
print("ok", os.path.join(CARPETA, "fp-lib-table"))
