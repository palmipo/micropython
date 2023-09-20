from devicei2c import DeviceI2C
import micropython
import machine

micropython.alloc_emergency_exception_buf(100)

class DS3231(DeviceI2C):
    def __init__(self, address, bus, pinSQW, cb):
        super().__init__(0x68 | (address & 0x01), bus)

        self.pinSQW = machine.Pin(pinSQW, machine.Pin.IN, machine.Pin.PULL_UP)
        self.pinSQW.irq(handler=self.__callback__, trigger=machine.Pin.IRQ_FALLING, hard=True)
        self.cb = cb

    def __callback__(self, pin):
#         try:
            state = machine.disable_irq()
            self.cb(pin)
            machine.enable_irq(state)
#         except exception:
#             print('exception callback')


    def setDayWeek(self, day):
        cmd = bytearray(2)
        cmd[0] = 0x03
        cmd[1] = day & 0x07
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
        return str((ord(data[0]) & 0x30) >> 4) + str(ord(data[0]) & 0x0F) + "/" + str((ord(data[1]) & 0x10) >> 4) + str(ord(data[1]) & 0x0F) + "/" + str((ord(data[2]) & 0xF0) >> 4) + str(ord(data[2]) & 0x0F)

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
        print(data)
        return str((ord(data[2]) & 0x30) >> 4) + str(ord(data[2]) & 0x0F) + ":" + str((ord(data[1]) & 0x70) >> 4) + str(ord(data[1]) & 0x0F) + ":" + str((ord(data[0]) & 0x70) >> 4) + str(ord(data[0]) & 0x0F)

    def setOut(self, etat):
        cmd = bytearray(2)
        cmd[0] = 0x07
        cmd[1] = (etat & 0x01) << 7
        self.busi2c.send(self.adresse, cmd)

    def setSquareWave(self, freq):
        cmd = bytearray(2)
        cmd[0] = 0x07
        cmd[1] = (freq & 0x03) | (1 << 4)
        self.busi2c.send(self.adresse, cmd)

    def setControlRegister(self, CONV, SqwareWaveFrequency, INTCN, A2IE, A1IE):
        (OSF, EN32kHz, BSY, A2F, A1F) = self.getStatusRegister()
        while BSY != 0:
            (OSF, EN32kHz, BSY, A2F, A1F) = self.getStatusRegister()

        cmd = bytearray(2)
        cmd[0] = 0x0E
        cmd[1] = ((CONV & 0x01) << 5) | ((CONV & 0x01) << 5) | ((SqwareWaveFrequency & 0x03) << 3) | ((INTCN & 0x01) << 2) | ((A2IE & 0x01) << 1) | (A1IE & 0x01)
        self.busi2c.send(self.adresse, cmd)
        
    def getTemperature(self):
        (OSF, EN32kHz, BSY, A2F, A1F) = self.getStatusRegister()
        while BSY != 0:
            (OSF, EN32kHz, BSY, A2F, A1F) = self.getStatusRegister()

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
