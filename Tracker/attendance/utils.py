import datetime

def is_working_day(date):
    return date.weekday() not in [5, 6]  # Cumartesi (5) ve Pazar (6)
