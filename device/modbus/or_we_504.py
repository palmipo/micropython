import struct
from device.modbus.modbusmsg03 import ModbusMsg03
from device.modbus.modbusmsg06 import ModbusMsg06
from device.modbus.modbusrtu import ModbusRtu

class OR_WE_504:
    def __init__(self, modbus_id, rs485):
        self.modbus_id = modbus_id
        self.bus = rs485

    def voltage(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        v = msg.readHoldingRegisters(0x00, 0x01)
        return v[0]/10

    def intensite(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        a = msg.readHoldingRegisters(0x01, 0x01)
        return a[0]/10

    def frequence(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        f = msg.readHoldingRegisters(0x02, 0x01)
        return f[0]

    def activePower(self):
        msg = ModbusMsg03(self.modbus_id, bus)
        ap = msg.readHoldingRegisters(0x03, 0x01)
        return ap[0]

    def reactivePower(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        rp = msg.readHoldingRegisters(0x04, 0x01)
        return rp[0]

    def apparentPower(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        ap = msg.readHoldingRegisters(0x05, 0x01)
        return ap[0]

    def powerFactor(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        pf = msg.readHoldingRegisters(0x06, 0x01)
        return pf[0]

    def activeEnergie(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        ae = msg.readHoldingRegisters(0x07, 0x02)
        return struct.pack('>H', ae)

    def reactiveEnergie(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        re = msg.readHoldingRegisters(0x09, 0x02)
        return struct.pack('>H', re)

    def setBaudRate(self, baud_rate):
        msg = ModbusMsg06(self.modbus_id, self.bus)
        msg.presetSingleRegister(0x0E, baud_rate)

    def getBaudRate(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        bd = msg.readHoldingRegisters(0x0E, 0x01)
        return bd[0]

    def setModbusId(self, modbus_id):
        msg = ModbusMsg06(self.modbus_id, self.bus)
        msg.presetSingleRegister(0x0F, modbus_id)

    def getModbusId(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        bd = msg.readHoldingRegisters(0x0F, 0x01)
        return bd[0]

    def passwordEfficacy(self, passwd):
        r = bus.transfer(struct.pack('>BBHHB', self.modbus_id, 0x10, 0x0040, len(passwd)>>1, len(passwd)) + passwd, 6)
        if len(r) != 0:
            rr = struct.unpack('>BBHH', r[0:6])
            if (rr[1] & 0x80) != 0x00:
                return 'erreur'

    def removePassword(self, passwd):
        r = bus.transfer(struct.pack('>BBHHB', self.modbus_id, 0x10, 0x116, len(passwd)>>1, len(passwd)) + passwd, 6)
        if len(r) != 0:
            rr = struct.unpack('>BBHH', r[0:6])
            if (rr[1] & 0x80) != 0x00:
                return 'erreur'
            #time.sleep(10)

if __name__ == "__main__":
    import machine, time
    uart = machine.UART(0, baudrate=9600, tx=machine.Pin(1), rx=machine.Pin(2))
    uart.init(9600, bits=8, parity=None, stop=1)
    # uart = serial.Serial('/dev/ttyUSB0', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=5)
    bus = ModbusRtu(uart)
    cpt = OR_WE_504(0x01, bus)

    print(cpt.getModbusId())
    print(cpt.getBaudRate())
    print(cpt.voltage())
    print(cpt.intensite())
    print(cpt.frequence())

    uart.close()

