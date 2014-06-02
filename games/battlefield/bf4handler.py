# -*- coding: utf-8 -*-

# File: bf4-handler.py
# Description: Contains basic connection to a battlefield 4 server

import logging
import os
import socket
import sys
import threading

from helpers import LoggHandler
from games import BaseHandler
from frostbite import Frostbite

class BF4Handler(BaseHandler):
    def __init__(self, servertype, name, ip, port, password, plugins=[]):
        self.logName = 'bf4-{}'.format(name.strip())
        BaseHandler.__init__(self, servertype, name, ip, port, password, plugins)

    def run(self):
        if self.connect():
            self.log.info('Connected [{}:{}] <{}>'.format(self.serverIp, self.serverPort, self.serverName))

            if self.serverPlugins:
                self.load_plugins()

            self.rcon_login()
            self.admin_eventsenabled(True)

            while True:
                data = self.receive_packet()
                event = data[0]

                # Only prints out received data when in DEBUG
                self.log.debug('{}'.format(data))   

                for plugin in self.serverLoadedPlugins:
                    try:
                        print event
                        self.events(plugin, event, data)
                    except Exception as ex:
                        self.log.warn('Unable to handle plugin: {}, with error: {}'.format(plugin, ex))
                        pass

            #if you get here something might got wrong or the connection was beautifully disconnected
            self.rcon_logout()
            self.disconnected()
            self.log.info('[{}:{}] Disconnected from server'.format(self.serverIp, self.serverPort))

            #load plugins for this instance
        else:
            self.log.error('Unable to establish a connection to [{}:{}] <{}>'.format(self.serverIp, self.serverPort, self.serverName))

    def events(self, plugin, event, data):
        #print "Event: {}  data: {}".format(event, data)
        evts = {
            #player events
            'player.on_authenticated': plugin.on_authenticated,
            'player.onJoin': plugin.on_join,
            'player.onLeave': plugin.on_leave,
            'player.onSpawn': plugin.on_spawn,
            'player.onKill': plugin.on_kill,
            'player.onChat': plugin.on_chat,
            'player.onConnect': plugin.on_connect,
            'player.onsquadchange': plugin.on_squadchange,
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

    def receive_packet(self, socket=None, receiveBuffer=""):
        if socket == None:
            receiveBuffer = ""
            while not Frostbite.containsCompletePacket(receiveBuffer):
                receiveBuffer += self.socket.recv(4096)

            packetSize = Frostbite.DecodeInt32(receiveBuffer[4:8])
            packet = receiveBuffer[0:packetSize]
            receiveBuffer = receiveBuffer[packetSize:len(receiveBuffer)]
            [isFromServer, isResponse, sequence, words] = Frostbite.DecodePacket(packet)

            return words
        elif socket:
            while not Frostbite.containsCompletePacket(receiveBuffer):
                receiveBuffer += self.socket.recv(4096)

            packetSize = Frostbite.DecodeInt32(receiveBuffer[4:8])
            packet = receiveBuffer[0:packetSize]
            receiveBuffer = receiveBuffer[packetSize:len(receiveBuffer)]

            return [packet, receiveBuffer]
        else:
            self.log.error('Unable to handle received packet!')

    def send_packet(self, data):
        receiveBuffer = ""
        getRequest = Frostbite.EncodeClientRequest(data)
        self.socket.send(getRequest)

        [getResponse, receiveBuffer] = self.receive_packet(self.socket, receiveBuffer)
        [isFromServer, isResponse, sequence, words] = Frostbite.DecodePacket(getResponse)

        self.log.debug('[{}:{}] Sending: {}'.format(self.serverIp, self.serverPort, data))

        return words
    
    def rcon_login(self):
        login = self.send_packet(["login.hashed"])
        passwordHash = Frostbite.generatePasswordHash(login[1].decode("hex"), self.serverPassword)
        passwordHashHexString = passwordHash.encode("hex").upper()
        response = self.send_packet(["login.hashed", passwordHashHexString])
        
        if response[0] != "OK":
            self.log.error('[{}:{}] Wrong RCON password. Exiting.'.format(self.serverIp, self.serverPort))
            sys.exit()
        elif response[0] == "OK":
            self.log.info('[{}:{}] is now logged in'.format(self.serverIp, self.serverPort))
        else:
            self.log.warn('Something went wrong, response: {}'.format(response))

        return response

    def rcon_logout(self):
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
