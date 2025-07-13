# pip install pypandoc
import os
import pypandoc
import update_math

# this is after pip install this download_pandoc
# pypandoc.download_pandoc()

def md_to_docx(input_md: str, output_docx: str):
    """
    Convert a Markdown file to a Word (.docx) file using pypandoc.

    Requirements:
        • pip install pypandoc
        • Pandoc installed on your system (https://pandoc.org/installing.html)
    """
    # pypandoc will call the pandoc CLI under the hood
    pypandoc.convert_file(input_md, 'docx', outputfile=output_docx)
    print(f"Converted {input_md} → {output_docx}")

if __name__ == '__main__':
    current_directory = os.path.dirname(__file__)
    # update the math expressions in the markdown file
    update_math.update_math()
    md_filename = current_directory + "/ex6.md"
    docx_filename = current_directory + "/copilot.docx"
    md_to_docx(md_filename, docx_filename)
