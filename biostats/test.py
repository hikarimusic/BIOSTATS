import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd

from biostats.widget import Tree, Option
from biostats import model

class Test(ttk.Frame):

    def __init__(self, parent, master):
        
        # Initialize
        ttk.Frame.__init__(self, parent)
        self.master = master

        # Variable
        self.test_type = ["", "Basic", "t-Test", "ANOVA", "Exact Test", "Chi-Square Test", "Linear Regression", "Logistic Regression", "Nonparametric", "Others"]
        self.test_list = {
            "Basic"               : ["", "Numeral", "Numeral (Grouped)", "Categorical", "Contingency"] ,
            "t-Test"              : ["", "One-Sample t-Test", "Two-Sample t-Test", "Paired t-Test", "Pairwise t-Test"] ,
            "ANOVA"               : ["", "One-Way ANOVA", "Two-Way ANOVA", "One-Way ANCOVA", "Two-Way ANCOVA", "Multivariate ANOVA", "Repeated Measures ANOVA"] ,
            "Exact Test"          : ["", "Binomial Test", "Fisher's Exact Test", "McNemar's Exact Test"] ,
            "Chi-Square Test"     : ["", "Chi-Square Test", "Chi-Square Test (Fit)", "McNemar's Test", "Mantel-Haenszel Test"] ,
            "Linear Regression"   : ["", "Correlation", "Correlation Matrix", "Simple Linear Regression", "Multiple Linear Regression"] ,
            "Logistic Regression" : ["", "Simple Logistic Regression", "Multiple Logistic Regression", "Ordered Logistic Regression", "Multinomial Logistic Regression"] ,
            "Nonparametric"       : ["", "Median Test", "Sign Test", "Wilcoxon Signed-Rank Test", "Wilcoxon Rank-Sum Test", "Kruskal-Wallis Test", "Friedman Test", "Spearman's Rank Correlation"] ,
            "Others"              : ["", "Screening Test", "Epidemiologic Study", "Factor Analysis", "Principal Component Analysis", "Linear Discriminant Analysis"]
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

        # Shortcut
        self.bind("<Control-s>", lambda event: self.save())

        
        self.test_change()


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

            if test == "McNemar's Exact Test":
                self.option_label[0].config(text="Variable 1:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["cat"])
                self.option[0].grid()

                self.option_label[1].config(text="Variable 2:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()

                self.option_label[2].config(text="Pair:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["cat"])
                self.option[2].grid()

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
            
            if test == "McNemar's Test":
                self.option_label[0].config(text="Variable 1:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["cat"])
                self.option[0].grid()

                self.option_label[1].config(text="Variable 2:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()

                self.option_label[2].config(text="Pair:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["cat"])
                self.option[2].grid()

            if test == "Mantel-Haenszel Test":
                self.option_label[0].config(text="Variable 1:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["cat"])
                self.option[0].grid()

                self.option_label[1].config(text="Variable 2:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()

                self.option_label[2].config(text="Stratum:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["cat"])
                self.option[2].grid()   

        if kind == "Linear Regression":

            if test == "Correlation":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["num"])
                self.option[1].grid()

            if test == "Correlation Matrix":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data_col["num"])
                self.option[0].grid()

            if test == "Simple Linear Regression":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["num"])
                self.option[1].grid()

            if test == "Multiple Linear Regression":
                self.option_label[0].config(text="X (nominal):")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="X (categorical):")
                self.option_label[1].grid()
                self.option[1].check_more_set(self.master.data_col["cat"])
                self.option[1].grid()
            
                self.option_label[2].config(text="Y:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["num"])
                self.option[2].grid()

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

            if test == "Multiple Logistic Regression":
                self.option_label[0].config(text="X (nominal):")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="X (categorical):")
                self.option_label[1].grid()
                self.option[1].check_more_set(self.master.data_col["cat"])
                self.option[1].grid()

                self.option_label[2].config(text="Y:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["cat"])
                self.option[2].grid()

                self.option_label[3].config(text="Target:")
                self.option_label[3].grid()
                self.option[3].radio_one_set([])
                self.option[3].grid()

                self.temp = ""
            
            if test == "Ordered Logistic Regression":
                self.option_label[0].config(text="X (nominal):")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="X (categorical):")
                self.option_label[1].grid()
                self.option[1].check_more_set(self.master.data_col["cat"])
                self.option[1].grid()

                self.option_label[2].config(text="Y:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["cat"])
                self.option[2].grid()

                self.option_label[3].config(text="Order:")
                self.option_label[3].grid()
                self.option[3].entry_more_set([], [], 6)
                self.option[3].grid()

                self.temp = ""
            
            if test == "Multinomial Logistic Regression":
                self.option_label[0].config(text="X (nominal):")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="X (categorical):")
                self.option_label[1].grid()
                self.option[1].check_more_set(self.master.data_col["cat"])
                self.option[1].grid()

                self.option_label[2].config(text="Y:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["cat"])
                self.option[2].grid()

                self.option_label[3].config(text="Baseline:")
                self.option_label[3].grid()
                self.option[3].radio_one_set([])
                self.option[3].grid()

                self.temp = ""

        if kind == "Nonparametric":

            if test == "Median Test":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Expect:")
                self.option_label[1].grid()
                self.option[1].entry_one_set(0, 6)
                self.option[1].grid()

            if test == "Sign Test":
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

            if test == "Wilcoxon Signed-Rank Test":
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

            if test == "Wilcoxon Rank-Sum Test":
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

                self.temp = ""

            if test == "Kruskal-Wallis Test":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Between:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()
            
            if test == "Friedman Test":
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

            if test == "Spearman's Rank Correlation":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["num"])
                self.option[1].grid()

        if kind == "Others":

            if test == "Screening Test":
                self.option_label[0].config(text="Disease:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["cat"])
                self.option[0].grid()

                self.option_label[1].config(text="Disease Target:")
                self.option_label[1].grid()
                self.option[1].radio_one_set([])
                self.option[1].grid()

                self.option_label[2].config(text="Test:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["cat"])
                self.option[2].grid()

                self.option_label[3].config(text="Test Target:")
                self.option_label[3].grid()
                self.option[3].radio_one_set([])
                self.option[3].grid()

                self.temp_1 = ""
                self.temp_2 = ""
            
            if test == "Epidemiologic Study":
                self.option_label[0].config(text="Disease:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["cat"])
                self.option[0].grid()

                self.option_label[1].config(text="Disease Target:")
                self.option_label[1].grid()
                self.option[1].radio_one_set([])
                self.option[1].grid()

                self.option_label[2].config(text="Factor:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["cat"])
                self.option[2].grid()

                self.option_label[3].config(text="Factor Target:")
                self.option_label[3].grid()
                self.option[3].radio_one_set([])
                self.option[3].grid()

                self.temp_1 = ""
                self.temp_2 = ""

            if test == "Factor Analysis":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Factors:")
                self.option_label[1].grid()
                self.option[1].radio_one_set([])
                self.option[1].grid()
    
                self.option_label[2].config(text="Analyze:")
                self.option_label[2].grid()
                self.option[2].entry_more_set([], [], 6)
                self.option[2].grid()

                self.temp = ""

            if test == "Principal Component Analysis":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data_col["num"])
                self.option[0].grid()
    
                self.option_label[1].config(text="Transform:")
                self.option_label[1].grid()
                self.option[1].entry_more_set([], [], 6)
                self.option[1].grid()

                self.temp = ""
                
            if test == "Linear Discriminant Analysis":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()
    
                self.option_label[2].config(text="Predict:")
                self.option_label[2].grid()
                self.option[2].entry_more_set([], [], 6)
                self.option[2].grid()

                self.temp = ""


        self.change()

    def change(self):

        for wid in self.result.values():
            wid.grid_remove()
            wid.data = pd.DataFrame()

        kind = self.test_1.get()
        test = self.test_2[kind].get()

        if kind == "Basic":

            if test == "Numeral":
                variable = self.option[0].check_more_get()
                if len(variable) == 0:
                    return
                
                result = model.numeral(self.master.data, variable=variable)
                self.result[0].data = result
                self.result[0].set(19)
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
                self.result[0].set(19)
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
                self.result[0].set(1)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(1)
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
                self.result[1].set(1)
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
                self.result[1].set(1)
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
                self.result[1].set(2)
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
                self.result[1].set(3)
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
                self.result[1].set(1)
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
                self.result[1].set(2)
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
                self.result[1].set(1)
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
                self.result[1].set(1)
                self.result[1].grid()

            if test == "McNemar's Exact Test":
                variable_1 = self.option[0].radio_one_get()
                variable_2 = self.option[1].radio_one_get()
                pair = self.option[2].radio_one_get()

                if not variable_1:
                    return
                if not variable_2:
                    return
                if not pair:
                    return

                summary, result = model.mcnemar_exact_test(self.master.data, variable_1=variable_1, variable_2=variable_2, pair=pair)

                self.result[0].data = summary
                self.result[0].set(2)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(1)
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
                self.result[1].set(2)
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
                self.result[1].set(1)
                self.result[1].grid()

            if test == "McNemar's Test":
                variable_1 = self.option[0].radio_one_get()
                variable_2 = self.option[1].radio_one_get()
                pair = self.option[2].radio_one_get()

                if not variable_1:
                    return
                if not variable_2:
                    return
                if not pair:
                    return

                summary, result = model.mcnemar_test(self.master.data, variable_1=variable_1, variable_2=variable_2, pair=pair)

                self.result[0].data = summary
                self.result[0].set(2)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(2)
                self.result[1].grid()

            if test == "Mantel-Haenszel Test":
                variable_1 = self.option[0].radio_one_get()
                variable_2 = self.option[1].radio_one_get()
                stratum = self.option[2].radio_one_get()

                if not variable_1:
                    return
                if not variable_2:
                    return
                if not stratum:
                    return

                summary, result = model.mantel_haenszel_test(self.master.data, variable_1=variable_1, variable_2=variable_2, stratum=stratum)

                self.result[0].data = summary
                self.result[0].set(13)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(1)
                self.result[1].grid()

        if kind == "Linear Regression":

            if test == "Correlation":
                x = self.option[0].radio_one_get()
                y = self.option[1].radio_one_get()

                if not x:
                    return
                if not y:
                    return

                summary, result = model.correlation(self.master.data, x=x, y=y)

                self.result[0].data = summary
                self.result[0].set(1)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(1)
                self.result[1].grid()

            if test == "Correlation Matrix":
                variable = self.option[0].check_more_get()

                if len(variable) == 0:
                    return
                
                result = model.correlation_matrix(self.master.data, variable=variable)
                self.result[0].data = result
                self.result[0].set(19)
                self.result[0].grid()

            if test == "Simple Linear Regression":
                x = self.option[0].radio_one_get()
                y = self.option[1].radio_one_get()

                if not x:
                    return
                if not y:
                    return

                summary, result = model.simple_linear_regression(self.master.data, x=x, y=y)

                self.result[0].data = summary
                self.result[0].set(2)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(1)
                self.result[1].grid()

            if test == "Multiple Linear Regression":
                x_nomianl = self.option[0].check_more_get()
                x_categorical = self.option[1].check_more_get()
                y = self.option[2].radio_one_get()

                if len(x_nomianl) == 0 and len(x_categorical) == 0:
                    return
                if not y:
                    return

                summary, result = model.multiple_linear_regression(self.master.data, x_nominal=x_nomianl, x_categorical=x_categorical, y=y)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(1)
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
                self.result[0].set(2)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(1)
                self.result[1].grid()

            if test == "Multiple Logistic Regression":
                x_nomianl = self.option[0].check_more_get()
                x_categorical = self.option[1].check_more_get()
                y = self.option[2].radio_one_get()

                if len(x_nomianl) == 0 and len(x_categorical) == 0:
                    return
                if not y:
                    return
                
                if y != self.temp:
                    self.option[3].radio_one_set(self.master.data[y].dropna().unique().tolist())
                self.temp = y
                
                target = self.option[3].radio_one_get()

                if not target:
                    return

                summary, result = model.multiple_logistic_regression(self.master.data, x_nominal=x_nomianl, x_categorical=x_categorical, y=y, target=target)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(1)
                self.result[1].grid()

            if test == "Ordered Logistic Regression":
                x_nomianl = self.option[0].check_more_get()
                x_categorical = self.option[1].check_more_get()
                y = self.option[2].radio_one_get()

                if len(x_nomianl) == 0 and len(x_categorical) == 0:
                    return
                if not y:
                    return
                
                if y != self.temp:
                    opt = self.master.data[y].dropna().unique().tolist()
                    self.option[3].entry_more_set(opt, [""]*len(opt), 6)
                self.temp = y

                order = self.option[3].entry_more_get()

                try:
                    for i in order:
                        order[i] = float(order[i])
                except:
                    return

                summary, result = model.ordered_logistic_regression(self.master.data, x_nominal=x_nomianl, x_categorical=x_categorical, y=y, order=order)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(1)
                self.result[1].grid()

            if test == "Multinomial Logistic Regression":
                x_nomianl = self.option[0].check_more_get()
                x_categorical = self.option[1].check_more_get()
                y = self.option[2].radio_one_get()

                if len(x_nomianl) == 0 and len(x_categorical) == 0:
                    return
                if not y:
                    return
                
                if y != self.temp:
                    self.option[3].radio_one_set(self.master.data[y].dropna().unique().tolist())
                self.temp = y
                
                baseline = self.option[3].radio_one_get()

                if not baseline:
                    return

                summary, result = model.multinomial_logistic_regression(self.master.data, x_nominal=x_nomianl, x_categorical=x_categorical, y=y, baseline=baseline)

                self.result[0].data = summary
                self.result[0].set(11)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(1)
                self.result[1].grid()

        if kind == "Nonparametric":

            if test == "Median Test":
                variable = self.option[0].radio_one_get()
                expect = self.option[1].entry_one_get()

                if not variable:
                    return
                try:
                    expect = float(expect)
                except:
                    return

                summary, result = model.median_test(self.master.data, variable=variable, expect=expect)
                
                self.result[0].data = summary
                self.result[0].set(1)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(2)
                self.result[1].grid()

            if test == "Sign Test":
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

                summary, result = model.sign_test(self.master.data, variable=variable, between=between, group=group, pair=pair)
                
                self.result[0].data = summary
                self.result[0].set(2)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(2)
                self.result[1].grid()

            if test == "Wilcoxon Signed-Rank Test":
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

                summary, result = model.wilcoxon_signed_rank_test(self.master.data, variable=variable, between=between, group=group, pair=pair)
                
                self.result[0].data = summary
                self.result[0].set(2)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(2)
                self.result[1].grid()

            if test == "Wilcoxon Rank-Sum Test":
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

                summary, result = model.wilcoxon_rank_sum_test(self.master.data, variable=variable, between=between, group=group)
                
                self.result[0].data = summary
                self.result[0].set(2)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(2)
                self.result[1].grid()
        
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
                self.result[1].set(1)
                self.result[1].grid()

            if test == "Friedman Test":
                variable = self.option[0].radio_one_get()
                between = self.option[1].radio_one_get()
                subject = self.option[2].radio_one_get()

                if not variable:
                    return
                if not between:
                    return
                if not subject:
                    return

                summary, result = model.friedman_test(self.master.data, variable=variable, between=between, subject=subject)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(1)
                self.result[1].grid()

            if test == "Spearman's Rank Correlation":
                x = self.option[0].radio_one_get()
                y = self.option[1].radio_one_get()

                if not x:
                    return
                if not y:
                    return

                summary, result = model.spearman_rank_correlation(self.master.data, x=x, y=y)

                self.result[0].data = summary
                self.result[0].set(1)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(1)
                self.result[1].grid()

        if kind == "Others":
            
            if test == "Screening Test":
                disease = self.option[0].radio_one_get()
                if not disease:
                    return
                
                if disease != self.temp_1:
                    self.temp_1 = disease
                    opt = self.master.data[disease].dropna().unique().tolist()
                    self.option[1].radio_one_set(opt)
                
                disease_target = self.option[1].radio_one_get()
                if not disease_target:
                    return

                test = self.option[2].radio_one_get()
                if not test:
                    return
                
                if test != self.temp_2:
                    self.temp_2 = test
                    opt = self.master.data[test].dropna().unique().tolist()
                    self.option[3].radio_one_set(opt)
                
                test_target = self.option[3].radio_one_get()
                if not test_target:
                    return

                summary, result = model.screening_test(self.master.data, disease=disease, disease_target=disease_target, test=test, test_target=test_target)

                self.result[0].data = summary
                self.result[0].set(2)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(6)
                self.result[1].grid()

            if test == "Epidemiologic Study":
                disease = self.option[0].radio_one_get()
                if not disease:
                    return
                
                if disease != self.temp_1:
                    self.temp_1 = disease
                    opt = self.master.data[disease].dropna().unique().tolist()
                    self.option[1].radio_one_set(opt)
                
                disease_target = self.option[1].radio_one_get()
                if not disease_target:
                    return

                factor = self.option[2].radio_one_get()
                if not factor:
                    return
                
                if factor != self.temp_2:
                    self.temp_2 = factor
                    opt = self.master.data[factor].dropna().unique().tolist()
                    self.option[3].radio_one_set(opt)
                
                factor_target = self.option[3].radio_one_get()
                if not factor_target:
                    return

                summary, result = model.epidemiologic_study(self.master.data, disease=disease, disease_target=disease_target, factor=factor, factor_target=factor_target)

                self.result[0].data = summary
                self.result[0].set(2)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(4)
                self.result[1].grid()

            if test == "Factor Analysis":
                x = self.option[0].check_more_get()

                if len(x) ==0 :
                    return

                if x != self.temp:
                    self.temp = x
                    self.option[1].radio_one_set([i+1 for i in range(len(x))])
                    self.option[2].entry_more_set(x, [""]*len(x), 6)
                
                factors = self.option[1].radio_one_get()
                analyze = self.option[2].entry_more_get()

                if not factors:
                    return

                try:
                    for i in analyze:
                        analyze[i] = float(analyze[i])
                except:
                    analyze = None

                summary, result, analysis = model.factor_analysis(self.master.data, x=x, factors=factors, analyze=analyze)
                
                self.result[0].data = summary
                self.result[0].set(1)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(9)
                self.result[1].grid()
                self.result[2].data = analysis
                self.result[2].set(1)
                self.result[2].grid()

            if test == "Principal Component Analysis":
                x = self.option[0].check_more_get()

                if len(x) ==0 :
                    return

                if x != self.temp:
                    self.temp = x
                    self.option[1].entry_more_set(x, [""]*len(x), 6)
                
                transform = self.option[1].entry_more_get()

                try:
                    for i in transform:
                        transform[i] = float(transform[i])
                except:
                    transform = None
                
                summary, result, transformation = model.principal_component_analysis(self.master.data, x=x, transform=transform)
                
                self.result[0].data = summary
                self.result[0].set(5)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(5)
                self.result[1].grid()
                self.result[2].data = transformation
                self.result[2].set(1)
                self.result[2].grid()

            if test == "Linear Discriminant Analysis":
                x = self.option[0].check_more_get()
                y = self.option[1].radio_one_get()

                if len(x) ==0 :
                    return
                if not y:
                    return

                if x != self.temp:
                    self.temp = x
                    self.option[2].entry_more_set(x, [""]*len(x), 6)
                
                predict = self.option[2].entry_more_get()

                try:
                    for i in predict:
                        predict[i] = float(predict[i])
                except:
                    predict = None
                
                summary, result, prediction = model.linear_discriminant_analysis(self.master.data, x=x, y=y, predict=predict)
                
                self.result[0].data = summary
                self.result[0].set(5)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(5)
                self.result[1].grid()
                self.result[2].data = prediction
                self.result[2].set(1)
                self.result[2].grid()


        self.master.updating()
        self.focus()

    def save(self):

        filename = filedialog.asksaveasfilename(
            title="Save File", 
            filetypes=[
                ("Excel File", "*.xlsx"), 
                ("Markdown FIle", "*.md"),
                ("Text File", "*.txt"),
                ("All Files", "*")
            ],
            initialfile="Test"
        )
        if filename:
            try:
                if ".xlsx" in filename:
                    pd.DataFrame().to_excel(filename, sheet_name="Sheet1" )
                    with pd.ExcelWriter(filename, mode='a', if_sheet_exists='overlay') as writer:
                        row = 0
                        for i in self.result:
                            if len(self.result[i].data) == 0:
                                continue
                            self.result[i].data.to_excel(writer, startrow=row)
                            row += len(self.result[i].data) + 2
                elif ".md" in filename:
                    result = ""
                    for i in self.result:
                        if len(self.result[i].data) == 0:
                            continue
                        result += self.result[i].data.to_markdown()
                        result += "\n\n"
                    with open(filename, 'w') as f:
                        f.write(result)
                else:
                    result = ""
                    for i in self.result:
                        if len(self.result[i].data) == 0:
                            continue
                        result += self.result[i].data.to_string()
                        result += "\n\n"
                    with open(filename, 'w') as f:
                        f.write(result)
            except:
                messagebox.showerror(
                    title="Error",
                    message="File could not be saved."
                )  