class I2CException(Exception):
    def derive(self, excs):
        return I2CException(self.message, excs)
