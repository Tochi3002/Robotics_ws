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

