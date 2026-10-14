# ESPECIFICACION.md — Especificación de la PCB KIDBOX (v0.7)

> **Estado: piezas medidas el 14-oct-2026.** Basado en el Game★Mite v1.3.2 (CC BY 4.0) con los cambios acordados con el profesor.
> Lo que sigue marcado **[PENDIENTE]** se confirma antes de la **Fase 4 (Gerbers para fabricar)**, no bloquea la Fase 2.
>
> **v0.5:** respuestas a la Fase 0 · **v0.6:** datos de hojas oficiales (Waveshare, LCDwiki, ETA6096).
> **v0.7 (14-oct):** medidas reales de las piezas; **se elimina el RESET del frente (SW9, C1)**; **batería LiPo 103450 de 2000 mAh** (resuelve
> la carga a 1 A); **layout reordenado** para la batería: pantalla sin girar (J3 a la izquierda), **se elimina J4**, SW10 y B desplazados;
> huella de SW10 cambiada a paso de 2,54 mm. Ver la sección 11, "Cambios v0.7".

Nombre del proyecto: `KIDBOX`

Autor: `Equipo KIDBOX (J. Becerra, B. Fernández, A. Medina, D. Pizarro)`   Fecha: `14-oct-2026`   Versión del documento: `0.7`
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
| Cara y orientación | **Cara posterior (Bottom)**, USB-C hacia el **borde superior** de la placa. ⚠ Montado por detrás queda espejado |
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
| Fuente de energía | **LiPo 103450, 3.7 V, 2000 mAh, 7.4 Wh** (del profesor). **Medida: 50.99 × 33.11 × 9.84 mm** ✅. Se conecta al conector BAT de la RP2350-Plus; **no pasa por esta PCB** |
| Corriente de carga | 1 A (ETA6096, R13 = 160 kΩ) = **0.5C** para 2000 mAh ✅. **El riesgo de la v0.6 queda resuelto.** La LiPo de 500 mAh ya no se usa |
| Cable de batería | Conector blanco de la batería (parece PH2.0) → **adaptador a 1.25 mm** (lo hace el profesor) **[PENDIENTE]**. **Verificar polaridad con multímetro antes de conectar** (rojo = + → ⊕ del BAT) |
| Tensión de entrada | 3.0–4.2 V (LiPo); 5 V por USB-C al cargar |
| Rieles | **3V3** desde el pin 36: pantalla (~80 mA máx.) + DAC (~20 mA). Total < 150 mA. Autonomía estimada ~10–13 h (por validar) |
| Encendido | Interruptor deslizante: **ON = 3V3_EN al aire; OFF = 3V3_EN a GND**. 3V3_EN tiene pull-up de 100 kΩ a VSYS en el módulo ✅. La consola carga estando apagada |
| Desacoplo | 100 nF junto a J3 (pantalla); 100 nF + 10 µF junto a J5 (DAC) |

## 4. Lista de componentes

| Ref | Cant. | Descripción / valor | THT/SMD | Cara | Símbolo · Huella KiCad | Notas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| J1, J2 | 2 | Tira hembra 1×20, 2.54 mm, para la RP2350-Plus | THT | Bottom | `Connector_Generic:Conn_01x20` · `Connector_PinSocket_2.54mm:PinSocket_1x20_P2.54mm_Vertical` | |
| J3 | 1 | Tira hembra 1×14 para la pantalla TFT ILI9341 2.4" | THT | Top | `Connector_Generic:Conn_01x14` · `Connector_PinSocket_2.54mm:PinSocket_1x14_P2.54mm_Vertical` | Orden de pines en la sección 5 |
| ~~J4~~ | — | **Eliminado en v0.7** | — | — | — | Sus patas caían en la zona de batería. La pantalla queda sostenida por J3, H5/H6 y el marco de la carcasa |
| J5 | 1 | Tira hembra 1×6 para el DAC GY-PCM5102 | THT | Bottom | `Connector_Generic:Conn_01x06` · `Connector_PinSocket_2.54mm:PinSocket_1x06_P2.54mm_Vertical` | Orden **confirmado** con la serigrafía ✅. Jack hacia el **borde inferior** |
| SW1–SW8 | 8 | Pulsador táctil 6×6 mm, 4 patas, **alto 9.1 mm** (DEC) | THT | Top | `Switch:SW_Push` · `Button_Switch_THT:SW_PUSH_6mm` | Patas a 6.5 × 4.5 mm **confirmado** ✅. Capuchones 3D más adelante |
| ~~SW9~~ | — | **Eliminado en v0.7** (RESET del frente) | — | — | — | Se usa el RESET de la RP2350-Plus |
| SW10 | 1 | Interruptor deslizante 1P2T recto, 3 patas (cuerpo 8.7 mm, alto ~11 mm con palanca) | THT | **Bottom** | `Switch:SW_SPDT` · `Button_Switch_THT:SW_Slide-03_Wuerth-WS-SLTV_10x2.5x6.4_P2.54mm` | **Paso 2.54 mm [PENDIENTE: confirmar con prueba en protoboard]**; si resulta 2.0 mm, volver a `SW_Slide_SPDT_Straight_CK_OS102011MS2Q`. ⚠ En esta huella el **pad central es el "1"**: el pad central debe ser el **común** (PWR_EN). Resolverlo sin modificar la huella oficial y documentarlo |
| ~~C1~~ | — | **Eliminado en v0.7** (era el del RESET) | — | — | — | |
| C2 | 1 | 100 nF cerámico (desacoplo pantalla) | THT | Top | `Device:C` · `Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm` | Junto a J3. Paso de patas [PENDIENTE: medir al recibir; muchos "104" vienen a 5 mm] |
| C3 | 1 | 100 nF cerámico (desacoplo DAC) | THT | Bottom | `Device:C` · ídem C2 | Junto a J5 |
| C4 | 1 | 10 µF electrolítico **≥16 V** (sirve 25 V) | THT | Bottom | `Device:C_Polarized` · `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm` | Polaridad. Diámetro y paso [PENDIENTE: medir al recibir] |
| H1–H4 | 4 | Agujero M2 (fijación a la carcasa) | NPTH 2.2 mm | — | `Mechanical:MountingHole` (in_bom no) · `MountingHole:MountingHole_2.2mm_M2` | |
| H5, H6 | 2 | Agujeros de la pantalla, **lado de J3** | NPTH 3.2 mm | — | `Mechanical:MountingHole` (in_bom no) · `MountingHole:MountingHole_3.2mm_M3` | Coinciden con los agujeros del módulo. El separador es opcional (se decide al montar; un separador redondo ≤ Ø4 mm queda muy cerca de J3) |

Regla para SMD: **no hay componentes SMD.**

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
| PWR_EN | SW10.común (pad central) | U1.3V3_EN | señal | Una pata extrema a GND (= apagado), la otra sin conectar. Qué posición es OFF [PENDIENTE: continuidad] |
| 3V3 | U1.3V3 | J3.1 (VCC), J5.1 (VIN), C2, C3, C4.+ | potencia | Pista ≥ 0.5 mm. [PENDIENTE: confirmar en protoboard que el DAC funciona con 3V3] |
| GND | U1.GND (todos, incluido el pin 33) | J3.2, J5.2, J5.6, SW1–SW8.2, C2–C4, SW10 | GND | Plano en B.Cu |

Sin conectar (`no_connect`):
- J3.9 (SDO/MISO) y J3.10–J3.14 (táctil).
- RP2350-Plus: **RUN (pin 30)**, GP4, GP5, GP7, GP8–GP11, GP27, GP28, VBUS, VSYS, ADC_VREF.

Con J1/J2 como conectores genéricos, el ERC necesita `PWR_FLAG` en 3V3 y en GND.

## 6. Mecánica y posiciones

> Medidas de los módulos **confirmadas** (salvo la pantalla, que se confirma el 15-oct con la pieza). Las posiciones de los botones
> siguen siendo una propuesta de ergonomía; se validan con un boceto 1:1 pero **no bloquean la Fase 2**.

| Dato | Valor |
| :--- | :--- |
| Dimensiones exteriores | **150 × 65 mm**. Se acepta el sobrecosto de JLCPCB por superar 100 × 100 mm |
| Forma / radio de esquinas | Rectángulo / 4 mm |
| Origen | Esquina superior izquierda = (0,0), Y hacia abajo, **visto desde el frente** |
| Referencia de las coordenadas | **Centro del cuerpo** de cada pieza |
| Rotaciones | **Manda la descripción geométrica** (qué pin queda dónde, visto desde el frente). Verificar la posición de los pads |
| Agujeros de montaje | M2 NPTH 2.2 mm en (4, 4), (146, 4), (4, 61), (146, 61) |
| Alturas | Top: pulsadores 9.1 mm; pantalla 12.68 mm sobre la placa (con su tira macho, según LCDwiki). Bottom: módulos sobre tira hembra ≈ 12 mm; batería 9.84 mm; SW10 ≈ 11 mm |
| Zona prohibida Top | Bajo el módulo de pantalla (x 36.4–113.6, y 6.6–49.4) no van componentes salvo J3; **sí** pistas y soldaduras de piezas de la cara Bottom |
| **Zona de batería (Bottom)** | Rectángulo **x 88.0–123.5, y 4.0–62.0** (35.5 × 58 mm para una batería de 33.1 × 51.0 mm, con holgura). **Sin componentes ni patas THT**; solo pistas y **vías tapadas**. La batería apoya con su lado largo vertical |
| Bordes libres | Superior x 70.7–79.6 (USB-C; abertura de carcasa x ≈ 68–82). Inferior bajo el jack del DAC |
| Espesor | 1.6 mm |

**Pantalla** (plano MSP2402 de LCDwiki; confirmar el 15-oct): placa **77.18 × 42.72 mm**, horizontal, centrada en (75, 28) → x 36.41–113.59,
y 6.64–49.36. **Sin girar** (v0.7): tira de 14 pines (**J3**) **vertical en el borde corto izquierdo**, a 2.00 mm del borde → **x ≈ 38.41**,
centrada en y = 28 (pines de y ≈ 11.49 a 44.51), **pin 1 (VCC) arriba** [VERIFICAR con la pieza el 15-oct]. Agujeros del módulo
Ø3.2 a 67.26 × 36.72 entre centros → los del lado de J3 en **(41.37, 9.64)** y **(41.37, 46.36)** = H5, H6. Los del lado derecho **no se usan**.
La imagen se orienta por firmware con `setRotation()`.

**RP2350-Plus** (cara Bottom, vista "a través" desde el frente): vertical, USB-C arriba, placa en x 64.5–85.5, y ≈ 0–51.5.
Pin 1 (GP0) arriba a la derecha: pines 1–20 en la columna derecha (x = 83.89) de arriba hacia abajo; pines 21–40 en la columna
izquierda (x = 66.11) de abajo hacia arriba. Conector BAT en el extremo inferior del módulo (y ≈ 48–51), del lado de la batería.

**DAC GY-PCM5102** (cara Bottom): **31.0 × 17.8 mm medido**. Vertical, **tira de 6 pines arriba y jack abajo**, a la izquierda de la
RP2350-Plus: módulo en **x ≈ 44–62, y ≈ 33–64**, tira en y ≈ 35.5 centrada en x ≈ 53, jack asomando al borde inferior (y = 65).
Pin 1 (VIN) [la orientación exacta la propone el agente para acortar las pistas I2S, avisando].

Posiciones fijas (centro del cuerpo):

| Ref | x (mm) | y (mm) | Cara | Por qué es fija |
| :--- | :--- | :--- | :--- | :--- |
| SW3 (UP) | 18 | 20 | Top | Cruceta, pulgar izquierdo (paso de 10 mm para capuchones) |
| SW1 (DOWN) | 18 | 40 | Top | Cruceta |
| SW2 (LEFT) | 8 | 30 | Top | Cruceta |
| SW4 (RIGHT) | 28 | 30 | Top | Cruceta; capuchón hasta x = 33, pantalla desde x = 36.4 |
| SW8 (A) | 138 | 25 | Top | Pulgar derecho |
| SW7 (B) | **128** | 35 | Top | Pulgar derecho, en diagonal con A. **Desplazado 2 mm a la derecha** (v0.7): sus patas (x ≥ 124.75) quedan fuera de la zona de batería |
| SW5 (SELECT) | 66 | 58 | Top | Bajo la pantalla, centrado |
| SW6 (START) | 84 | 58 | Top | Bajo la pantalla, centrado; patas hasta x = 87.25, fuera de la zona de batería |
| SW10 (ON/OFF) | **134** | 8 | **Bottom** | Recto, palanca hacia atrás. **Desplazado a x = 134** (v0.7) para dejar libre la zona de batería; lejos de las patas de A (y ≥ 22.75) |
| J3 (pantalla 1×14) | 38.41 | 28 | Top | Borde izquierdo de la pantalla, pin 1 arriba [VERIFICAR 15-oct] |
| H5, H6 | 41.37 | 9.64 y 46.36 | — | Agujeros del módulo de pantalla, lado de J3 |
| J1+J2 (RP2350-Plus) | centro (75, 25.8) | — | **Bottom** | USB-C en el borde superior |
| J5 (DAC) | tira en (≈ 53, ≈ 35.5) | — | Bottom | Ver descripción |

## 7. Fabricante y reglas de diseño (DFM)

| Parámetro | Mi valor | Mínimo del fabricante |
| :--- | :--- | :--- |
| Número de capas | `2` | — |
| Ancho mínimo de pista (señal) | `0.25 mm` | `0.127 mm` |
| Ancho de pistas de potencia | `0.50 mm` | — |
| Separación mínima cobre-cobre | `0.20 mm` | `0.127 mm` |
| Vía: diámetro / taladro | `0.60 / 0.30 mm` | `0.45 / 0.20 mm` |
| Vías | **Tapadas (tented)**: obligatorio en la zona de batería | — |
| Anillo anular THT | `≥ 0.35 mm` con **huellas oficiales sin modificar** | `0.15 mm` |
| Cobre a borde de placa | `0.30 mm` | `0.20 mm` |
| Agujero a agujero / agujero a cobre | `0.25 mm` / `0.25 mm` | — |
| Serigrafía: trazo / alto de texto | `0.15 / 1.0 mm` | `0.15 mm` |
| Acabado / máscara / ensamblaje | `HASL sin plomo` / `verde` / `No` | — |

## 8. Estrategia de ruteo

| Dato | Valor |
| :--- | :--- |
| Capa de señales preferente | `F.Cu` |
| Plano de masa | `B.Cu continuo`, con **alivios térmicos** en todos los pads de GND |
| ¿Vías? | Sí, cuando hagan falta (la pantalla quedó a la izquierda y sus pines del módulo a la derecha: las pistas SPI cruzan la placa bajo la pantalla, lo que está permitido) |
| Pistas bajo módulos | **Permitidas** en ambas caras (los módulos van 8.5 mm por encima, sobre tiras hembra) |
| Ancho por tipo de red | Señal 0.25 mm · 3V3 0.5 mm |
| Redes críticas | SPI (GP6/GP3) e I2S (GP20/21/22) lo más cortas posible y separadas entre sí |
| Autorouter | Solo si el agente no logra rutear en 2 intentos |
| ¿Reasignar pines? | Solo los botones, a pines libres; nunca SPI, pantalla ni I2S |
| Ángulos | `45° y 90°` |

## 9. Serigrafía y marcas

- F.SilkS: nombre de cada botón (UP, DOWN, LEFT, RIGHT, A, B, SELECT, START), 1.0 mm. **Sin "RESET"** (ya no hay botón en el frente).
- F.SilkS: contorno del módulo de pantalla y pin 1 de J3.
- B.SilkS: contorno de la RP2350-Plus **con la forma del USB-C**, el **pin 1 marcado en J1 y J2**, la posición de **BOOT/RESET** del módulo y "VISTA POSTERIOR — FILAS ESPEJADAS".
- B.SilkS: contorno del DAC, posición del jack y **"VIN" y "GND" en J5**.
- B.SilkS: "ON/OFF" junto a SW10 y el **contorno de la zona de batería** con el texto "BATERÍA 103450".
- Texto "KIDBOX v1.0 2026 — basado en Game★Mite de Thomas Hugo Williams (CC BY 4.0)" (o "Game*Mite" si no sale la ★), fuera de los módulos y de la zona de batería.

## 10. Entregables que espero del agente

- [ ] Proyecto KiCad completo que abre sin errores en KiCad `10.0`.
- [ ] ERC y DRC con 0 errores, mínimos DFM de la sección 7 escritos en el proyecto.
- [ ] `BOM.csv`, `netlist.csv`, `DECISIONES.md`, `README.md` (con el **orden de soldadura**: primero las piezas de la cara Bottom, J1, J2, J5, C3, C4, SW10, después las de Top).
- [ ] Imágenes de verificación (`verificacion/`).
- [ ] Gerbers **preliminares** para la entrega del 16-oct, marcados como "no fabricar hasta confirmar la pantalla y los [PENDIENTE]".

## 11. Decisiones tomadas y pendientes

Decisiones vigentes:
- Base Game★Mite v1.3.2. RP2350-Plus (respaldo Pico). Firmware en Arduino IDE.
- Pantalla TFT ILI9341 2.4" SPI (AFEL, MSP2402), sin SD ni táctil, brillo por PWM (GP26).
- Audio por DAC PCM5102A (I2S) con jack de 3,5 mm; sin parlante.
- 8 pulsadores 6×6 del DEC; capuchones 3D. Formato horizontal. Todo THT, 2 capas.
- USB-C arriba, jack abajo, ON/OFF por detrás. Cruceta en GP16–GP19.
- Fase 0 y Fase 1: ver historial en git (v0.5 y v0.6).

Cambios v0.7 (14-oct-2026, decididos por el alumno tras medir las piezas):
1. **Se elimina el RESET del frente** (SW9 y C1). RUN queda sin conectar. Se usan los botones BOOT/RESET de la RP2350-Plus por detrás.
2. **Batería LiPo 103450 de 2000 mAh** (50.99 × 33.11 × 9.84 mm): carga a 0.5C, el riesgo de la v0.6 queda resuelto.
3. **Layout reordenado** para la batería: pantalla sin girar (J3 a la izquierda en x ≈ 38.41, pin 1 arriba); **se elimina J4**; H5/H6 pasan al lado de J3; zona de batería x 88.0–123.5, y 4–62; **SW10 a (134, 8)**; **B a x = 128**.
4. **SW10 con huella de paso 2.54 mm** (`SW_Slide-03_Wuerth-WS-SLTV_10x2.5x6.4_P2.54mm`), pendiente de confirmar con la prueba de protoboard.
5. J5 (orden de pines), RP2350-Plus (medidas y pinout), pulsadores (6.5 × 4.5 mm, alto 9.1 mm) y DAC (31.0 × 17.8 mm) **confirmados con las piezas**.

Pendientes (antes de la Fase 4 de fabricación):
- **15-oct:** confirmar la pantalla con la pieza (contorno, agujeros, posición de J3 y lado del pin 1, alto total, puente J1 a 3.3 V).
- **SW10:** paso de las patas (protoboard) y qué posición es OFF (continuidad).
- **Protoboard (16–17 oct):** que el DAC funcione con VIN = 3V3.
- Condensadores: paso de patas y diámetro al recibirlos.
- Adaptador y polaridad de la batería (profesor).

## 12. Restricciones adicionales para el agente

- No usar componentes SMD. No modificar huellas oficiales. No descargar huellas de internet.
- No mover las posiciones fijas de la sección 6 sin preguntar.
- No reasignar pines de SPI, pantalla ni I2S.
- **No colocar componentes ni patas THT en la zona de batería** (Bottom, x 88.0–123.5, y 4.0–62.0).
- Anotar toda decisión no escrita aquí en `DECISIONES.md`.
- No generar Gerbers "para fabricar" mientras haya [PENDIENTE] de la pantalla o de SW10; los de la entrega del 16-oct van marcados como **preliminares**.
