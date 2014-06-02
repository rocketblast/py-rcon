from plugins.battlefield.base import PluginBase

class ingame_admin(PluginBase):
	def __init__(self):
		PluginBase.__init__(self)

	@classmethod
	def on_chat(self, data):
		print "ett chattmeddelande varsegod"

	@classmethod
	def on_authenticated(self, data):
		print data

	@classmethod
	def on_squadchange(self, data):
		return
