# =============================================================
# Imports
# =============================================================

import abc
import logging
import configparser

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

    def __init__(self):
        """
        This sets the default values within the context of the
        class.
        :return:
        """

        # Set default containers.
        self.__logger = configparser.ConfigParser()
        self.__configs = dict()
        self.__filename = ""
        return