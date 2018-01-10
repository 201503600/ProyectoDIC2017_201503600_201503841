from NodoCola import NodoCola
import sys
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin'
from graphviz import Digraph


class Playlist:

    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.actual = None
        self.size = 0

    def isEmpty(self):
        return self.size == 0

    def queue(self, nodo, datos):
        nuevo = NodoCola(nodo, datos)
        if self.isEmpty():
            nuevo.setSiguiente(nuevo)
            nuevo.setAnterior(nuevo)
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.setSiguiente(nuevo)
            nuevo.setAnterior(self.ultimo)
            nuevo.setSiguiente(self.primero)
            self.primero.setAnterior(nuevo)
            self.ultimo = nuevo
        self.size += 1
        return nuevo.getDatos()

    def getPrimero(self):
        return self.primero.getDatos()

    def peekAfter(self):
        if self.isEmpty():
            return None
        if self.actual == None:
            self.actual = self.primero
        else:
            self.actual = self.actual.siguiente
        return self.actual

    def peekBefore(self):
        if self.isEmpty():
            return None
        if self.actual == None:
            self.actual = self.primero
        else:
            self.actual = self.actual.anterior
        return self.actual

    def graph(self):
        dot = Digraph(comment='Cola Circular de Canciones')
        dot.format = 'png'
        actual = self.primero
        if self.size == 1:
            dot.node(str(0), 'Artista - ' + actual.getDatos().getArtista() + '\nCancion: ' + actual.getDatos().getCancion())
            dot.edge(str(0), str(0), constraint='false')
        elif self.size == 2:
            i = 0
            while actual:
                dot.node(str(i), 'Artista - ' + actual.getDatos().getArtista() + '\nCancion: ' + actual.getDatos().getCancion())
                actual = actual.getSiguiente()
                i += 1
                if actual == self.primero:
                    break
                dot.edge(str(i), str(i - 1), constraint='false')
            dot.edge(str(0), str(i - 1), constraint='false')
        elif self.size > 2:
            i = 0
            while actual:
                dot.node(str(i), 'Artista - ' + actual.getDatos().getArtista() + '\nCancion: ' + actual.getDatos().getCancion())
                actual = actual.getSiguiente()
                i += 1
                if actual == self.primero:
                    break
                dot.edge(str(i - 1), str(i), constraint='false')
                dot.edge(str(i), str(i - 1), constraint='false')
            dot.edge(str(i - 1), str(0), constraint='false')
            dot.edge(str(0), str(i - 1), constraint='false')
        dot.render(filename="colaCanciones", directory="C:\\Graphs\\", view=True, cleanup=True)
        print dot
