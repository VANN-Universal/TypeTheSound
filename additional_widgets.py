from tkinter import *
from tkinter.ttk import *
from style import *

class ScrollableFrame(Frame):
    def __init__(self, master, **kw):
        super(ScrollableFrame, self).__init__(master)
        height = 200
        if "height" in kw.keys():
            height = kw["height"]
        self.canvas = Canvas(self, background=bg, height=height)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.canvas_frame, width=e.width))
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind('<Enter>', self.bind_mouse_wheel)
        self.canvas.bind('<Leave>', self.unbind_mouse_wheel)

    def mouse_wheel(self, event):
        direction = (event.delta > 0) * 2 - 1
        self.canvas.yview_scroll(-direction, "units")

    def bind_mouse_wheel(self, _):
        self.canvas.bind_all("<MouseWheel>", self.mouse_wheel)

    def unbind_mouse_wheel(self, _):
        self.canvas.unbind_all("<MouseWheel>")