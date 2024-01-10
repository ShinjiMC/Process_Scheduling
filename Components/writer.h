#ifndef WRITER_H
#define WRITER_H

#include "process.h"
#include "execution.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#define MAX_NAME_LENGTH 6

void createResultsFolder()
{
#ifdef _WIN32
    mkdir("static");
#else
    mkdir("static", 0755);
#endif
}

void showProcesses(struct ProcessInfo *processes, int count, const char *route)
{
    FILE *file = fopen(route, "w");
    if (file == NULL)
    {
        printf("Error al abrir el archivo.");
        return;
    }
    fprintf(file, "PID,Name,Priority,Burst Time,Arrival Time,Left Time\n");
    for (int i = 0; i < count; i++)
    {
        char adjustedName[MAX_NAME_LENGTH + 1];
        strncpy(adjustedName, processes[i].name, MAX_NAME_LENGTH);
        adjustedName[MAX_NAME_LENGTH] = '\0';
        fprintf(file, "%d,%s,%d,%d,%d,%d\n", processes[i].pid, adjustedName,
                processes[i].priority, processes[i].burst_time, processes[i].arrival_time, processes[i].left_time);
    }
    fclose(file);
}

void showResults(struct ProcessInfo *processes, int count, const char *route)
{
    FILE *file = fopen(route, "w");
    if (file == NULL)
    {
        printf("Error al abrir el archivo.");
        return;
    }
    fprintf(file, "PID,Name,Priority,Arrival Time,Waiting Time,Response Time\n");
    double total_waiting_time = 0;
    double total_response_time = 0;
    for (int i = 0; i < count; i++)
    {
        char adjustedName[MAX_NAME_LENGTH + 1];
        strncpy(adjustedName, processes[i].name, MAX_NAME_LENGTH);
        adjustedName[MAX_NAME_LENGTH] = '\0';
        fprintf(file, "%d,%s,%d,%d,%d,%d\n", processes[i].pid, adjustedName,
                processes[i].priority, processes[i].arrival_time,
                processes[i].waiting_time, processes[i].response_time);
        total_waiting_time += processes[i].waiting_time;
        total_response_time += processes[i].response_time;
    }
    double avg_waiting_time = total_waiting_time / count;
    double avg_response_time = total_response_time / count;
    fprintf(file, "\nAverage Waiting Time: %.2lf\n", avg_waiting_time);
    fprintf(file, "Average Response Time: %.2lf\n", avg_response_time);
    fclose(file);
}
void saveExecutionOrderToFile(const char *route, const struct ExecutionOrder *executionOrder)
{
    FILE *file = fopen(route, "w");
    if (file == NULL)
    {
        printf("Error al abrir el archivo para escritura.\n");
        return;
    }
    fprintf(file, "PID,Name,Burst Time\n");
    for (int i = 0; i < executionOrder->size; ++i)
    {
        fprintf(file, "%d,%s,%d\n",
                executionOrder->list[i].pid,
                executionOrder->list[i].name,
                executionOrder->list[i].burst_time);
    }
    fclose(file);
}
#endif // WRITER_H