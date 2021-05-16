from app import app, view_functions as vf
import requests
import json
<<<<<<< HEAD
from blockchain import BlockchainEncoder, BlockchainDecoder
=======
from blockchain import BlockchainEncoder

>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9
"""
Clase que se encarga de realizar la multidifusión del gasto y del pago
"""

def multidifundirGasto(valores, sd):
    nodos_llamados = []
    for nodo in sd.agenda:
        # Si no soy yo
        if sd.ip_cliente != nodo['ip'] or sd.puerto_cliente != nodo['puerto']:
            nodos_llamados.append(nodo)

            # Le envío la transacción realizada, y mi blockchain
            answer = enviar_bloque(nodo['ip'],nodo['puerto'],valores,sd.blockchain)
<<<<<<< HEAD
            print(answer)
=======

>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9
            # Si el nodo no lo valida
            if answer != "OK":
                sd.blockchain.eliminarBloque()

                for nodo in nodos_llamados:
                    answer = solicitar_eliminar_bloque(nodo['ip'],nodo['puerto'])

                return "ERROR"
    return "OK"

def multidifundirPago(valores, sd):

    nodos_llamados = []
    # Multidifundimos el bloque a los nodos de la red
    for nodo in sd.agenda:

        # Si no soy yo
        if sd.ip_cliente != nodo['ip'] or sd.puerto_cliente != nodo['puerto']:

            nodos_llamados.append(nodo)
            # Le envío la transacción realizada, y mi blockchain
            answer = enviar_bloque(nodo['ip'],nodo['puerto'],valores,sd.blockchain)
<<<<<<< HEAD
            print(answer)
=======
>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9
            if answer != "OK":
                sd.blockchain.eliminarBloque()

                for nodo in nodos_llamados:
                    solicitar_eliminar_bloque(nodo['ip'],nodo['puerto'])

                return "ERROR"
    return "OK"
<<<<<<< HEAD
  
=======

>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9
def enviar_bloque(ip_receptor,puerto_receptor, bloque, blockchain):

    # Hago una petición POST a un nodo con los datos de la blockchain
    server = "http://" + ip_receptor + ":" + puerto_receptor + "/recibir_bloque"
    answer = requests.post(server, headers={ "Content-Type" : "application/json"}, params={"bloque":json.dumps(bloque),"blockchain":blockchain.hashBlockchain})   
    return bytes.decode(answer.content)

def solicitar_eliminar_bloque(ip_receptor,puerto_receptor):
    # Hago una petición POST a un nodo con los datos de la blockchain
    server = "http://" + ip_receptor + ":" + puerto_receptor + "/eliminar_ultimo_bloque"
    answer = requests.post(server, headers={ "Content-Type" : "application/json"})   
<<<<<<< HEAD
    return bytes.decode(answer.content)

##############################################################################
#           PROTOCOLO DE RECUPERACIÓN DE LA BLOCKCHAIN CORRUPTA              #
##############################################################################

def protocoloRecuperacionBlockchain(sd):

    hashes = []
    blockchains = []

    # Para cada nodo de mi agenda, le pido su blockchain
    for nodo in sd.agenda:
        if sd.ip_cliente != nodo['ip'] or sd.puerto_cliente != nodo['puerto']:
            answer = pedir_blockchain(nodo['ip'],nodo['puerto'])
            blockchains.append(answer)
            hashes.append(answer.hashBlockchain)
        else:
            blockchains.append(sd.blockchain)
            hashes.append(sd.blockchain.hashBlockchain)

    if len(set(hashes)) > 1:
        # Escogo el hash que tienen el mayor número de nodos
        blockchain_mayor_acuerdo = max(hashes,key=hashes.count)
        for i in range(0,len(blockchains)):

            # Encuentro esa blockchain
            if blockchains[i].hashBlockchain == blockchain_mayor_acuerdo:

                # Multidifundo la blockchain estable
                multidifundirBlockchain(sd, blockchains[i])
                break

def multidifundirBlockchain(sd, blockchain):

    # Para todos los nodos de la agenda
    for nodo in sd.agenda:
        if sd.ip_cliente != nodo['ip'] or sd.puerto_cliente != nodo['puerto']:
            enviar_blockchain(nodo['ip'],nodo['puerto'],sd.blockchain)

        # Si soy yo mismo
        else:
            sd.blockchain = blockchain           

def enviar_blockchain(ip_receptor,puerto_receptor, blockchain):

    # Hago una petición POST a un nodo con la nueva blockchain
    server = "http://" + ip_receptor + ":" + puerto_receptor + "/recibir_blockchain"
    answer = requests.post(server, headers={ "Content-Type" : "application/json"}, params={"blockchain":BlockchainEncoder.encode(blockchain)})   

def pedir_blockchain(ip_receptor,puerto_receptor):

    # Hago una petición GET a un nodo de su blockchain
    server = "http://" + ip_receptor + ":" + puerto_receptor + "/pedir_blockchain"
    answer = requests.get(server, headers={ "Content-Type" : "application/json"})   
    return BlockchainDecoder(json.loads(answer.content))
=======
    return bytes.decode(answer.content)
>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9
