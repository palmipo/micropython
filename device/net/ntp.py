import ntptime, machine

class Ntp:
    def __init__(self):
        self.rtc = machine.RTC()

    def ntp(self):
        ntptime.settime()
        return self.rtc.datetime()

