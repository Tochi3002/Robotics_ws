import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Twist


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

        # Creamos un publicador para mandarle velocidad a la tortuga
        # de turtlesim, usando el topico y tipo de mensaje que ella escucha
        self.cmd_vel_pub_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # Valor central teorico del ADC del ESP32 (rango 0 a 4095)
        self.centro = 2048.0

        # Velocidades maximas iniciales, sin ajustar todavia
        self.vel_lineal_max = 2.0
        self.vel_angular_max = 2.0

        self.get_logger().info('Controlador de tortuga iniciado')

    def joystick_callback(self, msg):
        # Convertimos el valor crudo del eje Y (0 a 4095) a un rango de -1.0 a 1.0
        # donde 0.0 representa el centro (joystick sin tocar)
        normalizado_y = (msg.y - self.centro) / self.centro

        # Convertimos el valor crudo del eje X de la misma forma
        normalizado_x = (msg.x - self.centro) / self.centro

        # La velocidad lineal (adelante/atras) depende del eje Y
        velocidad_lineal = normalizado_y * self.vel_lineal_max

        # La velocidad angular (giro) depende del eje X
        # Se invierte el signo para que mover el joystick a la derecha
        # gire la tortuga hacia la derecha
        velocidad_angular = -normalizado_x * self.vel_angular_max

        # Creamos el mensaje Twist y le asignamos las velocidades calculadas
        cmd = Twist()
        cmd.linear.x = velocidad_lineal
        cmd.angular.z = velocidad_angular

        # Publicamos el mensaje para mover la tortuga
        self.cmd_vel_pub_.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
