class ModbusException(Exception):
    def derive(self, excs):
        return ModbusException(self.message, excs)
