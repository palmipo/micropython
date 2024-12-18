from device.afficheur.oled_0inch91 import OLED_0inch91
# from oled_1_3 import OLED_1_3
from master.i2c.i2cpico import I2CPico
from master.i2c.i2cmux import I2CMux
from device.i2c.pca9548a import PCA9548A
from device.i2c.ds1307 import DS1307
from pimoroni.scrollphathd import ScrollPHatHd
from device.hd44780.lcd2004 import LCD2004
from device.hd44780.hd44780 import HD44780
# from master.net.wlanpico import WLanPico
# import network
import framebuf
import sys
import time

try:    # wlan = WLanPico(network.STA_IF)

    i2c = I2CPico(0, 4, 5) 
    print(i2c.scan())

    switch = PCA9548A(0, i2c, 3)
    switch.reset()

    # wlan.ntp() # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
    data_tuple = time.localtime()
    laDate = "{:02}/{:02}/{:02}".format(str(data_tuple[2]), str(data_tuple[1]), str(data_tuple[0]))
    lHeure = "{:02}:{:02}:{:02}".format(str(data_tuple[3]), str(data_tuple[4]), str(data_tuple[5]))

    mux0 = I2CMux(0, switch)
    print(mux0.scan())
    mux1 = I2CMux(1, switch)
    print(mux1.scan())
    mux6 = I2CMux(6, switch)
    print(mux6.scan())
    mux7 = I2CMux(7, switch)
    print(mux7.scan())

#     try:
#         lcd_io = LCD2004(0, i2c)
#         lcd_io.setBackLight(1)
#         lcd = HD44780(lcd_io)
#         lcd.clear()
#     except OSError:
#         print("erreur LCD2004")


    matrix = ScrollPHatHd(mux7)
    for y in range(matrix.height):
        for x in range(matrix.width):
            matrix.pixel(x, y, 0xF)
            matrix.show()
            time.sleep_ms(100)

    rtc = DS1307(0, mux1)
    rtc.setDate(laDate)
    rtc.setDayWeek(4)
    rtc.setTime(lHeure)

    display = OLED_0inch91(0, mux0)
    # display = OLED_1_3(0, mux0)
    try:
        display.init_display()
        display.setDisplayON()
        display.setEntireDisplayON()
        time.sleep(1)
        display.setEntireDisplayOFF()
    except OSError:
        print("erreur i2c")

    buffer = bytearray(display.width * (display.height >> 3))
    frame = framebuf.FrameBuffer(buffer, display.width, display.height, framebuf.MONO_VLSB)

    while True:
        frame.fill(0)
        frame.text('Hello World !!!', 0, 0)
        try:
            frame.text(rtc.getTime(), 0, 11)
            frame.text(rtc.getDate(), 0, 22)
        except OSError:
            print("erreur DS1307")
        display.show(buffer)

    #     try:
    #         lcd.home()
    #         lcd.writeText("Hello World !!!")
    #         lcd.setDDRAMAdrress(32)
    #         lcd.writeText(rtc.getTime())
    #         lcd.setDDRAMAdrress(20)
    #         lcd.writeText(rtc.getDate())
    #     except OSError:
    #         print("erreur LCD2004")
        time.sleep_ms(200)

    time.sleep(5)
    display.setDisplayOFF()

    switch.clear()
except KeyboardInterrupt:
    print("quit")
