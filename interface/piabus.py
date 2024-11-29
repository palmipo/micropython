import time, machine, rp2

class PiaBus:
    def __init__(self):
        pass
    
    def set(self, value):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

