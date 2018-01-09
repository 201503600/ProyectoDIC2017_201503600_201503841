from NodoDatoCancion import NodoDato


class ListaDato:

    def __init__(self):
        self.primero = None
        self.size = 0

    def isEmpty(self):
        return self.size == 0

    def insert(self, cancion, artista, album, genero, anio, path):
        nuevo = NodoDato(cancion, artista, album, genero, anio, path)
        nuevo.setSiguiente(self.primero)
        self.primero = nuevo
        self.size += 1

    def getAt(self, index):
        aux = self.primero
        if index < self.size:
            for i in xrange(0, index + 1):
                aux = aux.getSiguiente()
            return aux
        return None

    def getSize(self):
        return self.size
