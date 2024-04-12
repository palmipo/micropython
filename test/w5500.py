import network

nic = network.WIZNET5K(machine.SPI(0, baudrate=10_000_000, polarity=0, phase=0, bits=8, sck=machine.Pin(18), mosi=machine.Pin(19), miso=machine.Pin(16)), machine.Pin(17), machine.Pin(21))
print(nic.ifconfig())
