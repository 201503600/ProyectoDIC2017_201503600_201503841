class Nodo_Cola:

    def __init__(self, nodoCancion):
        self.nodo = nodoCancion
        self.siguiente = None
        self.anterior = None

    def getNodo(self):
        return self.nodo

    def getSiguiente(self):
        return self.siguiente

    def getAnterior(self):
        return self.snterior

    def setAnterior(self, anterior):
        self.anterior = anterior

    def setSiguiente(self, siguiente):
        self.siguiente = siguiente