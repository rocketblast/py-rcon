from plugins.battlefield.base import PluginBase

class ingame_admin(PluginBase):
	def __init__(self):
		PluginBase.__init__(self)

	def on_chat(self, data):
		print data

	def on_authenticated(self, data):
		print data

	def on_squadChange(self, data):
		return