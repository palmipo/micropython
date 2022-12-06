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
		time.sleep_ms(2)
		self.pia.set(data)
		busy = self.isBusy()
		while busy:
			busy = self.isBusy()

	def isBusy(self):
		octet = self.readCmd()
		if (octet & 0x80) != 0:
			return True
		else:
			return False

	def readData(self):
		self.pia.set((self.backlight << BACKLIGHT) | (1 << RW_) | (1 << RS) | (1 << EN))
		time.sleep_ms(1)
		octet = self.pia.get()
		data = ((octet & (1 << DB7)) >> DB7) << 7
		data |= ((octet & (1 << DB6)) >> DB6) << 6
		data |= ((octet & (1 << DB5)) >> DB5) << 5
		data |= ((octet & (1 << DB4)) >> DB4) << 4
		self.pia.set((self.backlight << BACKLIGHT) | (1 << RW_) | (1 << RS))
		time.sleep_ms(2)
		self.pia.set((self.backlight << BACKLIGHT) | (1 << RW_) | (1 << RS) | (1 << EN))
		time.sleep_ms(1)
		octet = self.pia.get()
		data |= ((octet & (1 << DB7)) >> DB7) << 3
		data |= ((octet & (1 << DB6)) >> DB6) << 2
		data |= ((octet & (1 << DB5)) >> DB5) << 1
		data |= ((octet & (1 << DB4)) >> DB4)
		self.pia.set(self.backlight << BACKLIGHT)
		return data

	def readCmd(self):
		self.pia.set((self.backlight << BACKLIGHT) | (1 << RW_) | (1 << EN))
		time.sleep_ms(1)
		octet = self.pia.get()
		data = ((octet & (1 << DB7)) >> DB7) << 7
		data |= ((octet & (1 << DB6)) >> DB6) << 6
		data |= ((octet & (1 << DB5)) >> DB5) << 5
		data |= ((octet & (1 << DB4)) >> DB4) << 4
		self.pia.set((self.backlight << BACKLIGHT) | (1 << RW_))
		time.sleep_ms(2)
		self.pia.set((self.backlight << BACKLIGHT) | (1 << RW_) | (1 << EN))
		time.sleep_ms(1)
		octet = self.pia.get()
		data |= ((octet & (1 << DB7)) >> DB7) << 3
		data |= ((octet & (1 << DB6)) >> DB6) << 2
		data |= ((octet & (1 << DB5)) >> DB5) << 1
		data |= ((octet & (1 << DB4)) >> DB4)
		self.pia.set(self.backlight << BACKLIGHT)
		return data

	def write(self, data, rs, rw_, en):
		cmd = ((data & 0x0F) << DB) | (rw_ << RW_) | (rs << RS) | (en << EN)
		self.enableBit(cmd)

	def bitMode(self):
		return 0

	def nLine(self):
		return 1
