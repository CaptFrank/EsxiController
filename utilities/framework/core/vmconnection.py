
# =============================================================
# Imports
# =============================================================

import atexit
import logging

from pysphere import VIServer

# =============================================================
# Source
# =============================================================

class VmConnection(object):
    """
    This class is the network configuration stager.
    It is responsible to start a config and turn on the requisite
    machines.

    It is also the class that handles the interactions to the libvirt
    module.
    """

    # The libvirt handle
    __handle = None

    # The config to act upon
    __config = None

    # The logger
    __logger = None

    def __init__(self, host, user, password, log_level=logging.INFO):
        """
        This is the default constructor to the class

        :param host:            the esxi host
        :param user:            the user to the esxi server
        :param password:        the password to the esxi host
        :return:
        """

        self.__logger = logging.getLogger("ESXiController - VmConnection")
        self.__logger.setLevel(log_level)

        try:
            # set internal handle
            self.__handle = VIServer()
            self.__handle.connect(host=host,
                                  user=user,
                                  password=password
                                  )
        except IOError, ex:
            self.__logger.info("Connection unsuccessful...")
            exit(1)
            pass

        atexit.register(VIServer.disconnect, self.__handle)

        self.__logger.info("Connection successful...")
        return

    def get_server(self):
        """
        Returns the server instance.

        :return:
        """
        return self.__handle

    def disconnect(self):
        """
        Disconnect from server
        :return:
        """
        self.__handle.disconnect()


