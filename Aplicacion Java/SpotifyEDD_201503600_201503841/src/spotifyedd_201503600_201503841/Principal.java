/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package spotifyedd_201503600_201503841;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonParser;
import com.placeholder.PlaceHolder;
import java.awt.Image;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JOptionPane;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import javazoom.jl.decoder.JavaLayerException;
import javazoom.jlgui.basicplayer.BasicPlayer;

/**
 *
 * @author Suseth
 */
public class Principal extends javax.swing.JFrame implements ActionListener, ListSelectionListener {

    /**
     * Creates new form Principal
     */
    private JsonParser parser;
    private NewJFrame referencia;
    public Musica bocina;
    private Reproductor reproductor;
    private String userLogged;
    private ListaCancion canciones, playlist;
    private Cancion actual;
    private int stateReproductor;
    private boolean state;

    /*   
    
    Para el stateReproductor los siguientes valores:
        - 0: Reproduccion por playlist (se utiliza lista canciones)
        - 1: Reproduccion por shuffle
        - 2: Reproduccion por cualquier otro modo (se utiliza lista playlist)
    
     */

    public Principal(NewJFrame referencia, String jsonUser) {
        initComponents();

        //setIconImage(Toolkit.getDefaultToolkit().getImage(this.getClass().getResource("/Imagenes/logo - spot.png")));
        this.referencia = referencia;
        parser = new JsonParser();
        userLogged = parser.parse(jsonUser).getAsJsonObject().get("nombre").getAsString();
        actual = null;
        playlist = new ListaCancion();

        JsonArray array = parser.parse(Conexion.postEncabezadoAnios()).getAsJsonArray();
        for (int pos = 0; pos < array.size(); pos++) {
            jComboBox1.addItem(array.get(pos).getAsJsonObject().get("anio").getAsString());
        }
        array = parser.parse(Conexion.postEncabezadoGeneros()).getAsJsonArray();
        for (int pos = 0; pos < array.size(); pos++) {
            jComboBox2.addItem(array.get(pos).getAsJsonObject().get("genero").getAsString());
        }

        canciones = new Gson().fromJson(Conexion.postListSongs(), ListaCancion.class);
        jTable1.setModel(new ModeloTablaCancion(canciones));
        jTable1.setOpaque(false);
        ((DefaultTableCellRenderer) jTable1.getDefaultRenderer(Object.class)).setOpaque(false);
        jTable1.setShowVerticalLines(false);

        jScrollPane1.setOpaque(false);
        jScrollPane1.getViewport().setOpaque(false);
        jScrollPane1.setBorder(null);

        jList1.setOpaque(false);
        jList1.addListSelectionListener(this);
        jList1.setSelectedIndex(0);

        bocina = new Musica();
        state = false;
        stateReproductor = 0;

        jButton1.addActionListener(this);
        jButton2.addActionListener(this);
        jButton3.addActionListener(this);
        jButton4.addActionListener(this);
        jButton5.addActionListener(this);

        jMenuItem2.addActionListener(this);
        jMenuItem3.addActionListener(this);
        jMenuItem4.addActionListener(this);
        jMenuItem5.addActionListener(this);
        jMenuItem6.addActionListener(this);
        jMenuItem7.addActionListener(this);
        jMenuItem9.addActionListener(this);
        jMenuItem10.addActionListener(this);
        jMenuItem11.addActionListener(this);
        jMenuItem12.addActionListener(this);
        jMenuItem13.addActionListener(this);
        jMenuItem14.addActionListener(this);
        jMenuItem15.addActionListener(this);
        jMenuItem16.addActionListener(this);
        
        reproductor = new Reproductor(this);
        
        PlaceHolder holderUsername = new PlaceHolder(jTextField2, "Artista");
        holderUsername = new PlaceHolder(jTextField3, "Album");
        holderUsername = new PlaceHolder(jTextField4, "Cancion");

    }
    
    public void setLabelSong(){
        jLabel1.setText(actual.getArtista());
        jLabel6.setText(actual.getAlbum() + " - " + actual.getCancion());
    }

    @Override
    public void valueChanged(ListSelectionEvent e) {
        //JOptionPane.showMessageDialog(this, jList1.getSelectedValue());
        switch(jList1.getSelectedValue()){
            case "Canción":
                jTextField2.setEnabled(true);
                jTextField3.setEnabled(true);
                jTextField4.setEnabled(true);
                break;
            case "Artista":
                jTextField2.setEnabled(true);
                jTextField3.setEnabled(false);
                jTextField4.setEnabled(false);
                break;
            case "Año y Genero":
                jTextField2.setEnabled(false);
                jTextField3.setEnabled(false);
                jTextField4.setEnabled(false);
                break;
        }
    }
    
    public class Reproductor extends Thread{
        private Principal instancia;
        private boolean pausa;
        
        public Reproductor(Principal instancia){
            this.instancia = instancia;
            this.pausa = false;
        }
        
        @Override
        public void run(){
            while (true) {
                if (!pausa) {
                    if (instancia.bocina.player.getStatus() == BasicPlayer.STOPPED) {
                        instancia.afterSong();
                    }
                }
            }
        }
        
        public void setEstado(boolean pause){
            this.pausa = pause;
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == jButton1) {
            // Boton search            
            String search = jTextField1.getText();
            if (!search.equals("")){
                canciones = new Gson().fromJson(Conexion.postSearch(search), ListaCancion.class);
                jTable1.setModel(new ModeloTablaCancion(canciones));
                jTable1.repaint();
            }
        } else if (e.getSource() == jButton2) {
            // Boton play - pause de reproductor
            if (state) {
                jButton2.setIcon(new ImageIcon(this.getClass().getResource("/Imagenes/play.jpg")));
                try {
                    bocina.pausar();
                    reproductor.setEstado(true);
                } catch (Exception ex) {

                }
                state = false;
            } else {
                jButton2.setIcon(new ImageIcon(this.getClass().getResource("/Imagenes/pausa.jpg")));
                try {
                    if (actual != null) {
                        bocina.continuar();
                        reproductor.setEstado(false);
                    } else {
                        //bocina.Play();
                    }
                } catch (Exception ex) {
                    //JOptionPane.showMessageDialog(this, ex.toString());
                }
                state = true;
            }
            jButton2.repaint();
        } else if (e.getSource() == jButton3) {
            // Boton siguiente playlist           
            afterSong();
            setLabelSong();
        } else if (e.getSource() == jButton4) {
            // Boton anterior playlist           
            //reproducir
            beforeSong();
            setLabelSong();
        } else if (e.getSource() == jButton5) {
            // Boton eliminar            
            String anio, genero, artista;
            anio = jComboBox1.getSelectedItem().toString();
            genero = jComboBox2.getSelectedItem().toString();
            switch (jList1.getSelectedIndex()) {
                case 2:
                    String cancion = jTextField4.getText();
                    String album = jTextField3.getText();
                    artista = jTextField2.getText();
                    try{
                        Conexion.postDeleteSong(anio, genero, artista, album, cancion);
                        canciones = new Gson().fromJson(Conexion.postListSongs(), ListaCancion.class);
                        jTable1.setModel(new ModeloTablaCancion(canciones));
                        jTable1.repaint();
                    }catch(Exception ex){}
                    break;
                case 1:
                    artista = jTextField2.getText();
                    try{
                        Conexion.postDeleteArtist(anio, genero, artista);
                        canciones = new Gson().fromJson(Conexion.postListSongs(), ListaCancion.class);
                        jTable1.setModel(new ModeloTablaCancion(canciones));
                        jTable1.repaint();
                    }catch(Exception ex){}
                    break;
                case 0:
                    try{
                        Conexion.postDeleteNodoMatriz(anio, genero);
                        canciones = new Gson().fromJson(Conexion.postListSongs(), ListaCancion.class);
                        jComboBox1.removeItem(anio);
                        jComboBox2.removeItem(genero);
                        jTable1.setModel(new ModeloTablaCancion(canciones));
                        jTable1.repaint();
                    }catch(Exception ex){
                    }
                    break;
            }
        } else if (e.getSource() == jMenuItem2) {
            // Reporte Matriz Dispersa            
            Conexion.postReportMatriz();
        } else if (e.getSource() == jMenuItem3) {
            // Reporte Arbol B            
            Conexion.postReportArtistas(jComboBox1.getSelectedItem().toString(), jComboBox2.getSelectedItem().toString());
        } else if (e.getSource() == jMenuItem4) {
            // Reporte ABB            
            Conexion.postReportAlbums(jComboBox1.getSelectedItem().toString(),
                    jComboBox2.getSelectedItem().toString(),
                    jTextField2.getText());
        } else if (e.getSource() == jMenuItem5) {
            // Reporte Lista Canciones            
            Conexion.postReportListSongs(jComboBox1.getSelectedItem().toString(),
                    jComboBox2.getSelectedItem().toString(),
                    jTextField2.getText(),
                    jTextField3.getText());
        } else if (e.getSource() == jMenuItem6) {
            // Reporte Usuarios            
            Conexion.postReportUsers();
        } else if (e.getSource() == jMenuItem7) {
            // Reporte Cola Playlist            
            Conexion.postReportQueueUser(userLogged);
        } else if (e.getSource() == jMenuItem9) {
            // reproducction por artista 
            stateReproductor = 2;           
            String artista = JOptionPane.showInputDialog(null, "Escribe el nombre del artista");
            if (!artista.equals("")) {
                
                try{
                    playlist = new Gson().fromJson(Conexion.postSongsByArtist(artista, userLogged), ListaCancion.class);
                    actual = playlist.getCanciones().get(0);
                    reproducir();
                    setLabelSong();
                }catch(Exception ex){
                    System.out.println(ex.toString());
                }
            }
        } else if (e.getSource() == jMenuItem10) {
            // reproduccion por album
            stateReproductor = 2;
            String cancion = JOptionPane.showInputDialog(null, "Escribe el nombre del album");
            if (!cancion.equals("")) {
                try{
                    playlist = new Gson().fromJson(Conexion.postSongsByAlbum(cancion, userLogged), ListaCancion.class);
                    actual = playlist.getCanciones().get(0);
                    reproducir();
                    setLabelSong();
                }catch(Exception ex){
                    System.out.println(ex.toString());
                }
            }
        } else if (e.getSource() == jMenuItem11) {
            // reproduccion por genero
            stateReproductor = 2;
            String cancion = JOptionPane.showInputDialog(null, "Escribe el nombre del genero");
            if (!cancion.equals("")) {
                try{
                    playlist = new Gson().fromJson(Conexion.postSongsByGender(cancion, userLogged), ListaCancion.class);
                    actual = playlist.getCanciones().get(0);
                    reproducir();
                    setLabelSong();
                }catch(Exception ex){
                    System.out.println(ex.toString());
                }
            }
        } else if (e.getSource() == jMenuItem12) {
            // reproduccion por a;o
            stateReproductor = 2;
            String cancion = JOptionPane.showInputDialog(null, "Escribe el anio");
            if (!cancion.equals("")) {
                try{
                    playlist = new Gson().fromJson(Conexion.postSongsByYear(cancion, userLogged), ListaCancion.class);
                    actual = playlist.getCanciones().get(0);
                    reproducir();
                    setLabelSong();
                }catch(Exception ex){
                    System.out.println(ex.toString());
                }
            }
        } else if (e.getSource() == jMenuItem13) {
            // reproduccion playlist
            stateReproductor = 0;
            try{
                actual = playlist.getCanciones().get(0);
                reproducir();
                setLabelSong();
            }catch(Exception ex){
                System.out.println(ex.toString());
            }
        } else if (e.getSource() == jMenuItem14) {
            // reproduccion shuffle
            stateReproductor = 1;
            try{
                actual = new Gson().fromJson(Conexion.postSongShuffle(), Cancion.class);
                reproducir();
                setLabelSong();
            }catch(Exception ex){}
        } else if (e.getSource() == jMenuItem15) {
            // Cerrar sesion            
            Conexion.logout();
            this.referencia.show();
            this.referencia.limpiar();
            this.dispose();
        } else if (e.getSource() == jMenuItem16) {
            // Eliminar cuenta
            Conexion.logout();
            Conexion.postDeleteUser(userLogged);
            this.referencia.show();
            this.referencia.limpiar();
            this.dispose();
        }
    }

    private void reproducir() {
        try {
            if (stateReproductor == 0 && actual == null) {
                actual = new Gson().fromJson(Conexion.postAfterSong(userLogged), Cancion.class);
            }
            //reproducir
            System.out.println(actual.getPath());
            bocina.AbrirArchivo(actual.getPath());
            bocina.Play();
            state = true;
            setLabelSong();
            if (reproductor.getState() == Thread.State.NEW)
                reproductor.start();
            //jButton2.setIcon(new ImageIcon(this.getClass().getResource("/Imagenes/pause.jpg")));
            //jButton2.repaint();
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "No se pudo reproducir la cancion");
            //JOptionPane.showMessageDialog(this, ex.toString());
        }
    }

    private void afterSong() {
        switch (stateReproductor) {
            case 0:
                try {
                    int indice = playlist.getCanciones().indexOf(actual);
                    if (indice < playlist.getCanciones().size() - 1) {
                        actual = playlist.getCanciones().get(indice + 1);
                    } else {
                        actual = playlist.getCanciones().get(0);
                    }
                    reproducir();
                } catch (Exception ex) {
                    //JOptionPane.showMessageDialog(this, ex.toString());
                }
                break;
            case 1:
                try {
                    actual = new Gson().fromJson(Conexion.postSongShuffle(), Cancion.class);
                    reproducir();
                } catch (Exception ex) {
                    //JOptionPane.showMessageDialog(this, ex.toString());
                }
                break;
            case 2:
                try {
                    int indice = playlist.getCanciones().indexOf(actual);
                    if (indice < playlist.getCanciones().size() - 1) {
                        actual = playlist.getCanciones().get(indice + 1);
                    } else {
                        actual = playlist.getCanciones().get(0);
                    }
                    reproducir();
                } catch (Exception ex) {
                    //JOptionPane.showMessageDialog(this, ex.toString());
                }
                break;
        }
        setLabelSong();
    }

    private void beforeSong() {
        switch (stateReproductor) {
            case 0:
                try {
                    int indice = playlist.getCanciones().indexOf(actual);
                    if (indice > 0) {
                        actual = playlist.getCanciones().get(indice - 1);
                    } else {
                        actual = playlist.getCanciones().get(playlist.getCanciones().size() - 1);
                    }
                    reproducir();
                } catch (Exception ex) {
                    //JOptionPane.showMessageDialog(this, ex.toString());
                }
                break;
            case 1:

            case 2:
                try {
                    int indice = playlist.getCanciones().indexOf(actual);
                    if (indice > 0) {
                        actual = playlist.getCanciones().get(indice - 1);
                    } else {
                        actual = playlist.getCanciones().get(playlist.getCanciones().size() - 1);
                    }
                    reproducir();
                } catch (Exception ex) {
                    //JOptionPane.showMessageDialog(this, ex.toString());
                }
                break;
        }
        setLabelSong();
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jPopupMenu1 = new javax.swing.JPopupMenu();
        jMenuItem1 = new javax.swing.JMenuItem();
        jSeparator1 = new javax.swing.JPopupMenu.Separator();
        jMenuItem8 = new javax.swing.JMenuItem();
        jScrollPane1 = new javax.swing.JScrollPane();
        jTable1 = new javax.swing.JTable();
        jComboBox1 = new javax.swing.JComboBox<>();
        jComboBox2 = new javax.swing.JComboBox<>();
        jLabel4 = new javax.swing.JLabel();
        jLabel5 = new javax.swing.JLabel();
        jLabel2 = new javax.swing.JLabel();
        jPanel1 = new javax.swing.JPanel();
        jTextField1 = new javax.swing.JTextField();
        jLabel3 = new javax.swing.JLabel();
        jScrollPane2 = new javax.swing.JScrollPane();
        jList1 = new javax.swing.JList<>();
        jButton1 = new javax.swing.JButton();
        jButton5 = new javax.swing.JButton();
        jSeparator3 = new javax.swing.JSeparator();
        jLabel7 = new javax.swing.JLabel();
        jTextField2 = new javax.swing.JTextField();
        jLabel8 = new javax.swing.JLabel();
        jLabel9 = new javax.swing.JLabel();
        jTextField3 = new javax.swing.JTextField();
        jTextField4 = new javax.swing.JTextField();
        jPanel2 = new javax.swing.JPanel();
        jButton3 = new javax.swing.JButton();
        jButton2 = new javax.swing.JButton();
        jButton4 = new javax.swing.JButton();
        jLabel1 = new javax.swing.JLabel();
        jLabel6 = new javax.swing.JLabel();
        jMenuBar1 = new javax.swing.JMenuBar();
        jMenu3 = new javax.swing.JMenu();
        jMenu4 = new javax.swing.JMenu();
        jMenuItem15 = new javax.swing.JMenuItem();
        jSeparator2 = new javax.swing.JPopupMenu.Separator();
        jMenuItem16 = new javax.swing.JMenuItem();
        jMenu6 = new javax.swing.JMenu();
        jMenuItem9 = new javax.swing.JMenuItem();
        jMenuItem10 = new javax.swing.JMenuItem();
        jMenuItem11 = new javax.swing.JMenuItem();
        jMenuItem12 = new javax.swing.JMenuItem();
        jMenuItem13 = new javax.swing.JMenuItem();
        jMenuItem14 = new javax.swing.JMenuItem();
        jMenu5 = new javax.swing.JMenu();
        jMenuItem2 = new javax.swing.JMenuItem();
        jMenuItem3 = new javax.swing.JMenuItem();
        jMenuItem4 = new javax.swing.JMenuItem();
        jMenuItem5 = new javax.swing.JMenuItem();
        jMenuItem6 = new javax.swing.JMenuItem();
        jMenuItem7 = new javax.swing.JMenuItem();

        jMenuItem1.setText("Añadir a cola ...");
        jMenuItem1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem1ActionPerformed(evt);
            }
        });
        jPopupMenu1.add(jMenuItem1);
        jPopupMenu1.add(jSeparator1);

        jMenuItem8.setText("Reproducir");
        jMenuItem8.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem8ActionPerformed(evt);
            }
        });
        jPopupMenu1.add(jMenuItem8);

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setTitle("Spotify - USAC");
        setBackground(java.awt.SystemColor.windowText);
        getContentPane().setLayout(new org.netbeans.lib.awtextra.AbsoluteLayout());

        jTable1.setBackground(new java.awt.Color(0, 0, 0));
        jTable1.setForeground(new java.awt.Color(255, 255, 255));
        jTable1.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {

            },
            new String [] {
                "TITULO", "GENERO", "ARTISTA", "ALBUM", "AÑO"
            }
        ) {
            boolean[] canEdit = new boolean [] {
                false, false, false, false, false
            };

            public boolean isCellEditable(int rowIndex, int columnIndex) {
                return canEdit [columnIndex];
            }
        });
        jTable1.setComponentPopupMenu(jPopupMenu1);
        jScrollPane1.setViewportView(jTable1);
        if (jTable1.getColumnModel().getColumnCount() > 0) {
            jTable1.getColumnModel().getColumn(0).setResizable(false);
            jTable1.getColumnModel().getColumn(1).setResizable(false);
            jTable1.getColumnModel().getColumn(2).setResizable(false);
            jTable1.getColumnModel().getColumn(3).setResizable(false);
            jTable1.getColumnModel().getColumn(4).setResizable(false);
        }

        getContentPane().add(jScrollPane1, new org.netbeans.lib.awtextra.AbsoluteConstraints(230, 150, 430, 200));

        jComboBox1.setBackground(new java.awt.Color(0, 0, 0));
        jComboBox1.setForeground(new java.awt.Color(255, 255, 255));
        getContentPane().add(jComboBox1, new org.netbeans.lib.awtextra.AbsoluteConstraints(560, 50, 100, -1));

        jComboBox2.setBackground(new java.awt.Color(0, 0, 0));
        jComboBox2.setForeground(new java.awt.Color(255, 255, 255));
        getContentPane().add(jComboBox2, new org.netbeans.lib.awtextra.AbsoluteConstraints(560, 90, 100, -1));

        jLabel4.setFont(new java.awt.Font("Tahoma", 1, 14)); // NOI18N
        jLabel4.setForeground(new java.awt.Color(255, 255, 255));
        jLabel4.setText("Año");
        getContentPane().add(jLabel4, new org.netbeans.lib.awtextra.AbsoluteConstraints(520, 50, -1, -1));

        jLabel5.setFont(new java.awt.Font("Tahoma", 1, 14)); // NOI18N
        jLabel5.setForeground(new java.awt.Color(255, 255, 255));
        jLabel5.setText("Genero");
        getContentPane().add(jLabel5, new org.netbeans.lib.awtextra.AbsoluteConstraints(500, 90, -1, -1));

        jLabel2.setIcon(new javax.swing.ImageIcon(getClass().getResource("/Imagenes/fondo1.jpg"))); // NOI18N
        getContentPane().add(jLabel2, new org.netbeans.lib.awtextra.AbsoluteConstraints(190, 0, 510, 370));

        jPanel1.setBackground(new java.awt.Color(0, 0, 0));
        jPanel1.setFont(new java.awt.Font("Tahoma", 0, 36)); // NOI18N

        jTextField1.setHorizontalAlignment(javax.swing.JTextField.RIGHT);

        jLabel3.setIcon(new javax.swing.ImageIcon(getClass().getResource("/Imagenes/SpotifyBlanco.JPG"))); // NOI18N

        jList1.setBackground(new java.awt.Color(0, 0, 0));
        jList1.setForeground(new java.awt.Color(255, 255, 255));
        jList1.setModel(new javax.swing.AbstractListModel<String>() {
            String[] strings = { "Año y Genero", "Artista", "Canción" };
            public int getSize() { return strings.length; }
            public String getElementAt(int i) { return strings[i]; }
        });
        jList1.setSelectionBackground(new java.awt.Color(255, 255, 255));
        jList1.setSelectionForeground(new java.awt.Color(0, 153, 255));
        jScrollPane2.setViewportView(jList1);

        jButton1.setBackground(new java.awt.Color(0, 0, 0));
        jButton1.setIcon(new javax.swing.ImageIcon(getClass().getResource("/Imagenes/lupita.JPG"))); // NOI18N
        jButton1.setBorder(null);
        jButton1.setName(""); // NOI18N

        jButton5.setBackground(new java.awt.Color(0, 204, 51));
        jButton5.setForeground(new java.awt.Color(255, 255, 255));
        jButton5.setText("Eliminar");

        jLabel7.setForeground(new java.awt.Color(255, 255, 255));
        jLabel7.setText("Artista");

        jTextField2.setHorizontalAlignment(javax.swing.JTextField.CENTER);

        jLabel8.setForeground(new java.awt.Color(255, 255, 255));
        jLabel8.setText("Album");

        jLabel9.setForeground(new java.awt.Color(255, 255, 255));
        jLabel9.setText("Cancion");

        jTextField3.setHorizontalAlignment(javax.swing.JTextField.CENTER);

        jTextField4.setHorizontalAlignment(javax.swing.JTextField.CENTER);

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jSeparator3, javax.swing.GroupLayout.Alignment.TRAILING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(jLabel3))
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(22, 22, 22)
                        .addComponent(jTextField1, javax.swing.GroupLayout.PREFERRED_SIZE, 120, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jButton1, javax.swing.GroupLayout.PREFERRED_SIZE, 27, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(28, 28, 28)
                        .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 111, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                                .addComponent(jLabel8, javax.swing.GroupLayout.Alignment.LEADING)
                                .addGroup(jPanel1Layout.createSequentialGroup()
                                    .addGap(10, 10, 10)
                                    .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                                        .addComponent(jTextField4)
                                        .addComponent(jTextField3, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.PREFERRED_SIZE, 127, javax.swing.GroupLayout.PREFERRED_SIZE))))
                            .addComponent(jLabel9)))
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(jPanel1Layout.createSequentialGroup()
                                .addGap(10, 10, 10)
                                .addComponent(jTextField2, javax.swing.GroupLayout.PREFERRED_SIZE, 127, javax.swing.GroupLayout.PREFERRED_SIZE))
                            .addComponent(jLabel7)))
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(44, 44, 44)
                        .addComponent(jButton5)))
                .addContainerGap(15, Short.MAX_VALUE))
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jLabel3, javax.swing.GroupLayout.PREFERRED_SIZE, 34, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(18, 18, 18)
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jTextField1, javax.swing.GroupLayout.PREFERRED_SIZE, 22, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jButton1, javax.swing.GroupLayout.PREFERRED_SIZE, 22, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jSeparator3, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jLabel7)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jTextField2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jLabel8)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jTextField3, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jLabel9)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(jTextField4, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(18, 18, 18)
                .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 57, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(18, 18, 18)
                .addComponent(jButton5)
                .addGap(19, 19, 19))
        );

        getContentPane().add(jPanel1, new org.netbeans.lib.awtextra.AbsoluteConstraints(0, 0, 190, 370));

        jPanel2.setBackground(new java.awt.Color(51, 51, 51));

        jButton3.setIcon(new javax.swing.ImageIcon(getClass().getResource("/Imagenes/next.JPG"))); // NOI18N
        jButton3.setBorder(null);

        jButton2.setIcon(new javax.swing.ImageIcon(getClass().getResource("/Imagenes/play.JPG"))); // NOI18N
        jButton2.setBorder(null);

        jButton4.setIcon(new javax.swing.ImageIcon(getClass().getResource("/Imagenes/back.JPG"))); // NOI18N
        jButton4.setBorder(null);

        jLabel1.setFont(new java.awt.Font("Century Gothic", 1, 14)); // NOI18N
        jLabel1.setForeground(new java.awt.Color(255, 255, 255));

        jLabel6.setFont(new java.awt.Font("Century Gothic", 0, 11)); // NOI18N
        jLabel6.setForeground(new java.awt.Color(255, 255, 255));

        javax.swing.GroupLayout jPanel2Layout = new javax.swing.GroupLayout(jPanel2);
        jPanel2.setLayout(jPanel2Layout);
        jPanel2Layout.setHorizontalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel2Layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addComponent(jLabel6)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 287, Short.MAX_VALUE)
                        .addComponent(jButton4, javax.swing.GroupLayout.PREFERRED_SIZE, 23, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addComponent(jLabel1)
                        .addGap(0, 0, Short.MAX_VALUE)))
                .addGap(18, 18, 18)
                .addComponent(jButton2, javax.swing.GroupLayout.PREFERRED_SIZE, 40, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(18, 18, 18)
                .addComponent(jButton3)
                .addGap(281, 281, 281))
        );
        jPanel2Layout.setVerticalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addGap(19, 19, 19)
                        .addComponent(jButton3))
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addGap(19, 19, 19)
                        .addComponent(jButton4))
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(jButton2, javax.swing.GroupLayout.PREFERRED_SIZE, 41, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addGap(5, 5, 5)
                        .addComponent(jLabel1)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jLabel6)))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        getContentPane().add(jPanel2, new org.netbeans.lib.awtextra.AbsoluteConstraints(0, 370, 700, 60));

        jMenuBar1.setBackground(java.awt.SystemColor.windowText);

        jMenu3.setIcon(new javax.swing.ImageIcon(getClass().getResource("/Imagenes/spotifymini.JPG"))); // NOI18N
        jMenuBar1.add(jMenu3);

        jMenu4.setForeground(new java.awt.Color(255, 255, 255));
        jMenu4.setText("Cuenta");
        jMenu4.setFont(new java.awt.Font("Segoe UI", 0, 18)); // NOI18N

        jMenuItem15.setText("Cerrar sesion ");
        jMenu4.add(jMenuItem15);
        jMenu4.add(jSeparator2);

        jMenuItem16.setText("Eliminar cuenta");
        jMenu4.add(jMenuItem16);

        jMenuBar1.add(jMenu4);

        jMenu6.setForeground(new java.awt.Color(255, 255, 255));
        jMenu6.setText("Reproducir");
        jMenu6.setFont(new java.awt.Font("Segoe UI", 0, 18)); // NOI18N

        jMenuItem9.setText("Por artista ...");
        jMenu6.add(jMenuItem9);

        jMenuItem10.setText("Por album ...");
        jMenu6.add(jMenuItem10);

        jMenuItem11.setText("Por genero ...");
        jMenu6.add(jMenuItem11);

        jMenuItem12.setText("Por año ...");
        jMenu6.add(jMenuItem12);

        jMenuItem13.setText("Playlist");
        jMenu6.add(jMenuItem13);

        jMenuItem14.setText("Shuffle play");
        jMenu6.add(jMenuItem14);

        jMenuBar1.add(jMenu6);

        jMenu5.setForeground(new java.awt.Color(255, 255, 255));
        jMenu5.setText("Reportes");
        jMenu5.setFont(new java.awt.Font("Segoe UI", 0, 18)); // NOI18N

        jMenuItem2.setText("Reporte Matriz Dispersa");
        jMenu5.add(jMenuItem2);

        jMenuItem3.setText("Reporte Artistas (Arbol B)");
        jMenu5.add(jMenuItem3);

        jMenuItem4.setText("Reporte Albums (ABB)");
        jMenu5.add(jMenuItem4);

        jMenuItem5.setText("Reporte Canciones");
        jMenu5.add(jMenuItem5);

        jMenuItem6.setText("Reporte Usuarios");
        jMenu5.add(jMenuItem6);

        jMenuItem7.setText("Reporte Playlist");
        jMenu5.add(jMenuItem7);

        jMenuBar1.add(jMenu5);

        setJMenuBar(jMenuBar1);

        pack();
    }// </editor-fold>//GEN-END:initComponents
    // Anadir a cola
    private void jMenuItem1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem1ActionPerformed
        int index = jTable1.getSelectedRow();
        //anadir a cola
        try{
            String cancion = Conexion.postAddCola(userLogged, String.valueOf(canciones.getCanciones().get(index).getAnio()),
                                                                                canciones.getCanciones().get(index).getGenero(),
                                                                                canciones.getCanciones().get(index).getArtista(),
                                                                                canciones.getCanciones().get(index).getAlbum(),
                                                                                canciones.getCanciones().get(index).getCancion());
            playlist.getCanciones().add(new Gson().fromJson(cancion, Cancion.class));
        }catch(Exception e){
            System.out.println(e.toString());
        }

    }//GEN-LAST:event_jMenuItem1ActionPerformed
    // Reproducir
    private void jMenuItem8ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem8ActionPerformed
        int index = jTable1.getSelectedRow();
        //reproducir
        try {
            //reproducir
            actual = new Gson().fromJson(Conexion.postAddCola(userLogged,
                    String.valueOf(canciones.getCanciones().get(index).getAnio()),
                    canciones.getCanciones().get(index).getGenero(),
                    canciones.getCanciones().get(index).getArtista(),
                    canciones.getCanciones().get(index).getAlbum(),
                    canciones.getCanciones().get(index).getCancion()), Cancion.class);

            reproducir();
        } catch (Exception ex) {
            //JOptionPane.showMessageDialog(this, ex.toString());
        }
    }//GEN-LAST:event_jMenuItem8ActionPerformed

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(Principal.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(Principal.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(Principal.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(Principal.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                //new Principal("").setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton jButton1;
    private javax.swing.JButton jButton2;
    private javax.swing.JButton jButton3;
    private javax.swing.JButton jButton4;
    private javax.swing.JButton jButton5;
    private javax.swing.JComboBox<String> jComboBox1;
    private javax.swing.JComboBox<String> jComboBox2;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JLabel jLabel5;
    private javax.swing.JLabel jLabel6;
    private javax.swing.JLabel jLabel7;
    private javax.swing.JLabel jLabel8;
    private javax.swing.JLabel jLabel9;
    private javax.swing.JList<String> jList1;
    private javax.swing.JMenu jMenu3;
    private javax.swing.JMenu jMenu4;
    private javax.swing.JMenu jMenu5;
    private javax.swing.JMenu jMenu6;
    private javax.swing.JMenuBar jMenuBar1;
    private javax.swing.JMenuItem jMenuItem1;
    private javax.swing.JMenuItem jMenuItem10;
    private javax.swing.JMenuItem jMenuItem11;
    private javax.swing.JMenuItem jMenuItem12;
    private javax.swing.JMenuItem jMenuItem13;
    private javax.swing.JMenuItem jMenuItem14;
    private javax.swing.JMenuItem jMenuItem15;
    private javax.swing.JMenuItem jMenuItem16;
    private javax.swing.JMenuItem jMenuItem2;
    private javax.swing.JMenuItem jMenuItem3;
    private javax.swing.JMenuItem jMenuItem4;
    private javax.swing.JMenuItem jMenuItem5;
    private javax.swing.JMenuItem jMenuItem6;
    private javax.swing.JMenuItem jMenuItem7;
    private javax.swing.JMenuItem jMenuItem8;
    private javax.swing.JMenuItem jMenuItem9;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel2;
    private javax.swing.JPopupMenu jPopupMenu1;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JPopupMenu.Separator jSeparator1;
    private javax.swing.JPopupMenu.Separator jSeparator2;
    private javax.swing.JSeparator jSeparator3;
    private javax.swing.JTable jTable1;
    private javax.swing.JTextField jTextField1;
    private javax.swing.JTextField jTextField2;
    private javax.swing.JTextField jTextField3;
    private javax.swing.JTextField jTextField4;
    // End of variables declaration//GEN-END:variables

}
