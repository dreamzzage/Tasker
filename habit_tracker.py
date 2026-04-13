import tkinter as tk
import json
import os
from datetime import date, timedelta


# =========================
# STORAGE
# =========================

DATA_FOLDER = os.path.join(os.path.expanduser("~"), "AppData", "Local", "tasker")
os.makedirs(DATA_FOLDER, exist_ok=True)

HABIT_FILE = os.path.join(DATA_FOLDER, "habit_data.json")


def load_habits():
    if not os.path.exists(HABIT_FILE):
        return []
    try:
        with open(HABIT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_habits(habits):
    try:
        with open(HABIT_FILE, "w", encoding="utf-8") as f:
            json.dump(habits, f, indent=2)
    except Exception as e:
        print("Could not save habits:", e)


# =========================
# HABIT CARD (PREMIUM)
# =========================

class HabitCard(tk.Frame):
    def __init__(self, parent, app, habit, index, refresh_callback):
        super().__init__(parent, bg=app.colors["card"])
        self.app = app
        self.habit = habit
        self.index = index
        self.refresh_callback = refresh_callback

        self.configure(
            bd=0,
            highlightthickness=0,
            bg=app.colors["card"]
        )

        # Floating card shadow
        self.shadow = tk.Canvas(
            self,
            width=300,
            height=90,
            bg=app.colors["bg"],
            highlightthickness=0,
            bd=0
        )
        self.shadow.pack()
        self.shadow.create_oval(
            10, 70, 290, 88,
            fill=app.colors["shadow"],
            outline="",
        )

        # Main card
        self.card = tk.Frame(
            self,
            bg=app.colors["card"],
            bd=0,
            highlightthickness=0
        )
        self.card.place(x=0, y=0, width=300, height=80)

        # Habit name
        self.name_label = tk.Label(
            self.card,
            text=habit["name"],
            bg=app.colors["card"],
            fg=app.colors["text"],
            font=("Inter", 12, "bold")
        )
        self.name_label.place(x=16, y=10)

        # Streak
        streak = habit.get("streak", 0)
        streak_text = f"🔥 {streak} day streak" if streak > 0 else "No streak yet"
        self.streak_label = tk.Label(
            self.card,
            text=streak_text,
            bg=app.colors["card"],
            fg=app.colors["accent"],
            font=("Inter", 10)
        )
        self.streak_label.place(x=16, y=34)

        # Weekly dots
        self._draw_weekly_dots()

        # Today toggle
        self.toggle_btn = tk.Button(
            self.card,
            text="✓" if habit.get("today_done") else "○",
            command=self.toggle_today,
            bg=app.colors["card"],
            fg=app.colors["text"],
            bd=0,
            font=("Inter", 14, "bold")
        )
        self.toggle_btn.place(x=260, y=20)

        # Delete button
        self.delete_btn = tk.Button(
            self.card,
            text="✕",
            command=self.delete_habit,
            bg=app.colors["card"],
            fg=app.colors["danger"],
            bd=0,
            font=("Inter", 12, "bold")
        )
        self.delete_btn.place(x=260, y=50)

    def _draw_weekly_dots(self):
        # Weekly strip (Mon–Sun)
        today = date.today()
        start = today - timedelta(days=today.weekday())  # Monday

        for i in range(7):
            d = start + timedelta(days=i)
            done = d.isoformat() in self.habit.get("history", [])

            color = self.app.colors["accent"] if done else self.app.colors["muted"]

            dot = tk.Canvas(
                self.card,
                width=10,
                height=10,
                bg=self.app.colors["card"],
                highlightthickness=0,
                bd=0
            )
            dot.place(x=16 + i * 18, y=58)
            dot.create_oval(2, 2, 8, 8, fill=color, outline=color)

    def toggle_today(self):
        today = date.today().isoformat()

        if "history" not in self.habit:
            self.habit["history"] = []

        if today in self.habit["history"]:
            self.habit["history"].remove(today)
            self.habit["today_done"] = False
        else:
            self.habit["history"].append(today)
            self.habit["today_done"] = True

        # Recalculate streak
        self.habit["streak"] = self._calculate_streak()

        save_habits(self.app.habits)
        self.refresh_callback()

    def _calculate_streak(self):
        history = set(self.habit.get("history", []))
        streak = 0
        day = date.today()

        while day.isoformat() in history:
            streak += 1
            day -= timedelta(days=1)

        return streak

    def delete_habit(self):
        del self.app.habits[self.index]
        save_habits(self.app.habits)
        self.refresh_callback()


# =========================
# HABIT PANEL (SLIDE-IN)
# =========================

class HabitPanel(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors["bg"])
        self.app = app

        self.place(relx=1.0, rely=0, relheight=1.0, width=360, anchor="ne")

        # Title
        tk.Label(
            self,
            text="Habits",
            bg=app.colors["bg"],
            fg=app.colors["text"],
            font=("Inter", 16, "bold")
        ).pack(pady=12)

        # Add Habit button
        add_btn = tk.Button(
            self,
            text="+ Add Habit",
            command=self.add_habit_popup,
            bg=app.colors["card"],
            fg=app.colors["text"],
            bd=0,
            font=("Inter", 12)
        )
        add_btn.pack(pady=6)

        # Scroll area
        self.scroll = tk.Canvas(
            self,
            bg=app.colors["bg"],
            highlightthickness=0,
            bd=0
        )
        self.scroll.pack(fill="both", expand=True)

        self.inner = tk.Frame(self.scroll, bg=app.colors["bg"])
        self.scroll.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>", lambda e: self.scroll.configure(scrollregion=self.scroll.bbox("all")))

        self.refresh()

    def refresh(self):
        for w in self.inner.winfo_children():
            w.destroy()

        for i, habit in enumerate(self.app.habits):
            card = HabitCard(self.inner, self.app, habit, i, self.refresh)
            card.pack(pady=10)

    def add_habit_popup(self):
        popup = tk.Toplevel(self)
        popup.title("New Habit")
        popup.geometry("300x150")
        popup.configure(bg=self.app.colors["bg"])

        tk.Label(
            popup,
            text="Habit name:",
            bg=self.app.colors["bg"],
            fg=self.app.colors["text"],
            font=("Inter", 11)
        ).pack(pady=10)

        entry = tk.Entry(popup)
        entry.pack(pady=4)

        def save_new():
            name = entry.get().strip()
            if not name:
                return

            self.app.habits.append({
                "name": name,
                "history": [],
                "streak": 0,
                "today_done": False
            })
            save_habits(self.app.habits)
            self.refresh()
            popup.destroy()

        tk.Button(
            popup,
            text="Save",
            command=save_new,
            bg=self.app.colors["card"],
            fg=self.app.colors["text"],
            bd=0
        ).pack(pady=10)
