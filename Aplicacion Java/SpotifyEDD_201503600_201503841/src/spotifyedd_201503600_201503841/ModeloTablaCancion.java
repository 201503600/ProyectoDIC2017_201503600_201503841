package spotifyedd_201503600_201503841;

import java.util.ArrayList;
import javax.swing.table.AbstractTableModel;

public class ModeloTablaCancion extends AbstractTableModel{
    
    private String[] columnas = {"Año","Genero","Artista","Album","Cancion"};
    private ArrayList<Cancion> listaCanciones;
    
    public ModeloTablaCancion(ListaCancion lista){
        this.listaCanciones = (ArrayList<Cancion>) lista.getCanciones();
    }

    @Override
    public int getRowCount() {
        return (this.listaCanciones == null)?0:this.listaCanciones.size();
    }

    @Override
    public int getColumnCount() {
        return columnas.length;
    }

    @Override
    public Object getValueAt(int rowIndex, int columnIndex) {
        Object auxiliar = null;
        if (columnIndex == 0)
            auxiliar = this.listaCanciones.get(rowIndex).getAnio();
        else if (columnIndex == 1)
            auxiliar = this.listaCanciones.get(rowIndex).getGenero();
        else if (columnIndex == 2)
            auxiliar = this.listaCanciones.get(rowIndex).getArtista();
        else if (columnIndex == 3)
            auxiliar = this.listaCanciones.get(rowIndex).getAlbum();
        else if (columnIndex == 4)
            auxiliar = this.listaCanciones.get(rowIndex).getCancion();
        return auxiliar;
    }
    
    public String getColumnName(int columnIndex){
        return columnas[columnIndex];
    }
    
    public Class getColumnClass(int columnIndex){
        return (columnIndex == 0)?Integer.class:String.class;
    }
    
}