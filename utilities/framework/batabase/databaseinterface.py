
# =============================================================
# Imports
# =============================================================


# =============================================================
# Source
# =============================================================


class DatabaseInterface(object):
    """
    This is the definition of the loaded database.
    In this class we define the structure of the database and
    the structure of the elements of which we put within the database.

    We also keep track of how big each database is and how many configs
    there are within that database.
    """

    # This is the dict that will store the
    # config handles and their size.
    __handle = dict()

    # This is the internal connection reference
    __connection = None

    def __init__(self, connection):
        """
        This is the initial constructor for the class.
        We use this constructor to set the connection.
        We also read the database storing the tables and their sizes.

        :param connection:      the connection to the database
        :return:
        """

        # Set the internal reference
        self.__connection = connection

        # Read the configs in the database
        self.__read()
        return

    def __read(self):

        return

    def create(self):

        return

    def delete(self):

        return

    def print_stats(self):

        return