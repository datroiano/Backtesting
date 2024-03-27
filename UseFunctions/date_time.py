from datetime import datetime, timedelta, date
import time


def to_unix_time(datetime_str):
    try:
        dt_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return int(time.mktime(dt_obj.timetuple()) * 1000)
    except ValueError:
        return None  # Catch the error properly in use-case


def from_unix_time(unix_time_str):
    try:
        unix_time_ms = int(unix_time_str)
        dt_obj = datetime.fromtimestamp(unix_time_ms / 1000.0)
        formatted_datetime = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_datetime
    except ValueError:
        return None


def previous_day(input_date):
    date_obj = datetime.strptime(input_date, '%Y-%m-%d')
    if date_obj.weekday() in [0, 6, 5]:  # Monday is 0, Sunday is 6, Saturday is 5
        previous_date = date_obj - timedelta(days=(date_obj.weekday() + 3) % 7)
    else:
        previous_date = date_obj - timedelta(days=1)
    return previous_date.strftime('%Y-%m-%d')


def unix_time_to_time_past_midnight(unix_time_ms):
    timestamp = datetime.fromtimestamp(unix_time_ms / 1000.0)
    midnight = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
    time_past_midnight = timestamp - midnight
    hours = time_past_midnight.seconds // 3600
    minutes = (time_past_midnight.seconds % 3600) // 60
    seconds = time_past_midnight.seconds % 60
    return hours, minutes, seconds


def unix_ms_to_seconds_since_midnight(unix_time_str):
    unix_seconds = unix_time_str / 1000
    date_time = datetime.fromtimestamp(unix_seconds)
    midnight_time = datetime(date_time.year, date_time.month, date_time.day)
    seconds_since_midnight = (date_time - midnight_time).total_seconds()
    return seconds_since_midnight


def seconds_since_midnight_to_readable_time(seconds_since_midnight):
    hours = int(seconds_since_midnight // 3600)
    minutes = int((seconds_since_midnight % 3600) // 60)
    seconds = int(seconds_since_midnight % 60)
    time_string = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    return time_string


def readable_time_to_seconds_since_midnight(readable_time):
    hours, minutes, seconds = map(int, readable_time.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def two_date_period(months_since_yesterday: int) -> tuple:
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    target_date = yesterday - timedelta(days=months_since_yesterday * 30)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    target_date_str = target_date.strftime('%Y-%m-%d')
    return yesterday_str, target_date_str


def get_date_next_friday(input_date=None):
    if input_date is None:
        today = date.today()
    else:
        today = datetime.strptime(input_date, '%Y-%m-%d').date()

    days_until_friday = (4 - today.weekday()) % 7  # Calculate days until next Friday (0=Monday, 1=Tuesday)
    if days_until_friday == 0:
        days_until_friday = 7  # If today is Friday, move to next Friday
    next_friday_date = today + timedelta(days=days_until_friday)
    formatted_date = next_friday_date.strftime('%Y-%m-%d')

    return formatted_date


def next_third_friday(input_date):
    date_obj = datetime.strptime(input_date, '%Y-%m-%d')
    day_of_week = date_obj.weekday()
    days_until_friday = (4 - day_of_week) % 7
    first_friday = date_obj + timedelta(days=days_until_friday)
    third_friday = first_friday + timedelta(weeks=2)

    if third_friday.month != date_obj.month:
        next_month = date_obj.replace(day=1) + timedelta(days=32)
        third_friday = next_month.replace(day=1)

        while third_friday.weekday() != 4:
            third_friday += timedelta(days=1)

        third_friday += timedelta(weeks=2)

    return third_friday.strftime('%Y-%m-%d')
