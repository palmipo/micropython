class Elexol:
	def __init__(self, address):
		self.__socket = socket.socket(af=AF_INET, type=DATA_STREAM, proto=IPPROTO_TCP)
		self.__socket.connect(self.__socket.socket.getaddrinfo("192.168.10.1", 2424)[0][-1])
		
	def deconnexion(self):
		self.__socket.close()
		
	def writePort(self, port, valeur):
		cmd = bytearray(2)
		cmd[0] = 0x41 | (port & 0x03)
		cmd[1] = valeur
		self.__socket.send(cmd)
		
	def readPort(self, port):
		cmd = bytearray(1)
		cmd = 0x61 | (port & 0x03)
		self.__socket.send(cmd)
		rsp = self.__socket.recv(2)
		return rsp[1]
		
	def setDirectionPort(self, port, direction):
		cmd = bytearray(3)
		cmd[0] = 0x21
		cmd[1] = 0x41 | (port & 0x03)
		cmd[2] = valeur
		self.__socket.send(cmd)
	
	def identifyIO24Units(self):
		cmd = bytearray(4)
		cmd[0] = 0x49
		cmd[1] = 0x4F
		cmd[2] = 0x32
		cmd[3] = 0x34
		self.__socket.send(cmd)
		rsp = self.__socket.recv(12)
		mac = rsp[0:10]
		firmware = rsp[11:12]