import tkinter as tk
from task import Calendar, Task
from stress import QMetric
BACKGROUND_COLOR = "#E8F8F5"
BUTTON_COLOR = "#F8E8EB"
class RecommendationsWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Recomendaciones", font = ("Helvetica", 10, "bold"), bg=BACKGROUND_COLOR, fg="black").pack(pady=(18, 8))
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
        self.calendar = calendar
        tk.Label(self, text="Próximas Tareas", font=("Helvetica", 10, "bold"), bg=BACKGROUND_COLOR, fg="black").pack(pady=(18, 8))

        self.task_list = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=8)

        self.refresh()
    
    def refresh(self):
        for w in self.task_list.winfo_children():
            w.destroy()
        
        sorted_tasks = sorted(self.calendar.tasks.values(), key=lambda t: t.date)
        for task in sorted_tasks:
            color = {
                QMetric.BAJO: "#00e5a0",
                QMetric.MEDIO: "#ffd166",
                QMetric.ALTO: "#ff4d6d",
            }.get(task.priority, "#00c8ff")
        
            card = tk.Frame(self.task_list, bg=BACKGROUND_COLOR, highlightbackground="#2a2a2a", highlightthickness=1)
            card.pack(fill=tk.X, pady=4)

            tk.Label(card, text=task.name, font=("Helvetica", 9, "bold"), bg=BACKGROUND_COLOR, fg="black").pack(anchor=tk.W, padx=10, pady=(8,2))

            tk.Label(card, text=f"{task.date}\t . {task.est_time}h\t . {task.difficulty.name}",
                     font=("Helvetica", 8), bg=BACKGROUND_COLOR, fg=color).pack(anchor=tk.W, padx=10, pady=(0,8))