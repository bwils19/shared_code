import csv
import sys
import pandas as pd
import re

# Check that the correct arguments were passed
if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    sys.exit(1)

# Read the csv as a data frame
df = pd.read_csv(sys.argv[1])

# get a list of the columns to determine the patterns to match
patterns = list(df)
patterns.remove('name')

# Open the text file for the sequence
seq = open(sys.argv[2], "r")
seq = seq.read()

# Initialize empty data frome
row = pd.DataFrame()

for i in patterns:
    
    p = rf'({i})\1*'
    pattern = re.compile(p)
    match = [match for match in pattern.finditer(seq)]
    max = 0
    for j in range(len(match)):
        if match[j].group().count(i) > max:
            max = match[j].group().count(i)

    row2 = pd.DataFrame({i: [max]})
    row = pd.concat([row, row2], axis=1)

# append the 2 dataframes on the patterns    
new_df = pd.merge(df, row,  how='inner', left_on=patterns, right_on=patterns)

if new_df.empty:
    # if the df is empty, there is no match
    print('No match')

else:
    # if there is a match, print the name 
    print(new_df.name.item())

