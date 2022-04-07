import tkinter as tk
from tkinter import ttk

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

        '''
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
        '''

        # Treeview
        self.scrollbar_1y = ttk.Scrollbar(self.data_view, orient="vertical")
        self.scrollbar_1y.grid(row=1, column=5, padx=(0,5), sticky="nsew")
        self.scrollbar_1x = ttk.Scrollbar(self.data_view, orient="horizontal")
        self.scrollbar_1x.grid(row=2, column=0, columnspan=5, padx=(5,0), sticky="nsew")

        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=30)
        
        self.tree = ttk.Treeview(
            self.data_view, selectmode="none", height=10
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

    def tree_update(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree.config(column=())

        geometry = self.winfo_toplevel().geometry()
        self.winfo_toplevel().geometry(geometry)

        column = len(self.model.group)
        try:
            precision = int(float(self.precision.get()))
        except:
            precision = 1
        width = [100]*column
        notation = self.scientific.get()

        self.tree.config(column=tuple(range(1,column+1)))
        self.tree.column("#0", anchor="center", minwidth=180, stretch="yes")
        self.tree.heading("#0", text="Statistic", anchor="center")

        for i in range(column):
            #self.tree.column(i+1, anchor="center", minwidth=0, width=100, stretch="no")
            temp = self.model.group[i]
            self.tree.column(i+1, anchor="center", minwidth=100)
            self.tree.heading(i+1, text=temp, anchor="center")
            width[i] = max(width[i],len(temp)*10)

        cnt = 0

        # Sample Size
        value = []
        for i in range(column):
            if notation == 1:
                temp = format(round(self.model.size[i],precision), '.{}E'.format(precision))
            else:
                temp = str(self.model.size[i])
                #temp = format(round(self.model.mean[i],0), '.{}f'.format())
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="Sample Size", values=tuple(value)
        )
        cnt += 1
            
        # Mean
        value = []
        for i in range(column):
            if notation == 1:
                temp = format(round(self.model.mean[i],precision), '.{}E'.format(precision))
            else:
                temp = format(round(self.model.mean[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="Mean", values=tuple(value)
        )
        cnt += 1

        # Median
        value = []
        for i in range(column):
            if notation == 1:
                temp = format(round(self.model.median[i],precision), '.{}E'.format(precision))
            else:
                temp = format(round(self.model.median[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="Median", values=tuple(value)
        )
        cnt += 1

        # Standard Deviation
        value = []
        for i in range(column):
            if self.model.std[i] == "N.A.":
                temp = "-"
            else:
                if notation == 1:
                    temp = format(round(self.model.std[i],precision), '.{}E'.format(precision))
                else:
                    temp = format(round(self.model.std[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="Standard Deviation", values=tuple(value)
        )
        cnt += 1

        # Variance
        value = []
        for i in range(column):
            if self.model.var[i] == "N.A.":
                temp = "-"
            else:
                if notation == 1:
                    temp = format(round(self.model.var[i],precision), '.{}E'.format(precision))
                else:
                    temp = format(round(self.model.var[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="Variance", values=tuple(value)
        )
        cnt += 1

        # Range
        value = []
        for i in range(column):
            if notation == 1:
                temp = format(round(self.model.range[i],precision), '.{}E'.format(precision))
            else:
                temp = format(round(self.model.range[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="Range", values=tuple(value)
        )
        cnt += 1

        # Minimum
        value = []
        for i in range(column):
            if notation == 1:
                temp = format(round(self.model.min[i],precision), '.{}E'.format(precision))
            else:
                temp = format(round(self.model.min[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="Minimum", values=tuple(value)
        )
        cnt += 1

        # Maximum
        value = []
        for i in range(column):
            if notation == 1:
                temp = format(round(self.model.max[i],precision), '.{}E'.format(precision))
            else:
                temp = format(round(self.model.max[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="Maximum", values=tuple(value)
        )
        cnt += 1


        for i in range(column):
            self.tree.column(i+1, minwidth=width[i])
