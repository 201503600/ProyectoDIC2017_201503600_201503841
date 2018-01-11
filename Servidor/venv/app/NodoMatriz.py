from ArbolB import ArbolArtista


class NodoMatriz:

    correlativo = 1

    def __init__(self, dato):
        self.dato = dato
        self.artistas = ArbolArtista()
        self.siguiente = None
        self.anterior = None
        self.abajo = None
        self.arriba = None
        self.id = NodoMatriz.correlativo
        NodoMatriz.correlativo += 1

    def getArtistas(self):
        return self.artistas

    def getCorrelativo(self):
        return self.id

    def getDato(self):
        return self.dato

    def getSiguiente(self):
        return self.siguiente

    def getAnterior(self):
        return self.anterior

    def getArriba(self):
        return self.arriba

    def getAbajo(self):
        return self.abajo

    def setArtista(self, artistas):
        self.artistas = artistas

    def setDato(self, dato):
        self.dato = dato

    def setSiguiente(self, siguiente):
        self.siguiente = siguiente

    def setAnterior(self, anterior):
        self.anterior = anterior

    def setArriba(self, arriba):
        self.arriba = arriba

    def setAbajo(self, abajo):
        self.abajo = abajo
