import tkinter as tk
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, radius =10, bg="#F8E8EB", fg="black", hover_bg="#E8F8F5", width=200, height=40, **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.fg = fg
        self.hover_bg = hover_bg
        self._text = text
        self.command = command
        self._radius = radius
        self._w = width
        self._h = height
        self._draw(bg)
        self.bind("<Enter>", lambda e: self._draw(hover_bg))
        self.bind("<Leave>", lambda e: self._draw(bg))
        self.bind("<ButtonRelease>", lambda e: command())
    
    def _draw(self, fill):
        self.delete("all")
        r, w, h = self._radius, self._w, self._h
        self.create_polygon(r, 0, w-r, 0,
                            w, 0, w, r,
                            w, h-r, w, h,
                            w-r, h, r, h,
                            0, h, 0, h-r,
                            0, r, 0, 0,
                            smooth=True, fill=fill, outline="")
        self.create_text(w//2, h//2, text=self._text, fill=self.fg, font=("Helvetica", 10, "bold"))