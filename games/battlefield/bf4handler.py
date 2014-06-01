# -*- coding: utf-8 -*-

# File: bf4-handler.py
# Description: Contains basic connection to a battlefield 4 server

import logging
import os
import socket
import sys
import threading

from helpers.EventHandler import LoggHandler
from games.battlefield import frostbite
#from plugins.battlefield.ingame_admin.py import 

runningpath = os.getcwd()

class BF4Handler(threading.Thread):
	bf4log = None

	def __init__(self, name, ip, port, password, plugins=None):
		threading.Thread.__init__(self)	#initilize the stuff!

		self.serverName = name
		self.serverIp = ip
		self.serverPort = port
		self.serverPassword = password
		self.serverPlugins = plugins
		self.serverLoadedPlugins = list()
		self.socket = None

		self.logName = 'bf4-{}'.format(name)
		self.bf4log = LoggHandler.setup_logger(self.logName, '{}/logs/servers/{}.log'.format(runningpath, self.logName))
		self.bf4log.info('Setup is ready for [{}:{}] - {}'.format(ip, port, name))

	@classmethod
	def run(self):
		if self.connect():
			self.bf4log.info('Connected [{}:{}] <{}>'.format(self.serverIp, self.serverPort, self.serverName))
			
			#load plugins for this instance
		else:
			self.bf4log.warn('Unable to establish a connection to [{}:{}] <{}>'.format(self.serverIp, self.serverPort, self.serverName))

	def events(self, plugin, event, data):
		evts = {
			#player events
			'player.onAuthenticated': plugin.on_authenticated,
			'player.onJoin': plugin.on_join,
			'player.onLeave': plugin.on_leave,
			'player.onSpawn': plugin.on_spawn,
			'player.onKill': plugin.on_kill,
			'player.onChat': plugin.on_chat,
			'player.onConnect': plugin.on_connect,
			'player.onSquadChange': plugin.on_squadchange,
			'player.onTeamChange': plugin.on_teamchange,

			#punkbuster events
			'punkBuster.onMessage': plugin.on_pb,

			#server events
			'server.onMaxPlayerCountChange': plugin.on_maxplayerchange,
			'server.onLevelLoaded': plugin.on_levelload,
			'server.onRoundOver': plugin.on_roundover,
			'server.onRoundOverPlayers': plugin.on_roundoverplayers,
			'server.onRoundOverTeamScores': plugin.on_roundoverscore,
		}
		return evts.get(event, plugin.on_unknown)(data)

	#def load_plugins(self):