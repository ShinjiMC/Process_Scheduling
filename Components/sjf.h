#ifndef SJF_H
#define SJF_H

#include "process.h"
#include <limits.h>

struct ExecutionOrder SJF(struct ProcessInfo *lista_procesos, int n)
{
    struct ExecutionOrder executionOrder;
    initExecutionList(&executionOrder);
    int tiempo_total = 0;
    int procesos_restantes = n;
    for (int i = 0; i < n; ++i)
    {
        lista_procesos[i].left_time = lista_procesos[i].burst_time;
        if (lista_procesos[i].left_time == 0)
            insertExecution(&executionOrder, lista_procesos[i].pid, lista_procesos[i].name, lista_procesos[i].burst_time);
    }

    while (procesos_restantes > 0)
    {
        int shortest_job = -1;
        int menor_tiempo = INT_MAX;
        int todos_procesos_terminados = 1;
        for (int i = 0; i < n; ++i)
        {
            if (lista_procesos[i].arrival_time <= tiempo_total && lista_procesos[i].left_time > 0)
            {
                if (lista_procesos[i].burst_time < menor_tiempo)
                {
                    menor_tiempo = lista_procesos[i].burst_time;
                    shortest_job = i;
                }
                todos_procesos_terminados = 0;
            }
        }

        if (todos_procesos_terminados)
            break;
        if (shortest_job == -1)
            tiempo_total++;
        else
        {
            lista_procesos[shortest_job].left_time = 0;
            lista_procesos[shortest_job].waiting_time = tiempo_total - lista_procesos[shortest_job].arrival_time;
            lista_procesos[shortest_job].response_time = lista_procesos[shortest_job].waiting_time + lista_procesos[shortest_job].burst_time;
            tiempo_total += lista_procesos[shortest_job].burst_time;
            insertExecution(&executionOrder, lista_procesos[shortest_job].pid, lista_procesos[shortest_job].name, lista_procesos[shortest_job].burst_time);
            procesos_restantes--;
        }
    }
    return executionOrder;
}

#endif // SJF_H
