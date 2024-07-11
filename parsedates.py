import re
from datetime import datetime, timedelta


class Person:
    def __init__(self, name):
        self.name = name
        self.available_dates = []

    def update_availability(self, dates):
        """Update the availability of the person with a given date string"""
        self.available_dates = self._parse_dates(dates)

    def _parse_dates(self, datestr: str) -> list:
        dates = re.split("\n|,", datestr)
        available_ranges = self.available_dates
        unavailable_ranges = []
        for s in dates:
            if s.startswith("x"):
                unavailable_ranges.extend(self._enumerate_days_in_range(s[1:]))
            else:
                available_ranges.extend(self._enumerate_days_in_range(s))
        return sorted(list(set(available_ranges) - set(unavailable_ranges)))

    def _enumerate_days_in_range(self, date_or_range) -> list:
        d = date_or_range.split("-")
        if len(d) == 1:
            return d[0]
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

    def print_dates(self):
        print(self.available_dates)


if __name__ == "__main__":
    EXAMPLE = """01/12/24-16/12/24,18/20/24-20/12/24
x05/12/24
x12/12/24-15/12/24"""
    nm = Person("Test")
    nm.update_availability(EXAMPLE)
    nm.print_dates()
