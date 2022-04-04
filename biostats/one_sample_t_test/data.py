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
        self.rowconfigure(index=1, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.configure(padding=(20,20))

        # Data View
        self.data_view = ttk.Frame(self)
        self.data_view.grid(
            row=0, column=0, sticky="nsew"
        )
        self.data_view.columnconfigure(index=2, weight=1)

        # Button
        self.edit_button = ttk.Button(self.data_view, text="Edit")
        self.edit_button.config(command=lambda: self.show("edit"))
        self.edit_button.grid(
            row=0, column=0, padx=5, pady=5, sticky="nsew"
        )

        self.open_button = ttk.Button(self.data_view, text="Open")
        self.open_button.config(command=self.open)
        self.open_button.grid(
            row=0, column=1, pady=5, sticky="nsew"
        )

        # Treeview
        self.scrollbar = ttk.Scrollbar(self.data_view)
        self.scrollbar.grid(row=1, column=5, padx=(0,5), sticky="nsew")

        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=30)
        
        self.tree = ttk.Treeview(
            self.data_view, selectmode="none", height=15
        )
        self.tree.config(column=(1))
        self.tree.grid(row=1, column=0, columnspan=5, padx=(5,0), sticky="nsew")

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
            self.data_view, text="Scientific", style="Switch.TCheckbutton"
        )
        self.notation.grid(
            row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew"
        )

        # Precision
        self.precision_label = ttk.Label(
            self.data_view, text="Precision"
        )
        self.precision_label.grid(
            row=2, column=3, pady=5, sticky="nsew"
        )


        self.precision = ttk.Spinbox(
            self.data_view, from_=0, to=99, increment=1, width=5
        )
        self.precision.insert(0, 0)
        self.precision.grid(
            row=2, column=4, padx=(5,0), pady=5, sticky="nsew"
        )

        # Data Edit
        self.data_edit = ttk.Frame(self) 
        self.data_edit.grid(
            row=0, column=0, sticky="nsew"
        )
        self.data_edit.columnconfigure(index=4, weight=1)
        self.data_edit.rowconfigure(index=1, weight=1)

        # Control Bar
        self.row_label = ttk.Label(self.data_edit, text="Row")
        self.row_label.grid(
            row=0, column=0, padx=(5,0), pady=5, sticky="nsew"
        )
        self.row_spin = ttk.Spinbox(
            self.data_edit, from_=1, to=999, increment=1, width=6
        )
        self.row_spin.grid(
            row=0, column=1, padx=5, pady=5, sticky="nsew"
        )
        self.row_spin.insert(0,10)

        self.column_label = ttk.Label(self.data_edit, text="Column")
        self.column_label.grid(
            row=0, column=2, padx=(5,0), pady=5, sticky="nsew"
        )
        self.column_spin = ttk.Spinbox(
            self.data_edit, from_=1, to=999, increment=1, width=6
        )
        self.column_spin.grid(
            row=0, column=3, padx=5, pady=5, sticky="nsew"
        )
        self.column_spin.insert(0,10)
        
        self.confirm_button = ttk.Button(
            self.data_edit, text="Confirm", style="Accent.TButton"
        )
        self.confirm_button.config(command=self.confirm)
        self.confirm_button.grid(
            row=0, column=5, columnspan=2, pady=5, sticky="e"
        )

        # Table
        self.table_frame = ttk.Notebook(self.data_edit)
        self.table_frame.grid(
            row=1, column=0, columnspan=7, padx=(5,0), sticky="nsew"
        )

        self.scrollbar2 = ttk.Scrollbar(self.data_edit)
        self.scrollbar2.grid(
            row=1, column=7, padx=(0,5), sticky="nsew"
        )

        # Cell Width

        self.cell_width_label = ttk.Label(
            self.data_edit, text="Cell Width"
        )
        self.cell_width_label.grid(
            row=2, column=5, padx=5, pady=5, sticky="nsew"
        )

        self.cell_width = ttk.Spinbox(
            self.data_edit, from_=1, to=99, increment=1, width=5
        )
        self.cell_width.insert(0, 10)
        self.cell_width.grid(
            row=2, column=6, padx=(5,0), pady=5, sticky="nsew"
        )

        # Export
        self.export = ttk.Button(self, text="Export")
        self.export.grid(
            row=2, column=0, sticky="e"
        )

        # Show
        self.show("view")

    def show(self, key):
        
        if key == "view":
            frame = self.data_view
        if key == "edit":
            frame = self.data_edit

        frame.tkraise()

    def open(self):
        pass

    def confirm(self):
        
        self.show("view")
