[TOC]

Tanto el cliente Python como el cliente Ruby son los más fáciles de
usar pero requieren que tengas instalado el cliente correspondiente
en tu máquina.

Instalación
-----------


1. Instalar el [intérprete de Ruby](https://www.ruby-lang.org/es/downloads/).
    * GNU/Linux: En muchas distribuciones viene preinstalado, en la mayoría
    puede ser instalado usando el gestor de paquetes de la distribución. Por
    ejemplo, en las distribuciones basadas en Debian, como Lihuen puede
    instalarse con `apt-get install ruby2.1`.
    * Otros sistemas: [Ver la guía de instalación de
    Ruby](https://www.ruby-lang.org/es/documentation/installation/)
1. Instalar el cliente usando Rubygems: `gem install xremotebot-client`



Conexión al servidor
--------------------

El código para conectarse implica instanciar un objeto `Server` pasándole
la URL de la API de XRemoteBot y una API key válida:

```ruby
require 'xremotebot'
server = XRemoteBot::Server.new('localhost', 8000, '/api', '4b9902d3-3295-41b9-a0f5-8bc2015d0ece')
```

Si el servidor se encuentra configurado para uso local es posible invocarlo
sin la API key.

Funciones útiles
----------------

`XRemoteBot.wait()` recibe un número que indica cuantos segundos demorar la ejecución
del programa. Equivale a invocar a `sleep()` con el mismo argumento.

Obteniendo información de los robots
------------------------------------

### get_robots()

El método `Server#get_robots()` retorna la lista de los robots libres.

```ruby
robots = server.get_robots
print robot
```

Salida en la consola:

```
[
    {"robot_id":"10","robot_model":"n6"},
    {"robot_id":"00:1E:19:01:0B:81","robot_model":"scribbler"},
    {"robot_id":"7","robot_model":"n6"}
]
```

### reserve()

El método `Server#reserve()` recibe como argumentos el modelo de un robot y
un identificador e intenta reservar un robot específico. Si tiene éxito
retorna un diccionario con los datos del robot:

```ruby
begin
    robot_data = server.reserve('n6', 10)
    print robot_data
rescue
    print 'No se pudo hacer la reserva'
end
```

Salida en la consola en caso de éxito:

```
{"robot_id":"10","robot_model":"n6"},
```

### fetch_robot()

El método `Server#fetch_robot()` no recibe argumentos y reserva, si es
posible, un robot libre. Retorna un objeto con los datos del robot al
igual que `Server#reserve()`. Sucesivas
invocaciones a `Server#fetch_robot()` pueden retornar robots repetidos.

```ruby
begin
    server.fetch_robot
    print robot_data
rescue
    print 'No se pudo hacer la reserva'
end
```

Salida en la consola en caso de éxito:

```
{"robot_id":"10","robot_model":"n6"},
```

Instanciación de un robot
-------------------------

Se puede controlar un robot creando objetos `Robot`, para esto es necesario
haber reservado previamente un robot con `Server#reserve()` o
`Server#fetch_robot()`. El constructor de `Robot` recibe dos argumentos: un
objeto `Server` y el objeto retornado por `Server#reserve()` o `Server#fetch_robot()`.

```ruby
begin
    robot_data = server.fetch_robot
rescue
    print 'No se pudo hacer la reserva'
end
robot = XRemoteBot::Robot.new(server, robot_data)
# ¡Tu código controlando al robot!
```

Movimientos
-----------

Los robots soportan 4 movimientos:

* `Robot.forward()`: Avanzar.
* `Robot.backward()`: Retroceder.
* `Robot.turnLeft()`: Girar a la izquierda.
* `Robot.turnRight()`: Girar a la derecha.

Cada uno de estos métodos puede recibir entre cero y dos
argumentos.

Si no reciben argumentos, el movimiento
se realiza a una velocidad predeterminada por un tiempo
indefinido (hasta que invoques `Robot.stop()`).

Si se le envían parámetros, el primero indica la velocidad
(entre -100 y 100, siendo 0 equivalente a invocar
`Robot.stop()`). Y el segundo indica el tiempo que debe
durar el movimiento en segundos, al finalizar ese tiempo
el robot se detendrá automáticamente.

Por ejemplo:

```ruby
robot.forward      # El robot se mueve indefinidamente
                     # a una velocidad predeterminada
```

```ruby
robot.forward(50)    # El robot se mueve indefinidamente
                     # a velocidad 50
```

```ruby
robot.forward(50, 1) # El robot se mueve a velocidad 50
                     # durante un segundo
```

Sensores
---------

Los objetos `Robot` cuentan con los siguientes métodos
para acceder a los valores de los sensores:

* `Robot#getLine()`: Retorna una secuencia, de 2 elementos, con los valores
    de los sensores de línea. El rango de los sensores depende
    del modelo de robot usado.
* `Robot#ping()`: Retorna la distancia aproximada de el objeto
    más cercano al robot. En el caso de los robots N6 esta distancia
    está en centímetros y tiene un rango de 0 a 600, en el caso
    de los robots scribbler la distancia es una aproximación a
    centímetros y tiene un rango de 0 a 92.
* `Robot#getObstacle()`: Retorna `true` si hay un obstáculo. Si
    se le envía un parámetro, éste determina la distancia máxima
    a la que
    debe estar un objeto para considerarse un obstáculo.
