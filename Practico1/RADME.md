Modelo de actores
=================

La clase Node (archivo node.py) define una interface para que sus subclases
implementen nodos (procesos) de una red que pueden comunicarse.

Cada instancia de cada nodo debería tener un nombre y debe implementar los
métodos start() y receive(msg). Esto implementa el modelo Actor, adecuado para
implementar aplicaciones (protocolos) en red y sistemas distribuidos.

Ver la implementación de los archivos ping.py y pong.py como ejemplo de su
implementación.
