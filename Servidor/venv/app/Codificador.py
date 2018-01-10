from flask.json import JSONEncoder
from NodoUsuario import NodoUsuario
from NodoDatoCancion import NodoDato
from NodoCola import NodoCola
from NodoCancion import NodoCancion
from ListaDatoCancion import ListaDato

class JsonEncoder(JSONEncoder):

	def default(self, obj):
		if isinstance(obj, NodoUsuario):
			return {'nombre':obj.getNombre(), 'contrasenia':obj.getPass()}
		elif isinstance(obj, NodoDato):
			return {'cancion':obj.getCancion(), 'artista':obj.getArtista(), 'album':obj.getAlbum(), 'genero':obj.getGenero(), 'anio':obj.getAnio(), 'path':obj.getPath()}
		elif isinstance(obj, ListaDato):
			canciones = []
			for pos in xrange(0,obj.getSize()):
				if obj.getAt(pos) != None:
					canciones.append(self.default(obj.getAt(pos)))
			return {'canciones':canciones}
		elif isinstance(obj, NodoCola):
			return self.default(obj.getDatos())
		return super(JsonEncoder, self).default(obj)
