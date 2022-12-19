from devicei2c import DeviceI2C

class LSM303D(DeviceI2C):

    def __init__(self, bus):
        super().__init__(0x1D, bus)

    def temp_out(self):
        cmd = bytearray(1)
        cmd[0] = 0x05;
        data = self.busi2c.transferer(self.adresse, cmd, 2)
        return (1<<12) - ((data[1] << 4) | (data[0] >> 4))
    
    def out_x_y_z(self):
        cmd = bytearray(1)
        cmd[0] = 0x8;
        data = self.busi2c.transferer(self.adresse, cmd, 6)
        x = (1 << 16) - ((data[1] << 8) | data[0])
        y = (1 << 16) - ((data[3] << 8) | data[2])
        z = (1 << 16) - ((data[5] << 8) | data[4])
        return x, y, z

    def who_am_i(self):
        cmd = bytearray(1)
        cmd[0] = 0x0F;
        data = self.busi2c.transferer(self.adresse, cmd, 1)[0]
        return data

    #odr : data rate selection -> 0 power-down / 9 normal
    # lpen : low power enable -> 0 normal mode
    # zen : z-axis enable -> 0 Z-axix disabled
    # yen : y-axis enable -> 0 Y-axix disabled
    # xen : x-axis enable -> 0 X-axix disabled
    def ctrl1(self, AODR, BDU, AZEN, AYEN, AXEN):
        cmd = bytearray(2)
        cmd[0] = 0x20;
        cmd[1] = (AODR & 0x0F) << 4
        cmd[1] |= (BDU & 0x01) << 3
        cmd[1] |= (AZEN & 0x01) << 2
        cmd[1] |= (AYEN & 0x01) << 1
        cmd[1] |= (AXEN & 0x01)
        self.busi2c.send(self.adresse, cmd)

    def ctrl2(self, ABW, AFS, AST, SIM):
        cmd = bytearray(2)
        cmd[0] = 0x21;
        cmd[1] = (ABW & 0x03) << 6
        cmd[1] |= (AFS & 0x07) << 3
        cmd[1] |= (AST & 0x01) << 1
        cmd[1] |= (SIM & 0x01)
        self.busi2c.send(self.adresse, cmd)

# INT1_BOOT
# INT1_Click
# INT1_IG1
# INT1_IG2
# INT1_IGM
# INT1_DRDY_A
# INT1_DRDY_M
# INT1_EMPTY
    def ctrl3(self, INT1_BOOT, INT1_Click, INT1_IG1, INT1_IG2, INT1_IGM, INT1_DRDY_A, INT1_DRDY_M, INT1_EMPTY):
        cmd = bytearray(2)
        cmd[0] = 0x22;
        cmd[1] = (INT1_BOOT & 0x01) << 7
        cmd[1] |= (INT1_Click & 0x01) << 6
        cmd[1] |= (INT1_IG1 & 0x01) << 5
        cmd[1] |= (INT1_IG2 & 0x01) << 4
        cmd[1] |= (INT1_IGM & 0x01) << 3
        cmd[1] |= (INT1_DRDY_A & 0x01) << 2
        cmd[1] |= (INT1_DRDY_M & 0x01) << 1
        cmd[1] |= (INT1_EMPTY & 0x01)
        self.busi2c.send(self.adresse, cmd)

# INT2_Click
# INT2_INT1
# INT2_INT2
# INT2_INTM
# INT2_DRDY_A
# INT2_DRDY_M
# INT2_Overrun
# INT2_FTH
    def ctrl4(self, INT2_Click, INT2_INT1, INT2_INT2, INT2_INTM, INT2_DRDY_A, INT2_DRDY_M, INT2_Overrun, INT2_FTH):
        cmd = bytearray(2)
        cmd[0] = 0x23;
        cmd[1] = (INT2_Click & 0x01) << 7
        cmd[1] |= (INT2_INT1 & 0x01) << 6
        cmd[1] |= (INT2_INT2 & 0x01) << 5
        cmd[1] |= (INT2_INTM & 0x01) << 4
        cmd[1] |= (INT2_DRDY_A & 0x01) << 3
        cmd[1] |= (INT2_DRDY_M & 0x01) << 2
        cmd[1] |= (INT2_Overrun & 0x01) << 1
        cmd[1] |= (INT2_FTH & 0x01)
        self.busi2c.send(self.adresse, cmd)

    # TEMP_EN Temperature sensor enable. Default value: 0
    #       (0: temperature sensor disabled; 1: temperature sensor enabled)
    # M_RES [1:0] Magnetic resolution selection. Default value: 00
    #       (00: low resolution, 11: high resolution)
    # M_ODR [2:0] Magnetic data rate selection. Default value: 110
    # LIR2 Latch interrupt request on INT2_SRC register, with INT2_SRC register cleared by
    # reading INT2_SRC itself. Default value: 0.
    # (0: interrupt request not latched; 1: interrupt request latched)
    # LIR1 Latch interrupt request on INT1_SRC register, with INT1_SRC register cleared by
    # reading INT1_SRC itself. Default value: 0.
    # (0: interrupt request not latched; 1: interrupt request latched)
    def ctrl5(self, TEMP_EN, M_RES, M_ODR, LIR2, LIR1):
        cmd = bytearray(2)
        cmd[0] = 0x24;
        cmd[1] = (TEMP_EN & 0x01) << 7
        cmd[1] |= (M_RES & 0x03) << 5
        cmd[1] |= (M_ODR & 0x07) << 2
        cmd[1] |= (LIR2 & 0x01) << 1
        cmd[1] |= (LIR1 & 0x01)
        self.busi2c.send(self.adresse, cmd)

    def ctrl6(self, MFS):
        cmd = bytearray(2)
        cmd[0] = 0x25;
        cmd[1] = (MFS & 0x03) << 5
        self.busi2c.send(self.adresse, cmd)

    def ctrl7(self, AHPM, AFDS, T_ONLY, MLP, MD):
        cmd = bytearray(2)
        cmd[0] = 0x26;
        cmd[1] = (AHPM & 0x03) << 6
        cmd[1] |= (AFDS & 0x01) << 5
        cmd[1] |= (T_ONLY & 0x01) << 4
        cmd[1] |= (MLP & 0x01) << 2
        cmd[1] |= (MD & 0x03)
        self.busi2c.send(self.adresse, cmd)

    def status_a(self):
        cmd = bytearray(1)
        cmd[0] = 0x27;
        data = self.busi2c.transferer(self.adresse, cmd, 1)[0]
        ZYXAOR = (data & 0x80) >> 7
        ZAOR = (data & 0x40) >> 6
        YAOR = (data & 0x20) >> 5
        XAOR = (data & 0x10) >> 4
        ZYXADA = (data & 0x08) >> 3
        ZADA = (data & 0x04) >> 2
        YADA = (data & 0x02) >> 1
        XADA = (data & 0x01)
        return ZYXAOR, ZAOR, YAOR, XAOR, ZYXADA, ZADA, YADA, XADA
