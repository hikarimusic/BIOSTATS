import tkinter as tk
from tkinter import ttk

from .widget import Tree, Option
from . import model

class Test(ttk.Frame):

    def __init__(self, parent, master):
        
        # Initialize
        ttk.Frame.__init__(self, parent)
        self.master = master

        # Variable
        self.test_type = ["", "Basic", "t-Test", "ANOVA", "Exact Test", "Chi-Square Test", "Linear Regression", "Logistic Regression", "Nonparametric"]
        self.test_list = {
            "Basic"               : ["", "Numeral", "Numeral (Grouped)", "Categorical", "Contingency"] ,
            "t-Test"              : ["", "One-Sample t-Test", "Two-Sample t-Test", "Paired t-Test", "Pairwise t-Test"] ,
            "ANOVA"               : ["", "One-Way ANOVA", "Two-Way ANOVA", "One-Way ANCOVA", "Two-Way ANCOVA", "Multivariate ANOVA", "Repeated Measures ANOVA"] ,
            "Exact Test"          : ["", "Binomial Test", "Fisher's Exact Test"] ,
            "Chi-Square Test"     : ["", "Chi-Square Test", "Chi-Square Test (Fit)"] ,
            "Linear Regression"   : ["", "Simple Linear Regression"] ,
            "Logistic Regression" : ["", "Simple Logistic Regression"] ,
            "Nonparametric"       : ["", "Kruskal-Wallis Test"]
        }
        self.test_1 = tk.StringVar(value="Basic")
        self.test_2 = {}
        for t in self.test_list:
            self.test_2[t] = tk.StringVar(value=self.test_list[t][1])

        # Setup
        self.setup()

    def setup(self):

        # Configure
        self.rowconfigure(index=2, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.configure(padding=(10,10))

        # Frame
        self.menu_frame = ttk.Frame(self)
        self.menu_frame.grid(row=0, column=0, sticky="nsew")
        self.menu_frame.columnconfigure(index=2, weight=1)

        self.option_frame = ttk.Frame(self)
        self.option_frame.grid(row=1, column=0, sticky="nsew")
        self.option_frame.columnconfigure(index=1, weight=1)

        self.result_frame = ttk.Frame(self)
        self.result_frame.grid(row=2, column=0, sticky="nsew")
        self.result_frame.columnconfigure(index=0, weight=1)
        self.result_frame.rowconfigure(index=4, weight=1)

        self.save_button = ttk.Button(self, text="Save")
        self.save_button.config(command=self.save)
        self.save_button.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        # Menu
        self.menu_1 = ttk.OptionMenu(
            self.menu_frame, self.test_1, *self.test_type, command=lambda e: self.test_change()
        )
        self.menu_1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.menu_2 = {}
        for t in self.test_list:
            self.menu_2[t] = ttk.OptionMenu(
                self.menu_frame, self.test_2[t], *self.test_list[t], command=lambda e: self.test_change()
            )
            self.menu_2[t].grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
            self.menu_2[t].grid_remove()

        # Option
        self.option_label = {}
        self.option = {}
        for i in range(4):
            self.option_label[i] = ttk.Label(self.option_frame)
            self.option_label[i].grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
            self.option[i] = Option(self.option_frame, self)
            self.option[i].grid(row=i, column=1, sticky="nsew")

        # Result
        self.result = {}
        for i in range(3):
            self.result[i] = Tree(self.result_frame, 1)
            self.result[i].grid(row=i, column=0, padx=5, pady=5, sticky="nsew")



        self.test_change()


    def save(self):
        pass

    def test_change(self):

        for wid in self.menu_2.values():
            wid.grid_remove()
        for wid in self.option_label.values():
            wid.grid_remove()
        for wid in self.option.values():
            wid.grid_remove()
        for wid in self.result.values():
            wid.grid_remove()

        kind = self.test_1.get()
        test = self.test_2[kind].get()

        self.menu_2[kind].grid()

        if kind == "Basic":

            if test == "Numeral":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data_col["num"])
                self.option[0].grid()
            
            if test == "Numeral (Grouped)":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Group:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()

            if test == "Categorical":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["cat"])
                self.option[0].grid()

            if test == "Contingency":
                self.option_label[0].config(text="Variable 1:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["cat"])
                self.option[0].grid()

                self.option_label[1].config(text="Variable 2:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()   

                self.option_label[2].config(text="Kind:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(["Count", "Vertical", "Horizontal", "Overall"])
                self.option[2].grid()

        if kind == "t-Test":

            if test == "One-Sample t-Test":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Expect:")
                self.option_label[1].grid()
                self.option[1].entry_one_set(0, 6)
                self.option[1].grid()

                self.option_label[2].config(text="Type:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(["Two-Side", "Greater", "Less"])
                self.option[2].grid()

            
            if test == "Two-Sample t-Test":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Between:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()            

                self.option_label[2].config(text="Group:")
                self.option_label[2].grid()
                self.option[2].check_two_set([])
                self.option[2].grid()      

                self.option_label[3].config(text="Type:")
                self.option_label[3].grid()
                self.option[3].radio_one_set(["Equal Variances", "Unequal Variances"])
                self.option[3].grid()

                self.temp = ""

            if test == "Paired t-Test":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Between:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()            

                self.option_label[2].config(text="Group:")
                self.option_label[2].grid()
                self.option[2].check_two_set([])
                self.option[2].grid()   

                self.option_label[3].config(text="Pair:")
                self.option_label[3].grid()
                self.option[3].radio_one_set(self.master.data_col["cat"])
                self.option[3].grid()

                self.temp = ""
            
            if test == "Pairwise t-Test":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Between:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()

        if kind == "ANOVA":

            if test == "One-Way ANOVA":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Between:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()

            if test == "Two-Way ANOVA":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Between 1:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()
    
                self.option_label[2].config(text="Between 2:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["cat"])
                self.option[2].grid()

            if test == "One-Way ANCOVA":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Between:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()
    
                self.option_label[2].config(text="Covariable:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["num"])
                self.option[2].grid()

            if test == "Two-Way ANCOVA":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Between 1:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()
    
                self.option_label[2].config(text="Between 2:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["cat"])
                self.option[2].grid()

                self.option_label[3].config(text="Covariable:")
                self.option_label[3].grid()
                self.option[3].radio_one_set(self.master.data_col["num"])
                self.option[3].grid()

            if test == "Multivariate ANOVA":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Between:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()

            if test == "Repeated Measures ANOVA":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Between:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()

                self.option_label[2].config(text="Subject:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["cat"])
                self.option[2].grid()

        if kind == "Exact Test":

            if test == "Binomial Test":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["cat"])
                self.option[0].grid()

                self.option_label[1].config(text="Expect:")
                self.option_label[1].grid()
                self.option[1].entry_more_set([], [], 6)
                self.option[1].grid()

                self.temp = ""

            if test == "Fisher's Exact Test":
                self.option_label[0].config(text="Variable 1:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["cat"])
                self.option[0].grid()

                self.option_label[1].config(text="Variable 2:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()   

        if kind == "Chi-Square Test":

            if test == "Chi-Square Test":
                self.option_label[0].config(text="Variable 1:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["cat"])
                self.option[0].grid()

                self.option_label[1].config(text="Variable 2:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()   

            if test == "Chi-Square Test (Fit)":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["cat"])
                self.option[0].grid()

                self.option_label[1].config(text="Expect:")
                self.option_label[1].grid()
                self.option[1].entry_more_set([], [], 6)
                self.option[1].grid()

                self.temp = ""

        if kind == "Linear Regression":

            if test == "Simple Linear Regression":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["num"])
                self.option[1].grid()

        if kind == "Logistic Regression":

            if test == "Simple Logistic Regression":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()

                self.option_label[2].config(text="Target:")
                self.option_label[2].grid()
                self.option[2].radio_one_set([])
                self.option[2].grid()

                self.temp = ""

        if kind == "Nonparametric":

            if test == "Kruskal-Wallis Test":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Between:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()

        self.change()

    def change(self):

        for wid in self.result.values():
            wid.grid_remove()

        kind = self.test_1.get()
        test = self.test_2[kind].get()

        if kind == "Basic":

            if test == "Numeral":
                variable = self.option[0].check_more_get()
                if len(variable) == 0:
                    return
                
                result = model.numeral(self.master.data, variable=variable)
                self.result[0].data = result
                self.result[0].set(20)
                self.result[0].grid()
            
            if test == "Numeral (Grouped)":
                variable = self.option[0].radio_one_get()
                group = self.option[1].radio_one_get()

                if not variable:
                    return
                if not group:
                    return
                
                result = model.numeral_grouped(self.master.data, variable=variable, group=group)
                self.result[0].data = result
                self.result[0].set(18)
                self.result[0].grid()  

            if test == "Categorical":
                variable = self.option[0].radio_one_get()
                if not variable:
                    return
                
                result = model.categorical(self.master.data, variable=variable)
                self.result[0].data = result
                self.result[0].set(20)
                self.result[0].grid()
            
            if test == "Contingency":
                variable_1 = self.option[0].radio_one_get()
                variable_2 = self.option[1].radio_one_get()
                kind = self.option[2].radio_one_get()

                if not variable_1:
                    return
                if not variable_2:
                    return
                if not kind:
                    return

                result = model.contingency(self.master.data, variable_1=variable_1, variable_2=variable_2, kind=kind)
                self.result[0].data = result
                self.result[0].set(17)
                self.result[0].grid()

        if kind == "t-Test":

            if test == "One-Sample t-Test":
                variable = self.option[0].radio_one_get()
                expect = self.option[1].entry_one_get()
                _kind = self.option[2].radio_one_get()

                if not variable:
                    return
                try:
                    expect = float(expect)
                except:
                    return
                if not _kind:
                    return

                summary, result = model.one_sample_t_test(self.master.data, variable=variable, expect=expect, kind=_kind.lower())
                
                self.result[0].data = summary
                self.result[0].set(3)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(3)
                self.result[1].grid()
        
            if test == "Two-Sample t-Test":
                variable = self.option[0].radio_one_get()
                if not variable:
                    return

                between = self.option[1].radio_one_get()
                if not between:
                    return

                if between != self.temp:
                    opt = self.master.data[between].dropna().unique().tolist()
                    self.option[2].check_two_set(opt)
                self.temp = between

                group = self.option[2].check_two_get()
                if not group:
                    return
                
                _kind = self.option[3].radio_one_get()
                if not _kind:
                    return

                summary, result = model.two_sample_t_test(self.master.data, variable=variable, between=between, group=group, kind=_kind.lower())
                
                self.result[0].data = summary
                self.result[0].set(3)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(3)
                self.result[1].grid()

            if test == "Paired t-Test":
                variable = self.option[0].radio_one_get()
                if not variable:
                    return

                between = self.option[1].radio_one_get()
                if not between:
                    return

                if between != self.temp:
                    opt = self.master.data[between].dropna().unique().tolist()
                    self.option[2].check_two_set(opt)
                self.temp = between

                group = self.option[2].check_two_get()
                if not group:
                    return
                
                pair = self.option[3].radio_one_get()
                if not pair:
                    return

                summary, result = model.paired_t_test(self.master.data, variable=variable, between=between, group=group, pair=pair)
                
                self.result[0].data = summary
                self.result[0].set(3)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(3)
                self.result[1].grid()
            
            if test == "Pairwise t-Test":
                variable = self.option[0].radio_one_get()
                between = self.option[1].radio_one_get()

                if not variable:
                    return
                if not between:
                    return

                summary, result = model.pairwise_t_test(self.master.data, variable=variable, between=between)

                self.result[0].data = summary
                self.result[0].set(5)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(10)
                self.result[1].grid()  

        if kind == "ANOVA":

            if test == "One-Way ANOVA":
                variable = self.option[0].radio_one_get()
                between = self.option[1].radio_one_get()

                if not variable:
                    return
                if not between:
                    return

                summary, result = model.one_way_anova(self.master.data, variable=variable, between=between)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(3)
                self.result[1].grid()

            if test == "Two-Way ANOVA":
                variable = self.option[0].radio_one_get()
                between_1 = self.option[1].radio_one_get()
                between_2 = self.option[2].radio_one_get()

                if not variable:
                    return
                if not between_1:
                    return
                if not between_2:
                    return
                
                summary, result = model.two_way_anova(self.master.data, variable=variable, between_1=between_1, between_2=between_2)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(4)
                self.result[1].grid()

            if test == "One-Way ANCOVA":
                variable = self.option[0].radio_one_get()
                between = self.option[1].radio_one_get()
                covariable = self.option[2].radio_one_get()

                if not variable:
                    return
                if not between:
                    return
                if not covariable:
                    return

                summary, result = model.one_way_ancova(self.master.data, variable=variable, between=between, covariable=covariable)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(4)
                self.result[1].grid()

            if test == "Two-Way ANCOVA":
                variable = self.option[0].radio_one_get()
                between_1 = self.option[1].radio_one_get()
                between_2 = self.option[2].radio_one_get()
                covariable = self.option[3].radio_one_get()

                if not variable:
                    return
                if not between_1:
                    return
                if not between_2:
                    return
                if not covariable:
                    return
                
                summary, result = model.two_way_ancova(self.master.data, variable=variable, between_1=between_1, between_2=between_2, covariable=covariable)

                self.result[0].data = summary
                self.result[0].set(9)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(4)
                self.result[1].grid()

            if test == "Multivariate ANOVA":
                variable = self.option[0].check_more_get()
                between = self.option[1].radio_one_get()

                if len(variable) <= 1:
                    return
                if not between:
                    return

                summary, result = model.multivariate_anova(self.master.data, variable=variable, between=between)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(3)
                self.result[1].grid()

            if test == "Repeated Measures ANOVA":
                variable = self.option[0].radio_one_get()
                between = self.option[1].radio_one_get()
                subject = self.option[2].radio_one_get()

                if not variable:
                    return
                if not between:
                    return
                if not subject:
                    return

                summary, result = model.repeated_measures_anova(self.master.data, variable=variable, between=between, subject=subject)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(3)
                self.result[1].grid()

        if kind == "Exact Test":

            if test == "Binomial Test":
                variable = self.option[0].radio_one_get()

                if not variable:
                    return
                
                if variable != self.temp:
                    opt = self.master.data[variable].dropna().unique().tolist()
                    initial = [1 / len(opt)] * len(opt)
                    self.option[1].entry_more_set(opt, initial, 6)
                self.temp = variable

                expect = self.option[1].entry_more_get()

                try:
                    for i in expect:
                        expect[i] = float(expect[i])
                except:
                    return

                summary, result = model.binomial_test(self.master.data, variable=variable, expect=expect)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(3)
                self.result[1].grid()

            if test == "Fisher's Exact Test":
                variable_1 = self.option[0].radio_one_get()
                variable_2 = self.option[1].radio_one_get()

                if not variable_1:
                    return
                if not variable_2:
                    return

                summary, result = model.fisher_exact_test(self.master.data, variable_1=variable_1, variable_2=variable_2)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(3)
                self.result[1].grid()

        if kind == "Chi-Square Test":

            if test == "Chi-Square Test":
                variable_1 = self.option[0].radio_one_get()
                variable_2 = self.option[1].radio_one_get()

                if not variable_1:
                    return
                if not variable_2:
                    return

                summary, result = model.chi_square_test(self.master.data, variable_1=variable_1, variable_2=variable_2)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(3)
                self.result[1].grid()

            if test == "Chi-Square Test (Fit)":
                variable = self.option[0].radio_one_get()

                if not variable:
                    return
                
                if variable != self.temp:
                    opt = self.master.data[variable].dropna().unique().tolist()
                    initial = [1 / len(opt)] * len(opt)
                    self.option[1].entry_more_set(opt, initial, 6)
                self.temp = variable

                expect = self.option[1].entry_more_get()

                try:
                    for i in expect:
                        expect[i] = float(expect[i])
                except:
                    return

                summary, result = model.chi_square_test_fit(self.master.data, variable=variable, expect=expect)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(3)
                self.result[1].grid()

        if kind == "Linear Regression":

            if test == "Simple Linear Regression":
                x = self.option[0].radio_one_get()
                y = self.option[1].radio_one_get()

                if not x:
                    return
                if not y:
                    return

                summary, result = model.simple_linear_regression(self.master.data, x=x, y=y)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(3)
                self.result[1].grid()

        if kind == "Logistic Regression":

            if test == "Simple Logistic Regression":
                x = self.option[0].radio_one_get()
                y = self.option[1].radio_one_get()

                if not x:
                    return
                if not y:
                    return
                
                if y != self.temp:
                    self.option[2].radio_one_set(self.master.data[y].dropna().unique().tolist())
                self.temp = y
                
                target = self.option[2].radio_one_get()

                if not target:
                    return

                summary, result = model.simple_logistic_regression(self.master.data, x=x, y=y, target=target)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(3)
                self.result[1].grid()

        if kind == "Nonparametric":

            if test == "Kruskal-Wallis Test":
                variable = self.option[0].radio_one_get()
                between = self.option[1].radio_one_get()

                if not variable:
                    return
                if not between:
                    return

                summary, result = model.kruskal_wallis_test(self.master.data, variable=variable, between=between)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(3)
                self.result[1].grid()

        self.master.updating()
