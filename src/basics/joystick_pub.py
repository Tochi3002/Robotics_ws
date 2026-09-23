import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
import serial


class JoystickPublisher(Node):
    def __init__(self):
        # Inicializamos el nodo con el nombre 'joystick_pub'
        super().__init__('joystick_pub')

        # Creamos un publicador que envia mensajes al topico '/joystick_raw'
        # Usamos mensajes tipo Point (tiene campos x, y, z) para mandar
        # los dos valores crudos del joystick, sin convertir a velocidad todavia
        self.publisher_ = self.create_publisher(Point, '/joystick_raw', 10)

        # Abrimos la conexion serial con el ESP32 (puerto, baudrate y timeout)
        self.serial_ = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

        # Creamos un temporizador que revisa el puerto serial cada 0.02 segundos
        self.timer_ = self.create_timer(0.02, self.read_serial)
        self.get_logger().info('ESP32 conectada, esperando datos del joystick')

    def read_serial(self):
        # Si hay datos esperando en el puerto serial, los leemos
        if self.serial_.in_waiting > 0:
            # Leemos una linea completa, la decodificamos de bytes a texto
            # y quitamos espacios/saltos de linea sobrantes
            linea = self.serial_.readline().decode().strip()

            # La linea debe venir en formato "valorX,valorY"
            # Verificamos que tenga una coma para separarla en dos partes
            if ',' in linea:
                partes = linea.split(',')

                # Nos aseguramos de que ambas partes sean numeros validos
                if len(partes) == 2 and partes[0].strip().isdigit() and partes[1].strip().isdigit():
                    valor_x = int(partes[0].strip())
                    valor_y = int(partes[1].strip())

                    # Creamos el mensaje Point y le asignamos los valores leidos
                    msg = Point()
                    msg.x = float(valor_x)
                    msg.y = float(valor_y)
                    msg.z = 0.0

                    # Publicamos el mensaje al topico '/joystick_raw'
                    self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = JoystickPublisher()
    rclpy.spin(node)
    node.serial_.close()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
