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

from helpers import ConfigHandler
from helpers import LoggHandler
from games.battlefield import BF4Handler

logg = None

def main(configfile="", logslocation="", serverfolder="", serverfile="", debug=False):
    # Logs
    ########################################################################
    runningpath = os.path.dirname(__file__)
    logdir = "" # Will be used as an argument to the handlers (so they know were to put logs)
    threads = []    #array were we store all threads

    # If log directory is not set, then just create logs were py-rcon is running
    ########################################################################
    if debug == True:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    if logslocation == "":
        logg = LoggHandler.setup_logger('py-rcon', '{}/logs/{}.log'.format(os.getcwd(), 'py-rcon'), loglevel)
    else:
        logdir = '{}\\py-rcon.log'.format(logslocation)
        logg = LoggHandler.setup_logger('py-rcon', '{}/logs/{}.log'.format(logdir, 'py-rcon'), loglevel)
    ########################################################################

    logg.info("Starting up py-rcon...")
    logg.debug("Debug has been activated!")
    logg.info("---------------------------")

    # Read server config/s
    ########################################################################
    if configfile == "" and serverfolder == "" or serverfile == "":  #Nothing is specified, GO DEFAULT!
        #ADD CHECKS FOR: create file if not exsists, if exsist try to parse it!
        logg.debug("No arguments given, goes for default settings")
        settings = ConfigHandler.getSection('{}/config.ini'.format(os.getcwd()), 'py-rcon', logg)
    elif configfile != "":  #configfile is given, tries to load it
        logg.debug("Configfile found, tries to load it")
        settings = ConfigHandler.getSection('{}', logg)
    else:
        logg.warn("Unable to figure out what to do, report this problem with error 22")

    # Single server file, with possible multiple server configs
    ###########################################
    #if serverfile isset, then tries to load it
    if settings != "":
        try:
            sections = ConfigHandler.getAllSections(settings["serverfile"], logg)
            logg.debug("Loaded serverfile: {}".format(settings["serverfile"]))

            if sections:
                # Tries to load all server configs inside config-file
                for sect in sections:
                    if sect.lower().startswith("server"):   # To make sure it only loads server configs
                        s = ConfigHandler.getSection(settings["serverfile"], sect, logg)

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
                logg.info("Unable to find anything in serverfile")
        except Exception as ex:
            logg.error("Unable to load serverfile: {}".format(settings["serverfile"]))
            logg.error("Error: {}".format(ex))
    else:
        logg.debug("There is no serverfile specified")
    ###########################################

    # Multiple server files, with only one server config per file
    ###########################################
    if settings != "":
        try:
            cfgFiles = ConfigHandler.findAllConfigs(settings["serverfolder"])

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
            logg.error("Unable to load serverfiles in folder: {}".format(settings["serverfolder"]))
    else:
        logg.debug("There is no serverfolder specified")

    ###########################################

    # Start each thread
    ########################################################################
    for t in threads:
    	t.daemon = True
    	t.start()
    ########################################################################

    # Run program, and wait for crash or user interupt (Ctrl + C)
    ########################################################################
    try:
    	while True:
    		time.sleep(1)
    except KeyboardInterrupt:
    	sys.exit('Ctrl^C received - exiting!')
    ########################################################################


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Py-rcon v0.9 by Rocketblast 2014, a mini-framework for handling connections 
        to different types of gameservers.''') #come up with a better description...
    parser.add_argument('-c', '--config', metavar='file', type=argparse.FileType('r'), 
        help='''configuration file for py-rcon, if non given then log, server or server directory must be specified. 
        Example: main.py -l C:\logs -sf C:\configs''')
    parser.add_argument('-l', '--log', metavar='folder', help='Location were your log files will be stored')
    parser.add_argument('-sf', '--serverfile', metavar='file', type=argparse.FileType('r'),
        help='Location of the single server configuration file (multiple server configs in one file')
    parser.add_argument('-sd', '--serverdirectory', metavar='folder', 
        help='Path to a directory containing server configuration files')
    parser.add_argument('-d', '--debug', 
        help='If set to true, console will print out more status messages. Can be used for debbuging your plugin')

    args = parser.parse_args()

    if args.config != "" or args.log != "" or serverfile != "" or serverdirectory != "" or debug != None:
        # Tries to check if startup parameters are set, if not just set them to empty string or False
        config = json.load(args.config) if args.config != None else ""
        log = json.load(args.log) if args.log != None else ""
        serverfile = json.load(args.serverfile) if args.serverfile != None else ""
        serverdirectory = json.load(args.serverdirectory) if args.serverdirectory != None else ""
        debug = bool(args.debug) if bool(args.debug) == True else False
        
        main(config, log, serverfile, serverdirectory, debug)
    else:
        main()