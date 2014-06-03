# -*- coding: utf-8 -*-

# File: main.py
# Description: Main file for starting up py-rcon

import ConfigParser
import time
import sys, os
import logging

from helpers import ConfigHandler
from helpers import LoggHandler
from games.battlefield import BF4Handler

logg = None

def main():
    runningpath = os.path.dirname(__file__)
    logg = LoggHandler.setup_logger('py-rcon', r'{}/logs/py-rcon.log'.format(runningpath))
    #logg.info('py-rcon is starting up!')

    threads = []
    t = BF4Handler('battlefield', 'testserver', '188.126.64.33', 47200, 'password', plugins=['ingame_admin'])
    threads.append(t)

    for t in threads:
    	t.daemon = True
    	t.start()
    
    try:
    	while True:
    		time.sleep(1)
    except KeyboardInterrupt:
    	sys.exit('Ctrl^C received - exiting!')
if __name__ == '__main__':
    main()