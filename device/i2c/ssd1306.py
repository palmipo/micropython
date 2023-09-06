from devicei2c import DeviceI2C
import time
 

class SSD1306(DeviceI2C):
    def __init__(self, width, heght, addr, bus):
        self.heght = heght
        self.width = width
        super().__init__(0x3C | (addr & 0x01), bus)

    def init_display(self):
        self.setDisplayON(0)
        self.setMemoryAddressingMode(0)
        self.setDisplayStartLine(0)
        self.setDisplayON(1)

    def initDisplay(self):
        self.TEMPO = 10
        #self.setDisplayOFF()
        time.sleep_ms(self.TEMPO)
        self.setMultiplexRatio(self.heght)
        time.sleep_ms(self.TEMPO)
        self.setDisplayOffset(0x00)
        time.sleep_ms(self.TEMPO)
        self.setDisplayStartLine(0x00)
        time.sleep_ms(self.TEMPO)
        self.setSegmentRemap(0x00)
        time.sleep_ms(self.TEMPO)
        self.setCOMOutputScanDirection(0x01)
        time.sleep_ms(self.TEMPO)
        self.SetCOMPinsHardwareConfiguration(0x00 if self.width > 2 * self.heght else 0x01)
        time.sleep_ms(self.TEMPO)
        self.setContrastControl(0x0F)
        time.sleep_ms(self.TEMPO)
        self.setEntireDisplayON(0x00)
        time.sleep_ms(self.TEMPO)
        self.setNormalDisplay(0x00)
        time.sleep_ms(self.TEMPO)
        self.setDisplayClockDivideRatioOscillatorFrequency(0x80)
        time.sleep_ms(self.TEMPO)
        self.setChargePumpSetting(0x01)
        time.sleep_ms(self.TEMPO)
        self.setDisplayON()
        time.sleep_ms(self.TEMPO)

    def show(self, buffer):
        self.setColumnAddress(0, self.width - 1)
        self.setPageAddress(0, 7)

        cmd = bytearray(1 + len(buffer))
        cmd[0] = 0x40 # Co=0 D/C=1
        cmd[1:] = buffer
        self.busi2c.send(self.adresse, cmd)

    def setContrastControl(self, valeur):
        cmd = bytearray(3)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0x81
        cmd[2] = valeur & 0xFF
        self.busi2c.send(self.adresse, cmd)

    def setChargePumpSetting(self, enable):
        cmd = bytearray(3)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0x8D
        cmd[2] = 0x10 | ((enable & 0x01) << 2)
        self.busi2c.send(self.adresse, cmd)

    def setEntireDisplayON(self, valeur):
        cmd = bytearray(2)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0xA4 | (valeur & 0x01)
        self.busi2c.send(self.adresse, cmd)

    def setNormalDisplay(self, valeur):
        cmd = bytearray(2)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0xA6 | (valeur & 0x01)
        self.busi2c.send(self.adresse, cmd)

    def setDisplayON(self):
        cmd = bytearray(2)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0xAF
        self.busi2c.send(self.adresse, cmd)

    def setDisplayOFF(self):
        cmd = bytearray(2)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0xAE
        self.busi2c.send(self.adresse, cmd)

    def continuousHorizontalScrollSetup(self, leftHorizontalScroll, startPageAddress, setTimeInterval, endPageAddress):
        cmd = bytearray(8)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0x26 | (leftHorizontalScroll & 0x01)
        cmd[2] = 0x00
        cmd[3] = startPageAddress & 0x07
        cmd[4] = setTimeInterval & 0x07
        cmd[5] = endPageAddress & 0x07
        cmd[6] = 0x00
        cmd[7] = 0xFF
        self.busi2c.send(self.adresse, cmd)

    def continuousVerticalHorizontalScrollSetup(self, leftHorizontalScroll, startPageAddress, setTimeInterval, endPageAddress):
        cmd = bytearray(7)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0x28 | (verticalAndRightHorizontalScroll & 0x01)
        cmd[2] = 0x28 | ((verticalAndLeftHorizontalScroll & 0x01) << 1)
        cmd[3] = startPageAddress & 0x07
        cmd[4] = setTimeInterval & 0x07
        cmd[5] = endPageAddress & 0x07
        cmd[6] = verticalScrollingOffset & 0x3F
        self.busi2c.send(self.adresse, cmd)

    def deactivateScroll(self):
        cmd = bytearray(2)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0x2E
        self.busi2c.send(self.adresse, cmd)

    def activateScroll(self):
        cmd = bytearray(2)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0x2F
        self.busi2c.send(self.adresse, cmd)

    def setVerticalScrollArea(self, setRowsInTopFixedArea, setRowsInScrollArea):
        cmd = bytearray(4)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0xA3
        cmd[2] = setRowsInTopFixedArea & 0x3F
        cmd[3] = setRowsInScrollArea & 0x7F
        self.busi2c.send(self.adresse, cmd)

    def setLowerColumnStartAddressForPageAddressingMode(self, setColumnStartAddressRegister):
        cmd = bytearray(2)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = setColumnStartAddressRegister & 0x0F
        self.busi2c.send(self.adresse, cmd)

        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0x10 | (setColumnStartAddressRegister >> 4)
        self.busi2c.send(self.adresse, cmd)

    def setMemoryAddressingMode(self, mode):
        cmd = bytearray(3)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0x20
        cmd[2] = mode & 0x03
        self.busi2c.send(self.adresse, cmd)

    def setColumnAddress(self, columnStartAddress, columnEndAddress):
        cmd = bytearray(4)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0x21
        cmd[2] = columnStartAddress & 0x7F
        cmd[3] = columnEndAddress & 0x7F
        self.busi2c.send(self.adresse, cmd)

    def setPageAddress(self, pageStartAddress, pageEndAddress):
        cmd = bytearray(4)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0x22
        cmd[2] = pageStartAddress & 0x07
        cmd[3] = pageEndAddress & 0x07
        self.busi2c.send(self.adresse, cmd)

    def setDisplayStartLine(self, displayStartLine):
        cmd = bytearray(2)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0x40 | (displayStartLine & 0x3F)
        self.busi2c.send(self.adresse, cmd)

    def setSegmentRemap(self, columnAddress0MappedtoSEG0):
        cmd = bytearray(2)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0xA0 | (columnAddress0MappedtoSEG0 & 0x01)
        self.busi2c.send(self.adresse, cmd)

    def setMultiplexRatio(self, valeur):
        cmd = bytearray(3)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0xA8
        cmd[2] = valeur & 0x3F
        self.busi2c.send(self.adresse, cmd)

    def setCOMOutputScanDirection(self, remappedMode):
        cmd = bytearray(2)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0xC0 | ((remappedMode & 0x01) << 3)
        self.busi2c.send(self.adresse, cmd)

    def setDisplayOffset(self, offset):
        cmd = bytearray(3)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0xD3
        cmd[2] = offset & 0x3F
        self.busi2c.send(self.adresse, cmd)

    def SetCOMPinsHardwareConfiguration(self, comPinConfiguration):
        cmd = bytearray(3)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0xDA
        cmd[2] = ((comPinConfiguration & 0x03) << 4) | 0x02
        self.busi2c.send(self.adresse, cmd)

    def setDisplayClockDivideRatioOscillatorFrequency(self, ratio):
        cmd = bytearray(3)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0xD5
        cmd[2] = ratio & 0xFF
        self.busi2c.send(self.adresse, cmd)

    def setPrechargePeriod(self, phase):
        cmd = bytearray(3)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0xD9
        cmd[2] = phase & 0xFF
        self.busi2c.send(self.adresse, cmd)

    def setVCOMHDeselectLevel(self, level):
        cmd = bytearray(3)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0xDB
        cmd[2] = (level & 0x07) << 4
        self.busi2c.send(self.adresse, cmd)

    def nop(self):
        cmd = bytearray(2)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = 0xE3
        self.busi2c.send(self.adresse, cmd)

    def getStatusRegister(self):
        cmd = bytearray(2)
        cmd[0] = 0x80 # Co=1 D/C=0
        data = self.busi2c.transfer(cmd, 1)[0]
