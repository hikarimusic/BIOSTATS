import tkinter as tk
from tkinter import ttk

class TypeFrame(ttk.LabelFrame):
    def __init__(self, parent, controller):
        ttk.LabelFrame.__init__(self, parent)
        self.controller = controller

        self.configure(text="Type", padding=(20,10))
        self.type = tk.IntVar(value=0)

        self.setup()

    def setup(self):
        self.radio_0 = ttk.Radiobutton(
            self, text="Measurement Data", variable=self.type, value=0, 
        )
        self.radio_0.configure(command=self.controller.show_frame)
        self.radio_0.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_1 = ttk.Radiobutton(
            self, text="Categorical Data", variable=self.type, value=1
        )
        self.radio_1.configure(command=self.controller.show_frame)
        self.radio_1.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_2 = ttk.Radiobutton(
            self, text="Regression", variable=self.type, value=2
        )
        self.radio_2.configure(command=self.controller.show_frame)
        self.radio_2.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.radio_3 = ttk.Radiobutton(
            self, text="Ranked Data", variable=self.type, value=3
        )
        self.radio_3.configure(command=self.controller.show_frame)
        self.radio_3.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
        

class ModelFrame0(ttk.LabelFrame):
    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent)

        self.configure(text="Model", padding=(20,10))
        self.model = tk.IntVar(value=0)

        self.setup()

    def setup(self):
        self.model_0 = ttk.Radiobutton(
            self, text="One Sample T Test", variable=self.model, value=0
        )
        self.model_0.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.model_1 = ttk.Radiobutton(
            self, text="Two Sample T Test", variable=self.model, value=1
        )
        self.model_1.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.model_2 = ttk.Radiobutton(
            self, text="Paired T Test", variable=self.model, value=2
        )
        self.model_2.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.model_3 = ttk.Radiobutton(
            self, text="One Way ANOVA", variable=self.model, value=3
        )
        self.model_3.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        self.model_4 = ttk.Radiobutton(
            self, text="Two Way ANOVA", variable=self.model, value=4
        )
        self.model_4.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

class ModelFrame1(ttk.LabelFrame):
    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent)

        self.configure(text="Model", padding=(20,10))
        self.model = tk.IntVar(value=0)

        self.setup()

    def setup(self):
        self.model_0 = ttk.Radiobutton(
            self, text="Chi Square", variable=self.model, value=0
        )
        self.model_0.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        '''
        self.model_1 = ttk.Radiobutton(
            self, text="Two Sample T Test", variable=self.model, value=1
        )
        self.model_1.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.model_2 = ttk.Radiobutton(
            self, text="Paired T Test", variable=self.model, value=2
        )
        self.model_2.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.model_3 = ttk.Radiobutton(
            self, text="One Way ANOVA", variable=self.model, value=3
        )
        self.model_3.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        self.model_4 = ttk.Radiobutton(
            self, text="Two Way ANOVA", variable=self.model, value=4
        )
        self.model_4.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
        '''

class MasterFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.columnconfigure(index=1, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=2, weight=1)


        self.setup() ;

    def setup(self):
        self.type_frame = TypeFrame(self, self)
        self.type_frame.grid(
            row=0, column=0, padx=(20,10), pady=(20,10), sticky="nsew"
        )

        self.separator = ttk.Separator(self)
        self.separator.grid(
            row=1, column=0, padx=(20,10), pady=10, sticky="ew"
        )

        self.model_frame = {}
        
        self.model_frame[0] = ModelFrame0(self)
        self.model_frame[0].grid(
            row=2, column=0, padx=(20,10), pady=10, sticky="nsew"
        )

        self.model_frame[1] = ModelFrame1(self)
        self.model_frame[1].grid(
            row=2, column=0, padx=(20,10), pady=10, sticky="nsew"
        )

        self.show_frame()
        

        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0,5), pady=(0,5))

    def show_frame(self):
        frame = self.model_frame[self.type_frame.type.get()]
        frame.tkraise()
        


        


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("BIOSTATS")

        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "dark")
        
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

        self.master_frame = MasterFrame(self)
        self.master_frame.grid(row=0, column=0, sticky="nsew")

        self.update()
        self.minsize(int(self.winfo_screenwidth() / 2), self.winfo_height())
        x_coordinate = int(self.winfo_screenwidth() / 4)
        y_coordinate = int((self.winfo_screenheight() / 2) - (self.winfo_height() / 2))
        self.geometry("+{}+{}".format(x_coordinate, y_coordinate-20))




if __name__ == "__main__":
    app = App()
    app.mainloop()
