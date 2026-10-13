# ESPECIFICACION.md — Especificación de la PCB (BORRADOR v0.1)

> **Estado: BORRADOR para revisión del equipo.** Basado en `../Diseno_Fusion_KIDBOX.md` (Game★Mite + RP2350-Plus + DEC).
> Todo lo marcado **[MEDIR]** o **[VERIFICAR]** debe completarse con las piezas en la mano antes de la Fase 0
> (la guía del profe: "lo que dejes vacío, el agente lo inventará"). Las coordenadas son una **[PROPUESTA]** del layout
> y deben validarse con el boceto en papel milimetrado.

Nombre del proyecto: `KIDBOX_UNIVERSAL`

Autor: `Equipo KIDBOX (J. Becerra, B. Fernández, A. Medina, D. Pizarro)`   Fecha: `13-oct-2026`   Versión: `0.1`

---

## 0. Entorno

| Dato | Valor |
| :--- | :--- |
| Sistema operativo | `Windows 11` |
| Versión de KiCad y ruta de `kicad-cli` | `10.0.6 — C:\Program Files\KiCad\10.0\bin\kicad-cli.exe` |
| Agente y modelo | `Claude Code — Opus (Fase 2), Sonnet (resto)` |
| Fabricante y servicio | `JLCPCB, PCB de 2 capas, 1.6 mm, sin ensamblaje` |
| Fuentes autorizadas para descargar huellas que no estén en KiCad | `ninguna` (usar tiras de pines/sockets genéricos para los módulos) |

## 1. Objetivo del circuito

Consola portátil para niños de 6 a 10 años (KIDBOX) con juegos de desarrollo cognitivo y límite de sesión incorporado.
Es una **placa portadora**: un módulo Waveshare RP2350-Plus lee 8 botones + reset, dibuja en una pantalla SPI y genera
audio PWM que amplifica un módulo PAM8403. La PCB es **universal**: admite una pantalla TFT ILI9341 2.8" (Alt. 2) o una
IPS 1.3" ST7789 (Alt. 1) en la misma zona; se suelda solo el conector de la pantalla usada. La energía viene de una LiPo
3.7 V 500 mAh conectada al cargador integrado de la RP2350-Plus. Basada en el Game★Mite (CC BY 4.0).

```
                       +--> [J2 ILI9341 2.8" + J6 SD]  (Alt. 2)
[LiPo 500 mAh]-->[RP2350-Plus]--SPI0--+
   (MX1.25)       |   |   |           +--> [J3 IPS 1.3" ST7789] (Alt. 1)
                  |   |   +--GP8..GP15--> 8 x [pulsador --> GND]
                  |   +--GP20 PWM--> [filtro RC]--> [pot. volumen]--> [PAM8403]--> [parlante 8 Ω]
                  +--3V3_EN <-- [interruptor ON/OFF]      RUN <-- [pulsador RESET]
```

## 2. Microcontrolador o módulo principal

| Dato | Valor |
| :--- | :--- |
| Modelo exacto | Waveshare **RP2350-Plus**, RP2350A, 16 MB flash, USB-C, cargador LiPo integrado. Respaldo: Raspberry Pi Pico (RP2040) del DEC, mismo pinout |
| Cómo va montado | Sobre **2 tiras hembra 1×20** (el módulo viene con pines macho soldados, confirmado por el profe) |
| Cara y orientación | **Cara posterior (Bottom)**, USB-C hacia el **borde inferior** de la placa. ⚠ Montado por detrás queda espejado: verificar fila por fila contra la foto |
| Paso de pines | 2.54 mm |
| Separación entre filas medida con calibre | **[MEDIR]** (nominal Pico: 17.78 mm) |
| Pines por fila y pin 1 | 20 por fila; pin 1 = GP0, junto al USB **[VERIFICAR en la serigrafía]** |
| Fuente del pinout | **[ADJUNTAR]** `datasheets/rp2350plus_pinout.jpg` (foto de la serigrafía) + diagrama del wiki de Waveshare |
| Pines que SÍ se pueden usar | GP0–GP22, GP26–GP28 (26 GPIO) |
| Pines PROHIBIDOS y por qué | VBUS, VSYS (alimentación), 3V3 (salida, solo para alimentar), ADC_VREF, GP23–GP25/GP29 si son internos **[VERIFICAR]** |
| ¿Trae regulador, USB y desacoplos? | Sí: regulador buck-boost (MP28164), USB-C, cargador LiPo y desacoplos propios |
| Huella KiCad | No existe para la RP2350-Plus: usar `Connector_PinSocket_2.54mm:PinSocket_1x20_P2.54mm_Vertical` ×2 |

## 3. Alimentación

| Dato | Valor |
| :--- | :--- |
| Fuente de energía | LiPo 3.7 V 500 mAh (DEC) → conversor a MX1.25 (lo hace el profe) → conector de batería **de la propia RP2350-Plus**. La batería no se conecta a nuestra PCB |
| Tensión de entrada | 3.0–4.2 V (LiPo); 5 V por USB-C al cargar |
| Rieles | **3V3** desde el pin 3V3 de la RP2350-Plus: pantalla (~20–80 mA según alternativa), amplificador (picos ~200 mA), resto < 10 mA |
| ¿Regulador? | No: lo trae la RP2350-Plus (2 A) |
| Encendido | Interruptor deslizante: **ON = 3V3_EN libre; OFF = 3V3_EN a GND** (como el Game★Mite). La batería se sigue cargando apagada |
| Protecciones | No (la RP2350-Plus gestiona carga y protección) **[VERIFICAR corriente de carga ≤ 500 mA para LiPo de 500 mAh]** |
| Desacoplo | 100 nF entre 3V3 y GND en cada conector de pantalla y junto al amplificador; filtro del amplificador **R 2.2 Ω ½ W en serie + 100 µF + 100 nF** (como R3/C3/C5 del Game★Mite) |

## 4. Lista de componentes

| Ref | Cant. | Descripción / valor | Encapsulado | THT/SMD | Cara | Huella KiCad (candidata, confirmar en Fase 0) | Hoja de datos | Notas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 (J_MCU_A, J_MCU_B) | 2 | Tira hembra 1×20, 2.54 mm, para RP2350-Plus | THT | THT | Bottom | `Connector_PinSocket_2.54mm:PinSocket_1x20_P2.54mm_Vertical` | — | Separación entre filas [MEDIR] |
| J2 | 1 | Tira hembra 1×14 — pantalla ILI9341 2.8" (Alt. 2) | THT | THT | Top | `Connector_PinSocket_2.54mm:PinSocket_1x14_P2.54mm_Vertical` | **[ADJUNTAR]** foto del módulo | Se suelda solo en Alt. 2 |
| J6 | 1 | Tira hembra 1×4 — lector SD de la ILI9341 (Alt. 2) | THT | THT | Top | `Connector_PinSocket_2.54mm:PinSocket_1x04_P2.54mm_Vertical` | — | Opcional |
| J3 | 1 | Tira hembra 1×7 — pantalla IPS 1.3" ST7789 (Alt. 1) | THT | THT | Top | `Connector_PinSocket_2.54mm:PinSocket_1x07_P2.54mm_Vertical` | **[ADJUNTAR]** foto del módulo | Se suelda solo en Alt. 1. Orden de pines [VERIFICAR] |
| U2 | 1 | Módulo amplificador PAM8403 (DEC) | módulo | THT | Bottom | Tira de pines según módulo: **buscar** | **[ADJUNTAR]** foto | Pines y medidas [MEDIR]. Se usa solo el canal L |
| J5 | 1 | Conector parlante 2 pines | THT | THT | Bottom | `Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical` | — | Parlante 8 Ω por cable |
| SW1–SW8 | 8 | Pulsador táctil 6×6 mm, 4 patas (DEC) | 6×6 THT | THT | Top | `Button_Switch_THT:SW_PUSH_6mm` | **[ADJUNTAR]** | Pares unidos internamente [VERIFICAR con multímetro]. Opción 12 mm: `Button_Switch_THT:SW_PUSH_12mm` |
| SW9 | 1 | Pulsador RESET 6×6 | 6×6 THT | THT | Top | `Button_Switch_THT:SW_PUSH_6mm` | — | A RUN, rebajado para evitar pulsaciones accidentales |
| SW10 | 1 | Interruptor deslizante 1 polo 2 posiciones | THT | THT | Top (borde) | **buscar** (candidato `Button_Switch_THT:SW_Slide_1P2T_CK_OS102011MS2Q`) | — | Modelo según disponibilidad del pañol [VERIFICAR] |
| RV1 | 1 | Potenciómetro 10 kΩ lineal (B10K, DEC) — volumen | THT | THT | Bottom (borde) | **buscar** según el modelo del DEC | — | Accesible desde un costado de la carcasa [MEDIR] |
| R1 | 1 | 330 Ω ¼ W (filtro PWM) | Axial | THT | Top | `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal` | — | Alternativa confirmada: 1 kΩ |
| R2 | 1 | 27 kΩ ¼ W (ganancia) | Axial | THT | Top | ídem | — | |
| R3 | 1 | 2.2 Ω ½ W (filtro alimentación amplificador) | Axial | THT | Top | `Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal` | — | ½ W |
| R4 | 1 | 68 Ω ¼ W (luz de fondo ILI9341) | Axial | THT | Top | ídem R1 | — | Solo Alt. 2 |
| C1 | 1 | 100 nF cerámico (filtro PWM) | Disco | THT | Top | `Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm` | — | Alternativa confirmada: 10 nF |
| C2 | 1 | 100 nF cerámico (acople audio) | Disco | THT | Top | ídem | — | |
| C3 | 1 | 100 µF 10 V electrolítico | Radial | THT | Top | `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm` | — | Polaridad |
| C4–C7 | 4 | 100 nF cerámico (desacoplo) | Disco | THT | Top | ídem C1 | — | |
| C8 | 1 | 100 nF (RESET, como C11 del Game★Mite) | Disco | THT | Top | ídem C1 | — | |
| H1–H4 | 4 | Agujero M2 | NPTH 2.2 mm | — | — | `MountingHole:MountingHole_2.2mm_M2` | — | Tornillos M2 confirmados por el profe |

Regla para SMD: **no hay componentes SMD.**

## 5. Conexiones (netlist funcional)

Numeración de pines de la RP2350-Plus = Pico **[VERIFICAR]**: GP0=1, GP1=2, GP2=4, GP3=5, GP4=6, GP5=7, GP6=9, GP7=10,
GP8=11, GP9=12, GP10=14, GP11=15, GP12=16, GP13=17, GP14=19, GP15=20, GP20=26, GP22=29, RUN=30, GP26=31, 3V3=36,
3V3_EN=37, GND=3/8/13/18/23/28/33/38.

| Red | Desde (ref.pin) | Hasta (ref.pin) | Tipo | Requisito |
| :--- | :--- | :--- | :--- | :--- |
| SPI_SCK | U1.GP6 | J2.7 (SCK), J2.10 (T_CLK), J6.4, J3.SCL | señal | — |
| SPI_MOSI | U1.GP3 | J2.6 (MOSI), J2.12 (T_DIN), J6.2, J3.SDA | señal | — |
| SPI_MISO | U1.GP4 | J2.9 (MISO), J2.13 (T_DOUT), J6.3 | señal | Solo Alt. 2 |
| LCD_CS | U1.GP0 | J2.3 (CS) | señal | J3 no tiene CS [VERIFICAR] |
| LCD_RST | U1.GP1 | J2.4 (RESET), J3.RES | señal | |
| LCD_DC | U1.GP2 | J2.5 (D/C), J3.DC | señal | |
| TOUCH_CS / TOUCH_IRQ | U1.GP5 / U1.GP7 | J2.11 / J2.14 | señal | Se rutea pero no se usa |
| SD_CS | U1.GP22 | J6.1 | señal | Solo Alt. 2 |
| LCD_LED | 3V3 → R4 (68 Ω) | J2.8 (LED) | potencia | Alt. 2 |
| LCD_BLK | U1.GP26 | J3.BLK | señal | PWM de brillo (Alt. 1) |
| BTN_DOWN | SW1.1 | U1.GP8 | señal | pull-up interno |
| BTN_LEFT | SW2.1 | U1.GP9 | señal | |
| BTN_UP | SW3.1 | U1.GP10 | señal | |
| BTN_RIGHT | SW4.1 | U1.GP11 | señal | |
| BTN_SELECT | SW5.1 | U1.GP12 | señal | |
| BTN_START | SW6.1 | U1.GP13 | señal | |
| BTN_B | SW7.1 | U1.GP14 | señal | |
| BTN_A | SW8.1 | U1.GP15 | señal | |
| RUN | SW9.1, C8.1 | U1.RUN | señal | C8.2 a GND |
| PWR_EN | SW10.común | U1.3V3_EN | señal | Otra posición de SW10 a GND (= apagado) |
| AUD_PWM | U1.GP20 | R1.1 | señal | |
| AUD_FILT | R1.2, C1.1, C2.1 | — | señal | C1.2 a GND |
| AUD_AC | C2.2 | R2.1 | señal | |
| AUD_VOL | R2.2 | RV1 extremo 1 | señal | RV1 extremo 2 a GND |
| AUD_IN | RV1 cursor | U2.L_IN | señal | U2.R_IN sin conectar o a GND [VERIFICAR] |
| AMP_VCC | 3V3 → R3 (2.2 Ω) | U2.VCC, C3.+, C7.1 | potencia | Pista ≥ 0.6 mm |
| SPK+ / SPK− | U2.L+ / U2.L− | J5.1 / J5.2 | potencia | Pista ≥ 0.6 mm |
| 3V3 | U1.3V3 | J2.1, J3.VCC, R3, R4, C4–C6 | potencia | Pista ≥ 0.5 mm |
| GND | U1.GND (todos) | J2.2, J3.GND, J6, SW1–SW9.2, C*, RV1, U2.GND, SW10 | GND | Plano en B.Cu |

Cada botón une su GPIO con GND; el firmware usa `INPUT_PULLUP` (pulsado = LOW). El agente puede reasignar pines libres
(GP16–GP19, GP21, GP27, GP28) para facilitar el ruteo, avisando y actualizando `netlist.csv`. Los pines de SPI no se reasignan.

## 6. Mecánica y posiciones

| Dato | Valor |
| :--- | :--- |
| Dimensiones exteriores | **160 × 70 mm [PROPUESTA]** |
| Forma | Rectángulo |
| Radio de esquinas | 4 mm (seguridad para niños; la carcasa redondea más) |
| Origen | Esquina superior izquierda = (0,0), Y hacia abajo |
| Agujeros de montaje | M2 NPTH 2.2 mm en (4, 4), (156, 4), (4, 66), (156, 66) |
| Altura máxima | Top: pantalla sobre tira hembra ≈ 13 mm [MEDIR]; botones ≈ 5 mm (+ capuchón). Bottom: RP2350-Plus sobre tira hembra ≈ 12 mm [MEDIR] |
| Zonas prohibidas (keep-out) | **Top:** rectángulo de la pantalla 2.8" x 37–123, y 6–56 [PROPUESTA]: solo conectores J2, J3, J6 y pistas, ningún componente alto (la pantalla queda encima). **Bottom:** zona del conector de batería y USB-C de la RP2350-Plus libre para la carcasa |
| Espesor | 1.6 mm |

Posiciones fijas [PROPUESTA — validar con piezas reales y boceto]:

| Ref | x (mm) | y (mm) | Rot. (°) | Cara | Por qué es fija |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SW3 (UP) | 18 | 24 | 0 | Top | Cruceta, pulgar izquierdo |
| SW1 (DOWN) | 18 | 44 | 0 | Top | Cruceta |
| SW2 (LEFT) | 8 | 34 | 0 | Top | Cruceta |
| SW4 (RIGHT) | 28 | 34 | 0 | Top | Cruceta |
| SW8 (A) | 148 | 30 | 0 | Top | Pulgar derecho |
| SW7 (B) | 136 | 40 | 0 | Top | Pulgar derecho |
| SW5 (SELECT) | 74 | 63 | 0 | Top | Bajo la pantalla; sus patas no deben chocar con la tira hembra de la RP2350-Plus (cara posterior) |
| SW6 (START) | 94 | 63 | 0 | Top | Bajo la pantalla |
| SW9 (RESET) | 150 | 62 | 0 | Top | Esquina, lejos de los pulgares |
| SW10 (ON/OFF) | 140 | 3 | 0 | Top | Borde superior, accesible desde la carcasa |
| J2 (ILI9341 1×14) | **[VERIFICAR con el módulo]** | — | 90 | Top | Define la posición de la pantalla 2.8" (centro de pantalla en (80, 31)) |
| J6 (SD 1×4) | **[VERIFICAR]** | — | 90 | Top | Lado opuesto a J2 en el mismo módulo |
| J3 (ST7789 1×7) | **[VERIFICAR con el módulo]** | — | 0 | Top | Que la pantalla 1.3" quede centrada en (80, 31) |
| U1 (RP2350-Plus) | centro ≈ (60, 44) | — | 90 | **Bottom** | USB-C en el borde inferior (y = 70) para cargar/programar |
| RV1 (volumen) | 158 | 50 | 90 | Bottom | Rueda accesible por el costado derecho |

> Si se usan pulsadores de 12 mm, la cruceta pasa a un paso de 13 mm y el ancho de la placa debe revisarse.

## 7. Fabricante y reglas de diseño (DFM)

| Parámetro | Mi valor | Mínimo del fabricante |
| :--- | :--- | :--- |
| Número de capas | `2` | — |
| Ancho mínimo de pista (señal) | `0.25 mm` | `0.127 mm` |
| Ancho de pistas de potencia | `0.50–0.80 mm` | — |
| Separación mínima cobre-cobre | `0.20 mm` | `0.127 mm` |
| Vía: diámetro / taladro | `0.60 / 0.30 mm` | `0.45 / 0.20 mm` |
| Anillo anular THT (soldadura manual) | `≥ 0.40 mm` | `0.15 mm` |
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
| Plano de masa | `B.Cu continuo` (los módulos en Bottom son THT; evitar cortar el plano con pistas) |
| ¿Vías? | Sí, máximo ~20, solo si no se puede rutear en F.Cu |
| Ancho por tipo de red | Señal 0.25 mm · 3V3 0.5 mm · AMP_VCC y parlante 0.6–0.8 mm |
| Redes críticas | SPI (GP6/GP3/GP4) lo más corto posible hacia J2/J3; audio PWM lejos de SPI |
| Autorouter | Solo si el agente no logra rutear en 2 intentos, y solo en F.Cu |
| ¿Reasignar pines? | Sí, solo entre GP16–GP19, GP21, GP27, GP28 y los botones; nunca SPI/LCD/audio |
| Ángulos | `45° y 90°` |

## 9. Serigrafía y marcas

- F.SilkS: nombre de cada botón (UP, DOWN, LEFT, RIGHT, A, B, SELECT, START, RESET) y "ON/OFF", 1.0 mm.
- F.SilkS: contorno de la pantalla 2.8" y de la 1.3" dentro de su zona, con el texto "ALT1 1.3in" / "ALT2 2.8in" junto a J3 / J2.
- B.SilkS: contorno de la RP2350-Plus, **pin 1 y posición del USB-C**, y "VISTA POSTERIOR — FILAS ESPEJADAS".
- Texto "KIDBOX v1.0 2026 — basado en Game★Mite (CC BY 4.0)" en la parte inferior.

## 10. Entregables que espero del agente

- [ ] Proyecto KiCad completo que abre sin errores en KiCad `10.0`.
- [ ] ERC y DRC con 0 errores, mínimos DFM de la sección 7 escritos en el proyecto.
- [ ] `BOM.csv`, `netlist.csv`, `DECISIONES.md`, `README.md`.
- [ ] Imágenes de verificación (`verificacion/`).
- [ ] Paquete de fabricación (`fabricacion/*.zip`) **solo cuando el equipo lo apruebe**.

## 11. Decisiones ya tomadas y preguntas abiertas

Decisiones tomadas:
- Plataforma RP2350-Plus (respaldo Pico), firmware en Arduino IDE (recomendación del profe).
- PCB universal: J2+J6 (ILI9341 2.8") y J3 (ST7789 1.3") en la misma zona; solo se suelda uno.
- Asignación de pines del Game★Mite (sección 5).
- Todo THT, 2 capas, sin ensamblaje. Módulos en la cara posterior.
- Batería conectada directo a la RP2350-Plus (no pasa por la PCB). Sin TP4056.
- Sin microSD propia (la SD de la ILI9341 queda disponible en Alt. 2).

Preguntas abiertas (Fase 0):
- ¿La separación entre filas de la RP2350-Plus es igual a la Pico (17.78 mm)?
- ¿Orden de pines de la IPS 1.3" y del PAM8403 del DEC? (adjuntar fotos)
- ¿Huella del potenciómetro B10K y del interruptor deslizante disponibles?
- ¿Cabe la cruceta de 12 mm en 160 mm de ancho?

## 12. Restricciones adicionales para el agente

- No usar componentes SMD.
- No mover las posiciones fijas de la sección 6 sin preguntar.
- No colocar componentes de más de 3 mm de alto en la zona de pantalla (Top), salvo los conectores J2, J3, J6.
- No descargar huellas de internet; si una huella no existe, proponer tira de pines genérica y avisar.
- No reasignar pines de SPI, pantalla ni audio.
- Anotar toda decisión no escrita aquí en `DECISIONES.md`.
