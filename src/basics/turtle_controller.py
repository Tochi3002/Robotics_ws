import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point


class TurtleController(Node):
    def __init__(self):
        # Inicializamos el nodo con el nombre 'turtle_controller'
        super().__init__('turtle_controller')

        # Nos suscribimos al topico '/joystick_raw' para recibir
        # los valores crudos del joystick publicados por joystick_pub.py
        self.subscription_ = self.create_subscription(
            Point,
            '/joystick_raw',
            self.joystick_callback,
            10
        )
        self.get_logger().info('Esperando datos del joystick')

    def joystick_callback(self, msg):
        # Por ahora solo mostramos en consola lo que recibimos,
        # para comprobar que la comunicacion funciona correctamente
        self.get_logger().info(f'Recibido: x={msg.x}, y={msg.y}')


def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
