import os
from plugins.battlefield.base import PluginBase

class ingame_admin(PluginBase):
	adminlist = {}

	def __init__(self, rcon, log):
		PluginBase.__init__(self)
		self.readAdmins()
		self.rcon = rcon
		self.log = log

	def readAdmins(self):
		text_file = open(os.getcwd() + '\\plugins\\battlefield\\admins.txt', 'r')
		lines = text_file.readlines()

		admins = list()
		for line in lines:
			line = line.replace('\n', '').replace('\r', '')
			admins.append(line)
		print "Loaded admins: " + str(admins)

		self.adminlist = admins
		return admins	#returns a collection of names

	def getPlayers(self):
		players = self.rcon.listplayer()
		return players

	# Events
	#############################
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
		#example on how only I can kick someone on the server
		player = data[1]
		message = data[2]
		print data

		if player == 'Server':
			pass	#Do nothing?
		else:
			for admin in self.adminlist:
				if player == str(admin):
					print "An admin is saying something"
					if message.split(' ')[0] == '!kick':
						player = message.split(' ')[1]
						reason = message.split(' ')[2]
						self.rcon.kickplayer(player, reason)

	def on_squadchange(self, data):
		return

	def on_teamchange(self, data):
		return

	def on_pb(self, data):
		return

	def on_maxplayerchange(self, data):
		return

	def on_levelload(self, data):
		#When a new map is loading, then just reload adminlist
		self.readAdmins()

	def on_roundover(self, data):
		return

	def on_roundoverscore(self, data):
		return

	def on_roundoverplayers(self, data):
		return

	def on_unknown(self, data):
		return
