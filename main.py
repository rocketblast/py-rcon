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

def main(logs=""):
    # Logs
    ########################################################################
    runningpath = os.path.dirname(__file__)
    logdir = "" # Will be used as an argument to the handlers (so they know were to put logs)
    threads = []    #array were we store all threads

    # If log directory is not set, then just create logs were py-rcon is running
    if logs == "":
        logdir = '{}\\logs\\py-rcon.log'.format(runningpath)
        logg = LoggHandler.setup_logger('py-rcon', r'{}'.format(logdir))
    else:
        logdir = '{}\\py-rcon.log'.format(logs)
        logg = LoggHandler.setup_logger('py-rcon', r'{}'.format(logdir))
    ########################################################################

    # Read server config/s
    ########################################################################
    settings = ConfigHandler.getSection('{}\config.ini'.format(runningpath), 'py-rcon')

    # Single server file, with possible multiple server configs
    ###########################################
    #if serverfile isset, then tries to load it
    if settings["serverfile"] != "":
        try:
            sections = ConfigHandler.getAllSections(settings["serverfile"], logg)
            logg.info("Loaded serverfile")

            if sections:
                # Tries to load all server configs inside config-file
                for sect in sections:
                    if sect.startswith("Server"):   # To make sure it only loads server configs
                        s = ConfigHandler.getSection(settings["serverfile"], sect, logg)

                        # Checks for supported gameserver types
                        if s["game"] == "battlefield4":
                            t = BF4Handler('battlefield4', s["name"], s["ip"], int(s["port"]), s["password"], plugins=s["plugins"].split(' '))
                            threads.append(t)
                            logg.info('[{}:{}] <{}> - Added server to list'.format(s["ip"], s["port"], s["name"]))
                        elif s["game"] == "battlefield3":
                            print "Found Battlefield 3 game"
                        else:
                            logg.info('Game name: {} is not supported'.format(s["name"]))
            else:
                logg.info("Unable to find anything in serverfile")
        except Exception as ex:
            logg.info("Unable to load serverfile: {}".format(settings["serverfile"]))
    else:
        logg.info("There is no serverfile specified")
    ###########################################

    # Multiple server files, with only one server config per file
    ###########################################
    if settings["serverfolder"] != "":
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
                        logg.info("Game name: {} is not supported".format(s["name"]))
        except Exception as ex:
            logg.info("Unable to load serverfiles in folder: {}".format(settings["serverfolder"]))
    else:
        logg.info("There is no serverfolder specified")

    ###########################################
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
    parser = argparse.ArgumentParser(description="Py-rcon v1.0 by Rocketblast")
    parser.add_argument('-c', '--config', metavar='file', type=argparse.FileType('r'), 
        help='Configuration file')

    args = parser.parse_args()

    if args.config != None:
        config = json.load(args.config)
        main("", config)
    else:
        main()