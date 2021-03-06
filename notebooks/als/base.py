from datetime import datetime, timedelta

class GPSTimeUtil:
    
    def __init__(self, flight_date):
        self.flight_date = flight_date
    
    def gpstime_to_datetime(self, gpstime, prev_sunday = None):
        if prev_sunday is None:
            prev_sunday = self.previous_sunday()
        dtime = prev_sunday + timedelta(0, gpstime)
        return dtime

    def gpstime_from_datetime(self, dtime, prev_sunday = None):
        if prev_sunday is None:
            prev_sunday = self.previous_sunday()
        delta = dtime - prev_sunday
        return delta.total_seconds()
    
    def previous_sunday(self):
        idx = (self.flight_date.weekday() +1 ) % 7
        prev_sunday = (self.flight_date - timedelta(idx)).replace(hour=0, minute=0, second=0)
        return prev_sunday
    
    @staticmethod
    def get_flight_date(year, day_of_year):
        return datetime(year, 1, 1) + timedelta(day_of_year-1, 0)