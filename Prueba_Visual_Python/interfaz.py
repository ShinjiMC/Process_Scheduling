import tkinter as tk
from tkinter import ttk
import pandas as pd


def load_csv_data():
    try:
        # Intenta leer el archivo CSV usando el delimitador de coma
        data = pd.read_csv('../src/showFCSNormal.csv', sep=',', engine='python', header=0)
        return data
    except FileNotFoundError:
        return None


def show_data():
    csv_data = load_csv_data()
    if csv_data is not None:
        print("Número de columnas en el archivo CSV:", len(csv_data.columns))  # Imprime el número de columnas

        # Borrar columnas existentes en el Treeview
        for col in tree.get_children():
            tree.delete(col)

        # Establecer encabezados automáticamente
        tree["columns"] = list(csv_data.columns)
        for col in csv_data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Insertar datos
        for i, row in csv_data.iterrows():
            tree.insert("", "end", values=list(row))


# Configuración de la ventana principal
root = tk.Tk()
root.title("Interfaz CSV")

# Frame izquierdo para la tabla
tree = ttk.Treeview(root)
tree.pack(side=tk.LEFT)  # Empaqueta el Treeview a la izquierda

# Botón para cargar y mostrar datos
load_button = tk.Button(root, text="Cargar datos CSV", command=show_data)
load_button.pack()

# Llamar a show_data después de que tree haya sido definido
show_data()

root.mainloop()
