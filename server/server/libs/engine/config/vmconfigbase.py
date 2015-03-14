
# =============================================================
# Imports
# =============================================================

from pprintpp import pprint
from abc import abstractmethod

# =============================================================
# Source
# =============================================================


class VmConfigBase(object):
    """
    This is the vm configuration base class that is inherited
    with all the used methods of importing and exporting configs

    Indexes:
        - {
            name        : <name>,
            collection  : <collection>,
            }
    """

    # The configs
    __configs = None

    # The config parser
    __parser = None

    # The internal logger
    __logger = None

    # The log level
    __log_level = None

    # The current config
    __current_config = None

    @abstractmethod
    def load_configs(self, config=None):
        """
        This is the load method for the configuration.

        :return:
        """
        raise NotImplemented

    @abstractmethod
    def save_configs(self, config=None):
        """
        This method saves the configs

        :return:
        """
        raise NotImplemented

    @abstractmethod
    def delete_configs(self, config):
        """
        This method saves the configs

        :param config:      the config to delete
        :return:
        """
        raise NotImplemented

    def update_configs(self):
        """
        This edits the config that is in the context of the
        config class.

        :return:
        """
        raise NotImplemented

    @abstractmethod
    def set_favorite(self, config=None):
        """
        This sets the config passed to be the favorite.

        :return:
        """
        raise NotImplemented

    @abstractmethod
    def set_current(self, config):
        """
        This is the method that sets the current config

        :param config:      The config by name
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def print_configs(self, json=False):
        """
        This method prints the loaded configs in a table form.

        :return:
        """
        raise NotImplemented

    @abstractmethod
    def print_all_configs(self):
        """
        This method prints the configs that are available with their links

        :return:
        """
        raise NotImplemented

    @abstractmethod
    def diff_configs(self, file1, file2):
        """
        This is a wrapper around the system vimdiff command.
        We use this to diff the 2 configs and check what was changed.

        :param file1:       the first file to diff
        :param file2:       the second file to diff
        :return:
        """
        raise NotImplemented