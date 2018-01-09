class NodoCola:

    def __init__(self, nodoCancion, nodoDato):
        self.nodo = nodoCancion
        self.datos = nodoDato
        self.siguiente = None
        self.anterior = None

    def getNodo(self):
        return self.nodo

    def getDatos(self):
        return self.datos

    def getSiguiente(self):
        return self.siguiente

    def getAnterior(self):
        return self.snterior

    def setAnterior(self, anterior):
        self.anterior = anterior

    def setSiguiente(self, siguiente):
        self.siguiente = siguiente