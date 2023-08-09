"""
:author Nicolas Boutin
:date 2023-07-07
"""

import calendar
import datetime

TimeRange = list[str]


def convert_time_ranges_to_duration(time_ranges: TimeRange) -> datetime.timedelta:
    """Convert datetime.time range data structure to datetime.timedelta"""
    duration = datetime.timedelta()
    for time_range in time_ranges:
        start = datetime.time.fromisoformat(time_range[0]+':00')
        end = datetime.time.fromisoformat(time_range[1]+':00')
        duration += datetime.timedelta(hours=end.hour, minutes=end.minute) - \
            datetime.timedelta(hours=start.hour, minutes=start.minute)
    return duration
    # duration = datetime.timedelta()
    # for index in range(0, len(time_range), 2):
    #     start = datetime.time.fromisoformat(time_range[index]+':00')
    #     end = datetime.time.fromisoformat(time_range[index+1]+':00')
    #     duration += datetime.timedelta(hours=end.hour, minutes=end.minute) - \
    #         datetime.timedelta(hours=start.hour, minutes=start.minute)
    # return duration


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

    last_date_last_week = get_last_day_of_week(year, last_week_number)

    if last_date_last_week.month != month:
        last_week_number -= 1

    week_numbers = []
    # Edge case for weeks in early January that count as the last week of the previous year
    if month == 1 and first_week_number > last_week_number:
        first_week_number = 1
        week_numbers = [52]

    # Week numbers for the specified month
    week_numbers.extend(list(range(first_week_number, last_week_number + 1)))

    return week_numbers


def get_last_day_of_week(year: int, week: int) -> datetime.date:
    """Return the last day of a given week"""
    first_day = datetime.date(year, 1, 1)

    # Counting the number of days to reach the first Thursday
    first_thursday_delta = 3 - first_day.weekday() if first_day.weekday() < 4 else 10 - first_day.weekday()

    # Identifying the first Thursday
    first_thursday = first_day + datetime.timedelta(days=first_thursday_delta)

    # Resolving the first Monday on or before the first Thursday
    first_monday = first_thursday - datetime.timedelta(days=3)

    # Resolving any given week's Sunday (last day of the week)
    last_day = first_monday + datetime.timedelta(weeks=(week-1), days=6)
    return last_day


def get_dates_in_month(in_date: datetime.date) -> list[datetime.date]:
    """Return all dates in a given month"""
    # Get the number of days in the month
    _, num_days = calendar.monthrange(in_date.year, in_date.month)
    # Create a list of all days in the month
    return [datetime.date(in_date.year, in_date.month, day)for day in range(1, num_days+1)]
