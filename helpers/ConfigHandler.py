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
                    try:
                        cfgs.append('{}{}'.format(path, file))
                        print "SUCCESS"
                    except Exception as ex:
                        log.error("Unable to add setting file: {}".format(file))
                        log.error("Error: {}".format(ex))
        #print "Type: {}".format(type(cfgs))
        return cfgs

    @staticmethod
    def getAllSections(file, log=None):
        Config = ConfigParser.ConfigParser()
        ConfigHandler.ifFile(file, log)
        
        try:
            Config.read(file)

            if Config:
                sections = Config.sections()
                return sections
            else:
                log.debug("No sections was found in config file")
                return None
        except Exception as ex:
            log.error("Unable to read sections, error: {}".format(ex))

    @staticmethod
    def getSection(file, section, log=None):
        Config = ConfigParser.ConfigParser()
        ConfigHandler.ifFile(file, log)

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
                        log.error("Unable to get config section")
                        log.error("Error: {}".format(e))
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
        ConfigHandler.ifFile(file, log)

        try:
            Config.read(file)
        except Exception as e:
            log.error("Unable to read config file")
            log.error("Error: {}".format(e))
            Config = None	#nulls the object, just in case

        # Check if config file does exist
        if Config:
            log.debug("Loaded config: {}".format(file))

            return Config
        else:
            log.debug("Didn't find: {}".format(file))

            return None

    @staticmethod
    def ifFile(filepath, log):
        log.debug("Tries to check if file exists: {}".format(filepath))
        if os.path.exists(filepath):
            log.debug("Config exists at location: {}".format(filepath))
        else:
            log.debug("Config does not exists, tries to create it")
            try:
                f = file(filepath, "w")
                f.write("[py-rcon]\n")
                f.write("plugins:\n")
                f.write("serverfile:\n")
                f.write("serverfolder:\n")
                f.close()

                log.info("Config did not exists, so created it at location: {}".format(filepath))
            except Exception as e:
                log.error("Unable to auto create a configfile at path: {}".format(filepath))
                log.error("With error: {}".format(e))