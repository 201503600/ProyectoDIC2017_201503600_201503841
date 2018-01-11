from Artista import NodoArtista
from PaginaArbolB import Pagina


class ArbolArtista:

    def __init__(self):
        self.raiz = None
        self.dot = ''

    def isEmpty(self):
        return self.raiz == None

    def add(self, nombre):
        nuevo = NodoArtista(nombre)
        if self.isEmpty():
            self.raiz = Pagina()
            self.raiz.add(nuevo)
        else:
            obj = self.inserta(nuevo, self.raiz)
            if isinstance(obj, NodoArtista):
                self.raiz = Pagina()
                obj.getDerecha().setPadre(self.raiz)
                obj.getIzquierda().setPadre(self.raiz)
                self.raiz.add(obj)
                self.raiz.setHoja(False)

    def printArtista(self, artista):
        if artista != None:
            print artista.getNombre()
            artista.getAlbumes().raiz.printAlbum(artista.getAlbumes().raiz)

    def inserta(self, nodo, rama):
        if rama.isHoja():
            rama.add(nodo)
            if rama.getSize() == 5:
                return self.partir(rama)
            else:
                return rama
        else:
            aux = rama.getPrimero()
            while True:
                if nodo.getNombre().lower() == aux.getNombre().lower():
                    return rama
                elif nodo.getNombre().lower() < aux.getNombre().lower():
                    obj = self.inserta(nodo, aux.getIzquierda())
                    if isinstance(obj, NodoArtista):
                        obj.getDerecha().setPadre(rama)
                        obj.getIzquierda().setPadre(rama)
                        rama.add(obj)
                        rama.setHoja(False)
                        if rama.getSize() == 5:
                            return self.partir(rama)
                    return rama
                elif aux.getSiguiente() == None:
                    obj = self.inserta(nodo, aux.getDerecha())
                    if isinstance(obj, NodoArtista):
                        obj.getDerecha().setPadre(rama)
                        obj.getIzquierda().setPadre(rama)
                        rama.add(obj)
                        rama.setHoja(False)
                        if (rama.getSize() == 5):
                            return self.partir(rama)
                    return rama
                aux = aux.getSiguiente()
                if aux == None:
                    break
        return rama

    def partir(self, rama):
        derecha = Pagina()
        izquierda = Pagina()
        medio = None
        aux = rama.getPrimero()
        i = 1
        while i < 6:
            nodo = NodoArtista(aux.getNombre())
            nodo.setIzquierda(aux.getIzquierda())
            nodo.setDerecha(aux.getDerecha())
            if (nodo.getDerecha() != None and nodo.getIzquierda() != None):
                izquierda.setHoja(False)
                derecha.setHoja(False)
            if i <= 2:
                izquierda.add(nodo)
            elif i == 3:
                medio = nodo
            elif i >= 4:
                derecha.add(nodo)
            aux = aux.getSiguiente()
            i += 1
        medio.setIzquierda(izquierda)
        medio.setDerecha(derecha)
        return medio

    def getDot(self):
        aux = 'digraph arbolB{\n\tnode [shape = record, style=filled];\n\tsplines=line;\n\t'
        self.getGrafNodos(self.raiz)
        aux += self.dot
        aux += '}'
        return aux

    def getGrafNodos(self, raiz):
        if raiz == None:
            return
        self.dot += raiz.getGraphPagina()
        aux = raiz.getPrimero()
        while aux != None:
            self.getGrafNodos(aux.getIzquierda())
            aux = aux.getSiguiente()
        aux = raiz.getPrimero()
        while aux.getSiguiente() != None:
            aux = aux.getSiguiente()
        self.getGrafNodos(aux.getDerecha())

    def search(self, nombre):
        if not(self.isEmpty()):
            return self.look(nombre, self.raiz)
        else:
            return None

    def look(self, nombre, rama):
        nodo = rama.getPrimero()
        while nodo != None:
            print nodo.getNombre()
            if nombre.lower() < nodo.getNombre().lower():
                if rama.isHoja():
                    return None
                else:
                    return self.look(nombre, nodo.getIzquierda())
            elif nombre.lower() == nodo.getNombre().lower():
                return nodo
            elif nodo.getSiguiente() == None:
                if rama.isHoja():
                    return None
                else:
                    return self.look(nombre, nodo.getDerecha())
            nodo = nodo.getSiguiente()
        return None

    def getRaiz(self):
        return self.raiz

    def deleteArtista(self, nombre):
        if not self.isEmpty():
            return self.delete(nombre, self.raiz)
        return False

    def delete(self, nombre, rama):
        nodo = rama.getPrimero()
        while nodo != None:
            if nombre.lower() < nodo.getNombre().lower():
                if rama.isHoja():
                    return False
                else:
                    return self.delete(nombre, nodo.getIzquierda())
            elif nombre.lower() == nodo.getNombre().lower():
                if rama.isHoja():
                    if self.raiz.getSize() == 1:
                        self.raiz = None
                    else:
                        rama.deleteArtista(nombre)
                        # Balancear el arbol
                        rama = balanceo(rama)
                    return True
                else:
                    if nodo.getIzquierda().getSize() >= nodo.getDerecha().getSize():
                        auxiliar = nodo.getIzquierda().getPrimero()
                        while auxiliar.getSiguiente() != None:
                            auxiliar = auxiliar.getSiguiente()
                            if auxiliar.getSiguiente() == None and auxiliar.getDerecha() != None:
                                auxiliar = auxiliar.getDerecha().getPrimero()
                        aux = NodoArtista(auxiliar.getArtista())
                        aux.setArbolAlbum(auxiliar.getArbolAlbumes())
                        auxiliar.setArtista(nodo.getArtista())
                        auxiliar.setArbolAlbum(nodo.getArbolAlbumes())
                        nodo.setArtista(aux.getArtista())
                        nodo.setArbolAlbum(aux.getArbolAlbumes())
                        return self.delete(nombre, nodo.getIzquierda())
                    else:
                        auxiliar = nodo.getDerecha().getPrimero()
                        while auxiliar.getIzquierda() != None:
                            auxiliar = auxiliar.getIzquierda().getPrimero()
                        aux = NodoArtista(auxiliar.getArtista())
                        aux.setArbolAlbum(auxiliar.getArbolAlbumes())
                        auxiliar.setArtista(nodo.getArtista())
                        auxiliar.setArbolAlbum(nodo.getArbolAlbumes())
                        nodo.setArtista(aux.getArtista())
                        nodo.setArbolAlbum(aux.getArbolAlbumes())
                        return self.delete(nombre, nodo.getDerecha())
            elif nodo.getSiguiente() == None:
                if rama.isHoja():
                    return False
                else:
                    return self.delete(nombre, nodo.getDerecha())
            nodo = nodo.getSiguiente()
        return False

    def balanceo(self, rama):
        if rama.getSize() == 1 and rama.getPadre() != None:
            padre = rama.getPadre().getPrimero()
            if rama == padre.getIzquierda():
                if (rama.getSize() + padre.getDerecha().getSize() + 1) < 5:
                    auxiliar = NodoArtista(padre.getNombre())
                    auxiliar.setAlbumes(padre.getAlbumes())
                    rama.add(auxiliar)
                    
        else:
            return rama
