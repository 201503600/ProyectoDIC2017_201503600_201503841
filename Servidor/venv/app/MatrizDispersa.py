from FilaMatriz import ListaFilaMatriz
from ArbolB import ArbolArtista

class Matriz:

    def __init__(self, altura, anchura):
        self.ultima = None
        self.altura = altura
        self.anchura = anchura
        self.dot = ''

        if anchura > 0 and altura > 0:
            self.ultima = ListaFilaMatriz(anchura)
            for i in xrange(1, altura):
                aux = ListaFilaMatriz(anchura)
                recorrerAux = aux.getPrimero()
                recorrerUltima = self.ultima.getPrimero()
                while recorrerAux != None and recorrerUltima != None:
                    recorrerAux.setArriba(recorrerUltima)
                    recorrerUltima.setAbajo(recorrerAux)
                    recorrerUltima = recorrerUltima.getSiguiente()
                    recorrerAux = recorrerAux.getSiguiente()
                self.ultima = aux

    def deleteDato(self, anio, genero):
        fila = self.getIndexAnio(anio)
        columna = self.getIndexGenero(genero)
        cabeza = self.ultima.getPrimero()
        while cabeza.getArriba() != None:
            cabeza = cabeza.getArriba()
        for x in xrange(0, fila):
            cabeza = cabeza.getAbajo()
        for x in xrange(0, columna):
            cabeza = cabeza.getSiguiente()
        print anio + ' / ' + genero
        cabeza.setDato(0)
        cabeza.setArtista(ArbolArtista())

    def setDato(self, dato, fila, columna):
        if fila < self.altura and columna < self.anchura:
            cabeza = self.ultima.getPrimero()
            while cabeza.getArriba() != None:
                cabeza = cabeza.getArriba()
            for x in xrange(0, fila):
                cabeza = cabeza.getAbajo()
            for x in xrange(0, columna):
                cabeza = cabeza.getSiguiente()
            cabeza.setDato(dato)

    def getDato(self, fila, columna):
        cabeza = self.ultima.getPrimero()
        while cabeza.getArriba() != None:
            cabeza = cabeza.getArriba()
        for x in xrange(0, fila):
            cabeza = cabeza.getAbajo()
        for x in xrange(0, columna):
            cabeza = cabeza.getSiguiente()
        return cabeza.getDato()

    def getArtistas(self, anio, genero):
        cabeza = self.ultima.getPrimero()
        while cabeza.getArriba() != None:
            cabeza = cabeza.getArriba()
        for x in xrange(0, self.getIndexAnio(anio)):
            cabeza = cabeza.getAbajo()
        for x in xrange(0, self.getIndexGenero(genero)):
            cabeza = cabeza.getSiguiente()
        #print cabeza.getDato()
        return cabeza.getArtistas()

    def addArtista(self, anio, genero, nombre):
        cabeza = self.ultima.getPrimero()
        while cabeza.getArriba() != None:
            cabeza = cabeza.getArriba()
        for x in xrange(0, self.getIndexAnio(anio)):
            cabeza = cabeza.getAbajo()
        for x in xrange(0, self.getIndexGenero(genero)):
            cabeza = cabeza.getSiguiente()
        cabeza.setDato(anio + ' - ' + genero)
        cabeza.getArtistas().add(nombre)

    def getIndexAnio(self, anio):
        for x in xrange(0, self.altura):
            if self.getDato(x, 0) == anio:
                return x
        return -1

    def getIndexGenero(self, genero):
        for x in xrange(0, self.anchura):
            if self.getDato(0, x) == genero:
                return x
        return -1

    def getAltura(self):
        return self.altura

    def getAnchura(self):
        return self.anchura

    def getUltima(self):
        return self.ultima

    def graph(self):
        dot = 'digraph matriz{\n\trankdir = TB;\n\tnode [shape = record, width = 25];\n\t'
        dot += 'Matriz[shape = record,label=\"{'
        for i in xrange(0, self.altura - 1):
            dot += '{'
            for j in xrange(0, self.anchura - 1):
                dot += '{' + str(self.getDato(i, j)) + '}|'
            dot += '{' + str(self.getDato(i, self.anchura - 1)) + '}'
            dot += '}|'
        dot += '{'
        for j in xrange(0, self.anchura - 1):
            dot += '{' + str(self.getDato(self.altura - 1, j)) + '}|'
        dot += '{' + str(self.getDato(self.altura - 1, self.anchura - 1)) + '}'
        dot += '}'
        dot += '}\"]; \n'
        dot += '}'
        return dot

    def graphManual(self):
        self.dot = 'digraph matriz{\n\trankdir=UD;\n\tnode[shape=box];\n\t'
        print 'Generando encabezado generos'
        self.graphHeaderGender()
        print 'Generando encabezado anios'
        nodoFila = self.getRaiz().getAbajo()
        while nodoFila.getAbajo() != None:
            self.graphRow(nodoFila)
            nodoFila = nodoFila.getAbajo()
        print 'Generando ultimo encabezado anio'
        self.dot += '{\n\t\trank=max;\n\t\t'
        while nodoFila.getSiguiente() != None:
            if nodoFila.getDato() != 0:
                self.dot += 'nodo' + str(nodoFila.getCorrelativo()) + '[label=\"' + str(nodoFila.getDato()) + '\"];\n\t\t'
            nodoFila = nodoFila.getSiguiente()
        if nodoFila.getDato() != 0:
            self.dot += 'nodo' + str(nodoFila.getCorrelativo()) + '[label=\"' + str(nodoFila.getDato()) + '\"];\n\t}\n\t'
        else:
            self.dot += '}'
        print 'Generando enlaces en encabezados'
        self.graphEdgeHeader()
        print 'Generando enlaces en nodos verticalmente'
        nodoFila = self.getRaiz().getSiguiente()
        for i in xrange(1, self.anchura):
            auxDatoCol = nodoFila
            aux = auxDatoCol.getAbajo()
            caminoRegreso = 'nodo' + str(auxDatoCol.getCorrelativo()) + ';'
            self.dot += 'nodo' + str(auxDatoCol.getCorrelativo())
            for j in xrange(1, self.altura):
                if aux.getDato() != 0:
                    auxDatoCol = aux
                    caminoRegreso = 'nodo' + str(aux.getCorrelativo()) + '->' + caminoRegreso
                    self.dot += '->nodo' + str(aux.getCorrelativo())
                aux = aux.getAbajo()
            self.dot += ';\n' + caminoRegreso + '\n'
            nodoFila = nodoFila.getSiguiente()
        print 'Generando enlaces en nodos horizontalmente'
        nodoFila = self.getRaiz().getAbajo()
        for i in xrange(1, self.altura):
            auxDato = nodoFila
            aux = auxDato.getSiguiente()
            for j in xrange(1, self.anchura):
                if aux.getDato() != 0 and auxDato != self.getRaiz().getAbajo():
                    self.dot += 'nodo' + str(auxDato.getCorrelativo()) + '->nodo' + str(aux.getCorrelativo()) + '[constraint=false];\n'
                    self.dot += 'nodo' + str(aux.getCorrelativo()) + '->nodo' + str(auxDato.getCorrelativo()) + '[constraint=false];\n'
                    auxDato = aux
                aux = aux.getSiguiente()
            nodoFila = nodoFila.getAbajo()
        # for i in xrange(1, self.altura):
        #     nodoCol = nodoFila.getArriba().getSiguiente()
        #     auxDatoIzq = nodoFila
        #     auxDatoUp = nodoCol
        #     aux = nodoFila.getSiguiente()
        #     for j in xrange(1, self.anchura):
        #         auxIzq = auxDatoIzq
        #         auxUp = auxDatoUp
        #         if aux.getDato() != 0:
        #             while auxIzq.getDato() == 0:
        #                 auxIzq = auxIzq.getAnterior()
        #             while auxUp.getDato() == 0:
        #                 auxUp = auxUp.getArriba()
        #             #if auxIzq == nodoFila:
        #             self.dot += 'nodo' + str(auxUp.getCorrelativo()) + '->nodo' + str(aux.getCorrelativo()) + ';\n\t'
        #             self.dot += 'nodo' + str(aux.getCorrelativo()) + '->nodo' + str(auxUp.getCorrelativo()) + ';\n\t'
        #             self.dot += 'nodo' + str(auxIzq.getCorrelativo()) + '->nodo' + str(aux.getCorrelativo()) + '[constraint=false];\n\t'
        #             self.dot += 'nodo' + str(aux.getCorrelativo()) + '->nodo' + str(auxIzq.getCorrelativo()) + '[constraint=false];\n\t'
        #         auxDatoIzq = auxDatoIzq.getSiguiente()
        #         auxDatoUp = auxDatoUp.getSiguiente()
        #         aux = aux.getSiguiente()
        #     nodoFila = nodoFila.getAbajo()
        self.dot += '}'
        return self.dot

    def graphHeaderGender(self):
        self.dot += '{\n\t\trank=min;\n\t\t'
        aux = self.getRaiz().getSiguiente()
        self.dot += 'm[label = \"Matriz Dispersa\"];\n\t\t'
        while aux.getSiguiente() != None:
            self.dot += 'nodo' + str(aux.getCorrelativo()) + '[label=\"' + str(aux.getDato()) + '\", rankdir = LR];\n\t\t'
            aux = aux.getSiguiente()
        self.dot += 'nodo' + str(aux.getCorrelativo()) + '[label=\"' + str(aux.getDato()) + '\", rankdir = LR];\n\t}\n\t'

    def graphRow(self, nodoFila):
        self.dot += '{\n\t\trank=same;\n\t\t'
        while nodoFila.getSiguiente() != None:
            if nodoFila.getDato() != 0:
                self.dot += 'nodo' + str(nodoFila.getCorrelativo()) + '[label=\"' + str(nodoFila.getDato()) + '\"];\n\t\t'
            nodoFila = nodoFila.getSiguiente()
        if nodoFila.getDato() != 0:
            self.dot += 'nodo' + str(nodoFila.getCorrelativo()) + '[label=\"' + str(nodoFila.getDato()) + '\"];\n\t}\n\t'
        else:
            self.dot += '}'

    def graphEdgeHeader(self):
        self.dot += 'm'
        aux = self.getRaiz().getSiguiente()
        while aux.getSiguiente() != None:
            self.dot += '->nodo' + str(aux.getCorrelativo())
            aux = aux.getSiguiente()
        while aux.getAnterior() != self.getRaiz():
            self.dot += '->nodo' + str(aux.getCorrelativo())
            aux = aux.getAnterior()
        self.dot += '->nodo' + str(aux.getCorrelativo())
        aux = self.getRaiz().getAbajo()
        self.dot += ';\n\tm->nodo' + str(aux.getCorrelativo()) + ';\n\t'
        aux = aux.getAbajo()
        while aux != None:
            self.dot += 'nodo' + str(aux.getArriba().getCorrelativo()) + '->nodo' + str(aux.getCorrelativo()) + ' [rankdir=UD];\n\t'
            self.dot += 'nodo' + str(aux.getCorrelativo()) + '->nodo' + str(aux.getArriba().getCorrelativo()) + ';\n\t'
            aux = aux.getAbajo()

    def getRaiz(self):
        cabeza = self.ultima.getPrimero()
        while cabeza.getArriba() != None:
            cabeza = cabeza.getArriba()
        return cabeza
