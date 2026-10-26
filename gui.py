from tkinter import *
from tkinter import ttk, messagebox

from matplotlib.figure import Figure # type: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # type: ignore

import numpy as np

from Methods.fitness import *
from Methods.methods import Method

class GUI():
    calculate = Method()

    def __init__(self, root: Tk, resolution:str):
        self.root = root
        
        self.root.title("Genetic algorithm")
        self.root.geometry(resolution)

        self.method_var = StringVar(value="bisection")

        self._create_widgets()

    def _create_widgets(self):
        config_frame = ttk.LabelFrame(self.root, text=" Параметри ", padding=15)
        config_frame.pack(fill="x", padx=15, pady=10)

        plot_frame = ttk.Frame(self.root, padding=10)
        plot_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        #precision
        ttk.Label(config_frame, text="Точність:").grid(row=0, column=0, sticky="w", pady=5)
        self.precision_entry = ttk.Entry(config_frame, width=30)
        self.precision_entry.insert(0, "0.001")
        self.precision_entry.grid(row=0, column=1, padx=10, pady=5)

        #range
        ttk.Label(config_frame, text="Границі [a, b]:").grid(row=1, column=0, sticky="w", pady=5)

        range_subframe = ttk.Frame(config_frame)
        range_subframe.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.range_a_entry = ttk.Entry(range_subframe, width=13)
        self.range_a_entry.insert(0, "-1.5")
        self.range_a_entry.pack(side="left")

        self.range_b_entry = ttk.Entry(range_subframe, width=13)
        self.range_b_entry.insert(0, "1.5")
        self.range_b_entry.pack(side="left",padx=10)

        methods_frame = ttk.LabelFrame(config_frame, text=" Оберіть метод ", padding=10)
        methods_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

        #bisection
        ttk.Radiobutton(
            methods_frame, 
            text="Метод половинного поділу (Bisection)", 
            variable=self.method_var, 
            value="bisection"
        ).pack(anchor="w", pady=2)

        # Newton
        ttk.Radiobutton(
            methods_frame, 
            text="Метод хорд (в розробці)", 
            variable=self.method_var, 
            value="chord",
            state="disabled" 
        ).pack(anchor="w", pady=2)

        # Newton
        ttk.Radiobutton(
            methods_frame, 
            text="Метод Ньютона (в розробці)", 
            variable=self.method_var, 
            value="newton",
            state="disabled" 
        ).pack(anchor="w", pady=2)

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
        try:
            range_a = float(self.range_a_entry.get())
            range_b = float(self.range_b_entry.get())

            self._range = (range_a, range_b)
            self._precision = float(self.precision_entry.get())

            self.selected_method = self.method_var.get()

            if self.selected_method in {"bisection", "chord"}:
                self.calculate.opposite_check(self._range)

            
        
            self.plotter()
            self.step_btn.config(state="normal")
        
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input values: {e}")
            self.step_btn.config(state="disabled")


    def next_step(self):
        match self.selected_method:
            case "bisection":
                self._range = self.calculate.bisection(self._range)
                print(f"range: {self._range}")

                _midpoint = self.calculate.midpoint(self._range[0], self._range[1])
                print(f"midpoint: x:{_midpoint}\ty:{fitness(_midpoint)}")

                self.plotter()
                self.draw_point(_midpoint, fitness(_midpoint))

                if abs(fitness(_midpoint)) < self._precision:
                    self.step_btn.config(state="disabled")

            case "chord":
                pass

            case "newton":
                pass
            
            case _: 
                print(f"Not implemented{self.selected_method}")

    def draw_point(self, x:float, y: float):
        self.ax.scatter([x], [y], color='red',s=100)
        self.canvas.draw()

    def plotter(self):
        self.ax.clear()

        range_a, range_b = self._range

        x_vals = np.linspace(range_a, range_b, 300)
        y_vals = [fitness(val) for val in x_vals]
        
        self.ax.plot(x_vals, y_vals, color="blue", label="f(x)", linewidth=2)

        x_padding = (range_b - range_a) * 0.05
        self.ax.set_xlim(range_a - x_padding, range_b + x_padding)

        y_min, y_max = min(y_vals), max(y_vals)
        y_padding = (y_max - y_min) * 0.1 if y_max != y_min else 1.0
        self.ax.set_ylim(y_min - y_padding, y_max + y_padding)

        self.ax.set_title("Графік метода")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.legend(loc="upper right")
        self.ax.grid(True, linestyle="--", alpha=0.6)
        
        self.canvas.draw()