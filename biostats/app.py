import os
import tkinter as tk
from tkinter import ttk

from biostats.master import Master

class App(tk.Tk):

    def __init__(self):

        # Initialize
        tk.Tk.__init__(self)
        self.title("BIOSTATS")

        # Setup
        self.setup()

    def setup(self):

        # Theme
        theme = os.path.join(os.path.dirname(__file__), "azure.tcl")
        self.tk.call("source", theme)
        self.tk.call("set_theme", "light")

        # Configure
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=30)

        # Master Frame
        master = Master(self, self)
        master.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=1, column=1, padx=5, pady=5)

        # Set Minimun Size
        self.minsize(int(self.winfo_screenwidth() / 2), int(self.winfo_screenheight() * 5 / 6))
        x_coordinate = int(self.winfo_screenwidth() / 4)
        y_coordinate = int(self.winfo_screenheight() / 12)
        self.geometry("+{}+{}".format(x_coordinate, y_coordinate))
    
    def swtich_mode(self, darkmode):
        
        if darkmode == 1 :
            self.tk.call("set_theme", "dark")
            self.style.configure("Treeview", rowheight=30)
        else:
            self.tk.call("set_theme", "light")
            self.style.configure("Treeview", rowheight=30)
        

