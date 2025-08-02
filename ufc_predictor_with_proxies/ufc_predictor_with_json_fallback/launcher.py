import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

def launch():
    try:
        subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'app.py'])
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("UFC Predictor Launcher")
root.geometry("300x100")
btn = tk.Button(root, text="Launch UFC Predictor", command=launch, padx=10, pady=10)
btn.pack(expand=True)
root.mainloop()
