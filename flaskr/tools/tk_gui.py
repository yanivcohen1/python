import subprocess
import tkinter as tk

def display_output():
    # proc = subprocess.Popen("calc", stdout=subprocess.PIPE, shell=True)
    # output_text = proc.communicate()[0].decode("utf-8")
    ans = eval(output.get("1.0", tk.END))
    output.delete(1.0, tk.END)
    output.insert(tk.END, ans)

# Create the main window
root = tk.Tk()

# Create buttons and text widget
display_button = tk.Button(root, text="Display output", command=display_output)
exit_button = tk.Button(root, text="Exit", fg="red", command=root.quit)
output = tk.Text(root, width=40, height=8)
output.insert(tk.END, "1+1")
# Pack widgets
display_button.pack(padx=20, pady=8)
exit_button.pack(padx=20, pady=18)
output.pack()

# Start the GUI event loop
root.mainloop()
