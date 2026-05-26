import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from stress import get_stress_level 
from task import Task, Calendar
from stress import QMetric
from datetime import datetime

BACKGROUND_COLOR = "#0f0f0f"
BUTTON_COLOR = "#e8001c"
TEXT_COLOR = "#ffffff"
SECONDARY_COLOR = "#1a1a1a"
ACCENT_COLOR = "#2a2a2a"

class OverlayPanel(tk.Frame):
    def __init__(self, parent, title, on_close):
        super().__init__(parent, bg=SECONDARY_COLOR, highlightthickness=2, highlightbackground=ACCENT_COLOR)
        
        header = tk.Frame(self, bg=SECONDARY_COLOR)
        header.pack(fill=tk.X, padx=12, pady=(12,0))
        tk.Label(header, text=title, bg=SECONDARY_COLOR, fg=TEXT_COLOR, font=("Helvetica", 14, "bold")).pack(side=tk.LEFT)
        tk.Button(header, text="✕", bg=ACCENT_COLOR, fg=TEXT_COLOR, relief=tk.FLAT, cursor="hand2", font=("Helvetica", 12), command=on_close).pack(side=tk.RIGHT)
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=12, pady=8)

class AddTaskPanel(OverlayPanel):
    def __init__(self, parent, on_close, on_add):
        super().__init__(parent, "Agregar Tarea", on_close)
        self.on_add = on_add
        container = tk.Frame(self, bg=SECONDARY_COLOR)
        container.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        #Text
        tk.Label(container, text="Nombre", font=("Helvetica", 9, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR
                 ).pack(anchor=tk.W, pady=(10,4))
        self.name_entry = self.make_entry(container, "Submit")

        tk.Label(container, text="Fecha", font=("Helvetica", 9, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR
                 ).pack(anchor=tk.W, pady=(10,4))
        self.date_entry = self.make_entry(container, "YYYY-MM-DD")

        tk.Label(container, text="Tiempo estimado", font=("Helvetica", 9, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR
                 ).pack(anchor=tk.W, pady=(10,4))
        self.time_entry = self.make_entry(container, "e.g. 1.5")

        metric_options = [m.name for m in QMetric]
        tk.Label(container, text="Prioridad", font=("Helvetica", 9, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR
                 ).pack(anchor=tk.W, pady=(10,4))
        self.priority_var = tk.StringVar(value=metric_options[0])
        self.make_dropdown(container, self.priority_var, metric_options)

        tk.Label(container, text="Dificultad", font=("Helvetica", 9, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR
                 ).pack(anchor=tk.W, pady=(10,4))
        self.difficulty_var = tk.StringVar(value=metric_options[0])
        self.make_dropdown(container, self.difficulty_var, metric_options)

        tk.Label(container, text="Start time", font=("Helvetica", 9, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(10,2))
        self.start_entry = self.make_entry(container, "HH:MM  e.g. 16:00")

        tk.Label(container, text="End time", font=("Helvetica", 9, "bold"), bg=SECONDARY_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(10,2))
        self.end_entry = self.make_entry(container, "HH:MM  e.g. 18:00")

        tk.Button(container, text="Anadir tarea", font=("Helvetica", 10, "bold"), bg=BUTTON_COLOR, fg=TEXT_COLOR,
                  activeforeground=TEXT_COLOR, relief=tk.FLAT, cursor="hand2", pady=6, command=self._add).pack(fill=tk.X, pady=12)
        
    
    def make_entry(self, parent, placeholder):
        entry = tk.Entry(parent, font=("Helvetica", 10), bg=ACCENT_COLOR, fg="#888" ,insertbackground=TEXT_COLOR, relief='flat')
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e, en=entry, ph=placeholder : 
                   (en.delete(0, tk.END), en.config(fg=TEXT_COLOR))
                   if en.get() == ph else None)
        entry.bind("<FocusOut>", lambda e, en=entry, ph=placeholder : 
                   (en.delete(0, ph), en.config(fg="#888"))
                   if en.get() == "" else None)
        entry.pack(fill=tk.X, ipady=8, pady=4)
        return entry



    def make_dropdown(self, parent, variable, options):
        om = tk.OptionMenu(parent, variable, *options)
        om.config(
            font=("Helvetica", 9, "bold"), bg=ACCENT_COLOR, fg=TEXT_COLOR, activebackground=BUTTON_COLOR, relief=tk.FLAT,
            highlightthickness=0
        
        )
        om["menu"].config(bg=ACCENT_COLOR, fg=TEXT_COLOR, font=("Helvetica", 9))
        om.pack(fill=tk.X, pady=4)

        

    def _add(self):
        name = self.name_entry.get()
        date = self.date_entry.get()
        time_str = self.time_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()

        if not name:
            messagebox.showwarning("Campo obligatorio. Por favor escribe el nombre")
            return
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Formato incorrecto", "La fecha debe ser YYYY-MM-DD")
            return
        try:
            est_time = float(time_str)
        except ValueError:
            messagebox.showwarning("Formato de tiempo incorrecto", "El tiempo estimado debe ser un numero")
            return
        
        for val, placeholder, label in [
            (start, "HH:MM  e.g. 16:00", "Start time"),
            (end,   "HH:MM  e.g. 18:00", "End time"),
        ]:
            if val != placeholder and val != "":
                try:
                    datetime.strptime(val, "%H:%M")
                except ValueError:
                    messagebox.showwarning("Bad time", f"{label} must be HH:MM")
                    return

        task = Task(
            name = name,
            date = date,
            priority = QMetric[self.priority_var.get()],
            difficulty = QMetric[self.difficulty_var.get()],
            est_time = est_time,
            s_time = None if start == "HH:MM  e.g. 16:00" else start,
            e_time = None if end == "HH:MM  e.g. 16:00" else end
        )
        self.on_add(task)

class EvaluateStressPanel(OverlayPanel):
    QUESTIONS = [
            "¿Te has sentido nervioso o estresado?",
            "¿Has sentido que no puedes controlar tus preocupaciones?",
            "¿Te has sentido sobrecargado de tareas? ",
            "¿Te has sentido incapaz de manejar tus responsabilidades? ",
            "¿Te has sentido frustrado por situaciones fuera de tu control? "
        ]
    SCALE = ["Nunca", "Casi Nunca", "A Veces", "Frecuentemente", "Muy Frecuentemente"]
    def __init__(self, parent, on_close, on_submit):
        super().__init__(parent, "Evaluar Estrés", on_close)
        self.on_submit = on_submit
        self.answers = []
        container = tk.Frame(self, bg=SECONDARY_COLOR)
        container.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        for i, question in enumerate(self.QUESTIONS):
            tk.Label(container, text=f"{i+1}. {question}", 
                     wraplength=300, justify=tk.LEFT, 
                     bg=SECONDARY_COLOR, fg=TEXT_COLOR, font=("Helvetica", 9, "bold")).pack(anchor=tk.W, pady=(12, 8))
            var = tk.IntVar(value=0)
            self.answers.append(var)
            btn_row = tk.Frame(container, bg=SECONDARY_COLOR)
            btn_row.pack(anchor=tk.W, padx=12, pady=(0, 12))
            for val, label in enumerate(self.SCALE):
                tk.Radiobutton(btn_row, text=label, variable=var, 
                               value=val, bg=SECONDARY_COLOR, fg=TEXT_COLOR, selectcolor=BUTTON_COLOR, activebackground=SECONDARY_COLOR, activeforeground=BUTTON_COLOR,
                               font=("Helvetica", 8)).pack(side=tk.LEFT, padx=4)
        
        submit_btn = tk.Button(self, text="Calcular Estrés", font=("Helvetica", 10, "bold"), bg=BUTTON_COLOR, fg=TEXT_COLOR, relief=tk.FLAT, cursor="hand2", command=self.calculate_stress)
        submit_btn.pack(pady=12, fill=tk.X, padx=12)

    def calculate_stress(self):
        total = [entry.get() for entry in self.answers]
        stress_level = get_stress_level(total)
        self.on_submit(stress_level)
        print(f"Nivel de estrés: {stress_level}")

