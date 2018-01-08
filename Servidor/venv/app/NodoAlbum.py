from ListaCanciones import ListaCanciones

import sys
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin'

class NodoAlbum:
    """docstring for Album"""
    correlativo = 1

    def __init__(self, nombre, canciones):
        self.nombre = nombre
        self.canciones = canciones
        self.izquierdo = None
        self.derecho = None
        self.id = NodoAlbum.correlativo
        NodoAlbum.correlativo += 1

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

    def addAlbum(self, nombre, canciones):
        if nombre.lower() < self.nombre.lower():
            if self.izquierdo == None:
                self.izquierdo = NodoAlbum(nombre, canciones)
            else:
                self.izquierdo.addAlbum(nombre, canciones)
        elif nombre.lower() > self.nombre.lower():
            if self.derecho == None:
                self.derecho = NodoAlbum(nombre, canciones)
            else:
                self.derecho.addAlbum(nombre, canciones)
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
            etiqueta = 'Album' + str(self.id) + ' [ label =\"<C0>|' + self.nombre + '<C1>\"];\n'
        if self.izquierdo != None:
            etiqueta += self.izquierdo.getDotNodo() + 'Album' + str(self.id) + ':C0->Album' + str(self.izquierdo.id) + '\n'
        if self.derecho != None:
            etiqueta += self.derecho.getDotNodo() + 'Album' + str(self.id) + ':C1->Album' + str(self.derecho.id) + '\n'
        return etiqueta
