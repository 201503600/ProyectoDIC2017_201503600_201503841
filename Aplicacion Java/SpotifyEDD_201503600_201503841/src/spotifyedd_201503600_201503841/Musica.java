/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package spotifyedd_201503600_201503841;
import java.io.File;
import javazoom.jlgui.basicplayer.BasicPlayer;

/**
 *
 * @author Suseth
 */
public class Musica {
    public BasicPlayer player;
    
    public Musica(){
        player = new BasicPlayer();
    }
    public void Play() throws Exception {
        player.play();
    }

    public void AbrirArchivo(String ruta) throws Exception {
        player.open(new File(ruta));
    }

    public void pausar() throws Exception {
        player.pause();
    }

    public void continuar() throws Exception {
        player.resume();
    }

    public void Stop() throws Exception {
        player.stop();
    }
    
      public void ReproducirCancion () throws Exception{
       try {
        Musica reproduciendo = new Musica();
            reproduciendo.AbrirArchivo("C:/Users/Suseth/Music/Camila   Solo Para Ti (Alt. Version).mp3");
            reproduciendo.Play();
        } catch (Exception ex) {
            System.out.println("error : " + ex.getMessage());
        }
       
    }
    public static void main(String args[]) throws Exception{
     Musica llamando = new Musica();
     llamando.AbrirArchivo("C:/Users/Suseth/Music/Camila   Solo Para Ti (Alt. Version).mp3");
     llamando.Play();
    }
    
}