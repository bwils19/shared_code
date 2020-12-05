#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        string key = argv[1];
        int ndigicnt = 0;
        // Check if each value in the input is a number
        for (int i = 0; key[i] != '\0'; i++)
        {
            if (isdigit(key[i]))
            {
            }
            else
            {
                ndigicnt++;
            }
        }
        if (ndigicnt == 0)
        {
            // convert key to an integer
            int intkey = atoi(key);
            string ptext = get_string("plaintext: ");
            printf("ciphertext: ");
            
            // Convert each character to rotate as far as the key says
            for (int j = 0; ptext[j] != '\0'; j++)
            {
                if (isalpha(ptext[j]))
                {
                    // If the character is uppercase
                    if (isupper(ptext[j]))
                    {
                        printf("%c", (((ptext[j] + intkey) - 65) % 26) + 65);
                    }
                    // If the character is lowercase
                    if (islower(ptext[j]))
                    {
                        printf("%c", (((ptext[j] + intkey) - 97) % 26) + 97);
                    }
                }
                else 
                {
                    printf("%c", ptext[j]);
                }
            }
            printf("\n");
            return 0;
        }
        else
        {
            // Send error message
            printf("Usage: ./caesar key");
            return 1;
        }

    }
    if (argc == 1 || argc > 2)
    {
        //Send error message
        printf("Usage: ./caesar key");
        return 1;
    }
    printf("\n");
}