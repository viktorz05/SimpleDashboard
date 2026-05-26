import tkinter as tk
from UI.RoundedFrame import RoundedFrame
from task import Calendar, Task
from stress import QMetric

BACKGROUND_COLOR = "#0f0f0f"
BUTTON_COLOR = "#e8001c"
TEXT_COLOR = "#ffffff"
SECONDARY_COLOR = "#1a1a1a"
ACCENT_COLOR = "#2a2a2a"

class RecommendationsWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        
        # Header
        header = tk.Frame(self, bg=BACKGROUND_COLOR)
        header.pack(fill=tk.X, padx=16, pady=(16, 12))
        tk.Label(header, text="💡 Recomendaciones", 
                 font=("Helvetica", 12, "bold"), 
                 bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(anchor="w")
        
        # Recommendations
        recommendations = [
            "🧘 Toma descansos regulares durante el estudio.",
            "🌬️ Practica técnicas de relajación.",
            "📅 Organiza tu tiempo para evitar sobrecarga.",
            "🥗 Alimentación saludable y ejercicio.",
            "👥 Busca apoyo social y convivencia."
        ]
        
        content = tk.Frame(self, bg=BACKGROUND_COLOR)
        content.pack(fill=tk.BOTH, expand=True, padx=12)
        
        for rec in recommendations:
            rec_frame = tk.Frame(content, bg=ACCENT_COLOR, highlightbackground="#3a3a3a", highlightthickness=1)
            rec_frame.pack(fill=tk.X, pady=6, padx=4)
            tk.Label(rec_frame, text=rec, 
                     font=("Helvetica", 9), 
                     bg=ACCENT_COLOR, fg="#ccc", wraplength=180, justify=tk.LEFT).pack(anchor="w", padx=12, pady=10)
# class ComingTasksWidget(tk.Frame):
#     def __init__(self, parent, calendar: Calendar):
#         super().__init__(parent)
#         self.calendar = calendar
#         tk.Label(self, text="Próximas Tareas", font=("Helvetica", 10, "bold"), bg=BACKGROUND_COLOR, fg="black").pack(pady=(18, 8))

#         self.task_list = tk.Frame(self, bg=BACKGROUND_COLOR)
#         self.task_list.pack(fill=tk.BOTH, expand=True, padx=8)

#         self.refresh()
    
#     def refresh(self):
#         for w in self.task_list.winfo_children():
#             w.destroy()
        
#         sorted_tasks = sorted(self.calendar.tasks.values(), key=lambda t: t.date)
#         for task in sorted_tasks:
#             color = {
#                 QMetric.BAJO: "#00e5a0",
#                 QMetric.MEDIO: "#ffd166",
#                 QMetric.ALTO: "#ff4d6d",
#             }.get(task.priority, "#00c8ff")
        
#             card = RoundedFrame(self.task_list, radius=12, bg=color, height = 60) 
#             card.pack(fill=tk.X, pady=4)

#             # tk.Label(card, text=task.name, font=("Helvetica", 9, "bold"), bg=BACKGROUND_COLOR, fg="black").pack(anchor=tk.W, padx=10, pady=(8,2))

#             # tk.Label(card, text=f"{task.date}\t . {task.est_time}h\t . {task.difficulty.name}",
#             #          font=("Helvetica", 8), bg=BACKGROUND_COLOR, fg=color).pack(anchor=tk.W, padx=10, pady=(0,8))
#             card.create_window(10, 12, anchor="nw",
#                    window=tk.Label(card, text=task.name,
#                                    font=("Courier New", 9, "bold"),
#                                    bg="#1e1e1e", fg="white"))
#             card.create_window(10, 36, anchor="nw",
#                    window=tk.Label(card, text=f"{task.date}  ·  {task.est_time}h",
#                                    font=("Courier New", 8),
#                                    bg="#1e1e1e", fg=color))
class ComingTasksWidget(tk.Frame):
    def __init__(self, parent, calendar: Calendar):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        self.calendar = calendar

        tk.Label(self, text="Próximas Tareas",
                 font=("Helvetica", 10, "bold"),
                 bg=BACKGROUND_COLOR, fg="white").pack(anchor="w", padx=12, pady=(14, 6))

        self.task_list = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=8)

        self.refresh()

    def refresh(self):
        for w in self.task_list.winfo_children():
            w.destroy()

        sorted_tasks = sorted(self.calendar.tasks.values(), key=lambda t: t.date)

        if not sorted_tasks:
            tk.Label(self.task_list, text="No hay tareas aún.",
                     font=("Courier New", 9), bg=BACKGROUND_COLOR,
                     fg="#555").pack(pady=20)
            return

        for task in sorted_tasks:
            self._build_card(self.task_list, task)

    def _build_card(self, parent, task):
        color = {
            QMetric.BAJO:  "#00e5a0",
            QMetric.MEDIO: "#ffd166",
            QMetric.ALTO:  "#ff4d6d",
        }.get(task.priority, "#555")

        card = tk.Frame(parent, bg=SECONDARY_COLOR,
                        highlightbackground=color,
                        highlightthickness=2)
        card.pack(fill=tk.X, pady=4)

        # Colored left bar
        tk.Frame(card, bg=color, width=4).pack(side=tk.LEFT, fill=tk.Y)

        body = tk.Frame(card, bg=SECONDARY_COLOR)
        body.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)

        # Row 1: task name + priority badge
        top = tk.Frame(body, bg=SECONDARY_COLOR)
        top.pack(fill=tk.X)
        tk.Label(top, text=task.name,
                 font=("Courier New", 10, "bold"),
                 bg=SECONDARY_COLOR, fg="white").pack(side=tk.LEFT)
        tk.Label(top, text=task.priority.label,
                 font=("Courier New", 7, "bold"),
                 bg=color, fg="black", padx=4, pady=1).pack(side=tk.RIGHT)

        # Row 2: date + time block
        mid = tk.Frame(body, bg=SECONDARY_COLOR)
        mid.pack(fill=tk.X, pady=(3, 0))
        tk.Label(mid, text=f"📅 {task.date}",
                 font=("Courier New", 8),
                 bg=SECONDARY_COLOR, fg="#888").pack(side=tk.LEFT)
        if task.time_block:
            tk.Label(mid, text=f"  🕐 {task.time_block}",
                     font=("Courier New", 8),
                     bg=SECONDARY_COLOR, fg="#888").pack(side=tk.LEFT)

        # Row 3: chips
        bot = tk.Frame(body, bg=SECONDARY_COLOR)
        bot.pack(fill=tk.X, pady=(4, 0))
        for chip_text, chip_color in [
            (f"⏱ {task.est_time}h",        "#333"),
            (f"⚡ {task.difficulty.label}", "#333"),
        ]:
            tk.Label(bot, text=chip_text,
                     font=("Courier New", 7),
                     bg=chip_color, fg="#aaa",
                     padx=5, pady=2).pack(side=tk.LEFT, padx=(0, 4))