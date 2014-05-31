# -*- coding: utf-8 -*-

# File: bf4-handler.py
# Description: Contains basic connection to a battlefield 4 server

import logging
import os
import socket
import sys
import threading

import helpers.EventHandler as LoggHandler
from battlefield import frostbite
from plugins import base_bf4plugin	#might need to work on the paths...

runningpath = os.path.dirname(__file__)

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
		# Logghandler.setup_logger(self.logName, '{}/logs/servers/{}'.format(runningpath, self.logName))
		# self.bf4log = logging.getLogger()
		# LoggHandler.setup_logger('py-rcon', r'{}/logs/py-rcon.log'.format(runningpath))
		# self.bf4log = logging.getLogger('py-rcon')
		# self.bf4log.info('Setup is ready for [{}:{}] - {}'.format(ip, port, name))