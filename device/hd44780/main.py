from i2cpico import I2CPico
from lcd2004 import LCD2004
from hd44780 import HD44780
import sys
import time

try:
    
    i2c = I2CPico(0, 4, 5) 
    print( i2c.scan() )

    lcd_io = LCD2004(0, i2c)
    lcd_io.setBackLight(1)
    lcd = HD44780(lcd_io)
    lcd.clear()

    while True:

        data_tuple = time.localtime()
        laDate = "{:02}/{:02}/{:02}".format(str(data_tuple[2]), str(data_tuple[1]), str(data_tuple[0]))
        lHeure = "{:02}:{:02}:{:02}".format(str(data_tuple[3]), str(data_tuple[4]), str(data_tuple[5]))

        try:
            lcd.home()
            lcd.writeText("Hello World !!!")
#             lcd.setDDRAMAdrress(32)
#             lcd.writeText(lHeure)
#             lcd.setDDRAMAdrress(20)
#             lcd.writeText(laDate)
        except OSError:
            print("erreur LCD2004")

        time.sleep(1)

except OSError:
    print("erreur LCD2004")
    sys.exit()

except KeyboardInterrupt:
    print("exit")
    sys.exit()
