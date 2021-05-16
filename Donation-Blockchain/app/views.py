from flask import render_template, request, redirect, jsonify, url_for, flash
from app import app
from flask import jsonify
from app import static_data as sd
import requests
import hashlib
from app import view_functions as vf
import json
from options import OptionsData
from blockchain import BloqueDecoder, BlockchainDecoder, BlockchainEncoder
import traceback 
from hashlib import sha256
import multidifusion as md

###################################################################
#                   VISTAS DE LA PÁGINA
###################################################################
"""
Página de inicio de la aplicación cliente.
"""

@app.route("/",methods=["GET","POST"])
def index():
    
    # Si es un método POST 
    if request.method == "POST":
    
        # Recoger los valores del formulario y comprueba de que están todos
        valores = vf.index_post_args_check(request)
        if not valores:
            flash("Error: el DNI es incorrecto.","Warning")
            return redirect(request.url)
        try:

<<<<<<< HEAD
            sd.blockchain_anterior = sd.blockchain
            sd.saldo_anterior = sd.saldo
            sd.destinado_anterior= sd.destinado
            sd.tabla_anterior = sd.tabla

=======
>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9
            # Si todos los nodos devuelven un OK, registramos la nueva transaccion en nuestra blockchain
            bloque = sd.blockchain.realizarPago(valores['DNI'],valores['ConceptoPago'],valores['DineroAportado'])

            # Si la cadena está vacía
            if bloque == None:
                flash("Error: la cadena está vacía","Warning")
                return redirect(url_for("blockchain"))

            # En caso contrario
            else:
                respuesta = md.multidifundirPago(valores,sd)
<<<<<<< HEAD

                # En caso de error
                if respuesta == "ERROR":
                    # Restauramos la blockchain
                    sd.blockchain = sd.blockchain_anterior

                    # Llamamos al protocolo de recuperación de la blockchain
                    md.protocoloRecuperacionBlockchain(sd)

=======
                if respuesta == "ERROR":
>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9
                    flash("El resto de nodos no han confirmado el bloque.","Danger")
                    return redirect(request.url)
                else:
                    # Añadimos los valores a la tabla a mostrar
                    vf.actualizarDatos(valores,sd) 
                    flash("Bloque añadido","Success")
                    # Redirige a la página de blockchain
                    return redirect(url_for("blockchain"))

        except:
            traceback.print_exc() 
            flash("Ha ocurrido un error interno.","Warning")
            return redirect(request.url)

    # Tanto para GET como para POST, renderizo la página principal
    return render_template("index.html", pay_options = OptionsData.pay_options, taxes_options = OptionsData.spend_options)

"""
Vista del administrador para gestionar Pagos
"""

@app.route("/admin",methods=['GET','POST'])
def admin():

    # si es una petición POST, significa que está haciendo un GASTO
    if request.method == "POST":

        # Recogemos los valores de la página
        valores = vf.admin_post_args_check(request)
        if not valores:
            flash("Error: los datos introducidos no son correctos.","Warning")
            return redirect(request.url)

        # Realizamos la transacción en nuestra blockchain y la enviamos a los nodos
<<<<<<< HEAD
        sd.blockchain_anterior = sd.blockchain
        sd.saldo_anterior = sd.saldo
        sd.destinado_anterior= sd.destinado
        sd.tabla_anterior = sd.tabla
        bloque = sd.blockchain.realizarGasto(valores['IDAdministrador'],valores['ConceptoGasto'],valores['DineroGastado'])

        # Si la cadena está vacía
        if bloque == None:
            flash("Error: estás intentando gastar de más en un concepto.","Warning")
            return redirect(request.url)
=======
>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9

        bloque = sd.blockchain.realizarGasto(valores['IDAdministrador'],valores['ConceptoGasto'],valores['DineroGastado'])

<<<<<<< HEAD
            # Multidifundimos el bloque a los nodos de la red
            respuesta = md.multidifundirGasto(valores,sd)

            # En caso de que haya habido un error
            if respuesta == "ERROR":

                # Restauramos la blockchain
                sd.blockchain = sd.blockchain_anterior
                sd.saldo = sd.saldo_anterior
                sd.destinado = sd.destinado_anterior
                sd.tabla = sd.tabla_anterior
                # Llamamos al protocolo de recuperación de la blockchain
                md.protocoloRecuperacionBlockchain(sd)

=======
        # Si la cadena está vacía
        if bloque == None:
            flash("Error: estás intentando gastar de más en un concepto.","Warning")
            return redirect(request.url)

        # En caso contrario
        else:

            # Multidifundimos el bloque a los nodos de la red
            respuesta = md.multidifundirGasto(valores,sd)
            if respuesta == "ERROR":
>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9
                flash("Error: no todos los nodos han confirmado la transaccion.","warning")
                return redirect(request.url)
            else:
                # En caso de que se haya multidifundido con éxito, se lo indicamos
                vf.actualizarDatos(valores,sd)
                flash("Bloque añadido","Success")
                return redirect(url_for("blockchain"))

    # Si es una petición GET, significa que está intentando acceder al panel de administrador
    else:

        try:
                
            # Si está registrado
            if sd.register == True:
                return render_template("admin.html",spend_options=OptionsData.spend_options,saldo=sd.saldo, destinado=sd.destinado)

            # En caso contrario, lo redirigimos a index
            else:
                if sd.intentos > 0:
                    flash("Estás intentando acceder sin registrarte. Tienes " + str(sd.intentos) + " intentos más.", "Danger")
                    sd.intentos = sd.intentos - 1
                else:
                    flash("Lo has intentado demasiadas veces.", "Danger")
                return redirect(url_for("index"))
        except:
            traceback.print_exc() 


"""
Vista de la tabla de blockchain
"""
@app.route("/blockchain",methods=['GET','POST'])
def blockchain():
<<<<<<< HEAD
=======
    print(sd.tabla)
    sd.blockchain.mostrarBlockchain()
>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9
    return render_template("blockchain.html",tabla=sd.tabla, trans=[],saldo=sd.saldo,destinado=sd.destinado)



###################################################################
#          FUNCIONES DE MANEJO DE LOS NODOS EN LA RED             #
###################################################################

"""
Añade a un nuevo nodo a la red y comunica al resto de nodos que tienen que añadir a ese nodo
a su agenda
Acepta métodos GET
"""
@app.route("/unirse_red/<ip>/<puerto>",methods=["GET"])
def unirse_red(ip,puerto):

    # Si alguno de los argumentos es Nulo, devuelvo un invalido
    if ip == None or puerto == None:
        return "Invalid data", 400

    # En caso contrario
    else:

        # Creo un nuevo nodo
        nuevo_nodo = {
            "ip":ip, 
            "puerto":puerto
        }

        # Comunico el nuevo nodo al resto de nodos
        try:
            for nodo in sd.agenda:
                if nodo['ip'] != sd.ip_cliente or nodo['puerto'] != sd.puerto_cliente:
                    vf.comunicar_nuevo_nodo(nodo['ip'], nodo['puerto'], ip, puerto)
<<<<<<< HEAD

            # Si el nuevo nodo no está en mi agenda, lo añado
            if nuevo_nodo not in sd.agenda:
                sd.agenda.append(nuevo_nodo)

=======

            # Si el nuevo nodo no está en mi agenda, lo añado
            if nuevo_nodo not in sd.agenda:
                sd.agenda.append(nuevo_nodo)

>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9
            # Devuelvo la agenda de los nodos
            return jsonify({'agenda':sd.agenda, 'blockchain':json.dumps(sd.blockchain, default=lambda o: o.__dict__), 'saldo':sd.saldo, 'destinado':sd.destinado, 'tabla': sd.tabla}), 200
        except:
            return "ERROR"


"""
Método que se encargar de agregar el nodo que le comunique el coordinador
a su agenda de nodos de la red.
"""
@app.route("/anadir_nodo_red/<ip>/<puerto>",methods=["POST"])
def anadir_nodo_red(ip,puerto):

    # Creo el nodo con los parámetros que se me han indicado
    nuevo_nodo = {
        "ip":ip, 
        "puerto":puerto
    }

    # Si el nodo no está en mi agenda, lo añado
    if nuevo_nodo not in sd.agenda:
        sd.agenda.append(nuevo_nodo)

    # Devuelvo un OK
    return "OK", 200

"""
Elimina a un nodo de la red de nodos.
En caso de que se caiga el nodo coordinador, indica quien será el nuevo coordinador
"""
@app.route("/eliminar_nodo_red/<ip>/<puerto>/<ip_coordinador>/<puerto_coordinador>",methods=["POST"])
def eliminar_nodo_red(ip,puerto,ip_coordinador,puerto_coordinador):

    # Creo un diccionario con el nodo a eliminar
    nodo_a_eliminar = {
        "ip":ip, 
        "puerto":puerto
    }

    # Si el nodo está en mi lista, lo elimino
    if nodo_a_eliminar in sd.agenda: 
        sd.agenda.remove(nodo_a_eliminar)
    if ip_coordinador != None and puerto_coordinador != None:
        sd.ip_coordinador = ip_coordinador
        sd.puerto_coordinador = puerto_coordinador        

    # Devuelvo un OK
    return "OK", 200

###################################################################
#                VISTAS PARA EL MANEJO DE ERRORES                 #
###################################################################
"""
Muestra la vista para el manejo de errores 404
"""
@app.errorhandler(404)
def not_found(error):
    return render_template("not_found.html"), 404


"""
Muestra la vista para el manejo de errores 500
"""
@app.errorhandler(500)
def down_server(error):
    return render_template("down_server.html"), 500

###################################################################
#               FUNCIONES PARA EL MANEJO DEL BLOCKCHAIN           #
###################################################################

"""
Recibe un bloque una vez que alguien ha actualizado su blockchain
"""
@app.route("/recibir_bloque",methods=["POST"])
def recibir_bloque():

    # Comprobamos que recibimos un bloque 
    if 'bloque' in request.args and 'blockchain' in request.args:


        # Lo cargamos en formato json
        bloque = json.loads(request.args['bloque'])
        blockchain_recibida = json.loads(request.args['blockchain'])
<<<<<<< HEAD

        sd.blockchain_anterior = sd.blockchain
=======
>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9

        if bloque['tipoTransaccion'] == "pago":
            # Añadimos los nuevos datos a la tabla de valores que se van a mostrar
            valores = {
                "tipoTransaccion":bloque['tipoTransaccion'],
                "DNI":bloque['DNI'],
                "ConceptoPago":bloque['ConceptoPago'],
                "DineroAportado":int(bloque['DineroAportado'])
            }
<<<<<<< HEAD
            resultado =  sd.blockchain.realizarPago(valores['DNI'],valores["ConceptoPago"],valores["DineroAportado"])
=======
            sd.blockchain.realizarPago(valores['DNI'],valores["ConceptoPago"],valores["DineroAportado"])
>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9
        else:

            # Añadimos los nuevos datos a la tabla de valores que se van a mostrar
            valores = {
                "tipoTransaccion":bloque['tipoTransaccion'],
                "IDAdministrador":bloque['IDAdministrador'],
                "ConceptoGasto":bloque['ConceptoGasto'],
                "DineroGastado":int(bloque['DineroGastado'])
            }
<<<<<<< HEAD
            resultado = sd.blockchain.realizarGasto(valores['IDAdministrador'],valores["ConceptoGasto"],valores["DineroGastado"])

        if sd.blockchain.hashBlockchain == blockchain_recibida and resultado != None:
=======
            sd.blockchain.realizarGasto(valores['IDAdministrador'],valores["ConceptoGasto"],valores["DineroGastado"])

        #if vf.getsha256str(sd.blockchain) == blockchain_recibida:
        #if sd.blockchain.areEqual(blockchain_recibida):
        if sd.blockchain.hashBlockchain == blockchain_recibida:
>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9
            if valores['tipoTransaccion'] == 'pago':
                sd.saldo[bloque['ConceptoPago']] += int(bloque['DineroAportado'])
            else:
                sd.saldo[bloque['ConceptoGasto']] -= int(bloque['DineroGastado'])
                sd.destinado[bloque['ConceptoGasto']] += int(bloque['DineroGastado'])
            sd.tabla.append(valores)
            # Devolvemos OK
            return "OK", 200
        else:
            sd.blockchain = sd.blockchain_anterior
            sd.saldo = sd.saldo_anterior
            sd.destinado = sd.destinado_anterior
            sd.tabla = sd.tabla_anterior
            return "ERROR", 400

    # En caso contrario, devolvemos un 400
    else:
        return "Necesito un bloque", 400

"""
Acción a la que se llama cuando no se ha confirmado el último bloque y se tiene que eliminar
"""
@app.route("/eliminar_ultimo_bloque", methods=["POST"])
def eliminar_ultimo_bloque():
<<<<<<< HEAD
    #sd.blockchain.eliminarBloque()
    sd.blockchain = sd.blockchain_anterior
    sd.saldo = sd.saldo_anterior
    sd.destinado = sd.destinado_anterior
    sd.tabla = sd.tabla_anterior
    return "OK"

@app.route("/recibir_blockchain",methods=["POST"])
def recibir_blockchain():
    if 'blockchain' in request.args:
        sd.blockchain = BlockchainDecoder(json.loads(request.args['blockchain']))

@app.route("/pedir_blockchain",methods=["GET"])
def pedir_blockchain():
    return json.dumps(sd.blockchain, default=lambda o: o.__dict__)
    
=======
    sd.blockchain.eliminarBloque()
    return "OK"

>>>>>>> 0809871c897f9fe3c22511b7d0ff6dace95908b9
###################################################################
#               FUNCIONES PARA LOGGING ADMINISTRADOR              #
###################################################################

@app.route("/amiadmin")
def amiadmin():
    if sd.register == True:
        return json.dumps(dict(
            state="True",
        ))
    else:
        return json.dumps(dict(
            state="False",
        ))

@app.route("/login",methods=["GET","POST"])
def login():
    # En el caso de que sea
    if 'adminPassword' in request.values:
        if sd.intentos > 0:
            if request.values['adminPassword'] in sd.adminPassword:
                sd.register = True
                sd.id_login = request.values['adminPassword']
                return redirect(url_for("admin"))
            else:
                flash("Contraseña incorrecta. Tienes " + str(sd.intentos) + " intentos más.", "warning")
                sd.intentos = sd.intentos - 1
                return redirect(request.url)
        else:
            flash("Intentos de inicio de sesión superados.", "warning")
            return redirect(request.url)

###################################################################
#               FUNCIONES PARA VER TRANSACCIONES                  #
###################################################################

@app.context_processor
def my_utility_processor():

    def getsha256str(input):
        return sha256(input.encode('utf-8')).hexdigest()

    return dict(getsha256str=getsha256str)
    
@app.route("/ver_transacciones",methods=["GET","POST"])
def ver_transacciones():
    trans = []
    if 'docIdent' in request.values:
        doc = request.values['docIdent']
    else:
        return redirect(request.url)
    for item in sd.tabla:
        if 'DNI' in item and item['DNI']==doc:
            trans.append(item)
    return render_template("blockchain.html", tabla=sd.tabla, trans = trans,saldo=sd.saldo, destinado=sd.destinado)