import struct
from tools.mqtt.mqttmsg import MqttMsg

# UNSUBSCRIBE - Unsubscribe to topics
class MqttUnsubcribe(MqttMsg):
    def __init__(self, packed_id):
        taille = 4

        offset = 0
        self.buffer = bytearray(taille)
        packed_type = 0xA2
        struct.pack_into('!B', self.buffer, offset, packed_type)
        offset += 1
        struct.pack_into('!B', self.buffer, offset, taille-2)
        offset += 1

        # PACKET_ID
        struct.pack_into('!H', self.buffer, offset, packed_id)
        offset += 2

# UNSUBACK – Unsubscribe acknowledgement
class MqttUnsubAck(MqttMsg):
    def __init__(self, buffer):

        offset = 0
        self.packet_id = struct.unpack_from('!H', buffer, offset)[0]
        offset += 2
