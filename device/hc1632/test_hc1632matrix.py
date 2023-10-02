from i2cpico import I2CPico
from ds1307 import DS1307
from piapico import PiaPico
from hc1632matrix import Hc1632Matrix
import micropython
import machine
import network, time, ntptime, ubinascii
import onewire, ds18x20

micropython.alloc_emergency_exception_buf(100)

class Aff:
    def __init__(self):
        self.i2c = I2CPico(0, 4, 5)
        self.rtc = DS1307(0, self.i2c)
        self.rtc.setSquareWave(0)
        maj = 0
        self.pinSQW = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_UP)
        self.pinSQW.irq(handler=self.callback, trigger=machine.Pin.IRQ_FALLING, hard=True)
        
        self.bp_pin = []
        self.bp_pin.append(PiaPico(20, self.irq))
        self.bp_pin.append(PiaPico(21, self.irq))
        self.bp_pin.append(PiaPico(22, self.irq))

        self.data_pin = PiaPico(8)
        self.write_pin = PiaPico(9)
        self.cs_pin = []
        self.cs_pin.append(PiaPico(14))
        self.cs_pin.append(PiaPico(12))
        self.cs_pin.append(PiaPico(10))
        self.cs_pin.append(PiaPico(16))
        self.cs_pin.append(PiaPico(18))
        self.cs_pin.append(PiaPico(15))
        self.cs_pin.append(PiaPico(13))
        self.cs_pin.append(PiaPico(11))
        self.cs_pin.append(PiaPico(17))
        self.cs_pin.append(PiaPico(19))

        self.paint = Hc1632Matrix(5, 2, self.data_pin, self.write_pin, self.cs_pin)
        self.paint.fill(0)
        self.paint.show()

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect('domoticus', '9foF2sxArWU5')
        while not self.wlan.isconnected() and self.wlan.status() >= 0:
            time.sleep(1)
        time.sleep(5)

        self.paint.text(self.wlan.ifconfig()[0], 0, 0)
        self.paint.show()

        try:
            ntptime.settime() # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
            data_tuple = time.localtime()
            laDate = "{:02}/{:02}/{:02}".format(data_tuple[2], data_tuple[1], data_tuple[0])
            lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])
            self.rtc.setDayWeek(data_tuple[6])
            self.rtc.setDate(laDate)
            self.rtc.setTime(lHeure)
        except OSError:
            print('erreur ntptime')

        self.paint.text(self.rtc.getDate(), 0, 30)
        self.paint.text(self.rtc.getTime(), 0, 40)
        self.paint.show()

    def callback(self, pin):
        state = machine.disable_irq()
        global maj
        maj = 1
        machine.enable_irq(state)


    def irq(self, pin):
        state = machine.disable_irq()
        self.print('appui sur bp {}'.format(pin))
        machine.enable_irq(state)



# import socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind((wlan.ifconfig()[0], 2222))
# sock.listen(1)
# (clientsocket, (ip, port)) = sock.accept()
# buffer = clientsocket.recv(48 * 48).decode()
# clientsocket.close()
# sock.close()

ow = onewire.OneWire(machine.Pin(6)) # create a OneWire bus on GPIO12
print(ow.scan())               # return a list of devices on the bus
ow.reset()              # reset the bus
ds = ds18x20.DS18X20(ow)
roms = ds.scan()
print(roms)
ds.convert_temp()
time.sleep_ms(750)
for rom in roms:
    print(ds.read_temp(rom))

i=0
aff = Aff()
while True:
    if maj == 1:
        ds.convert_temp()
        aff.paint.fill(0)
        aff.paint.text(aff.wlan.ifconfig()[0], 0, 0)
        aff.paint.text('{}'.format(ds.read_temp(roms[0])), 0, 20)
        aff.paint.text(aff.rtc.getDate(), 0, 30)
        aff.paint.text(aff.rtc.getTime(), 0, 40)
        aff.paint.show()
        maj = 0
        i -= 5
        if i==10:
            i=0

# wlan.disconnect()

