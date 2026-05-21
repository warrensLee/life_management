import customtkinter as ctk


class RoundedCard(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        height=125,
        bg="#0F141C",
        card_color="#101720",
        border_color="#263345",
        radius=24,
        border_width=1,
        **kwargs
    ):
        super().__init__(
            parent,
            fg_color=card_color,
            border_color=border_color,
            border_width=border_width,
            corner_radius=radius,
            height=height,
            **kwargs
        )

        self.pack_propagate(False)

        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=radius
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=12
        )