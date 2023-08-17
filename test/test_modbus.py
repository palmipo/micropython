from picouart import PicoUart
from modbusrtu import ModbusRtu
from modbusexception import ModbusException
from modbusmsg03 import ModbusMsg03
from modbusmsg06 import ModbusMsg06

rs485 = PicoUart(0)
rtu = ModbusRtu(rs485)
fc03 = ModbusMsg03(0xff, rtu)
print("adresse module : " + fc03.readHoldingRegisters(0x00FE, 0x0001))
