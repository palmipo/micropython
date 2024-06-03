from devicei2c import DeviceI2C

class BMP280(DeviceI2C):

    def __init__(self, bus):
        super().__init__(0x77, bus)

    def __statusRegister(self):
        buf = bytearray(1)
        buf[0] = 0xf3
        data = self.busi2c.transferer(self.adresse, buf, 1)
        mesuring = (data[0] & 0x04) >> 3
        im_update = data[0] & 0x01
        return mesuring, im_update
    
    # osrs_t x2  : 010b
    # osrs_p x16 : 101b
    # mode       : normal 11b
    def ctrlMeasureRegister(self, osrs_t, osrs_p, mode):
        buf = bytearray(2)
        buf[0] = 0xf4
        buf[1] = ((osrs_t & 0x07) << 5) | ((osrs_p & 0x07) << 2) | (mode & 0x02)
        self.busi2c.send(self.adresse, buf)

    # t_sb   3
    # filtre 16
    def configRegister(self, t_sb, filtre):
        buf = bytearray(2)
        buf[0] = 0xf5
        buf[1] = ((t_sb & 0x07) << 5) | ((filtre & 0x07) << 2)
        self.busi2c.send(self.adresse, buf)

    def __rawMeasureRegister(self):
        buf = bytearray(1)
        buf[0] = 0xf7
        data = self.busi2c.transferer(self.adresse, buf, 6)
        self.raw_pressure = int((data[0] << 12) | (data[1] << 4) | (data[2] >> 4))
        self.raw_temperature = int((data[3] << 12) | (data[4] << 4) | (data[5] >> 4))

    def __readCompensationRegister(self):
        buf = bytearray(1)
        buf[0] = 0x88
        data = self.busi2c.transferer(self.adresse, buf, 24)
        self.dig_T1 = int((data[0] << 8) | data[1])
        self.dig_T2 = int((1 << 16) - ((data[2] << 8) | data[3]))
        self.dig_T3 = int((1 << 16) - ((data[4] << 8) | data[5]))
        self.dig_P1 = int((data[6] << 8) | data[7])
        self.dig_P2 = int((1 << 16) - ((data[8] << 8) | data[9]))
        self.dig_P3 = int((1 << 16) - ((data[10] << 8) | data[11]))
        self.dig_P4 = int((1 << 16) - ((data[12] << 8) | data[13]))
        self.dig_P5 = int((1 << 16) - ((data[14] << 8) | data[15]))
        self.dig_P6 = int((1 << 16) - ((data[16] << 8) | data[17]))
        self.dig_P7 = int((1 << 16) - ((data[18] << 8) | data[19]))
        self.dig_P8 = int((1 << 16) - ((data[20] << 8) | data[21]))
        self.dig_P9 = int((1 << 16) - ((data[22] << 8) | data[23]))

    def __calculer_t_fine(self):
        self.__rawMeasureRegister()
        self.__readCompensationRegister()
        var1 = (((self.raw_temperature >> 3) - (self.dig_T1 << 1)) * self.dig_T2) >> 11
        var2 = (((((self.raw_temperature >> 4) - self.dig_T1) * ((self.raw_temperature >> 4) - self.dig_T1)) >> 12) * self.dig_T3) >> 14
        t_fine = int(var1) + int(var2)
        return t_fine

    def compensateT(self):
        mesuring, im_update = self.__statusRegister()
        while mesuring != 0:
            mesuring, im_update = self.__statusRegister()
        t_fine = self.__calculer_t_fine()
        t = (t_fine * 5 + 128) >> 8;
        return float(t) / 100.0

    def compensateP(self):
        mesuring, im_update = self.__statusRegister()
        while mesuring != 0:
            mesuring, im_update = self.__statusRegister()
        t_fine = self.__calculer_t_fine()

        var1 = t_fine - 128000
        var2 = var1 * var1 * self.dig_P6
        var2 = var2 + ((var1 * self.dig_P5) << 17)
        var2 = var2 + (self.dig_P4 << 35)
        var1 = ((var1 * var1 * self.dig_P3) >> 8) + ((var1 * self.dig_P2) << 12)
        var1 = ((1 << 47) * self.dig_P1) >> 33
        if var1 == 0:
            return 0.0
        
        p = 1048576 - self.raw_pressure
        p = int((((p << 31) - var2) * 3125) / var1)
        var1 = (self.dig_P9 * (p >> 13) * (p >> 13)) >> 25
        var2 = (self.dig_P8 * p) >> 19
        p = ((p + var1 + var2) >> 8) + (self.dig_P7 << 4)

        return float(p)

    def chipIdRegister(self):
        buf = bytearray(1)
        buf[0] = 0xd0
        id = self.busi2c.transferer(self.adresse, buf, 1)
        if id[0] in [0x58, 0x60]:
            return True
        else:
            return False

    def reset(self):
        buf = bytearray(2)
        buf[0] = 0xe0
        buf[1] = 0xb6
        self.busi2c.send(self.adresse, buf)

if __name__ == '__main__':
    from i2cpico import I2CPico
    i2c = I2CPico(1, 6, 7)
    sensor = BMP280(i2c)
    sensor.reset()
    time.sleep(1)
    print("chipIdRegister {}".format(sensor.chipIdRegister()))
    try:
        # sensor.setup()
        data = []
        data = sensor.readData()
        print("pressure : %7.2f hPa" %data[0])
        print("temp : %-6.2f ℃" %data[1])
        print("hum : %6.2f ％" %data[2])
    except KeyboardInterrupt:
        pass

