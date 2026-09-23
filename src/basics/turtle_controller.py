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

        # Bandera y variables para calibrar el centro real del joystick
        # la primera vez que llega un dato, en vez de asumir 2048 fijo
        self.calibrado = False
        self.centro_x = 2048.0
        self.centro_y = 2048.0

        # Zona muerta: porcentaje del rango total que ignoramos alrededor
        # del centro, para que el ruido natural del sensor no mueva la tortuga
        # cuando el joystick esta soltado. 5% es suficiente para cubrir el
        # ruido que se observo en las pruebas (variaciones de +-15 unidades
        # sobre un rango de 4095), sin hacer la zona muerta demasiado grande
        self.zona_muerta = 0.05

        # Velocidades maximas: se eligieron tras varias pruebas en turtlesim.
        # Con estos valores la tortuga se mueve de forma clara y controlable
        # dentro de la ventana de turtlesim (~11x11 unidades) sin salirse
        # de cuadro de inmediato ni moverse demasiado lento para notarlo
        self.vel_lineal_max = 2.0
        self.vel_angular_max = 2.0

        self.get_logger().info('Controlador de tortuga iniciado, calibrando centro...')

    def normalizar(self, valor, centro):
        # Convertimos el valor crudo (0 a 4095) a un rango de -1.0 a 1.0
        # usando el centro real detectado, no un centro teorico fijo
        rango = 2048.0
        normalizado = (valor - centro) / rango

        # Limitamos el resultado entre -1.0 y 1.0 por si el centro
        # detectado hace que el calculo se pase un poco de esos limites
        return max(-1.0, min(1.0, normalizado))

    def aplicar_zona_muerta(self, valor):
        # Si el valor normalizado esta muy cerca de 0 (dentro de la zona
        # muerta), lo forzamos a 0 para que la tortuga quede quieta
        if abs(valor) < self.zona_muerta:
            return 0.0
        return valor

    def joystick_callback(self, msg):
        # La primera vez que recibimos un dato, lo usamos como centro real
        # del joystick (calibracion automatica al iniciar el nodo)
        if not self.calibrado:
            self.centro_x = msg.x
            self.centro_y = msg.y
            self.calibrado = True
            self.get_logger().info(f'Centro calibrado: x={self.centro_x}, y={self.centro_y}')
            return

        # Normalizamos ambos ejes usando el centro real calibrado
        normalizado_x = self.normalizar(msg.x, self.centro_x)
        normalizado_y = self.normalizar(msg.y, self.centro_y)

        # Aplicamos la zona muerta a ambos ejes
        normalizado_x = self.aplicar_zona_muerta(normalizado_x)
        normalizado_y = self.aplicar_zona_muerta(normalizado_y)

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
