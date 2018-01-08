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

    
    public static String getString(String metodo, RequestBody formBody) {

        try {
            URL url = new URL("http://localhost:5000/" + metodo);
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
    
     public static String metodoPost(String parametroJava) {
        RequestBody formBody = new FormEncodingBuilder()
                .add("x", parametroJava)
                .build();
        String r = getString("metodos", formBody);
        System.out.println("respuesta:" + r);
        return r;
    }

    
    public static void main(String[] args) {
        metodoPost("secreto");
    }
    
}