# Datos del proyecto KIDBOX (componentes, pines y redes) segun ESPECIFICACION.md v0.9, secciones 2 a 5.
# No se ejecuta solo: lo importan gen_esquematico.py y gen_bom_netlist.py, para que el esquematico,
# BOM.csv y netlist.csv salgan de una unica fuente. Si cambia la especificacion, se edita aqui y se regeneran.

PROYECTO = "KIDBOX"

FP_SOCKET = "Connector_PinSocket_2.54mm:PinSocket_1x{:02d}_P2.54mm_Vertical"
FP_PUSH = "Button_Switch_THT:SW_PUSH_6mm"
FP_C = "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm"  # paso 5 mm medido en los ceramicos reales (21-oct)
# Huella propia del DAC (v0.9): tira 1x06 + contorno del modulo y del jack; la genera scripts/gen_huella_dac.py en
# KIDBOX/KIDBOX.pretty. El nombre de la libreria empieza por "Connector" para cumplir el filtro de huellas del simbolo
# Conn_01x06 ("Connector*:*_1x??_*"); la carpeta es KIDBOX.pretty (ver KIDBOX/fp-lib-table).
FP_DAC = "Connector_KIDBOX:GY-PCM5102_1x06_P2.54mm"

# Pines de la RP2350-Plus (= Pico, confirmado con el pinout oficial de Waveshare).
# pin del modulo -> (nombre en el modulo, red o None = sin conectar)
# "GND" y "+3V3" son las redes globales de los simbolos de alimentacion.
MODULO = {
    1: ("GP0", "LCD_CS"), 2: ("GP1", "LCD_RST"), 3: ("GND", "GND"), 4: ("GP2", "LCD_DC"),
    5: ("GP3", "LCD_MOSI"), 6: ("GP4", None), 7: ("GP5", None), 8: ("GND", "GND"),
    9: ("GP6", "LCD_SCK"), 10: ("GP7", None), 11: ("GP8", None), 12: ("GP9", None),
    13: ("GND", "GND"), 14: ("GP10", None), 15: ("GP11", None), 16: ("GP12", "BTN_SELECT"),
    17: ("GP13", "BTN_START"), 18: ("GND", "GND"), 19: ("GP14", "BTN_B"), 20: ("GP15", "BTN_A"),
    21: ("GP16", "BTN_DOWN"), 22: ("GP17", "BTN_LEFT"), 23: ("GND", "GND"), 24: ("GP18", "BTN_UP"),
    25: ("GP19", "BTN_RIGHT"), 26: ("GP20", "I2S_BCK"), 27: ("GP21", "I2S_LRCK"), 28: ("GND", "GND"),
    29: ("GP22", "I2S_DIN"), 30: ("RUN", None), 31: ("GP26", "LCD_LED"), 32: ("GP27", None),
    33: ("AGND", "GND"), 34: ("GP28", None), 35: ("ADC_VREF", None), 36: ("3V3", "+3V3"),
    37: ("3V3_EN", "PWR_EN"), 38: ("GND", "GND"), 39: ("VSYS", None), 40: ("VBUS", None),
}

# Pantalla TFT ILI9341 2.4" (MSP2402): pin de J3 -> (funcion, red)
PANTALLA = {
    1: ("VCC", "+3V3"), 2: ("GND", "GND"), 3: ("CS", "LCD_CS"), 4: ("RESET", "LCD_RST"),
    5: ("DC", "LCD_DC"), 6: ("SDI(MOSI)", "LCD_MOSI"), 7: ("SCK", "LCD_SCK"), 8: ("LED", "LCD_LED"),
    9: ("SDO(MISO)", None), 10: ("T_CLK", None), 11: ("T_CS", None), 12: ("T_DIN", None),
    13: ("T_DO", None), 14: ("T_IRQ", None),
}
# DAC GY-PCM5102, orden confirmado con la serigrafia de la pieza (14-oct, espec. v0.7)
DAC = {1: ("VIN", "+3V3"), 2: ("GND", "GND"), 3: ("LCK", "I2S_LRCK"), 4: ("DIN", "I2S_DIN"),
       5: ("BCK", "I2S_BCK"), 6: ("SCK", "GND")}

# Componentes: ref -> dict(lib, valor, huella, cara, tipo, notas, pines{num: (funcion, red)})
# pines None = el simbolo no tiene pines (agujeros de montaje).
def _pines_modulo(desde):
    return {n: MODULO[desde + n - 1] for n in range(1, 21)}

BOTONES = [  # ref, nombre, red
    ("SW1", "DOWN", "BTN_DOWN"), ("SW2", "LEFT", "BTN_LEFT"), ("SW3", "UP", "BTN_UP"),
    ("SW4", "RIGHT", "BTN_RIGHT"), ("SW5", "SELECT", "BTN_SELECT"), ("SW6", "START", "BTN_START"),
    ("SW7", "B", "BTN_B"), ("SW8", "A", "BTN_A"),
]

COMPONENTES = {
    "J1": dict(lib="Connector_Generic:Conn_01x20", valor="RP2350-Plus 1-20", huella=FP_SOCKET.format(20),
               cara="Bottom", notas="Tira hembra 1x20; pines 1-20 del modulo (GP0 junto al USB-C)",
               pines=_pines_modulo(1)),
    "J2": dict(lib="Connector_Generic:Conn_01x20", valor="RP2350-Plus 21-40", huella=FP_SOCKET.format(20),
               cara="Bottom", notas="Tira hembra 1x20; J2.n = pin 20+n del modulo",
               pines=_pines_modulo(21)),
    "J3": dict(lib="Connector_Generic:Conn_01x14", valor="TFT ILI9341 2.4in", huella=FP_SOCKET.format(14),
               cara="Top", notas="Tira hembra 1x14; pin 1 = VCC; SDO y tactil sin conectar", pines=PANTALLA),
    "J5": dict(lib="Connector_Generic:Conn_01x06", valor="DAC GY-PCM5102", huella=FP_DAC,
               cara="Top", notas="Tira hembra 1x6 (huella propia con el contorno del DAC); VIN = pin 1 abajo; jack centrado "
                                 "en x = 77.5 con la boca al borde inferior", pines=DAC),
    # Huella Wuerth WS-SLTV (paso 2.54 mm): pad 1 = CENTRAL, pads 2 y 3 en los extremos. Se usa el simbolo oficial
    # Switch:SW_SPDT_312, cuyo pin 1 es el comun (B): asi el pad central queda como comun sin tocar la huella.
    "SW10": dict(lib="Switch:SW_SPDT_312", valor="ON/OFF",
                 huella="Button_Switch_THT:SW_Slide-03_Wuerth-WS-SLTV_10x2.5x6.4_P2.54mm",
                 cara="Bottom", notas="Deslizante recto, paso 2.54 mm confirmado en protoboard (14-oct); comun = pad 1 (central) a 3V3_EN; "
                                      "OFF = pad 2 a GND; pad 3 sin conectar; continuidad confirmada en protoboard (21-oct): palanca hacia "
                                      "un lado = comun con la pata de ese lado (OFF junto al pad 2, ON junto al pad 3)",
                 pines={1: ("comun (B)", "PWR_EN"), 2: ("C (OFF)", "GND"), 3: ("A (ON, al aire)", None)}),
    "C2": dict(lib="Device:C", valor="100n", huella=FP_C, cara="Top",
               notas="Ceramico; desacoplo de la pantalla, junto a J3", pines={1: ("1", "+3V3"), 2: ("2", "GND")}),
    "C3": dict(lib="Device:C", valor="100n", huella=FP_C, cara="Top",
               notas="Ceramico; desacoplo del DAC, vertical junto a J5", pines={1: ("1", "+3V3"), 2: ("2", "GND")}),
    "C4": dict(lib="Device:C_Polarized", valor="10u 25V", huella="Capacitor_THT:CP_Radial_D4.0mm_P1.50mm",
               cara="Top", notas="Electrolitico (pieza real D4 x 7-8 mm, paso 1.5 mm, medida 21-oct); desacoplo del DAC a la "
                                 "altura de VIN; polaridad (+ = pin 1, pad cuadrado)",
               pines={1: ("+", "+3V3"), 2: ("-", "GND")}),
}
for ref, nombre, red in BOTONES:
    COMPONENTES[ref] = dict(lib="Switch:SW_Push", valor=nombre, huella=FP_PUSH, cara="Top",
                            notas="Pulsador 6x6 mm (DEC); pull-up interno, pulsado = LOW",
                            pines={1: ("1", red), 2: ("2", "GND")})
for i in range(1, 5):
    COMPONENTES[f"H{i}"] = dict(lib="Mechanical:MountingHole", valor="M2", huella="MountingHole:MountingHole_2.2mm_M2",
                                cara="-", notas="NPTH 2.2 mm; fijacion a la carcasa", pines=None,
                                # igual que la huella oficial (attr exclude_from_pos_files): F8 no cambia nada
                                flags={"in_pos_files": "no"})
# Puntos de prueba (v0.9, sugerencia del profesor): pads THT sin costo; la huella oficial va excluida de BOM y de
# archivos de posicion, y el simbolo igual para que F8 no cambie nada.
COMPONENTES["TP1"] = dict(lib="Connector:TestPoint", valor="3V3", huella="TestPoint:TestPoint_THTPad_D2.0mm_Drill1.0mm",
                          cara="Top", notas="Punto de prueba +3V3 junto a C2 (pad, no se compra)",
                          pines={1: ("1", "+3V3")}, flags={"in_bom": "no", "in_pos_files": "no"})
COMPONENTES["TP2"] = dict(lib="Connector:TestPoint", valor="GND", huella="TestPoint:TestPoint_THTPad_D2.0mm_Drill1.0mm",
                          cara="Top", notas="Punto de prueba GND junto a C2 (pad, no se compra)",
                          pines={1: ("1", "GND")}, flags={"in_bom": "no", "in_pos_files": "no"})
# Bateria: solo en el esquematico y la BOM ("excluir de la placa"); se conecta al conector BAT del RP2350-Plus.
COMPONENTES["BT1"] = dict(lib="Device:Battery_Cell", valor="LiPo 103450 3.7V 2000mAh", huella="", cara="-",
                          notas="Excluida de la placa: va al conector BAT (PH1.25) del RP2350-Plus con el adaptador; "
                                "medir la polaridad con multimetro antes de conectar",
                          pines={1: ("+", None), 2: ("-", None)}, flags={"on_board": "no"})
# H5/H6 (agujeros del modulo de pantalla) eliminados en la Fase 3: la pantalla se sujeta con J3 y la carcasa

# ---------------------------------------------------------------- BOM de compra (v0.9, sugerencia del profesor 5.1)
# Una fila por articulo que hay que tener para armar una consola, incluidos los que no estan en el esquematico
# (modulos, bateria, capuchones, tornillos). gen_bom_netlist.py la escribe en KIDBOX/BOM_compra.csv.
# Precio, proveedor y codigo quedan "por cotizar" cuando el equipo no los ha fijado: no se inventan.
POR = "por cotizar"
COMPRA = [
    dict(ref="U1", item="Waveshare RP2350-Plus (RP2350A, 16 MB flash, USB-C, cargador LiPo ETA6096)", por=1, comprar=1,
         fab="Waveshare", mpn="RP2350-Plus", prov=POR, cod=POR, precio=POR,
         estado="En mano; medido 21.0 x 51.55 mm, filas a 17.78 mm (confirmado)",
         notas="Pinout Pico 2; trae la tira macho soldada; va sobre J1/J2"),
    dict(ref="U2", item="Modulo TFT 2.4in SPI ILI9341 240x320, 14 pines (MSP2402 o clon)", por=1, comprar=1,
         fab="AFEL (clon de LCDwiki MSP2402)", mpn="MSP2402", prov=POR, cod=POR, precio=POR,
         estado="En mano; confirmado con la pieza (15-oct)",
         notas="Sin tactil ni SD; firmware con tft.setRotation(3); revisar el puente J1 del modulo (3.3 V)"),
    dict(ref="U3", item="Modulo DAC GY-PCM5102 (PCM5102A, I2S, jack 3.5 mm)", por=1, comprar=1,
         fab="generico", mpn="GY-PCM5102", prov=POR, cod=POR, precio=POR,
         estado="En mano; medido 31.85 x 17.5 mm; probado con VIN = 3V3 (23-oct)",
         notas="Puentes FLT/DEMP/FMT = L y XSMT = H (en este modulo H3L = FMT y H4L = XSMT); trae la tira macho; va sobre J5"),
    dict(ref="BT1", item="Bateria LiPo 103450 3.7 V 2000 mAh con proteccion", por=1, comprar=1,
         fab="generico", mpn="103450", prov="profesor", cod="-", precio="-",
         estado="En mano (del profesor); medida 50.99 x 33.11 x 9.84 mm",
         notas="Conector blanco (parece PH2.0); va en un bolsillo de la carcasa con fondo de plastico, detras de la zona marcada; no se pega a la PCB"),
    dict(ref="-", item="Adaptador de bateria (conector de la bateria -> PH1.25 2P del RP2350-Plus)", por=1, comprar=1,
         fab="-", mpn="-", prov="profesor", cod="-", precio="-", estado="Pendiente (lo hace el profesor)",
         notas="Medir la polaridad con multimetro antes de conectar (rojo = + -> + del BAT)"),
    dict(ref="J1 J2", item="Tira hembra 1x20, paso 2.54 mm, recta", por=2, comprar=2,
         fab="generico", mpn="-", prov=POR, cod=POR, precio=POR, estado="Por confirmar", notas="Para el RP2350-Plus"),
    dict(ref="J3", item="Tira hembra 1x14, paso 2.54 mm, recta", por=1, comprar=1,
         fab="generico", mpn="-", prov=POR, cod=POR, precio=POR, estado="Por confirmar", notas="Para la pantalla"),
    dict(ref="J5", item="Tira hembra 1x6, paso 2.54 mm, recta", por=1, comprar=1,
         fab="generico", mpn="-", prov=POR, cod=POR, precio=POR, estado="Por confirmar",
         notas="Para el DAC (opcional: el DAC tambien se puede soldar directo para bajar el grosor)"),
    dict(ref="SW1-SW8", item="Pulsador tactil 6x6 mm THT, 4 patas, alto 9.1 mm", por=8, comprar=10,
         fab="generico", mpn="-", prov="DEC", cod="-", precio="-", estado="En mano (DEC); patas 6.5 x 4.5 mm confirmadas",
         notas="2 de repuesto"),
    dict(ref="-", item="Capuchon redondo D9 para pulsador 6x6", por=8, comprar=10,
         fab="impresion 3D", mpn="-", prov="-", cod="-", precio="-", estado="Por disenar e imprimir",
         notas="Redondos D9: >= 1.5 mm de aire a los modulos (ESPECIFICACION seccion 6)"),
    dict(ref="SW10", item="Interruptor deslizante 1P2T recto, 3 patas, paso 2.54 mm", por=1, comprar=2,
         fab="Wurth Elektronik (o equivalente)", mpn="450301014042 (o equivalente)", prov=POR, cod=POR, precio=POR,
         estado="En mano (equivalente metalico pequeno); paso y continuidad medidos (14 y 21-oct)", notas="1 de repuesto"),
    dict(ref="C2 C3", item="Condensador ceramico 100 nF, disco, paso 5 mm", por=2, comprar=4,
         fab="generico", mpn="-", prov=POR, cod=POR, precio=POR, estado="En mano; paso medido (21-oct)", notas="2 de repuesto"),
    dict(ref="C4", item="Condensador electrolitico 10 uF 25 V, radial D4 mm, paso 1.5 mm", por=1, comprar=2,
         fab="generico", mpn="-", prov=POR, cod=POR, precio=POR, estado="En mano; medido D4 x 7-8 mm, paso 1.5 (21-oct)",
         notas="Polaridad: + en el pad cuadrado"),
    dict(ref="TP1 TP2", item="Puntos de prueba (pads de la placa)", por=2, comprar=0,
         fab="-", mpn="-", prov="-", cod="-", precio="0", estado="No se compran", notas="TP1 = +3V3, TP2 = GND"),
    dict(ref="H1-H4", item="Tornillo M2 x L + separador M2 + tuerca", por=4, comprar=4,
         fab="generico", mpn="-", prov=POR, cod=POR, precio=POR, estado="Por definir", notas="L segun la carcasa"),
    dict(ref="-", item="Sujecion de la bateria en la carcasa (bolsillo impreso con fondo de plastico, traba y canal para el cable)",
         por=1, comprar=1, fab="impresion 3D", mpn="-", prov="-", cod="-", precio="-", estado="Por disenar con la carcasa",
         notas="Reemplaza la cinta doble faz: la bateria no se pega a la PCB (sugerencia del profesor 4.6)"),
    dict(ref="PCB", item="Placa KIDBOX v0.9, 2 capas, 150 x 70 mm, 1.6 mm, HASL sin plomo, verde", por=1, comprar=5,
         fab="JLCPCB", mpn="-", prov="JLCPCB", cod="fabricacion/KIDBOX_gerbers_v0.9_PRELIMINAR.zip", precio=POR,
         estado="No pedir hasta la prueba 1:1 de la v0.9", notas="5 es el minimo de JLCPCB"),
]
