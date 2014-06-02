from plugins.battlefield.base import PluginBase

class sample_plugin(PluginBase):
	def __init__(self):
		PluginBase.__init__(self)

	@classmethod
	def on_connect(self, data):
		return

	@classmethod
	def on_authenticated(self, data):
		return

	@classmethod
	def on_join(self, data):
		return

	@classmethod
	def on_leave(self, data):
		return

	@classmethod
	def on_spawn(self, data):
		return

	@classmethod
	def on_kill(self, data):
		return

	@classmethod
	def on_chat(self, data):
		return

	@classmethod
	def on_squadchange(self, data):
		return

	@classmethod
	def on_teamchange(self, data):
		return

	@classmethod
	def on_pb(self, data):
		return

	@classmethod
	def on_maxplayerchange(self, data):
		return

	@classmethod
	def on_levelload(self, data):
		return

	@classmethod
	def on_roundover(self, data):
		return

	@classmethod
	def on_roundoverscore(self, data):
		return

	@classmethod
	def on_roundoverplayers(self, data):
		return

	@classmethod
	def on_unknown(self, data):
		return
