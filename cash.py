from cs50 import get_float

change = get_float("Change Owed: ")
while change < 0:
    change = get_float("Change Owed: ")
    
# convert dollar amounts to cents
cents = round(change*100)

# number of quarters
quarters = int(cents / 25)
remain = cents - (quarters * 25)

# number of dimes
dimes = int(remain / 10)
remain = remain - (dimes * 10)

# number of nickels
nickels = int(remain / 5)
remain = remain - (nickels * 5)

# pennies are what's left
pennies = int(remain)

# total it all up
total = quarters + dimes + nickels + pennies
print(total)