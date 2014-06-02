from plugins.battlefield.base import PluginBase

class PluginAdmin(PluginBase):
	def __init__(self):
		PluginBase.__init__(self)

	def on_chat(self, data):
		print data