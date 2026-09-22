import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class AnalogSubscriber(Node):
    def __init__(self):
        # Inicializamos el nodo con el nombre 'analog_subscriber'
        super().__init__('analog_subscriber')

        # Creamos un suscriptor que escucha el topico '/analog'
        # Cada vez que llega un mensaje, se ejecuta analog_callback
        self.subscription_ = self.create_subscription(Int32, '/analog', self.analog_callback, 10)
        self.get_logger().info('Esperando datos')

    def analog_callback(self, msg):
        # Extraemos el valor del mensaje recibido y lo mostramos en consola
        valor = msg.data
        self.get_logger().info(f'ADC = {valor}')

def main(args=None):
    rclpy.init(args=args)
    node = AnalogSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
