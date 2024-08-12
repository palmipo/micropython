from interface.uartbus import UartBus

class Lunartec:
    def __init__(self, ident, uart):
        self._uart = uart
        self._id = ident
        cmd = "<ID><{}><E>".format(self._id)
        self._uart.send(cmd)

    def set_time(self):
        data = "<SC>{:02d}{:02d}{:02d}{:02d}{:02d}{:02d}{:02d}".format(73,04,01,18,16,45,00)
        self.__write__(data);

    def send(self, text):
        data = "<L1><PB><FA><MC><WA><FA>"
        data += text[:420]
        self.__write__(data);

    def __write__(self, data):
        cmd = str.format("<ID{}>{:s}{:02X}<E>".format(self._id, data, self.__check_sum__(data)))
        self._uart.send(cmd)

    def __check_sum__(self, text):
        cs = 0
        for i in range(len(text)):
            cs = cs ^ ord(text[i])
        return cs;
