import tkinter as tk
from tkinter import ttk

from .one_sample_t_test import master as one_sample_t_test
from .two_sample_t_test import master as two_sample_t_test
from .paired_t_test import master as paired_t_test
from .one_way_anova import master as one_way_anova
from .two_way_anova import master as two_way_anova


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

        self.select_model[3] = Ranked(self, self)
        self.select_model[3].grid(
            row=2, column=0, padx=(20,10), pady=10, sticky="nsew"
        )

        # Model
        self.model = {}

        '''
        self.model[(0,0)] = one_sample_t_test.Master(self)
        self.model[(0,0)].grid(
            row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
        )

        self.model[(0,1)] = two_sample_t_test.Master(self)
        self.model[(0,1)].grid(
            row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
        )

        self.model[(0,2)] = paired_t_test.Master(self)
        self.model[(0,2)].grid(
            row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
        )

        self.model[(0,3)] = one_way_anova.Master(self)
        self.model[(0,3)].grid(
            row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
        )

        self.model[(0,4)] = two_way_anova.Master(self)
        self.model[(0,4)].grid(
            row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
        )

        #temp
        self.model[(1,0)] = one_sample_t_test.Master(self)
        self.model[(1,0)].grid(
            row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
        )

        self.model[(2,0)] = one_sample_t_test.Master(self)
        self.model[(2,0)].grid(
            row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
        )

        self.model[(3,0)] = one_sample_t_test.Master(self)
        self.model[(0,0)].grid(
            row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
        )

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0,5), pady=(0,5))
        '''

        # Show
        self.show()

    def show(self):
        i = self.select_type.type.get()
        j = self.select_model[i].model.get()
        frame1 = self.select_model[i]
        frame1.tkraise()
        if not (i,j) in self.model:
            self.model_open((i,j))
        frame2 = self.model[(i,j)]
        frame2.tkraise()

    def model_open(self, target):

        if target == (0,0):
            self.model[(0,0)] = one_sample_t_test.Master(self)
            self.model[(0,0)].grid(
                row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
            )

        if target == (0,1):
            self.model[(0,1)] = two_sample_t_test.Master(self)
            self.model[(0,1)].grid(
                row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
            )

        if target == (0,2):
            self.model[(0,2)] = paired_t_test.Master(self)
            self.model[(0,2)].grid(
                row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
            )

        if target == (0,3):
            self.model[(0,3)] = one_way_anova.Master(self)
            self.model[(0,3)].grid(
                row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
            )

        if target == (0,4):
            self.model[(0,4)] = two_way_anova.Master(self)
            self.model[(0,4)].grid(
                row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
            )

        if target == (1,0):
            self.model[(1,0)] = one_sample_t_test.Master(self)
            self.model[(1,0)].grid(
                row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
            )

        if target == (2,0):
            self.model[(2,0)] = one_sample_t_test.Master(self)
            self.model[(2,0)].grid(
                row=0, column=1, padx=10, pady=(20,10), sticky="nsew", rowspan=3
            )

        if target == (3,0):
            self.model[(3,0)] = one_sample_t_test.Master(self)
            self.model[(0,0)].grid(
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
        self.radio_0 = ttk.Radiobutton(
            self, text="Measurement Data", variable=self.type, value=0, 
        )
        self.radio_0.configure(command=self.controller.show)
        self.radio_0.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_1 = ttk.Radiobutton(
            self, text="Categorical Data", variable=self.type, value=1
        )
        self.radio_1.configure(command=self.controller.show)
        self.radio_1.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_2 = ttk.Radiobutton(
            self, text="Regression", variable=self.type, value=2
        )
        self.radio_2.configure(command=self.controller.show)
        self.radio_2.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_3 = ttk.Radiobutton(
            self, text="Other Tests", variable=self.type, value=3
        )
        self.radio_3.configure(command=self.controller.show)
        self.radio_3.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")


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
        self.radio_0 = ttk.Radiobutton(
            self, text="One Sample T Test", variable=self.model, value=0
        )
        self.radio_0.configure(command=self.controller.show)
        self.radio_0.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_1 = ttk.Radiobutton(
            self, text="Two Sample T Test", variable=self.model, value=1
        )
        self.radio_1.configure(command=self.controller.show)
        self.radio_1.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_2 = ttk.Radiobutton(
            self, text="Paired T Test", variable=self.model, value=2
        )
        self.radio_2.configure(command=self.controller.show)
        self.radio_2.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_3 = ttk.Radiobutton(
            self, text="One Way ANOVA", variable=self.model, value=3
        )
        self.radio_3.configure(command=self.controller.show)
        self.radio_3.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_4 = ttk.Radiobutton(
            self, text="Two Way ANOVA", variable=self.model, value=4
        )
        self.radio_4.configure(command=self.controller.show)
        self.radio_4.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_5 = ttk.Radiobutton(
            self, text="Nested ANOVA", variable=self.model, value=5
        )
        self.radio_5.configure(command=self.controller.show)
        self.radio_5.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_6 = ttk.Radiobutton(
            self, text="Welch's T Test", variable=self.model, value=6
        )
        self.radio_6.configure(command=self.controller.show)
        self.radio_6.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_7 = ttk.Radiobutton(
            self, text="Bartlett's Test", variable=self.model, value=7
        )
        self.radio_7.configure(command=self.controller.show)
        self.radio_7.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

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

        self.label_0 = ttk.Label(
            self, text="Goodness of Fit", font="-slant italic"
        )
        self.label_0.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_0 = ttk.Radiobutton(
            self, text="Exact Test", variable=self.model, value=0
        )
        self.radio_0.configure(command=self.controller.show)
        self.radio_0.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_1 = ttk.Radiobutton(
            self, text="Chi-Square Test", variable=self.model, value=1
        )
        self.radio_1.configure(command=self.controller.show)
        self.radio_1.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_2 = ttk.Radiobutton(
            self, text="G Test", variable=self.model, value=2
        )
        self.radio_2.configure(command=self.controller.show)
        self.radio_2.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_3 = ttk.Radiobutton(
            self, text="Repeated G Test", variable=self.model, value=3
        )
        self.radio_3.configure(command=self.controller.show)
        self.radio_3.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

        self.label_1 = ttk.Label(
            self, text="Test for Independence", font="-slant italic"
        )
        self.label_1.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_4 = ttk.Radiobutton(
            self, text="Fisher's Exact Test", variable=self.model, value=4
        )
        self.radio_4.configure(command=self.controller.show)
        self.radio_4.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_5 = ttk.Radiobutton(
            self, text="Chi-Square Test", variable=self.model, value=5
        )
        self.radio_5.configure(command=self.controller.show)
        self.radio_5.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_6 = ttk.Radiobutton(
            self, text="G Test", variable=self.model, value=6
        )
        self.radio_6.configure(command=self.controller.show)
        self.radio_6.grid(row=8, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_7 = ttk.Radiobutton(
            self, text="McNemer's Test", variable=self.model, value=7
        )
        self.radio_7.configure(command=self.controller.show)
        self.radio_7.grid(row=9, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_8 = ttk.Radiobutton(
            self, text="CMH Test", variable=self.model, value=8
        )
        self.radio_8.configure(command=self.controller.show)
        self.radio_8.grid(row=10, column=0, padx=5, pady=10, sticky="nsew")

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
        self.radio_0 = ttk.Radiobutton(
            self, text="Linear Regression", variable=self.model, value=0
        )
        self.radio_0.configure(command=self.controller.show)
        self.radio_0.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_1 = ttk.Radiobutton(
            self, text="Multiple Regression", variable=self.model, value=1
        )
        self.radio_1.configure(command=self.controller.show)
        self.radio_1.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_2 = ttk.Radiobutton(
            self, text="Polynomial Regression", variable=self.model, value=2
        )
        self.radio_2.configure(command=self.controller.show)
        self.radio_2.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_3 = ttk.Radiobutton(
            self, text="ANCOVA", variable=self.model, value=3
        )
        self.radio_3.configure(command=self.controller.show)
        self.radio_3.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_4 = ttk.Radiobutton(
            self, text="Simple Logistic\nRegression", variable=self.model, value=4
        )
        self.radio_4.configure(command=self.controller.show)
        self.radio_4.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_5 = ttk.Radiobutton(
            self, text="Multiple Logistic\nRegression", variable=self.model, value=5
        )
        self.radio_5.configure(command=self.controller.show)
        self.radio_5.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

class Ranked(ttk.LabelFrame):

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
        self.radio_0 = ttk.Radiobutton(
            self, text="Sign Test", variable=self.model, value=0
        )
        self.radio_0.configure(command=self.controller.show)
        self.radio_0.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_1 = ttk.Radiobutton(
            self, text="Wilcoxon\nSigned-Rank Test", variable=self.model, value=1
        )
        self.radio_1.configure(command=self.controller.show)
        self.radio_1.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_2 = ttk.Radiobutton(
            self, text="Wilcoxon\nRank-Sum Test", variable=self.model, value=2
        )
        self.radio_2.configure(command=self.controller.show)
        self.radio_2.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_3 = ttk.Radiobutton(
            self, text="Kruskal-Wallis Test", variable=self.model, value=3
        )
        self.radio_3.configure(command=self.controller.show)
        self.radio_3.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_4 = ttk.Radiobutton(
            self, text="Spearman Rank\nCorrelation", variable=self.model, value=4
        )
        self.radio_4.configure(command=self.controller.show)
        self.radio_4.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

