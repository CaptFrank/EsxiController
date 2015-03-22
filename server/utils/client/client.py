"""

    client.py
    ==========

    This module is the web interface socket interface to the
    backend engine server.

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
import snakemq
import logging
import threading

import snakemq.link
import snakemq.message
import snakemq.messaging
import snakemq.packeter
from snakemq.message import FLAG_PERSISTENT


"""
=============================================
Constants
=============================================
"""

CLIENT_TITLE                    = 'CONTROLLER_CLIENT'
SERVER_TITLE                    = 'CONTROLLER_SERVER'

LOCALHOST                       = ''
DB_PATH                         = 'db/controllerClient.db'

CLIENT_PORT                     = 9999


class client(threading.Thread):
    """
    This is the client facing socket that is used to
    pass data back and forth between both decoupled entities
    of the application.

    extends: Thread
    """

    # ====================
    # Configs

    # The internal logger
    __logger                            = None

    # log level
    __log_level                         = logging.INFO

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

    # Messenger
    __messenger                         = None

    def __init__(self, log_level=logging.INFO):
        """
        The default constructor for the class
        """

        # Override the threading class
        threading.Thread.__init__(self)

        # Logger
        self.__logger = logging.getLogger("ESXiController - client")
        self.__logger.setLevel(log_level)
        self.__log_level = log_level

        # Init the snake mq logger
        snakemq.init_logging(self.__logger)
        return

    def setup(self, app):
        """
        This sets up the client proxy.
        """

        # Setup the sakemq engine
        self.__logger.info("Creating a snakemq interface")
        self.__link = snakemq.link.Link()
        self.__packeter = snakemq.packeter.Packeter(self.__link)
        self.__messenger = snakemq.messaging.Messaging(CLIENT_TITLE,
                                                       LOCALHOST,
                                                       self.__packeter)

        self.__logger.info("Adding connector")
        self.__link.add_connector((LOCALHOST, CLIENT_PORT))
        self.__logger.info("Created client port on localhost:" + str(CLIENT_PORT))

        app.client = self
        self.__logger.info("Setup complete")
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



    def send_config(self, configs):
        """
        Sends the configs to the server.

        :param configs:
        :return:
        """

        message = snakemq.message.Message(configs,
                                          ttl = 600,
                                          flags = FLAG_PERSISTENT)
        self.__messenger.send_message(SERVER_TITLE, message)
        return
