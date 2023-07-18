from modbusmsg03 import ModbusMsg03


rs485 = Rs485()
msg = ModbusMsg03(1, rs485)
io = msg.readHoldingRegisters(10, 8)
