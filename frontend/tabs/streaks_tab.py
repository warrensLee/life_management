from backend.routes import streaks  
from backend.services import parse_due_date

from tkinter import messagebox
import traceback
import customtkinter as ctk

class StreaksTab(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="nsew")

        self.parent = parent
        self.build_streaks_tab(parent)
        self.refresh()

    def add_streak(self):
        title = self.streak_title_entry.get().strip()
        desc = self.streak_description_entry.get().strip()
        days = self.streak_days_entry.get().strip()
        due = self.streak_date_entry.get().strip()

        try:
            due = parse_due_date(due)
            streaks.add_streak(title, desc, days, due)
        except ValueError as e:
            messagebox.showwarning("Invalid", str(e))
            return
        except Exception as e:
            print("Error while adding streak:", e)
            traceback.print_exc()
            messagebox.showwarning("Invalid", str(e))
            return

        self.streak_title_entry.delete(0, "end")
        self.streak_description_entry.delete(0, "end")
        self.streak_days_entry.delete(0, "end")
        self.streak_date_entry.delete(0, "end")
        self.refresh()

    def streak_refresh(self):
        # clear existing rows
        for _, _, row in self.streak_rows:
            row.destroy()
        self.streak_rows.clear()

        self.show_completed = ctk.BooleanVar(value=True)
        all_streaks = streaks.get_streaks(include_completed=self.show_completed.get())
        for s in all_streaks:
            row = ctk.CTkFrame(self.streak_list_frame)
            row.pack(fill="x", padx=6, pady=6)

            done_var = ctk.BooleanVar(value=s.completed)
            chk = ctk.CTkCheckBox(row, text="", variable=done_var,
                                    command=lambda sid=s.id, v=done_var: self.toggle_streak_complete(sid, v))
            chk.pack(side="left", padx=(10, 6))

            lbl = ctk.CTkLabel(row, text=s.display(), anchor="w", font=self.streak_font_completed if s.completed
                else self.streak_font_active, text_color="#9ca3af" if s.completed else None)
            lbl.pack(side="left", padx=6, fill="x", expand=True)

            del_btn = ctk.CTkButton(
                row, text="Delete", width=70, command=lambda sid=s.id: self.delete_streak(sid))
            del_btn.pack(side="right", padx=10)

            self.streak_rows.append((s.id, done_var, row))

    def toggle_streak_complete(self, streak_id, var):
        try:
            if var.get():
                streaks.increment_streak(streak_id)
                streaks.set_streaks_completed(streak_id, True)
            else:
                streaks.set_streaks_completed(streak_id, False)
        finally:
            self.refresh()

    def delete_streak(self, streak_id):
        streaks.remove_streak(streak_id)
        self.refresh()

    def refresh(self):
        self.streak_refresh()

    def build_streaks_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        # Top input panel
        top = ctk.CTkFrame(parent)
        top.grid(row=0, column=0, padx=16, pady=16, sticky="ew")
        for i in range(6):
            top.grid_columnconfigure(i, weight=1)

        self.streak_font_title = ctk.CTkFont(size=18, weight="bold")
        self.streak_font_label = ctk.CTkFont(size=14)
        self.streak_font_entry = ctk.CTkFont(size=14)
        self.streak_font_button = ctk.CTkFont(size=14, weight="bold")
        self.streak_font_active = ctk.CTkFont(size=15, weight="normal")
        self.streak_font_completed = ctk.CTkFont(size=14, slant="italic")

        # input sections, their title and stylization
        ctk.CTkLabel(top, text="Title", font=self.streak_font_title).grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        ctk.CTkLabel(top, text="Description", font=self.streak_font_title).grid(
            row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        
        ctk.CTkLabel(top, text="Days Already Completed", font=self.streak_font_title).grid(
            row=0, column=2, padx=10, pady=(10, 0), sticky="w")
        
        ctk.CTkLabel(top, text="Start Date (YYYY-MM-DD)", font=self.streak_font_title).grid(
            row=0, column=3, padx=10, pady=(10, 0), sticky="w")
        
        # now for placeholder text and entry points
        self.streak_title_entry = ctk.CTkEntry(top, placeholder_text="Sleep On Time")
        self.streak_title_entry.grid(row=1, column=0, padx=8, pady=10, sticky="ew")

        self.streak_description_entry = ctk.CTkEntry(top, placeholder_text="Go to bed by 11:00 PM")
        self.streak_description_entry.grid(row=1, column=1, padx=8, pady=10, sticky="ew")

        self.streak_days_entry = ctk.CTkEntry(top, placeholder_text="3")
        self.streak_days_entry.grid(row=1, column=2, padx=8, pady=10, sticky="ew")

        self.streak_date_entry = ctk.CTkEntry(top, placeholder_text="2026-02-01")
        self.streak_date_entry.grid(row=1, column=3, padx=8, pady=10, sticky="ew")

        add_btn = ctk.CTkButton(top, text="Add Streak", command=self.add_streak)
        add_btn.grid(row=1, column=4, padx=8, pady=10, sticky="ew")

        refresh_btn = ctk.CTkButton(top, text="Refresh", command=self.refresh)
        refresh_btn.grid(row=1, column=5, padx=8, pady=10, sticky="ew")

        # Scrollable streaks list
        mid = ctk.CTkFrame(parent)
        mid.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")
        mid.grid_columnconfigure(0, weight=1)
        mid.grid_rowconfigure(0, weight=1)

        self.streak_list_frame = ctk.CTkScrollableFrame(mid)
        self.streak_list_frame.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

        self.streak_rows = []  # store tuples: (streak_id, completed_var, row_frame)