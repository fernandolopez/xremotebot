[TOC]

El cliente Javascript de XRemoteBot es asincrónico y
su uso está basado en la utilización de callbacks y Promises. Esto
es porque dentro del entorno de un navegador, en la mayoría de
los casos, no es posible realizar operaciones bloqueantes, y cuando
es posible no es recomendable

Esto hacer que el uso del cliente Javascript sea un poco más
complejo que el uso de los clientes Python y Ruby.
Sin embargo, se intentó que la API de
este cliente se parezca lo más posible al resto.

Conexión al servidor
--------------------

La forma más sencilla de empezar a usar el cliente Javascript es, simplemente,
usando el ejemplo [provisto en su página](/javascript).

El código para conectarse implica instanciar un objeto `Server` pasándole
la URL de la API de XRemoteBot y una
[API key](/user)
válida e invocar al método
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

### get_robots()

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

### reserve()

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

### fetch_robot()

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

Cada uno de estos métodos puede recibir entre cero y dos
argumentos, y retorna un objeto
[Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise).

Si no reciben argumentos, el movimiento
se realiza a una velocidad predeterminada por un tiempo
indefinido (hasta que invoques `Robot.stop()`).

Si se le envían parámetros, el primero indica la velocidad
(entre -100 y 100, siendo 0 equivalente a invocar
`Robot.stop()`). Y el segundo indica el tiempo que debe
durar el movimiento en segundos, al finalizar ese tiempo
el robot se detendrá automáticamente.

Por ejemplo:

```javascript
robot.forward(); // El robot se mueve indefinidamente
                 // a una velocidad predeterminada
```

```javascript
robot.forward(50); // El robot se mueve indefinidamente
                   // a velocidad 50
```

```javascript
robot.forward(50, 1); // El robot se mueve a velocidad 50
                      // durante un segundo
```

Si se envían movimientos en secuencia, XRemoteBot los
encola y los envía en orden:

```javascript
robot.forward(50, 1);     // El robot se mueve hacia adelante 1 segundo.
robot.turnLeft(100, 0.5); // Luego gira a la izquierda durante medio segundo.
```

Pero hay que tener en cuenta que la ejecución del código
no se demora por la invocación a estos métodos, en el
ejemplo anterior el método `Robot#turnLeft()` no se ejecuta
un segundo después de `Robot#forward()` sino que se ejecuta
unos pocos milisegundos después del mismo.

Para esperar a que realmente termine de realizar la acción
el robot antes de proseguir es necesario usar `Promise#then()`:

```javascript
robot.forward(50, 1).then(function(){
    alert('El robot acaba de detenerse');
});
```

Se puede esperar a que termine toda una secuencia de movimientos
encadenando las invocaciones a `Promise#then()` o bien utilizando
`Promise#all()`:

```javascript
// Encadenando promesas
robot.forward(50, 1).then(function(){
    robot.turnLeft(100, 1);
}).then(function(){
    alert('El robot se detuvo');
});

// El mismo efecto con Promise#all()
Promise.all([
    robot.forward(50, 1),
    robot.turnLeft(100, 1),
]).then(function(){
    alert('El robot se detuvo');
});
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
* `Robot#getObstacle()`: Retorna `True` si hay un obstáculo. Si
    se le envía un parámetro, éste determina la distancia máxima
    a la que
    debe estar un objeto para considerarse un obstáculo.

En todos los casos es necesario usar `Promise#then()` para acceder
al valor retornado, por ejemplo:

```javascript
robot.getObstacle().then(function(obstacle){
    if (obstacle){
        alert('Hay un obstáculo');
    }
    else{
        alert('No hay obstáculo');
    }
});
```

Iteraciones y demoras
---------------------

Si bien es imposible tener operaciones bloqueantes que demoren
la ejecución del resto del programa, es posible simular este
comportamiento usando las funciones de Javascript `setTimeout()`,
`setInterval()` o los objetos `Promise` retornados por la API.

### Demoras con setTimeout()

Por ejemplo, es para ejecutar una acción 5 segundos después
de una primer acción se puede usar `setTimeout()`.

```javascript
robot.forward(50);
setTimeout(function(){
    $('h1').text('Pasaron 5 segundos');
}, 5000);
```

### Iteraciones usando invocaciones a función y promesas

En caso de las iteraciones es especial, ya que si usamos
`while` o `for` el comportamiento no es intuitivo.

Veamos un *mal* ejemplo de un programa para esquivar obstáculos:

```javascript
// Se ignora la inicialización de server y robot para
// simplificar el ejemplo
robot.forward();
while (true){
    robot.getObstacle().then(function(obstacle){
        if (obstacle){
            robot.backward(30, 1);
            robot.turnLeft(40, 1);
            robot.forward();
        }
    });
}
```

Este script bloquea rápidamente el navegador, ya que el `while`
encola en las estructuras de datos internas de XRemoteBot para
Javascript, una secuencia infinita de mensajes `Robot#getObstacle()`.
En algunos casos en navegador se bloquea sin llegar a enviar
ni uno de esos mensajes.

Esto es porque ninguna de las operaciones es bloqueante, todas
se ejecutan en pocos milisegundos y retornan una promesa.

Una forma mejor de implementar este mismo algoritmo sería
generando un mensaje `Robot#getObstacle()` sólo cuando recibimos
la respuesta del mensaje anterior. Esto se puede lograr usando una
función "recursiva":

```javascript
// Se ignora la inicialización de server y robot para
// simplificar el ejemplo

function esquivar(){
    robot.getObstacle().then(function(obstacle){
        if (obstacle){
            robot.backward(30, 1);
            robot.turnLeft(40, 1);
            robot.forward();
        }
        esquivar();
    });
}

robot.forward();
esquivar();
```

En el párrafo anterior se escribió "recursiva" usando comillas,
porque realmente no es recursiva ya que `esquivar()` no se
invoca a si misma, sino que es la promesa retornada por
`Robot#getObstacle()`, la que lo invoca.

Si fuera una recursión real
eventualmente se llenaría el stack del intérprete de
Javascript.

### Operaciones repetidas con setInterval()

Si el intervalo de tiempo entre una operación y otra no
es muy chico (de manera que no se encolan operaciones sin
respuesta) es posible utilizar la función de Javascript
`setInterval()` para repetir operaciones.

Por ejemplo, el siguiente ejemplo actualiza el encabezado de
la página con los valores del sensor de línea, cada 1 segundo:

```javascript
setInterval(function(){
    robot.getLine().then(function(line){
        $('h1').text(line);
    });
}, 1000);
```

Por supuesto también es posible escribir este ejemplo
sin usar `setInterval()` como se explica en el punto
anterior.

### setTimeout() y setInteval() VS. window.setTimeout() y window.setInterval()

Para detener un `setInterval()` o un `setTimeout()` es necesario invocar
a `clearInterval()` o `clearTimeout()` o recargar la página.

Para que la ejecución de un script que use estas funciones no interfiera
con una ejecución posterior, XRemoteBot para Javascript, provee
su propia versión de estas funciones. Estas versiones de
`setTimeout()` y `setInterval()` son iguales a las originales
(accesibles con `window.setTimeout()` y `window.setInterval()`)
excepto que también se interrumpe su ejecución al presionar el
botón "Ejecutar" de la interfaz web.

Por lo tanto es recomendable usar `setTimeout()` y `setInterval()`, pero
si el usuario así lo desea, puede invocar a las funciones originales
con su nombre precedido de `window.`.


