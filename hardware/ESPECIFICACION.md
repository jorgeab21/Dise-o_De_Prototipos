# ESPECIFICACION.md — Especificación de la PCB KIDBOX (BORRADOR v0.5)

> **Estado: BORRADOR CON SUPUESTOS.** Basado en el Game★Mite v1.3.2 (CC BY 4.0) con los cambios acordados con el profesor el 13-oct-2026.
> Las piezas físicas no se han medido todavía. Todo lo marcado **[SUPUESTO]** viene de hojas de datos, de la página del vendedor o de
> módulos típicos, y debe confirmarse con la pieza real **antes de la Fase 2 (PCB)**. Las secciones 2 a 5 bastan para las Fases 0 y 1 (esquemático).
>
> **v0.5:** incorpora las respuestas a la Fase 0 (13-oct). Ver la sección 11, "Respuestas a la Fase 0".

Nombre del proyecto: `KIDBOX`

Autor: `Equipo KIDBOX (J. Becerra, B. Fernández, A. Medina, D. Pizarro)`   Fecha: `13-oct-2026`   Versión del documento: `0.5`
(La versión del documento no es la de la placa: la primera placa fabricada se rotula **v1.0**.)

---

## 0. Entorno

| Dato | Valor |
| :--- | :--- |
| Sistema operativo | `Windows 11` |
| Versión de KiCad y ruta de `kicad-cli` | `10.0.6 — C:\Program Files\KiCad\10.0\bin\kicad-cli.exe` |
| Agente y modelo | `Claude Code` |
| Fabricante y servicio | `JLCPCB, PCB de 2 capas, 1.6 mm, sin ensamblaje` |
| Fuentes autorizadas para descargar huellas que no estén en KiCad | `ninguna` (solo huellas oficiales de KiCad 10) |
| Fuentes autorizadas para CONSULTAR hojas de datos | Wiki y esquemático oficiales de **Waveshare RP2350-Plus**; ficha del **MSP2402** en **LCDwiki**. Se pueden guardar como PDF o imagen en `datasheets/` (dejar la URL de origen en `DECISIONES.md`). No descargar huellas ni software |

## 1. Objetivo del circuito

Consola portátil para niños de 6 a 10 años (KIDBOX) con juegos de desarrollo cognitivo y límite de sesión incorporado.
Es una **placa portadora de módulos** basada en el Game★Mite: un módulo Waveshare RP2350-Plus lee 8 botones y un reset,
dibuja en una pantalla TFT ILI9341 de 2.4" por SPI (la misma familia que usa el Game★Mite, con brillo regulable por PWM)
y envía audio por I2S a un DAC PCM5102A con salida de 3,5 mm para audífonos. No se usan ni la SD ni el táctil de la pantalla.
La batería LiPo se conecta directamente al cargador integrado de la RP2350-Plus y no pasa por esta PCB. Formato horizontal.

```
[LiPo 500 mAh]──>[RP2350-Plus]──SPI0 (GP6, GP3) + CS/DC/RST/LED──> [J3 TFT ILI9341 2.4"]   (J4: solo apoyo mecánico)
                   │   │  │
                   │   │  └──I2S (GP20, GP21, GP22)──> [J5 DAC PCM5102A] ──> jack 3,5 mm (audífonos)
                   │   └──cruceta GP16..GP19 · SELECT/START/B/A GP12..GP15──> 8 × [pulsador 6×6 ──> GND]
                   └──3V3_EN <── [SW10 interruptor ON/OFF, cara posterior]        RUN <── [SW9 pulsador RESET + C]
```

## 2. Microcontrolador o módulo principal

| Dato | Valor |
| :--- | :--- |
| Modelo exacto | Waveshare **RP2350-Plus** (RP2350A, 16 MB flash, USB-C, cargador LiPo integrado). Respaldo: Raspberry Pi Pico (RP2040) del DEC, mismo pinout |
| Cómo va montado | Sobre **2 tiras hembra 1×20** (el módulo trae pines macho soldados) |
| Representación en el esquemático | **J1 y J2**, dos `Connector_Generic:Conn_01x20` con etiquetas de red por pin (GP0, GP1, …). **No** se usa el símbolo `MCU_Module:RaspberryPi_Pico`. En este documento, "U1.GPx" significa el pin del módulo en J1 (pines 1–20) o J2 (pines 21–40) |
| Cara y orientación | **Cara posterior (Bottom)**, girada 180°: USB-C hacia el **borde superior** de la placa (como un control de PlayStation: se puede jugar mientras carga). ⚠ Montado por detrás queda espejado: verificar fila por fila contra la foto |
| Paso de pines | 2.54 mm |
| Separación entre filas | **17.78 mm [SUPUESTO: igual que la Pico]** |
| Dimensiones del módulo | **51 × 21 mm [SUPUESTO: formato Pico]** |
| Pines por fila y pin 1 | 20 por fila; pin 1 = GP0, junto al USB **[SUPUESTO: igual que la Pico]** |
| Fuente del pinout | Pinout de la Raspberry Pi Pico (igual al esquemático del Game★Mite). Contrastar con la wiki o el esquemático oficial de Waveshare (autorizado en la sección 0). **[PENDIENTE]** foto de la serigrafía en `datasheets/rp2350plus_pinout.jpg` |
| Pines que SÍ se pueden usar | GP0–GP22, GP26–GP28 |
| Pines PROHIBIDOS y por qué | VBUS, VSYS (alimentación del módulo), ADC_VREF, 3V3 (solo como salida para alimentar) |
| ¿Trae regulador, USB y desacoplos? | Sí: regulador, USB-C, cargador LiPo y desacoplos propios |
| Huella KiCad | `Connector_PinSocket_2.54mm:PinSocket_1x20_P2.54mm_Vertical` ×2 (J1, J2) |

## 3. Alimentación

| Dato | Valor |
| :--- | :--- |
| Fuente de energía | LiPo Soshine 902030 3.7 V 500 mAh (9 × 20 × 30 mm) → conector de batería **de la RP2350-Plus**. No se conecta a esta PCB |
| Tensión de entrada | 3.0–4.2 V (LiPo); 5 V por USB-C al cargar |
| Rieles | **3V3** desde el pin 36 de la RP2350-Plus: pantalla (~80 mA con luz de fondo al máximo) + DAC (~20 mA) + pull-ups. Total < 150 mA |
| ¿Regulador? | No: lo trae la RP2350-Plus |
| Encendido | Interruptor deslizante: **ON = 3V3_EN al aire; OFF = 3V3_EN a GND** (como el Game★Mite). **[PENDIENTE: confirmar en el esquemático de Waveshare que 3V3_EN tiene pull-up y que en OFF la placa queda apagada con la batería conectada]** |
| Protecciones | No (la RP2350-Plus gestiona carga y protección) **[PENDIENTE: confirmar que la corriente de carga es ≤ 500 mA]** |
| Desacoplo | 100 nF entre 3V3 y GND junto a J3 (pantalla); 100 nF + 10 µF junto a J5 (DAC) |

## 4. Lista de componentes

| Ref | Cant. | Descripción / valor | THT/SMD | Cara | Símbolo · Huella KiCad | Notas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| J1, J2 | 2 | Tira hembra 1×20, 2.54 mm, para la RP2350-Plus | THT | Bottom | `Connector_Generic:Conn_01x20` · `Connector_PinSocket_2.54mm:PinSocket_1x20_P2.54mm_Vertical` | Separación entre filas 17.78 mm [SUPUESTO] |
| J3 | 1 | Tira hembra 1×14 para la pantalla TFT ILI9341 2.4" | THT | Top | `Connector_Generic:Conn_01x14` · `Connector_PinSocket_2.54mm:PinSocket_1x14_P2.54mm_Vertical` | Orden de pines en la sección 5 |
| J4 | 1 | Tira hembra 1×4, lado SD de la pantalla | THT | Top | `Connector_Generic:Conn_01x04` · `Connector_PinSocket_2.54mm:PinSocket_1x04_P2.54mm_Vertical` | **Solo apoyo mecánico**: sus 4 pines sin conectar |
| J5 | 1 | Tira hembra 1×6 para el DAC GY-PCM5102 | THT | Bottom | `Connector_Generic:Conn_01x06` · `Connector_PinSocket_2.54mm:PinSocket_1x06_P2.54mm_Vertical` | El jack del DAC debe apuntar hacia el **borde inferior** |
| SW1–SW8 | 8 | Pulsador táctil 6×6 mm, 4 patas (DEC) | THT | Top | `Switch:SW_Push` · `Button_Switch_THT:SW_PUSH_6mm` | Capuchones impresos en 3D más adelante |
| SW9 | 1 | Pulsador RESET 6×6 mm | THT | Top | `Switch:SW_Push` · `Button_Switch_THT:SW_PUSH_6mm` | A RUN |
| SW10 | 1 | Interruptor deslizante 1 polo 2 posiciones, **recto** | THT | **Bottom** | `Switch:SW_SPDT` · `Button_Switch_THT:SW_Slide_SPDT_Straight_CK_OS102011MS2Q` | Palanca hacia la parte trasera; la carcasa trasera lleva un **rebaje** para alcanzarla. Modelo exacto según el pañol [PENDIENTE] |
| C1 | 1 | 100 nF cerámico (RESET, como C11 del Game★Mite) | THT | Top | `Device:C` · `Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm` | |
| C2 | 1 | 100 nF cerámico (desacoplo pantalla) | THT | Top | `Device:C` · ídem C1 | Junto a J3, fuera del área que tapa la pantalla si es posible |
| C3 | 1 | 100 nF cerámico (desacoplo DAC) | THT | Bottom | `Device:C` · ídem C1 | Junto a J5 |
| C4 | 1 | 10 µF electrolítico 16 V (desacoplo DAC) | THT | Bottom | `Device:C_Polarized` · `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm` | Polaridad |
| H1–H4 | 4 | Agujero M2 (fijación a la carcasa) | NPTH 2.2 mm | — | `Mechanical:MountingHole` (in_bom no) · `MountingHole:MountingHole_2.2mm_M2` | Tornillos M2 confirmados por el profesor |
| H5–H8 | 4 | Agujeros para **separadores de la pantalla**, alineados con los 4 agujeros de las esquinas del módulo | NPTH | — | `Mechanical:MountingHole` (in_bom no) · según el diámetro medido | **[PENDIENTE 15-oct]**: posición y diámetro. Solo Fase 2 |
| H9 | 0–1 | Agujero para separador del DAC, **solo si el módulo tiene agujero** | NPTH | — | `Mechanical:MountingHole` (in_bom no) | **[PENDIENTE 14-oct]**. Solo Fase 2 |

Regla para SMD: **no hay componentes SMD.**
Si la medición del pin LED (15-oct) obliga a agregar un transistor, se agrega antes de la Fase 2 (ver la sección 5).

## 5. Conexiones (netlist funcional)

Numeración de pines de la RP2350-Plus = Pico **[SUPUESTO]**: GP0=1, GP1=2, GND=3, GP2=4, GP3=5, GP4=6, GP5=7, GND=8,
GP6=9, GP7=10, GP8=11, GP9=12, GND=13, GP10=14, GP11=15, GP12=16, GP13=17, GND=18, GP14=19, GP15=20, GP16=21, GP17=22,
GND=23, GP18=24, GP19=25, GP20=26, GP21=27, GND=28, GP22=29, RUN=30, GP26=31, GP27=32, GND=33, GP28=34, ADC_VREF=35,
3V3=36, 3V3_EN=37, GND=38, VSYS=39, VBUS=40. J1 = pines 1–20, J2 = pines 21–40.
El pin 33 es AGND en la Pico; se conecta a GND (lo permite la hoja de datos de la Pico).

Orden de pines de J3 (pantalla, según la serigrafía de la foto del vendedor, igual al J2 del Game★Mite):
1 VCC, 2 GND, 3 CS, 4 RESET, 5 DC, 6 SDI(MOSI), 7 SCK, 8 LED, 9 SDO(MISO), 10 T_CLK, 11 T_CS, 12 T_DIN, 13 T_DO, 14 T_IRQ.

Orden de pines de J5 (DAC GY-PCM5102) **[SUPUESTO: foto del vendedor]**: 1 VIN, 2 GND, 3 LCK, 4 DIN, 5 BCK, 6 SCK.

| Red | Desde (ref.pin) | Hasta (ref.pin) | Tipo | Requisito |
| :--- | :--- | :--- | :--- | :--- |
| LCD_CS | U1.GP0 | J3.3 (CS) | señal | Igual que el Game★Mite |
| LCD_RST | U1.GP1 | J3.4 (RESET) | señal | Igual |
| LCD_DC | U1.GP2 | J3.5 (DC) | señal | Igual |
| LCD_MOSI | U1.GP3 | J3.6 (SDI) | señal | SPI0 TX, igual |
| LCD_SCK | U1.GP6 | J3.7 (SCK) | señal | SPI0 SCK, igual |
| LCD_LED | U1.GP26 | J3.8 (LED) | señal | PWM de brillo, **conexión directa** (según LCDwiki el módulo MSP2402 trae transistor en LED). **Cambio respecto al Game★Mite** (allí va a VCC con 68 Ω). [PENDIENTE 15-oct: medir la corriente del pin LED; si supera ~10 mA se agrega transistor antes de la Fase 2] |
| I2S_BCK | U1.GP20 | J5.5 (BCK) | señal | BCK y LCK en pines consecutivos (requisito de la librería I2S) |
| I2S_LRCK | U1.GP21 | J5.3 (LCK) | señal | |
| I2S_DIN | U1.GP22 | J5.4 (DIN) | señal | |
| DAC_SCK | J5.6 (SCK) | GND | GND | El DAC usa su reloj interno |
| BTN_DOWN | SW1.1 | U1.GP16 | señal | pull-up interno. **Cruceta reasignada a GP16–GP19** (columna izquierda de U1, del lado de la cruceta) |
| BTN_LEFT | SW2.1 | U1.GP17 | señal | |
| BTN_UP | SW3.1 | U1.GP18 | señal | |
| BTN_RIGHT | SW4.1 | U1.GP19 | señal | |
| BTN_SELECT | SW5.1 | U1.GP12 | señal | Igual que el Game★Mite |
| BTN_START | SW6.1 | U1.GP13 | señal | Igual |
| BTN_B | SW7.1 | U1.GP14 | señal | Igual |
| BTN_A | SW8.1 | U1.GP15 | señal | Igual |
| RUN | SW9.1, C1.1 | U1.RUN | señal | SW9.2 y C1.2 a GND |
| PWR_EN | SW10.común | U1.3V3_EN | señal | Otra posición de SW10 a GND (= apagado); la tercera pata sin conectar |
| 3V3 | U1.3V3 | J3.1 (VCC), J5.1 (VIN), C2, C3, C4.+ | potencia | Pista ≥ 0.5 mm [PENDIENTE: confirmar que el DAC funciona con 3V3] |
| GND | U1.GND (todos, incluido el pin 33) | J3.2, J5.2, J5.6, SW1–SW9.2, C1–C4, SW10 | GND | Plano en B.Cu |

Sin conectar (`no_connect`):
- J3.9 (SDO/MISO): no se lee nada de la pantalla.
- J3.10–J3.14 (táctil): **no se usa el táctil**.
- J4.1–J4.4 (SD): **no se usa la SD**; J4 es solo apoyo mecánico.
- RP2350-Plus: GP4, GP5, GP7, **GP8–GP11**, GP27, GP28, VBUS, VSYS, ADC_VREF.

Con J1/J2 como conectores genéricos, el ERC necesita `PWR_FLAG` en 3V3 y en GND.

Cada botón une su GPIO con GND; el firmware usa `INPUT_PULLUP` (pulsado = LOW). El agente puede reasignar los **botones** a
pines libres para facilitar el ruteo, avisando y actualizando `netlist.csv`. Los pines de SPI, pantalla e I2S no se reasignan.

## 6. Mecánica y posiciones

> **Toda esta sección es [SUPUESTO]** para avanzar. Se confirma con las piezas (la pantalla llega el jueves 15) y el boceto en papel antes de la Fase 2.

| Dato | Valor |
| :--- | :--- |
| Dimensiones exteriores | **150 × 65 mm [SUPUESTO]**. Se acepta el sobrecosto de JLCPCB por superar 100 × 100 mm |
| Forma | Rectángulo |
| Radio de esquinas | 4 mm (seguridad para niños; la carcasa redondea más) |
| Origen | Esquina superior izquierda = (0,0), Y hacia abajo |
| Referencia de las coordenadas | **Centro del cuerpo** de cada pieza (no el origen de la huella; en `SW_PUSH_6mm` el origen es el pad 1, desplazado (−3.25, −2.25) mm del centro) |
| Rotaciones | **Manda la descripción geométrica** (qué pin queda dónde, visto desde el frente). El ángulo de la tabla es orientativo: en la cara Bottom KiCad cambia el ángulo al voltear. Verificar la posición de los pads |
| Agujeros de montaje | M2 NPTH 2.2 mm en (4, 4), (146, 4), (4, 61), (146, 61) |
| Altura máxima | Top: botones ≈ 5 mm (+ capuchón); pantalla sobre tira hembra ≈ 8.5 mm + módulo (AFEL indica "1,15 cm de altura total"; **[PENDIENTE 15-oct: medir]**). Bottom: RP2350-Plus y DAC sobre tira hembra ≈ 12 mm; batería 9 mm [SUPUESTO] |
| Zonas prohibidas (keep-out) | **Top:** bajo el módulo de pantalla (x 36–114, y 6.5–49.5) no van componentes salvo J3 y J4; **sí se permiten pistas y las soldaduras** de las piezas THT de la cara Bottom (J1, J2, J5, C3, C4), porque la pantalla va 8.5 mm más arriba. **Bottom — zona de batería:** rectángulo **x 88–108, y 10–40** sin componentes ni patas de piezas THT; solo pistas y vías tapadas (la batería apoya ahí y la sujeta un bolsillo de la carcasa, sin espuma). Borde superior libre en x 71–79 (USB-C) y borde inferior libre bajo el jack |
| Espesor | 1.6 mm |

Módulo de pantalla [SUPUESTO, página del vendedor]: 78 × 43 mm, horizontal, centrado en (75, 28) → ocupa x 36–114, y 6.5–49.5.
Montado **girado 180°**: tira de 14 pines (J3) **vertical** en el borde corto **derecho**, con el **pin 1 (VCC) abajo**; tira de 4 pines (J4)
vertical en el borde corto **izquierdo**. La imagen se endereza en el firmware con `setRotation()`. Distancias exactas de cada tira al borde
del módulo y posición de sus 4 agujeros de montaje [PENDIENTE: medir el jueves].

RP2350-Plus girada 180° (USB-C arriba) vista desde el frente "a través" de la placa: pin 1 (GP0) arriba a la derecha, pines 1–20 en la
columna derecha (x = 83.89) de arriba hacia abajo, pines 21–40 en la columna izquierda (x = 66.11) de abajo hacia arriba [VERIFICAR con foto].
Dibujo de referencia: `datasheets/layout_propuesto.svg` (generado con `scripts/gen_layout.py`).

Posiciones fijas [SUPUESTO — validar con piezas reales y boceto] (centro del cuerpo):

| Ref | x (mm) | y (mm) | Rot. (°) | Cara | Por qué es fija |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SW3 (UP) | 18 | 20 | 0 | Top | Cruceta, pulgar izquierdo (paso de 10 mm para capuchones). Corrida 2 mm a la izquierda: el capuchón queda a 3 mm de la pantalla |
| SW1 (DOWN) | 18 | 40 | 0 | Top | Cruceta |
| SW2 (LEFT) | 8 | 30 | 0 | Top | Cruceta |
| SW4 (RIGHT) | 28 | 30 | 0 | Top | Cruceta; capuchón hasta x = 33, pantalla desde x = 36 |
| SW8 (A) | 138 | 25 | 0 | Top | Pulgar derecho |
| SW7 (B) | 126 | 35 | 0 | Top | Pulgar derecho, en diagonal con A; fuera del módulo (x ≤ 114) |
| SW5 (SELECT) | 66 | 58 | 0 | Top | Bajo la pantalla, centrado; la RP2350-Plus termina en y = 53.5 |
| SW6 (START) | 84 | 58 | 0 | Top | Bajo la pantalla, centrado |
| SW9 (RESET) | 140 | 54 | 0 | Top | Esquina, lejos de los pulgares |
| SW10 (ON/OFF) | 125 | 8 | 0 | **Bottom** | Recto, palanca hacia atrás: no se apaga sin querer mientras se juega. Fuera de la zona de batería y de las patas de A (y ≥ 22.75) |
| J3 (pantalla 1×14) | ≈ 111.5 | 28 | 180 | Top | Vertical en el borde derecho del módulo, pin 1 abajo [PENDIENTE: medir] |
| J4 (apoyo 1×4) | ≈ 38.5 **[PENDIENTE]** | ≈ 28 **[PENDIENTE]** | 180 | Top | Vertical en el borde izquierdo del módulo, según la posición real de los pines SD |
| U1 (RP2350-Plus, J1+J2) | centro (75, 28) | — | ver descripción | **Bottom** | Vertical, USB-C en el borde superior (y = 0) para cargar y programar sin estorbar las manos |
| J5 (DAC) | módulo en x 36–61, y 33–64; tira en y ≈ 36 **[SUPUESTO]** | — | — | Bottom | A la izquierda de la RP2350-Plus, junto a los pines I2S; jack de 3,5 mm hacia el borde inferior |

## 7. Fabricante y reglas de diseño (DFM)

| Parámetro | Mi valor | Mínimo del fabricante |
| :--- | :--- | :--- |
| Número de capas | `2` | — |
| Ancho mínimo de pista (señal) | `0.25 mm` | `0.127 mm` |
| Ancho de pistas de potencia | `0.50 mm` | — |
| Separación mínima cobre-cobre | `0.20 mm` | `0.127 mm` |
| Vía: diámetro / taladro | `0.60 / 0.30 mm` | `0.45 / 0.20 mm` |
| Vías | **Tapadas (tented)** con máscara: obligatorio en la zona de batería | — |
| Anillo anular THT (soldadura manual) | `≥ 0.35 mm` (el que dan las **huellas oficiales** de KiCad: tiras hembra y SW10 0.35 mm; pulsadores y condensadores 0.40–0.45 mm). No modificar huellas | `0.15 mm` |
| Cobre a borde de placa | `0.30 mm` | `0.20 mm` |
| Agujero a agujero | `0.25 mm` | — |
| Serigrafía: trazo / alto de texto | `0.15 / 1.0 mm` | `0.15 mm` |
| Acabado superficial | `HASL sin plomo` | — |
| Color de máscara | `verde` | — |
| ¿Ensamblaje SMT? | `No` | — |

## 8. Estrategia de ruteo

| Dato | Valor |
| :--- | :--- |
| Capa de señales preferente | `F.Cu` |
| Plano de masa | `B.Cu continuo` (evitar cortarlo con pistas), con **alivios térmicos** en todos los pads de GND para poder soldar con cautín |
| ¿Vías? | Sí, solo si no se puede rutear en F.Cu |
| Pistas bajo módulos | **Permitidas**, también en la cara donde se sueldan: los módulos van 8.5 mm más arriba sobre tiras hembra. La regla de `AGENTS.md` "sin pistas bajo módulos THT en la cara donde se sueldan" **no aplica** en este proyecto |
| Ancho por tipo de red | Señal 0.25 mm · 3V3 0.5 mm |
| Redes críticas | SPI (GP6/GP3) e I2S (GP20/21/22) lo más cortas posible y separadas entre sí |
| Autorouter | Solo si el agente no logra rutear en 2 intentos, y solo en F.Cu |
| ¿Reasignar pines? | Solo los botones, a pines libres; nunca SPI, pantalla ni I2S |
| Ángulos | `45° y 90°` |

## 9. Serigrafía y marcas

- F.SilkS: nombre de cada botón (UP, DOWN, LEFT, RIGHT, A, B, SELECT, START, RESET), 1.0 mm.
- F.SilkS: contorno del módulo de pantalla y pin 1 de J3.
- B.SilkS: contorno de la RP2350-Plus **con la forma del USB-C**, el **pin 1 marcado en J1 y J2**, y "VISTA POSTERIOR — FILAS ESPEJADAS".
- B.SilkS: contorno del DAC, posición del jack y **"VIN" y "GND" rotulados en J5**.
- B.SilkS: "ON/OFF" junto a SW10.
- Texto "KIDBOX v1.0 2026 — basado en Game★Mite de Thomas Hugo Williams (CC BY 4.0)". Si la fuente de KiCad no tiene "★", escribir "Game*Mite".
- Ningún texto bajo la pantalla ni bajo la RP2350-Plus (no se vería): ubicarlos fuera de los módulos.

## 10. Entregables que espero del agente

- [ ] Proyecto KiCad completo que abre sin errores en KiCad `10.0`.
- [ ] ERC y DRC con 0 errores, mínimos DFM de la sección 7 escritos en el proyecto.
- [ ] `BOM.csv`, `netlist.csv`, `DECISIONES.md`, `README.md`.
- [ ] `README.md` con el **orden de soldadura**: primero las piezas de la cara Bottom que se sueldan desde Top (J1, J2, J5, C3, C4, SW10), después las de Top.
- [ ] Imágenes de verificación (`verificacion/`).
- [ ] Paquete de fabricación (`fabricacion/*.zip`) **solo cuando el equipo lo apruebe**.

## 11. Decisiones ya tomadas y preguntas abiertas

Decisiones tomadas (13-oct-2026):
- Base Game★Mite v1.3.2; se descarta la PCB "universal".
- RP2350-Plus (respaldo Pico); firmware en Arduino IDE.
- Pantalla TFT **ILI9341 2.4"** SPI (AFEL, 78 × 43 mm), misma familia y pinout que el Game★Mite. **Sin SD y sin táctil.** Brillo por PWM (GP26).
  La IPS 1.3" ST7789 del DEC se usa solo para pruebas en protoboard mientras llega la 2.4".
- Audio por DAC PCM5102A (I2S) con jack de 3,5 mm; sin parlante ni amplificador. Se mantiene la placa GY-PCM5102 de una tira de 1×6.
- Botones 6×6 del DEC; capuchones impresos en 3D.
- Formato horizontal. Todo THT, 2 capas, sin ensamblaje. Batería conectada a la RP2350-Plus.
- USB-C de la RP2350-Plus hacia el borde superior; jack de audífonos hacia el borde inferior. Pantalla montada girada 180°.

Respuestas a la Fase 0 (13-oct-2026):
1. Módulo como **J1/J2** (`Conn_01x20`), no U1.
2. Manda la **geometría descrita**, no el ángulo. J3 y J4 van a 180° (verticales, pin 1 abajo).
3. Coordenadas = **centro del cuerpo**.
4. Anillo anular **≥ 0.35 mm** con huellas oficiales sin modificar.
5. SW10 **recto, en la cara Bottom**, en (125, 8), con rebaje en la carcasa trasera.
6. Batería en la cara Bottom en **x 88–108, y 10–40**, sin patas THT ni componentes en esa zona, vías tapadas y bolsillo en la carcasa (sin espuma).
7. Luz de fondo **directa** a GP26; se confirma el 15-oct antes de la Fase 2.
8. **Cruceta a GP16–GP19** (DOWN GP16, LEFT GP17, UP GP18, RIGHT GP19).
9. Se **permiten** pistas y soldaduras bajo los módulos (sección 8).
10. **Agujeros para separadores** de la pantalla (H5–H8) y del DAC (H9, si tiene); posiciones el 14 y 15 de octubre, solo para la Fase 2.
11. **Permiso para consultar** la wiki y el esquemático de Waveshare RP2350-Plus y LCDwiki (MSP2402), y guardar las hojas de datos en `datasheets/`. Sin huellas.
12. Placa rotulada **"KIDBOX v1.0"**. Los "11,5 mm" son el alto total que indica AFEL; se mide el 15-oct.
13. Se acepta el **sobrecosto** de JLCPCB por superar 100 mm.
- Además (2c): cruceta corrida 2 mm a la izquierda (centro en x = 18), alivios térmicos en GND, marcas de orientación en la serigrafía y orden de soldadura en el README.

Pendientes:
- 14-oct: separación entre filas, dimensiones, posición del conector de batería y pinout de la RP2350-Plus (foto de la serigrafía); medidas del DAC, orden real de sus pines, posición del jack y si tiene agujero de montaje; que el DAC funcione con 3V3 (protoboard); modelo del interruptor deslizante; separación entre patas y altura de los pulsadores del DEC; altura de las tiras hembra.
- 15-oct (llega la pantalla): distancias de J3 y J4 a los bordes del módulo; posición y diámetro de sus 4 agujeros; alto total; corriente del pin LED (si supera ~10 mA hace falta un transistor).
- Boceto 1:1 de 150 × 65 mm con las manos encima.

## 12. Restricciones adicionales para el agente

- No usar componentes SMD.
- No mover las posiciones fijas de la sección 6 sin preguntar.
- No descargar huellas de internet; si una huella no existe, proponer tira de pines genérica y avisar.
- No modificar huellas oficiales (sección 7).
- No reasignar pines de SPI, pantalla ni I2S.
- No colocar componentes ni patas THT en la zona de batería de la cara Bottom (x 88–108, y 10–40).
- Anotar toda decisión no escrita aquí en `DECISIONES.md`.
- No avanzar a la Fase 2 mientras la sección 6 siga marcada como [SUPUESTO].
