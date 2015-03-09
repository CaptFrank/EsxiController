
# =============================================================
# Imports
# =============================================================

import time
import thread
import Queue
import logging

from utilities.framework.core.vmstagetask import VmStageTask

# =============================================================
# Source
# =============================================================


class VmNetworkStager(object):
    """
    This class is the network configuration stager.
    It is responsible to start a config and turn on the requisite
    machines.

    It is also the class that handles the interactions to the libvirt
    module.
    """

    # The connection handle
    __handle = None

    # Logger
    __logger = None

    # The task server
    __server = None

    # The kill flag
    __alive = True

    # Task list
    __task_list = {}

    # The task queue
    __task_queue = Queue.Queue()

    # Destinations to email
    __destinations = []

    def __init__(self, connection, destinations, log_level=logging.INFO):
        """
        This is the default constructor to the class
        :param connection:      the connection to the vcenter instance
        :param destinations:    the destinations to email.
        :return:
        """

        self.__logger = logging.getLogger("ESXiController - VmNetworkStager")
        self.__logger.setLevel(log_level)

        # Set the internal handles to the connection and config
        self.__handle = connection
        self.__destinations = destinations

        # Create a server thread
        self.__server = thread.start_new(self.task_server, (self.__task_queue,
                                                            self.__handle))
        self.__logger.info("Created a new task server thread.")
        return

    def add_stage_task(self, configuration, name):
        """
        Here we add a task to the task queue.

        :param configuration:   the configurations to start
        :param name:            the name of the task
        :return:
        """

        # We add the configuration and name to a task object
        task = {
            'configurations': configuration,
            'name': name,
            'destinations': self.__destinations
        }

        # We then add it to our task queue to get it executed
        if not self.__task_queue.full():
            self.__task_queue.put(task, block=True)
            self.__task_queue.task_done()
            self.__logger.info("Added a new task with name {name} to the task queue.".format(name=name))
        else:
            self.__logger.info("Cannot add task... Task queue is full.")
        return

    def delete_stage_task(self):
        """
        This deletes an arbitrary task from the task list and returns it.

        :return:
        """

        # If the task queue is empty we return None
        task = None

        if not self.__task_queue.empty():
            task = self.__task_queue.get(block=True)
            self.__task_queue.task_done()
            self.__logger.info("Deleted task with name {name} from the task queue.".format(name=task['name']))
        else:
            self.__logger.info("Cannot add task... Task queue is empty.")
        return task

    def task_server(self, queue, connection):
        """
        This is the main task server method. This is the task server
        thread worker method.

        :param queue:               the queue to address
        :param connection:          the connection to use
        :return:
        """

        # Loop until killed
        while self.__alive:

            # We create a new vmstagetask
            if not queue.empty():

                # We get a stage reference
                task_config = queue.get()

                # Create a stage object
                stage = VmStageTask(connection, task_config)

                # We start it
                stage.start()

                # Add the task to the list
                self.__task_list[task_config['name']] = stage

            time.sleep(5)
        self.__logger.info("Server thread not alive... Returning")
        return

    def kill_task(self, name):
        """
        Here we take a name and kill that task.

        :param name:                the task name to kill
        :return:
        """

        # We kill the task specified
        self.__logger.info("Attempting to kill the task <{nam}>.".format(name=name))
        self.__task_list[name].kill_task()
        return

    def kill_server(self):
        """
        This kills the task server.
        :return:
        """
        self.__alive = False
        return






