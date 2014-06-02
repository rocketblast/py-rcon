import os
import socket
import threading
import importlib

from helpers import LoggHandler

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
        self.socket = None

        #self.logName = 'bf4-{}'.format(name)
        self.log = LoggHandler.setup_logger(self.logName, '{}/logs/servers/{}.log'.format(os.getcwd(), self.logName))
        self.log.info('Setup is ready for [{}:{}] - {}'.format(ip, port, name))

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(1)
            self.socket.connect((self.serverIp, self.serverPort))
            self.socket.setblocking(1)
            
            return True
        except socket.error as err:
            self.log.error('[{}:{}] Unable to connect ({})'.format(self.serverIp, self.serverPort, err))
            return False

    def disconnect(self):
        if self.socket:
            self.socket.close()
        self.socket = None

    def load_plugins(self):
        for plugin in self.serverPlugins:
            try:
                #__import__('plugins.{}.{}'.format(str(self.serverType), str(plugin)))
                #importlib.import_module('plugins.{}.{}'.format(self.serverType, plugin))
                #module = self.load_class('plugins.{}.{}'.format(str(self.serverType), str(plugin)))
                mod = __import__('plugins.{}.{}'.format(self.serverType, plugin), fromlist=[str(plugin)])
                nclass = getattr(mod, str(plugin))
                self.serverLoadedPlugins.append(nclass)   #Keep track on this, might need to change it
            except Exception as ex:
                self.log.error('Unable to load plugin: {} from path: plugins.{}.{}'.format(plugin, self.serverType, plugin)) 
                self.log.error(ex)
        self.log.info('Loaded all plugins for this server')
