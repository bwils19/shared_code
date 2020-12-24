from cs50 import get_string
import re

s = get_string("Text: ")

# count letters, words and sentences
letters = sum(c.isalpha() for c in s)
words = len(s.split())
sent = re.split('[!?.]',s)

# remove the weird empty character from the list in sentences
for i in sent:
    if i == '':
        sent.remove(i)
sent = len(sent)        
    
# calculate the grade
grade = round(0.0588 * (100 * letters / words) - 0.296 * (100 * sent / words)  - 15.8)

# determine the grade range
if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")
