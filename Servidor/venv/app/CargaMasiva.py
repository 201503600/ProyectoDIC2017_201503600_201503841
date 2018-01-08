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
        self.generos = None
        self.anios = None

    def cargarUsuarios(self, root):
        coleccionUsuarios = root.findall('usuarios')
        for usuarios in coleccionUsuarios:
            coleccionUsuario = usuarios.findall('usuario')
            for usuario in coleccionUsuario:
                self.usuarios.queueUsuario(usuario.find('nombre').text, usuario.find('pass').text)

    def crearMatriz(self, root):
        self.generos = ['--- Matriz ---']
        self.anios = ['--- Matriz ---']
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
                        if not(gen in self.generos):
                            self.generos.append(gen)
                        if not(anio in self.anios):
                            self.anios.append(anio)
        altura = len(self.anios)
        anchura = len(self.generos)
        self.anios.sort()
        self.matriz = Matriz(altura, anchura)
        for x in xrange(0, altura):
            self.matriz.setDato(self.anios[x], x, 0)
        for y in xrange(0, anchura):
            self.matriz.setDato(self.generos[y], 0, y)

    def llenarMatriz(self, root):
        coleccionArtistas = root.findall('artistas')
        for artistas in coleccionArtistas:
            coleccionArtista = artistas.findall('artista')
            for artista in coleccionArtista:
                nombreArtista = artista.find('nombre').text
                abbAlbumes = ArbolAlbum()
                coleccionAlbumes = artista.findall('albumes')
                for albumes in coleccionAlbumes:
                    coleccionAlbum = albumes.findall('album')
                    for album in coleccionAlbum:
                        nombreAlbum = album.find('nombre').text
                        gen = album.find('genero').text
                        anio = album.find('anio').text
                        listaCanciones = ListaCanciones()
                        coleccionCanciones = album.findall('canciones')
                        for canciones in coleccionCanciones:
                            coleccionCancion = canciones.findall('cancion')
                            for cancion in coleccionCancion:
                                can = cancion.find('nombre').text
                                path = cancion.find('path').text
                                listaCanciones.add(can, path)
                                #print can + ' - ' + path
                                self.datos.insert(can, nombreArtista, nombreAlbum, gen, anio)
                        abbAlbumes.add(nombreAlbum, listaCanciones)
                #self.datos.insertar("", "", "", "", "")
                print 'Anio\t' + str(anio) + '\Genero\t' + str(gen) + '\tArtista\t' + nombreArtista
                self.matriz.addArtista(anio, gen, nombreArtista, abbAlbumes)

    def analizarXML(self, cadena):
        full_file = os.path.abspath(cadena)
        with codecs.open(full_file, "r", encoding='utf-8', errors='ignore') as fdata:
            contenido = fdata.read().replace('\n', '')
        root = ElementTree.fromstring(contenido)
        self.cargarUsuarios(root)
        self.crearMatriz(root)
        self.llenarMatriz(root)
        print "Exito!"

    def getUsuario(self):
        return self.usuarios

    def getMatriz(self):
        return self.matriz

    def getDatos(self):
        return self.datos

    def getEncabezadoAnios(self):
        return self.anios

    def getEncabezadoGeneros(self):
        return self.generos

def main():
    arch = CargaMasiva()
    arch.analizarXML("C:\\Users\\Javier\\Desktop\\entradaEDD2.xml")
    #Reporte.reporteAlbumes(arch.getMatriz(), '1995', '(12)other', 'bob marley')

if __name__ == '__main__':
    main()