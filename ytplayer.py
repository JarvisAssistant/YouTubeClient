import pafy, vlc
from multiprocessing.managers import BaseManager
from threading import RLock

class YouTubePlayer(BaseManager):
	def __init__(self):
		super().__init__(address=('', 7777), authkey=b'password')
		self.lock = RLock()
		self.video = None
		self.player = vlc.MediaPlayer()
		self.instance = self.player.get_instance()
	
	def init(self):
		self.register('play', self.play)
		self.register('stop', self.stop)
		self.register('pause', self.pause)
		self.register('resume', self.resume)
		self.register('is_playing', self.is_playing)

	def info(self):
		info = {
				'artists' : [],
				'track' : 'Unknown'
			}

		if self.video:
			info['artists'].append(self.video.author)
			info['track'] = self.video.title

		return info

	def play(self, id):
		self.video = pafy.new(id)
		with self.lock:
			m = self.instance.media_new(self.video.getbestaudio().url)
			self.player.set_media(m)
			self.player.play()

	def stop(self):
		with self.lock:
			self.player.stop()

	def pause(self):
		with self.lock:
			self.player.set_pause(True)

	def resume(self):
		with self.lock:
			self.player.set_pause(False)
	
	def is_playing(self):
		return self.player.is_playing()
