import tkinter as tk
from tkinter import ttk

from numpy import var

from .widget import Tree, Option
from . import model

class Test(ttk.Frame):

    def __init__(self, parent, master):
        
        # Initialize
        ttk.Frame.__init__(self, parent)
        self.master = master

        # Variable
        self.test_type = ["", "Basic", "ANOVA"]
        self.test_list = {
            "Basic"  : ["", "Numeral"],
            "ANOVA"  : ["", "One-Way ANOVA"]
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

        #self.confirm_button = ttk.Button(self.menu_frame, text="Confirm")
        #self.confirm_button.config(command=self.confirm)
        #self.confirm_button.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        # Option
        self.option_label = {}
        self.option = {}
        for i in range(3):
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



        """
        self.input_list = ["", "Title", "X Label", "Y Label"]
        self.input = tk.StringVar()
        self.input.set(self.input_list[1])

        self.input_menu = ttk.OptionMenu(
            self.control_bar, self.input, *self.input_list
        )
        self.input_menu.config(width=6)
        self.input_menu.grid(
           row=1, column=2, padx=5, pady=0, sticky="nsew"
        )

        self.label = ttk.Label(self, text="Option:")
        self.label.grid(row=0, column=0, padx=5, pady=5)

        self.test = Option(self, self)
        self.test.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        #self.but = ttk.Button(self, text="Option:", command=self.temp)
        #self.but.grid(row=1, column=0, padx=5, pady=5)

        self.test.check_more_set(["a", "b", "c"])
        self.test.check_more_set(["Stream", "Crab", "Temparature", "Temparature", "Temparature", "Temparature", "Temparature", "Temparature", "Temparature"])
        self.test.check_more_set(["a", "b", "c"])
        """

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
                
                result = model.numeral(self.master.data, variable)
                self.result[0].data = result
                self.result[0].set(20)
                self.result[0].grid()

        if kind == "ANOVA":

            if test == "One-Way ANOVA":

                variable = self.option[0].radio_one_get()
                between = self.option[1].radio_one_get()

                if not variable:
                    return
                if not between:
                    return

                summary, result = model.one_way_anova(self.master.data, variable, between)

                self.result[0].data = summary
                self.result[0].set(10)
                self.result[0].grid()
                self.result[1].data = result
                self.result[1].set(3)
                self.result[1].grid()


        self.master.updating()
