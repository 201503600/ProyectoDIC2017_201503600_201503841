import os
from flask import Flask, session, request, jsonify
from CargaMasiva import CargaMasiva
from Reporte import generarImagen, reporteAlbumes, reporteArtistas, reporteCola, reporteGeneral, reporteMatriz, reporteUsuarios, reporteListaCanciones
from Codificador import JsonEncoder
from NodoUsuario import NodoUsuario

app = Flask(__name__)
app.json_encoder = JsonEncoder
app.secret_key = os.urandom(20)
carga = CargaMasiva()

@app.route('/')
def main():
   # prueba = NodoUsuario('carlos', '1234')
    return jsonify({})

@app.route('/carga_archivo', methods=['POST'])
def cargar():
    path = request.form['path']
    carga.analizarXML(path)
    return jsonify({})

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = carga.getUsuario().login(username, password)
    if isinstance(user, NodoUsuario):
        session['username'] = user
        stringJson = jsonify(user)
        return stringJson
    else:
        return jsonify({})

@app.route('/logout', methods=['POST'])
def logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({})

@app.route('/encabezadoAnio')
def getEncabezadoAnios():
    return jsonify(carga.getEncabezadoAnios)

@app.route('/encabezadoGenero')
def getEncabezadoGeneros():
    return jsonify(carga.getEncabezadoGeneros)

if __name__ == '__main__':
    app.run(debug=True)