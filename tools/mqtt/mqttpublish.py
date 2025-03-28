import struct
from tools.mqtt.mqttmsg import MqttMsg

class MqttPublish(MqttMsg):
    def __init__(self, topic_name, text, dup_flag=0, QoS=0, retain=0, packed_id=None):
        topic_len = len(topic_name)
        text_len = len(text)
        packed_id_len = 0
        taille = 4 + topic_len + text_len
        if QoS != 0:
            packed_id_len = len(packed_id)
            taille += 2 + packed_id_len
        
        # FIXED_HEADER
        offset = 0
        self.buffer = bytearray(taille)
        packed_type = 0x30
        packed_type = packed_type | ((dup_flag & 0x01) << 3)
        packed_type = packed_type | ((QoS & 0x03) << 1)
        packed_type = packed_type | ((retain & 0x01) << 0)
        struct.pack_into('!B', self.buffer, offset, packed_type)
        offset += 1
        struct.pack_into('!B', self.buffer, offset, taille-2)
        offset += 1

        # VARIABLE_HEADER.TOPIC_NAME
        struct.pack_into('!H', self.buffer, offset, topic_len)
        offset += 2
        
        for i in range(topic_len):
            struct.pack_into('s', self.buffer, offset, topic_name[i])
            offset += 1

        # VARIABLE_HEADER.PACKED_IDENTIFIER
        if QoS != 0:
            struct.pack_into('!H', self.buffer, offset, packed_id_len)
            offset += 2
            
            for i in range(packed_id_len):
                struct.pack_into('s', self.buffer, offset, packed_id[i])
                offset += 1
        
        # TEXT
        for i in range(text_len):
            struct.pack_into('s', self.buffer, offset, text[i])
            offset += 1

# PUBACK – Publish acknowledgement
class MqttPubRecv(MqttMsg):
    def __init__(self, buffer, dup_flag, QoS_level, retain):
        offset = 0
        topic_len = struct.unpack_from('!H', buffer, offset)[0]
        offset += 2
        
        self.topic_name = buffer[offset:offset+topic_len]
        offset += topic_len


        # VARIABLE_HEADER.PACKED_IDENTIFIER
        if QoS_level != 0:
            packed_id_len = struct.unpack_from('!H', buffer, offset)[0]
            offset += 2
            
            packed_id = buffer[offset:offset+packed_id_len]
            offset += packed_id_len

        # TEXT
        taille_text = len(buffer) - offset
        self.text = buffer[offset:offset+taille_text]
        offset += taille_text

# PUBACK – Publish acknowledgement
class MqttPubAck(MqttMsg):
    def __init__(self, buffer):

        offset = 0
        self.packet_id = struct.unpack_from('!H', buffer, offset)[0]
        offset += 2

# PUBREC – Publish received (QoS 2 publish received, part 1)
class MqttPubRec(MqttMsg):
    def __init__(self, buffer):

        offset = 0
        self.packet_id = struct.unpack_from('!H', buffer, offset)[0]
        offset += 2
        
# PUBREL – Publish release (QoS 2 publish received, part 2)
class MqttPubRel(MqttMsg):
    def __init__(self, buffer):

        offset = 0
        self.packet_id = struct.unpack_from('!H', buffer, offset)[0]
        offset += 2
       
# PUBCOMP – Publish complete (QoS 2 publish received, part 3)
class MqttPubComp(MqttMsg):
    def __init__(self, buffer):

        offset = 0
        self.packet_id = struct.unpack_from('!H', buffer, offset)[0]
        offset += 2
