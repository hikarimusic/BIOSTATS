import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .widget import Option
from . import model

class Plot(ttk.Frame):

    def __init__(self, parent, master):
        
        # Initialize
        ttk.Frame.__init__(self, parent)
        self.master = master

        # Variable
        self.plot_type = ["", "Distribution", "Categorical"]
        self.plot_list = {
            "Distribution" : ["", "Histogram", "Density Plot"],
            "Categorical"  : ["", "Strip Plot"] 
        }
        self.plot_1 = tk.StringVar(value="Distribution")
        self.plot_2 = {}
        for t in self.plot_list:
            self.plot_2[t] = tk.StringVar(value=self.plot_list[t][1])

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

        self.graph_frame = ttk.Frame(self)
        self.graph_frame.grid(row=2, column=0, sticky="nsew")
        self.graph_frame.columnconfigure(index=0, weight=1)
        self.graph_frame.rowconfigure(index=0, weight=1)

        self.save_button = ttk.Button(self, text="Save")
        self.save_button.config(command=self.save)
        self.save_button.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        # Menu
        self.menu_1 = ttk.OptionMenu(
            self.menu_frame, self.plot_1, *self.plot_type, command=lambda e: self.plot_change()
        )
        self.menu_1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.menu_2 = {}
        for t in self.plot_list:
            self.menu_2[t] = ttk.OptionMenu(
                self.menu_frame, self.plot_2[t], *self.plot_list[t], command=lambda e: self.plot_change()
            )
            self.menu_2[t].grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
            self.menu_2[t].grid_remove()

        # Option
        self.option_label = {}
        self.option = {}
        for i in range(3):
            self.option_label[i] = ttk.Label(self.option_frame)
            self.option_label[i].grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
            self.option[i] = Option(self.option_frame, self)
            self.option[i].grid(row=i, column=1, sticky="nsew")

        # Graph
        self.graph = plt.figure()
        self.canvas = FigureCanvasTkAgg(self.graph, master=self.graph_frame) 
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")


        self.plot_change()


    def plot_change(self):

        for wid in self.menu_2.values():
            wid.grid_remove()
        for wid in self.option_label.values():
            wid.grid_remove()
        for wid in self.option.values():
            wid.grid_remove()
        self.canvas.get_tk_widget().grid_remove()
        plt.clf()
        plt.close()

        kind = self.plot_1.get()
        plot = self.plot_2[kind].get()

        self.menu_2[kind].grid()

        if kind == "Distribution":

            if plot == "Histogram":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Band:")
                self.option_label[1].grid()
                self.option[1].spin_one_set(1, 999, 1, 10, 6)
                self.option[1].grid()

                self.option_label[2].config(text="Color:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(["None"]+self.master.data_col["cat"])
                self.option[2].grid()
            
            if plot == "Density Plot":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Smooth:")
                self.option_label[1].grid()
                self.option[1].entry_one_set(1, 6)
                self.option[1].grid()

                self.option_label[2].config(text="Color:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(["None"]+self.master.data_col["cat"])
                self.option[2].grid()

        if kind == "Categorical":

            if plot == "Strip Plot":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["cat"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["num"])
                self.option[1].grid()

                self.option_label[2].config(text="Color:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(["None"]+self.master.data_col["cat"])
                self.option[2].grid()


        self.change()

    def change(self):

        self.canvas.get_tk_widget().grid_remove()
        plt.clf()
        plt.close()

        kind = self.plot_1.get()
        plot = self.plot_2[kind].get()

        if kind == "Distribution":

            if plot == "Histogram":
                x = self.option[0].radio_one_get()
                band = self.option[1].spin_one_get()
                color = self.option[2].radio_one_get()

                if not x:
                    return
                if not color:
                    return
                
                if color == "None":
                    self.graph = model.histogram(self.master.data, x=x, band=band)
                else:
                    self.graph = model.histogram(self.master.data, x=x, band=band, color=color)

            if plot == "Density Plot":
                x = self.option[0].radio_one_get()
                smooth = self.option[1].entry_one_get()
                color = self.option[2].radio_one_get()

                if not x:
                    return
                try:
                    smooth = float(smooth)
                    if smooth <= 0:
                        return
                except:
                    return
                if not color:
                    return

                if color == "None":
                    self.graph = model.density(self.master.data, x=x, smooth=smooth)
                else:
                    self.graph = model.density(self.master.data, x=x, smooth=smooth, color=color)
            
        if kind == "Categorical":

            if plot == "Strip Plot":
                x = self.option[0].radio_one_get()
                y = self.option[1].radio_one_get()
                color = self.option[2].radio_one_get()

                if not x:
                    return
                if not y:
                    return
                if not color:
                    return

                if color == "None":
                    self.graph = model.strip(self.master.data, x=x, y=y)
                else:
                    self.graph = model.strip(self.master.data, x=x, y=y, color=color)





        self.canvas = FigureCanvasTkAgg(self.graph, master=self.graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def save(self):

        filename = filedialog.asksaveasfilename(
            title="Save File", 
            filetypes=[
                ("PNG File", "*.png"), 
                ("JPEG File", "*.jpg"), 
                ("PDF File", "*.pdf"), 
                ("All Files", "*")
            ],
            initialfile="Plot"
        )
        if filename:
            try:
                self.graph.savefig(filename)
            except:
                messagebox.showerror(
                    title="Error",
                    message="File could not be saved."
                )  