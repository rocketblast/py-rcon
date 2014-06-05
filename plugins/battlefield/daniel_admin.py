import ConfigParser
import datetime
import os

from plugins.battlefield.base import PluginBase

# A basic admin plugin for py-rcon

class daniel_admin(PluginBase):
	def __init__(self, rcon, log):
		PluginBase.__init__(self)
		self.rcon = rcon  # use this to communicate back to the server
		self.log = log    # use this if you want to log things
		
		# Default values
		self.admins = list()
		self.prefix = "!"
		self.welcome_message = ""
		self.rules_message = ""
		self.help_message = ""

		self.public_commands = ["help", "status", "rules", "time"]
		self.private_commands = ["say", "yell", "kick"]

		# Read our config file
		self.read_config()

		self.log.info('{} loaded succesfully'.format(__name__))

	def read_config(self):
		config = ConfigParser.ConfigParser()
		config_plugin = os.path.join("plugins", "battlefield", "daniel_admin","config.ini")
		config.read(config_plugin)

		# Try to load our settings. If something goes wrong, it will pass and use the defaults in the class instead
		try:
			self.prefix = config.get('plugin', 'commandprefix').strip()
			self.admins = config.get('plugin', 'admins').split(' ')
			self.welcome_message = config.get('plugin', 'welcome')
			self.rules_message = config.get('plugin', 'rules')
			self.help_message = config.get('plugin', 'help')
		except:
			pass

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
		self.target = data[3] # All/Team/Squad/Player

		command = self.message.split(' ')[0].lower().strip(self.prefix) # Grab the command
		self.message_clean = self.message[(self.prefix + command).__len__() + 1:] # Message without the command

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

	def command_help(self):
		if self.help_message:
			self.rcon.say_message(self.help_message, 'all')

		public_commands = ', {}'.format(self.prefix).join(self.public_commands)
		self.rcon.say_message("Commands: {}".format(self.prefix) + public_commands, 'all')

		# Show additional admin commands if player is an admin
		if self.player in self.admins:
			private_commands = ', {}'.format(self.prefix).join(self.private_commands)
			self.rcon.say_message("Admin commands: {}".format(self.prefix) + private_commands, self.player)

	def command_rules(self):
		self.rcon.say_message(self.rules_message, 'all')

	def command_time(self):
		date = datetime.datetime.now()
		self.rcon.say_message('Server time: {}'.format(date.strftime('%H:%M:%S')), "all")

	def command_status(self):
		if self.player in self.admins:
			self.rcon.say_message('You are an admin :)', self.player)
		else:
			self.rcon.say_message('You are not an admin :(', self.player)

	# Private commands

	def command_say(self):
		self.rcon.say_message(self.message_clean, 'all')

	def command_yell(self):
		self.rcon.sendcommand(["admin.yell", self.message_clean, "8", "all"])

	def command_kick(self):
		if not self.message_clean:
			self.rcon.say_message('You have to specify a player to kick', self.player)
			return

		_temp = self.message_clean.split(' ')
		target = _temp[0]

		if len(_temp) > 1:
			_temp.pop(0)
			reason = ' '.join(_temp)
		else:
			reason = ''

		kick = self.rcon.kickplayer(target, reason)
		if kick[0] == 'InvalidPlayerName':
			self.rcon.say_message('Could not find player {}'.format(target), self.player)
		elif kick[0] == 'OK':
			self.rcon.say_message('Player {} has been kicked. Reason: {}'.format(target, reason), 'all')


#########################################################
