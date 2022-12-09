class HD44780IO:

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
