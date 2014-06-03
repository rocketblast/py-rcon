# -*- coding: utf-8 -*-

# File: basehandler.py
# Description: Base class for gamehandlers

import os
import socket
import threading
import importlib

from helpers import LoggHandler
from sockethandler import SocketHandler

class BaseHandler(threading.Thread):
    def __init__(self, servertype, name, ip, port, password, plugins):
        threading.Thread.__init__(self)

        self.serverType = servertype
        self.serverName = name
        self.serverIp = ip
        self.serverPort = port
        self.serverPassword = password
        self.serverPlugins = plugins
        self.serverLoadedPlugins = list()

        #self.logName = 'bf4-{}'.format(name)
        self.log = LoggHandler.setup_logger(self.logName, '{}/logs/servers/{}.log'.format(os.getcwd(), self.logName))
        self.log.info('[{}:{}] <{}> - Setup is ready'.format(ip, port, name))

    def load_plugins(self):
        for plugin in self.serverPlugins:
            try:
                mod = __import__('plugins.{}.{}'.format(self.serverType, plugin), fromlist=[str(plugin)])
                nclass = getattr(mod, str(plugin))
                self.serverLoadedPlugins.append(nclass())   #Keep track on this, might need to change it
            except Exception as ex:
                self.log.error('Unable to load plugin: {} from path: plugins.{}.{}'.format(plugin, self.serverType, plugin)) 
                self.log.error(ex)
        self.log.info('Loaded all plugins for this server')
