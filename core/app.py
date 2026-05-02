# app.py
import customtkinter as ctk

from backend import database
from backend import services

from frontend.tabs.goals_tab import GoalsTab
from frontend.tabs.streaks_tab import StreaksTab

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("core/app_theme.json")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        database.init_db()

        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=0, column=0, padx=16, pady=16, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.goals_tab = GoalsTab(self.tabs.add("Goals"))
        self.streaks_tab = StreaksTab(self.tabs.add("Streaks"))

    # def on_add(self):
    #     self.add_goal()
    #     self.add_streak()
    #     self.refresh()
            
    # def refresh(self):
    #     self.goal_refresh()
    #     self.streak_refresh()  # TODO: implement streak refresh similar to goal_refresh


def run():
    App().mainloop()
