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
    int choice = 0;
    struct ExecutionOrder resultOrder;
    showProcesses(processes, count, "./static/Process.csv");
    sort_by_arrival(processes, count);
    resultOrder = FCFS(processes, count);
    saveExecutionOrderToFile("./static/OrderViewFCFS.csv", &resultOrder);
    showResults(processes, count, "./static/algorithmFCFS.csv");
    resultOrder = SJF(processes, count);
    saveExecutionOrderToFile("./static/OrderViewSJF.csv", &resultOrder);
    showResults(processes, count, "./static/algorithmSJF.csv");
    int quantum = 12;
    resultOrder = roundRobin(processes, count, quantum);
    saveExecutionOrderToFile("./static/OrderViewRR.csv", &resultOrder);
    showResults(processes, count, "./static/algorithmRR.csv");
    /*while (choice != 5)
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
    }*/

    return 0;
}
