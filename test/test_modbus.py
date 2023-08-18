from picouart import PicoUart
from modbusrtu import ModbusRtu
from modbusexception import ModbusException
from modbusmsg03 import ModbusMsg03
from modbusmsg06 import ModbusMsg06
from r4dcb08 import R4DCB08

rs485 = PicoUart(1)
rtu = ModbusRtu(rs485)
temperature = R4DCB08(1, rtu)
print(temperature.read(1)[0]/10)
print(temperature.readAll())
# fc03 = ModbusMsg03(0xff, rtu)
# print("adresse module : " + fc03.readHoldingRegisters(0x00FE, 0x0001))
