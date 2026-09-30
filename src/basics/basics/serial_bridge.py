import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial


class SerialBridge(Node):
    def __init__(self):
        # Inicializamos el nodo con el nombre 'serial_bridge'
        super().__init__('serial_bridge')

        # Creamos un suscriptor que escucha el topico '/led_command'
        # Cada vez que llega un mensaje, se ejecuta led_callback
        self.subscription_ = self.create_subscription(Int32, '/led_command', self.led_callback, 10)

        # Abrimos la conexion serial con el ESP32 (puerto, baudrate y timeout)
        self.serial_ = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

        self.get_logger().info('Esperando mensajes')

    def led_callback(self, msg):
        # Si el mensaje recibido es 1, mandamos el caracter '1' por serial
        # para que el ESP32 encienda el LED
        if msg.data == 1:
            self.serial_.write(b'1\n')
            self.get_logger().info('ROS 2 -> Serial: 1')

        # Si el mensaje recibido es 0, mandamos el caracter '0' por serial
        # para que el ESP32 apague el LED
        elif msg.data == 0:
            self.serial_.write(b'0\n')
            self.get_logger().info('ROS 2 -> Serial: 0')


def main(args=None):
    rclpy.init(args=args)
    node = SerialBridge()
    rclpy.spin(node)
    node.serial_.close()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
