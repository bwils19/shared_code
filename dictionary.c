// Implements a dictionary's functionality

#include <stdbool.h>
#include <strings.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 1;

// Hash table
node *table[N];

int wrd_cnt = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int h_index = hash(word);
    node *holder = table[h_index];

    while (holder != NULL)
    {
        if (strcasecmp(holder->word, word) == 0)
        {
            return true;
        }

        holder = holder->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int len = strlen(word);
    int sum = 0;

    for (int w = 0; w < len; w++)
    {
        sum += tolower(word[w]);
    }

    int tot = sum % N;
    return tot;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    // Return 1 if the file doesn't exist
    if (file == NULL)
    {
        return 1;
    }
    char word[LENGTH + 1];

    // scan through words and load to node
    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            unload();
            return false;
        }

        // copy to node
        strcpy(n->word, word);
        n->next = NULL;

        // store hash index
        int index = hash(n->word);

        // intialize list head
        node *head = table[index];

        if (head == NULL)
        {
            table[index] = n;
        }
        else
        {
            n->next = table[index];
            table[index] = n;
        }
        wrd_cnt += 1;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return wrd_cnt;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *list = table[i];
        node *holder = list;
        node *temp = list;

        while (holder != NULL)
        {
            holder = holder->next;
            free(temp);
            temp = holder;
        }
    }

    return true;
}
