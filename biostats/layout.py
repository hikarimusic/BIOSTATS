import tkinter as tk
from tkinter import ttk

from .basic_measurement import master as basic_measurement
from .one_sample_t_test import master as one_sample_t_test


class Master(ttk.Frame):

    def __init__(self, parent):

        # Initialize
        ttk.Frame.__init__(self, parent)

        # Setup
        self.setup() ;

    def setup(self):

        # Configure
        self.columnconfigure(index=1, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=2, weight=1)

        # Select Type
        self.select_type = SelectType(self, self)
        self.select_type.grid(
            row=0, column=0, padx=(20,10), pady=(20,10), sticky="nsew"
        )

        # Separator
        self.separator = ttk.Separator(self)
        self.separator.grid(
            row=1, column=0, padx=(20,10), pady=10, sticky="ew"
        )

        # Select Model
        self.select_model = {}

        self.select_model[0] = Measurement(self, self)
        self.select_model[0].grid(
            row=2, column=0, padx=(20,10), pady=10, sticky="nsew"
        )

        self.select_model[1] = Categorical(self, self)
        self.select_model[1].grid(
            row=2, column=0, padx=(20,10), pady=10, sticky="nsew"
        )

        self.select_model[2] = Regression(self, self)
        self.select_model[2].grid(
            row=2, column=0, padx=(20,10), pady=10, sticky="nsew"
        )

        self.select_model[3] = Nonparametric(self, self)
        self.select_model[3].grid(
            row=2, column=0, padx=(20,10), pady=10, sticky="nsew"
        )

        self.select_model[4] = PersonTime(self, self)
        self.select_model[4].grid(
            row=2, column=0, padx=(20,10), pady=10, sticky="nsew"
        )

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0,5), pady=(0,5))

        # Model
        self.model = {}

        # Show
        self.show()

    def show(self):

        # Show Selected Model
        i = self.select_type.type.get()
        j = self.select_model[i].model.get()

        frame1 = self.select_model[i]
        frame1.tkraise()

        if not (i,j) in self.model:
            self.model_open((i,j))
        frame2 = self.model[(i,j)]
        frame2.tkraise()

    def model_open(self, target):

        # Measurement Data
        if target == (0,0):
            self.model[(0,0)] = basic_measurement.Master(self)
            self.model[(0,0)].grid(
                row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
            )

        # Categorical Data
        if target == (1,0):
            self.model[(1,0)] = one_sample_t_test.Master(self)
            self.model[(1,0)].grid(
                row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
            )

        # Regression
        if target == (2,0):
            self.model[(2,0)] = one_sample_t_test.Master(self)
            self.model[(2,0)].grid(
                row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
            )

        # Nonparametric
        if target == (3,0):
            self.model[(3,0)] = one_sample_t_test.Master(self)
            self.model[(3,0)].grid(
                row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
            )
        
        # Person-Time Data
        if target == (4,0):
            self.model[(4,0)] = one_sample_t_test.Master(self)
            self.model[(4,0)].grid(
                row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
            )

class SelectType(ttk.LabelFrame):

    def __init__(self, parent, controller):

        # Initialize
        ttk.LabelFrame.__init__(self, parent)
        self.controller = controller

        # Variables
        self.type = tk.IntVar(value=0)

        # Setup
        self.setup()

    def setup(self):
        
        # Configure
        self.configure(text="Type", padding=(20,10))

        # Radio Button
        self.radio = {}
        self.type_name = [
            "Measurement Data", "Categorical Data",
            "Regression", "Nonparametric", "Person-Time Data"
        ]

        for i in range(len(self.type_name)):
            self.radio[i] = ttk.Radiobutton(
                self, text=self.type_name[i], variable=self.type, value=i
            )
            self.radio[i].configure(command=self.controller.show)
            self.radio[i].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")

class Measurement(ttk.LabelFrame):

    def __init__(self, parent, controller):

        # Initialize
        ttk.LabelFrame.__init__(self, parent)
        self.controller = controller
        
        # Variables
        self.model = tk.IntVar(value=0)

        # Setup
        self.setup()

    def setup(self):

        # Configure
        self.configure(text="Model", padding=(20,10))

        # Radio Button
        self.radio = {}
        self.model_name = [
            "Basic Statistic", "One-Sample t Test", "Two-Sample t Test", "Paired t Test",
            "One-Way ANOVA", "Two-Way ANOVA", "One-Way ANCOVA", "Two-Way ANCOVA"
        ]

        for i in range(len(self.model_name)):
            self.radio[i] = ttk.Radiobutton(
                self, text=self.model_name[i], variable=self.model, value=i
            )
            self.radio[i].configure(command=self.controller.show)
            self.radio[i].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")

class Categorical(ttk.LabelFrame):

    def __init__(self, parent, controller):

        # Initialize
        ttk.LabelFrame.__init__(self, parent)
        self.controller = controller
        
        # Variables
        self.model = tk.IntVar(value=0)

        # Setup
        self.setup()

    def setup(self):

        # Configure
        self.configure(text="Model", padding=(20,10))

        # Radio Button
        self.radio = {}
        self.model_name = [
            "Basic Statistic", "Chi-Square Test", "Chi-Square Test\n(Goodness of Fit)",
            "Binomial Exact Test", "Fisher's Exact Test", "McNemar's Test", "Mantel-Haenszel Test"
        ]

        for i in range(len(self.model_name)):
            self.radio[i] = ttk.Radiobutton(
                self, text=self.model_name[i], variable=self.model, value=i
            )
            self.radio[i].configure(command=self.controller.show)
            self.radio[i].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")

class Regression(ttk.LabelFrame):

    def __init__(self, parent, controller):

        # Initialize
        ttk.LabelFrame.__init__(self, parent)
        self.controller = controller
        
        # Variables
        self.model = tk.IntVar(value=0)

        # Setup
        self.setup()

    def setup(self):

        # Configure
        self.configure(text="Model", padding=(20,10))

        # Radio Button
        self.radio = {}
        self.model_name = [
            "Correlation", "Linear Regression",
            "Multiple Regression", "Logistic Regression"
        ]

        for i in range(len(self.model_name)):
            self.radio[i] = ttk.Radiobutton(
                self, text=self.model_name[i], variable=self.model, value=i
            )
            self.radio[i].configure(command=self.controller.show)
            self.radio[i].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")

class Nonparametric(ttk.LabelFrame):

    def __init__(self, parent, controller):

        # Initialize
        ttk.LabelFrame.__init__(self, parent)
        self.controller = controller
        
        # Variables
        self.model = tk.IntVar(value=0)

        # Setup
        self.setup()

    def setup(self):

        # Configure
        self.configure(text="Model", padding=(20,10))

        # Radio Button
        self.radio = {}
        self.model_name = [
            "Sign Test", "Wilcoxon\nSigned-Rank Test", "Wilcoxon\nRank-Sum Test",
            "Kruskal-Wallis Test", "Spearman\nRank-Correlation"
        ]

        for i in range(len(self.model_name)):
            self.radio[i] = ttk.Radiobutton(
                self, text=self.model_name[i], variable=self.model, value=i
            )
            self.radio[i].configure(command=self.controller.show)
            self.radio[i].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")

class PersonTime(ttk.LabelFrame):

    def __init__(self, parent, controller):

        # Initialize
        ttk.LabelFrame.__init__(self, parent)
        self.controller = controller
        
        # Variables
        self.model = tk.IntVar(value=0)

        # Setup
        self.setup()

    def setup(self):

        # Configure
        self.configure(text="Model", padding=(20,10))

        # Radio Button
        self.radio = {}
        self.model_name = [
            "One-Sample\nIncidence Rate", "Two-Sample\nIncidence Rate", "Log-Rank Test"
        ]

        for i in range(len(self.model_name)):
            self.radio[i] = ttk.Radiobutton(
                self, text=self.model_name[i], variable=self.model, value=i
            )
            self.radio[i].configure(command=self.controller.show)
            self.radio[i].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")

