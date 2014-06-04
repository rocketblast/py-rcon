import ConfigParser
import datetime
import os

from plugins.battlefield.base import PluginBase

class daniel_admin(PluginBase):
	def __init__(self, rcon, log):
		PluginBase.__init__(self)
		self.rcon = rcon  # use this to communicate back to the server
		self.log = log    # use this if you want to log things
		
		# Default values
		self.admins = list()
		self.prefix = "!"
		self.public_commands = ["status", "rules", "date"]
		self.private_commands = ["kick", "yell"]

		# Read our config file
		self.read_config()

		self.log.info('daniel_admin Loaded')

	def read_config(self):
		config = ConfigParser.ConfigParser()
		config_plugin = os.path.join("plugins", "battlefield", "daniel_admin","config.ini")
		config.read(config_plugin)

		self.prefix = config.get('plugin', 'commandprefix').strip()
		self.admins = config.get('plugin', 'admins').split(' ')

	#########################################################
	# RCON EVENTS                                           #
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
		self.player = data[1] # Who is writing the message?
		self.message = data[2] # The message
		self.target = data[3] # All/Team/Player

		command = self.message.split(' ')[0].lower().strip(self.prefix) # Grab the command

		# Check for public commands
		if command in self.public_commands:
			command_run = getattr(self, 'command_' + command)
			command_run()

		# Check for private commands
		if command in self.private_commands:
			if self.player in self.admins:
				command_run = getattr(self, 'command_' + command)
				command_run()
			else:
				self.rcon.say_message('You are not allowed to run this command', self.player)

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
	# COMMANDS                                              #
	#########################################################

	# Public comands

	def command_rules(self):
		self.rcon.say_message('Our server rules lalalala', 'all')

	def command_date(self):
		date = datetime.date.today()
		self.rcon.say_message('Current date: {}'.format(date), self.player)

	def command_status(self):
		if self.player in self.admins:
			self.rcon.say_message('You are an admin :)', self.player)
		else:
			self.rcon.say_message('You are not an admin :(', self.player)

	# Private commands

	def command_kick(self):
		self.rcon.say_message('Kick player', 'all')

	def command_yell(self):
		print self.rcon.sendcommand(["admin.yell", self.message, "5", "all"])


#########################################################
