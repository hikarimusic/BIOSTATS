import tkinter as tk
from tkinter import ttk

from . import data
from . import statistic
from . import graph
from . import test
from . import core

class Master(ttk.Notebook):

    def __init__(self, parent):
        
        # Intialize
        ttk.Notebook.__init__(self, parent)

        # Data
        self.model = core.Model()

        # Setup
        self.setup()

        # Change Tab
        self.bind("<<NotebookTabChanged>>", self.tab_change)

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
        self.add(self.graph, text="Graph")

        self.test = test.Test(self, self)
        self.add(self.test, text="Test")

    def update(self):
        self.model.update()
        #self.statistic.tree_update()

    def tab_change(self, event):
        tab = event.widget.tab("current")["text"]
        if tab == "Statistic":
            self.winfo_toplevel().update()
            self.statistic.tree_update()
        
