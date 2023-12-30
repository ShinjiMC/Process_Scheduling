#include "../Components/reader.h"
#include "../Components/fcfs.h"
#include "../Components/sjf.h"
#include "../Components/round_robin.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>



#define MAX_NAME_LENGTH 6

void showProcesses(struct ProcessInfo *processes, int count, const char *route)
{
    FILE *file = fopen(route, "w"); // Abre el archivo en modo escritura

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

    fclose(file); // Cierra el archivo después de escribir
}

void showResults(struct ProcessInfo *processes, int count, const char *route)
{
    FILE *file = fopen(route, "w"); // Abre el archivo en modo escritura

    if (file == NULL)
    {
        printf("Error al abrir el archivo.");
        return;
    }

    fprintf(file, "PID,Name,Priority,Burst Time,Arrival Time,Waiting Time,Response Time\n");

    double total_waiting_time = 0;
    double total_response_time = 0;

    for (int i = 0; i < count; i++)
    {
        char adjustedName[MAX_NAME_LENGTH + 1];
        strncpy(adjustedName, processes[i].name, MAX_NAME_LENGTH);
        adjustedName[MAX_NAME_LENGTH] = '\0';

        fprintf(file, "%d,%s,%d,%d,%d,%d,%d\n", processes[i].pid, adjustedName,
               processes[i].priority, processes[i].burst_time, processes[i].arrival_time,
               processes[i].waiting_time, processes[i].response_time);

        total_waiting_time += processes[i].waiting_time;
        total_response_time += processes[i].response_time;
    }

    double avg_waiting_time = total_waiting_time / count;
    double avg_response_time = total_response_time / count;

    fprintf(file, "\nAverage Waiting Time: %.2lf\n", avg_waiting_time);
    fprintf(file, "Average Response Time: %.2lf\n", avg_response_time);

    fclose(file); // Cierra el archivo después de escribir
}

int main()
{
    struct ProcessInfo processes[MAX_PROC_ENTRIES];
    int count;
    count = getProcesses(processes);
    //    Test data para comprobar schedule
    /*struct ProcessInfo processes[] = {
        {"P1", 1, 0, 3, 0, 3, 0, 0},
        {"P2", 2, 0, 6, 2, 6, 0, 0},
        {"P3", 3, 0, 4, 4, 4, 0, 0},
        {"P4", 4, 0, 2, 8, 2, 0, 0},
    };
    int count = sizeof(processes) / sizeof(processes[0]);*/
    int choice = 0;
    while (choice != 5)
    {
        printf("\nMenu:\n");
        printf("1. Show Processes\n");
        printf("2. Run FCFS\n");
        printf("3. Run SJF\n");
        printf("4. Run Round Robin\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice)
        {
        case 1:
            showProcesses(processes, count,"showProcessNormal.csv");
            break;
        case 2:
            sort_by_arrival(processes, count);
            FCFS(processes, count);
            showResults(processes, count,"showFCSNormal.csv");
            break;
        case 3:
            SJF(processes, count);
            showResults(processes, count,"showSJFNormal.csv");
            break;
        case 4:
            int quantum = 12;
            roundRobin(processes, count, quantum);
            showResults(processes, count,"showRoundRobinNormal.csv");
            break;
        case 5:
            printf("Exiting...\n");
            break;
        default:
            printf("Invalid choice. Please enter a valid option.\n");
            break;
        }
    }

    return 0;
}
