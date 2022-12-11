import rp2
from machine import Pin
import onewire
import time, ds18x20

ow = onewire.OneWire(Pin(7)) # create a OneWire bus on GPIO12
print (ow.scan())               # return a list of devices on the bus
ow.reset()              # reset the bus
ds = ds18x20.DS18X20(ow)
roms = ds.scan()
ds.convert_temp()
while True:
    time.sleep(60)
    for rom in roms:
        print(ds.read_temp(rom))
