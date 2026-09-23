# Robotics_ws

**Alumno:** Axalli Lopez

## Descripcion
Practica de comunicacion entre nodos en ROS2 usando el patron publicador-subscriptor. Se implementaron dos nodos: uno que publica valores de velocidad y otro que los recibe y los muestra en consola.

## Funcionamiento

### velocity_publisher.py
Nodo que publica mensajes de tipo std_msgs/msg/Float32 al topico /velocity cada 0.5 segundos. El valor de velocidad aumenta de 0.1 en 0.1, empezando en 0.0, hasta llegar a 1.5, momento en el cual se reinicia a 0.0 y el ciclo se repite.

### velocity_subscriber.py
Nodo que se suscribe al topico /velocity y recibe los mensajes de tipo Float32 publicados por velocity_publisher.py. Cada vez que llega un mensaje nuevo, lo muestra en consola con el valor recibido.

## Comandos utilizados

Ejecutar el publicador: python3 velocity_publisher.py
Ejecutar el subscriptor (en otra terminal): python3 velocity_subscriber.py
Verificar los nodos activos: ros2 node list
Verificar los topicos activos: ros2 topic list
Ver informacion del topico: ros2 topic info /velocity
Visualizar el grafo de comunicacion: ros2 run rqt_graph rqt_graph


## Actividad 2: Publicador y subscriptor con turtlesim

### Descripcion breve
A partir de los scripts de la actividad anterior, se crearon dos nuevos nodos (velocity_turtle_pub.py y velocity_turtle_subs.py) para controlar y monitorear la velocidad de traslacion de la tortuga simulada de turtlesim.

### Modificaciones realizadas
Se copiaron velocity_publisher.py y velocity_subscriber.py con los nuevos nombres. En el publicador se cambio el tipo de mensaje de std_msgs/msg/Float32 a geometry_msgs/msg/Twist, y el topico de /velocity a /turtle1/cmd_vel, que es el topico que escucha turtlesim para mover a la tortuga. El incremento se cambio para ir de 0.0 a 1.2 en pasos de 0.1 cada 0.5 segundos, y en vez de reiniciar el ciclo, al llegar a 1.2 se publica un mensaje con velocidad 0.0 y el nodo deja de publicar, deteniendo a la tortuga. En el subscriptor solo se cambio el tipo de mensaje y el topico al que se suscribe, para que coincida con el nuevo publicador.

### Funcionamiento
velocity_turtle_pub.py publica mensajes tipo geometry_msgs/msg/Twist al topico /turtle1/cmd_vel, usando el campo linear.x para indicar la velocidad de traslacion de la tortuga. velocity_turtle_subs.py se suscribe al mismo topico y tipo de mensaje, y muestra en consola cada valor de velocidad recibido.

### Comandos utilizados
Ejecutar turtlesim: ros2 run turtlesim turtlesim_node
Ejecutar el publicador: python3 velocity_turtle_pub.py
Ejecutar el subscriptor (en otra terminal): python3 velocity_turtle_subs.py
Verificar los nodos activos: ros2 node list
Verificar los topicos activos: ros2 topic list
Ver informacion del topico: ros2 topic info /turtle1/cmd_vel
Visualizar el grafo de comunicacion: rqt_graph

### Problemas encontrados
No se presentaron problemas relevantes durante el desarrollo del codigo; la modificacion del publicador y el subscriptor funciono correctamente desde las primeras pruebas.

## Actividad 3: Comunicacion con ESP32 - Ejemplo LED

### Descripcion breve
Se agrego el paquete colmibot_firmware con el sketch LED_Serial.ino para el ESP32, y se probo la comunicacion entre ROS2 y el ESP32 usando los nodos led_blink.py y serial_bridge.py para encender y apagar un LED.

### Funcionamiento
LED_Serial.ino corre en el ESP32: configura el pin GPIO2 (LED integrado de la placa) como salida y escucha el puerto serial. Si recibe el caracter '1' enciende el LED, si recibe '0' lo apaga.

led_blink.py publica mensajes de tipo std_msgs/msg/Int32 al topico /led_command cada 1 segundo, alternando entre 1 y 0. serial_bridge.py se suscribe al topico /led_command y, por cada mensaje recibido, lo traduce a un caracter ('1' o '0') que envia por el puerto serial /dev/ttyUSB0 hacia el ESP32.

### Comandos utilizados
Subir el sketch al ESP32: se realizo desde Arduino IDE 2.3.10 seleccionando la tarjeta ESP32 Dev Module y el puerto /dev/ttyUSB0
Ejecutar el puente serial: python3 serial_bridge.py
Ejecutar el publicador (en otra terminal): python3 led_blink.py
Verificar los nodos activos: ros2 node list
Verificar los topicos activos: ros2 topic list
Ver informacion del topico: ros2 topic info /led_command
Visualizar el grafo de comunicacion: rqt_graph

### Problemas encontrados
Al instalar Arduino IDE en la maquina virtual, la aplicacion no abria por un error de sandbox de Electron; se soluciono ejecutando el AppImage con la bandera --no-sandbox. Tambien el puerto serial no era accesible por permisos; se soluciono agregando el usuario al grupo dialout con sudo usermod -a -G dialout $USER y reiniciando la sesion para que el cambio de grupo se aplicara.


## Actividad 4: Comunicacion con ESP32 - Ejemplo Potenciometro

### Descripcion breve
Se probo la comunicacion entre ROS2 y el ESP32 usando el sketch ADC_Pot.ino junto con los nodos analog_serial_pub.py y analog_subs.py, para leer el valor de un potenciometro conectado al ESP32 mediante una protoboard.

### Funcionamiento
ADC_Pot.ino corre en el ESP32: lee el valor analogico del pin GPIO15 (donde esta conectada la pata central del potenciometro) y lo envia por el puerto serial cada 100 milisegundos, como un numero entre 0 y 4095.

analog_serial_pub.py lee el puerto serial /dev/ttyUSB0, toma cada valor recibido del ESP32 y lo publica como un mensaje de tipo std_msgs/msg/Int32 al topico /analog. analog_subs.py se suscribe al topico /analog y muestra en consola cada valor recibido.

### Comandos utilizados
Subir el sketch al ESP32: se realizo desde Arduino IDE 2.3.10 seleccionando la tarjeta ESP32 Dev Module y el puerto /dev/ttyUSB0
Ejecutar el publicador: python3 analog_serial_pub.py
Ejecutar el subscriptor (en otra terminal): python3 analog_subs.py
Verificar los nodos activos: ros2 node list
Verificar los topicos activos: ros2 topic list
Ver informacion del topico: ros2 topic info /analog
Visualizar el grafo de comunicacion: rqt_graph

### Problemas encontrados
Al hacer la primera prueba con el potenciometro, el valor leido se mantenia practicamente fijo; se debia a que la perilla del potenciometro no estaba siendo girada, no a un problema real del circuito ni del codigo. Al girar la perilla, el valor cambio correctamente entre 0 y 4095.
