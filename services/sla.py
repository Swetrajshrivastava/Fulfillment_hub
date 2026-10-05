from datetime import datetime
import math


def classify_sla(due_at, priority, status, now=None):
    if status == "Shipped":
        return "Complete", None

    try:
        due_time = datetime.fromisoformat(str(due_at))
    except (TypeError, ValueError):
        return "Unknown", None

    minutes_remaining = (due_time - (now or datetime.now())).total_seconds() / 60
    if minutes_remaining <= 0:
        return "Delayed", minutes_remaining
    if minutes_remaining <= 30:
        return "Critical", minutes_remaining

    risk_window = 120 if priority == "High" else 60
    if minutes_remaining <= risk_window:
        return "At Risk", minutes_remaining
    return "On Track", minutes_remaining


def format_time_remaining(minutes):
    if minutes is None or not math.isfinite(minutes):
        return "-"
    if minutes <= 0:
        return f"{abs(int(minutes))} min overdue"
    if minutes < 60:
        return f"{int(minutes)} min"
    hours, remaining_minutes = divmod(int(minutes), 60)
    return f"{hours}h {remaining_minutes}m"