# VotingBlockchain

Aplicación distribuida para la donación de una cantidad de dinero y destinarla hacia un propósito.

## Instalación

Cómo instalar el repositorio:

    git clone https://github.com/alejandrosanchezm/blockchain.git

Para activar el entorno virtual

    source distri/bin/activate

En caso de fallar el paso anterior, crear un entorno virtual propio

    python3 -m venv distri
    source distri/bin/activate

Para realizar una instalación de las librerías utilizadas actualmente, ejecutar el comando

    pip install -r requirements.txt

## Uso

### Cómo se inicial los nodos de la red

La arquitectura de la red es la siguiente:

- Habrá (al menos) un nodo coordinador. Este nodo se encargará de introducir al nodo a la red.
Cuando un nodo cliente quiera añadirse a la red, al iniciarse conectará con el nodo coordinador indicándole su ip y puerto, y éste
le devolverá una lista de diccionarios con las ips y puertos de todos los nodos de la red.
Así mismo, difundirá a todos los nodos de la red la ip y puerto del nuevo nodo para que actualicen su 'agenda' de nodos.

- Los nodos clientes tendrán que conocer la dirección del nodo coordinador para conectarse a la red.

![alt text](https://raw.githubusercontent.com/alejandrosanchezm/blockchain/master/imgs/Esquema1.png)

- Si un nodo cliente de la red se cierra, se indica al resto de nodos que ese nodo se ha eliminado para que lo eliminen de la agenda.
- Si es el nodo coordinador el que se elimina, antes de cerrarse elegirá al primer nodo de la red como nodo coordinador

Los argumentos para iniciar el servidor son los siguientes en este orden:
- ip cliente (es decir, la nuestra)
- puerto cliente (es decir, la nuestra)
- ip coordinador (si somos el coordinador será la nuestra)
- puerto coordinador (si somos el coordinador será el nuestro)
- coordinador (Valor a True o False), indicará True si es coordinador, False en caso contrario

Para iniciar un nodo coordinador:
  
    $ python run.py -c True -ip localhost -p 5000
Para iniciar un nodo cliente:
  
    $ python run.py -c False -ip localhost -p 5001 -ipc localhost -pc 5000
    
### Cómo funciona la Blockchain

Este es el esquema mediante el cual funciona la blockchain:

![alt text](https://raw.githubusercontent.com/alejandrosanchezm/blockchain/master/imgs/Diagrama.png)

