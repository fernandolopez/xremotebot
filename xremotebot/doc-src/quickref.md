XRemoteBot permite mover los robots con distintas modalidades
dependiendo de la cantidad de argumentos utilizados.

Los robots soportan 4 movimientos:

* `Robot.forward()`: Avanzar.
* `Robot.backward()`: Retroceder.
* `Robot.turnLeft()`: Girar a la izquierda.
* `Robot.turnRight()`: Girar a la derecha.

Avanzando de a pasos
--------------------

Una de las formas más intuitivas de mover un robot es indicándole
hacia donde ir, a que velocidad y por cuanto tiempo moverse en esa
dirección. Para esto se debe invocar al método deseado con 2 argumentos:

1. La velocidad (un número entre 0 y 100).
1. El tiempo a moverse (en segundos).

El siguiente ejemplo mueve al robot a velocidad máxima para que
tenga un recorrido (aproximadamente) cuadrado. El lado del "cuadrado"
está determinado por la velocida y por la duración del movimiento:

```javascript
robot.forward(100, 1)
robot.turnLeft(100, 1)
robot.forward(100, 1)
robot.turnLeft(100, 1)
```

Avanzando mientras se realizan otras tareas
-------------------------------------------

Si se invoca al método de movimiento deseado, indicando solamente
la velocidad, el robot se moverá en esa dirección hasta que
se le indique que vaya en otra dirección o se invoque a `robot.stop()`.

El siguiente ejemplo mueve el robot hacia adelante, a velocidad 80,
mientras se realizan otras tareas y luego lo detiene:

```javascript
robot.forward(80)
// realizar otras actividades
robot.stop()
```

Los métodos sin argumentos
--------------------------

También es posible invocar a los métodos de movimiento sin ningún argumento,
esto hace que el robot se mueva por un tiempo indeterminado como en el caso
anterior y a velocidad 50.

Este ejemplo se comporta igual que el anterior, pero se mueve a velocidad
50, en lugar de a velocidad 80:

```javascript
robot.forward()
// realizar otras actividades
robot.stop()
```
