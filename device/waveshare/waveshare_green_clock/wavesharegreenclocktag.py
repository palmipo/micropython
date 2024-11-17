from device.waveshare.waveshare_green_clock.wavesharegreenclockcodec import WaveshareGreenClockCodec

class WaveshareGreenClockTag:
    def __init__(self, buffer):
        self.codec = WaveshareGreenClockCodec()
        self.buffer = buffer
        
    def clear(self):
        for i in range(len(self.buffer)):
            self.buffer[i] = 0

    def setDayWeek(self, day):
        if day == 0: # lundi
            self.codec.encode(self.codec.Champ(self.buffer, 3, 2), self.codec.Champ(b'\xff', 0, 2))
        elif day == 1: # mardi
            self.codec.encode(self.codec.Champ(self.buffer, 6, 2), self.codec.Champ(b'\xff', 0, 2))
        elif day == 2: # mercredi
            self.codec.encode(self.codec.Champ(self.buffer, 9, 2), self.codec.Champ(b'\xff', 0, 2))
        elif day == 3: # jeudi
            self.codec.encode(self.codec.Champ(self.buffer, 12, 2), self.codec.Champ(b'\xff', 0, 2))
        elif day == 4: # vendredi
            self.codec.encode(self.codec.Champ(self.buffer, 15, 2), self.codec.Champ(b'\xff', 0, 2))
        elif day == 5: # samedi
            self.codec.encode(self.codec.Champ(self.buffer, 18, 2), self.codec.Champ(b'\xff', 0, 2))
        elif day == 6: # dimanche
            self.codec.encode(self.codec.Champ(self.buffer, 21, 2), self.codec.Champ(b'\xff', 0, 2))
            
    def led(self, led1, led2):
        self.codec.encode(self.codec.Champ(self.buffer, 2, 1), self.codec.Champ(led1, 0, 1))
        self.codec.encode(self.codec.Champ(self.buffer, 5, 1), self.codec.Champ(led2, 0, 1))

            
    def uniteTemperature(self, degree, farehein):
        self.codec.encode(self.codec.Champ(self.buffer, 97, 1), self.codec.Champ(degree, 0, 1))
        self.codec.encode(self.codec.Champ(self.buffer, 96, 1), self.codec.Champ(farehein, 0, 1))

# Octet           0        1        2        3
# MoveOn    = 00000011 00000000 00000000 00000000
# LED 1     = 00000100 00000000 00000000 00000000
# MON       = 00011000 00000000 00000000 00000000
# LED 2     = 00100000 00000000 00000000 00000000
# TUES      = 11000000 00000000 00000000 00000000
# WED       = 00000000 00000110 00000000 00000000
# THUR      = 00000000 00110000 00000000 00000000
# FRI       = 00000000 10000000 00000001 00000000
# SAT       = 00000000 00000000 00001100 00000000
# SUN       = 00000000 00000000 01100000 00000000

# Octet           4        5        6        7
# AlarmOn   = 00000011

# Octet           8        9       10       11
# CountDown = 00000011

# Octet          12       13       14       15
# °F        = 00000001
# °C        = 00000010

# Octet          16       17        18       19
# AM        = 00000001
# PM        = 00000010

# Octet          20       21       22       23
# CountUp   = 00000011

# Octet          24       25       26       27
# Hourly    = 00000011

# Octet          28       29       30        31
# AutoLight =  00000011

