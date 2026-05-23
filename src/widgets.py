import tkinter as tk
from task import Calendar, Task
from stress import QMetric

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
        self.calendar = calendar
        tk.Label(self, text="Próximas Tareas", bg="red", fg="white").pack(pady=(18, 8))

        self.task_list = tk.Frame(self, bg ="#141414")
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
        
            card = tk.Frame(self.task_list, bg="#1e1e1e", highlightbackground="#2a2a2a", highlightthickness=1)
            card.pack(fill=tk.X, pady=4)

            tk.Label(card, text=task.name, font=("Helvetica", 9, "bold"), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=10, pady=(8,2))

            tk.Label(card, text=f"{task.date}\t . {task.est_time}h\t . {task.difficulty.name}",
                     font=("Helvetica", 8), bg="#1e1e1e", fg=color).pack(anchor=tk.W, padx=10, pady=(0,8))