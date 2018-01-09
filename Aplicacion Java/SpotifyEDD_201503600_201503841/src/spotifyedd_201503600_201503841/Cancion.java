package spotifyedd_201503600_201503841;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Javier
 */
public class Cancion {

    public Cancion(){
        album = "";
        artista = "";
        genero = "";
        anio = 0;
        cancion = "";
        path = "";
    }
    
    public Cancion(int anio, String genero, String artista, String album, String cancion, String path){
        this.anio = anio;
        this.genero = genero;
        this.artista = artista;
        this.album = album;
        this.cancion = cancion;
        this.path = path;
    }
    
    /**
     * @return the album
     */
    public String getAlbum() {
        return album;
    }

    /**
     * @param album the album to set
     */
    public void setAlbum(String album) {
        this.album = album;
    }

    /**
     * @return the anio
     */
    public int getAnio() {
        return anio;
    }

    /**
     * @param anio the anio to set
     */
    public void setAnio(int anio) {
        this.anio = anio;
    }

    /**
     * @return the artista
     */
    public String getArtista() {
        return artista;
    }

    /**
     * @param artista the artista to set
     */
    public void setArtista(String artista) {
        this.artista = artista;
    }

    /**
     * @return the cancion
     */
    public String getCancion() {
        return cancion;
    }

    /**
     * @param cancion the cancion to set
     */
    public void setCancion(String cancion) {
        this.cancion = cancion;
    }

    /**
     * @return the genero
     */
    public String getGenero() {
        return genero;
    }

    /**
     * @param genero the genero to set
     */
    public void setGenero(String genero) {
        this.genero = genero;
    }
    
    private String album;
    private int anio;
    private String artista;
    private String cancion;
    private String genero;
    private String path;

    /**
     * @return the path
     */
    public String getPath() {
        return path;
    }

    /**
     * @param path the path to set
     */
    public void setPath(String path) {
        this.path = path;
    }
    
}
