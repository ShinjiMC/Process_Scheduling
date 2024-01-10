from ctypes import cdll
from pathlib import Path
import matplotlib.pyplot as plt
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import ttk
import pandas as pd
from tkinter import  Label
import tkinter as tk
import subprocess
import csv
from tkinter import ttk, Scrollbar, VERTICAL
mi_canvas = None
id_penultimo = None
id_ultimo = None

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame0")

def execute():
    compilation_command = "make"
    execution_command = "./bin/main"
    try:
        subprocess.run(compilation_command, shell=True, check=True, capture_output=True)
        subprocess.run(execution_command, shell=True, check=True, capture_output=True)
        print("Loaded Successfully")
    except subprocess.CalledProcessError as error:
        print(f"Error compiling. Please check the errors: {error}")

def draw_gantt_chart(processes):
    fig, gnt = plt.subplots()

    gnt.set_title('Gantt Chart')
    gnt.set_xlabel('Tiempo')
    gnt.set_ylabel('Procesos')

    yticks = []
    labels = []

    for i, proc in enumerate(processes):
        # Utiliza la llegada absoluta y el tiempo de ráfaga absoluto
        gnt.broken_barh([(proc['Arrival Time'], proc['Burst Time'])], (10 * i, 5), facecolors=('red'))
        yticks.append(10 * i + 5)
        labels.append(f'P{proc["PID"]}')

    gnt.set_yticks(yticks)
    gnt.set_yticklabels(labels)

    plt.savefig('gantt_chart.png')  # Guardar la gráfica como imagen
    # plt.show()  # Esta línea mostraría la gráfica en pantalla, coméntala si no necesitas visualización interactiva


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class LineaTiempoFrame(tk.Frame):
    def __init__(self, master, lista_procesos, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.lista_procesos = lista_procesos
        self.iniciar_interfaz()

    def iniciar_interfaz(self):
        self.canvas = tk.Canvas(self, width=1045, height=108)
        self.canvas.pack(side="top", fill="both", expand=True)

        scrollbar_horizontal = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        scrollbar_horizontal.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=scrollbar_horizontal.set)

        index = 0
        self.graficar_linea_tiempo_paso_a_paso(index)

    def obtener_color(self, proceso_index):
        colores = ["lightblue", "lightgreen", "lightcoral", "lightyellow", "lightpink"]
        return colores[proceso_index % len(colores)]

    def graficar_linea_tiempo_paso_a_paso(self, index, posicion_actual=0, tiempo_acumulado=0):
        if index < len(self.lista_procesos):
            proceso = self.lista_procesos[index]
            x_inicio = posicion_actual
            ancho_rectangulo = 50  # Puedes ajustar este valor según tus necesidades
            x_fin = x_inicio + ancho_rectangulo
            y_inicio = 20
            y_fin = 80
            color = self.obtener_color(index)

            self.canvas.create_rectangle(x_inicio, y_inicio, x_fin, y_fin, fill=color)
            self.canvas.create_text((x_inicio + x_fin) / 2, (y_inicio + y_fin) / 2,
                                    text=f"PID: {proceso[0]}", font=("Arial", 8), fill="black")
            self.canvas.create_text(x_inicio, y_fin + 5, anchor=tk.W,
                                    text=f"{tiempo_acumulado}", font=("Arial", 8), fill="black")

            self.after(1000, self.graficar_linea_tiempo_paso_a_paso, index + 1, x_fin, tiempo_acumulado + proceso[2])
            self.canvas.xview_moveto(1)  # Mover la barra de desplazamiento al final

def cargar_procesos_desde_csv(archivo):
    procesos = []

    with open(archivo, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Saltar la primera fila (encabezado)
        
        for row in reader:
            if len(row) >= 3:  # Asegurarse de que hay al menos tres elementos en la fila
                procesos.append((int(row[0]), row[1], int(row[2])))

    return procesos

def visualizar_grafico(archivo_csv, id_algoritmo):
    global mi_frame

    # Verificar si el id_algoritmo es 5
    if id_algoritmo == '5':
        # Borrar el contenido del frame si el id_algoritmo es 5
        mi_frame.destroy()
        return

    # Cargar procesos desde el archivo CSV
    lista_procesos = cargar_procesos_desde_csv(archivo_csv)

    # Crear un nuevo frame si no es el id_algoritmo 5
    mi_frame = LineaTiempoFrame(window, lista_procesos )
    mi_frame.place(x=26, y=570)

    # Puedes agregar más elementos y configuraciones a la ventana principal aquí

def load_csv_data(opcion):
    file_paths = {
        '1': './static/Process.csv',
        '2': './static/algorithmFCFS.csv',
        '3': './static/algorithmSJF.csv',
        '4': './static/algorithmRR.csv',
        '5': './static/OrderViewFCFS.csv',
        '6': './static/OrderViewSJF.csv',
        '7': './static/OrderViewRR.csv',
    }

    if opcion in file_paths:
        if opcion in ['5', '6', '7']:
            return file_paths[opcion]
        else:
            try:
                data = pd.read_csv(file_paths[opcion], sep=',', engine='python', header=0)
                id_penultimo, id_ultimo = mostrar_numeros_desde_archivo(file_paths[opcion], canvas)
                return data
            except FileNotFoundError:
                print("Error: File not found.")
                return None
    else:
        print("Invalid option. Please select a valid option.")
        return None

def clear_data():
    for col in tree_1.get_children():
        tree_1.delete(col)

    for col in tree_2.get_children():
        tree_2.delete(col)

    # Destroy the Canvas (mi_canvas) if it exists
    if mi_canvas:
        mi_canvas.destroy()
        
def mostrar_numeros_desde_archivo(file_path, canvas):
    with open(file_path, 'r') as file:
        lineas = file.readlines()

    try:
        penultimo_numero = float(lineas[-2].split()[-1])
        ultimo_numero = float(lineas[-1].split()[-1])
    except (ValueError, IndexError) as e:
        print(f"Error al procesar el archivo: {e}")
        return None, None

    canvas.delete("penultimo_texto")
    canvas.delete("ultimo_texto")
    # Crear textos y devolver los ID
    id_penultimo = canvas.create_text(
        692.0,
        195.0,
        anchor="nw",
        text=f"{penultimo_numero}",
        fill="black",
        font=("Inter Bold", 14 * -1),
        tags="penultimo_texto"  # Agregar un tag para identificar este texto
    )
    id_ultimo = canvas.create_text(
        925.0,
        195.0,
        anchor="nw",
        text=f"{ultimo_numero}",
        fill="black",
        font=("Inter Bold", 14 * -1),
        tags="ultimo_texto"  # Agregar un tag para identificar este texto

    )

    return id_penultimo, id_ultimo


def show_data(id_primer,id_segundo):
    global mi_canvas

    csv_process_1 = load_csv_data('1')
    csv_process_2 = load_csv_data(id_primer)
    csv_process_3 = load_csv_data(id_segundo)
    if csv_process_1 is not None:
        # Borrar columnas existentes en el Treeview
        for col in tree_1.get_children():
            tree_1.delete(col)

        # Establecer encabezados automáticamente
        tree_1["columns"] = list(csv_process_1.columns)
        for col in csv_process_1.columns:
            tree_1.heading(col, text=col)
            tree_1.column(col, width=100)

        # Insertar datos
        for i, row in csv_process_1.iterrows():
            tree_1.insert("", "end", values=list(row))
    if csv_process_2 is not None:
        # Borrar columnas existentes en el Treeview
        for col in tree_2.get_children():
            tree_2.delete(col)

        # Establecer encabezados automáticamente
        tree_2["columns"] = list(csv_process_2.columns)
        for col in csv_process_2.columns:
            tree_2.heading(col, text=col)
            tree_2.column(col, width=100)

        # Insertar datos (hasta el penúltimo índice)
        for i, row in csv_process_2.iloc[:-2].iterrows():
            tree_2.insert("", "end", values=list(row))
    #print(csv_process_3)
    visualizar_grafico(csv_process_3,'1')

    


window = Tk()

window.geometry("1092x700")
window.configure(bg = "#005187")


canvas = Canvas(
    window,
    bg = "#005187",
    height = 700,
    width = 1092,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    3.0,
    1093.0,
    51.0,
    fill="#C4DAFA",
    outline="")

canvas.create_text(
    67.0,
    4.0,
    anchor="nw",
    text="PLANIFICADOR DE PROCESOS",
    fill="#000000",
    font=("Inter Bold", 30 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    37.0,
    22.0,
    image=image_image_1
)

canvas.create_rectangle(
    20.0,
    68.0,
    559.0,
    99.0,
    fill="#6A9CDE",
    outline="")

canvas.create_rectangle(
    20.0,
    549.0,
    1076.0,
    683.0,
    fill="#6A9CDE",
    outline="")

canvas.create_rectangle(
    20.0,
    163.0,
    577.0,
    539.0,
    fill="#6A9CDE",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (clear_data(), canvas.delete(id_penultimo), canvas.delete(id_ultimo)),
    relief="flat"
)

button_1.place(
    x=331.0,
    y=113.0,
    width=116.0,
    height=34.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_data('1','1'),
    relief="flat"
)
button_2.place(
    x=20.0,
    y=113.0,
    width=296.0,
    height=34.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=462.0,
    y=114.0,
    width=98.54730224609375,
    height=34.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_data('4','7'),
    relief="flat"
)
button_4.place(
    x=839.0,
    y=114.0,
    width=143.05262756347656,
    height=34.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:show_data('3','6'),
    relief="flat"
)
button_5.place(
    x=720.0,
    y=114.0,
    width=98.54730224609375,
    height=34.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_data('2','5'),
    relief="flat"
)
button_6.place(
    x=597.0,
    y=114.0,
    width=98.54730224609375,
    height=34.0
)

canvas.create_text(
    61.0,
    71.0,
    anchor="nw",
    text="Ingresar Información de Proceso",
    fill="#000000",
    font=("Inter Bold", 20 * -1)
)

canvas.create_rectangle(
    597.0,
    157.0,
    1076.0,
    228.0,
    fill="#D9D9D9",
    outline="")





canvas.create_rectangle(
    925.0,
    195.0,
    981.0,
    221.0,
    fill="#FFFFFF",
    outline="")




canvas.create_rectangle(
    26.0,
    570.0,
    1071.0,
    678.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    56.0,
    552.0,
    anchor="nw",
    text="Diagrama Gantt",
    fill="#000000",
    font=("Inter Bold", 12 * -1)
)

canvas.create_rectangle(
    597.0,
    242.0,
    1076.0,
    539.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    26.0,
    189.0,
    572.0,
    534.0,
    fill="#000000",
    outline="")

canvas.create_text(
    605.0,
    166.0,
    anchor="nw",
    text="Tiempo Promedio de Espera",
    fill="#000000",
    font=("Inter Bold", 15 * -1)
)

canvas.create_text(
    839.0,
    166.0,
    anchor="nw",
    text="Tiempo Promedio de Ejecución",
    fill="#000000",
    font=("Inter Bold", 15 * -1)
)

canvas.create_rectangle(
    692.0,
    195.0,
    748.0,
    221.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    597.0,
    68.0,
    994.0,
    99.0,
    fill="#6A9CDE",
    outline="")

canvas.create_text(
    55.0,
    168.0,
    anchor="nw",
    text="Lista de Procesos",
    fill="#000000",
    font=("Inter Bold", 15 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    628.0,
    83.0,
    image=image_image_2
)

canvas.create_text(
    651.0,
    72.0,
    anchor="nw",
    text="Modelos de Planificación",
    fill="#000000",
    font=("Inter Bold", 20 * -1)
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    49.0,
    85.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    42.0,
    559.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    41.0,
    178.0,
    image=image_image_5
)


# Crear el Treeview y Frame para la tabla 1
data_frame_1 = ttk.Frame(window)
data_frame_1.place(x=26, y=189, width=546, height=345)
tree_1 = ttk.Treeview(data_frame_1)
tree_1.pack(expand=True, fill="both")

# Crear la barra de desplazamiento vertical para el Treeview 1
scrollbar_1 = Scrollbar(data_frame_1, orient=VERTICAL, command=tree_1.yview)
scrollbar_1.pack(side="right", fill="y")
tree_1.configure(yscrollcommand=scrollbar_1.set)

# ... (tu código para la tabla 2)

# Crear el Treeview y Frame para la tabla 2
data_frame_2 = ttk.Frame(window)
data_frame_2.place(x=597, y=242, width=479, height=297)
tree_2 = ttk.Treeview(data_frame_2)
tree_2.pack(expand=True, fill="both")

# Crear la barra de desplazamiento vertical para el Treeview 2
scrollbar_2 = Scrollbar(data_frame_2, orient=VERTICAL, command=tree_2.yview)
scrollbar_2.pack(side="right", fill="y")
tree_2.configure(yscrollcommand=scrollbar_2.set)

window.resizable(False, False)
window.mainloop()

