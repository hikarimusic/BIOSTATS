import tkinter as tk
from tkinter import ttk

class Graph(ttk.Frame):

    def __init__(self, parent, master):

        ttk.Frame.__init__(self, parent)
        self.master = master

