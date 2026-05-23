import tkinter as tk
import math
from tkinter import ttk
from tkinter import messagebox

from stress import QMetric, get_stress_level 
from task import Task, Calendar
from panels import AddTaskPanel, EvaluateStressPanel, OverlayPanel
from widgets import RecommendationsWidget, ComingTasksWidget

MAX_STRESS_LEVEL = 21


class Dashboard(tk.Tk):
    def __init__(self):
        # Main setup
        super().__init__()
        self.title("MindCode")
        self.geometry("900x560")
        self.minsize(750,480)
        self.configure(bg="#111")
        self.calendar = Calendar() 
        self.stress_level = 14
        self.build_ui()



    def build_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.tasks_widget = ComingTasksWidget(self, self.calendar)
        self.tasks_widget.grid(row=0, column=0, sticky="nsew")

        # Ring
        center = tk.Frame(self, bg="#1a1a1a")
        center.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        center.rowconfigure(0, weight=1)
        center.columnconfigure(0, weight=1)

        self.ring_canvas = tk.Canvas(center, bg="#111")
        self.ring_canvas.grid(row=0, column=0, sticky="nsew")
        self.ring_canvas.bind("<Configure>", lambda e: self.update_ring())
        # Evaluate Stress Button
        tk.Button(center, text="Evaluar Estrés", bg="#e8001c", fg="white", command= self.open_questionnaire).grid(row=1, column=0, pady=10)

        # Suggestions and add task button
        right = tk.Frame(self, bg="#1a1a1a")
        right.grid(row=0, column=2, sticky="nsew")
        right.rowconfigure(0, weight=1)
        self.suggestions_widget = RecommendationsWidget(right)
        self.suggestions_widget.pack(fill=tk.BOTH, expand=True)

        tk.Button(right, text="Agregar Tarea", bg="#e8001c", fg="white", command= self.open_add_task).pack(fill=tk.X, padx=12, pady=12)

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


class CircularProgressBar(tk.Canvas):
    def __init__(self, parent, x0, y0, x1, y1, width=2, start_ang=90, full_extent=360):
        super().__init__(parent, width=x1-x0, height=y1-y0, bg="#111", highlightthickness=0)
        self.x0, self.y0, self.x1, self.y1 = x0+width, y0+width, x1-width, y1-width
        self.tx, self.ty = (x1-x0) // 2, (y1-y0) // 2
        self.width = width
        self.start_ang = start_ang
        self.full_extent = full_extent
        w2 = width // 2
        self.oval1 = self.create_oval(self.x0-w2, self.y0-w2,
                                      self.x1+w2, self.y1+w2)
        self.oval2 = self.create_oval(self.x0+w2, self.y0+w2,
                                      self.x1-w2, self.y1-w2)
        self.running = False
    
    def start(self, interval=100):
        pass

def draw_ring(canvas, x, y, radius, stress_level, thickness=32):
    stress_pts = stress_level.value / MAX_STRESS_LEVEL
    color = "#000000"
    match stress_level:
        case QMetric.BAJO:
            color = "#00ff00"
        case QMetric.MEDIO:
            color = "#ffff00"
        case QMetric.ALTO:
            color = "#ff0000"
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
    canvas.create_text(x, y - 20, text=f"{stress_level.name}", fill="white", font=("Arial", 16, "bold"))




if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()