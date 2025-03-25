from device.modbus.modbusexception import ModbusException
import struct

class ModbusHeader:
    def __init__(self, modbus_id):
        self.modbus_id = modbus_id
    
    def decode(self, recvBuffer):
        modbus_id = struct.unpack_from('>B', recvBuffer, 0)[0]

        if modbus_id != self.modbus_id:
            raise ModbusException('adresse modbus de la reponse differente de la question')

    def encode(self, sendBuffer):
        struct.pack_into('>B', sendBuffer, 0, self.modbus_id)
