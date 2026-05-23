import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from stress import get_stress_level 
from task import Task, Calendar
from stress import QMetric
from datetime import datetime

class OverlayPanel(tk.Frame):
    def __init__(self, parent, title, on_close):
        super().__init__(parent, bg = "#1a1a1a", highlightthickness=2, highlightbackground="red")
        tk.Label(self, background="red", text="Menu").pack(expand= True, fill=tk.BOTH)
        header = tk.Frame(self, bg="#1a1a1a")
        header.pack(fill=tk.X, padx=12, pady=(12,0))
        tk.Label(header, text=title, bg="#1a1a1a", fg="white").pack(side=tk.LEFT)
        tk.Button(header, text="X", bg="#1a1a1a", fg="white", relief=tk.FLAT, cursor="hand2", command=on_close).pack(side=tk.RIGHT)
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=12, pady=8)

class AddTaskPanel(OverlayPanel):
    def __init__(self, parent, on_close, on_add):
        super().__init__(parent, "Agregar Tarea", on_close)
        self.on_add = on_add
        container = tk.Frame(self, bg="#1a1a1a")
        container.pack(fill=tk.BOTH, expand=True)

        #Text
        tk.Label(container, text="Nombre", font=("Helvetica", 9, "bold"), bg="#1a1a1a", fg="#aaa"
                 ).pack(anchor=tk.W, pady=(10,12))
        self.name_entry = self.make_entry(container, "Submit")

        tk.Label(container, text="Fecha", font=("Helvetica", 9, "bold"), bg="#1a1a1a", fg="#aaa"
                 ).pack(anchor=tk.W, pady=(10,12))
        self.date_entry = self.make_entry(container, "YYYY-MM-DD")

        tk.Label(container, text="Tiempo estimado", font=("Helvetica", 9, "bold"), bg="#1a1a1a", fg="#aaa"
                 ).pack(anchor=tk.W, pady=(10,12))
        self.time_entry = self.make_entry(container, "e.g. 1.5")

        metric_options = [m.name for m in QMetric]
        tk.Label(container, text="Prioridad", font=("Helvetica", 9, "bold"), bg="#1a1a1a", fg="#aaa"
                 ).pack(anchor=tk.W, pady=(10,12))
        self.priority_var = tk.StringVar(value=metric_options[0])
        self.make_dropdown(container, self.priority_var, metric_options)

        tk.Label(container, text="Dificultad", font=("Helvetica", 9, "bold"), bg="#1a1a1a", fg="#aaa"
                 ).pack(anchor=tk.W, pady=(10,12))
        self.difficulty_var = tk.StringVar(value=metric_options[0])
        self.make_dropdown(container, self.difficulty_var, metric_options)

        tk.Button(container, text="Anadir tarea", font=("Helvetica", 10, "bold"), bg="#e8001c", fg="white",
                  activeforeground="white", relief=tk.FLAT, cursor="hand2", pady=6, command=self._add).pack(fill=tk.X, padx=12, pady=12)
        
    
    def make_entry(self, parent, placeholder):
        entry = tk.Entry(parent, font=("Helvetica", 10), bg="#222", fg="#555" ,insertbackground="white", relief='flat')
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e, en=entry, ph=placeholder : 
                   (en.delete(0, tk.END), en.config(fg="white"))
                   if en.get() == ph else None)
        entry.bind("<FocusOut>", lambda e, en=entry, ph=placeholder : 
                   (en.delete(0, ph), en.config(fg="#555"))
                   if en.get() == "" else None)
        entry.pack(fill=tk.X, ipady=6, padx=6)
        return entry



    def make_dropdown(self, parent, variable, options):
        om = tk.OptionMenu(parent, variable, *options)
        om.config(
            font=("Helvetica", 9, "bold"), bg ="#222", fg="white", activebackground="#e8001c", relief=tk.FLAT,
            highlightthickness=0
        
        )
        om["menu"].config(bg="#222", fg="white", font=("Helvetica", 9))
        om.pack(fill=tk.X, padx=2)

        

    def _add(self):
        name = self.name_entry.get()
        date = self.date_entry.get()
        time_str = self.time_entry.get()

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

        task = Task(
            name = name,
            date = date,
            priority = QMetric[self.priority_var.get()],
            difficulty = QMetric[self.difficulty_var.get()],
            est_time = est_time
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
        tk.Label(self, text="Evaluar Estrés", bg="red", fg="white").pack(pady=(18, 8))
        self.on_submit = on_submit
        self.answers = []
        container = tk.Frame(self, bg="#1a1a1a")
        container.pack(fill=tk.BOTH, expand=True)

        for i, question in enumerate(self.QUESTIONS):
            tk.Label(container, text=f"{i+1}., {question}", 
                     wraplength= 320, justify=tk.LEFT, 
                     bg="#1a1a1a", fg="white").pack(anchor=tk.W, padx=10, pady=5)
            var = tk.IntVar(value=0)
            self.answers.append(var)
            btn_row = tk.Frame(container, bg="#1a1a1a")
            btn_row.pack(anchor=tk.W, padx=20)
            for val, label in enumerate(self.SCALE):
                tk.Radiobutton(btn_row, text=label, variable=var, 
                               value=val, bg="#1a1a1a", fg="white", 
                               selectcolor="#333333").pack(side=tk.LEFT, padx=5)
        submit_btn = tk.Button(self, text="Calcular Estrés", command=self.calculate_stress)
        submit_btn.pack(pady=10)

    def calculate_stress(self):
        total = [entry.get() for entry in self.answers]
        stress_level = get_stress_level(total)
        self.on_submit(stress_level)
        print(f"Nivel de estrés: {stress_level}")

