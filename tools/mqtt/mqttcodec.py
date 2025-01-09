import struct, select

# taille CONNECT : 44, client_id : 12, user : 4 passwd : 10
# bytearray(b'\x10\x2a\x00\x04MQTT\x04\xc2\x00\x00\x00\x0c84f703e869e6\x00\x04XXXX\x00\nXXXXXXXXXX')
class MqttConnect:
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
class MqttConnAck:
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

class MqttPublish:
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
class MqttPubRecv:
    def __init__(self, buffer, dup_flag, QoS_level, retain):

        offset = 0
        topic_len = struct.unpack_from('!H', buffer, offset)[0]
        offset += 2
        
        for i in range(topic_len):
            print(struct.unpack_from('s', buffer, offset)[0])
            offset += 1


        # VARIABLE_HEADER.PACKED_IDENTIFIER
        if QoS_level != 0:
            packed_id_len = struct.unpack_from('!H', self.buffer, offset)[0]
            offset += 2
            
            for i in range(packed_id_len):
                print(struct.unpack_from('s', self.buffer, offset)[0])
                offset += 1

        # TEXT
        taille_text = len(buffer) - offset
        for i in range(taille_text):
            print(struct.unpack_from('s', buffer, offset)[0])
            offset += 1

# PUBACK – Publish acknowledgement
class MqttPubAck:
    def __init__(self, buffer):

        offset = 0
        print('MqttPubAck packet_id : {}'.format(struct.unpack_from('!H', buffer, offset)[0]))
        offset += 2

# PUBREC – Publish received (QoS 2 publish received, part 1)
class MqttPubRec:
    def __init__(self, buffer):

        offset = 0
        print('MqttPubRec packet_id : {}'.format(struct.unpack_from('!H', buffer, offset)[0]))
        offset += 2
        
# PUBREL – Publish release (QoS 2 publish received, part 2)
class MqttPubRel:
    def __init__(self, buffer):

        offset = 0
        print('MqttPubRel packet_id : {}'.format(struct.unpack_from('!H', buffer, offset)[0]))
        offset += 2
       
# PUBCOMP – Publish complete (QoS 2 publish received, part 3)
class MqttPubComp:
    def __init__(self, buffer):

        offset = 0
        print('MqttPubComp packet_id : {}'.format(struct.unpack_from('!H', buffer, offset)[0]))
        offset += 2

# SUBSCRIBE - Subscribe to topics
class MqttSubcribe:
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
class MqttSubAck:
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
class MqttUnsubcribe:
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
class MqttUnsubAck:
    def __init__(self, buffer):

        offset = 0
        print('MqttUnsubAck packet_id : {}'.format(struct.unpack_from('!H', buffer, offset)[0]))
        offset += 2

# PINGREQ – PING request
class MqttPingReq:
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
class MqttPingResp:
    def __init__(self, buffer):
        pass

# DISCONNECT – Disconnect notification
class MqttDisconnect:
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

class MqttResponse:
    def __init__(self, evnt):
        if evnt[1] == select.POLLIN:
            header = evnt[0].read(2)
            print('header ack : {}'.format(header))
            (type_packet, taille) = struct.unpack('!BB', header)
            if taille > 0:
                buffer = evnt[0].read(taille)
        
                # CONNACK
                if (type_packet & 0xF0) == 0x20:
                    MqttConnAck(buffer)

                # PUBLISH
                elif (type_packet & 0xF0) == 0x30:
                    MqttPubRecv(buffer, ((type_packet & 0x04) >> 3), ((type_packet & 0x06) >> 1), (type_packet & 0x01))

                # PUBACK
                elif (type_packet & 0xF0) == 0x40:
                    MqttPubAck(buffer)

                # PUBREC
                elif (type_packet & 0xF0) == 0x50:
                    pass
                
                # PUBREL
                elif (type_packet & 0xF0) == 0x60:
                    MqttPubRel(buffer)
                
                # PUBCOMP
                elif (type_packet & 0xF0) == 0x70:
                    MqttPubComp(buffer)
                
                # SUBACK
                elif (type_packet & 0xF0) == 0x90:
                    MqttSubAck(buffer)
                
                # UNSUBACK
                elif (type_packet & 0xB0) == 0xB0:
                    MqttUnsubAck(buffer)
                
                # PINGRESP
                elif (type_packet & 0xF0) == 0xD0:
                    MqttPingResp(buffer)

                else:
                    print('PAS GERER ...')

