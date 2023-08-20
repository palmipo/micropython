import sys
sys.path.insert(0, '../interface')
sys.path.insert(0, '../master/elexol')
sys.path.insert(0, '../device/elexol')
from elexol import Elexol
from elexolrelay import ElexolRelay

io = Elexol("192.168.20.1")
print(io.identifyIO24Units())
io.setDirectionPort(0, 0xff)
io.setDirectionPort(1, 0)
io.setDirectionPort(2, 0)

print(hex(io.readPort(0)))

relay = ElexolRelay(io, 2)
relay.momentary(2)
io.deconnexion()

