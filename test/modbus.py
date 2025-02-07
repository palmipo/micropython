import serial, select, struct, time

class ModbusRtu:
    def __init__(self, rs485):
        self.rs485 = rs485
        self.p = select.poll()
        self.p.register(rs485, select.POLLIN)
    
    def transfer(self, sendBuffer, recvLen):
        buffer = bytearray(len(sendBuffer) + 2)
        buffer[0:len(sendBuffer)] = sendBuffer
        crc0 = self.calcul_crc(sendBuffer)
        buffer[len(sendBuffer):] = crc0
        print(buffer)

        self.rs485.write(buffer)
        recvBuffer = self.rs485.read(recvLen + 2)
        print(recvBuffer)
        if len(recvBuffer) == 0:
            print("buffer de reception vide !")
  
        buffer = recvBuffer[0:recvLen]
        crc1 = recvBuffer[recvLen:]
        crc2 = self.calcul_crc(buffer)
        if crc1 != crc2:
            print("crc calcule different du crc recu !")

        return buffer
        

    def calcul_crc(self, data):
        auchCRCHi = b'\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40\x00\xC1\x81\x40\x01\xC0\x80\x41\x00\xC1\x81\x40\x01\xC0\x80\x41\x01\xC0\x80\x41\x00\xC1\x81\x40'
        auchCRCLo = b'\x00\xC0\xC1\x01\xC3\x03\x02\xC2\xC6\x06\x07\xC7\x05\xC5\xC4\x04\xCC\x0C\x0D\xCD\x0F\xCF\xCE\x0E\x0A\xCA\xCB\x0B\xC9\x09\x08\xC8\xD8\x18\x19\xD9\x1B\xDB\xDA\x1A\x1E\xDE\xDF\x1F\xDD\x1D\x1C\xDC\x14\xD4\xD5\x15\xD7\x17\x16\xD6\xD2\x12\x13\xD3\x11\xD1\xD0\x10\xF0\x30\x31\xF1\x33\xF3\xF2\x32\x36\xF6\xF7\x37\xF5\x35\x34\xF4\x3C\xFC\xFD\x3D\xFF\x3F\x3E\xFE\xFA\x3A\x3B\xFB\x39\xF9\xF8\x38\x28\xE8\xE9\x29\xEB\x2B\x2A\xEA\xEE\x2E\x2F\xEF\x2D\xED\xEC\x2C\xE4\x24\x25\xE5\x27\xE7\xE6\x26\x22\xE2\xE3\x23\xE1\x21\x20\xE0\xA0\x60\x61\xA1\x63\xA3\xA2\x62\x66\xA6\xA7\x67\xA5\x65\x64\xA4\x6C\xAC\xAD\x6D\xAF\x6F\x6E\xAE\xAA\x6A\x6B\xAB\x69\xA9\xA8\x68\x78\xB8\xB9\x79\xBB\x7B\x7A\xBA\xBE\x7E\x7F\xBF\x7D\xBD\xBC\x7C\xB4\x74\x75\xB5\x77\xB7\xB6\x76\x72\xB2\xB3\x73\xB1\x71\x70\xB0\x50\x90\x91\x51\x93\x53\x52\x92\x96\x56\x57\x97\x55\x95\x94\x54\x9C\x5C\x5D\x9D\x5F\x9F\x9E\x5E\x5A\x9A\x9B\x5B\x99\x59\x58\x98\x88\x48\x49\x89\x4B\x8B\x8A\x4A\x4E\x8E\x8F\x4F\x8D\x4D\x4C\x8C\x44\x84\x85\x45\x87\x47\x46\x86\x82\x42\x43\x83\x41\x81\x80\x40'
        uchCRCHi = 0xFF #; /* high byte of CRC initialized */
        uchCRCLo = 0xFF #; /* low byte of CRC initialized */
        uIndex = 0x00 #; /* will index into CRC lookup table */

        for i in range(len(data)): #/* pass through message buffer */
            uIndex = uchCRCHi ^ data[i] # ; /* calculate the CRC */
            uchCRCHi = uchCRCLo ^ auchCRCHi[uIndex];
            uchCRCLo = auchCRCLo[uIndex] ;

        res = bytearray(2)
        res[0] = uchCRCHi
        res[1] = uchCRCLo
        return res


class OR_WE_504:
    def __init__(self, modbus_id, rs485):
        self.modbus_id = modbus_id

    def setModbusId(self, modbus_id):
        #r = bus.transfer(struct.pack('>BBHHBH', self.modbus_id, 0x10, 0x000F, 0x01, 0x02, modbus_id), 6)
        r = bus.transfer(struct.pack('>BBHH', self.modbus_id, 0x06, 0x000F, modbus_id), 6)
        if len(r) != 0:
            vv = struct.unpack('>BBHH', r[0:6])
            if (vv[1] & 0x80) != 0x00:
                return ('erreur')
            self.modbus_id = vv[3]
            #time.sleep(10)

    def getModbusId(self):
        v = bus.transfer(struct.pack('>BBHH', self.modbus_id, 0x03, 0x000F, 0x01), 5)
        if len(v) != 0:
            vv = struct.unpack('>BBBH', v[0:5])
            if (vv[1] & 0x80) != 0x00:
                return 'erreur'
            return vv[3]

    def getBaudRate(self):
        v = bus.transfer(struct.pack('>BBHH', self.modbus_id, 0x03, 0x000E, 0x01), 5)
        if len(v) != 0:
            vv = struct.unpack('>BBBH', v[0:5])
            if (vv[1] & 0x80) != 0x00:
                return 'erreur'
            return vv[3]

    def passwordEfficacy(self, passwd):
        r = bus.transfer(struct.pack('>BBHHB', self.modbus_id, 0x10, 0x0040, len(passwd)>>1, len(passwd)) + passwd, 6)
        if len(r) != 0:
            rr = struct.unpack('>BBHH', r[0:6])
            if (rr[1] & 0x80) != 0x00:
                return 'erreur'

    def removePassword(self, passwd):
        r = bus.transfer(struct.pack('>BBHHB', self.modbus_id, 0x10, 0x116, len(passwd)>>1, len(passwd)) + passwd, 6)
        if len(r) != 0:
            rr = struct.unpack('>BBHH', r[0:6])
            if (rr[1] & 0x80) != 0x00:
                return 'erreur'
            #time.sleep(10)

    def voltage(self):
        v = bus.transfer(struct.pack('>BBHH', self.modbus_id, 0x03, 0x00, 0x01), 5)
        if len(v) != 0:
            vv = struct.unpack('>BBBH', v[0:5])
            if (vv[1] & 0x80) != 0x00:
                return 'erreur'
            return vv[3]/10

    def intensite(self):
        v = bus.transfer(struct.pack('>BBHH', self.modbus_id, 0x03, 0x01, 0x01), 5)
        if len(v) != 0:
            vv = struct.unpack('>BBBH', v[0:5])
            if (vv[1] & 0x80) != 0x00:
                return 'erreur'
            return vv[3]/10

    def frequence(self):
        v = bus.transfer(struct.pack('>BBHH', self.modbus_id, 0x03, 0x02, 0x01), 5)
        if len(v) != 0:
            vv = struct.unpack('>BBBH', v[0:5])
            if (vv[1] & 0x80) != 0x00:
                return 'erreur'
            return vv[3]/10

uart = serial.Serial('/dev/ttyUSB0', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=5)
bus = ModbusRtu(uart)
cpt = OR_WE_504(0x01, bus)

#print(cpt.getModbusId())
#cpt.passwordEfficacy(struct.pack('>HHHH', 0x12, 0x34, 0x56, 0x78))
#cpt.passwordEfficacy(struct.pack('>HHHH', 0, 0, 0, 0))
#cpt.removePassword(struct.pack('>HHHH', 0, 0, 0, 0))
#cpt.setModbusId(0x02)
#print(cpt.getBaudRate())
#print(cpt.voltage())
#print(cpt.intensite())
#print(cpt.frequence())
for i in range(0xffff):
    print(i)
    bus.transfer(struct.pack('>BBHH', 0x00, 0x03, i, 0x01), 5)
    print('')
uart.close()
