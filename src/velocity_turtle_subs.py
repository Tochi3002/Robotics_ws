import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class VelocitySubscriber(Node):

    def __init__(self):
        # Inicializamos el nodo con el nombre 'velocity_subscriber'
        super().__init__('velocity_subscriber')

        # Creamos un subscriptor que escucha el tópico '/velocity'
        # Recibe mensajes de tipo Float32 (igual que el publicador)
        # El '10' es el tamaño de la cola de mensajes pendientes
        self.subscription = self.create_subscription(
            Float32,
            '/velocity',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        # Esta función se ejecuta automáticamente cada vez que
        # llega un mensaje nuevo al tópico '/velocity'
        self.get_logger().info(f'Velocidad recibida: {msg.data:.1f}')


def main(args=None):
    rclpy.init(args=args)

    node = VelocitySubscriber()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
