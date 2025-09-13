from datetime import datetime, timedelta
from enum import Enum

class DateFilterEnum(str, Enum):
    today = "today"
    yesterday = "yesterday"
    last_week = "last_week"
    this_month = "this_month"
    last_month = "last_month"
    last_three_months = "last_three_months"
    last_six_months = "last_six_months"
    last_year = "last_year"

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def get_date_range(filter_value: DateFilterEnum) -> tuple[datetime, datetime]:
        now = datetime.utcnow()
        
        if filter_value == DateFilterEnum.today:
            start = datetime(now.year, now.month, now.day)
            end = now
        elif filter_value == DateFilterEnum.yesterday:
            start = datetime(now.year, now.month, now.day) - timedelta(days=1)
            end = datetime(now.year, now.month, now.day)
        elif filter_value == DateFilterEnum.last_week:
            start = now - timedelta(weeks=1)
            end = now
        elif filter_value == DateFilterEnum.this_month:
            start = datetime(now.year, now.month, 1)
            end = now
        elif filter_value == DateFilterEnum.last_month:
            first_this_month = datetime(now.year, now.month, 1)
            last_month_end = first_this_month
            last_month_start = datetime(
                last_month_end.year if last_month_end.month > 1 else last_month_end.year - 1,
                last_month_end.month - 1 if last_month_end.month > 1 else 12,
                1
            )
            start, end = last_month_start, last_month_end
        elif filter_value == DateFilterEnum.last_three_months:
            start = now - timedelta(days=90)
            end = now
        elif filter_value == DateFilterEnum.last_six_months:
            start = now - timedelta(days=180)
            end = now
        elif filter_value == DateFilterEnum.last_year:
            start = now - timedelta(days=365)
            end = now
        else:
            raise ValueError("Unsupported filter")

        return start, end

