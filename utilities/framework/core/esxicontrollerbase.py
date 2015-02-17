# =============================================================
# Imports
# =============================================================

import abc
import logging
import configparser

from utilities.framework.core.vmconnection import VmConnection
from utilities.framework.core.vmnetworkstager import VmNetworkStager

# =============================================================
# Source
# =============================================================


class EsxiControllerBase(object):
    """
    This is the base class for the esxi controllers.
    It houses the base logger, filename, parser and configs.
    We also include some utility methods within this context.
    """

    # The configs
    __configs = None

    # The filename
    __filename = None

    # The config parser
    __parser = None

    # The internal logger
    __logger = None

    # The vm connection
    __vm_connection = None

    # The network stager
    __stager_handle = None

    # The database
    __database = False

    def __init__(self, file, db=True, log_level=logging.INFO):
        """
        This sets the default values within the context of the
        class.

        Create a vm connection.
        Setup the configurations

        :param file:        the host config file
        :param db:          the bool that toggle the db
        :return:
        """

        # Logger
        self.__logger = logging.getLogger("ESXiController - EsxiControllerBase")
        self.__logger.setLevel(log_level)

        # Configs
        self.__logger.info("Reading the host configuratons.")
        self.__parser = configparser.ConfigParser()
        self.__parser.read(file)

        # Get the handles
        host = self.__parser.get('host', 'host')
        user = self.__parser.get('host', 'user')
        password = self.__parser.get('host', 'password')

        self.__logger.info("Connecting to host...")
        self.__vm_connection = VmConnection(host=host,
                                            user=user,
                                            password=password)

        # Take configs from db
        self.__database = db
        return

    def setup(self, config, config_type, file=True, save=True):
        """
        This is the setup method for the class

        :param config:              the config name to load
        :param config_type:         the config type (collection)
        :param file:                the file bool -- db of file ??
        :param save:                the save bool -- save?
        :return:
        """

        # Get the configs


        return


    def start(self):
        """
        This is the start method.
        :return:
        """

        self.__stager_handle.start_stage()
        return

    def stop(self):
        """
        This is stops the stage
        :return:
        """

        self.__stager_handle.stop_stage()
        return

