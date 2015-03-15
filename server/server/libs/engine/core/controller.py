# =============================================================
# Imports
# =============================================================

import ast
import logging
import ConfigParser

from server.server.libs.engine.core.connection import connection
from server.server.libs.engine.core.networkstager import networkStager

# =============================================================
# Source
# =============================================================


class controller(object):
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

    # ====================
    # Handles

    # The config parser
    __parser                            = None

    # The vm connection
    __vm_connection                     = None

    # Database handle
    __db_handle                         = None

    # Stage
    __stage                             = None

    def __init__(self, host_config, log_level=logging.INFO):
        """
        This sets the default values within the context of the
        class.

        Create a vm connection.
        Setup the configurations

        :param host_config:        the host config file
        :return:
        """

        # Logger
        self.__logger = logging.getLogger("ESXiController - esxiControllerBase")
        self.__logger.setLevel(log_level)
        self.__log_level = log_level

        # Configs
        self.__logger.info("Reading the host configurations.")
        self.__parser = ConfigParser.ConfigParser()
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

        return

    def setup(self, config):
        """
        This is the setup method for the class
        The input is in the form of a dict{} where the structure is
        the following:

            config = {}

        :param config:              the config struct to load
        :return:
        """

        # We set the configs to teh internal reference
        self.__configs = config


        # Create a network stager
        self.__logger.info("Creating a network stager.")
        self.__stage = networkStager(self.__vm_connection,
                                     self.__email_dest,
                                     self.__log_level)
        self.__logger.info("Setup complete")
        return


    def start(self):
        """
        This is the start method.
        :return:
        """
        self.__logger.info("Starting stage...")
        self.__stage.add_stage_task(self.__configs,
                                    self.__configs['attributes']['name'])
        return

    def stop(self):
        """
        This is stops the stage
        :return:
        """
        self.__logger.info("Stopping stage...")
        self.__stage.kill_task(self.__configs['attributes']['name'])
        return

