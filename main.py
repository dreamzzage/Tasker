import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
import calendar
from datetime import datetime, date
from habit_tracker import HabitPanel, load_habits, save_habits
from pomodoro import PomodoroWidget
from deadline_utils import get_deadline_status, get_color_for_status

# =========================
# THEME — Minimal Rounded Hybrid
# =========================

def get_theme_colors(theme="Lavender", dark=False):
    if theme == "Lavender":
        if dark:
            return {
                "bg": "#1A1824",
                "card": "#23212F",
                "accent": "#C9A7FF",
                "accent_soft": "#3A3455",
                "text": "#F5F1FF",
                "muted": "#A59BC8",
                "danger": "#FF6B81",
                "shadow": "#000000",
                "shadow_opacity": 0.22,
            }
        else:
            return {
                "bg": "#F5F3FF",
                "card": "#FFFFFF",
                "accent": "#C9A7FF",
                "accent_soft": "#E8DEFF",
                "text": "#2A2438",
                "muted": "#7A6F9B",
                "danger": "#FF4B6E",
                "shadow": "#000000",
                "shadow_opacity": 0.18,
            }
    return {
        "bg": "#F0F0F0",
        "card": "#FFFFFF",
        "accent": "#4A90E2",
        "accent_soft": "#D0E4FF",
        "text": "#222222",
        "muted": "#777777",
        "danger": "#E24A4A",
        "shadow": "#000000",
        "shadow_opacity": 0.18,
    }

def get_background(theme="Lavender", dark=False):
    colors = get_theme_colors(theme, dark)
    return colors["bg"], None

class ThemeManager:
    def __init__(self, colors):
        self.colors = colors

    def apply(self, widget):
        bg = self.colors["bg"]
        card = self.colors["card"]
        text = self.colors["text"]

        if isinstance(widget, tk.Frame):
            try: widget.configure(bg=bg)
            except: pass
        elif isinstance(widget, tk.Label):
            try: widget.configure(bg=bg, fg=text)
            except: pass
        elif isinstance(widget, tk.Button):
            try:
                widget.configure(
                    bg=card,
                    fg=text,
                    activebackground=self.colors["accent_soft"],
                    activeforeground=text,
                    bd=0,
                    relief="flat",
                )
            except: pass

        for child in widget.winfo_children():
            self.apply(child)

# =========================
# GLOBAL DATA PATHS
# =========================

DATA_FOLDER = os.path.join(os.path.expanduser("~"), "AppData", "Local", "tasker")
os.makedirs(DATA_FOLDER, exist_ok=True)

DATA_FILE = os.path.join(DATA_FOLDER, "adhd_app_data.json")
POMO_FILE = os.path.join(DATA_FOLDER, "pomodoro_settings.json")

# =========================
# MODELS + STORAGE
# =========================

class Task:
    def __init__(self, title, done=False, created=None):
        self.title = title
        self.done = done
        self.created = created or datetime.now().isoformat()

    def to_dict(self):
        return {
            "title": self.title,
            "done": self.done,
            "created": self.created,
        }

class Deadline:
    def __init__(self, title, due_date, done=False):
        self.title = title
        self.due_date = due_date
        self.done = done

    def to_dict(self):
        return {
            "title": self.title,
            "due_date": self.due_date,
            "done": self.done,
        }

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"tasks": [], "commissions": [], "completed_count": 0, "stickers": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"tasks": [], "commissions": [], "completed_count": 0, "stickers": []}

def save_data(tasks, commissions, completed_count, stickers):
    data = {
        "tasks": tasks,
        "commissions": commissions,
        "completed_count": completed_count,
        "stickers": stickers,
    }
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save your data.\n\n{e}")

def load_pomodoro_settings():
    if not os.path.exists(POMO_FILE):
        return {"work": 25, "break": 5, "sound": "Digital Beep"}
    try:
        with open(POMO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"work": 25, "break": 5, "sound": "Digital Beep"}

def save_pomodoro_settings(data):
    try:
        with open(POMO_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save Pomodoro settings.\n\n{e}")

# =========================
# ROUNDED CARDS + BUTTONS
# =========================

class RoundedCard(tk.Canvas):
    def __init__(self, parent, radius=16, bg="#FFFFFF",
                 shadow_color="#000000", shadow_opacity=0.18,
                 shadow_offset=(0, 8), **kwargs):
        super().__init__(parent, highlightthickness=0, bg=parent["bg"], bd=0, **kwargs)
        self.radius = radius
        self.card_color = bg
        self.shadow_color = shadow_color
        self.shadow_opacity = shadow_opacity
        self.shadow_offset = shadow_offset
        self.inner_frame = tk.Frame(self, bg=bg, bd=0, highlightthickness=0)
        self.bind("<Configure>", self._draw)

    def _hex_with_opacity(self, hex_color, opacity):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _draw(self, event=None):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w <= 0 or h <= 0:
            return

        r = self.radius
        sx, sy = self.shadow_offset
        shadow_fill = self._hex_with_opacity(self.shadow_color, self.shadow_opacity)

        self.create_rounded_rect(sx, sy, w, h, r, fill=shadow_fill, outline=shadow_fill)
        self.create_rounded_rect(0, 0, w - sx, h - sy, r, fill=self.card_color, outline=self.card_color)

        self.inner_frame.place(x=10, y=10, width=w - sx - 20, height=h - sy - 20)

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
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
        return self.create_polygon(points, smooth=True, **kwargs)

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, radius=18,
                 bg="#FFFFFF", fg="#2A2438", hover_bg="#E8DEFF",
                 font=("Inter", 11), padding_x=82, padding_y=22, **kwargs):
        super().__init__(parent, highlightthickness=0, bg=parent["bg"], bd=0, **kwargs)

        self.command = command
        self.radius = radius
        self.bg_color = bg
        self.fg_color = fg
        self.hover_bg = hover_bg
        self.font = font
        self.text = text
        self.padding_x = padding_x
        self.padding_y = padding_y

        self._draw_button(self.bg_color)

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", lambda e: self._draw_button(self.hover_bg))
        self.bind("<Leave>", lambda e: self._draw_button(self.bg_color))

    def _measure_text(self):
        temp = tk.Label(text=self.text, font=self.font)
        temp.update_idletasks()
        w, h = temp.winfo_width(), temp.winfo_height()
        temp.destroy()
        return w, h

    def _draw_button(self, fill_color):
        self.delete("all")
        tw, th = self._measure_text()

        w = tw + self.padding_x * 2
        h = th + self.padding_y * 2
        r = self.radius

        self.configure(width=w, height=h)
        self.create_rounded_rect(0, 0, w, h, r, fill=fill_color, outline=fill_color)
        self.create_text(w / 2, h / 2, text=self.text, fill=self.fg_color, font=self.font)

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
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
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_click(self, event):
        if self.command:
            self.command()

# =========================
# BASE PANEL
# =========================

class BasePanel(tk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app

    def open(self):
        self.place(relx=1.0, rely=0, relheight=1.0, width=360, anchor="ne")

    def close(self):
        self.place_forget()

    def apply_theme(self, colors):
        self.configure(bg=colors["bg"])

# =========================
# EDITORS
# =========================

class TaskEditor(tk.Toplevel):
    def __init__(self, app, callback):
        super().__init__(app.root)
        self.app = app
        self.callback = callback
        self.title("New Task")
        self.geometry("340x200")
        self.configure(bg=app.colors["bg"])

        tk.Label(
            self,
            text="Task title:",
            bg=app.colors["bg"],
            fg=app.colors["text"],
            font=("Inter", 11)
        ).pack(pady=(16, 6))

        self.entry = tk.Entry(self)
        self.entry.pack(fill="x", padx=24, pady=(0, 12))

        save_btn = RoundedButton(
            self, "Save",
            command=self.save_task,
            bg=self.app.colors["card"],
            fg=self.app.colors["text"],
            hover_bg=self.app.colors["accent_soft"]
        )
        save_btn.pack(pady=8)

    def save_task(self):
        title = self.entry.get().strip()
        if not title:
            messagebox.showwarning("Empty", "Please enter a task title.")
            return
        self.callback(Task(title))
        self.destroy()
# =========================
# POMODORO SETTINGS PANEL
# =========================

class PomodoroSettingsPanel(BasePanel):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, app, **kwargs)
        self.settings = load_pomodoro_settings()
        self.build()

    def build(self):
        c = self.app.colors

        card = RoundedCard(
            self, radius=16, bg=c["card"],
            shadow_color=c["shadow"], shadow_opacity=c["shadow_opacity"]
        )
        card.pack(fill="both", expand=True, padx=16, pady=16)
        inner = card.inner_frame

        tk.Label(
            inner, text="Pomodoro Settings",
            bg=c["card"], fg=c["text"],
            font=("Inter", 14, "bold")
        ).pack(pady=(8, 10))

        # Work duration
        tk.Label(inner, text="Work duration (minutes):",
                 bg=c["card"], fg=c["text"], font=("Inter", 11)).pack(pady=(4, 2))
        self.work_entry = tk.Entry(inner)
        self.work_entry.pack(fill="x", padx=16, pady=(0, 8))
        self.work_entry.insert(0, str(self.settings["work"]))

        # Break duration
        tk.Label(inner, text="Break duration (minutes):",
                 bg=c["card"], fg=c["text"], font=("Inter", 11)).pack(pady=(4, 2))
        self.break_entry = tk.Entry(inner)
        self.break_entry.pack(fill="x", padx=16, pady=(0, 12))
        self.break_entry.insert(0, str(self.settings["break"]))

        save_btn = RoundedButton(
            inner, "Save",
            command=self.save,
            bg=c["card"], fg=c["text"],
            hover_bg=c["accent_soft"]
        )
        save_btn.pack(pady=6)

        close_btn = RoundedButton(
            inner, "Close",
            command=self.app.close_panel,
            bg=c["card"], fg=c["text"],
            hover_bg=c["accent_soft"]
        )
        close_btn.pack(pady=(4, 8))

    def save(self):
        try:
            work = int(self.work_entry.get())
            brk = int(self.break_entry.get())
        except ValueError:
            messagebox.showwarning("Invalid", "Durations must be numbers.")
            return

        self.settings["work"] = work
        self.settings["break"] = brk
        save_pomodoro_settings(self.settings)

        # Update live Pomodoro widget
        self.app.dashboard.pomodoro_widget.update_settings(work, brk)

        messagebox.showinfo("Saved", "Pomodoro settings updated.")
        self.app.close_panel()


# =========================
# CALENDAR PANEL
# =========================

class CalendarPanel(BasePanel):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, app, **kwargs)
        self.today = date.today()
        self.year = self.today.year
        self.month = self.today.month
        self.build()

    def build(self):
        c = self.app.colors

        card = RoundedCard(
            self, radius=16, bg=c["card"],
            shadow_color=c["shadow"], shadow_opacity=c["shadow_opacity"]
        )
        card.pack(fill="both", expand=True, padx=16, pady=16)
        inner = card.inner_frame

        header = tk.Frame(inner, bg=c["card"])
        header.pack(fill="x", pady=(4, 8))

        prev_btn = tk.Button(header, text="<", command=self.prev_month)
        prev_btn.pack(side="left", padx=6)

        next_btn = tk.Button(header, text=">", command=self.next_month)
        next_btn.pack(side="right", padx=6)

        self.month_label = tk.Label(
            header,
            text=f"{calendar.month_name[self.month]} {self.year}",
            bg=c["card"], fg=c["text"],
            font=("Inter", 13, "bold")
        )
        self.month_label.pack()

        self.calendar_frame = tk.Frame(inner, bg=c["card"])
        self.calendar_frame.pack(fill="both", expand=True)

        self.draw_calendar()

        close_btn = RoundedButton(
            inner, "Close",
            command=self.app.close_panel,
            bg=c["card"], fg=c["text"],
            hover_bg=c["accent_soft"]
        )
        close_btn.pack(pady=10)

    def draw_calendar(self):
        for w in self.calendar_frame.winfo_children():
            w.destroy()

        c = self.app.colors
        cal = calendar.monthcalendar(self.year, self.month)

        # Weekday header
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, d in enumerate(days):
            tk.Label(
                self.calendar_frame, text=d,
                bg=c["card"], fg=c["text"],
                font=("Inter", 10, "bold")
            ).grid(row=0, column=i, padx=4, pady=4)

        # Calendar days
        for r, week in enumerate(cal, start=1):
            for col, day in enumerate(week):
                if day == 0:
                    tk.Label(self.calendar_frame, text="",
                             bg=c["card"]).grid(row=r, column=col)
                    continue

                date_str = f"{self.year}-{self.month:02d}-{day:02d}"
                deadlines_today = [
                    d for d in self.app.commissions if d.due_date == date_str
                ]

                color = c["text"]
                if deadlines_today:
                    color = c["danger"]

                btn = tk.Button(
                    self.calendar_frame,
                    text=str(day),
                    bg=c["card"], fg=color,
                    command=lambda ds=date_str: self.show_day(ds),
                    bd=0
                )
                btn.grid(row=r, column=col, padx=4, pady=4)

    def show_day(self, date_str):
        deadlines = [
            d.title for d in self.app.commissions if d.due_date == date_str
        ]
        if deadlines:
            messagebox.showinfo("Deadlines", "\n".join(deadlines))
        else:
            messagebox.showinfo("Deadlines", "No deadlines on this day.")

    def prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.month_label.config(text=f"{calendar.month_name[self.month]} {self.year}")
        self.draw_calendar()

    def next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.month_label.config(text=f"{calendar.month_name[self.month]} {self.year}")
        self.draw_calendar()


# =========================
# SETTINGS PANEL (with sound selector)
# =========================

class SettingsPanel(BasePanel):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, app, **kwargs)
        self.pomo_settings = load_pomodoro_settings()
        self.build()

    def build(self):
        c = self.app.colors

        card = RoundedCard(
            self, radius=16, bg=c["card"],
            shadow_color=c["shadow"], shadow_opacity=c["shadow_opacity"]
        )
        card.pack(fill="both", expand=True, padx=16, pady=16)
        inner = card.inner_frame

        tk.Label(
            inner, text="Settings",
            bg=c["card"], fg=c["text"],
            font=("Inter", 14, "bold")
        ).pack(pady=(8, 10))

        # Sound selector
        tk.Label(
            inner, text="Pomodoro Sound:",
            bg=c["card"], fg=c["text"],
            font=("Inter", 11)
        ).pack(pady=(4, 2))

        self.sound_var = tk.StringVar(value=self.pomo_settings["sound"])
        sounds = ["Chime", "Soft Bell", "Pop", "Digital Beep"]
        self.sound_menu = tk.OptionMenu(inner, self.sound_var, *sounds)
        self.sound_menu.pack(pady=(0, 8))

        preview_btn = tk.Button(
            inner, text="Preview",
            command=self.preview_sound,
            bg=c["card"], fg=c["text"], bd=0
        )
        preview_btn.pack(pady=(0, 10))

        save_sound_btn = RoundedButton(
            inner, "Save Sound",
            command=self.save_sound,
            bg=c["card"], fg=c["text"],
            hover_bg=c["accent_soft"]
        )
        save_sound_btn.pack(pady=6)

        # Delete completed tasks
        delete_completed_btn = RoundedButton(
            inner, "Delete Completed Tasks",
            command=self.delete_completed_tasks,
            bg=c["card"], fg=c["text"],
            hover_bg=c["accent_soft"]
        )
        delete_completed_btn.pack(pady=6)

        # Delete all data
        delete_data_btn = RoundedButton(
            inner, "Delete Data Folder",
            command=self.delete_data_folder,
            bg=c["card"], fg=c["text"],
            hover_bg=c["accent_soft"]
        )
        delete_data_btn.pack(pady=6)

        close_btn = RoundedButton(
            inner, "Close",
            command=self.app.close_panel,
            bg=c["card"], fg=c["text"],
            hover_bg=c["accent_soft"]
        )
        close_btn.pack(pady=(10, 8))

    def preview_sound(self):
        sound = self.sound_var.get()
        self.app.dashboard.pomodoro_widget.play_sound(sound)

    def save_sound(self):
        self.pomo_settings["sound"] = self.sound_var.get()
        save_pomodoro_settings(self.pomo_settings)
        self.app.dashboard.pomodoro_widget.update_sound(self.sound_var.get())
        messagebox.showinfo("Saved", "Sound updated.")

    def delete_completed_tasks(self):
        self.app.tasks = [t for t in self.app.tasks if not t.done]
        self.app.dashboard.today_big_widget.update_content()
        self.app.dashboard.stats_widget.update_stats()
        self.app.save()
        messagebox.showinfo("Completed Tasks Deleted", "All completed tasks have been removed.")

    def delete_data_folder(self):
        import shutil

        confirm = messagebox.askyesno(
            "Delete All Data",
            "This will delete ALL saved tasks, deadlines, stickers, and settings.\n\nAre you sure?"
        )
        if not confirm:
            return

        try:
            shutil.rmtree(DATA_FOLDER, ignore_errors=True)
            os.makedirs(DATA_FOLDER, exist_ok=True)

            self.app.tasks = []
            self.app.commissions = []
            self.app.completed_count = 0
            self.app.sticker_data = []

            self.app.dashboard.today_big_widget.update_content()
            self.app.dashboard.deadlines_widget.build()
            self.app.dashboard.stats_widget.update_stats()

            self.app.save()

            messagebox.showinfo("Data Deleted", "All saved data has been deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete data folder.\n\n{e}")


# =========================
# TODAY TASKS WIDGET
# =========================

class TodayTasksWidget(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors["card"])
        self.app = app

        self.listbox = tk.Listbox(
            self, activestyle="none", bd=0, highlightthickness=0,
            bg=app.colors["card"], fg=app.colors["text"],
            selectbackground=app.colors["accent_soft"],
            selectforeground=app.colors["text"],
            font=("Inter", 11)
        )
        self.listbox.pack(fill="both", expand=True, padx=8, pady=8)

        self.listbox.bind("<Double-Button-1>", self.toggle_done)
        self.listbox.bind("<Button-3>", self.right_click)

        self.update_content()

    def update_content(self):
        self.listbox.delete(0, tk.END)
        for t in self.app.tasks:
            if not t.done:
                self.listbox.insert(tk.END, f"• {t.title}")

    def toggle_done(self, event=None):
        idx = self.listbox.curselection()
        if not idx:
            return

        active = [i for i, t in enumerate(self.app.tasks) if not t.done]
        real_index = active[idx[0]]

        t = self.app.tasks[real_index]
        t.done = True
        self.app.completed_count += 1

        self.update_content()
        self.app.dashboard.stats_widget.update_stats()
        self.app.save()

    def right_click(self, event):
        idx = self.listbox.nearest(event.y)
        if idx < 0:
            return

        active = [i for i, t in enumerate(self.app.tasks) if not t.done]
        if idx >= len(active):
            return

        real_index = active[idx]

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Edit", command=lambda: self.app.open_panel(EditTaskPanel, task_index=real_index))
        menu.add_command(label="Delete", command=lambda: self.app.open_panel(DeleteConfirmPanel, kind="task", index=real_index))
        menu.tk_popup(event.x_root, event.y_root)


# =========================
# DEADLINES WIDGET
# =========================

class DeadlinesWidget(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors["card"])
        self.app = app

        self.listbox = tk.Listbox(
            self, activestyle="none", bd=0, highlightthickness=0,
            bg=app.colors["card"], fg=app.colors["text"],
            selectbackground=app.colors["accent_soft"],
            selectforeground=app.colors["text"],
            font=("Inter", 11)
        )
        self.listbox.pack(fill="both", expand=True, padx=8, pady=8)

        self.listbox.bind("<Double-Button-1>", self.toggle_done)
        self.listbox.bind("<Button-3>", self.right_click)

        self.build()

    def build(self):
        self.listbox.delete(0, tk.END)

        def parse(d):
            try:
                return datetime.strptime(d.due_date, "%Y-%m-%d").date()
            except:
                return date.max

        sorted_deadlines = sorted(self.app.commissions, key=parse)

        for d in sorted_deadlines:
            icon, urgency = get_deadline_status(d.due_date)
            color = get_color_for_status(urgency, self.app.colors)

            text = f"{icon} {d.title} ({d.due_date})"
            self.listbox.insert(tk.END, text)
            self.listbox.itemconfig(tk.END, fg=color)

    def toggle_done(self, event=None):
        idx = self.listbox.curselection()
        if not idx:
            return

        def parse(d):
            try:
                return datetime.strptime(d.due_date, "%Y-%m-%d").date()
            except:
                return date.max

        sorted_deadlines = sorted(enumerate(self.app.commissions), key=lambda x: parse(x[1]))
        original_index = sorted_deadlines[idx[0]][0]

        d = self.app.commissions[original_index]
        d.done = not d.done
        if d.done:
            self.app.completed_count += 1

        self.build()
        self.app.dashboard.stats_widget.update_stats()
        self.app.save()

    def right_click(self, event):
        idx = self.listbox.nearest(event.y)
        if idx < 0:
            return

        def parse(d):
            try:
                return datetime.strptime(d.due_date, "%Y-%m-%d").date()
            except:
                return date.max

        sorted_deadlines = sorted(enumerate(self.app.commissions), key=lambda x: parse(x[1]))
        original_index = sorted_deadlines[idx][0]

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Edit", command=lambda: self.app.open_panel(EditDeadlinePanel, deadline_index=original_index))
        menu.add_command(label="Delete", command=lambda: self.app.open_panel(DeleteConfirmPanel, kind="deadline", index=original_index))
        menu.tk_popup(event.x_root, event.y_root)


# =========================
# STATS WIDGET
# =========================

class StatsWidget(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors["card"])
        self.app = app

        self.label = tk.Label(
            self, text="", anchor="w",
            bg=app.colors["card"], fg=app.colors["text"],
            font=("Inter", 11)
        )
        self.label.pack(fill="x", padx=10, pady=(10, 4))

        self.completed_header = tk.Label(
            self, text="Completed tasks:", anchor="w",
            bg=app.colors["card"], fg=app.colors["text"],
            font=("Inter", 11, "bold")
        )
        self.completed_header.pack(fill="x", padx=10, pady=(6, 2))

        self.completed_list = tk.Label(
            self, text="", anchor="nw", justify="left",
            bg=app.colors["card"], fg=app.colors["text"],
            font=("Inter", 10)
        )
        self.completed_list.pack(fill="both", expand=True, padx=14, pady=(0, 10))

        self.update_stats()

    def update_stats(self):
        total_tasks = len(self.app.tasks)
        done_tasks = sum(1 for t in self.app.tasks if t.done)
        total_deadlines = len(self.app.commissions)
        done_deadlines = sum(1 for d in self.app.commissions if d.done)

        self.label.config(
            text=f"Tasks: {done_tasks}/{total_tasks} | "
                 f"Deadlines: {done_deadlines}/{total_deadlines} | "
                 f"Completed total: {self.app.completed_count}"
        )

        completed = [t.title for t in self.app.tasks if t.done]
        formatted = "\n".join(f"✔ {title}" for title in completed) if completed else "None yet"
        self.completed_list.config(text=formatted)



# =========================
# DASHBOARD GRID
# =========================

class DashboardGrid(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors["bg"])
        self.app = app

        # Pomodoro card
        self.pomodoro_card = RoundedCard(
            self, radius=16, bg=app.colors["card"],
            shadow_color=app.colors["shadow"], shadow_opacity=app.colors["shadow_opacity"]
        )
        self.pomodoro_card.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=12, pady=12)

        # Load Pomodoro settings
        settings = load_pomodoro_settings()
        self.pomodoro_widget = PomodoroWidget(
            self.pomodoro_card.inner_frame,
            app,
            work_minutes=settings["work"],
            break_minutes=settings["break"],
            sound=settings["sound"]
        )
        self.pomodoro_widget.pack(fill="both", expand=True)

        # Today tasks
        self.today_card = RoundedCard(
            self, radius=16, bg=app.colors["card"],
            shadow_color=app.colors["shadow"], shadow_opacity=app.colors["shadow_opacity"]
        )
        self.today_card.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=12, pady=12)
        self.today_big_widget = TodayTasksWidget(self.today_card.inner_frame, app)
        self.today_big_widget.pack(fill="both", expand=True)

        # Deadlines
        self.deadlines_card = RoundedCard(
            self, radius=16, bg=app.colors["card"],
            shadow_color=app.colors["shadow"], shadow_opacity=app.colors["shadow_opacity"]
        )
        self.deadlines_card.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)
        self.deadlines_widget = DeadlinesWidget(self.deadlines_card.inner_frame, app)
        self.deadlines_widget.pack(fill="both", expand=True)

        # Stats
        self.stats_card = RoundedCard(
            self, radius=16, bg=app.colors["card"],
            shadow_color=app.colors["shadow"], shadow_opacity=app.colors["shadow_opacity"]
        )
        self.stats_card.grid(row=1, column=1, sticky="nsew", padx=12, pady=12)
        self.stats_widget = StatsWidget(self.stats_card.inner_frame, app)
        self.stats_widget.pack(fill="both", expand=True)

        # Grid weights
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)

    def apply_theme(self, colors):
        self.configure(bg=colors["bg"])
        self.today_card.card_color = colors["card"]
        self.deadlines_card.card_color = colors["card"]
        self.stats_card.card_color = colors["card"]
        self.pomodoro_card.card_color = colors["card"]



# =========================
# TOP BAR (UPDATED)
# =========================

class TopBar(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(bg=app.colors["bg"])
        self.pack(fill="x", pady=(4, 0))

        # Pomodoro Settings
        self.pomo_btn = RoundedButton(
            self, "Pomodoro Settings",
            command=lambda: self.app.open_panel(PomodoroSettingsPanel),
            bg=app.colors["card"], fg=app.colors["text"],
            hover_bg=app.colors["accent_soft"],
            padding_x=82, padding_y=10
        )
        self.pomo_btn.pack(side="left", padx=6, pady=8)

        # Calendar
        self.calendar_btn = RoundedButton(
            self, "Calendar",
            command=lambda: self.app.open_panel(CalendarPanel),
            bg=app.colors["card"], fg=app.colors["text"],
            hover_bg=app.colors["accent_soft"],
            padding_x=82, padding_y=10
        )
        self.calendar_btn.pack(side="left", padx=6, pady=8)

        # NEW — Habits
        self.habits_btn = RoundedButton(
            self, "Habits",
            command=lambda: self.app.open_panel(HabitPanel),
            bg=app.colors["card"], fg=app.colors["text"],
            hover_bg=app.colors["accent_soft"],
            padding_x=82, padding_y=10
        )
        self.habits_btn.pack(side="left", padx=6, pady=8)

        # Add Deadline
        self.add_deadline_btn = RoundedButton(
            self, "+ Deadline",
            command=self.app.add_deadline,
            bg=app.colors["card"], fg=app.colors["text"],
            hover_bg=app.colors["accent_soft"]
        )
        self.add_deadline_btn.pack(side="right", padx=6, pady=8)

        # Add Task
        self.add_task_btn = RoundedButton(
            self, "+ Task",
            command=self.app.add_task,
            bg=app.colors["card"], fg=app.colors["text"],
            hover_bg=app.colors["accent_soft"]
        )
        self.add_task_btn.pack(side="right", padx=6, pady=8)

# =========================
# MAIN APP
# =========================

class ADHDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tasker")

        # Theme
        self.theme = "Lavender"
        self.dark = False

        bg, _ = get_background(self.theme, self.dark)
        self.colors = get_theme_colors(self.theme, self.dark)
        self.theme_manager = ThemeManager(self.colors)
        self.root.configure(bg=bg)

        # Load data
        data = load_data()
        self.tasks = [Task(**t) for t in data.get("tasks", [])]
        self.commissions = [Deadline(**c) for c in data.get("commissions", [])]
        self.completed_count = data.get("completed_count", 0)
        self.sticker_data = data.get("stickers", [])

        # Load habits
        self.habits = load_habits()

        # Active slide-in panel
        self.panel = None

        # Layout
        self.main_area = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_area.pack(fill="both", expand=True)

        self.topbar = TopBar(self.main_area, self)
        self.dashboard = DashboardGrid(self.main_area, self)
        self.dashboard.pack(fill="both", expand=True)

        # Bottom controls
        self.controls = tk.Frame(self.root, bg=self.colors["bg"])
        self.controls.pack(fill="x", side="bottom", pady=8)

        self.settings_btn = RoundedButton(
            self.controls, "Settings",
            command=lambda: self.toggle_panel(SettingsPanel),
            bg=self.colors["card"], fg=self.colors["text"],
            hover_bg=self.colors["accent_soft"],
            padding_x=82, padding_y=10
        )
        self.settings_btn.pack(side="right", padx=12)

        self.apply_theme()

    # -------------------------
    # THEME
    # -------------------------

    def apply_theme(self):
        bg, _ = get_background(self.theme, self.dark)
        self.colors = get_theme_colors(self.theme, self.dark)
        self.theme_manager = ThemeManager(self.colors)
        self.root.configure(bg=bg)
        self.theme_manager.apply(self.root)

        self.topbar.configure(bg=self.colors["bg"])
        self.dashboard.apply_theme(self.colors)
        self.controls.configure(bg=self.colors["bg"])

        if self.panel:
            self.panel.configure(bg=self.colors["bg"])
            try:
                self.panel.apply_theme(self.colors)
            except:
                pass

    # -------------------------
    # SAVE
    # -------------------------

    def save(self):
        tasks_data = [t.to_dict() for t in self.tasks]
        commissions_data = [c.to_dict() for c in self.commissions]
        save_data(tasks_data, commissions_data, self.completed_count, self.sticker_data)
        save_habits(self.habits)

    # -------------------------
    # PANEL SYSTEM
    # -------------------------

    def toggle_panel(self, panel_class, **kwargs):
        if self.panel and isinstance(self.panel, panel_class):
            self.close_panel()
            return
        self.open_panel(panel_class, **kwargs)

    def open_panel(self, panel_class, **kwargs):
        if self.panel:
            try:
                self.panel.place_forget()
            except:
                pass

        self.panel = panel_class(self.main_area, self, **kwargs)
        try:
            self.panel.apply_theme(self.colors)
        except:
            pass
        self.panel.place(relx=1.0, rely=0, relheight=1.0, width=360, anchor="ne")

    def close_panel(self):
        if self.panel:
            try:
                self.panel.place_forget()
            except:
                pass
            self.panel = None

    # -------------------------
    # TASKS
    # -------------------------

    def add_task(self):
        TaskEditor(self, self._add_task_callback)

    def _add_task_callback(self, task):
        self.tasks.append(task)
        self.dashboard.today_big_widget.update_content()
        self.dashboard.stats_widget.update_stats()
        self.save()

    # -------------------------
    # DEADLINES
    # -------------------------

    def add_deadline(self):
        DeadlineEditor(self, self._add_deadline_callback)

    def _add_deadline_callback(self, deadline):
        self.commissions.append(deadline)
        self.dashboard.deadlines_widget.build()
        self.dashboard.stats_widget.update_stats()
        self.save()



# =========================
# MAIN ENTRY POINT
# =========================

if __name__ == "__main__":
    root = tk.Tk()

    # Load icon
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "icon.ico")

    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception as e:
            print("Icon found but could not be loaded:", e)
    else:
        print("icon.ico not found in:", script_dir)

    # Windows taskbar icon
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ADHDTasker.App")
        except Exception as e:
            print("Could not set taskbar icon:", e)

    app = ADHDApp(root)
    root.mainloop()
