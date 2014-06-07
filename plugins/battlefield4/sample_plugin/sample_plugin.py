'''
	This is a an example on how plugins to py-rcon look like. There is 
	a few things that needs to be in this file in order for this to work.

	* The import of PluginBase is needed in order for fetching events

	* Constructor, even if you don't plan on using rcon or log they need
	  to be in the plugin (for now). In the future you might be able to create 
	  plugins that only listens etc.

	* List of already defined events (all methods starting with on_****).
	  For now you must be able to handle all events, in the future we might 
	  remove this dependency in order to make it easier for you.

	The mentioned list above this are things that must be in every plugin right
	now. In the future we might strip down required code in order to make your
	plugin to work.

	If you are planning on using the rcon layer there are a few things you need to 
	know. You don't have to write your own methods for sending and receiving data.
	Nor do you need to make basic methods for basic things, like kicking players 
	and similar. Basic already available methods are:

	* Serverinfo, method: self.rcon.serverinfo()
	  Returns serverinfo 

	* Version, method: self.rcon.version()
	  Returns version

	* Admin eventsenabled, method: self.rcon.admin_eventsenabled(True)
	  Which activates events for current connection. By default this is already
	  set to True.

	* Say message, method: self.rcon.say_message('my message', 'all')
	  Send chatmessages with this method, all can be changed to either
	  1 or 2 (depending on team). Sending a chatmessage to a specific player
	  is not yet implemented.

	* Yell message, method: self.rcon.yell_message('my message', 20, 'all')
	  Works simliar to say message but you can also specify a duration

	* Kick player, method: self.rcon.kickplayer('playername', 'reason')
	  Kicks out matching player with given reason. Remember, playername has 
	  to be a perfect match. Otherwise nothing will happen.

	  Suggestion: List all players and try to match as many characters you can
	  and then kick the player with most matches.

	* List players, method: self.rcon.listplayer()
	  Returns a list of all connected players

	* Add VIP, method: self.rcon.addvip('playername')
	  Adds a given player to the viplist, when you call this method it will 
	  also save the list. Otherwise you need to save it by your self.

	* Remove VIP, method: self.rcon.removevip('playername')
	  Removes a given player from the viplist, when you call this method it 
	  will also save the list. Otherwise you need to save it by your self.

	* List VIPlist, method: self.rcon.listvip()
	  Returns a list of all players in the VIPlist.

	* Get ping, method: self.rcon.getping('playername')
	  Gets current ping for a given player on the server. It won't work 
	  unless the player is connected to current server.

	* Restart round, method: self.rcon.restartround()
	  Will restart current round.

	* Next map, method: self.rcon.nextmap()
	  Will force the server to rotate to the next map in the list.

	* Shutdown server, method: self.rcon.shutdown()
	  Will try to shutdown current server.
'''

from plugins.battlefield4.bf4base import BF4PluginBase

class sample_plugin(PluginBase):
	# Default constructor for all plugins, don't mess with
	# this unless you know what you are doing
	def __init__(self, rcon, log):
		self.rcon = rcon  # use this to communicate back to the server
		self.log = log    # use this if you want to log things
		PluginBase.__init__(self)

	#########################################################
	# RCON EVENTS                                           #
	# You can't remove any of these, they have to be in     #
	# your plugin. If you don't want to do anything on a    #
	# specific event, just leave it be.                     #   
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
