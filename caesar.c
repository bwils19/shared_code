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
        for (int i=0; key[i] != '\0'; i++)
        {
            if (isdigit(key[i]))
            {
            }
            else
            {
                ndigicnt++;
            }
        }
        if (ndigicnt ==0)
        {
            int intkey = atoi(key);
            string ptext = get_string("plaintext: ");
            printf("ciphertext: ");
            
            for (int j=0; ptext[j]!= '\0'; j++)
            {
                if (isalpha(ptext[j]))
                    {
                    if (isupper(ptext[j]))
                    {
                        printf("%c", (((ptext[j] + intkey) - 65) % 26) + 65);
                    }

                    if (islower(ptext[j]))
                    {
                        printf("%c", (((ptext[j] + intkey) - 97) % 26) + 97);
                    }
                }
                else //print character as is
                {
                    printf("%c", ptext[j]);
                }
            }
                // int lett = ptext[j] - '0';
                // int shift = key - '0';
                // printf("%d ",ptext[j]);
                // printf(" ");
                // printf(" %c : %d\n", ptext[j],ptext[j]);
                
                
                // printf("adjust: %i\n", lett + shift);
                // printf("%s", ctext);
                printf("\n");
                return 0;
        }
        else
        {
            printf("Usage: ./caesar key");
            return 1;
        }

    }
    if (argc == 1 || argc > 2)
    {
        printf("Usage: ./caesar key");
        return 1;
    }
    printf("\n");
}