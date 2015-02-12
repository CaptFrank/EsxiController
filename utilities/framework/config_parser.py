
# =============================================================
# Imports
# =============================================================

import os
import logging
import configparser

# =============================================================
# Source
# =============================================================

class config_parser(object):
    """
    This is the configuration parser for the the framework.
    It uses the configparser class to read the sections of the
    configuration file.
    """

    # The configs
    __configs                   = dict()

    # The filename
    __filename                  = ""

    # The config parser
    __parser                    = None

    # The internal logger
    __logger                    = None

    def __init__(self, filename, logLevel = logging.INFO):
        """
        This is the default constructor for the class.

        :param filename:    The filename of the configurations
        :param logLevel:    The log level
        :return:
        """

        # Set the internal handle
        self.__filename         = filename
        self.__parser           = configparser.ConfigParser()
        self.__logger           = logging.getLogger("ESXiController - config_parser")

        # Log the setup
        self.__logger.setLevel(logLevel)
        self.__logger.info("Created a config parser object.")
        return

    def read_configs(self):
        """
        This method reads the configurations that are in the configuration
        file saved internally.

        :return:
        """

        # Read the configs
        self.__parser.read(self.__filename)
        self.__logger.info("Read the config file: %s", self.__filename)

        # Get file stats
        stats = os.stat(self.__filename)

        # Print file stats
        self.__logger.info("File size:      %i\n" %stats.st_size)
        return

    def get_configs(self):
        """
        This is the method which gets the configs and writes them into
        a dictionary.

        :return:
        """

        # Get the items in the sections
        for section in self.__parser.sections():
            self.__configs[section] = self.__parser.items(section)
        return

    def print_configs(self):
        """
        This method prints the loaded configs in a table form.

        :return:
        """

        return

if __name__ == "__main__":

    parser = config_parser("../malware/configurations/malware_template.conf")
    parser.read_configs()
    parser.get_configs()
    parser.print_configs()