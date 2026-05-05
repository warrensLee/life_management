from backend.routes import streaks  
from backend.services import parse_due_date

from tkinter import messagebox
import traceback
import customtkinter as ctk
from PIL import Image, ImageFilter, ImageEnhance

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

    def make_popping_emoji(self, path, size=(64, 64), glow_color=(255, 90, 40, 180)):
        img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)

        # use emoji alpha as the outline/glow shape
        alpha = img.getchannel("A")

        glow = Image.new("RGBA", size, glow_color)
        glow.putalpha(alpha)

        # bigger/softer glow behind emoji
        glow = glow.filter(ImageFilter.GaussianBlur(3))

        # slightly boost original emoji
        img = ImageEnhance.Color(img).enhance(1.25)
        img = ImageEnhance.Contrast(img).enhance(1.1)

        final = Image.alpha_composite(glow, img)

        return ctk.CTkImage(
            light_image=final,
            dark_image=final,
            size=size
        )

    def streak_refresh(self):
        # clear existing rows
        for _, _, row in self.streak_rows:
            row.destroy()
        self.streak_rows.clear()

        self.show_completed = ctk.BooleanVar(value=True)
        all_streaks = streaks.get_streaks(include_completed=self.show_completed.get())
        for s in all_streaks:
            row = ctk.CTkFrame(
                self.streak_list_frame,
                corner_radius=0,
                height=80
            )
            row.pack(fill="x", padx=10, pady=10)
            row.pack_propagate(False)

            # user signals the streak is complete for the day
            done_var_checkbox = ctk.BooleanVar(value=s.completed)
            chk = ctk.CTkCheckBox(row, text="", width=44, variable=done_var_checkbox, command=lambda sid=s.id, v=done_var_checkbox: self.toggle_streak_complete(sid, v))
            chk.pack(side="left", anchor="n", padx=(10, 0), pady=(30, 0))

            # left side with title, description, created at, and days completed
            left = ctk.CTkFrame(row, fg_color="transparent")
            left.pack(side="left", fill="y", expand=False, padx=(2, 0), pady=(10, 0))

            # currently just the emoji
            beside_left = ctk.CTkFrame(row, width=110, fg_color="transparent")
            beside_left.pack(side="left", anchor="n", padx=(0, 0), pady=(10, 0))
            beside_left.pack_propagate(False)

            # add space for furture calendar view
            spacer = ctk.CTkFrame(row, fg_color="transparent")
            spacer.pack(side="left", expand=True)
            
            # right side for delete button, emoji, and a future calendar view
            right = ctk.CTkFrame(row, fg_color="transparent", width=160)
            right.pack(side="right", fill="y", padx=12, pady=8)
            right.pack_propagate(False)

            emoji_path = "core/images/emojis/fire_3d.png" if s.completed else "core/images/emojis/seedling_3d.png"

            glow_color = (255, 120, 50, 200) if s.completed else (120, 255, 140, 180)

            emoji_img = self.make_popping_emoji(
                emoji_path,
                size=(64, 64),
                glow_color=glow_color
            )

            emoji_label = ctk.CTkLabel(
                beside_left,
                text="",
                image=emoji_img
            )
            emoji_label.image = emoji_img
            emoji_label.pack(anchor="n", pady=(0, 0))

            del_btn = ctk.CTkButton(
                right,
                text="Delete",
                width=70,
                command=lambda sid=s.id: self.delete_streak(sid)
            )
            del_btn.pack(side="right", anchor="n", padx=(0, 0), pady=(5, 0))

            #del_btn.pack(pady=(0, 4))

            # if there is no color selected, this is the default seleciton
            # it depends on complteion of the streak
            default_color = "#51E484"
            if s.completed:
                     default_color="#E47F51" 

            # title formatting and details
            title = ctk.CTkLabel(
                left,
                text=s.title,
                font=("Cooper Black", 28), 
                text_color=s.streak_color if hasattr(s, "streak_color") else default_color,
                anchor="w"
            )
            title.pack(anchor="w")

            # below title details, and their formatting
            details = ctk.CTkLabel(
                left,
                text=f"{s.description} • {s.created_at} • {s.days_completed} days",
                font=("Cooper Black", 24),
                text_color=s.streak_color if hasattr(s, "streak_color") else default_color,
                anchor="w"
            )
            details.pack(anchor="w", pady=(0, 0))

            self.streak_rows.append((s.id, done_var_checkbox, row))

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