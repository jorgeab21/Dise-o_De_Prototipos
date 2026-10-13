# DECISIONES.md — KIDBOX

Registro de fuentes consultadas, datos obtenidos de ellas y supuestos del agente que no están en `ESPECIFICACION.md`.
Formato de cada supuesto: fecha · qué se supuso · por qué · qué pasa si está mal.

---

## 1. Hojas de datos consultadas (autorizadas en la sección 0 de la especificación, v0.5)

Descargadas el 13-oct-2026 en `datasheets/`. No se descargaron huellas, modelos 3D ni software.

| Archivo en `datasheets/` | Qué es | URL de origen |
| :--- | :--- | :--- |
| `RP2350_Plus_esquematico.pdf` | Esquemático oficial de la Waveshare RP2350-Plus | https://files.waveshare.com/wiki/RP2350-Plus/RP2350_Plus.pdf |
| `RP2350_Plus_pinout_waveshare.jpg` | Pinout oficial (vista posterior del módulo) | https://www.waveshare.com/w/upload/3/3c/680px-RP2350-Plus-details-inter.jpg (página: https://www.waveshare.com/wiki/File:680px-RP2350-Plus-details-inter.jpg) |
| `RP2350_Plus_dimensiones_waveshare.jpg` | Plano de dimensiones oficial (vista frontal del módulo) | https://www.waveshare.com/w/upload/2/22/800px-RP2350-Plus-details-size.jpg (página: https://www.waveshare.com/wiki/File:800px-RP2350-Plus-details-size.jpg) |
| `MSP2402_esquematico_lcdwiki.pdf` | Esquemático del módulo TFT 2.4" SPI MSP2402 | https://www.lcdwiki.com/res/MSP2402/MSP2402-2.4-SPI.pdf |
| `MSP2402_dimensiones_lcdwiki.pdf` | Plano mecánico (rotulado "MSP2401", misma PCB) | https://www.lcdwiki.com/res/MSP2402/MSP2401_Size.pdf |
| `MSP2402_manual_lcdwiki.pdf` | Manual de usuario del MSP2402 | https://www.lcdwiki.com/res/MSP2402/2.4inch_SPI_Module_MSP2402_User_Manual_EN.pdf |

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
