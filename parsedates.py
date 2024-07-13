import re
from datetime import datetime, timedelta
from typing import List


class DateParser:
    @staticmethod
    def update_availability(current_dates, new_dates):
        """Update the availability of the person with a given date string"""
        return DateParser._parse_dates(current_dates, new_dates)

    @staticmethod
    def _parse_dates(available_dates: List, datestr: str) -> List[str]:
        dates = re.split("\n|,", datestr.strip())
        available_ranges = available_dates
        unavailable_ranges = []
        for s in dates:
            if s.startswith("x"):
                unavailable_ranges.extend(DateParser._enumerate_days_in_range(s[1:]))
            else:
                available_ranges.extend(DateParser._enumerate_days_in_range(s))
        return sorted(list(set(available_ranges) - set(unavailable_ranges)))

    @staticmethod
    def _enumerate_days_in_range(date_or_range: str) -> List[str]:
        d = date_or_range.split("-")
        if len(d) == 1:
            return d

        start_date_str = d[0]
        end_date_str = d[1]
        assert len(d) == 2, f"Invalid date range: {date_or_range}"

        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%y")
            end_date = datetime.strptime(end_date_str, "%d/%m/%y")

            if start_date > end_date:
                raise ValueError("Start date cannot be greater than end date")

            days = []
            current_date = start_date

            while current_date <= end_date:
                days.append(current_date.strftime("%d/%m/%y"))
                current_date += timedelta(days=1)

            return days

        except ValueError as e:
            print(f"Invalid date format: {e}")
        return []
