import pafy, vlc

class YouTubePlayer:
	def __init__(self):
		self.video = None
		self.player = vlc.MediaPlayer()
		self.instance = self.player.get_instance()

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
		m = self.instance.media_new(self.video.getbestaudio().url)
		self.player.set_media(m)
		self.player.play()

	def stop(self):
		self.player.stop()

	def pause(self):
		self.player.set_pause(True)

	def resume(self):
		self.player.set_pause(False)
	
	def is_playing(self):
		return self.player.is_playing()
