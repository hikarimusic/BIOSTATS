import tkinter as tk
from tkinter import ttk

from . import core

class Data(ttk.Frame):

    def __init__(self, parent, master):
        
        # Initialize
        ttk.Frame.__init__(self, parent)
        self.master = master

        # Setup
        self.setup()

    def setup(self):

        # Configure
        self.columnconfigure(index=2, weight=1)
        #self.rowconfigure(index=0, weight=1)
        #self.rowconfigure(index=1, weight=1)
        self.rowconfigure(index=3, weight=1)
        self.configure(padding=(20,20))

        # Description
        '''
        self.description = ttk.Label(
            self, text="Analyze one dimensional measurement data of one group."
        )
        #self.description.config(font="-slant italic")
        self.description.grid(
            row=0, column=0, padx=15, pady=(0,10), sticky="nsew"
        )
        '''

        # Data Frame
        '''
        self.data_frame = ttk.Frame(self)
        self.data_frame.grid(
            row=0, column=0, sticky="nsew"
        )
        self.data_frame.columnconfigure(index=2, weight=1)
        '''
        
        # Button
        self.edit = ttk.Button(self, text="edit")
        self.edit.grid(
            row=0, column=0, padx=(5,0), pady=5, #sticky="nsew"
        )
        self.edit.config(command=lambda: self.show(1))

        self.open = ttk.Button(self, text="open")
        self.open.grid(
            row=0, column=1, padx=(5,0), pady=5, #sticky="nsew"
        )

        # Table
        self.table = ttk.Frame(self)
        self.table.grid(
            row=1, column=0, columnspan=5, padx=5, sticky="nsew"
        )
        self.table.columnconfigure(index=0, weight=1)

        self.scrollbar = ttk.Scrollbar(self.table)
        self.scrollbar.grid(row=0, column=1, sticky="nsew")
        
        self.tree = ttk.Treeview(
            self.table, selectmode="none", column=(1), height=20
        )
        self.tree.grid(row=0, column=0, sticky="nsew")

        self.tree.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tree.yview)
        
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column(1, anchor="center", width=20)

        self.tree.heading("#0", text="Label", anchor="center")
        self.tree.heading(1, text="Group", anchor="center")

        for i in range(50):
            self.tree.insert(
                parent='', index="end", iid=i, values=i*100
            )
        
        # Notation
        self.notation = ttk.Checkbutton(
            self, text="Scientific", style="Switch.TCheckbutton"
        )
        self.notation.grid(
            row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew"
        )

        # Precision
        self.precision_label = ttk.Label(
            self, text="Precision"
        )
        self.precision_label.grid(
            row=2, column=3, padx=5, pady=5
        )


        self.precision = ttk.Spinbox(
            self, from_=0, to=99, increment=1, width=5
        )
        self.precision.insert(0, 0)
        self.precision.grid(
            row=2, column=4, padx=5, pady=5
        )

        # Export
        self.export = ttk.Button(self, text="export")
        self.export.grid(
            row=4, column=3, columnspan=2, sticky="e"
        )

    def show(self, frame):
        pass
