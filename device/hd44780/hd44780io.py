class HD44780IO:

    self.BACKLIGHT = 0
    self.DB7 = 1
    self.DB6 = 2
    self.DB5 = 3
    self.DB4 = 4
    self.EN = 5
    self.RW_ = 6
    self.RS = 7

    def writeCmd(self, value):
        raise NotImplementedError

    def writeData(self, value):
        raise NotImplementedError

    def readCmd(self):
        raise NotImplementedError

    def readData(self):
        raise NotImplementedError

    def write (self, value, rs, rw_, en):
        raise NotImplementedError

    def setBackLight(self, value):
        raise NotImplementedError

    def bitMode(self):
        raise NotImplementedError

    def nLine(self):
        raise NotImplementedError

    def fontMode(self):
        raise NotImplementedError
