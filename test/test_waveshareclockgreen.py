import ntptime, network, framebuf, sys, time
from wavesharegreenclock import WaveshareGreenClock
from wavesharegreenclockapps import WaveshareGreenClockApps
from wavesharegreenclockascii import WaveshareGreenClockAscii
from wavesharegreenclockcodec import WaveshareGreenClockCodec


# class AppTime(WaveshareGreenClockApps):
#     def __init__(self):
#         wlan = network.WLAN(network.STA_IF)
#         wlan.active(True)
#         wlan.connect('domoticus', '9foF2sxArWU5')
#         while not wlan.isconnected() and wlan.status() >= 0:
#             time.sleep(1)
#         time.sleep(5)
#         
#         data_tuple = time.localtime()
#         laDate = "{:02}/{:02}/{:02}".format(data_tuple[2], data_tuple[1], data_tuple[0])
#         lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])
#         clock.rtc.setDate(laDate)
#         clock.rtc.setDayWeek(str(data_tuple[6]))
#         clock.rtc.setTime(lHeure)
# 
#     def cb_up(self):
#         ntptime.settime() # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
# 
#     def run(self, buffer):
#         self.encode(self.Champ(self.picture, 2, 22), self.Champ(buffer, width * (i-1), 22))
# 
#     def cb_down(self):
#         print('down')
# 
#     def cb_rtc(self):
#         print('rtc')
# 
# 
# class AppCompteur(WaveshareGreenClockApps):
    # def __init__(self):
        # width = 256
        # height = 7
        # buffer = bytearray((width * height) >> 3)
        # frame = framebuf.FrameBuffer(buffer, width, height, framebuf.MONO_HMSB) # 154 bits / 20 octets
        # frame.fill(0)
        # temp = clock.rtc.getTemperature()
        # frame.text("{}".format(str(float(temp))), 10, 0)
    
    # def cb_up(self):
        # print('up')

    # def run(self, buffer):
        # temp = clock.rtc.getTemperature()

    # def cb_down(self):
        # print('down')

    # def cb_rtc(self):
        # print('rtc')

class AppCompteur(WaveshareGreenClockApps):
    def __init__(self):
        self.codec = WaveshareGreenClockCodec()
        self.ascii = WaveshareGreenClockAscii()
        self.cpt_gauche = 0
        self.cpt_droit = 0

    def cb_up(self):
        self.cpt_gauche += 1

    def cb_down(self):
        self.cpt_droit += 1

    def cb_rtc(self):
        print('rtc')

    def run(self, buffer):
        clock.column.OutputDisable()
        texte = '{}:{}'.format(str(self.cpt_gauche), str(self.cpt_droit)) 
        offset = 0
        for i in range(len(texte)):
            (a, w, h) = self.ascii.encode(texte[i])
            for j in range(h):
                self.codec.encode(self.codec.Champ(buffer, offset + 2 + (j+1) * 32, w), self.codec.Champ(a, j * 8, w))
            offset += w + 1
        clock.column.OutputEnable()

class AppTemperature(WaveshareGreenClockApps):
    def __init__(self):
        self.codec = WaveshareGreenClockCodec()
        self.ascii = WaveshareGreenClockAscii()

    def cb_up(self):
        print('up')

    def cb_down(self):
        print('down')

    def cb_rtc(self):
        print('rtc')

    def run(self, buffer):
        clock.column.OutputDisable()
        temp = clock.rtc.getTemperature()
        texte = str(temp)
        offset = 0
        buffer[3*4] = 0x2
        for i in range(len(texte)):
            (a, w, h) = self.ascii.encode(texte[i])
            for j in range(h):
                self.codec.encode(self.codec.Champ(buffer, offset + 2 + (j+1) * 32, w), self.codec.Champ(a, j * 8, w))
            offset += w + 1
        clock.column.OutputEnable()



buffer = bytearray(4*8)
app_temp = AppCompteur()
clock = WaveshareGreenClock()
clock.column.OutputEnable()

while True:
    app_temp.run(buffer)
    clock.show(buffer)
