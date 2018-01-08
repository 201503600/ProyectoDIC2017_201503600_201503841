from MatrizDispersa import Matriz
import os


def generarImagen(nombre, dot):
    archivo = open(nombre + ".txt", 'w')
    archivo.write(dot)
    archivo.close()
    dotPath = "\"C:\\Program Files (x86)\\Graphviz\\bin\\dot.exe\""
    fileInputPath = nombre + ".txt"
    fileOutputPath = nombre + ".png"
    tParam = " -Tpng "
    tOParam = " -o "
    tuple = (dotPath + tParam + fileInputPath + tOParam + fileOutputPath)
    os.system(tuple)

def reporteMatriz(matriz):
    dot = matriz.graficar()
    generarImagen(dot)

def reporteArtistas(matriz, anio, genero):
    dot = matriz.getArtistas(anio, genero).getDot()
    generarImagen(dot)

def reporteAlbumes(matriz, anio, genero, nombreArtista):
    dot = matriz.getArtistas(anio, genero).busqueda(
        nombreArtista).getAlbumes().graficar()
    generarImagen(dot)

def reporteListaCanciones(matriz, anio, genero, nombreArtista, nombreAlbum):
    matriz.getArtistas(anio, genero).busqueda(nombreArtista).getAlbumes(
    ).getAlbum(nombreAlbum).getCanciones().graficar()

def reporteUsuarios(listaUsuarios):
    listaUsuarios.graficar()

def reporteGeneral(matriz):
    print "ya valimos xD"

def reporteCola(listaUsuarios, nombre):
    listaUsuarios.getCola(nombre).graficar()
