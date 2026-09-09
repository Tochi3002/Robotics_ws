import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class VelocityPublisher(Node):

    def __init__(self):
        # Inicializamos el nodo con el nombre 'velocity_publisher'
        super().__init__('velocity_publisher')

        # Creamos un publicador que envía mensajes al tópico '/velocity'
        # Usamos mensajes de tipo Float32 (números decimales)
        # El '10' es el tamaño de la cola de mensajes pendientes
        self.publisher_ = self.create_publisher(
            Float32,
            '/velocity',
            10
        )

        # Variable que guarda el valor actual de velocidad
        self.Vel = 0.0

        # Creamos un temporizador que llama a publish_velocity()
        # cada 0.5 segundos automáticamente
        self.timer_ = self.create_timer(
            0.5,
            self.publish_velocity
        )

    def publish_velocity(self):
        # Creamos el mensaje y le asignamos el valor actual de velocidad
        msg = Float32()
        msg.data = self.Vel

        # Publicamos el mensaje al tópico '/velocity'
        self.publisher_.publish(msg)

        # Mostramos en consola el valor que se está publicando
        self.get_logger().info(f'Vel = {self.Vel:.1f}')

        # Si la velocidad es menor a 1.5, la aumentamos de 0.1 en 0.1
        # Si ya llegó a 1.5, la reiniciamos a 0.0
        if self.Vel < 1.5:
            self.Vel = round(self.Vel + 0.1, 1)
        else:
            self.Vel = 0.0


def main(args=None):
    rclpy.init(args=args)

    node = VelocityPublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
