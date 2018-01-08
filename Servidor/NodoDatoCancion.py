class NodoDato:
	def __init__(self, cancion, artista, album, genero, anio):
		self.cancion = cancion
		self.artista = artista
		self.album = album
		self.genero = genero
		self.anio = anio
		self.siguiente = None

	def getCancion(self):
		return self.cancion

	def getArtista(self):
		return self.artista

	def getAlbum(self):
		return self.album

	def getGenero(self):
		return self.genero

	def getAnio(self):
		return self.anio

	def getSiguiente(self):
		return self.siguiente

	def setSiguiente(self, siguiente):
		self.siguiente = siguiente