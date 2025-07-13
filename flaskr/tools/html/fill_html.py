import os
from jinja2 import Environment, FileSystemLoader

# Set up the Jinja2 environment to load templates from the current directory.
current_path = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(current_path))
template = env.get_template('table_template.html')

# Define the data with additional table information.
data = {
    'title': 'Data Table Example',
    'heading': 'Sample Data Table',
    'content': 'Below is a table dynamically generated using Jinja2:',
    'table_headers': ['Name', 'Age', 'City'],
    'table_rows': [
        ['Alice', 30, 'New York'],
        ['Bob', 25, 'Los Angeles'],
        ['Charlie', 35, 'Chicago']
    ]
}

# Render the template with data.
rendered_html = template.render(data)

# Optionally, write the rendered HTML to a file.
with open(current_path + '\\output.html', 'w') as f:
    f.write(rendered_html)

print("HTML file 'output.html' has been generated.")
