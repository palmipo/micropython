from machine import UART

uart = machine.UART(0, baudrate = 9600)
print("UART Info : ", uart)
#print(uart.read())
uart.write("hello world")
#while 1 :
#    texte = uart.read()
#    print (texte)