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

    def deleteSong(self, anio, genero, artista, album, nombre):
        aux = self.primero
        anterior = aux
        for i in xrange(0, self.size):
            if aux.getAnio() == anio and aux.getGenero() == genero and aux.getArtista() == artista and aux.getAlbum() == album and aux.getCancion() == nombre:
                if aux == anterior:
                    self.primero = aux.getSiguiente()
                else:
                    anterior.setSiguiente(aux.getSiguiente())
                break
            if aux.getSiguiente() == None:
                break
            anterior = aux
            aux = aux.getSiguiente()

    def deleteArtist(self, anio, genero, nombre):
        aux = self.primero
        anterior = aux
        for i in xrange(0, self.size):
            if aux.getArtista() == nombre and aux.getAnio() == anio and aux.getGenero() == genero:
                if aux == anterior:
                    self.primero = aux.getSiguiente()
                else:
                    anterior.setSiguiente(aux.getSiguiente())
                break
            if aux.getSiguiente() == None:
                break
            anterior = aux
            aux = aux.getSiguiente()

    def deleteAnioGenero(self, anio, genero):
        aux = self.primero
        anterior = aux
        for i in xrange(0, self.size):
            if aux.getAnio() == anio and aux.getGenero() == genero:
                if aux == anterior:
                    self.primero = aux.getSiguiente()
                else:
                    anterior.setSiguiente(aux.getSiguiente())                
            if aux.getSiguiente() == None:
                break
            anterior = aux
            aux = aux.getSiguiente()

    def getAt(self, index):
        aux = self.primero
        if index < self.size:
            for i in xrange(0, index + 1):
                if aux.getSiguiente() != None:
                    aux = aux.getSiguiente()
                else:
                    break
            return aux
        return None

    def getSize(self):
        return self.size
