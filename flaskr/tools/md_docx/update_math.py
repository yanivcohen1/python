import re
import os

def update_math():
    # Replace with your actual file name
    current_directory = os.path.dirname(__file__)
    filename = current_directory + "/copilot.md"

    # Read the file content
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    content = content.replace(r"\[", "$$").replace(r"\]", "$$")
    content = content.replace(r"\(", "$").replace(r"\)", "$")

    filename = current_directory + "/ex6.md"
    # Write the modified content back to the same file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    print("Math expressions updated successfully.")

if __name__ == "__main__":
    update_math()
