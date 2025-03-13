from device.modbus.modbusheader import ModbusHeader

class ModbusMsg(ModbusHeader):
    def __init__(self, modbus_id, msg_id):
        super().__init__(modbus_id)
        self.msg_id = msg_id