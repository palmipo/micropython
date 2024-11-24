from master.i2c.i2cpico import I2CPico
from device.i2c.ds1307_sqw import DS1307_SQW
from master.pia.piapico import PiaOutputPico
from master.pia.piaisrpico import PiaIsrPico
from master.net.wlanpico import WLanPico
from device.hc1632.hc1632matrix import Hc1632Matrix
import micropython
import machine, time
import onewire, ds18x20

class Aff:
    def __init__(self):
        try:
            self.i2c = I2CPico(0, 4, 5)
            self.rtc = DS1307_SQW(0, self.i2c, 7)
            self.rtc.setSquareWave(0x01)
        except OSError:
            print('erreur i2c')
        
        self.bp_pin = []
        self.bp_pin.append(PiaIsrPico(20))
        self.bp_pin.append(PiaIsrPico(21))
        self.bp_pin.append(PiaIsrPico(22))

        self.data_pin = PiaOutputPico(8)
        self.write_pin = PiaOutputPico(9)
        self.cs_pin = []
        self.cs_pin.append(PiaOutputPico(14))
        self.cs_pin.append(PiaOutputPico(12))
        self.cs_pin.append(PiaOutputPico(10))
        self.cs_pin.append(PiaOutputPico(16))
        self.cs_pin.append(PiaOutputPico(18))
        self.cs_pin.append(PiaOutputPico(15))
        self.cs_pin.append(PiaOutputPico(13))
        self.cs_pin.append(PiaOutputPico(11))
        self.cs_pin.append(PiaOutputPico(17))
        self.cs_pin.append(PiaOutputPico(19))

        self.paint = Hc1632Matrix(5, 2, self.data_pin, self.write_pin, self.cs_pin)
        self.paint.fill(0)
        self.paint.show()

        self.wlan = WLanPico()
        self.wlan.connect()

        self.paint.text(self.wlan.ifconfig(), 0, 0)
        self.paint.show()

#         try:
#             data_tuple = self.wlan.ntp()
#             laDate = "{:02}/{:02}/{:02}".format(data_tuple[2], data_tuple[1], data_tuple[0])
#             lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])
#             self.rtc.setDayWeek(data_tuple[6])
#             self.rtc.setDate(laDate)
#             self.rtc.setTime(lHeure)
#         except OSError:
#             print('erreur ntptime')

#         try:
#             self.paint.text(self.rtc.getDate(), 0, 30)
#             self.paint.text(self.rtc.getTime(), 0, 40)
#             self.paint.show()
#         except OSError:
#             print("erreur i2c")


try:

# import socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind((wlan.ifconfig()[0], 2222))
# sock.listen(1)
# (clientsocket, (ip, port)) = sock.accept()
# buffer = clientsocket.recv(48 * 48).decode()
# clientsocket.close()
# sock.close()

#     ow = onewire.OneWire(machine.Pin(6)) # create a OneWire bus on GPIO12
#     print(ow.scan())               # return a list of devices on the bus
#     ow.reset()              # reset the bus
#     ds = ds18x20.DS18X20(ow)
#     roms = ds.scan()
#     print(roms)
#     ds.convert_temp()
#     time.sleep_ms(750)
#     for rom in roms:
#         print(ds.read_temp(rom))

    aff = Aff()
    fin = False
    while fin == False:
        if aff.rtc.isActivated() == True:
            print('rtc')
        
        for bp in aff.bp_pin:
            if bp.isActivated() == True:
                print('bp')

#         aff.paint.fill(0)
#         try:
#             aff.paint.text(aff.wlan.ifconfig(), 0, 0)
#         except OSError:
#                 print("erreur wlan")
#                 
#             try:
#                 aff.paint.text('{:02}'.format(ds.read_temp(roms[0])), 0, 20)
#             except OSError:
#                 print("erreur OneWire")
            
#             try:
#                 aff.paint.text(aff.rtc.getDate(), 0, 30)
#                 aff.paint.text(aff.rtc.getTime(), 0, 40)
#             except OSError:
#                 print("erreur i2c")
            
#         aff.paint.show()
#         ds.convert_temp()

except KeyboardInterrupt:
    fin = True
    print("quit")

finally:
  aff.wlan.disconnect()

