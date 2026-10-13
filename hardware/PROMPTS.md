# PROMPTS.md — Un prompt por fase

Copia el prompt de la fase en la que estás, reemplaza lo que va entre `[corchetes]` y pégalo en el agente.
**No pases a la siguiente fase hasta haber revisado la anterior tú mismo.** Entre fases, si el agente ya acumuló mucha
conversación, es buena práctica empezar una sesión nueva: los archivos del proyecto (`AGENTS.md`, `ESPECIFICACION.md`,
`DECISIONES.md`) contienen todo el contexto necesario.

---

## Fase 0 — Entorno y revisión de la especificación (no se crea ningún archivo de KiCad)

```
Lee AGENTS.md, ESPECIFICACION.md y todos los archivos de esta carpeta (incluidos DXF, CSV y hojas de datos si las hay).

1. Verifica el entorno y pega la salida de cada comando:
   - kicad-cli version
   - el Python de KiCad ejecuta: python -c "import pcbnew; print(pcbnew.GetBuildVersion())"
   - python scripts/verificar.py --help (basta con que arranque)
2. Revisa la especificación y entrega tres listas numeradas:
   a) Datos que FALTAN y sin los cuales no puedes diseñar sin inventar (pinout no verificado, huellas no identificadas, posiciones sin coordenadas, etc.).
   b) Contradicciones o ambigüedades (cita el texto de las dos partes que chocan).
   c) Riesgos de fabricación o de montaje (DFM) que ves y qué propones.
3. Propón un diagrama de bloques en texto y una tabla preliminar de componentes con su huella KiCad candidata (nombre exacto de librería:huella) y si existe o no en la librería oficial.

No crees archivos de KiCad todavía. Termina con las preguntas que necesitas que yo responda, numeradas.
```

Responde a sus preguntas **editando `ESPECIFICACION.md`** (no solo en el chat) y pídele que la vuelva a leer. Repite hasta que la lista (a) quede vacía.

---

## Fase 1 — Esquemático

```
La especificación ya está completa y aprobada. Crea el proyecto KiCad en la carpeta [NOMBRE_PROYECTO]/ con el nombre [NOMBRE_PROYECTO]:

1. [NOMBRE_PROYECTO].kicad_pro, .kicad_sch (y .kicad_pcb vacío solo con el contorno, para que verificar.py pueda correr).
2. Esquemático completo según las secciones 2 a 5 de ESPECIFICACION.md: símbolos copiados de las librerías oficiales, etiquetas de red con nombre, GND y alimentación globales, pines sin uso marcados como no conectados, huella asignada a cada símbolo (campo Footprint).
3. Ejecuta python scripts/verificar.py [NOMBRE_PROYECTO] hasta que el ERC tenga 0 errores. Explica cada aviso que quede.
4. Genera BOM.csv (Referencia, Cantidad, Valor, Descripción, Huella KiCad, THT/SMD, Cara, Notas) y netlist.csv (Red, Componente, Pin, Función).
5. Crea DECISIONES.md con todo lo que hayas decidido que no estaba en la especificación.

Entrega el resumen de la sección 5 de AGENTS.md. Yo abriré el esquemático en KiCad para revisarlo antes de la Fase 2.
```

---

## Fase 2 — PCB (colocación, reglas, ruteo, plano de masa, serigrafía)

```
El esquemático está revisado y aprobado [con estos cambios: ...]. Construye el PCB en [NOMBRE_PROYECTO].kicad_pcb siguiendo el orden de la sección 3 de AGENTS.md:

1. Contorno y agujeros según la sección 6 de ESPECIFICACION.md [o: importa el contorno del DXF adjunto a Edge.Cuts y las marcas mecánicas a User.Drawings].
2. Huellas con posición fija en las coordenadas indicadas, bloqueadas. Resto de huellas agrupadas por bloque, con separación razonable para soldar a mano.
3. Reglas DFM de la sección 7 de la especificación escritas en el .kicad_pro (mínimos y net class Default). verificar.py debe mostrarlas todas como OK.
4. Ruteo según la sección 8 de la especificación. Guarda en scripts/ cualquier script que uses para rutear, con instrucciones para reproducirlo.
5. Zona de GND en B.Cu rellena, conectada a todos los pads de GND.
6. Serigrafía: referencias, nombres de conectores, pin 1 y orientación de módulos, textos de la sección 9.
7. python scripts/verificar.py [NOMBRE_PROYECTO] con 0 errores, 0 elementos sin conectar y 0 errores de paridad.

Entrega el resumen de la sección 5 de AGENTS.md e indica dónde están verificacion/F_Cu.svg, B_Cu.svg, 3d_top.png y 3d_bottom.png. Yo revisaré el PCB en KiCad y mediré los componentes reales antes de la Fase 3.
```

Si el agente se queda atascado ruteando (más de dos intentos sin DRC limpio), pídele que **reduzca el problema**: mover componentes no fijos, cambiar pines libres del microcontrolador (avisando), o usar Freerouting solo en `F.Cu`.

---

## Fase 3 — Correcciones tras tu revisión en KiCad y medición física

```
Revisé el PCB en KiCad y medí los componentes reales. Corrige SOLO lo siguiente, sin tocar nada más, y vuelve a ejecutar verificar.py:

1. [ej.: la separación real entre filas del módulo es 15.30 mm, no 15.24; corrige J1/J2]
2. [ej.: el conector USB queda a 1 mm del borde, necesita 2 mm libres para la carcasa]
3. [ej.: la referencia SW3 queda debajo del pulsador, muévela a la serigrafía visible]

Cuando termine con 0 errores, confirma qué cambió (archivos y coordenadas) y actualiza DECISIONES.md.
```

Repite la Fase 3 las veces que haga falta. **No sigas a la Fase 4 hasta que tú, no el agente, hayas dado el visto bueno.**

---

## Fase 4 — Archivos de fabricación y documentación

```
Doy por aprobado el PCB tras mi revisión. Genera el paquete de fabricación para [JLCPCB, 2 capas] en la carpeta fabricacion/:

1. Gerbers con kicad-cli (F.Cu, B.Cu, F.Mask, B.Mask, F.SilkS, B.SilkS, Edge.Cuts [y F.Paste si hay SMD]) y taladros Excellon (origen absoluto, PTH y NPTH en archivos separados, mapa PDF).
2. Comprime todo en fabricacion/[NOMBRE_PROYECTO]_gerbers.zip y lista su contenido con tamaños.
3. [Si hay ensamblaje SMT: BOM y CPL en formato JLCPCB con kicad-cli sch export bom y pcb export pos --format csv --units mm --side front.]
4. Interactive HTML BOM si está instalado (o indícame cómo generarlo desde la GUI).
5. Escribe README.md del proyecto: qué es la placa, cómo se montan los componentes (orden de soldadura), tabla de parámetros de pedido en JLCPCB (capas, espesor, acabado, color, ensamblaje sí/no) y la lista de verificaciones que yo debo hacer en el visor de Gerbers de JLCPCB antes de pagar.

No modifiques el .kicad_pcb en esta fase. Si al generar detectas algo que requiere cambiarlo, detente y avísame.
```
