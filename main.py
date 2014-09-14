# -*- coding: utf-8 -*-

# File: main.py
# Description: Main file for starting up py-rcon

import argparse
import ConfigParser
import time
import sys
import os
import logging
import json
import thread
import threading
import time
from Queue import *

from helpers import ConfigHandler
from helpers import LoggHandler
from games.battlefield import BF4Handler

#from websocket.wsserver import WebSocketServer
#from websocket.wsserver import WebSocketHandler, ThreadedWebSocket, WebSocketServer
from websocket.wsserver import CustomTcpServer, WebSocketHandler

logg = None

def main(args):
    # 1. Check for arguments
    # 1.a If non given then go for default values
    # 1.b If -c given, try to open config file
    # 1.c If -l given, try to find folder, if not found create it
    # 1.d If -sf given, try to find folder with config files in it
    # 1.e If -s given, try to open a file with server configuration
    # 1.f If -d given, run program in debug, prints out more messages
    # 2. Handle configuration (default or given arguments)
    # 3. Connect to all servers

    # Logs
    ########################################################################
    logdir = "" # Will be used as an argument to the handlers (so they know were to put logs)
    threads = []    #array were we store all threads
    webthreads = []

    # Check if argument debug isset, if not go for default (INFO)
    ########################################################################
    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    # If argument log isset, then tries to create a log file (and folder) at path
    if args.log:
        logdir = '{}/py-rcon.log'.format(args.log)
        logg = LoggHandler.setup_logger('py-rcon', logdir, loglevel)
    else:
        # If no location for logs has been given, then just go default
        logg = LoggHandler.setup_logger('py-rcon', '{}/logs/{}.log'.format(os.getcwd(), 'py-rcon'), loglevel)
    ########################################################################


    # Read server config/s
    ########################################################################
    if args.config == 'config.ini':
        logg.debug('No arguments given, goes for default settings')
        settings = ConfigHandler.getConfig('{}/{}'.format(os.getcwd(), args.config), logg)
    elif configfile != 'config.ini':  #configfile is given, tries to load it
        logg.debug('Configfile found, tries to load it')
        settings = ConfigHandler.getConfig('{}'.format(args.config), logg)
    else:
        logg.warn('Unable to figure out what to do, report this problem with error 22')
    ########################################################################


    # If debug is given, then print out more messages and information both in console and logfiles
    ########################################################################    
    if args.debug:
        logg.debug("Config has been loaded")
        logg.debug("Starting up py-rcon in debug...")
    else:
        logg.info("Starting up py-rcon...")
    logg.info("---------------------------")
    ########################################################################


    # Single server file, with possible multiple server configs
    ###########################################
    if settings != None: # <--- Might not be needed for the new flow
        logg.debug("Tries to load settings from a single file")
        # if serverfile is passed as an argument, then override anything in the configfile
        # 1. Check if serverfile has been set as an startup argument
        # 2. Check configfile
        #    - For section py-rcon if serverfile has been set in config
        #    - For Section Server for server settings
        # 3. Load server settings OR give message no serverconfig was found
        # 4. Add server settings to the thread queue

        #serverfile = None
        #if args.serverfile != None:
            # If serverfile was given as an startup argument
            #serverfile = args.serverfile
        #elif settings:
            #sections = ConfigHandler.getAllSections(serverfile, logg)
            #if sections:

        serverfile = None
        if args.serverfile != None:
            serverfile = args.serverfile
        elif settings.get('py-rcon', 'serverfile') != "":
            serverfile = settings.get('py-rcon', 'serverfile')
        else:
            serverfile = ""
            logg.debug("Unable to find any value for serverfile")

        if serverfile:
            logg.debug("Serverfile has been set to: {}".format(serverfile))
            sections = ConfigHandler.getAllSections(serverfile, logg)
            #logg.debug("Loaded serverfile: {}".format(settings["serverfile"]))

            if sections:
                # Tries to load all server configs inside config-file
                for sect in sections:
                    if sect.lower().startswith("py-rcon") == False:   # To make sure it only loads server configs
                        s = ConfigHandler.getSection(serverfile, sect, logg)

                        # Checks for supported gameserver types
                        if s["game"] == "battlefield4":
                            t = BF4Handler('battlefield4', s["name"], s["ip"], int(s["port"]), s["password"], plugins=s["plugins"].split(' '))
                            threads.append(t)
                            logg.debug('[{}:{}] <{}> - Added server to list'.format(s["ip"], s["port"], s["name"]))
                        elif s["game"] == "battlefield3":
                            print "Found Battlefield 3 game"
                        else:
                            logg.info('Game name: {} is not supported'.format(s["name"]))
                    else:
                        logg.debug("Unable to find any sections in config file")
            else:
                logg.debug("There is no settings in your config file")
        else:
            logg.debug("Setting serverfile is not set")
    else:
        logg.debug("Settings were None, report this error with code 33")
    ###########################################

    # Multiple server files, with only one server config per file
    ###########################################
    if settings != None:
        logg.debug("Tries to load settings from file/s")
        if args.serverfolder: #if setting isset
            try:
                cfgFiles = ConfigHandler.findAllConfigs(args.serverfolder)
                
                if cfgFiles:    #might need to count number of results
                    for cfg in cfgFiles:    # Foreach file, load config
                        s = ConfigHandler.getSection(cfg, "server")

                        if s["game"] == "battlefield4":
                            t = BF4Handler('battlefield4', s["name"], s["ip"], s["port"], s["password"], plugins=s["plugins"].split(' '))
                            threads.append(t)
                            logg.info('[{}:{}] <{}> - Added server to list'.format(s["ip"], s["port"], s["name"]))
                        elif s["game"] == "battlefield3":
                            print "Found Battlefield 3 game"
                        else:
                            logg.warn("Game name: {} is not supported".format(s["name"]))
            except Exception as ex:
                logg.error("Unable to load serverfiles in folder: {}".format(args.serverfolder))
                logg.error("Error: {}".format(ex))
        else:
            logg.debug("No serverfolder was specified")
    else:
        logg.debug("There is no serverfolder specified")

    ###########################################

    #server = WebSocketServer()
    #server = WebSocketServer(("localhost", 9999), WebSocketHandler)
    HOST = ''
    PORT = 9999
    commandQueue = Queue()
    server = CustomTcpServer((HOST, PORT), WebSocketHandler, commandQueue)
    #threads.append(server)
    webthreads.append(server)

    # Start each thread
    ########################################################################
    for t in threads:
    	t.daemon = True
    	t.start()

    for s in webthreads:
        s.daemon = True
        try:
            s.start()
        except KeyboardInterrupt:
            os._exit()

    #server_thread = threading.Thread(target=server.serve_forever)
    #server_thread.daemon = True
    #server_thread.start()
    #    print s
    ########################################################################


    # Run program, and wait for crash or user interupt (Ctrl + C)
    ########################################################################
    try:
    	while True:
    		time.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()
        logg.info("---------------------------")
    	sys.exit('Ctrl^C received - exiting!')
    ########################################################################


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
        Py-rcon v1.0 by Rocketblast 2014, a mini framework for handling connections to different 
        types of gameservers.
        ''')
    parser.add_argument('-c', '--config', default='config.ini', help='''
        Default configuration file for py-rcon, if none given it tries to open config.ini in the same folder 
        as main.py. If it does not exist then it will create it. Config.ini can contain server configuration 
        as well.
        ''')
    parser.add_argument('-l', '--log', metavar='folder', help='''
        Path to log files, if none given then a default folder will be created inside the same folder as 
        main.py
        ''')
    parser.add_argument('-sf', '--serverfolder', metavar='folder', help='''
        Path to were configuration file/s are located. This should be used when multiple files for 
        configuration is expected. Have no default value.
        ''')
    parser.add_argument('-s', '--serverfile', help='''
        Path to a configuration file for server/s (should be .ini). This should be used when a single 
        file is expected. Have no default value.
        ''')
    parser.add_argument('-d', '--debug', action='store_true', help='''
        Use debug flag to get more information printed out in both console and log files.
        ''')

    args = parser.parse_args()

    try:
        main(args)
    except:
        raise
    raw_input()
