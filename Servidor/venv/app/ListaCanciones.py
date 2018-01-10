from NodoCancion import NodoCancion

import sys
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin'

class ListaCanciones:

    def __init__(self):
        self.head = None
        self.size = 0

    def isEmpty(self):
        return self.head == None

    def add(self, nombre, path):
        nuevo = NodoCancion(nombre, path)
        if self.isEmpty():
            nuevo.setSiguiente(nuevo)
            nuevo.setAnterior(nuevo)
            self.head = nuevo
        else:
            nuevo.setSiguiente(self.head)
            nuevo.setAnterior(self.head.getAnterior())
            self.head.getAnterior().setSiguiente(nuevo)
            self.head.setAnterior(nuevo)
            #self.head = nuevo
        self.size += 1

    def find(self, nombre):
        aux = self.head
        for pos in xrange(0, self.size):
            if aux.getNombre() == nombre:
                return aux
            aux = aux.getSiguiente()
        return

    def delete(self, nombre):
        aux = self.head
        if self.size == 1:
            self.head = None
            self.size = 0
        else:
            for pos in xrange(0,self.size):
                if aux.getNombre() == nombre:
                    aux.getAnterior().setSiguiente(aux.getSiguiente())
                    aux.getSiguiente().setAnterior(aux.getAnterior())
                    self.size -= 1
                    break
                aux = aux.getSiguiente()

    def getSize(self):
        return self.size

    def graph(self):
        dot = Digraph(comment='Lista Canciones')
        dot.format = 'png'
        actual = self.head
        i = 0
        while actual:
            dot.node(str(i), actual.getNombre())
            actual = actual.getSiguiente()
            i += 1
            if actual == self.head:
                break
            dot.edge(str(i - 1), str(i), constraint='false')
            dot.edge(str(i), str(i - 1), constraint='false')
        dot.edge(str(i - 1), str(0), constraint='false')
        dot.edge(str(0), str(i - 1), constraint='false')
        dot.render(filename="listaCanciones", directory="C:\\Graphs\\", view=True, cleanup=True)

    def printCancion(self):
        aux = self.head
        for pos in xrange(0, self.size):
            print aux.getNombre() + ' - ' + aux.getPath()
            aux = aux.getSiguiente()