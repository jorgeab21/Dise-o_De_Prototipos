# Genera layout_propuesto.svg (KIDBOX, espec. v0.5) a escala 1 unidad = 1 mm.
# v0.4: USB-C de la RP2350-Plus hacia el borde SUPERIOR (como un control de PlayStation),
#       pantalla girada 180° (J3 a la derecha), DAC a la izquierda con el jack hacia el borde INFERIOR.
# v0.6: solo separadores H5/H6 (lado J4) y bateria en y 12.5-42.5.
# v0.5: cruceta 2 mm a la izquierda, SW10 recto en la cara posterior, bateria detras de la pantalla, separadores de pantalla.
# Uso: python gen_layout.py <salida.svg>
import sys

out = []
def a(s): out.append(s)

W, H = 150, 65
HOLES = [(4, 4), (146, 4), (4, 61), (146, 61)]
BTNS = [("SW3", "UP", 18, 20), ("SW1", "DOWN", 18, 40), ("SW2", "LEFT", 8, 30), ("SW4", "RIGHT", 28, 30),
        ("SW8", "A", 138, 25), ("SW7", "B", 126, 35), ("SW5", "SELECT", 66, 58), ("SW6", "START", 84, 58),
        ("SW9", "RESET", 140, 54)]
PEND = "#e65100"   # supuesto / pendiente
PAD = "#f9a825"

def board():
    a(f'<rect x="0" y="0" width="{W}" height="{H}" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="0.5"/>')
    for x, y in HOLES:
        a(f'<circle cx="{x}" cy="{y}" r="2.6" fill="none" stroke="#9e9e9e" stroke-width="0.2" stroke-dasharray="0.6 0.4"/>')
        a(f'<circle cx="{x}" cy="{y}" r="1.1" fill="#fff" stroke="#424242" stroke-width="0.25"/>')

def pad(x, y, sq=False, r=0.8, color=PAD):
    if sq:
        a(f'<rect x="{x-r}" y="{y-r}" width="{2*r}" height="{2*r}" fill="{color}" stroke="#6d4c00" stroke-width="0.15"/>')
    else:
        a(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" stroke="#6d4c00" stroke-width="0.15"/>')

def text(x, y, s, size=2.0, anchor="middle", color="#212121", weight="normal", rot=None):
    t = f' transform="rotate({rot} {x} {y})"' if rot is not None else ""
    a(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{color}" font-weight="{weight}"{t}>{s}</text>')

def button(ref, lab, x, y, ghost=False):
    if ghost:
        a(f'<rect x="{x-3}" y="{y-3}" width="6" height="6" fill="none" stroke="#90a4ae" stroke-width="0.2" stroke-dasharray="0.5 0.4"/>')
        for dx in (-3.25, 3.25):
            for dy in (-2.25, 2.25):
                a(f'<circle cx="{x+dx}" cy="{y+dy}" r="0.6" fill="#cfd8dc"/>')
        return
    a(f'<rect x="{x-3}" y="{y-3}" width="6" height="6" fill="#eceff1" stroke="#455a64" stroke-width="0.25"/>')
    a(f'<circle cx="{x}" cy="{y}" r="1.75" fill="#90a4ae"/>')
    for dx in (-3.25, 3.25):
        for dy in (-2.25, 2.25):
            pad(x + dx, y + dy, r=0.6)
    text(x, y + 6.4, lab, 1.9, weight="bold")
    text(x, y - 3.6, ref, 1.3, color="#616161")

def cap(ref, x, y, label_dy=3):
    a(f'<rect x="{x-2.2}" y="{y-1}" width="4.4" height="2" rx="1" fill="#ffe082" stroke="#795548" stroke-width="0.15"/>')
    pad(x - 1.25, y, r=0.55); pad(x + 1.25, y, r=0.55)
    text(x, y + label_dy, ref, 1.3, color="#5d4037")

def dim_h(x1, x2, y, label):
    a(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#616161" stroke-width="0.2" marker-start="url(#ar)" marker-end="url(#ar)"/>')
    text((x1 + x2) / 2, y - 0.8, label, 2.0, color="#424242")

def dim_v(x, y1, y2, label):
    a(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#616161" stroke-width="0.2" marker-start="url(#ar)" marker-end="url(#ar)"/>')
    text(x - 0.9, (y1 + y2) / 2, label, 2.0, color="#424242", rot=-90)

VBW, VBH = 178, 234
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VBW} {VBH}" width="{VBW*6}" height="{VBH*6}" font-family="Arial, Helvetica, sans-serif">')
a('<defs><marker id="ar" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
  '<path d="M0,0 L6,3 L0,6 z" fill="#616161"/></marker></defs>')
a(f'<rect width="{VBW}" height="{VBH}" fill="#ffffff"/>')
text(VBW / 2, 7, "KIDBOX — layout propuesto · espec. v0.6 (supuesto, escala 1:1 en mm)", 3.6, weight="bold")
text(VBW / 2, 11.2, "Base Game★Mite · RP2350-Plus · TFT ILI9341 2.4\" (sin SD ni táctil) · DAC PCM5102A · 9 pulsadores 6×6 · todo THT, 2 capas", 2.0, color="#424242")

# ---------- Vista 1: cara frontal ----------
OX, OY = 16, 24
text(OX, OY - 6.5, "1 · CARA FRONTAL (Top) — lo que ve el niño", 2.8, anchor="start", weight="bold", color="#1b5e20")
a(f'<g transform="translate({OX},{OY})">')
dim_h(0, W, -2.2, "150 mm")
dim_v(-2.6, 0, H, "65 mm")
board()
# modulo de pantalla (girado 180°: J3 a la derecha)
a('<rect x="36" y="6.5" width="78" height="43" rx="1" fill="#ffcdd2" stroke="#c62828" stroke-width="0.35"/>')
a('<rect x="48.5" y="9.65" width="49" height="36.7" fill="#263238"/>')
text(73, 25.5, "PANTALLA ILI9341 2.4\"", 2.6, color="#ffffff", weight="bold")
text(73, 29, "320 × 240 · área activa ≈ 49 × 37 mm", 1.8, color="#eceff1")
text(73, 32.2, "montada girada 180° (setRotation)", 1.6, color="#cfd8dc")
# J3 1x14 a la derecha (pin 1 = VCC abajo, por verificar)
for i in range(14):
    pad(111.5, 11.49 + i * 2.54, sq=(i == 13))
text(109.6, 14, "J3 1×14", 1.5, anchor="end", color="#b71c1c", weight="bold")
text(112.9, 45, "1", 1.2, anchor="start", color="#b71c1c")
# J4 1x4 apoyo a la izquierda
for i in range(4):
    pad(38.5, 24.19 + i * 2.54, color="#ffe0b2")
a(f'<rect x="37.2" y="22.6" width="2.6" height="10.8" fill="none" stroke="{PEND}" stroke-width="0.25" stroke-dasharray="0.6 0.4"/>')
text(40.6, 36.2, "J4 1×4", 1.4, anchor="start", color=PEND, weight="bold")
text(40.6, 38, "solo apoyo", 1.2, anchor="start", color=PEND)
text(40.6, 39.6, "(por medir)", 1.2, anchor="start", color=PEND)
# capuchones 3D (punteado)
a('<polygon points="13.5,14.5 22.5,14.5 22.5,25.5 33,25.5 33,34.5 22.5,34.5 22.5,45.5 13.5,45.5 13.5,34.5 3,34.5 3,25.5 13.5,25.5" '
  'fill="none" stroke="#6a1b9a" stroke-width="0.3" stroke-dasharray="1 0.6"/>')
for (x, y) in [(138, 25), (126, 35)]:
    a(f'<circle cx="{x}" cy="{y}" r="5" fill="none" stroke="#6a1b9a" stroke-width="0.3" stroke-dasharray="1 0.6"/>')
for (x, y) in [(66, 58), (84, 58)]:
    a(f'<rect x="{x-5.5}" y="{y-2.8}" width="11" height="5.6" rx="2.8" fill="none" stroke="#6a1b9a" stroke-width="0.3" stroke-dasharray="1 0.6"/>')
for b in BTNS:
    button(*b)
cap("C2", 112, 54)
cap("C1", 130, 50)
# SW10 va en la cara posterior: aqui solo se ven sus 3 soldaduras
for dx in (-2, 0, 2):
    pad(125 + dx, 8, r=0.45, color="#ffe0b2")
text(129, 8.5, "SW10 ON/OFF por detrás", 1.3, anchor="start", color="#546e7a")
# separadores de la pantalla (H5-H8), posicion por medir
for (hx, hy) in [(41.4, 9.6), (41.4, 46.4)]:
    a(f'<circle cx="{hx}" cy="{hy}" r="1.6" fill="#fff" stroke="{PEND}" stroke-width="0.3" stroke-dasharray="0.6 0.4"/>')
text(75, 48.4, "módulo 78 × 43 mm · H5/H6 = separadores M3 de la pantalla (lado de J4)", 1.3, color=PEND)
# marcas de salidas por la cara posterior
text(75, 4.3, "▲ USB-C sale por arriba (cara posterior)", 1.3, color="#546e7a")
text(48.5, 63.6, "▼ jack de audífonos (cara posterior)", 1.3, color="#546e7a")
text(118, 63.2, "KIDBOX v1.0 · basado en Game★Mite (CC BY 4.0)", 1.4, anchor="middle", color="#2e7d32")
a('</g>')

# ---------- Vista 2: cara posterior (vista a traves desde el frente) ----------
OX2, OY2 = 16, 108
text(OX2, OY2 - 9, "2 · CARA POSTERIOR (Bottom) — dibujada \"a través\" desde el frente, como en KiCad", 2.8, anchor="start", weight="bold", color="#1b5e20")
text(OX2, OY2 - 5.6, "Vista real desde atrás = espejo izquierda↔derecha. Los botones y la pantalla del frente aparecen en gris como referencia.", 1.7, anchor="start", color="#616161")
text(OX2 + 75, OY2 - 1.3, "▼ USB-C: cargar y programar por el borde superior (se puede jugar mientras carga)", 1.6, color="#263238")
a(f'<g transform="translate({OX2},{OY2})">')
board()
a('<rect x="36" y="6.5" width="78" height="43" rx="1" fill="none" stroke="#e57373" stroke-width="0.25" stroke-dasharray="0.8 0.6"/>')
for b in BTNS:
    button(*b, ghost=True)
# bateria (en la carcasa), lado derecho
a(f'<rect x="88" y="12.5" width="20" height="30" rx="2" fill="#fff3e0" stroke="{PEND}" stroke-width="0.3" stroke-dasharray="1 0.6"/>')
text(98, 23.5, "BATERÍA", 1.7, weight="bold", color="#bf360c")
text(98, 25.9, "LiPo 902030", 1.4, weight="bold", color="#bf360c")
text(98, 28.3, "500 mAh", 1.3, color="#bf360c")
text(98, 30.5, "20 × 30 × 9 mm", 1.3, color="#bf360c")
text(98, 34.0, "zona sin patas", 1.2, color="#bf360c")
text(98, 35.7, "ni componentes;", 1.2, color="#bf360c")
text(98, 37.4, "vías tapadas", 1.2, color="#bf360c")
text(98, 40.1, "bolsillo en la carcasa", 1.1, color="#bf360c")
a(f'<path d="M88 40 C 87 44, 87 48, 86 50" fill="none" stroke="{PEND}" stroke-width="0.3" stroke-dasharray="0.6 0.4"/>')
text(98, 46.5, "cable al conector MX1.25 (abajo del módulo)", 1.1, color=PEND)
# SW10 recto en la cara posterior
a('<rect x="120.7" y="5.8" width="8.6" height="4.4" rx="0.4" fill="#b0bec5" stroke="#37474f" stroke-width="0.25"/>')
a('<rect x="123.6" y="6.8" width="2.8" height="2.4" fill="#546e7a"/>')
for dx in (-2, 0, 2):
    pad(125 + dx, 8, r=0.45)
text(125, 12.8, "SW10 ON/OFF", 1.5, weight="bold")
text(125, 14.6, "recto · palanca hacia atrás", 1.2, color="#37474f")
text(125, 16.2, "(rebaje en la carcasa)", 1.2, color=PEND)
# U1 RP2350-Plus girada 180°: USB arriba, pin 1 arriba a la derecha
a('<rect x="64.5" y="2.5" width="21" height="51" rx="1.2" fill="#d1c4e9" stroke="#4527a0" stroke-width="0.35"/>')
a('<rect x="71" y="0.2" width="8" height="4.6" rx="1" fill="#78909c" stroke="#263238" stroke-width="0.2"/>')
text(75, 3.3, "USB-C", 1.3, color="#ffffff", weight="bold")
text(63.3, 28, "U1 RP2350-Plus (J1 + J2) · 21 × 51 mm", 1.5, weight="bold", color="#311b92", rot=-90)
text(88, 4.4, "pin 1 = GP0 (CS)", 1.3, anchor="start", color=PEND, weight="bold")
text(88, 6.1, "[VERIFICAR con foto]", 1.1, anchor="start", color=PEND)
RL = {2: "GP1 RST", 4: "GP2 DC", 5: "GP3 MOSI", 9: "GP6 SCK", 16: "GP12 SEL", 17: "GP13 START", 19: "GP14 B", 20: "GP15 A"}
LL = {21: "GP16 DOWN", 22: "GP17 LEFT", 24: "GP18 UP", 25: "GP19 RIGHT", 26: "GP20 BCK", 27: "GP21 LCK", 29: "GP22 DIN",
      30: "RUN", 31: "GP26 LED", 36: "3V3", 37: "3V3_EN"}
for n in range(1, 21):          # columna derecha: pin 1 arriba
    y = 3.87 + (n - 1) * 2.54
    pad(83.89, y, sq=(n == 1), r=0.75)
    if n in RL:
        text(82.7, y + 0.45, RL[n], 1.2, anchor="end", color="#311b92")
for n in range(21, 41):         # columna izquierda: pin 21 abajo, pin 40 arriba
    y = 52.13 - (n - 21) * 2.54
    pad(66.11, y, r=0.75)
    if n in LL:
        text(67.3, y + 0.45, LL[n], 1.2, anchor="start", color="#311b92")
# J5 DAC a la izquierda, jack hacia el borde inferior
a('<rect x="36" y="33" width="25" height="31" rx="1" fill="#e1bee7" stroke="#6a1b9a" stroke-width="0.35"/>')
a(f'<rect x="36" y="33" width="25" height="31" rx="1" fill="none" stroke="{PEND}" stroke-width="0.25" stroke-dasharray="0.8 0.6"/>')
for i, nm in enumerate(["VIN", "GND", "LCK", "DIN", "BCK", "SCK"]):
    x = 42.15 + i * 2.54
    pad(x, 36, sq=(i == 0), r=0.75)
    text(x, 38.6, nm, 0.95, color="#4a148c")
text(48.5, 44.5, "J5 · DAC PCM5102A", 1.7, weight="bold", color="#4a148c")
text(48.5, 47, "medidas ≈ 25 × 31 [SUPUESTO]", 1.3, color=PEND)
text(48.5, 49.2, "SCK→GND · soldar 4 puentes", 1.2, color="#4a148c")
a('<rect x="44.5" y="58.5" width="8" height="6.5" fill="#424242"/>')
text(48.5, 62.3, "JACK", 1.4, color="#ffffff", weight="bold")
text(48.5, 64.3, "3,5 mm", 1.0, color="#ffffff")
# C3, C4 junto al DAC
a('<rect x="39.8" y="27" width="4.4" height="2" rx="1" fill="#ffe082" stroke="#795548" stroke-width="0.15"/>')
pad(40.75, 28, r=0.55); pad(43.25, 28, r=0.55)
text(42, 25.8, "C3 100n", 1.2, color="#5d4037")
a('<circle cx="54" cy="28" r="2.5" fill="#bbdefb" stroke="#0d47a1" stroke-width="0.2"/>')
pad(53, 28, sq=True, r=0.5); pad(55, 28, r=0.5)
text(54, 24.6, "C4 10µ", 1.2, color="#0d47a1")
a('</g>')
text(OX2 + 48.5, OY2 + H + 3.4, "▲ jack de audífonos por el borde inferior", 1.6, color="#263238")

# ---------- Leyenda y notas ----------
LY = 184
text(16, LY, "Leyenda", 2.4, anchor="start", weight="bold")
items = [("pad", "Pad THT (cuadrado = pin 1)"), ("btn", "Pulsador 6×6 del DEC"), ("cap", "Capuchón impreso en 3D"),
         ("pend", "Supuesto / por medir")]
x = 16
for kind, lab in items:
    if kind == "pad":
        a(f'<circle cx="{x+1.5}" cy="{LY+4}" r="0.9" fill="{PAD}" stroke="#6d4c00" stroke-width="0.15"/>')
    elif kind == "btn":
        a(f'<rect x="{x}" y="{LY+2.5}" width="3" height="3" fill="#eceff1" stroke="#455a64" stroke-width="0.25"/>')
    elif kind == "cap":
        a(f'<circle cx="{x+1.5}" cy="{LY+4}" r="1.5" fill="none" stroke="#6a1b9a" stroke-width="0.3" stroke-dasharray="0.8 0.5"/>')
    else:
        a(f'<rect x="{x}" y="{LY+2.5}" width="3" height="3" fill="none" stroke="{PEND}" stroke-width="0.3" stroke-dasharray="0.6 0.4"/>')
    text(x + 4.2, LY + 4.6, lab, 1.7, anchor="start")
    x += 40
notes = [
    "• Todas las posiciones son [SUPUESTO] (espec. sección 6). Se confirman con las piezas el 14 y 15 de octubre y con un boceto 1:1 antes de la Fase 2.",
    "• USB-C por arriba, como un control de PlayStation: el cable no molesta las manos y se puede jugar cargando. Jack de audífonos por abajo.",
    "• Cruceta (paso 10 mm, centro x = 18, capuchón a 3 mm de la pantalla) y A/B en diagonal, para capuchones 3D cómodos a los 6–10 años.",
    "• Ningún botón ni capuchón queda bajo la pantalla. La RP2350-Plus termina en y = 53,5, así que Select/Start van centrados sin chocar.",
    "• Ruteo: pantalla (GP0–GP6) del lado de J3, I2S (GP20–GP22) junto al DAC y cruceta reasignada a GP16–GP19, del lado de la cruceta.",
    "• ON/OFF recto por detrás (no se apaga sin querer). Batería detrás de la pantalla, en una zona sin patas: no hace falta espuma.",
    "• Pantalla montada girada 180° para acercar J3 a sus pines: la imagen se endereza en el firmware con setRotation().",
]
for i, n in enumerate(notes):
    text(16, LY + 11 + i * 3.6, n, 1.75, anchor="start", color="#37474f")
a('</svg>')

with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("ok", sys.argv[1])
