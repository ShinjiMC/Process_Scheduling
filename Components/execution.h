#ifndef EXECUTION_H
#define EXECUTION_H

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
struct ExecutionRecord
{
    int pid;
    char name[256];
    int burst_time;
};
struct ExecutionOrder
{
    struct ExecutionRecord *list;
    int size;
};

void initExecutionList(struct ExecutionOrder *executionList)
{
    executionList->list = NULL;
    executionList->size = 0;
}

void freeExecutionList(struct ExecutionOrder *executionList)
{
    free(executionList->list);
    executionList->list = NULL;
    executionList->size = 0;
}

void insertExecution(struct ExecutionOrder *executionList, int pid, const char *name, int burst_time)
{
    executionList->list = (struct ExecutionRecord *)realloc(executionList->list, (executionList->size + 1) * sizeof(struct ExecutionRecord));
    if (executionList->list == NULL)
    {
        printf("Error: no se pudo asignar memoria.\n");
        exit(EXIT_FAILURE);
    }
    executionList->list[executionList->size].pid = pid;
    strncpy(executionList->list[executionList->size].name, name, 7);
    executionList->list[executionList->size].name[6] = '\0';
    executionList->list[executionList->size].burst_time = burst_time;
    executionList->size++;
}

void printExecutionList(struct ExecutionOrder *executionList)
{
    printf("Execution Order:\n");
    printf("PID\tName\tBurst Time\n");
    for (int i = 0; i < executionList->size; i++)
        printf("%d\t%s\t%d\n", executionList->list[i].pid, executionList->list[i].name, executionList->list[i].burst_time);
}
#endif // EXECUTION_H