# =============================================================
# Imports
# =============================================================

import time
import threading

from __init__ import DictDiffer as diff
from server.server.utils.notification.notificationdispatch import *


# =============================================================
# Source
# =============================================================

class stageTask(threading.Thread):
    """
    This is the stage task definition. This is the
    class that handles the direct interactions between
    the ESXI server and the ESXI controller framework.
    """

    # The connection handle
    __handle                            = None

    # The config to act upon
    __config                            = None

    # The vm list
    __vm_list                           = list()

    # The kill flag
    __alive                             = True

    # Status
    __status                            = dict()

    # Dispatch
    __dispatch                          = None


    def __init__(self, connection, configurations, log_level=logging.INFO):
        """
        This is the default constructor for the class.

        :param connection:          the server connection object
        :param configurations:      the configurations object
        :return:
        """

        # Building thread
        threading.Thread.__init__(self)

        self.__logger = logging.getLogger("ESXiController - VmStageTask")
        self.__logger.setLevel(log_level)

        # Set the internal handles to the connection and config
        self.__handle = connection
        self.__config = configurations

        # Setup the dispatch
        self.__dispatch = notificationDispatch()

        # Get the vms
        self.__get_vms()
        return

    def run(self):
        """
        The worker method for the thread.

        :return:
        """

        try:
            # Start the stage
            self.__start_stage()

        except Exception, e:
            # Send a notification that the stage is done
            self.__dispatch.send_notification(self.__config['destinations'],
                                          'error',
                                          '%s staging incomplete!!!\n'
                                          'Error: %s' % (self.__config['configurations']['name'],
                                          e),
                                          self.__config['configurations']
                                          )

        # Send a notification that the stage is done
        self.__dispatch.send_notification(self.__config['destinations'],
                                          'complete',
                                          '%s staging complete!!!' % self.__config['configurations']['name'],
                                          self.__config['configurations']
                                          )

        # Store current statues
        self.__status = self.__get_status()

        # Continue task until the task is killed
        while self.__alive:

            # we sleep
            time.sleep(10)

            # Monitor -- vm status
            temp = self.__get_status()

            # We diff the 2 dicts
            changed = diff(self.__status, temp)

            # Print change
            for change in changed.changed():
                self.__logger.info("Vm %s changed status to %s" % (change, temp[change]))

                # Set original
                self.__status[change] = temp[change]

        # We kill the stage
        self.__stop_stage()
        self.join()

        # Successfully killed the task
        self.__logger.info("Successfully killed the task thread.")
        return True

    def kill_task(self):
        """
        This sets the kill flag to false
        :return:
        """
        self.__alive = False
        return

    def __start_stage(self):
        """
        This method takes the connection instance and the configuration
        and starts the network stage process.

        There are 3 major actions that we can do to setup the network
            - Start
            - Stop
            - Reboot

        :return:
        """

        self.__logger.info('Powering the machines on the config.')
        # Start the tasks
        self.__power_on()
        return

    def __stop_stage(self):
        """
        This method takes the connection instance and the configuration
        and stops the network stage process.

        :return:
        """

        self.__logger.info('Resetting the machines on the config.')
        # Stop the tasks
        self.__power_off()
        return

    def __get_vms(self):
        """
        We retrieve the vms by their names

        :return:
        """

        # Only get the active machines
        for vm in self.__config['configurations']:
            if vm['Active']:
                self.__vm_list.append(self.__handle.get_vm_by_name(vm['Name']))
                self.__logger.info(self.__handle.get_properties())
        return

    def __power_on(self):
        """
        This powers on the configuration vms.

        :return:
        """

        for vm in self.__vm_list:

            self.__revert_snapshot(vm, self.__config[vm.name]['Snapshot'])

            # Reset if already running
            if vm.is_powered_on():
                self.__logger.info("Resetting machine: " + vm.name)
                self.__task = vm.reset(sync_run=True)
                self.__check_operation()

            else:
                self.__logger.info("Powering machine: " + vm.name)
                self.__task = vm.power_on(sync_run=True)
                self.__check_operation()
        return

    def __power_off(self):
        """
        This powers off the configuration vms.

        :return:
        """

        for vm in self.__vm_list:

            if self.__config[vm.name]['Backup']:
                self.__create_snapshot(vm)

            if vm.is_powered_on():
                self.__logger.info("Shutting down machine: " + vm.name)
                self.__task = vm.suspend(sync_run=False)
                self.__check_operation()

            else:
                self.__logger.info("Machine already shutdown !!!: " + vm.name)
        return

    def __revert_snapshot(self, vm, snapshot):
        """
        Revert to the specified snapshot.

        :param vm:              the vm instance
        :param snapshot:        the snapshot name
        :return:
        """

        self.__logger.info("Revert to: " + snapshot)
        self.__task = vm.revert_to_named_snapshot(snapshot, sync_run=False)
        self.__check_operation()
        return

    def __create_snapshot(self, vm):
        """
        Create the specified snapshot.

        :param vm:              the vm instance
        :return:
        """

        name = vm.name + "Analysis-" + time.strftime('%y-%m-%d %H:%M:%S')
        self.__logger.info("Creating: " + name)
        self.__task = vm.create_snapshot(name, sync_run=False)
        self.__check_operation()
        return

    def __get_status(self):
        """
        This returns the status of all vms in a dict.

        :return:
        """

        # Status
        status = dict()

        # Get the status
        for vm in self.__vm_list:
            status[vm.name] = vm.get_status()
        return status

    def __check_operation(self):
        """
        This checks the operations.
        :return:
        """

        try:
            status = self.__task.wait_for_state(['running', 'error'], timeout=10)
            if status == 'error':
                self.__logger.error("Error powering on: " + self.__task.get_error_message())
            else:
                self.__logger.info("Successfully powered on machine.")
        except Exception:
            self.__logger.error("Timeout !")
        return