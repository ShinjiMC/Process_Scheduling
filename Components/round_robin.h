#ifndef ROUND_ROBIN_H
#define ROUND_ROBIN_H
#include <stdio.h>
#include <stdlib.h>
#include "process.h"
#include "queue.h"

void roundRobin(struct ProcessInfo *processes, int count, int quantum)
{
    int tiempo_total = 0;
    int procesos_restantes = count;
    for (int i = 0; i < count; ++i)
        processes[i].left_time = processes[i].burst_time;
    struct Queue processQueue;
    initializeQueue(&processQueue);
    while (procesos_restantes > 0)
    {
        for (int i = 0; i < count; ++i)
        {
            if (processes[i].left_time > 0 && processes[i].arrival_time < tiempo_total && search(&processQueue, processes[i].pid) == false)
            {
                enqueue(&processQueue, processes[i]);
            }
        }

        if (!isQueueEmpty(&processQueue))
        {
            struct ProcessInfo currentProcess = dequeue(&processQueue);
            // printf("Processing process %d\n", currentProcess.pid);
            if (currentProcess.left_time > quantum)
            {
                tiempo_total += quantum;
                currentProcess.left_time -= quantum;
                for (int i = 0; i < count; ++i)
                {
                    if (processes[i].arrival_time < tiempo_total &&
                        processes[i].left_time > 0 &&
                        processes[i].pid != currentProcess.pid &&
                        search(&processQueue, processes[i].pid) == false)
                    {
                        enqueue(&processQueue, processes[i]);
                    }
                }
                enqueue(&processQueue, currentProcess);
            }
            else
            {
                tiempo_total += currentProcess.left_time;
                currentProcess.left_time = 0;
                procesos_restantes--;
                currentProcess.response_time = tiempo_total - currentProcess.arrival_time - 1;
                currentProcess.waiting_time = currentProcess.response_time - currentProcess.burst_time;
                for (int i = 0; i < count; ++i)
                {
                    if (processes[i].pid == currentProcess.pid)
                    {
                        processes[i] = currentProcess;
                        break;
                    }
                }
            }
        }
        else
        {
            tiempo_total++;
        }
    }
}

#endif // ROUND_ROBIN_H
