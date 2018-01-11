from Playlist import Playlist
from ListaDatoCancion import ListaDato
from NodoCancion import NodoCancion
class NodoUsuario:

    def __init__(self, nombre, contrasenia):
        self.nombre = nombre
        self.contrasenia = contrasenia
        self.siguiente = None
        self.anterior = None
        self.canciones = Playlist()

    def getColaCanciones(self):
        return self.canciones

    def setColaCanciones(self, canciones):
        if isinstance(canciones, ListaDato):
            aux = canciones.getAt(0)
            while aux != None:
                self.canciones.queue(NodoCancion(aux.getCancion(), aux.getPath()), aux)
                aux = aux.getSiguiente()
        else:
            self.canciones = canciones
        
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
