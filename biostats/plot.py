import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from biostats.widget import Option
from biostats import model

class Plot(ttk.Frame):

    def __init__(self, parent, master):
        
        # Initialize
        ttk.Frame.__init__(self, parent)
        self.master = master

        # Variable
        self.plot_type = ["", "Distribution", "Categorical", "Relational", "Multiple", "Others"]
        self.plot_list = {
            "Distribution" : ["", "Histogram", "Density Plot", "Cumulative Plot", "2D Histogram", "2D Density Plot"],
            "Categorical"  : ["", "Count Plot", "Strip Plot", "Swarm Plot", "Box Plot", "Boxen Plot", "Violin Plot", "Bar Plot"],
            "Relational"   : ["", "Scatter Plot", "Line Plot", "Regression Plot"],
            "Multiple"     : ["", "Ultimate Plot", "Pair Plot", "Joint Plot"],
            "Others"       : ["", "Heatmap", "FA Plot", "PCA Plot", "LDA Plot"]
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
        for i in range(4):
            self.option_label[i] = ttk.Label(self.option_frame)
            self.option_label[i].grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
            self.option[i] = Option(self.option_frame, self)
            self.option[i].grid(row=i, column=1, sticky="nsew")

        # Graph
        self.graph = plt.figure()
        self.canvas = FigureCanvasTkAgg(self.graph, master=self.graph_frame) 
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Shortcut
        self.bind("<Control-s>", lambda event: self.save())

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

            if plot == "Cumulative Plot":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Color:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(["None"]+self.master.data_col["cat"])
                self.option[1].grid()

            if plot == "2D Histogram":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["num"])
                self.option[1].grid()

                self.option_label[2].config(text="Color:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(["None"]+self.master.data_col["cat"])
                self.option[2].grid()
    
            if plot == "2D Density Plot":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["num"])
                self.option[1].grid()

                self.option_label[2].config(text="Color:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(["None"]+self.master.data_col["cat"])
                self.option[2].grid()

        if kind == "Categorical":

            if plot == "Count Plot":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["cat"])
                self.option[0].grid()

                self.option_label[1].config(text="Color:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(["None"]+self.master.data_col["cat"])
                self.option[1].grid()

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

            if plot == "Swarm Plot":
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

            if plot == "Box Plot":
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

            if plot == "Boxen Plot":
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

            if plot == "Violin Plot":
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

            if plot == "Bar Plot":
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
        
        if kind == "Relational":

            if plot == "Scatter Plot":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["num"])
                self.option[1].grid()

                self.option_label[2].config(text="Color:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(["None"]+self.master.data_col["cat"])
                self.option[2].grid()

            if plot == "Line Plot":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["num"])
                self.option[1].grid()

                self.option_label[2].config(text="Color:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(["None"]+self.master.data_col["cat"])
                self.option[2].grid()

            if plot == "Regression Plot":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["num"])
                self.option[1].grid()

        if kind == "Multiple":

            if plot == "Ultimate Plot":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data.columns.tolist())
                self.option[0].grid()

            if plot == "Pair Plot":
                self.option_label[0].config(text="Variable:")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Color:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(["None"]+self.master.data_col["cat"])
                self.option[1].grid()

                kind_list = ["scatter", "regression", "density", "histogram"]

                self.option_label[2].config(text="Kind:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(kind_list)
                self.option[2].grid()

            if plot == "Joint Plot":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["num"])
                self.option[1].grid()

                self.option_label[2].config(text="Color:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(["None"]+self.master.data_col["cat"])
                self.option[2].grid()

                kind_list = ["scatter", "regression", "density", "histogram", "hexagon"]

                self.option_label[3].config(text="Kind:")
                self.option_label[3].grid()
                self.option[3].radio_one_set(kind_list)
                self.option[3].grid()

        if kind == "Others":

            if plot == "Heatmap":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].radio_one_set(self.master.data_col["cat"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()

                self.option_label[2].config(text="Value:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["num"])
                self.option[2].grid()

            if plot == "FA Plot":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data_col["num"])
                self.option[0].grid()

                self.option_label[1].config(text="Factors:")
                self.option_label[1].grid()
                self.option[1].radio_one_set([])
                self.option[1].grid()
            
                self.option_label[2].config(text="Color:")
                self.option_label[2].grid()
                self.option[2].radio_one_set(self.master.data_col["cat"])
                self.option[2].grid()

                self.temp = ""

            if plot == "PCA Plot":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Color:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()

            if plot == "LDA Plot":
                self.option_label[0].config(text="X:")
                self.option_label[0].grid()
                self.option[0].check_more_set(self.master.data_col["num"])
                self.option[0].grid()
            
                self.option_label[1].config(text="Y:")
                self.option_label[1].grid()
                self.option[1].radio_one_set(self.master.data_col["cat"])
                self.option[1].grid()


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
                    self.graph = model.density_plot(self.master.data, x=x, smooth=smooth)
                else:
                    self.graph = model.density_plot(self.master.data, x=x, smooth=smooth, color=color)

            if plot == "Cumulative Plot":
                x = self.option[0].radio_one_get()
                color = self.option[1].radio_one_get()

                if not x:
                    return
                if not color:
                    return

                if color == "None":
                    self.graph = model.cumulative_plot(self.master.data, x=x)
                else:
                    self.graph = model.cumulative_plot(self.master.data, x=x, color=color)      

            if plot == "2D Histogram":
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
                    self.graph = model.histogram_2D(self.master.data, x=x, y=y)
                else:
                    self.graph = model.histogram_2D(self.master.data, x=x, y=y, color=color)

            if plot == "2D Density Plot":
                x = self.option[0].radio_one_get()
                y = self.option[1].radio_one_get()
                color = self.option[2].radio_one_get()

                if not x:
                    return
                if not y:
                    return
                if not color:
                    return
                if x == y:
                    return

                if color == "None":
                    self.graph = model.density_plot_2D(self.master.data, x=x, y=y)
                else:
                    self.graph = model.density_plot_2D(self.master.data, x=x, y=y, color=color)

        if kind == "Categorical":

            if plot == "Count Plot":
                x = self.option[0].radio_one_get()
                color = self.option[1].radio_one_get()

                if not x:
                    return
                if not color:
                    return

                if color == "None":
                    self.graph = model.count_plot(self.master.data, x=x)
                else:
                    self.graph = model.count_plot(self.master.data, x=x, color=color)

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
                    self.graph = model.strip_plot(self.master.data, x=x, y=y)
                else:
                    self.graph = model.strip_plot(self.master.data, x=x, y=y, color=color)

            if plot == "Swarm Plot":
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
                    self.graph = model.swarm_plot(self.master.data, x=x, y=y)
                else:
                    self.graph = model.swarm_plot(self.master.data, x=x, y=y, color=color)

            if plot == "Box Plot":
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
                    self.graph = model.box_plot(self.master.data, x=x, y=y)
                else:
                    self.graph = model.box_plot(self.master.data, x=x, y=y, color=color)

            if plot == "Boxen Plot":
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
                    self.graph = model.boxen_plot(self.master.data, x=x, y=y)
                else:
                    self.graph = model.boxen_plot(self.master.data, x=x, y=y, color=color)

            if plot == "Violin Plot":
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
                    self.graph = model.violin_plot(self.master.data, x=x, y=y)
                else:
                    self.graph = model.violin_plot(self.master.data, x=x, y=y, color=color)

            if plot == "Bar Plot":
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
                    self.graph = model.bar_plot(self.master.data, x=x, y=y)
                else:
                    self.graph = model.bar_plot(self.master.data, x=x, y=y, color=color)

        if kind == "Relational":

            if plot == "Scatter Plot":        
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
                    self.graph = model.scatter_plot(self.master.data, x=x, y=y)
                else:
                    self.graph = model.scatter_plot(self.master.data, x=x, y=y, color=color)

            if plot == "Line Plot":        
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
                    self.graph = model.line_plot(self.master.data, x=x, y=y)
                else:
                    self.graph = model.line_plot(self.master.data, x=x, y=y, color=color)

            if plot == "Regression Plot":        
                x = self.option[0].radio_one_get()
                y = self.option[1].radio_one_get()

                if not x:
                    return
                if not y:
                    return

                self.graph = model.regression_plot(self.master.data, x=x, y=y)

        if kind == "Multiple":

            if plot == "Ultimate Plot":
                variable = self.option[0].check_more_get()

                if not variable:
                    return

                self.graph = model.ultimate_plot(self.master.data, variable=variable)

            if plot == "Pair Plot":
                variable = self.option[0].check_more_get()
                color = self.option[1].radio_one_get()
                kind = self.option[2].radio_one_get()

                if not variable:
                    return
                if not color:
                    return
                if not kind:
                    return

                if color == "None":
                    self.graph = model.pair_plot(self.master.data, variable=variable, kind=kind)
                else:
                    self.graph = model.pair_plot(self.master.data, variable=variable, color=color, kind=kind)

            if plot == "Joint Plot":
                x = self.option[0].radio_one_get()
                y = self.option[1].radio_one_get()
                color = self.option[2].radio_one_get()
                kind = self.option[3].radio_one_get()

                if not x:
                    return
                if not y:
                    return
                if not color:
                    return
                if not kind:
                    return

                if color == "None":
                    self.graph = model.joint_plot(self.master.data, x=x, y=y, kind=kind)
                else:
                    self.graph = model.joint_plot(self.master.data, x=x, y=y, color=color, kind=kind)

        if kind == "Others":

            if plot == "Heatmap":
                x = self.option[0].radio_one_get()
                y = self.option[1].radio_one_get()
                value = self.option[2].radio_one_get()

                if not x:
                    return
                if not y:
                    return
                if not value:
                    return

                self.graph = model.heatmap(self.master.data, x=x, y=y, value=value)

            if plot == "FA Plot":
                x = self.option[0].check_more_get()

                if len(x) ==0 :
                    return

                if x != self.temp:
                    self.temp = x
                    self.option[1].radio_one_set([i+1 for i in range(len(x))])
                
                factors = self.option[1].radio_one_get()
                color = self.option[2].radio_one_get()

                if not factors:
                    return
                if not color:
                    return

                if color == "None":
                    self.graph = model.fa_plot(self.master.data, x=x, factors=factors)
                else:
                    self.graph = model.fa_plot(self.master.data, x=x, factors=factors, color=color)
                    
            if plot == "PCA Plot":
                x = self.option[0].check_more_get()
                color = self.option[1].radio_one_get()

                if len(x) ==0:
                    return
                if not color:
                    return
                
                if color == "None":
                    self.graph = model.pca_plot(self.master.data, x=x)
                else:
                    self.graph = model.pca_plot(self.master.data, x=x, color=color)

            if plot == "LDA Plot":
                x = self.option[0].check_more_get()
                y = self.option[1].radio_one_get()

                if len(x) ==0:
                    return
                if not y:
                    return
                
                self.graph = model.lda_plot(self.master.data, x=x, y=y)



        self.canvas = FigureCanvasTkAgg(self.graph, master=self.graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.update()
        self.focus()

    def save(self):

        filename = filedialog.asksaveasfilename(
            title="Save File", 
            filetypes=[
                ("PNG File", "*.png"), 
                ("JPEG File", "*.jpg"), 
                ("PDF File", "*.pdf"), 
                ("EPS File", "*.eps"),
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