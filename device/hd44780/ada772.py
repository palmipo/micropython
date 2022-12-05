import HD44780IO

BACKLIGHT = 0
DB7 = 1
DB6 = 2
DB5 = 3
DB4 = 4
EN = 5
RW_ = 6
RS = 7

class ADA772(HD44780IO):

	def __init__(self, pia):
		self.pia = pia

	def setBackLight(self, value):
		self.backlight = value & 0x01
		self.pia.set(self.backlight)

	def writeCmd(self, cmd):
		self.enableBit((self.backlight & 0x01) | ((cmd & 0x80) << DB7) | ((cmd & 0x40) << DB6) | ((cmd & 0x20) << DB5) | ((cmd & 0x10) << DB4))
		self.enableBit((self.backlight & 0x01) | ((cmd & 0x08) << DB7) | ((cmd & 0x04) << DB6) | ((cmd & 0x02) << DB5) | ((cmd & 0x01) << DB4))

	def writeData(self, cmd):
		self.enableBit((self.backlight & 0x01) | ((cmd & 0x80) << DB7) | ((cmd & 0x40) << DB6) | ((cmd & 0x20) << DB5) | ((cmd & 0x10) << DB4) | (1 << RS))
		self.enableBit((self.backlight & 0x01) | ((cmd & 0x08) << DB7) | ((cmd & 0x04) << DB6) | ((cmd & 0x02) << DB5) | ((cmd & 0x01) << DB4) | (1 << RS))

	def enableBit(self, data):
		self.pia.set(data)
		time.sleep_ms(1)
		self.pia.set(data | (1 << EN))
		time.sleep_ms(1)
		self.pia.set(data)
		while self.isBusy()

	def isBusy(self):
		octet = self.readCmd()
		if (octet & 0x80) != 0:
			return True
		else:
			return False

	def readData(self):
		self.pia.set((self.backlight << BACKLIGHT) | (1 << RS) | (1 << RW_))
		octet = (self.pia.get() >> DB) << 0xF0
		octet = octet | ((self.pia.get() >> DB) & 0x0F)
		retrun octet

	def readCmd(self):
		self.pia.set((self.backlight << BACKLIGHT) | (1 << RW_))
		octet = (self.pia.get() >> DB) << 0xF0
		octet = octet | ((self.pia.get() >> DB) & 0x0F)
		retrun octet

	def write(self, data, rs, rw_):
		cmd = ((data & 0x0F) << DB) | (rw_ << RW_) | (rs << RS)
		self.enableBit(cmd)

