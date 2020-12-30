import sqlite3
import csv
import sys

# ensure the correct number of arguments are passed at the cli
if (len(sys.argv) != 2):
    sys.exit("Usage: import.py file.csv")

file = sys.argv[1]

# connect to the db
sqlite_file = "students.db"
conn = sqlite3.connect(sqlite_file)

cursor = conn.cursor()

# open csv file 
with open(file, "r") as characters:

    # Create Dictreader
    reader = csv.DictReader(characters)

    for row in reader:
        names = []

        # split name
        for part in row["name"].split(" "):
            names.append(part)

        names.append(row["house"])
        names.append(row["birth"])

        # insert split name into the database
        if (len(names) == 5):
            cursor.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", names[:5])

        if (len(names) == 4):
            cursor.execute("INSERT INTO students (first, last, house, birth) VALUES(?, ?, ?, ?)", names[:4])

conn.commit()
conn.close()
