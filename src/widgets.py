import tkinter as tk
from task import Calendar, Task

class RecommendationsWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Recomendaciones", bg="red", fg="white").pack(pady=(18, 8))
        recommendations = [
            "Toma descansos regulares durante el estudio.",
            "Practica técnicas de relajación como la respiración profunda.",
            "Organiza tu tiempo y tareas para evitar la sobrecarga.",
            "Mantén una alimentación saludable y haz ejercicio regularmente.",
            "Busca apoyo social hablando con amigos o familiares."
        ]
        # Placeholder for recommendations content
class ComingTasksWidget(tk.Frame):
    def __init__(self, parent, calendar: Calendar):
        super().__init__(parent)
        tk.Label(self, text="Próximas Tareas", bg="red", fg="white").pack(pady=(18, 8))
        for task in calendar.tasks.values():
            row = tk.Frame(self, bg ="white")
            row.pack(fill=tk.X, pady=5)
            tk.Label(row, text=task.name, bg="white").pack(side=tk.LEFT, padx=10)
            tk.Label(row, text=task.date, bg="white").pack(side=tk.LEFT, padx=10)
    
    def refresh(self):
        pass