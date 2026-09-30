// Pines donde estan conectados los ejes del joystick (entradas analogicas)
#define VRX 34
#define VRY 35

void setup() {
  // Iniciamos la comunicacion serial a 115200 baudios
  Serial.begin(115200);
}

void loop() {
  // Leemos el valor analogico de cada eje (0 a 4095 en ESP32)
  int valorX = analogRead(VRX);
  int valorY = analogRead(VRY);

  // Enviamos ambos valores en una sola linea, separados por una coma
  // para que el nodo de Python los pueda separar facilmente
  Serial.print(valorX);
  Serial.print(",");
  Serial.println(valorY);

  // Esperamos 50 milisegundos antes de la siguiente lectura
  delay(50);
}
