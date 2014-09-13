import ConfigParser
import datetime
import os
from plugins.battlefield4.bf4base import PluginBase

class ingame_admin(PluginBase):
	def __init__(self, rcon, log):
		PluginBase.__init__(self)
		self.rcon = rcon
		self.log = log

		self.adminlist = {}
		#self.readAdmins()	# Reads admins from a textfile
		self.admins = list()
		self.prefix = "!"

		self.public_commands = ["help", "status", "rules"]
		self.admin_commands = ["kick", "yell", "warn", "kick", "ban", "move"]
		
		self.prefix = ""
		self.welcome_message = ""
		self.server_rules = ""

		self.public_commands = ["help", "killed", "rules", "time"]
		self.admin_commands = ["adminhelp", "ban", "kick", "move", "say", "yell", "warn"]

		self.readConfig()

		#print player_info["ping"]
		#self.log.info("Location: {}".format(self.__location))

	# Old method for reading admins
	def readAdmins(self):
		#text_file = open(os.getcwd() + '\\plugins\\battlefield4\\ingame_admin\\admins.txt', 'r')
		__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
		text_file = open(os.path.join(__location__, 'admins.txt'))
		lines = text_file.readlines()

		admins = list()
		for line in lines:
			line = line.replace('\n', '').replace('\r', '')
			admins.append(line)
		self.log.info("Loaded admins: " + str(admins))
		
		self.adminlist = admins
		return admins	#returns a collection of names

	def readConfig(self):
		config = ConfigParser.ConfigParser()
		config_plugin = os.path.join('plugins', 'battlefield4', 'ingame_admin', 'plugin_config.ini')
		config.read(config_plugin)

		#	Wanted prefix for commands (recommended: !)
		################################################################
		try:
			self.prefix = config.get('plugin', 'command_prefix').strip()
		except:
			self.log.warn("No prefix was given in plugin_config.ini")
		################################################################

		#	A list of admins for the server
		################################################################
		try:
			self.adminlist = config.get('plugin', 'admins').split(' ')
		except:
			self.log.warn("No admins was given in plugin_config.ini")
		################################################################

		#	A string containing rules for the server
		################################################################
		try:
			self.welcome_message = config.get('plugin', 'rules')
		except:
			self.log.warn("No welcome message was specified in plugin_config.ini")
		################################################################

		self.log.debug("Plugin config has been loaded")
		self.log.info("Admins loaded: {}".format(self.adminlist))

	def getPlayers(self):
		players = self.rcon.listplayer()
		return players

	##########################################################
	#					Server Events   					 #
	##########################################################
	def on_connect(self, data):
		print data

		return

	def on_authenticated(self, data):
		print data
		return

	def on_join(self, data):
		print data
		return

	def on_leave(self, data):
		print data
		return

	def on_spawn(self, data):
		print data

		return

	def on_kill(self, data):

		return

	def on_chat(self, data):
		self.player = data[1]	# Grab playername
		self.message = data[2]	# Grab the message
		self.target = data[3]	# Grab to whom the message is for

		self.log.info('({}) {} - {}'.format(self.target, self.player, self.message))

		if self.player == 'Server':
			pass	#Do nothing?
		else:
			if self.message[0] == self.prefix: # Checks if given prefix is the same as config file
				# Tries to grab the command and clears out message from prefix and command
				self.command = self.message.split(' ')[0].lower().strip(self.prefix)
				self.message = self.message[(self.prefix + self.command).__len__() + 1:]

				if self.command in self.public_commands:
					public_cmd = getattr(self, 'public_' + self.command)
					public_cmd() 	# Run command for public methods
				elif self.command in self.admin_commands:
					if self.player in self.adminlist:
						admin_cmd = getattr(self, 'admin_' + self.command)
						admin_cmd()	# Run admin command
					else:
						self.rcon.say_message("Insufficient permissions, you're not an admin", self.player)
			#else:
				# Do something about bad language here?

		return

	def on_squadchange(self, data):
		print data
		return

	def on_teamchange(self, data):
		print data
		return

	def on_pb(self, data):
		print data
		return

	def on_maxplayerchange(self, data):
		print data
		return

	def on_levelload(self, data):
		#When a new map is loading, then just reload adminlist
		self.log.debug("Server is loading next map, tries to reload adminlist")
		self.readAdmins()

	def on_roundover(self, data):
		print data
		return

	def on_roundoverscore(self, data):
		print data
		return

	def on_roundoverplayers(self, data):
		print data
		return

	def on_unknown(self, data):
		print data
		return


	##########################################################
	#					Public Commands 					 #
	##########################################################
	def public_help(self):
		public = ', {}'.format(self.prefix).join(self.public_commands)
		self.rcon.say_message("Public Commands: {}".format(self.prefix) + public, self.player)

		# If player asking for help is an admin, then send a extra message with available commands
		if self.player in self.adminlist:
			admincmd = ', {}'.format(self.prefix).join(self.admin_commands)
			self.rcon.say_message("Admin Commands: {}".format(self.prefix) + admincmd, self.player)

	def public_killed(self):
		# Check who killed you lasttime and if it was a headshot (maybe more)
		self.rcon.say_message("This command is yet not implemented", self.player)

	def public_rules(self):
		self.rcon.say_message(self.server_rules, 'all')

	def public_time(self):
		date = datetime.datetime.now()
		self.rcon.say_message('Server time: {}'.format(date.strftime('%H:%M:%S')), 'all')

	##########################################################
	#					Admin Commands  					 #
	##########################################################
	def admin_adminhelp(self):
		if self.player in self.adminlist:
			admincmd = ', {}'.format(self.prefix).join(self.admin_commands)
			self.rcon.say_message("Admin Commands: {}".format(self.prefix) + admincmd, self.player)
		else:
			self.rcon.say_message("Insufficient permissions, you're not an admin", self.player)

	def admin_ban(self):
		self.rcon.say_message("This command is yet not implemented", self.player)

	def admin_kick(self):
		self.rcon.say_message("This command is yet not implemented", self.player)

	def admin_move(self):
		self.rcon.say_message("This command is yet not implemented", self.player)

	def admin_say(self):
		self.rcon.say_message("This command is yet not implemented", self.player)

	def admin_yell(self):
		self.rcon.say_message("This command is yet not implemented", self.player)

	def admin_warn(self):
		self.rcon.say_message("This command is yet not implemented", self.player)
