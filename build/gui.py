from ctypes import cdll
from pathlib import Path
import matplotlib.pyplot as plt
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import ttk
import pandas as pd
from tkinter import  Label
import tkinter as tk
import csv

mi_canvas = None
id_penultimo = None
id_ultimo = None

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../build/assets/frame0")

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

def visualizar_grafico(archivo_csv, id_algoritmo):
    global mi_canvas 
    # Verificar si el id_algoritmo es 5
    if id_algoritmo == '5':
        # Borrar el contenido del canvas si el id_algoritmo es 5
        mi_canvas.delete("all")
        mi_canvas.destroy()
        return

    # Cargar procesos desde el archivo CSV
    lista_procesos = cargar_procesos_desde_csv(archivo_csv)

    # Crear un nuevo canvas si no es el id_algoritmo 5
    mi_canvas = tk.Canvas(window, width=1045, height=108, bg="white")
    mi_canvas.place(x=26, y=570)

    # Agregar barra de desplazamiento horizontal al Canvas
    scrollbar_horizontal = ttk.Scrollbar(window, orient="horizontal", command=mi_canvas.xview)
    scrollbar_horizontal.place(x=26, y=678, width=1045)

    # Configurar el Canvas para trabajar con la barra de desplazamiento
    mi_canvas.configure(xscrollcommand=scrollbar_horizontal.set)

    # Llamar a la función para iniciar la visualización dentro de tu widget
    iniciar_grafico_paso_a_paso(id_algoritmo, lista_procesos, mi_canvas)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_csv_data(opcion):
    file_paths = {
        '1': '../Resultados/showProcessNormal.csv',
        '2': '../Resultados/showFCSNormal.csv',
        '3': '../Resultados/showSJFNormal.csv',
        '4': '../Resultados/showRoundRobinNormal.csv',
    }

    if opcion in file_paths:
        try:
            # Intenta leer el archivo CSV usando el delimitador de coma
            data = pd.read_csv(file_paths[opcion], sep=',', engine='python', header=0)
            id_penultimo, id_ultimo = mostrar_numeros_desde_archivo(file_paths[opcion], canvas)
            return data
        except FileNotFoundError:
            print("Error: Archivo no encontrado.")
            return None
    else:
        print("Opción no válida. Por favor, selecciona una opción válida.")
        return None

def clear_data():
    for col in tree.get_children():
        tree.delete(col)

class Proceso:
    def __init__(self, pid, nombre, tiempo_ejecucion):
        self.pid = pid
        self.nombre = nombre
        self.tiempo_ejecucion = tiempo_ejecucion
        self.tiempo_restante = tiempo_ejecucion  # Nueva propiedad

def fcfs(procesos):
    tiempo_actual = 0
    lista_procesos = []

    for proceso in procesos:
        if tiempo_actual < proceso.tiempo_ejecucion:
            tiempo_actual = proceso.tiempo_ejecucion

        lista_procesos.append(Proceso(proceso.pid, proceso.nombre, proceso.tiempo_ejecucion))
        tiempo_actual += proceso.tiempo_ejecucion

    return lista_procesos

def sjf(procesos):
    tiempo_actual = 0
    lista_procesos = []

    # Ordenar procesos por tiempo de ejecución restante
    procesos.sort(key=lambda x: x.tiempo_restante)

    for proceso in procesos:
        if tiempo_actual < proceso.tiempo_restante:
            tiempo_actual = proceso.tiempo_restante

        lista_procesos.append(Proceso(proceso.pid, proceso.nombre, proceso.tiempo_restante))
        tiempo_actual += proceso.tiempo_restante

    return lista_procesos

def round_robin(procesos, quantum):
    tiempo_actual = 0
    lista_procesos = []

    while any(proceso.tiempo_restante > 0 for proceso in procesos):
        for proceso in procesos:
            if proceso.tiempo_restante > 0:
                tiempo_ejecucion = min(quantum, proceso.tiempo_restante)
                lista_procesos.append(Proceso(proceso.pid, proceso.nombre, tiempo_ejecucion))
                proceso.tiempo_restante -= tiempo_ejecucion
                tiempo_actual += tiempo_ejecucion

    return lista_procesos

def graficar_linea_tiempo_paso_a_paso(linea_tiempo, canvas, index, posicion_actual=0):
    if index < len(linea_tiempo):
        proceso = linea_tiempo[index]
        x_inicio = posicion_actual
        ancho_rectangulo = 50  # Puedes ajustar este valor según tus necesidades
        x_fin = x_inicio + ancho_rectangulo
        y_inicio = 20
        y_fin = 80
        color = "lightblue"

        canvas.create_rectangle(x_inicio, y_inicio, x_fin, y_fin, fill=color)
        canvas.create_text((x_inicio + x_fin) / 2, (y_inicio + y_fin) / 2, text=f"PID: {proceso.pid}", font=("Arial", 8), fill="black")
        canvas.create_text(x_inicio, y_fin + 5, anchor=tk.W, text=f"{proceso.tiempo_ejecucion}", font=("Arial", 8), fill="black")

        canvas.after(1000, graficar_linea_tiempo_paso_a_paso, linea_tiempo, canvas, index + 1, x_fin)
        canvas.xview_moveto(1)  # Mover la barra de desplazamiento al final

def iniciar_grafico_paso_a_paso(algoritmo_id, lista_procesos, canvas, quantum=12):
    canvas.delete("all")  # Limpia el contenido existente en el Canvas

    if algoritmo_id == '1':
        linea_tiempo = fcfs(lista_procesos)
    elif algoritmo_id == '2':
        linea_tiempo = sjf(lista_procesos)
    elif algoritmo_id == '3':
        linea_tiempo = round_robin(lista_procesos, quantum)
    else:
        raise ValueError("ID de algoritmo no válido")

    index = 0
    graficar_linea_tiempo_paso_a_paso(linea_tiempo, canvas, index)

def cargar_procesos_desde_csv(archivo):
    procesos = []

    with open(archivo, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Saltar la primera fila (encabezado)
        
        for row in reader:
            pid = int(row[0])
            nombre = row[1]
            tiempo_ejecucion = int(row[3])
            procesos.append(Proceso(pid, nombre, tiempo_ejecucion))

    return procesos


def mostrar_numeros_desde_archivo(file_path, canvas):
    with open(file_path, 'r') as file:
        lineas = file.readlines()

    try:
        penultimo_numero = float(lineas[-2].split()[-1])
        ultimo_numero = float(lineas[-1].split()[-1])
    except (ValueError, IndexError) as e:
        print(f"Error al procesar el archivo: {e}")
        return None, None

    # Crear textos y devolver los ID
    id_penultimo = canvas.create_text(
        692.0,
        195.0,
        anchor="nw",
        text=f"{penultimo_numero}",
        fill="black",
        font=("Inter Bold", 14 * -1)
    )
    id_ultimo = canvas.create_text(
        925.0,
        195.0,
        anchor="nw",
        text=f"{ultimo_numero}",
        fill="black",
        font=("Inter Bold", 14 * -1)
    )

    return id_penultimo, id_ultimo
def show_data(file_path,id_algoritmo):
    archivo_csv = '../Resultados/showProcessNormal.csv'  # Reemplaza con la ruta real de tu archivo CSV
    #lista_procesos = cargar_procesos_desde_csv(archivo_csv)
    visualizar_grafico(archivo_csv,id_algoritmo)

    csv_data = load_csv_data(file_path)
    if csv_data is not None:
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
    command=lambda:(show_data('1','5'),clear_data(),canvas.delete(id_penultimo)),
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
    command=lambda: show_data('4','3'),
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
    command=lambda:show_data('3','2'),
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
    command=lambda: show_data('2','1'),
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

data_frame = ttk.Frame(window)
data_frame.place(x=26, y=189, width=546, height=345)

tree = ttk.Treeview(data_frame)
tree.pack(expand=True, fill="both")


window.resizable(False, False)
window.mainloop()
