from bs4 import BeautifulSoup
# import requests
import pandas as pd

# Sample HTML content
# html = requests.get('https://www.google.com').text

# Sample HTML content with a table
html_content = """
<html>
    <body>
        <div class="example">
            <p id="target">This is the paragraph you want to find.</p>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Column1</th>
                    <th>Column2</th>
                    <th>Column3</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Data1</td>
                    <td>Data2</td>
                    <td>Data3</td>
                </tr>
                <tr>
                    <td>Data4</td>
                    <td>Data5</td>
                    <td>Data6</td>
                </tr>
            </tbody>
        </table>
    </body>
</html>
"""

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find element by CSS path
target_element = soup.select("div.example > p#target")[0]

# Print the found element's text
print("find by css: (div.example > p#target) is:", target_element.text)

# Find the table
table = soup.find('table')

# Extract the table headers
headers = [header.text for header in table.find_all('th')]

# Extract the table rows
rows = []
for row in table.find_all('tr')[1:]:  # Skip the header row
    rows.append([cell.text for cell in row.find_all('td')])

row_names = ['Row1', 'Row2']
# Create the DataFrame
df = pd.DataFrame(rows, columns=headers, index=row_names)

# Display the DataFrame
print(df)
print('Column2 is',df['Column2'][0:2].values)
element = df.loc['Row2', 'Column2']
print('row2 column2 is:', element)
