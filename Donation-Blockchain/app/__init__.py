from flask import Flask, request
import requests
import sys
import json
import argparse
import atexit
import os
from blockchain import Blockchain
from blockchain import BlockchainDecoder
import re
import time
from options import OptionsData
import joblib
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
"""
===================================================
             RECOGIDA DE ARGUMENTOS
===================================================
"""
def ip_regex(arg_value, pat=re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')):
    if not pat.match(arg_value) and arg_value != 'localhost':
        raise argparse.ArgumentTypeError('No es una IP válida.')
    return arg_value

def str2bool(arg_value):
    if isinstance(arg_value, bool) or arg_value == "True" or arg_value == "False":
        return arg_value
    else:
        raise argparse.ArgumentTypeError('Se esperaba True/False')

parser = argparse.ArgumentParser(description='Nodo de la red VotingBlockchain')

parser.add_argument('-ip',action='store',dest='ip_cliente',
                    help='Ip de tu máquina.', type=ip_regex, required=True)
parser.add_argument('-p', action='store', dest='puerto_cliente',
                    help='Puerto de tu máquina.', required=True)

parser.add_argument('-c', type=str2bool ,action='store', dest='coordinador', 
                    help='Indica si eres o no nodo coordinador.', required=True)

parser.add_argument('-ipc', action='store',dest='ip_coordinador',
                    help='Ip del nodo coordinador.', type=ip_regex)
parser.add_argument('-pc', action='store', dest='puerto_coordinador',
                    help='Puerto del coordinador.')

results = parser.parse_args()
if results.coordinador == "False" and (results.ip_coordinador is None or results.puerto_coordinador is None):
    parser.error("-c False requiere introducir tambien los parámetros --ipc y --pc.")

if results.coordinador == "True" and (results.ip_coordinador is not None or results.puerto_coordinador is not None):
    parser.error("-c True no requiere los parámetros --ipc y --pc.")

"""
===================================================
         INICIALIZACIÓN CON LOS ARGUMENTOS
===================================================
"""
sd.nodo_coordinador = results.coordinador
sd.ip_cliente = results.ip_cliente
sd.puerto_cliente = results.puerto_cliente
if results.coordinador == "False":
    sd.ip_coordinador = results.ip_coordinador
    sd.puerto_coordinador = results.puerto_coordinador

# Creamos la estructura que guarda los saldos disponibles para cada opcion
for value in OptionsData.spend_options.values():
    sd.saldo[value] = 0
    sd.destinado[value] = 0

# Si el nodo NO ES nodo coordinador
if sd.nodo_coordinador == 'False':

    """
    ===================================================
                    UNIRSE A LA RED
    ===================================================
    """
    # Hace una petición GET al nodo coordinador para obtener todos los nodos de la red
    try:
        server = "http://" + sd.ip_coordinador + ":" + sd.puerto_coordinador + "/unirse_red/" + sd.ip_cliente + "/" + sd.puerto_cliente
        response = requests.get(server, headers={ "Content-Type" : "application/json"})
    except:
        print("Error: el nodo coordinador no está disponible o está caido.")
        sys.exit()

    # La añade a su variable agenda
    sd.agenda = response.json()['agenda']
    sd.saldo = response.json()['saldo']
    sd.destinado = response.json()['destinado']
    sd.tabla = response.json()['tabla']
    print(response.json()['blockchain'])
    sd.blockchain =  BlockchainDecoder(json.loads(response.json()['blockchain']))
    json_data = json.loads(response.json()['blockchain'])

# En caso de SI SER nodo coordinador
else:
    
    """
    ===================================================
                    INICIAR UNA RED
    ===================================================
    """
    try:
        if os.path.isfile('blockchain'):
            sd.blockchain = joblib.load("blockchain")['blockchain']
            sd.tabla = joblib.load("blockchain")['tabla']
            sd.saldo = joblib.load("blockchain")['saldo']
            sd.destinado = joblib.load("blockchain")['destinado']
        else:
            sd.blockchain = Blockchain()
    except:
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

    if len(sd.agenda) == 1:
        joblib.dump({'blockchain':sd.blockchain,'tabla':sd.tabla,'saldo':sd.saldo,'destinado':sd.destinado},"blockchain")

# añado la función
atexit.register(close_running)

# Importamos las vistas de la aplicación
from app import views
