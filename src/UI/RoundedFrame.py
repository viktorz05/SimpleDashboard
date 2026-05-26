import tkinter as tk

class RoundedFrame(tk.Canvas):
    def __init__(self, parent, radius=14, bg="#1a1a1a", border="#2a2a2a", **kwargs):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0)
        self._radius = radius
        self._fill = bg
        self._border = border
        self.bind("<Configure>", self._redraw)

    def _redraw(self, event=None):
        self.delete("bg_rect")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 2 or h < 2:
            return
        r = self._radius
        self.create_polygon(r, 0, w-r, 0,
                            w, 0, w, r,
                            w, h-r, w, h,
                            w-r, h, r, h,
                            0, h, 0, h-r,
                            0, r, 0, 0,
                            smooth=True, fill=self._fill, outline=self._border, width=1, tags="bg_rect")