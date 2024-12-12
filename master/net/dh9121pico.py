import machine
import network

uart = machine.UART(bus, baudrate=bdrate, tx=machine.Pin(pinTx), rx=machine.Pin(pinRx))
uart.init(bdrate, bits=8, parity=None, stop=1)

ppp = network.PPP(uart)
ppp.connect()


# uart2 = UART(2, baudrate=921600, tx = 14, rx=21,txbuf=4096, rxbuf=4096, timeout=200) ### AUX PORT FOR PPP
# uart2.write('AT\r\n')
# if "OK" in (uart2.read()):
# print("Aux uart connected") #activate context
# uart2.write("ATD*99#\r\n")
# 
# pppos = network.PPP(uart2)
# pppos.active(True)
# pppos.connect()