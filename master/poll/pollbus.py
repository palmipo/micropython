import select

class PollClnt:
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

	def run(self, timeout):
		try:
			events = self.poll.poll(timeout)
			if not events:
				return 0

			else:
				for (fd, event) in events:
                    if (event == select.POLLIN):
                        if obj.cb_pollin != None:
                            obj.cb_pollin()

                    elif (event == select.POLLOUT):
                        if obj.cb_pollout != None:
                            obj.cb_pollout()

                    elif (event == select.POLLHUP):
                        if obj.cb_pollhup != None:
                            obj.cb_pollhup()

                    elif (event == select.POLLERR):
                        if obj.cb_pollerr != None:
                            obj.cb_pollerr()
                return 1

		except OSError:
			print('erreur poll')
            return -1

