import struct
from tools.mqtt.mqttmsg import MqttMsg

# PINGREQ – PING request
class MqttPingReq(MqttMsg):
    def __init__(self):

        taille = 2

        offset = 0
        self.buffer = bytearray(taille)
        self.struct.pack_into('!B', self.buffer, offset, 0xC0)
        offset += 1
        struct.pack_into('!B', self.buffer, offset, 0)
        offset += 1

#  PINGRESP – PING response
class MqttPingResp(MqttMsg):
    def __init__(self, buffer):
        pass
