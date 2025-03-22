import time, sys

try:
    time.sleep(5)

    # Change myprogram to whatever you renamed your current main.py to.
    import orno_we504_mqtt
    orno_we504_mqtt.main()

except KeyboardInterrupt:
    print("exit")
    sys.quit()
