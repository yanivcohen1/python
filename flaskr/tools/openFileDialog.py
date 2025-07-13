import tkinter as tk
from tkinter import filedialog

# root = tk.Tk()
# root.withdraw()

# open file dialog
def openFile():
    file = filedialog.askopenfilename()
    return file

if __name__ == '__main__':
    print(filedialog.askopenfilename())
