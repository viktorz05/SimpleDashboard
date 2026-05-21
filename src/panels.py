import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from stress import get_stress_level 
from task import Task, Calendar

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
        fields = [
                ("Nombre", "e.g. Estudiar para el examen"),
                ("Fecha", "YYYY-MM-DD"),
                ("Prioridad", "Bajo, Medio, Alto"),
                ("Dificultad", "Bajo, Medio, Alto"),
                ("Tiempo Estimado (hrs)", "e.g. 2")
                ]
        self.answers = {}
        for label, placeholder in fields:
            tk.Label(container, text=label, bg="#1a1a1a", fg="white").pack(side=tk.LEFT, padx=10)
            entry = tk.Entry(container)
            entry.insert(0, placeholder)
            entry.bind("<FocusIn>", lambda e, en = entry, ph=placeholder: (en.delete(0, tk.END), en.config(fg="white") if en.get() == ph else None))
            entry.bind("<FocusOut>", lambda e, en = entry, ph=placeholder: (en.insert(0, ph), en.config(fg="gray") if en.get() == "" else None))
            entry.pack(fill=tk.X, ipadx=6, padx=2)
            self.answers[label] = (entry, placeholder)
        tk.Button(self, text="Agregar Tarea", bg="#e8001c", fg="white", command=self._add).pack(fill=tk.X, padx=12, pady=12)

    def _add(self):
        data = {}
        for label, (entry, placeholder) in self.answers:
            value = entry.get()
            data[label] = "" if value == placeholder else value
        if not data["Nombre"] or not data["Fecha"]:
            messagebox.showwarning("Error", "Nombre y Fecha son obligatorios.")
            return
        self.on_add(data)

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

