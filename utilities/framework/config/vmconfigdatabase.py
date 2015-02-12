
# =============================================================
# Imports
# =============================================================

import os
import redis
import logging

from vmconfigbase import VmConfigBase

# =============================================================
# Source
# =============================================================


class VmConfigDatabase(VmConfigBase):
    """
    This is a glorified configuration file writer.
    We use this class to handle the writing of the configurations to a file.
    This could be to edit or to save guard.
    """

    # Database handle
    __handle = None

    # Database address
    __address = None

    # Database port
    __port = None

    def __init__(self):
        """
        This is the default constructor for the class.

        :return:
        """

        return

    def load_configs(self):
        """
        This method loads a specific config for the network.

        :return:
        """
        return

    def save_configs(self):
        """
        This takes the configs and saves them to the configuration database
        :return:
        """

        return

    def edit_configs(self, config):
        """
        This edits the configuration passed.

        :param config:
        :return:
        """
        return

    def set_favorite(self):
        """
        This sets the config passed to be the favorite.

        :return:
        """
        raise NotImplemented

    def print_configs(self, json=False):
        """
        This method prints the loaded configs in a table form.

        :return:
        """
        raise NotImplemented

    def diff_configs(self, file1, file2=None):
        """
        This is a wrapper around the system vimdiff command.
        We use this to diff the 2 configs and check what was changed.

        :param file1:       the first file to diff
        :param file2:       the second file to diff
        :return:
        """
        raise NotImplemented
