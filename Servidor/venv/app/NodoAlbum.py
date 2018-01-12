from ListaCanciones import ListaCanciones

import sys
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin'

class NodoAlbum:
    """docstring for Album"""
    correlativo = 1

    def __init__(self, nombre):
        self.nombre = nombre
        self.canciones = ListaCanciones()
        self.izquierdo = None
        self.derecho = None
        self.padre = None
        self.id = NodoAlbum.correlativo
        NodoAlbum.correlativo += 1

    def getPadre(self):
        return self.padre

    def setPadre(self, padre):
        self.padre = padre

    def getCanciones(self):
        return self.canciones

    def getNombre(self):
        return self.nombre

    def getHijoIzq(self):
        return self.izquierdo

    def getHijoDer(self):
        return self.derecho

    def getCorrelativo(self):
        return self.id

    def addAlbum(self, nombre):
        if nombre.lower() < self.nombre.lower():
            if self.izquierdo == None:
                self.izquierdo = NodoAlbum(nombre)
                self.izquierdo.padre = self
            else:
                self.izquierdo.addAlbum(nombre)
        elif nombre.lower() > self.nombre.lower():
            if self.derecho == None:
                self.derecho = NodoAlbum(nombre)
                self.derecho.padre = self
            else:
                self.derecho.addAlbum(nombre)
        else:
            print 'No se permiten valores duplicados'

    def getDot(self):
        dot = 'digraph arbolABB{\nrankdir=TB;\nnode [shape = record, style=filled, fillcolor=seashell2];\n' + self.getDotNodo() + '}\n'
        print dot
        return dot

    def getDotNodo(self):
        etiqueta = ''
        if self.izquierdo == None and self.derecho == None:
            etiqueta = 'Album' + str(self.id) + ' [ label =\"' + self.nombre + '\"];\n'
        else:
            etiqueta = 'Album' + str(self.id) + ' [ label =\"<C0>|<C1>' + self.nombre + '|<C2>\"];\n'
        if self.izquierdo != None:
            etiqueta += self.izquierdo.getDotNodo() + 'Album' + str(self.id) + ':C0->Album' + str(self.izquierdo.id) + '\n'
        if self.derecho != None:
            etiqueta += self.derecho.getDotNodo() + 'Album' + str(self.id) + ':C2->Album' + str(self.derecho.id) + '\n'
        return etiqueta

    def printAlbum(self, nodo):
        print nodo.getNombre()
        print nodo.getCanciones().printCancion()
        if nodo.getHijoIzq() != None:
            self.printAlbum(nodo.getHijoIzq())
        if nodo.getHijoDer() != None:
            self.printAlbum(nodo.getHijoDer())
