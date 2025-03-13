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

    def reactiveEnergie(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        re = msg.readHoldingRegisters(0x09, 0x02)
        return re[1]

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
        r = bus.transfer(struct.pack('>BBHHB', self.modbus_id, 0x10, 0x0116, len(passwd)>>1, len(passwd)) + passwd, 6)
        if len(r) != 0:
            rr = struct.unpack('>BBHH', r[0:6])
            if (rr[1] & 0x80) != 0x00:
                return 'erreur'
            #time.sleep(10)

if __name__ == "__main__":
    from master.uart.uartpico import UartPico
    from device.modbus.modbusrtu import ModbusRtu
    import time
    uart1 = UartPico(bus=0, bdrate=9600, pinTx=0, pinRx=1)
    uart2 = UartPico(bus=1 , bdrate=9600, pinTx=4, pinRx=5)
    bus1 = ModbusRtu(uart1)
    bus2 = ModbusRtu(uart2)
    cpt1 = OR_WE_504(0x01, bus1)
    cpt2 = OR_WE_504(0x01, bus2)

    while True:
    # print(cpt.getModbusId())
    # print(cpt.getBaudRate())
        print('tension', cpt1.voltage(), cpt2.voltage())
        print('intensite', cpt1.intensite(), cpt2.intensite())
        print('frequence', cpt1.frequence(), cpt2.frequence())
        print('puissance active', cpt1.activePower(), cpt2.activePower())
        print('puissance reactive', cpt1.reactivePower(), cpt2.reactivePower())
        print('puissance apparente', cpt1.apparentPower(), cpt2.apparentPower())
        print('dephasage', cpt1.powerFactor(), cpt2.powerFactor())
        print(cpt1.activeEnergie(), cpt2.activeEnergie())
        print(cpt1.reactiveEnergie(), cpt2.reactiveEnergie())
        time.sleep(20)

#     uart.close()

