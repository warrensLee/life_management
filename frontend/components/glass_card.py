import customtkinter as ctk

class GlassCard(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color="#161A20",
            border_color="#303844",
            border_width=1,
            corner_radius=20,
            **kwargs
        )
