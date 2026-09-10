import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityTurtleSubscriber(Node):

    def __init__(self):
        # Inicializamos el nodo con el nombre 'velocity_turtle_subscriber'
        super().__init__('velocity_turtle_subscriber')

        # Creamos un suscriptor que escucha el tópico '/turtle1/cmd_vel'
        # Usamos mensajes de tipo Twist, igual que el publicador
        # El '10' es el tamaño de la cola de mensajes pendientes
        self.subscription_ = self.create_subscription(
            Twist,
            '/turtle1/cmd_vel',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        # Cada vez que llega un mensaje, mostramos en consola
        # la velocidad lineal en x que recibimos
        self.get_logger().info(f'Velocidad recibida: {msg.linear.x:.1f}')


def main(args=None):
    rclpy.init(args=args)

    node = VelocityTurtleSubscriber()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
