import tkinter as tk
from interfaz import DesactivacionTotal
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    root = tk.Tk()
    app = DesactivacionTotal(root)
    root.mainloop()