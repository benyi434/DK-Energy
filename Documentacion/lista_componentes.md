# Lista de Componentes - DK Energy

## Componentes de Potencia

| Ref | Componente | Valor/Especificación | Cantidad | Proveedor | Precio (ARS) | Estado |
|-----|------------|----------------------|----------|-----------|--------------|--------|
| SP1 | Panel solar | 5V, 2W, salida USB, máx 380mA | 1 | - | - | Disponible |
| D1 | Diodo Schottky | 1N5822 o SS34, 3A, 40V | 1 | Starware | ~$500 | Por comprar |
| U1 | Módulo TP4056 | Con protección DW01+ML8205A, 1A | 1 | Starware | $859 | Disponible |
| BT1 | Batería 18650 | 3.7V, 1600mAh (vendedor) | 1 | Mercado Libre | $5.735 | Disponible |
| BT1_H | Portabatería 18650 | 2 pines, paso 70mm aprox | 1 | Starware | $4.459 | Por comprar |
| U2 | Módulo MT3608 | Step-up 2A, ajustable a 5.0V | 1 | Mercado Libre | $2.897 | Disponible |
| J1 | Conector USB-A hembra | Salida a teléfono, 4 pines + shield | 1 | Starware | $619 | Por comprar |

## Componentes de Control (PIC16F887)

| Ref | Componente | Valor/Especificación | Cantidad | Proveedor | Precio (ARS) | Estado |
|-----|------------|----------------------|----------|-----------|--------------|--------|
| U3 | PIC16F887-I/P | DIP-40, 14KB Flash, 368B RAM | 1 | - | $0 | Reusar de placa |
| X1 | Cristal | 32.768 kHz, 12.5pF carga | 1 | - | ~$200 | Por comprar |
| C1, C2 | Capacitores cristal | 15pF cerámicos (a masa cada pin) | 2 | - | ~$50 | Por comprar |
| J2 | LCD 16x2 | LM016L o compatible HD44780 | 1 | - | ~$2.500 | Por comprar |
| RV1 | Potenciómetro | 10kΩ (contraste LCD) | 1 | - | ~$300 | Por comprar |
| R1-R8 | Resistencias 1% | 10kΩ (divisores tensión) | 8 | - | ~$200 | Por comprar |
| R9, R10 | Resistencias | 3.3kΩ (pull-ups botones) | 2 | - | ~$50 | Por comprar |
| R11 | Resistencia shunt | 0.1Ω 1% 1W (medición corriente) | 1 | - | ~$500 | Por comprar |
| R12 | Resistencia | 1kΩ (pull-up LM393 salida) | 1 | - | ~$50 | Por comprar |
| R13 | Resistencia | 470kΩ (ganancia LM393) | 1 | - | ~$50 | Por comprar |
| R14 | Resistencia | 10kΩ (ganancia LM393) | 1 | - | ~$50 | Por comprar |
| R15 | Resistencia | 330Ω (LED verde) | 1 | - | ~$50 | Por comprar |
| R16 | Resistencia | 1kΩ (base transistor) | 1 | - | ~$50 | Por comprar |
| C3-C10 | Capacitores 100nF | Cerámicos (desacople VDD/VSS PIC, ADC, etc.) | 8 | - | ~$200 | Por comprar |
| C11 | Capacitor 100µF | 16V electrolítico (salida 5V MT3608) | 1 | - | ~$300 | Por comprar |
| U4 | LM393 | Dual comparador (amplificador no inversor corriente) | 1 | - | ~$500 | Disponible (2 unidades) |
| Q1 | Transistor NPN | BC547 o 2N2222 (retroiluminación LCD) | 1 | - | ~$150 | Por comprar |
| D2 | LED verde | 3mm, 20mA (indicador carga) | 1 | - | ~$100 | Por comprar |
| SW1 | Pulsador táctil | 6x6mm (B.A - encendido) | 1 | - | ~$150 | Por comprar |
| SW2 | Pulsador táctil | 6x6mm (B.M - menú) | 1 | - | ~$150 | Por comprar |
| SW3 | Pulsador táctil | 6x6mm (B.C - teléfono simulado) | 1 | - | ~$150 | Por comprar |
| J3 | Header ICSP | 1x6 pines 2.54mm (programación PIC) | 1 | - | ~$200 | Por comprar |

## Componentes Opcionales / Alternativos

| Ref | Componente | Valor/Especificación | Notas |
|-----|------------|----------------------|-------|
| J4 | Jack DC 2.1mm | Entrada alternativa 5V | Opcional, no en diseño final |
| - | Zócalo DIP-40 | Para PIC16F887 | Ya está en la placa entrenadora |

## Resumen de Costos Estimados

| Categoría | Costo Estimado (ARS) |
|-----------|---------------------|
| Potencia (panel, TP4056, MT3608, batería, portabatería, diodo, USB) | ~$15.000 |
| Control (LCD, cristal, potenciómetro, LM393, transistor, LED, botones, ICSP, passives) | ~$6.000 |
| PCB (fabricación) | ~$5.000 - $10.000 |
| Carcasa (impresión 3D PET-G) | ~$2.000 |
| **Total estimado** | **~$28.000 - $33.000** |
| **Presupuesto máximo** | **$100.000** |
| **Margen** | **~$67.000 - $72.000** |

## Notas de Compra

1. **PIC16F887**: Se reutiliza de la placa entrenadora vieja del colegio. NO comprar.
2. **Zócalo DIP-40**: Ya está soldado en la placa entrenadora. NO comprar.
3. **Resistencias/capacitores/cristal/reguladores**: Reciclar de la placa vieja → puede bajar la compra a ~$10-15k.
4. **Precios Starware**: Verificar re-rodando scraper antes de comprar (precios cambian).
5. **Mercado Libre**: Links de búsqueda para confirmar precios manualmente (no scrapeable).

---

*Lista basada en presupuesto confirmado 2026-08-05 y contexto del proyecto DK Energy*
*Fecha: 2026-11-20*