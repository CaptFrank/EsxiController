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
import logging
import threading

from retask import *

"""
=============================================
Constants
=============================================
"""


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
    __queue                              = None

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
        return

    def setup(self, app):
        """
        This sets up the client proxy.
        """

        # Setup the sakemq engine
        self.__logger.info("Creating a task queue interface")

        self.__queue = Queue('esxicontroller')
        self.__queue.connect()

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
        self.__queue.enqueue(Task(configs))
        self.__logger.info("Added a new task to the task queue.")
        return
