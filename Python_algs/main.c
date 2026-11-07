#include <stdio.h>
#include <stdlib.h>

/* Константы */
#define MIN_ID 1
#define MIN_COURSE 1
#define MAX_COURSE 6
#define MIN_SCORE 0.0
#define MAX_SCORE 5.0
#define MIN_N 0
#define MAX_N 1000
#define MIN_K 1
#define INPUT_FILENAME "input.txt"
#define OUTPUT_FILENAME "output.txt"

typedef struct
{
    int id;
    int course;
    double score;
} Student;

typedef struct Node
{
    Student data;
    struct Node *next;
} Node;

/* Прототипы функций */
Node *input_list(FILE *in, int *k_out, int *error);
void print_list(FILE *out, const Node *head);
void free_list(Node *head);
int validate_student(const Student *s);
Node *reverse_blocks(Node *head, int k);

int main(void)
{
    FILE *in = fopen(INPUT_FILENAME, "r");
    if (in == NULL)
    {
        perror(INPUT_FILENAME);
        return 1;
    }

    int k = 0;
    int error = 0;
    Node *head = input_list(in, &k, &error);
    
    if (error != 0)
    {
        fclose(in);
        return 1;
    }

    if (fclose(in) != 0)
    {
        free_list(head);
        return 1;
    }

    head = reverse_blocks(head, k);

    FILE *out = fopen(OUTPUT_FILENAME, "w");
    if (out == NULL)
    {
        free_list(head);
        perror(OUTPUT_FILENAME);
        return 1;
    }

    print_list(out, head);

    if (fclose(out) != 0)
    {
        free_list(head);
        perror(OUTPUT_FILENAME);
        return 1;
    }

    free_list(head);
    return 0;
}

/* Проверяет корректность полей записи */
int validate_student(const Student *s)
{
    if (s->id < MIN_ID)
    {
        return 1;
    }
    if (s->course < MIN_COURSE || s->course > MAX_COURSE)
    {
        return 1;
    }
    if (s->score < MIN_SCORE || s->score > MAX_SCORE)
    {
        return 1;
    }
    return 0;
}

/* Читает N, затем N записей и K */
Node *input_list(FILE *in, int *k_out, int *error)
{
    *error = 1;

    int n = 0;
    if (fscanf(in, "%d", &n) != 1)
    {
        fprintf(stderr, "Error reading N\n");
        return NULL;
    }
    if (n < MIN_N || n > MAX_N)
    {
        fprintf(stderr, "N out of range\n");
        return NULL;
    }

    if (n == 0)
    {
        *error = 0;
        return NULL;
    }

    Node *head = NULL;
    Node *tail = NULL;

    for (int i = 0; i < n; i++)
    {
        Student s;
        int read_count = fscanf(in, "%d %d %lf", &s.id, &s.course, &s.score);
        if (read_count != 3 || validate_student(&s) != 0)
        {
            fprintf(stderr, "Invalid record %d\n", i + 1);
            free_list(head);
            return NULL;
        }

        Node *node = malloc(sizeof(*node));
        if (node == NULL)
        {
            fprintf(stderr, "Memory allocation error\n");
            free_list(head);
            return NULL;
        }
        node->data = s;
        node->next = NULL;

        if (tail == NULL)
        {
            head = tail = node;
        }
        else
        {
            tail->next = node;
            tail = node;
        }
    }

    if (fscanf(in, "%d", k_out) != 1)
    {
        fprintf(stderr, "Error reading K\n");
        free_list(head);
        return NULL;
    }
    if (*k_out < MIN_K || *k_out > n)
    {
        fprintf(stderr, "K out of range\n");
        free_list(head);
        return NULL;
    }

    *error = 0;
    return head;
}


/* Записывает содержимое списка в файл в формате: id course score */
void print_list(FILE *out, const Node *head)
{
    for (const Node *p = head; p != NULL; p = p->next)
    {
        fprintf(out, "%d %d %.2f\n", p->data.id, p->data.course, p->data.score);
    }
}

/* Освобождает динамически выделенную память под все узлы списка */
void free_list(Node *head)
{
    while (head != NULL)
    {
        Node *next = head->next;
        free(head);
        head = next;
    }
}

/* Разворачивает каждый блок длины k */
Node *reverse_blocks(Node *head, int k)
{
    if (head == NULL || k <= 1)
    {
        return head;
    }

    Node *res_head = NULL;
    Node *res_tail = NULL;
    Node *cur = head;

    while (cur != NULL)
    {
        Node *block_end = cur;
        for (int c = 0; c < k && block_end != NULL; c++)
        {
            block_end = block_end->next;
        }

        Node *prev = NULL;
        Node *p = cur;
        while (p != block_end)
        {
            Node *next = p->next;
            p->next = prev;
            prev = p;
            p = next;
        }

        if (res_head == NULL)
        {
            res_head = prev;
            res_tail = cur;
        }
        else
        {
            res_tail->next = prev;
            res_tail = cur;
        }

        cur = block_end;
    }

    if (res_tail != NULL)
    {
        res_tail->next = NULL;
    }

    return res_head;
}