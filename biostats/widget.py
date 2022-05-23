import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np

from biostats import data

class Tree(ttk.Frame):

    def __init__(self, parent, height):
        
        # Initialize
        ttk.Frame.__init__(self, parent)

        self.height = height
        self.data = pd.DataFrame()

        self.setup()

    def setup(self):

        # Configure
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)

        # Treeview
        self.treeview = ttk.Treeview(self, selectmode="none", height=self.height)
        self.treeview.grid(row=0, column=0, sticky="nsew")

        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical")
        self.scrollbar_y.grid(row=0, column=1, sticky="nsew")
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal")
        self.scrollbar_x.grid(row=1, column=0, sticky="nsew")

        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=30)
        
        self.treeview.config(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_y.config(command=self.treeview.yview)
        self.treeview.config(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.config(command=self.treeview.xview)

    def show(self, scientific, precision):

        # Clear
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        self.treeview.config(column=())

        geometry = self.winfo_toplevel().geometry()
        self.winfo_toplevel().geometry(geometry)

        # Width
        width = [100]*len(self.data.columns)

        # Columns
        self.treeview.config(columns=self.data.columns.tolist())
        self.treeview.column("#0", anchor="center", minwidth=50, width=50, stretch="no")

        for i, col in enumerate(self.data.columns.tolist()):
            self.treeview.column(col, anchor="center", minwidth=100, width=100)
            self.treeview.heading(col, text=col, anchor="center")
            width[i] = max(width[i],len(col)*10)

        # Data
        for i in range(len(self.data)):
            value = []
            for j in range(len(self.data.columns)):
                if pd.isna(self.data.iloc[i][j]):
                    temp = ""
                elif isinstance(self.data.iloc[i][j], np.floating):
                    if scientific == 1:
                        temp = format(round(self.data.iloc[i][j],precision), '.{}E'.format(precision))
                    else:
                        temp = format(round(self.data.iloc[i][j],precision), '.{}f'.format(precision))
                else:
                    temp = str(self.data.iloc[i][j])
                value.append(temp)
                width[j] = max(width[j],len(temp)*10)
            self.treeview.insert(parent="", index="end", text=i+1, values=value)

        for i, col in enumerate(self.data.columns.tolist()):
            self.treeview.column(col, minwidth=width[i])


                
                
                

        '''
        for i in range(row):
            value = []
            for j in range(column):
                try:
                    if notation == 1:
                        temp = format(round(self.model.data[j][i],precision), '.{}E'.format(precision))
                    else:
                        temp = format(round(self.model.data[j][i],precision), '.{}f'.format(precision))
                    value.append(temp)
                    width[j] = max(width[j],len(temp)*10)
                except:
                    value.append("")
            self.tree.insert(
                parent='' , index="end", iid=i, values=value
            )
        value = []
        for i in range(column):
            if self.model.size[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    temp = format(round(self.model.size[i],precision), '.{}E'.format(precision))
                else:
                    temp = str(self.model.size[i])
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="Sample Size", values=tuple(value)
        )
        '''