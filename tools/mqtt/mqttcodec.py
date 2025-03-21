import struct, select

class MqttMsg:
    pass

class MqttConnect(MqttMsg):
    def __init__(self, client_id, will_topic=None, will_message=None, user=None, passwd=None, retain=0, QoS=0, clean=0, keep_alive=0):
        client_id_len = len(client_id)
        
        taille = 14 + client_id_len
        
        will_topic_len = 0
        if will_topic != None:
            will_topic_len = len(will_topic)
            taille += 2 + will_topic_len
            
        will_message_len = 0
        if will_message != None:
            will_message_len = len(will_message)
            taille += 2 + will_message_len
            
        user_len = 0
        passwd_len = 0
        if user != None:
            user_len = len(user)
            taille += 2 + user_len
            if passwd != None:
                passwd_len = len(passwd)
                taille += 2+ passwd_len

        print('taille CONNECT : {}, client_id : {}, user : {} passwd : {}'.format(taille, client_id_len, user_len, passwd_len))
        
        # FIXED_HEADER
        offset = 0
        self.buffer = bytearray(taille)
        struct.pack_into('!B', self.buffer, offset, 0x10)
        offset += 1
        struct.pack_into('!B', self.buffer, offset, taille - 2)
        offset += 1
        
        # VARIABLE_HEADER
        # LENGTH
        struct.pack_into('!H', self.buffer, offset, 4)
        offset += 2
        # MAGIC_NUMBER
        self.buffer[offset:offset+4] = b'MQTT'
        offset += 4
        
        # PROTOCOL_LEVEL
        struct.pack_into('!B', self.buffer, offset, 4)
        offset += 1

        # FLAG
        flag = 0
        # User Name Flag
        if user != None:
            flag = flag | 0x01 << 7

        # Password Flag
            if passwd != None:
                flag = flag | 0x01 << 6

        # Will Retain 
        if retain != 0:
            flag = flag | (1 << 5)

        # Will QoS 
        if QoS != 0:
            flag = flag | ((QoS & 0x03) << 3)

        # Will Flag
        if will_topic != None:
            flag = flag | (1 << 2)

        # Clean Session
        if clean != 0:
            flag = flag | (1 << 1)
        struct.pack_into('!B', self.buffer, offset, flag)
        offset += 1

        # KEEP_ALIVE
        struct.pack_into('!H', self.buffer, offset, keep_alive)
        offset += 2

        # PAYLOAD
        # CLIENT_ID.LENGTH
        struct.pack_into('!H', self.buffer, offset, client_id_len)
        offset += 2
        
        # CLIENT_ID
        for i in range(client_id_len):
            struct.pack_into('!B', self.buffer, offset, client_id[i])
            offset += 1

        if will_topic != None:
            struct.pack_into('!H', self.buffer, offset, will_topic_len)
            offset += 2
            
            for i in range(will_topic_len):
                struct.pack_into('s', self.buffer, offset, will_topic[i])
                offset += 1

        if will_message != None:
            struct.pack_into('!H', self.buffer, offset, will_message_len)
            offset += 2
            
            for i in range(will_message_len):
                struct.pack_into('s', self.buffer, offset, will_message[i])
                offset += 1

        if user != None:
            struct.pack_into('!H', self.buffer, offset, user_len)
            offset += 2
            
            for i in range(user_len):
                struct.pack_into('s', self.buffer, offset, user[i])
                offset += 1

            if passwd != None:
                struct.pack_into('!H', self.buffer, offset, passwd_len)
                offset += 2
                
                for i in range(passwd_len):
                    struct.pack_into('s', self.buffer, offset, passwd[i])
                    offset += 1

        print(self.buffer)

# CONNACK – Acknowledge connection request
class MqttConnAck(MqttMsg):
    def __init__(self, buffer):

        offset = 0
        print('MqttConnAck connectAcknowledgeFlags : {}'.format(struct.unpack_from('!B', buffer, offset)[0]))
        offset += 1

        # 0x00 Connection Accepted Connection accepted
        # 0x01 Connection Refused, unacceptable protocol version The Server does not support the level of the MQTT protocol requested by the Client
        # 0x02 Connection Refused, identifier rejected The Client identifier is correct UTF-8 but not allowed by the Server
        # 0x03 Connection Refused, Server unavailable The Network Connection has been made but the MQTT service is unavailable
        # 0x04 Connection Refused, bad user name or password The data in the user name or password is malformed
        # 0x05 Connection Refused, not authorized The Client is not authorized to connect
        print('MqttConnAck connection : {}'.format(struct.unpack_from('!B', buffer, offset)[0] == 0x00))
        offset += 1

class MqttPublish(MqttMsg):
    def __init__(self, topic_name, text, dup_flag=0, QoS=0, retain=0, packed_id=None):
        topic_len = len(topic_name)
        text_len = len(text)
        packed_id_len = 0
        taille = 4 + topic_len + text_len
        if QoS != 0:
            packed_id_len = len(packed_id)
            taille += 2 + packed_id_len
        
        print("taille PUBLISH : {}".format(taille))

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

        print(self.buffer)

# PUBACK – Publish acknowledgement
class MqttPubRecv(MqttMsg):
    def __init__(self, buffer, dup_flag, QoS_level, retain):
        offset = 0
        topic_len = struct.unpack_from('!H', buffer, offset)[0]
        offset += 2
        
        topic_name = buffer[offset:offset+topic_len]
        offset += topic_len


        # VARIABLE_HEADER.PACKED_IDENTIFIER
        if QoS_level != 0:
            packed_id_len = struct.unpack_from('!H', buffer, offset)[0]
            offset += 2
            
            packed_id = buffer[offset:offset+packed_id_len]
            offset += packed_id_len

        # TEXT
        taille_text = len(buffer) - offset
        text = buffer[offset:offset+taille_text]
        offset += taille_text

        print('reception publication {} : {}'.format(topic_name, text))

# PUBACK – Publish acknowledgement
class MqttPubAck(MqttMsg):
    def __init__(self, buffer):

        offset = 0
        print('MqttPubAck packet_id : {}'.format(struct.unpack_from('!H', buffer, offset)[0]))
        offset += 2

# PUBREC – Publish received (QoS 2 publish received, part 1)
class MqttPubRec(MqttMsg):
    def __init__(self, buffer):

        offset = 0
        print('MqttPubRec packet_id : {}'.format(struct.unpack_from('!H', buffer, offset)[0]))
        offset += 2
        
# PUBREL – Publish release (QoS 2 publish received, part 2)
class MqttPubRel(MqttMsg):
    def __init__(self, buffer):

        offset = 0
        print('MqttPubRel packet_id : {}'.format(struct.unpack_from('!H', buffer, offset)[0]))
        offset += 2
       
# PUBCOMP – Publish complete (QoS 2 publish received, part 3)
class MqttPubComp(MqttMsg):
    def __init__(self, buffer):

        offset = 0
        print('MqttPubComp packet_id : {}'.format(struct.unpack_from('!H', buffer, offset)[0]))
        offset += 2

# SUBSCRIBE - Subscribe to topics
class MqttSubcribe(MqttMsg):
    def __init__(self, packed_id, topic_name, QoS):
        topic_len = len(topic_name)
        
        taille = 7 + topic_len
        print("taille SUBSCRIBE : {}".format(taille))

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

        print(self.buffer)

# SUBACK – Subscribe acknowledgement
class MqttSubAck(MqttMsg):
    def __init__(self, buffer):

        offset = 0
        print('MqttSubAck packet_id : {}'.format(struct.unpack_from('!H', buffer, offset)[0]))
        offset += 2
        # 0x00 - Success - Maximum QoS 0
        # 0x01 - Success - Maximum QoS 1
        # 0x02 - Success - Maximum QoS 2
        # 0x80 - Failure
        print('MqttSubAck erreur : {}'.format((struct.unpack_from('!B', buffer, offset)[0] & 0x80) == 0x80))
        print('MqttSubAck return_code : {}'.format(struct.unpack_from('!B', buffer, offset)[0] & 0x03))
        offset += 1

# UNSUBSCRIBE - Unsubscribe to topics
class MqttUnsubcribe(MqttMsg):
    def __init__(self, packed_id):
        taille = 4
        print("taille UNSUBSCRIBE : {}".format(taille))

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

        print(self.buffer)

# UNSUBACK – Unsubscribe acknowledgement
class MqttUnsubAck(MqttMsg):
    def __init__(self, buffer):

        offset = 0
        print('MqttUnsubAck packet_id : {}'.format(struct.unpack_from('!H', buffer, offset)[0]))
        offset += 2

# PINGREQ – PING request
class MqttPingReq(MqttMsg):
    def __init__(self):

        taille = 2
        print("taille PINGREQ : {}".format(taille))

        offset = 0
        self.buffer = bytearray(taille)
        struct.pack_into('!B', self.buffer, offset, 0xC0)
        offset += 1
        struct.pack_into('!B', self.buffer, offset, 0)
        offset += 1
        
        print(self.buffer)

#  PINGRESP – PING response
class MqttPingResp(MqttMsg):
    def __init__(self, buffer):
        pass

# DISCONNECT – Disconnect notification
class MqttDisconnect(MqttMsg):
    def __init__(self):
        
        taille = 2
        print("taille DISCONNECT : {}".format(taille))

        offset = 0
        self.buffer = bytearray(taille)
        struct.pack_into('!B', self.buffer, offset, 0xE0)
        offset += 1
        struct.pack_into('!B', self.buffer, offset, 0x00)
        offset += 1
        
        print(self.buffer)

class MqttError(BaseException):
    pass

class MqttResponse:
    def __init__(self):
        pass
    
    def analayseHeader(self, buffer):
        print('analayseHeader : ', buffer)
        if len(buffer) != 2:
            raise MqttError()

        type_packet, taille = struct.unpack('!BB', buffer)
        return type_packet, taille

    def analayseBody(self, type_packet, taille, buffer):
        print('analayseBody : ', buffer)

        if len(buffer) != taille:
            raise MqttError()

        # CONNACK
        if (type_packet & 0xF0) == 0x20:
            return MqttConnAck(buffer)

        # PUBLISH
        elif (type_packet & 0xF0) == 0x30:
            return MqttPubRecv(buffer, ((type_packet & 0x04) >> 3), ((type_packet & 0x06) >> 1), (type_packet & 0x01))

        # PUBACK
        elif (type_packet & 0xF0) == 0x40:
            return MqttPubAck(buffer)

        # PUBREC
        elif (type_packet & 0xF0) == 0x50:
            return MqttPubRec(buffer)
        
        # PUBREL
        elif (type_packet & 0xF0) == 0x60:
            return MqttPubRel(buffer)
        
        # PUBCOMP
        elif (type_packet & 0xF0) == 0x70:
            return MqttPubComp(buffer)
        
        # SUBACK
        elif (type_packet & 0xF0) == 0x90:
            return MqttSubAck(buffer)
        
        # UNSUBACK
        elif (type_packet & 0xB0) == 0xB0:
            return MqttUnsubAck(buffer)
        
        # PINGRESP
        elif (type_packet & 0xF0) == 0xD0:
            return MqttPingResp(buffer)

        else:
            raise MqttError()

