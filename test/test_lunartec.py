from lunartec import Lunartec
from uartpico import UartPico

uart = UartPico(0, 9600, 0, 1)
aff = Lunartec("01", uart)
aff.send("HELLO GRENOUILLETTE 8)")

