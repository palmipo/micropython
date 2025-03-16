import time, sys

try:
    time.sleep(5)

    # Change myprogram to whatever you renamed your current main.py to.
    import device.modbus.or_we_504
    device.modbus.or_we_504.main()

except KeyboardInterrupt:
    print("exit")
    sys.exit()
