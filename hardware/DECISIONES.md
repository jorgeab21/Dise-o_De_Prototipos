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
  4. Pendiente para el 14-oct: orden real de J5 y posición OFF de SW10. Se corrigen en `kidbox_datos.py` antes de la Fase 2. **(J5 confirmado el 14-oct; la posición OFF de SW10, por continuidad el 21-oct, ver sección 15.)**
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
  ~~Si en la protoboard el paso resulta 2.0 mm (vuelta a `CK_OS102011MS2Q`, común = pad 2), hay que volver a `Switch:SW_SPDT`.~~ **(Resuelto: paso 2.54 mm confirmado en protoboard el 14-oct.)**
- **14-oct · Descripción de SW10 en la BOM:** "Würth WS-SLTV 450301014042 o equivalente" (es el modelo de la huella); la pieza real es la del DEC con paso 2.54 mm, **confirmado en protoboard el 14-oct**.
- **14-oct · Paridad esquemático-PCB: 22 avisos `missing_footprint`** (antes 25: salieron SW9, C1 y J4). Siguen siendo esperados hasta la Fase 2.


### Revisión del alumno (Paso A)
- **14-oct-2026 · Corrección v0.7 del esquemático REVISADA Y APROBADA.** Acepta `Switch:SW_SPDT_312` para SW10 (ya en la sección 4 de la especificación). `scripts/gen_layout.py` y `datasheets/layout_propuesto.svg` quedan como histórico de la v0.6 (sección 6) y no se actualizan.

## 6. Fase 2 — PCB (14-oct-2026)

### Cómo se reproduce
| Script | Qué hace | Cómo se ejecuta (desde `hardware/`, con KiCad cerrado) |
| :--- | :--- | :--- |
| `scripts/gen_pcb.py` | PCB completo: contorno, agujeros, huellas oficiales con su red y su enlace al esquemático (netlist real de `kicad-cli`), pistas (lista fija de polilíneas, sin autorouter), plano GND, serigrafía y reglas en `.kicad_pro` (desde la Fase 3 ya no hay `KIDBOX.kicad_dru`). UUID deterministas (3 ejecuciones → mismo md5) | `"C:\Program Files\KiCad\10.0\bin\python.exe" scripts/gen_pcb.py` y después `python scripts/verificar.py KIDBOX` |
| `scripts/gen_pcb_vacio.py` | Reorganizado: `contorno()` y `escribir_reglas()` ahora son funciones que reutiliza `gen_pcb.py`. Ejecutado solo, hace lo mismo que antes | igual que antes |

Igual que con el esquemático, **los cambios del PCB van en `gen_pcb.py`**: si se edita el PCB en la GUI y se regenera, se pierde.

### Posiciones (sección 6), todas con `locked` salvo C2–C4
- **RP2350-Plus (J1, J2, Bottom):** USB-C a ras de y = 0; placa del módulo y 0.55–51.55 (51.55 medido = 51 de placa + 0.55 del USB-C), centro (75, 25.8). Pin 1 a 1.37 mm del borde de su placa → **J1.1 en (83.89, 1.92)**, J1.20 en (83.89, 50.18); J2.1 (= pin 21) en (66.11, 50.18), J2.20 (= pin 40) en (66.11, 1.92).
  Supuesto: el USB-C sobresale por arriba y el módulo se apoya contra el borde. Si en la carcasa el módulo queda más abajo, todo J1/J2 baja en bloque y hay que regenerar.
- **J3** (Top): pin 1 (VCC) en (38.41, 11.49), pin 14 en (38.41, 44.51). ~~**H5/H6** en (41.37, 9.64) y (41.37, 46.36)~~ (eliminados en la Fase 3). H1–H4 en las esquinas de la sección 6.
- **Pulsadores:** centro del cuerpo en la coordenada de la sección 6, patas 6.5 mm en horizontal y 4.5 mm en vertical. La fila del pin 1 se eligió para rutear (cruceta, A y B: pin 1 abajo; SELECT y START: pin 1 arriba). El pulsador es simétrico, así que no cambia nada mecánico.
- **SW10** (Bottom): centro del cuerpo (134, 8) = pad 1 (central, común). Pad 2 (GND) a la derecha visto de frente (x 136.54), pad 3 sin conectar a la izquierda.
- ~~**J5 (DAC, Bottom): tira centrada en (53, 35.5) con el pin 1 (VIN) a la DERECHA visto de frente (x 59.35) y el pin 6 (SCK) a la izquierda (x 46.65).**
  Por qué: en el módulo el orden de arriba hacia abajo es DIN (GP22), LCK (GP21), BCK (GP20). Con VIN a la izquierda, LCK y DIN se cruzan sí o sí, y eso obliga a meter una vía en una señal I2S. Con VIN a la derecha, DIN y LCK llegan por encima de la tira y BCK por debajo, sin cruces ni vías (15–20 mm cada una).
  **Visto desde atrás**, con el DAC de componentes hacia el observador y el jack hacia abajo, VIN queda a la izquierda. **[VERIFICAR con la pieza]**: si el DAC entra al revés, hay que soldar su tira macho por la otra cara (si aún no está soldada) o espejar J5 en `gen_pcb.py`. Espejarlo obliga a una vía en I2S_LRCK.~~ **(reemplazado en la Fase 3: DAC horizontal, ver sección 8)**
- **C2** (Top): pad 1 (3V3) en (34.6, 11.49), a la izquierda de J3 y fuera de la pantalla. ~~**C3** (Bottom): (55.0, 26.07)–(55.0, 28.57). **C4** (Bottom): + en (59.35, 26.07), justo encima de J5.1. Los dos quedan por encima del DAC (y < 33), porque C4 mide ~11 mm de alto y no cabe debajo del módulo.~~ **(C3 y C4 movidos en la Fase 3, ver sección 8)**

### Ruteo (sección 8): 0 vías, 980 mm en F.Cu y 9.4 mm en B.Cu
- **SPI:** cada pista sale de J1 (columna derecha), pasa entre dos pines de J2 (los huecos y 13.35–23.51 caen junto a pines sin uso) y llega a J3 en paralelo, a 2.54 mm. El orden de arriba hacia abajo se mantiene en ambos extremos, así que no hay cruces. LCD_SCK mide 47.3 mm (la distancia en línea recta es 45.7 mm).
- **PWR_EN** (J2.17 → SW10, 85 mm) **va pegado al borde superior (y = 0.6 mm) por encima de J2.20 y J1.1**. Es la única forma de salir de la columna izquierda hacia la derecha sin cortar el haz SPI en F.Cu. Holguras: 0.475 mm al borde (mínimo 0.30) y 0.345 mm a los pads (mínimo 0.20). La otra opción era un puente en B.Cu bajo el haz SPI, que cortaría el plano debajo de las señales rápidas.
- **3V3:** J2.16 → J3.1 → C2 → baja por la izquierda de J3 → cruza la tira J3 **entre sus pines 9 y 10 (sin uso) con 0.40 mm de ancho en 4 mm**, porque el hueco entre pads es de 0.84 mm → C3 → C4+. ~~**De C4+ a J5.1 (VIN) va un puente de 9.4 mm por B.Cu**, pad THT a pad THT y sin vías, porque VIN queda encerrado entre LCK y BCK. Es la única pista en B.Cu: corta el plano con una ranura abierta que cruzan solo DIN y LCK.~~ **(eliminado en la Fase 3: ya no hay pistas en B.Cu, ver sección 8)** Las demás pistas de 3V3 son de 0.5 mm.
- **Pulsadores:** los dos pads "1" de cada `SW_PUSH_6mm` son pads distintos en la huella oficial (el pulsador los une por dentro). Se unen con una pista en F.Cu para que la red quede completa sin modificar la huella.
- **Plano GND en B.Cu:** una sola zona y **un solo polígono relleno** (9100 de 9750 mm²), con alivios térmicos (separación 0.5 mm, radios de 0.5 mm), 0.30 mm de separación y eliminación de islas. **Vías tapadas** activadas en el proyecto (`tenting` en ambas caras), aunque este ruteo no tiene vías.

### Choques con posiciones fijas (no se movió nada)
- ~~**H5/H6 contra J3**~~ **(resuelto en la Fase 3: H5 y H6 eliminados, ver sección 7)**: el agujero de Ø3.2 queda a 0.09 mm del cuerpo de la tira hembra (borde del agujero en x 39.77; cuerpo de la tira hasta x 39.68). Los courtyards se solapan. Sin la regla de abajo, el DRC da 6 errores (`courtyards_overlap`, `pth_inside_courtyard` y `npth_inside_courtyard` en H5 y H6).
  Se resolvió con una regla en `KIDBOX.kicad_dru` que solo afecta a H5/H6 contra J3 (`courtyard_clearance` −10 mm). Por qué: son los agujeros del propio módulo de pantalla y no hay cobre ni pieza que choque (holguras de cobre verificadas por el DRC). Consecuencia: **un tornillo o separador por esos agujeros toca la tira** (ya lo advertía la sección 4). Sirve un tornillo M3 con cabeza ≤ Ø3.4 mm por el lado de la pantalla, o no usarlos.
- ~~**SW6 (START) contra la zona de batería**~~ **(resuelto en la Fase 3: SW6 a x = 83.5, ver sección 7)**: las patas están en x = 87.25 (fuera de la zona, como dice la sección 6), pero el pad de cobre (r = 1.0 mm) llega a x = 88.25, 0.25 mm dentro de la zona. Con la batería centrada (33.1 mm en 35.5 mm) queda ~1.2 mm de holgura por lado, así que la soldadura no debería tocarla. Si se quiere margen, la opción es SW6 en x ≤ 83.75 (cambio de posición fija, a decidir por el alumno).

### Serigrafía (sección 9)
- Frente: UP, DOWN, LEFT, RIGHT, A, B, SELECT, START a 1.0 mm fuera del cuerpo. Referencia SWx dentro del cuerpo, contorno de la pantalla, "1" junto al pin 1 de J3 y "PANTALLA TFT 2.4" (J3)". Créditos en 6 líneas a la derecha, bajo B (x ≈ 136, y 44–54), fuera de la pantalla y de la zona de batería. Se usa **"Game*Mite"** (la sección 9 lo permite), porque no se pudo comprobar sin GUI si la fuente de KiCad trae la ★.
- Detrás: contorno de la RP2350-Plus (los lados 0.5 mm por fuera, para no pisar la serigrafía de las tiras) con el rectángulo del USB-C, "1" en J1.1 y en J2.1, "BOOT/RST" con marcas a y = 23, "VISTA POSTERIOR / FILAS ESPEJADAS". Contorno del DAC con el JACK (posición del jack **aproximada**, centrada en el borde inferior), "VIN" y "GND" en J5, "ON/OFF" en SW10 y el contorno de la zona de batería con "BATERÍA 103450".
- Las referencias de H1–H6 están ocultas: son agujeros sin pieza.
- Las líneas de serigrafía se cortan automáticamente a 0.4 mm de cualquier pad.

### Revisión del alumno (Fase 2)
- **14-oct-2026 · PCB de la Fase 2 revisado.** El alumno **acepta** J5 con VIN a la derecha visto de frente (a la izquierda visto desde atrás) y PWR_EN por el borde superior (y = 0.6 mm). Pide las correcciones de la sección 7. La especificación la actualiza él.

## 7. Fase 3 — correcciones tras la revisión (14-oct-2026)

Solo se cambió esto (comparación huella por huella y pista por pista contra el PCB de la Fase 2):

| Cambio | Antes | Ahora | Archivos |
| :--- | :--- | :--- | :--- |
| **H5 y H6 eliminados** (la pantalla se sujeta con J3 y la carcasa) | M3 NPTH en (41.37, 9.64) y (41.37, 46.36), en el esquemático, el PCB y la BOM | No existen. Se elimina también `KIDBOX/KIDBOX.kicad_dru` (su única regla los exceptuaba del DRC de courtyard). Quedan 4 agujeros NPTH (H1–H4) | `kidbox_datos.py`, `gen_esquematico.py`, `gen_pcb.py`, `KIDBOX.kicad_sch`, `KIDBOX.kicad_pcb`, `BOM.csv` |
| **SW5 (SELECT)** | centro (66, 58); patas x 62.75 / 69.25 | **centro (66.5, 58)**; patas x **63.25 / 69.75** | `gen_pcb.py` |
| **SW6 (START)** | centro (84, 58); patas x 80.75 / 87.25 (cobre hasta 88.25, dentro de la zona de batería) | **centro (83.5, 58)**; patas x **80.25 / 86.75**; cobre hasta **87.75, 0.25 mm fuera** de la zona (x ≥ 88.0) | `gen_pcb.py` |
| Pistas de SELECT | (72.5, 40.02) → (72.5, 52.5) → (69.25, 55.75); unión de pads 62.75–69.25 | (72.5, 40.02) → **(72.5, 53.0) → (69.75, 55.75)**; unión **63.25–69.75** | `gen_pcb.py` |
| Pistas de START | (78, 42.56) → (78, 53.0) → (80.75, 55.75); unión de pads 80.75–87.25 | (78, 42.56) → **(78, 53.5) → (80.25, 55.75)**; unión **80.25–86.75** | `gen_pcb.py` |
| Serigrafía | "SELECT"/"START" y SW5/SW6 centrados en x 66 / 84 | Centrados en **x 66.5 / 83.5** (siguen a sus botones) | `gen_pcb.py` |

- No se movió ninguna otra huella ni pista. `netlist.csv` no cambia: los agujeros no tienen pines, así que las 20 redes y sus 85 filas quedan iguales.
- `ESPECIFICACION.md` no se tocó: el alumno actualiza las secciones 4 y 6 (H5/H6, SW5/SW6).
- Nota de holgura: SELECT y START quedan ahora a 17 mm entre centros (antes 18), simétricos respecto de x = 75. Los capuchones de 10 mm de paso no se tocan.

## 8. Fase 3 — segunda ronda de correcciones (14-oct-2026)

Pedido del alumno (2.1–2.5), tras actualizar la especificación (sección 4 fila J5, sección 6 "DAC GY-PCM5102", sección 11 cambio 7).
Todo se hizo por los scripts; nada en la GUI.

| # | Cambio | Archivos |
| :--- | :--- | :--- |
| 2.1 | `min_connection` = 0.20 mm en las reglas del proyecto (antes 0). Los rayos de alivio térmico son de 0.5 mm y el ancho mínimo de la zona es 0.25 mm, así que no cambia el relleno | `gen_pcb_vacio.py` (`REGLAS`), `KIDBOX.kicad_pro` |
| 2.2 | C4 = **"10u 25V"** (antes "10u 16V") | `kidbox_datos.py` → `KIDBOX.kicad_sch`, `BOM.csv`, `netlist.csv` (texto de la función de C4), `KIDBOX.kicad_pcb` |
| 2.3 | Las huellas quedan como las dejaría F8: **Sheetname "/"**, **Sheetfile "KIDBOX.kicad_sch"**, **filtros de huella del símbolo** (`C_*`, `CP_*`, `SW*`...), solo los campos del símbolo (se quita `KiLib_Generator`, que traen las huellas de la librería). **H1–H4 con "excluir de archivos de posición"** también en el símbolo (`in_pos_files no`), igual que la huella oficial (`attr exclude_from_pos_files`) | `gen_pcb.py` (función `enlazar`), `gen_esquematico.py` (`flags` por símbolo), `kidbox_datos.py` |
| 2.4 | DAC horizontal: J5, C3, C4, I2S, 3V3 del DAC, serigrafía (detalle abajo) | `gen_pcb.py` |
| 2.5 | `KIDBOX/.history/` en `.gitignore` (historial local de KiCad 10) | `.gitignore` |

### 2.3 — cómo se comprobó (nuevo `scripts/verificar_extra.py`)
- **kicad-cli no tiene "Actualizar PCB desde esquemático"**, así que no se puede correr F8 desde un script. `verificar_extra.py` lo emula: exporta la netlist que usa F8 (`kicadsexpr`) y compara cada huella con su símbolo (valor, huella, enlace, hoja, archivo de hoja, filtros, campos, BOM, archivos de posición, DNP). Resultado: **0 cambios**. Contra el PCB anterior detecta 63 diferencias, así que la comparación sí ve lo que F8 cambiaría.
- **Supuesto:** que F8 quita de la huella los campos que el símbolo no tiene (`KiLib_Generator`). Si en tu KiCad esa opción ("eliminar campos sobrantes") está desactivada, no habría cambio en ningún caso. **Confírmalo con F8 en la GUI**: el diálogo debe decir que no hay cambios.
- El mismo script corre **ERC y DRC con los tests que el `.kicad_pro` ignora activados como error** (`footprint_filters_mismatch`, `footprint_type_mismatch`, `missing_courtyard`, `track_not_centered_on_via`, `tuning_profile_track_geometries`), sobre una copia temporal. El proyecto real queda igual. Resultado: 0 en todo.

### 2.4 — DAC horizontal
- **(Reemplazado en la sección 12: J5 en x = 56.)** **J5 (Bottom) en columna vertical en x = 59.0**: pin 6 (SCK) en y = 47.1 … pin 1 (VIN) en y = 59.8, VIN abajo. **Se corrió 1 mm hacia la cruceta** (la especificación dice x ≈ 60, y permite hasta 1 mm). Por qué: el haz de la cruceta tiene que pasar por encima de J5, y con J5 en x = 60 la pista de DOWN quedaba a 0.07 mm de la esquina del pin 6 (mínimo 0.20). En x = 59 queda a 0.38 mm. Separación de J5 con SELECT: pad de J5 hasta x 59.85, pad de SW5 desde x 62.25 (2.4 mm).
- **(Reemplazado en la sección 12: contorno x 25.65–57.5, jack centrado en x = 30.)** **Contorno del DAC en B.SilkS: x 28.65–60.5, y 44.2–61.98** (31.85 × 17.78, la columna a 1.5 mm del lado corto derecho). **Jack** dibujado en x 30–36, y 52–64.3, **centro en x = 33**, boca al borde inferior (posición estimada de fotos, igual que en la especificación; se corrió 1 mm junto con J5). "VIN" y "GND" junto a los pines 1 y 2 de J5.
- ~~**C3 (Bottom)**: pad 1 (+3V3) en (60.6, 63.3), pad 2 (GND) en (58.1, 63.3).~~ **(Reemplazado en la sección 12: C3 vertical entre J5 y SELECT.)** Queda **3.5 mm bajo VIN**, en la franja entre el contorno del DAC (y 61.98) y el borde (cuerpo en y 62.5–64.1). El contorno se esquiva por 0.25 mm de serigrafía.
- **C4 (Bottom)**: pad 1 (+) en (74.0, 59.0), pad 2 (GND) en (76.0, 59.0), cuerpo Ø5 centrado en (75, 59), **entre SELECT y START**. **Aceptado por el alumno (14-oct): "C3 junto a VIN es el que importa".** Queda a ~15 mm de VIN (unos 20 mm de pista desde la derivación de VIN), no "junto a VIN". Junto a VIN no cabe fuera del contorno del módulo:
  - entre J5 y SW5 hay 2.4 mm;
  - bajo el módulo no se puede;
  - en la franja inferior hay ~3 mm y C4 mide 5 mm;
  - entre las patas de SW5 sus pads caen dentro del courtyard de SW5 (2 errores `pth_inside_courtyard`, probado).

  Para un electrolítico de 10 µF, 20 mm de pista de 0.5 mm son despreciables. El 100 nF (C3), que es el que importa en alta frecuencia, sí queda a 3.5 mm.
- **Ruteo (todo en F.Cu, 0 vías, ya no hay pistas en B.Cu)**:
  - El haz de la cruceta sale de J2 hacia la izquierda y tapa el camino de J2 a J5. Por eso el **I2S sale de J2 hacia la derecha**, baja por dentro del módulo (x 67.5–68.7, entre J2 y SELECT), pasa bajo J2.1 y llega a J5 por la derecha.
  - **LCK cruza entre los pines 5 y 4 de J5 y entra al pin 3 por la izquierda.** Es el único orden sin cruces ni vías, porque en J2 el orden es DIN, LCK, BCK y en J5 es BCK, DIN, LCK.
  - Largos: BCK 25.6 mm, DIN 35.2 mm, LRCK 35.5 mm (antes 15–20 mm). Siguen lejos del SPI: el I2S va en y ≥ 28.6 y el SPI en y ≤ 23.5.
  - **3V3** entra al módulo **entre J2.10 (RUN, sin uso) y J2.9 con 0.40 mm** (hueco de 0.84 mm, como en J3), baja por fuera del I2S (x = 69.5) y llega a J5.1 por la derecha. Sigue a C3 y, por debajo de SW5 (y = 62.4), a C4+. Total de 3V3: 150.9 mm (antes 92.9).
  - **El puente de 3V3 en B.Cu se eliminó**: el plano GND queda sin ninguna pista.
  - **GND del DAC** (J5.2, J5.6 = SCK, C3.2 y C4.2): directo al plano de B.Cu con alivios térmicos.
- **Aviso: también se re-ruteó el haz de la cruceta en el tramo entre J2 y x = 50** (ninguna huella se movió). J5 cae justo donde pasaba el haz (y 48.6–51.6). Ahora sube por encima de J5 (y 44.1–45.6), baja bajo el DAC y desde x = 50 sigue igual que antes. DOWN pasa de 67.8 a 71.6 mm y LEFT de 79.3 a 81.4 mm; UP y RIGHT no cambian de largo.
- Ruteo total: 1094 mm en F.Cu (antes 980 mm en F.Cu + 9.4 mm en B.Cu).
- **`KIDBOX.kicad_pro` lo reescribió KiCad al cerrarse (no los scripts).**
  - En la prueba en una copia, con el proyecto anterior, los 5 tests de DRC seguían en "ignore".
  - En el proyecto real, al cerrar KiCad quedaron en **"warning"** (`footprint_filters_mismatch`, `footprint_type_mismatch`, `missing_courtyard`, `track_not_centered_on_via`, `tuning_profile_track_geometries`) y se agregó el bloque `erc`, con 4 tests de ERC en "ignore".
  - Los scripts solo tocan `rules` y las net classes, y conservan el resto, así que se deja como lo dejó KiCad.
  - Con eso, `verificar.py` ya corre esos 5 tests de DRC (0 avisos). `verificar_extra.py` activa los 4 de ERC (`footprint_filter`, `four_way_junction`, `simulation_model_issue`, `single_global_label`) y da 0.

## 9. Fase 3 — tercera ronda (14-oct-2026)

| # | Cambio | Archivos |
| :--- | :--- | :--- |
| 3.1 | B.SilkS junto a SW10: "ON/OFF" se reemplaza por **"OFF" en (136.54, 11.3)**, bajo el pad 2 (GND), y **"ON" en (131.46, 11.3)**, bajo el pad 3. Visto desde atrás (texto espejado) se lee OFF a la izquierda y ON a la derecha, como pide la sección 9. El cableado no cambia | `gen_pcb.py`, `KIDBOX.kicad_pcb`, `verificacion/3d_bottom.png` |
| 3.2 | **Metadatos de unidad en las 20 huellas**: `(units (unit (name "A") (pins "1" "2" ...)))` justo después de `(sheetfile ...)`, con los pines en el orden de la netlist (SW10: "1" "3" "2"; H1–H4: `(pins)` vacío) | `gen_pcb.py` (`con_unidades`), `verificar_extra.py` |

### 3.2 — cómo se supo qué campo es (sin adivinar)
- El demo oficial `share/kicad/demos/pic_programmer/pic_programmer.kicad_pcb` tiene la misma versión de archivo que el nuestro (`20260206`). Todas sus huellas llevan ese bloque tras `sheetfile`, y los agujeros de montaje lo llevan con `(pins)` vacío. Es la copia que hace F8 del bloque `(units ...)` de la netlist (`kicad-cli sch export netlist`).
- El API de Python tiene `FOOTPRINT.SetUnitInfo` / `FP_UNIT_INFO`, pero la lista de pines (`m_pins`) no está expuesta. Por eso `gen_pcb.py` inserta el bloque en el texto del archivo, antes de reescribir los UUID.
- **Comprobado con KiCad:** `verificar.py` carga y vuelve a guardar el PCB con `kicad-cli` (`--save-board`), y los 20 bloques siguen ahí. KiCad los lee como propios.
- `verificar_extra.py` ahora compara también las unidades, que lee del `.kicad_pcb`. Con el PCB anterior daba **20 cambios, los mismos 20 que mostró F8 en la GUI**; con el nuevo da **0**.
- Falta confirmarlo con F8 en la GUI: no debería quedar ningún "Actualizar metadatos de unidad".

## 10. Fase 4 — paquete de fabricación PRELIMINAR (14-oct-2026)

El alumno aprobó el PCB por escrito para la **entrega preliminar del 16-oct** ("Doy por aprobado el PCB para la entrega PRELIMINAR").
**El `.kicad_pcb` no se modificó en esta fase:** su md5 es el mismo antes y después (`6d5a8ce3…`), y `gen_fabricacion.py` lo comprueba.

| Script | Qué hace | Cómo se ejecuta (desde `hardware/`) |
| :--- | :--- | :--- |
| `scripts/gen_fabricacion.py` | Genera en `fabricacion/` los Gerbers (F/B.Cu, F/B.Mask, F/B.SilkS, Edge.Cuts; extensiones Protel, X2), los taladros Excellon (mm, origen absoluto, PTH y NPTH separados, mapas PDF y reporte), `KIDBOX_gerbers_PRELIMINAR.zip` y los PDF 1:1 de frente y reverso | `python scripts/gen_fabricacion.py` |

- Comprobado en los archivos generados:
  - El contorno del Gerber mide 150.000 × 65.000 mm.
  - F.Cu solo tiene aperturas de 0.25, 0.40 y 0.50 mm (pistas) y pads; B.Cu tiene una sola zona y pads.
  - Taladros: 101 PTH (9 × 0.8, 60 × 1.0, 32 × 1.1) y 4 NPTH (2.2 mm), que coinciden con las piezas.
- **PDF 1:1 con escala 1.0001.** Con escala exactamente 1, KiCad deja la placa en su posición absoluta, pegada a la esquina de la hoja: la impresora recorta unos 4 mm y el reverso espejado se sale de la hoja. Con 1.0001 la centra; el error es de 0.015 mm en 150 mm.
- **Interactive HTML BOM:** el plugin no está instalado y no se instaló (hace falta permiso). Se genera desde la GUI: *Herramientas → Gestor de plugins y contenidos → "Interactive Html Bom" → Instalar*; después, en el editor de PCB, *Herramientas → Plugins externos → Generate Interactive HTML BOM*, con salida en `fabricacion/`.
- ~~**Pendiente sin tocar:** la nota de SW10 en `BOM.csv` todavía dice "paso 2.54 mm [PENDIENTE: protoboard]", aunque la sección 11 ya lo da por confirmado.~~ **(Corregido en la sección 11.)**
- `README.md` nuevo: recuadro "PRELIMINAR — NO FABRICAR" con los pendientes de la sección 11, orden de soldadura, notas de montaje, parámetros de pedido y revisión en el visor de JLCPCB.

## 11. Fase 4 — BOM al día y ubicación del número de pedido (14-oct-2026)

| # | Cambio | Archivos |
| :--- | :--- | :--- |
| 4.1 | Nota de SW10 en la BOM: "paso 2.54 mm **confirmado en protoboard (14-oct)**", como en la sección 11 de la especificación. En `DECISIONES.md` se marcan como resueltos (tachados o anotados, sin borrar la historia) el paso de SW10 y el orden de J5. Lo único que sigue `[PENDIENTE]` es la posición OFF de SW10 por continuidad, que está abierta de verdad. La pantalla ya figuraba como confirmada en el README | `kidbox_datos.py` → `BOM.csv`; `DECISIONES.md` |
| 4.2 | Texto **"JLCJLCJLCJLC"** en B.SilkS (alto 1.0 mm, trazo 0.15 mm) en **(102.5, 33), vertical**, dentro de la zona de batería. Queda centrado en y y simétrico con "sin patas THT" (x 109) respecto de "BATERÍA 103450" (x 105.75), sin tocarlo. En el README: **"Order number: Specify a location"** | `gen_pcb.py`, `KIDBOX.kicad_pcb`, `README.md`, Gerbers y zip |

- El PCB solo cambia en ese texto: las 116 pistas tienen la misma geometría que en el commit anterior (cambia su orden en el archivo porque se corren los UUID).
- `verificar.py`: SIN ERRORES. `verificar_extra.py`: 0 en todo, F8 en seco con 0 cambios.
- Gerbers y zip regenerados (`B_Silkscreen.gbo` pasa de 62.6 a 67.2 KB por el texto).

## 12. Fase 4 — nada bajo el DAC y C3 lejos del borde (21-oct-2026)

Pedido por el alumno, que también autorizó actualizar `ESPECIFICACION.md` (secciones 6 y 11, cambio 8). **Por qué:** que ninguna pata
quede bajo el DAC, por si el módulo se suelda directo a la placa (sin tira hembra) para bajar el grosor, y que C3 no quede al borde.

| # | Pieza | Antes | Ahora |
| :--- | :--- | :--- | :--- |
| 5.1 | J3 (Top) | x 38.41, centro y = 28 (pines y 11.49–44.51) | x 38.41, **centro y = 25 (pines y 8.49–41.51)** |
| 5.1 | C2 (Top) | (34.6, 11.49) / (34.6, 13.99) | **(34.6, 8.49) / (34.6, 10.99)**, pad 1 a la altura del pin 1 de J3 |
| 5.1 | Contorno de la pantalla (F.SilkS) | x 36.41–113.59, y 6.64–49.36 | x 36.41–113.59, **y 3.64–46.36** |
| 5.2 | J5 (Bottom) | x = 59, y 47.1–59.8 | **x = 56**, y 47.1–59.8 (VIN abajo) |
| 5.2 | Contorno del DAC (B.SilkS) | x 28.65–60.5, y 44.2–61.98 | **x 25.65–57.5**, y 44.2–61.98 |
| 5.2 | Jack (B.SilkS) | x 30–36, y 52–64.3, centro x = 33 | **x 27–33**, y 52–64.3, **centro x = 30**, boca al borde inferior |
| 5.3 | C3 (Bottom) | horizontal en y = 63.3 (pads x 60.6 / 58.1), junto al borde | **vertical en x = 59.5: pad 1 (+3V3) en y = 59.8 (altura de VIN), pad 2 (GND) en y = 57.3** |

Medidas (con `pcbnew` sobre el archivo generado):
- **J3:** el último pin (14) queda a 2.69 mm del borde superior del DAC (y 44.2), centro a centro, y el borde de su pad a 1.84 mm (pedido: ≥ 1.5).
  Su courtyard termina en y 43.33, también fuera.
- **C3:** cobre en x 58.7–60.3. Quedan 1.85 mm de cobre a J5 y 1.98 mm a los pads de SELECT (pedido: ≥ 0.5). El contorno del DAC queda a
  1.2 mm. Sus agujeros quedan fuera del courtyard de SW5 (desde x 61.75), que es lo que en la Fase 3 impidió poner C4 entre las patas de SW5.
- `gen_pcb.py` ahora **falla** si alguna pata, salvo las de J5, cae dentro del contorno del DAC, o si J3 queda a menos de 1.5 mm de él.

Ruteo (sigue sin vías y sin pistas en B.Cu; 116 segmentos, 1096 mm):
- **SPI (CS, RST, DC, MOSI, SCK):** los huecos de J2 no se mueven, así que las pistas llegan 0.22 mm por encima de los pines de J3. Hay un salto
  corto a 45° en x 45.5 (antes la diagonal bajaba 3.22 mm). LED baja 1.49 mm en x 45.5–47.
- **3V3:** J2.16 → diagonal a J3.1 (38.41, 8.49) → C2 → x 36.2 hasta y 30.08. El tramo de 0.40 mm pasa entre los pines 9 y 10 de J3 (antes en y 33.08).
  Sigue por y 30.08 hasta el mismo paso entre J2.10 y J2.9. Después baja por x 69.5 y por **x 61.3, entre C3 y SELECT**. Desde ahí, una rama va
  a C3.1 y J5.1 (y 59.8) y la otra a C4+ por y 62.4, como antes.
- **I2S y cruceta:** el mismo trazado de la Fase 3, corrido 3 mm a la izquierda junto con J5 (LCK sigue cruzando entre los pines 5 y 4).
  Las diagonales del haz de la cruceta bajan en x 51.5–53 → 47, antes en x 54.5–56 → 50.
- Serigrafía que se movió con sus piezas: "PANTALLA TFT 2.4" (J3)" en y = 6, el "1" de J3 en y = 6.3 y las referencias de J3 y C2.
  En el DAC: "JACK" en x = 30, "DAC PCM5102" en x = 42, "VIN"/"GND" en x = 52.9, la referencia de J5 en (53, 48.4) y la de C3 en (59.5, 61.7).
- No se movió nada más: pulsadores, RP2350-Plus, SW10, C4, agujeros, zona de batería y textos de batería y JLC.

Resultado: `verificar.py` SIN ERRORES (ERC 0/0, DRC 0/0, sin conectar 0, paridad 0). `verificar_extra.py`: 0 en todo y F8 con 0 cambios.
Gerbers, zip y PDF 1:1 regenerados. Como el PCB cambió, la prueba de impresión 1:1 del README hay que repetirla.

## 13. v0.8 — C2 y C3 con huella de paso 5 mm (21-oct-2026)

Los cerámicos reales de 100 nF tienen **paso de 5 mm (medido por el alumno)**. C2 y C3 pasan de `C_Disc_D3.0mm_W1.6mm_P2.50mm` a
**`Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm`**. Los pads siguen siendo de Ø1.6 mm con taladro de 0.8 mm, así que el total de taladros
no cambia (9 × 0.8 mm). Se cierra el pendiente "paso de patas de C2/C3"; sigue abierto el de C4.

| Pieza | Antes (paso 2.5 mm) | Ahora (paso 5 mm), ambos en vertical |
| :--- | :--- | :--- |
| C2 (Top) | (34.6, 8.49) / (34.6, 10.99) | **pad 1 (+3V3) en (34.6, 8.49)**, a la altura del pin 1 de J3; **pad 2 (GND) en (34.6, 13.49)** |
| C3 (Bottom) | (59.5, 59.8) / (59.5, 57.3) | **pad 1 (+3V3) en (59.5, 59.8)**, a la altura de VIN; **pad 2 (GND) en (59.5, 54.8)** |

Separaciones, medidas con `pcbnew` entre el contorno de cada pad y cualquier pad o pista de otra red (pedido: ≥ 0.5 mm):
- **C2:** la menor es 0.55 mm, del pad 2 (GND) a la pista vertical de 3V3 en x = 36.2. Le siguen J3.3 a 2.16 mm y LCD_CS a 2.89 mm.
  Courtyard en x 33.05–36.15, fuera del de J3 (desde x 36.59).
- **C3:** la menor es 0.75 mm, del pad 2 (GND) a la pista de 3V3 en x = 61.3. Le siguen el codo de 3V3 en (61.3, 53.4) a 1.23 mm y I2S_DIN
  (y 52.6) a 1.27 mm. Además quedan 1.85 mm a J5 y 1.98 mm a SELECT. El cobre ocupa x 58.7–60.3, a 1.2 mm del contorno del DAC (x 57.5).
- No hubo que re-rutear: las pistas existentes ya dejan esas separaciones. Solo se movió la referencia de C2 a (32.3, 10.99) para que
  no pise el cuerpo, que ahora es más largo.
- Archivos: `kidbox_datos.py` (FP_C), `gen_bom_netlist.py` (descripción), `gen_pcb.py` → `KIDBOX.kicad_sch`, `BOM.csv`, `KIDBOX.kicad_pcb`.

Resultado: `verificar.py` SIN ERRORES y `verificar_extra.py` en 0 (F8 con 0 cambios). Imágenes, Gerbers, zip y PDF 1:1 regenerados.

## 14. v0.8 — C4 medido (21-oct-2026)

- **C4 real (medido por el alumno):** Ø ≈ 4 mm, alto ≈ 7–8 mm, paso ≈ 1.5 mm.
- **Se mantiene la huella `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm`, por decisión del alumno.** Las patas se abren 0.25 mm por lado al
  soldar. El contorno de Ø5 mm de la huella cubre el cuerpo real de Ø4 mm. **El PCB no cambia**: mismo `.kicad_pcb`, Gerbers y zip.
- Se cierra el pendiente de C4 (sección 11 de la especificación y recuadro del README).
- La tabla de soldadura del README dice "abrir levemente las patas de C4" y "respetar la polaridad". La nota de C4 en `BOM.csv` sale de `kidbox_datos.py`.

## 15. v0.8 — continuidad de SW10 confirmada (21-oct-2026)

- **Medido por el alumno en protoboard.** Visto desde arriba, que es la vista desde atrás de la consola: con la palanca a la izquierda, el común
  se une con la pata izquierda, y con la palanca a la derecha, con la derecha.
- **Coincide con el diseño**, sin cambios: OFF junto al pad 2 (GND, x 136.54) y ON junto al pad 3 (x 131.46). Visto desde atrás, OFF queda a la
  izquierda y ON a la derecha (sección 9, ronda 3.1).
- Se cierra el pendiente en la sección 11 de la especificación, en el recuadro del README y en la nota de SW10 de `BOM.csv`. **El PCB no cambia.**

## 16. v0.9 — 155 × 75, simetría, imagen centrada, DAC adelante y correcciones del profesor (26-oct-2026)

Fuentes: informe del profesor del 22-oct (`G5_SUGERENCIAS.md` y `G5_ESTUDIO_ERGONOMICO.md`, carpeta de documentación del curso) y
decisiones del equipo del 23–26 oct. El plan de coordenadas se aprobó antes de implementarlo; la especificación pasa a la v0.9.

### Qué cambió

| Elemento | v0.8 | v0.9 |
| :--- | :--- | :--- |
| Placa | 150 × 65, agujeros en (4, 4), (146, 4), (4, 61), (146, 61) | **155 × 75**, agujeros en (4, 4), (151, 4), (4, 71), (151, 71); eje x = 77.5 |
| Pantalla | módulo centrado en (75, 25), J3 en x = 38.41 | **imagen** centrada en (77.5, 25); módulo en (73.5, 25), x 34.91–112.09; **J3 en x = 36.91** |
| RP2350-Plus | columnas 66.11 / 83.89 | **68.61 / 86.39**; USB-C x 73.2–82.15 (plano oficial) |
| Zona de batería | x 88.0–123.5, y 4–62 | **x 90.5–126.0**, y 4–62 |
| DAC | atrás, J5 en x = 56, jack en x ≈ 30 | **adelante**, huella propia, J5 en x = 52.6 (VIN y = 71.2), módulo x 51.1–82.95 × y 56.1–73.6, **jack x 75.15–79.85, boca en y = 75** |
| Cruceta | centro (18, 30) | **centro (18, 44)**, brazos de 10 mm |
| A / B | (138, 25) / (128, 35) | **(142, 39) / (132, 49)** (espejo de la cruceta) |
| SELECT / START | (66.5, 58) / (83.5, 58) | **(41, 67) / (114, 67)** |
| SW10 | atrás, (134, 8) | atrás, **(50, 8)**; pad 2 (GND = OFF) en x = 52.54 |
| C2 | (34.6, 8.49 / 13.49) | (33.1, 8.49 / 13.49) |
| C3 | atrás, (59.5, 59.8 / 54.8) | **adelante**, + en (48.3, 67.6), GND en (48.3, 62.6) |
| C4 | atrás, `CP_Radial_D5.0mm_P2.00mm` en (74, 59) | **adelante, `CP_Radial_D4.0mm_P1.50mm`**, + en (49.05, 71.2) a la altura de VIN |
| TP1 / TP2 | — | **(29.8, 8.49) +3V3 / (29.8, 13.49) GND** |
| BT1 | — | símbolo `Device:Battery_Cell` "LiPo 103450 3.7V 2000mAh", excluido de la placa |

### Decisiones y supuestos del agente

- **26-oct · Librería de la huella del DAC con nombre `Connector_KIDBOX`** (carpeta `KIDBOX/KIDBOX.pretty`, tal como se pidió). Por qué: el
  símbolo `Conn_01x06` filtra huellas con `Connector*:*_1x??_*` y `verificar_extra.py` activa ese test como error; con una librería
  llamada `KIDBOX` el test fallaría. La huella se llama `GY-PCM5102_1x06_P2.54mm`. Si está mal: solo cambia el nombre (sin efecto eléctrico).
- **26-oct · Pads de la huella del DAC iguales a los de la tira oficial** (1.7 mm, taladro 1.0, pad 1 cuadrado). El contorno de la boca del
  jack (lo que sobresale 1.4 mm) va solo en F.Fab: en F.SilkS llegaría al borde de la placa.
- **26-oct · Ruteo del I2S.** J2 tiene DIN, LRCK, BCK de arriba abajo y J5 tiene BCK, DIN, LCK. El orden está rotado y VIN cierra la columna
  de J5 por abajo, así que sin vías una de las tres tiene que pasar entre pines (se comprobó con las cuatro combinaciones de entrada por la
  izquierda o la derecha de J5). Se eligió **LRCK entre J2.30 (RUN, sin uso) y J2.29 (DIN)**, aceptado por el alumno. El riesgo es un
  puente LRCK–RUN, que reiniciaría el módulo: está en el README.
- **26-oct · 3V3 al DAC.** Baja por la izquierda de J3, pasa **bajo J3.14** (sin pasar entre pines de J3), sube en diagonal bajo la pantalla y
  entra al interior del módulo **entre J2.31 (LCD_LED) y J2.30 (RUN)** con un tramo de 0.25 mm × 4 mm (0.295 mm a cada pad, unos 3 mΩ más).
  Llega a VIN por la derecha y sigue a C4+ y a C3. Largo total de +3V3: 194 mm de 0.5 mm, unos 0.2 Ω, 6 mV a 30 mA.
- **26-oct · TP1/TP2 excluidos de la BOM y de los archivos de posición**, igual que la huella oficial `TestPoint_THTPad`, para que F8 no
  cambie nada. Figuran en `BOM_compra.csv` con costo 0.
- **26-oct · Alturas (sección 6):** tira hembra de 8.5 mm (estándar) y alto del jack ≈ 6 mm (provisorio, dato del alumno) → DAC con socket
  ≈ 18.6 mm; grosor sin carcasa ≈ 32 mm. Si el jack mide distinto, cambia la abertura de la carcasa, no la placa.
- **26-oct · Imagen dibujada con el dato del panel (48.96 × 36.72).** Las medidas 19 + 11 mm suman 1.8 mm más que el módulo con un área de 49 mm;
  el centro (desfase de 4.0 mm) no depende de eso.
- **26-oct · `BOM_compra.csv`:** precio, proveedor y código quedan "por cotizar" donde el equipo no los fijó. No se inventaron.
- **26-oct · Paquete de entrega** (`scripts/gen_entrega.py`): `entrega/KIDBOX_PCB_v0.9/` copia la misma estructura del repositorio (README,
  especificación, DECISIONES, `KIDBOX/`, `fabricacion/`, `scripts/`) más un zip. Así la tabla de archivos del README vale para los dos. La
  carpeta `entrega/` no se versiona en git porque se regenera con el script.

### Holguras logradas (medidas con `pcbnew`)

| Qué | Mínimo pedido | Logrado |
| :--- | :--- | :--- |
| Capuchón Ø10 → contorno de la pantalla | 1.5 mm | **1.91 mm** (RIGHT); el resto ≥ 11.9 mm |
| Capuchón Ø10 → contorno del DAC | 1.5 mm | **5.10 mm** (SELECT) |
| DAC → pantalla (en planta) | — | 9.74 mm |
| Pista → pad de otra red (regla `pista_lejos_de_pad_ajeno`) | 0.29 mm | **0.295 mm**, solo en los cruces entre pines de J2 (SPI ×5, +3V3, LRCK); el resto ≥ 0.40 mm |
| 3V3 → pad de otra red (regla `3V3_lejos_de_pads`) | 0.29 mm | **0.295 mm** en J2.31/J2.30. Los dos pads de C4 quedan a 0.30 mm entre sí (paso 1.5 mm, Ø1.2 de la huella oficial) |
| BCK → J2.21 | 0.29 mm | 0.845 mm |
| Pista → pista | 0.20 mm | 0.35 mm |
| Cobre → borde | 0.30 mm | 1.07 mm (J1.1 / J2.20, igual que antes); PWR_EN a 7.9 mm del borde superior |
| Patas THT → zona de batería | fuera | B a 1.75 mm (x), START a 1.75 mm (y) |
| Courtyards C3 / C4 / SELECT / DAC | sin solaparse | SELECT ≤ 45.80 · C3 46.76–49.84 · C4 46.00–50.59 · DAC ≥ 50.80 (x) |

Cuando el mínimo de las reglas se sube a 0.40 mm (prueba en una copia), el DRC marca exactamente los 7 cruces de J2 y los pads de C4.
Eso demuestra que las reglas están activas.

### Verificación

`verificar.py`: ERC 0/0 · DRC 0 errores, 0 avisos (con las reglas de 0.29 mm) · 0 sin conectar · paridad 0 → SIN ERRORES.
`verificar_extra.py`: ERC, DRC, sin conectar y paridad en 0 con los tests ignorados activados; F8 en seco con 0 cambios (22 símbolos, 22 huellas).
Placa: 101 segmentos, 1192 mm, 0 vías. Taladros PTH: 2 × 0.6 (C4), 7 × 0.8 (C2, C3, SW10), 62 × 1.0 (J1, J2, J3, J5, TP1, TP2) y
32 × 1.1 (pulsadores) = 103; NPTH 4 × 2.2. Archivos: Gerbers, taladros, `fabricacion/KIDBOX_gerbers_v0.9_PRELIMINAR.zip` y PDF 1:1 en
A4 y Carta.

## 17. v0.9 — ajuste tras la prueba 1:1: 150 × 70, controles Ø9, muro DAC–pantalla, batería en carcasa (26-oct-2026)

Decisiones del equipo tras imprimir la v0.9 a escala real. Sigue siendo la v0.9 y va en el mismo PR #27. Reemplaza las coordenadas de la
sección 16; el resto de la sección 16 (huella del DAC, C4 P1.50, reglas de 0.29 mm, LRCK y 3V3 por J2, TP, serigrafía) se mantiene.

| Elemento | v0.9 (sección 16) | Ajuste |
| :--- | :--- | :--- |
| Placa | 155 × 75, eje x = 77.5 | **150 × 70**, eje **x = 75**; agujeros en (4, 4), (146, 4), (4, 66), (146, 66) |
| Pantalla | módulo x 34.91–112.09, J3 en x = 36.91 | módulo **x 32.41–109.59**, **J3 en x = 34.41** (misma altura); imagen en x 50.52–99.48 |
| RP2350-Plus | 68.61 / 86.39 | **66.11 / 83.89**; USB-C x 70.7–79.65 |
| DAC | J5 en x = 52.6, VIN en y = 71.2, módulo y 56.1–73.6 | **J5 en x = 50.1, VIN en y = 66.2**, módulo **x 48.6–80.45, y 51.1–68.6**, jack x 72.65–77.35, boca en y = 70 |
| Cruceta | centro (18, 44), brazos de 10 | **centro (16.5, 39), brazos de 9**: UP (16.5, 30), DOWN (16.5, 48), LEFT (7.5, 39), RIGHT (25.5, 39) |
| A / B | (142, 39) / (132, 49) | **(138, 34.5) / (129, 43.5)** (punto medio x = 133.5, diagonal de 9 mm) |
| SELECT / START | (41, 67) / (114, 67) | **(38.5, 62) / (111.5, 62)** |
| Capuchones | redondos Ø10 | **redondos Ø9** (mínimo 1.5 mm de aire a los módulos) |
| SW10 | (50, 8) | **(47.5, 8)**; pad 2 (GND = OFF) en x = 50.04 |
| C2 / TP1 / TP2 | x 33.1 / 29.8 | **x 30.6 / 27.3** (igual respecto de J3) |
| C3 / C4 | + en (48.3, 67.6) / (49.05, 71.2) | **+ en (45.8, 62.6) / (46.55, 66.2)** (grupo corrido −2.5 / −5 junto con SELECT y el DAC) |
| Batería | zona sin patas THT en x 90.5–126.0 | **va en la carcasa**: zona solo de referencia en x 88.0–123.5, y 4–62, con una flecha hacia el conector BAT. Patas THT permitidas (caen las de START); sin componentes altos de la cara Bottom |
| Muro | — | **franja de 4.74 mm** (y 46.36–51.1, x 48.6–80.45) sin piezas de la cara Top; línea "muro carcasa" en F.Fab en y = 48.73 |

### Decisiones y supuestos

- **26-oct · Muro colgante (decisión del alumno).** La franja de 4.74 mm entre la pantalla y el DAC no puede quedar libre de patas: las
  últimas patas del RP2350-Plus (J2.21/J2.22 en x = 66.11 y J1.19/J1.20 en x = 83.89, cobre en y 46.79–51.03) caen dentro. Para que el muro
  pasara entero por debajo de J2 habría hecho falta bajar el DAC 4.43 mm, y la placa no da. Por eso el muro cuelga de la tapa frontal, mide
  ≈ 2 mm, tiene una altura útil de 9 a 18 mm sobre la PCB y termina ≥ 4 mm sobre ella: pasa por encima de las soldaduras (≈ 2 mm). El
  generador comprueba que ninguna pieza de la cara Top tenga patas en la franja.
- **26-oct · J2.21 junto al DAC.** El cobre de J2.21 queda a 0.07 mm del contorno del DAC, por fuera.
  - No hay violación en el DRC: J2 está en la cara Bottom y J5 en la Top, y el agujero de J2.21 (hasta y 50.68) queda 0.13 mm fuera del
    courtyard de J5 (desde y 50.81).
  - Tampoco hay choque físico: la soldadura mide ≈ 2 mm y la placa del DAC está a ≈ 11 mm.
- **26-oct · Ruteo de la cruceta con brazos de 9 mm.** Entre las columnas de pads de la cruceta solo quedan 0.5 mm, y una pista de 0.25
  necesita 0.83 mm con la regla de 0.29. Por eso el ruteo usa los dos canales horizontales de 2.5 mm que quedan entre las filas.
  - RIGHT, LEFT y DOWN salen de J2 por la izquierda y van por el canal inferior (y 43.6 / 44.2 / 44.8).
  - **UP sale de J2 hacia el interior del módulo**, baja a 0.315 mm de J2.21–J2.23, pasa bajo la cruceta (y = 52), sube por el borde
    izquierdo (x = 2) y entra por el canal superior (y = 34.5) a su pad oeste. Es la única forma sin vías ni cambio de pines: en J2,
    RIGHT está por encima de UP y la cruceta ya no deja pasar una pista entre sus columnas.
  - UP mide ≈ 110 mm; para un pulsador eso no importa.
- **26-oct · A** pasa bajo B y sube por la derecha de A (x = 144), porque entre B y A también quedan 0.5 mm.
- **26-oct · Zona de batería.** Ahora es solo una referencia en B.SilkS. `gen_pcb.py` ya no prohíbe patas THT ahí; prohíbe el cuerpo
  (courtyard) de cualquier pieza de la cara Bottom salvo J1/J2.

### Holguras logradas (medidas con `pcbnew`)

| Qué | Mínimo | Logrado |
| :--- | :--- | :--- |
| Capuchón Ø9 → pantalla | 1.5 mm | **2.41 mm** (RIGHT); el resto ≥ 11.1 mm |
| Capuchón Ø9 → DAC | 1.5 mm | **5.60 mm** (SELECT) |
| Capuchón Ø9 → borde de la placa | — | 3.0 mm (LEFT); 3.5 mm (SELECT y START) |
| Franja del muro (pantalla → DAC) | 4.5 mm | **4.74 mm** |
| Pista → pad de otra red | 0.29 mm | 0.295 mm solo en los cruces de J2 (SPI ×5, 3V3, LRCK); después 0.31 (3V3 bajo J3.14) y 0.315 (UP junto a J2.21–J2.23) |
| Pista → pista | 0.20 mm | 0.305 mm (3V3 bajo J3.14 / RIGHT) |
| Cobre → borde | 0.30 mm | 1.07 mm (J1.1 / J2.20); SELECT a 1.275 mm del borde inferior; UP a 1.875 mm del borde izquierdo |
| Courtyards | sin solaparse | sin solapes (cruceta, A/B, C3/C4/SELECT/DAC) |

### Verificación

`verificar.py`: ERC 0/0 · DRC 0 errores, 0 avisos (con las reglas de 0.29 mm) · 0 sin conectar · paridad 0 → SIN ERRORES.
`verificar_extra.py`: ERC, DRC, sin conectar y paridad en 0 con los tests ignorados activados; F8 en seco con 0 cambios (22 símbolos, 22 huellas).
Placa: 103 segmentos, 1219 mm, 0 vías. Taladros: 103 PTH (2 × 0.6, 7 × 0.8, 62 × 1.0, 32 × 1.1) y 4 NPTH × 2.2.
`BOM_compra.csv`: capuchones Ø9 y "sujeción de la batería en la carcasa" en lugar de la cinta doble faz.

## 18. v1.0 — pistas a 45°, prueba 1:1 y versión de fabricación (27-oct-2026)

Revisión 2 del profesor (26-oct): aprobada salvo dos puntos, las esquinas a 90° y la prueba 1:1 de la 150 × 70. Van en el mismo PR #27.

### Esquinas a 45°

- **Antes:** 82 vértices entre dos pistas; 46 a 45°, **33 a 90°** y 3 colineales. Coincide con el conteo del profesor.
- **Cómo se corrige:** en `gen_pcb.py`, antes de crear las pistas.
  - Se reemplaza cada vértice donde se juntan exactamente dos segmentos de la misma red y capa formando 90°. Se tratan también los que vienen
    de polilíneas distintas: 3 de las 33 esquinas estaban en el centro de un pad, donde la llegada al pulsador se junta con la unión de sus
    dos pads.
  - El reemplazo es un chaflán: dos puntos a d = 1.0 mm del codo, o d = largo/2 si un tramo mide menos de 2d.
  - Si el chaflán queda a menos de 0.29 mm de un pad de otra red, o a menos de 0.30 mm de otra pista, d se achica en ese codo (0.75, 0.5,
    0.35 o 0.25 veces).
  - **Supuesto del agente:** el límite de 0.30 mm entre pistas es más exigente que el mínimo del proyecto (0.20). Se puso para no empeorar
    la separación de la v0.9 (0.305 mm). Con 0.20, un chaflán de I2S_DIN quedaba a 0.245 mm de I2S_BCK, que era legal pero peor.
  - No se movió ninguna huella.
- **Después:** 115 vértices; **112 a 45°**, 3 colineales y **0 a 90°**. 33 chaflanes; 12 con d < 1.0 mm:
  - **por tramo corto:** LRCK en (64.5, 34.94), RIGHT en (28.75, 41.25), PWR_EN y los dos codos de UP junto a J2;
  - **por holgura:** los codos del haz I2S bajo J2.21 y junto a J5, con d = 0.35–0.945 mm.
- **`verificar_extra.py`** suma un tercer paso: une los segmentos por red y capa, mide el giro en cada vértice y falla si alguno es de 90°.
  También falla si una pista llega en T a 90° a otra de la misma red.
- **Holguras:**
  - **Pista → pad de otra red:** mínimo **0.295 mm**, en los mismos 14 pares de antes (cruces de J2: SPI ×5, 3V3 y LRCK). Siguen 0.31 mm
    (3V3 bajo J3.14) y 0.315 mm (UP junto a J2.21–J2.23).
  - **Pista → pista:** 0.305 mm.
- **Placa:** 136 segmentos, 1202 mm, 0 vías. Taladros sin cambios: 103 PTH y 4 NPTH.

### Prueba 1:1 (27-oct, hecha por el alumno)

- **Fotos** en `KIDBOX/verificacion/`: `prueba_1a1_v09_frente.jpg`, `prueba_1a1_v09_reverso.jpg`, `prueba_1a1_v09_escala_largo.jpg` y
  `prueba_1a1_v09_escala_alto.jpg`.
- **Resultado:**
  - escala 150 × 70 confirmada con regla;
  - pantalla, DAC (jack centrado, boca al borde), pulsadores, C3, C4, RP2350-Plus, batería y SW10 calzan.
- **C2 no aparece** porque se perdió la pieza (es igual a C3). En `BOM_compra.csv` pasa de 4 a 5 condensadores de 100 nF.
- **Carcasa:** el README anota que la batería se orienta con el cable hacia el conector BAT.
- **Serigrafía de las fotos:** dice v0.9. La v1.0 tiene la misma geometría; solo cambian las esquinas de las pistas y el número de versión.

### Versión de fabricación

- **Todo pasa a v1.0:** serigrafía ("KIDBOX v1.0 2026" y cajetín "KIDBOX v1.0 - 27-oct-2026"), revisión y fecha de los cajetines del
  esquemático y del PCB, `ESPECIFICACION.md` (v1.0), README, `BOM_compra.csv`, `fabricacion/KIDBOX_gerbers_v1.0.zip` y la carpeta de entrega
  `KIDBOX_PCB_v1.0/`.
- **README:** se quita "PRELIMINAR — NO FABRICAR". Quedan los pendientes de después de la placa:
  - revisar con lupa los cruces LRCK–RUN y 3V3–RUN en J2;
  - SW10 en ON/OFF y la corriente en OFF;
  - TP1–TP2;
  - carcasa;
  - alto del jack;
  - polaridad del adaptador;
  - puente J1 de la pantalla.

### Verificación

`verificar.py`: ERC 0/0 · DRC 0 errores, 0 avisos (con las reglas de 0.29 mm) · 0 sin conectar · paridad 0 → SIN ERRORES.
`verificar_extra.py`: ERC, DRC, sin conectar y paridad en 0 con los tests ignorados activados; F8 en seco con 0 cambios; esquinas a 90°: 0.
