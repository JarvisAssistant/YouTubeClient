from limitedmessagesocket.limited_message_socket import LimitedMessageSocket
from time import sleep

class YouTubeClient:
	def __init__(self):
		self.socket = LimitedMessageSocket(('https://api.lucaduran.com', 17777))

	def _establish_connection(self):
		while True:
			try:
				self.socket.connect()
				break
			except:
				sleep(5)
	
	def _wait_command(self):
		try:
			command = self.socket.receive()
			parsed = self._parse_command(command)
			return parsed

		except ParseException as e:
			print(str(e))
			return { 'error' : None }

		except Exception as e:
			print(str(e))
			self.socket.close()
			return None
	
	def _parse_command(self, command):
		command_args =  command.split(' ')

		method = command[0]
		args = []
		if len(command_args) > 1:
			args = command_args[1:]

		args_correct, cargs = self._convert_args(args, str)

		if not args_correct:
			raise ParseException(method, args)

		return {
				'method' : 'play',
				'args' : cargs
			}
	
	def _convert_args(args, *converters):
		cargs = []
		args_correct = True

		for i in range(len(args)):
			arg = args[i]
			conv = converters[i]
			try:
				cargs.append(conv(arg))
			finally:
				args_correct = False
				break

		return args_correct, cargs

	def serve_forever(self):
		while True:
			print('Establishing connection...')
			self._establish_connection()
			print('Connection established')

			print('Waiting for commands')
			self._wait_commands()
			print('Connection lost')
	
	def _wait_commands(self):
		while True:
			command = self._wait_command()
			if not command: return
			if 'error' in command:
				print('Error in parsing command')
				continue
			self._execute(command)
	
	def _execute(self, command):
		print(command)

class ParseException(Exception):
	def __init__(self, method, args):
		self.method = method
		self.args = args

	def __str__(self):
		return '%s with args %s' % (self.method, ''.join(self.args))

client = YouTubeClient()
client.serve_forever()



