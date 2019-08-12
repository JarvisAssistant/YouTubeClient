from limitedmessagesocket.limited_message_socket import LimitedMessageSocket
from time import sleep
from ytplayer import YouTubePlayer
import json

class YouTubeClient:
	def __init__(self):
		self.server_address = ('18.220.151.1', 17777)
		self.socket = None
		self.player = YouTubePlayer()

	def _establish_connection(self):
		while True:
			try:
				self.socket = LimitedMessageSocket(self.server_address)
				self.socket.connect()
				break
			except Exception as e:
				print(str(e))
				print('Error connecting, trying again...')
				sleep(1)
	
	def _wait_command(self):
		try:
			command = self.socket.receive()
			parsed = self._parse_command(command)
			return parsed

		except ParseException as e:
			print('ParseException:' + str(e))
			return { 'error' : None }

		except Exception as e:
			print(str(e))
			self.socket.close()
			return None
	
	def _parse_command(self, command):
		command_args = command.split(' ')

		method = command_args[0]
		args = []
		if len(command_args) > 1:
			args = command_args[1:]

		args_correct, cargs = self._convert_args(args, None)

		if not args_correct:
			raise ParseException(method, args)

		return {
				'method' : method,
				'args' : cargs
			}
	
	def _convert_args(self, args, *converters):
		cargs = []
		args_correct = True

		for i in range(len(args)):
			arg = args[i]
			try:
				if i < len(converters) and converters[i]:
					cargs.append(converters[i](arg))
				else:
					cargs.append(arg)
			except:
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
			ret = self._execute(command)
			self.socket.send(json.dumps(ret))
	
	def _execute(self, command):
		method = command['method']
		args = command['args']

		if method == 'play' and len(args) == 1:
			self.player.play(args[0])
			return {}

		if method == 'stop':
			self.player.stop()
			return {}

		if method == 'pause':
			self.player.pause()
			return {}

		if method == 'resume':
			self.player.resume()
			return {}

class ParseException(Exception):
	def __init__(self, method, args):
		self.method = method
		self.args = args

	def __str__(self):
		return '%s with args %s' % (self.method, ''.join(self.args))

client = YouTubeClient()
client.serve_forever()



