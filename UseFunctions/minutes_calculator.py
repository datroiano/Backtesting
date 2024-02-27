from datetime import datetime, timedelta, time


def minutes_within_range(start_datetime, end_datetime):
    trading_start_time = time(9, 30)
    trading_end_time = time(16, 0)

    total_minutes = 0

    current_datetime = start_datetime
    while current_datetime < end_datetime:
        current_date = current_datetime.date()
        current_time = current_datetime.time()

        # Check if current time is within trading hours
        if trading_start_time <= current_time <= trading_end_time:
            trading_start_datetime = datetime.combine(current_date, trading_start_time)
            trading_end_datetime = datetime.combine(current_date, trading_end_time)

            # Calculate minutes within trading hours
            minutes_within_day = (min(end_datetime, trading_end_datetime) - max(start_datetime, trading_start_datetime)).total_seconds() / 60
            total_minutes += max(0, minutes_within_day)

        current_datetime += timedelta(days=1)  # Move to next day

    return total_minutes

# Example usage:
start_datetime = datetime(2024, 2, 26, 9, 30)  # February 26, 2024, 08:00 AM
end_datetime = datetime(2024, 2, 26, 16, 0)   # February 27, 2024, 05:00 PM

minutes = minutes_within_range(start_datetime, end_datetime)
print("Number of minutes within trading hours:", minutes)