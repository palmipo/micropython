from devicei2c import DeviceI2C

class LSM303D(DeviceI2C):

    def __init__(self, bus):
        super().__init__(0x31, bus)

    def init(self):

    def temp_out(self):
        cmd = bytearray(1)
        cmd[0] = 0x31;
        data = self.busi2c.transferer(self.adresse, cmd, 2)
        return ((data[0] << 4) | (data[0] >> 4))

#odr : data rate selection -> 0 power-down / 9 normal
# lpen : low power enable -> 0 normal mode
# zen : z-axis enable -> 0 Z-axix disabled
# yen : y-axis enable -> 0 Y-axix disabled
# xen : x-axis enable -> 0 X-axix disabled
    def linearAccelerationRegister(self, odr, lpen, zen, yen, xen):
        cmd = bytearray(2)
        cmd[0] = 0x20;
        cmd[1] = (odr & 0x07) << 4
        cmd[1] |= (lpen & 0x01) << 3
        cmd[1] |= (zen & 0x01) << 2
        cmd[1] |= (yen & 0x01) << 1
        cmd[1] |= (xen & 0x01)
        self.busi2c.send(self.adresse, cmd)

    def ctrlReg2A(self, hpm, hpcf, fds, hpclick, hpis2, hpis1):
        cmd = bytearray(2)
        cmd[0] = 0x21;
        cmd[1] = (hpm & 0x03) << 6
        cmd[1] |= (hpcf & 0x03) << 4
        cmd[1] |= (fds & 0x01) << 3
        cmd[1] |= (hpclick & 0x01) << 2
        cmd[1] |= (hpis2 & 0x01) << 1
        cmd[1] |= (hpis1 & 0x01)
        self.busi2c.send(self.adresse, cmd)

    def ctrlReg3A(self, i1_click, i1_aoi1, i1_aoi2, i1_drdy1, i1_drdy2, i1_wtm, i1_overrun):
        cmd = bytearray(2)
        cmd[0] = 0x22;
        cmd[1] = (i1_click & 0x01) << 7
        cmd[1] |= (i1_aoi1 & 0x01) << 6
        cmd[1] |= (i1_aoi2 & 0x01) << 5
        cmd[1] |= (i1_drdy1 & 0x01) << 4
        cmd[1] |= (i1_drdy2 & 0x01) << 3
        cmd[1] |= (i1_wtm & 0x01) << 2
        cmd[1] |= (i1_overrun & 0x01)
        self.busi2c.send(self.adresse, cmd)

    def ctrlReg4A(self, bdu, ble, fs, hr, sim):
        cmd = bytearray(2)
        cmd[0] = 0x23;
        cmd[1] = (bdu & 0x01) << 7
        cmd[1] |= (ble & 0x01) << 6
        cmd[1] |= (fs & 0x03) << 4
        cmd[1] |= (hr & 0x01) << 3
        cmd[1] |= (sim & 0x01)
        self.busi2c.send(self.adresse, cmd)
