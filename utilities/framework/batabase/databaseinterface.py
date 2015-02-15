
# =============================================================
# Imports
# =============================================================

import time
import logging

from subprocess import call, Popen
from pprintpp import pprint
from pymongo import MongoClient

from databasesingleton import DatabaseSingleton

# =============================================================
# Constants
# =============================================================

SERVERLOG = 'log/serverlog.log'

# =============================================================
# Source
# =============================================================


@DatabaseSingleton
class DatabaseInterface(object):
    """
    This is the definition of the loaded database.
    In this class we define the structure of the database and
    the structure of the elements of which we put within the database.

    We also keep track of how big each database is and how many configs
    there are within that database.

    Indexes:
        - {config : collection}

    Configs:
        - { _id : config
            ...
            }
    """

    # The constants
    HOME = 'home-configs'
    INDEXES = 'config-indexes'
    ATTACK = 'attack-configs'
    FAVORITE = 'favorite-config'
    ANALYSIS = 'analysis-configs'

    # Databases to house our configs
    __collections = {
        "home-configs" : None,
        "attack-configs" : None,
        "favorite-config" : None,
        "analysis-configs" : None,
        "config-indexes" : None,
    }

    # This is the internal connection reference
    __connection = None

    # The database handle
    __database = None

    # The logger
    __logger = None

    # Server handle
    __handle = None

    def __init__(self):
        """
        This is the default constructor, nothing is done here.
        :return:
        """
        return

    def setup_interface(self, data, log_level=logging.INFO):
        """
        This is the initial setup for the class.
        We use this constructor to set the connection.
        We also read the database storing the tables and their sizes.

        :param data:      the data file
        :return:
        """

        self.__logger = logging.getLogger("ESXiController - DatabaseInterface")
        self.__logger.setLevel(log_level)
        self.__logger.info("Starting the mongdb daemon.")

        # Start the server
        call(['killall', 'mongod'])
        log = open(SERVERLOG, 'w')
        self.__handle = Popen(['mongod', '--dbpath', '%s' % data], stdout=log)

        self.__logger.info("The mongdb daemon started.")

        # Wait for server to start
        time.sleep(2)

        # Set the internal reference
        self.__connection = MongoClient()
        self.__logger.info("Connected to the localhost server.")


        # Set the database name
        self.__database = self.__connection['esxiControllerConfigs']
        self.__logger.info("Added a database: esxiControllerConfigs")


        # Add the collections
        for item in self.__collections.keys():
            self.__collections[item] = self.__database.create_collection(item)
            self.__logger.info("Added a collection: " + item)
        return

    def get_collection(self, collection):
        """
        This gets the handle to a table.

        :param collection:   the collection to write to
        :return:
        """
        return self.__collections[collection]

    def get_db(self):
        """
        Gets the db handle
        :return:
        """
        return self.__database

    def get_connection(self):
        """
        Returns to connection to the mongodb

        :return:
        """
        return self.__connection

    def check_collection_integrity(self, collection):
        """
        This method checks the validity of a collection passed.

        :param collection:   the collection to test
        :return:
        """
        return self.get_db().validate_collection(collection)

    def set(self, config, collection=None, dictionary=None):
        """
        This is the method that sets an object to a collection.

        :param config:       the configs name
        :param dictionary:   the object to set
        :param collection:   the collection to set the object to.
        :return:
        """
        if collection == DatabaseInterface.FAVORITE:
            self.__logger.info("Setting favorite config to: " + config)
            return self.get_collection(collection).update({'$set':{'favorite': config}})

        elif self.filter(collection, config):
            self.__logger.info("The name < %s > already exists, choose another." % config)
            return None
        else:
            # Set the internal name
            dictionary['_id'] = config

            # Add the title in the indexes collection
            self.get_collection(DatabaseInterface.INDEXES).insert(config)
            return self.get_collection(collection).insert(dictionary)

    def remove(self, collection, config=None):
        """
        This is the method that removes a dict instance from
        the collection.

        :param config:        the config to match
        :param collection:    the collection to address
        :return:
        """

        # if we remove the config only
        if config is not None:
            self.__logger.info("Removing config: " + config)

            # Remove from index
            self.get_collection(DatabaseInterface.INDEXES).remove(config)
            return self.get_collection(collection).remove({'name' : config})

        # if we need to remove a collection
        else:
            self.__logger.info("Removing collection: " + collection)
            return self.get_db().drop_collection(collection)


    def get_collection_stats(self, collection):
        """
        This method gets the collection statistics.

        :param collection:  the collection to get the stats from
        :return:
        """
        return pprint(self.get_db().command('collstats', collection))

    def get_all_records(self, collection):
        """
        This method returns the records stored within the collection
        specified.

        :param collection:     the collection to search
        :return:
        """
        return self.get_collection(collection).find()

    def get_all_collections(self):
        """
        This method gets all the collections in the database.

        :return:
        """
        return self.get_db().collection_names()

    def get_database_stats(self):
        """
        This is the method that gets the database statistics.

        :return:
        """
        return pprint(self.get_db().command('dbstats', 'esxiControllerConfigs'))

    def filter(self, collection, config):
        """
        This method filters the collection for a specific config.

        :param collection:     the collection to filter through
        :param config:         the config to look for
        :return:
        """
        return self.get_collection(collection).find_one({'_id' : config})