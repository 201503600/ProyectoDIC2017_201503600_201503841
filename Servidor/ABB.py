from Album import Album


class ABB:
    """docstring for ABB"""

    def __init__(self):
        self.raiz = None

    def add(self, nombre, listaCanciones):
        if self.raiz == None:
            self.raiz = Album(nombre, listaCanciones)
        else:
            self.raiz.addAlbum(nombre, listaCanciones)

    def graph(self):
        return self.raiz.getDot()

    def getAlbum(self, nombre):
        return self.getAlbumAux(self.raiz, nombre)

    def getAlbumAux(self, actual, nombre):
        if actual == None:
            return None
        if actual.getNombre() == nombre:
            return actual
        if actual.getNombre() < nombre:
            return self.getAlbumAux(actual.getHijoDer(), nombre)
        else:
            return self.getAlbumAux(actual.getHijoIzq(), nombre)
