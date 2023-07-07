"""
:author Nicolas Boutin
:datetime.date 2023-07-07
"""

import calendar
import datetime

time_range_t = list[str]


def convert_time_range_to_duration(time_range: time_range_t) -> datetime.timedelta:
    """Convert datetime.time range data structure to datetime.timedelta"""
    if len(time_range) % 2 != 0:
        raise ValueError(
            f"Time range must be a multiple of 2, got {len(time_range)}")

    duration = datetime.timedelta()
    for index in range(0, len(time_range), 2):
        start = datetime.time.fromisoformat(time_range[index]+':00')
        end = datetime.time.fromisoformat(time_range[index+1]+':00')
        duration += datetime.timedelta(hours=end.hour, minutes=end.minute) - \
            datetime.timedelta(hours=start.hour, minutes=start.minute)

    return duration


def get_dates_in_week(year, week_number) -> list[datetime.date]:
    """Return all dates in a given week"""
    # Check if week number is valid
    if not 1 <= week_number <= 53:
        raise ValueError(f'Invalid ISO week number {week_number}. Week number must be in 1-53.')
    
    # Jan 1 of the given year
    jan1 = datetime.date(year, 1, 1)

    # Number of days to the first Thursday
    days_to_first_thursday = (3 - jan1.weekday() + 7) % 7

    # First Thursday of the given year
    first_thursday = jan1 + datetime.timedelta(days=days_to_first_thursday)

    # If week number is 53, check if the year actually has a week 53
    if week_number == 53 and jan1.isocalendar()[1] == 1:
        raise ValueError(f'The year {year} does not have 53 weeks.')

    # Compute the datetime.date of the Thursday in the given ISO week number
    week_thursday = first_thursday + datetime.timedelta(weeks=week_number-1)

    # Compute the dates of the Monday to Sunday of the week
    week_dates = [week_thursday + datetime.timedelta(days=i) for i in range(-3, 4)]

    return week_dates

def get_week_numbers(year, month) -> list[int]:
    """Return all week numbers in a given month"""
    # Number of days in the month
    month_days = calendar.monthrange(year, month)[1]

    # Date for the first day and last day of the month
    first_date = datetime.date(year, month, 1)
    last_date = datetime.date(year, month, month_days)

    # Week numbers for the first day and last day of the month
    first_week_number = first_date.isocalendar()[1]
    last_week_number = last_date.isocalendar()[1]

    # If the first day of the month is Saturday and it's still
    # the previous month's week, then increase the first_week_number by 1
    if first_date.weekday() == 5 and first_week_number < last_week_number:
        first_week_number += 1

    # Edge case for weeks in early January that count as the last week of the previous year
    if month == 1 and first_week_number > last_week_number:
        first_week_number = 1

    # Week numbers for the specified month
    week_numbers = list(range(first_week_number, last_week_number + 1))

    return week_numbers
    

def get_dates_in_month(in_date:datetime.date) -> list[datetime.date]:
    """Return all dates in a given month"""
    # Get the number of days in the month
    _, num_days = calendar.monthrange(in_date.year, in_date.month)
    # Create a list of all days in the month
    return [datetime.date(in_date.year, in_date.month, day)for day in range(1, num_days+1)]