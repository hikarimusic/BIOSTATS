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
        self.data_view.columnconfigure(index=4, weight=1)

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

        # Control Bar
        self.percent_label = ttk.Label(self.data_view, text="Percentile(%)")
        self.percent_label.grid(
            row=0, column=0, padx=(5,0), pady=5, sticky="nsew"
        )
        self.percent_spin = ttk.Spinbox(
            self.data_view, from_=1, to=99, increment=1, width=5, command=self.tree_update
        )
        self.percent_spin.insert(0,90)
        self.percent_spin.grid(
            row=0, column=1, padx=5, pady=5, sticky="nsew"
        )

        self.CI_label = ttk.Label(self.data_view, text="Confidence Level(%)")
        self.CI_label.grid(
            row=0, column=2, padx=(5,0), pady=5, sticky="nsew"
        )
        self.CI_spin = ttk.Spinbox(
            self.data_view, from_=1, to=99, increment=1, width=5, command=self.tree_update
        )
        self.CI_spin.insert(0,95)
        self.CI_spin.grid(
            row=0, column=3, padx=5, pady=5, sticky="nsew"
        )

        # Treeview
        self.scrollbar_1y = ttk.Scrollbar(self.data_view, orient="vertical")
        self.scrollbar_1y.grid(row=1, column=7, padx=(0,5), sticky="nsew")
        self.scrollbar_1x = ttk.Scrollbar(self.data_view, orient="horizontal")
        self.scrollbar_1x.grid(row=2, column=0, columnspan=7, padx=(5,0), sticky="nsew")

        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=30)
        
        self.tree = ttk.Treeview(
            self.data_view, selectmode="none", height=10
        )
        self.tree.config(column=(1))
        self.tree.grid(row=1, column=0, columnspan=7, padx=(5,0), sticky="nsew")

        self.tree.config(yscrollcommand=self.scrollbar_1y.set)
        self.scrollbar_1y.config(command=self.tree.yview)
        self.tree.config(xscrollcommand=self.scrollbar_1x.set)
        self.scrollbar_1x.config(command=self.tree.xview)
        
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column(1, anchor="center")

        self.tree.heading("#0", text="Label", anchor="center")
        self.tree.heading(1, text="", anchor="center")

        self.open_state = {}

        # Notation
        self.scientific = tk.IntVar()
        self.notation = ttk.Checkbutton(
            self.data_view, text="Scientific", style="Switch.TCheckbutton"
        )
        self.notation.config(
            variable=self.scientific, command=self.tree_update
        )
        self.notation.grid(
            row=3, column=0, columnspan=4, padx=5, pady=5, sticky="nsew"
        )

        # Precision
        self.precision_label = ttk.Label(
            self.data_view, text="Precision"
        )
        self.precision_label.grid(
            row=3, column=5, pady=5, sticky="nsew"
        )


        self.precision = ttk.Spinbox(
            self.data_view, from_=1, to=99, increment=1, width=5, command=self.tree_update
        )
        self.precision.insert(0,1)
        self.precision.grid(
            row=3, column=6, padx=(5,0), pady=5, sticky="nsew"
        )

    def tree_update(self):
        if "CI" in self.open_state:
            self.open_state["CI"] = self.tree.item(self.CI_iid, "open")
            self.open_state["per"] = self.tree.item(self.per_iid, "open")
        else:
            self.open_state["CI"] = 0
            self.open_state["per"] = 0
    
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree.config(column=())

        #geometry = self.winfo_toplevel().geometry()
        #self.winfo_toplevel().geometry(geometry)

        column = len(self.model.group)
        try:
            precision = int(float(self.precision.get()))
        except:
            precision = 1
        width = [100]*column
        notation = self.scientific.get()

        self.tree.config(column=tuple(range(1,column+1)))
        #self.tree.column("#0", anchor="center", minwidth=200)
        self.tree.column("#0", anchor="center", minwidth=200, width=200, stretch="yes")
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
        cnt += 1

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

        # Percentile
        try:
            percent = int(float(self.percent_spin.get()))
        except:
            percent = 95

        self.model.percent_cal(percent)

        value = []
        for i in range(column):
            if notation == 1:
                temp = format(round(self.model.percent[i],precision), '.{}E'.format(precision))
            else:
                temp = format(round(self.model.percent[i],precision), '.{}f'.format(precision))
            value.append(temp)
            width[i] = max(width[i],len(temp)*10)
        self.tree.insert(
            parent="", index="end", iid=cnt, text="{}th Percentile".format(percent), values=tuple(value)
        )
        if self.open_state["per"] == 1:
            self.tree.item(cnt, open=True)
        self.per_iid = cnt
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
            parent=self.per_iid, index="end", iid=cnt, text="Minimum", values=tuple(value)
        )
        cnt += 1

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
            parent=self.per_iid, index="end", iid=cnt, text="Maximum", values=tuple(value)
        )
        cnt += 1


        '''
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
        '''


        # Resize Column
        for i in range(column):
            self.tree.column(i+1, minwidth=width[i])


