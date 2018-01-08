from flask.json import JSONEncoder
from NodoUsuario import NodoUsuario
from NodoMatriz import NodoMatriz
from NodoDatoCancion import NodoDato
from NodoCola import NodoCola
from NodoCancion import NodoCancion
from NodoAlbum import NodoAlbum

class JsonEncoder(JSONEncoder):

	def default(self, obj):
		if isinstance(obj, NodoUsuario):
			return {'nombre':obj.getNombre(), 'contrasenia':obj.getPass()}
		elif isinstance(obj, NodoMatriz):
			return {'dato':obj.getDato()}
		elif isinstance(obj, NodoDato):
			return {}
		elif isinstance(obj, NodoCola):
			return {}
		elif isinstance(obj, NodoCancion):
			return {}
		elif isinstance(obj, NodoAlbum):
			return {}
		return super(JsonEncoder, self).default(obj)
