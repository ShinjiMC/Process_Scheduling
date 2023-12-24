#ifndef FCFS_H
#define FCFS_H

#include "process.h"

void sort_by_arrival(struct ProcessInfo *lista_procesos, int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (lista_procesos[j].arrival_time > lista_procesos[j + 1].arrival_time)
            {
                struct ProcessInfo temp = lista_procesos[j];
                lista_procesos[j] = lista_procesos[j + 1];
                lista_procesos[j + 1] = temp;
            }
        }
    }
}

void FCFS(struct ProcessInfo *lista_procesos, int n)
{
    int w = 0;
    if (lista_procesos[0].arrival_time == 0)
        lista_procesos[0].waiting_time = 0;
    else
    {
        lista_procesos[0].waiting_time = lista_procesos[0].arrival_time;
        w = lista_procesos[0].arrival_time;
    }
    lista_procesos[0].response_time = lista_procesos[0].burst_time;
    for (int i = 1; i < n; i++)
    {
        int waiting = w;
        for (int j = 0; j < i; j++)
        {
            waiting += lista_procesos[j].burst_time;
        }
        lista_procesos[i].waiting_time = waiting - lista_procesos[i].arrival_time;
        if (lista_procesos[i].waiting_time < 0)
        {
            lista_procesos[i].waiting_time = 0;
        }
        lista_procesos[i].response_time = lista_procesos[i].burst_time + lista_procesos[i].waiting_time;
    }
}

#endif // FCFS_H