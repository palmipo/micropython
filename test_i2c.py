import rp2
from machine import Pin
from picoi2c import PicoI2C
from pca9548a import PCA9548A
# from is31fl3731 import IS31FL3731
# from bmp280 import BMP280
from ds1307 import DS1307
# from ds1621 import DS1621
# from mcp23017 import MCP23017
# from l298n import L298N
from lcd2004 import LCD2004
from hd44780 import HD44780
import onewire
import ds18x20
import time

class Test_I2C:
    def callback(self, pin):
        state = machine.disable_irq()
        self.action_callback = True
        machine.enable_irq(state)

    def __init__(self):
        self.action_callback = False
        self.i2c = PicoI2C(0, 4, 5)
        circuits = self.i2c.scan()
        print("liste des circuits i2c presents sur le bus :")
        print(circuits)

        if (len(circuits) != 0):
            self.mux = PCA9548A(0, self.i2c, 3)
            self.mux.reset()
            
            self.mux.setCanal((1<<2) | (1<<7)) # 2 : (0x27)lcd2004 # 7 : (0x50)memeoire / (0x68)rtc
            circuits = self.i2c.scan()
            print("liste des circuits i2c presents sur le bus multiplexe :")
            print(circuits)

    def onewire(self):
        ow = onewire.OneWire(Pin(7)) # create a OneWire bus on GPIO12
        print (ow.scan())               # return a list of devices on the bus
        ow.reset()              # reset the bus
        ds = ds18x20.DS18X20(ow)
        roms = ds.scan()
        ds.convert_temp()
        for rom in roms:
            self.lcd.writeText(str(ds.read_temp(rom)))

    def lcd2004(self):
        self.lcd_io = LCD2004(0, self.i2c)
        self.lcd_io.setBackLight(1)
        self.lcd = HD44780(self.lcd_io)
        self.lcd.clear()
        self.lcd.home()
        self.lcd.writeText("Hello World !")

    def bmp280(self):
        bmp = BMP280(self.i2c)
        if bmp.chipIdRegister():
            bmp.reset()
            time.sleep(1)
            bmp.ctrlMeasureRegister(5, 5, 3)
            bmp.configRegister(4, 4)
            bmp.readCompensationRegister()
            bmp.ctrlMeasureRegister(5, 5, 3)
            print(bmp.rawMeasureRegister())
            print(bmp.compensateT())
            time.sleep(1)
            print(bmp.rawMeasureRegister())
            print(bmp.compensateT())
            time.sleep(1)
            print(bmp.rawMeasureRegister())
            print(bmp.compensateT())
            time.sleep(1)
            print(bmp.rawMeasureRegister())
            print(bmp.compensateT())

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
        self.rtc = DS1307(0, self.i2c, 6, self.callback)
        self.rtc.setDate("10/11/22")
        self.rtc.setTime("09:10:30")
        self.rtc.setSquareWave(1)
        self.rtc.setDayWeek(3)
#         self.rtc.setOut(0)

    def led(self):
        self.led = Pin(25, Pin.OUT)

    def l298h(self):
        pontH1 = L298N(15, 10, 11)
        pontH1.forward(65535)

        pontH2 = L298N(16, 13, 12)
        pontH2.forward(65535)
        
        time.sleep(5)

        pontH1.off()
        pontH2.off()

try:
    test = Test_I2C()
    test.lcd2004()
    test.lcd.clear()
    test.onewire()
    test.ds1307()
    while True:
        if test.action_callback == True:
            try:
                texte = test.rtc.getDate() + " " + test.rtc.getTime()
#                 roms = test.ds.scan()
#                 test.ds.convert_temp()
#                 for rom in roms:
#                     texte += (str(ds.read_temp(rom)))
                test.lcd.home()
                test.lcd.writeText(texte)
            except:
                print("exception")
        test.action_callback = False
        time.sleep_ms(100)
    test.mux.clear()
    print("FIN.")
except:
    print("exception dans main !")
