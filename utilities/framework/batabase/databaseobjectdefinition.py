
# =============================================================
# Imports
# =============================================================


# =============================================================
# Source
# =============================================================


class DatabaseObjectDefinition(object):
    """
    This is the definition of the loaded database.
    In this class we define the structure of the database and
    the structure of the elements of which we put within the database.

    We also keep track of how big each database is and how many configs
    there are within that database.
    """

    # This is the database machine object definition
    # Each item is originally set to None.
    __db_config = []

    def __init__(self):
        return

    def create_object(self, configs):
        """
        This method takes in a config object and creates a database object.

        :param configs:         the configs object
        :return:
        """

        return