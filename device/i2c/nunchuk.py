from device.i2c.devicei2c import DeviceI2C
import time, struct

#  http://domoticx.com/pinout-wii-nunchuk/
#  connections to Arduino
#  gnd   -- white  -- gnd
#  +3.3V -- red    -- 3.3V
#  SDA   -- green  -- sda
#  SCK   -- yellow -- scl

class Nunchuk(DeviceI2C):

    def __init__(self, bus):
        super().__init__(0x52, bus)

        # nunchuk noir
        self.busi2c.send(self.adresse, b'\xF0\x55')
        self.busi2c.send(self.adresse, b'\xFB\x00')

        # nunchuk blanc
        #self.busi2c.send(self.adresse, b'\x40\x00')
        #self.busi2c.send(self.adresse, b'\x00')

    def lecture(self):
        self.busi2c.send(self.adresse, b'\x00')
        time.sleep_ms(10)

        msg = self.busi2c.recv(0x52, 6)
        self.joy_x_axis, self.joy_y_axis, accel_xx, accel_yy, accel_zz, bp = struct.unpack('!BBBBBB', msg, 0)
        self.accel_x_axis = (accel_xx << 2) | ((bp >> 6) & 0x03)
        self.accel_y_axis = (accel_yy << 2) | ((bp >> 2) & 0x03)
        self.accel_z_axis = (accel_zz << 2) | ((bp >> 4) & 0x03)
        self.c_button = (bp >> 1) & 0x01
        self.z_button = bp & 0x01

    def get_joy_axis(self):
        return self.joy_x_axis, self.joy_y_axis

    def get_accel_axis(self):
        return self.accel_x_axis, self.accel_y_axis, self.accel_z_axis

    def get_buttons(self):
        return self.c_button, self.z_button

if __name__ == "__main__":
    try:
        from master.i2c.i2cpico import I2CPico

        i2c = I2CPico(1, 26, 27)
        print(i2c.scan())

        manette = Nunchuk(i2c)

        while True:
            manette.lecture()
            x, y = manette.get_joy_axis()
            accel_x, accel_y, accel_z = manette.get_accel_axis()
            bp_c, bp_z = manette.get_buttons()
            print("{:02} {:02} {:03} {:03} {:03} {} {}".format(x-127, y-127, accel_x-512, accel_y-512, accel_z-512, bp_c, bp_z))
            time.sleep(1)

    except KeyboardInterrupt:
        print("exit")
        sys.exit()
