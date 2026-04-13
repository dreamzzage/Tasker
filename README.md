## TASKER — Productivity Suite


Tasker is a modern, theme‑aware productivity application designed for focus, 
clarity, and daily structure. It includes a circular Pomodoro timer, a premium 
habit tracker, task management, deadline tracking, and a clean dashboard UI.

Built with Python + Tkinter, Tasker uses floating rounded cards, soft shadows, 
and a minimal SaaS‑style aesthetic.

FEATURES

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

REQUIREMENTS
----------------------------------------

Python 3.10+ recommended

Required modules:
- tkinter (built‑in)
- winsound (Windows only)
- json (built‑in)
- os, sys, datetime (built‑in)

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



SAVE LOCATIONS
----------------------------------------

General app data:
    tasker/data/

Habit tracker data:
    C:\Users\<USER>\AppData\Local\tasker\habit_data.json



LICENSE
----------------------------------------

This project is provided as-is for personal use.
You may modify or extend it freely.

IT License

Copyright (c) 2026 Dreamzzage

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



AUTHOR
----------------------------------------

Created by Dreamzzage.



CHANGELOG
========================================

Project: Tasker — Productivity Suite
Author: Dreamzzage
----------------------------------------

Version 1.3.0 — Circular Pomodoro + Habit Tracker
------------------------------------------------
• Added circular Pomodoro timer with medium-thickness ring
• Added animated shrinking ring for work/break cycles
• Added premium Linear-style Habit Tracker
• Added floating habit cards with shadows
• Added weekly dot strip (Mon–Sun)
• Added automatic streak calculation
• Added Add/Delete habit functionality
• Added slide-in Habit Panel
• Updated DashboardGrid to include new Pomodoro and Habit systems
• Updated TopBar with new “Habits” button
• Improved theme propagation across panels
• Improved StatsWidget integration
• Added build_tasker.bat for PyInstaller builds
• Added README.txt and LICENSE.txt

Version 1.2.0 — UI Modernization
--------------------------------
• Introduced RoundedCard system with soft shadows
• Added Lavender theme with accent colors
• Added Pomodoro settings panel
• Added Calendar panel
• Improved layout spacing and card elevation
• Added sticker and completion tracking

Version 1.1.0 — Deadlines + Tasks Upgrade
-----------------------------------------
• Added deadline urgency color coding
• Added deadline editor
• Added task editor
• Added Today Tasks widget
• Added Stats widget

Version 1.0.0 — Initial Release
-------------------------------
• Basic task management
• Basic deadline tracking
• Simple Pomodoro timer
• Basic theme support


