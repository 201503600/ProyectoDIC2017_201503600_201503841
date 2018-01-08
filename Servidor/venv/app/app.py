import os
#from urllib2 import urlopen, urlparse, Request, URLError
from flask import Flask, session, request, json, jsonify, redirect, url_for
from flask_oauth import OAuth
from CargaMasiva import CargaMasiva
from Reporte import generarImagen, reporteAlbumes, reporteArtistas, reporteCola, reporteGeneral, reporteMatriz, reporteUsuarios, reporteListaCanciones
from Codificador import JsonEncoder
from NodoUsuario import NodoUsuario

# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = '331131262019-1spdas7uih7cv5nnt0l2i7morh9bgg17.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'HCuDz2wwggC9OPD9824CsJGI'
REDIRECT_URI = '/accounts.google.com'  # one of the Redirect URIs from Google APIs console
 
SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.json_encoder = JsonEncoder
app.secret_key = SECRET_KEY
oauth = OAuth()
carga = CargaMasiva()

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

####
###### loginOAuth - loginGoo - authorized - getAccessToken 
######### metodos para OAuth
@app.route('/loginOAuth')
def loginOAuth():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('loginGoo'))
 
    access_token = access_token[0]
    #from urllib2 import Request, urlopen, URLError
 
    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('loginGoo'))
        return res.read()
    obJson = res.read().encode()
    return obJson['email']

@app.route('/loginGoo')
def loginGoo():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('loginOAuth'))
 
@google.tokengetter
def get_access_token():
    return session.get('access_token')

#### METODOS PROPIOS

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

@app.route('/encabezadoAnio', methods=['POST'])
def getEncabezadoAnios():
    return jsonify(carga.getEncabezadoAnios)

@app.route('/encabezadoGenero', methods=['POST'])
def getEncabezadoGeneros():
    return jsonify(carga.getEncabezadoGeneros)

@app.route('/reporteMatriz', methods=['POST'])
def getReportMatriz():
    reporteMatriz(carga.getMatriz())
    return jsonify({})

@app.route('/reporteArtistas', methods=['POST'])
def getReportArtist():
    anio = request.form['anio']
    genero = request.form['genero']
    reporteArtistas(carga.getMatriz(), anio, genero)
    return jsonify({})

@app.route('/reporteAlbumes', methods=['POST'])
def getReportAlbums():
    anio = request.form['anio']
    genero = request.form['genero']
    artista = request.form['artista']
    print 'Anio\t' + str(anio) + '\tGenero\t' + str(genero) + '\tartista\t' + str(artista)
    reporteAlbumes(carga.getMatriz(), anio, genero, artista)
    return jsonify({})

@app.route('/reporteListaCanciones', methods=['POST'])
def getReportListSongs():
    anio = request.form['anio']
    genero = request.form['genero']
    artista = request.form['artista']
    album = request.form['album']
    reporteListaCanciones(carga.getMatriz(), anio, genero, artista, album)
    return jsonify({})

@app.route('/reporteUsuarios', methods=['POST'])
def getReportUsers():
    reporteUsuarios(carga.getUsuario())
    return jsonify({})

@app.route('/reporteQueueUser', methods=['POST'])
def getReportQueueUser():
    username = request.form['username']
    reporteCola(carga.getUsuario(), username)
    return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)