from NodoMatriz import NodoMatriz


class ListaFilaMatriz:

    def __init__(self, anchura):
        self.primero = None
        for i in xrange(0, anchura):
            self.push()

    def getPrimero(self):
        return self.primero

    def isEmpty(self):
        return self.primero == None

    def push(self):
        if self.isEmpty():
            self.primero = NodoMatriz(0)
        else:
            nuevo = NodoMatriz(0)
            nuevo.setSiguiente(self.primero)
            self.primero.setAnterior(nuevo)
            self.primero = nuevo
