# ESPECIFICACION.md — Especificación de la PCB KIDBOX (v0.9)

> **Estado: piezas medidas (14–23 oct) y correcciones del profesor aplicadas (26-oct-2026).** Basado en el Game★Mite v1.3.2 (CC BY 4.0) con los cambios acordados con el profesor.
> Lo que sigue marcado **[PENDIENTE]** se confirma antes de la **Fase 4 (Gerbers para fabricar)**, no bloquea la Fase 2.
>
> **v0.5:** respuestas a la Fase 0 · **v0.6:** datos de hojas oficiales (Waveshare, LCDwiki, ETA6096).
> **v0.7 (14-oct):** medidas reales de las piezas; **se elimina el RESET del frente (SW9, C1)**; **batería LiPo 103450 de 2000 mAh** (resuelve
> la carga a 1 A); **layout reordenado** para la batería: pantalla sin girar (J3 a la izquierda), **se elimina J4**, SW10 y B desplazados;
> huella de SW10 cambiada a paso de 2,54 mm. Ver la sección 11, "Cambios v0.7".
> **v0.8 (21-oct):** **pantalla 3 mm más arriba** (J3 centrada en y = 25), **DAC 3 mm hacia la cruceta** (J5 en x = 56, jack en x ≈ 30)
> y **C3 al costado de J5** (vertical entre J5 y SELECT). Motivo: que nada quede bajo el DAC (por si se suelda directo para bajar el
> grosor) y que C3 quede lejos del borde. Ver la sección 11, "Cambios v0.8".
> **v0.9 (26-oct):** correcciones del profesor (informe G5 del 22-oct) y decisiones del equipo del 23–26 oct: placa simétrica
> (primero 155 × 75, ajustada a **150 × 70** tras la prueba 1:1); **imagen** de la pantalla centrada (el módulo va 4.0 mm hacia J3); RP2350-Plus centrado;
> **DAC adelante** con huella propia y el **jack centrado** en el borde inferior; controles simétricos (propuesta P2 del estudio
> ergonómico); SW10 arriba a la izquierda por detrás; C4 con huella P1.50; TP1/TP2; BT1 en el esquemático; reglas de 0.29 mm.
> Ver la sección 11, "Cambios v0.9".
> **Ajuste v0.9 tras la prueba 1:1 (26-oct):** placa **150 × 70** (eje x = 75), controles compactos con capuchones Ø9, DAC 5 mm más
> arriba, franja de 4.74 mm para un **muro colgante** de la carcasa entre pantalla y DAC, y **batería en la carcasa** (la zona de la
> PCB queda solo como referencia). Ver la sección 11, punto 15.

Nombre del proyecto: `KIDBOX`

Autor: `Equipo KIDBOX (J. Becerra, B. Fernández, A. Medina, D. Pizarro)`   Fecha: `26-oct-2026`   Versión del documento: `0.9`
(Desde la v0.9 la placa se rotula con la misma versión que este documento: **v0.9**. Se reserva **v1.0** para la que se fabrique.)

---

## 0. Entorno

| Dato | Valor |
| :--- | :--- |
| Sistema operativo | `Windows 11` |
| Versión de KiCad y ruta de `kicad-cli` | `10.0.6 — C:\Program Files\KiCad\10.0\bin\kicad-cli.exe` |
| Agente y modelo | `Claude Code` |
| Fabricante y servicio | `JLCPCB, PCB de 2 capas, 1.6 mm, sin ensamblaje` |
| Fuentes autorizadas para descargar huellas que no estén en KiCad | `ninguna` (solo huellas oficiales de KiCad 10). Excepción v0.9: la huella del DAC es **propia del proyecto**, generada por `scripts/gen_huella_dac.py` con las medidas reales (no se descarga) |
| Fuentes autorizadas para CONSULTAR hojas de datos | Wiki y esquemático oficiales de **Waveshare RP2350-Plus**; ficha del **MSP2402** en **LCDwiki**. Se pueden guardar en `datasheets/` (URL de origen en `DECISIONES.md`). No descargar huellas ni software |

## 1. Objetivo del circuito

Consola portátil para niños de 6 a 10 años (KIDBOX) con juegos de desarrollo cognitivo y límite de sesión incorporado.
Es una **placa portadora de módulos** basada en el Game★Mite: un módulo Waveshare RP2350-Plus lee 8 botones, dibuja en una
pantalla TFT ILI9341 de 2.4" por SPI (brillo regulable por PWM) y envía audio por I2S a un DAC PCM5102A con salida de 3,5 mm
para audífonos. No se usan ni la SD ni el táctil de la pantalla. La batería LiPo se conecta directamente al cargador integrado
de la RP2350-Plus y no pasa por esta PCB. **No hay botón de reset en el frente:** se usan los botones BOOT y RESET que trae la
RP2350-Plus, accesibles por detrás (agujeros en la tapa de la carcasa). Formato horizontal.

```
[LiPo 2000 mAh]──>[RP2350-Plus]──SPI0 (GP6, GP3) + CS/DC/RST/LED──> [J3 TFT ILI9341 2.4"]
                    │   │  │
                    │   │  └──I2S (GP20, GP21, GP22)──> [J5 DAC PCM5102A] ──> jack 3,5 mm (audífonos)
                    │   └──cruceta GP16..GP19 · SELECT/START/B/A GP12..GP15──> 8 × [pulsador 6×6 ──> GND]
                    └──3V3_EN <── [SW10 interruptor ON/OFF, cara posterior]      (RUN sin conectar: reset propio del módulo)
```

## 2. Microcontrolador o módulo principal

| Dato | Valor |
| :--- | :--- |
| Modelo exacto | Waveshare **RP2350-Plus** (RP2350A, 16 MB flash, USB-C, cargador LiPo integrado). Respaldo: Raspberry Pi Pico (RP2040) del DEC, mismo pinout |
| Cómo va montado | Sobre **2 tiras hembra 1×20** (el módulo trae pines macho soldados) |
| Representación en el esquemático | **J1 y J2**, dos `Connector_Generic:Conn_01x20`. "U1.GPx" = pin del módulo en J1 (pines 1–20) o J2 (pines 21–40) |
| Cara y orientación | **Cara posterior (Bottom)**, USB-C hacia el **borde superior** de la placa, módulo centrado en x = 75 (v0.9). ⚠ Montado por detrás queda espejado. El USB-C llegó al borde en las pruebas 1:1 de la v0.7 y la v0.8 ✅ |
| Paso de pines / separación entre filas | 2.54 mm / **17.78 mm** (plano oficial; medido 17.3 interior y 18.6 exterior ✅) |
| Dimensiones del módulo | **21.0 × 51.55 mm medido** (51 mm de placa + USB-C que sobresale) ✅ |
| Pin 1 | GP0, junto al USB. Confirmado con la serigrafía de la pieza ("20" y "21" en el extremo opuesto al USB) ✅ |
| Conector de batería | **BAT**, 2 pines, paso 1.25 mm, en el extremo opuesto al USB-C. Con el USB-C arriba y los componentes hacia el observador: **⊕ izquierda, ⊖ derecha** (serigrafía) |
| Botones propios | **BOOT** y **RESET** en la cara de componentes, a **≈ 23 mm del extremo del USB-C** (centro; medido 24.5 mm al borde lejano). Quedan mirando hacia la tapa trasera |
| Pines que SÍ se pueden usar | GP0–GP22, GP26–GP28 |
| Pines PROHIBIDOS | VBUS, VSYS, ADC_VREF, 3V3 (solo como salida) |
| Huella KiCad | `Connector_PinSocket_2.54mm:PinSocket_1x20_P2.54mm_Vertical` ×2 (J1, J2) |

## 3. Alimentación

| Dato | Valor |
| :--- | :--- |
| Fuente de energía | **LiPo 103450, 3.7 V, 2000 mAh, 7.4 Wh** (del profesor). **Medida: 50.99 × 33.11 × 9.84 mm** ✅. Se conecta al conector BAT de la RP2350-Plus; **no pasa por esta PCB**. Va en un bolsillo de la **carcasa** (ajuste v0.9), no pegada a la placa |
| Corriente de carga | 1 A (ETA6096, R13 = 160 kΩ) = **0.5C** para 2000 mAh ✅. **El riesgo de la v0.6 queda resuelto.** La LiPo de 500 mAh ya no se usa |
| Cable de batería | Conector blanco de la batería (parece PH2.0) → **adaptador a 1.25 mm** (lo hace el profesor) **[PENDIENTE]**. **Verificar polaridad con multímetro antes de conectar** (rojo = + → ⊕ del BAT) |
| Tensión de entrada | 3.0–4.2 V (LiPo); 5 V por USB-C al cargar |
| Rieles | **3V3** desde el pin 36: pantalla (~80 mA máx.) + DAC (~20 mA). Total < 150 mA. Autonomía estimada ~10–13 h (por validar). **DAC probado con VIN = 3V3 (23-oct)** ✅: VIN = 3.26 V, A3V3 = 3.27 V, suena en estéreo con audífonos; VIN se queda en 3V3 |
| Encendido | Interruptor deslizante: **ON = 3V3_EN al aire; OFF = 3V3_EN a GND**. 3V3_EN tiene pull-up de 100 kΩ a VSYS en el módulo ✅. La consola carga estando apagada |
| Desacoplo | 100 nF junto a J3 (pantalla); 100 nF + 10 µF junto a VIN de J5 (DAC) |
| Puntos de prueba (v0.9) | **TP1 = +3V3** y **TP2 = GND**, junto a C2, accesibles con los módulos puestos |

## 4. Lista de componentes

| Ref | Cant. | Descripción / valor | THT/SMD | Cara | Símbolo · Huella KiCad | Notas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| J1, J2 | 2 | Tira hembra 1×20, 2.54 mm, para la RP2350-Plus | THT | Bottom | `Connector_Generic:Conn_01x20` · `Connector_PinSocket_2.54mm:PinSocket_1x20_P2.54mm_Vertical` | |
| J3 | 1 | Tira hembra 1×14 para la pantalla TFT ILI9341 2.4" | THT | Top | `Connector_Generic:Conn_01x14` · `Connector_PinSocket_2.54mm:PinSocket_1x14_P2.54mm_Vertical` | Orden de pines en la sección 5 |
| ~~J4~~ | — | **Eliminado en v0.7** | — | — | — | Sus patas caían en la zona de batería. La pantalla queda sostenida por J3 y el marco de la carcasa |
| J5 | 1 | Tira hembra 1×6 para el DAC GY-PCM5102 | THT | **Top** (v0.9) | `Connector_Generic:Conn_01x06` · `Connector_KIDBOX:GY-PCM5102_1x06_P2.54mm` (**huella propia**, v0.9) | Orden **confirmado** con la serigrafía ✅. La huella propia lleva los 6 pads de la tira (1.7 mm, taladro 1.0, pad 1 cuadrado = VIN) más el contorno del módulo y del jack y su courtyard. La genera `scripts/gen_huella_dac.py` en `KIDBOX/KIDBOX.pretty`; la librería se llama `Connector_KIDBOX` para cumplir el filtro de huellas del símbolo |
| SW1–SW8 | 8 | Pulsador táctil 6×6 mm, 4 patas, **alto 9.1 mm** (DEC) | THT | Top | `Switch:SW_Push` · `Button_Switch_THT:SW_PUSH_6mm` | Patas a 6.5 × 4.5 mm **confirmado** ✅. Capuchones 3D más adelante |
| ~~SW9~~ | — | **Eliminado en v0.7** (RESET del frente) | — | — | — | Se usa el RESET de la RP2350-Plus |
| SW10 | 1 | Interruptor deslizante 1P2T recto, 3 patas (cuerpo 8.7 mm, alto ~11 mm con palanca) | THT | **Bottom** | `Switch:SW_SPDT_312` · `Button_Switch_THT:SW_Slide-03_Wuerth-WS-SLTV_10x2.5x6.4_P2.54mm` | **Paso 2.54 mm confirmado en protoboard (14-oct)** ✅ con el interruptor metálico pequeño (el negro grande queda descartado). Se usa el símbolo oficial `SW_SPDT_312` (común = pin 1) para que el **pad central** de la huella sea el **común** (PWR_EN); pad 2 a GND, pad 3 sin conectar. Si el paso resulta 2.0 mm, volver a la huella CK `SW_Slide_SPDT_Straight_CK_OS102011MS2Q` con el símbolo `SW_SPDT` |
| ~~C1~~ | — | **Eliminado en v0.7** (era el del RESET) | — | — | — | |
| C2 | 1 | 100 nF cerámico (desacoplo pantalla) | THT | Top | `Device:C` · `Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm` | Vertical junto al pin 1 de J3. **Paso de patas 5 mm, medido (21-oct)** ✅ |
| C3 | 1 | 100 nF cerámico (desacoplo DAC) | THT | **Top** | `Device:C` · ídem C2 (paso 5 mm, medido ✅) | Vertical entre SELECT y el DAC, sobre C4 |
| C4 | 1 | 10 µF electrolítico **25 V** (el disponible; cualquiera ≥16 V sirve) | THT | **Top** | `Device:C_Polarized` · `Capacitor_THT:CP_Radial_D4.0mm_P1.50mm` (v0.9) | Polaridad. **Medido (21-oct)** ✅: Ø ≈ 4 mm, alto ≈ 7–8 mm, paso ≈ 1.5 mm. Desde la v0.9 la huella coincide con la pieza (no hay que abrir las patas). A la altura de VIN |
| TP1, TP2 | 2 | Puntos de prueba +3V3 y GND | THT (pad) | Top | `Connector:TestPoint` · `TestPoint:TestPoint_THTPad_D2.0mm_Drill1.0mm` | v0.9 (sugerencia del profesor 3.3). No se compran; excluidos de la BOM y de los archivos de posición (igual que la huella oficial) |
| BT1 | 1 | Batería LiPo 103450 3.7 V 2000 mAh | — | — (detrás, sin huella) | `Device:Battery_Cell` (excluido de la placa) | v0.9. Solo en el esquemático y la BOM: va al conector BAT del RP2350-Plus, no a esta PCB. Pines sin conectar |
| H1–H4 | 4 | Agujero M2 (fijación a la carcasa) | NPTH 2.2 mm | — | `Mechanical:MountingHole` (in_bom no) · `MountingHole:MountingHole_2.2mm_M2` | |
| ~~H5, H6~~ | — | **Eliminados (Fase 2, 14-oct)** | — | — | — | El borde del agujero quedaba a 0.09 mm de J3: un tornillo tocaría la tira. La pantalla se sujeta con J3 y la carcasa (marco frontal + soporte impreso bajo su lado derecho, más adelante) |

Regla para SMD: **no hay componentes SMD.**

Referencias: **no se re-anota** (v0.9). C1, J4 y SW9 no existen porque se eliminaron en la v0.7; el README lo explica.
La lista de compra completa (módulos, batería, capuchones, tornillos, con estado y cantidades) está en `KIDBOX/BOM_compra.csv`.

## 5. Conexiones (netlist funcional)

Numeración de pines de la RP2350-Plus = Pico (**confirmado** con la hoja oficial y la pieza): GP0=1, GP1=2, GND=3, GP2=4, GP3=5,
GP4=6, GP5=7, GND=8, GP6=9, GP7=10, GP8=11, GP9=12, GND=13, GP10=14, GP11=15, GP12=16, GP13=17, GND=18, GP14=19, GP15=20,
GP16=21, GP17=22, GND=23, GP18=24, GP19=25, GP20=26, GP21=27, GND=28, GP22=29, RUN=30, GP26=31, GP27=32, GND=33 (AGND),
GP28=34, ADC_VREF=35, 3V3=36, 3V3_EN=37, GND=38, VSYS=39, VBUS=40. J1 = pines 1–20, J2 = pines 21–40.

Orden de pines de J3 (pantalla, LCDwiki MSP2402 ✅): 1 VCC, 2 GND, 3 CS, 4 RESET, 5 DC, 6 SDI(MOSI), 7 SCK, 8 LED, 9 SDO(MISO),
10 T_CLK, 11 T_CS, 12 T_DIN, 13 T_DO, 14 T_IRQ.

Orden de pines de J5 (DAC GY-PCM5102, **confirmado con la serigrafía** ✅): 1 VIN (pad cuadrado), 2 GND, 3 LCK, 4 DIN, 5 BCK, 6 SCK.

| Red | Desde (ref.pin) | Hasta (ref.pin) | Tipo | Requisito |
| :--- | :--- | :--- | :--- | :--- |
| LCD_CS | U1.GP0 | J3.3 (CS) | señal | |
| LCD_RST | U1.GP1 | J3.4 (RESET) | señal | |
| LCD_DC | U1.GP2 | J3.5 (DC) | señal | |
| LCD_MOSI | U1.GP3 | J3.6 (SDI) | señal | SPI0 TX |
| LCD_SCK | U1.GP6 | J3.7 (SCK) | señal | SPI0 SCK |
| LCD_LED | U1.GP26 | J3.8 (LED) | señal | PWM de brillo, conexión directa (≈ 2.6 mA por el transistor del módulo) |
| I2S_BCK | U1.GP20 | J5.5 (BCK) | señal | BCK y LCK consecutivos |
| I2S_LRCK | U1.GP21 | J5.3 (LCK) | señal | |
| I2S_DIN | U1.GP22 | J5.4 (DIN) | señal | |
| DAC_SCK | J5.6 (SCK) | GND | GND | Reloj interno del DAC |
| BTN_DOWN | SW1.1 | U1.GP16 | señal | pull-up interno |
| BTN_LEFT | SW2.1 | U1.GP17 | señal | |
| BTN_UP | SW3.1 | U1.GP18 | señal | |
| BTN_RIGHT | SW4.1 | U1.GP19 | señal | |
| BTN_SELECT | SW5.1 | U1.GP12 | señal | |
| BTN_START | SW6.1 | U1.GP13 | señal | |
| BTN_B | SW7.1 | U1.GP14 | señal | |
| BTN_A | SW8.1 | U1.GP15 | señal | |
| PWR_EN | SW10.común (pad central) | U1.3V3_EN | señal | Una pata extrema a GND (= apagado), la otra sin conectar. **OFF = pad 2 (a GND)**: continuidad medida el 21-oct ✅ (la palanca une el común con la pata de su lado) |
| 3V3 | U1.3V3 | J3.1 (VCC), J5.1 (VIN), C2, C3, C4.+, TP1 | potencia | Pista de 0.5 mm (0.25 mm solo en el cruce entre J2.31 y J2.30). DAC probado con 3V3 el 23-oct ✅ |
| GND | U1.GND (todos, incluido el pin 33) | J3.2, J5.2, J5.6, SW1–SW8.2, C2–C4, SW10, TP2 | GND | Plano en B.Cu |

Sin conectar (`no_connect`):
- J3.9 (SDO/MISO) y J3.10–J3.14 (táctil).
- RP2350-Plus: **RUN (pin 30)**, GP4, GP5, GP7, GP8–GP11, GP27, GP28, VBUS, VSYS, ADC_VREF.
- BT1 (+ y −): la batería está en el esquemático solo para la BOM.

Con J1/J2 como conectores genéricos, el ERC necesita `PWR_FLAG` en 3V3 y en GND.

## 6. Mecánica y posiciones

> Medidas de todos los módulos **confirmadas** con las piezas. Las posiciones siguen las decisiones del equipo del 23–26 oct
> (simetría, imagen centrada, DAC adelante) y el **ajuste tras la prueba 1:1 de la v0.9** (26-oct): placa 150 × 70, controles
> compactos con capuchones Ø9, DAC 5 mm más arriba, franja para el muro de la carcasa y batería en la carcasa.

| Dato | Valor |
| :--- | :--- |
| Dimensiones exteriores | **150 × 70 mm** (ajuste v0.9). Se acepta el sobrecosto de JLCPCB por superar 100 × 100 mm |
| Eje de simetría | **x = 75**: centro de la imagen, del RP2350-Plus (y su USB-C) y del jack; controles en espejo |
| Forma / radio de esquinas | Rectángulo / 4 mm |
| Origen | Esquina superior izquierda = (0,0), Y hacia abajo, **visto desde el frente** |
| Referencia de las coordenadas | **Centro del cuerpo** de cada pieza |
| Rotaciones | **Manda la descripción geométrica** (qué pin queda dónde, visto desde el frente). Verificar la posición de los pads |
| Agujeros de montaje | M2 NPTH 2.2 mm en (4, 4), (146, 4), (4, 66), (146, 66) |
| Alturas | Top: pulsadores 9.1 mm; pantalla ≈ 17 mm sobre la placa sobre la tira hembra (medido: módulo 6 mm + pines 10 mm; el lector SD baja ≈ 3 mm por detrás del módulo); **DAC sobre socket ≈ 18.6 mm** (tira hembra 8.5 + plástico de la tira macho 2.5 + placa 1.6 + jack ≈ 6, provisorio; la placa del DAC queda a ≈ 11 mm; las puntas de la tira macho sobresalen ≈ 2.5 mm, menos que el jack). Bottom: módulos sobre tira hembra ≈ 12 mm; SW10 ≈ 11 mm. **Grosor sin carcasa ≈ 18.6 + 1.6 + 12 ≈ 32 mm** (con el DAC soldado directo, ≈ 31 mm). La batería (9.84 mm) va en la carcasa |
| Zona prohibida Top | Bajo el módulo de pantalla (x 32.4–109.6, y 3.6–46.4) no van componentes salvo J3; **sí** pistas y soldaduras de piezas de la cara Bottom. Bajo el DAC (x 48.6–80.45, y 51.1–68.6) solo J5 |
| **Franja del muro (Top)** | Entre el borde inferior de la pantalla (y 46.36) y el contorno del DAC (y 51.1): **4.74 mm** en planta, en x 48.6–80.45. Sin componentes ni patas de piezas de la cara Top (solo pistas). El **muro de la carcasa es colgante** desde la tapa frontal: ≈ 2 mm de ancho, centrado en **y = 48.73**, con altura útil entre **9 y 18 mm sobre la PCB** (lo que debe tapar es la placa del DAC, a ≈ 11–18 mm). Termina **≥ 4 mm sobre la PCB** para pasar sobre las soldaduras de J2.21/J2.22 y J1.19/J1.20 (≈ 2 mm de alto), que caen dentro de la franja. **No apoyar el muro sobre esas soldaduras.** Está dibujado en F.Fab |
| **Batería (en la carcasa)** | **No va pegada a la PCB**: va en un **bolsillo de la carcasa con fondo de plástico** entre la LiPo y la placa, con sujeción propia y un canal para el cable hasta el conector BAT del módulo. En B.SilkS queda solo como **referencia**: rectángulo x 88.0–123.5, y 4.0–62.0 (al lado derecho del RP2350-Plus), con "BATERÍA 103450 / va en la carcasa, no pegar a la PCB" y una flecha hacia el conector BAT. **En esa zona no van componentes altos de la cara Bottom; las patas THT sí se permiten** (las de START caen ahí) |
| Bordes libres | Superior x 70.7–79.65 (USB-C; abertura de carcasa x ≈ 68–82). Inferior bajo el jack, x 72.65–77.35 (boca al ras de y = 70; el jack queda ≈ 13–19 mm sobre la placa) |
| Espesor | 1.6 mm |

El boceto `datasheets/layout_propuesto.svg` corresponde a la v0.6 y queda como **histórico**: la referencia de posiciones es esta sección
y las imágenes de `KIDBOX/verificacion/`.

**Pantalla** (plano MSP2402 de LCDwiki; **confirmada con la pieza el 15-oct** ✅: 77 × 42 mm, J3 a la izquierda, pin 1 VCC arriba, mismo orden de pines): placa **77.18 × 42.72 mm**, horizontal, **sin girar**, tira de 14 pines (**J3**) **vertical en el borde corto izquierdo**, a 2.00 mm del borde, **pin 1 (VCC) arriba** ✅.
- **La IMAGEN va centrada en x = 75, no el módulo.** Medido con la pieza encendida (marco 320×240): del borde del módulo del lado
  de J3 a los píxeles hay 19 mm y del borde opuesto 11 mm; el área activa está centrada en vertical. El centro de la imagen queda
  **4.0 mm** corrido respecto del centro del módulo, hacia el lado opuesto a J3.
- Módulo centrado en **(71, 25)** → x 32.41–109.59, y 3.64–46.36. **J3 en x = 34.41**, pines y 8.49–41.51.
- Imagen dibujada con el dato del panel, **48.96 × 36.72 mm**, centrada en (75, 25) → x 50.52–99.48, y 6.64–43.36.
  (19 + 11 + 48.96 = 78.96 mm, 1.8 mm más que el módulo medido: el centro no cambia, por eso se usa el dato del panel.)
- Firmware: `tft.setRotation(3)`.
- El lector SD (por detrás del módulo, mitad derecha vista de frente) y el táctil quedan sin usar. Agujeros del módulo Ø3.2 a
  67.26 × 36.72 entre centros: **no se usan en la PCB**.

**RP2350-Plus** (cara Bottom, vista "a través" desde el frente): vertical, USB-C arriba, **centrado en x = 75**: placa en
x 64.5–85.5, y ≈ 0.55–51.55. Columnas en **x = 66.11 (J2) y 83.89 (J1)**. Pin 1 (GP0) arriba a la derecha: pines 1–20 en la columna
derecha de arriba hacia abajo; pines 21–40 en la columna izquierda de abajo hacia arriba. **USB-C según el plano oficial**: 8.95 mm de
ancho, a 6.2 mm del borde izquierdo del módulo visto de frente → x 70.7–79.65 (0.15 mm descentrado respecto del módulo).
Conector BAT en el extremo inferior del módulo (y ≈ 48–51); la flecha de la serigrafía trasera lo señala.

**DAC GY-PCM5102** (**cara Top**): medidas reales **31.85 × 17.5 mm** (ancho medido 17.3–17.5); la tira de 6 pines está
en un **lado corto**, a 1.5 mm del borde y centrada a lo ancho; el **eje del jack está a 24.9 mm de la columna**; el jack mide
**4.7 mm de ancho × 14 mm de largo** y **sobresale 1.4 mm** del borde largo; alto del jack sobre la placa del DAC ≈ 6 mm (provisorio).
- Va **adelante**, en la franja bajo la pantalla, con los componentes del módulo hacia el frente y la tira macho hacia la PCB.
- **Jack con eje en x = 75** y la **boca al ras del borde inferior** (y = 70). Visto de frente: pines a la izquierda (hacia la
  cruceta), jack a la derecha, boca abajo, **VIN abajo** (el pin más cercano a la boca), SCK arriba.
- **J5 en x = 50.1**, pines de **y = 53.5 (pin 6, SCK) a y = 66.2 (pin 1, VIN)**. Módulo en **x 48.6–80.45, y 51.1–68.6**; jack en
  x 72.65–77.35, y 56–70. Separación con la pantalla: **4.74 mm** (franja del muro); no se superponen en planta.
- **J2.21 (cara Bottom) queda con su cobre a 0.07 mm del contorno del DAC** (fuera de él). No es violación: J2 está en la cara Bottom
  y la huella de J5 en la Top, y el agujero de J2.21 queda 0.13 mm fuera del courtyard de J5. Físicamente no chocan: la soldadura de
  J2.21 mide ≈ 2 mm y la placa del DAC está a ≈ 11 mm sobre la PCB.
- **Huella propia** `Connector_KIDBOX:GY-PCM5102_1x06_P2.54mm` (pads de la tira + contorno del módulo y del jack + courtyard).
- **Nada bajo el DAC:** ninguna pata THT dentro de su contorno salvo J5, por si el módulo se suelda directo a la placa (sin tira
  hembra) para bajar el grosor. Solo pasan pistas de F.Cu y el plano de B.Cu.
- **C4 a la altura de VIN**, entre SELECT y el DAC: pad + en (46.55, 66.2), pad − en (45.05, 66.2). **C3 vertical justo encima**:
  pad +3V3 en (45.8, 62.6), pad GND en (45.8, 57.6). Los dos fuera del contorno del DAC (courtyards: SELECT hasta x 43.3, C3 44.3–47.3,
  C4 43.5–48.1, DAC desde 48.3).
- Puentes del reverso del módulo: **FLT, DEMP y FMT = L; XSMT = H** (3.21 V). En este módulo **H3L controla FMT y H4L controla XSMT**;
  venían abiertos. Volumen por software, con máximo limitado.

**Controles**: simétricos respecto de x = 75 y compactos (ajuste v0.9). Capuchones **redondos Ø9**: ≥ 1.5 mm de aire entre el
círculo de Ø9 y el contorno de cualquier módulo (`gen_pcb.py` lo comprueba). Con brazos de 9 mm, entre las columnas de pads de la
cruceta quedan solo 0.5 mm; el ruteo usa los canales horizontales entre filas, y UP entra por el borde izquierdo.

Posiciones fijas (centro del cuerpo):

| Ref | x (mm) | y (mm) | Cara | Por qué es fija |
| :--- | :--- | :--- | :--- | :--- |
| SW3 (UP) | 16.5 | 30 | Top | Cruceta, centro (16.5, 39), brazos de 9 mm |
| SW1 (DOWN) | 16.5 | 48 | Top | Cruceta |
| SW2 (LEFT) | 7.5 | 39 | Top | Cruceta; capuchón a 3.0 mm del borde izquierdo |
| SW4 (RIGHT) | 25.5 | 39 | Top | Cruceta; capuchón a **2.41 mm** de la pantalla (mínimo de la placa) |
| SW7 (B) | 129 | 43.5 | Top | Espejo de la cruceta: punto medio de A/B en x = 133.5, diagonal de 9 mm |
| SW8 (A) | 138 | 34.5 | Top | A arriba a la derecha |
| SW5 (SELECT) | 38.5 | 62 | Top | Franja inferior, simétrico con START. Capuchón a 5.6 mm del DAC |
| SW6 (START) | 111.5 | 62 | Top | Franja inferior. Sus patas caen en la zona de referencia de la batería (permitido) |
| SW10 (ON/OFF) | 47.5 | 8 | **Bottom** | Arriba a la izquierda por detrás, fuera de la zona de los índices. Pad 2 (GND = OFF) en x = 50.04, pad 3 en x = 44.96 |
| J3 (pantalla 1×14) | 34.41 | 25 | Top | Borde izquierdo del módulo de pantalla, pin 1 arriba ✅ |
| J1+J2 (RP2350-Plus) | centro (75, 26.05) | — | **Bottom** | USB-C en el borde superior; columnas x = 83.89 / 66.11 |
| J5 (DAC) | columna en **x = 50.1**, y = 53.5–66.2 | — | **Top** | Jack con eje en x = 75, boca en y = 70 |
| TP1 / TP2 | 27.3 | 8.49 / 13.49 | Top | Puntos de prueba +3V3 / GND junto a C2 (C2 en x = 30.6) |

## 7. Fabricante y reglas de diseño (DFM)

| Parámetro | Mi valor | Mínimo del fabricante |
| :--- | :--- | :--- |
| Número de capas | `2` | — |
| Ancho mínimo de pista (señal) | `0.25 mm` | `0.127 mm` |
| Ancho de pistas de potencia | `0.50 mm` | — |
| Separación mínima cobre-cobre | `0.20 mm` | `0.127 mm` |
| **Pista o 3V3 contra pad de otra red** (v0.9, `KIDBOX.kicad_dru`) | `0.29 mm`, como **error** del DRC (reglas `3V3_lejos_de_pads` y `pista_lejos_de_pad_ajeno`, sugerencias del profesor 3.1 y 3.2) | — |
| Vía: diámetro / taladro | `0.60 / 0.30 mm` | `0.45 / 0.20 mm` |
| Vías | **Tapadas (tented)**: obligatorio en la zona de batería | — |
| Anillo anular THT | `≥ 0.35 mm` con **huellas oficiales sin modificar** (la huella propia del DAC usa los mismos pads que la tira oficial) | `0.15 mm` |
| Cobre a borde de placa | `0.30 mm` | `0.20 mm` |
| Agujero a agujero / agujero a cobre | `0.25 mm` / `0.25 mm` | — |
| Serigrafía: trazo / alto de texto | `0.15 / 1.0 mm` (rótulos de botones `0.18 / 1.2 mm`) | `0.15 mm` |
| Acabado / máscara / ensamblaje | `HASL sin plomo` / `verde` / `No` | — |

## 8. Estrategia de ruteo

| Dato | Valor |
| :--- | :--- |
| Capa de señales preferente | `F.Cu` |
| Plano de masa | `B.Cu continuo`, con **alivios térmicos** en todos los pads de GND |
| ¿Vías? | Sí, cuando hagan falta (la v0.9 no tiene ninguna) |
| Pistas bajo módulos | **Permitidas** en ambas caras (los módulos van 8.5 mm por encima, sobre tiras hembra) |
| Ancho por tipo de red | Señal 0.25 mm · 3V3 0.5 mm (0.25 mm solo en el cruce entre J2.31 y J2.30) |
| Pistas entre pines | **J3 y J5: ninguna** (v0.9). **J2:** el haz SPI (5 pistas), +3V3 (entre J2.31 y J2.30) e I2S_LRCK (entre J2.30 y J2.29), todas a 0.295 mm de cada pad. El orden de J2 (DIN, LRCK, BCK) y el de J5 (BCK, DIN, LCK) están rotados y VIN cierra la columna de J5: sin vías, una pista I2S tiene que pasar entre pines, y se eligió J2 |
| Redes críticas | SPI (GP6/GP3) e I2S (GP20/21/22) lo más cortas posible y separadas entre sí |
| Autorouter | Solo si el agente no logra rutear en 2 intentos |
| ¿Reasignar pines? | Solo los botones, a pines libres; nunca SPI, pantalla ni I2S |
| Ángulos | `45° y 90°` |

## 9. Serigrafía y marcas

- F.SilkS: nombre de cada botón (UP, DOWN, LEFT, RIGHT, A, B, SELECT, START) en **1.2 mm / 0.18 mm** (v0.9). **Sin "RESET"** (ya no hay botón en el frente).
- F.SilkS: contorno del módulo de pantalla, **contorno de la imagen (48.96 × 36.72, centrada en x = 75)** y pin 1 de J3.
- F.SilkS: contorno del DAC y del jack (en la huella de J5), "VIN" y "GND" junto a J5, y "3V3" / "GND" junto a TP1 / TP2.
- B.SilkS: contorno de la RP2350-Plus **con la forma del USB-C**, el **pin 1 marcado en J1 y J2**, la posición de **BOOT/RESET** del módulo y "VISTA POSTERIOR — FILAS ESPEJADAS".
- B.SilkS: junto a SW10, **"OFF" sobre el pad 2 (GND, x 52.54) y "ON" sobre el pad 3 (x 47.46)**: visto desde atrás, OFF a la izquierda y ON a la derecha. La continuidad está medida (21-oct ✅): la palanca une el común con la pata de su lado.
- B.SilkS: **contorno de referencia de la batería** con "BATERÍA 103450 / va en la carcasa, no pegar a la PCB" y una flecha hacia el conector BAT del módulo, y el cajetín "KIDBOX v0.9 — 150 × 70 mm — 1.6 mm — 2 capas".
- F.Fab: línea del **muro de la carcasa** al centro de la franja pantalla–DAC (y = 48.73), con su descripción.
- Texto "KIDBOX v0.9 2026 — basado en Game★Mite de Thomas Hugo Williams (CC BY 4.0)" (o "Game*Mite" si no sale la ★), fuera de los módulos y de la zona de batería (en el frente, entre el DAC y START).

## 10. Entregables que espero del agente

- [ ] Proyecto KiCad completo que abre sin errores en KiCad `10.0`.
- [ ] ERC y DRC con 0 errores, mínimos DFM de la sección 7 escritos en el proyecto.
- [ ] `BOM.csv`, `BOM_compra.csv`, `netlist.csv`, `DECISIONES.md`, `README.md` (con el **orden de soldadura**: primero las piezas de la cara Bottom, J1, J2, SW10, después las de Top).
- [ ] Imágenes de verificación (`verificacion/`).
- [ ] Gerbers, taladros, zip y PDF 1:1 (A4 y Carta) con la versión **v0.9**, marcados como **preliminares** hasta la prueba 1:1 del ajuste 150 × 70.
- [ ] Carpeta de entrega con la especificación, `DECISIONES.md` y los scripts (`scripts/gen_entrega.py`).

## 11. Decisiones tomadas y pendientes

Decisiones vigentes:
- Base Game★Mite v1.3.2. RP2350-Plus (respaldo Pico). Firmware en Arduino IDE.
- Pantalla TFT ILI9341 2.4" SPI (AFEL, MSP2402), sin SD ni táctil, brillo por PWM (GP26). Firmware con `tft.setRotation(3)`.
- Audio por DAC PCM5102A (I2S) con jack de 3,5 mm; sin parlante. VIN = 3V3 (probado el 23-oct). **Volumen por software con máximo limitado.**
- 8 pulsadores 6×6 del DEC; capuchones 3D redondos Ø9. Formato horizontal. Todo THT, 2 capas.
- USB-C arriba y jack abajo, los dos centrados en x = 75; ON/OFF por detrás, arriba a la izquierda. Batería en la carcasa. Cruceta en GP16–GP19.
- Fase 0 y Fase 1: ver historial en git (v0.5 y v0.6).

Cambios v0.7 (14-oct-2026, decididos por el alumno tras medir las piezas):
1. **Se elimina el RESET del frente** (SW9 y C1). RUN queda sin conectar. Se usan los botones BOOT/RESET de la RP2350-Plus por detrás.
2. **Batería LiPo 103450 de 2000 mAh** (50.99 × 33.11 × 9.84 mm): carga a 0.5C, el riesgo de la v0.6 queda resuelto.
3. **Layout reordenado** para la batería: pantalla sin girar (J3 a la izquierda en x ≈ 38.41, pin 1 arriba); **se elimina J4**; zona de batería x 88.0–123.5, y 4–62; **SW10 a (134, 8)**; **B a x = 128**.
6. **Fase 2 (revisión del alumno, 14-oct):** se eliminan H5/H6 (chocaban con J3); SELECT y START pasan a x = 66.5 y 83.5; se aceptan J5 con VIN a la derecha visto de frente y PWR_EN por el borde superior.
4. **SW10 con huella de paso 2.54 mm** (`SW_Slide-03_Wuerth-WS-SLTV_10x2.5x6.4_P2.54mm`), **confirmado en protoboard el 14-oct** (entra directo en paso de 2.54 mm).
5. J5 (orden de pines), RP2350-Plus (medidas y pinout), pulsadores (6.5 × 4.5 mm, alto 9.1 mm) y DAC (31.85 × 17.78 mm; 17.5 en la v0.9) **confirmados con las piezas**.
7. **DAC horizontal (revisión en KiCad, 14-oct):** con el DAC vertical la boca del jack apuntaba hacia el interior (SELECT/START y la batería),
   porque sale por un lado largo del módulo. Se gira 90°: J5 en columna junto a J2 y jack al borde inferior en x ≈ 33. Reemplaza lo
   aceptado en el punto 6 sobre J5. Se evaluó el CJMCU-1334 (UDA1334A), con el jack en el lado corto, pero se descarta: su salida es de
   línea (~0.9 V rms frente a ~2.1 V rms del PCM5102A) y, según el profesor, uno de los dos suena muy bajo con audífonos. Queda como respaldo.
Cambios v0.8 (21-oct-2026, decididos por el alumno en la revisión de la Fase 4):
8. **Nada bajo el DAC y C3 lejos del borde:** pantalla (J3 y C2) **3 mm más arriba** (J3 centrada en y = 25, pines
   y 8.49–41.51); DAC (J5, contorno y jack) **3 mm hacia la cruceta** (J5 en x = 56, jack centrado en x ≈ 30); **C3 vertical entre J5 y
   SELECT** (pad +3V3 a la altura de VIN). Así ninguna pata queda bajo el DAC, por si se suelda directo para bajar el grosor, y C3 deja el
   borde inferior.
Cambios v0.9 (26-oct-2026, correcciones del profesor del 22-oct y decisiones del equipo del 23–26 oct; posiciones en la sección 6):
9. *(Coordenadas 9–12 reemplazadas por el ajuste del punto 15.)* **Placa 155 × 75 mm**, esquinas r = 4, agujeros M2 en (4, 4), (151, 4), (4, 71), (151, 71). Eje de simetría x = 77.5.
10. **Imagen de la pantalla centrada** en x = 77.5 (módulo en x = 73.5, J3 en x = 36.91). **RP2350-Plus centrado** (columnas 68.61 / 86.39)
    y zona de batería corrida igual (x 90.5–126.0).
11. **DAC adelante** con huella propia, jack centrado con la boca al ras del borde inferior; C3 y C4 junto a VIN, fuera del DAC.
12. **Controles simétricos** (propuesta P2 del estudio ergonómico, adaptada): cruceta en (18, 44), A/B en espejo, SELECT/START en
    (41, 67) / (114, 67). Capuchones redondos Ø10 con ≥ 1.5 mm de aire a los módulos. **SW10 atrás en (50, 8)**.
13. Sugerencias del profesor aplicadas: 3V3 sin pasar entre pines de J3 y a 0.25 mm en J2; LRCK fuera de entre los pines de J5; BCK a
    ≥ 0.29 mm de J2.21; reglas de 0.29 mm en `KIDBOX.kicad_dru`; **C4 con `CP_Radial_D4.0mm_P1.50mm`**; **TP1/TP2**; **BT1** excluida de
    la placa; PWR_EN lejos del borde; rótulos de botones a 1.2/0.18; versión v0.9 en serigrafía, cajetín, README y zip; BOM de compra
    completa; tabla de archivos del README; carpeta de entrega.
14. No se re-anotan las referencias (C1, J4 y SW9 faltan): basta la nota del README.
15. **Ajuste tras la prueba 1:1 (26-oct, mismo PR):** placa **150 × 70** (agujeros en (4, 4), (146, 4), (4, 66), (146, 66)), eje
    x = 75; imagen centrada en x = 75 (módulo x 32.41–109.59, J3 en x = 34.41); controles compactos con capuchones **Ø9**: cruceta
    centro (16.5, 39) con brazos de 9 mm, A (138, 34.5) / B (129, 43.5), SELECT/START (38.5, 62) / (111.5, 62); DAC 5 mm más arriba
    (J5 en x = 50.1, jack con eje en x = 75 y boca en y = 70); **franja de 4.74 mm para un muro colgante** de la carcasa entre
    pantalla y DAC; RP2350-Plus en 66.11 / 83.89; SW10 en (47.5, 8); **batería en la carcasa** (zona solo de referencia: patas THT
    permitidas, sin componentes altos). El resto de la v0.9 se mantiene.

Pendientes (antes de fabricar):
- **Prueba 1:1 del ajuste 150 × 70:** imprimir los PDF nuevos al 100 % (A4 o Carta), medir 150 × 70 mm y apoyar las piezas reales.
- **Carcasa:** muro colgante entre pantalla y DAC (≈ 2 mm, termina ≥ 4 mm sobre la PCB) y bolsillo de la batería con fondo de plástico.
- **Alto real del jack** sobre la placa del DAC (hoy ≈ 6 mm, provisorio): define la abertura de la carcasa.
- Pantalla: falta solo revisar el **puente J1** del módulo (alimentación a 3.3 V); no afecta a la PCB.
- Adaptador y polaridad de la batería (profesor).
- Con la placa armada (sugerencia del profesor 3.5): medir SW10 en ON/OFF, la corriente de la batería en OFF y TP1–TP2 ≈ 3.3 V.

Cerrados en la v0.9: DAC probado con 3V3 y puentes (23-oct) ✅; medidas del DAC (31.85 × 17.5, columna, jack) ✅; RP2350-Plus 21.0 × 51.55
y filas a 17.78 ✅; continuidad de SW10 ✅; C2/C3/C4 medidos ✅.

## 12. Restricciones adicionales para el agente

- No usar componentes SMD. No modificar huellas oficiales. No descargar huellas de internet (la del DAC es propia, generada por script).
- No mover las posiciones fijas de la sección 6 sin preguntar.
- No reasignar pines de SPI, pantalla ni I2S.
- **Zona de batería** (Bottom, x 88.0–123.5, y 4.0–62.0, solo referencia: la batería va en la carcasa): no colocar componentes altos de la cara Bottom; las patas THT se permiten.
- **Franja del muro** (Top, y 46.36–51.1, x 48.6–80.45): sin componentes ni patas de piezas de la cara Top; solo pistas.
- Anotar toda decisión no escrita aquí en `DECISIONES.md`.
- No generar Gerbers "para fabricar" mientras quede un pendiente que afecte a la placa (hoy: la prueba 1:1 del ajuste 150 × 70); hasta entonces van marcados como **preliminares**.
