# DECISIONES.md — KIDBOX

Registro de fuentes consultadas, datos obtenidos de ellas y supuestos del agente que no están en `ESPECIFICACION.md`.
Formato de cada supuesto: fecha · qué se supuso · por qué · qué pasa si está mal.

---

## 1. Hojas de datos consultadas (autorizadas en la sección 0 de la especificación, v0.5)

Descargadas el 13-oct-2026 en `datasheets/`. No se descargaron huellas ni software. El único modelo 3D es el STEP oficial de la RP2350-Plus, autorizado en la v0.6 (fila de abajo).

| Archivo en `datasheets/` | Qué es | URL de origen |
| :--- | :--- | :--- |
| `RP2350_Plus_esquematico.pdf` | Esquemático oficial de la Waveshare RP2350-Plus | https://files.waveshare.com/wiki/RP2350-Plus/RP2350_Plus.pdf |
| `RP2350_Plus_pinout_waveshare.jpg` | Pinout oficial (vista posterior del módulo) | https://www.waveshare.com/w/upload/3/3c/680px-RP2350-Plus-details-inter.jpg (página: https://www.waveshare.com/wiki/File:680px-RP2350-Plus-details-inter.jpg) |
| `RP2350_Plus_dimensiones_waveshare.jpg` | Plano de dimensiones oficial (vista frontal del módulo) | https://www.waveshare.com/w/upload/2/22/800px-RP2350-Plus-details-size.jpg (página: https://www.waveshare.com/wiki/File:800px-RP2350-Plus-details-size.jpg) |
| `MSP2402_esquematico_lcdwiki.pdf` | Esquemático del módulo TFT 2.4" SPI MSP2402 | https://www.lcdwiki.com/res/MSP2402/MSP2402-2.4-SPI.pdf |
| `MSP2402_dimensiones_lcdwiki.pdf` | Plano mecánico (rotulado "MSP2401", misma PCB) | https://www.lcdwiki.com/res/MSP2402/MSP2401_Size.pdf |
| `MSP2402_manual_lcdwiki.pdf` | Manual de usuario del MSP2402 | https://www.lcdwiki.com/res/MSP2402/2.4inch_SPI_Module_MSP2402_User_Manual_EN.pdf |
| `RP2350_Plus_STEP.zip` | Modelo 3D oficial (STEP, 28.8 MB descomprimido; se guarda comprimido) para alturas y carcasa. Autorizado en ESPECIFICACION v0.6 | https://files.waveshare.com/wiki/RP2350-Plus/RP2350_Plus_STEP.zip |

Páginas leídas: https://www.waveshare.com/wiki/RP2350-Plus y https://www.lcdwiki.com/2.4inch_SPI_Module_ILI9341_SKU:MSP2402

No hay renderizador de PDF instalado. Los esquemáticos se leyeron extrayendo texto y líneas con `pypdf` (ya instalado), dibujándolos con PIL en un archivo temporal fuera del proyecto. No se instaló nada.

## 2. Datos obtenidos (13-oct-2026)

### RP2350-Plus (Waveshare)
- **Pinout idéntico al de la Pico**, pines 1–40, tal como dice la sección 5. El pin 33 es AGND, el 36 es "3V3(OUT)" y el 37 es 3V3_EN. El esquemático rotula el bloque de pines como "Pico no debug".
- **Dimensiones**: 21.00 × 51.00 mm; filas a 17.78 mm; pin 1 a 1.37 mm del borde superior y a 1.61 mm del borde lateral. Coincide con el supuesto de la sección 2 y con las coordenadas de la sección 6 (columnas en x 66.11 y 83.89; pin 1 en y 3.87).
- **USB-C**: 8.95 mm de ancho, a ras del borde superior del módulo y 0.15 mm descentrado (6.17 mm hasta el borde lateral en la vista frontal). Visto desde el frente de la KIDBOX ocupa x ≈ 70.7–79.6.
- **Conector de batería**: P3, **PH1.25-2P** (paso 1.25 mm), en la cara de componentes y en el extremo **opuesto al USB-C**, junto a los pines 20/21 (centro aproximado del módulo en x, y ≈ 48–53.5 en coordenadas de la placa). La serigrafía marca la polaridad (+ y −).
- **3V3_EN** (red PWR_EN) va al pin EN del regulador buck-boost **MP28164** (hasta 2 A), con **R6 = 100 kΩ de pull-up a VSYS**. Es igual que en la Pico, así que "ON = al aire" enciende y "OFF = a GND" apaga el riel 3V3.
- **Cargador**: **ETA6096** (cargador conmutado). El esquemático trae la tabla "R13: 160k → 1A · 82k → 2A · 66k → 2.5A" y R13 montada = **160 kΩ → corriente de carga ≈ 1 A**.
- VSYS sale de VBUS y de VBAT a través de diodos Schottky MBR230 (D1, D2). El cargador funciona con 3V3_EN a GND, así que **carga aunque la consola esté apagada**.

### Pantalla MSP2402 (LCDwiki)
- **Pines 1–14** iguales a la sección 5 (1 VCC … 8 LED … 14 T_IRQ). VCC admite 3.3–5 V.
- **Luz de fondo**: el pin LED (TFT_BL) entra a la base de un **NPN S8050 por 1 kΩ** (R6 del módulo); los LED se alimentan del riel 3.3 V del módulo con 10 Ω (R5). Corriente estimada del pin LED ≈ (3.3 − 0.7) V / 1 kΩ ≈ **2.6 mA**, por debajo de los 4 mA por defecto de un GPIO del RP2350.
- **Alimentación del módulo**: LDO XC6206 de VCC a 3.3 V, con un puente J1 (0 Ω) "VCC5V / VCC3.3" para saltarlo cuando se alimenta con 3.3 V.
- **Mecánica** (plano V1.0, 2024-04-15): PCB **77.18 × 42.72 mm**; **4 agujeros Ø3.20 mm** (pad Ø4.70) a **67.26 × 36.72 mm** entre centros (a 4.96 mm de los bordes cortos y a 3.00 mm de los largos). Tira de 14 pines centrada en un borde corto (13 × 2.54 = 33.02 mm, 4.85 mm a cada lado), con la fila a 2.00 mm del borde [lectura del plano, confirmar]. Tira SD 1×4 en el borde opuesto: fila a ≈ 3.00 mm del borde, primer pin a 17.23 mm de un borde largo [lectura del plano, confirmar]. Alto de la tira macho 11.17 mm; alto total con la tira 12.68 mm.

## 3. Supuestos del agente

- **13-oct-2026 · El AFEL "ILI9341 2.4" SPI" es el MSP2402 de LCDwiki (o un clon con el mismo esquemático).** Por qué: mismo pinout de 14 + 4 pines y mismas medidas que la especificación (78 × 43 ≈ 77.18 × 42.72). Si está mal: cambian la corriente del pin LED (podría hacer falta un transistor) y las cotas de J3, J4 y H5–H8. Se confirma el 15-oct.
- **13-oct-2026 · R6 (100 kΩ) del RP2350-Plus va a VSYS.** Por qué: en el dibujo reconstruido del PDF, la etiqueta VSYS queda en el extremo libre de R6 y el otro extremo va a EN/PWR_EN; además es el circuito de la Pico. Si está mal: "ON = al aire" podría no encender. Se comprueba el 14-oct midiendo el pin 37 con el módulo alimentado y sin nada conectado (debe dar ≈ VSYS).
- **13-oct-2026 · Corriente de carga de 1 A, leída de la tabla de R13 del propio esquemático.** No se consultó la hoja de datos del ETA6096 (no está entre las fuentes autorizadas). Si está mal, la carga podría ser otra; se confirma midiendo la corriente de la batería durante la carga.

## 4. Fase 1 — esquemático (13-oct-2026)

### Cómo se reproduce
Todo sale de scripts con UUID deterministas (re-ejecutarlos da archivos idénticos; comprobado con md5):

| Script | Qué hace | Cómo se ejecuta (desde `hardware/`) |
| :--- | :--- | :--- |
| `scripts/kidbox_datos.py` | Única fuente de componentes, pines y redes (secciones 2–5) | lo importan los otros dos |
| `scripts/gen_esquematico.py` | Escribe `KIDBOX/KIDBOX.kicad_sch` copiando los símbolos de las librerías oficiales de KiCad 10 | `python scripts/gen_esquematico.py` |
| `scripts/gen_pcb_vacio.py` | PCB solo con el contorno + reglas DFM en el `.kicad_pro` (se niega a pisar un PCB con huellas) | `"C:\Program Files\KiCad\10.0\bin\python.exe" scripts/gen_pcb_vacio.py` |
| `scripts/gen_bom_netlist.py` | `BOM.csv` y `netlist.csv` desde la netlist real (`kicad-cli`) y comparación red por red con la sección 5 | `python scripts/gen_bom_netlist.py` |

Si se edita el esquemático en la GUI, el cambio se pierde al regenerar: los cambios van en `kidbox_datos.py`.

### Decisiones y supuestos nuevos
- **13-oct · Nombres de red = los de la sección 5 (LCD_CS, BTN_UP, I2S_BCK…), y el nombre del pin del módulo (GP0, GP1…) como texto junto a cada pin de J1/J2.** Por qué: la sección 2 pide "etiquetas de red por pin (GP0, GP1, …)", pero una red tiene un solo nombre y la sección 5 y `netlist.csv` usan los funcionales. Las dos cosas se ven en el esquemático: etiqueta funcional a la izquierda y "pin del conector · pin del módulo · GPx" a la derecha. Si está mal: si prefieren redes "GP0_LCD_CS", es un cambio de una línea en `kidbox_datos.py`.
- **13-oct · La red de 3V3 se llama `+3V3`** (el símbolo oficial `power:+3V3`). Es la "3V3" de la especificación. Tiene la net class `Potencia` (pista de 0.5 mm, sección 8) definida en el `.kicad_pro`.
- **13-oct · H5 y H6 ya están en el esquemático** (con su huella `MountingHole_3.2mm_M3`), aunque la sección 4 dice "Solo Fase 2". Por qué: cantidad y huella ya están decididas, y así el esquemático que el alumno revisa ahora no cambia en la Fase 2; solo su posición es de la Fase 2. H9 no se agregó (0–1, depende del 14-oct). Si está mal: se borran dos líneas en `kidbox_datos.py`.
- ~~**13-oct · Orden de pines de J5 = [SUPUESTO] de la sección 5**~~ **(resuelto el 14-oct, v0.7: orden confirmado con la serigrafía, ver sección 5)** (1 VIN, 2 GND, 3 LCK, 4 DIN, 5 BCK, 6 SCK), por decisión del alumno (respuesta 1 de la segunda vuelta). Si la pieza del 14-oct tiene otro orden: se cambia el diccionario `DAC` y se regenera; ninguna otra red cambia.
- ~~**13-oct · SW10: pin 2 (común) a PWR_EN, pin 1 a GND (= OFF), pin 3 sin conectar.**~~ **(reemplazado el 14-oct por la huella Würth, ver sección 5)** En `Switch:SW_SPDT` y en la huella `OS102011MS2Q` el pin 2 es el central. Qué lado de la palanca es OFF depende del modelo: se verifica con el multímetro (continuidad 1–2 en la posición que se quiera como OFF) y, si hace falta, se intercambian 1 y 3.
- **13-oct · Valores de los símbolos = función** (DOWN, RESET, ON/OFF, "RP2350-Plus 1-20"…) para revisar pin por pin sin abrir la BOM. La descripción de compra está en `BOM.csv`.
- **13-oct · PWR_FLAG en +3V3 y en GND** (sección 5): J1/J2 son conectores pasivos y el ERC no sabe que el 3V3 lo genera el regulador de la RP2350-Plus.
- **13-oct · Origen del PCB = origen absoluto de KiCad (0,0)**, igual que el de la especificación (esquina superior izquierda, Y hacia abajo). Así las coordenadas de la sección 6 se escriben tal cual en la Fase 2. Por eso la placa queda pegada a la esquina de la hoja de dibujo; es solo estético.
- **13-oct · Reglas en el `.kicad_pro`**: las de la sección 7, más `min_hole_clearance = 0.25 mm` (agujero a cobre), que la especificación no menciona. Es conservador para JLCPCB y no afecta a las huellas oficiales.
- **13-oct · Paridad esquemático-PCB con 25 avisos `missing_footprint`**: esperado en la Fase 1, porque el PCB todavía no tiene huellas (`PROMPTS.md`: "vacío solo con el contorno"). Son avisos (`warning`), no errores, y desaparecen en la Fase 2.

### Revisión del alumno
- **13-oct-2026 · Esquemático REVISADO Y APROBADO por el alumno.** Revisión pin por pin en KiCad (redes con el Navegador de redes; pines de J1/J2 contra el pinout oficial de Waveshare), sin observaciones. Respuestas a las preguntas de la Fase 1:
  1. Se mantienen los nombres de red funcionales, con GPx como texto junto a J1/J2.
  2. H5 y H6 se quedan en el esquemático.
  3. El alumno **no edita en la GUI**: todo cambio pasa por `scripts/kidbox_datos.py` y se regenera con los scripts. El `.kicad_sch` es un archivo generado.
  4. Pendiente para el 14-oct: orden real de J5 y posición OFF de SW10. Se corrigen en `kidbox_datos.py` antes de la Fase 2.
- **13-oct-2026 · `.gitignore` en `hardware/`**: excluye `__pycache__/`, `*-backups/`, `fp-info-cache`, `*.lck`, `_autosave-*` y `*.kicad_prl` (preferencias locales de KiCad, no forman parte del diseño).

## 5. Corrección de la Fase 1 por la especificación v0.7 (14-oct-2026)

Cambios hechos en `scripts/kidbox_datos.py` (y textos de `gen_esquematico.py` / `gen_bom_netlist.py`), regenerados con los scripts:

| Cambio | Antes (v0.6) | Ahora (v0.7) |
| :--- | :--- | :--- |
| SW9 (RESET del frente) y C1 | RUN = J2.10 + SW9.1 + C1.1 | **Eliminados**. J2.10 (RUN, pin 30) con `no_connect`; la red `RUN` desaparece |
| J4 (tira SD de la pantalla) | 4 pines sin conectar | **Eliminado** |
| J5 | orden [SUPUESTO] | orden **confirmado**; se quitan los avisos en esquemático, BOM y netlist. Redes sin cambios |
| SW10 | `Switch:SW_SPDT` + `SW_Slide_SPDT_Straight_CK_OS102011MS2Q`; común = pin 2 | `Switch:SW_SPDT_312` + `SW_Slide-03_Wuerth-WS-SLTV_10x2.5x6.4_P2.54mm`; común = pin/pad 1 |
| H5, H6 | "separador, lado de J4" | "agujero del módulo de pantalla, lado de J3" (solo la nota) |

### Decisiones y supuestos nuevos
- **14-oct · SW10: el pad central "1" de la huella Würth es el común, resuelto cambiando el SÍMBOLO, no la huella.**
  En la huella oficial `SW_Slide-03_Wuerth-WS-SLTV_10x2.5x6.4_P2.54mm` el pad 1 (rectangular) está en el centro, (0, 0), y los pads 2 y 3 en −2.54 y +2.54 mm.
  Con `Switch:SW_SPDT` (A = 1, común B = 2, C = 3) el pin común del esquemático caería en una pata extrema.
  KiCad une símbolo y huella por número de pin, así que se usa el símbolo **oficial** `Switch:SW_SPDT_312`, que es el mismo SPDT con el común (B) numerado **1**, C = 2 y A = 3
  (existe en la librería justamente para huellas con el común en el pad 1). Resultado: **pad 1 (central) = PWR_EN, pad 2 = GND (OFF), pad 3 sin conectar.**
  Se descartó conectar `PWR_EN` al pin 1 de `SW_SPDT`: daría la misma placa, pero el dibujo del esquemático mostraría una pata extrema como común.
  Desviación respecto a la especificación: la sección 4 nombra el símbolo `Switch:SW_SPDT`; se usa su variante `SW_SPDT_312` de la misma librería. Si el alumno prefiere `SW_SPDT`, se cambia en una línea, pero entonces el esquemático no reflejará el pad central como común.
  Qué pata extrema (2 o 3) es OFF sigue **[PENDIENTE: continuidad]**; si resulta ser la 3, se intercambian las redes de los pines 2 y 3 en `kidbox_datos.py`.
  Si en la protoboard el paso resulta 2.0 mm (vuelta a `CK_OS102011MS2Q`, común = pad 2), hay que volver a `Switch:SW_SPDT`.
- **14-oct · Descripción de SW10 en la BOM:** "Würth WS-SLTV 450301014042 o equivalente" (es el modelo de la huella); la pieza real es la del DEC con paso 2.54 mm por confirmar.
- **14-oct · Paridad esquemático-PCB: 22 avisos `missing_footprint`** (antes 25: salieron SW9, C1 y J4). Siguen siendo esperados hasta la Fase 2.


### Revisión del alumno (Paso A)
- **14-oct-2026 · Corrección v0.7 del esquemático REVISADA Y APROBADA.** Acepta `Switch:SW_SPDT_312` para SW10 (ya en la sección 4 de la especificación). `scripts/gen_layout.py` y `datasheets/layout_propuesto.svg` quedan como histórico de la v0.6 (sección 6) y no se actualizan.
