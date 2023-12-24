#ifndef PROCESS_H
#define PROCESS_H

#include <string.h>

struct ProcessInfo
{
    char name[256];
    int pid;
    int priority;
    int burst_time;
    int arrival_time;
    int left_time;
    int waiting_time;
    int response_time;
};

struct ProcessInfo initializeProcessInfo(char *name, int pid, int priority, int burst_time, int arrival_time)
{
    struct ProcessInfo newProcess;
    strcpy(newProcess.name, name);
    newProcess.pid = pid;
    newProcess.priority = priority;
    newProcess.burst_time = burst_time;
    newProcess.arrival_time = arrival_time;
    newProcess.left_time = burst_time;
    newProcess.waiting_time = 0;
    newProcess.response_time = 0;
    return newProcess;
}

#endif // PROCESS_H