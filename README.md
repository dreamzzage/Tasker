========================================
            ## TASKER — Productivity Suite
========================================


Tasker is a modern, theme‑aware productivity application designed for focus, 
clarity, and daily structure. It includes a circular Pomodoro timer, a premium 
habit tracker, task management, deadline tracking, and a clean dashboard UI.

Built with Python + Tkinter, Tasker uses floating rounded cards, soft shadows, 
and a minimal SaaS‑style aesthetic.

----------------------------------------
FEATURES
----------------------------------------

1. Circular Pomodoro Timer
   - Smooth shrinking ring animation
   - Medium‑thickness progress arc
   - Lavender work mode / Mint break mode
   - Custom work/break durations
   - Selectable notification sounds
   - No long breaks (simple alternating cycle)

2. Premium Habit Tracker
   - Linear‑style floating habit cards
   - Animated checkmark toggle
   - Weekly dot strip (Mon–Sun)
   - Automatic streak calculation
   - Add/Delete habits
   - Stored in habit_data.json

3. Task Management
   - Add, edit, complete tasks
   - Daily task view
   - Persistent storage

4. Deadline Tracking
   - Add deadlines with dates
   - Automatic color‑coded urgency
   - Stored in data/ folder

5. Dashboard Overview
   - Today’s tasks
   - Deadlines
   - Stats summary
   - Pomodoro timer

6. Slide‑In Panels
   - Settings panel
   - Pomodoro settings
   - Calendar panel
   - Habit panel

7. Theme System
   - Lavender theme (light/dark)
   - Floating rounded cards
   - Soft shadows
   - Accent colors

----------------------------------------
REQUIREMENTS
----------------------------------------

Python 3.10+ recommended

Required modules:
- tkinter (built‑in)
- winsound (Windows only)
- json (built‑in)
- os, sys, datetime (built‑in)

----------------------------------------
RUNNING THE APP
----------------------------------------

Double‑click:
    main.py

Download from Releases
    Tasker_0.1.zip

Or run from terminal:
    python main.py

----------------------------------------
BUILDING THE EXECUTABLE
----------------------------------------

Use the included build script:

    build_tasker.bat

This script:
- Cleans old builds
- Runs PyInstaller
- Includes all project modules
- Excludes .bat files
- Uses icon.ico
- Outputs to: dist/main/

----------------------------------------
PROJECT STRUCTURE
----------------------------------------

tasker/
│
├── main.py
├── pomodoro.py
├── habit_tracker.py
├── deadline_utils.py
├── icon.ico
├── build.bat
├── script.bat (for cleaning __pycache__ folders, NOT included in build.bat)

----------------------------------------
SAVE LOCATIONS
----------------------------------------

General app data:
    tasker/data/

Habit tracker data:
    C:\Users\<USER>\AppData\Local\tasker\habit_data.json

----------------------------------------
LICENSE
----------------------------------------

This project is provided as-is for personal use.
You may modify or extend it freely.

----------------------------------------
AUTHOR
----------------------------------------

Created by Dreamzzage.
