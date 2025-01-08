import struct

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
    def __init__(self, buffer, connectAcknowledgeFlags):

        offset = 0
        assert struct.unpack_from('!B', buffer, offset)[0] == 0x20
        offset += 1
        assert struct.unpack_from('!B', buffer, offset)[0] == 2
        offset += 1
        assert struct.unpack_from('!B', buffer, offset)[0] == connectAcknowledgeFlags
        offset += 1

        # 0x00 Connection Accepted Connection accepted
        # 0x01 Connection Refused, unacceptable protocol version The Server does not support the level of the MQTT protocol requested by the Client
        # 0x02 Connection Refused, identifier rejected The Client identifier is correct UTF-8 but not allowed by the Server
        # 0x03 Connection Refused, Server unavailable The Network Connection has been made but the MQTT service is unavailable
        # 0x04 Connection Refused, bad user name or password The data in the user name or password is malformed
        # 0x05 Connection Refused, not authorized The Client is not authorized to connect
        assert struct.unpack_from('!B', buffer, offset)[0] == 0x00
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
class MqttPubAck:
    def __init__(self, buffer, packet_id):

        offset = 0
        assert struct.unpack_from('!B', buffer, offset)[0] == 0x40
        offset += 1
        assert struct.unpack_from('!B', buffer, offset)[0] == 2
        offset += 1
        assert struct.unpack_from('!B', buffer, offset)[0] == packet_id
        offset += 1

# PUBREC – Publish received (QoS 2 publish received, part 1)
class MqttPubRec:
    def __init__(self, buffer, packet_id):

        offset = 0
        assert struct.unpack_from('!B', buffer, offset)[0] == 0x50
        offset += 1
        assert struct.unpack_from('!B', buffer, offset)[0] == 2
        offset += 1
        assert struct.unpack_from('!H', buffer, offset)[0] == packet_id
        offset += 2
        
# PUBREL – Publish release (QoS 2 publish received, part 2)
class MqttPubRel:
    def __init__(self, buffer, packet_id):

        offset = 0
        assert struct.unpack_from('!B', buffer, offset)[0] == 0x60
        offset += 1
        assert struct.unpack_from('!B', buffer, offset)[0] == 2
        offset += 1
        assert struct.unpack_from('!H', buffer, offset)[0] == packet_id
        offset += 2
       
# PUBCOMP – Publish complete (QoS 2 publish received, part 3)
class MqttPubComp:
    def __init__(self, buffer, packet_id):

        offset = 0
        assert struct.unpack_from('!B', buffer, offset)[0] == 0x70
        offset += 1
        assert struct.unpack_from('!B', buffer, offset)[0] == 2
        offset += 1
        assert struct.unpack_from('!H', buffer, offset)[0] == packet_id
        offset += 2

# SUBSCRIBE - Subscribe to topics
class MqttSubcribe:
    def __init__(self, packed_id, topic_name, QoS):
        topic_len = len(topic_name)
        
        taille = 9 + topic_len
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
    def __init__(self, buffer, packet_id, return_code):

        offset = 0
        assert struct.unpack_from('!B', buffer, offset)[0] == 0x90
        offset += 1
        assert struct.unpack_from('!B', buffer, offset)[0] == 3
        offset += 1
        assert struct.unpack_from('!H', buffer, offset)[0] == packet_id
        offset += 2
        # 0x00 - Success - Maximum QoS 0
        # 0x01 - Success - Maximum QoS 1
        # 0x02 - Success - Maximum QoS 2
        # 0x80 - Failure
        assert (struct.unpack_from('!B', buffer, offset)[0] & 0x80) != 0x80
        assert (struct.unpack_from('!B', buffer, offset)[0] & 0x03) == return_code
        offset += 1

# # PINGREQ – PING request
# class MqttPingReq:
#     def __init__(self):
# 
#         PINGREQ = {
#             "FIXED_HEADER" : (0, FIXED_HEADER)
#         }
#         
#         taille = 2
#         self.buffer = bytearray(taille)
#         msg = uctypes.struct(uctypes.addressof(self.buffer), PINGREQ, uctypes.BIG_ENDIAN)
#         msg.FIXED_HEADER.CTRL_PACKED.TYPE = CTRL_PACKED_TYPE.PINGREQ
#         msg.FIXED_HEADER.REMAINING_LENGTH = 0
#         
#         print(self.buffer)
# 
# #  PINGRESP – PING response
# class MqttPingResp:
#     def __init__(self, buffer):
# 
#         PINGRESP = {
#             "FIXED_HEADER" : (0, FIXED_HEADER)
#         }
#         
#         msg = uctypes.struct(uctypes.addressof(buffer), PINGRESP, uctypes.BIG_ENDIAN)
#         assert msg.FIXED_HEADER.CTRL_PACKED.TYPE == CTRL_PACKED_TYPE.PINGRESP
#         assert msg.FIXED_HEADER.REMAINING_LENGTH == 0
# 
# # DISCONNECT – Disconnect notification
# class MqttDisconnect:
#     def __init__(self):
# 
#         DISCONNECT = {
#             "FIXED_HEADER" : (0, FIXED_HEADER)
#         }
#         
#         taille = 2
#         self.buffer = bytearray(taille)
#         msg = uctypes.struct(uctypes.addressof(self.buffer), DISCONNECT, uctypes.BIG_ENDIAN)
#         msg.FIXED_HEADER.CTRL_PACKED.TYPE = CTRL_PACKED_TYPE.DISCONNECT
#         msg.FIXED_HEADER.REMAINING_LENGTH = 0
#         
#         print(self.buffer)

import network, time
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('domoticus', '9foF2sxArWU5')
while not wlan.isconnected() and wlan.status() >= 0:
    time.sleep(1)
time.sleep(5)

import binascii, machine, socket
PORT =  1883
SERVER = "192.168.1.108"
CLIENT_ID = binascii.hexlify(machine.unique_id())
# CLIENT_ID = (machine.unique_id())
sock = socket.socket()
# sock.setblocking(True)
sock.settimeout(20)
addr = socket.getaddrinfo(SERVER, PORT)[0][-1]
print(addr)
sock.connect(addr)

try:

    cnx = MqttConnect(client_id=CLIENT_ID, user='toff', passwd='crapaud8))', retain=0, QoS=0, clean=1, keep_alive=10)
    sock.write(cnx.buffer)

    cnxack = sock.read(4)
    print('connection ack : {}'.format(cnxack))
    if len(cnxack) != 0:
        MqttConnAck(cnxack, 0)

#     ping = MqttPingReq()
#     sock.write(ping.buffer)

#     pingresp = sock.read(2)
#     print('ping response : {}'.format(pingresp))
#     if len(pingresp) != 0:
#         MqttPingResp(pingresp)

    sub = MqttSubcribe(1, "a/b", 0)
    sock.write(sub.buffer)
    subresp = sock.read(5)
    print('sub response : {}'.format(subresp))
    MqttSubAck(subresp, 1, 0)

    pub = MqttPublish("a/b", "coucou")
    sock.write(pub.buffer)
    pubresp = sock.read(15)
    print('pub response : {}'.format(pubresp))
    if len(pubresp) != 0:
        MqttPubAck(pubresp, 3)

#     print('notification : {}'.format(sock.read(5)))

#     discnx = MqttDisconnect()
#     sock.write(discnx.buffer)
finally:
    sock.close()
    wlan.disconnect()

# 
# MqttPubRec(b'\x50\x02\x00\x00', 0)
# MqttPubRel(b'\x60\x02\x00\x00', 0)
# MqttPubComp(b'\x70\x02\x00\x00', 0)
# MqttPingReq()
# MqttPingResp(b'\xd0\00')
# MqttDisconnect()

