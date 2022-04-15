import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd

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
        self.rowconfigure(index=3, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.configure(padding=(20,20))

        # Setting Bar
        self.setting_bar = ttk.Frame(self)
        self.setting_bar.grid(
            row=0, column=0, sticky="nsew"
        )
        self.setting_bar.columnconfigure(index=2, weight=1)

        self.percent_label = ttk.Label(self.setting_bar, text="Percentile(%)")
        self.percent_label.grid(
            row=0, column=0, padx=(5,0), pady=5, sticky="nsew"
        )

        self.percent_spin = ttk.Spinbox(
            self.setting_bar, from_=1, to=99, increment=1, width=5, command=self.tree_update
        )
        self.percent_spin.set(88)
        self.percent_spin.grid(
            row=0, column=1, padx=5, pady=5, sticky="nsew"
        )

        # Treeview
        self.treeview = ttk.Frame(self)
        self.treeview.grid(
            row=1, column=0, sticky="nsew"
        )
        self.treeview.rowconfigure(index=0, weight=1)
        self.treeview.columnconfigure(index=0, weight=1)

        self.scrollbar_1y = ttk.Scrollbar(self.treeview, orient="vertical")
        self.scrollbar_1y.grid(row=0, column=1, padx=(0,5), sticky="nsew")
        self.scrollbar_1x = ttk.Scrollbar(self.treeview, orient="horizontal")
        self.scrollbar_1x.grid(row=1, column=0, padx=(5,0), sticky="nsew")

        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=30)
        
        self.tree = ttk.Treeview(
            self.treeview, selectmode="none", height=14
        )
        self.tree.config(column=(1))
        self.tree.grid(row=0, column=0, padx=(5,0), sticky="nsew")

        self.tree.config(yscrollcommand=self.scrollbar_1y.set)
        self.scrollbar_1y.config(command=self.tree.yview)
        self.tree.config(xscrollcommand=self.scrollbar_1x.set)
        self.scrollbar_1x.config(command=self.tree.xview)
        
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column(1, anchor="center")

        self.tree.heading("#0", text="Label", anchor="center")
        self.tree.heading(1, text="", anchor="center")

        self.open_state = {}

        # Control Bar
        self.control_bar = ttk.Frame(self)
        self.control_bar.grid(
           row=2, column=0, sticky="nsew"
        )
        self.control_bar.columnconfigure(index=1, weight=1)

        self.scientific = tk.IntVar()
        self.notation = ttk.Checkbutton(
            self.control_bar, text="Scientific", style="Switch.TCheckbutton"
        )
        self.notation.config(
            variable=self.scientific, command=self.tree_update
        )
        self.notation.grid(
            row=0, column=0, padx=5, pady=5, sticky="nsew"
        )

        self.precision_label = ttk.Label(
            self.control_bar, text="Precision"
        )
        self.precision_label.grid(
            row=0, column=2, pady=5, sticky="nsew"
        )


        self.precision = ttk.Spinbox(
            self.control_bar, from_=1, to=99, increment=1, width=5, command=self.tree_update
        )
        self.precision.insert(0,1)
        self.precision.grid(
            row=0, column=3, padx=(5,15), pady=5, sticky="nsew"
        )

        # Shortcut
        self.bind("<Control-s>", lambda event: self.save())

        # Save
        self.save_button = ttk.Button(self, text="Save")
        self.save_button.config(command=self.save)
        self.save_button.grid(
            row=4, column=0, sticky="e"
        )

    def tree_update(self):

        # Keep State
        if "mean" in self.open_state:
            self.open_state["mean"] = self.tree.item(self.mean_iid, "open")
            self.open_state["med"] = self.tree.item(self.med_iid, "open")
            self.open_state["var"] = self.tree.item(self.var_iid, "open")
            self.open_state["std"] = self.tree.item(self.std_iid, "open")
        else:
            self.open_state["mean"] = 0
            self.open_state["med"] = 1
            self.open_state["var"] = 0
            self.open_state["std"] = 0
    
        # Clear
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree.config(column=())

        # Initialize
        column = len(self.model.group)
        try:
            precision = int(float(self.precision.get()))
        except:
            precision = 1
        width = [100]*column
        notation = self.scientific.get()

        self.tree.config(column=tuple(range(1,column+1)))
        self.tree.column("#0", anchor="center", minwidth=200, width=200, stretch="yes")
        self.tree.heading("#0", text="Statistic", anchor="center")

        for i in range(column):
            temp = self.model.group[i]
            self.tree.column(i+1, anchor="center", minwidth=100)
            self.tree.heading(i+1, text=temp, anchor="center")
            width[i] = max(width[i],len(temp)*10)

        cnt = 0

        # Sample Size
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
        cnt += 1
            
        # Mean
        value = []
        for i in range(column):
            if self.model.mean[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    temp = format(round(self.model.mean[i],precision), '.{}E'.format(precision))
                else:
                    temp = format(round(self.model.mean[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="Mean", values=tuple(value)
        )
        if self.open_state["mean"] == 1:
            self.tree.item(cnt, open=True)
        self.mean_iid = cnt
        cnt += 1

        self.tree.insert(
            parent=self.mean_iid, index="end", iid=cnt, text="Arithmetic Mean", values=tuple(value)
        )
        cnt += 1

        # Geometric Mean
        value = []
        for i in range(column):
            if self.model.gmean[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    temp = format(round(self.model.gmean[i],precision), '.{}E'.format(precision))
                else:
                    temp = format(round(self.model.gmean[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent=self.mean_iid, index="end", iid=cnt, text="Geometric Mean", values=tuple(value)
        )
        cnt += 1

        # Median
        value = []
        for i in range(column):
            if self.model.median[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    temp = format(round(self.model.median[i],precision), '.{}E'.format(precision))
                else:
                    temp = format(round(self.model.median[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="Median", values=tuple(value)
        )
        if self.open_state["med"] == 1:
            self.tree.item(cnt, open=True)
        self.med_iid = cnt
        cnt += 1

        # Minimum
        value = []
        for i in range(column):
            if self.model.min[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    temp = format(round(self.model.min[i],precision), '.{}E'.format(precision))
                else:
                    temp = format(round(self.model.min[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent=self.med_iid, index="end", iid=cnt, text="Minimum", values=tuple(value)
        )
        cnt += 1

        # Maximum
        value = []
        for i in range(column):
            if self.model.max[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    temp = format(round(self.model.max[i],precision), '.{}E'.format(precision))
                else:
                    temp = format(round(self.model.max[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent=self.med_iid, index="end", iid=cnt, text="Maximum", values=tuple(value)
        )
        cnt += 1

        # Range
        value = []
        for i in range(column):
            if self.model.range[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    temp = format(round(self.model.range[i],precision), '.{}E'.format(precision))
                else:
                    temp = format(round(self.model.range[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent=self.med_iid, index="end", iid=cnt, text="Range", values=tuple(value)
        )
        cnt += 1

        # Percentile
        try:
            percent = int(float(self.percent_spin.get()))
        except:
            percent = 88

        self.model.percent_cal(percent)

        value = []
        for i in range(column):
            if self.model.percent[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    temp = format(round(self.model.percent[i],precision), '.{}E'.format(precision))
                else:
                    temp = format(round(self.model.percent[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent=self.med_iid, index="end", iid=cnt, text="{}th Percentile".format(percent), values=tuple(value)
        )
        cnt += 1

        # Variance
        value = []
        for i in range(column):
            if self.model.var[i] == "-":
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
        if self.open_state["var"] == 1:
            self.tree.item(cnt, open=True)
        self.var_iid = cnt
        cnt += 1

        self.tree.insert(
            parent=self.var_iid, index="end", iid=cnt, text="Sample Variance", values=tuple(value)
        )
        cnt += 1

        # Population Variance
        value = []
        for i in range(column):
            if self.model.var[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    temp = format(round(self.model.pvar[i],precision), '.{}E'.format(precision))
                else:
                    temp = format(round(self.model.pvar[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent=self.var_iid, index="end", iid=cnt, text="Population Variance", values=tuple(value)
        )
        cnt += 1

        # Standard Deviation
        value = []
        for i in range(column):
            if self.model.std[i] == "-":
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
        if self.open_state["std"] == 1:
            self.tree.item(cnt, open=True)
        self.std_iid = cnt
        cnt += 1

        self.tree.insert(
            parent=self.std_iid, index="end", iid=cnt, text="Sample Std.", values=tuple(value)
        )
        cnt += 1

        # Popular Standard Deviation
        value = []
        for i in range(column):
            if self.model.std[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    temp = format(round(self.model.pstd[i],precision), '.{}E'.format(precision))
                else:
                    temp = format(round(self.model.pstd[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent=self.std_iid, index="end", iid=cnt, text="Population Std.", values=tuple(value)
        )
        cnt += 1

        # Coefficient of Variation
        value = []
        for i in range(column):
            if self.model.CV[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    temp = format(round(self.model.CV[i],precision), '.{}E'.format(precision))
                else:
                    temp = format(round(self.model.CV[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="Coefficient of Variation", values=tuple(value)
        )
        cnt += 1

        self.max_row = cnt


        # Resize Column
        for i in range(column):
            self.tree.column(i+1, minwidth=width[i])

    def save(self):
        filename = filedialog.asksaveasfilename(
            title="Save File", 
            filetypes=[("Excel File", "*.xlsx"), ("All Files", "*")],
            initialfile="Results"
        )
        if filename:
            try:
                group = ["Statistic"] + self.model.group
                data = []
                for i in range(self.max_row):
                    row = [self.tree.item(i, "text")] + list(self.tree.item(i, "values"))
                    data.append(row)
                df = pd.DataFrame(data, columns=group)
                df.to_excel(filename, index=False, sheet_name="Data")

            except:
                messagebox.showerror(
                    title="Error",
                    message="File could not be saved."
                )       
