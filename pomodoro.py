# pomodoro.py

import tkinter as tk
import winsound
import time
import threading


class PomodoroWidget(tk.Frame):
    def __init__(self, parent, app, work_minutes=25, break_minutes=5, sound="Digital Beep"):
        super().__init__(parent, bg=app.colors["card"])
        self.app = app

        # Settings
        self.work_minutes = work_minutes
        self.break_minutes = break_minutes
        self.sound = sound

        # State
        self.is_running = False
        self.is_break = False
        self.total_seconds = self.work_minutes * 60
        self.remaining = self.total_seconds

        # Ring config (medium thickness)
        self.ring_thickness = 10
        self.ring_size = 160

        # Canvas for circular timer
        self.canvas = tk.Canvas(
            self,
            width=self.ring_size,
            height=self.ring_size,
            bg=app.colors["card"],
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(pady=10)

        # Time label in center
        self.time_label = tk.Label(
            self,
            text=self._format_time(self.remaining),
            font=("Inter", 18, "bold"),
            bg=app.colors["card"],
            fg=app.colors["text"]
        )
        self.time_label.pack(pady=(0, 8))

        # Controls
        btn_frame = tk.Frame(self, bg=app.colors["card"])
        btn_frame.pack(pady=4)

        self.start_btn = tk.Button(
            btn_frame, text="Start", command=self.start,
            bg=app.colors["card"], fg=app.colors["text"],
            bd=0
        )
        self.start_btn.pack(side="left", padx=6)

        self.reset_btn = tk.Button(
            btn_frame, text="Reset", command=self.reset,
            bg=app.colors["card"], fg=app.colors["text"],
            bd=0
        )
        self.reset_btn.pack(side="left", padx=6)

        # Initial draw
        self._draw_ring()

    # -------------------------
    # SETTINGS UPDATE METHODS
    # -------------------------

    def update_settings(self, work, brk):
        self.work_minutes = work
        self.break_minutes = brk
        if not self.is_running:
            self.is_break = False
            self.total_seconds = self.work_minutes * 60
            self.remaining = self.total_seconds
            self.time_label.config(text=self._format_time(self.remaining))
            self._draw_ring()

    def update_sound(self, sound):
        self.sound = sound

    # -------------------------
    # SOUND SYSTEM
    # -------------------------

    def play_sound(self, sound=None):
        sound = sound or self.sound

        sounds = {
            "Chime": (880, 200),
            "Soft Bell": (660, 300),
            "Pop": (1200, 80),
            "Digital Beep": (1000, 200),
        }

        freq, dur = sounds.get(sound, (1000, 200))

        def _beep():
            try:
                winsound.Beep(freq, dur)
            except Exception:
                print("Sound not supported on this OS")

        threading.Thread(target=_beep, daemon=True).start()

    # -------------------------
    # TIMER LOGIC
    # -------------------------

    def _format_time(self, sec):
        m = sec // 60
        s = sec % 60
        return f"{m:02d}:{s:02d}"

    def start(self):
        if not self.is_running:
            self.is_running = True
            self._tick()

    def reset(self):
        self.is_running = False
        self.is_break = False
        self.total_seconds = self.work_minutes * 60
        self.remaining = self.total_seconds
        self.time_label.config(text=self._format_time(self.remaining))
        self._draw_ring()

    def _tick(self):
        if not self.is_running:
            return

        if self.remaining > 0:
            self.remaining -= 1
            self.time_label.config(text=self._format_time(self.remaining))
            self._draw_ring()
            self.after(1000, self._tick)
        else:
            self.play_sound()
            self._switch_mode()

    def _switch_mode(self):
        # No long breaks — simple alternating cycle
        self.is_break = not self.is_break
        if self.is_break:
            self.total_seconds = self.break_minutes * 60
        else:
            self.total_seconds = self.work_minutes * 60

        self.remaining = self.total_seconds
        self.time_label.config(text=self._format_time(self.remaining))
        self._draw_ring()
        self._tick()

    # -------------------------
    # RING DRAWING
    # -------------------------

    def _draw_ring(self):
        self.canvas.delete("all")

        size = self.ring_size
        pad = self.ring_thickness // 2 + 4
        x0, y0 = pad, pad
        x1, y1 = size - pad, size - pad

        # Background ring (track)
        track_color = self.app.colors["accent_soft"]
        self.canvas.create_oval(
            x0, y0, x1, y1,
            outline=track_color,
            width=self.ring_thickness
        )

        # Progress ring
        if self.total_seconds > 0:
            progress = self.remaining / self.total_seconds
        else:
            progress = 0

        # Full circle = 360 degrees
        extent = 360 * progress

        # Work vs break color
        if self.is_break:
            ring_color = "#6ED6A0"  # mint/green
        else:
            ring_color = self.app.colors["accent"]  # lavender accent

        # Draw arc from top, clockwise
        self.canvas.create_arc(
            x0, y0, x1, y1,
            start=90, extent=-extent,
            style="arc",
            outline=ring_color,
            width=self.ring_thickness
        )
