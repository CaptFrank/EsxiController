# =============================================================
# Imports
# =============================================================

import ast
import time
import json
import logging
import threading

from configparser import ConfigParser
from server.server.utils.engine.core.connection import connection
from server.server.utils.engine.core.networkstager import networkStager

import snakemq.link
import snakemq.message
import snakemq.messaging
import snakemq.packeter
from snakemq.message import FLAG_PERSISTENT
from snakemq.storage.sqlite import SqliteQueuesStorage


# =============================================================
# Constants
# =============================================================

SERVER_TITLE                            = 'CONTROLLER_SERVER'
LOCALHOST                               = ''
DB_PATH                                 = 'db/controllerServer.db'

CLIENT_PORT                             = 9999

# =============================================================
# Source
# =============================================================


class controller(threading.Thread):
    """
    This is the base class for the esxi controllers.
    It houses the base logger, filename, parser and configs.
    We also include some utility methods within this context.
    """

    # ====================
    # Configs

    # The host settings
    __host_configs                      = dict()

    # The email address to send the notifications
    __email_dest                        = list()

    # The configs
    __configs                           = dict()

    # The internal logger
    __logger                            = None

    # log level
    __log_level                         = logging.INFO

    # =======================
    # Handles

    # The config parser
    __parser                            = None

    # The vm connection
    __vm_connection                     = None

    # Database handle
    __db_handle                         = None

    # Stage
    __stage                             = None

    # =======================
    # Process attributes

    # The alive bool
    __alive                             = True

    # =======================
    # External communication

    # Communication context
    __snake                             = None

    # Packeter
    __packeter                          = None

    # Link
    __link                              = None

    # Message Storage
    __storage                           = None

    # Messenger
    __messenger                         = None

    def __init__(self, host_config, log_level=logging.INFO):
        """
        This sets the default values within the context of the
        class.

        Create a vm connection.
        Setup the configurations

        :param host_config:        the host config file
        :return:
        """

        # Threading override
        threading.Thread.__init__(self)

        # Logger
        self.__logger = logging.getLogger("ESXiController - controller")
        self.__logger.setLevel(log_level)
        self.__log_level = log_level

        # Init the snake mq logger
        snakemq.init_logging(self.__logger)

        # Configs
        self.__logger.info("Reading the host configurations.")
        self.__parser = ConfigParser()
        self.__parser.read(host_config)

        # Get the handles
        self.__host_configs['host'] = self.__parser.get('host', 'host')
        self.__host_configs['user'] = self.__parser.get('host', 'user')
        self.__host_configs['password'] = self.__parser.get('host', 'password')
        self.__host_configs['data'] = self.__parser.get('host', 'data')

        # Get the emails to notify
        self.__email_dest = ast.literal_eval(self.__parser.get('client', 'email_notifications'))

        # Connect to the host
        self.__logger.info("Connecting to host...")
        self.__vm_connection = connection(host=self.__host_configs['host'],
                                          user=self.__host_configs['user'],
                                          password=self.__host_configs['password'])
        return

    def run(self):
        """
        The default run method for the thread.
        All we do in this method is call upon the
        idle method to idle the main context until killed

        :return:
        """

        self.idle()
        return


    def idle(self):
        """
        This is the main loop for the app that is called upon in the
        top level main context.

        :return:
        """

        while self.__alive:
            self.__link.loop()
            try:
                time.sleep(1)
            except (KeyboardInterrupt, SystemExit):
                self.__logger.info("Killing app based on user input...")
                exit(0)
        return

    def setup(self):
        """
        This is the setup method for the class
        :return:
        """

        # Create a network stager
        self.__logger.info("Creating a network stager.")
        self.__stage = networkStager(self.__vm_connection,
                                     self.__email_dest,
                                     self.__log_level)

        # Setup the sakemq engine
        self.__logger.info("Creating a snakemq interface")
        self.__link = snakemq.link.Link()
        self.__packeter = snakemq.packeter.Packeter(self.__link)
        self.__storage = SqliteQueuesStorage(DB_PATH)
        self.__messenger = snakemq.messaging.Messaging(SERVER_TITLE,
                                                       LOCALHOST,
                                                       self.__packeter,
                                                       self.__storage)

        self.__logger.info("Adding listener")
        self.__link.add_listener((LOCALHOST, CLIENT_PORT))
        self.__logger.info("Created server port on localhost:" + str(CLIENT_PORT))

        self.__messenger.on_message_recv.add(self.on_receive)
        self.__messenger.on_connect.add(self.on_connect)
        self.__messenger.on_disconnect.add(self.on_disconnect)
        self.__messenger.on_message_drop.add(self.on_message_drop)
        self.__messenger.on_error.add(self.on_error)
        self.__logger.info("Setup complete")
        return

    def on_receive(self, conn, ident, message):
        """
        We receive a packet message

        The message should be in the form of json dictionary

        :param conn:                    The connection
        :param ident:                   The identity
        :param message:                 The message
        :return:
        """

        # Get the config
        config = json.loads(message)

        # Check for nulity
        if config is not None:
            self.start_task(config)

        return

    def on_connect(self, conn, ident, message):
        """
        We receive a packet message

        :param conn:                    The connection
        :param ident:                   The identity
        :param message:                 The message
        :return:
        """
        self.__logger.info("Connected to: " + ident + " through: " + conn)
        return

    def on_disconnect(self, conn, ident, message):
        """
        We receive a packet message

        :param conn:                    The connection
        :param ident:                   The identity
        :param message:                 The message
        :return:
        """
        self.__logger.info("Disconnected from: " + ident + " through: " + conn)
        self.__alive = False
        return

    def on_message_drop(self, conn, ident, message):
        """
        We receive a packet message

        :param conn:                    The connection
        :param ident:                   The identity
        :param message:                 The message
        :return:
        """
        self.__logger.error("Messaging engine reported a message drop")
        return

    def on_error(self, conn, ident, message):
        """
        We receive a packet message

        :param conn:                    The connection
        :param ident:                   The identity
        :param message:                 The message
        :return:
        """
        self.__logger.error("Messaging engine error!")
        return

    def start_task(self, config):
        """
        This is the start method.

        The input is in the form of a dict{} where the structure is
        the following:

            config = {}

        :param config:              the config struct to load
        :return:
        """
        self.__logger.info("Starting stage...")
        self.__stage.add_stage_task(config,
                                    config['attributes']['name'])
        return

    def stop_task(self, config):
        """
        This is stops the stage
        :return:
        """
        self.__logger.info("Stopping stage...")
        self.__stage.kill_task(config['attributes']['name'])
        return

