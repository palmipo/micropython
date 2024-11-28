import ntptime, time

class Ntp:
    def __init__(self):
        pass

    def ntp(self):
        try:
            ntptime.settime() # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
        except OSError:
            pass

        return time.localtime()


