import threading
from helpers import LoggHandler
import os
import socket

class BaseHandler(threading.Thread):

    def __init__(self, stype, name, ip, port, password, plugins, communicator, **kwargs):
        threading.Thread.__init__(self, **kwargs)

        self.serverType = stype
        self.serverName = name
        self.serverIp = ip
        self.serverPort = port
        self.serverPassword = password
        self.serverPlugins = plugins
        self.serverLoadedPlugins = list()

        #handle communication with server
        self.communicator = communicator
        self.socket = None

        #self.logName = 'bf4-{}'.format(name)
        self.log = LoggHandler.setup_logger(self.logName, '{}/logs/servers/{}.log'.format(os.getcwd(), self.logName))
        self.log.info('Setup is ready for [{}:{}] - {}'.format(ip, port, name))

    def connect(self):
        self.log.info('[{}:{}] Connecting to server...'.format(self.serverIp, self.serverPort))
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(1)
            self.socket.connect((self.serverIp, self.serverPort))
            self.socket.setblocking(1)
            return True
        except socket.error as err:
            self.log.error('[{}:{}] Unable to connect ({})'.format(self.serverIp, self.serverPort, err))
        return False

    def connected(self):
        if self.socket.recv(4096):
            self.log.debug('Seems like we still are connected, good!')
            return True
        else:
            self.log.error('Hmm, not connected?')
        return False

    def disconnect(self):
        if self.socket:
            self.socket.close()
        self.socket = None

    def load_plugins(self):
        for plugin in self.serverPlugins:
            try:
                __import__('plugins.{}.{}'.format(self.serverType, plugin))
                self.serverLoadedPlugins.append(plugin())   #Keep track on this, might need to change it
            except:
                self.log.error('Unable to load plugin: {}'.format(plugin)) 
        self.log.info('Loaded all plugins for this server')

    @property
    def rcon(self):
        return self.communicator(self.socket, self.log)
