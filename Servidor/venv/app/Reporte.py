from MatrizDispersa import Matriz
from CargaMasiva import CargaMasiva
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
    os.system(fileOutputPath)

def reporteMatriz(matriz):
    dot = matriz.graphManual()
    generarImagen('matriz', dot)

def reporteArtistas(matriz, anio, genero):
    dot = matriz.getArtistas(anio, genero).getDot()
    generarImagen('artista', dot)

def reporteAlbumes(matriz, anio, genero, nombreArtista):
    dot = matriz.getArtistas(anio, genero).search(nombreArtista).getAlbumes().graph()
    generarImagen('albumes', dot)

def reporteListaCanciones(matriz, anio, genero, nombreArtista, nombreAlbum):
    matriz.getArtistas(anio, genero).search(nombreArtista).getAlbumes().getAlbum(nombreAlbum).getCanciones().graph()

def reporteUsuarios(listaUsuarios):
    listaUsuarios.graph()

def reporteGeneral(matriz):
    print "ya valimos xD"

def reporteCola(listaUsuarios, nombre):
    listaUsuarios.getCola(nombre).graph()


# def main():
#     arch = CargaMasiva()
#     arch.analizarXML("C:\\Users\\Javier\\Desktop\\entradaEDD2.xml")
#     reporteMatriz(arch.getMatriz())

# if __name__ == '__main__':
#     main()