import tkinter as tk
from tkinter import ttk

class Master(ttk.Frame):

    def __init__(self, parent, master):

        # Initialize
        ttk.Frame.__init__(self, parent)
        self.master = master

        # Variables
        self.window = tk.IntVar(value=0)
        self.scientific = tk.IntVar(value=0)
        self.precision = tk.StringVar(value=1)
        self.darkmode = tk.IntVar(value=0)

        # Setup
        self.setup() 

    def setup(self):

        # Configure
        self.columnconfigure(index=1, weight=1)
        self.rowconfigure(index=3, weight=1)

        # Window
        self.window_frame = ttk.LabelFrame(self, text="Window", padding=(10,5))
        self.window_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.choose = {}
        self.choose_list = ["Data", "Test", "Plot"]

        for i in range(3):
            self.choose[i] = ttk.Radiobutton(self.window_frame, text=self.choose_list[i])
            self.choose[i].configure(variable=self.window, value=i, command=self.switch)
            self.choose[i].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")

        # Setting
        self.setting_frame = ttk.LabelFrame(self, text="Setting", padding=(10,5))
        self.setting_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.notation = ttk.Checkbutton(self.setting_frame, style="Switch.TCheckbutton")
        self.notation.config(variable=self.scientific, offvalue=0, onvalue=1, command=self.updating)
        self.notation.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.notation_label = ttk.Label(self.setting_frame, text="Scientific")
        self.notation_label.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

        self.decimal = ttk.Spinbox(self.setting_frame, from_=1, to=99, increment=1, width=1)
        self.decimal.config(textvariable=self.precision, command=self.updating)
        self.decimal.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.decimal_label = ttk.Label(self.setting_frame, text="Precision")
        self.decimal_label.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

        self.screenmode = ttk.Checkbutton(self.setting_frame, style="Switch.TCheckbutton")
        self.screenmode.config(variable=self.darkmode, offvalue=0, onvalue=1)
        self.screenmode.config(command=lambda: self.master.swtich_mode(self.darkmode.get()))
        self.screenmode.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.screenmode_label = ttk.Label(self.setting_frame, text="Dark Mode")
        self.screenmode_label.grid(row=2, column=1, padx=5, pady=10, sticky="nsew")


    def switch(self):
        pass

    def updating(self):
        pass
