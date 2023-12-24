#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <ctype.h>

#define MAX_PROC_ENTRIES 2048
#define MAX_PROC_PATH_LENGTH 128

struct ProcessInfo
{
    char name[256];
    int pid;
    int priority;
    int burst_time;
    int arrival_time;
};

void getProcessInfo(struct ProcessInfo *processes, int *count)
{
    DIR *dir;
    struct dirent *entry;
    FILE *fp;
    char path[MAX_PROC_PATH_LENGTH];
    *count = 0;
    dir = opendir("/proc");
    if (dir == NULL)
    {
        perror("opendir");
        exit(EXIT_FAILURE);
    }
    while ((entry = readdir(dir)) != NULL && *count < MAX_PROC_ENTRIES)
    {
        if (isdigit(*entry->d_name))
        {
            int pid = atoi(entry->d_name);
            sprintf(path, "/proc/%d/stat", pid);
            fp = fopen(path, "r");
            if (fp != NULL)
            {
                struct ProcessInfo info;
                fscanf(fp, "%d %s %*c %*d %*d %*d %*d %*d %*u %*lu %*lu %*lu %*lu %*lu %*ld %*ld %*ld %d",
                       &info.pid, info.name, &info.priority);
                fclose(fp);
                sprintf(path, "/proc/%d/sched", pid);
                fp = fopen(path, "r");
                if (fp != NULL)
                {
                    char line[256];
                    while (fgets(line, sizeof(line), fp))
                    {
                        if (strstr(line, "se.sum_exec_runtime"))
                            sscanf(line, "se.sum_exec_runtime %*s %d", &info.burst_time);
                        else if (strstr(line, "se.statistics.wait_start"))
                            sscanf(line, "se.statistics.wait_start %*s %d", &info.arrival_time);
                    }
                    fclose(fp);
                    processes[*count] = info;
                    (*count)++;
                }
            }
        }
    }
    closedir(dir);
}

int main()
{
    struct ProcessInfo processes[MAX_PROC_ENTRIES];
    int count, i;
    getProcessInfo(processes, &count);
    printf("PID\tName\tPriority\tBurst Time\tArrival Time\n");
    for (i = 0; i < count; i++)
    {
        printf("%d\t%s\t%d\t\t%d\t\t%d\n", processes[i].pid, processes[i].name,
               processes[i].priority, processes[i].burst_time, processes[i].arrival_time);
    }

    return 0;
}
