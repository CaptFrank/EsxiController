
# =============================================================
# Imports
# =============================================================

import time
import atexit
import logging
import pysphere
import logging

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

    # The config to act upon
    __config = None

    # Vm list
    __vm_list = []

    # Task list
    __task = None

    # Logger
    __logger = None

    def __init__(self, configuration, connection, log_level=logging.INFO):
        """
        This is the default constructor to the class

        :param configuration:   the config dict
        :param connection:      the connection to the vcenter instance
        :return:
        """

        self.__logger = logging.getLogger("ESXiController - VmNetworkStager")
        self.__logger.setLevel(log_level)

        # Set the internal handles to the connection and config
        self.__handle = connection
        self.__config = configuration

        self.__logger.info("Getting all the vm properties.")

        # Get the vms
        self.__get_vms()
        return

    def start_stage(self):
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

    def stop_stage(self):
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
        for vm in self.__config:
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

            self.__revert_snapshot(vm, self.__config['vm.name']['Snapshot'])

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

            self.__create_snapshot(vm, self.__config['vm.name']['Snapshot'])

            if vm.is_powered_on():
                self.__logger.info("Shutting down machine: " + vm.name)
                self.__task = vm.power_off(sync_run=True)
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
        self.__task = vm.revert_to_named_snapshot(snapshot, sync_run=True)
        self.__check_operation()
        return

    def __create_snapshot(self, vm, snapshot):
        """
        Create the specified snapshot.

        :param vm:              the vm instance
        :param snapshot:        the snapshot name
        :return:
        """

        self.__logger.info("Creating: " + vm.name + "Analysis-" + time.strftime('%d-%m-%y'))
        self.__task = vm.create_snapshot(snapshot, sync_run=True)
        self.__check_operation()
        return

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
        except:
            self.__logger.error("Timeout !")
        return
