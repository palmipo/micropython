import uctypes
    
FIXED_HEADER = {
    "CTRL_PACKED": (0, {
        "TYPE" : 0 | uctypes.BFUINT8 | 4 << uctypes.BF_POS | 4 << uctypes.BF_LEN,
        "FLAG" : 0 | uctypes.BFUINT8 | 0 << uctypes.BF_POS | 4 << uctypes.BF_LEN,
        "DUP_FLAG" : 0 | uctypes.BFUINT8 | 3 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
        "QoS_LEVEL" : 0 | uctypes.BFUINT8 | 1 << uctypes.BF_POS | 2 << uctypes.BF_LEN,
        "RETAIN" : 0 | uctypes.BFUINT8 | 0 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
        }),
    "REMAINING_LENGTH": 1 | uctypes.UINT8
}

STR = {
    "LENGTH" : 0 | uctypes.UINT16,
    "PHRASE" : (2 | uctypes.ARRAY, uctypes.UINT8)
}

class CTRL_PACKED_TYPE:
        # Reserved 0 Forbidden Reserved
        CONNECT = 1 # Client to Server Client request to connect to Server
        CONNACK = 2 # Server to Client Connect acknowledgment
        PUBLISH = 3 # Client to Server or Publish message Server to Client
        PUBACK = 4 # Client to Server or Server to Client Publish acknowledgment
        PUBREC = 5 # Client to Server or Server to Client Publish received (assured delivery part 1)
        PUBREL = 6 # Client to Server or Server to Client Publish release (assured delivery part 2)
        PUBCOMP = 7 # Client to Server or Server to Client Publish complete (assured delivery part 3)
        SUBSCRIBE = 8 # Client to Server Client subscribe request
        SUBACK = 9 # Server to Client Subscribe acknowledgment
        UNSUBSCRIBE = 10 # Client to Server Unsubscribe request
        UNSUBACK = 11 # Server to Client Unsubscribe acknowledgment
        PINGREQ = 12 # Client to Server PING request
        PINGRESP = 13 # Server to Client PING response
        DISCONNECT = 14 # Client to Server Client is disconnecting
        # Reserved 15 Forbidden Reserved


class MqttConnect:
    def __init__(self, client_id, will_topic=None, will_message=None, user=None, passwd=None, retain=0, QoS=0, clean=0, keep_alive=0):
        client_id_len = len(client_id)
        
        will_topic_len = 0
        if will_topic != None:
            will_topic_len = len(will_topic)
            
        will_message_len = 0
        if will_message != None:
            will_message_len = len(will_message)

        user_len = 0
        passwd_len = 0
        if user != None:
            user_len = len(user)
    
            if passwd != None:
                passwd_len = len(passwd)

        CONNECT = {
            "FIXED_HEADER" : (0, FIXED_HEADER),
            "VARIABLE_HEADER" : (2 , {
                "PROTOCOL_NAME" : (0, {
                    "LENGTH": 0 | uctypes.UINT16,
                    "MAGIC_NUMBER": (2 | uctypes.ARRAY, 4 | uctypes.UINT8)
                }),
                "PROTOCOL_LEVEL": 6 | uctypes.UINT8,
                "FLAG" : (7, {
                    # User Name Flag
                    "USER_NAME" : 0 | uctypes.BFUINT8 | 7 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
                    # Password Flag
                    "PASSWORD" : 0 | uctypes.BFUINT8 | 6 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
                    # Will Retain 
                    "WILL_RETAIN" : 0 | uctypes.BFUINT8 | 5 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
                    # Will QoS 
                    "WILL_QoS" : 0 | uctypes.BFUINT8 | 3 << uctypes.BF_POS | 2 << uctypes.BF_LEN,
                    # Will Flag
                    "WILL" : 0 | uctypes.BFUINT8 | 2 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
                    # Clean Session
                    "CLEAN" : 0 | uctypes.BFUINT8 | 1 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
                }),
                "KEEP_ALIVE" : 8 | uctypes.UINT16,
            }),
            "PAYLOAD" : (12 , {
                "CLIENT_ID" : (0, {
                    "LENGTH" : 0 | uctypes.UINT16,
                    "PHRASE" : (2 | uctypes.ARRAY, client_id_len | uctypes.UINT8)
                })
            })
        }
        
        WILL_TOPIC = {
            "LENGTH" : 0 | uctypes.UINT16,
            "PHRASE" : (2 | uctypes.ARRAY, 0 | uctypes.UINT8)
        }
        
        WILL_MESSAGE = {
            "LENGTH" : 0 | uctypes.UINT16,
            "PHRASE" : (2 | uctypes.ARRAY, 0 | uctypes.UINT8)
        }
        
        USER_NAME = {
            "LENGTH" : 0 | uctypes.UINT16,
            "PHRASE" : (2 | uctypes.ARRAY, 0 | uctypes.UINT8)
        }
        
        PASSWD = {
            "LENGTH" : 0 | uctypes.UINT16,
            "PHRASE" : (2 | uctypes.PTR, 0 | uctypes.UINT8)
        }
        
        taille = 14 + client_id_len
        
        if will_topic != None:
            taille += 2 + will_topic_len
            
        if will_message != None:
            taille += 2 + will_message_len
            
        if user != None:
            taille += 2 + user_len
            if passwd != None:
                taille += 2+ passwd_len
        print('taille CONNECT : {}, client_id : {}, user : {} passwd : {}'.format(taille, client_id_len, user_len, passwd_len))
        self.buffer = bytearray(taille)
        msg = uctypes.struct(uctypes.addressof(self.buffer), CONNECT, uctypes.BIG_ENDIAN)
        
        msg.FIXED_HEADER.CTRL_PACKED.TYPE = CTRL_PACKED_TYPE.CONNECT
        msg.FIXED_HEADER.REMAINING_LENGTH = taille-2
        msg.VARIABLE_HEADER.PROTOCOL_NAME.LENGTH = 4
        msg.VARIABLE_HEADER.PROTOCOL_NAME.MAGIC_NUMBER[0] = ord('M')
        msg.VARIABLE_HEADER.PROTOCOL_NAME.MAGIC_NUMBER[1] = ord('Q')
        msg.VARIABLE_HEADER.PROTOCOL_NAME.MAGIC_NUMBER[2] = ord('T')
        msg.VARIABLE_HEADER.PROTOCOL_NAME.MAGIC_NUMBER[3] = ord('T')
        msg.VARIABLE_HEADER.PROTOCOL_LEVEL = 0x04
        msg.VARIABLE_HEADER.FLAG.CLEAN = clean
        msg.VARIABLE_HEADER.KEEP_ALIVE = keep_alive
        msg.PAYLOAD.CLIENT_ID.LENGTH = client_id_len
        offset = 14
        self.buffer[ offset : offset + client_id_len] = uctypes.bytes_at(uctypes.addressof(client_id), client_id_len)
        offset += client_id_len

        if will_topic != None:
            msg.VARIABLE_HEADER.FLAG.WILL = 1
            msg.VARIABLE_HEADER.FLAG.WILL_RETAIN = retain
            msg.VARIABLE_HEADER.FLAG.WILL_QoS = QoS
            msg_will_topic = uctypes.struct(uctypes.addressof(self.buffer) + offset, WILL_TOPIC, uctypes.BIG_ENDIAN)
            msg_will_topic.LENGTH = will_topic_len
            self.buffer[ offset + 2 : offset + will_topic_len + 2] = uctypes.bytes_at(uctypes.addressof(will_topic), will_topic_len)
            offset += will_topic_len + 2

        if will_message != None:
            msg.VARIABLE_HEADER.FLAG.WILL = 1
            msg.VARIABLE_HEADER.FLAG.WILL_RETAIN = retain
            msg.VARIABLE_HEADER.FLAG.WILL_QoS = QoS
            msg_will_message = uctypes.struct(uctypes.addressof(self.buffer) + offset, WILL_MESSAGE, uctypes.BIG_ENDIAN)
            msg_will_message.LENGTH = will_message_len
            self.buffer[ offset + 2 : offset + will_message_len + 2] = uctypes.bytes_at(uctypes.addressof(will_message), will_message_len)
            offset += will_message_len + 2

        if user != None:
            msg.VARIABLE_HEADER.FLAG.USER_NAME = 1
            msg_user = uctypes.struct(uctypes.addressof(self.buffer) + offset, USER_NAME, uctypes.BIG_ENDIAN)
            msg_user.LENGTH = user_len
            self.buffer[ offset + 2 : offset + user_len + 2] = uctypes.bytes_at(uctypes.addressof(user), user_len)
            offset += user_len + 2

            if passwd != None:
                msg.VARIABLE_HEADER.FLAG.PASSWORD = 1
                msg_passwd = uctypes.struct(uctypes.addressof(self.buffer) + offset, PASSWD, uctypes.BIG_ENDIAN)
                msg_passwd.LENGTH = passwd_len
                self.buffer[ offset + 2 : offset + passwd_len + 2] = uctypes.bytes_at(uctypes.addressof(passwd), passwd_len)
                offset += passwd_len + 2

        print(self.buffer)

# CONNACK – Acknowledge connection request
class MqttConnAck:
    def __init__(self, buffer, ack):

        CONNACK = {
            "FIXED_HEADER" : (0, FIXED_HEADER),
            "VARIABLE_HEADER" : (2 , {
                "FLAG" : (0, {
                    "ACKNOWLEDGE" : 0 | uctypes.BFUINT8 | 0 << uctypes.BF_POS | 1 << uctypes.BF_LEN
                    }),
                "RETURN_CODE": 1 | uctypes.UINT8
                })
        }

        msg = uctypes.struct(uctypes.addressof(buffer), CONNACK, uctypes.BIG_ENDIAN)
        assert msg.FIXED_HEADER.CTRL_PACKED.TYPE == CTRL_PACKED_TYPE.CONNACK
        assert msg.FIXED_HEADER.REMAINING_LENGTH == 2
        assert msg.VARIABLE_HEADER.FLAG.ACKNOWLEDGE == ack

        # 0x00 Connection Accepted Connection accepted
        # 0x01 Connection Refused, unacceptable protocol version The Server does not support the level of the MQTT protocol requested by the Client
        # 0x02 Connection Refused, identifier rejected The Client identifier is correct UTF-8 but not allowed by the Server
        # 0x03 Connection Refused, Server unavailable The Network Connection has been made but the MQTT service is unavailable
        # 0x04 Connection Refused, bad user name or password The data in the user name or password is malformed
        # 0x05 Connection Refused, not authorized The Client is not authorized to connect
        assert msg.VARIABLE_HEADER.RETURN_CODE == 0x00

class MqttPublish:
    def __init__(self, topic_name, text, dup_flag=0, QoS=0, retain=0, packed_id=None):
        topic_len = len(topic_name)
        text_len = len(text)
        packed_id_len = 0
        if packed_id != None:
            packed_id_len = len(packed_id)

        PUBLISH = {
            "FIXED_HEADER" : (0, FIXED_HEADER),
            "VARIABLE_HEADER" : (2 , {
                "TOPIC_NAME" : (0, {
                    "LENGTH" : 0 | uctypes.UINT16,
                    "TEXT" : (2 | uctypes.ARRAY, topic_len | uctypes.UINT8)
                })
            })
        }
        
        taille = 4 + topic_len + text_len
        if packed_id != None:
            taille += packed_id_len
        print("taille PUBLISH : {}".format(taille))

        self.buffer = bytearray(taille)
        msg = uctypes.struct(uctypes.addressof(self.buffer), PUBLISH, uctypes.BIG_ENDIAN)
        msg.FIXED_HEADER.CTRL_PACKED.TYPE = CTRL_PACKED_TYPE.PUBLISH
        msg.FIXED_HEADER.CTRL_PACKED.DUP_FLAG = dup_flag
        msg.FIXED_HEADER.CTRL_PACKED.QoS_LEVEL = QoS
        msg.FIXED_HEADER.CTRL_PACKED.RETAIN = retain
        msg.FIXED_HEADER.REMAINING_LENGTH = taille-2
        msg.VARIABLE_HEADER.TOPIC_NAME.LENGTH = topic_len
        self.buffer[ 4 : 4 + topic_len] = uctypes.bytes_at(uctypes.addressof(topic_name), topic_len)

        self.buffer[ 4 + topic_len : 4 + topic_len + text_len ] = uctypes.bytes_at(uctypes.addressof(text), text_len)

        print(self.buffer)

# PUBACK – Publish acknowledgement
class MqttPubAck:
    def __init__(self, buffer, packet_id):

        PUBACK = {
            "FIXED_HEADER" : (0, FIXED_HEADER),
            "VARIABLE_HEADER" : (2 , {
                "PACKET_ID" : 0 | uctypes.UINT16
            })
        }

        msg = uctypes.struct(uctypes.addressof(buffer), PUBACK, uctypes.BIG_ENDIAN)
        assert msg.FIXED_HEADER.CTRL_PACKED.TYPE == CTRL_PACKED_TYPE.PUBACK
        assert msg.FIXED_HEADER.REMAINING_LENGTH == 2
        assert msg.VARIABLE_HEADER.PACKET_ID == packet_id
       

# PUBREC – Publish received (QoS 2 publish received, part 1)
class MqttPubRec:
    def __init__(self, buffer, packet_id):

        PUBREC = {
            "FIXED_HEADER" : (0, FIXED_HEADER),
            "VARIABLE_HEADER" : (2 , {
                "PACKET_ID" : 0 | uctypes.UINT16
            })
        }

        msg = uctypes.struct(uctypes.addressof(buffer), PUBREC, uctypes.BIG_ENDIAN)
        assert msg.FIXED_HEADER.CTRL_PACKED.TYPE == CTRL_PACKED_TYPE.PUBREC
        assert msg.FIXED_HEADER.REMAINING_LENGTH == 2
        assert msg.VARIABLE_HEADER.PACKET_ID == packet_id
       
# PUBREL – Publish release (QoS 2 publish received, part 2)
class MqttPubRel:
    def __init__(self, buffer, packet_id):

        PUBREL = {
            "FIXED_HEADER" : (0, FIXED_HEADER),
            "VARIABLE_HEADER" : (2 , {
                "PACKET_ID" : 0 | uctypes.UINT16
            })
        }

        msg = uctypes.struct(uctypes.addressof(buffer), PUBREL, uctypes.BIG_ENDIAN)
        assert msg.FIXED_HEADER.CTRL_PACKED.TYPE == CTRL_PACKED_TYPE.PUBREL
        assert msg.FIXED_HEADER.REMAINING_LENGTH == 2
        assert msg.VARIABLE_HEADER.PACKET_ID == packet_id
       
# PUBCOMP – Publish complete (QoS 2 publish received, part 3)
class MqttPubComp:
    def __init__(self, buffer, packet_id):

        PUBCOMP = {
            "FIXED_HEADER" : (0, FIXED_HEADER),
            "VARIABLE_HEADER" : (2 , {
                "PACKET_ID" : 0 | uctypes.UINT16
            })
        }

        msg = uctypes.struct(uctypes.addressof(buffer), PUBCOMP, uctypes.BIG_ENDIAN)
        assert msg.FIXED_HEADER.CTRL_PACKED.TYPE == CTRL_PACKED_TYPE.PUBCOMP
        assert msg.FIXED_HEADER.REMAINING_LENGTH == 2
        assert msg.VARIABLE_HEADER.PACKET_ID == packet_id


# SUBSCRIBE - Subscribe to topics
class MqttSubcribe:
    def __init__(self, packed_id, topic_name, QoS):
        topic_len = len(topic_name)

        SUBSCRIBE = {
            "FIXED_HEADER" : (0, FIXED_HEADER),
            "VARIABLE_HEADER" : (2 , {
                "PACKET_ID" : 0 | uctypes.UINT16
            }),
            "PAYLOAD" : (4 , {
#                 "TOPIC_LEN" : 0 | uctypes.UINT16,
                "TOPIC_FILTER" : (0, {
                    "LENGTH" : 0 | uctypes.UINT16,
                    "TEXT" : (2 | uctypes.ARRAY, topic_len | uctypes.UINT8)
                }),
                "REQ_QoS" : (2 + topic_len, {
                    "QoS" : (0 | uctypes.BFUINT8 | 0 << uctypes.BF_POS | 2 << uctypes.BF_LEN)
                })
            })
        }
        print("taille SUBSCRIBE : {}".format(uctypes.sizeof(SUBSCRIBE)))
        
        taille = 9 + topic_len
        self.buffer = bytearray(taille)
        msg = uctypes.struct(uctypes.addressof(self.buffer), SUBSCRIBE, uctypes.BIG_ENDIAN)
        msg.FIXED_HEADER.CTRL_PACKED.TYPE = CTRL_PACKED_TYPE.SUBSCRIBE
        msg.FIXED_HEADER.CTRL_PACKED.QoS_LEVEL = 1
        msg.FIXED_HEADER.REMAINING_LENGTH = taille-2
        msg.VARIABLE_HEADER.PACKET_ID = packed_id
#         msg.PAYLOAD.TOPIC_LEN = 1
        msg.PAYLOAD.TOPIC_FILTER.LENGTH = topic_len
        # msg.TOPIC_FILTER.TEXT = ""
        self.buffer[8:8+topic_len] = uctypes.bytes_at(uctypes.addressof(topic_name), topic_len)
        msg.PAYLOAD.REQ_QoS.QoS = QoS
        
        print(self.buffer)

# SUBACK – Subscribe acknowledgement
class MqttSubAck:
    def __init__(self, buffer, packet_id, return_code):

        SUBACK = {
            "FIXED_HEADER" : (0, FIXED_HEADER),
            "VARIABLE_HEADER" : (2 , {
                "PACKET_ID" : 0 | uctypes.UINT16
            }),
            "PAYLOAD" : (4 , {
                "RETURN_CODE" : 0 | uctypes.UINT8
            }),
        }

        msg = uctypes.struct(uctypes.addressof(buffer), SUBACK, uctypes.BIG_ENDIAN)
        assert msg.FIXED_HEADER.CTRL_PACKED.TYPE == CTRL_PACKED_TYPE.SUBACK
        assert msg.FIXED_HEADER.REMAINING_LENGTH == 3
        assert msg.VARIABLE_HEADER.PACKET_ID == packet_id
        assert msg.PAYLOAD.RETURN_CODE == return_code

# PINGREQ – PING request
class MqttPingReq:
    def __init__(self):

        PINGREQ = {
            "FIXED_HEADER" : (0, FIXED_HEADER)
        }
        
        taille = 2
        self.buffer = bytearray(taille)
        msg = uctypes.struct(uctypes.addressof(self.buffer), PINGREQ, uctypes.BIG_ENDIAN)
        msg.FIXED_HEADER.CTRL_PACKED.TYPE = CTRL_PACKED_TYPE.PINGREQ
        msg.FIXED_HEADER.REMAINING_LENGTH = 0
        
        print(self.buffer)

#  PINGRESP – PING response
class MqttPingResp:
    def __init__(self, buffer):

        PINGRESP = {
            "FIXED_HEADER" : (0, FIXED_HEADER)
        }
        
        msg = uctypes.struct(uctypes.addressof(buffer), PINGRESP, uctypes.BIG_ENDIAN)
        assert msg.FIXED_HEADER.CTRL_PACKED.TYPE == CTRL_PACKED_TYPE.PINGRESP
        assert msg.FIXED_HEADER.REMAINING_LENGTH == 0

# DISCONNECT – Disconnect notification
class MqttDisconnect:
    def __init__(self):

        DISCONNECT = {
            "FIXED_HEADER" : (0, FIXED_HEADER)
        }
        
        taille = 2
        self.buffer = bytearray(taille)
        msg = uctypes.struct(uctypes.addressof(self.buffer), DISCONNECT, uctypes.BIG_ENDIAN)
        msg.FIXED_HEADER.CTRL_PACKED.TYPE = CTRL_PACKED_TYPE.DISCONNECT
        msg.FIXED_HEADER.REMAINING_LENGTH = 0
        
        print(self.buffer)

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
sock = socket.socket()
#sock.setblocking(True)
sock.settimeout(20)
addr = socket.getaddrinfo(SERVER, PORT)[0][-1]
print(addr)
sock.connect(addr)

try:

    cnx = MqttConnect(client_id=CLIENT_ID, user='toff', passwd='crapaud8))', retain=0, QoS=0, clean=1, keep_alive=0)
    sock.write(cnx.buffer)

    cnxack = sock.read(4)
    print('connection ack : {}'.format(cnxack))
    if len(cnxack) != 0:
        MqttConnAck(cnxack, 0)

#     ping = MqttPingReq()
#     sock.write(ping.buffer)
# 
#     pingresp = sock.read(2)
#     print('ping response : {}'.format(pingresp))
#     if len(pingresp) != 0:
#         MqttPingResp(pingresp)

#     sub = MqttSubcribe(1, "a/b", 0)
    sock.write(b'\x82\x08\x00\x01\x00\x03a/b\x00')
    subresp = sock.read(5)
    print('sub response : {}'.format(subresp))
    MqttSubAck(subresp, 1, 0)

    pub = MqttPublish("a/b", "coucou")
    sock.write(pub.buffer)
    pubresp = sock.read(4)
    print('pub response : {}'.format(pubresp))
    MqttPubAck(pubresp, 3)

    print('notification : {}'.format(sock.read(5)))

    discnx = MqttDisconnect()
    sock.write(discnx.buffer)
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
