import rp2
import machine
from picoi2c import PicoI2C
from muxi2c import MuxI2C
from pca9548a import PCA9548A
# from is31fl3731 import IS31FL3731
from bmp280 import BMP280
from ds1307 import DS1307
# from ds1621 import DS1621
# from mcp23017 import MCP23017
# from l298n import L298N
from lcd2004 import LCD2004
from hd44780 import HD44780
from pca9685 import PCA9685
from rouecodeuse import RoueCodeuse
import onewire
import ds18x20
import time
import micropython
micropython.alloc_emergency_exception_buf(100)

class Test_I2C:
    def callbackDs1307(self, pin):
        state = machine.disable_irq()
        self.action_callback = True
        machine.enable_irq(state)
        
    def __init__(self):
        self.action_callback = False
        self.stop_bt = False
        self.i2c = PicoI2C(0, 4, 5)
        circuits = self.i2c.scan()
        print("liste des circuits i2c presents sur le bus :")
        print(circuits)

        if (len(circuits) != 0):
            self.pca9548a = PCA9548A(0, self.i2c, 3)
            self.pca9548a.reset()
            time.sleep_ms(100)

            self.mux2 = MuxI2C(2, self.pca9548a, self.i2c)
            print(self.mux2.scan())

            self.mux3 = MuxI2C(3, self.pca9548a, self.i2c)
            print(self.mux3.scan())

            self.mux5 = MuxI2C(5, self.pca9548a, self.i2c)
            print(self.mux5.scan())

            self.mux6 = MuxI2C(6, self.pca9548a, self.i2c)
            print(self.mux6.scan())

            self.mux7 = MuxI2C(7, self.pca9548a, self.i2c)
            print(self.mux7.scan())

        self.code = RoueCodeuse(8, 9, 10)

    def pca8596(self):
        self.pca9685 = PCA9685(0, self.mux6)
        self.pca9685.mode1(50)
        for i in range(1, 512):
            self.pca9685.allLed(0, i)
            time.sleep_ms(10)
        self.pca9685.allLedOff()

    def onewire(self):
        self.ow = onewire.OneWire(machine.Pin(7)) # create a OneWire bus on GPIO12
        print (self.ow.scan())               # return a list of devices on the bus
        self.ow.reset()              # reset the bus
        self.ds = ds18x20.DS18X20(self.ow)
        roms = self.ds.scan()
        self.ds.convert_temp()
#         for rom in roms:
#             time.sleep(60)
#             self.lcd.writeText(ds.read_temp(rom))

    def lcd2004(self):
        self.lcd_io = LCD2004(0, self.mux2)
        self.lcd_io.setBackLight(1)
        self.lcd = HD44780(self.lcd_io)
        self.lcd.clear()
        self.lcd.home()
        self.lcd.writeText("Hello World !")

    def bmp280(self):
        self.bmp = BMP280(self.mux3)
        if self.bmp.chipIdRegister():
            self.bmp.reset()
            time.sleep(1)
            self.bmp.configRegister(4, 4)
            self.bmp.readCompensationRegister()
            self.bmp.ctrlMeasureRegister(5, 5, 3)

    def is313731(self):
        matrix = IS31FL3731(0, self.i2c)
        matrix.shutdown(1)
        time.sleep(1)

        matrix.configurationRegister(0, 0)
        matrix.pictureDisplayRegister(0)
        matrix.displayOptionRegister(0, 1, 1)
        matrix.autoplayControlRegister(0, 0, 0)
        matrix.breathControlRegister(0, 0, 0, 0)

        led = bytearray(18)
        blink = bytearray(18)
        pwm = bytearray(144)

        for i in range(0, 18):
            led[i] = 0
            blink[i] = 0

        for i in range(0, 144):
            pwm[i]=0xf

        for i in range(0, 8):
            matrix.frameRegister(i, led, blink, pwm)

        while True:
            for i in range(0, 18):
                led[i] = 0xff
                matrix.frameRegister(0, led, blink, pwm)
                time.sleep_ms(10)
            for i in range(0, 18):
                led[17-i] = 0
                matrix.frameRegister(0, led, blink, pwm)
                time.sleep_ms(10)
        matrix.shutdown(0)

    def ds1621(self):
        t = DS1621(0, self.i2c)
        t.start()
        for i in range(0, 10):
            print(t.readTemperature())
        t.stop()
    
    def ds1307(self):
        self.rtc = DS1307(0, self.mux7)
        self.rtc.setDate("14/12/22")
        self.rtc.setTime("20:06:30")
        self.rtc.setSquareWave(1)
        self.rtc.setDayWeek(3)

        self.pin6 = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_UP)
        self.pin6.irq(self.callbackDs1307, machine.Pin.IRQ_FALLING, hard=True)

    def led(self):
        self.led = machine.Pin(25, machine.Pin.OUT)

try:
    test = Test_I2C()
    test.lcd2004()
    #test.onewire()
    test.pca8596()
    test.bmp280()
    test.lcd.clear()
    test.lcd.writeText("Hello World !!!")
    test.ds1307()
    while test.stop_bt == False:
        if test.action_callback == True:
            try:
                texte = " " + test.rtc.getDate() + "  " + test.rtc.getTime() + " "
                mesuring, im_update = test.bmp.statusRegister()
                while mesuring != 0:
                    mesuring, im_update = test.bmp.statusRegister()
                test.bmp.rawMeasureRegister()
                t = test.bmp.compensateT()
                texte += "temperature : " + str(t) + "  "
                test.lcd.home()
                test.lcd.writeText(texte)
            except:
                print("exception")
            test.action_callback = False
        time.sleep_ms(100)
    test.pca9548a.clear()
    print("FIN.")
except:
    print("exception dans main !")
