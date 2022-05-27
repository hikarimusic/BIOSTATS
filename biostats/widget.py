import tkinter as tk
from tkinter import ttk
from click import command
import pandas as pd
from io import StringIO

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
        self.treeview.column("#0", anchor="center", minwidth=50, width=50)

        for i, col in enumerate(self.data.columns.tolist()):
            self.treeview.column(col, anchor="center", minwidth=100, width=100)
            self.treeview.heading(col, text=col, anchor="center")
            width[i] = max(width[i],len(col)*10)

        if len(self.data.columns) == 0 :
            self.treeview.config(columns=[1])
            self.treeview.column(1, anchor="center", minwidth=100, width=100)
            self.treeview.heading(1, text="", anchor="center")

        # Index
        index = self.data.index.tolist()
        width_id = 50

        # Data
        for i in range(len(self.data)):
            idd = str(index[i])
            width_id = max(width_id, len(idd)*10+30)
            value = []
            for j in range(len(self.data.columns)):
                col_type = str(self.data.dtypes[self.data.columns[j]])
                if pd.isna(self.data.iloc[i][j]):
                    temp = ""
                elif col_type == "float64":
                    if scientific == 1:
                        temp = format(round(self.data.iloc[i][j],precision), '.{}E'.format(precision))
                    else:
                        temp = format(round(self.data.iloc[i][j],precision), '.{}f'.format(precision))
                elif col_type == "Int64":
                    if scientific == 1:
                        temp = format(round(self.data.iloc[i][j],precision), '.{}E'.format(precision))
                    else:
                        temp = str(round(self.data.iloc[i][j]))
                else:
                    temp = str(self.data.iloc[i][j])
                value.append(temp)
                width[j] = max(width[j],len(temp)*10)
            self.treeview.insert(parent="", index="end", text=idd, values=value)
            
        self.treeview.column('#0', minwidth=width_id, width=width_id, stretch="no")
        for i, col in enumerate(self.data.columns.tolist()):
            self.treeview.column(col, minwidth=width[i])

        self.treeview.update()

    def set(self, height):

        self.treeview.config(height=height)


class Table(ttk.Frame):

    def __init__(self, parent, master):
        
        # Initialize
        ttk.Frame.__init__(self, parent)
        self.master = master

        # Variable
        self.row_num = 10
        self.col_num = 3
        self.cell_width = 10
        self.large = False

        self.setup()

    def setup(self):

        # Configure
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)

        # Border
        self.border = ttk.Frame(self, style="Card.TFrame", padding=(2,2))
        self.border.grid(row=0, column=0, sticky="nsew")
        self.border.rowconfigure(index=0, weight=1)
        self.border.columnconfigure(index=0, weight=1)

        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical")
        self.scrollbar_y.grid(row=0, column=1, sticky="nsew")
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal")
        self.scrollbar_x.grid(row=1, column=0, sticky="nsew")

        # Entry
        self.entry_canvas = tk.Canvas(self.border, highlightthickness=0)
        self.entry_canvas.grid(row=0, column=0, sticky="nsew")

        self.entry_frame = ttk.Frame(self.entry_canvas, padding=(0,10))
        self.entry_frame.grid(row=0, column=0)

        self.scrollbar_y.configure(command=self.entry_canvas.yview)
        self.scrollbar_x.configure(command=self.entry_canvas.xview)
        self.entry_frame.bind(
            "<Configure>",
            lambda e: self.entry_canvas.configure(
                scrollregion=self.entry_canvas.bbox("all")
            )
        )

        self.entry_canvas.create_window((0,0), window=self.entry_frame, anchor="nw")
        self.entry_canvas.configure(yscrollcommand=self.scrollbar_y.set)
        self.entry_canvas.configure(xscrollcommand=self.scrollbar_x.set)

        self.border.bind("<Enter>", lambda e: self.scroll_on())
        self.border.bind("<Leave>", lambda e: self.scroll_off())

        self.entry = {}
        self.number = {}

        ## Too Large
        self.too_large = ttk.Frame(self, style="Card.TFrame", padding=(2,2))
        self.too_large.grid(row=0, column=0, sticky="nsew")
        self.too_large.rowconfigure(index=0, weight=1)
        self.too_large.columnconfigure(index=0, weight=1)
        self.too_large_l = ttk.Label(self.too_large, text="The data is too large to be edited.")
        self.too_large_l.grid(row=0, column=0)

    def resize(self, row, col):
        
        self.row_num = row
        self.col_num = col

        if row * col > 300:
            self.large = True
            self.too_large.tkraise()
            return
        else:
            self.large = False
            self.border.tkraise()

        for i in range(1,row+1):
            for j in range(1,col+1):
                if not (i,j) in self.entry:
                    self.entry[(i,j)] = ttk.Entry(self.entry_frame, width=self.cell_width, justify="center")
                    self.entry[(i,j)].grid(row=i, column=j)
                    self.entry[(i,j)].bind("<Up>", lambda e, target=(i-1,j): self.move_focus(target))
                    self.entry[(i,j)].bind("<Down>", lambda e, target=(i+1,j): self.move_focus(target))
                    self.entry[(i,j)].bind("<Left>", lambda e, target=(i,j-1): self.move_focus(target))
                    self.entry[(i,j)].bind("<Right>", lambda e, target=(i,j+1): self.move_focus(target))
                    self.entry[(i,j)].bind("<Return>", lambda e: self.master.confirm())

        for i in range(1,row+1):
            if not i in self.number:
                self.number[i] = ttk.Label(self.entry_frame, text=i)
                self.number[i].grid(row=i, column=0, padx=5)

        for j in range(1,col+1):
            if not (0,j) in self.entry:
                self.entry[(0,j)] = ttk.Entry(self.entry_frame, width=self.cell_width, justify="center")
                self.entry[(0,j)].grid(row=0, column=j)
                self.entry[(0,j)].bind("<Down>", lambda e, target=(1,j): self.move_focus(target))
                self.entry[(0,j)].bind("<Left>", lambda e, target=(0,j-1): self.move_focus(target))
                self.entry[(0,j)].bind("<Right>", lambda e, target=(0,j+1): self.move_focus(target))
                self.entry[(0,j)].bind("<Return>", lambda e: self.master.confirm())

        for j in range(1,col+1):
            if not self.entry[(0,j)].get():
                self.entry[(0,j)].insert(0,"Variable "+self.group_name(j))

        for (i,j), entry in self.entry.items():
            if i>row or j>col:
                entry.grid_remove()
            else:
                entry.grid()

        for i, number in self.number.items():
            if i>row:
                number.grid_remove()
            else:
                number.grid()


    def change_width(self, wid):

        if self.large:
            return 

        self.cell_width = wid

        for entry in self.entry.values():
            entry.configure(width=wid)

    def data_save(self):

        if self.large:
            return True, 0
        
        str = ""
        for i in range(self.row_num+1):
            for j in range(1, self.col_num+1):
                str += self.entry[(i,j)].get() + ","
            str = str[:-1]
            str += '\n'
        df = pd.read_csv(StringIO(str), dtype=object)

        return False, df

    def data_write(self, data):

        row = len(data)
        col = len(data.columns)

        if row == 0:
            self.resize(10,3)
            return

        self.master.row_num.set(row)
        self.master.col_num.set(col)

        self.resize(row, col)

        if self.large:
            return

        for entry in self.entry.values():
            entry.delete(0,tk.END)

        for j in range(col):
            self.entry[(0,j+1)].insert(0, data.columns[j])
            col_type = str(data.dtypes[data.columns[j]])
            for i in range(row):
                if pd.isna(data.iloc[i][j]):
                    self.entry[(i+1,j+1)].insert(0, "")
                elif col_type == "Int64":
                    self.entry[(i+1,j+1)].insert(0, round(data.iloc[i][j]))
                else:
                    self.entry[(i+1,j+1)].insert(0, data.iloc[i][j])

    def move_focus(self, target):

        (i,j) = target
        if (i>=0 and i<=self.row_num and j>=1 and j<=self.col_num):
            self.entry[(i,j)].focus()
            self.entry[(i,j)].icursor("end")

    def scroll_on(self):

        # Linux 
        self.entry_canvas.bind_all('<4>', lambda e: self.entry_canvas.yview('scroll', -1, 'units'))
        self.entry_canvas.bind_all('<5>', lambda e: self.entry_canvas.yview('scroll', 1, 'units'))
        self.entry_canvas.bind_all('<Shift-4>', lambda e: self.entry_canvas.xview('scroll', -1, 'units'))
        self.entry_canvas.bind_all('<Shift-5>', lambda e: self.entry_canvas.xview('scroll', 1, 'units'))

    def scroll_off(self):

        self.entry_canvas.unbind_all('<4>')
        self.entry_canvas.unbind_all('<5>')
        self.entry_canvas.unbind_all('<Shift-4>')
        self.entry_canvas.unbind_all('<Shift-5>')

    def group_name(self, j):

        s = ""
        while j>0:
            j = j - 1
            s = chr(j%26+65) + s
            j = j // 26
        return s


class Option(ttk.Frame):

    def __init__(self, parent, master):
        
        # Initialize
        ttk.Frame.__init__(self, parent)
        self.master = master

        # Variable
        self.option = {}
        self.now = ""

        # Setup
        self.setup()

    def setup(self):

        # Configure
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)

        # Canvas
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient="horizontal")

        self.frame = ttk.Frame(self.canvas)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.scrollbar.configure(command=self.canvas.xview)
        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0,0), window=self.frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.bind("<Enter>", lambda e: self.scroll_on())
        self.bind("<Leave>", lambda e: self.scroll_off())
        


    def entry_one(self):
        pass

    def entry_more(self):
        pass

    def radio_one(self):
        pass

    def check_two(self):
        pass

    def check_more_set(self, opt):
        
        if self.now != "":
            self.option[self.now].grid_remove()

        self.now = "check_more"
        if "check_more" not in self.option:
            self.option["check_more"] = ttk.Frame(self.frame)
            self.option["check_more"].grid(row=0, column=0, sticky="nsew")
            self.check_more_item = {}
            self.check_more_var = {}
            self.check_more_dict = {}
        else:
            self.option["check_more"].grid()

        for i, var in enumerate(opt):
            if i not in self.check_more_item:
                self.check_more_var[i] = tk.IntVar()
                self.check_more_item[i] = ttk.Checkbutton(self.option["check_more"])
                self.check_more_item[i].config(variable=self.check_more_var[i], onvalue=1, offvalue=0)
                self.check_more_item[i].config(command=self.master.change)
                self.check_more_item[i].grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            self.check_more_item[i].config(text=var)
            self.check_more_var[i].set(0)
            self.check_more_dict[i] = var

        for i, wid in self.check_more_item.items():
            if i >= len(opt):
                wid.grid_remove()
            else:
                wid.grid()

        self.frame.update()
        self.canvas.config(height=self.frame.winfo_height())

    def check_more_get(self):

        temp = []
        for i, var in self.check_more_dict.items():
            if self.check_more_var[i].get() == 1:
                temp.append(var)
        
        return temp
        

    def scroll_on(self):

        self.scrollbar.update()
        (x,y) = self.scrollbar.get()
        if x == 0.0 and y == 1.0:
            return

        # Linux 
        self.canvas.bind_all('<Shift-4>', lambda e: self.canvas.xview('scroll', -1, 'units'))
        self.canvas.bind_all('<Shift-5>', lambda e: self.canvas.xview('scroll', 1, 'units'))

    def scroll_off(self):

        self.canvas.unbind_all('<Shift-4>')
        self.canvas.unbind_all('<Shift-5>')