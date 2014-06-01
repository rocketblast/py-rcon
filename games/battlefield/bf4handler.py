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
from frostbite import Battlefield4
#from plugins.battlefield.ingame_admin.py import 

#runningpath = os.getcwd()

class BF4Handler(BaseHandler):
    def __init__(self, name, ip, port, password, plugins=[], **kwargs):

        self.logName = 'bf4-{}'.format(name.strip())
        BaseHandler.__init__(self, name, ip, port, password, plugins, Battlefield4, **kwargs)

    def run(self):
        if self.connect():
            self.log.info('Connected [{}:{}] <{}>'.format(self.serverIp, self.serverPort, self.serverName))
            print(self.rcon.login(self.serverPassword))
            print(self.rcon.getEvents(True))
            while self.connected():
                data = self.rcon.receive_event()
                print(data)
                self.log.debug('Got event: {} with data: {}'.format(data[0], data))


            #load plugins for this instance
        else:
            self.log.error('Unable to establish a connection to [{}:{}] <{}>'.format(self.serverIp, self.serverPort, self.serverName))

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