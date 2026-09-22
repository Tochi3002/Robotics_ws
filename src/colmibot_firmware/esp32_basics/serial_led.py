import serial
import time

# Puerto y velocidad de comunicacion con el ESP32
PORT = '/dev/ttyUSB0'
BAUDRATE = 115200

# Abrimos la conexion serial
esp32 = serial.Serial(PORT, BAUDRATE, timeout=1)

# Esperamos 2 segundos para que el ESP32 termine de reiniciar
# despues de abrir el puerto serial
time.sleep(2)

while True:
    # Pedimos al usuario que decida si encender, apagar o salir
    dato = input("Escribe 1 para encender, 0 para apagar, q para salir: ")

    if dato == '1':
        # Mandamos el caracter '1' al ESP32 para encender el LED
        esp32.write(b'1\n')

    elif dato == '0':
        # Mandamos el caracter '0' al ESP32 para apagar el LED
        esp32.write(b'0\n')

    elif dato == 'q':
        # Salimos del ciclo
        break

# Cerramos la conexion serial al terminar
esp32.close()
