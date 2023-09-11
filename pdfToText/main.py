# importing required modules
from PyPDF2 import PdfReader
import sys

if len(sys.argv) != 2:
    print("Incorrect Usage", file=sys.stderr)
    sys.exit(1)
input = sys.argv[1]

output = input.replace(".pdf", ".txt")

f = open(output, "a")

# creating a pdf reader object
reader = PdfReader(input)

# printing number of pages in pdf file
# print(len(reader.pages))

for i in range(len(reader.pages)):
    page = reader.pages[i]
    text = page.extract_text()
    f.write(text)

f.close()
