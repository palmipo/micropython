import sys
sys.path.insert(0, '../interface')
sys.path.insert(0, '../device/elexol')
from elexol import Elexol

io = Elexol("192.168.20.1")
print(io.identifyIO24Units())
# io.resetModule()
# io.writeEnableEeprom()
# io.writeEepromWord(5, 0xffff)
# for i in range(5,29):
#     print(i, hex(io.readEepromWord(i)))
io.setDirectionPort(0, 0xff)
io.setDirectionPort(1, 0)
io.setDirectionPort(2, 0)
print(hex(io.readPort(0)))
io.writePort(1, 0)
io.writePort(2, 0)
io.deconnexion()

