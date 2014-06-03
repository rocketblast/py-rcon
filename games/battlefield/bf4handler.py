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
from transportlayer import BFRCON

class BF4Handler(BaseHandler):
    def __init__(self, servertype, name, ip, port, password, plugins=[]):
        self.logName = 'bf4-{}'.format(name.strip())
        BaseHandler.__init__(self, servertype, name, ip, port, password, plugins)
        self.rcon = BFRCON(ip, port, password, self.log)

    def run(self):
        if self.rcon.connect():
            self.log.info('[{}:{}] <{}> - is Connected'.format(self.serverIp, self.serverPort, self.serverName))

            self.rcon.login()
            self.rcon.admin_eventsenabled(True)

            #loads all given plugins
            if self.serverPlugins:
                self.load_plugins()

            while True:
                data = self.rcon.receive_packet()
                event = data[0]

                # Only prints out received data when in DEBUG
                self.log.debug('{}'.format(data))   

                for plugin in self.serverLoadedPlugins:
                    try:
                        self.events(plugin, event, data)
                    except Exception as ex:
                        self.log.warn('Unable to handle plugin: {}, with error: {}'.format(plugin, ex))
                        pass

            #if you get here something might got wrong or the connection was beautifully disconnected
            self.rcon.logout()
            self.rcon.disconnect()
            self.log.info('[{}:{}] Disconnected from server'.format(self.serverIp, self.serverPort))
        else:
            self.log.error('[{}:{}] <{}> - Unable to establish a connection'.format(self.serverIp, self.serverPort, self.serverName))

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

    def load_plugins(self):
        for plugin in self.serverPlugins:
            try:
                mod = __import__('plugins.{}.{}'.format(self.serverType, plugin), fromlist=[str(plugin)])
                nclass = getattr(mod, str(plugin))
                self.serverLoadedPlugins.append(nclass(self.rcon, self.log))   #Keep track on this, might need to change it
            except Exception as ex:
                self.log.error('Unable to load plugin: {} from path: plugins.{}.{}'.format(plugin, self.serverType, plugin)) 
                self.log.error(ex)
        self.log.info('Loaded all plugins for this server')
