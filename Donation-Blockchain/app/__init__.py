from flask import Flask, request
import requests
import sys
import json
import argparse
import atexit
import os
from blockchain import Blockchain
from blockchain import BlockchainDecoder

"""
===================================================
       VARIABLES GLOBALES DE LA APLICACIÓN
===================================================
"""

from app import static_data as sd
from app import view_functions as vf

"""
===================================================
            ARGUMENTOS DEL PROGRAMA
===================================================
"""

"""
Esta parte se depurará más adelante. 

Recogo los valores de los parámetros del programa
- argumento 1: ip_cliente (es decir, la ip del nodo que se conecta)
- argumento 2: puerto_cliente (es decir, el puerto del nodo que se conecta)
- argumento 3: ip_coordinador (es decir, la ip del coordinador de la red)
- argumento 4: puerto_coordinador (es decir, el puerto del coordinador de la red)
- argumento 5: nodo_coordinador True o False, indica si es o no el nodo coordinador

Para ejecutarlo, tendríais que realizar:

- Para el nodo coordinador: python3 run.py localhost 5000 localhost 5000 True
- Para el nodo cliente: python3 run.py localhost 5001 localhost 5000 False

"""
sd.nodo_coordinador = sys.argv[1]
sd.ip_cliente = sys.argv[2]
sd.puerto_cliente = sys.argv[3]

if sd.nodo_coordinador == 'False':
    sd.ip_coordinador = sys.argv[4]
    sd.puerto_coordinador = sys.argv[5]

"""
===================================================
            INICIALIZACIÓN DE FLASK
===================================================
"""
app = Flask(__name__)

app.config['SECRET_KEY'] = "OCML3BRawWEUeaxcuKHLpw"

"""
===================================================
            ACCIONES DE INICIO
===================================================
"""


# Si el nodo NO ES nodo coordinador
if sd.nodo_coordinador == 'False':

    # Hace una petición GET al nodo coordinador para obtener todos los nodos de la red
    server = "http://" + sd.ip_coordinador + ":" + sd.puerto_coordinador + "/unirse_red/" + sd.ip_cliente + "/" + sd.puerto_cliente
    response = requests.get(server, headers={ "Content-Type" : "application/json"})
    # La añade a su variable agenda
    sd.agenda = response.json()['agenda']
    sd.blockchain =  BlockchainDecoder(json.loads(response.json()['blockchain']))
    json_data = json.loads(response.json()['blockchain'])
    for bloque in json_data['blockchain']:
        if bool(bloque['transaccion']) != False:
            valores = {
                
                "DNI":bloque['transaccion']['DNI'],
                "ConceptoPago":bloque['transaccion']['ConceptoPago'],
                "DineroAportado":bloque['transaccion']['DineroAportado']
            }
            sd.tabla.append(valores)
            sd.num_personas = sd.num_personas + 1

# En caso de SI SER nodo coordinador
else:
    
    sd.blockchain = Blockchain()
    # Añade su propio nodo a la lista de nodos
    nuevo_nodo = {
        'ip': sd.ip_cliente,
        'puerto':sd.puerto_cliente
    }
    if nuevo_nodo not in sd.agenda:
        sd.agenda.append(nuevo_nodo)

"""
Definimos el comportamiento para cuando un nodo se cierra.
Envía una petición POST a todos los nodos de la agenda que no son él 
para que le eliminen de su agenda.
"""
def close_running():

    for nodo in sd.agenda:
        try:
            if sd.ip_cliente != nodo['ip'] or sd.puerto_cliente != nodo['puerto']:
                # Si no soy nodo coordinador
                if sd.nodo_coordinador == 'False':
                    server = "http://" + nodo['ip'] + ":" + nodo['puerto'] + "/eliminar_nodo_red/" + sd.ip_cliente + "/" + sd.puerto_cliente + "/None/None"
                    requests.post(server, headers={ "Content-Type" : "application/json"})
                
                # Si soy nodo coordinador, elijo al nodo más antiguo (el primero de la agenda) como nuevo coordinador
                else:
                    server = "http://" + nodo['ip'] + ":" + nodo['puerto'] + "/eliminar_nodo_red/" + sd.ip_cliente + "/" + sd.puerto_cliente + "/" + sd.agenda[0]['ip'] + "/"  + sd.agenda[0]['puerto'] 
                    requests.post(server, headers={ "Content-Type" : "application/json"})             
        except:
            print("Error. No he conseguido comunicar mi salida de la red al nodo "+ nodo['ip'] + ":"+ nodo['puerto'])
            
# añado la función
atexit.register(close_running)

# Importamos las vistas de la aplicación
from app import views
