
# =============================================================
# Imports
# =============================================================

import os
import logging

from vmconfigbase import VmConfigBase
from ConfigParser import ConfigParser
from utilities.framework.database.databaseinterface import *

# =============================================================
# Source
# =============================================================


class VmConfigDatabase(VmConfigBase):
    """
    This is a glorified configuration file writer.
    We use this class to handle the writing of the configurations to a file.
    This could be to edit or to save guard.
    """

    # Database object
    __db_object = None

    # The log level
    __log_level = None

    # The current config
    __current_config = None

    # The configs
    __configs = None


    def __init__(self, data, log_level=logging.INFO):
        """
        This is the default constructor for the class.

        :param data:        the datafile that will contain the db data
        :return:
        """

        self.__logger = logging.getLogger("ESXiController - VmConfigDatabase")
        self.__logger.setLevel(log_level)
        self.__logger.info("Connecting to the mongoDB instance.")

        # We connect to the database
        DatabaseInterface.instance().setup_interface(data, log_level)

        # We get the configs
        self.__logger.info("Reading the saved configurations...")
        self.__configs = list(DatabaseInterface.instance().get_all_records(INDEXES))
        return

    def load_configs(self, config=None, collection=None):
        """
        This is the load method for the configuration.

        :return:
        """

        # We pass the collection title to the database interface
        # and we receive the configs. We store them in the internal
        # context of this class for future.

        if (config is not None) and (collection is not None):

            self.__logger.info("Getting config: %s from collection: %s" % (config, collection))
            self.__db_object = self.get_configs(config, collection)
            if self.__db_object is None:

                # Means its a file config
                # Read it,
                configs = self.read_file_configs(config)

                # store it
                self.__logger.info("New config load request....")
                self.__logger.info("Saving the new config...")
                self.save_configs(configs, collection)

                # We get the configs again to store internally
                self.__db_object = self.get_configs(config, collection)

            # print
            self.print_configs()
            self.__logger.info("Favorite set to: %s"  % self.__db_object['id'])
            self.set_current(config)
            return self.__db_object
        else:
            self.__logger.info("Cannot get configs...")
            return self.__db_object

    def get_configs(self, config=None, collection=None):
        """
        This is the load method for the configuration.

        :return:
        """
        if (config is not None) and (collection is not None):
            return DatabaseInterface.instance().filter(collection, config)
        else:
            self.__logger.info("No valid collection of config...")
            return None

    def save_configs(self, config=None, collection=None):
        """
        This method saves the configs

        :return:
        """

        if (config is not None) and (collection is not None):

            # Set a reference
            res = DatabaseInterface.instance().set(config['attributes']['name'],
                                             collection, config)
            if res:
                self.__logger.info("Created a new entry: %s in collection: %s" % (config['attributes']['name'],
                                                                                    collection))
            else:
                self.__logger.info("Duplicate entry...")
        else:
            self.__logger.info("No valid collection of config...")
            return None

    def delete_configs(self, collection, config=None):
        """
        This method saves the configs

        :param config:      the config to delete
        :return:
        """
        if config is not None:
            self.__logger.info("Removing config: %s from collection: %s" % (config, collection))
            DatabaseInterface.instance().remove(collection, config)
            DatabaseInterface.instance().remove(INDEXES, config)

        else:
            self.__logger.info("Removing collection: %s" % collection)
            DatabaseInterface.instance().remove(collection)

    def set_favorite(self, config=None):
        """
        This sets the config passed to be the favorite.

        :return:
        """

        # Set current config
        if config is not None:
            self.set_current(config)

        if self.__current_config is not None:
            DatabaseInterface.instance().set(config, FAVORITE)
            self.__logger.info("Set the favorite to: %s" % self.__current_config['name'])
        else:
            self.__logger.error("You must select a current config to set as favorite.")
        return

    def set_current(self, config):
        """
        This is the method that sets the current config

        :param config:      The config by name
        :return:
        """

        # Set the config by name
        if config is not None:
            for item in self.__configs:
                if config in item.values():
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
            pprint(self.__db_object)
            return

        # We print in table format
        self.__logger.info("Printing out formatted settings: ")
        for item_key, item_value in zip(self.__db_object.keys(),
                                        self.__db_object.values()):

            if (item_key != 'id') and (item_key != '_id'):

                log = "\n ========================================================== \n"
                log += "[+] name:" .ljust(20, ' ') + "%s\n" % item_key
                for item in item_value:
                    log += ("[+] %s" % item).ljust(20, ' ') + "%s\n" % item_value[item]
                log += "\n ========================================================== \n"
                self.__logger.info(log)

    def print_all_configs(self):
        """
        This method prints the configs that are available with their links

        :return:
        """
        # We print in table format
        self.__logger.info("Printing out formatted settings: ")

        possible = DatabaseInterface.instance().get_all_records(INDEXES)
        log = "\n ========================================================== \n"
        for item in possible:
            log += "[+] {name: collection}:" .ljust(20, ' ') + "%s\n" % item
        log += "\n ========================================================== \n"
        self.__logger.info(log)
        return

    def diff_configs(self, config1, collection1, config2=None, collection2=None):
        """
        This is a wrapper around the system vimdiff command.
        We use this to diff the 2 configs and check what was changed.

        :param config1:       the first file to diff
        :param collection1:   the collection that the config is in
        :param config2:       the second file to diff
        :param collection2:   the collection that the config is in
        :return:
        """
        temp1 = temp2 = None

        self.__logger.info("Calling the diff tool with: %s <-> %s", config1, config2)

        # load configs
        # check if valid config and collection
        if (config1 in self.__configs.keyes())\
                and (collection1 in DatabaseInterface.instance().get_all_collections()):
            temp1 = self.get_configs(config1, collection1)

        # check if there is a specific config we diff to
        if (config2 is not None) \
            and (collection2 is not None):
                if (config1 in self.__configs.keyes())\
                    and (collection1 in DatabaseInterface.instance().get_all_collections()):
                    temp2 = self.get_configs(config2, collection2)
        else:
            temp2 = DatabaseInterface.instance().get_configs(self.__current_config,
                                                             self.__configs[self.__current_config])

        diff(temp1, temp2)
        return

    @staticmethod
    def get_db_handle():
        """
        Returns the internal db object

        :return:
        """

        return DatabaseInterface.instance()

    @staticmethod
    def filter(collection, config):
        """
        This method filters the collection for a specific config.

        :param collection:     the collection to filter through
        :param config:         the config to look for
        :return:
        """
        return DatabaseInterface.instance().filter(collection, config)

    def read_file_configs(self, file):
        """
        This method reads the configurations that are in the configuration
        file saved internally.

        :return:
        """

        # Container
        configs = {}

        # Read the configs
        parser = ConfigParser()
        parser.read(file)
        self.__logger.info("Read the config file: %s", file)

        # Get file stats
        stats = os.stat(file)

        # Print file stats
        self.__logger.info("File size:      %i\n" % stats.st_size)

        # Get the items in the sections
        for section in parser.sections():

            # Read sections and report
            configs[section] = dict((key, value)
                                           for key, value in parser.items(section))
            self.__logger.info("Section read: %s" % section)
        return configs

    @staticmethod
    def get_available_configs():
        """
        This gets the available configs.

        :return:
        """
        return list(DatabaseInterface.instance().get_all_records(INDEXES))

    @staticmethod
    def get_collections():
        """
        This returns the collections

        :return:
        """
        return DatabaseInterface.instance().get_all_collections()
