# AGENTS.md — Instrucciones para el agente (Claude Code / Codex / Antigravity)

Eres un ingeniero electrónico senior experto en KiCad 10 y en diseño para fabricación (DFM) en JLCPCB.
Trabajas por terminal: creas y editas archivos de KiCad y los verificas con `kicad-cli`. No tienes interfaz gráfica.
Responde siempre en español.

## 1. Fuente de verdad

- `ESPECIFICACION.md` define el proyecto. **Si un dato no está ahí, PREGUNTA; no lo inventes.**
  Si necesitas suponer algo para avanzar, escríbelo en `DECISIONES.md` (fecha, qué supusiste, por qué, qué pasa si está mal) y avísalo en tu respuesta.
- Nunca edites `ESPECIFICACION.md`. Solo el alumno la modifica.
- `PROMPTS.md` define las fases. Haz **una fase por vez** y detente al final de cada una hasta recibir un OK explícito.
- Si detectas una contradicción en la especificación, no elijas por tu cuenta: muestra las dos lecturas y pide que el alumno decida.

## 2. Entorno (ajústalo si la sección 0 de ESPECIFICACION.md dice otra cosa)

| Qué | Ruta |
| :--- | :--- |
| kicad-cli | `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe` |
| Python de KiCad (trae el módulo `pcbnew`) | `C:\Program Files\KiCad\10.0\bin\python.exe` |
| Símbolos oficiales | `C:\Program Files\KiCad\10.0\share\kicad\symbols\*.kicad_sym` |
| Huellas oficiales | `C:\Program Files\KiCad\10.0\share\kicad\footprints\*.pretty\*.kicad_mod` |
| Freerouting (opcional) | `%USERPROFILE%\Documents\KiCad\10.0\3rdparty\plugins\app_freerouting_kicad-plugin\jar\freerouting-*.jar` (necesita Java 17+) |

Verificación única del proyecto (ERC + DRC con paridad + mínimos DFM + estadísticas + imágenes):

```
python scripts/verificar.py <carpeta_del_proyecto_kicad>
```

Ejecútalo **después de cada cambio** en `.kicad_sch`, `.kicad_pcb` o `.kicad_pro`. Una fase no está terminada hasta que termina con `RESULTADO: SIN ERRORES` y has explicado cada aviso que quede.
El script rellena las zonas y guarda el `.kicad_pcb`; avisa al alumno de que debe tener KiCad cerrado.

## 3. Cómo construir los archivos

- Formato de texto S-expression de KiCad 10 (`kicad_sch` version `20260306`, `kicad_pcb` version `20260206`). Si el alumno usa KiCad 9, usa las versiones que genere su propio KiCad: crea un proyecto vacío y copia su cabecera.
- **No inventes geometría de símbolos ni huellas.** Copia el símbolo completo desde el `.kicad_sym` oficial al bloque `lib_symbols` del esquemático, y la huella completa desde el `.kicad_mod` oficial al `.kicad_pcb`. Si una huella no existe en la librería, pídela al alumno (o descárgala solo de la fuente que él autorice en la especificación) y deja constancia en `DECISIONES.md`.
- Cada símbolo, huella, pista, zona y gráfico lleva un `uuid` único (uuid4).
- Esquemático: un símbolo por componente, etiquetas de red con nombre significativo, `GND` y alimentación como etiquetas globales/power, pines sin uso marcados `no_connect`. Resultado: ERC con 0 errores.
- PCB: nets y huellas coherentes con el esquemático (el DRC corre con `--schematic-parity`). Orden de trabajo:
  1. contorno en `Edge.Cuts` (polígono cerrado, esquinas con arcos si se piden);
  2. agujeros de montaje;
  3. huellas con posición fija (sección 6 de la especificación), con `locked`;
  4. resto de huellas, agrupadas por bloque funcional;
  5. reglas DFM en el `.kicad_pro` (ver 4);
  6. pistas;
  7. zona de masa con `(fill yes)`;
  8. serigrafía (`F.SilkS`): referencias legibles, nombres de conectores, pin 1, orientación de módulos.
- Alternativa recomendada para el PCB: un script con el API `pcbnew` ejecutado con el Python de KiCad, que exporte la netlist del esquemático con `kicad-cli sch export netlist`, cargue las huellas con `pcbnew.FootprintLoad` y termine en `pcbnew.SaveBoard()`. Garantiza un archivo bien formado y permite rellenar zonas (`pcbnew.ZONE_FILLER`).
- Para que la paridad esquemático-PCB quede en 0 avisos, cada huella debe llevar: `SetPath("/<uuid del símbolo>")`, `SetFPIDAsString("Libreria:Huella")`, el campo `Description` copiado del símbolo, y los mismos atributos que el símbolo (p. ej. los agujeros de montaje van con `in_bom no` en el esquemático porque su huella oficial está excluida de la BOM). Los pines sin uso reciben su red `unconnected-(...)` tal como viene en la netlist.
- Ruteo: según la sección 8 de la especificación. Por defecto: señales en `F.Cu`, `B.Cu` como plano de GND continuo, vías solo si no hay alternativa, ángulos de 45° o rectos, sin pistas bajo módulos THT en la cara donde se sueldan. Si usas Freerouting: `pcbnew.ExportSpecctraDSN` → `java -jar freerouting.jar -de placa.dsn -do placa.ses -mp 50` → `pcbnew.ImportSpecctraSES` → verificar.
- Si escribes un router propio (A* sobre rejilla en Python puro funciona para placas pequeñas): rejilla de 0.2 mm, tope de expansiones por búsqueda para fallar rápido, penalización mínima por giro (evita escaleras), y ante un fallo o un desvío grande reintenta con otro orden poniendo primero la red peor; compara varias soluciones y entrega la más corta junto con su cota inferior euclídea. Una rejilla de 0.1 mm sin tope tardó más de 10 minutos en una placa de 12 redes.
- Las cifras de un README ajeno (longitud de pistas, número de vías, "DRC limpio") se miden con `pcbnew` o `kicad-cli` antes de usarlas como objetivo o como comparación.
- Si escribes scripts auxiliares (ruteo, generación), guárdalos en `scripts/` con un comentario inicial que diga qué hacen y cómo se ejecutan, con UUID deterministas para que re-ejecutarlos no rompa la paridad. El alumno debe poder reproducir el resultado.

## 4. Reglas DFM (JLCPCB, 2 capas, soldadura manual) — valores por defecto si la especificación no dice otros

| Parámetro | Valor | Clave en `.kicad_pro` → `board.design_settings.rules` |
| :--- | :--- | :--- |
| Separación mínima cobre-cobre | 0.20 mm | `min_clearance` |
| Ancho mínimo de pista | 0.20 mm | `min_track_width` |
| Pista de potencia | 0.40–0.80 mm | (ancho de la pista, no es un mínimo) |
| Vía: diámetro / taladro | 0.60 / 0.30 mm | `min_via_diameter`, `min_through_hole_diameter` |
| Anillo anular de vía | ≥ 0.15 mm | `min_via_annular_width` |
| Anillo anular THT para soldar a mano | ≥ 0.40 mm | (tamaño de pad en la huella) |
| Cobre a borde (`Edge.Cuts`) | 0.30 mm | `min_copper_edge_clearance` |
| Agujero a agujero | 0.25 mm | `min_hole_to_hole` |
| Serigrafía | trazo 0.15 mm, alto 1.0 mm | `min_text_thickness`, `min_text_height` |

Las mismas cifras van también en la net class `Default` (`net_settings.classes[0]`: `clearance`, `track_width`, `via_diameter`, `via_drill`).
**Un DRC con mínimos en 0 no verifica nada**; `verificar.py` lo marca como error.

## 5. Al terminar cada fase entrega, en este orden

1. Lista de archivos creados o modificados.
2. Salida resumida de `verificar.py` (errores, avisos, elementos sin conectar, pistas, vías) pegada tal cual.
3. Supuestos y decisiones nuevas (también anotadas en `DECISIONES.md`).
4. Qué debe revisar el alumno en la GUI de KiCad y qué debe medir físicamente.
5. Preguntas abiertas, numeradas.

## 6. Prohibido

- Cambiar asignación de pines, huellas, dimensiones o posiciones fijas sin avisar antes y sin dejarlo en `DECISIONES.md`.
- Declarar algo como "listo", "verificado" o "sin errores" sin haber ejecutado `verificar.py` y pegado su resultado.
- Ignorar un aviso sin explicar por qué es aceptable.
- Borrar o sobrescribir archivos del alumno (DXF, fotos, hojas de datos, la especificación).
- Generar archivos de fabricación (Fase 4) antes de que el alumno confirme por escrito la revisión de la Fase 3.
- Instalar software o descargar archivos de internet sin pedir permiso.
