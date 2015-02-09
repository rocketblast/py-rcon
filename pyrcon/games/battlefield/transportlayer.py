# -*- coding: utf-8 -*-

# File: transportlayer.py
# Description: Is a subclass for handling battlefield connections

import socket
import sys

from pyrcon.games import SocketHandler
from frostbite import Frostbite

class BFRCON(SocketHandler):
	def __init__(self, ip, port, password, log):
		self.serverIp = ip
		self.serverPort = port
		self.serverPassword = password
		self.socket = None

		SocketHandler.__init__(self, ip, port, log)

	def receive_packet(self, socket=None, receiveBuffer=""):
		while True:
			#Fills the buffer until it's full or complete
			while not Frostbite.containsCompletePacket(receiveBuffer):
				receiveBuffer += self.socket.recv(4096)

			packetSize = Frostbite.DecodeInt32(receiveBuffer[4:8])
			packet = receiveBuffer[0:packetSize]
			receiveBuffer = receiveBuffer[packetSize:len(receiveBuffer)]

			# This code needs to be cleared out a bit, so it's more obvious 
			# when a response is received or expected
			if socket == None:	#waiting for events
				[isFromServer, isResponse, sequence, words] = Frostbite.DecodePacket(packet)
				return words
			elif socket:	#waiting for a response
				return [packet, receiveBuffer]
			else:
				self.log.error('Unable to handle received packet!')
				return None

	def sendcommand(self, data):
		receiveBuffer = ""
		getRequest = Frostbite.EncodeClientRequest(data)
		self.socket.send(getRequest)

		[getResponse, receiveBuffer] = self.receive_packet(self.socket, receiveBuffer)
		[isFromServer, isResponse, sequence, words] = Frostbite.DecodePacket(getResponse)

		self.log.debug('[{}:{}] Sending: {}'.format(self.serverIp, self.serverPort, data))

		return words

	def send_packet(self, data):
		receiveBuffer = ""
		getRequest = Frostbite.EncodeClientRequest(data)
		self.socket.send(getRequest)

		[getResponse, receiveBuffer] = self.receive_packet(self.socket, receiveBuffer)
		[isFromServer, isResponse, sequence, words] = Frostbite.DecodePacket(getResponse)

		self.log.debug('[{}:{}] Sending: {}'.format(self.serverIp, self.serverPort, data))

		return words

	def login(self):
		login = self.send_packet(["login.hashed"])
		passwordHash = Frostbite.generatePasswordHash(login[1].decode("hex"), self.serverPassword)
		passwordHashHexString = passwordHash.encode("hex").upper()
		response = self.send_packet(["login.hashed", passwordHashHexString])

		if response[0] != "OK":
			self.log.error('[{}:{}] Wrong RCON password. Exiting.'.format(self.serverIp, self.serverPort))
			sys.exit()
		elif response[0] == "OK":
			self.log.info('[{}:{}] is now logged on'.format(self.serverIp, self.serverPort))
		else:
			self.log.warn('Something went wrong, response: {}'.format(response))

		return response

	def logout(self):
		response = self.send_packet(["logout"])
		return response

	def serverinfo(self):
		response = self.send_packet(["serverinfo"])
		return response

	def version(self):
		response = self.send_packet(["version"])
		return response

	def currentlevel(self):
		response = self.send_packet(["currentLevel"])
		return response

	def admin_eventsenabled(self, status):
		response = self.send_packet(["admin.eventsEnabled", status])
		return response

	def say_message(self, message, to):
		if to == 'all':
			response = self.send_packet(["admin.say", message, "all"])
		elif to == '1' or to == '2':
			response = self.send_packet(["admin.say", message, "team", to])
		else:	#Sends message to a specific player
			response = self.send_packet(["admin.say", message, "player", to])

		return response

	def yell_message(self, message, duration, to):
		if to == 'all':
			response = self.send_packet(["admin.yell", message, duration, "all"])
		else: #sends message to a specific player
			response = self.send_packet(["admin.yell", message, duration, "player", to])
		return response

	def kickplayer(self, player, reason=''):
		response = self.send_packet(["admin.kickPlayer", player, reason])
		return response

	def listplayer(self):
		playerlist = self.send_packet(["admin.listPLayers", "all"])
		return playerlist

	def addvip(self, player):
		response = self.send_packet(["reservedSlotsList.add", player])
		self.send_packet(["reservedSlotsList.save"])
		return response

	def listvip(self):
		viplist = self.send_packet(["reservedSlotsList.list"])
		return viplist

	def removevip(self, player):
		response = self.send_packet(["response.remove", player])
		self.send_packet(["reservedSlotsList.save"])
		return response

	def getping(self, player):
		response = self.send_packet(["player.ping", player])
		return response

	def restartround(self):
		response = self.send_packet(["mapList.restartRound"])
		return response

	def nextmap(self):
		response = self.send_packet(["mapList.runNextRound"])
		return response

	def shutdown(self):
		response = self.send_packet(["admin.shutDown"])
		return response

	def matchplayer(self, player):
		playerlist = self.listplayer()
		#del playerlist[0:13] #removes header values

		return playerlist
