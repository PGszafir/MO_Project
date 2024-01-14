from datetime import datetime, timedelta

from defense import *

class WishList():
    def __init__(self, filename):
        self.wishlist = self.load_from_file(filename)

    def __getitem__(self, index):
        return self.wishlist[index]

    def load_from_file(self, filename):
        workbook = openpyxl.load_workbook(filename)
        sheet = workbook.active

        wishlist = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            academic_name, date, start_time, end_time = row[:4]

            academic = Academic(academic_name)
            wish = Wish(academic, date, start_time, end_time)
            wishlist.append(wish)

        return wishlist

class Wish():
    def __init__(self, academic, date, start_hour, end_hour):
        self.academic = academic
        self.date = date
        self.start_hour = start_hour
        self.end_hour = end_hour

    def check_availability(self, datetime, duration=30):
        start_datetime_str = f"{self.date} {self.start_hour}"
        end_datetime_str = f"{self.date} {self.end_hour}"

        start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M")

        if (start_datetime is None or end_datetime is None or
                not (start_datetime <= datetime <= end_datetime) or
                not (datetime + timedelta(minutes=duration) <= start_datetime or
                     datetime >= end_datetime)):
            return True
        else:
            return False
