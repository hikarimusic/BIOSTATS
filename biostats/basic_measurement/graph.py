import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Graph(ttk.Frame):

    def __init__(self, parent, master):

        ttk.Frame.__init__(self, parent)
        self.master = master

        self.setup()

    def setup(self):

        # Configure
        self.rowconfigure(index=1, weight=1)
        self.rowconfigure(index=3, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.configure(padding=(20,20))

        # Setting Bar
        self.setting_bar = ttk.Frame(self)
        self.setting_bar.grid(
            row=0, column=0, sticky="nsew"
        )
        self.setting_bar.columnconfigure(index=2, weight=1)

        self.percent_label = ttk.Button(self.setting_bar, text="Type")
        self.percent_label.grid(
            row=0, column=0, padx=(5,0), pady=5, sticky="nsew"
        )

        '''
        self.percent_spin = ttk.Spinbox(
            self.setting_bar, from_=1, to=99, increment=1, width=5, command=self.tree_update
        )
        self.percent_spin.set(88)
        self.percent_spin.grid(
            row=0, column=1, padx=5, pady=5, sticky="nsew"
        )
        '''
        
        # Figure
        self.fig = plt.Figure()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self) 
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=5, sticky="nsew")

        '''
        # Treeview
        self.treeview = ttk.Frame(self)
        self.treeview.grid(
            row=1, column=0, sticky="nsew"
        )
        self.treeview.rowconfigure(index=0, weight=1)
        self.treeview.columnconfigure(index=0, weight=1)

        self.scrollbar_1y = ttk.Scrollbar(self.treeview, orient="vertical")
        self.scrollbar_1y.grid(row=0, column=1, padx=(0,5), sticky="nsew")
        self.scrollbar_1x = ttk.Scrollbar(self.treeview, orient="horizontal")
        self.scrollbar_1x.grid(row=1, column=0, padx=(5,0), sticky="nsew")

        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=30)

        self.tree = ttk.Treeview(
            self.treeview, selectmode="none", height=14
        )
        self.tree.config(column=(1))
        self.tree.grid(row=0, column=0, padx=(5,0), sticky="nsew")

        self.tree.config(yscrollcommand=self.scrollbar_1y.set)
        self.scrollbar_1y.config(command=self.tree.yview)
        self.tree.config(xscrollcommand=self.scrollbar_1x.set)
        self.scrollbar_1x.config(command=self.tree.xview)

        self.tree.column("#0", width=0, stretch="no")
        self.tree.column(1, anchor="center")

        self.tree.heading("#0", text="Label", anchor="center")
        self.tree.heading(1, text="", anchor="center")

        self.open_state = {}
        '''

        # Control Bar
        self.control_bar = ttk.Frame(self)
        self.control_bar.grid(
           row=2, column=0, sticky="nsew"
        )
        self.control_bar.columnconfigure(index=1, weight=1)

        self.scientific = tk.IntVar()
        self.notation = ttk.Checkbutton(
            self.control_bar, text="Scientific", style="Switch.TCheckbutton"
        )
        self.notation.grid(
            row=0, column=0, padx=5, pady=5, sticky="nsew"
        )

        '''
        self.precision_label = ttk.Label(
            self.control_bar, text="Precision"
        )
        self.precision_label.grid(
            row=0, column=2, pady=5, sticky="nsew"
        )


        self.precision = ttk.Spinbox(
            self.control_bar, from_=1, to=99, increment=1, width=5, command=self.tree_update
        )
        self.precision.insert(0,1)
        self.precision.grid(
            row=0, column=3, padx=(5,15), pady=5, sticky="nsew"
        )
        '''

        # Shortcut
        self.bind("<Control-s>", lambda event: self.save())

        # Save
        self.save_button = ttk.Button(self, text="Save")
        self.save_button.config(command=self.save)
        self.save_button.grid(
            row=4, column=0, sticky="e"
        )

    def graph_update(self):

        self.fig.clear()

        # Prepare Data
        x1 = np.linspace(0.0, 5.0)
        y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
        x2 = np.linspace(0.0, 3.0)
        y2 = np.cos(2 * np.pi * x2) * np.exp(-x1)

        # ax1
        self.ax1 = self.fig.add_subplot(221)
        self.ax1.plot(x1, y1)
        #ax1.set_title('line plot')
        self.ax1.set_title(str(np.random.randint(100)))
        self.ax1.set_ylabel('Damped oscillation')

        # ax2
        ax2 = self.fig.add_subplot(222)
        ax2.scatter(x1, y1, marker='o')
        ax2.set_title('Scatter plot')

        # ax3
        ax3 = self.fig.add_subplot(223)
        ax3.plot(x2, y2)
        ax3.set_ylabel('Damped oscillation')
        ax3.set_xlabel('time (s)')

        # ax4
        ax4 = self.fig.add_subplot(224)
        ax4.scatter(x2, y2, marker='o')
        ax4.set_xlabel('time (s)')

        self.canvas.draw()

    def save(self):
        filename = filedialog.asksaveasfilename(
            title="Save File", 
            filetypes=[
                ("PNG File", "*.png"), 
                ("JPEG File", "*.jpg"), 
                ("PDF File", "*.pdf"), 
                ("All Files", "*")
            ],
            initialfile="Graph"
        )

        if filename:
            try:
                self.fig.savefig(filename)
            except:
                messagebox.showerror(
                    title="Error",
                    message="File could not be saved."
                )      





