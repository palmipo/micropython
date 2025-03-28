import struct
from tools.mqtt.mqtterror import MqttError
from tools.mqtt.mqttping import MqttPingResp
from tools.mqtt.mqttunsubcribe import MqttUnsubAck
from tools.mqtt.mqttsubcribe import MqttSubAck
from tools.mqtt.mqttpublish import MqttPubRecv
from tools.mqtt.mqttpublish import MqttPubAck
from tools.mqtt.mqttpublish import MqttPubRec
from tools.mqtt.mqttpublish import MqttPubRel
from tools.mqtt.mqttpublish import MqttPubComp
from tools.mqtt.mqttconnect import MqttConnAck

class MqttResponse:
    def __init__(self):
        pass
    
    def analayseHeader(self, buffer):
        if len(buffer) != 2:
            raise MqttError('taille analyseHeader incorrect !')

        type_packet, taille = struct.unpack('!BB', buffer)
        return type_packet, taille

    def analayseBody(self, type_packet, taille, buffer):
        if len(buffer) != taille:
            raise MqttError('taille analayseBody incorrect !')

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
            raise MqttError('Message inconnu !')
