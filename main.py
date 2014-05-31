# -*- coding: utf-8 -*-

# File: main.py
# Description: Main file for starting up py-rcon

import ConfigParser
import time
import sys, os
import logging

from helpers import ConfigHandler
from helpers.EventHandler import LoggHandler

logg = None

def main():
	runningpath = os.path.dirname(__file__)
	LoggHandler.setup_logger('py-rcon', r'{}/logs/py-rcon.log'.format(runningpath))
	logg = logging.getLogger('py-rcon')

	logg.info('py-rcon is starting up!')

if __name__ == '__main__':
	main()