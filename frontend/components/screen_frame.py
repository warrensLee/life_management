import customtkinter as ctk

SCREEN_BG = "#070B11"
SCREEN_PANEL = "#0F141C"
SCREEN_BORDER = "#2A3442"


class ScreenFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=SCREEN_PANEL,
            border_color=SCREEN_BORDER,
            border_width=1,
            corner_radius=28,
            **kwargs
        )