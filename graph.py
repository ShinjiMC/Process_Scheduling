import matplotlib.pyplot as plt

def draw_gantt_chart(processes):
    fig, gnt = plt.subplots()

    gnt.set_title('Gantt Chart')
    gnt.set_xlabel('Tiempo')
    gnt.set_ylabel('Procesos')

    yticks = []
    labels = []

    for i, proc in enumerate(processes):
        gnt.broken_barh([(proc['arrival_time'], proc['burst_time'])], (10 * i, 5), facecolors=('red'))
        yticks.append(10 * i + 5)
        labels.append(f'P{proc["pid"]}')

    gnt.set_yticks(yticks)
    gnt.set_yticklabels(labels)

    plt.savefig('gantt_chart.png')  # Guardar la gráfica como imagen
    # plt.show()  # Esta línea mostraría la gráfica en pantalla, coméntala si no necesitas visualización interactiva

# Ejemplo de datos de procesos
processes = [
    {'pid': 1, 'burst_time': 3, 'arrival_time': 0},
    {'pid': 2, 'burst_time': 6, 'arrival_time': 2},
    {'pid': 3, 'burst_time': 4, 'arrival_time': 4},
    {'pid': 4, 'burst_time': 2, 'arrival_time': 8}
    # Agrega los procesos que desees visualizar en el gráfico
]

draw_gantt_chart(processes)
