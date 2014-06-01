# -*- coding: utf-8 -*-

# File: EventHandler.py
# Description: This file contains a basic static class for logging events through the application

import os
import sys
import logging
import logging.handlers

class LoggHandler(object):
    """
        Example how you can use this class would be something like this:
        LoggHandler.setup_logger('log1', r'C:\logs\log1.log')
        log1 = logging.getLogger('log1')
        log1.info('logger is now working...')
        log1.critical('all your base belong to us!...')
    """

    logger = None

    @staticmethod
    def setup_logger(logger_name, log_file, level=logging.INFO):
        #if directory does not exsists, then just create it
        path = log_file.rsplit('/', 1)[0] #removes filename for log, e.g /example/example.log into /example/
        if not os.path.exists(path):
            os.makedirs(path)

        LoggHandler.logger = logging.getLogger(logger_name)
        formatter = logging.Formatter(fmt='[%(asctime)s] (%(levelname)s) - %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')

        #by default it runs a rotating filehandler for looping through log files
        filehandler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 100, backupCount=20)
        filehandler.setFormatter(formatter)

        #basically for printing out messages to the console it self
        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(formatter)

        LoggHandler.logger.setLevel(level)
        LoggHandler.logger.addHandler(filehandler)
        LoggHandler.logger.addHandler(streamhandler)

        return LoggHandler.logger