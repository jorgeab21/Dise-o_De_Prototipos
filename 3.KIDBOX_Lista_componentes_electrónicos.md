# Bill of Materials (BOM) — KIDBOX V1

| # | Componente | Cant. | Especificación / función | Estado |
|---|---|---:|---|---|
| 1 | **Waveshare RP2350-Plus** | 1 | MCU principal RP2350A, USB-C, cargador LiPo y regulación integrados | ✅ DEC |
| 2 | **TFT Touch 2.4" ILI9341** | 1 | 240×320, SPI, XPT2046 integrado, zócalo MicroSD | 🛒 Comprar |
| 3 | **PCM5102A GY-PCM5102** | 1 | DAC I2S para salida de audio | ✅ DEC / profesor |
| 4 | **Jack 3.5 mm** | 1 | Salida de audio | ✅ Integrado en PCM5102A |
| 5 | **Audífonos** | 1 | Reproducción y validación de audio | ✅ / conseguir |
| 6 | **LiPo 1S 3.7 V, 1000–1200 mAh** | 1 | Protección PCM, carga admitida ≥1 A, grosor ≤10 mm; dimensiones reales compatibles con carcasa | 🛒 Comprar |
| 7 | **Adaptador/conector batería 2P** | 1 | Compatible con conector 1.25 mm del RP2350-Plus; adaptar PH2.0 si la batería elegida lo requiere | 🟡 Según batería |
| 8 | **Interruptor ON/OFF** | 1 | Control mediante PWR_EN / 3V3_EN del RP2350-Plus | 🟡 Revisar / comprar |
| 9 | **Tact switches 6×6 mm** | 8 | ↑ ↓ ← →, A, B, Start, Select | ✅ DEC |
| 10 | **Headers macho 2.54 mm** | varios | Conexión de módulos | ✅ DEC |
| 11 | **Headers hembra 2.54 mm** | varios | RP2350-Plus, pantalla y DAC desmontables | ✅ DEC |
| 12 | **Capacitores 100 nF** | 2–3 | Desacoplo adicional si el esquemático lo requiere | 🟡 DEC / revisar |
| 13 | **Capacitor 10–47 µF** | 1–2 | Filtrado/bulk próximo a módulos si se requiere | 🟡 DEC / revisar |
| 14 | **PCB KIDBOX 2 capas** | 1 | Carrier board propia | 🔴 Fabricar |
| 15 | **Carcasa impresa 3D** | 1 | Enclosure KIDBOX | 🔴 Diseñar / imprimir |
| 16 | **Insertos roscados M2/M2.5** | 4–6 | Fijación PCB/carcasa | ✅ DEC |
| 17 | **Tornillos M2/M2.5** | 4–6 | Ensamble | 🟡 DEC / revisar |
| 18 | **Cable USB-C** | 1 | Programación y carga del RP2350-Plus | ✅ DEC |

---

## Batería — Requisito definitivo

> Batería LiPo 1S de 3,7 V y 1000–1200 mAh, con protección integrada, cuya ficha técnica autorice una corriente de carga de al menos 1 A. Grosor máximo objetivo de 10 mm y dimensiones reales compatibles con un espacio aproximado de 21,5 × 54 mm, dejando tolerancia y sin comprimir la celda. Conector 2P compatible con el RP2350-Plus o adaptador correspondiente, verificando polaridad antes de conectar.

- **Candidata MCI 1000 mAh:** Puede figurar como candidata (*Pendiente confirmar dimensiones físicas reales*).
- **Adaptación de conector:** Si viene con conector PH2.0, se requiere adaptación hacia el conector de 1,25 mm 2P de Waveshare.
- **Cargador integrado:** El esquema oficial muestra ese conector de batería y el cargador ETA6096 configurado alrededor de 1 A ([Waveshare Files](https://files.waveshare.com/wiki/RP2350-Plus/RP2350_Plus.pdf?utm_source=chatgpt.com)).

---

## Interruptor ON/OFF: Pequeña mejora importante

Con el módulo **RP2350-Plus**, no se debe colocar el interruptor cortando directamente el cable de la batería.  
Se aprovechará el pin:

**`PWR_EN` / `3V3_EN`** del propio módulo.

El esquema de Waveshare muestra que ese pin controla el pin EN del regulador MP28164 y dispone de un pull-up interno en la placa ([Waveshare Files](https://files.waveshare.com/wiki/RP2350-Plus/RP2350_Plus.pdf?utm_source=chatgpt.com)).

**Conceptualmente:**

```text
PWR_EN ── Switch ── GND
```

De esa forma podemos apagar la electrónica principal sin desconectar necesariamente el sistema de carga de la batería. Esto es mucho más limpio para una consola recargable.

---

## Controles definitivos

| Función | Cant. |
|---|:---:|
| ↑ ↓ ← → | 4 |
| A / B | 2 |
| Start | 1 |
| Select | 1 |
| **Total** | **8** |

- La cruceta exterior será una pieza impresa en 3D que acciona cuatro tact switches 6×6 mm, por lo que no necesitamos comprar un D-pad electrónico.
- No se incluyen botones L/R en KIDBOX V1: agregan complejidad mecánica y no son necesarios para los juegos educativos definidos.

---

## Pantalla

La TFT queda definida como:
**ILI9341 2.4", 240×320, SPI, touch XPT2046 y lector MicroSD integrados.**

Para V1:

| Función pantalla | Uso |
|---|:---:|
| ILI9341 | ✅ Sí |
| Backlight | ✅ Sí |
| XPT2046 Touch | ❌ No inicialmente |
| MicroSD | ❌ No inicialmente |

*Aunque esos componentes vengan físicamente en el módulo, no forman parte funcional de la V1.*

---

## Arquitectura definitiva actualizada

```text
                             KIDBOX V1
                       Waveshare RP2350-Plus
                             (RP2350A)
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
       SPI                      I2S                      GPIO
        │                        │                        │
        ▼                        ▼                        ▼
  ILI9341 2.4"                PCM5102A                 8 botones
    240×320                      │                   ↑ ↓ ← →, A, B
        │                        ▼                   Start, Select
 ┌──────┴───────┐            Jack 3.5 mm
 │ XPT2046 Touch│                │
 │  [NO USADO]  │                ▼
 │MicroSD socket│            Audífonos
 │  [NO USADO]  │
 └──────────────┘

               ┌────── ALIMENTACIÓN ──────┐
               │                          │
               │ LiPo 3.7 V 1S 1000–1200mAh│
               │            │             │
               │     conector 1.25 mm     │
               │            │             │
               │            ▼             │
               │  RP2350-Plus integrado   │
               │     ┌──────┴──────┐      │
               │     │             │      │
               │  ETA6096       MP28164   │
               │ cargador     regulación  │
               │     │             │      │
               │   USB-C      sistema 3V3 │
               │                   │      │
               │                PWR_EN    │
               │                   │      │
               │                ON / OFF  │
               │                 (GND)    │
               └──────────────────────────┘
```