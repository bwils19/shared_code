#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
                // Read the value of each color for each pixel 
                int red = image[i][j].rgbtRed;
                int blue = image[i][j].rgbtBlue;
                int green = image[i][j].rgbtGreen;
                
                // Get the average of the 3 colors in each pixel
                int average = round((red + blue + green)/3.0);
                
                // Get the average of the 3 colors
                // average = round(average);
                
                // Apply the average value back to each color scale for each pixel
                image[i][j].rgbtRed = average;
                image[i][j].rgbtBlue = average;
                image[i][j].rgbtGreen = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
                // Read the value of each color for each pixel 
                int originalRed = image[i][j].rgbtRed;
                int originalBlue = image[i][j].rgbtBlue;
                int originalGreen = image[i][j].rgbtGreen;
                
                // Get the sepia value for each color scale for each pixel
                float sepiaRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
                if (sepiaRed > 255)
                {
                    sepiaRed = 255;
                }
                
                float sepiaGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
                if (sepiaGreen > 255)
                {
                    sepiaGreen = 255;
                }
                
                float sepiaBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);
                if (sepiaBlue > 255)
                {
                    sepiaBlue = 255;
                }
                
                // Apply the sepia value to each of the colors in each pixel
                image[i][j].rgbtRed = sepiaRed;
                image[i][j].rgbtBlue = sepiaGreen;
                image[i][j].rgbtGreen = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // The middle index
    int mid = width / 2;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < mid; j++)
        {
            // Swap the left t with right 
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int avgR, avgG, avgB, cnt;

        // copy table

        RGBTRIPLE copy[height][width];

        for (int i = 0; i < height; i++)
        {
            for (int j = 0; j < width; j++)
            {
                copy[i][j] = image[i][j];
            }
        }

        for (int k = 0; k < height; k++)
        {
            for (int l = 0; l < width; l++)
            {
                // initialize variables to 0
                avgR = avgG = avgB = cnt = 0;

                for (int row = -1; row < 2; row++)
                {
                    for (int col = -1; col < 2; col++)
                    {
                        if (k + row < 0 || l + col < 0 || k + row >= height || l + col >= width)
                        {

                        }
                        else
                        {
                            avgR += copy[k + row][l + col].rgbtRed;
                            avgG += copy[k + row][l + col].rgbtGreen;
                            avgB += copy[k + row][l + col].rgbtBlue;
                            cnt ++;
                        }
                    }
                }
                image[k][l].rgbtRed = round(avgR / (float) cnt);
                image[k][l].rgbtGreen = round(avgG / (float) cnt);
                image[k][l].rgbtBlue = round(avgB / (float) cnt);
            }
        }
    return;
}
