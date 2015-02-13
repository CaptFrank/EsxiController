
# =============================================================
# Imports
# =============================================================

from pprintpp import pprint
from pymongo import MongoClient

# =============================================================
# Source
# =============================================================


class DatabaseInterface(object):
    """
    This is the definition of the loaded database.
    In this class we define the structure of the database and
    the structure of the elements of which we put within the database.

    We also keep track of how big each database is and how many configs
    there are within that database.
    """

    # The constants
    ATTACK = 'attack-configs'
    ANALYSIS = 'analysis-configs'

    # Databases to house our configs
    __collections = {
        "attack-configs" : None,
        "analysis-configs" : None
    }

    # This is the dict that will store the
    # config handles and their size.
    __handle = dict()

    # This is the internal connection reference
    __connection = None

    # The database handle
    __database = None

    def __init__(self, config):
        """
        This is the initial constructor for the class.
        We use this constructor to set the connection.
        We also read the database storing the tables and their sizes.

        :param config:      the config file that has the attributes
        :return:
        """

        # Set the internal reference
        self.__connection = MongoClient()

        # Set the database name
        self.__database = self.__connection['esxiControllerConfigs']

        # Add the collections
        for item in self.__collections.keys():
            self.__collections[item] = self.__database.create_collection(item)
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

    def set(self, config, dictionary, collection):
        """
        This is the method that sets an object to a collection.

        :param config:       the configs name
        :param dictionary:   the object to set
        :param collection:   the collection to set the object to.
        :return:
        """
        if self.filter(collection, config):
            return None
        else:
            return self.get_collection(collection).insert(dictionary)

    def remove(self, config, collection):
        """
        This is the method that removes a dict instance from
        the collection.

        :param config:        the config to match
        :param collection:    the collection to address
        :return:
        """
        return self.get_collection(collection).remove({'name' : config})


    def get_collection_stats(self, collection):
        """
        This method gets the collection statistics.

        :param collection:  the collection to get the stats from
        :return:
        """
        return pprint(self.get_db().command('collstats', collection))

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

        return self.get_collection(collection).find_one({'name' : config})