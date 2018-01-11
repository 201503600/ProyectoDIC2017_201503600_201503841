import os
import random
from urllib2 import urlopen, urlparse, Request, URLError
from flask import Flask, session, request, json, jsonify, redirect, url_for
from flask_oauth import OAuth
from MatrizDispersa import Matriz
from FilaMatriz import ListaFilaMatriz
from NodoUsuario import NodoUsuario
from NodoDatoCancion import NodoDato
from Reproductor import Reproductor
from CargaMasiva import CargaMasiva, Buscador
from Codificador import JsonEncoder
from Reporte import generarImagen, reporteAlbumes, reporteArtistas, reporteCola, reporteGeneral, reporteMatriz, reporteUsuarios, reporteListaCanciones

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
loginoauth = 'None'

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
    global loginoauth
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
    obJson = res.read()
    nombre = str(obJson).split(',')[1].split(':')[1].replace('\"', '', 2)
    carga.getUsuario().pushUsuario(nombre, 'google')
    if carga.getUsuario().find(nombre):
        session['loginoauth'] = nombre
        loginoauth = nombre
        return 'Usuario registrado'
    loginoaut = 'Error'
    session['loginoauth'] = 'Error'
    return 'Ocurrio un error'

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

@app.route('/verifyUserOAuth', methods=['POST'])
def verifyUserOAuth():
    global loginoauth
    if loginoauth == 'None':
        return 'False'
    elif loginoauth == 'Error':
        return 'Error'
    else:
        return loginoauth
    # if 'loginoauth' in session:
    #     loginoauth = session['loginoauth']
    #     session.pop('loginoauth', None)
    #     if loginoauth == 'Error':
    #         return 'Error'
    #     else:
    #         return loginoauth
    # return 'False'

@app.route('/carga_archivo', methods=['POST'])
def cargar():
    path = request.form['path']
    print path
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
    return jsonify(carga.getEncabezadoAnios())

@app.route('/encabezadoGenero', methods=['POST'])
def getEncabezadoGeneros():
    return jsonify(carga.getEncabezadoGeneros())

@app.route('/reporteMatriz', methods=['POST'])
def getReportMatriz():
    reporteMatriz(carga.getMatriz())
    return jsonify({})

@app.route('/reporteArtistas', methods=['POST'])
def getReportArtist():
    anio = request.form['anio']
    genero = request.form['genero']
    try:
        reporteArtistas(carga.getMatriz(), anio, genero)
    except Exception as e:
        print 'Ocurrio un error:\t' + str(e)
    return jsonify({})

@app.route('/reporteAlbumes', methods=['POST'])
def getReportAlbums():
    anio = request.form['anio']
    genero = request.form['genero']
    artista = request.form['artista']
    #print 'Anio\t' + str(anio) + '\tGenero\t' + str(genero) + '\tartista\t' + str(artista)
    try:
        reporteAlbumes(carga.getMatriz(), anio, genero, artista)
    except Exception as e:
        print 'Ocurrio un error:\t' + str(e)
    return jsonify({})

@app.route('/reporteListaCanciones', methods=['POST'])
def getReportListSongs():
    anio = request.form['anio']
    genero = request.form['genero']
    artista = request.form['artista']
    album = request.form['album']
    try:
        reporteListaCanciones(carga.getMatriz(), anio, genero, artista, album)
    except Exception as e:
        print 'Ocurrio un error:\t' + str(e)
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

@app.route('/canciones', methods=['POST'])
def getListSongs():
    return jsonify(carga.getDatos())

@app.route('/agregarCola', methods=['POST'])
def addCola():
    anio = request.form['anio']
    genero = request.form['genero']
    artista = request.form['artista']
    album = request.form['album']
    cancion = request.form['cancion']
    username = request.form['username']
    try:
        nodoCancion = carga.getMatriz().getArtistas(anio, genero).search(artista).getAlbumes().getAlbum(album).getCanciones().find(cancion)
        nodo = carga.getUsuario().getCola(username).queue(nodoCancion, NodoDato(cancion, artista, album, genero, anio, nodoCancion.getPath()))
    except Exception as e:
        print 'Ocurrio un error:\t' + str(e)
        return jsonify({})
    return jsonify(nodo)

@app.route('/afterSong', methods=['POST'])
def afterSong():
    username = request.form['username']
    return jsonify(carga.getUsuario().getCola(username).peekAfter())

@app.route('/beforeSong', methods=['POST'])
def beforeSong():
    username = request.form['POST']
    nodo = carga.getUsuario().getCola(username).peekBefore()
    print nodo
    return jsonify(nodo)

@app.route('/getSongsByArtist', methods=['POST'])
def getSongsByArtist():
    nombreArtista = request.form['artista']
    buscador = Buscador(carga.getMatriz())
    buscador.getByArtist(nombreArtista)
    #reproductor.setListaArtista(buscador.getCanciones())
    return jsonify(buscador.getCanciones())

@app.route('/getSongsByAlbum', methods=['POST'])
def getSongsByAlbum():
    nombreAlbum = request.form['album']
    buscador = Buscador(carga.getMatriz())
    buscador.getByAlbum(nombreAlbum)
    #reproductor.setListaAlbum(buscador.getCanciones())
    return jsonify(buscador.getCanciones())

@app.route('/getSongsByGender', methods=['POST'])
def getSongsByGender():
    genero = request.form['genero']
    buscador = Buscador(carga.getMatriz())
    buscador.getByGender(genero)
    return jsonify(buscador.getCanciones())

@app.route('/getSongsByYear', methods=['POST'])
def getSongsByYear():
    anio = request.form['anio']
    buscador = Buscador(carga.getMatriz())
    buscador.getByYear(anio)
    return jsonify(buscador.getCanciones())

@app.route('/getSongShuffle', methods=['POST'])
def getSongShuffle():
    return jsonify(carga.getDatos().getAt(random.randint(-1, carga.getDatos().getSize() - 1)))

@app.route('/search', methods=['POST'])
def search():
    cadena = request.form['cadena']
    buscador = Buscador(carga.getMatriz())
    buscador.getByArtistAlbumSong(cadena)
    return jsonify(buscador.getCanciones())

if __name__ == '__main__':
    app.run(debug=True)