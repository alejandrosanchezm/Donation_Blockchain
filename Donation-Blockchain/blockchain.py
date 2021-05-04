# Script encargado de controlar el blockchain

from hashlib import sha256
import json
import copy
import re
from json import JSONEncoder
import traceback 


# RepresentaciOn de los Bloques de la cadena
class Bloque:

    # Constructor del bloque:
    # hashBloqueAnterior: hash del bloque anterior para asegurar la integridad
    # transaccion: transacciOn que se va a llevar a cabo
    # indiceBloque: el Indice del bloque dentro de la cadena
    # incognitaDeMinado: valor que cambia el hash del bloque para cumplir con la prueba de trabajo
    # hashBloque: hash del propio bloque
    def __init__(self, hashBloqueAnterior, transaccion, indiceBloque,send_incognitaDeMinado=None, send_hashBloque=None):
        
        self.hashBloqueAnterior = hashBloqueAnterior
        self.transaccion = transaccion
        self.indiceBloque = indiceBloque
        if (send_incognitaDeMinado == None):
            self.incognitaDeMinado = 0
        else:
            self.incognitaDeMinado = send_incognitaDeMinado
        if (send_hashBloque == None):
            self.hashBloque = 0
        else: 
            self.hashBloque = send_hashBloque

 
    # FunciOn que calcula el hash del bloque.
    # Fuente: https://recursospython.com/guias-y-manuales/aplicacion-blockchain-desde-cero/
    # A diferencia de la fuente, nosotros ponemos a 0 el valor del hash para forzar la solo dependencia de la incOgnita de minado para hacer el cAlculo.
    def calcularHash(self):
        self.hashBloque = 0
        datosBloque = json.dumps(self.__dict__, sort_keys=True).encode()
        self.hashBloque = sha256(datosBloque).hexdigest()
        return self.hashBloque

# Clase que representa la Blockchain
class Blockchain:

    # Constructor
    def __init__(self, send_blockchain=None, send_transaccionNoValidada=None):

        # blockchain: lista de objetos Bloque
        # transaccionNoValidada: diccionario que guarda la transacciOn de forma temporal antes de aNadirse al bloque (solo se considera 1 transacciOn por bloque)
        if send_blockchain == None:
            self.blockchain = []
        else:
            self.blockchain = send_blockchain
        if send_transaccionNoValidada == None:
            self.transaccionNoValidada = {}
        else:
            self.transaccionNoValidada = send_transaccionNoValidada

        # CreaciOn del bloque gEnesis (se toma por 0 el valor del hash anterior)
        if send_blockchain == None:
            bloqueGenesis = self.nuevoBloque(0)
            
            # Si el bloque gEnesis es nulo devolver None
            if bloqueGenesis == None:
                return None

    def areEqual(self,b2):
        if b2 != None:
            if len(self.blockchain) == len(b2.blockchain):
                for i in range(0,len(self.blockchain)):
                    bloque1 = self.blockchain[i]
                    bloque2 = b2.blockchain[i]
                    if bloque1.hashBloqueAnterior != bloque2.hashBloqueAnterior: return False
                    if bloque1.transaccion != bloque2.transaccion: return False
                    if bloque1.indiceBloque != bloque2.indiceBloque: return False
                    if bloque1.incognitaDeMinado != bloque2.incognitaDeMinado: return False
                    if bloque1.hashBloque != bloque2.hashBloque: return False
                return True
            else:
                return False

    # Propiedad empleada para la devoluciOn del Ultimo bloque de la cadena o None si la cadena estA vacIa
    @property
    def ultimoBloque(self):
        if len(self.blockchain) == 0:
            return None

        return self.blockchain[-1]  # DevoluciOn del Ultimo bloque

    # FunciOn para la creaciOn de una nueva transacciOn de pago
    def nuevaTransaccionPago(self, DNI, conceptoPago, dineroAportado):

        # DNI: identificaciOn del pagador (pagador anOnimo)
        # ConceptoPago: razOn a la que se destina el dinero
        # DineroAportado: cantidad aportada
        transaccion = {
            'tipoTransaccion': "pago",
            'DNI': DNI,
            'ConceptoPago': conceptoPago,
            'DineroAportado': dineroAportado
        }
        
        # Se registra la transacciOn como 'no validada' previamente a la formaciOn de su Bloque
        self.transaccionNoValidada = transaccion
    
    # FunciOn para la creaciOn de una nueva transacciOn de gasto
    def nuevaTransaccionGasto(self, idAdmin, conceptoGasto, dineroGastado):

        # IDAdministrador: id de administrador que realiza el gasto de impuestos
        # ConceptoGasto: razOn del gasto
        # DineroGastado: cantidad usada (en balance negativo)
        transaccion = {
            'tipoTransaccion': "gasto",
            'IDAdministrador': idAdmin,
            'ConceptoGasto': conceptoGasto,
            'DineroGastado': -1 * dineroGastado
        }
        
        # Se registra la transacciOn como 'no validada' previamente a la formaciOn de su Bloque
        self.transaccionNoValidada = transaccion
       

    # FunciOn para la creaciOn de un nuevo bloque
    def nuevoBloque(self, hashBloqueAnterior):

        # CreaciOn del nuevo bloque. ParAmetros: hash del bloque anterior, transacciOn no validada y valor de Indice en la cadena a partir de la longitud de Esta
        bloque = Bloque(hashBloqueAnterior, self.transaccionNoValidada, len(self.blockchain))

        # CAlculo de la incOgnita de Minado
        self.calcularIncognitaDeMinado(bloque)

        # VerificaciOn del nuevo Bloque
        # Bloque vAlido: limpiar la transacciOn no validada y aNadir el Bloque a la cadena
        # Bloque no vAlido: devolver None
        if self.verificarBloqueMinado(bloque) == 0:
            self.transaccionNoValidada = {}
            self.blockchain.append(bloque)
            return bloque
        else:
            return None

    # FunciOn para calcular la incOgnita de minado   
    def calcularIncognitaDeMinado(self, bloque):

        bloque.incognitaDeMinado = 0

        # Prueba de trabajo: cAlculo de una incOgnita que dE lugar a un hash que empiece por '00000' usando fuerza bruta
        hashBloque = bloque.calcularHash()
        while not hashBloque.startswith('00000'):  # A mayor nUmero de '0' mayor grado de dificultad
            bloque.incognitaDeMinado += 1
            hashBloque = bloque.calcularHash()

    # FunciOn para verificar la correcciOn del bloque minado
    def verificarBloqueMinado(self, bloque):

        # VerificaciOn 1: El hash del bloque debe empezar por el nUmero de '0' fijado como grado de dificultad
        if not bloque.hashBloque.startswith('00000'):
            print("ERROR. Formato de hash incorrecto. Hash: ", bloque.hashBloque)
            return -1

        # VerificaciOn 2: En el bloque examinado (si es distinto al gEnesis) el campo "hashBloqueAnterior" debe coincidir con el valor de hashBloque del bloque previo
        if bloque.indiceBloque > 0 and not bloque.hashBloqueAnterior == self.blockchain[bloque.indiceBloque - 1].hashBloque:
            print("ERROR. La Blockchain se ha roto.")
            print("Hash anterior: [" + str(bloque.hashBloqueAnterior) + "]. Esperado: [" + str(self.blockchain[bloque.indiceBloque - 1].hashBloque) + "]")
            return -2

        # VerificaciOn 3: Comprobar que el hash del bloque estA verdaderamente bien construido
        # Creamos una copia del bloque examinado (fundamentalmente con la misma incOgnita de minado precalculada) y fijamos su hash a 0.
        # Recalculamos el hash y comprobamos si se obtiene un hash idEntico al del bloque examinado
        bloqueComprobacion = copy.copy(bloque)
        bloqueComprobacion.hashBloque = 0
        bloqueComprobacion.calcularHash()
        hashComprobacion = bloqueComprobacion.hashBloque
        
        if not hashComprobacion == bloque.hashBloque:
            print("ERROR. El Hash calculado para los datos del bloque no es correcto.")
            print("Hash del bloque: [" + str(bloque.hashBloque) + "]. Hash recalculado: [" + str(hashComprobacion) + "]")
            return -3

        return 0
        

    # FunciOn para mostrar los datos de un bloque
    def mostrarBloque(self, bloque):
        print("Indice Bloque:\t\t", bloque.indiceBloque)
        print("Hash anterior:\t\t", bloque.hashBloqueAnterior)
        print("TransacciOn:\t\t", bloque.transaccion)
        print("IncOgnita:\t\t", bloque.incognitaDeMinado)
        print("Hash Bloque:\t\t", bloque.hashBloque)
        print("\n\n")

    # FunciOn utilizada para realizar el pago
    def realizarPago(self, DNI, conceptoPago, dineroAportado):

        # CreaciOn de una nueva transacciOn de pago a partir de los datos recibidos como parAmetro
        self.nuevaTransaccionPago(DNI, conceptoPago, dineroAportado)

        # Comprobar la integridad de la cadena antes de crear el bloque (el Bloque GEnesis debe existir)
        # En caso de Exito, se crea el Bloque y se muestra
        if len(self.blockchain) == 0 or self.nuevoBloque(self.ultimoBloque.hashBloque) == None:
            return None
        else:
            bloque = self.ultimoBloque
            print("NUEVO BLOQUE:")
            self.mostrarBloque(bloque)
            return bloque
    
    def anadirBloque(self,bloque):
        self.blockchain.append(bloque)

    def eliminarBloque(self):
        if len(self.blockchain) > 0:
            del self.blockchain[-1]

    def realizarGasto(self, idAdmin, conceptoGasto, dineroAGastar):

        #Verificacion 1: el id de Administrador debe seguir el formato USAL[6 DIGITOS]
        """regexAdmin = re.compile("^USAL[0-9]{6}$")
        if not regexAdmin.search(str(idAdmin)):
            print("El identificador de Administrador [" + str(idAdmin) + "] no es vAlido.")
            return None"""

        # Obtener cantidad de dinero invertido por los pagadores en el concepto 
        dineroInvertido = 0

        # Para cada transacciOn, comprobamos el concepto objetivo
        # Si el concepto coincide con el buscado, se acumula el valor de dinero aportado o gastado(valor negativo)
        for bloque in self.blockchain:
            for key,value in bloque.transaccion.items():
                if (key == "ConceptoPago" or key == "ConceptoGasto") and not conceptoGasto == value:
                    break
                
                if key == "DineroAportado" or key == "DineroGastado":
                    dineroInvertido += value
        
        # VerificaciOn 2: El gasto no puede superar a la aportaciOn de fondos para ese concepto
        if dineroInvertido < dineroAGastar:
            print("ERROR. No se puede gastar mas dinero del invertido por los contribuyentes en este concepto.")
            print("Saldo restante para este concepto: " +  str(dineroInvertido) + "€ | Peticion de Gasto: " + str(dineroAGastar) + "€")
            return None
        
        # Exito: CreaciOn de una nueva transacciOn de gasto a partir de los datos recibidos como parAmetro
        self.nuevaTransaccionGasto(idAdmin, conceptoGasto, dineroAGastar)

        # Comprobar la integridad de la cadena antes de crear el bloque (el Bloque GEnesis debe existir)
        # En caso de Exito, se crea el Bloque y se muestra
        if len(self.blockchain) == 0 or self.nuevoBloque(self.ultimoBloque.hashBloque) == None:
            return None
        else:
            bloque = self.ultimoBloque
            print("NUEVO BLOQUE:")
            self.mostrarBloque(bloque)
            return bloque
        
    def mostrarBlockchain(self):
        for bloque in self.blockchain:
            self.mostrarBloque(bloque)

class BloqueEncoder(JSONEncoder):

    def default(self, object):

        if isinstance(object, Bloque):
            return object.__dict__

        else:
            return json.JSONEncoder.default(self, object)

class BlockchainEncoder(JSONEncoder):

    def default(self, object):

        if isinstance(object, Blockchain):
            data = {}
            data['transaccionNoValidada'] = object.transaccionNoValidada
            data['blockchain'] = [BloqueEncoder().encode(x) for x in object.blockchain]
            return data

        else:
            return json.JSONEncoder.default(self, object)

def BlockchainDecoder(json_string):

    if type(json_string) == str:
        json_string_formatted = json.loads(json_string)
    else:
        json_string_formatted = json_string
    try:
        bloques = []
        #bloques = [Bloque(hashBloqueAnterior=x['hashBloqueAnterior'],transaccion=x['transaccion'],indiceBloque=x['indiceBloque'],send_incognitaDeMinado=x['incognitaDeMinado'],send_hashBloque=x['hashBloque']) for x in json_string_formatted['blockchain']]
        for block in json_string_formatted['blockchain']:
            if type(block) == str:
                x = json.loads(block)
            else:
                x = block
            bloques.append(Bloque(hashBloqueAnterior=x['hashBloqueAnterior'],transaccion=x['transaccion'],indiceBloque=x['indiceBloque'],send_incognitaDeMinado=x['incognitaDeMinado'],send_hashBloque=x['hashBloque']))
        return Blockchain(bloques, json_string_formatted['transaccionNoValidada'])
    except:
        traceback.print_exc() 
        return None

def BloqueDecoder(json_string):
    return Bloque(hashBloqueAnterior=json_string['hashBloqueAnterior'],transaccion=json_string['transaccion'],indiceBloque=json_string['indice'],send_incognitaDeMinado=json_string['incognitaDeMinado'],send_hashBloque=json_string['hashBloque'])