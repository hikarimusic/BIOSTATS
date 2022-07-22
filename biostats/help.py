import tkinter as tk
from tkinter import ttk

class Example(ttk.Menubutton):

    def __init__(self, parent, master, text, width):
        
        # Initialize
        ttk.Menubutton.__init__(self, parent, text=text, width=width)
        self.master = master

        # Variable
        self.test_type = ["Basic", "t-Test", "ANOVA", "Exact Test", "Chi-Square Test", "Linear Regression", "Logistic Regression", "Nonparametric", "Others"]
        self.test_list = {
            "Basic"               : ["Numeral", "Numeral (Grouped)", "Categorical", "Contingency"] ,
            "t-Test"              : ["One-Sample t-Test", "Two-Sample t-Test", "Paired t-Test", "Pairwise t-Test"] ,
            "ANOVA"               : ["One-Way ANOVA", "Two-Way ANOVA", "One-Way ANCOVA", "Two-Way ANCOVA", "Multivariate ANOVA", "Repeated Measures ANOVA"] ,
            "Exact Test"          : ["Binomial Test", "Fisher's Exact Test", "McNemar's Exact Test"] ,
            "Chi-Square Test"     : ["Chi-Square Test", "Chi-Square Test (Fit)", "McNemar's Test", "Mantel-Haenszel Test"] ,
            "Linear Regression"   : ["Correlation", "Correlation Matrix", "Simple Linear Regression", "Multiple Linear Regression"] ,
            "Logistic Regression" : ["Simple Logistic Regression", "Multiple Logistic Regression", "Ordered Logistic Regression", "Multinomial Logistic Regression"] ,
            "Nonparametric"       : ["Median Test", "Sign Test", "Wilcoxon Signed-Rank Test", "Wilcoxon Rank-Sum Test", "Kruskal-Wallis Test", "Friedman Test", "Spearman's Rank Correlation"] ,
            "Others"              : ["Screening Test", "Epidemiologic Study", "Factor Analysis", "Principal Component Analysis", "Linear Discriminant Analysis"]
        }
        self.plot_type = ["Distribution", "Categorical", "Relational", "Multiple", "Others"]
        self.plot_list = {
            "Distribution" : ["Histogram", "Density Plot", "Cumulative Plot", "2D Histogram", "2D Density Plot"],
            "Categorical"  : ["Count Plot", "Strip Plot", "Swarm Plot", "Box Plot", "Boxen Plot", "Violin Plot", "Bar Plot"],
            "Relational"   : ["Scatter Plot", "Line Plot", "Regression Plot"],
            "Multiple"     : ["Ultimate Plot", "Pair Plot", "Joint Plot"],
            "Others"       : ["Heatmap", "FA Plot", "PCA Plot", "LDA Plot"]
        }

        # Setup
        self.setup()

    def setup(self):

        self.menu_0 = tk.Menu(self)
        self.config(menu=self.menu_0)

        self.menu_1 = {}
        self.which = tk.StringVar()

        for test_1 in self.test_type:
            self.menu_1[test_1] = tk.Menu(self.menu_0)
            self.menu_0.add_cascade(label=test_1, menu=self.menu_1[test_1])
            for test_2 in self.test_list[test_1]:
                self.menu_1[test_1].add_radiobutton(label=test_2, value=test_2, variable=self.which, command=self.change)
    
    def change(self):

        print(self.which.get())





class Manual(ttk.Menubutton):

    def __init__(self, parent, master, text, width):
        
        # Initialize
        ttk.Menubutton.__init__(self, parent, text=text, width=width)
        self.master = master

        # Setup
        self.setup()

    def setup(self):

        pass
