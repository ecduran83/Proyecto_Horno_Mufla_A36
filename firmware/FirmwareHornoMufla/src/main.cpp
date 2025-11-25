#include <Arduino.h>
#include <ESP32Encoder.h>
#include <LiquidCrystal_I2C.h>
#include <Preferences.h>
#include <max6675.h>

// Configuracion de pines
# define ENCODER_CLK 14//18//14//19
# define ENCODER_DT 27//19//27//18
# define BUTTON_START_PIN 25//27///25//23
# define BUTTON_STOP_PIN 32//26//32//27

// Pines para MAX6675
# define MAX_SCK_PIN 5//25//5//17
# define MAX_CS_PIN 18//33////18//5
# define MAX_MISO_PIN 19//32//19//16

// Pines Led
# define LED_ON 4
# define LED_OFF 16

// Nombre para la memoria NVS
# define NVS_NAMESPACE "horno_config"
# define NVS_KEY_SETPOINT "last_sp"
# define NVS_KEY_SOAK "last_soak"
# define NVS_KEY_RAMP "last_ramp"
# define NVS_KEY_MODE "last_mode"
# define MAX_CMD_LEN 50 
#define CONTROL_CYCLE_TIME_MS 1000

// Definiciones de Control PID y SSR
# define SSR_PIN 13//4//13//25

void limpiarSerialEntrada();

// Objetos globales y de FreeRTOS
LiquidCrystal_I2C lcd(0x27, 16, 2);
ESP32Encoder encoder;
Preferences preferences;
MAX6675 max6675(MAX_SCK_PIN, MAX_CS_PIN, MAX_MISO_PIN);

QueueHandle_t counterQueue;
QueueHandle_t tempQueue;
SemaphoreHandle_t startSignal;
QueueHandle_t commandQueue;

TaskHandle_t h_task_Encoder;
TaskHandle_t h_task_LCD_Display;
TaskHandle_t h_task_ButtonReader;
TaskHandle_t h_task_Control_PID;
TaskHandle_t h_task_SensorReader;
TaskHandle_t h_task_SerialReader;
TaskHandle_t h_task_CommandHandler;
TaskHandle_t h_task_SerialWatchdog;
TaskHandle_t h_task_Control_SSR;

// Variable global para almacenar el valor inicial
volatile int g_currentSetpoint = 0;
volatile float g_actualTemp = 0.0;
volatile bool g_isRunning = false;
volatile bool g_isRunning_SSR = false;
volatile int g_controlSource = 0;
volatile int g_soakTime = 0;
volatile int g_rampRate = 0;
volatile int g_controlMode = 0;
volatile int g_fixPower = 0;
volatile unsigned long g_lastSerialTime = 0;
volatile unsigned long timeInCycle_ms = 0;
volatile unsigned long on_time_ms = 0;
volatile unsigned long currentTime_ms = 0;
volatile unsigned long cycleStartTime_ms = 0;

// Constantes de sintonia PID
float Kp = 0.252;
float Ki = 0.0367;
float Kd = 0.432;

// Tolerancia para llegar al setpoint
const float SETPOINT_TOLERANCE = 2.0;
const unsigned long SERIAL_TIMEOUT_MS = 5000;

// Ciclo de control (200 ms)
const int PID_CYCLE_TIME_MS = 1000;

// Tarea 1. Monitorear el Encoder
void task_Encoder(void *pvParameters) {

  int oldCounterValue = g_currentSetpoint;
  int newCounterValue = g_currentSetpoint;

  // Definimos los limies
  const int MIN_COUNT = 0;
  const int MAX_COUNT = 1000;

  TickType_t xLastWakeTime = xTaskGetTickCount();
  // Frecuencia de revision. 100ms es un buen balance
  const TickType_t xFrequency = pdMS_TO_TICKS(100);

  for(;;) {
    if (g_controlSource == 0) {
      if (!g_isRunning){ 
        // 1. Obtener el valor actual del hardware PCNT
        newCounterValue = encoder.getCount();
        bool valorCambiado = false;

        // 2. Aplicando limites 
        if(newCounterValue > MAX_COUNT) {
          newCounterValue = MAX_COUNT;
          encoder.setCount(MAX_COUNT);
        } else if (newCounterValue < MIN_COUNT) {
          newCounterValue = MIN_COUNT;
          encoder.setCount(MIN_COUNT);
        }
        // 3. Hubo un cambio?
        if(newCounterValue != oldCounterValue) {
          // 4. Si hubo cambio, enviar el nuevo valor a la cola
          xQueueSend(counterQueue, &newCounterValue, pdMS_TO_TICKS(10));
          // 5. Guarda el valor en la memoria flash
          preferences.putInt(NVS_KEY_SETPOINT, newCounterValue);
          // 6. Actualizar el valor antiguo
          oldCounterValue = newCounterValue;
        }
      } else {
        encoder.setCount(oldCounterValue);
      }
    } else {
      encoder.setCount(g_currentSetpoint);
    }
    // 7. Poner la tarea a dormir hasta el proximo ciclo de revision
    vTaskDelayUntil(&xLastWakeTime, xFrequency)
  }
}

// Tarea 2. Mostrar por pantalla LCD
void task_LCD_Display(void *pvParameters) {
  long setpointToShow = g_currentSetpoint;
  float tempToShow = g_actualTemp;
  char lcdBuffer[17];
  // Para que la tarea despierte periodicamente
  const TickType_t xFrequency = pdMS_TO_TICKS(250);

  for (;;) {
    // 1. Espera hasta que un valor llega a la cola
    if (xQueueReceive(counterQueue, &setpointToShow, xFrequency) == pdPASS) {
      // 2. Desperto. Recibimos un nuevo valor
        g_currentSetpoint = setpointToShow;
    }

    float newTemp;
    if (xQueueReceive(tempQueue, &newTemp, 0) == pdPASS) {
      tempToShow = newTemp;
      g_actualTemp = newTemp;
    }
    // Formatea el string para la LCD
    lcd.setCursor(0, 0);
    sprintf(lcdBuffer, "Set: %4ld C", g_currentSetpoint);
    lcd.print(lcdBuffer);
    
    
    if (g_isRunning) {
      lcd.setCursor(12, 0);
      lcd.print("ON  ");
    } else {
      lcd.setCursor(12, 0);
      lcd.print("IDLE");
    }

    // Temperatura actual
    lcd.setCursor(0, 1);
    if (tempToShow < 0) {
      sprintf(lcdBuffer, "Act: --ERROR--");
    } else {
      sprintf(lcdBuffer, "Act: %4.1f C", tempToShow);
    }
    lcd.print(lcdBuffer);
  }
}

// Tarea 3. Leer el boton de inicio
void task_ButtonReader(void *pvParameters) {
  
  bool lastStartState = HIGH;
  bool lastStopState = HIGH;

  TickType_t xLastWakeTime = xTaskGetTickCount();
  const TickType_t xFrequency = pdMS_TO_TICKS(50);

  for (;;){
    if (g_controlSource == 0){ 
      bool currentStartState = digitalRead(BUTTON_START_PIN);
      bool currentStopState = digitalRead(BUTTON_STOP_PIN);

      // Logica del boton de inicio
      if (currentStartState == LOW && lastStartState == HIGH) {
        // Antirrebote simple: esperar un poco y confirmar
        vTaskDelay(pdMS_TO_TICKS(50));
        if (digitalRead(BUTTON_START_PIN) == LOW) {
          if (!g_isRunning) {
            g_isRunning = true;
            digitalWrite(LED_ON, HIGH);
            digitalWrite(LED_OFF, LOW);
            xSemaphoreGive(startSignal);
          }
        }
      }
      lastStartState = currentStartState;

      // Logica para el boton detener
      if (currentStopState == LOW && lastStopState == HIGH) {
        vTaskDelay(pdMS_TO_TICKS(50));
        if (digitalRead(BUTTON_STOP_PIN) == LOW) {
          if (g_isRunning) {
            g_isRunning = false;
            g_isRunning_SSR = false;
            digitalWrite(LED_OFF, HIGH);
            digitalWrite(LED_ON, LOW);
            digitalWrite(SSR_PIN, LOW);
          }
        }
      }
      lastStopState = currentStopState;
    }
    vTaskDelayUntil(&xLastWakeTime, xFrequency);
  }
}

// Tarea 4. Control principal PID
void task_Control_PID(void *pvParameteres) {

  // Variables de estado del PID
  float error_integral = 0.0;
  float error_anterior = 0.0;
  float setpoint_pid_k; // El setpoint que el PID persigue

  // Variables de estado del perfil
  float currentRampSP_K;
  unsigned long soakTimerStart_ms;
  int profileStep;

  float dt_s = (float)PID_CYCLE_TIME_MS / 1000.0; // Tiempo del ciclo en segundos

  // Helpers para conversion
  auto C_para_k = [](float C){return C + 273.15; };
  float last_pid_output = 0.0;
  
  for (;;) {
    // Estado IDLE
    xSemaphoreTake(startSignal, portMAX_DELAY);
    
    // Inicial variables para este nuevo ciclo
    float setpoint_K = (float)g_currentSetpoint + 273.15;
    float rampRate_K_s = (float)g_rampRate/60;
    unsigned long soakDuration_ms = (unsigned long)g_soakTime * 60 * 1000;

    // EL PID y la Rampa siempre empiezan desde la Temp. Actual
    float temp_actual_k = C_para_k(g_actualTemp);
    currentRampSP_K = temp_actual_k;
    setpoint_pid_k = temp_actual_k;

    profileStep = 0;  // 0=rampa (o calentando), 1=meseta
    
    float error_k = 0.0;     // Error actual (e[k])
    float error_k1 = 0.0;    // Error del ciclo anterior (e[k-1])
    float error_k2 = 0.0;    // Error de hace dos ciclos (e[k-2])
    float output_k1 = 0.0;   // Salida del ciclo anterior (MV[k-1])
    float output_k = 0.0;    // Salida calculada para este ciclo (MV[k])

    // Variables para el control del SSR
    last_pid_output = 0.0;
    //cycleStartTime_ms = millis(); // Iniciar el primer ciclo del SSR

    // Bucle de control
    while(g_isRunning) {

      // Leer la temperatura actual
      temp_actual_k = C_para_k(g_actualTemp);

      // Inicio maquina de estados del perfil
      // Modo 0: Solo ir al setpoint y quedarse ahi
      if (g_controlMode == 0) {
        setpoint_pid_k = setpoint_K;
        // El ciclo nunca termina, solo espera el boton STOP
      } // Modo 1: (Paso + Meseta)
      else if(g_controlMode == 1){
        setpoint_pid_k = setpoint_K;
        if (profileStep == 0) { // 0 Calentando
          if (abs(temp_actual_k - setpoint_K) < SETPOINT_TOLERANCE) {
            // Paso mas meseta
            profileStep = 1;  // Mueve a meseta
            soakTimerStart_ms = millis();
          }
        } else {  // 1 En pausa
          if (millis() - soakTimerStart_ms > soakDuration_ms) {
            // Meseta terminada
            Serial.println("M1:END");
            g_isRunning = false;
          }
        }
      } // Modo 2: Rampa mas meseta
      else if (g_controlMode == 2) {
        if (profileStep == 0) { // 0 En rampa
          currentRampSP_K += rampRate_K_s * (PID_CYCLE_TIME_MS / 1000);
          if (currentRampSP_K > setpoint_K) {
            currentRampSP_K = setpoint_K;
          }
          setpoint_pid_k = currentRampSP_K; // El pid persigue la rampa

          if (abs(currentRampSP_K - setpoint_K) < 0.1 && 
          abs(temp_actual_k - setpoint_K) < SETPOINT_TOLERANCE) {
            profileStep = 1;
            soakTimerStart_ms = millis();
          }
        } else {  // 1 En meseta
          setpoint_pid_k = setpoint_K;  // mantener el SP
          if (millis() - soakTimerStart_ms > soakDuration_ms) {
            Serial.println("M2:END");
            g_isRunning = false;
          }
        }
      }
      // Fin maquina de estados

      // Calculo del PID
      // Comprobando si hay errores de lectura del sensor
      if (temp_actual_k < C_para_k(0)) {
        // Error de la termocupla, detenido el proceso
        g_isRunning = false;
      }

      if (g_controlMode == 3) { 
        // Ajuste de potencia fija
        on_time_ms = g_fixPower; 
        float power = g_fixPower / 500.0;
        char output_buffer[10];
        sprintf(output_buffer, "OU:%4.2f", power);
        Serial.println(output_buffer);
        //Serial.println(output_buffer);
      } else {
        // Calculo del error
        error_k = setpoint_pid_k - temp_actual_k;
        // Calculo de terminos del pid
        float P_term = Kp * (error_k - error_k1);
        float I_term = Ki * dt_s * error_k;
        float D_term = (Kd / dt_s) * (error_k -2*error_k1 + error_k2);
        float delta_output = P_term + I_term + D_term;
        output_k = output_k1 + delta_output;

        // Control y saturación del SSR
        if (output_k > 1.0) {
          output_k = 1.0;
        } else if (output_k < 0.0) {
          output_k = 0.0;
        }
        char output_buffer[10];
        sprintf(output_buffer, "OU:%4.2f", output_k);
        Serial.println(output_buffer);
        last_pid_output = output_k/2;
        on_time_ms = (unsigned long)(last_pid_output * CONTROL_CYCLE_TIME_MS);
      }

      error_k2 = error_k1;
      error_k1 = error_k;
      output_k1 = output_k;

      g_isRunning_SSR = true;
      cycleStartTime_ms = millis();
;
       vTaskDelay(pdMS_TO_TICKS(1000));
    }
  }
}

// Tarea para controlar el SSR
void task_Control_SSR(void *pvParameters) {
  for(;;){
    currentTime_ms = millis();
    timeInCycle_ms = currentTime_ms - cycleStartTime_ms;

    if (g_isRunning_SSR) {
      if (timeInCycle_ms < on_time_ms) {
        digitalWrite(SSR_PIN, HIGH);
      } else {
        digitalWrite(SSR_PIN, LOW);
      }
    }
    vTaskDelay(pdMS_TO_TICKS(2));
  }
}

// Tarea 5. Leer el sensor de temperatura 
void task_SensorReader(void *pvParameters) {
  char lcdBuffer[17];
  TickType_t xLastWakeTime = xTaskGetTickCount();
  // El Max6675 tarda 0.22s en convertir. Leemos cada 1s.
  const TickType_t xFrequency = pdMS_TO_TICKS(1000);

  for (;;) {
    // Leer temperatura
    float tempC = max6675.readCelsius();
    // Comprobar si hay un error (NaN o 0)
    if (isnan(tempC)) {
      tempC = -1.0;
    }
    if (g_isRunning) {
      sprintf(lcdBuffer, "TP: %4.1f", tempC);
      Serial.println(lcdBuffer);
    } else {
      sprintf(lcdBuffer, "T: %4.1f", tempC);
      Serial.println(lcdBuffer);
    }

    // Enviar la temperatura o el error a la cola
    xQueueSend(tempQueue, &tempC, 0);
    // Esperar 1 segundo
    vTaskDelayUntil(&xLastWakeTime, xFrequency);
  }
}

// Tarea 6: Leer el puerto serie
void task_SerialReader(void *pvParameters) {
  static char cmdBuffer[MAX_CMD_LEN];
  static int cmdIndex = 0;
  char c;
  TickType_t xLastWakeTime = xTaskGetTickCount();
  for (;;) {
    while(Serial.available() > 0) {
      c = Serial.read();
      if (c == '\r') continue;
      if (c == '\n') {
        if (cmdIndex > 0) {
          cmdBuffer[cmdIndex] = '\0';
          xQueueSend(commandQueue, &cmdBuffer, pdMS_TO_TICKS(100));
          cmdIndex = 0;
        }
      } else if (cmdIndex < MAX_CMD_LEN - 1 ) {
        cmdBuffer[cmdIndex++] = c;
      }
    }
    vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(20));
  }
}

// Tarea 7: Interpretar comandos
void task_CommandHandler(void *pvParameters) {
  char cmd[MAX_CMD_LEN];
  for (;;) {
    if (xQueueReceive(commandQueue, &cmd, portMAX_DELAY) == pdPASS) {
      g_lastSerialTime = millis();

      // Logica de parseo
      if (strcmp(cmd, "START:1") == 0) {
        if (!g_isRunning) {
          g_isRunning = true;
          digitalWrite(LED_OFF, LOW);
          digitalWrite(LED_ON, HIGH);
          xSemaphoreGive(startSignal);
          Serial.println("START1:OK");
        } else {
          Serial.println("ERR:ALREADY RUNNING");
        }
      } else if(strcmp(cmd, "HM:UMSA") == 0) {
        Serial.println("HM:OK");
      } else if(strcmp(cmd, "BEAT") == 0){
        g_controlSource = 1;
      } else if (strcmp(cmd, "START:0") == 0) {
        if (g_isRunning) {
          g_isRunning = false;
          digitalWrite(LED_OFF, HIGH);
          digitalWrite(LED_ON, LOW);
          g_isRunning_SSR = false;
          digitalWrite(SSR_PIN, LOW);
          Serial.println("START0:OK");
        } else {
          Serial.println("ERR:ALREADY STOPPED");
        }
      } else if (strncmp(cmd, "SET_", 4) == 0) {
        if (g_isRunning) {
          Serial.println("ERR:RUNNING");
        } else {
          bool success = false;

          if (strncmp(cmd, "SET_SP:", 7) == 0) {
            g_currentSetpoint = atoi(cmd + 7);
            preferences.putLong(NVS_KEY_SETPOINT, g_currentSetpoint);
            Serial.println("SET_SP:OK");
          } else if (strncmp(cmd, "SET_SOAK:", 9) == 0) {
            g_soakTime = atoi(cmd + 9);
            Serial.println("SET_SOAK:OK");
          } else if (strncmp(cmd, "SET_RAMP:", 9) == 0) {
            g_rampRate = atoi(cmd + 9);
            Serial.println("SET_RAMP:OK");
          } else if (strncmp(cmd, "SET_PF:", 7) == 0) {
            g_fixPower = atof(cmd + 7);
            Serial.println("SET_PF:OK");
          } else if (strncmp(cmd, "SET_MODE:", 9) == 0) {
            g_controlMode = atoi(cmd + 9);
            Serial.println("SET_MODE:OK");
          } else if (strncmp(cmd, "SET_KP:", 7) == 0) {
            Kp = atof(cmd + 7);
          } else if (strncmp(cmd, "SET_KI:", 7) == 0) {
            Ki = atof(cmd + 7);
          } else if (strncmp(cmd, "SET_KD:", 7) == 0) {
            Kd = atof(cmd + 7);
            success = true;
          }

          if (success) Serial.println("SET_K:OK");
          success = false;
        }
      } else {
        Serial.println("ERR:UNKNOWN");
        limpiarSerialEntrada();
      }
    }
  }
}

void task_SerialWatchdog(void *pvParameters) {
  TickType_t xLastWakeTime = xTaskGetTickCount();
  const TickType_t xFrequency = pdMS_TO_TICKS(1000);

  for (;;) {
    if (g_controlSource == 1) {
      if (millis() - g_lastSerialTime > SERIAL_TIMEOUT_MS) {
        g_controlSource = 0;
        g_controlMode = 0;
        g_isRunning = false;
        g_isRunning_SSR = false;
        digitalWrite(LED_OFF, HIGH);
        digitalWrite(LED_ON, LOW);
        encoder.setCount(g_currentSetpoint);
      }
    }
    vTaskDelayUntil(&xLastWakeTime, xFrequency);
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  btStop();
  limpiarSerialEntrada();
  pinMode(BUTTON_START_PIN, INPUT);
  pinMode(BUTTON_STOP_PIN, INPUT);
  pinMode(SSR_PIN, OUTPUT);
  pinMode(LED_ON, OUTPUT);
  pinMode(LED_OFF, OUTPUT);
  digitalWrite(LED_OFF, HIGH);
  digitalWrite(LED_ON, LOW);
  g_isRunning = false;
  g_isRunning_SSR = false;

  g_actualTemp = max6675.readCelsius();

  // Abrimos nuestro namespace en modo lectura/escritura
  preferences.begin(NVS_NAMESPACE, false);
  g_currentSetpoint = preferences.getInt(NVS_KEY_SETPOINT, 0);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("LAB. MATERIALES");
  lcd.setCursor(6, 1);
  lcd.print("UMSA");
  delay(1000);
  lcd.clear();

  ESP32Encoder::useInternalWeakPullResistors = puType::up;
  encoder.attachFullQuad(ENCODER_DT, ENCODER_CLK);
  encoder.setCount(g_currentSetpoint);
  // 1. Crear la cola (Queue)
  counterQueue = xQueueCreate(5, sizeof(long));
  tempQueue = xQueueCreate(5, sizeof(float));
  startSignal = xSemaphoreCreateBinary();
  commandQueue = xQueueCreate(5, sizeof(char[MAX_CMD_LEN]));

  if(counterQueue == NULL || startSignal == NULL || tempQueue == NULL || commandQueue == NULL){
        Serial.println("Error al crear la colas/semaforos");
  }

  // 2. Crear la tarea del encoder
  xTaskCreatePinnedToCore(
    task_Encoder, "EncoderTask", 2048, NULL, 1, &h_task_Encoder, 0);

  xTaskCreatePinnedToCore(
    task_SensorReader, "SensorTask", 2048, NULL, 2, &h_task_SensorReader, 0);

  // 3. Crear la tarea del display (Core 1)
  xTaskCreatePinnedToCore(
    task_LCD_Display, "LCDDisplayTask", 4096, NULL, 2, &h_task_LCD_Display, 1);

  // 4.Crea tarea para el boton
  xTaskCreatePinnedToCore(
    task_ButtonReader, "ButtonTask", 2048, NULL, 2, &h_task_ButtonReader, 1);

  xTaskCreatePinnedToCore(
    task_Control_PID, "ControlPIDTask", 4096, NULL, 3, &h_task_Control_PID, 1);

  xTaskCreatePinnedToCore(
    task_SerialReader, "SerialRead", 4096, NULL, 3, &h_task_SerialReader, 1);

  xTaskCreatePinnedToCore(
    task_CommandHandler, "CmdHandle", 4096, NULL, 4, &h_task_CommandHandler, 1);

  xTaskCreatePinnedToCore(
    task_SerialWatchdog, "SerialWatchdog", 2048, NULL, 1, &h_task_SerialWatchdog, 0);
  
  xTaskCreatePinnedToCore(
    task_Control_SSR, "ControlSSRTask", 2048, NULL, 4, &h_task_Control_SSR, 0);

  vTaskDelete(NULL);
}

void loop() {
}

void limpiarSerialEntrada() {
    // Mientras haya bytes en el búfer de entrada...
    while (Serial.available() > 0) {
        Serial.read(); // Lee el byte y lo descarta
    }
}

