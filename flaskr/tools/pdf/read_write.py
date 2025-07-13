import os
import pdfplumber
from reportlab.pdfgen import canvas

current_path = os.path.dirname(os.path.abspath(__file__))
# File paths
input_pdf = current_path + "/input.pdf"
output_pdf = current_path + "/output.pdf"

# Step 1. Extract text from the input PDF using pdfplumber
extracted_pages = []
with pdfplumber.open(input_pdf) as pdf:
    for page in pdf.pages:
        text = page.extract_text()  # you can also extract tables or images as needed
        extracted_pages.append(text)

# Step 2. Create a new PDF using ReportLab and write the extracted text
c = canvas.Canvas(output_pdf)
width, height = c._pagesize  # get page size, for example A4 or letter

# You might want to define some margins and line height
x_margin = 50
y_margin = 50
line_height = 15

for page_text in extracted_pages:
    if not page_text:
        # In case the PDF page has no text.
        c.showPage()
        continue

    # Start drawing text near the top of the page
    y_position = height - y_margin

    # Loop over each line in the extracted text
    for line in page_text.split('\n'):
        # If there isn’t enough room in the current page, start a new one.
        if y_position < y_margin:
            c.showPage()
            y_position = height - y_margin
        c.drawString(x_margin, y_position, line)
        y_position -= line_height

    # After processing one pdfplumber page, move to a new page in our output PDF.
    c.showPage()

# Save the new PDF file
c.save()

print("New PDF created:", output_pdf)
