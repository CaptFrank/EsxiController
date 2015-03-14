"""

    db.py
    ==========

    This module is the database interface module. It handles
    all the interactions with the mongodb database.

    :copyright: (c) 2015 by GammaRay.
    :license: BSD, see LICENSE for more details.

    Author:         GammaRay
    Version:        1.0
    Date:           3/11/2015

"""

"""
=============================================
Imports
=============================================
"""

import time
import logging
from subprocess import call, Popen

from datetime import datetime
from server.server.db.dbsingleton import *
from flask_mongokit import MongoKit, Document, Connection

"""
=============================================
Constant
=============================================
"""

SERVERLOG = '/var/log/esxicontroller/serverlog.log'

"""
=============================================
Source
=============================================
"""

@DatabaseSingleton
class VmStagerDatabase(object):
    """
    This is the stager database class that interfaces,
    the app with the APIs that are used to connect to
    the mongdb instance.
    """

    # Mongo db connection instance.
    __mongodb           = None

    # The connection
    __connection        = None

    # The configs for the mongodb
    __configs           = None

    # The logger
    __logger            = None

    def __init__(self, configs, data_path, log_level=logging.INFO):
        """
        This is the default constructor for the class.
        We use this API to start the mongodb  connection.

        configs = {
                'app': <the app to reference>,
                'db': <the database name to connect>,
                'host': <the host to connect to>,
                'port': <the port to connect to>,
                'user': <the user name to conenct>,
                'pass': <the password>,
                }

        :param configs:             the configs to use to connect
        :param data_path:           the data path to use for data.
        :param log_level:           the logging level for the logger.
        :return:
        """

        self.__logger = logging.getLogger("ESXiController - DatabaseInterface")
        self.__logger.setLevel(log_level)
        self.__logger.info("Starting the mongdb daemon.")

        # Start the server
        call(['killall', 'mongod'])
        log = open(SERVERLOG, 'w')
        self.__handle = Popen(['mongod', '--dbpath', '%s' % data_path], stdout=log)

        self.__logger.info("The mongdb daemon started.")

        # Wait for server to start
        time.sleep(2)

        # Init the mongo kit.
        self.__mongodb = MongoKit().init_app(self.__configs['app'])
        return

    def connect(self):
        """
        This connects the database and sets a handle internally.

        :return:
        """
        self.__connection = Connection()
        return

    def disconnect(self):
        """
        This disconnects the database and sets a handle internally.

        :return:
        """
        self.__connection.disconnect()
        return

    def register(self, tables):
        """
        This registers the tables within the mongodb database.

        tables = []

        :return:
        """
        self.__connection.register(tables)
        return

