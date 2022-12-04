import network
import time
import ubinascii
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print(mac)
wlan.connect('xxxx', 'xxxx')
while not wlan.isconnected() and wlan.status() >= 0:
  print("Waiting to connect:")
  time.sleep(1)
time.sleep(5)
print(wlan.ifconfig())
wlan.disconnect()
