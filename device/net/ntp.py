import ntptime, time

class Ntp:
    def __init__(self):
        pass

    def ntp(self, stream):
        # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
        # self.eth.connect(1, '162.159.200.123', 123)
    
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1B
        stream.send(NTP_QUERY)
        msg = stream.recv(48)
        val = struct.unpack("!I", msg[40:44])[0]

        # 2024-01-01 00:00:00 converted to an NTP timestamp
        MIN_NTP_TIMESTAMP = 3913056000

        if val < MIN_NTP_TIMESTAMP:
            val += 0x100000000

        # Convert timestamp from NTP format to our internal format

        EPOCH_YEAR = gmtime(0)[0]
        if EPOCH_YEAR == 2000:
            # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
            NTP_DELTA = 3155673600
        elif EPOCH_YEAR == 1970:
            # (date(1970, 1, 1) - date(1900, 1, 1)).days * 24*60*60
            NTP_DELTA = 2208988800
        else:
            raise Exception("Unsupported epoch: {}".format(EPOCH_YEAR))

        t = val - NTP_DELTA


        tm = gmtime(t)
        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

        return time.localtime()


