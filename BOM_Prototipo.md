# Bill of Materials (BOM) — KIDBOX V1

| # | Componente | Cant. | Especificación / función | Estado |
|---|---|---:|---|---|
| 1 | **Raspberry Pi Pico RP2040** | 1 | Microcontrolador principal | ✅ DEC |
| 2 | **TFT Touch 2.4" ILI9341** | 1 | 240×320, SPI, XPT2046 integrado | 🛒 Comprar |
| 3 | **PCM5102A GY-PCM5102** | 1 | DAC I2S para salida de audio | ✅ DEC |
| 4 | **Jack 3.5 mm** | 1 | Salida de audio | ✅ Integrado en módulo PCM5102A |
| 5 | **Audífonos** | 1 | Para probar audio | ✅ / conseguir |
| 6 | **LiPo Soshine 902030** | 1 | 3.7 V, 500 mAh | ✅ DEC |
| 7 | **TP4056** | 1 | Cargador para batería LiPo 1S | ✅ DEC |
| 8 | **Resistencia RPROG TP4056** | 1 | Ajustar carga aprox. a 200–250 mA | 🟡 Revisar disponibilidad |
| 9 | **Interruptor ON/OFF** | 1 | Encendido general de la consola | 🟡 Revisar / comprar |
| 10 | **Tact switches 6×6 mm** | 8 | ↑ ↓ ← →, A, B, Start, Select | ✅ DEC |
| 11 | **Headers macho 2.54 mm** | varios | Pines para módulos | ✅ DEC |
| 12 | **Headers hembra 2.54 mm** | varios | Pico y módulos desmontables | ✅ DEC |
| 13 | **Conector JST 2 pines** | 1 | Conexión batería–PCB | 🟡 Según conector batería |
| 14 | **Capacitores 100 nF** | 2–3 | Desacoplo de alimentación | 🟡 DEC / comprar |
| 15 | **Capacitor 10–47 µF** | 1–2 | Estabilización de alimentación | 🟡 DEC / comprar |
| 16 | **PCB KIDBOX 2 capas** | 1 | Carrier board propia | 🔴 Fabricar |
| 17 | **Carcasa impresa 3D** | 1 | Enclosure KIDBOX | 🔴 Diseñar/imprimir |
| 18 | **Insertos roscados M2/M2.5** | 4–6 | Fijación de carcasa/PCB | ✅ DEC |
| 19 | **Tornillos M2/M2.5** | 4–6 | Ensamble | 🟡 Revisar/DEC |
| 20 | **Cable USB para Pico** | 1 | Programación y pruebas | ✅ Disponible |

## Controles

Los 8 botones quedarían:

| Función | Cant. |
|---|:---:|
| ↑ ↓ ← → | 4 |
| A / B | 2 |
| Start | 1 |
| Select | 1 |
| **Total** | **8** |

El D-pad visible de la carcasa puede ser una pieza impresa en 3D que presione cuatro tact switches 6×6, así que tampoco necesitamos comprar un D-pad electrónico.

## Arquitectura definitiva V1

```text
               KIDBOX V1

          Raspberry Pi Pico RP2040
                    │
        ┌───────────┼────────────┐
        │           │            │
       SPI         I2S          GPIO
        │           │            │
        ▼           ▼            ▼
 ILI9341 2.4"   PCM5102A     8 botones
   240×320          │       ↑ ↓ ← → A B
                    │       Start / Select
                 Jack 3.5"
                    │
                Audífonos


          LiPo 3.7 V / 500 mAh
                    │
                 TP4056
                    │
                ON / OFF
                    │
                 Pico VSYS
```