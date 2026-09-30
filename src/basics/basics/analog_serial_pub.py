import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial


class AnalogSerialPublisher(Node):
    def __init__(self):
        # Inicializamos el nodo con el nombre 'analog_serial_pub'
        super().__init__('analog_serial_pub')

        # Creamos un publicador que envia mensajes al topico '/analog'
        # Usamos mensajes de tipo Int32 (el valor leido del potenciometro)
        self.publisher_ = self.create_publisher(Int32, '/analog', 10)

        # Abrimos la conexion serial con el ESP32 (puerto, baudrate y timeout)
        self.serial_ = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

        # Creamos un temporizador que revisa el puerto serial cada 0.01 segundos
        self.timer_ = self.create_timer(0.01, self.read_serial)
        self.get_logger().info('ESP32 conectada')

    def read_serial(self):
        # Si hay datos esperando en el puerto serial, los leemos
        if self.serial_.in_waiting > 0:
            # Leemos una linea completa, la decodificamos de bytes a texto
            # y quitamos espacios/saltos de linea sobrantes
            linea = self.serial_.readline().decode().strip()

            # Si lo que llego son solo digitos, lo convertimos a numero
            # y lo publicamos al topico '/analog'
            if linea.isdigit():
                valor = int(linea)
                msg = Int32()
                msg.data = valor
                self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = AnalogSerialPublisher()
    rclpy.spin(node)
    node.serial_.close()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
