import tkinter as tk
from tkinter import ttk

class Graph(ttk.Frame):

    def __init__(self, parent, controller):

        ttk.Frame.__init__(self, parent)
        self.controller = controller

