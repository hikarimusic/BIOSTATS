import tkinter as tk
from tkinter import ttk

import data
import statistic
import graph
import test

class Master(ttk.Notebook):

    def __init__(self, parent):
        
        # Intialize
        ttk.Notebook.__init__(self, parent)

        # Setup
        self.setup()

    def setup(self):

        # Configure
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

        # Tab
        self.data = data.Data(self, self)
        self.add(self.data, text="Data")

        self.statistic = statistic.Statistic(self, self)
        self.add(self.statistic, text="Statistic")

        self.graph = graph.Graph(self, self)
        self.add(self.graph, text="Gaprh")

        self.test = test.Test(self, self)
        self.add(self.test, text="Test")
