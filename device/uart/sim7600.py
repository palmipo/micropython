from uartbus import UartBus

class Sim7600:
	def __init__(self, uart):
		__uart__ = uart
        __uart__.send("AT")
   		__uart__.recv(8)

	def sendSms(self, phoneNumber, texte):
		__uart__.send("AT+CMGF=1")
		__uart__.send("AT+CMGS=\"" + phoneNumber + "\"")
		__uart__.recv(1)
		__uart__.send(texte)
		__uart__.send(b'\x1A')
   		__uart__.recv(8)

    def sendCall(self, phoneNumber):
        __uart__.send("ATD<" + phoneNumber + ">;")
   		__uart__.recv(8)

    def hangUp(self):
        __uart__.send("AT+CHUP")

    def answerCall(self):
        __uart__.send("ATA")

    def gps(self):
        __uart__.send("AT+CGPS=1")
        __uart__.send("AT+CGPSINFO")
        trame = __uart__.recv(50)
        __uart__.send("AT+CGPS=0")
        return trame
