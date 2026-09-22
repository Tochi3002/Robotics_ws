import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class LedBlink(Node):
    def __init__(self):
        # Inicializamos el nodo con el nombre 'led_blink'
        super().__init__('led_blink')

        # Creamos un publicador que envia mensajes al topico '/led_command'
        # Usamos mensajes de tipo Int32 (numeros enteros: 1 = encendido, 0 = apagado)
        self.publisher_ = self.create_publisher(Int32, '/led_command', 10)

        # Variable que guarda el estado actual del LED (arranca encendido)
        self.estado = 1

        # Creamos un temporizador que llama a blink_callback() cada 1 segundo
        self.timer_ = self.create_timer(1.0, self.blink_callback)
        self.get_logger().info('Nodo iniciado')

        # Publicamos el estado inicial antes de que empiece el temporizador
        self.publicar_estado()

    def blink_callback(self):
        # Invertimos el estado del LED cada vez que se llama esta funcion
        if self.estado == 1:
            self.estado = 0
        else:
            self.estado = 1

        self.publicar_estado()

    def publicar_estado(self):
        # Creamos el mensaje y le asignamos el estado actual
        msg = Int32()
        msg.data = self.estado

        # Publicamos el mensaje al topico '/led_command'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publicando: {self.estado}')


def main(args=None):
    rclpy.init(args=args)
    node = LedBlink()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
