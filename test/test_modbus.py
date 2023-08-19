from uartpico import UartPico
from modbusrtu import ModbusRtu
from modbusexception import ModbusException
from modbusmsg03 import ModbusMsg03
from modbusmsg06 import ModbusMsg06
from r4dcb08 import R4DCB08
from n4dog16 import N4DOG16

rs1 = UartPico(1)
rtu1 = ModbusRtu(rs1)
temperature = R4DCB08(1, rtu1)
print(temperature.read(1)[0]/10)
print(temperature.readAll())

rs0 = UartPico(0)
rtu0 = ModbusRtu(rs0)
relay = N4DOG16(4, rtu0)
relay.momentary(4)
