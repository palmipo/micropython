
class NixieApp:
    def __init__(self):
        pass

    def init(self):
        raise NotImplementedError

    def krActivated(self):
        raise NotImplementedError

    def klActivated(self):
        raise NotImplementedError

    def kmActivated(self):
        raise NotImplementedError

    def rtcActivated(self):
        raise NotImplementedError

    def publisherRecev(self, topic, value):
        raise NotImplementedError