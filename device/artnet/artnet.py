import socket

class ArtNet:

	def __init__(self, protocol, portPysique, univers):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		trameDmx = bytearray(530)
		trameDmx[0] = 'A'
		trameDmx[1] = 'r'
		trameDmx[2] = 't'
		trameDmx[3] = '-'
		trameDmx[4] = 'N'
		trameDmx[5] = 'e'
		trameDmx[6] = 't'
		trameDmx[7] = 0
		trameDmx[8] = (protocol & 0xFF00) >> 8
		trameDmx[9] = (protocol & 0x00FF)
		trameDmx[10] = 0
		trameDmx[11] = 0x0E
		trameDmx[12] = 0
		trameDmx[13] = portPysique & 0xFF
		trameDmx[14] = (univers & 0xFF00) >> 8
		trameDmx[15] = (univers & 0x00FF)
		trameDmx[16] = 0x02
		trameDmx[17] = 0x00

	def connect(self, adresseIp):
		sock.connect(adresseIp, 0x1936)

	def setValue(self, canal, valeur):
		trameDmx[18+canal] = valeur;

	def write(self, numeroTrame):
		trameDmx[12] = numeroTrame & 0xFF
		sock.write(trameDmx)

	def close(self):
		sock.close()
