#include <stdio.h>
#include <stdlib.h>

struct Process
{ // Estructura que almacenara los procesos con sus respectivos datos
    int pid;
    int burst_time;
    int waiting_time;
    int arrival_time;
    int response_time;
};

void sort_by_arrival(struct Process *lista_procesos, int n)
{ // algoritmo que ordenara la lista de procesos segun orden de llegada
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (lista_procesos[j].arrival_time > lista_procesos[j + 1].arrival_time)
            {
                struct Process temp = lista_procesos[j];
                lista_procesos[j] = lista_procesos[j + 1];
                lista_procesos[j + 1] = temp;
            }
        }
    }
}

void FCFS(struct Process *lista_procesos, int n) // funcion FCFS
{
    int w = 0;                               // el tiempo inicial
    if (lista_procesos[0].arrival_time == 0) // si el primer tiempo es 0 se le define el tiempo de espera 0
        lista_procesos[0].waiting_time = 0;
    else // caso contario se cambia el tiempo inicial al tiempo de llegada del primer proceso
    {
        lista_procesos[0].waiting_time = lista_procesos[0].arrival_time;
        w = lista_procesos[0].arrival_time;
    }
    lista_procesos[0].response_time = lista_procesos[0].burst_time; // se define el tiempo de respuesta segun el de rafaga

    for (int i = 1; i < n; i++) // bucle para otorgar los datos de espera y respuesta de los demas procesos restantes
    {
        int waiting = w;
        for (int j = 0; j < i; j++) // bucle hasta llegar al tiempo de inicio del proceso actual i
        {
            waiting += lista_procesos[j].burst_time;
        }
        lista_procesos[i].waiting_time = waiting - lista_procesos[i].arrival_time; // guardando dato de espera restando el tiempo de llegada
        if (lista_procesos[i].waiting_time < 0)                                    // si el tiempo de espera es menor a 0 se define como 0
        {
            lista_procesos[i].waiting_time = 0;
        }
        lista_procesos[i].response_time = lista_procesos[i].burst_time + lista_procesos[i].waiting_time; // se define el tiempo de respuesta igual al tiempo de rafaga mas el de espera
    }
}

int main()
{
    int n;
    printf("Enter the number of processes: "); // ingresamos la cantidad de procesos a ingresar
    scanf("%d", &n);
    struct Process *lista_procesos = (struct Process *)malloc(n * sizeof(struct Process)); // creamos una lista segun n

    for (int i = 0; i < n; i++) // bucle para ingresar los datos de cada proceso en la lista
    {
        struct Process p;
        printf("Enter process ID: ");
        scanf("%d", &p.pid);
        printf("Enter burst time for process %d: ", p.pid);
        scanf("%d", &p.burst_time);
        printf("Enter arrival time for process %d: ", p.pid);
        scanf("%d", &p.arrival_time);
        p.waiting_time = 0;
        p.response_time = 0;
        lista_procesos[i] = p;
    }

    sort_by_arrival(lista_procesos, n); // ordenamos la lista segun el orden de llegada
    FCFS(lista_procesos, n);            // aplicamos fcsfs

    printf("\nProcess Details:\n");
    printf("PID\tBurst Time\tArrival Time\tWaiting Time\tResponse Time\n");
    int total_waiting_time = 0, total_response_time = 0;
    for (int i = 0; i < n; i++) // Mostramos los datos de cada proceso y aprovechamos para sumar todos los tiempo de espera y respuesta
    {
        printf("%d\t%d\t\t%d\t\t%d\t\t%d\n", lista_procesos[i].pid, lista_procesos[i].burst_time,
               lista_procesos[i].arrival_time, lista_procesos[i].waiting_time, lista_procesos[i].response_time);
        total_waiting_time += lista_procesos[i].waiting_time;
        total_response_time += lista_procesos[i].response_time;
    }
    // calculamos el tiempo promedio de espera y respuesta
    double avg_waiting_time = (double)total_waiting_time / n;
    double avg_response_time = (double)total_response_time / n;
    // mostramos los tiempos promedios
    printf("\nAverage Waiting Time: %.2lf\n", avg_waiting_time);
    printf("Average Response Time: %.2lf\n", avg_response_time);
    free(lista_procesos); // liberamos memoria de la lista de procesos
    return 0;
}