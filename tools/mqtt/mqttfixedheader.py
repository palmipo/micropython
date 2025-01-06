class MqttFixedHeader:
	def __init__(self, ctrl):
        self.ctrlPacketType = ctrl # MQTT Control Packet type 
        self.flagPacketType = 0 # Flags specific to each MQTT Control Packet type
        self.fixedHeaderLength = 0

        # Reserved 0 Forbidden Reserved
        self.CONNECT = 1 # Client to Server Client request to connect to Server
        self.CONNACK = 2 # Server to Client Connect acknowledgment
        self.PUBLISH = 3 # Client to Server or Publish message Server to Client
        self.PUBACK = 4 # Client to Server or Server to Client Publish acknowledgment
        self.PUBREC = 5 # Client to Server or Server to Client Publish received (assured delivery part 1)
        self.PUBREL = 6 # Client to Server or Server to Client Publish release (assured delivery part 2)
        self.PUBCOMP = 7 # Client to Server or Server to Client Publish complete (assured delivery part 3)
        self.SUBSCRIBE = 8 # Client to Server Client subscribe request
        self.SUBACK = 9 # Server to Client Subscribe acknowledgment
        self.UNSUBSCRIBE = 10 # Client to Server Unsubscribe request
        self.UNSUBACK = 11 # Server to Client Unsubscribe acknowledgment
        self.PINGREQ = 12 # Client to Server PING request
        self.PINGRESP = 13 # Server to Client PING response
        self.DISCONNECT = 14 # Client to Server Client is disconnecting
        # Reserved 15 Forbidden Reserved

class MqttConnect(MqttFixedHeader):
    def __init__(self):
        super().__init__(MqttFixedHeader.CONNECT)
        self.variableHeader = b'\x00\x04MQTT'
        self.protocolLevel = b'\x04'

        # User Name Flag
        # Password Flag
        # Will Retain 
        # Will QoS 
        # Will Flag
        # Clean Session
        self.connectFlag = 0
        
        # Keep Alive MSB / LSB
        seld.keepAlive = 0
        
# CONNACK – Acknowledge connection request
class MqttConnack(MqttFixedHeader):
    def __init__(self):
        super().__init__(MqttFixedHeader.CONNACK)

        self.connectAcknowledgeFlags = 0

        # 0x00 Connection Accepted Connection accepted
        # 0x01 Connection Refused, unacceptable protocol version The Server does not support the level of the MQTT protocol requested by the Client
        # 0x02 Connection Refused, identifier rejected The Client identifier is correct UTF-8 but not allowed by the Server
        # 0x03 Connection Refused, Server unavailable The Network Connection has been made but the MQTT service is unavailable
        # 0x04 Connection Refused, bad user name or password The data in the user name or password is malformed
        # 0x05 Connection Refused, not authorized The Client is not authorized to connect
        self.connectReturnCode = 0