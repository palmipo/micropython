from devicei2c import DeviceI2C

class MCP23017(DeviceI2C):

    def __init__(self, address, bus):
        super().__init__(0x20 | (address & 0x03), bus)

        # The registers are in the same bank (addresses are sequential)
        cmd = bytearray(2)
        cmd[0] = 0x0A
        cmd[1] = 0x00
        self.busi2c.send(self.adresse, cmd)

# Controls the direction of the data I/O.
# When a bit is set, the corresponding pin becomes an
# input. When a bit is clear, the corresponding pin
# becomes an output.
    def getIODIR(self, port):
        cmd = bytearray(1)
        cmd[0] = 0x00 + (port & 0x01)
        return self.busi2c.transferer(self.adresse, cmd, 1)

    def setIODIR(self, port, io):
        cmd = bytearray(2)
        cmd[0] = 0x00 + (port & 0x01)
        cmd[1] = io & 0xff
        self.busi2c.send(self.adresse, cmd)

# This register allows the user to configure the polarity on
# the corresponding GPIO port bits.
# If a bit is set, the corresponding GPIO register bit will
# reflect the inverted value on the pin.
    def getIPOL(self, port):
        cmd = bytearray(1)
        cmd[0] = 0x02 + (port & 0x01)
        return self.busi2c.transferer(self.adresse, cmd, 1)

    def setIPOL(self, port, ip):
        cmd = bytearray(2)
        cmd[0] = 0x02 + (port & 0x01)
        cmd[1] = ip & 0xff
        self.busi2c.send(self.adresse, cmd)

# The GPINTEN register controls the
# interrupt-on-change feature for each pin.
# If a bit is set, the corresponding pin is enabled for
# interrupt-on-change. The DEFVAL and INTCON
# registers must also be configured if any pins are
# enabled for interrupt-on-change.
    def getGPINTEN(self, port):
        cmd = bytearray(1)
        cmd[0] = 0x04 + (port & 0x01)
        return self.busi2c.transferer(self.adresse, cmd, 1)

    def setGPINTEN(self, port, gpint):
        cmd = bytearray(2)
        cmd[0] = 0x04 + (port & 0x01)
        cmd[1] = gpint & 0xff
        self.busi2c.send(self.adresse, cmd)

# The default comparison value is configured in the
# DEFVAL register. If enabled (via GPINTEN and
# INTCON) to compare against the DEFVAL register, an
# opposite value on the associated pin will cause an
# interrupt to occur.
    def getDEFVAL(self, port):
        cmd = bytearray(1)
        cmd[0] = 0x06 + (port & 0x01)
        return self.busi2c.transferer(self.adresse, cmd, 1)

    def setDEFVAL(self, port, val):
        cmd = bytearray(2)
        cmd[0] = 0x06 + (port & 0x01)
        cmd[1] = val & 0xff
        self.busi2c.send(self.adresse, cmd)

# The INTCON register controls how the associated pin
# value is compared for the interrupt-on-change feature.
# If a bit is set, the corresponding I/O pin is compared
# against the associated bit in the DEFVAL register. If a
# bit value is clear, the corresponding I/O pin is compared
# against the previous value.
    def getINTCON(self, port):
        cmd = bytearray(1)
        cmd[0] = 0x08 + (port & 0x01)
        return self.busi2c.transferer(self.adresse, cmd, 1)

    def setINTCON(self, port, val):
        cmd = bytearray(2)
        cmd[0] = 0x08 + (port & 0x01)
        cmd[1] = val & 0xff
        self.busi2c.send(self.adresse, cmd)

    def getIOCON(self, port):
        cmd = bytearray(1)
        cmd[0] = 0x0A + (port & 0x01)
        return self.busi2c.transferer(self.adresse, cmd, 1)

    def setIOCON(self, port, mirror, seqop, disslw, haen, odr, intpol):
        cmd = bytearray(2)
        cmd[0] = 0x0A + (port & 0x01)
        cmd[1] = ((mirror & 1) << 6) | ((seqop & 1) << 5) | ((disslw & 1) << 4) | ((haen & 1) << 3) | ((odr & 1) << 2) | ((intpol & 1) << 1)
        self.busi2c.send(self.adresse, cmd)

# The GPPU register controls the pull-up resistors for the
# port pins. If a bit is set and the corresponding pin is
# configured as an input, the corresponding port pin is
# internally pulled up with a 100 kOhm resistor.
    def getGPPU(self, port):
        cmd = bytearray(1)
        cmd[0] = 0x0C + (port & 0x01)
        return self.busi2c.transferer(self.adresse, cmd, 1)

    def setGPPU(self, port, pullup):
        cmd = bytearray(2)
        cmd[0] = 0x0C + (port & 0x01)
        cmd[1] = pullup & 0xff
        self.busi2c.send(self.adresse, cmd)

# The INTF register reflects the interrupt condition on the
# port pins of any pin that is enabled for interrupts via the
# GPINTEN register. A set bit indicates that the
# associated pin caused the interrupt.
# This register is read-only. Writes to this register will be
# ignored.
    def getINTF(self, port):
        cmd = bytearray(1)
        cmd[0] = 0x0E + (port & 0x01)
        return self.busi2c.transferer(self.adresse, cmd, 1)

# The INTCAP register captures the GPIO port value at
# the time the interrupt occurred. The register is
# read-only and is updated only when an interrupt
# occurs. The register remains unchanged until the
# interrupt is cleared via a read of INTCAP or GPIO.
    def getINTCAP(self, port):
        cmd = bytearray(1)
        cmd[0] = 0x10 + (port & 0x01)
        return self.busi2c.transferer(self.adresse, cmd, 1)

# The GPIO register reflects the value on the port.
# Reading from this register reads the port. Writing to this
# register modifies the Output Latch (OLAT) register.
    def getGPIO(self, port):
        cmd = bytearray(1)
        cmd[0] = 0x12 + (port & 0x01)
        return self.busi2c.transferer(self.adresse, cmd, 1)

    def setGPIO(self, port, gp):
        cmd = bytearray(2)
        cmd[0] = 0x12 + (port & 0x01)
        cmd[1] = gp & 0xff
        self.busi2c.send(self.adresse, cmd)

# The OLAT register provides access to the output
# latches. A read from this register results in a read of the
# OLAT and not the port itself. A write to this register
# modifies the output latches that modifies the pins
# configured as outputs.
    def getOLAT(self, port):
        cmd = bytearray(1)
        cmd[0] = 0x14 + (port & 0x01)
        return self.busi2c.transferer(self.adresse, cmd, 1)

    def setOLAT(self, port, ol):
        cmd = bytearray(2)
        cmd[0] = 0x14 + (port & 0x01)
        cmd[1] = ol & 0xff
        self.busi2c.send(self.adresse, cmd)
