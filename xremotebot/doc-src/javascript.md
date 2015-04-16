Por las limitaciones del entorno el cliente Javascript es asincrónico y
su uso está basado en la utilización de callbacks y Promises.

Dentro de estas limitaciones, sin embargo, se intentó que las API de
este cliente se parezca lo más posible al resto.

Conexión al servidor
--------------------

La forma más sencilla de empezar a usar el cliente Javascript es, simplemente,
usando el ejemplo [provisto en su página](/javascript).

El código para conectarse implica instanciar un objeto `Server` pasándole
la URL de la API de XRemoteBot y una API key válida e invocar al método
`Server#onConnect()` pasándole como argumento una función. Esta función
se ejecutará cuando la conexión se establezca:

```javascript
var server = Server('ws://localhost:8000/api', '4b9902d3-3295-41b9-a0f5-8bc2015d0ece');
server.onConnect(function(){
    // ¡Tu código!
});
```

Es posible no utilizar `Server#onConnect()`, pero sin usar esta función no hay
ninguna garantía de que la conexión se encuentre establecida y el script puede
fallar.

Funciones útiles
----------------

`println` imprime una línea en la "consola" de XRemoteBot.

`rblog` imprime una línea en la "consola" de XRemoteBot, solamente si se
encuentra habilitado el modo "debug".

Obteniendo información de los robots
------------------------------------

### `get_robots()`

El método `Server#get_robots()` retorna la lista de los robots libres.

```javascript
server.get_robots().then(function(robots){
    println(robots);
});
```

Salida en la consola:

```
[
    {"robot_id":"10","robot_model":"n6"},
    {"robot_id":"00:1E:19:01:0B:81","robot_model":"scribbler"},
    {"robot_id":"7","robot_model":"n6"}
]
```

### `reserve()`

El método `Server#reserve()` recibe como argumentos el modelo de un robot y
un identificador e intenta reservar un robot específico. Si tiene éxito
retorna un objeto Javascript con los datos del robot:

```javascript
server.reserve('n6', 10).then(function(robot_data){
    println(robot_data);
}).catch(function(){
    println('No se pudo hacer la reserva');
});
```

Salida en la consola en caso de éxito:

```
{"robot_id":"10","robot_model":"n6"},
```

### `fetch_robot()`

El método `Server#fetch_robot()` no recibe argumentos y reserva, si es
posible, un robot libre. Retorna un objeto con los datos del robot al
igual que `Server#reserve()`. Sucesivas
invocaciones a `Server#fetch_robot()` pueden retornar robots repetidos.

```javascript
server.fetch_robot.then(function(robot_data){
    println(robot_data);
}).catch(function(){
    println('No se pudo hacer la reserva');
});
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

```javascript
server.fetch_robot.then(function(robot_data){
    var robot = Robot.new(server, robot_data);
    // ¡Tu código controlando al robot!
}).catch(function(){
    println('No se pudo hacer la reserva');
});
```

Movimientos
-----------

Los robots soportan 4 movimientos:

* `Robot.forward()`: Avanzar.
* `Robot.backward()`: Retroceder.
* `Robot.turnLeft()`: Girar a la izquierda.
* `Robot.turnRight()`: Girar a la derecha.

Sensores
---------
