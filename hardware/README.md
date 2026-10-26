# KIDBOX — PCB v0.9

> ## ⚠️ PRELIMINAR — NO FABRICAR
> Los Gerbers de `fabricacion/` son la **versión v0.9 (26-oct-2026)**, con las correcciones del profesor del 22-oct. **No se pagan ni se
> fabrican** hasta cerrar los pendientes que afectan a la placa (`ESPECIFICACION.md`, sección 11). Si alguno obliga a cambiarla, se
> corrige en los scripts, se regenera todo y se vuelven a generar los Gerbers.
>
> - [ ] **Prueba 1:1 de la v0.9:** imprimir `fabricacion/KIDBOX_1a1_frente_A4.pdf` y `KIDBOX_1a1_reverso_A4.pdf` (o las versiones `_Carta`)
>       al **100 % / tamaño real**. Medir con regla que la placa mida **155 × 75 mm** y apoyar encima las piezas reales: pantalla, DAC con su
>       tira (adelante), RP2350-Plus, pulsadores con capuchón, SW10, condensadores y la batería por detrás. Foto con la regla visible.
> - [ ] **Alto real del jack** sobre la placa del DAC (hoy ≈ 6 mm, provisorio): define la abertura de la carcasa, no la placa.
> - [ ] **Polaridad del adaptador de la batería** (lo hace el profesor): medir con el multímetro antes de conectar (rojo = + → ⊕ del BAT).
> - [ ] Pantalla: revisar el puente J1 del módulo (3.3 V). No afecta a la PCB.
> - [x] **Medidas del DAC (23–26 oct):** placa 31.85 × 17.5 mm (17.3–17.5), columna a 1.5 mm del borde corto y centrada, eje del jack a
>       24.9 mm de la columna, jack de 4.7 × 14 mm que sobresale 1.4 mm. Ya están en la huella propia de J5.
> - [x] **DAC con 3V3 (23-oct):** VIN = 3.26 V, A3V3 = 3.27 V, suena en estéreo con audífonos. Puentes: venían abiertos; en este módulo
>       **H3L controla FMT y H4L controla XSMT**. Quedaron FLT/DEMP/FMT = L y **XSMT = H** (3.21 V). VIN se queda en 3V3.
> - [x] **RP2350-Plus:** 21.0 × 51.55 mm y filas a 17.78 mm (confirmado); el USB-C llegó al borde en las pruebas 1:1 de la v0.7 y la v0.8.
> - [x] **Continuidad de SW10 (21-oct):** la palanca une el común con la pata de su lado. OFF = pad conectado a GND.
> - [x] **Condensadores medidos (21-oct):** C2/C3 con paso de 5 mm; C4 de Ø ≈ 4 mm, alto 7–8 mm y paso 1.5 mm (desde la v0.9, huella P1.50).
>
> Con la placa armada (sugerencia del profesor 3.5): medir SW10 en ON y OFF (3V3_EN ≈ VSYS / 0 V), la corriente de la batería en OFF
> (esperable del orden de decenas de µA; si pasa de ≈ 1 mA algo queda alimentado) y TP1–TP2 ≈ 3.3 V con SW10 en ON.

## Qué es

Consola portátil educativa basada en el **Game★Mite v1.3.2 de Thomas Hugo Williams (CC BY 4.0)**. Placa de **155 × 75 mm**, 2 capas,
todo THT, **simétrica respecto de x = 77.5**. Lleva:
- un **Waveshare RP2350-Plus** (J1/J2, por detrás, centrado, con el USB-C en el borde superior);
- una **pantalla TFT ILI9341 de 2.4"** por SPI (J3, por delante), con la **imagen** centrada en la placa (`tft.setRotation(3)`);
- un **DAC PCM5102A (GY-PCM5102)** por I2S (J5, **por delante**, bajo la pantalla), con el **jack de 3.5 mm centrado** en el borde inferior;
- **8 pulsadores** con capuchones redondos de Ø10: cruceta a la izquierda, A y B en espejo a la derecha, SELECT y START abajo;
- un **interruptor ON/OFF** (SW10, por detrás, arriba a la izquierda) que corta 3V3_EN;
- **TP1 (+3V3) y TP2 (GND)**, puntos de prueba junto a C2;
- una **batería LiPo 103450** que va por detrás, en la zona marcada (sin patas THT debajo). Está en el esquemático como BT1, excluida de la placa.

Volumen por software, con máximo limitado.

**Referencias que faltan:** no hay C1, J4 ni SW9 porque se eliminaron en la v0.7 (RESET del frente y conector de la pantalla). No se
re-anotó para no cambiar referencias que ya están en la documentación y en las fotos.

## Archivos

La carpeta de entrega (`KIDBOX_PCB_v0.9/`, la arma `scripts/gen_entrega.py`) tiene la misma estructura que el repositorio:

| Ruta | Qué es |
| :--- | :--- |
| `README.md` | Este archivo |
| `ESPECIFICACION.md` | Fuente de verdad del proyecto (la escribe el alumno), v0.9 |
| `DECISIONES.md` | Supuestos y decisiones del diseño, fase por fase (la v0.9 está en la sección 16) |
| `KIDBOX/` | Proyecto KiCad 10: `KIDBOX.kicad_pro`, `.kicad_sch`, `.kicad_pcb`, `.kicad_dru` (reglas de 0.29 mm), `fp-lib-table` y `KIDBOX.pretty/` (huella propia del DAC) |
| `KIDBOX/BOM.csv` | Lista de materiales del esquemático (referencia, valor, huella, cara, notas) |
| `KIDBOX/BOM_compra.csv` | **Lista de compra completa**: módulos, batería, tiras, pulsadores, capuchones, tornillos, cinta y la placa, con cantidades, estado y proveedor (o "por cotizar") |
| `KIDBOX/netlist.csv` | Red, componente, pin y función de cada pin |
| `KIDBOX/verificacion/` | ERC/DRC en JSON, estadísticas, esquemático en SVG, cobre frontal y trasero (SVG) y vistas 3D (PNG) |
| `scripts/` | Generadores (huella del DAC, esquemático, BOM/netlist, PCB, fabricación, entrega) y verificaciones; cada uno dice cómo se ejecuta en su cabecera |
| `fabricacion/KIDBOX_gerbers_v0.9_PRELIMINAR.zip` | **Lo que se sube a JLCPCB:** Gerbers + taladros Excellon |
| `fabricacion/gerbers/` | Los mismos archivos sueltos, más los mapas de taladros (PDF) y el reporte de taladros |
| `fabricacion/KIDBOX_1a1_frente_A4.pdf`, `KIDBOX_1a1_reverso_A4.pdf` | Frente y reverso (espejado) a escala real en hoja A4, para la prueba de impresión |
| `fabricacion/KIDBOX_1a1_frente_Carta.pdf`, `KIDBOX_1a1_reverso_Carta.pdf` | Lo mismo en hoja Carta |

Para regenerar todo desde cero (con KiCad cerrado), desde la carpeta raíz:

```
python scripts/gen_huella_dac.py
python scripts/gen_esquematico.py
python scripts/gen_bom_netlist.py
"C:\Program Files\KiCad\10.0\bin\python.exe" scripts/gen_pcb.py
python scripts/verificar.py KIDBOX
"C:\Program Files\KiCad\10.0\bin\python.exe" scripts/verificar_extra.py KIDBOX
python scripts/gen_fabricacion.py
python scripts/gen_entrega.py
```

## Orden de soldadura

Las piezas de la **cara Bottom** se insertan por detrás y se sueldan por delante. Las de **Top** se insertan por delante y se sueldan
por detrás. Primero va todo Bottom y después Top, de lo más bajo a lo más alto.

| # | Ref | Cara | Pieza | Cuidado |
| :--- | :--- | :--- | :--- | :--- |
| 1 | J1 | Bottom | Tira hembra 1×20 (pines 1–20 del módulo) | Pin 1 = pad cuadrado, junto al USB-C. Cortar al ras |
| 2 | J2 | Bottom | Tira hembra 1×20 (pines 21–40) | **Poco estaño**: por delante pasan entre sus pines el haz SPI, 3V3 y LRCK (ver notas). Cortar al ras |
| 3 | SW10 | Bottom | Interruptor deslizante, paso 2.54 mm | Palanca hacia atrás; pad central = común. Las patas quedan bajo la pantalla: cortar al ras |
| 4 | C2 | Top | 100 nF cerámico (paso 5 mm) | Vertical junto al pin 1 de J3 |
| 5 | C3 | Top | 100 nF cerámico (paso 5 mm) | Vertical entre SELECT y el DAC, encima de C4 |
| 6 | C4 | Top | 10 µF 25 V electrolítico (Ø4 × 7–8 mm, paso 1.5 mm) | **Respetar la polaridad:** + en el pad cuadrado, del lado de J5 (a la derecha visto de frente). La huella ya tiene paso 1.5 mm: no hay que abrir las patas |
| 7 | J3 | Top | Tira hembra 1×14 (pantalla) | Pin 1 (VCC) arriba, marcado "1". Cortar al ras |
| 8 | J5 | Top | Tira hembra 1×6 (DAC) | VIN = pin 1, pad cuadrado, abajo. El DAC va con sus componentes hacia el frente y el jack hacia el borde inferior |
| 9 | SW1–SW8 | Top | Pulsadores 6×6 | Bien apoyados contra la placa para que los capuchones queden a la misma altura |

TP1 y TP2 son pads de la placa: no llevan pieza.

### Notas de montaje
- **J2 con poco estaño.** Entre sus pines pasan, por la cara donde se suelda, todas a 0.295 mm de cada pad:
  - el haz SPI (5 pistas);
  - **3V3**, entre J2.31 (LCD_LED) y J2.30 (RUN);
  - **I2S_LRCK**, entre J2.30 (RUN) y J2.29 (DIN).

  Hay que **revisar con lupa sobre todo el puente LRCK–RUN**: reiniciaría el módulo cada vez que suena el audio. Medir que no haya
  continuidad entre J2.30 y J2.29, entre J2.30 y J2.31, ni entre 3V3 (TP1) y J2.30 o J2.31.
- **J3 y J5 sin pistas entre sus pines** (v0.9). Se puede soldar normal.
- **DAC adelante:** la tira macho se suelda con el **plástico del lado sin componentes** del módulo. Los componentes del DAC quedan hacia el
  frente y la boca del jack al ras del borde inferior. Bajo el DAC no queda ninguna pata salvo las de J5, así que el módulo también se
  puede soldar directo a la placa para bajar el grosor.
- **Puentes del DAC:** FLT, DEMP y FMT = L; **XSMT = H** (sin él, el DAC queda en silencio). En este módulo H3L controla FMT y H4L controla XSMT.
- **Cortar al ras las patas de J1, J2, J3 y SW10** después de soldar: las de J1/J2 y SW10 quedan bajo la pantalla.
- La placa no tiene vías. La cara de atrás es un plano de masa con alivios térmicos, así que los pads de GND se sueldan igual que los demás.
- Antes de poner los módulos: medir que no haya corto entre **TP1 (3V3) y TP2 (GND)**.
- Firmware: `tft.setRotation(3)`; volumen limitado por software.

## Pedido en JLCPCB

| Parámetro | Valor |
| :--- | :--- |
| Archivo | `fabricacion/KIDBOX_gerbers_v0.9_PRELIMINAR.zip` (extensiones Protel, Gerber X2, taladros Excellon en mm con origen absoluto) |
| Base material | FR-4 |
| Layers | **2** |
| Dimensions | **155 × 75 mm** (lo detecta solo; el sobrecosto por pasar de 100 × 100 mm está aceptado) |
| PCB Qty | 5 (mínimo) |
| Product type | Industrial/Consumer electronics |
| Different design | 1 |
| Delivery format | Single PCB |
| PCB thickness | **1.6 mm** |
| PCB color | **Verde** |
| Silkscreen | Blanco |
| Surface finish | **HASL (with lead free)** |
| Outer copper weight | 1 oz |
| Via covering | Tented (la placa no tiene vías) |
| Mark on PCB / order number | **Order number: Specify a location**: va donde está el texto "JLCJLCJLCJLC" de la serigrafía inferior, dentro de la zona de batería |
| Gold fingers, castellated holes, edge plating | No |
| **PCB Assembly (PCBA)** | **No** (sin ensamblaje) |
| Stencil | No |
| Resto de opciones | Las que JLCPCB trae por defecto |

## Qué revisar en el visor de Gerbers de JLCPCB antes de pagar

1. **2 capas y 155 × 75 mm.** El contorno tiene esquinas redondeadas (r = 4 mm), sin líneas sueltas ni recortes de más.
2. **Taladros: 107 en total.**
   - 103 metalizados: 2 × 0.6 mm (C4), 7 × 0.8 mm (C2, C3 y SW10), 62 × 1.0 mm (J1, J2, J3, J5, TP1 y TP2) y 32 × 1.1 mm (pulsadores).
   - 4 sin metalizar de 2.2 mm, en las esquinas (4, 4), (151, 4), (4, 71) y (151, 71).
   - Ningún agujero en la zona de la batería (rectángulo marcado "BATERÍA 103450" por detrás).
3. **Cobre superior (Top):** todas las pistas están aquí. Las de señal son de 0.25 mm y las de 3V3 de 0.5 mm, salvo un tramo de 0.25 mm entre
   dos pines de J2. Ninguna pista toca un pad que no le corresponde. No hay vías.
4. **Cobre inferior (Bottom):** un plano de masa casi completo. Los pads de GND tienen alivios térmicos (4 "radios") y los demás pads,
   un anillo libre a su alrededor. No hay pistas.
5. **Máscara:** hay abertura en todos los pads, y ninguna sobre las pistas ni sobre el plano.
6. **Serigrafía superior:**
   - UP, DOWN, LEFT, RIGHT, A, B, SELECT y START junto a sus botones (texto de 1.2 mm);
   - el contorno de la pantalla con "PANTALLA TFT 2.4" (J3)" y "1" junto al pin 1 de J3, y dentro el contorno de la imagen;
   - el contorno del DAC con el jack, "DAC PCM5102", "VIN" y "GND" junto a J5;
   - "3V3" y "GND" junto a TP1 y TP2;
   - los créditos del Game*Mite entre el DAC y START.
7. **Serigrafía inferior.** En la vista desde arriba se ve espejada, que es lo correcto; al dar vuelta la placa en el visor se lee al derecho:
   - "VISTA POSTERIOR / FILAS ESPEJADAS", el contorno de la RP2350-Plus con el USB-C arriba y "1" en J1 y J2;
   - "OFF" y "ON" en SW10 (desde atrás, arriba a la derecha, con OFF a la izquierda);
   - "BATERÍA 103450" y, bajo la zona de batería, el cajetín "KIDBOX v0.9 – 155 x 75 mm – 1.6 mm – 2 capas".
8. Ningún texto de serigrafía cae sobre un pad. El DRC dio 0 avisos, pero hay que confirmarlo a la vista.
9. En la serigrafía inferior aparece **"JLCJLCJLCJLC"** en vertical, dentro de la zona de batería, junto a "BATERÍA 103450". Ahí JLCPCB pone su número de pedido (con "Specify a location").
10. Precio y plazo coherentes con 5 placas de 155 × 75 mm, sin ensamblaje ni opciones extra marcadas por error.

## Verificación del diseño (26-oct-2026)

`verificar.py`: ERC 0/0 · DRC 0 errores, 0 avisos (con las reglas de 0.29 mm de `KIDBOX.kicad_dru`) · 0 sin conectar · paridad
esquemático-PCB 0 · mínimos DFM OK.

`verificar_extra.py`:
- ERC y DRC con los tests que el proyecto ignora activados: 0.
- Emulación de "Actualizar PCB desde esquemático" (F8): 0 cambios.

Detalle y holguras medidas en `DECISIONES.md`, sección 16.

Licencia y créditos: basado en el Game★Mite de Thomas Hugo Williams (CC BY 4.0).
