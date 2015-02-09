import ConfigParser
import datetime
import os

from pyrcon.plugins.battlefield4.bf4base import PluginBase

# A basic admin plugin for py-rcon

# Todo
# - More logging
# - Better config loading
# - Move players in game modes more than 2 teams

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
		self.private_commands = ["say", "yell", "warn", "kick", "ban", "move"]

		# Read our config file
		self.read_config()

		self.log.info('{} loaded succesfully'.format(__name__))

	def read_config(self):
		config = ConfigParser.ConfigParser()
		config_plugin = os.path.join("plugins", "battlefield4", "daniel_admin","plugin.ini")
		config.read(config_plugin)

		# Try to load our settings. If something goes wrong, it will pass and use the defaults in the class instead
		# This could probably be done more beautiful!
		try:
			self.prefix = config.get('plugin', 'commandprefix').strip()
		except:
			pass

		try:
			self.admins = config.get('plugin', 'admins').split(' ')
		except:
			pass

		try:
			self.rules_message = config.get('plugin', 'rules')
		except:
			pass

		try:
			self.help_message = config.get('plugin', 'help')
		except:
			pass

		self.log.info('Admins loaded: {}'.format(self.admins))

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
		# Re-read our config file on map change
		self.read_config()
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
		if not self.message_clean:
			self.rcon.say_message('You have to enter a message', self.player)
			return

		self.rcon.say_message(self.message_clean, 'all')

	def command_yell(self):
		if not self.message_clean:
			self.rcon.say_message('You have to enter a message', self.player)
			return

		self.rcon.sendcommand(["admin.yell", self.message_clean, "8", "all"])

	def command_warn(self):
		if not self.message_clean:
			self.rcon.say_message('You have to specify a player to warn', self.player)
			return

		_temp = self.message_clean.split(' ')
		target = _temp[0]

		if len(_temp) < 2:
			self.rcon.say_message('You have to specify a reason', self.player)
			return

		_temp.pop(0)
		reason = ' '.join(_temp)

		warn = self.rcon.sendcommand(["admin.yell", "Warning: {}".format(reason), "10", "player", target])
		if warn[0] == 'PlayerNotFound':
			self.rcon.say_message('Could not find player {}'.format(target), self.player)
		elif warn[0] == 'MessageIsTooLong':
			self.rcon.say_message('Message is too long', self.player)
		elif warn[0] == 'OK':
			self.rcon.sendcommand(["admin.killPlayer", target])
			self.rcon.say_message('Warning: {}'.format(reason), target)
			self.rcon.say_message('Sent warning to {}'.format(target), self.player)

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

	def command_ban(self):
		if not self.message_clean:
			self.rcon.say_message('You have to specify a player to ban', self.player)
			return

		_temp = self.message_clean.split(' ')
		target = _temp[0]

		if len(_temp) < 2:
			self.rcon.say_message('You have to specify a ban duration', self.player)
			return
		else:
			duration = _temp[1]
		
		# Convert input duration to seconds
		if duration.endswith('h'):
			duration = int(duration[:-1]) * 60 * 60
		elif duration.endswith('d'):
			duration = int(duration[:-1]) * 24 * 60 * 60
		elif duration.endswith('w'):
			duration = int(duration[:-1]) * 7 * 24 * 60 * 60
		elif duration.startswith('perm'):
			duration = "perm"
		else:
			self.rcon.say_message('Invalid ban duration', self.player)
			return

		if len(_temp) < 3:
			self.rcon.say_message('You have to specify a ban reason', self.player)
			return
		else:
			_temp.pop(0)
			_temp.pop(0)
			reason = ' '.join(_temp)

		# Get player (if online)
		player = self.get_player(target)
		if not player:
			self.rcon.say_message('Could not find player {}'.format(target), self.player)
			return

		if isinstance(duration, int):
			ban = self.rcon.sendcommand(["banList.add", "guid", player['ea_guid'], 'seconds', duration, reason])
		else:
			ban = self.rcon.sendcommand(["banList.add", "guid", player['ea_guid'], duration, reason])

		if ban[0] == "OK":
			self.rcon.say_message('Player {} has been banned. Reason: {}'.format(target, reason), 'all')
			self.rcon.sendcommand(["banList.save"])

		return

	def command_move(self):
		if not self.message_clean:
			self.rcon.say_message('You have to specify a player to move', self.player)
			return

		target = self.message_clean

		# Get player (if online)
		player = self.get_player(target)
		if not player:
			self.rcon.say_message('Could not find player {}'.format(target), self.player)
			return

		team = int(player['team'])

		# Move player - Only work with modes that have 2 teams right now
		if team == 1:
			move_to = 2
		elif team == 2:
			move_to = 1
		else:
			self.rcon.say_message('Could not move player. Sorry.', self.player)
			return

		# We don't get a response code back from "admin.movePlayer" =/
		move = self.rcon.sendcommand(["admin.movePlayer", target, move_to, 0, True])
		self.rcon.sendcommand(["admin.yell", "You have been moved to the other team", "8", "player", target])
		self.rcon.say_message('You have been moved to the other team', target)

		return


	# Other functions

	def get_player(self, player):
		playerlist = self.get_playerlist(details=True)

		if player in playerlist:
			return playerlist[player]
		else:
			return False


	def get_playerlist(self, details=False):
		playerlist = self.rcon.listplayer()

		# Remove 14 first columns - we don't need them
		del playerlist[0:13]

		# Split list for each player
		playerlist=[playerlist[x:x+10] for x in xrange(0, len(playerlist), 10)]
		players = {}
		test = {}

		for player in playerlist:
			if details == False:
				players.append(player[0])
			else:
				playerinfo = {
					'name': player[0],
					'ea_guid': player[1],
					'team': player[2],
					'squad': player[3],
					'kills': player[4],
					'deaths': player[5],
					'score': player[6],
					'rank': player[7],
					'ping': player[8],
					'type': player[9],
				}

				#players.insert(len(players), playerinfo)
				players[player[0]] = playerinfo

		return players



#########################################################
