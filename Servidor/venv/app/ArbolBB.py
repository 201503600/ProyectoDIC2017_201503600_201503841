from NodoAlbum import NodoAlbum


class ArbolAlbum:
    """docstring for ABB"""

    def __init__(self):
        self.raiz = None

    def add(self, nombre):
        if self.raiz == None:
            self.raiz = NodoAlbum(nombre)
        else:
            self.raiz.addAlbum(nombre)

    def graph(self):
        return self.raiz.getDot()

    def getAlbum(self, nombre):
        return self.getAlbumAux(self.raiz, nombre)

    def getAlbumAux(self, actual, nombre):
        if actual == None:
            return None
        if nombre != None:
            if actual.getNombre().lower() == nombre.lower():
                return actual
            if actual.getNombre().lower() < nombre.lower():
                return self.getAlbumAux(actual.getHijoDer(), nombre)
            else:
                return self.getAlbumAux(actual.getHijoIzq(), nombre)

    def getRaiz(self):
        return self.raiz
