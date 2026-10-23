from tkinter import *
from tkinter import ttk, messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import numpy as np

class GUI():
    def __init__(self, root: Tk, resolution:str):
        self.root = root
        
        self.root.title("Genetic algorithm")
        self.root.geometry(resolution)

        self._create_widgets()

    def _create_widgets(self):
        config_frame = ttk.LabelFrame(self.root, text=" Параметри ", padding=15)
        config_frame.pack(fill="x", padx=15, pady=10)

        plot_frame = ttk.Frame(self.root, padding=10)
        plot_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        #range
        ttk.Label(config_frame, text="Границі [a, b]:").grid(row=1, column=0, sticky="w", pady=5)

        range_subframe = ttk.Frame(config_frame)
        range_subframe.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.range_a_entry = ttk.Entry(range_subframe, width=13)
        self.range_a_entry.insert(0, "-10.0")
        self.range_a_entry.pack(side="left")

        self.range_b_entry = ttk.Entry(range_subframe, width=13)
        self.range_b_entry.insert(0, "10.0")
        self.range_b_entry.pack(side="left",padx=10)

        #buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=15, pady=5)

        self.init_btn = ttk.Button(btn_frame, text="Ініціалізувати", command=self.initialize)
        self.init_btn.pack(side="left", expand=True, fill="x", padx=2)

        self.step_btn = ttk.Button(btn_frame, text="Наступна ітерація", command=self.next_step, state="disabled")
        self.step_btn.pack(side="left", expand=True, fill="x", padx=2)

        #plot
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    def initialize(self):


        self.plotter()

    def next_step(self):

        
        self.plotter()

    def plotter(self, pivot = [0,0]):
        self.ax.clear()

        range_a, range_b = self._range

        x_vals = np.linspace(range_a, range_b, 300)
        y_vals = [self.algorithm._fitness(val) for val in x_vals]
        
        self.ax.plot(x_vals, y_vals, color="blue", label="f(x)", linewidth=2)

        self.ax.plot(pivot)

        x_padding = (range_b - range_a) * 0.05
        self.ax.set_xlim(range_a - x_padding, range_b + x_padding)

        y_min, y_max = min(y_vals), max(y_vals)
        y_padding = (y_max - y_min) * 0.1 if y_max != y_min else 1.0
        self.ax.set_ylim(y_min - y_padding, y_max + y_padding)

        self.ax.set_title("Графік методів рішення")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.legend(loc="upper right")
        self.ax.grid(True, linestyle="--", alpha=0.6)
        
        self.canvas.draw()