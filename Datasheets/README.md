# Datasheets Verificados - DK Energy

Este directorio contiene la información técnica verificada directamente de los datasheets de fabricante para cada componente principal del proyecto.

## Índice de Datasheets

1. [PIC16F887](PIC16F887.md) - Microcontrolador principal
2. [TP4056](TP4056.md) - Cargador Li-ion
3. [MT3608](MT3608.md) - Boost converter step-up
4. [LM2596](LM2596.md) - Buck converter step-down (NO USADO EN DISEÑO FINAL)
5. [LM393](LM393.md) - Dual comparador (amplificador corriente)
6. [1N5822](1N5822.md) - Diodo Schottky 3A
7. [18650](18650.md) - Celda Li-ion genérica
8. [LCD_LM016L](LCD_LM016L.md) - Display LCD 16x2
9. [BC547](BC547.md) - Transistor NPN

---

## Resumen de Datos Críticos para el Diseño

### PIC16F887 (Microchip DS41291)
- **Alimentación:** 2.0V - 5.5V
- **ADC:** 10 bits, 14 canales (AN0-AN13)
- **UART:** TX=RC6, RX=RC7
- **ADC Canal 0:** RA0/AN0 (pin 2)
- **ADC Canal 1:** RA1/AN1 (pin 3)
- **ADC Canal 2:** RA2/AN2 (pin 4)
- **Oscilador LP:** RA6/OSC2 (pin 14), RA7/OSC1 (pin 13) - cristal 32.768 kHz
- **INT externo:** RB0/INT (pin 33) - flanco descendente para wake-up
- **I/O:** 35 pines (Puertos A-E)
- **Empaque:** DIP-40 (PDIP)

### TP4056 (Nanjing Top Power)
- **Entrada:** 4.0V - 8.0V (máx abs 8V)
- **Corriente carga máx:** 1000mA (ajustable con R_PROG: I=1200/R_PROG mA)
- **Voltaje fin de carga:** 4.2V ±1.5%
- **Fases:** Trickle (<2.9V) → CC → CV → Terminación C/10
- **Protecciones:** Térmica (145°C), UVLO, Soft-start, NTC en pin TEMP
- **Pines:** IN+(4), IN-(3), BAT+(5), BAT-(3), OUT+(5), OUT-(3), PROG(2), CHRG(7), STDBY(6), TEMP(1), CE(8)
- **LED:** CHRG=rojo (carga), STDBY=verde (fin carga)
- **Sleep:** <2µA
- **Encapsulado:** SOP-8

### MT3608 (Aerosemi)
- **Entrada:** 2V - 24V (UVLO ~1.98V)
- **Salida:** hasta 28V ajustable
- **Corriente switch:** 4A límite (~2A salida real)
- **Frecuencia:** 1.2 MHz fija
- **Eficiencia:** hasta 97%
- **VREF:** 0.6V → VOUT = 0.6 × (1 + Rtop/Rbot)
- **Inductor:** 4.7-22µH
- **Capacitor salida:** 22µF
- **Diodo:** Schottky requerido
- **Protecciones:** Soft-start, térmica 155°C
- **Encapsulado:** SOT23-6
- **Pines:** 1=SW, 2=GND, 3=FB, 4=EN, 5=IN, 6=NC

### LM393 (Texas Instruments)
- **Dual comparador**, colector abierto
- **Alimentación:** 2V - 36V (o ±1V a ±18V)
- **Corriente salida:** 6-16mA (colector abierto)
- **Tiempo respuesta:** 1.3µs típico
- **Offset entrada:** ±1mV típico, ±5mV máx
- **Consumo:** 0.4mA típico (ambos comparadores)
- **Encapsulado:** SOIC-8, DIP-8

### 1N5822 / SS34 (Vishay / Generic)
- **Corriente directa:** 3A
- **Voltaje inverso:** 40V (1N5822), 40V (SS34)
- **Caída directa:** ~0.3V a 3A (Schottky)
- **Tiempo recuperación:** ~0ns (mayoría portadores)
- **Encapsulado:** DO-214AA (SMB) - SMT

### 18650 Genérica (Parámetros típicos)
- **Química:** Li-ion (LiCoO2 o NMC)
- **Voltaje nominal:** 3.7V
- **Voltaje carga completa:** 4.2V
- **Voltaje corte descarga:** 2.5V - 3.0V (según protección)
- **Capacidad típica:** 1600-3500mAh
- **Corriente descarga máx:** 0.5C - 1C (800mA - 3A para 1600mAh)
- **Energía:** ~5.9 Wh (1600mAh × 3.7V)
- **Temperatura carga:** 0°C a 45°C
- **Temperatura descarga:** -20°C a 60°C

### LCD LM016L (Orient Display)
- **Controlador:** HD44780 compatible
- **Caracteres:** 16 columnas × 2 líneas
- **Modos:** 8 bits o 4 bits (DK Energy usa 4 bits)
- **Alimentación:** 5V (VDD-VSS)
- **Contraste:** Pin VO (0-VCC), potenciómetro 10kΩ
- **Retroiluminación:** LED, pines A (ánodo) y K (cátodo), ~15-20mA a 5V
- **Pines:** 16 (1=VSS, 2=VDD, 3=VO, 4=RS, 5=RW, 6=E, 7-14=D0-D7, 15=A, 16=K)

### BC547 / 2N2222 (ON Semiconductor / Generic)
- **Tipo:** NPN propósito general
- **VCEO:** 45V (BC547), 40V (2N2222)
- **IC máx:** 100mA (BC547), 600mA (2N2222)
- **hFE:** 110-800 (BC547), 100-300 (2N2222)
- **Encapsulado:** TO-92 (ambos)
- **Uso en DK Energy:** Switch retroiluminación LCD (base 1kΩ desde RC0/RCx PIC)

---

## Reglas de Diseño Derivadas de Datasheets

1. **TP4056 NO da 5V regulado** - Solo carga la celda a 4.2V. La salida 5V viene del MT3608.
2. **MT3608 entrada 2-24V** - Funciona directo desde batería 3.0-4.2V.
3. **LM393 salida colector abierto** - REQUIERE pull-up (1kΩ a VCC en DK Energy).
4. **PIC16F887 oscilador LP** - Cristal 32.768kHz en RA6/RA7 (NO en RC0/RC1).
5. **Divisores tensores ADC** - 10k/10k da 0-2.5V en ADC para entrada 0-5V (referencia VDD=5V).
6. **Shunt 0.1Ω + LM393 ganancia 48** - 50mV offset = 50mA error → calibrar con carga cero.
7. **Protección TP4056 en OUT+/OUT-** - Cargar teléfono en OUT+/OUT-, NO en B+/B-.
8. **MT3608 ajustar a 5.0V SIN carga** - Medir en USB-A antes de conectar teléfono.
9. **Diodo Schottky panel** - Caída ~0.3V vs 0.7V 1N4007. Panel 5V → ~4.7V en TP4056 IN (OK, >4.0V mínimo).
10. **Cristal 32kHz + 15pF cada pin** - Especificación Microchip para oscilador LP.

---

*Datos extraídos directamente de datasheets PDF usando PyMuPDF (fitz)*
*Ubicación original: C:\Users\gabyr\DKEnergy\investigacion\datasheets\*
*Fecha verificación: 2026-08-05 (actualizado 2026-11-20)*