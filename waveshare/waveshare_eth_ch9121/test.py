import time, machine

# uart1 = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5))
uart0 = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))

CFG = machine.Pin(14, machine.Pin.OUT)#,machine.Pin.PULL_UP)
CFG.value(1)
RST = machine.Pin(17, machine.Pin.OUT)#,machine.Pin.PULL_UP)
RST.value(1)

MODE = 1  #0:TCP Server 1:TCP Client 2:UDP Server 3:UDP Client
GATEWAY = (192, 168, 1, 25)   # GATEWAY
TARGET_IP = (169, 254, 88, 17)# TARGET_IP
LOCAL_IP = (192,168,1,250)    # LOCAL_IP
SUBNET_MASK = (255,255,255,0) # SUBNET_MASK
LOCAL_PORT1 = 5000             # LOCAL_PORT1
LOCAL_PORT2 = 4000             # LOCAL_PORT2
TARGET_PORT = 3000            # TARGET_PORT
BAUD_RATE = 115200            # BAUD_RATE



print("begin")

CFG.value(0)
time.sleep(0.1)

uart0.write(b'\x57\xab\x01')
time.sleep(0.1)
print('chip version number : {}'.format(ord(uart0.read(1))))

uart0.write(b'\x57\xab\x81')
time.sleep(0.1)
print('MAC address : {}'.format(uart0.read(6)))

uart0.write(b'\x57\xab\x03')
time.sleep(0.1)
print('port 1 connecté : {}'.format(uart0.read(1)))

uart0.write(b'\x57\xab\x04')
time.sleep(0.1)
print('port 2  connecté : {}'.format(uart0.read(1)))

uart0.write(b'\x57\xab\x10'+MODE.to_bytes(1, 'little'))
time.sleep(0.1)
print('mode TCP Client {}'.format(uart0.read(1)))

# uart0.write(b'\x57\xab\x11'+bytes(bytearray(LOCAL_IP)))
# time.sleep(0.1)
# print(uart0.read(1))

# uart0.write(b'\x57\xab\x12'+bytes(bytearray(SUBNET_MASK)))
# time.sleep(0.1)
# print(uart0.read(1))

# uart0.write(b'\x57\xab\x13'+bytes(bytearray(GATEWAY)))
# time.sleep(0.1)
# print(uart0.read(1))

# DHCP
uart0.write(b'\x57\xab\x17\x01')
time.sleep(0.1)
print(uart0.read(1))

# uart0.write(b'\x57\xab\x14'+LOCAL_PORT1.to_bytes(2, 'little'))
# time.sleep(0.1)
# print(uart0.read(1))

# uart0.write(b'\x57\xab\x15'+bytes(bytearray(TARGET_IP)))
# time.sleep(0.1)
# print(uart0.read(1))

# uart0.write(b'\x57\xab\x16'+TARGET_PORT.to_bytes(2, 'little'))
# time.sleep(0.1)
# print(uart0.read(1))

# uart0.write(b'\x57\xab\x21'+BAUD_RATE.to_bytes(4, 'little'))
# time.sleep(0.1)
# print(uart0.read(1))

#set port 2 OFF
uart0.write(b'\x57\xab\x39\x00')
time.sleep(0.1)
print(uart0.read(1))

uart0.write(b'\x57\xab\x33\x01')
time.sleep(0.1)
print(uart0.read(1))

uart0.write(b'\x57\xab\x0D')
time.sleep(0.1)
print(uart0.read(1))

uart0.write(b'\x57\xab\x0E')
time.sleep(0.1)
print(uart0.read(1))

uart0.write(b'\x57\xab\x5E')
time.sleep(1)
print(uart0.read(1))

CFG.value(1)
time.sleep(0.1)

print("end")
