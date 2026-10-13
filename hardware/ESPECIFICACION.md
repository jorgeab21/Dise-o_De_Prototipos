# ESPECIFICACION.md — Especificación de la PCB KIDBOX (BORRADOR v0.4)

> **Estado: BORRADOR CON SUPUESTOS.** Basado en el Game★Mite v1.3.2 (CC BY 4.0) con los cambios acordados con el profesor el 13-oct-2026.
> Las piezas físicas no se han medido todavía. Todo lo marcado **[SUPUESTO]** viene de hojas de datos, de la página del vendedor o de
> módulos típicos, y debe confirmarse con la pieza real **antes de la Fase 2 (PCB)**. Las secciones 2 a 5 bastan para las Fases 0 y 1 (esquemático).

Nombre del proyecto: `KIDBOX`

Autor: `Equipo KIDBOX (J. Becerra, B. Fernández, A. Medina, D. Pizarro)`   Fecha: `13-oct-2026`   Versión: `0.4`

---

## 0. Entorno

| Dato | Valor |
| :--- | :--- |
| Sistema operativo | `Windows 11` |
| Versión de KiCad y ruta de `kicad-cli` | `10.0.6 — C:\Program Files\KiCad\10.0\bin\kicad-cli.exe` |
| Agente y modelo | `Claude Code` |
| Fabricante y servicio | `JLCPCB, PCB de 2 capas, 1.6 mm, sin ensamblaje` |
| Fuentes autorizadas para descargar huellas que no estén en KiCad | `ninguna` (usar tiras de pines genéricas para los módulos) |

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
                   │   └──GP8..GP15──> 8 × [pulsador 6×6 ──> GND]
                   └──3V3_EN <── [SW10 interruptor ON/OFF]        RUN <── [SW9 pulsador RESET + C]
```

## 2. Microcontrolador o módulo principal

| Dato | Valor |
| :--- | :--- |
| Modelo exacto | Waveshare **RP2350-Plus** (RP2350A, 16 MB flash, USB-C, cargador LiPo integrado). Respaldo: Raspberry Pi Pico (RP2040) del DEC, mismo pinout |
| Cómo va montado | Sobre **2 tiras hembra 1×20** (el módulo trae pines macho soldados) |
| Cara y orientación | **Cara posterior (Bottom)**, girada 180°: USB-C hacia el **borde superior** de la placa (como un control de PlayStation: se puede jugar mientras carga). ⚠ Montado por detrás queda espejado: verificar fila por fila contra la foto |
| Paso de pines | 2.54 mm |
| Separación entre filas | **17.78 mm [SUPUESTO: igual que la Pico]** |
| Dimensiones del módulo | **51 × 21 mm [SUPUESTO: formato Pico]** |
| Pines por fila y pin 1 | 20 por fila; pin 1 = GP0, junto al USB **[SUPUESTO: igual que la Pico]** |
| Fuente del pinout | Pinout de la Raspberry Pi Pico (igual al esquemático del Game★Mite). **[PENDIENTE]** foto de la serigrafía en `datasheets/rp2350plus_pinout.jpg` |
| Pines que SÍ se pueden usar | GP0–GP22, GP26–GP28 |
| Pines PROHIBIDOS y por qué | VBUS, VSYS (alimentación del módulo), ADC_VREF, 3V3 (solo como salida para alimentar) |
| ¿Trae regulador, USB y desacoplos? | Sí: regulador, USB-C, cargador LiPo y desacoplos propios |
| Huella KiCad | `Connector_PinSocket_2.54mm:PinSocket_1x20_P2.54mm_Vertical` ×2 |

## 3. Alimentación

| Dato | Valor |
| :--- | :--- |
| Fuente de energía | LiPo Soshine 902030 3.7 V 500 mAh (9 × 20 × 30 mm) → conector de batería **de la RP2350-Plus**. No se conecta a esta PCB |
| Tensión de entrada | 3.0–4.2 V (LiPo); 5 V por USB-C al cargar |
| Rieles | **3V3** desde el pin 36 de la RP2350-Plus: pantalla (~80 mA con luz de fondo al máximo) + DAC (~20 mA) + pull-ups. Total < 150 mA |
| ¿Regulador? | No: lo trae la RP2350-Plus |
| Encendido | Interruptor deslizante: **ON = 3V3_EN al aire; OFF = 3V3_EN a GND** (como el Game★Mite) |
| Protecciones | No (la RP2350-Plus gestiona carga y protección) **[PENDIENTE: confirmar con el profesor que la corriente de carga es ≤ 500 mA]** |
| Desacoplo | 100 nF entre 3V3 y GND junto a J3 (pantalla); 100 nF + 10 µF junto a J5 (DAC) |

## 4. Lista de componentes

| Ref | Cant. | Descripción / valor | THT/SMD | Cara | Huella KiCad (candidata, confirmar en Fase 0) | Notas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| J1, J2 | 2 | Tira hembra 1×20, 2.54 mm, para la RP2350-Plus | THT | Bottom | `Connector_PinSocket_2.54mm:PinSocket_1x20_P2.54mm_Vertical` | Separación entre filas 17.78 mm [SUPUESTO] |
| J3 | 1 | Tira hembra 1×14 para la pantalla TFT ILI9341 2.4" | THT | Top | `Connector_PinSocket_2.54mm:PinSocket_1x14_P2.54mm_Vertical` | Orden de pines en la sección 5 |
| J4 | 1 | Tira hembra 1×4, lado SD de la pantalla | THT | Top | `Connector_PinSocket_2.54mm:PinSocket_1x04_P2.54mm_Vertical` | **Solo apoyo mecánico**: sus 4 pines sin conectar |
| J5 | 1 | Tira hembra 1×6 para el DAC GY-PCM5102 | THT | Bottom | `Connector_PinSocket_2.54mm:PinSocket_1x06_P2.54mm_Vertical` | El jack del DAC debe apuntar hacia el **borde inferior** |
| SW1–SW8 | 8 | Pulsador táctil 6×6 mm, 4 patas (DEC) | THT | Top | `Button_Switch_THT:SW_PUSH_6mm` | Capuchones impresos en 3D más adelante |
| SW9 | 1 | Pulsador RESET 6×6 mm | THT | Top | `Button_Switch_THT:SW_PUSH_6mm` | A RUN |
| SW10 | 1 | Interruptor deslizante 1 polo 2 posiciones | THT | Top (borde) | `Button_Switch_THT:SW_Slide_1P2T_CK_OS102011MS2Q` [SUPUESTO] | Modelo según disponibilidad [PENDIENTE] |
| C1 | 1 | 100 nF cerámico (RESET, como C11 del Game★Mite) | THT | Top | `Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm` | |
| C2 | 1 | 100 nF cerámico (desacoplo pantalla) | THT | Top | ídem C1 | Junto a J3, fuera del área que tapa la pantalla si es posible |
| C3 | 1 | 100 nF cerámico (desacoplo DAC) | THT | Bottom | ídem C1 | Junto a J5 |
| C4 | 1 | 10 µF electrolítico 16 V (desacoplo DAC) | THT | Bottom | `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm` | Polaridad |
| H1–H4 | 4 | Agujero M2 | NPTH 2.2 mm | — | `MountingHole:MountingHole_2.2mm_M2` | Tornillos M2 confirmados por el profesor |

Regla para SMD: **no hay componentes SMD.**

## 5. Conexiones (netlist funcional)

Numeración de pines de la RP2350-Plus = Pico **[SUPUESTO]**: GP0=1, GP1=2, GND=3, GP2=4, GP3=5, GP4=6, GP5=7, GND=8,
GP6=9, GP7=10, GP8=11, GP9=12, GND=13, GP10=14, GP11=15, GP12=16, GP13=17, GND=18, GP14=19, GP15=20, GP16=21, GP17=22,
GND=23, GP18=24, GP19=25, GP20=26, GP21=27, GND=28, GP22=29, RUN=30, GP26=31, GP27=32, GND=33, GP28=34, ADC_VREF=35,
3V3=36, 3V3_EN=37, GND=38, VSYS=39, VBUS=40. J1 = pines 1–20, J2 = pines 21–40.

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
| LCD_LED | U1.GP26 | J3.8 (LED) | señal | PWM de brillo. **Cambio respecto al Game★Mite** (allí va a VCC con 68 Ω) [PENDIENTE: medir corriente del pin LED] |
| I2S_BCK | U1.GP20 | J5.5 (BCK) | señal | BCK y LCK en pines consecutivos (requisito de la librería I2S) |
| I2S_LRCK | U1.GP21 | J5.3 (LCK) | señal | |
| I2S_DIN | U1.GP22 | J5.4 (DIN) | señal | |
| DAC_SCK | J5.6 (SCK) | GND | GND | El DAC usa su reloj interno |
| BTN_DOWN | SW1.1 | U1.GP8 | señal | pull-up interno |
| BTN_LEFT | SW2.1 | U1.GP9 | señal | |
| BTN_UP | SW3.1 | U1.GP10 | señal | |
| BTN_RIGHT | SW4.1 | U1.GP11 | señal | |
| BTN_SELECT | SW5.1 | U1.GP12 | señal | |
| BTN_START | SW6.1 | U1.GP13 | señal | |
| BTN_B | SW7.1 | U1.GP14 | señal | |
| BTN_A | SW8.1 | U1.GP15 | señal | |
| RUN | SW9.1, C1.1 | U1.RUN | señal | SW9.2 y C1.2 a GND |
| PWR_EN | SW10.común | U1.3V3_EN | señal | Otra posición de SW10 a GND (= apagado); la tercera pata sin conectar |
| 3V3 | U1.3V3 | J3.1 (VCC), J5.1 (VIN), C2, C3, C4.+ | potencia | Pista ≥ 0.5 mm [PENDIENTE: confirmar que el DAC funciona con 3V3] |
| GND | U1.GND (todos) | J3.2, J5.2, J5.6, SW1–SW9.2, C1–C4, SW10 | GND | Plano en B.Cu |

Sin conectar (`no_connect`):
- J3.9 (SDO/MISO): no se lee nada de la pantalla.
- J3.10–J3.14 (táctil): **no se usa el táctil**.
- J4.1–J4.4 (SD): **no se usa la SD**; J4 es solo apoyo mecánico.
- RP2350-Plus: GP4, GP5, GP7, GP16–GP19, GP27, GP28, VBUS, VSYS, ADC_VREF.

Cada botón une su GPIO con GND; el firmware usa `INPUT_PULLUP` (pulsado = LOW). El agente puede reasignar los **botones** a
pines libres para facilitar el ruteo, avisando y actualizando `netlist.csv`. Los pines de SPI, pantalla e I2S no se reasignan.

## 6. Mecánica y posiciones

> **Toda esta sección es [SUPUESTO]** para avanzar. Se confirma con las piezas (la pantalla llega el jueves 15) y el boceto en papel antes de la Fase 2.

| Dato | Valor |
| :--- | :--- |
| Dimensiones exteriores | **150 × 65 mm [SUPUESTO]** |
| Forma | Rectángulo |
| Radio de esquinas | 4 mm (seguridad para niños; la carcasa redondea más) |
| Origen | Esquina superior izquierda = (0,0), Y hacia abajo |
| Agujeros de montaje | M2 NPTH 2.2 mm en (4, 4), (146, 4), (4, 61), (146, 61) |
| Altura máxima | Top: pantalla sobre tira hembra ≈ 8.5 mm + 11.5 mm del módulo; botones ≈ 5 mm (+ capuchón). Bottom: RP2350-Plus y DAC sobre tira hembra ≈ 12 mm [SUPUESTO] |
| Zonas prohibidas (keep-out) | **Top:** bajo el módulo de pantalla (78 × 43 mm, centrado en (75, 28)) solo J3, J4 y pistas; nada más alto que la tira hembra. **Bottom:** batería (9 × 20 × 30 mm) en la carcasa detrás de A/B (x 112–142, y 40–60); borde superior libre en x 71–79 para el USB-C y borde inferior libre bajo el jack para la carcasa |
| Espesor | 1.6 mm |

Módulo de pantalla [SUPUESTO, página del vendedor]: 78 × 43 mm, horizontal, centrado en (75, 28) → ocupa x 36–114, y 6.5–49.5.
Montado **girado 180°**: tira de 14 pines (J3) en el borde corto **derecho** (cerca de GP0–GP6 de la RP2350-Plus) y tira de 4 pines (J4)
en el borde corto **izquierdo**. La imagen se endereza en el firmware con `setRotation()`. Distancias exactas de cada tira al borde del
módulo [PENDIENTE: medir el jueves].

RP2350-Plus girada 180° (USB-C arriba) vista desde el frente "a través" de la placa: pin 1 (GP0) arriba a la derecha, pines 1–20 en la
columna derecha (x = 83.89) de arriba hacia abajo, pines 21–40 en la columna izquierda (x = 66.11) de abajo hacia arriba [VERIFICAR con foto].
Dibujo de referencia: `datasheets/layout_propuesto.svg` (generado con `scripts/gen_layout.py`).

Posiciones fijas [SUPUESTO — validar con piezas reales y boceto]:

| Ref | x (mm) | y (mm) | Rot. (°) | Cara | Por qué es fija |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SW3 (UP) | 20 | 20 | 0 | Top | Cruceta, pulgar izquierdo (paso de 10 mm para capuchones) |
| SW1 (DOWN) | 20 | 40 | 0 | Top | Cruceta |
| SW2 (LEFT) | 10 | 30 | 0 | Top | Cruceta |
| SW4 (RIGHT) | 30 | 30 | 0 | Top | Cruceta; queda fuera del módulo de pantalla (x ≥ 36) |
| SW8 (A) | 138 | 25 | 0 | Top | Pulgar derecho |
| SW7 (B) | 126 | 35 | 0 | Top | Pulgar derecho, en diagonal con A; fuera del módulo (x ≤ 114) |
| SW5 (SELECT) | 66 | 58 | 0 | Top | Bajo la pantalla, centrado; la RP2350-Plus termina en y = 53.5 |
| SW6 (START) | 84 | 58 | 0 | Top | Bajo la pantalla, centrado |
| SW9 (RESET) | 140 | 54 | 0 | Top | Esquina, lejos de los pulgares |
| SW10 (ON/OFF) | 125 | 3 | 0 | Top | Borde superior, accesible desde la carcasa |
| J3 (pantalla 1×14) | ≈ 111.5 | 28 | 270 | Top | Borde derecho del módulo (pantalla girada 180°); pin 1 abajo [PENDIENTE: medir] |
| J4 (apoyo 1×4) | ≈ 38.5 **[PENDIENTE]** | — | 270 | Top | Borde izquierdo del módulo, según la posición real de los pines SD |
| U1 (RP2350-Plus) | centro (75, 28) | — | 180 | **Bottom** | Vertical, USB-C en el borde superior (y = 0) para cargar y programar sin estorbar las manos |
| J5 (DAC) | módulo en x 36–61, y 33–64; tira en y ≈ 36 **[SUPUESTO]** | — | — | Bottom | A la izquierda de la RP2350-Plus, junto a los pines I2S; jack de 3,5 mm hacia el borde inferior |

## 7. Fabricante y reglas de diseño (DFM)

| Parámetro | Mi valor | Mínimo del fabricante |
| :--- | :--- | :--- |
| Número de capas | `2` | — |
| Ancho mínimo de pista (señal) | `0.25 mm` | `0.127 mm` |
| Ancho de pistas de potencia | `0.50 mm` | — |
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
| Plano de masa | `B.Cu continuo` (evitar cortarlo con pistas) |
| ¿Vías? | Sí, solo si no se puede rutear en F.Cu |
| Ancho por tipo de red | Señal 0.25 mm · 3V3 0.5 mm |
| Redes críticas | SPI (GP6/GP3) e I2S (GP20/21/22) lo más cortas posible y separadas entre sí |
| Autorouter | Solo si el agente no logra rutear en 2 intentos, y solo en F.Cu |
| ¿Reasignar pines? | Solo los botones, a pines libres; nunca SPI, pantalla ni I2S |
| Ángulos | `45° y 90°` |

## 9. Serigrafía y marcas

- F.SilkS: nombre de cada botón (UP, DOWN, LEFT, RIGHT, A, B, SELECT, START, RESET) y "ON/OFF", 1.0 mm.
- F.SilkS: contorno del módulo de pantalla y pin 1 de J3.
- B.SilkS: contorno de la RP2350-Plus con **pin 1 y posición del USB-C**, y "VISTA POSTERIOR — FILAS ESPEJADAS".
- B.SilkS: contorno del DAC y posición del jack.
- Texto "KIDBOX v0.1 2026 — basado en Game★Mite de Thomas Hugo Williams (CC BY 4.0)".

## 10. Entregables que espero del agente

- [ ] Proyecto KiCad completo que abre sin errores en KiCad `10.0`.
- [ ] ERC y DRC con 0 errores, mínimos DFM de la sección 7 escritos en el proyecto.
- [ ] `BOM.csv`, `netlist.csv`, `DECISIONES.md`, `README.md`.
- [ ] Imágenes de verificación (`verificacion/`).
- [ ] Paquete de fabricación (`fabricacion/*.zip`) **solo cuando el equipo lo apruebe**.

## 11. Decisiones ya tomadas y preguntas abiertas

Decisiones tomadas (13-oct-2026):
- Base Game★Mite v1.3.2; se descarta la PCB "universal".
- RP2350-Plus (respaldo Pico); firmware en Arduino IDE.
- Pantalla TFT **ILI9341 2.4"** SPI (AFEL, 78 × 43 mm), misma familia y pinout que el Game★Mite. **Sin SD y sin táctil.** Brillo por PWM (GP26).
  La IPS 1.3" ST7789 del DEC se usa solo para pruebas en protoboard mientras llega la 2.4".
- Audio por DAC PCM5102A (I2S) con jack de 3,5 mm; sin parlante ni amplificador.
- Botones 6×6 del DEC; capuchones impresos en 3D.
- Formato horizontal. Todo THT, 2 capas, sin ensamblaje. Batería conectada a la RP2350-Plus.
- USB-C de la RP2350-Plus hacia el borde superior; jack de audífonos hacia el borde inferior. Pantalla montada girada 180°.

Pendientes:
- 14-oct: separación entre filas, dimensiones y pinout de la RP2350-Plus (foto de la serigrafía); medidas del DAC, orden real de sus pines y posición del jack; que el DAC funcione con 3V3 (protoboard); modelo del interruptor deslizante.
- 15-oct (llega la pantalla): distancias de J3 y J4 a los bordes del módulo; corriente del pin LED (si supera ~10 mA hace falta un transistor).
- Boceto 1:1 de 150 × 65 mm con las manos encima.

## 12. Restricciones adicionales para el agente

- No usar componentes SMD.
- No mover las posiciones fijas de la sección 6 sin preguntar.
- No descargar huellas de internet; si una huella no existe, proponer tira de pines genérica y avisar.
- No reasignar pines de SPI, pantalla ni I2S.
- Anotar toda decisión no escrita aquí en `DECISIONES.md`.
- No avanzar a la Fase 2 mientras la sección 6 siga marcada como [SUPUESTO].
