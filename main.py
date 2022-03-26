import tkinter as tk
from tkinter import ttk


class MasterFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        self.columnconfigure(index=1, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=2, weight=1)

        self.type = tk.IntVar(value=0)

        self.setup() ;

    def setup(self):
        self.type_frame = ttk.LabelFrame(self, text="Type", padding=(20,10))
        self.type_frame.grid(
            row=0, column=0, padx=(20,10), pady=(20,10), sticky="nsew"
        )

        self.radio_0 = ttk.Radiobutton(
            self.type_frame, text="Measurement Data", variable=self.type, value=0
        )
        self.radio_0.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")


        self.radio_1 = ttk.Radiobutton(
            self.type_frame, text="Categorical Data", variable=self.type, value=1
        )
        self.radio_1.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")


        self.radio_2 = ttk.Radiobutton(
            self.type_frame, text="Regression", variable=self.type, value=2
        )
        self.radio_2.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        

        self.radio_3 = ttk.Radiobutton(
            self.type_frame, text="Ranked Data", variable=self.type, value=3
        )
        self.radio_3.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        self.separator = ttk.Separator(self)
        self.separator.grid(row=1, column=0, padx=(20,10), pady=10, sticky="ew")

        




        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0,5), pady=(0,5))

        


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("BIOSTATS")

        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "dark")

        self.master_frame = MasterFrame(self)
        #self.master_frame.pack(fill="both", expand=True)

        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

        self.master_frame.grid(row=0, column=0, sticky="nsew")
        

        self.update()
        self.minsize(int(self.winfo_screenwidth() / 2), self.winfo_height())
        x_coordinate = int(self.winfo_screenwidth() / 4)
        y_coordinate = int((self.winfo_screenheight() / 2) - (self.winfo_height() / 2))
        self.geometry("+{}+{}".format(x_coordinate, y_coordinate-20))




if __name__ == "__main__":
    app = App()
    app.mainloop()
