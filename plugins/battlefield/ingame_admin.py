from plugins.battlefield.base import PluginBase

class ingame_admin(PluginBase):
	def __init__(self, rcon, log):
		self.rcon = rcon
		self.log = log
		PluginBase.__init__(self)

	def on_connect(self, data):
		return

	def on_authenticated(self, data):
		return

	def on_join(self, data):
		return

	def on_leave(self, data):
		return

	def on_spawn(self, data):
		return

	def on_kill(self, data):
		return

	def on_chat(self, data):
		print data
		#example on how only I can kick someone on the server
		if data[1] == 'asabla':
			player = data[2].split(' ')[1]
			reason = data[2].split(' ')[2]
			self.rcon.kickplayer(player, reason)

	def on_squadchange(self, data):
		return

	def on_teamchange(self, data):
		return

	def on_pb(self, data):
		return

	def on_maxplayerchange(self, data):
		return

	def on_levelload(self, data):
		return

	def on_roundover(self, data):
		return

	def on_roundoverscore(self, data):
		return

	def on_roundoverplayers(self, data):
		return

	def on_unknown(self, data):
		return
