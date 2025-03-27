import time

class PiaBus:
    def __init__(self):
        pass
    
    def send(self, value):
        raise NotImplementedError

    def recv(self):
        raise NotImplementedError

