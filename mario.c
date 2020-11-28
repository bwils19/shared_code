#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    do
    {
        // Prompt the user for the height
        height = get_int("Height:");
    }
    // ensure the height is within bounds
    while (height < 1 || height >8);
    int i;
    for ( i = 1; i <= height; i++)
    {
        int space;
        for (space = height - i; space >0; space --){
            // print the spaces before the hashes
            putchar(' ');
        }
        int hash;
        for (hash = 0; hash < i; hash++){
            // print the hashes
            putchar('#');
        }
        putchar('\n');
    }
}
