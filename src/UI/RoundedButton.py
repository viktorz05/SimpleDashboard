import tkinter as tk

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, radius=18,
                 bg="#e8001c", fg="white", hover_bg="#ff1a38",
                 width=200, height=40, **kwargs):
        
        super().__init__(parent, width=width, height=height,
                         bg=parent["bg"], highlightthickness=0)
        
        self._bg       = bg
        self._hover_bg = hover_bg
        self._fg       = fg
        self._text     = text
        self._command  = command
        self._radius   = radius
        
        self.btn_width  = width
        self.btn_height = height
        
        self.after(10, lambda: self._draw(bg))
        
        self.bind("<Enter>",          lambda e: self._draw(hover_bg))
        self.bind("<Leave>",          lambda e: self._draw(bg))
        self.bind("<ButtonRelease-1>", lambda e: command() if command else None)
    
    def _draw(self, fill):
        self.delete("all")
        r, w, h = self._radius, self.btn_width, self.btn_height
        
        # Draw rounded rectangle
        self.create_polygon(r, 0, w-r, 0,
                            w, 0, w, r,
                            w, h-r, w, h,
                            w-r, h, r, h,
                            0, h, 0, h-r,
                            0, r, 0, 0,
                            smooth=True, fill=fill, outline="")
        
        # Draw text with shadow effect
        self.create_text(w//2 + 1, h//2 + 1, text=self._text, fill="#00000030", font=("Helvetica", 11, "bold"))
        self.create_text(w//2, h//2, text=self._text, fill=self._fg, font=("Helvetica", 11, "bold"))