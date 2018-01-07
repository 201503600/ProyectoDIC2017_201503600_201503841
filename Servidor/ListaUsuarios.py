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

    def queueUsuario(self, nombre, contrasenia):
        nuevo = NodoUsuario(nombre, contrasenia)
        if self.isEmpty():
            self.inicio = nuevo
            self.fin = nuevo
        else:
            nuevo.setAnterior(self.fin)
            self.fin.setSiguiente(nuevo)
            self.fin = nuevo
        self.size += 1

    def login(self, nombre, contrasenia):
        aux = self.inicio
        while aux.getSiguiente() != None:
            if aux.getNombre() == Nombre and aux.getPass() == contrasenia:
                return aux
            aux = aux.getSiguiente()
        return

    # def getCola(self, nombre):
    #     aux = self.Inicio
    #     while aux.getSiguiente() != None:
    #         if aux.getNombreUsuario() == Nombre:
    #             return aux.getColaCanciones()
    #         aux = aux.getSiguiente()
    #     return None

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