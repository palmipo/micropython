from devicei2c import DeviceI2C
import time
 

class SSD1306(DeviceI2C):
    def __init__(self, width, height, addr, bus):
        self.height = height
        self.width = width
        super().__init__(0x3C | (addr & 0x01), bus)

    def initDisplay(self):
        self.setDisplayOFF()
        self.setMultiplexRatio(self.height - 1)
        self.setDisplayOffset(0x00)
        self.setDisplayStartLine(0x00)
        self.setSegmentRemap(0x00)
        self.setCOMOutputScanDirection(0x01)
        self.SetCOMPinsHardwareConfiguration(0x00)
        self.setContrastControl(0x0F)
        self.setEntireDisplayON(0x00)
        self.setNormalDisplay(0x00)
        self.setDisplayClockDivideRatioOscillatorFrequency(0x80)
        self.setChargePumpSetting(0x01)
        self.setDisplayON()

    def show(self, buffer):
        self.setColumnAddress(0, self.width-1)
        self.setPageAddress(0, 7)
        self.write_data(buffer)

    def read_data(self):
        return self.busi2c.recv(1)[0]

    def write_data(self, buffer):
        cmd = bytearray(1+self.width)
        cmd[0] = 0x40 # Co=0 D/C=1
        cmd[1:] = buffer[:self.width]
        self.busi2c.send(self.adresse, cmd)

    def write_cmd(self, reg):
        cmd = bytearray(2)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1] = reg
        self.busi2c.send(self.adresse, cmd)

    def write_cmd_data(self, val):
        cmd = bytearray(2)
        cmd[0] = 0xC0 # Co=1 D/C=0
        cmd[1] = val & 0xFF
        self.busi2c.send(self.adresse, cmd)

    def setContrastControl(self, valeur):
        self.write_cmd(0x81)
        self.write_cmd_data(valeur & 0xFF)

    def setChargePumpSetting(self, enable):
        self.write_cmd(0x8D)
        self.write_cmd_data(0x10 | ((enable & 0x01) << 2))

    def setEntireDisplayON(self, valeur):
        self.write_cmd(0xA4 )
        self.write_cmd_data((valeur & 0x01))

    def setNormalDisplay(self, valeur):
        self.write_cmd(0xA6)
        self.write_cmd_data((valeur & 0x01))

    def setDisplayON(self):
        self.write_cmd(0xAF)

    def setDisplayOFF(self):
        self.write_cmd(0xAE)

    def continuousHorizontalScrollSetup(self, leftHorizontalScroll, startPageAddress, setTimeInterval, endPageAddress):
        self.write_cmd(0x26 | (leftHorizontalScroll & 0x01))
        self.write_cmd_data(0x00)
        self.write_cmd_data(startPageAddress & 0x07)
        self.write_cmd_data(setTimeInterval & 0x07)
        self.write_cmd_data(endPageAddress & 0x07)
        self.write_cmd_data(0x00)
        self.write_cmd_data(0xFF)

    def continuousVerticalHorizontalScrollSetup(self, leftHorizontalScroll, startPageAddress, setTimeInterval, endPageAddress):
        self.write_cmd(0x28 | (verticalAndRightHorizontalScroll & 0x01))
        self.write_cmd_data(0x28 | ((verticalAndLeftHorizontalScroll & 0x01) << 1))
        self.write_cmd_data(startPageAddress & 0x07)
        self.write_cmd_data(setTimeInterval & 0x07)
        self.write_cmd_data(endPageAddress & 0x07)
        self.write_cmd_data(verticalScrollingOffset & 0x3F)

    def deactivateScroll(self):
        self.write_cmd(0x2E)

    def activateScroll(self):
        self.write_cmd(0x2F)

    def setVerticalScrollArea(self, setRowsInTopFixedArea, setRowsInScrollArea):
        self.write_cmd(0xA3)
        self.write_cmd_data(setRowsInTopFixedArea & 0x3F)
        self.write_cmd_data(setRowsInScrollArea & 0x7F)

    def setLowerColumnStartAddressForPageAddressingMode(self, setColumnStartAddressRegister):
        self.write_cmd(setColumnStartAddressRegister & 0x0F)
        self.write_cmd(0x10 | (setColumnStartAddressRegister >> 4))

    def setMemoryAddressingMode(self, mode):
        self.write_cmd(0x20)
        self.write_cmd_data(mode & 0x03)

    def setColumnAddress(self, columnStartAddress, columnEndAddress):
        self.write_cmd(0x21)
        self.write_cmd_data(columnStartAddress & 0x7F)
        self.write_cmd_data(columnEndAddress & 0x7F)

    def setPageAddress(self, pageStartAddress, pageEndAddress):
        self.write_cmd(0x22)
        self.write_cmd_data(pageStartAddress & 0x07)
        self.write_cmd_data(pageEndAddress & 0x07)

    def setDisplayStartLine(self, displayStartLine):
        self.write_cmd(0x40 | (displayStartLine & 0x3F))

    def setSegmentRemap(self, columnAddress0MappedtoSEG0):
        self.write_cmd(0xA0 | (columnAddress0MappedtoSEG0 & 0x01))

    def setMultiplexRatio(self, valeur):
        self.write_cmd(0xA8)
        self.write_cmd_data(valeur & 0x3F)

    def setCOMOutputScanDirection(self, remappedMode):
        self.write_cmd(0xC0 | ((remappedMode & 0x01) << 3))

    def setDisplayOffset(self, offset):
        self.write_cmd(0xD3)
        self.write_cmd_data(offset & 0x3F)

    def SetCOMPinsHardwareConfiguration(self, comPinConfiguration):
        self.write_cmd(0xDA)
        self.write_cmd_data(((comPinConfiguration & 0x03) << 4) | 0x02)

    def setDisplayClockDivideRatioOscillatorFrequency(self, ratio):
        self.write_cmd(0xD5)
        self.write_cmd_data(ratio & 0xFF)

    def setPrechargePeriod(self, phase):
        self.write_cmd(0xD9)
        self.write_cmd_data(phase & 0xFF)

    def setVCOMHDeselectLevel(self, level):
        self.write_cmd(0xDB)
        self.write_cmd_data((level & 0x07) << 4)

    def nop(self):
        self.write_cmd(0xE3)

    def getStatusRegister(self):
        return self.read_data()
