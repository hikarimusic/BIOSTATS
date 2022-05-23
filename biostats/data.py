import tkinter as tk
from tkinter import ttk
import pandas as pd

from .widget import Tree

class Data(ttk.Frame):

    def __init__(self, parent, master):
        
        # Initialize
        ttk.Frame.__init__(self, parent)
        self.master = master

        # Setup
        self.setup()

    def setup(self):

        # Configure
        self.rowconfigure(index=3, weight=1)
        self.columnconfigure(index=4, weight=1)
        self.configure(padding=(10,10))

        # Edit, Open
        self.edit_button = ttk.Button(self, text="Edit")
        self.edit_button.config(command=lambda: self.switch("edit"))
        self.edit_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.open_button = ttk.Button(self, text="Open")
        self.open_button.config(command=self.open)
        self.open_button.grid(row=0, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Tree
        self.tree = Tree(self, 15)
        self.tree.grid(row=1, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")
        self.tree.data = pd.read_csv("biostats/dataset/penguins.csv")

        self.updating()

    def updating(self):

        self.tree.show(self.master.scientific.get(), self.master.precision.get())

    def switch(self, key):
        pass

    def open(self):
        pass