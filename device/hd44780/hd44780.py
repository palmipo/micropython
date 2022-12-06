from hd44780io import HD44780IO
import time

class HD44780:
    def __init__(self, ctrl_io):
        self.ctrl = ctrl_io
        self.init()
        self.clear()

    def writeText(self, texte):
        for i in range(0, len(texte)):
            self.ctrl.writeData(texte[i])

    def clear(self):
        self.ctrl.writeCmd(0x01)

    def home(self):
        self.ctrl.writeCmd(0x02)

    def setEntryMode(self, increment, shift):
        self.ctrl.writeCmd(0x04 | ((increment & 0x01) << 1) | (shift & 0x01))

    def setDisplayControl(self, displayOn, cursorOn, blinkingCursor):
        self.ctrl.writeCmd(0x08 | ((displayOn & 0x1) << 2) | ((cursorOn & 0x1) << 1) | (blinkingCursor & 0x1))

    def setCursorDisplayShift(self, displayShift, shiftToRight):
        self.ctrl.writeCmd(0x10 | ((displayShift & 0x1) << 3) | ((shiftToRight & 0x1) << 2))

    def setFunction(self, dataLength, numberLine, characterFont):
        self.ctrl.writeCmd(0x20 | ((dataLength & 0x1) << 4) | ((numberLine & 0x1) << 3) | ((characterFont & 0x1) << 2))

    def setCGRAMAdrress(self, address):
        self.ctrl.writeCmd(0x40 | (address & 0x3F))

    def setDDRAMAdrress(self, address):
        self.ctrl.writeCmd(0x80 | (address & 0x7F))

    def readAddress(self):
        return self.ctrl.readCmd()

    def readData(self):
        return self.ctrl.readData()

    def setPosition(self, line, column):
        if line == 0:
            pos = column;
        else:
            if line == 1:
                pos = 40 + column;
            else:
                if line == 2:
                    pos = 20 + column;
                else:
                    if line == 3:
                        pos = 60 + column;
        self.setDDRAMAdrress(pos)

    def init(self):
        self.reset() # Call LCD reset
        self.setFunction(self.ctrl.bitMode(), self.ctrl.nLine(), 0) #0, 1, 0 // 4-bit mode - 2 lines - 5x8 font.
        self.setDisplayControl(1, 0, 0) # Display no cursor - no blink.
        self.setEntryMode(1, 0) # Automatic Increment - No Display shift.
        self.setCursorDisplayShift(0, 0)

    def reset(self):
        time.sleep_ms(15)

        self.ctrl.write(0x30, 0, 0, 0)
        time.sleep_ms(45)

        self.ctrl.write(0x30, 0, 0, 0)
        time.sleep_ms(45)

        self.ctrl.write(0x30, 0, 0, 0)
        time.sleep_ms(15)

        self.ctrl.write(0x20, 0, 0, 0)
        time.sleep_ms(15)


