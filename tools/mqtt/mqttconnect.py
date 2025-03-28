import struct
from tools.mqtt.mqttmsg import MqttMsg

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


# CONNACK – Acknowledge connection request
class MqttConnAck(MqttMsg):
    def __init__(self, buffer):

        offset = 0
        self.connectAcknowledgeFlags = struct.unpack_from('!B', buffer, offset)[0]
        offset += 1

        # 0x00 Connection Accepted Connection accepted
        # 0x01 Connection Refused, unacceptable protocol version The Server does not support the level of the MQTT protocol requested by the Client
        # 0x02 Connection Refused, identifier rejected The Client identifier is correct UTF-8 but not allowed by the Server
        # 0x03 Connection Refused, Server unavailable The Network Connection has been made but the MQTT service is unavailable
        # 0x04 Connection Refused, bad user name or password The data in the user name or password is malformed
        # 0x05 Connection Refused, not authorized The Client is not authorized to connect
        self.connection = struct.unpack_from('!B', buffer, offset)[0]
        offset += 1
