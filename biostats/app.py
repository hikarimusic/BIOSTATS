import os
import tkinter as tk
from tkinter import ttk

from . import layout

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
        self.tk.call("set_theme", "dark")

        # Configure
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

        # Master Frame
        self.master = layout.Master(self)
        self.master.grid(row=0, column=0, sticky="nsew")

        # Set Minimun Size
        self.update()
        self.minsize(int(self.winfo_screenwidth() * 2 / 3), self.winfo_height())
        x_coordinate = int(self.winfo_screenwidth() / 6)
        y_coordinate = int((self.winfo_screenheight() / 2) - (self.winfo_height() / 2))
        self.geometry("+{}+{}".format(x_coordinate, y_coordinate-20))
