import os
import codecs
from xml.etree import ElementTree

from ListaUsuarios import ListaUsuarios
from ListaCanciones import ListaCanciones
from ListaDatoCancion import ListaDato
from MatrizDispersa import Matriz
from ArbolBB import ArbolAlbum

class CargaMasiva:

    def __init__(self):
        self.usuarios = ListaUsuarios()
        self.datos = ListaDato()
        self.matriz = None
        self.engeneros = None
        self.enanios = None

    def cargarUsuarios(self, root):
        coleccionUsuarios = root.findall('usuarios')
        for usuarios in coleccionUsuarios:
            coleccionUsuario = usuarios.findall('usuario')
            for usuario in coleccionUsuario:
                self.usuarios.queueUsuario(usuario.find('nombre').text, usuario.find('pass').text)

    def crearMatriz(self, root):
        self.engeneros = []
        self.enanios = []
        generos = ['--- Matriz ---']
        anios = ['--- Matriz ---']
        coleccionArtistas = root.findall('artistas')
        for artistas in coleccionArtistas:
            coleccionArtista = artistas.findall('artista')
            for artista in coleccionArtista:
                coleccionAlbumes = artista.findall('albumes')
                for albumes in coleccionAlbumes:
                    coleccionAlbum = albumes.findall('album')
                    for album in coleccionAlbum:
                        gen = album.find('genero').text
                        anio = album.find('anio').text
                        if not(gen in generos):
                            generos.append(gen)
                            self.engeneros.append({'genero':gen})
                        if not(anio in anios):
                            anios.append(anio)
                            self.enanios.append({'anio':anio})
        altura = len(anios)
        anchura = len(generos)
        anios.sort()
        self.engeneros.sort()
        self.enanios.sort()
        self.matriz = Matriz(altura, anchura)
        for x in xrange(0, altura):
            self.matriz.setDato(anios[x], x, 0)
        for y in xrange(0, anchura):
            self.matriz.setDato(generos[y], 0, y)

    def llenarMatriz(self, root):
        coleccionArtistas = root.findall('artistas')
        for artistas in coleccionArtistas:
            coleccionArtista = artistas.findall('artista')
            for artista in coleccionArtista:
                nombreArtista = artista.find('nombre').text
                #abbAlbumes = ArbolAlbum()
                coleccionAlbumes = artista.findall('albumes')
                for albumes in coleccionAlbumes:
                    coleccionAlbum = albumes.findall('album')
                    for album in coleccionAlbum:
                        nombreAlbum = album.find('nombre').text
                        gen = album.find('genero').text
                        anio = album.find('anio').text
                        self.matriz.addArtista(anio, gen, nombreArtista)
                        self.matriz.getArtistas(anio, gen).search(nombreArtista).getAlbumes().add(nombreAlbum)
                        #listaCanciones = ListaCanciones()
                        coleccionCanciones = album.findall('canciones')
                        for canciones in coleccionCanciones:
                            coleccionCancion = canciones.findall('cancion')
                            for cancion in coleccionCancion:
                                can = cancion.find('nombre').text
                                path = cancion.find('path').text
                                self.matriz.getArtistas(anio, gen).search(nombreArtista).getAlbumes().getAlbum(nombreAlbum).getCanciones().add(can, path)
                                #listaCanciones.add(can, path)
                                self.datos.insert(can, nombreArtista, nombreAlbum, gen, anio, path)
                        #abbAlbumes.add(nombreAlbum, listaCanciones)
                #self.datos.insertar("", "", "", "", "")
                #self.matriz.addArtista(anio, gen, nombreArtista, abbAlbumes)
                #self.matriz.getArtistas(anio, gen).printArtista(self.matriz.getArtistas(anio, gen).search(nombreArtista))

    def analizarXML(self, cadena):
        full_file = os.path.abspath(cadena)
        with codecs.open(full_file, "r", errors='ignore') as fdata:
            contenido = fdata.read().replace('\n', '')
        root = ElementTree.fromstring(contenido)
        self.cargarUsuarios(root)
        self.crearMatriz(root)
        self.llenarMatriz(root)

    def getUsuario(self):
        return self.usuarios

    def getMatriz(self):
        return self.matriz

    def getDatos(self):
        return self.datos

    def getEncabezadoAnios(self):
        return self.enanios

    def getEncabezadoGeneros(self):
        return self.engeneros

class Buscador:

    def __init__(self, matriz):
        self.canciones = ListaDato()
        self.matriz = matriz

    def getByArtistAlbumSong(self, name):
        self.canciones = ListaDato()
        auxFila = self.matriz.getRaiz().getAbajo()
        auxCol = auxFila.getArriba().getSiguiente()
        for i in xrange(1, self.matriz.getAltura()):
            auxG = auxCol
            aux = auxFila.getSiguiente()
            for j in xrange(1, self.matriz.getAnchura()):
                anio = auxFila.getDato()
                genero = auxG.getDato()
                artista = aux.getArtistas().search(name)
                if aux.getDato() != 0:
                    if artista != None:
                        self.roamABBArtista(genero, anio, name, artista.getAlbumes().getRaiz())
                    else:
                        self.roamBT(genero, anio, aux.getArtistas().getRaiz().getPrimero(), name)                
                auxG = auxG.getSiguiente()
                aux = aux.getSiguiente()
            auxFila = auxFila.getAbajo()

    def roamBT(self, genero, anio, nodo, nombre):
        if nodo.getIzquierda() != None:
            self.roamBT(genero, anio, nodo.getIzquierda().getPrimero(), nombre)
        nodoAlbum = nodo.getAlbumes().getAlbum(nombre)
        if nodoAlbum != None:
            cancion = nodoAlbum.getCanciones().head
            while True:
                self.canciones.insert(cancion.getNombre(), nodo.getNombre(), nodoAlbum.getNombre(), genero, anio, cancion.getPath())
                cancion = cancion.getSiguiente()
                if cancion == nodoAlbum.getCanciones().head:
                    break
        else:
            self.roamBBT(genero, anio, nodo.getNombre(), nodo.getAlbumes().getRaiz(), nombre)
        if nodo.getSiguiente() != None:
            self.roamBT(genero, anio, nodo.getSiguiente(), nombre)
        elif nodo.getDerecha() != None:
            self.roamBT(genero, anio, nodo.getDerecha().getPrimero(), nombre)

    def roamBBT(self, genero, anio, artista, nodo, nombre):
        cancion = nodo.getCanciones().find(nombre)
        if cancion != None:
            self.canciones.insert(cancion.getNombre(), artista, nodo.getNombre(), genero, anio, cancion.getPath())
        if nodo.getHijoIzq() != None:
            self.roamBBT(genero, anio, artista, nodo.getHijoIzq(), nombre)
        if nodo.getHijoDer() != None:
            self.roamBBT(genero, anio, artista, nodo.getHijoDer(), nombre)

    def getByArtist(self, nombreArtista):
        self.canciones = ListaDato()
        auxFila = self.matriz.getRaiz().getAbajo()
        auxCol = auxFila.getArriba().getSiguiente()
        for i in xrange(1, self.matriz.getAltura()):
            auxG = auxCol
            aux = auxFila.getSiguiente()
            for j in xrange(1, self.matriz.getAnchura()):
                artista = aux.getArtistas().search(nombreArtista)
                if artista != None and aux.getDato() != 0:
                    anio = auxFila.getDato()
                    genero = auxG.getDato()
                    self.roamABBArtista(genero, anio, nombreArtista, artista.getAlbumes().getRaiz())
                auxG = auxG.getSiguiente()
                aux = aux.getSiguiente()
            auxFila = auxFila.getAbajo()

    def roamABBArtista(self, genero, anio, artista, nodo):
        cancion = nodo.getCanciones().head
        while True:
            self.canciones.insert(cancion.getNombre(), artista, nodo.getNombre(), genero, anio, cancion.getPath())
            cancion = cancion.getSiguiente()
            if cancion == nodo.getCanciones().head:
                break
        if nodo.getHijoIzq() != None:
            self.roamABBArtista(genero, anio, artista, nodo.getHijoIzq())
        if nodo.getHijoDer() != None:
            self.roamABBArtista(genero, anio, artista, nodo.getHijoDer())

    def getByAlbum(self, nombreAlbum):
        self.canciones = ListaDato()
        auxFila = self.matriz.getRaiz().getAbajo()
        auxCol = auxFila.getArriba().getSiguiente()
        for i in xrange(1, self.matriz.getAltura()):
            auxG = auxCol
            aux = auxFila.getSiguiente()
            for j in xrange(1, self.matriz.getAnchura()):
                if aux.getDato() != 0:
                    anio = auxFila.getDato()
                    genero = auxG.getDato()
                    self.roamABAlbum(genero, anio, aux.getArtistas().getRaiz().getPrimero(), nombreAlbum)
                auxG = auxG.getSiguiente()
                aux = aux.getSiguiente()
            auxFila = auxFila.getAbajo()

    def roamABAlbum(self, genero, anio, nodo, album):
        if nodo.getIzquierda() != None:
            self.roamABAlbum(genero, anio, nodo.getIzquierda().getPrimero(), album)
        nodoAlbum = nodo.getAlbumes().getAlbum(album)
        if nodoAlbum != None:
            cancion = nodoAlbum.getCanciones().head
            while True:
                self.canciones.insert(cancion.getNombre(), nodo.getNombre(), nodoAlbum.getNombre(), genero, anio, cancion.getPath())
                cancion = cancion.getSiguiente()
                if cancion == nodoAlbum.getCanciones().head:
                    break
        if nodo.getSiguiente() != None:
            self.roamABAlbum(genero, anio, nodo.getSiguiente(), album)
        elif nodo.getDerecha() != None:
            self.roamABAlbum(genero, anio, nodo.getDerecha().getPrimero(), album)

    def getByGender(self, genero):
        self.canciones = ListaDato()
        aux = self.matriz.getRaiz().getSiguiente()
        auxF = aux.getAnterior().getAbajo()
        while aux != None:
            if aux.getDato() == genero:
                aux = aux.getAbajo()
                for fila in xrange(1, self.matriz.getAltura()):
                    if aux.getDato() != 0:
                        anio = auxF.getDato()
                        self.roamAB(genero, anio, aux.getArtistas().getRaiz().getPrimero())
                    aux = aux.getAbajo()
                    auxF = auxF.getAbajo()
            if aux != None:
                aux = aux.getSiguiente()

    def getByYear(self, anio):
        self.canciones = ListaDato()
        aux = self.matriz.getRaiz().getAbajo()
        auxC = aux.getArriba().getSiguiente()
        while aux != None:
            if aux.getDato() == anio:
                aux = aux.getSiguiente()
                for col in xrange(1, self.matriz.getAnchura()):
                    if aux.getDato() != 0:
                        genero = auxC.getDato()
                        self.roamAB(genero, anio, aux.getArtistas().getRaiz().getPrimero())
                    aux = aux.getSiguiente()
                    auxC = auxC.getSiguiente()
            if aux != None:
                aux = aux.getAbajo()

    def roamAB(self, genero, anio, nodo):
        if nodo.getIzquierda() != None:
            self.roamABA(genero, anio, nodo.getIzquierda().getPrimero())
        self.roamABB(genero, anio, nodo.getNombre(), nodo.getAlbumes().getRaiz())
        if nodo.getSiguiente() != None:
            self.roamAB(genero, anio, nodo.getSiguiente())
        elif nodo.getDerecha() != None:
            self.roamAB(genero, anio, nodo.getDerecha().getPrimero())

    def roamABB(self, genero, anio, artista, nodo):
        cancion = nodo.getCanciones().head
        while True:
            self.canciones.insert(cancion.getNombre(), artista, nodo.getNombre(), genero, anio, cancion.getPath())
            cancion = cancion.getSiguiente()
            if cancion == nodo.getCanciones().head:
                break
        if nodo.getHijoIzq() != None:
            self.roamABB(genero, anio, artista, nodo.getHijoIzq())
        if nodo.getHijoDer() != None:
            self.roamABB(genero, anio, artista, nodo.getHijoDer())

    def getCanciones(self):
        return self.canciones

def main():
    arch = CargaMasiva()
    arch.analizarXML("C:\\Users\\Javier\\Desktop\\entradaEDD2.xml")
    #print type(arch.getEncabezadoAnios())
    #Reporte.reporteAlbumes(arch.getMatriz(), '1995', '(12)other', 'bob marley')

if __name__ == '__main__':
    main()