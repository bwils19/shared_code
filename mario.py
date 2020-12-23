from cs50 import get_int

height = get_int("Height: ")

while height < 1 or height > 8:
    height = get_int("Height: ")

for i in range(height):
    ha = i + 1
    sp = height - ha
    for s in range(sp):
        print(' ', end="")
    for h in range(ha):
        print("#", end="")
    print("")    
