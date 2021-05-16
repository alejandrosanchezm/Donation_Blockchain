
from hashlib import sha256
import requests
from blockchain import BloqueEncoder, BloqueDecoder, BlockchainEncoder
import json
from options import OptionsData
from app import static_data as sd

def getsha256str(input):
    return sha256(input).hexdigest()

"""
Se encarga de hacer una petición POST a los nodos conocidos de la red para que añadan el nuevo
nodo a su agenda
"""
def comunicar_nuevo_nodo(ip_receptor,puerto_receptor,ip_nuevo_nodo,puerto_nuevo_nodo):

    # Hago una petición POST a un nodo con los datos del nuevo nodo
    server = "http://" + ip_receptor + ":" + puerto_receptor + "/anadir_nodo_red/" + ip_nuevo_nodo + "/" + puerto_nuevo_nodo
    requests.post(server, headers={ "Content-Type" : "application/json"})

def index_post_args_check(request):
    arguments = ['dni','option-type','payment-type']
    for valor in arguments:
        if valor not in request.values:
            return None

    #Validamos que sea el DNI en el formato correcto
    if(validarDNI(request.values['dni'])==1):
        
        # Recogemos el concepto y el dinero
        valores = {
            "tipoTransaccion":"pago", # indicamos que el tipo de transacción es de pago
            "DNI":request.values['dni'], #El hash lo calcula despues
            "ConceptoPago":OptionsData.spend_options[request.values['option-type']],
            "DineroAportado":int(OptionsData.pay_options[request.values['payment-type']])
        }
        return valores
    else:
        return None

def admin_post_args_check(request):
    if 'option-type' not in request.values or 'quantity' not in request.values:
        return None
    else:
        valores = {
            'tipoTransaccion': "gasto",
            'IDAdministrador': sd.id_login,
            'ConceptoGasto': OptionsData.spend_options[request.values['option-type']],
            'DineroGastado': int(request.values['quantity'])
        }
        return valores

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

def actualizarDatos(valores,sd):

    if 'ConceptoPago' in valores:
        sd.tabla.append(valores)
        sd.saldo[valores['ConceptoPago']] += valores['DineroAportado']
    else:
        sd.tabla.append(valores)
        sd.saldo[valores['ConceptoGasto']] -= valores['DineroGastado']
        sd.destinado[valores['ConceptoGasto']] += valores['DineroGastado']