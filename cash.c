#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float amt;
    do
    {
    amt = get_float("Change owed: ");
    }
    while(amt < 0);
    // convert the dollar amount to cents
    int cents = round(amt * 100);
    
    // How many quarters do we need
    int quarts, dimes, nicks, pens = 0;
    quarts = cents / 25;
    int coins = quarts;
    int amt_remain = cents - (quarts*25);
    
    // how many dimes
    if (amt_remain > 0)
    {
        dimes = amt_remain / 10;
        amt_remain = amt_remain - (dimes*10);
        coins = coins + dimes;
    }
    
    // how many nickels
    if (amt_remain > 0)
    {
        nicks = amt_remain / 5;
        amt_remain = amt_remain - (nicks * 5);
        coins = coins + nicks;
    }
    
    // how many pennies
    if (amt_remain > 0)
    {
        pens = amt_remain;
        amt_remain = 0;
        coins = coins + pens;
    }
    // print the minimum number of coins needed
    printf("%i\n", coins);
}