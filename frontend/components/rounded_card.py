import tkinter as tk
import customtkinter as ctk

class RoundedCard(tk.Canvas):
    def __init__(
        self,
        parent,
        height=115,
        bg="#0F141C",
        card_color="#101720",
        border_color="#263345",
        radius=24,
        **kwargs
    ):
        super().__init__(
            parent,
            height=height,
            bg=bg,
            highlightthickness=0,
            bd=0,
            **kwargs
        )

        self.card_color = card_color
        self.border_color = border_color
        self.radius = radius
        self.height = height

        self.content = ctk.CTkFrame(self, fg_color=card_color, corner_radius=0)

        self.bind("<Configure>", self.draw)

    def draw(self, event=None):
        self.delete("card")

        w = self.winfo_width()
        h = self.height
        r = self.radius

        # border
        self.create_round_rect(
            1, 1, w - 2, h - 2,
            r,
            fill=self.border_color,
            outline="",
            tags="card"
        )

        # inner fill
        self.create_round_rect(
            2, 2, w - 3, h - 3,
            r - 1,
            fill=self.card_color,
            outline="",
            tags="card"
        )

        self.create_window(
            16,
            0,
            anchor="nw",
            window=self.content,
            width=w - 32,
            height=h
        )

    def create_round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1,
        ]

        return self.create_polygon(points, smooth=True, splinesteps=24, **kwargs)