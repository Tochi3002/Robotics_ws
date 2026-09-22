// Pin donde esta conectado el LED
#define LED 2

void setup() {
  // Configuramos el pin del LED como salida
  pinMode(LED, OUTPUT);

  // Iniciamos la comunicacion serial a 115200 baudios
  Serial.begin(115200);
}

void loop() {
  // Revisamos si llego algun dato por el puerto serial
  if (Serial.available() > 0) {
    // Leemos un solo caracter
    char dato = Serial.read();

    // Si el caracter es '1', encendemos el LED
    if (dato == '1') {
      digitalWrite(LED, HIGH);
    }

    // Si el caracter es '0', apagamos el LED
    if (dato == '0') {
      digitalWrite(LED, LOW);
    }
  }
}
