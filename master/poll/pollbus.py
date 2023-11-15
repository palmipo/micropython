import select

class PollClnt:
    def cb_timeout(self):
        raise NotImplementedError
    
    def cb_pollin(self):
        raise NotImplementedError
    
    def cb_pollout(self):
        raise NotImplementedError
    
    def cb_pollhup(self):
        raise NotImplementedError
    
    def cb_pollerr(self):
        raise NotImplementedError
    
class Poll:
	def __init__(self):
		self.poll = select.poll()

	def add(self, obj):
		self.poll.register(obj, select.POLLIN)

    def remove(self, obj):
        self.poll.unregister(obj)

	def run(self):
		try:
			events = self.poll.poll(20)
			if not events:
				self.cb_timeout()

			else:
				for (fd, event) in events:
                    if (event == select.POLLIN):
                        obj.cb_pollin()

                    elif (event == select.POLLOUT):
                        obj.cb_pollout()

                    elif (event == select.POLLHUP):
                        obj.cb_pollhup()

                    elif (event == select.POLLERR):
                        obj.cb_pollerr()

		except OSError:
			print('erreur poll')

