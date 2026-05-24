import tkinter as tk
import math
from tkinter import ttk
from tkinter import messagebox

from stress import QMetric, get_stress_level 
from task import Task, Calendar
from panels import AddTaskPanel, EvaluateStressPanel, OverlayPanel
from widgets import RecommendationsWidget, ComingTasksWidget
from UI.RoundedButton import RoundedButton 
from UI.RoundedFrame import RoundedFrame 

MAX_STRESS_LEVEL = 20
BACKGROUND_COLOR = "#E8F8F5"
BUTTON_COLOR = "#F8E8EB"

class Dashboard(tk.Tk):
    def __init__(self):
        # Main setup
        super().__init__()
        self.title("MindCode")
        self.geometry("900x560")
        self.minsize(750,480)
        self.configure(bg=BACKGROUND_COLOR)
        self.calendar = Calendar() 
        self.stress_level = (0, QMetric.BAJO)
        self.build_ui()



    def build_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.tasks_widget = ComingTasksWidget(self, self.calendar)
        self.tasks_widget.grid(row=0, column=0, sticky="nsew")

        # Column 1 Ring
        center = tk.Frame(self, bg=BACKGROUND_COLOR)
        center.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        center.rowconfigure(0, weight=1)
        center.columnconfigure(0, weight=1)

        RING_SIZE = 200
        ring_wrapper = tk.Frame(center, width=RING_SIZE, height=RING_SIZE, bg=BACKGROUND_COLOR)
        ring_wrapper.grid(row=0, column=0)
        ring_wrapper.grid_propagate(False)
        ring_wrapper.pack_propagate(False)
        self.ring_canvas = tk.Canvas(ring_wrapper, width=RING_SIZE, height=RING_SIZE, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.ring_canvas.pack(fill=tk.BOTH, expand=True)
        self.ring_canvas.bind("<Configure>", self.update_ring)
        # Evaluate Stress Button
        # tk.Button(center, text="Evaluar Estrés", font=("Helvetica", 12, "bold"), bg=BUTTON_COLOR, fg="black", command= self.open_questionnaire).grid(row=1, column=0, pady=10)
        RoundedButton(center, text="Evaluar Estrés", command=self.open_questionnaire, width =220, height = 40, bg=BUTTON_COLOR, fg="black").grid(row=1, column=0, pady=10)

        # Suggestions and add task button
        right = tk.Frame(self, bg=BACKGROUND_COLOR)
        right.grid(row=0, column=2, sticky="nsew")
        right.rowconfigure(0, weight=1)
        self.suggestions_widget = RecommendationsWidget(right)
        self.suggestions_widget.pack(fill=tk.BOTH, expand=True)

        # tk.Button(right, text="Agregar Tarea", font=("Helvetica", 12, "bold"),bg=BUTTON_COLOR, fg="black", command= self.open_add_task).pack(fill=tk.X, padx=12, pady=12)
        RoundedButton(right, text="Agregar Tarea", command=self.open_add_task, width=220, height=40, bg=BUTTON_COLOR, fg="black").pack(fill=tk.X, padx=12, pady=12)

        self.overlay = None

    def open_add_task(self):
        self.show_overlay(AddTaskPanel, on_add=self.save_new_task)

    def open_questionnaire(self):
        self.show_overlay(EvaluateStressPanel, on_submit=self.set_stress_level)

    def save_new_task(self, task : Task):
        self.calendar.add_task(task)
        self.tasks_widget.refresh()
        self.close_overlay()

    def show_overlay(self, panel_class, *args, **kwargs):
        self.close_overlay()
        self.overlay = panel_class(self, on_close=self.close_overlay, *args, **kwargs)
        self.overlay.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.overlay.lift()

    def close_overlay(self):
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None

    def set_stress_level(self, level):
        self.stress_level = level
        self.update_ring()
        self.close_overlay()

    def update_ring(self, event=None):
        canvas = self.ring_canvas
        canvas.delete("all")
        cx = canvas.winfo_width() // 2
        cy = canvas.winfo_height() // 2
        r = min(cx, cy) - 20
        if r > 20:
            draw_ring(canvas, cx, cy, r, self.stress_level)

def draw_ring(canvas, x, y, radius, stress_level: tuple[int, QMetric], thickness=32):
    score, stress_metric = stress_level
    stress_pts = score / MAX_STRESS_LEVEL
    color = stress_metric.color
    extent = min(stress_pts * 360, 359.9)
    print(f"extent is: {extent}")
    x0, y0, x1, y1 = x - radius, y - radius, x + radius, y + radius
    t = thickness
    canvas.create_arc(x0, y0, x1, y1, start=0, extent=359.9, style=tk.ARC, outline="#330005", width=t)
    if extent > 0:
        canvas.create_arc(x0, y0, x1, y1, start=90, extent=-extent, style=tk.ARC, outline=color, width = t)
    r = t / 2
    cap_x1 = x
    cap_y1 = y - radius
    canvas.create_oval(cap_x1 - r, cap_y1 - r, cap_x1 + r, cap_y1 + r, fill=color, outline="")
    angle_rad = math.radians(90 - extent)
    dx = x + radius * math.cos(angle_rad)
    dy = y - radius * math.sin(angle_rad)
    canvas.create_oval(dx - r, dy - r, dx + r, dy + r, fill=color, outline="")
    canvas.create_text(x, y - 20, text=f"{stress_metric.label}", fill="white", font=("Arial", 16, "bold"))




if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()