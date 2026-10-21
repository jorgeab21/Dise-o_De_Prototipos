# KIDBOX — PCB v1.0

> ## ⚠️ PRELIMINAR — NO FABRICAR
> Los Gerbers de `fabricacion/` son la **entrega preliminar del 16-oct-2026**. **No se pagan ni se fabrican** hasta cerrar todos
> estos pendientes (`ESPECIFICACION.md`, sección 11). Si alguno obliga a cambiar la placa, se corrige en los scripts, se regenera
> y se vuelven a generar los Gerbers.
>
> - [ ] **Medidas del DAC con pie de metro:** posición de la columna de pines (hoy, a 1.5 mm del lado corto y centrada) y de la boca del
>       jack (hoy, centro en x = 30). Ambas son estimaciones de fotos. Si cambian, se mueven J5 y la serigrafía del DAC.
> - [ ] **Continuidad de SW10:** confirmar con el multímetro qué posición de la palanca une el pad central (1) con el pad 2 (GND). Esa
>       posición es OFF; la serigrafía dice OFF junto al pad 2 y ON junto al pad 3.
> - [ ] **DAC con 3V3 y audífonos en protoboard (16–17 oct):** que funcione con VIN = 3V3 y suene bien. Revisar los puentes del reverso
>       (FLT → L, DEMP → L, **XSMT → H**, FMT → L).
> - [ ] **Condensador C4:** paso de patas y diámetro reales (Ø5 mm, paso 2 mm) al recibirlo. C2/C3: paso de 5 mm medido el 21-oct ✅.
> - [ ] **Polaridad del adaptador de la batería** (lo hace el profesor): medir con el multímetro antes de conectar (rojo = + → ⊕ del BAT).
> - [ ] **Impresión 1:1:** imprimir `fabricacion/KIDBOX_1a1_frente.pdf` y `KIDBOX_1a1_reverso.pdf` al **100 % / tamaño real**. Medir con
>       regla que la placa mida 150 × 65 mm y apoyar encima las piezas reales: módulos, pulsadores, SW10, condensadores y batería.
> - [ ] Pantalla: confirmada el 15-oct. Falta solo revisar el puente J1 del módulo (3.3 V), que no afecta a la PCB.

## Qué es

Consola portátil educativa basada en el **Game★Mite v1.3.2 de Thomas Hugo Williams (CC BY 4.0)**. Placa de **150 × 65 mm**, 2 capas,
todo THT. Lleva:
- un **Waveshare RP2350-Plus** (J1/J2, por detrás, con el USB-C en el borde superior);
- una **pantalla TFT ILI9341 de 2.4"** por SPI (J3, por delante);
- un **DAC PCM5102A (GY-PCM5102)** por I2S, con jack de 3.5 mm para audífonos (J5, por detrás, con el jack hacia el borde inferior);
- **8 pulsadores** (cruceta a la izquierda; A y B a la derecha; SELECT y START bajo la pantalla);
- un **interruptor ON/OFF** (SW10, por detrás) que corta 3V3_EN;
- una **batería LiPo 103450** que va por detrás, en la zona marcada (sin patas THT debajo).

Archivos:

| Ruta | Qué es |
| :--- | :--- |
| `ESPECIFICACION.md` | Fuente de verdad del proyecto (la escribe el alumno) |
| `DECISIONES.md` | Supuestos y decisiones del diseño, fase por fase |
| `KIDBOX/` | Proyecto KiCad 10 (`.kicad_sch`, `.kicad_pcb`, `.kicad_pro`), `BOM.csv`, `netlist.csv`, `verificacion/` |
| `scripts/` | Generadores (esquemático, PCB, BOM/netlist, fabricación) y verificaciones; cada uno dice cómo se ejecuta en su cabecera |
| `fabricacion/KIDBOX_gerbers_PRELIMINAR.zip` | **Lo que se sube a JLCPCB:** Gerbers + taladros Excellon |
| `fabricacion/gerbers/` | Los mismos archivos sueltos, más los mapas de taladros (PDF) y el reporte de taladros |
| `fabricacion/KIDBOX_1a1_*.pdf` | Frente y reverso (espejado) a escala real, para la prueba de impresión |

Para regenerar todo desde cero (con KiCad cerrado), desde `hardware/`:

```
python scripts/gen_esquematico.py
python scripts/gen_bom_netlist.py
"C:\Program Files\KiCad\10.0\bin\python.exe" scripts/gen_pcb.py
python scripts/verificar.py KIDBOX
"C:\Program Files\KiCad\10.0\bin\python.exe" scripts/verificar_extra.py KIDBOX
python scripts/gen_fabricacion.py
```

## Orden de soldadura

Las piezas de la **cara Bottom** se insertan por detrás y se sueldan por delante. Las de **Top** se insertan por delante y se sueldan
por detrás. Primero va todo Bottom, de lo más bajo a lo más alto, y después Top.

| # | Ref | Cara | Pieza | Cuidado |
| :--- | :--- | :--- | :--- | :--- |
| 1 | J1 | Bottom | Tira hembra 1×20 (pines 1–20 del módulo) | Pin 1 = pad cuadrado, junto al USB-C. Cortar al ras |
| 2 | J2 | Bottom | Tira hembra 1×20 (pines 21–40) | Las pistas SPI y la de 3V3 pasan entre sus pines por delante: poco estaño. Cortar al ras |
| 3 | J5 | Bottom | Tira hembra 1×6 (DAC) | **Poco estaño**: la pista LCK pasa entre sus pines 5 y 4. VIN = pin 1, pad cuadrado, abajo |
| 4 | C3 | Bottom | 100 nF cerámico (paso 5 mm) | Vertical entre J5 y SELECT; pata +3V3 a la altura de VIN |
| 5 | C4 | Bottom | 10 µF 25 V electrolítico | **Polaridad:** + en el pad cuadrado (x = 74; visto desde atrás queda a la derecha) |
| 6 | SW10 | Bottom | Interruptor deslizante, paso 2.54 mm | Palanca hacia atrás; pad central = común |
| 7 | J3 | Top | Tira hembra 1×14 (pantalla) | Pin 1 (VCC) arriba, marcado "1". Cortar al ras |
| 8 | C2 | Top | 100 nF cerámico (paso 5 mm) | Vertical junto al pin 1 de J3 |
| 9 | SW1–SW8 | Top | Pulsadores 6×6 | Bien apoyados contra la placa para que los capuchones queden a la misma altura |

### Notas de montaje
- **J5 con poco estaño:** la pista I2S_LRCK (LCK) pasa entre los pines 5 y 4 de J5, por la cara donde se suelda. La máscara la protege,
  pero un puente de estaño la corta o la cortocircuita con BCK o DIN. Revisar con lupa y medir continuidad entre pines vecinos.
  Lo mismo con J2: el haz SPI pasa entre sus pines y 3V3 pasa entre J2.10 y J2.9.
- **J3 con poco estaño:** la pista de 3V3 (0.40 mm) pasa entre los pines 9 y 10 de J3, a 0.22 mm de cada pad. J3 se suelda por detrás
  y la pista va por delante, pero el estaño que sube por el agujero puede hacer puente. Igual que en J5 y J2: poco estaño, revisar
  con lupa y medir que no haya continuidad entre 3V3 y J3.9 ni J3.10.
- **Tira macho del DAC:** se suelda con el **plástico del lado sin componentes** del módulo. Los componentes del DAC quedan hacia afuera
  (tapa trasera) y el jack apunta al borde inferior.
- **Cortar al ras las patas de J1, J2 y J3** después de soldar. Las de J1/J2 quedan bajo la pantalla. Bajo el DAC no queda ninguna
  pata salvo las de J5, así que el módulo también se puede soldar directo a la placa para bajar el grosor.
- **Puente XSMT → H del DAC:** sin él, el DAC queda en silencio. Revisar también FLT → L, DEMP → L y FMT → L.
- La placa no tiene vías. La cara de atrás es un plano de masa con alivios térmicos, así que los pads de GND se sueldan igual que los demás.
- Antes de poner los módulos: medir que no haya corto entre 3V3 y GND (J2.16 contra J2.18, o J5.1 contra J5.2).

## Pedido en JLCPCB

| Parámetro | Valor |
| :--- | :--- |
| Archivo | `fabricacion/KIDBOX_gerbers_PRELIMINAR.zip` (extensiones Protel, Gerber X2, taladros Excellon en mm con origen absoluto) |
| Base material | FR-4 |
| Layers | **2** |
| Dimensions | **150 × 65 mm** (lo detecta solo; el sobrecosto por pasar de 100 × 100 mm está aceptado) |
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
| Mark on PCB / order number | **Order number: Specify a location** — va donde está el texto "JLCJLCJLCJLC" de la serigrafía inferior, dentro de la zona de batería |
| Gold fingers, castellated holes, edge plating | No |
| **PCB Assembly (PCBA)** | **No** (sin ensamblaje) |
| Stencil | No |
| Resto de opciones | Las que JLCPCB trae por defecto |

## Qué revisar en el visor de Gerbers de JLCPCB antes de pagar

1. **2 capas y 150 × 65 mm**. El contorno tiene esquinas redondeadas (r = 4 mm), sin líneas sueltas ni recortes de más.
2. **Taladros: 105 en total.**
   - 101 metalizados: 9 × 0.8 mm (C2, C3, C4 y SW10), 60 × 1.0 mm (J1, J2, J3 y J5) y 32 × 1.1 mm (pulsadores).
   - 4 sin metalizar de 2.2 mm, en las esquinas (4, 4), (146, 4), (4, 61) y (146, 61).
   - Ningún agujero en la zona de la batería (rectángulo marcado "BATERÍA 103450" por detrás).
3. **Cobre superior (Top):** todas las pistas están aquí (0.25 mm de señal; 0.5 mm de 3V3, con dos tramos de 0.4 mm entre pines de J3 y de J2).
   Ninguna pista toca un pad que no le corresponde. No hay vías.
4. **Cobre inferior (Bottom):** un plano de masa casi completo. Los pads de GND tienen alivios térmicos (4 "radios") y los demás pads,
   un anillo libre a su alrededor. No hay pistas.
5. **Máscara:** hay abertura en todos los pads, y ninguna sobre las pistas ni sobre el plano.
6. **Serigrafía superior:**
   - UP, DOWN, LEFT, RIGHT, A, B, SELECT y START junto a sus botones;
   - el contorno de la pantalla y "PANTALLA TFT 2.4" (J3)", con "1" junto al pin 1 de J3;
   - los créditos del Game*Mite a la derecha.
7. **Serigrafía inferior.** En la vista desde arriba se ve espejada, que es lo correcto; al dar vuelta la placa en el visor se lee al derecho:
   - "VISTA POSTERIOR / FILAS ESPEJADAS", el contorno de la RP2350-Plus con el USB-C arriba y "1" en J1 y J2;
   - el contorno del DAC con "JACK" junto al borde inferior, y "VIN" y "GND" en J5;
   - "OFF" y "ON" en SW10 (desde atrás, OFF a la izquierda);
   - "BATERÍA 103450".
8. Ningún texto de serigrafía cae sobre un pad (el DRC dio 0 avisos, pero confirmarlo a la vista).
9. En la serigrafía inferior aparece **"JLCJLCJLCJLC"** en vertical, dentro de la zona de batería, junto a "BATERÍA 103450". Ahí JLCPCB pone su número de pedido (con "Specify a location").
10. Precio y plazo coherentes con 5 placas de 150 × 65 mm, sin ensamblaje ni opciones extra marcadas por error.

## Verificación del diseño (21-oct-2026)

`verificar.py`: ERC 0/0 · DRC 0 errores, 0 avisos · 0 sin conectar · paridad esquemático-PCB 0 · mínimos DFM OK.
`verificar_extra.py`:
- ERC y DRC con los tests que el proyecto ignora activados: 0.
- Emulación de "Actualizar PCB desde esquemático" (F8): 0 cambios.

Detalle en `DECISIONES.md`.

Licencia y créditos: basado en el Game★Mite de Thomas Hugo Williams (CC BY 4.0).
