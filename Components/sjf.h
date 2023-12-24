#ifndef SJF_H
#define SJF_H

#include "process.h"
#include <limits.h> // Para usar INT_MAX
void SJF(struct ProcessInfo *lista_procesos, int n)
{
    int tiempo_total = 0;
    int procesos_restantes = n;

    while (procesos_restantes > 0)
    {
        int shortest_job = -1;
        int menor_tiempo = INT_MAX; // Se establece el menor tiempo como el máximo valor posible

        for (int i = 0; i < n; ++i)
        {
            if (lista_procesos[i].arrival_time <= tiempo_total && lista_procesos[i].left_time > 0)
            {
                if (lista_procesos[i].left_time < menor_tiempo)
                {
                    menor_tiempo = lista_procesos[i].left_time;
                    shortest_job = i;
                }
            }
        }

        if (shortest_job == -1)
        {
            tiempo_total++;
            continue;
        }

        lista_procesos[shortest_job].left_time = 0;
        lista_procesos[shortest_job].waiting_time = tiempo_total - lista_procesos[shortest_job].arrival_time;
        lista_procesos[shortest_job].response_time = lista_procesos[shortest_job].waiting_time + lista_procesos[shortest_job].burst_time;
        tiempo_total += lista_procesos[shortest_job].burst_time;
        procesos_restantes--;

        // Actualizar el tiempo restante de los otros procesos
        for (int i = 0; i < n; ++i)
        {
            if (i != shortest_job && lista_procesos[i].arrival_time <= tiempo_total && lista_procesos[i].left_time > 0)
            {
                lista_procesos[i].left_time -= lista_procesos[shortest_job].burst_time;
            }
        }
    }
}

#endif // SJF_H
