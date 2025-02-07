from master.uart.uartpico import UartPico
from device.modbus.modbusrtu import ModbusRtu
from device.modbus.modbusmsg03 import ModbusMsg03
from device.modbus.modbusmsg06 import ModbusMsg06
from device.modbus.modbusexception import ModbusException

uart = UartPico(9600)
modbus = ModbusRtu(uart)

print("UART Info : ", modbus)

try:
    msg1 = ModbusMsg03(0x01, modbus)
    bitBuffer1 = msg1.readHoldingRegisters(0, 1)
    print(bitBuffer1)
except ModbusException as e:
    print("exception ", e)
