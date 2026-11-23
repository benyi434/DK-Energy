# Investigación de Proyectos Similares en GitHub

## Resumen ejecutivo
Se investigaron repositorios públicos relacionados con powerbanks solares, cargadores TP4056/MT3608, monitoreo de baterías con PIC16F887, y diseños PCB en KiCad. Se encontraron **12 repositorios relevantes** con distintos grados de compatibilidad con DK Energy.

---

## 1. Proyectos de arquitectura similar (TP4056 + MT3608 + 18650)

### 1.1 adityabalul/Solar-Mobile-Charging-Using-Embedded-System ⭐ MÁS RELEVANTE
- **URL:** https://github.com/adityabalul/Solar-Mobile-Charging-Using-Embedded-System
- **Arquitectura:** Panel solar → 1N5819 Schottky → TP4056 → 18650 → MT3608 → USB 5V
- **MCU:** Arduino Nano (no PIC)
- **Display:** LCD 16x2 I2C
- **Medición:** Módulo sensor de voltaje 25V (divisor resistivo) → ADC Arduino
- **Licencia:** MIT
- **Partes reutilizables:**
  - Diagrama de bloques de potencia (idéntico a DK Energy salvo el diodo: 1N5819 vs 1N5822/SS34)
  - Esquema de conexión TP4056 (IN+/IN- del panel, B+/B- batería, OUT+/OUT- a MT3608)
  - Cálculo de voltaje con divisor resistivo
  - Estructura de carpeta del repo (code/, docs/, images/)
- **Diferencias clave:**
  - Arduino Nano vs PIC16F887 (cambia firmware, pines, ADC)
  - LCD I2C vs LCD paralelo 4 bits (menos pines, distinta librería)
  - No mide corriente de descarga (DK Energy sí, con shunt + LM393)
  - No tiene sleep mode ni botones de menú

### 1.2 scorpHQ/SOLAR-BATTERY-CHARGER
- **URL:** https://github.com/scorpHQ/SOLAR-BATTERY-CHARGER
- **Enfoque:** Tutorial paso a paso, sin MCU ni monitoreo
- **Componentes:** TP4056 + MT3608 + 1N4007 (diodo, no Schottky ideal)
- **Útil para:** Validar conexiones básicas de potencia, confirmar que OUT+/OUT- del TP4056 va al MT3608 (no B+/B-)
- **Advertencia:** Usa 1N4007 (recuperación lenta, caída ~0.7V) en lugar de Schottky (caída ~0.3V). DK Energy usa Schottky 3A.

### 1.3 Wirecora - Solar power bank (artículo técnico, no repo)
- **URL:** https://wirecora.com/circuits/solar-power-bank
- **Valor crítico:** Explica **por qué el boost va en OUT+/OUT- del TP4056, no en B+/B-**. La protección (DW01+8205A) está entre B- y OUT-. Conectar la carga en B saltea la protección.
- **Detalles de diseño:** Panel 5V/2W → TP4056 → 18650 → MT3608 ajustado a 5.0V → USB-A
- **Cálculo energético:** 18650 2200mAh ≈ 8.1 Wh → ~7.3 Wh tras boost (90% eficiencia) → ~1/3 de carga de teléfono (19 Wh típicos)
- **Coincide 100% con la arquitectura de DK Energy.**

### 1.4 AZ-Delivery / Hackster.io - Solar Powerbank
- **Mismo esquema:** Panel 5V → TP4056 → 18650 → MT3608 → USB-A
- **Corriente de carga real:** ~150 mA a pleno sol (panel 2W), 30-80 mA nublado
- **Carcasa:** PET-G impresa 3D (PLA se ablanda >60°C)
- **Confirmación práctica:** El MT3608 se ajusta ANTES de conectar el teléfono (medir en USB-A y girar trimmer hasta 5.0V)

---

## 2. Proyectos con PIC16F887 / PIC para monitoreo de batería

### 2.1 Artículo académico - "Design and Construction of a Remote Battery Monitoring... Using PIC16F887"
- **Fuente:** Journal of Energy Technology and Environment, 2023
- **MCU:** PIC16F887 + módulo GSM A6 (no Bluetooth)
- **Función:** Monitoreo remoto de SOC, control de carga
- **Relevancia:** Confirma PIC16F887 como MCU viable para monitoreo de batería. Usa ADC interno.
- **Diferencia:** Comunicación GSM vs LCD local + Bluetooth (DK Energy usa HC-05 → app, pero el contexto actual dice LCD + botones, sin Bluetooth).

### 2.2 Microchip Official - Battery Monitoring System (PIC16F15276)
- **Repo:** microchip-pic-avr-examples/pic16f15276-cnano-battery-monitoring-system-mplab-mcc
- **MCU:** PIC16F15276 (familia moderna, no 16F887)
- **Características:** ADC 10-bit, EUSART, medición carga/descarga, estimación SoC
- **Útil para:** Referencia de código C (MCC/MPLAB X) para medición de corriente y voltaje, cálculo SoC. Adaptable a CCS C.

---

## 3. Diseños PCB en KiCad (para referencia de esquemáticos y footprints)

### 3.1 kubabuda/misc_footprints ⭐ FOOTPRINTS LISTOS
- **URL:** https://github.com/kubabuda/misc_footprints
- **Contiene footprints KiCad para:**
  - TP4056 módulo con BMS (DW01 + 8205S) - **EXACTAMENTE el módulo de DK Energy**
  - MT3608 DC-DC step-up
  - XL6009 (boost alternativo)
  - MP1584 (buck)
  - Portabatería 18650 (casket)
- **Licencia:** No especificada en la descripción, verificar en el repo.
- **Uso directo:** Copiar footprints a librería local de KiCad para DK Energy.

### 3.2 jaisor/SNAP_Power_Controller ⭐ DISEÑO KICAD COMPLETO
- **URL:** https://github.com/jaisor/SNAP_Power_Controller
- **Herramienta:** KiCad 10
- **Arquitectura:** CN3791 MPPT (no TP4056) + INA3221 (monitor I2C 3 canales) + 1S LiPo
- **Licencia:** CERN-OHL-P-2.0 (hardware) + MIT (scripts) - **Permisiva, permite reuso con atribución**
- **Partes reutilizables:**
  - Estructura de proyecto KiCad profesional
  - Esquemático con jerarquía (hojas separadas: charger, monitor, conectores)
  - Footprints de conectores JST, portabatería
  - Reglas DRC, zonas de cobre, pistas de potencia
  - Scripts de validación (tools/)
- **Diferencia clave:** Usa CN3791 (MPPT) + INA3221 (I2C) vs TP4056 + ADC directo + LM393. La parte de **monitor de potencia (INA3221) es alternativa superior al LM393** si se quiere I2C, pero DK Energy ya decidió LM393 por simplicidad y costo.

### 3.3 panovvv/solar-harvester
- **URL:** https://github.com/panovvv/solar-harvester
- **Enfoque:** Cajas impresas 3D para placas solares + electrónica (TP4056, CN3065, CN3791, MCP73871)
- **PCB:** No parece tener esquemático/PCB propio, solo STLs de cajas.
- **Útil para:** Referencia de cajas 3D para 18650 + TP4056 + panel solar.

### 3.4 fadushin/solar-esp32
- **URL:** https://github.com/fadushin/solar-esp32
- **KiCad:** Esquemático + PCB para cargador solar LiFePO4 (3.2V) con ESP32
- **Diferencia:** Química LiFePO4 (3.2V/3.65V) vs Li-ion 3.7V/4.2V. TK4056 no sirve para LiFePO4 sin modificación.
- **Valor:** Ver cómo organizan un proyecto KiCad de potencia + MCU.

---

## 4. Proyectos avanzados (MPPT, STM32, ESP32) - Solo referencia

### 4.1 RASITH7/MPPT-Solar-Charger-with-Advanced-Control-and-Monitoring
- **MCU:** STM32F407 + ESP32
- **Topología:** Boost MPPT con IA (Redes Neuronales)
- **Licencia:** No clara
- **Valor:** Solo como referencia de "estado del arte", NO compatible con DK Energy (complejidad, costo, componentes).

---

## 5. Tabla comparativa de compatibilidad

| Repo | Arquitectura potencia | MCU | Display | Medición corriente | PCB KiCad | Licencia | Compatibilidad DK Energy |
|------|----------------------|-----|---------|-------------------|-----------|----------|-------------------------|
| adityabalul/Solar-Mobile... | **IDÉNTICA** | Arduino Nano | LCD I2C | No | No | MIT | **ALTA** (potencia), Media (MCU) |
| Wirecora (artículo) | **IDÉNTICA** | Ninguno | No | No | No | - | **ALTA** (validación teoría) |
| kubabuda/misc_footprints | N/A (solo footprints) | - | - | - | **SÍ (TP4056, MT3608, 18650)** | ? | **ALTA** (footprints listos) |
| jaisor/SNAP_Power_Controller | CN3791 MPPT | ESP32/MCU externo | No (INA3221 I2C) | **SÍ (INA3221 3ch)** | **SÍ (KiCad 10 completo)** | CERN-OHL-P-2.0 | Media (PCB), Baja (arquitectura) |
| panovvv/solar-harvester | Múltiples | No | No | No | No (solo STLs) | ? | Baja (solo cajas 3D) |
| Microchip PIC16F15276 | Genérica | PIC16F15276 | No (EUSART) | **SÍ (ADC + shunt)** | No | MIT | Media (código C referencia) |

---

## 6. Decisiones derivadas de la investigación

### 6.1 Confirmaciones de diseño DK Energy
1. ✅ **Arquitectura de potencia validada:** Panel → Schottky → TP4056 (IN) → Batería (B) → TP4056 (OUT) → MT3608 → USB-A. **Wirecora confirma que OUT+/OUT- es correcto para no saltear protección.**
2. ✅ **Diodo Schottky 3A (1N5822/SS34):** Correcto vs 1N4007 (scorpHQ usa 1N4007, menos eficiente).
3. ✅ **MT3608 ajustado a 5.0V SIN carga:** Confirmado por AZ-Delivery y Wirecora.
4. ✅ **Capacidad real:** 1600mAh → ~5.9 Wh → ~5 Wh útiles → ~30-45% carga teléfono. Coincide con Wirecora (2200mAh → ~1/3 carga).
5. ✅ **Corriente de carga realista:** Panel 2W/5V → ~380mA máx → TP4056 limita a lo que dé el panel. AZ-Delivery midió 150mA real a pleno sol.

### 6.2 Recursos reutilizables directos
1. **Footprints KiCad:** `kubabuda/misc_footprints` → TP4056 módulo, MT3608, portabatería 18650. **Copiar a librería local.**
2. **Estructura proyecto KiCad:** `jaisor/SNAP_Power_Controller` → jerarquía de hojas, reglas DRC, scripts. **Adaptar como plantilla.**
3. **Código C referencia ADC + shunt:** `microchip-pic-avr-examples` (PIC16F15276) → adaptar a PIC16F887 + CCS C.
4. **Diagrama de bloques potencia:** `adityabalul/Solar-Mobile...` → usar como base visual para documentación.

### 6.3 Alternativas técnicas identificadas
| Función | Actual DK Energy | Alternativa encontrada | Pros/Contras |
|---------|------------------|------------------------|--------------|
| Medición corriente | LM393 + shunt 0.1Ω (ganancia 48) | INA219/INA3221 I2C | +Preciso, +Fácil código, -Costo, -Complejidad I2C, -Pines extra |
| Medición voltaje | Divisor resistivo 10k/10k + ADC | Módulo sensor 25V (divisor integrado) | +Simple, -Costo extra, -Ocupa mismo pin ADC |
| Display | LCD 16x2 paralelo 4 bits (6 pines) | LCD I2C (2 pines) | +Libera 4 pines, -Costo módulo I2C, -Código distinto |
| Cargador | TP4056 (no MPPT) | CN3791 (MPPT) | +Eficiencia panel, -Costo, -Complejidad, -Inductor extra |

**Decisión:** Mantener diseño actual (TP4056 + LM393 + LCD paralelo) por simplicidad, costo y requisitos de cátedra (explicar cada etapa). Documentar alternativas en informe.

---

## 7. Próximos pasos para el repositorio DK-Energy

1. **Descargar footprints** de `kubabuda/misc_footprints` → `DK-Energy/Referencias_GitHub/kubabuda_footprints/`
2. **Clonar/descargar** `jaisor/SNAP_Power_Controller` → `DK-Energy/Referencias_GitHub/SNAP_Power_Controller/` como plantilla KiCad
3. **Crear estructura KiCad** en `DK-Energy/Esquematico/` y `DK-Energy/PCB/`
4. **Documentar datasheets** en `DK-Energy/Datasheets/` (ya tenemos banco verificado en skill)
5. **Escribir guía de esquemático** basada en validaciones de Wirecora + adityabalul
6. **Preparar firmware PIC16F887** en `DK-Energy/Firmware/` (basado en contexto + código Microchip de referencia)

---

## 8. Enlaces directos a recursos clave

- **Footprints TP4056/MT3608/18650:** https://github.com/kubabuda/misc_footprints
- **Plantilla KiCad completa:** https://github.com/jaisor/SNAP_Power_Controller
- **Validación arquitectura potencia:** https://wirecora.com/circuits/solar-power-bank
- **Proyecto Arduino similar:** https://github.com/adityabalul/Solar-Mobile-Charging-Using-Embedded-System
- **Código Microchip batería:** https://github.com/microchip-pic-avr-examples/pic16f15276-cnano-battery-monitoring-system-mplab-mcc
- **Datasheets verificados:** Ver `DK-Energy/Datasheets/` y skill `dk-energy-project` → `references/bank-datasheets.md`

---

*Investigación realizada: 2026-11-20*
*Fuentes: GitHub Search, web search, documentación técnica*
*Licencias respetadas: MIT, CERN-OHL-P-2.0 - atribución requerida al reusar*