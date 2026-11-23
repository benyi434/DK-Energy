// FIRMWARE PIC16F887 - DK ENERGY
// Modo: Low Power (LP) con cristal 32.768 kHz
// Compilador: CCS C (adaptado para Proteus)
// Objetivo: Lectura ADC batería/divisor, mostrar V y A en LCD 16x2 via UART HC-05

// CONFIGURACIÓN DE FUSIBLES (PROTEUS LP MODE):
// #fuses LP, NOWDT, NOPROTECT, NOBROWNOUT, NOLVP, PUT, NOMCLR
// Usar oscilador interno con timer1 desactivado o externo

// --- DEFINICIONES CONFIGURABLES ---

// Valores divisor de tensión (para convertir ADC en voltios reales)
// Definir R1 y R2 según el divisor físico en la placa
#define R1        10000.0     // 10 kohm (bateria)
#define R2         3300.0     // 3.3 kohm (bateria)
#define VREF      5.0         // tension de referencia del ADC (VDD)

// Curva de la bateria 18650 (limites de trabajo)
#define V_MIN       3.30      // bateria "vacia" (0%)
#define V_MAX       4.20      // bateria llena (100%)

// --- GLOBALES ---

int promedio = 0;        // promedio de las lecturas (10 bits)
float tension  = 0;      // tension real de la bateria en voltios
unsigned int porcent  = 0;       // porcentaje de carga calculado
char         cadena[20];         // buffer donde se arma lo que se envia

// --- FUNCION: leer_adc_promedio() ---
// Lee 16 muestras por el canal AN0 y devuelve el promedio.
// Promediar varias muestras ayuda a quitar el ruido de la senal.

int leer_adc_promedio(void){
   int32 suma = 0;      // sumatoria de las muestras
   int i;

   for (i = 0; i < 16; i++){
      suma = suma + read_adc();   // lee el canal ya seleccionado (AN0)
      delay_ms(20);               // separo las muestras en el tiempo
   }
   return (int)(suma / 16);       // promedio entero
}

// --- FUNCION: calcular_tension() ---
// Convierte el valor promedio del ADC en voltios reales usando
// la formula del divisor de resistencias (R1 y R2).
// Vbat = ADC x VREF / 1023 x (R1 + R2) / R2

float calcular_tension(int adc_prom){
   float v;

   v = (float)adc_prom * (VREF / 1023.0);          // a voltios (esc. ADC)
   v = v * ((R1 + R2) / R2);                     // le agrega el divisor

   return (v);
}

// --- FUNCION: calcular_porcentaje() ---
// Convierte la tension de la bateria a un porcentaje dentro
// del rango util de la celda (entre V_MIN y V_MAX).

unsigned int calcular_porcentaje(float v){
   unsigned int por;

   if (v >= V_MAX)       por = 100;   // total
   else if (v <= V_MIN)  por = 0;     // agotada
   else{
      /* regla de tres simple dentro del rango util */
      por = (unsigned int)((v - V_MIN) * 100.0 / (V_MAX - V_MIN));
   }
   return (por);
}

// --- FUNCION MAIN ---
void main(void){
   // ----- configuracion inicial de los modulos -----
   // Configurar ADC para usar canal AN0
   setup_adc_ports(sAN0);            // solo RA0/AN0 configurado analogico
   setup_adc(ADC_CLOCK_INTERNAL);   // reloj interno del ADC
   set_adc_channel(0);               // selecciono el canal 0 (RA0)

   delay_ms(500);                    // espera de estabilizacion del sistema

   // ----- bucle infinito (el micro nunca se apaga) -----
   while (TRUE){
      // paso 1: tomar las muestras de la bateria y promediar
      promedio = leer_adc_promedio();

      // paso 2: pasar el numero del ADC a voltios reales
      tension = calcular_tension(promedio);

      // paso 3: pasar de voltios a porcentaje (0 - 100%)
      porcent = calcular_porcentaje(tension);

      // paso 4: armar el mensaje que se envia por UART al modulo HC-05
      // Formato: V:xx.xx|yy%
      sprintf(cadena, "V:%5.2f|%u%%\n", tension, porcent);

      // paso 5: enviarlo por UART al HC-05
      printf("%s", cadena);

      // espera antes del siguiente envio (se actualiza cada 1 segundo)
      delay_ms(1000);
   }
}
