#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    // Get the text from the user
    string s = get_string("Text: ");
    int lett = 0; 
    int word = 0;
    int sent = 0;
    
    // Count letters, words anbd sentences
    for (int i = 0; s[i] != '\0'; i++)
    {
        if (isalpha(s[i]))
        {
            lett++; 
        }
        if (isspace(s[i]))
        {
            word++;
        }
        if (s[i] == '.' || s[i] == '!' || s[i] == '?')
        {
            sent++;
        }
    }
    word++;
    
    // Calculate the Coleman-Liau index
    int grade = round(0.0588 * (100 * lett / (float) word) - 0.296 * (100 * sent / (float) word)  - 15.8);
    if (grade < 1)
    {
        printf("Before Grade 1");
    }
    if (grade >= 16)
    {
        printf("Grade 16+");
    }
    if (grade >= 1 && grade < 16)
    {
        printf("Grade %i", grade);
    }
    printf("\n");
}
