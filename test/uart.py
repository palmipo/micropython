from picouart import PicoUart
from modbusrtu import ModbusRtu
from modbusmsg03 import ModbusMsg03
from modbusmsg06 import ModbusMsg06
from modbusexception import ModbusException

uart = PicoUart(9600)
modbus = ModbusRtu(uart)

print("UART Info : ", modbus)

try:
    msg1 = ModbusMsg03(0x01, modbus)
    bitBuffer1 = msg1.readHoldingRegisters(2, 1)
    print(bitBuffer1)

    msg2 = ModbusMsg06(0x01, modbus)
    msg2.presetSingleRegister(1, 0xFFF)
except ModbusException as e:
    print("exception ", e)