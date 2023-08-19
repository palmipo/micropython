class RelayBus:
    
    def read(self, voie):
        raise NotImplementedError

    def open(self, voie):
        raise NotImplementedError

    def close(self, voie):
        raise NotImplementedError

    def toggle(self, voie):
        raise NotImplementedError

    def latch(self, voie):
        raise NotImplementedError

    def momentary(self, voie):
        raise NotImplementedError

    def delay(self, voie, tempo):
        raise NotImplementedError
