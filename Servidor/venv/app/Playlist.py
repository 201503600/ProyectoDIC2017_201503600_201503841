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

    def queue(self, nodo):
        nuevo = NodoCola(nodo)
        if self.isEmpty():
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.setSiguiente(nuevo)
            nuevo.setAnterior(self.ultimo)
            nuevo.setSiguiente(self.primero)
            self.primero.setAnterior(nuevo)
            self.ultimo = nuevo
        self.size += 1

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
        i = 0
        while actual:
            dot.node(str(i), actual.getNombreCola())
            actual = actual.getSiguiente()
            i += 1
            if actual == self.Primero:
                break
            dot.edges([str(i - 1) + str(i)], constraint='false')
            dot.edges([str(i) + str(i - 1)], constraint='false')
        dot.edges([str(i - 1) + str(0)], constraint='false')
        dot.edges([str(0) + str(i - 1)], constraint='false')
        dot.render(filename="colaCanciones", directory="C:\\Graphs\\", view=True, cleanup=True)
        print dot
