import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd

from biostats.widget import Spin, Tree, Table

class Data(ttk.Frame):

    def __init__(self, parent, master):
        
        # Initialize
        ttk.Frame.__init__(self, parent)
        self.master = master

        # Variable
        self.row_num = tk.IntVar(value=10)
        self.col_num = tk.IntVar(value=3)
        self.cell_width = tk.IntVar(value=10)

        # Setup
        self.setup()

    def setup(self):

        # Configure
        self.rowconfigure(index=3, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.configure(padding=(10,10))

        # Edit, Open
        self.bar_view = ttk.Frame(self)
        self.bar_view.grid(row=0, column=0, sticky="nsew")
        self.bar_view.columnconfigure(index=2, weight=1)

        self.edit_button = ttk.Button(self.bar_view, text="Edit")
        self.edit_button.config(command=lambda: self.switch("edit"))
        self.edit_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.open_button = ttk.Button(self.bar_view, text="Open")
        self.open_button.config(command=self.open)
        self.open_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Tree
        self.tree = Tree(self, 20)
        self.tree.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Table
        self.table = Table(self, self)
        self.table.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.table.resize(self.row_num.get(), self.col_num.get())
        self.table.change_width(self.cell_width.get())
        
        # Row, Column, Confirm
        self.bar_edit = ttk.Frame(self)
        self.bar_edit.grid(row=0, column=0, sticky="nsew")
        self.bar_edit.columnconfigure(index=4, weight=1)

        self.row_label = ttk.Label(self.bar_edit, text="Row")
        self.row_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.row_spin = Spin(
            self.bar_edit, from_=1, to=999, increment=1, width=6, textvariable=self.row_num
        )
        self.row_spin.set_command(lambda : self.table.resize(self.row_num.get(), self.col_num.get()))
        self.row_spin.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.col_label = ttk.Label(self.bar_edit, text="Column")
        self.col_label.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.col_spin = Spin(
            self.bar_edit, from_=1, to=999, increment=1, width=6, textvariable=self.col_num
        )
        self.col_spin.set_command(lambda : self.table.resize(self.row_num.get(), self.col_num.get()))
        self.col_spin.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
        
        self.confirm_button = ttk.Button(self.bar_edit, text="Confirm", style="Accent.TButton")
        self.confirm_button.config(command=self.confirm)
        self.confirm_button.grid(row=0, column=5, padx=5, pady=5, sticky="e")

        # Cell Width
        self.cell_scale = ttk.Scale(self, from_=1, to=29)
        self.cell_scale.config(variable=self.cell_width, command=lambda e: self.table.change_width(self.cell_width.get()))
        self.cell_scale.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # Save
        self.save_button = ttk.Button(self, text="Save")
        self.save_button.config(command=self.save)
        self.save_button.grid(row=4, column=0, padx=5, pady=5, sticky="e")

        # Shortcut
        self.bind("<e>", lambda event: self.switch("edit"))
        self.bind("<o>", lambda event: self.open())
        self.bind("<Control-s>", lambda event: self.save())


        self.switch("view")


    def switch(self, key):

        if key == "view":
            self.bar_view.tkraise()
            self.tree.tkraise()
            self.cell_scale.grid_remove()
            self.update()
            self.focus()
        
        if key == "edit":
            self.bar_edit.tkraise()
            self.table.data_write(self.master.data)
            self.table.tkraise()
            self.cell_scale.grid()
            self.table.entry[(1,1)].focus()


    def open(self):

        filename = filedialog.askopenfilename(
            title="Open File", 
            filetypes=[
                ("All Files", "*"),
                ("Excel File", "*.xlsx"), 
                ("CSV File", "*.csv"), 
                ("JSON File", "*.json"),
                ("SAS File", "*.sas7bdat"),
                ("Stata File", "*.dta"),
                ("SPSS File", "*.sav")
            ]
        )
        if filename:
            try:
                if ".xlsx" in filename:
                    df = pd.read_excel(filename, dtype=object)
                elif ".csv" in filename:
                    df = pd.read_csv(filename, dtype=object)
                elif ".json" in filename:
                    df = pd.read_json(filename, dtype=object)
                elif ".sas7bdat" in filename:
                    df = pd.read_sas(filename)
                elif ".dta" in filename:
                    df = pd.read_stata(filename)
                elif ".sav" in filename:
                    df = pd.read_spss(filename)

                self.data_process(df)
                self.switch("view")

            except ValueError:
                messagebox.showerror(
                    title="Error",
                    message="File could not be opened."
                )

            except FileNotFoundError:
                messagebox.showerror(
                    title="Error",
                    message="File not found."
                )

    def confirm(self):

        large, df = self.table.data_save()
        if large == False:
            self.data_process(df)
        
        self.switch("view")

    def data_process(self, df):

        df = df.dropna(how="all")
        df = df.dropna(how="all", axis=1)
        df = df.reset_index(drop=True)
        df.index += 1

        col_num = []
        col_cat = []

        for col in df:
            try: 
                df[col] = df[col].astype('float64')
                col_num.append(col)
                try: 
                    df[col] = df[col].astype('Int64')
                    col_cat.append(col)
                except:
                    pass
            except:
                col_cat.append(col)


        df.columns = df.columns.map(str)
        df.index = df.index.map(str)

        self.master.data = df
        self.master.data_col["num"] = col_num
        self.master.data_col["cat"] = col_cat

        self.master.changed()
        

    def save(self):

        filename = filedialog.asksaveasfilename(
            title="Save File", 
            filetypes=[
                ("Excel File", "*.xlsx"), 
                ("CSV File", "*.csv"), 
                ("JSON File", "*.json"),
                ("Stata File", "*.dta"),
                ("LaTex File", "*.tex"),
                ("Markdown FIle", "*.md"),
                ("Text File", "*.txt"),
                ("All Files", "*")
            ],
            initialfile="Data"
        )
        if filename:
            try:
                df = self.tree.data
                if ".xlsx" in filename:
                    df.to_excel(filename, index=False)
                elif ".csv" in filename:
                    df.to_csv(filename, index=False)
                elif ".json" in filename:
                    with open(filename, 'w') as f:
                        f.write(df.to_json())
                elif ".dta" in filename:
                    df.to_stata(filename)
                elif ".tex" in filename:
                    with open(filename, 'w') as f:
                        f.write(df.to_latex(index=False))
                elif ".md" in filename:
                    with open(filename, 'w') as f:
                        f.write(df.to_markdown(index=False))
                else:
                    with open(filename, 'w') as f:
                        f.write(df.to_string(index=False))
            except:
                messagebox.showerror(
                    title="Error",
                    message="File could not be saved."
                )       

