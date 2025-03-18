# On a black Wii Nunchuk, send 0xF0, 0x55 followed by 0xFB, 0x00.
# On a white Wii Nunchuk, send 0x40, 0x00 followed by 0x00.
# The I2C address of both Wii Nunchuks is 0x52.
# The frequency used to communicate with the Wii Nunchuk is 100KHz.

import sys, struct, machine, time

try:
    i2c = machine.I2C(id=1, sda=machine.Pin(26), scl=machine.Pin(27), freq=400000)
    print(i2c.scan())
    time.sleep_ms(100)

    # black
    i2c.writeto(0x52, b'\xF0\x55')
    i2c.writeto(0x52, b'\xFB\x00')
    time.sleep_ms(100)

    # white
#     i2c.writeto(0x52, b'\x40\x00')
#     i2c.writeto(0x52, b'\x00')
#     time.sleep_ms(100)
    
    while True:
        i2c.writeto(0x52, b'\x00')
        time.sleep_ms(10)

        msg = i2c.readfrom(0x52, 6)
        x, y, accel_xx, accel_yy, accel_zz, bp = struct.unpack('!BBBBBB', msg, 0)
        accel_x = (accel_xx << 2) | ((bp >> 6) & 0x03)
        accel_y = (accel_yy << 2) | ((bp >> 2) & 0x03)
        accel_z = (accel_zz << 2) | ((bp >> 4) & 0x03)
        bp_c = (bp >> 1) & 0x01
        bp_z = bp & 0x01
        print("{:02} {:02} {:03} {:03} {:03} {} {}".format(x-127, y-127, accel_x-512, accel_y-512, accel_z-512, bp_c, bp_z))

        time.sleep(1)
    

#     manette = Nunchuk(i2c)
except KeyboardInterrupt:
    print("quit")
    sys.quit()


