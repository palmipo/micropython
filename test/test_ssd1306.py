from ssd1306 import SSD1306_I2C
from i2cpico import I2CPico

busi2c = I2CPico(0, 4, 5)
print(hex(busi2c.scan()[0]))
afficheur = SSD1306_I2C(128, 64, busi2c)
#afficheur.poweron()
#afficheur.poweroff()
#afficheur.fill(0xF)
afficheur.text('Hello World !!!', 0, 10)
#afficheur.hline(0, 9, 96, 0xffff)
#afficheur.contrast(255)
afficheur.show()