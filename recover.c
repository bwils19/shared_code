#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define block_size 512

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover key \n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    // Return 1 if the file doesn't exist
    if (file == NULL)
    {
        return 1;
    }

    typedef uint8_t BYTE; 
    BYTE *buffer = malloc(512);
    char filename[8];
    FILE *img = NULL;
    int file_cnt = 0;
    
    // reading a block of 512 in memory card
    // BYTE buffer[block_size];
    
    while (fread(buffer, sizeof(unsigned char), 512, file))
    {
        if (buffer[0] == 0xFF && buffer[1] == 0xd8 && buffer[2] == 0xFF && (buffer[3] & 0xF0) == 0xe0)
        {
            file_cnt ++;
            
            // if 1st file
            if (file_cnt == 1)
            {
                sprintf(filename, "%03i.jpg", file_cnt - 1);
                img = fopen(filename, "a");
                fwrite(buffer, 1, 512, img);
            }
            // if it's not the 1st file
            else
            {
                // close previous file
                fclose(img);
                sprintf(filename, "%03i.jpg", file_cnt - 1);
                img = fopen(filename, "a");
                fwrite(buffer, 1, 512, img);
            }
        }
        else
        {
            if (img != NULL)
            {
                fwrite(buffer, 1, 512, img);
            }
        }
    }
            
    fclose(file);
    fclose(img);
    free(buffer);  
}    