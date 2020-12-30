from cs50 import SQL
import sys

# ensure the correct number of arguments are passed at the cli
if (len(sys.argv) != 2):
    sys.exit("Usage: roster.py House")

# define db
database = SQL("sqlite:///students.db")

# assign the house name that was passed at the cli to variable house
house = sys.argv[1]

# query database for everyone in that house
rows = database.execute("SELECT * FROM students WHERE house = ? ORDER BY last, first", house)

# return the results
for row in rows:
    first, middle, last, birth = row["first"], row["middle"], row["last"], row["birth"]
    print(f"{first} {middle + ' ' if middle else ''}{last}, born {birth}")