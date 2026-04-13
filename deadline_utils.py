# deadline_utils.py
from datetime import datetime, date, timedelta

def get_deadline_status(due_date_str):
    try:
        due = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except:
        return ("•", "normal")  # fallback

    today = date.today()
    delta = (due - today).days

    if delta < 0:
        return ("⚠️", "overdue")
    elif delta == 0:
        return ("🔥", "today")
    elif delta == 1:
        return ("⏳", "tomorrow")
    elif delta <= 2:
        return ("⏳", "soon")
    else:
        return ("•", "normal")


def get_color_for_status(status, colors):
    if status == "overdue":
        return "#FF4B6E"  # red
    if status == "today":
        return "#FF8A3D"  # orange
    if status == "tomorrow":
        return "#FFC93D"  # yellow
    if status == "soon":
        return "#FFE08A"  # soft yellow
    return colors["text"]
