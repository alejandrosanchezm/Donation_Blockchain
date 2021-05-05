from app import app
import requests
import json
from blockchain import BlockchainEncoder

def multidifundirGasto(valores, sd):
    nodos_llamados = []
    for nodo in sd.agenda:
        # Si no soy yo
        if sd.ip_cliente != nodo['ip'] or sd.puerto_cliente != nodo['puerto']:
            nodos_llamados.append(nodo)

            # Le envío la transacción realizada, y mi blockchain
            answer = enviar_bloque(nodo['ip'],nodo['puerto'],valores,sd.blockchain)

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
            if answer != "OK":
                sd.blockchain.eliminarBloque()

                for nodo in nodos_llamados:
                    solicitar_eliminar_bloque(nodo['ip'],nodo['puerto'])

                return "ERROR"
    return "OK"


def enviar_bloque(ip_receptor,puerto_receptor, bloque, blockchain):

    # Hago una petición POST a un nodo con los datos de la blockchain
    server = "http://" + ip_receptor + ":" + puerto_receptor + "/recibir_bloque"
    answer = requests.post(server, headers={ "Content-Type" : "application/json"}, params={"bloque":json.dumps(bloque),"blockchain":BlockchainEncoder().encode(blockchain)})   
    return bytes.decode(answer.content)

def solicitar_eliminar_bloque(ip_receptor,puerto_receptor):
    # Hago una petición POST a un nodo con los datos de la blockchain
    server = "http://" + ip_receptor + ":" + puerto_receptor + "/eliminar_ultimo_bloque"
    answer = requests.post(server, headers={ "Content-Type" : "application/json"})   
    return bytes.decode(answer.content)