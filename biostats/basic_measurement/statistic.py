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
            self.treeview, selectmode="none", height=10
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




        # Resize Column
        for i in range(column):
            self.tree.column(i+1, minwidth=width[i])


        '''
        # Standard Error
        value = []
        for i in range(column):
            if self.model.sem[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    temp = format(round(self.model.sem[i],precision), '.{}E'.format(precision))
                else:
                    temp = format(round(self.model.sem[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="Standard Error", values=tuple(value)
        )
        cnt += 1
        '''

        '''
        # Confidence Interval
        try:
            level = int(float(self.CI_spin.get()))
        except:
            level = 95

        self.model.CI_cal(level/100)

        # Two Tailed
        value = []
        CI_width = []
        for i in range(column):
            if self.model.CI_two[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    CI1 = format(round(self.model.CI_two[i][0],precision), '.{}E'.format(precision))
                    CI2 = format(round(self.model.CI_two[i][1],precision), '.{}E'.format(precision))
                    temp = "{}~{}".format(CI1, CI2)
                else:
                    CI1 = format(round(self.model.CI_two[i][0],precision), '.{}f'.format(precision))
                    CI2 = format(round(self.model.CI_two[i][1],precision), '.{}f'.format(precision))
                    temp = "{}~{}".format(CI1, CI2)
            value.append(temp)
            CI_width.append(len(temp))
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="{}% Confidence Interval".format(level), values=tuple(value)
        )
        if self.open_state["CI"] == 1:
            self.tree.item(cnt, open=True)
        self.CI_iid = cnt
        cnt += 1

        self.tree.insert(
            parent=self.CI_iid, index="end", iid=cnt, text="Two Tailed".format(level), values=tuple(value)
        )
        cnt += 1

        # One Tailed
        value = []
        for i in range(column):
            if self.model.CI_one_1[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    CI = format(round(self.model.CI_one_1[i],precision), '.{}E'.format(precision))
                    s = "{}~".format(CI)
                    temp = '{0: <{l}}'.format(s, l=CI_width[i]+1)
                else:
                    CI = format(round(self.model.CI_one_1[i],precision), '.{}f'.format(precision))
                    s = "{}~".format(CI)
                    temp = '{0: <{l}}'.format(s, l=CI_width[i]+1)
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent=self.CI_iid, index="end", iid=cnt, text="One Tailed".format(level), values=tuple(value)
        )
        cnt += 1

        value = []
        for i in range(column):
            if self.model.CI_one_2[i] == "-":
                temp = "-"
            else:
                if notation == 1:
                    CI = format(round(self.model.CI_one_2[i],precision), '.{}E'.format(precision))
                    s = "~{}".format(CI)
                    temp = '{0: >{l}}'.format(s, l=CI_width[i]+1)
                else:
                    CI = format(round(self.model.CI_one_2[i],precision), '.{}f'.format(precision))
                    s = "~{}".format(CI)
                    temp = '{0: >{l}}'.format(s, l=CI_width[i]+1)
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent=self.CI_iid, index="end", iid=cnt, text="One Tailed".format(level), values=tuple(value)
        )
        cnt += 1
        '''

        '''
        # 1st Quartile
        value = []
        for i in range(column):
            if notation == 1:
                temp = format(round(self.model.per_25[i],precision), '.{}E'.format(precision))
            else:
                temp = format(round(self.model.per_25[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent=self.per_iid, index="end", iid=cnt, text="1st Quartile", values=tuple(value)
        )
        cnt += 1

        # 2nd Quartile
        value = []
        for i in range(column):
            if notation == 1:
                temp = format(round(self.model.per_50[i],precision), '.{}E'.format(precision))
            else:
                temp = format(round(self.model.per_50[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent=self.per_iid, index="end", iid=cnt, text="2nd Quartile", values=tuple(value)
        )
        cnt += 1

        # 3rd Quartile
        value = []
        for i in range(column):
            if notation == 1:
                temp = format(round(self.model.per_75[i],precision), '.{}E'.format(precision))
            else:
                temp = format(round(self.model.per_75[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent=self.per_iid, index="end", iid=cnt, text="3rd Quartile", values=tuple(value)
        )
        cnt += 1
        '''



