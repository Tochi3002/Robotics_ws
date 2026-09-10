import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityTurtlePublisher(Node):

    def __init__(self):
        # Inicializamos el nodo con el nombre 'velocity_turtle_publisher'
        super().__init__('velocity_turtle_publisher')

        # Creamos un publicador que envía mensajes al tópico '/turtle1/cmd_vel'
        # Usamos mensajes de tipo Twist, que es el tipo que entiende turtlesim
        # para mover a la tortuga (tiene velocidad lineal y angular)
        # El '10' es el tamaño de la cola de mensajes pendientes
        self.publisher_ = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # Variable que guarda el valor actual de velocidad translacional
        self.Vel = 0.0

        # Bandera para saber si ya llegamos al límite y la tortuga debe detenerse
        self.detenido = False

        # Creamos un temporizador que llama a publish_velocity()
        # cada 0.5 segundos automáticamente
        self.timer_ = self.create_timer(
            0.5,
            self.publish_velocity
        )

    def publish_velocity(self):
        # Si ya mandamos la orden de detenerse, ya no hacemos nada más
        if self.detenido:
            return

        # Creamos el mensaje Twist y le asignamos la velocidad lineal en x
        msg = Twist()
        msg.linear.x = self.Vel

        # Publicamos el mensaje al tópico '/turtle1/cmd_vel'
        self.publisher_.publish(msg)

        # Mostramos en consola el valor que se está publicando
        self.get_logger().info(f'Vel = {self.Vel:.1f}')

        # Si la velocidad es menor a 1.2, la aumentamos de 0.1 en 0.1
        if self.Vel < 1.2:
            self.Vel = round(self.Vel + 0.1, 1)
        else:
            # Ya llegamos a 1.2: mandamos una orden extra con velocidad 0
            # para que la tortuga se detenga por completo
            self.get_logger().info('Velocidad maxima alcanzada, deteniendo tortuga')
            stop_msg = Twist()
            stop_msg.linear.x = 0.0
            self.publisher_.publish(stop_msg)
            self.detenido = True


def main(args=None):
    rclpy.init(args=args)

    node = VelocityTurtlePublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
