from picouart import PicoUart
from modbusrtu import ModbusRtu
from modbusmsg03 import ModbusMsg03


rs485 = PicoUart(9600)
rtu = ModbusRtu(rs485)
msg = ModbusMsg03(0x11, rtu)
io = msg.readHoldingRegisters(0x006B, 3)
print(io)