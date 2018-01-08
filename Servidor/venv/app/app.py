from flask import Flask, session, request
from CargaMasiva import CargaMasiva

app = Flask(__name__)
carga = CargaMasiva()

@app.route('/')
def main():
    return 'json.dumps(carga)'
	#return jsonify(carga)

@app.route('/carga_archivo', methods=['POST'])
def cargar():
    path = request.form['path']
    carga.analizarXML(path)
    usuarios = carga.getUsuario()

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = carga.getUsuario().login(username, password)
    if isinstance(user, NodoUsuario):
        session['username'] = user
        stringJson = json.dumps(user)
        return stringJson
    else:
        return ''

if __name__ == '__main__':
    app.run(debug=True)