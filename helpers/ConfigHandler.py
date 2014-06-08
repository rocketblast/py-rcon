# -*- coding: utf-8 -*-

# File: EventHandler.py
# Description: This class handles how config files should be read and returns wanted data from it

import os
import ConfigParser

class ConfigHandler:
    """ There will be some awesome comments here later on...i hope..."""

    @staticmethod
    def findAllConfigs(path, log=None):
        cfgs = []

        # Loops through the folder and finds all ini-files
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".ini"):
                    cfgs.append('{}{}'.format(path, file))

        return cfgs

    @staticmethod
    def getAllSections(file, log=None):
        Config = ConfigParser.ConfigParser()
        try:
            Config.read(file)
            sections = Config.sections()
            return sections
        except Exception as ex:
            log.error("Unable to read sections, error: {}".format(ex))

    @staticmethod
    def getSection(file, section, log=None):
        Config = ConfigParser.ConfigParser()
        try:
            Config.read(file)

            if Config.has_section(section):
                dict_sections = {}
                options = Config.options(section)
                for option in options:
                    try:
                        #fetches any section matching given argument
                        dict_sections[option] = Config.get(section, option)
                        #if dict_sections[option] == -1:
                            # Do some debbuging stuff here later on
                    except Exception as e:
                        print("There's a freakin exception in your confighandler!")
                        print("Here's the error: %s" % e)
                        dict_sections[option] = None	#nulls the object, just in case

                return dict_sections
            else:
                log.error("Found no section: {} in file: {}".format(section, file))
                return ""
        except Exception as ex:
            log.error("Unable to load serverfile from: {}".format(file))

    @staticmethod
    def getConfig(file, log=None):
        Config = ConfigParser.ConfigParser()
        Config.read(file)	#might need a try'n catch here...

        dict_config = {}
        try:
            dict_config = Config._sections
        except Exception as e:
            print("There is a scary exception reading your entire configfile!")
            print("Here's the error: %s" % e)
            dict_config = None	#nulls the object, just in case

        return dict_config
