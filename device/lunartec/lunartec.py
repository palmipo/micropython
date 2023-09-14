from uartbus import UartBus

class Lunartec:
	def __init__(self, id, uart):
        self._uart = uart
		self._usart.setConfig(B9600, 8, 'N', 1, 1)
	
        std::stringstream cmd;
        cmd << std::string("<ID><");
        cmd << std::setw(2) << std::setfill('0') << std::setbase(10) << (_id & 0xFF);
        cmd << std::string("><E>");
		self._usart.send(cmd)

	def set_time(self):
		std::stringstream data;
		data << std::string("<SC>");
		data << std::setw(2) << std::setfill('0') << t->tm_year-100;
		data << std::setw(2) << std::setfill('0') << t->tm_wday;
		data << std::setw(2) << std::setfill('0') << t->tm_mon+1;
		data << std::setw(2) << std::setfill('0') << t->tm_mday;
		data << std::setw(2) << std::setfill('0') << t->tm_hour;
		data << std::setw(2) << std::setfill('0') << t->tm_min;
		data << std::setw(2) << std::setfill('0') << t->tm_sec;
		self.write(data);

	def send(self, text, page, speed):
		std::stringstream data;
		data << std::string("<L1><P");
		data << page;
		data << std::string("><FA><M");
		data << speed;
		data << std::string("><WA><FA>");

		if (page == 'A'):
			data << text.substr(0, 80);
		else if (page == 'B'):
			data << text.substr(0, 420);
		else:
			throw RS232Exception(__FILE__, __LINE__, "Lunartec::send()");
		self.write(data);

	def write(self, data):
		std::stringstream cmd;
		cmd << std::string("<ID");
		cmd << std::setw(2) << std::setfill('0') << std::setbase(10) << _id;
		cmd << std::string(">");
		cmd << data;
		cmd << std::setw(2) << std::setfill('0') << std::setbase(16) << (int)check_sum(data);
		cmd << std::string("<E>");
		self._usart->write((uint8_t *)cmd.str().c_str(), cmd.str().length());

	def check_sum(self, text):
		uint8_t cs = 0;

		for c in text:
			cs ^= c

		return cs;
