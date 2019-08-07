from limitedmessagesocket.limited_message_socket import LimitedMessageSocket
from threading import sleep

class YouTubeClient:
	def __init__(self):
		self.socket = Socket(('https://api.lucaduran.com', 17777))

	def _establish_connection(self):
		while True:
			try:
				self.socket.connect()
				break
			except:
				sleep(5)
	
	def _wait_command(self):
		try:
			command = self.socket.recv(1024)
			parsed = self._parse_command(command)
			return parsed
		finally:
			self.socket.close()
			return None
	
	def _parse_command(self, command):
		pass
	
	def serve_forever(self):
		while True:
			print('Establishing connection...')
			self.establish_connection()
			print('Connection established')
			print('Waiting for commands')
			self._wait_commands()
			print('Connection lost')
	
	def _wait_commands(self):
		while True:
			command = self._wait_command()
			if not command: return
			self._execute(command)
	
	def _execute(self, command):
		pass

