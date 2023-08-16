from picouart import PicoUart
from modbusrtu import ModbusRtu
from modbusexception import ModbusException
from modbusmsg03 import ModbusMsg03
from modbusmsg06 import ModbusMsg06


rs485 = PicoUart(0)
rtu = ModbusRtu(rs485)
# fc03 = ModbusMsg03(0x4, rtu)
# io = fc03.readHoldingRegisters(0, 2)
# print(io[0])
# print(io[1])
fc06 = ModbusMsg06(0x4, rtu)
io = fc06.presetSingleRegister(0x0001, 0X0602)