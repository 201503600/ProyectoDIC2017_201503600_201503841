class NodoCancion():

    def __init__(self, nombre, path):
        self.nombre = nombre
        self.path = path
        self.siguiente = None
        self.anterior = None

    def getNombre(self):
        return self.nombre

    def getPath(self):
        return self.path

    def getSiguiente(self):
        return self.siguiente

    def getAnterior(self):
        return self.anterior

    def setSiguiente(self, siguiente):
        self.siguiente = siguiente

    def setAnterior(self, anterior):
        self.anterior = anterior
