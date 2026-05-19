import tkinter as tk
from tkinter import ttk

from stress import get_stress_level, QUESTIONS
from task import Task, Calendar

MAX_STRESS_LEVEL = 21

class Dashboard(tk.Tk):
    def __init__(self):
        # Main setup
        super().__init__()
        self.title("MindCode")
        self.geometry("800x600")
        self.minsize(600,600)
        # Widgets
        self.menu = Menu(self)
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)
        draw_ring(self.canvas, 400, 300, 100, 10)  # Example stress level
    
    def show_panel(self, name: str):
        pass

    def build_ui(self):
        # left = tk.Frame(self, bg="orange")
        pass


class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, background="red", text="Menu").pack(expand= True, fill=tk.BOTH)
        self.pack(side=tk.LEFT, fill=tk.Y)

class Button(ttk.Button):
    def __init__(self, parent, text):
        super().__init__(parent, text=text)
        self.pack()

def draw_ring(canvas, x, y, radius, stress_level):
    # Define colors based on stress level
    if stress_level < 7:
        color = "green"
    elif stress_level < 14:
        color = "yellow"
    else:
        color = "red"
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline=color)

class ComingTasksPanel(tk.Frame):
    def __init__(self, parent, calendar: Calendar):
        super().__init__(parent)
        tk.Label(self, text="Próximas Tareas", bg="red", fg="white").pack(pady=(18, 8))
        for task in calendar.tasks.values():
            row = tk.Frame(self, bg ="white")
            row.pack(fill=tk.X, pady=5)
            tk.Label(row, text=task.name, bg="white").pack(side=tk.LEFT, padx=10)
            tk.Label(row, text=task.date, bg="white").pack(side=tk.LEFT, padx=10)



if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()