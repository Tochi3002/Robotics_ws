import serial

# Puerto y velocidad de comunicacion con el ESP32
PORT = '/dev/ttyUSB0'
BAUDRATE = 115200

# Abrimos la conexion serial
esp32 = serial.Serial(PORT, BAUDRATE, timeout=1)

while True:
    # Leemos una linea completa del puerto serial y la decodificamos a texto
    linea = esp32.readline().decode().strip()

    if linea:
        # Mostramos en consola el valor recibido del potenciometro
        print(f'ADC = {linea}')
