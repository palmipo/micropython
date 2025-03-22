import select

class PollStreamException(Exception):
    pass

class PollStream:
    def __init__(self):
        self.poule = select.poll()
        self.lst = []
    
    def register(self, flux):
        self.poule.register(flux, select.POLLIN | select.POLLERR | select.POLLHUP)
        self.lst.append(flux)

    def unregister(self, flux):
        self.poule.unregister(flux)
        self.lst.remove(flux)
    
    def scrute(self, timeout):
        events = self.poule.poll(timeout)
        if events == []:
            raise PollStreamException('poll vide')

        for (fd, event) in events:
            if event == select.POLLIN:
                return 1, fd
            
            elif event == select.POLLERR or event == select.POLLHUP:
                return -1, fd

            else:
                return 0, None
