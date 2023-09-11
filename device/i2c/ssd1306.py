from devicei2c import DeviceI2C
import time
 

class SSD1306(DeviceI2C):
    def __init__(self, width, height, addr, bus):
        self.height = height
        self.width = width
        super().__init__(0x3C | (addr & 0x01), bus)

    def initDisplay(self):
        self.setDisplayOFF()
        self.setMemoryAddressingMode(0)
        self.setDisplayStartLine(0)
        self.setSegmentRemap(1)
        self.setMultiplexRatio(self.height - 1)
        self.setCOMOutputScanDirection(1)
        self.setDisplayOffset(0x00)
        self.SetCOMPinsHardwareConfiguration(0x01)
        self.setDisplayClockDivideRatioOscillatorFrequency(0x80)
        self.setPrechargePeriod(1)
        self.setVCOMHDeselectLevel(1)
        self.setContrastControl(0x0F)
        self.setEntireDisplayON()
        self.setNormalDisplay()
        self.setChargePumpSetting(1)
        self.setDisplayON()

    def show(self, buffer):
        self.setColumnAddress(0, self.width-1)
        self.setPageAddress(0, 7)
        self.write_data(buffer)

    def read_data(self):
        cmd = bytearray(1)
        cmd[0] = 0x80
        return self.busi2c.transfer(cmd, 1)[0]

    def write_data(self, buffer):
        cmd = bytearray(1+len(buffer))
        cmd[0] = 0x40 # Co=0 D/C=1
        cmd[1:] = buffer
        self.busi2c.send(self.adresse, cmd)

    def write_cmd(self, reg):
        cmd = bytearray(2)
        cmd[0] = 0x80 # Co=1 D/C=0
        cmd[1:] = reg
        self.busi2c.send(self.adresse, cmd)
        time.sleep_ms(10)

    def setContrastControl(self, valeur):
        cmd = bytearray(2)
        cmd[0] = 0x81
        cmd[1] = valeur & 0xFF
        self.write_cmd(cmd)

    def setChargePump(self, valeur):
        cmd = bytearray(2)
        cmd[0] = 0x8D
        cmd[1] = 0x10 | ((valeur & 0x1) << 2)
        self.write_cmd(cmd)

    def setEntireDisplayON(self):
        cmd = bytearray(1)
        cmd[0] = 0xA5
        self.write_cmd(cmd)

    def setEntireDisplayOFF(self):
        cmd = bytearray(1)
        cmd[0] = 0xA4
        self.write_cmd(cmd)

    def setNormalDisplay(self):
        cmd = bytearray(1)
        cmd[0] = 0xA6
        self.write_cmd(cmd)

    def setInverseDisplay(self):
        cmd = bytearray(1)
        cmd[0] = 0xA7
        self.write_cmd(cmd)

    def setDisplayON(self):
        cmd = bytearray(1)
        cmd[0] = 0xAF
        self.write_cmd(cmd)

    def setDisplayOFF(self):
        cmd = bytearray(1)
        cmd[0] = 0xAE
        self.write_cmd(cmd)

    def setLowerColumnStartAddressForPageAddressingMode(self, setColumnStartAddressRegister):
        cmd = bytearray(1)
        cmd[0] = setColumnStartAddressRegister & 0x0F
        self.write_cmd(cmd)
        cmd[0] = 0x10 | (setColumnStartAddressRegister >> 4)
        self.write_cmd(cmd)

    def setMemoryAddressingMode(self, mode):
        cmd = bytearray(2)
        cmd[0] = 0x20
        cmd[1] = mode & 0x03
        self.write_cmd(cmd)

    def setColumnAddress(self, columnStartAddress, columnEndAddress):
        cmd = bytearray(3)
        cmd[0] = 0x21
        cmd[1] = columnStartAddress & 0x7F
        cmd[2] = columnEndAddress & 0x7F
        self.write_cmd(cmd)

    def setPageAddress(self, pageStartAddress, pageEndAddress):
        cmd = bytearray(3)
        cmd[0] = 0x22
        cmd[1] = pageStartAddress & 0x07
        cmd[2] = pageEndAddress & 0x07
        self.write_cmd(cmd)

    def setPageStartAddress(self, pageAddressMode):
        cmd = bytearray(3)
        cmd[0] = 0xB0
        cmd[1] = pageAddressMode & 0x07
        self.write_cmd(cmd)

    def setDisplayStartLine(self, displayStartLine):
        cmd = bytearray(1)
        cmd[0] = 0x40 | (displayStartLine & 0x3F)
        self.write_cmd(cmd)

    def setSegmentRemap(self):
        cmd = bytearray(1)
        cmd[0] = 0xA0
        self.write_cmd(cmd)

    def setSegmentRemapInversed(self):
        cmd = bytearray(1)
        cmd[0] = 0xA1
        self.write_cmd(cmd)

    def setMultiplexRatio(self, valeur):
        cmd = bytearray(2)
        cmd[0] = 0xA8
        cmd[1] = valeur & 0x3F
        self.write_cmd(cmd)

    def setCOMOutputScanDirection(self, remappedMode):
        cmd = bytearray(1)
        cmd[0] = 0xC0 | ((remappedMode & 0x01) << 3)
        self.write_cmd(cmd)

    def setDisplayOffset(self, offset):
        cmd = bytearray(2)
        cmd[0] = 0xD3
        cmd[1] = offset & 0x3F
        self.write_cmd(cmd)

    def SetCOMPinsHardwareConfiguration(self, comPinConfiguration):
        cmd = bytearray(2)
        cmd[0] = 0xDA
        cmd[1] = ((comPinConfiguration & 0x03) << 4) | 0x02
        self.write_cmd(cmd)

    def setDisplayClockDivideRatioOscillatorFrequency(self, divideRatio, oscillatorFrequency):
        cmd = bytearray(2)
        cmd[0] = 0xD5
        cmd[1] = ((oscillatorFrequency & 0x0F) << 4) | (divideRatio & 0x0F)
        self.write_cmd(cmd)

    def setPrechargePeriod(self, phase1, phase2):
        cmd = bytearray(2)
        cmd[0] = 0xD9
        cmd[1] = ((phase2 & 0x0F) << 4) | (phase1 & 0x0F)
        self.write_cmd(cmd)

    def setVCOMHDeselectLevel(self, level):
        cmd = bytearray(2)
        cmd[0] = 0xDB
        cmd[1] = (level & 0x07) << 4
        self.write_cmd(cmd)

    def nop(self):
        cmd = bytearray(1)
        cmd[0] = 0xE3
        self.write_cmd(cmd)

    def getStatusRegister(self):
        return self.read_data()

    def rightHorizontalScrollSetup(self, startPageAddress, setTimeInterval, endPageAddress):
        cmd = bytearray(7)
        cmd[0] = 0x26
        cmd[1] = 0x00
        cmd[2] = startPageAddress & 0x07
        cmd[3] = setTimeInterval & 0x07
        cmd[4] = endPageAddress & 0x07
        cmd[5] = 0x00
        cmd[6] = 0xFF
        self.write_cmd(cmd)

    def leftHorizontalScrollSetup(self, startPageAddress, setTimeInterval, endPageAddress):
        cmd = bytearray(7)
        cmd[0] = 0x27
        cmd[1] = 0x00
        cmd[2] = startPageAddress & 0x07
        cmd[3] = setTimeInterval & 0x07
        cmd[4] = endPageAddress & 0x07
        cmd[5] = 0x00
        cmd[6] = 0xFF
        self.write_cmd(cmd)

    def verticalRightHorizontalScrollSetup(self, startPageAddress, setTimeInterval, endPageAddress):
        cmd = bytearray(6)
        cmd[0] = 0x29
        cmd[1] = 0x2A
        cmd[2] = startPageAddress & 0x07
        cmd[3] = setTimeInterval & 0x07
        cmd[4] = endPageAddress & 0x07
        cmd[5] = verticalScrollingOffset & 0x3F
        self.write_cmd(cmd)

    def verticalLeftHorizontalScrollSetup(self, startPageAddress, setTimeInterval, endPageAddress):
        cmd = bytearray(6)
        cmd[0] = 0x28 | (verticalAndRightHorizontalScroll & 0x01)
        cmd[1] = 0x28 | ((verticalAndLeftHorizontalScroll & 0x01) << 1)
        cmd[2] = startPageAddress & 0x07
        cmd[3] = setTimeInterval & 0x07
        cmd[4] = endPageAddress & 0x07
        cmd[5] = verticalScrollingOffset & 0x3F
        self.write_cmd(cmd)

    def deactivateScroll(self):
        cmd = bytearray(1)
        cmd[0] = 0x2E
        self.write_cmd(cmd)

    def activateScroll(self):
        cmd = bytearray(1)
        cmd[0] = 0x2F
        self.write_cmd(cmd)

    def setVerticalScrollArea(self, setRowsInTopFixedArea, setRowsInScrollArea):
        cmd = bytearray(3)
        cmd[0] = 0xA3
        cmd[1] = setRowsInTopFixedArea & 0x3F
        cmd[2] = setRowsInScrollArea & 0x7F
        self.write_cmd(cmd)
