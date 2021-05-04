
from hashlib import sha256
import requests
from blockchain import BloqueEncoder, BloqueDecoder, BlockchainEncoder
import json

def getsha256str(input):
    return sha256(input).hexdigest()

"""
Se encarga de hacer una petición POST a los nodos conocidos de la red para que añadan el nuevo
nodo a su agenda
"""
def comunicar_nuevo_nodo(ip_receptor,puerto_receptor,ip_nuevo_nodo,puerto_nuevo_nodo):

    # Hago una petición POST a un nodo con los datos del nuevo nodo
    server = "http://" + ip_receptor + ":" + puerto_receptor + "/añadir_nodo_red/" + ip_nuevo_nodo + "/" + puerto_nuevo_nodo
    requests.post(server, headers={ "Content-Type" : "application/json"})

"""
def enviar_blockchain(ip_receptor,puerto_receptor, blockchain):

    # Hago una petición POST a un nodo con los datos de la blockchain
    server = "http://" + ip_receptor + ":" + puerto_receptor + "/actualizar_blockchain"
    requests.post(server, headers={ "Content-Type" : "application/json"}, params={'blockchain':blockchain})   
"""

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

def validarDNI(dni):
        if(len(dni)==9):
            if(dni[0:8].isdigit()):
                if (dni[8].isalpha()):
                    return 1
                else:
                    return 0
            else: 
                return 0
        else:
            return 0

class sentenciasSwitch():
    def switch_concepto(self,option):
        default = "Opcion incorrecta"
        return getattr(self, 'case'+str(option),lambda:default)()
    def case1(self):
        return "IRPF"
    def case2(self):
        return "IS"
    def case3(self):
        return "Patrimonio"
    def case4(self):
        return "DYS"
    def case5(self):
        return "IVA"
    def case6(self):
        return "IAE"
    def case7(self):
        return "IBI"
    def case8(self):
        return "IVTM"

    def switch_dinero(self,option):
        default = "Opcion incorrecta"
        return getattr(self, 'case_'+str(option),lambda:default)()
    def case_1(self):
        return 100
    def case_2(self):
        return 200
    def case_3(self):
        return 500
    def case_4(self):
        return 1000
    def case_5(self):
        return 2000


