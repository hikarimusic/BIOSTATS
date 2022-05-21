import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np


class Statistic(ttk.Frame):

    def __init__(self, parent, master):
        
        # Initialize
        ttk.Frame.__init__(self, parent)
        self.master = master
        self.model = master.model

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
        self.open_button.config(command=self.tree_update)
        self.open_button.grid(
            row=0, column=1, pady=5, sticky="nsew"
        )

        # Treeview
        self.scrollbar_1y = ttk.Scrollbar(self.data_view, orient="vertical")
        self.scrollbar_1y.grid(row=1, column=5, padx=(0,5), sticky="nsew")
        self.scrollbar_1x = ttk.Scrollbar(self.data_view, orient="horizontal")
        self.scrollbar_1x.grid(row=2, column=0, columnspan=5, padx=(5,0), sticky="nsew")

        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=30)
        
        self.tree = ttk.Treeview(
            self.data_view, selectmode="none", height=15
        )
        self.tree.config(column=(1))
        self.tree.grid(row=1, column=0, columnspan=5, padx=(5,0), sticky="nsew")

        self.tree.config(yscrollcommand=self.scrollbar_1y.set)
        self.scrollbar_1y.config(command=self.tree.yview)
        self.tree.config(xscrollcommand=self.scrollbar_1x.set)
        self.scrollbar_1x.config(command=self.tree.xview)
        
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column(1, anchor="center")

        self.tree.heading("#0", text="Label", anchor="center")
        self.tree.heading(1, text="", anchor="center")

        # Notation
        self.scientific = tk.IntVar()
        self.notation = ttk.Checkbutton(
            self.data_view, text="Scientific", style="Switch.TCheckbutton"
        )
        self.notation.config(
            variable=self.scientific, command=self.tree_update
        )
        self.notation.grid(
            row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew"
        )

        # Precision
        self.precision_label = ttk.Label(
            self.data_view, text="Precision"
        )
        self.precision_label.grid(
            row=3, column=3, pady=5, sticky="nsew"
        )


        self.precision = ttk.Spinbox(
            self.data_view, from_=1, to=99, increment=1, width=5, command=self.tree_update
        )
        self.precision.insert(0,1)
        self.precision.grid(
            row=3, column=4, padx=(5,0), pady=5, sticky="nsew"
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
            self.data_edit, from_=1, to=999, increment=1, width=6, command=self.resize
        )
        self.row_spin.insert(0,10)
        self.row_spin.grid(
            row=0, column=1, padx=5, pady=5, sticky="nsew"
        )

        self.column_label = ttk.Label(self.data_edit, text="Column")
        self.column_label.grid(
            row=0, column=2, padx=(5,0), pady=5, sticky="nsew"
        )
        self.column_spin = ttk.Spinbox(
            self.data_edit, from_=1, to=999, increment=1, width=6, command=self.resize
        )
        self.column_spin.insert(0,3)
        self.column_spin.grid(
            row=0, column=3, padx=5, pady=5, sticky="nsew"
        )
        
        self.confirm_button = ttk.Button(
            self.data_edit, text="Confirm", style="Accent.TButton"
        )
        self.confirm_button.config(command=self.confirm)
        self.confirm_button.grid(
            row=0, column=5, columnspan=2, pady=5, sticky="e"
        )

        # Table
        self.table_frame = ttk.Frame(self.data_edit, style="Card.TFrame", padding=(2,2))
        self.table_frame.grid(
            row=1, column=0, columnspan=7, padx=(5,0), ipadx=20, sticky="nsew"
        )
        self.table_frame.rowconfigure(index=0, weight=1)
        self.table_frame.columnconfigure(index=0, weight=1)

        self.scrollbar_2y = ttk.Scrollbar(self.data_edit, orient="vertical")
        self.scrollbar_2y.grid(
            row=1, column=7, padx=(0,5), sticky="nsew"
        )
        self.scrollbar_2x = ttk.Scrollbar(self.data_edit, orient="horizontal")
        self.scrollbar_2x.grid(
            row=2, column=0, columnspan=7, padx=(5,0), sticky="nsew"
        )

        # Entry
        self.entry_canvas = tk.Canvas(self.table_frame)
        self.entry_canvas.grid(row=0, column=0, sticky="nsew")

        self.entry_frame = ttk.Frame(self.entry_canvas)
        self.entry_frame.grid(
            row=0, column=0
        )

        self.scrollbar_2y.configure(command=self.entry_canvas.yview)
        self.scrollbar_2x.configure(command=self.entry_canvas.xview)
        self.entry_frame.bind(
            "<Configure>",
            lambda e: self.entry_canvas.configure(
                scrollregion=self.entry_canvas.bbox("all")
            )
        )

        self.entry_canvas.create_window((0,0), window=self.entry_frame, anchor="nw")
        self.entry_canvas.configure(yscrollcommand=self.scrollbar_2y.set)
        self.entry_canvas.configure(xscrollcommand=self.scrollbar_2x.set)

        self.table_frame.bind("<Enter>", self.mouse_enter)
        self.table_frame.bind("<Leave>", self.mouse_leave)

        self.entry = {}
        self.number = {}
        '' '
        for i in range(0,11):
            self.number[i] = ttk.Label(self.entry_frame, text=i)
            self.number[i].grid(
                row=i, column=0, padx=5
            )
            self.entry[i] = ttk.Entry(self.entry_frame, width=10, justify="center")
            self.entry[i].bind("<Up>", lambda event, target=i-1: self.move_focus(event, target))
            self.entry[i].bind("<Down>", lambda event, target=i+1: self.move_focus(event, target))
            self.entry[i].grid(row=i, column=1)
        self.entry[0].insert(0,"Group A")
        '' '

        '' '
        # Clear

        self.clear_button = ttk.Button(
            self.data_edit, text="Clear", command=self.clear
        )
        self.clear_button.grid(
            row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w"
        )
        '' '

        # Cell Width

        self.cell_width_label = ttk.Label(
            self.data_edit, text="Cell Width"
        )
        self.cell_width_label.grid(
            row=3, column=5, padx=5, pady=5, sticky="nsew"
        )

        self.cell_width = ttk.Spinbox(
            self.data_edit, from_=1, to=99, increment=1, width=5, command=self.change_width
        )
        self.cell_width.insert(0,10)
        self.cell_width.grid(
            row=3, column=6, padx=(5,0), pady=5, sticky="nsew"
        )

        # Export
        self.export = ttk.Button(self, text="Export")
        self.export.grid(
            row=2, column=0, sticky="e"
        )

        # Show
        self.show("view")
        self.resize()
        

    def show(self, key):
        
        if key == "view":
            frame = self.data_view
        if key == "edit":
            frame = self.data_edit
            self.entry[(1,1)].focus()

        frame.tkraise()

    def mouse_enter(self, event):
        # Linux 
        self.entry_canvas.bind_all('<4>', lambda event : self.entry_canvas.yview('scroll', -1, 'units'))
        self.entry_canvas.bind_all('<5>', lambda event : self.entry_canvas.yview('scroll', 1, 'units'))
        self.entry_canvas.bind_all('<Shift-4>', lambda event : self.entry_canvas.xview('scroll', -1, 'units'))
        self.entry_canvas.bind_all('<Shift-5>', lambda event : self.entry_canvas.xview('scroll', 1, 'units'))

    def mouse_leave(self, event):
        self.entry_canvas.unbind_all('<4>')
        self.entry_canvas.unbind_all('<5>')

    def resize(self):
        #print(self.row_spin.get())
        #print(self.column_spin.get())
        
        #row = int(float(self.row_spin.get()))
        #print(type(row))

        try: 
            row = int(float(self.row_spin.get()))
        except:
            row = 10
        try:
            column = int(float(self.column_spin.get()))
        except:
            column = 3
        try:
            width_val = int(float(self.cell_width.get()))
        except:
            width_val = 10
        
        for i in range(1,row+1):
            for j in range(1,column+1):
                if not (i,j) in self.entry:
                    self.entry[(i,j)] = ttk.Entry(self.entry_frame, width=width_val, justify="center")
                    self.entry[(i,j)].bind("<Up>", lambda event, target=(i-1,j): self.move_focus(event, target))
                    self.entry[(i,j)].bind("<Down>", lambda event, target=(i+1,j): self.move_focus(event, target))
                    self.entry[(i,j)].bind("<Left>", lambda event, target=(i,j-1): self.move_focus(event, target))
                    self.entry[(i,j)].bind("<Right>", lambda event, target=(i,j+1): self.move_focus(event, target))
                    self.entry[(i,j)].grid(row=i, column=j)

        for i in range(1,row+1):
            if not i in self.number:
                self.number[i] = ttk.Label(self.entry_frame, text=i)
                self.number[i].grid(row=i, column=0, padx=5)

        for j in range(1,column+1):
            if not (0,j) in self.entry:
                self.entry[(0,j)] = ttk.Entry(self.entry_frame, width=width_val, justify="center")
                self.entry[(0,j)].insert(0,"Group "+self.group_name(j))
                self.entry[(0,j)].grid(row=0, column=j, pady=(10,0))
                self.entry[(0,j)].bind("<Down>", lambda event, target=(1,j): self.move_focus(event, target))
                self.entry[(0,j)].bind("<Left>", lambda event, target=(0,j-1): self.move_focus(event, target))
                self.entry[(0,j)].bind("<Right>", lambda event, target=(0,j+1): self.move_focus(event, target))

        for (i,j), entry in self.entry.items():
            if i>row or j>column:
                entry.grid_remove()
            else:
                entry.grid()
        for i, number in self.number.items():
            if i>row:
                number.grid_remove()
            else:
                number.grid()

    '' '
    def clear(self):
        
        for entry in self.entry.values():
            entry.destroy()
            del entry
        self.entry = {}
        self.number = {}
        self.row_spin.insert(0,10)
        self.column_spin.insert(0,3)
        self.resize()
    '' '


    def change_width(self):
        try:
            width_val = int(self.cell_width.get())
        except:
            width_val = 10
        for entry in self.entry.values():
            entry.configure(width=width_val)

    def move_focus(self, event, target):
        (i,j) = target
        try:
            row = int(float(self.row_spin.get()))
        except:
            row = 10
        try:
            column = int(float(self.column_spin.get()))
        except:
            column=3

        if (i>=0 and i<=row and j>=1 and j<=column):
            self.entry[(i,j)].focus()
            self.entry[(i,j)].icursor("end")

    def open(self):
        pass

    def confirm(self):
        
        self.show("view")

    def group_name(self, j):
        s = ""
        while j>0:
            j = j - 1
            s = chr(j%26+65) + s
            j = j // 26
        return s

    def confirm(self):
        try:
            row = int(float(self.row_spin.get()))
        except:
            row = 10
        try:
            column = int(float(self.column_spin.get()))
        except:
            column = 3

        self.model.group = []
        self.model.data = []
        for j in range(column):
            temp_group=[]
            for i in range(row):
                if self.entry[(i+1,j+1)].get():
                    try:
                        temp_group.append(float(self.entry[(i+1,j+1)].get()))
                    except:
                        messagebox.showerror(
                            title="Error",
                            message=(
                                'Invalid input "{}" at ({}, {}).'.format(self.entry[(i+1,j+1)].get(),i+1,j+1)
                            )
                        )
                        return
            if len(temp_group)>0:
                self.model.data.append(np.array(temp_group))
                self.model.group.append(self.entry[(0,j+1)].get())
        self.tree_update()
        self.show("view")

    def tree_update(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree.config(column=())

        geometry = self.winfo_toplevel().geometry()
        self.winfo_toplevel().geometry(geometry)

        column = len(self.model.group)
        row = 1
        try:
            precision = int(float(self.precision.get()))
        except:
            precision = 1
        width = [100]*column
        notation = self.scientific.get()

        self.tree.config(column=tuple(range(1,column+1)))
        self.tree.column("#0", minwidth=0, stretch="no")
        self.tree.heading("#0", text="Label", anchor="center")

        for i in range(column):
            #self.tree.column(i+1, anchor="center", minwidth=0, width=100, stretch="no")
            temp = self.model.group[i]
            self.tree.column(i+1, anchor="center", minwidth=100)
            self.tree.heading(i+1, text=temp, anchor="center")
            #row = max(row, len(self.model.data[i]))
            width[i] = max(width[i],len(temp)*10)

        for i in range(row):
            value = []
            for j in range(column):
                try:
                    if notation == 1:
                        temp = format(round(self.model.mean[j],precision), '.{}E'.format(precision))
                    else:
                        temp = format(round(self.model.mean[j],precision), '.{}f'.format(precision))
                    value.append(temp)
                    width[j] = max(width[j],len(temp)*10)
                except:
                    value.append("")
            self.tree.insert(
                parent='' , index="end", iid=i, values=value
            )

        for i in range(column):
            self.tree.column(i+1, minwidth=width[i])




