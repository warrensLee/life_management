# app.py
import customtkinter as ctk

from backend import database
from backend import services

from frontend.tabs.goals_tab import GoalsTab
from frontend.tabs.streaks_tab import StreaksTab

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("core/themes/green_theme.json")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Life Manager V1")
        self.geometry("1280x720")

        database.init_db()

        self.configure(fg_color="#070B11")

        self.tabs = ctk.CTkTabview(
            self,
            fg_color="#070B11",
            segmented_button_fg_color="#101720",
            segmented_button_selected_color="#166221",
            segmented_button_selected_hover_color="#1D7A2D",
            segmented_button_unselected_color="#101720",
            segmented_button_unselected_hover_color="#182536",
            corner_radius=24,
            border_width=0
        )
        self.tabs.grid(row=0, column=0, padx=16, pady=16, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        streaks_page = self.tabs.add("Streaks")
        goals_page = self.tabs.add("Goals")

        streaks_page.configure(fg_color="#070B11")
        goals_page.configure(fg_color="#070B11")

        self.streaks_tab = StreaksTab(streaks_page)
        self.goals_tab = GoalsTab(goals_page)


def run():
    App().mainloop()
