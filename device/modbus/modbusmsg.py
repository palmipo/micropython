from device.modbus.modbusheader import ModbusHeader
from device.modbus.modbusexception import ModbusException
import struct

class ModbusMsg(ModbusHeader):
    def __init__(self, modbus_id, msg_id):
        super().__init__(modbus_id)
        self.msg_id = msg_id
    
    def decode(self, recvBuffer):
        super().decode(recvBuffer)

        msg_id = struct.unpack_from('>B', recvBuffer, 1)[0]

        if msg_id & 0x80 != 0:
            err = struct.unpack_from('>B', recvBuffer, 2)[0]
            raise ModbusException('erreur de l\'esclave')

        if msg_id & 0x7F != self.msg_id:
            raise ModbusException('numero de fonction de la reponse differente de la question')

    def encode(self, sendBuffer):
        super().encode(sendBuffer)
        struct.pack_into('>B', sendBuffer, 1, self.msg_id)
