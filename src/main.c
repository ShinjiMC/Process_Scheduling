#include "../Components/reader.h"
#include "../Components/fcfs.h"
#include "../Components/sjf.h"
#include "../Components/round_robin.h"
#include "../Components/writer.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    createResultsFolder();
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
    int count = sizeof(processes) / sizeof(processes[0]); // hasta aqui
*/
    int choice = 0;
    struct ExecutionOrder resultOrder;
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
            showProcesses(processes, count, "./static/Process.csv");
            break;
        case 2:
            sort_by_arrival(processes, count);
            resultOrder = FCFS(processes, count);
            saveExecutionOrderToFile("./static/OrderView.csv", &resultOrder);
            showResults(processes, count, "./static/algorithm.csv");
            break;
        case 3:
            resultOrder = SJF(processes, count);
            saveExecutionOrderToFile("./static/OrderView.csv", &resultOrder);
            showResults(processes, count, "./static/algorithm.csv");
            break;
        case 4:
            int quantum = 12;
            resultOrder = roundRobin(processes, count, quantum);
            saveExecutionOrderToFile("./static/OrderView.csv", &resultOrder);
            showResults(processes, count, "./static/algorithm.csv");
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
