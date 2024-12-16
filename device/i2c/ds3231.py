from device.i2c.devicei2c import DeviceI2C

class DS3231(DeviceI2C):
    def __init__(self, address, bus):
        super().__init__(0x68 | (address & 0x01), bus)

    def setDayWeek(self, day):
        cmd = bytearray(2)
        cmd[0] = 0x03
        cmd[1] = ord(day) & 0x07
        self.busi2c.send(self.adresse, cmd)

    def getDayWeek(self):
        cmd = bytearray(1)
        cmd[0] = 0x03
        data = self.busi2c.transferer(self.adresse, cmd, 1)
        return data[0] & 0x07

    #18/01/73
    def setDate(self, date):
        cmd = bytearray(4)
        cmd[0] = 0x04
        cmd[1] = ((ord(date[0]) & 0x03) << 4) | (ord(date[1]) & 0x0F)
        cmd[2] = ((ord(date[3]) & 0x01) << 4) | (ord(date[4]) & 0x0F)
        cmd[3] = ((ord(date[6]) & 0x0F) << 4) | (ord(date[7]) & 0x0F)
        self.busi2c.send(self.adresse, cmd)

    def getDate(self):
        cmd = bytearray(1)
        cmd[0] = 0x04
        data = self.busi2c.transferer(self.adresse, cmd, 3)
        res = str(((data[0]) & 0x30) >> 4) + str((data[0]) & 0x0F)
        res += "/"
        res += (((data[1]) & 0x10) >> 4) + str((data[1]) & 0x0F)
        res += "/"
        res +=str(((data[2]) & 0xF0) >> 4) + str((data[2]) & 0x0F)
        return res

    #18:25:59
    def setTime(self, hour):
        cmd = bytearray(4)
        cmd[0] = 0x00
        cmd[1] = ((ord(hour[6]) & 0x07) << 4) | (ord(hour[7]) & 0x0F)
        cmd[2] = ((ord(hour[3]) & 0x07) << 4) | (ord(hour[4]) & 0x0F)
        cmd[3] = ((ord(hour[0]) & 0x03) << 4) | (ord(hour[1]) & 0x0F)
        self.busi2c.send(self.adresse, cmd)

    def getTime(self):
        cmd = bytearray(1)
        cmd[0] = 0x00
        data = self.busi2c.transferer(self.adresse, cmd, 3)
        res = str(((data[2]) & 0x30) >> 4) + str((data[2]) & 0x0F)
        res += ":"
        res += str(((data[1]) & 0x70) >> 4) + str((data[1]) & 0x0F)
        res += ":"
        res += str(((data[0]) & 0x70) >> 4) + str((data[0]) & 0x0F)
        return res

    # DY/DT ALARM 1 REGISTER MASK BITS (BIT 7) ALARM RATE
    # A1M4 A1M3 A1M2 A1M1
    # X 1 1 1 1 Alarm once per second
    # X 1 1 1 0 Alarm when seconds match
    # X 1 1 0 0 Alarm when minutes and seconds match
    # X 1 0 0 0 Alarm when hours, minutes, and seconds match
    # 0 0 0 0 0 Alarm when date, hours, minutes, and seconds match
    # 1 0 0 0 0 Alarm when day, hours, minutes, and seconds match
    # A1M=0 hour='18:25:59' day='18'
    # A1M=1 hour='18:25:59' day='05'
    def setAlarm1(self, A1M, hour, day):
        cmd = bytearray(5)
        cmd[0] = 0x07
        cmd[1] = ((A1M & 0x01) << 7) | ((ord(hour[6]) & 0x07) << 4) | (ord(hour[7]) & 0x0F)
        cmd[2] = (((A1M >> 1) & 0x01) << 7) | ((ord(hour[3]) & 0x07) << 4) | (ord(hour[4]) & 0x0F)
        cmd[3] = (((A1M >> 2) & 0x01) << 7) | ((ord(hour[0]) & 0x03) << 4) | (ord(hour[1]) & 0x0F)
        cmd[4] = (((A1M >> 3) & 0x01) << 7) | (((A1M >> 4) & 0x01) << 6) | ((ord(day[0]) & 0x03) << 4) | (ord(day[1]) & 0x0F)
        self.busi2c.send(self.adresse, cmd)

    def getAlarm1(self):
        cmd = bytearray(1)
        cmd[0] = 0x07
        data = self.busi2c.transferer(self.adresse, cmd, 4)
        hour = str(((data[2]) & 0x30) >> 4) + str((data[2]) & 0x0F)
        hour += ":"
        hour += str(((data[1]) & 0x70) >> 4) + str((data[1]) & 0x0F)
        hour += ":"
        hour += str(((data[0]) & 0x70) >> 4) + str((data[0]) & 0x0F)
        day = str(((data[3]) & 0x30) >> 4) + str((data[3]) & 0x0F)
        A1M = (data[0] & 0x01) >> 7
        A1M |= ((data[1] & 0x80) >> 7) << 1
        A1M |= ((data[2] & 0x80) >> 7) << 2
        A1M |= ((data[3] & 0x80) >> 7) << 3
        A1M |= ((data[3] & 0x40) >> 6) << 4
        return A1M, hour, day

    # DY/DT ALARM 2 REGISTER MASK BITS (BIT 7) ALARM RATE
    # A2M4 A2M3 A2M2
    # X 1 1 1 Alarm once per minute (00 seconds of every minute)
    # X 1 1 0 Alarm when minutes match
    # X 1 0 0 Alarm when hours and minutes match
    # 0 0 0 0 Alarm when date, hours, and minutes match
    # 1 0 0 0 Alarm when day, hours, and minutes match
    def setAlarm2(self, A2M, hour, day):
        cmd = bytearray(4)
        cmd[0] = 0x0B
        cmd[1] = ((A2M & 0x01) << 7) | ((ord(hour[3]) & 0x07) << 4) | (ord(hour[4]) & 0x0F)
        cmd[2] = (((A2M >> 1) & 0x01) << 7) | ((ord(hour[0]) & 0x03) << 4) | (ord(hour[1]) & 0x0F)
        cmd[3] = (((A2M >> 2) & 0x01) << 7) | (((A2M >> 3) & 0x01) << 6) | ((ord(day[0]) & 0x03) << 4) | (ord(day[1]) & 0x0F)
        self.busi2c.send(self.adresse, cmd)

    def getAlarm2(self):
        cmd = bytearray(1)
        cmd[0] = 0x0B
        data = self.busi2c.transferer(self.adresse, cmd, 3)
        hour = str(((data[1]) & 0x30) >> 4) + str((data[1]) & 0x0F)
        hour += ":"
        hour += str(((data[0]) & 0x70) >> 4) + str((data[0]) & 0x0F)
        hour += ":00"
        day = str(((data[2]) & 0x30) >> 4) + str((data[2]) & 0x0F)
        A2M = (data[0] & 0x01) >> 7
        A2M |= ((data[1] & 0x80) >> 7) << 1
        A2M |= ((data[2] & 0x80) >> 7) << 3
        A2M |= ((data[2] & 0x40) >> 6) << 4
        return A2M, hour, day

    # CONV : convert temperature
    # RS : rate select 0 : 1Hz / 1 : 1024Hz / 2 : 4096Hz / 3 : 8192Hz
    # INTCN : interrupt control 0 : alarm / 1 square wave
    # A2IE : alarm 2 interrupt enable
    # A1IE : alarm 1 interrupt enable
    # EN32kHz : Enable 32kHz Output
    def setControlRegister(self, CONV=0, RS=0, INTCN=0, A2IE=0, A1IE=0, EN32kHz=0):
        self.waitWhileBusy()

        # 0Eh EOSC BBSQW CONV RS2 RS1 INTCN A2IE A1IE Control —
        # 0Fh OSF 0 0 0 EN32kHz BSY A2F A1F Control/Status
        cmd = bytearray(3)
        cmd[0] = 0x0E
        cmd[1] = ((CONV & 0x01) << 5) | ((RS & 0x03) << 3) | ((INTCN & 0x01) << 2) | ((A2IE & 0x01) << 1) | (A1IE & 0x01)
        cmd[2] = 0x80 | ((EN32kHz & 0x01) << 3)
        self.busi2c.send(self.adresse, cmd)

    def getControlRegister(self):
        cmd = bytearray(1)
        cmd[0] = 0x0E
        data = self.busi2c.transferer(self.adresse, cmd, 1)
        CONV = (data[0] & 0x20) >> 5
        RS = (data[0] & 0x18) >> 3
        INTCN = (data[0] & 0x04) >> 2
        A2IE = (data[0] & 0x02) >> 1
        A1IE = data[0] & 0x01
        return CONV, RS, INTCN, A2IE, A1IE

    def getTemperature(self):
        self.waitWhileBusy()

        cmd = bytearray(1)
        cmd[0] = 0x11
        data = self.busi2c.transferer(self.adresse, cmd, 2)
        return ((data[0] << 2) | (data[1] >> 6)) * 0.25

    def getStatusRegister(self):
        cmd = bytearray(1)
        cmd[0] = 0x0F
        data = self.busi2c.transferer(self.adresse, cmd, 1)
        OSF = (data[0] & 0x80) >> 7
        EN32kHz = (data[0] & 0x08) >> 3
        BSY = (data[0] & 0x04) >> 2
        A2F = (data[0] & 0x02) >> 1
        A1F = data[0] & 0x01
        return (OSF, EN32kHz, BSY, A2F, A1F)

    def waitWhileBusy(self):
        (OSF, EN32kHz, BSY, A2F, A1F) = self.getStatusRegister()
        while BSY != 0:
            (OSF, EN32kHz, BSY, A2F, A1F) = self.getStatusRegister()
