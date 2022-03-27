import tkinter as tk
from tkinter import ttk

class master(ttk.Notebook):
    def __init__(self, parent):
        ttk.Notebook.__init__(self, parent)

        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

        self.setup()

    def setup(self):
        self.tab_0 = Data(self)
        self.add(self.tab_0, text="Data")

        self.tab_1 = Statistic(self)
        self.add(self.tab_1, text="Statistic")
        
        self.tab_2 = Graph(self)
        self.add(self.tab_2, text="Gaprh")
        
        self.tab_3 = Test(self)
        self.add(self.tab_3, text="Test")



class Data(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=3)
        self.rowconfigure(index=3, weight=1)

        self.setup()

    def setup(self):
        # frame
        self.frame_0 = ttk.Frame(self)
        self.frame_0.grid(
            row=0, column=0, sticky="nsew"
        )
        self.frame_1 = ttk.Frame(self)
        self.frame_1.grid(
            row=1, column=0, sticky="nsew"
        )
        self.frame_2 = ttk.Frame(self)
        self.frame_2.grid(
            row=2, column=0, sticky="nsew"
        )
        self.frame_3 = ttk.Frame(self)
        self.frame_3.grid(
            row=3, column=0, sticky="nsew"
        )

        # frame_0
        self.frame_0_label_1 = ttk.Label(
            self.frame_0, text="Sampel size"
        )
        self.frame_0_label_1.grid(
            row=0, column=0, padx=40, pady=(20,5), sticky="w"
        )
        
        # frame_1
        self.frame_1.columnconfigure(index=0, weight=1)
        self.frame_1.rowconfigure(index=0, weight=1)

        self.frame_1_box = ttk.LabelFrame(
            self.frame_1, text="Inpur Data"
        )
        self.frame_1_box.grid(row=0, column=0, padx=40, pady=5, sticky="nsew")
        self.frame_1_box.columnconfigure(index=0, weight=1)
        self.frame_1_box.rowconfigure(index=0, weight=1)

        self.frame_1_scroll = ttk.Scrollbar(
            self.frame_1_box, orient="vertical"
        )
        self.frame_1_scroll.grid(row=0, column=1, sticky="nsew")

        # frame_2
        self.frame_2_label_1 = ttk.Label(
            self.frame_2, text="Switch"
        )
        self.frame_2_label_1.grid(
            row=0, column=0, padx=40, pady=5, sticky="w"
        )
        


        

        



class Statistic(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)


class Graph(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)


class Test(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
