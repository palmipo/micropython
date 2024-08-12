from device.i2c.devicei2c import DeviceI2C
import time
 

class SSD1306(DeviceI2C):
    def __init__(self, width, height, addr, bus):
        super().__init__(0x3C | (addr & 0x01), bus)

        self.height = height
        self.width = width
        self.temp = bytearray(2)

    def setDisplayON(self):
        self.__write_cmd__(0xAF)

    def setDisplayOFF(self):
        self.__write_cmd__(0xAE)

    def setEntireDisplayON(self):
        self.__write_cmd__(0xA5)

    def setEntireDisplayOFF(self):
        self.__write_cmd__(0xA4)

    def setContrastControl(self, valeur):
        self.__write_cmd__(0x81)
        self.__write_cmd__(valeur & 0xFF)

    def setChargePumpSetting(self, enable):
        self.__write_cmd__(0x8D)
        self.__write_cmd__(0x10 | ((enable & 0x01) << 2))

    def setNormalDisplay(self):
        self.__write_cmd__(0xA6)

    def setInverseDisplay(self):
        self.__write_cmd__(0xA7)

    def setVerticalScrollArea(self, setRowsInTopFixedArea, setRowsInScrollArea):
        self.__write_cmd__(0xA3)
        self.__write_cmd__(setRowsInTopFixedArea & 0x3F)
        self.__write_cmd__(setRowsInScrollArea & 0x7F)

    def setLowerColumnStartAddressForPageAddressingMode(self, setColumnStartAddressRegister):
        self.__write_cmd__(setColumnStartAddressRegister & 0x0F)
        self.__write_cmd__(0x10 | (setColumnStartAddressRegister >> 4))

    def setMemoryAddressingMode(self, mode):
        self.__write_cmd__(0x20)
        self.__write_cmd__(mode & 0x03)

    def setColumnAddress(self, columnStartAddress, columnEndAddress):
        self.__write_cmd__(0x21)
        self.__write_cmd__(columnStartAddress & 0x7F)
        self.__write_cmd__(columnEndAddress & 0x7F)

    def setPageAddress(self, pageStartAddress, pageEndAddress):
        self.__write_cmd__(0x22)
        self.__write_cmd__(pageStartAddress & 0x07)
        self.__write_cmd__(pageEndAddress & 0x07)

    def setDisplayStartLine(self, displayStartLine):
        self.__write_cmd__(0x40 | (displayStartLine & 0x3F))

    def setSegmentRemap(self, columnAddress0MappedtoSEG0):
        self.__write_cmd__(0xA0 | (columnAddress0MappedtoSEG0 & 0x01))

    def setMultiplexRatio(self, valeur):
        self.__write_cmd__(0xA8)
        self.__write_cmd__(valeur & 0x3F)

    def setCOMOutputScanDirection(self, remappedMode):
        self.__write_cmd__(0xC0 | ((remappedMode & 0x01) << 3))

    def setDisplayOffset(self, offset):
        self.__write_cmd__(0xD3)
        self.__write_cmd__(offset & 0x3F)

    def SetCOMPinsHardwareConfiguration(self, comPinConfiguration):
        self.__write_cmd__(0xDA)
        self.__write_cmd__(((comPinConfiguration & 0x03) << 4) | 0x02)

    def setDisplayClockDivideRatioOscillatorFrequency(self, ratio):
        self.__write_cmd__(0xD5)
        self.__write_cmd__(ratio & 0xFF)

    def setPrechargePeriod(self, phase):
        self.__write_cmd__(0xD9)
        self.__write_cmd__(phase & 0xFF)

    def setVCOMHDeselectLevel(self, level):
        self.__write_cmd__(0xDB)
        self.__write_cmd__((level & 0x07) << 4)

    def nop(self):
        self.__write_cmd__(0xE3)

    def continuousHorizontalScrollSetup(self, leftHorizontalScroll, startPageAddress, setTimeInterval, endPageAddress):
        self.__write_cmd__(0x26 | (leftHorizontalScroll & 0x01))
        self.__write_cmd__(0x00)
        self.__write_cmd__(startPageAddress & 0x07)
        self.__write_cmd__(setTimeInterval & 0x07)
        self.__write_cmd__(endPageAddress & 0x07)
        self.__write_cmd__(0x00)
        self.__write_cmd__(0xFF)

    def continuousVerticalHorizontalScrollSetup(self, leftHorizontalScroll, startPageAddress, setTimeInterval, endPageAddress):
        self.__write_cmd__(0x28 | ((verticalAndLeftHorizontalScroll & 0x01) << 1))
        self.__write_cmd__(startPageAddress & 0x07)
        self.__write_cmd__(setTimeInterval & 0x07)
        self.__write_cmd__(endPageAddress & 0x07)
        self.__write_cmd__(verticalScrollingOffset & 0x3F)

    def rightHorizontalScrollSetup(self, startPageAddress, setTimeInterval, endPageAddress):
        self.__write_cmd__( 0x26)
        self.__write_cmd__( 0x00)
        self.__write_cmd__( startPageAddress & 0x07)
        self.__write_cmd__( setTimeInterval & 0x07)
        self.__write_cmd__( endPageAddress & 0x07)
        self.__write_cmd__( 0x00)
        self.__write_cmd__( 0xFF)

    def leftHorizontalScrollSetup(self, startPageAddress, setTimeInterval, endPageAddress):
        self.__write_cmd__( 0x27)
        self.__write_cmd__( 0x00)
        self.__write_cmd__( startPageAddress & 0x07)
        self.__write_cmd__( setTimeInterval & 0x07)
        self.__write_cmd__( endPageAddress & 0x07)
        self.__write_cmd__( 0x00)
        self.__write_cmd__( 0xFF)

    def verticalRightHorizontalScrollSetup(self, startPageAddress, setTimeInterval, endPageAddress):
        self.__write_cmd__( 0x29)
        self.__write_cmd__( 0x2A)
        self.__write_cmd__( startPageAddress & 0x07)
        self.__write_cmd__( setTimeInterval & 0x07)
        self.__write_cmd__( endPageAddress & 0x07)
        self.__write_cmd__( verticalScrollingOffset & 0x3F)

    def verticalLeftHorizontalScrollSetup(self, startPageAddress, setTimeInterval, endPageAddress):
        self.__write_cmd__( 0x28 | (verticalAndRightHorizontalScroll & 0x01))
        self.__write_cmd__( 0x28 | ((verticalAndLeftHorizontalScroll & 0x01) << 1))
        self.__write_cmd__( startPageAddress & 0x07)
        self.__write_cmd__( setTimeInterval & 0x07)
        self.__write_cmd__( endPageAddress & 0x07)
        self.__write_cmd__( verticalScrollingOffset & 0x3F)

    def deactivateScroll(self):
        self.__write_cmd__(0x2E)

    def activateScroll(self):
        self.__write_cmd__(0x2F)

    def __write_cmd__(self, cmd):
        self.temp[0] = 0x00
        self.temp[1] = cmd
        self.busi2c.send(self.adresse, self.temp)

    def __write_data__(self, buf):
        self.temp[0] = 0x40
        self.temp[1] = buf
        self.busi2c.send(self.adresse, self.temp)
