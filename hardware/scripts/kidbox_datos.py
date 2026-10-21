# Datos del proyecto KIDBOX (componentes, pines y redes) segun ESPECIFICACION.md v0.7, secciones 2 a 5.
# No se ejecuta solo: lo importan gen_esquematico.py y gen_bom_netlist.py, para que el esquematico,
# BOM.csv y netlist.csv salgan de una unica fuente. Si cambia la especificacion, se edita aqui y se regeneran.

PROYECTO = "KIDBOX"

FP_SOCKET = "Connector_PinSocket_2.54mm:PinSocket_1x{:02d}_P2.54mm_Vertical"
FP_PUSH = "Button_Switch_THT:SW_PUSH_6mm"
FP_C = "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm"  # paso 5 mm medido en los ceramicos reales (21-oct)

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
    "J5": dict(lib="Connector_Generic:Conn_01x06", valor="DAC GY-PCM5102", huella=FP_SOCKET.format(6),
               cara="Bottom", notas="Tira hembra 1x6; orden de pines confirmado con la serigrafia; jack hacia el borde inferior", pines=DAC),
    # Huella Wuerth WS-SLTV (paso 2.54 mm): pad 1 = CENTRAL, pads 2 y 3 en los extremos. Se usa el simbolo oficial
    # Switch:SW_SPDT_312, cuyo pin 1 es el comun (B): asi el pad central queda como comun sin tocar la huella.
    "SW10": dict(lib="Switch:SW_SPDT_312", valor="ON/OFF",
                 huella="Button_Switch_THT:SW_Slide-03_Wuerth-WS-SLTV_10x2.5x6.4_P2.54mm",
                 cara="Bottom", notas="Deslizante recto, paso 2.54 mm confirmado en protoboard (14-oct); comun = pad 1 (central) a 3V3_EN; "
                                      "OFF = pad 2 a GND; pad 3 sin conectar; posicion OFF [PENDIENTE: continuidad]",
                 pines={1: ("comun (B)", "PWR_EN"), 2: ("C (OFF)", "GND"), 3: ("A (ON, al aire)", None)}),
    "C2": dict(lib="Device:C", valor="100n", huella=FP_C, cara="Top",
               notas="Ceramico; desacoplo de la pantalla, junto a J3", pines={1: ("1", "+3V3"), 2: ("2", "GND")}),
    "C3": dict(lib="Device:C", valor="100n", huella=FP_C, cara="Bottom",
               notas="Ceramico; desacoplo del DAC, junto a J5", pines={1: ("1", "+3V3"), 2: ("2", "GND")}),
    "C4": dict(lib="Device:C_Polarized", valor="10u 25V", huella="Capacitor_THT:CP_Radial_D5.0mm_P2.00mm",
               cara="Bottom", notas="Electrolitico; desacoplo del DAC; polaridad (+ = pin 1)",
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
# H5/H6 (agujeros del modulo de pantalla) eliminados en la Fase 3: la pantalla se sujeta con J3 y la carcasa
