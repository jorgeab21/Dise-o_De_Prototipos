# KIDBOX

**Consola portátil para niños de 6 a 10 años, sin internet, con juegos que ejercitan la atención y la tolerancia a la frustración, y con un límite de sesión incorporado.**

Proyecto semestral del curso **IND474 · Diseño y Prototipo para el Desarrollo de Productos Físicos** · Universidad Adolfo Ibáñez, Facultad de Ingeniería y Ciencias · 2026, segundo semestre · Profesor: Sebastián Duarte.

> **Estado (13-oct-2026):** propuesta entregada (Semana 8). Para la Semana 10 están listos los documentos de diseño y el esquemático de la PCB (ERC sin errores); en curso, el layout de la PCB y el prototipo en protoboard.

---

## Carta de presentación

Somos un equipo de cuatro estudiantes de Ingeniería Civil Industrial de la UAI. Este repositorio reúne el trabajo de nuestro proyecto semestral: el diseño y prototipo de **KIDBOX**, un producto físico que nace de una pregunta simple: ¿qué le pueden pasar los padres a su hijo cuando hoy le pasan el celular o la tablet?

Partimos del problema y no de la tecnología. Revisamos estudios sobre el uso de pantallas en la infancia, sobre por qué los padres las entregan y sobre qué tipo de juegos pueden aportar al desarrollo cognitivo. De ahí salió un concepto: una consola cerrada, sin internet ni tienda de aplicaciones, con pocos juegos elegidos por su objetivo y con un límite de tiempo que pone la propia consola, no el adulto.

A lo largo del semestre vamos a llevar ese concepto a un prototipo funcional que integra electrónica (PCB propia), programación (firmware y juegos) y diseño mecánico (carcasa impresa en 3D), y lo vamos a probar con niños y padres reales. Aquí documentamos cada etapa: lo que investigamos, lo que decidimos y por qué.

## Equipo

| Integrante | GitHub |
| :-- | :-- |
| Jorge Becerra | [jorgeab21](https://github.com/jorgeab21) |
| Benjamín Fernández | [benjafer38](https://github.com/benjafer38) |
| Adrián Medina | — |
| Daniel Pizarro | [DanielPizarroJ](https://github.com/DanielPizarroJ) |

---

## Problemas identificados

### 1. El problema de las familias

Los padres entregan el celular o la tablet para ocupar o calmar al niño, se sienten culpables al hacerlo y después no pueden limitar su uso sin conflicto.

| Dato | Fuente |
| :-- | :-- |
| El tiempo de juego en niños de 0 a 8 años creció 65 % entre 2020 y 2024. Los de 0 a 8 años pasan 2 h 27 min diarias frente a pantallas. | Common Sense Media, 2025 |
| En Chile, la edad promedio de primer uso es 7,2 años y la del primer celular propio, 9,7 años. | ClaroVTR y Criteria, 2025 |
| El 59,7 % de los cuidadores de niños de 0 a 6 años cree que lo ideal sería que no usaran dispositivos móviles, pero solo el 33,3 % de los niños no los usa en días sin jardín. | Centro UC de la Familia, 2025 |
| El 66 % de los padres usa pantallas para mantener ocupado al niño y el 25 % para calmarlo cuando está enojado. | Common Sense Media, 2025 |
| El 42 % de los padres siente que podría manejar mejor el tiempo de pantalla de sus hijos. | Pew Research Center, 2025 |

La exposición temprana se asocia con retrasos de comunicación y con más rabia y desregulación emocional (Takahashi 2023, Fitzpatrick 2024, Radesky 2022). Son estudios de asociación, no de causalidad. El detalle y las 16 referencias están en [KIDBOX.md](Documentacion/KIDBOX.md).

**Necesidad:** los padres necesitan que sus hijos se entretengan de forma autónoma por periodos cortos, sin contenido inapropiado ni diseños que capturan la atención, y sin tener que ser ellos quienes impongan el límite.

### 2. Usuario y cliente

- **Usuario:** niños y niñas de 6 a 10 años. Es la edad en que empieza el uso habitual de dispositivos y aún no llega el celular propio, y corresponde a la etapa de operaciones concretas de Piaget. El rango se validará en las pruebas con usuarios.
- **Cliente:** madres, padres y cuidadores. Quien compra no es quien usa.

### 3. Desafíos técnicos detectados en la factibilidad

- El parlante disponible en el DEC (CEET120B085) es de 12 V, así que no sirve como parlante definitivo.
- No se puede conectar la batería LiPo directo al microcontrolador: hay que resolver carga y regulación según la placa exacta que se use.
- No hay un D-pad listo en el inventario. Para el prototipo se resuelve con 4 tact switches y una pieza impresa en 3D.
- La PCB de referencia (ESP32-Emu-Turbo) es de 4 capas con componentes SMD, un nivel de complejidad que hay que contrastar con el calendario del curso.

El análisis completo está en [Ideación de Conceptos y factibilidad.pdf](Documentacion/Ideación%20de%20Conceptos%20y%20factibilidad.pdf).

---

## Nuestra propuesta

### Concepto

- **Dispositivo cerrado:** sin WiFi, sin tienda de aplicaciones, sin video ni publicidad.
- **Controles físicos** (cruceta y botones) en lugar de pantalla táctil, para evitar la lógica del scroll.
- **Biblioteca de 3 a 4 juegos**, cada uno con un objetivo: atención sostenida, planificación y memoria de trabajo.
- **Sesiones de 15 a 30 minutos** con aviso previo y cierre automático. La consola pone el límite, no el adulto.
- **Diseño que acompaña la frustración:** deshacer, pistas y dificultad adaptativa, sin cronómetro ni pantalla de game over.
- **Sin mecánicas de retención:** sin rachas, recompensas variables ni reproducción automática.

KIDBOX no se presenta como herramienta para calmar al niño en una crisis, ni como un producto que "mejora la concentración". Se presenta como un producto diseñado a partir de la evidencia, cuyo efecto mediremos en las pruebas con usuarios.

### Diferenciación

No encontramos en el mercado chileno un dispositivo que combine las cuatro características de KIDBOX.

| Producto | Juego | Objetivo cognitivo o emocional | Sin internet abierto | Dispositivo propio |
| :-- | :-: | :-: | :-: | :-: |
| SoyMomo Reloj | No | No | Sí | Sí |
| SoyMomo Tablet Pro 2.0 | Sí, apps de terceros | Parcial | No | Sí |
| PleIQ | Sí | Sí | No | No |
| Tonies / Yoto | No, solo audio | No | Sí | Sí |
| LeapFrog / VTech | Sí | Solo académico | Sí | Sí |
| **KIDBOX** | **Sí** | **Sí** | **Sí** | **Sí** |

### Cómo lo vamos a construir

| Área | Propuesta |
| :-- | :-- |
| Interacción | Táctil (cruceta y botones), visual (pantalla a color) y auditiva (efectos y aviso de fin de sesión). |
| Hardware | Microcontrolador Waveshare RP2350-Plus, pantalla TFT ILI9341 de 2.4", 9 botones, DAC de audio con salida para audífonos, batería con carga USB-C y PCB propia. |
| Software | Firmware con menú, temporizador de sesión y biblioteca de 3 a 4 juegos con dificultad adaptativa. |
| Carcasa | Impresa en 3D, pensada para manos de niños de 6 a 10 años. |

**Base técnica.** Entre dos proyectos open source evaluados elegimos **[ESP32-Emu-Turbo](https://github.com/pjcau/esp32-emu-turbo)** (Concepto A), porque documenta las tres áreas que exige el curso (PCB, firmware y carcasa) y su hardware ya fue validado físicamente. Descartamos **[Cihaz Console](https://github.com/aid-buildandlearn/Cihaz-Console)** (Concepto B) porque usa componentes que no tenemos y tiene la microSD deshabilitada en el firmware. Dada la complejidad de la placa de referencia, estamos evaluando una versión simplificada de la PCB para el prototipo.

**Actualización (13-oct, con el profesor).** Para simplificar la PCB, la base técnica pasó a ser **[Game★Mite](https://github.com/thwill1000/mmbasic-gamemite)** (CC BY 4.0): una placa portadora de módulos, de 2 capas y toda con componentes THT, con una Waveshare RP2350-Plus (que trae cargador de batería), una pantalla ILI9341 de 2.4", un DAC de audio con salida para audífonos (sin parlante) y formato horizontal. El diseño de la PCB está en [`hardware/`](hardware/).

**Fuentes de juegos.** [Simon Tatham's Portable Puzzle Collection](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/) (MIT, puzzles con deshacer y pistas), juegos open source de Game Boy como Tobu Tobu Girl Deluxe, 2048-gb y Petris, y [GCompris](https://gcompris.net/) (KDE, AGPL) como fuente de mecánicas de memoria, lógica y secuencias.

---

## Índice del trabajo

### Entregas

| Semana | Fecha | Entrega | Documentos |
| :-- | :-- | :-- | :-- |
| 8 | 2 oct 2026 | Propuesta del proyecto, ideación y factibilidad (Concepto A vs. B) y BOM preliminar | [KIDBOX.md](Documentacion/KIDBOX.md) · [Documentacion KIDBOX.pdf](Documentacion/Documentacion%20KIDBOX.pdf) · [Ideación de Conceptos y factibilidad.pdf](Documentacion/Ideación%20de%20Conceptos%20y%20factibilidad.pdf) (el BOM preliminar fue reemplazado por la lista de la Semana 10) |
| 10 | 16 oct 2026 | Requisitos, bocetos, BOM, arquitectura HW/SW, PCB/Gerber y plan de desarrollo | [1. Requisitos](1.KIDBOX_Requisitos_y_Requerimientos_Tecnicos.md) · [2. Bocetos](2.KIDBOX_Diagramas_Bocetos_Diseno_Fisico.md) · [3. Componentes](3.KIDBOX_Lista_componentes_electrónicos.md) · [4. Arquitectura](4.KIDBOX_Diagrama_arquitectura_del_Sistema.md) · [5. PCB](hardware/) *(esquemático listo; layout y Gerbers en curso)* · [6. Plan](6.KIDBOX_Plan_de_Desarrollo.md) |
| 12 | 30 oct 2026 | Prototipo en desarrollo | *Pendiente* |
| 13 | 6 nov 2026 | Pruebas con usuarios | *Pendiente* |
| 14 | 13 nov 2026 | Entrega final y presentación | *Pendiente* |

### Documentos del repositorio

| Documento | Contenido |
| :-- | :-- |
| [1.KIDBOX_Requisitos_y_Requerimientos_Tecnicos.md](1.KIDBOX_Requisitos_y_Requerimientos_Tecnicos.md) | Requisitos funcionales, requerimientos técnicos y metas físicas. |
| [2.KIDBOX_Diagramas_Bocetos_Diseno_Fisico.md](2.KIDBOX_Diagramas_Bocetos_Diseno_Fisico.md) | Distribución de controles, boceto de la consola, corte lateral y consideraciones mecánicas. |
| [3.KIDBOX_Lista_componentes_electrónicos.md](3.KIDBOX_Lista_componentes_electrónicos.md) | Lista de componentes del producto (BOM), criterio de batería y estado de cada pieza. |
| [4.KIDBOX_Diagrama_arquitectura_del_Sistema.md](4.KIDBOX_Diagrama_arquitectura_del_Sistema.md) | Arquitectura de hardware y software, asignación de pines y flujo del firmware. |
| [6.KIDBOX_Plan_de_Desarrollo.md](6.KIDBOX_Plan_de_Desarrollo.md) | Cronograma hasta la entrega final y matriz de riesgos. |
| [`hardware/`](hardware/) | Diseño de la PCB: especificación, esquemático KiCad, BOM de la PCB, netlist, layout propuesto y hojas de datos. |
| [Documentacion/KIDBOX.md](Documentacion/KIDBOX.md) | Propuesta completa: problema, usuario, concepto, evidencia, mercado y 16 referencias. |
| [Documentacion/Ideación de Conceptos y factibilidad.pdf](Documentacion/Ideación%20de%20Conceptos%20y%20factibilidad.pdf) | Comparación de los Conceptos A y B, faltantes y justificación de la elección. |
| [Documentacion/Documentacion KIDBOX.pdf](Documentacion/Documentacion%20KIDBOX.pdf) | Propuesta en PDF (entrega Semana 8). |
| [Documentacion/Componentes_DEC_UAI.xlsx](Documentacion/Componentes_DEC_UAI.xlsx) | Inventario de componentes disponibles en el DEC UAI. |
| `Documentacion/01 Problema - Pantallas en niños/` | Uso de pantallas en la infancia (Common Sense Media, Radiografía Digital). |
| `Documentacion/02 Padres - Por qué entregan pantallas/` | Motivos de los padres (Pew, Centro UC de la Familia, estudios cualitativos). |
| `Documentacion/03 Videojuegos y desarrollo cognitivo/` | Evidencia sobre videojuegos y desarrollo (Kollins, Ducharme, Sauce, Siegler, Piaget). |

---

## Evaluación del curso

Tres entregas de avance (25 %, 35 % y 40 % de la nota de entregas) y una presentación final con un prototipo original. La nota final es `NF = NP × 0,7 + PF × 0,3`.

## Nota sobre los documentos

La carpeta `Documentacion/` contiene artículos e informes de terceros usados como respaldo de la propuesta, y pertenecen a sus autores y editoriales. Los datos citados están referenciados en [KIDBOX.md](Documentacion/KIDBOX.md).
