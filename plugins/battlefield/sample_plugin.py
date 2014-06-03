from plugins.battlefield.base import PluginBase

class sample_plugin(PluginBase):
	# Default constructor for all plugins, don't mess with
	# this unless you know what you are doing
	def __init__(self, rcon, log):
		self.rcon = rcon  # use this to communicate back to the server
		self.log = log    # use this if you want to log things
		PluginBase.__init__(self)

#########################################################
# Rcon events, by default you can't send anything back  #
# You can't either remove any of these, they have to    #
# be in your plugin. If you don't want to do anything   #
# on a specific event, just leave it be.                #   
#########################################################
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
		return

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
#########################################################
