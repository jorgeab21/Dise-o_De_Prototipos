# Genera KIDBOX/KIDBOX.kicad_sch (KiCad 10) a partir de scripts/kidbox_datos.py.
# Copia cada simbolo completo desde las librerias oficiales de KiCad 10 al bloque lib_symbols (no inventa geometria),
# coloca los simbolos, une cada pin a su red con un tramo de cable y una etiqueta (o un simbolo GND/+3V3),
# marca los pines sin uso con no_connect y anota junto a cada pin su funcion en el modulo (GP0, VCC...).
# Los UUID son deterministas (uuid5): re-ejecutarlo da el mismo archivo y no rompe la paridad con el PCB.
#
# Uso (Python 3.8+ del sistema, sin dependencias), desde hardware/:
#     python scripts/gen_esquematico.py
import math
import os
import re
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kidbox_datos import COMPONENTES, PROYECTO  # noqa: E402

LIBS = os.environ.get("KICAD10_SYMBOL_DIR", r"C:\Program Files\KiCad\10.0\share\kicad\symbols")
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", PROYECTO, PROYECTO + ".kicad_sch")
NS = uuid.UUID("6b1d0c52-6a1e-4f43-9a8e-4b49d0f2a001")


def uid(clave):
    return str(uuid.uuid5(NS, clave))


ROOT = uid("raiz")


# ---------------------------------------------------------------- librerias oficiales
def bloque(texto, inicio):
    """Devuelve el bloque S-expression que empieza en texto[inicio] == '('."""
    d = 0
    for j in range(inicio, len(texto)):
        if texto[j] == "(":
            d += 1
        elif texto[j] == ")":
            d -= 1
            if d == 0:
                return texto[inicio:j + 1]
    raise ValueError("parentesis sin cerrar")


_cache = {}


def simbolo_lib(lib_id):
    if lib_id in _cache:
        return _cache[lib_id]
    lib, nombre = lib_id.split(":")
    with open(os.path.join(LIBS, lib + ".kicad_sym"), encoding="utf-8") as f:
        texto = f.read()
    i = texto.index(f'\t(symbol "{nombre}"\n') + 1
    b = bloque(texto, i)
    if "(extends" in b:
        raise SystemExit(f"{lib_id} es un simbolo derivado (extends); no soportado")
    pines = [dict(x=float(x), y=float(y), ang=float(a), num=n) for x, y, a, n in re.findall(
        r'\(pin \w+ \w+\s*\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)\s*\(length [-\d.]+\).*?\(number "([^"]+)"', b, re.S)]
    # los simbolos de libreria solo tienen propiedades en su nivel superior
    props = {m.group(1): bloque(b, m.start()) for m in re.finditer(r'\(property "([^"]+)" ', b)}
    flags = {k: v for k, v in re.findall(r"^\t\t\((exclude_from_sim|in_bom|on_board|in_pos_files) (\w+)\)", b, re.M)}
    texto_lib = b.replace(f'(symbol "{nombre}"', f'(symbol "{lib_id}"', 1)
    _cache[lib_id] = dict(texto=texto_lib, pines=pines, props=props, flags=flags)
    return _cache[lib_id]


def valor_prop(bloque_prop):
    return re.match(r'\(property "[^"]+" "((?:[^"\\]|\\.)*)"', bloque_prop).group(1)


# ---------------------------------------------------------------- geometria
def r4(v):
    return round(v + 0.0, 4)


def rot(x, y, ang):
    a = math.radians(ang)
    return x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)


def extremo_pin(sx, sy, srot, pin):
    """Punto de conexion del pin en coordenadas del esquematico y direccion hacia fuera del simbolo."""
    X, Y = rot(pin["x"], pin["y"], srot)
    a = math.radians(pin["ang"] + srot)
    return (r4(sx + X), r4(sy - Y)), (round(-math.cos(a)), round(math.sin(a)))


# ---------------------------------------------------------------- emisores
items = []
n_pwr = {"#PWR": 0, "#FLG": 0}


def fmt(v):
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def prop_instancia(bloque_prop, valor, sx, sy, srot, clave):
    m = re.search(r"\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)", bloque_prop)
    px, py, pa = map(float, m.groups())
    X, Y = rot(px, py, srot)
    nuevo = bloque_prop.replace(m.group(0), f"(at {fmt(sx + X)} {fmt(sy - Y)} {fmt(pa)})", 1)
    nuevo = re.sub(r'^\(property "([^"]+)" "(?:[^"\\]|\\.)*"', lambda mm: f'(property "{mm.group(1)}" "{esc(valor)}"',
                   nuevo, count=1)
    return nuevo


def simbolo(ref, lib_id, sx, sy, srot=0, valor=None, huella=None, clave=None, pos_valor=None, flags=None):
    s = simbolo_lib(lib_id)
    banderas = dict(s["flags"], **(flags or {}))  # atributos del simbolo; `flags` los cambia por instancia
    clave = clave or ref
    vals = {k: valor_prop(v) for k, v in s["props"].items()}
    vals["Reference"] = ref
    if valor is not None:
        vals["Value"] = valor
    if huella is not None:
        vals["Footprint"] = huella
    out = [f'\t(symbol\n\t\t(lib_id "{lib_id}")\n\t\t(at {fmt(sx)} {fmt(sy)} {fmt(srot)})\n\t\t(unit 1)\n\t\t(body_style 1)']
    for k in ("exclude_from_sim", "in_bom", "on_board", "in_pos_files"):
        out.append(f"\t\t({k} {banderas.get(k, 'yes' if k != 'exclude_from_sim' else 'no')})")
    out.append(f'\t\t(dnp no)\n\t\t(uuid "{uid("sym/" + clave)}")')
    for k in ("Reference", "Value", "Footprint", "Datasheet", "Description"):
        if k in s["props"]:
            pb = prop_instancia(s["props"][k], vals[k], sx, sy, srot, clave)
            if k == "Value" and pos_valor:  # texto horizontal en la fila del pin (simbolo girado)
                pb = re.sub(r"\(at [-\d.]+ [-\d.]+ [-\d.]+\)", "(at {} {} {})".format(*map(fmt, pos_valor)), pb,
                            count=1)
            out.append("\t\t" + pb.replace("\n", "\n\t"))
    for p in s["pines"]:
        out.append(f'\t\t(pin "{p["num"]}"\n\t\t\t(uuid "{uid("pin/" + clave + "/" + p["num"])}")\n\t\t)')
    out.append(f'\t\t(instances\n\t\t\t(project "{PROYECTO}"\n\t\t\t\t(path "/{ROOT}"\n\t\t\t\t\t(reference "{ref}")'
               f'\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)')
    items.append("\n".join(out))
    return {p["num"]: extremo_pin(sx, sy, srot, p) for p in s["pines"]}


def cable(a, b, clave):
    items.append(f'\t(wire\n\t\t(pts\n\t\t\t(xy {fmt(a[0])} {fmt(a[1])}) (xy {fmt(b[0])} {fmt(b[1])})\n\t\t)\n'
                 f'\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type default)\n\t\t)\n\t\t(uuid "{uid("wire/" + clave)}")\n\t)')


def etiqueta(nombre, p, d, clave):
    ang, just = {(-1, 0): (180, "right bottom"), (1, 0): (0, "left bottom"),
                 (0, -1): (90, "left bottom"), (0, 1): (270, "right bottom")}[d]
    items.append(f'\t(label "{nombre}"\n\t\t(at {fmt(p[0])} {fmt(p[1])} {ang})\n\t\t(effects\n\t\t\t(font\n'
                 f'\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify {just})\n\t\t)\n\t\t(uuid "{uid("label/" + clave)}")\n\t)')


def texto(t, x, y, clave, tam=1.27, just="left bottom", negrita=False):
    b = "\n\t\t\t\t(bold yes)" if negrita else ""
    items.append(f'\t(text "{esc(t)}"\n\t\t(exclude_from_sim no)\n\t\t(at {fmt(x)} {fmt(y)} 0)\n\t\t(effects\n\t\t\t(font\n'
                 f'\t\t\t\t(size {tam} {tam}){b}\n\t\t\t)\n\t\t\t(justify {just})\n\t\t)\n\t\t(uuid "{uid("text/" + clave)}")\n\t)')


def no_conectar(p, clave):
    items.append(f'\t(no_connect\n\t\t(at {fmt(p[0])} {fmt(p[1])})\n\t\t(uuid "{uid("nc/" + clave)}")\n\t)')


def alimentacion(red, p, d, clave):
    """Simbolo GND o +3V3 en p, con el cuerpo apuntando en la direccion d (hacia fuera del cable)."""
    pref = "#PWR"
    n_pwr[pref] += 1
    lib = "power:GND" if red == "GND" else "power:+3V3"
    # GND dibuja su cuerpo hacia abajo (0,1) con rot 0; +3V3 hacia arriba (0,-1).
    base = (0, 1) if red == "GND" else (0, -1)
    giros = {0: base, 90: (base[1], -base[0]), 180: (-base[0], -base[1]), 270: (-base[1], base[0])}
    srot = next(a for a, v in giros.items() if v == d)
    pos = None
    if srot in (90, 270):  # girado: el valor va horizontal, mas alla del simbolo, en la misma fila
        pos = (p[0] + d[0] * 6.35, p[1] - 0.635, 90)
    simbolo(f"{pref}{n_pwr[pref]:02d}", lib, p[0], p[1], srot, clave="pwr/" + clave, pos_valor=pos)


def conectar(ref, num, red, p, d, largo=5.08, codo=None):
    """Tramo de cable desde el pin hacia fuera y, al final, etiqueta o simbolo de alimentacion."""
    clave = f"{ref}.{num}"
    fin = (r4(p[0] + d[0] * largo), r4(p[1] + d[1] * largo))
    cable(p, fin, clave)
    if codo:  # segundo tramo (p. ej. bajar a GND)
        fin2 = (r4(fin[0] + codo[0] * 2.54), r4(fin[1] + codo[1] * 2.54))
        cable(fin, fin2, clave + "/codo")
        fin, d = fin2, codo
    if red in ("GND", "+3V3"):
        alimentacion(red, fin, d, clave)
    else:
        etiqueta(red, fin, d, clave)


def colocar(ref, x, y, largo=5.08, anotar=None, codo_gnd=None):
    c = COMPONENTES[ref]
    if anotar is None:
        anotar = c["lib"].startswith("Connector")
    pins = simbolo(ref, c["lib"], x, y, valor=c["valor"], huella=c["huella"], flags=c.get("flags"))
    if not c["pines"]:
        return pins
    for num, (p, d) in pins.items():
        funcion, red = c["pines"][int(num)]
        if red is None:
            no_conectar(p, f"{ref}.{num}")
        else:
            # en los conectores, GND/+3V3 con tramo corto: el simbolo no tapa las etiquetas de las filas vecinas
            l = 2.54 if c["lib"].startswith("Connector") and red in ("GND", "+3V3") else largo
            conectar(ref, num, red, p, d, l, codo=codo_gnd if red == "GND" else None)
        if anotar:  # funcion del pin del lado opuesto al cable (dentro del dibujo del conector)
            texto(f"{num}  {funcion}", x + 3.81, p[1] + 0.635, f"anot/{ref}.{num}", tam=1.27)
    return pins


# ---------------------------------------------------------------- hoja
texto("KIDBOX v0.9 — placa portadora (basada en Game*Mite v1.3.2, CC BY 4.0)", 25.4, 22.86, "titulo", 2.54,
      negrita=True)
texto("Generado con scripts/gen_esquematico.py desde scripts/kidbox_datos.py (ESPECIFICACION.md v0.9; los scripts van en la "
      "entrega). Para cambiarlo: editar los datos y regenerar (ver README).", 25.4, 27.94, "subtitulo", 1.524)

# Bloque 1: RP2350-Plus sobre J1 + J2 (cara posterior)
texto("U1 · Waveshare RP2350-Plus (cara Bottom) sobre J1 + J2", 45.72, 55.88, "t_mod", 1.778, negrita=True)
texto("Columna: pin del conector · pin del modulo · nombre en el modulo", 45.72, 60.96, "t_mod2", 1.27)
colocar("J1", 76.2, 91.44, largo=10.16, anotar=False)
colocar("J2", 152.4, 91.44, largo=10.16, anotar=False)
from kidbox_datos import MODULO  # noqa: E402
for base, x in ((1, 76.2), (21, 152.4)):
    for n in range(20):
        y = 91.44 - 22.86 + n * 2.54
        texto(f"{n + 1}  ·  {base + n}  {MODULO[base + n][0]}", x + 3.81, y + 0.635, f"anot/mod{base + n}")

# Bloque 2: pantalla y DAC
texto("Pantalla TFT ILI9341 2.4\" (MSP2402), cara Top", 213.36, 55.88, "t_tft", 1.778, negrita=True)
texto("Pin LED: transistor S8050 + 1 kΩ en el modulo (≈2,6 mA): directo a GP26", 213.36, 60.96, "t_tft2", 1.27)
colocar("J3", 233.68, 86.36)
colocar("C2", 264.16, 81.28)
texto("C2 junto a J3", 259.08, 99.06, "t_c2", 1.27)
colocar("TP1", 276.86, 73.66, anotar=False)
colocar("TP2", 287.02, 73.66, anotar=False)
texto("TP1 (+3V3) y TP2 (GND): puntos de prueba junto a C2", 259.08, 102.87, "t_tp", 1.27)

texto("DAC GY-PCM5102 (PCM5102A, I2S), cara Top", 299.72, 55.88, "t_dac", 1.778, negrita=True)
texto("Orden de pines de J5 confirmado con la serigrafía de la pieza (14-oct)", 299.72, 60.96, "t_dac2", 1.27)
colocar("J5", 320.04, 81.28)
texto("SCK a GND: el DAC usa su reloj interno", 299.72, 101.6, "t_dac3", 1.27)
colocar("C3", 350.52, 81.28)
colocar("C4", 365.76, 81.28)
texto("C3, C4 junto a VIN de J5", 345.44, 99.06, "t_c34", 1.27)
texto("VIN = 3V3 probado el 23-oct: VIN 3.26 V, A3V3 3.27 V; FLT/DEMP/FMT = L, XSMT = H", 299.72, 104.14, "t_dac4", 1.27)

# Banderas de alimentacion (J1/J2 son conectores pasivos: el ERC necesita saber de donde viene la energia)
texto("PWR_FLAG: el 3V3 lo genera el regulador de la RP2350-Plus", 299.72, 119.38, "t_flag", 1.27)
n_pwr["#FLG"] = 1
simbolo("#PWR90", "power:+3V3", 309.88, 127.0, clave="flag/3v3/pwr")
cable((309.88, 127.0), (309.88, 132.08), "flag/3v3")
simbolo("#FLG01", "power:PWR_FLAG", 309.88, 132.08, 180, clave="flag/3v3/flg")
simbolo("#FLG02", "power:PWR_FLAG", 330.2, 127.0, clave="flag/gnd/flg")
cable((330.2, 127.0), (330.2, 132.08), "flag/gnd")
simbolo("#PWR91", "power:GND", 330.2, 132.08, clave="flag/gnd/pwr")

# Bloque 3: botones
texto("Botones (pulsado = LOW, pull-up interno). Cruceta en GP16–GP19", 25.4, 160.02, "t_btn", 1.778, negrita=True)
for i, ref in enumerate(["SW3", "SW1", "SW2", "SW4", "SW5", "SW6", "SW7", "SW8"]):
    colocar(ref, 45.72 + i * 40.64, 175.26, anotar=False, codo_gnd=(0, 1))

# Bloque 4: reset, encendido y agujeros
texto("Encendido (3V3_EN). Sin reset propio: RUN sin conectar (BOOT/RESET del módulo)", 25.4, 203.2, "t_rst", 1.778,
      negrita=True)
colocar("SW10", 76.2, 220.98, anotar=False)
texto("SW10: común = pin 1 (pad central de la huella Würth) a 3V3_EN; OFF = pin 2 a GND; pin 3 al aire", 45.72, 236.22,
      "t_sw10", 1.27)
texto("3V3_EN tiene pull-up de 100 kΩ a VSYS en la RP2350-Plus", 45.72, 240.03, "t_sw10b", 1.27)

texto("Agujeros (sin conexión eléctrica)", 182.88, 203.2, "t_h", 1.778, negrita=True)
for i in range(1, 5):
    colocar(f"H{i}", 190.5 + (i - 1) * 20.32, 220.98)
texto("H1–H4: M2, fijación a la carcasa. La pantalla se sujeta con J3 y la carcasa (sin H5/H6)", 182.88, 236.22,
      "t_h2", 1.27)

texto("Batería (excluida de la placa)", 279.4, 203.2, "t_bt", 1.778, negrita=True)
colocar("BT1", 292.1, 220.98, anotar=False)
texto("BT1 va al conector BAT (PH1.25) del RP2350-Plus con el adaptador, no a esta PCB.", 279.4, 236.22, "t_bt2", 1.27)
texto("Medir la polaridad con multímetro antes de conectar (rojo = + -> ⊕ del BAT).", 279.4, 240.03, "t_bt3", 1.27)

# ---------------------------------------------------------------- archivo
libs = sorted({c["lib"] for c in COMPONENTES.values()} | {"power:GND", "power:+3V3", "power:PWR_FLAG"})
lib_txt = "\n".join("\t\t" + simbolo_lib(l)["texto"].replace("\n", "\n\t") for l in libs)
cab = (f'(kicad_sch\n\t(version 20260306)\n\t(generator "eeschema")\n\t(generator_version "10.0")\n\t(uuid "{ROOT}")\n'
       f'\t(paper "A3")\n\t(title_block\n\t\t(title "KIDBOX")\n\t\t(date "2026-10-26")\n\t\t(rev "v0.9")\n'
       f'\t\t(company "Equipo KIDBOX")\n\t\t(comment 1 "Basado en Game*Mite v1.3.2 de Thomas Hugo Williams (CC BY 4.0)")\n'
       f'\t\t(comment 2 "ESPECIFICACION.md v0.9")\n\t)\n\t(lib_symbols\n{lib_txt}\n\t)\n')
pie = '\t(sheet_instances\n\t\t(path "/"\n\t\t\t(page "1")\n\t\t)\n\t)\n\t(embedded_fonts no)\n)\n'
os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
with open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
    f.write(cab + "\n".join(items) + "\n" + pie)
print("ok", os.path.normpath(SALIDA), f"({len(items)} elementos)")
