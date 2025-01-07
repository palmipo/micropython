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
    def __init__(self, user=None, passwd=None, keep_alive=0):
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
            "PAYLOAD" : (10 , {
                "USER" : (0, {
                    "LENGTH" : 0 | uctypes.UINT16,
                    "PHRASE" : (2 | uctypes.ARRAY, user_len | uctypes.UINT8)
                }),
                "PASSWD" : (2 + user_len, {
                    "LENGTH" : 0 | uctypes.UINT16,
                    "PHRASE" : (2 | uctypes.PTR, (user_len + passwd_len) | uctypes.UINT8)
                })
            })
        }

        taille = uctypes.sizeof(CONNECT)
        print('taille : {}, user : {} passwd : {}'.format(taille, user_len, passwd_len))
        buffer = bytearray(taille)
        msg = uctypes.struct(uctypes.addressof(buffer), CONNECT, uctypes.BIG_ENDIAN)
        
        msg.FIXED_HEADER.CTRL_PACKED.TYPE = CTRL_PACKED_TYPE.CONNECT
        msg.FIXED_HEADER.CTRL_PACKED.FLAG = 0
        msg.FIXED_HEADER.REMAINING_LENGTH = taille-2
        msg.VARIABLE_HEADER.PROTOCOL_NAME.LENGTH = 4
        msg.VARIABLE_HEADER.PROTOCOL_NAME.MAGIC_NUMBER[0] = ord('M')
        msg.VARIABLE_HEADER.PROTOCOL_NAME.MAGIC_NUMBER[1] = ord('Q')
        msg.VARIABLE_HEADER.PROTOCOL_NAME.MAGIC_NUMBER[2] = ord('T')
        msg.VARIABLE_HEADER.PROTOCOL_NAME.MAGIC_NUMBER[3] = ord('T')
        msg.VARIABLE_HEADER.PROTOCOL_LEVEL = 0x04
        msg.VARIABLE_HEADER.FLAG.CLEAN = 1
        msg.VARIABLE_HEADER.KEEP_ALIVE = keep_alive

        if user != None:
            msg.FIXED_HEADER.REMAINING_LENGTH += user_len
            msg.VARIABLE_HEADER.FLAG.USER_NAME = 1
            msg.PAYLOAD.USER.LENGTH = user_len
            buffer[ 12 : 12 + user_len] = uctypes.bytes_at(uctypes.addressof(user), user_len)

            if passwd != None:
                msg.FIXED_HEADER.REMAINING_LENGTH += passwd_len
                msg.VARIABLE_HEADER.FLAG.PASSWORD = 1
                msg.PAYLOAD.PASSWD.LENGTH = passwd_len
                buffer[ 14 + user_len : 14 + user_len + passwd_len] = uctypes.bytes_at(uctypes.addressof(passwd), passwd_len)

        print(buffer)

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
        assert msg.VARIABLE_HEADER.FLAG.ACKNOWLEDGE == ack

        # 0x00 Connection Accepted Connection accepted
        # 0x01 Connection Refused, unacceptable protocol version The Server does not support the level of the MQTT protocol requested by the Client
        # 0x02 Connection Refused, identifier rejected The Client identifier is correct UTF-8 but not allowed by the Server
        # 0x03 Connection Refused, Server unavailable The Network Connection has been made but the MQTT service is unavailable
        # 0x04 Connection Refused, bad user name or password The data in the user name or password is malformed
        # 0x05 Connection Refused, not authorized The Client is not authorized to connect
        assert msg.VARIABLE_HEADER.RETURN_CODE == 0x00

class MqttPublish:
    def __init__(self, topic_name, text):
        text_len = len(text)
        topic_len = len(topic_name)

        PUBLISH = {
            "FIXED_HEADER" : (0, FIXED_HEADER),
            "VARIABLE_HEADER" : (2 , {
                "TOPIC_NAME" : (0, {
                    "LENGTH" : 0 | uctypes.UINT16,
                    "TEXT" : (2 | uctypes.ARRAY, topic_len | uctypes.UINT8)
                }),
                "PACKET_ID": (5, {
                    "LENGTH" : 0 | uctypes.UINT16,
                    "TEXT": (2 | uctypes.ARRAY, text_len | uctypes.UINT8)
                })
            })
        }
        print("taille PUBLISH : {}".format(uctypes.sizeof(PUBLISH)))
        
        taille = uctypes.sizeof(PUBLISH) - 1
        buffer = bytearray(taille)
        msg = uctypes.struct(uctypes.addressof(buffer), PUBLISH, uctypes.BIG_ENDIAN)
        msg.FIXED_HEADER.CTRL_PACKED.TYPE = CTRL_PACKED_TYPE.PUBLISH
        msg.FIXED_HEADER.CTRL_PACKED.DUP_FLAG = 0
        msg.FIXED_HEADER.CTRL_PACKED.QoS_LEVEL = 0
        msg.FIXED_HEADER.CTRL_PACKED.RETAIN = 0
        msg.FIXED_HEADER.REMAINING_LENGTH = taille-2
        msg.VARIABLE_HEADER.TOPIC_NAME.LENGTH = topic_len
        # msg.VARIABLE_HEADER.TOPIC_NAME.TEXT = ""
        msg.VARIABLE_HEADER.PACKET_ID.LENGTH = text_len
        # msg.VARIABLE_HEADER.PACKET_ID.TEXT = ""
        buffer[ 9 : 9 + len(text)] = uctypes.bytes_at(uctypes.addressof(text), len(text))

        print(buffer)

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
        
        taille = uctypes.sizeof(SUBSCRIBE) - 2
        buffer = bytearray(taille)
        msg = uctypes.struct(uctypes.addressof(buffer), SUBSCRIBE, uctypes.BIG_ENDIAN)
        msg.FIXED_HEADER.CTRL_PACKED.TYPE = CTRL_PACKED_TYPE.SUBSCRIBE
        msg.FIXED_HEADER.CTRL_PACKED.DUP_FLAG = 0
        msg.FIXED_HEADER.CTRL_PACKED.QoS_LEVEL = 1
        msg.FIXED_HEADER.CTRL_PACKED.RETAIN = 0
        msg.FIXED_HEADER.REMAINING_LENGTH = taille-2
        msg.VARIABLE_HEADER.PACKET_ID = packed_id
        msg.PAYLOAD.TOPIC_FILTER.LENGTH = topic_len
        # msg.TOPIC_FILTER.TEXT = ""
        buffer[6:6+topic_len] = uctypes.bytes_at(uctypes.addressof(topic_name), topic_len)
        msg.PAYLOAD.REQ_QoS.QoS = QoS
        
        print(buffer)

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
        assert msg.FIXED_HEADER.REMAINING_LENGTH == 5
        assert msg.VARIABLE_HEADER.PACKET_ID == packet_id
        assert msg.PAYLOAD.RETURN_CODE == return_code



MqttConnect(user='toff', passwd='leMotDePasseDeLaMortQuiTue', keep_alive=0xffff)
MqttConnAck(b'\x20\x02\x01\x00', 1)
MqttPublish("a/b", "coucou")
MqttPubAck(b'\x40\x02\x00\x00', 0)
MqttPubRec(b'\x50\x02\x00\x00', 0)
MqttPubRel(b'\x60\x02\x00\x00', 0)
MqttPubComp(b'\x70\x02\x00\x00', 0)
MqttSubcribe(0, "a/b", 1)
MqttSubAck(b'\x90\x05\x00\x00\x80', 0, 0x80)