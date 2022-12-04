from devicei2c import DeviceI2C

class BMP280(DeviceI2C):

    def statusRegister(self):
        buf = bytearray(1)
        buf[0] = 0xf3
        data = self.busi2c.transferer(self.adresse, buf, 1)
        mesuring = (data[0] & 0x04) >> 3
        im_update = data[0] & 0x01
        return mesuring, im_update
    
    def ctrlMeasureRegister(self, osrs_t, osrs_p, mode):
        buf = bytearray(2)
        buf[0] = 0xf4
        buf[1] = ((osrs_t & 0x07) << 5) | ((osrs_p & 0x07) << 2) | (mode & 0x02)
        self.busi2c.send(self.adresse, buf)

    def configRegister(self, t_sb, filtre):
        buf = bytearray(2)
        buf[0] = 0xf5
        buf[1] = ((t_sb & 0x07) << 5) | ((filtre & 0x07) << 2)
        self.busi2c.send(self.adresse, buf)

    def rawMeasureRegister(self):
        buf = bytearray(1)
        buf[0] = 0xf7
        data = self.busi2c.transferer(self.adresse, buf, 6)
        self.raw_pressure = (data[0] << 12) | (data[1] << 4) | ((data[2] & 0xF0) >> 4)
        self.raw_temperature = (data[3] << 12) | (data[4] << 4) | ((data[5] & 0xF0) >> 4)

    def readCompensationRegister(self):
        buf = bytearray(1)
        buf[0] = 0x88
        data = self.busi2c.transferer(self.adresse, buf, 24)
        self.dig_T1 = (data[0] << 8) | data[1]
        self.dig_T2 = (1 << 16) - ((data[2] << 8) | data[3])
        self.dig_T3 = (1 << 16) - ((data[4] << 8) | data[5])
        self.dig_P1 = (data[6] << 8) | data[7]
        self.dig_P2 = (1 << 16) - ((data[8] << 8) | data[9])
        self.dig_P3 = (1 << 16) - ((data[10] << 8) | data[11])
        self.dig_P4 = (1 << 16) - ((data[12] << 8) | data[13])
        self.dig_P5 = (1 << 16) - ((data[14] << 8) | data[15])
        self.dig_P6 = (1 << 16) - ((data[16] << 8) | data[17])
        self.dig_P7 = (1 << 16) - ((data[18] << 8) | data[19])
        self.dig_P8 = (1 << 16) - ((data[20] << 8) | data[21])
        self.dig_P9 = (1 << 16) - ((data[22] << 8) | data[23])

    def compute(self):
        var1=(self.raw_temperature/16384.0-self.dig_T1/1024.0)*self.dig_T2 # formula for temperature from datasheet
        var2=(self.raw_temperature/131072.0-self.dig_T1/8192.0)*(self.raw_temperature/131072.0-self.dig_T1/8192.0)*self.dig_T3 # formula for temperature from datasheet
        temp=(var1+var2)/5120.0 # formula for temperature from datasheet
        t_fine=(var1+var2) # need for pressure calculation

        var1=t_fine/2.0-64000.0 # formula for pressure from datasheet
        var2=var1*var1*self.dig_P6/32768.0 # formula for pressure from datasheet
        var2=var2+var1*self.dig_P5*2 # formula for pressure from datasheet
        var2=var2/4.0+self.dig_P4*65536.0 # formula for pressure from datasheet
        var1=(self.dig_P3*var1*var1/524288.0+self.dig_P2*var1)/524288.0 # formula for pressure from datasheet
        var1=(1.0+var1/32768.0)*self.dig_P1 # formula for pressure from datasheet
        press=1048576.0-self.raw_pressure # formula for pressure from datasheet
        press=(press-var2/4096.0)*6250.0/var1 # formula for pressure from datasheet
        var1=self.dig_P9*press*press/2147483648.0 # formula for pressure from datasheet
        var2=press*self.dig_P8/32768.0 # formula for pressure from datasheet
        press=press+(var1+var2+self.dig_P7)/16.0 # formula for pressure from datasheet

        return temp, press

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
