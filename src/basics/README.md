# Robotics_ws

**Alumno:** Axalli Lopez

## Descripcion general del paquete basics
basics es un paquete de ROS2 Jazzy de tipo ament_python que reune los nodos desarrollados durante las sesiones guiadas del Seminario de Titulacion: comunicacion publicador-subscriptor, control de Turtlesim, comunicacion serial con una ESP32 (LED, potenciometro y joystick) y archivos launch para ejecutar varios nodos con un solo comando.

### Estructura del paquete
    basics/
      README.md, package.xml, setup.py, setup.cfg, resource/
      basics/        nodos de ROS2 en Python
      esp32_basics/  sketches de la ESP32 (ADC_Pot, LED_Serial, joystick) y scripts seriales de prueba
      launch/        velocity_system.launch.py y turtle_joy_controller.launch.py

### Compilar y ejecutar
    cd ~/robotics_ws
    colcon build --packages-select basics
    source install/setup.bash
    ros2 launch basics velocity_system.launch.py
    ros2 launch basics turtle_joy_controller.launch.py

En las actividades 1 a 5 los nodos se ejecutaban directamente con python3. A partir de la actividad 6 se registraron en console_scripts de setup.py los nodos que usan los archivos launch (velocity_publisher, velocity_subscriber, joystick_pub y turtle_controller). En la actividad 7 se reorganizo el repositorio para que src/basics contenga el paquete completo; el firmware que antes estaba en colmibot_firmware/esp32_basics ahora esta en basics/esp32_basics.

## Actividad 1: Publicador y subscriptor de velocidad

### Descripcion breve
Practica de comunicacion entre nodos en ROS2 usando el patron publicador-subscriptor. Se implementaron dos nodos: uno que publica valores de velocidad y otro que los recibe y los muestra en consola.

### Funcionamiento

#### velocity_publisher.py
Nodo que publica mensajes de tipo std_msgs/msg/Float32 al topico /velocity cada 0.5 segundos. El valor de velocidad aumenta de 0.1 en 0.1, empezando en 0.0, hasta llegar a 1.5, momento en el cual se reinicia a 0.0 y el ciclo se repite.

#### velocity_subscriber.py
Nodo que se suscribe al topico /velocity y recibe los mensajes de tipo Float32 publicados por velocity_publisher.py. Cada vez que llega un mensaje nuevo, lo muestra en consola con el valor recibido.

### Comandos utilizados

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

## Actividad 5: Control de Turtlesim con Joystick via ESP32

### Descripcion breve
Se integro un modulo joystick de dos ejes conectado a un ESP32 para controlar el movimiento de la tortuga en Turtlesim, usando tres componentes: el sketch joystick.ino, el nodo publicador joystick_pub.py y el nodo controlador turtle_controller.py.

### Que se genero
Se creo joystick.ino, que lee los dos ejes analogicos del joystick (X en GPIO34, Y en GPIO35) y los envia por serial en una sola linea separados por coma. Se creo joystick_pub.py, que lee esa linea del puerto serial, la separa en dos valores y los publica como mensaje Point al topico /joystick_raw. Se creo turtle_controller.py, que se suscribe a ese topico, convierte los valores crudos en velocidad lineal y angular, y publica un mensaje Twist al topico /turtle1/cmd_vel para mover la tortuga.

### Funcionamiento de los tres archivos

joystick.ino: nodo de firmware en el ESP32 (no es un nodo de ROS2). Lee analogRead() en los pines GPIO34 (eje X) y GPIO35 (eje Y), y envia ambos valores por Serial.println() cada 50 milisegundos en formato "valorX,valorY".

joystick_pub.py: nodo de ROS2 llamado joystick_pub. Lee el puerto serial /dev/ttyUSB0, separa la linea recibida por la coma y publica un mensaje de tipo geometry_msgs/msg/Point al topico /joystick_raw, usando los campos x e y del mensaje para los dos ejes del joystick. Este nodo no envia nada a Turtlesim directamente.

turtle_controller.py: nodo de ROS2 llamado turtle_controller. Se suscribe al topico /joystick_raw (mensaje Point) publicado por joystick_pub.py. En la primera lectura recibida, guarda esos valores como el centro real del joystick (calibracion automatica). En cada lectura posterior, normaliza los valores de X y Y a un rango de -1.0 a 1.0 respecto a ese centro, aplica una zona muerta del 5% para ignorar el ruido cuando el joystick esta soltado, y multiplica el resultado por las velocidades maximas para obtener la velocidad lineal (eje Y) y angular (eje X). Publica un mensaje geometry_msgs/msg/Twist al topico /turtle1/cmd_vel para mover la tortuga.

### Limites de velocidad
Se establecieron vel_lineal_max = 2.0 y vel_angular_max = 2.0 tras probar varios valores en Turtlesim. Con estos, la tortuga se mueve de forma clara y controlable dentro de la ventana de Turtlesim (aproximadamente 11x11 unidades), sin salirse de cuadro casi de inmediato como ocurria con valores mas altos, ni moverse demasiado lento para notar el control proporcional.

### Zona muerta
Se eligio un 5% del rango normalizado (equivalente a unas 100 unidades del rango crudo de 0 a 4095) como zona muerta, ya que en las pruebas el joystick sin tocar mostraba variaciones de ruido de hasta +-15 unidades sobre su centro real; un 5% cubre ese ruido con margen sin hacer la zona muerta tan grande que reduzca notablemente el rango util de movimiento.

### Comandos utilizados
Subir el sketch al ESP32: se realizo desde Arduino IDE 2.3.10 seleccionando la tarjeta ESP32 Dev Module y el puerto /dev/ttyUSB0
Ejecutar turtlesim: ros2 run turtlesim turtlesim_node
Ejecutar el publicador del joystick: python3 joystick_pub.py
Ejecutar el controlador (en otra terminal): python3 turtle_controller.py
Verificar los nodos activos: ros2 node list
Verificar los topicos activos: ros2 topic list
Ver informacion del topico: ros2 topic info /joystick_raw
Visualizar el grafo de comunicacion: rqt_graph

### Problemas encontrados
Al usar el Monitor Serial de Arduino IDE para probar el joystick, la velocidad de comunicacion (baud rate) configurada por defecto no coincidia con la usada en el codigo (9600 en vez de 115200), lo que mostraba texto ilegible; se soluciono cambiando el baud rate del monitor a 115200.

En la primera version de turtle_controller.py se uso un valor central teorico fijo (2048) para normalizar las lecturas del joystick, lo que causaba que la tortuga se moviera sola aun con el joystick sin tocar, ya que el centro real de este joystick especifico es distinto (aproximadamente x=1883, y=1934). Se soluciono agregando una calibracion automatica: el nodo toma la primera lectura recibida al iniciar como su centro de referencia, y ademas se agrego una zona muerta del 5% para filtrar el ruido natural del sensor.

### Asignacion de pines de la ESP32
GPIO34: entrada analogica, eje X del joystick (VRx)
GPIO35: entrada analogica, eje Y del joystick (VRy)

## Actividad 6: Archivo launch para el sistema de velocidad

### Descripcion breve
Se creo el archivo velocity_system.launch.py, que ejecuta los nodos velocity_publisher y velocity_subscriber al mismo tiempo desde una sola terminal con el comando ros2 launch, en lugar de abrir una terminal para cada nodo como se hacia en la primera actividad.

### Que se genero
Siguiendo la presentacion 4-Launch, se creo la carpeta launch dentro del paquete basics del workspace robotics_ws y en ella el archivo velocity_system.launch.py (en este repositorio se encuentra en src/basics/launch). Tambien se modifico el setup.py del paquete en dos partes: en data_files se agrego la ruta del archivo launch para que se instale al compilar, y en console_scripts se registraron velocity_publisher y velocity_subscriber para que ROS2 pueda encontrarlos por nombre.

### Funcionamiento
velocity_system.launch.py define la funcion generate_launch_description(), que regresa un LaunchDescription con dos Node. Cada Node indica el paquete (basics) y el nombre del ejecutable registrado en setup.py, y usa output='screen' para que los mensajes de ambos nodos se vean en la misma terminal. Al ejecutarlo, velocity_publisher publica un mensaje Float32 en el topico /velocity cada 0.5 segundos, aumentando la velocidad de 0.0 a 1.5 m/s y reiniciando en 0.0, y velocity_subscriber recibe cada valor y lo imprime.

### Comprobacion
Con el launch en ejecucion, en otra terminal se verifico lo siguiente:
- ros2 node list mostro los nodos /velocity_publisher y /velocity_subscriber.
- ros2 topic list mostro el topico /velocity.
- ros2 topic info /velocity mostro el tipo std_msgs/msg/Float32 con 1 publisher y 1 subscriber.
- rqt_graph, en modo Nodes/Topics (all), mostro la conexion velocity_publisher -> /velocity -> velocity_subscriber.

### Comandos utilizados
Compilar el paquete: colcon build --packages-select basics
Cargar el workspace: source install/setup.bash
Verificar los ejecutables registrados: ros2 pkg executables basics
Ejecutar el launch: ros2 launch basics velocity_system.launch.py
Verificar los nodos activos: ros2 node list
Verificar los topicos activos: ros2 topic list
Ver informacion del topico: ros2 topic info /velocity
Ver un mensaje del topico: ros2 topic echo /velocity --once
Visualizar el grafo de comunicacion: rqt_graph

### Problemas encontrados
En las actividades anteriores los nodos se ejecutaban con python3, por lo que la seccion console_scripts de setup.py estaba vacia. El launch busca los nodos por nombre, asi que fue necesario registrarlos en console_scripts antes de compilar.

La primera vez que se ejecuto ros2 topic list no aparecia /velocity y ros2 topic info /velocity respondia Unknown topic, aunque ros2 topic echo si recibia mensajes y rqt_graph si mostraba el topico. Al repetir los comandos unos segundos despues el topico ya aparecia; esto se debe a que el daemon de ROS2 apenas estaba iniciando y todavia no descubria el topico.

Al detener el launch con Ctrl+C aparecen mensajes KeyboardInterrupt y process has died con exit code -2. Esto es la interrupcion enviada con Ctrl+C y no una falla del launch.

### Video
Evidencia de la ejecucion del launch y su comprobacion: [Ver video en Google Drive](https://drive.google.com/file/d/1bPA1DMds35-zMymm6oaXHYXsHtUVBufa/view?usp=sharing)

## Actividad 7: Launch del control de Turtlesim con joystick y reestructura del paquete

### Descripcion breve
Se creo el archivo turtle_joy_controller.launch.py, que ejecuta con un solo comando los tres nodos de la actividad del joystick: turtlesim_node, joystick_pub y turtle_controller. Ademas se reorganizo el repositorio para que src/basics contenga el paquete completo de ROS2.

### Que se genero
Se creo turtle_joy_controller.launch.py en la carpeta launch del paquete. En setup.py se agrego este archivo en data_files y se registraron joystick_pub y turtle_controller en console_scripts para que el launch pueda encontrarlos por nombre.

### Conexion del joystick con la ESP32
VRx del joystick a D34 (GPIO34), eje X
VRy del joystick a D35 (GPIO35), eje Y
+5V del joystick a 3V3 de la ESP32
GND del joystick a GND de la ESP32
SW sin conectar

### Funcionamiento
El launch define tres Node. El primero es turtlesim_node del paquete turtlesim, que abre la ventana con la tortuga. El segundo es joystick_pub, que lee del puerto /dev/ttyUSB0 los valores del joystick enviados por la ESP32 y los publica como geometry_msgs/msg/Point en el topico /joystick_raw. El tercero es turtle_controller, que se suscribe a /joystick_raw, toma la primera lectura como centro del joystick (en la prueba quedo en x=1890, y=1936), convierte las lecturas en velocidad lineal y angular, y publica geometry_msgs/msg/Twist en /turtle1/cmd_vel para mover la tortuga. Por la calibracion automatica, el joystick debe estar sin tocar al iniciar el launch.

### Comprobacion
Con el launch en ejecucion, en otra terminal se verifico lo siguiente:
- ros2 node list mostro /joystick_pub, /turtle_controller y /turtlesim.
- ros2 topic info /joystick_raw mostro el tipo geometry_msgs/msg/Point con 1 publisher y 1 subscriber.
- ros2 topic info /turtle1/cmd_vel mostro el tipo geometry_msgs/msg/Twist con 1 publisher y 1 subscriber.
- rqt_graph, en modo Nodes/Topics (all), mostro la cadena /joystick_pub -> /joystick_raw -> /turtle_controller -> /turtle1/cmd_vel -> /turtlesim.

### Comandos utilizados
Verificar que Ubuntu detecta la ESP32: ls /dev/ttyUSB*
Compilar el paquete: colcon build --packages-select basics
Cargar el workspace: source install/setup.bash
Ejecutar el launch: ros2 launch basics turtle_joy_controller.launch.py
Verificar los nodos activos: ros2 node list
Verificar los topicos activos: ros2 topic list
Ver informacion de los topicos: ros2 topic info /joystick_raw y ros2 topic info /turtle1/cmd_vel
Visualizar el grafo de comunicacion: rqt_graph

### Reestructura del repositorio
Los nodos pasaron de src/basics a src/basics/basics, el firmware de src/colmibot_firmware/esp32_basics a src/basics/esp32_basics, la carpeta launch de src/launch a src/basics/launch y el README de src a src/basics. Se agregaron package.xml, setup.py, setup.cfg y resource del paquete, y el archivo basics/__init__.py, que es necesario para que ROS2 reconozca los nodos como paquete de Python al compilar.

### Problemas encontrados
No se presentaron errores en esta actividad. Como en la actividad 6, al detener el launch con Ctrl+C aparecen mensajes KeyboardInterrupt y process has died, que corresponden a la interrupcion y no a una falla.

### Video
Evidencia de la ejecucion del launch y su comprobacion: [Ver video en Google Drive](https://drive.google.com/file/d/1fcTuRp_OV_WLP7eNzfz_oft5erNqjuQg/view?usp=sharing)
