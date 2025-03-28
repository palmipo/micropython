import struct
from tools.mqtt.mqttmsg import MqttMsg

# SUBSCRIBE - Subscribe to topics
class MqttSubcribe(MqttMsg):
    def __init__(self, packed_id, topic_name, QoS):
        topic_len = len(topic_name)
        
        taille = 7 + topic_len

        offset = 0
        self.buffer = bytearray(taille)
        packed_type = 0x82
        struct.pack_into('!B', self.buffer, offset, packed_type)
        offset += 1
        struct.pack_into('!B', self.buffer, offset, taille-2)
        offset += 1

        # PACKET_ID
        struct.pack_into('!H', self.buffer, offset, packed_id)
        offset += 2
        
        # TOPIC_NAME
        struct.pack_into('!H', self.buffer, offset, topic_len)
        offset += 2
        
        for i in range(topic_len):
            struct.pack_into('s', self.buffer, offset, topic_name[i])
            offset += 1

        struct.pack_into('!B', self.buffer, offset, (QoS & 0x03))
        offset += 1

# SUBACK – Subscribe acknowledgement
class MqttSubAck(MqttMsg):
    def __init__(self, buffer):

        offset = 0
        self.packet_id = struct.unpack_from('!H', buffer, offset)[0]
        offset += 2
        # 0x00 - Success - Maximum QoS 0
        # 0x01 - Success - Maximum QoS 1
        # 0x02 - Success - Maximum QoS 2
        # 0x80 - Failure
        self.erreur = struct.unpack_from('!B', buffer, offset)[0] & 0x80
        self.return_code  = struct.unpack_from('!B', buffer, offset)[0] & 0x03
        offset += 1
