from Playlist import Playlist

class NodoUsuario:

    def __init__(self, nombre, contrasenia):
        self.nombre = nombre
        self.contrasenia = contrasenia
        self.siguiente = None
        self.anterior = None
        self.canciones = Playlist()

    def getColaCanciones(self):
        return self.canciones
        
    def getNombre(self):
        return  self.nombre

    def getPass(self):
        return self.contrasenia

    def getSiguiente(self):
        return self.siguiente

    def getAnterior(self):
        return self.anterior

    def setSiguiente(self, siguiente):
        self.siguiente = siguiente

    def setAnterior(self, anterior):
        self.anterior = anterior
