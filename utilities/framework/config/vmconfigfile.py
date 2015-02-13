
# =============================================================
# Imports
# =============================================================

import os
import ast
import time
import shutil
import logging

from pprintpp import pprint
from subprocess import call
from configparser import ConfigParser
from vmconfigbase import VmConfigBase

# =============================================================
# Constants
# =============================================================

CONFIGURATION_STORE = 'configurations/configurations.conf'

# =============================================================
# Source
# =============================================================


class VmConfigFile(VmConfigBase):
    """
    This is the configuration parser for the the framework.
    It uses the configparser class to read the sections of the
    configuration file.

    It extends the esxicontrollerbase class.
    """

    # The possible configs
    __possible = None

    # The favorite config
    __favorite = None

    # The configs
    __configs = None

    # The filename
    __filename = ""

    # The config parser
    __parser = None

    # The talbe
    __table = None

    # The internal logger
    __logger = None

    # The current config
    __current_config = None

    def __init__(self, filename=None, log_level=logging.INFO):
        """
        This is the default constructor for the class.

        :param filename:    The filename of the configurations
        :param log_level:    The log level
        :return:
        """

        # Set the internal handle
        self.__configs = dict()
        self.__filename = filename
        self.__parser = ConfigParser()
        self.__table = ConfigParser()
        self.__logger = logging.getLogger("ESXiController - VmConfigFile")

        # log the setup
        self.__logger.setLevel(log_level)
        self.__logger.info("Created a config parser object.")

        # We read the possible configs
        self.__logger.info("Reading table of configurations.")
        self.__table.read(CONFIGURATION_STORE)

        # Load the possible configs
        self.__possible = \
            ast.literal_eval(self.__table.get('configurations', 'configurations'))

        self.__logger.info("Loaded the possible configurations.")
        self.print_all_configs()

        # Find the favorite
        self.__favorite = self.__table.get('favorite', 'favorite')
        self.__logger.info("Current favorite set to: %s", self.__favorite)
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
        self.__logger.info("File size:      %i\n" % stats.st_size)

        # Get the items in the sections
        for section in self.__parser.sections():

            # Read sections and report
            self.__configs[section] = dict((key, value)
                                           for key, value in self.__parser.items(section))
            self.__logger.info("Section read: %s" % section)
        return

    def save_configs(self):
        """
        This saves the configs to the store folder.

        Assuming the current config is not set, need to do:
            - Add config struct to the possible struct
            - Set that attribute to the config

        :return:
        """

        if self.__current_config is None:
            self.__logger.error("A current config must be loaded in order to save it.")
            return

        # Set a new config
        config = dict()
        config['created'] = time.strftime('%m/%d/%y')
        config['location'] = 'configurations/' + os.path.basename(self.__filename)

        # We add it the the list of possible configs
        self.__possible[self.__configs['attributes']['name']] = config
        self.__logger.info("Added a possible config to the config database.")

        self.__table.set('configurations', 'configurations', str(self.__possible))

        self.write_file()
        self.__logger.info("Saved the config in the conguration table.")

        # Here all we are doing is taking a config file and putting it in the
        # Store folder. (./configurations)
        shutil.move(self.__filename, 'configurations/' + os.path.basename(self.__filename))
        self.__logger.info("Moved the config file to the data store.")
        return

    def delete_configs(self, config):
        """
        This method deletes a passed config

        :param config:      the config to delete
        :return:
        """

        # Remove the dict instance
        # Set the config by name
        if config is not None:
            if config in self.__possible.keys():

                # delete the file
                # We only hide the file for now...
                shutil.move(self.__possible[config]['location'], 'configurations/'
                            + "." + os.path.basename(self.__possible[config]['location']))

                del self.__possible[config]
                self.__table.set('configurations', 'configurations', str(self.__possible))
                self.write_file()

                self.__logger.info("Deleted the config %s" % config)

                # Check if they were favorite
                if self.__favorite == config:
                    self.set_favorite('default')

            else:
                self.__logger.error("Not a valid config title. <%s>" % config)

        # write the conf
        self.write_file()


        return

    def set_favorite(self, config=None):
        """
        This method sets the configuration to being the
        favorite config.

        :return:
        """

        # Set current config
        if config is not None:
            self.set_current(config)

        if self.__current_config is not None:
            self.__table.set('favorite', 'favorite', self.__current_config)

            self.write_file()
            self.__logger.info("Set the favorite to: %s" % self.__current_config)
        else:
            self.__logger.error("You must select a current config to set as favorite.")
        return

    def edit_configs(self):
        """
        This is basic wrapper around the system call for nano.

        :return:
        """

        # Call nano
        call(['vim', self.__filename])
        return

    def load_configs(self, config=None, filename=None, favorite=False):
        """
        This is the method which gets the configs and writes them into
        a dictionary.

        :param config:          the config name to load
        :param filename:        the config filename to load
        :param favorite:        the favorite bool

        :return:
        """

        # Load the favorite config
        if favorite:
            filename = self.__possible[self.__favorite]['location']
            self.__current_config = self.__favorite

        # Set the config by name
        if config is not None:
            if config in self.__possible.keys():
                filename = self.__possible[config]['location']
                self.__current_config = config
            else:
                self.__logger.error("Not a valid config title.")

        # Set the config by path
        if filename is not None:
            self.__filename = filename

        # Read the configs
        self.read_configs()
        return

    def set_current(self, config):
        """
        This is the method that sets the current config

        :param config:      The config by name
        :return:
        """

        # Set the config by name
        if config is not None:
            if config in self.__possible.keys():
                self.__current_config = config
                self.__logger.info("Set current config to: %s" % config)
            else:
                self.__logger.error("Not a valid config title. <%s>" % config)
        return

    def print_configs(self, json=False):
        """
        This method prints the loaded configs in a table form.

        :return:
        """

        # Do we print in json format??
        if json:

            # Get the json text
            self.__logger.info("Printing out JSON formatted settings: ")
            pprint(self.__configs)
            return

        # We print in table format
        self.__logger.info("Printing out formatted settings: ")
        for item_key, item_value in zip(self.__configs.keys(),
                                        self.__configs.values()):

            log = "\n ============================ \n"
            log += "[+] name:" .ljust(20, ' ') + "%s\n" % item_key
            for item in item_value:
                log += ("[+] %s" % item).ljust(20, ' ') + "%s\n" % item_value[item]
            log += " ============================ "
            self.__logger.info(log)
        return

    def print_all_configs(self):
        """
        This method prints the configs that are available with their links

        :return:
        """

        for item_key, item_value in zip(self.__possible.keys(),
                                        self.__possible.values()):
            log = "\n ============================ \n"
            log += "[+] name:" .ljust(20, ' ') + "%s\n" % item_key
            log += "[+] created:" .ljust(20, ' ') + "%s\n" % item_value['created']
            log += "[+] location:" .ljust(20, ' ') + "%s\n" % item_value['location']
            log += " ============================ "
            self.__logger.info(log)
        return

    def diff_configs(self, file1, file2=None):
        """
        This is a wrapper around the system vimdiff command.
        We use this to diff the 2 configs and check what was changed.

        :param file1:       the first file to diff
        :param file2:       the second file to diff
        :return:
        """

        self.__logger.info("Calling the diff tool with: %s <-> %s", file1, file2)

        # Set the file1
        if file2 is None:
            file2 = self.__filename

        # Call the command
        call(['vimdiff', file1, file2])
        return

    def write_file(self):
        """
        This writes to the configuration file.
        :return:
        """

        file = open(CONFIGURATION_STORE, "w+")
        self.__table.write(file)
        return