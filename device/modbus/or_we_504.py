import struct
from device.modbus.modbusmsg03 import ModbusMsg03
from device.modbus.modbusmsg06 import ModbusMsg06
from device.modbus.modbusmsg16 import ModbusMsg16
from device.modbus.modbusmsgfree import ModbusMsgFree
from device.modbus.modbusexception import ModbusException

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
        return f[0]/10

    def activePower(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
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
        return pf[0]/1000

    def activeEnergie(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        ae = msg.readHoldingRegisters(0x07, 0x02)
        return ae[1]

    def clearActiveEnergy(self, passwd):
        self.login(passwd)

        msg16 = ModbusMsg16(self.modbus_id, self.bus)
        msg16.presetMultipleRegisters(0x07, [0, 0])

    def reactiveEnergie(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        re = msg.readHoldingRegisters(0x09, 0x02)
        return re[1]

    def clearReactiveEnergie(self, passwd):
        self.login(passwd)

        msg16 = ModbusMsg16(self.modbus_id, self.bus)
        msg16.presetMultipleRegisters(0x09, [0, 0])

    def setBaudRate(self, baud_rate):
        msg = ModbusMsg06(self.modbus_id, self.bus)
        msg.presetSingleRegister(0x0E, baud_rate)

    def getBaudRate(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        bd = msg.readHoldingRegisters(0x0E, 0x01)
        return bd[0]

    def setModbusId(self, modbus_id):
        msg = ModbusMsg16(self.modbus_id, self.bus)
        msg.presetMultipleRegisters(0x0F, modbus_id)

    def getModbusId(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        bd = msg.readHoldingRegisters(0x0F, 0x01)
        return bd[0]

    # setting：01 28 FE 01 00 02 04 00 00 00 00 FB 12 //00 00 00 00 password
    # return：01 28 FE 01 00 01 C0 24
    def login(self, passwd=b'\x00\x00\x00\x00'):
        msg = ModbusMsgFree(self.modbus_id, 0x28, self.bus)
        recvBuffer = msg.transfer(b'\xFE\x01\x00\x02\x04' + passwd, 4)
        addr, value = struct.unpack_from('>HH', recvBuffer, 0)

        if addr != 0xFE01:
            raise ModbusException()

        if value != 0x0001:
            raise ModbusException()

    # Write password：02 10 00 10 00 02 04 11 11 11 11 64 82 //setting password 11 11 11 11
    # return：02 10 00 10 00 02 40 3E
    def setPassword(self, passwd):
        msg16 = ModbusMsg16(self.modbus_id, self.bus)
        msg16.presetMultipleRegisters(0x10, passwd)

    # setting : 01 28 FE 01 00 02 04 00 00 00 00 -> 00 00 00 00 password
    # return  : 01 28 FE 01 00 01
    def removePassword(self, passwd):
        msg = ModbusMsgFree(self.modbus_id, 0x28, self.bus)
        recvBuffer = msg.transfer(b'\xFE\x01\x00\x02\x04' + passwd, 4)
        addr, value = struct.unpack_from('>HH', recvBuffer, 2)

        if addr != 0xFE01:
            raise ModbusException()

        if value != 0x0001:
            raise ModbusException()

if __name__ == "__main__":
    from master.uart.uartpico import UartPico
    from device.modbus.modbusrtu import ModbusRtu
    from device.modbus.modbusexception import ModbusException
    import time
    try:
        #uart = UartPico(bus=1 , bdrate=9600, pinTx=4, pinRx=5)
        uart = UartPico(bus=0, bdrate=9600, pinTx=0, pinRx=1)
        orno = OR_WE_504(1, ModbusRtu(uart))
        orno.login(b'\x00\x00\x00\x00')
        time.sleep(5)
        orno.setModbusId(2)
#         orno.clearActiveEnergy(b'\x00\x00\x00\x00')
#         orno.clearReactiveEnergie(b'\x00\x00\x00\x00')
    except KeyboardInterrupt:
        print("exit")
        sys.quit()
