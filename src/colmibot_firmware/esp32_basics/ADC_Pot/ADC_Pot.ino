// Pin donde esta conectado el potenciometro (entrada analogica)
#define POT 15

void setup() {
  // Iniciamos la comunicacion serial a 115200 baudios
  Serial.begin(115200);
}

void loop() {
  // Leemos el valor analogico del potenciometro (0 a 4095 en ESP32)
  int valor = analogRead(POT);

  // Enviamos el valor leido por el puerto serial
  Serial.println(valor);

  // Esperamos 100 milisegundos antes de la siguiente lectura
  delay(100);
}
