#include <stdio.h>
#include <stdlib.h>

struct Proceso
{
    char nombre[100];
    int tiempo_llegada;
    int tiempo_servicio;
    int tiempo_restante;
    int tiempo_espera;
    int tiempo_retorno;
};

int main()
{
    // Se solicita la entrada de cantidad de procesos a ejecutar
    printf("\nIngrese la cantidad de procesos (máx. 10): ");
    int n = 0;
    scanf("%d", &n);
    if (n <= 0 || n > 10)
    {
        printf("\nNúmero de procesos inválido. Ingrese un número entre 1 y 10.\n");
        return 1;
    }
    struct Proceso procesos[10]; // Array de Proceso para almacenar como una Cola
    // Se solicita la entrada de los datos de cada Proceso
    printf("\nIngrese tiempo de llegada y tiempo de servicio para cada proceso (e.g., P1 0 8): \n");
    for (int i = 0; i < n; ++i)
    {
        printf("P%d: ", i + 1);
        scanf("%d %d", &procesos[i].tiempo_llegada, &procesos[i].tiempo_servicio);
        sprintf(procesos[i].nombre, "P%d", i + 1);                 // Se asigna un nombre a cada proceso (P1, P2, etc.)
        procesos[i].tiempo_restante = procesos[i].tiempo_servicio; // El tiempo restante al principio es igual al tiempo de servicio
        procesos[i].tiempo_espera = 0;                             // Se inicializa con 0 igual al retorno
        procesos[i].tiempo_retorno = 0;
    }
    int tiempo_total = 0;
    int procesos_restantes = n;
    // Shortest Job First (SJF)
    while (procesos_restantes > 0)
    {
        int shortest_job = -1;     // Variable para almacenar el índice del proceso más corto
        int menor_tiempo = 999999; // Inicialización de la variable con un valor grande para hallar el menor
        for (int i = 0; i < n; ++i)
        {
            if (procesos[i].tiempo_llegada <= tiempo_total && procesos[i].tiempo_restante > 0)
            {
                if (procesos[i].tiempo_servicio < menor_tiempo)
                {                                               // si el proceso es menor al menor tiempo anterior
                    menor_tiempo = procesos[i].tiempo_servicio; // se actualiza el menor
                    shortest_job = i;                           // se define el que se ejecutara con el indice del proceso actual
                }
            }
        }
        if (shortest_job == -1)
        {                   // Si no se encuentra un proceso corto para ejecutar
            tiempo_total++; // Se incrementa el tiempo total y se continúa con el siguiente ciclo
            continue;
        }
        // Proceso actual terminado
        procesos[shortest_job].tiempo_restante = 0; // Establece el tiempo restante del proceso actual como 0
        procesos[shortest_job].tiempo_espera = tiempo_total - procesos[shortest_job].tiempo_llegada;
        procesos[shortest_job].tiempo_retorno = procesos[shortest_job].tiempo_espera + procesos[shortest_job].tiempo_servicio;
        tiempo_total += procesos[shortest_job].tiempo_servicio;
        // Calulos de tiempo segun la llegada y tiempo total
        procesos_restantes--; // se catualizan cuantos procesos faltan por ejecutar
    }                         // mostramos los datos de los procesos despues del SJF
    printf("\nDatos de cada proceso:\n");
    for (int i = 0; i < n; ++i)
    {
        printf("%s Tiempo de espera: %d Tiempo de retorno: %d\n", procesos[i].nombre, procesos[i].tiempo_espera, procesos[i].tiempo_retorno);
    }
    return 0;
}