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

        # Bind
        self.data.bind("<Right>", lambda event: self.select(1))
        self.statistic.bind("<Left>", lambda event: self.select(0))
        self.statistic.bind("<Right>", lambda event: self.select(2))
        self.graph.bind("<Left>", lambda event: self.select(1))

    def update(self):
        self.model.update()

    def tab_change(self, event):
        tab = event.widget.tab("current")["text"]

        # Data
        if tab == "Data":
            self.data.focus()

        # Statistic
        if tab == "Statistic":
            geometry = self.winfo_toplevel().geometry()
            self.winfo_toplevel().geometry(geometry)
            self.winfo_toplevel().update()
            self.statistic.tree_update()
            self.statistic.focus()

        # Graph
        if tab == "Graph":
            geometry = self.winfo_toplevel().geometry()
            self.winfo_toplevel().geometry(geometry)
            self.winfo_toplevel().update()
            self.graph.graph_update()
            self.graph.focus()
        
