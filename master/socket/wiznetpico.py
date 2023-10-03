import network

class WiznetPico(LanBus):
    def open(self):
        nic = network.WIZNET5K(spi=machine.SPI(0), pin_cs=machine.Pin(17, machine.Pin.Output), pin_rst=machine.Pin(20, machine.Pin.Output))
        while !nic.isconnected():
            pass
        print(nic.ifconfig())

    def close(self):
        self.nic.disconnect()