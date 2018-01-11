from NodoUsuario import NodoUsuario
import sys
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin'


class ListaUsuarios:

    def __init__(self):
        self.inicio = None
        self.fin = None
        self.size = 0

    def isEmpty(self):
        return self.inicio == None

    def pushUsuario(self, nombre, contrasenia):
        nuevo = NodoUsuario(nombre, contrasenia)
        if self.isEmpty():
            self.inicio = nuevo
            self.fin = nuevo
        else:
            nuevo.setSiguiente(self.inicio)
            self.inicio.setAnterior(nuevo)
            self.inicio = nuevo
        self.size += 1

    def deleteUsuario(self, nombre):
        if self.size == 1 and self.inicio.getNombre() == nombre:
            self.inicio = None
            self.fin = None
            self.size = 0
        else:
            aux = self.inicio
            while aux != None:
                if aux.getNombre() == nombre:
                    if aux == self.inicio:
                        self.inicio = aux.getSiguiente()
                        self.inicio.setAnterior(None)
                        aux.setSiguiente(None)
                    elif aux == self.fin:
                        self.fin = aux.getAnterior()
                        self.fin.setSiguiente(None)
                        aux.setAnterior(None)
                    else:
                        aux.getAnterior().setSiguiente(aux.getSiguiente())
                        aux.getSiguiente().setAnterior(aux.getAnterior())
                    self.size -= 1
                    break
                aux = aux.getSiguiente()

    def login(self, nombre, contrasenia):
        aux = self.inicio
        while aux != None:
            if aux.getNombre() == nombre and aux.getPass() == contrasenia:
                return aux
            aux = aux.getSiguiente()
        return None

    def find(self, nombre):
        aux = self.inicio
        while aux != None:
            if aux.getNombre() == nombre:
                return aux
            aux = aux.getSiguiente()
        return None

    def getCola(self, nombre):
        aux = self.inicio
        while aux != None:
            if aux.getNombre() == nombre:
                return aux.getColaCanciones()
            aux = aux.getSiguiente()
        return None

    def graph(self):
        dot = Digraph(comment='Lista de Usuarios')
        dot.format = 'png'
        actual = self.inicio
        i = 0
        while actual != None:
            dot.node(str(i), actual.getNombre())
            actual = actual.getSiguiente()
            i += 1
            if actual != None:
                dot.edge(str(i - 1), str(i), constraint='false')
                dot.edge(str(i), str(i - 1), constraint='false')

        dot.render(filename="listaUsuario", directory="C:\\Graphs\\", view=True, cleanup=True)
        print dot