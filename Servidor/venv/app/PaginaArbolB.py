from Artista import NodoArtista


class Pagina:

    def __init__(self):
        self.size = 0
        self.hoja = True
        self.padre = None
        self.primero = None
        self.dot = ''

    def add(self, nuevo):
        if self.isEmpty():
            self.primero = nuevo
            self.primero.setAnterior(None)
            self.primero.setSiguiente(None)
            self.size += 1
        else:
            aux = self.primero
            while True:
                if nuevo.getNombre().lower() == aux.getNombre().lower():
                    break
                elif nuevo.getNombre().lower() < aux.getNombre().lower():
                    self.size += 1
                    if (aux == self.primero):
                        self.primero.setAnterior(nuevo)
                        self.primero.setIzquierda(nuevo.getDerecha())
                        nuevo.setSiguiente(self.primero)
                        self.primero = nuevo
                        break
                    else:
                        nuevo.setAnterior(aux.getAnterior())
                        nuevo.setSiguiente(aux)
                        aux.getAnterior().setSiguiente(nuevo)
                        aux.getAnterior().setDerecha(nuevo.getIzquierda())
                        aux.setAnterior(nuevo)
                        aux.setIzquierda(nuevo.getDerecha())
                        break
                elif (aux.getSiguiente() == None):
                    self.size += 1
                    aux.setSiguiente(nuevo)
                    aux.setDerecha(nuevo.getIzquierda())
                    nuevo.setAnterior(aux)
                    nuevo.setSiguiente(None)
                    break
                aux = aux.getSiguiente()
                if aux == None:
                    break

    def isEmpty(self):
        return self.primero == None

    def getGraphPagina(self):
        self.dot = ''
        temp = 'nodo' + self.primero.getNombre() + ' [ label =\"'
        tempRecorre = self.primero
        i = 0
        while i < self.size:
            temp += '<C' + str(i) + '>|<D' + str(i) + '>Nombre Artista: ' + tempRecorre.getNombre() + '|'
            if tempRecorre.getIzquierda() != None:
                self.dot += 'nodo' + self.primero.getNombre() + ':C' + str(i) + '->nodo' + tempRecorre.getIzquierda().primero.getNombre() + '\n'
            tempRecorre = tempRecorre.getSiguiente()
            i += 1
        temp += '<C' + str(i) + '>\" fillcolor=\"#58FAD0\"]\n'
        tempRecorre = self.primero
        while tempRecorre.getSiguiente() != None:
            tempRecorre = tempRecorre.getSiguiente()
        if tempRecorre.getDerecha() != None:
            self.dot += 'nodo' + self.primero.getNombre() + ':C' + str(i) + '->nodo' + tempRecorre.getDerecha().primero.getNombre() + '\n'
        temp += self.dot
        return temp

    def isHoja(self):
        return self.hoja

    def setHoja(self, hoja):
        self.hoja = hoja

    def getSize(self):
        return self.size

    def getPrimero(self):
        return self.primero

    def getPadre(self):
        return self.padre

    def setPadre(self, padre):
        self.padre = padre
