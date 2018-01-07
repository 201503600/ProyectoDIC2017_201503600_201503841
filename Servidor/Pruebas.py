from ListaCanciones import ListaCanciones
from ABB import ABB


def main():
    lista = ListaCanciones()
    lista.add('perfect two', 'path')
    lista.add('sensualidad', 'Path')
    lista.add('bella y sensual', 'Path')
    lista.graph()
    arbol_texto = ABB()
    arbol_texto.add("Juan", lista)
    arbol_texto.add("Pedro", lista)
    arbol_texto.add("Maria", lista)
    arbol_texto.add("Roberto", lista)
    arbol_texto.add("Teodoro", lista)
    arbol_texto.add("Manuel", lista)
    arbol_texto.add("Diego", lista)
    arbol_texto.add("Alejandro", lista)
    print arbol_texto.graph()
    print "exito!!"
    print str(arbol_texto.getAlbum('Pedro'))

if __name__ == "__main__":
    main()