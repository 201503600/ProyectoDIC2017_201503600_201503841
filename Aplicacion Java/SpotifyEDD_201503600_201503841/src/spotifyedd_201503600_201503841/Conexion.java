/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package spotifyedd_201503600_201503841;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.logging.Level;
import com.squareup.okhttp.FormEncodingBuilder;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.RequestBody;
import com.squareup.okhttp.Response;


/**
 *
 * @author Suseth
 */
public class Conexion {
     public static OkHttpClient webClient = new OkHttpClient();

    
    private static String getString(String metodo, RequestBody formBody) {

        try {
            URL url = new URL("http://127.0.0.1:5000/" + metodo);
            Request request = new Request.Builder().url(url).post(formBody).build();
            Response response = webClient.newCall(request).execute();//Aqui obtiene la respuesta en dado caso si hayas pues un return en python
            String response_string = response.body().string();//y este seria el string de las respuesta
            return response_string;
        } catch (MalformedURLException ex) {
            java.util.logging.Logger.getLogger(Conexion.class.getName()).log(Level.SEVERE, null, ex);
        } catch (Exception ex) {
            java.util.logging.Logger.getLogger(Conexion.class.getName()).log(Level.SEVERE, null, ex);
        }
        return null;
    }
    
    public static String getStringGet(String metodo){
        try {
            URL url = new URL("http://127.0.0.1:5000/" + metodo);
            Request request = new Request.Builder().url(url).get().build();
            Response response = webClient.newCall(request).execute();//Aqui obtiene la respuesta en dado caso si hayas pues un return en python
            String response_string = response.body().string();//y este seria el string de las respuesta
            return response_string;
        } catch (MalformedURLException ex) {
            java.util.logging.Logger.getLogger(Conexion.class.getName()).log(Level.SEVERE, null, ex);
        } catch (Exception ex) {
            java.util.logging.Logger.getLogger(Conexion.class.getName()).log(Level.SEVERE, null, ex);
        }
        return null;
    }
    
     public static String postCargaArchivo(String parametroJava) {
        RequestBody formBody = new FormEncodingBuilder()
                                        .add("path", parametroJava)
                                        .build();
        return getString("carga_archivo", formBody);
    }
     
     public static String loginOAuth(){
//         RequestBody formBody = new FormEncodingBuilder()
//                                        .add("", "")
//                                        .build();
         return getStringGet("loginOAuth");
     }
     
     public static String login(String username, String pass){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("username", username)
                                        .add("password", pass)
                                        .build();
         return getString("login", formBody);
     }
     
     public static String logout(){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("", "")
                                        .build();
         return getString("logout", formBody);
     }
     
     public static String postEncabezadoAnios(){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("", "")
                                        .build();
         return getString("encabezadoAnio", formBody);
     }
     
     public static String postEncabezadoGeneros(){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("", "")
                                        .build();
         return getString("encabezadoGenero", formBody);
     }
     
     public static String postReportMatriz(){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("", "")
                                        .build();
         return getString("reporteMatriz", formBody);
     }
     
     public static String postReportArtistas(String anio, String genero){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("anio", anio)
                                        .add("genero", genero)
                                        .build();
         return getString("reporteArtistas", formBody);
     }
     
     public static String postReportAlbums(String anio, String genero, String artista){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("anio", anio)
                                        .add("genero", genero)
                                        .add("artista", artista)
                                        .build();
         return getString("reporteAlbumes", formBody);
     }
     
     public static String postReportListSongs(String anio, String genero, String artista, String album){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("anio", anio)
                                        .add("genero", genero)                 
                                        .add("artista", artista)
                                        .add("album", album)
                                        .build();
         return getString("reporteListaCanciones", formBody);
     }
     
     public static String postReportUsers(){         
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("", "")
                                        .build();
         return getString("reporteUsuarios", formBody);
     }
     
     public static String postReportQueueUser(String username){         
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("username", username)
                                        .build();
         return getString("reporteQueueUser", formBody);
     }
     
     public static String postListSongs(){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("username", "")
                                        .build();
         return getString("canciones", formBody);
     }
     
     public static String postAddCola(String username, String anio, String genero, String artista,
                                        String album, String cancion){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("username", username)
                                        .add("anio", anio)
                                        .add("genero", genero)
                                        .add("artista", artista)
                                        .add("album", album)
                                        .add("cancion", cancion)
                                        .build();
         return getString("agregarCola", formBody); 
    }
     
     public static String postReproducir(String username, String anio, String genero, String artista,
                                        String album, String cancion){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("username", username)
                                        .add("anio", anio)
                                        .add("genero", genero)
                                        .add("artista", artista)
                                        .add("album", album)
                                        .add("cancion", cancion)
                                        .build();
         return getString("agregarCola", formBody); 
     }
     
     public static String postAfterSong(String username){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("username", username)
                                        .build();
         return getString("afterSong", formBody);
     }
     
     public static String postBeforeSong(String username){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("username", username)
                                        .build();
         String before = getString("beforeSong", formBody);
         return before;
     }
     
     public static String postSongsByArtist(String artista){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("artista", artista)
                                        .build();
         String before = getString("getSongsByArtist", formBody);
         return before;
     }
     
     public static String postSongsByAlbum(String album){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("album", album)
                                        .build();
         String before = getString("getSongsByAlbum", formBody);
         return before;
     }
     
     public static String postSongsByGender(String gender){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("genero", gender)
                                        .build();
         String before = getString("getSongsByGender", formBody);
         return before;
     }
     
     public static String postSongsByYear(String anio){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("anio", anio)
                                        .build();
         String before = getString("getSongsByYear", formBody);
         return before;
     }
     
     public static String postSongShuffle(){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("", "")
                                        .build();
         String before = getString("getSongShuffle", formBody);
         return before;
     }
     
     public static String postSearch(String cadena){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("cadena", cadena)
                                        .build();
         String before = getString("search", formBody);
         return before;
     }
     
     public static String verifyUserOAuth(){
         RequestBody formBody = new FormEncodingBuilder()
                                        .add("", "")
                                        .build();
         String before = getString("verifyUserOAuth", formBody);
         return before;
     }
    
}
