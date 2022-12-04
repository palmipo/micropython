from devicei2c import DeviceI2C

#  http://domoticx.com/pinout-wii-nunchuk/
#  connections to Arduino
#  gnd   -- white  -- gnd
#  +3.3V -- red    -- 3.3V
#  SDA   -- green  -- sda
#  SCK   -- yellow -- scl

class Nunchuk(DeviceI2C):

    def __init__(self, bus):
        super().__init__(0x52, bus)

    def init(self):
        buf = bytearray(2)
        buf[0] = 0x40;
        buf[1] = 0x00;
        self.busi2c.send(self.adresse, buf)

        buf[0] = 0xFB;
        buf[1] = 0x00;
        self.busi2c.send(self.adresse, buf)

    def get_joy_x_axis(self):
        return self.joy_x_axis

    def get_joy_y_axis(self):
        return self.joy_y_axis

    def get_accel_x_axis(self):
        return self.accel_x_axis

    def get_accel_y_axis(self):
        return self.accel_y_axis

    def get_accel_z_axis(self):
        return self.accel_z_axis

    def get_z_button(self):
        return self.z_button

    def get_c_button(self):
        return self.c_button

    def lecture(self):
        cmd = bytearray(1)
        cmd[0] = 0x00
        msg = self.busi2c.transferer(self.adresse, cmd)

        buf = bytearray(6)
        for i in range(0, len(msg)):
            buf[i] = decode_byte(msg[i]);

        self.joy_x_axis = buf[0];
        self.joy_y_axis = buf[1];

        self.accel_x_axis = ((buf[2] << 2) | ((buf[5] >> 2) & 0x03));
        self.accel_y_axis = ((buf[3] << 2) | ((buf[5] >> 4) & 0x03));
        self.accel_z_axis = ((buf[4] << 2) | ((buf[5] >> 6) & 0x03));

        self.z_button = ! (buf[5] & 0x01);
        self.c_button = !((buf[5] >> 1) & 0x01);

    def decode_byte(self, x)
        return (x ^ 0x17) + 0x17
