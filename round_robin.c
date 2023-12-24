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
    // Se solicita la entrada del tiempo quantum
    printf("\nIngrese el tiempo quantum [1-100]: ");
    int quantum = 0;
    scanf("%d", &quantum);
    while (quantum < 1 || quantum > 100)
    {
        printf("\nQuantum inválido. Ingrese un valor entre 1 y 100: ");
        scanf("%d", &quantum);
    }
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
    printf("\nQuantum %d unidades\n", quantum);
    // Round Robin
    while (procesos_restantes > 0)
    {
        for (int i = 0; i < n; ++i)
        { // bucle de los elementos del array
            if (procesos[i].tiempo_restante > 0)
            { // si el restante es mayor a 0 del proceso actual
                if (procesos[i].tiempo_restante > quantum)
                {                                           // si restante es mayor a quantum
                    tiempo_total += quantum;                // se suma al timpo el quantum
                    procesos[i].tiempo_restante -= quantum; // y al proceso actual se le resta quantum
                }
                else
                {                                                                                                        // si es menor o igual a quantum
                    tiempo_total += procesos[i].tiempo_restante;                                                         // al tiempo total se le suma el tiempo restante del proceso actual
                    procesos[i].tiempo_espera = tiempo_total - procesos[i].tiempo_servicio - procesos[i].tiempo_llegada; // calculo del tiempo de espera segun el total, servicio y la llegada
                    procesos[i].tiempo_restante = 0;                                                                     // definimos a restante como 0
                    procesos[i].tiempo_retorno = tiempo_total - procesos[i].tiempo_llegada;                              // el tiempo de retorno se define como el tiempo total menos el de la llegada
                    procesos_restantes--;
                }
            }
        }
    } // mostramos los datos de los procesos despues del round robin
    printf("Datos de cada proceso:\n");
    for (int i = 0; i < n; ++i)
    {
        printf("%s Tiempo de espera: %d Tiempo de retorno: %d\n", procesos[i].nombre, procesos[i].tiempo_espera, procesos[i].tiempo_retorno);
    }
    return 0;
}