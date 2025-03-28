import struct
from tools.mqtt.mqttmsg import MqttMsg

# DISCONNECT – Disconnect notification
class MqttDisconnect(MqttMsg):
    def __init__(self):
        
        taille = 2

        offset = 0
        self.buffer = bytearray(taille)
        struct.pack_into('!B', self.buffer, offset, 0xE0)
        offset += 1
        struct.pack_into('!B', self.buffer, offset, 0x00)
        offset += 1
