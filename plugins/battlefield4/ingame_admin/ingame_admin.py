import os
from plugins.battlefield4.bf4base import PluginBase
import csv

class ingame_admin(PluginBase):
	adminlist = {}

	def __init__(self, rcon, log):
		PluginBase.__init__(self)

		self.rcon = rcon
		self.log = log
		self.readAdmins()

		p = self.rcon.listplayer()
		p.pop(0)
		p.pop(0)
		reader = csv.reader(p)
		rows = [row for row in reader if row]
		headings = rows[0]

		player_info = {}
		for row in rows[1:]:
			for col_header, data_column in zip(headings, row):
				player_info.setdefault(col_header, []).append(data_column)
		
		print player_info["ping"]

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
		#print data
		#print self.rcon.matchplayer('derp')

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
		self.log.debug("Server is loading next map, tries to reload adminlist")
		self.readAdmins()

	def on_roundover(self, data):
		return

	def on_roundoverscore(self, data):
		return

	def on_roundoverplayers(self, data):
		return

	def on_unknown(self, data):
		return
