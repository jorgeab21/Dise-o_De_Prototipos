# KIDBOX

**Propuesta de proyecto · IND474 Diseño y Prototipo para el Desarrollo de Productos Físicos · Entrega Semana 8, 2 de octubre de 2026**

## Resumen

KIDBOX es una consola portátil para niños de 6 a 10 años que reemplaza el celular o la tablet de los padres por un dispositivo cerrado, sin internet, con una biblioteca acotada de juegos diseñados para ejercitar la atención, la planificación y la tolerancia a la frustración. La sesión de juego tiene un límite incorporado, de modo que es la consola, y no el adulto, la que avisa y cierra el tiempo de uso.

Elegimos la categoría videojuego porque el problema que abordamos ocurre justamente en el juego digital: los niños usan pantallas desde muy temprano, los padres las entregan para resolver necesidades reales y se sienten culpables al hacerlo, y existe evidencia de que juegos con mecánicas bien diseñadas pueden apoyar el desarrollo cognitivo. Como base técnica usaremos el proyecto open source ESP32-Emu-Turbo, que ya documenta hardware, firmware y carcasa.

## Categoría seleccionada y justificación

Categoría: videojuego.

Las razones para elegir videojuego por sobre instrumento musical digital son las siguientes:

- El problema identificado está en el uso de pantallas y juegos digitales. El tiempo de juego en niños de 0 a 8 años creció 65 % entre 2020 y 2024 (Common Sense Media, 2025), y casi la mitad de los niños chilenos de 8 a 17 años juega en línea todos o casi todos los días (Radiografía Digital, 2025).
- Hay evidencia de que un juego puede apoyar el desarrollo cognitivo cuando su mecánica está diseñada para un objetivo concreto (ver sección Concepto).
- Existe un proyecto open source maduro que cubre las tres áreas que exige el curso (PCB, firmware y carcasa), y el inventario del DEC UAI ya tiene varios componentes compatibles para prototipar: ESP32, amplificador PAM8403, lector microSD, cargador TP4056, joystick y botones.

## Problema

### Los niños usan pantallas desde muy temprano

- A los 2 años, el 40 % de los niños tiene su propia tablet, y a los 4 años el 58 %. Los niños de 0 a 8 años pasan en promedio 2 h 27 min diarias frente a pantallas, y los de 5 a 8 años 3 h 28 min (Common Sense Media, 2025).
- En Chile, el 55 % de los niños y adolescentes usó un aparato electrónico antes de los 7 años. La edad promedio de primer uso es 7,2 años y la del primer celular propio, 9,7 años. El 90 % cree que lo adecuado es estar conectado menos de 4 horas al día, pero el 38 % supera ese límite entre semana y el 52 % el fin de semana (ClaroVTR y Criteria, 2025).
- En niños chilenos de 0 a 6 años, el 59,7 % de los cuidadores cree que lo ideal sería que no usaran dispositivos móviles. Sin embargo, solo el 41,3 % de los niños no los usa en días de jardín y el 33,3 % en días sin jardín (Centro UC de la Familia, 2025).

### La exposición se asocia con problemas de desarrollo y de regulación emocional

- En 7.097 niños japoneses, más tiempo de pantalla al año de edad se asoció con retrasos en comunicación y resolución de problemas a los 2 y 4 años (Takahashi et al., 2023).
- El uso de tablet a los 3,5 años predijo más expresiones de rabia y frustración a los 4,5 años, y esos niños luego usaron más la tablet, en un ciclo que perjudica la regulación emocional (Fitzpatrick et al., 2024).
- Usar el celular para calmar a niños de 3 a 5 años se asoció con mayor desregulación emocional, porque desplaza la práctica de otras formas de calmarse (Radesky et al., 2022).

Estos estudios muestran asociación, no causalidad, pero apuntan en la misma dirección que las recomendaciones de la OMS (2019): no más de una hora diaria de pantalla entre los 2 y los 4 años.

## Perfil de usuario y necesidad identificada

### Usuario: niños y niñas de 6 a 10 años

Es la edad en que comienza el uso habitual de dispositivos (7,2 años en promedio en Chile) y en que todavía no llega el celular propio (9,7 años). Según Piaget, entre los 7 y los 11 años los niños están en la etapa de operaciones concretas: pueden seguir reglas, ordenar secuencias y razonar con lógica sobre objetos, que es lo que exigen los juegos de atención y planificación. El rango se validará en las pruebas con usuarios.

### Cliente: madres, padres y cuidadores

Quien compra KIDBOX no es quien lo usa. Los padres entregan el celular o la tablet porque les resuelve problemas concretos:

- El 66 % usa pantallas para mantener ocupado al niño mientras hace otras cosas o se toma un tiempo para sí, el 44 % para mantenerlo ocupado en lugares públicos y el 25 % para calmarlo cuando está enojado (Common Sense Media, 2025).
- Entre los padres cuyo hijo usa smartphone, el 85 % lo permite para entretenerlo y el 43 % para calmarlo; en niños menores de 5 años, ese último porcentaje sube a 65 % (Pew Research Center, 2025).
- A mayor estrés parental, más tiempo de pantalla del niño: los autores describen la pantalla como un chupete moderno (Brauchli et al., 2024).
- En entrevistas, los padres describen la tablet como una niñera conveniente, se sienten juzgados si la usan y también si no la usan, y algunos fingen que se acabó la batería para poder quitarla sin conflicto (Mallawaarachchi et al., 2022).

Al mismo tiempo, el 42 % de los padres siente que podría manejar mejor el tiempo de pantalla de sus hijos (Pew Research Center, 2025). Entre quienes no le dan smartphone a su hijo, las razones principales son el contenido inapropiado (88 %), la seguridad (84 %), el daño al desarrollo (84 %) y el exceso de tiempo de pantalla (82 %).

### Necesidad identificada

Los padres necesitan una forma de que sus hijos se entretengan de manera autónoma por periodos cortos, sin contenido inapropiado ni diseños que capturan la atención, y sin tener que ser ellos quienes impongan el límite. KIDBOX responde a las cuatro razones por las que hoy los padres evitan el smartphone: no tiene internet ni tienda de aplicaciones, sus juegos están elegidos por su aporte al desarrollo y el tiempo de uso está acotado por diseño.

### Proceso de diseño aplicado

Siguiendo el diagrama del curso, el problema se descompone así:

| **Etapa del diagrama** | **KIDBOX** |
| :-- | :-- |
| Dolor | Los padres recurren a la tablet o al celular para ocupar o calmar al niño, y después no pueden limitar su uso sin conflicto. |
| Usuario | Niños y niñas de 6 a 10 años (usuario) y sus madres, padres o cuidadores (cliente). |
| Beneficio | El niño juega de forma autónoma con juegos que ejercitan atención, planificación y tolerancia a la frustración. El adulto recupera el control del tiempo y del contenido. |
| Interacción | Física y táctil: cruceta y botones. Visual: pantalla a color. Auditiva: parlante con efectos de juego y aviso de fin de sesión. |
| Hardware | Microcontrolador ESP32-S3, pantalla TFT, botones, amplificador y parlante, microSD, batería con carga por USB-C y PCB propia. |
| Software | Firmware con menú, temporizador de sesión y una biblioteca de 3 a 4 juegos con dificultad adaptativa. |

## Concepto seleccionado

KIDBOX es una consola portátil con controles físicos y pantalla a color, pensada para cumplir la misma función que hoy cumple la tablet para los padres, sin sus costos. Sus características principales son:

- Dispositivo cerrado: sin WiFi, sin tienda de aplicaciones, sin video ni publicidad.
- Controles físicos (cruceta y botones) en lugar de pantalla táctil, para evitar la lógica del scroll.
- Biblioteca acotada de 3 a 4 juegos, cada uno asociado a un objetivo: atención sostenida, planificación y memoria de trabajo.
- Sesiones de 15 a 30 minutos con aviso previo y cierre automático.
- Diseño que acompaña la frustración: deshacer, pistas, dificultad que se adapta al desempeño, sin cronómetro ni pantalla de game over.
- Sin mecánicas que buscan retener al usuario, como rachas, recompensas variables o reproducción automática, siguiendo la recomendación del Centro UC de la Familia (2026).

KIDBOX no se usa ni se promociona como herramienta para calmar al niño en una crisis, porque la evidencia indica que eso empeora la autorregulación. Los juegos pueden en cambio practicar estrategias de calma fuera de esos momentos.

### Evidencia que respalda el concepto

- En un ensayo aleatorizado con 348 niños de 8 a 12 años con TDAH, un videojuego diseñado para la atención, jugado 25 minutos al día durante 4 semanas, mejoró el índice de atención (TOVA API) más que un juego educativo de control (cambio medio 0,93 frente a 0,03; p = 0,006). El efecto adverso más frecuente fue la frustración, en el 3 % de los niños (Kollins et al., 2020). Es la base de EndeavorRx, autorizado por la FDA en 2020.
- Cuatro sesiones de 15 minutos de un juego de tablero con números eliminaron la brecha en conocimiento numérico entre preescolares de bajos y medianos ingresos. El mismo juego con colores no tuvo efecto: el beneficio viene de la mecánica específica (Siegler y Ramani, 2008).
- En jóvenes de 10 a 17 años con problemas de control de la rabia, un juego que solo se puede ganar manteniendo bajo el pulso redujo la agresión y el oposicionismo más que un juego simulado (Ducharme et al., 2021).
- En 9.855 niños de 9 a 10 años, más tiempo de videojuegos se asoció con un aumento de 2,55 puntos de CI en dos años, controlando por genética y nivel socioeconómico (Sauce et al., 2022).

Los programas de entrenamiento cerebral mejoran la tarea entrenada, pero hay poca evidencia de que esa mejora se traspase a otras tareas (Simons et al., 2016), y Lumosity debió pagar US$2 millones a la FTC en 2016 por afirmar lo contrario sin respaldo. Por eso KIDBOX se presenta como un producto diseñado a partir de la evidencia, no como uno que mejora la concentración, y medirá su efecto en las pruebas con usuarios.

### Mercado y diferenciación

Hay empresas que ya venden productos para niños con menos pantalla. Tonies, que vende un parlante para niños sin pantalla, facturó 630 millones de euros en 2025, un 31 % más que el año anterior. En Chile, SoyMomo vende relojes y tablets para niños con control parental, y en 2021 tenía ventas cercanas a US$6 millones al año y una valorización de US$40 millones. No encontramos en el mercado chileno un dispositivo que combine las cuatro características de KIDBOX:

| **Producto** | **Juego** | **Objetivo cognitivo o emocional** | **Sin internet abierto** | **Dispositivo propio** |
| :-- | :-: | :-: | :-: | :-: |
| SoyMomo Reloj | No | No | Sí | Sí |
| SoyMomo Tablet Pro 2.0 | Sí, apps de terceros | Parcial | No | Sí |
| PleIQ | Sí | Sí | No | No, usa celular o tablet |
| Tonies / Yoto | No, solo audio | No | Sí | Sí |
| LeapFrog / VTech | Sí | Solo académico | Sí | Sí |
| **KIDBOX** | **Sí** | **Sí** | **Sí** | **Sí** |

### Bocetos preliminares

\[Insertar aquí los bocetos del equipo: vista frontal con disposición de botones y pantalla, vista lateral y una propuesta de agarre para manos de niños de 6 a 10 años.\]

## Referencias open source

- **ESP32-Emu-Turbo** ([github.com/pjcau/esp32-emu-turbo](https://github.com/pjcau/esp32-emu-turbo)): base de hardware, firmware y carcasa. Usa ESP32-S3, pantalla ILI9488 de 3,95 pulgadas, amplificador PAM8403, microSD, USB-C, batería LiPo y 12 botones, con una PCB de 4 capas de 160 × 75 mm ya validada físicamente. Corre el emulador Retro-Go, que carga juegos desde la microSD. Su complejidad se evaluará frente al calendario del curso, y una versión simplificada de la PCB es una alternativa.
- **Simon Tatham's Portable Puzzle Collection** (licencia MIT): 41 puzzles de lógica escritos en C, con deshacer y pistas. Nueve de ellos son aptos para niños, como Same Game, Fifteen e Inertia.
- **Juegos open source de Game Boy que corren en Retro-Go**, como Tobu Tobu Girl Deluxe (código MIT, gráficos y música CC-BY 4.0), 2048-gb y Petris.
- **GCompris** (KDE, licencia AGPL): más de 100 actividades educativas para niños de 2 a 10 años, como fuente de mecánicas de memoria, lógica y secuencias ya usadas en colegios.
- **Cihaz Console** ([github.com/aid-buildandlearn/Cihaz-Console](https://github.com/aid-buildandlearn/Cihaz-Console)): alternativa evaluada y descartada por usar componentes que no tenemos y tener la microSD deshabilitada en el firmware actual.

## Referencias

1. Brauchli, V., Sticca, F., Edelsbrunner, P., von Wyl, A. y Lannen, P. (2024). Are screen media the new pacifiers? The role of parenting stress and parental attitudes for children's screen time in early childhood. *Computers in Human Behavior, 152*, 108057.
2. Centro UC de la Familia y Escuela de Trabajo Social UC (2025). Resultados de la encuesta Uso de dispositivos móviles en la primera infancia en Chile. Pontificia Universidad Católica de Chile.
3. Centro UC de la Familia (2026). Recomendaciones para el bienestar digital en la primera infancia. Pontificia Universidad Católica de Chile.
4. ClaroVTR y Criteria (2025). Radiografía Digital Niños, Niñas y Adolescentes 2025.
5. Common Sense Media (2025). *The Common Sense Census: Media Use by Kids Zero to Eight.*
6. Ducharme, P., Kahn, J., Vaudreuil, C. et al. (2021). A proof of concept randomized controlled trial of a video game requiring emotional regulation to augment anger control training. *Frontiers in Psychiatry, 12*, 591906.
7. Fitzpatrick, C. et al. (2024). Early-childhood tablet use and outbursts of anger. *JAMA Pediatrics*. doi:10.1001/jamapediatrics.2024.2511
8. Kollins, S. H., DeLoss, D. J., Cañadas, E. et al. (2020). A novel digital intervention for actively reducing severity of paediatric ADHD (STARS-ADHD): a randomised controlled trial. *The Lancet Digital Health, 2*, e168–e178.
9. Mallawaarachchi, S. R., Hooley, M., Sutherland-Smith, W. y Horwood, S. (2022). You're damned if you do, you're damned if you don't: a qualitative exploration of parent motives for provision of mobile screen devices in early childhood. *BMC Public Health, 22*, 2011.
10. Organización Mundial de la Salud (2019). *Guidelines on physical activity, sedentary behaviour and sleep for children under 5 years of age.*
11. Pew Research Center (2025). *How Parents Manage Screen Time for Kids.*
12. Radesky, J. S. et al. (2022). Longitudinal associations between use of mobile devices for calming and emotional reactivity and executive functioning in children aged 3 to 5 years. *JAMA Pediatrics*.
13. Sauce, B., Liebherr, M., Judd, N. y Klingberg, T. (2022). The impact of digital media on children's intelligence while controlling for genetic differences in cognition and socioeconomic background. *Scientific Reports, 12*, 7720.
14. Siegler, R. S. y Ramani, G. B. (2008). Playing linear numerical board games promotes low-income children's numerical development. *Developmental Science, 11*(5), 655–661.
15. Simons, D. J., Boot, W. R., Charness, N. et al. (2016). Do brain-training programs work? *Psychological Science in the Public Interest, 17*(3), 103–186.
16. Takahashi, I. et al. (2023). Screen time at age 1 year and communication and problem-solving developmental delay at 2 and 4 years. *JAMA Pediatrics*.
