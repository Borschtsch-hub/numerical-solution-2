from tkinter import *
from tkinter import ttk, messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Methods.fitness import *
from Methods.methods import Method

class GUI():
    calculate = Method()

    def __init__(self, root: Tk, resolution:str):
        self.root = root
        
        self.root.title("Genetic algorithm")
        self.root.geometry(resolution)

        self.method_var = StringVar(value="bisection")

        self.x_prev, self.x_curr = (None, None)

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
        self.range_a_entry.insert(0, "-1.35")
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

        # regula-falsi
        ttk.Radiobutton(
            methods_frame, 
            text="Метод хорд (secant)", 
            variable=self.method_var, 
            value="secant",
        ).pack(anchor="w", pady=2)

        # regula-falsi
        ttk.Radiobutton(
            methods_frame, 
            text="Метод хорд (regula-falsi)", 
            variable=self.method_var, 
            value="regula-falsi",
        ).pack(anchor="w", pady=2)

        # Newton
        ttk.Radiobutton(
            methods_frame, 
            text="Метод Ньютона (Newton)", 
            variable=self.method_var, 
            value="newton", 
        ).pack(anchor="w", pady=2)

        # single-point
        ttk.Radiobutton(
            methods_frame, 
            text="Метод простої ітерації (single-point)", 
            variable=self.method_var, 
            value="single-point", 
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

            if self.selected_method in {"bisection", "regula-falsi"}:
                self.calculate.opposite_check(self._range)

            if self.selected_method == "newton":
                self.x_curr = range_a
            elif self.selected_method == "single-point":
                self.x_curr = range_b
            elif self.selected_method == "secant":
                self.x_prev = range_a
                self.x_curr = range_b

            self.plotter()
            self.step_btn.config(state="normal")
        
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input values: {e}")
            self.step_btn.config(state="disabled")


    def next_step(self):
        match self.selected_method:
            case "bisection" | "regula-falsi":
                
                if self.selected_method == "bisection":
                    self._range = self.calculate.bisection(self._range)
                else:
                    self._range = self.calculate.regula_falsi(self._range)

                print(f"range: {self._range}")

                _midpoint = self.calculate.midpoint(self._range[0], self._range[1])
                y_val = fitness(_midpoint)
                print(f"point: x:{_midpoint}\ty:{y_val}")

                self.plotter()
                self.draw_point(_midpoint, y_val)

                if abs(y_val) < self._precision or abs(self._range[1] - self._range[0]) < self._precision:
                    self.step_btn.config(state="disabled")
                    messagebox.showinfo("Готово", f"Корінь знайдено: x = {_midpoint:.5f}")

            case "secant":
                try:
                    if self.x_prev is None or self.x_curr is None:
                        self.x_prev, self.x_curr = self._range

                    x_next, _ = self.calculate.secant(x_prev=self.x_prev,x_curr=self.x_curr)

                    self.x_prev = self.x_curr
                    self.x_curr = x_next

                    self.plotter()
                    self.draw_point(self.x_curr, fitness(self.x_curr))
                    self.draw_point(self.x_prev, fitness(self.x_prev))
                    self.draw_line([self.x_curr, self.x_prev],[fitness(self.x_curr), fitness(self.x_prev)])

                    if abs(fitness(self.x_curr)) < self._precision:
                        self.step_btn.config(state="disabled")
                        messagebox.showinfo("Готово", f"Корінь знайдено: x = {self.x_curr:.5f}")
                except (ZeroDivisionError, OverflowError) as e:
                    self.step_btn.config(state="disabled")
                    messagebox.showerror(
                        "Помилка збіжності", 
                        "Метод розходиться: значення занадто великі (Overflow) або похідна дорівнює нулю."
                    )
                    return

            case "newton" | "single-point":
                try:
                    if self.selected_method == "newton":
                        self.x_curr = self.calculate.newton(self.x_curr)
                    else:
                        self.x_curr = fitness_x(self.x_curr)
                    x_curr = self.x_curr

                    y_val = fitness(x_curr)
                    print(f"point: x:{x_curr}\ty:{y_val}")

                    self.plotter()
                    self.draw_point(x_curr, y_val)

                    if abs(y_val) < self._precision:
                        self.step_btn.config(state="disabled")
                        messagebox.showinfo("Готово", f"Корінь знайдено: x = {x_curr:.5f}")

                except (ZeroDivisionError, OverflowError) as e:
                    self.step_btn.config(state="disabled")
                    messagebox.showerror(
                        "Помилка збіжності", 
                        "Метод розходиться: значення занадто великі (Overflow) або похідна дорівнює нулю."
                    )
                    return

            case _: 
                print(f"Not implemented {self.selected_method}")

    def draw_point(self, x:float, y: float):
        self.ax.scatter([x], [y], color='red',s=100)
        self.canvas.draw()

    def draw_line(self, x_vals:list[float], y_vals: list[float]):
        self.ax.plot(x_vals, y_vals, 'o-', color='blue')
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