import tkinter as tk
from tkinter import ttk

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

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()