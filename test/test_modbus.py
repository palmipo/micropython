from picouart import PicoUart
from n4dog16 import N4DOG16

rs485 = PicoUart(0)
rtu = ModbusRtu(rs485)
out = N4DOG16(0x04, rtu)
out.close(1)
