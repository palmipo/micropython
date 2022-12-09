from hd44780io import HD44780IO
import time

class HD44780:
    def __init__(self, ctrl_io):
        self.ctrl = ctrl_io
        self.init()

    def writeText(self, texte):
#         print("writeText")
        for i in range(0, len(texte)):
            self.ctrl.writeData(texte[i].encode()[0])

    def clear(self):
#         print("clear")
        self.ctrl.writeCmd(0x01)
        time.sleep_ms(2)

    def home(self):
#         print("home")
        self.ctrl.writeCmd(0x02)
        time.sleep_ms(2)

    def setEntryMode(self, increment, shift):
#         print("setEntryMode")
        self.ctrl.writeCmd(0x04 | ((increment & 0x01) << 1) | (shift & 0x01))

    def setDisplayControl(self, displayOn, cursorOn, blinkingCursor):
#         print("setDisplayControl")
        self.ctrl.writeCmd(0x08 | ((displayOn & 0x1) << 2) | ((cursorOn & 0x1) << 1) | (blinkingCursor & 0x1))

    def setCursorDisplayShift(self, displayShift, shiftToRight):
#         print("setCursorDisplayShift")
        self.ctrl.writeCmd(0x10 | ((displayShift & 0x1) << 3) | ((shiftToRight & 0x1) << 2))

    def setFunction(self, dataLength, numberLine, characterFont):
#         print("setFunction")
        self.ctrl.writeCmd(0x20 | ((dataLength & 0x1) << 4) | ((numberLine & 0x1) << 3) | ((characterFont & 0x1) << 2))

    def setCGRAMAdrress(self, address):
#         print("setCGRAMAdrress")
        self.ctrl.writeCmd(0x40 | (address & 0x3F))

    def setDDRAMAdrress(self, address):
#         print("setDDRAMAdrress")
        self.ctrl.writeCmd(0x80 | (address & 0x7F))

    def init(self):
#         print("init")
        self.reset() # Call LCD reset
        self.setFunction(self.ctrl.bitMode(), self.ctrl.nLine(), self.ctrl.fontMode()) #4-bit mode - 2 lines - 5x8 font.
        self.setDisplayControl(1, 0, 0) # Display no cursor - no blink.
        self.setEntryMode(1, 0) # Automatic Increment - No Display shift.
        self.setCursorDisplayShift(0, 0)

    def reset(self):
#         print("reset")
        time.sleep_ms(15)

        self.ctrl.write(0x30, 0, 0, 0)
        time.sleep_ms(5)

        self.ctrl.write(0x30, 0, 0, 0)
        time.sleep_ms(1)

        self.ctrl.write(0x30, 0, 0, 0)
        time.sleep_ms(1)

        self.ctrl.write(0x20, 0, 0, 0)
        time.sleep_ms(15)


