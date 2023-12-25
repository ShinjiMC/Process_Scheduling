#ifndef QUEUE_H
#define QUEUE_H

#include <stdio.h>
#include <stdbool.h>
#include "process.h"

#define MAX_QUEUE_SIZE 5000

struct Queue
{
    struct ProcessInfo data[MAX_QUEUE_SIZE];
    int front, rear;
};

void initializeQueue(struct Queue *q)
{
    q->front = -1;
    q->rear = -1;
}

bool isQueueEmpty(struct Queue *q)
{
    return (q->front == -1);
}

bool isQueueFull(struct Queue *q)
{
    return ((q->rear + 1) % MAX_QUEUE_SIZE == q->front);
}

void enqueue(struct Queue *q, struct ProcessInfo process)
{
    if (isQueueFull(q))
    {
        printf("Queue is full, cannot enqueue more elements.\n");
        return;
    }

    if (isQueueEmpty(q))
    {
        q->front = q->rear = 0;
    }
    else
    {
        q->rear = (q->rear + 1) % MAX_QUEUE_SIZE;
    }

    q->data[q->rear] = process;
}

struct ProcessInfo dequeue(struct Queue *q)
{
    if (isQueueEmpty(q))
    {
        printf("Queue is empty, cannot dequeue.\n");
        struct ProcessInfo empty;
        return empty;
    }

    struct ProcessInfo process = q->data[q->front];

    if (q->front == q->rear)
    {
        q->front = q->rear = -1;
    }
    else
    {
        q->front = (q->front + 1) % MAX_QUEUE_SIZE;
    }

    return process;
}

void printQueue(struct Queue *q)
{
    if (isQueueEmpty(q))
    {
        printf("Queue is empty.\n");
        return;
    }

    int i = q->front;
    while (i != q->rear)
    {
        printf("%d ", q->data[i].pid);
        i = (i + 1) % MAX_QUEUE_SIZE;
    }
    printf("%d\n", q->data[i].pid);
}

bool search(struct Queue *q, int pid)
{
    if (isQueueEmpty(q))
        return false;
    int i = q->front;
    while (i != q->rear)
    {
        if (q->data[i].pid == pid)
            return true;
        i = (i + 1) % MAX_QUEUE_SIZE;
    }
    if (q->data[i].pid == pid)
        return true;
    return false;
}

#endif // QUEUE_H
